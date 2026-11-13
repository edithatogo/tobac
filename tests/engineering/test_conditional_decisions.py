"""Exact accounting bounds have analytical and independent interior-point checks."""

import json
from fractions import Fraction
from pathlib import Path

import pytest

from scripts.conditional_decisions import accounting_box, run_scenarios


def test_closed_form_advantage_bounds_and_threshold():
    result = accounting_box(["3/4", "1"], ["39/250", "39/250"], ["0", "1/10"])
    assert result["advantage_lower"] == "17/1000"
    assert result["advantage_upper"] == "39/250"
    assert result["minimum_response_for_weak_dominance"] == "25/39"
    assert result["decision"]["common_optimal_actions"] == ["act"]


def test_joint_rectangle_sensitivity_reverses_minimum_response_dominance():
    result = accounting_box(["3/4", "1"], ["133/1000", "179/1000"], ["0", "1/10"])
    assert result["advantage_lower"] == "-1/4000"
    assert result["decision"]["common_optimal_actions"] == []
    assert result["minimum_response_for_weak_dominance"] == "100/133"


def test_exact_threshold_retains_both_actions():
    result = accounting_box(["1/2", "1/2"], ["39/250", "39/250"], ["39/500", "39/500"])
    assert result["decision"]["common_optimal_actions"] == ["act", "wait"]


def test_corner_bounds_cover_independent_interior_grid():
    result = accounting_box(["0", "1"], ["1/10", "1/5"], ["0", "1/10"])
    low, high = Fraction(result["advantage_lower"]), Fraction(result["advantage_upper"])
    for numerator in range(11):
        for d in (Fraction(1, 10), Fraction(3, 20), Fraction(1, 5)):
            for c in (Fraction(0), Fraction(1, 20), Fraction(1, 10)):
                assert low <= Fraction(numerator, 10) * d - c <= high


def test_unknown_response_is_not_assigned_a_range():
    result = accounting_box(None, ["39/250", "39/250"], None)
    assert result["status"] == "not_assessable_missing_restrictions"
    assert "decision" not in result


@pytest.mark.parametrize(
    ("response", "gain", "burden"),
    [
        (["1", "0"], ["1", "1"], ["0", "1"]),
        (["0", "2"], ["1", "1"], ["0", "1"]),
        (["0", "1"], ["-1", "1"], ["0", "1"]),
        (["0", "1"], ["1", "1"], ["-1", "0"]),
        (["0", "1"], ["NaN", "1"], ["0", "1"]),
    ],
)
def test_invalid_support_cannot_yield_a_certificate(response, gain, burden):
    with pytest.raises(ValueError, match=r"support|rational"):
        accounting_box(response, gain, burden)


def test_scenarios_bind_coefficients_and_preserve_all_prespecified_cases():
    root = Path(__file__).resolve().parents[2]
    path = root / "conductor/tracks/nz_au_empirical_20261106/conditional-scenarios-20261113.json"
    packet = json.loads(path.read_text())
    assert len(run_scenarios(root, packet)) == 7
    packet["scenarios"][1]["gain"] = ["1", "1"]
    with pytest.raises(ValueError, match="coefficient"):
        run_scenarios(root, packet)


def test_binary_float_and_boolean_endpoints_are_not_silently_accepted():
    with pytest.raises(TypeError, match="rational string"):
        accounting_box([False, 1.0], ["1", "1"], ["0", "0"])
