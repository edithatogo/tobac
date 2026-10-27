"""Set-valued M2a accounting and ratio bounds; no likelihood or prior update.

Rectangular input sets are explicit assumptions, not confidence intervals or
independence probabilities. Sharp marginal bounds do not make q and d independent.
M2a excludes total-consumption increases and other mechanisms; an empty set is
model/data incompatibility, not a reason to clip observations or alter the model.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    """Finite closed scalar interval, retaining signed discrepancies."""

    lower: float
    upper: float

    def __post_init__(self) -> None:
        """Reject malformed supports instead of silently sorting or truncating them."""
        if not math.isfinite(self.lower) or not math.isfinite(self.upper) or self.lower > self.upper:
            msg = "Finite ordered interval endpoints required"
            raise ValueError(msg)

    def subtract(self, other: Interval) -> Interval:
        """Project a Cartesian set through subtraction without clipping negative values."""
        return Interval(self.lower - other.upper, self.upper - other.lower)

    def divide_positive(self, other: Interval) -> Interval:
        """Divide a nonnegative support by a strictly positive calibration support."""
        if self.lower < 0 or other.lower <= 0:
            msg = "Nonnegative quantities and strictly positive calibration required"
            raise ValueError(msg)
        return Interval(self.lower / other.upper, self.upper / other.lower)


@dataclass(frozen=True)
class RatioBounds:
    """Sharp marginal supports conditional on the declared M2a ratio structure."""

    feasible: bool
    quitting: Interval | None
    switching: Interval | None


def _ratio(observed: Interval | None, bias: Interval) -> Interval | None:
    if bias.lower <= 0:
        msg = "A strictly positive reporting bias is required"
        raise ValueError(msg)
    if observed is None:
        return Interval(0, 1)
    corrected = observed.divide_positive(bias)
    lower, upper = max(0.0, corrected.lower), min(1.0, corrected.upper)
    return None if lower > upper else Interval(lower, upper)


def restriction_bounds(
    total: Interval | None,
    lawful: Interval | None,
    *,
    total_bias: Interval,
    lawful_bias: Interval,
) -> RatioBounds:
    """Bound q,d from R_T=b_T*(1-q), R_L=b_L*(1-q)*(1-d).

    All four input supports are a Cartesian set; correlated restrictions can
    narrow it further. Bias supports are explicit even when an outcome is absent.
    q,d lie in[0,1]. At q=1, d is structurally irrelevant and unidentified. The
    original measurements remain unchanged when intersecting parameter support.
    Ratios concern restriction alone, before mitigation/replacement; other
    causal structures require separate bounds.
    """
    total_ratio, lawful_ratio = _ratio(total, total_bias), _ratio(lawful, lawful_bias)
    if total_ratio is None or lawful_ratio is None or lawful_ratio.lower > total_ratio.upper:
        return RatioBounds(feasible=False, quitting=None, switching=None)
    minimum_total = max(total_ratio.lower, lawful_ratio.lower)
    quitting = Interval(1 - total_ratio.upper, 1 - minimum_total)
    if minimum_total == 0:
        switching = Interval(0, 1)
    else:
        switching = Interval(
            1 - min(1.0, lawful_ratio.upper / minimum_total), 1 - lawful_ratio.lower / total_ratio.upper
        )
    return RatioBounds(feasible=True, quitting=quitting, switching=switching)


def accounting_bounds(  # noqa: PLR0913 -- Keep explicit dimensioned accounting components, matching supply.py.
    releases: Interval,
    *,
    reporting_bias: Interval,
    unrecorded: Interval,
    stock: Interval,
    outbound: Interval,
    wastage: Interval,
) -> Interval:
    """Invert existing release accounting over an explicit Cartesian uncertainty set.

    All amounts must have a qualified common Scope, product coverage and unit;
    this scalar helper cannot establish those semantics. Unrecorded is absolute.
    Stock accumulation is positive; stock may be negative. Unknown components
    require supports or a missing result, never an implicit zero. Signed results
    remain discrepancies until a physical measurement model is qualified.
    """
    if any(value.lower < 0 for value in (unrecorded, outbound, wastage)):
        msg = "Unrecorded, outbound and wastage supports must be nonnegative"
        raise ValueError(msg)
    recorded = releases.divide_positive(reporting_bias).subtract(stock).subtract(outbound).subtract(wastage)
    return Interval(recorded.lower + unrecorded.lower, recorded.upper + unrecorded.upper)
