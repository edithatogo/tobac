"""Conditional M2a projections for matched inspection game scenarios."""

from __future__ import annotations

from fractions import Fraction

from tobac.partial_identification import Interval, RatioBounds, _ratio, restriction_bounds


def inspection_restriction_bounds(
    total: Interval | None,
    lawful: Interval | None,
    *,
    total_bias: Interval,
    lawful_bias: Interval,
    switching_support: Interval,
) -> RatioBounds:
    """Condition the ratio model on switching among continuing consumers.

    The support must describe the same population, product and observation
    period as the ratios. The projections are conditional on that support.
    At zero continuing consumption, switching is undefined and remains
    unrestricted in the projection.
    """
    if switching_support.lower < 0 or switching_support.upper > 1:
        msg = "Switching support must lie within [0, 1]"
        raise ValueError(msg)
    if switching_support == Interval(0, 1):
        return restriction_bounds(total, lawful, total_bias=total_bias, lawful_bias=lawful_bias)
    total_ratio, lawful_ratio = _ratio(total, total_bias), _ratio(lawful, lawful_bias)
    if total_ratio is None or lawful_ratio is None:
        return RatioBounds(feasible=False, quitting=None, switching=None)
    # For remaining consumption t and lawful share s, lawful use is t*s.
    # A given t admits a feasible s when t*max(s) >= min(lawful) and
    # t*min(s) <= max(lawful). Keep these comparisons exact at point boundaries.
    minimum_lawful, maximum_lawful = Fraction(lawful_ratio.lower), Fraction(lawful_ratio.upper)
    minimum_share = 1 - Fraction(switching_support.upper)
    maximum_share = 1 - Fraction(switching_support.lower)
    if maximum_share == 0 and minimum_lawful > 0:
        return RatioBounds(feasible=False, quitting=None, switching=None)

    minimum_total, maximum_total = Fraction(total_ratio.lower), Fraction(total_ratio.upper)
    if maximum_share > 0:
        minimum_total = max(minimum_total, minimum_lawful / maximum_share)
    if minimum_share > 0:
        maximum_total = min(maximum_total, maximum_lawful / minimum_share)
    if minimum_total > maximum_total:
        return RatioBounds(feasible=False, quitting=None, switching=None)

    quitting = Interval(float(1 - maximum_total), float(1 - minimum_total))
    if minimum_total == 0:
        switching = Interval(0, 1)
    else:
        switching = Interval(
            float(1 - min(maximum_share, maximum_lawful / minimum_total)),
            float(1 - max(minimum_share, minimum_lawful / maximum_total)),
        )
    return RatioBounds(feasible=True, quitting=quitting, switching=switching)
