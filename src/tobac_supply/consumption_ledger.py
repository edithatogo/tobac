"""Lawful supply-to-consumption accounting with explicit units and shared stocks.

The ledger does not estimate illegal origin. Adjustments are supplied assumptions
or observations; no catchment allocation or tonnes-to-sticks conversion is implicit.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Integral, Real
from typing import Any, cast
lazy from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray

from tobac_supply.longitudinal import aggregate_uniform_years

Array = NDArray[np.float64]
YearsArray = NDArray[np.int64]


# Named bounds preserve the existing scientific/data contract.
MAX_YEAR_BEFORE_CLOSING = 9998


def _scalar(value: float, name: str, minimum: float = 0.0) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(cast("object", value), Real):
        msg = f"{name} must be numeric, not boolean"
        raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
    x = float(value)
    if not math.isfinite(x) or x < minimum:
        msg = f"{name} must be finite and >= {minimum}"
        raise ValueError(msg)
    return x


def _array(values: Iterable[float], name: str, length: int, *, signed: bool = False) -> Array:
    try:
        a = np.array([_scalar(x, name, -math.inf if signed else 0.0) for x in values])
    except TypeError as exc:
        msg = f"{name} must be a sequence"
        raise ValueError(msg) from exc
    if len(a) != length:
        msg = f"{name} needs {length} values, got {len(a)}"
        raise ValueError(msg)
    return a



def _source_ids(values: tuple[str, ...]) -> tuple[str, ...]:
    """Validate a declared source identity; the empty tuple is the unattributed default."""
    if not isinstance(values, tuple):
        raise ValueError(f"source_ids must be a tuple of strings; got {type(values).__name__}")
    stripped: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f"source_ids must contain strings; got {type(value).__name__} {value!r}")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("source_ids contains an empty source id; each source id must be non-empty after stripping whitespace")
        if cleaned in stripped:
            raise ValueError(f"source_ids contains duplicate source id {cleaned!r}; source ids must be unique")
        stripped.append(cleaned)
    return tuple(stripped)


def _observation_years(values: tuple[int, ...]) -> tuple[int, ...]:
    """Validate declared observation years; the empty tuple means unattributed years."""
    if not isinstance(values, tuple):
        raise ValueError(f"observation_years must be a tuple of integer years; got {type(values).__name__}")
    years: list[int] = []
    for value in values:
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
            raise ValueError(f"observation_years must contain integer calendar years; got {value!r}")
        year = int(value)
        if not 1 <= year <= 9998:
            raise ValueError(f"observation_years value {year} is not a calendar year (must be 1..9998)")
        years.append(year)
    for previous, current in zip(years, years[1:]):
        if current == previous:
            raise ValueError(f"observation_years contains duplicate year {current}; calendar years must be unique")
        if current < previous:
            raise ValueError(
                f"observation_years is not strictly increasing: {current} follows {previous}; "
                "calendar years must be strictly increasing"
            )
    return tuple(years)

@dataclass(frozen=True)
class SupplyBasis:
    """Source-specific product, geographic and duty-free coverage, not inferred from units."""

    unit: str = "cigarette_equivalents"
    geography: str = "NZ_national"
    products: str = "factory_made_and_RYO_at_source_0.7g_convention"
    duty_free_included: bool = True
    source_ids: tuple[str, ...] = ()
    observation_years: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        """Validate construction invariants and normalize the stored values."""
        if self.unit != "cigarette_equivalents":
            msg = "Incompatible unit: an explicit audited conversion is required"
            raise ValueError(msg)
        if not isinstance(cast("object", self.geography), str) or not self.geography.strip():
            msg = "geography is required"
            raise ValueError(msg)
        if not isinstance(cast("object", self.products), str) or not self.products.strip():
            msg = "product basis is required"
            raise ValueError(msg)
        if not isinstance(cast("object", self.duty_free_included), bool):
            msg = "duty_free_included must be boolean"
            raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
        if self.source_ids != _source_ids(self.source_ids):
            msg = "source_ids normalization changed the declared identity"
            raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
        if self.observation_years != _observation_years(self.observation_years):
            msg = "observation_years normalization changed the declared identity"
            raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.


@dataclass(frozen=True)
class LawfulLedger:
    """Aligned releases, stock and lawful-channel accounting under a declared basis."""

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
        for name in (
            "years",
            "releases",
            "stocks",
            "unrecorded",
            "net_visitors",
            "duty_free_addition",
            "consumption",
        ):
            frozen = np.array(getattr(self, name), copy=True)
            frozen.setflags(write=False)
            object.__setattr__(self, name, frozen)


def lawful_ledger(  # noqa: PLR0913  # Preserve explicit dimensioned inputs and the established API.
    years: Iterable[int],
    releases: Iterable[float],
    stocks: Iterable[float],
    *,
    unrecorded: Iterable[float] | None = None,
    net_visitors: Iterable[float] | None = None,
    duty_free_addition: Iterable[float] | None = None,
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
    if not yy or any(
        isinstance(y, (bool, np.bool_))
        or not isinstance(y, Integral)
        or not 1 <= y <= MAX_YEAR_BEFORE_CLOSING
        for y in yy
    ):
        msg = "years must be nonempty calendar integers"
        raise ValueError(msg)
    y = np.asarray(yy, dtype=np.int64)
    if np.any(np.diff(y) != 1):
        msg = "years must be consecutive, unique and increasing"
        raise ValueError(msg)
    if not isinstance(cast("object", basis), SupplyBasis):
        msg = "A validated SupplyBasis is required"
        raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
    n = len(y)
    r, s = _array(releases, "releases", n), _array(stocks, "stocks", n + 1)
    u = _array(np.zeros(n) if unrecorded is None else unrecorded, "unrecorded", n)
    v = _array(np.zeros(n) if net_visitors is None else net_visitors, "net_visitors", n, signed=True)
    d = _array(np.zeros(n) if duty_free_addition is None else duty_free_addition, "duty_free", n)
    if basis.duty_free_included and np.any(d != 0):
        msg = "Additional duty-free would double count this source"
        raise ValueError(msg)
    c = r + s[:-1] - s[1:] + u + v + d
    negative = np.flatnonzero(c < 0)
    if negative.size:
        details = "; ".join(
            f"negative lawful consumption in {int(y[i])} (index {int(i)}): "
            f"R={r[i]:.6g}, S_prev-S={s[i] - s[i + 1]:.6g}, U={u[i]:.6g}, "
            f"V={v[i]:.6g}, D={d[i]:.6g}"
            for i in negative
        )
        msg = (
            f"{details}. The caller must supply a release/stock/adjustment set "
            f"that does not imply negative consumption"
        )
        raise ValueError(msg)
    if not np.isfinite(c).all():
        msg = "Ledger overflow"
        raise ValueError(msg)
    return LawfulLedger(y, r, s, u, v, d, c, basis)


def stock_scenario(releases: Iterable[float], days: float) -> Array:
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
        msg = "releases must not be empty"
        raise ValueError(msg)
    a = _array(r, "releases", len(r))
    d = _scalar(days, "stock days")
    return np.r_[a[0], a] * d / 365.0


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
        dict(zip(ledger.years.tolist(), ledger.consumption.tolist(), strict=True)), start, end
    )
    covered_days = result["covered_days"]
    if covered_days <= 0:
        msg = (
            f"Window {start} to {end} covers {covered_days} days: an annualised "
            f"per-365-day rate requires at least one covered day"
        )
        raise ValueError(msg)
    result["annualised_per_365_days"] = result["allocated_total"] / covered_days * 365.0
    result["unit"] = "cigarette_equivalents/365_day_equivalent"
    result["allocation_is_observed"] = False
    result["geography"] = ledger.basis.geography
    result["products"] = ledger.basis.products
    return result
