"""Independent checks for identified sets, not fitted policy effects."""

import math

import numpy as np
import pytest
from scipy.optimize import linprog

from tobac.partial_identification import Interval, accounting_bounds, restriction_bounds

UNIT = Interval(1.0, 1.0)


def test_no_data_does_not_shrink_structural_support() -> None:
    result = restriction_bounds(None, None, total_bias=UNIT, lawful_bias=UNIT)
    assert result.feasible
    assert result.quitting == Interval(0, 1)
    assert result.switching == Interval(0, 1)


def test_matched_exact_ratios_identify_only_under_declared_structure() -> None:
    result = restriction_bounds(Interval(0.9, 0.9), Interval(0.72, 0.72), total_bias=UNIT, lawful_bias=UNIT)
    assert result.quitting.lower == pytest.approx(0.1)
    assert result.switching.lower == pytest.approx(0.2)
    assert result.switching.lower == result.switching.upper


def test_total_only_cannot_identify_switching() -> None:
    result = restriction_bounds(Interval(0.8, 0.9), None, total_bias=UNIT, lawful_bias=UNIT)
    assert result.switching == Interval(0, 1)
    assert result.quitting.lower == pytest.approx(0.1)
    assert result.quitting.upper == pytest.approx(0.2)


def test_lawful_only_bounds_but_does_not_separate_quitting_and_switching() -> None:
    result = restriction_bounds(None, Interval(0.8, 0.8), total_bias=UNIT, lawful_bias=UNIT)
    assert result.quitting.upper == pytest.approx(0.2)
    assert result.switching.upper == pytest.approx(0.2)
    assert result.quitting.lower == result.switching.lower == 0


def test_zero_consumption_leaves_switching_undefined_and_unrestricted() -> None:
    result = restriction_bounds(Interval(0, 0), Interval(0, 0), total_bias=UNIT, lawful_bias=UNIT)
    assert result.quitting == UNIT
    assert result.switching == Interval(0, 1)


def test_incompatible_model_is_empty_not_clipped_to_a_point() -> None:
    result = restriction_bounds(Interval(0.5, 0.6), Interval(0.8, 0.9), total_bias=UNIT, lawful_bias=UNIT)
    assert not result.feasible
    assert result.quitting is result.switching is None
    assert not restriction_bounds(Interval(1.1, 1.2), None, total_bias=UNIT, lawful_bias=UNIT).feasible


def test_reporting_bias_widens_identification() -> None:
    a = restriction_bounds(Interval(0.9, 0.9), Interval(0.72, 0.72), total_bias=UNIT, lawful_bias=UNIT)
    b = restriction_bounds(
        Interval(0.9, 0.9),
        Interval(0.72, 0.72),
        total_bias=Interval(0.9, 1.1),
        lawful_bias=Interval(0.9, 1.1),
    )
    assert b.quitting.lower <= a.quitting.lower <= a.quitting.upper <= b.quitting.upper
    assert b.switching.lower <= a.switching.lower <= a.switching.upper <= b.switching.upper


@pytest.mark.parametrize(("lower", "upper"), [(2, 1), (math.nan, 1), (0, math.inf)])
def test_invalid_intervals_fail(lower, upper) -> None:
    with pytest.raises(ValueError, match="Finite ordered"):
        Interval(lower, upper)


@pytest.mark.parametrize("bias", [Interval(0, 1), Interval(-1, 1)])
def test_nonpositive_bias_is_not_a_calibration(bias) -> None:
    with pytest.raises(ValueError, match="positive"):
        restriction_bounds(None, None, total_bias=bias, lawful_bias=UNIT)


def test_signed_accounting_residual_is_not_clipped() -> None:
    lawful = accounting_bounds(
        Interval(90, 110),
        reporting_bias=UNIT,
        unrecorded=Interval(0, 2),
        stock=Interval(-5, 10),
        outbound=Interval(0, 3),
        wastage=Interval(0, 1),
    )
    assert lawful == Interval(76, 117)
    assert Interval(80, 100).subtract(lawful) == Interval(-37, 24)


def test_all_admissible_samples_are_contained_and_marginals_are_sharp() -> None:
    # Independent linear-fractional optimisation: x=1/T, y=L/T, d=1-y.
    # T in[a,b], L in[c,e], L<=T gives c*x<=y<=e*x and0<=y<=1.
    cases = [(0.4, 0.9, 0.2, 0.3), (0.4, 0.9, 0.2, 0.8), (0.1, 1, 0.3, 0.9)]
    for a, b, c, e in cases:
        result = restriction_bounds(Interval(a, b), Interval(c, e), total_bias=UNIT, lawful_bias=UNIT)
        feasible_lower = max(a, c)
        constraints = np.array([[c, -1], [-e, 1]])
        bounds = [(1 / b, 1 / feasible_lower), (0, 1)]
        minimum = linprog([0, 1], A_ub=constraints, b_ub=[0, 0], bounds=bounds, method="highs")
        maximum = linprog([0, -1], A_ub=constraints, b_ub=[0, 0], bounds=bounds, method="highs")
        assert minimum.success
        assert maximum.success
        assert result.switching.lower == pytest.approx(1 + maximum.fun)
        assert result.switching.upper == pytest.approx(1 - minimum.fun)
        for total in np.linspace(a, b, 23):
            for lawful in np.linspace(c, e, 23):
                if lawful <= total:
                    assert result.quitting.lower - 1e-12 <= 1 - total <= result.quitting.upper + 1e-12
                    assert (
                        result.switching.lower - 1e-12 <= 1 - lawful / total <= result.switching.upper + 1e-12
                    )


@pytest.mark.parametrize("ratio", [Interval(-0.1, 0.5), Interval(-1, -0.5)])
def test_negative_ratio_requires_a_different_measurement_model(ratio) -> None:
    with pytest.raises(ValueError, match="Nonnegative"):
        restriction_bounds(ratio, None, total_bias=UNIT, lawful_bias=UNIT)


def test_zero_is_not_replaced_by_missing() -> None:
    result = restriction_bounds(None, Interval(0, 0), total_bias=UNIT, lawful_bias=UNIT)
    assert result.feasible
    assert result.switching == Interval(0, 1)
    assert result.quitting == Interval(0, 1)
    result = restriction_bounds(Interval(0.5, 1), Interval(0, 0), total_bias=UNIT, lawful_bias=UNIT)
    assert result.switching == UNIT


def test_negative_flow_corrections_are_invalid() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        accounting_bounds(
            Interval(1, 2),
            reporting_bias=UNIT,
            unrecorded=Interval(-1, 1),
            stock=Interval(0, 0),
            outbound=Interval(0, 0),
            wastage=Interval(0, 0),
        )
