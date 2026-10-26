"""Lawful supply-to-consumption accounting with explicit units and shared stocks.

The ledger does not estimate illegal origin. Adjustments are supplied assumptions
or observations; no catchment allocation or tonnes-to-sticks conversion is implicit.
"""
from __future__ import annotations

from dataclasses import dataclass
from numbers import Integral, Real
from typing import Any, Iterable
import math

import numpy as np
from numpy.typing import NDArray

from tobac_supply.longitudinal import aggregate_uniform_years

Array = NDArray[np.float64]
YearsArray = NDArray[np.int64]


def _scalar(value: Real, name: str, minimum: float = 0.) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f'{name} must be numeric, not boolean')
    x = float(value)
    if not math.isfinite(x) or x < minimum:
        raise ValueError(f'{name} must be finite and >= {minimum}')
    return x


def _array(values: Iterable[Real], name: str, length: int, signed: bool = False) -> Array:
    try:
        a = np.array([_scalar(x, name, -math.inf if signed else 0.) for x in values])
    except TypeError as exc:
        raise ValueError(f'{name} must be a sequence') from exc
    if len(a) != length:
        raise ValueError(f'{name} needs {length} values, got {len(a)}')
    return a


def _source_ids(values: tuple[str, ...]) -> tuple[str, ...]:
    """Validate a declared source identity; empty tuple is the unattributed default.

    Rejects non-string elements, blank (after stripping) ids and duplicates. The
    canonical whitespace-stripped form is stored, so two spellings of one source
    cannot declare distinct identities.
    """
    if not isinstance(values, tuple):
        raise ValueError(f'source_ids must be a tuple of strings; got {type(values).__name__}')
    stripped: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f'source_ids must contain strings; got {type(value).__name__} {value!r}')
        cleaned = value.strip()
        if not cleaned:
            raise ValueError('source_ids contains an empty source id; each source id must be '
                             'non-empty after stripping whitespace')
        if cleaned in stripped:
            raise ValueError(f'source_ids contains duplicate source id {cleaned!r}; '
                             'source ids must be unique')
        stripped.append(cleaned)
    return tuple(stripped)


def _observation_years(values: tuple[int, ...]) -> tuple[int, ...]:
    """Validate declared observation years; empty tuple means unattributed years.

    Rejects non-integral values, non-calendar years and duplicates or a
    non-increasing order, so a series cannot be mislabelled with another run's
    observation window.
    """
    if not isinstance(values, tuple):
        raise ValueError(f'observation_years must be a tuple of integer years; '
                         f'got {type(values).__name__}')
    years: list[int] = []
    for value in values:
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
            raise ValueError(f'observation_years must contain integer calendar years; got {value!r}')
        year = int(value)
        if not 1 <= year <= 9998:
            raise ValueError(f'observation_years value {year} is not a calendar year '
                             '(must be 1..9998)')
        years.append(year)
    for previous, current in zip(years, years[1:]):
        if current == previous:
            raise ValueError(f'observation_years contains duplicate year {current}; '
                             'calendar years must be unique')
        if current < previous:
            raise ValueError(f'observation_years is not strictly increasing: {current} '
                             f'follows {previous}; calendar years must be strictly increasing')
    return tuple(years)


@dataclass(frozen=True)
class SupplyBasis:
    """Source-specific product, geographic and duty-free coverage, not inferred from units.

    `source_ids` and `observation_years` are optional identity declarations: they
    name WHICH source and WHICH observation years a series came from, so two runs
    conditioning the same MOH/NZHS source are distinguishable at the ledger layer.
    An empty tuple is documented as "unattributed", and a caller that omits them
    must not claim a source identity.
    """
    unit: str = 'cigarette_equivalents'
    geography: str = 'NZ_national'
    products: str = 'factory_made_and_RYO_at_source_0.7g_convention'
    duty_free_included: bool = True
    source_ids: tuple[str, ...] = ()
    observation_years: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.unit != 'cigarette_equivalents':
            raise ValueError('Incompatible unit: an explicit audited conversion is required')
        if not isinstance(self.geography, str) or not self.geography.strip():
            raise ValueError('geography is required')
        if not isinstance(self.products, str) or not self.products.strip():
            raise ValueError('product basis is required')
        if not isinstance(self.duty_free_included, bool):
            raise ValueError('duty_free_included must be boolean')
        # Normalise the declared identity (strip whitespace, canonise ints) on a
        # frozen dataclass; validation is not a default that changes a scientific input.
        object.__setattr__(self, 'source_ids', _source_ids(self.source_ids))
        object.__setattr__(self, 'observation_years', _observation_years(self.observation_years))


@dataclass(frozen=True)
class LawfulLedger:
    years: YearsArray
    releases: Array
    stocks: Array
    unrecorded: Array
    net_visitors: Array
    duty_free_addition: Array
    consumption: Array
    basis: SupplyBasis

    def __post_init__(self) -> None:
        """Detach and freeze the arrays so a returned ledger cannot be mutated."""
        for name in ('years', 'releases', 'stocks', 'unrecorded', 'net_visitors',
                     'duty_free_addition', 'consumption'):
            frozen = np.array(getattr(self, name), copy=True)
            frozen.setflags(write=False)
            object.__setattr__(self, name, frozen)


def lawful_ledger(
    years: Iterable[int], releases: Iterable[Real], stocks: Iterable[Real], *,
    unrecorded: Iterable[Real] | None = None,
    net_visitors: Iterable[Real] | None = None,
    duty_free_addition: Iterable[Real] | None = None,
    basis: SupplyBasis,
) -> LawfulLedger:
    """Compute C_t = R_t + S_(t-1) - S_t + U_t + V_t + D_t.

    Stocks have n+1 boundaries; stock changes telescope rather than independently
    inflating every year's consumption. V is net lawful consumption in the target
    geography absent from releases (negative for lawful exports/outbound visitors).
    D must be zero when duty-free is already included in the release series.

    `basis` is required with no default: it declares the unit, geography, product
    coverage and duty-free treatment the caller has audited. There is no implicit
    conversion, so a tonne- or stick-valued series is NOT detected here; the
    caller must supply a series already on the declared basis.
    """
    yy = list(years)
    if not yy or any(isinstance(y, (bool, np.bool_)) or not isinstance(y, Integral)
                     or not 1 <= y <= 9998 for y in yy):
        raise ValueError('years must be nonempty calendar integers')
    y = np.asarray(yy, dtype=np.int64)
    if np.any(np.diff(y) != 1):
        raise ValueError('years must be consecutive, unique and increasing')
    if not isinstance(basis, SupplyBasis):
        raise ValueError('A validated SupplyBasis is required')
    n = len(y)
    r, s = _array(releases, 'releases', n), _array(stocks, 'stocks', n+1)
    u = _array(np.zeros(n) if unrecorded is None else unrecorded, 'unrecorded', n)
    v = _array(np.zeros(n) if net_visitors is None else net_visitors, 'net_visitors', n, True)
    d = _array(np.zeros(n) if duty_free_addition is None else duty_free_addition, 'duty_free', n)
    if basis.duty_free_included and np.any(d != 0):
        raise ValueError('Additional duty-free would double count this source')
    c = r + s[:-1] - s[1:] + u + v + d
    negative = np.flatnonzero(c < 0)
    if negative.size:
        details = '; '.join(
            f'negative lawful consumption in {int(y[i])} (index {int(i)}): '
            f'R={r[i]:.6g}, S_prev-S={s[i]-s[i+1]:.6g}, U={u[i]:.6g}, '
            f'V={v[i]:.6g}, D={d[i]:.6g}'
            for i in negative)
        raise ValueError(
            f'{details}. The caller must supply a release/stock/adjustment set '
            f'that does not imply negative consumption')
    if not np.isfinite(c).all():
        raise ValueError('Ledger overflow')
    return LawfulLedger(y, r, s, u, v, d, c, basis)


def stock_scenario(releases: Iterable[Real], days: Real) -> Array:
    """Assumed stock boundaries: opening=first release rate; closings=current rate.

    A fixed days-of-supply scenario, not observed stocks. The source's 365-day
    cigarette-equivalent convention is retained for this scenario only.

    `days` is the declared days-of-supply assumption, so `days=0` is the declared
    "no stock adjustment" case: it returns an all-zero boundary array, which is a
    scenario result and NOT an observed zero inventory. `annualised_supply`
    deliberately spreads period totals by actual calendar-year length instead, so
    the two day counts are not interchangeable.
    """
    r = list(releases)
    if not r:
        raise ValueError('releases must not be empty')
    a = _array(r, 'releases', len(r))
    d = _scalar(days, 'stock days')
    return np.r_[a[0], a] * d / 365.


def annualised_supply(ledger: LawfulLedger, start: str, end: str) -> dict[str, Any]:
    """Period-average daily supply times 365, to match the paper's annual-equivalent unit.

    Two quantities in the ledger's declared basis are returned and must not be used
    interchangeably: `allocated_total` is the window total in source annual units,
    and `annualised_per_365_days` is that total rescaled to a 365-day year. For a
    366-day window the rate is lower than the total.

    Annual totals are spread uniformly within their calendar years, so the divisor
    is the actual calendar-year length (366 in a leap year), unlike
    `stock_scenario`, which deliberately keeps the source's fixed 365-day
    convention. Actual month-level consumption has NOT been observed.

    Raises:
        ValueError: if the window covers no days, so no annualised rate is defined.
    """
    result = aggregate_uniform_years(
        dict(zip(ledger.years.tolist(), ledger.consumption.tolist())), start, end)
    covered_days = result['covered_days']
    if covered_days <= 0:
        raise ValueError(
            f'Window {start} to {end} covers {covered_days} days: an annualised '
            f'per-365-day rate requires at least one covered day')
    result['annualised_per_365_days'] = result['allocated_total'] / covered_days * 365.
    result['unit'] = 'cigarette_equivalents/365_day_equivalent'
    result['allocation_is_observed'] = False
    result['geography'] = ledger.basis.geography
    result['products'] = ledger.basis.products
    return result
