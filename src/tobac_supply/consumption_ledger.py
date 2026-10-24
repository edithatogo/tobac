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
        raise ValueError(f'{name} needs {length} values')
    return a


@dataclass(frozen=True)
class SupplyBasis:
    """Source-specific product, geographic and duty-free coverage, not inferred from units."""
    unit: str = 'cigarette_equivalents'
    geography: str = 'NZ_national'
    products: str = 'factory_made_and_RYO_at_source_0.7g_convention'
    duty_free_included: bool = True

    def __post_init__(self) -> None:
        if self.unit != 'cigarette_equivalents':
            raise ValueError('Incompatible unit: an explicit audited conversion is required')
        if not isinstance(self.geography, str) or not self.geography.strip():
            raise ValueError('geography is required')
        if not isinstance(self.products, str) or not self.products.strip():
            raise ValueError('product basis is required')
        if not isinstance(self.duty_free_included, bool):
            raise ValueError('duty_free_included must be boolean')


@dataclass(frozen=True)
class LawfulLedger:
    years: NDArray[np.int64]
    releases: Array
    stocks: Array
    unrecorded: Array
    net_visitors: Array
    duty_free_addition: Array
    consumption: Array
    basis: SupplyBasis


def lawful_ledger(
    years: Iterable[int], releases: Iterable[Real], stocks: Iterable[Real], *,
    unrecorded: Iterable[Real] | None = None,
    net_visitors: Iterable[Real] | None = None,
    duty_free_addition: Iterable[Real] | None = None,
    basis: SupplyBasis = SupplyBasis(),
) -> LawfulLedger:
    """Compute C_t = R_t + S_(t-1) - S_t + U_t + V_t + D_t.

    Stocks have n+1 boundaries; stock changes telescope rather than independently
    inflating every year's consumption. V is net lawful consumption in the target
    geography absent from releases (negative for lawful exports/outbound visitors).
    D must be zero when duty-free is already included in the release series.
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
    if np.any(c < 0):
        raise ValueError('Inputs imply negative lawful consumption')
    if not np.isfinite(c).all():
        raise ValueError('Ledger overflow')
    return LawfulLedger(y, r, s, u, v, d, c, basis)


def stock_scenario(releases: Iterable[Real], days: Real) -> Array:
    """Assumed stock boundaries: opening=first release rate; closings=current rate.

    A fixed days-of-supply scenario, not observed stocks. The source's 365-day
    cigarette-equivalent convention is retained for this scenario only.
    """
    r = list(releases)
    if not r:
        raise ValueError('releases must not be empty')
    a = _array(r, 'releases', len(r))
    d = _scalar(days, 'stock days')
    return np.r_[a[0], a] * d / 365.


def annualised_supply(ledger: LawfulLedger, start: str, end: str) -> dict[str, Any]:
    """Period-average daily supply times 365, to match the paper's annual-equivalent unit.

    Annual totals are spread uniformly within their calendar years. Actual
    month-level consumption has NOT been observed. Leap years are respected.
    """
    result = aggregate_uniform_years(
        dict(zip(ledger.years.tolist(), ledger.consumption.tolist())), start, end)
    actual = float(result['value'])
    result['period_total'] = actual
    result['value'] = actual / result['covered_days'] * 365.
    result['unit'] = 'cigarette_equivalents/365_day_equivalent'
    result['allocation_is_observed'] = False
    result['geography'] = ledger.basis.geography
    result['products'] = ledger.basis.products
    return result
