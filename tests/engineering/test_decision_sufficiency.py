"""Independent finite-state witnesses and invalid-input controls."""

from fractions import Fraction

import pytest

from scripts.decision_identification_benchmark import run_benchmark
from scripts.decision_sufficiency import assess


def test_conflicting_states_have_exact_regret_and_counterexamples():
    result = assess(["low", "high"], ["act", "wait"], [["-2", "0"], ["3", "0"]])
    assert result["common_optimal_actions"] == []
    assert result["status"] == "not_identified"
    assert result["worst_case_regret"] == {"act": "2", "wait": "3"}
    assert result["pairwise"][0] == {
        "action": "act",
        "comparator": "wait",
        "lower": "-2",
        "upper": "3",
        "lower_state": "low",
        "upper_state": "high",
    }
    assert result["minimax_regret_actions"] == ["act"]


def test_dominance_ties_and_exact_decimal_boundaries():
    result = assess(["s1", "s2"], ["a", "b", "c"], [["0.1", "0.1", "0"], ["0.3", "0.3", "0.2"]])
    assert result["common_optimal_actions"] == ["a", "b"]
    assert result["status"] == "common_optimum_with_ties"
    assert result["worst_case_regret"]["c"] == "1/10"
    assert Fraction(result["pairwise"][1]["lower"]) == Fraction(1, 10)


def test_restriction_retains_state_identity_and_does_not_use_prior():
    result = assess(["s1", "s2"], ["a", "b"], [[0, 2], [3, 0]], compatible=["s2"])
    assert result["status"] == "unique_common_optimum"
    assert result["common_optimal_actions"] == ["a"]
    assert result["state_optima"] == {"s2": ["a"]}


@pytest.mark.parametrize(
    ("states", "actions", "values", "compatible"),
    [
        (["s", "s"], ["a"], [[1], [2]], None),
        (["s"], ["a", "a"], [[1, 2]], None),
        (["s"], ["a"], [[None]], None),
        (["s"], ["a"], [["NaN"]], None),
        (["s"], ["a"], [[True]], None),
        (["s"], ["a"], [[0.1]], None),
        (["s"], ["a"], [[1, 2]], None),
        (["s"], ["a"], [[1]], ["unknown"]),
        (["s"], ["a"], [[1]], ["s", "s"]),
    ],
)
def test_invalid_or_unknown_inputs_fail(states, actions, values, compatible):
    with pytest.raises((ValueError, TypeError), match=r"required|match|Unknown|rational"):
        assess(states, actions, values, compatible=compatible)


def test_contradictory_support_is_not_vacuous_dominance():
    result = assess(["s"], ["a"], [[1]], compatible=[])
    assert result["status"] == "incompatible"
    assert result["common_optimal_actions"] == []
    assert result["pairwise"] == []


def test_restricting_support_cannot_increase_worst_case_regret():
    full = assess(["s1", "s2", "s3"], ["a", "b"], [[-2, 0], [3, 0], [1, 1]])
    restricted = assess(["s1", "s2", "s3"], ["a", "b"], [[-2, 0], [3, 0], [1, 1]], compatible=["s3"])
    for action in ("a", "b"):
        assert Fraction(restricted["worst_case_regret"][action]) <= Fraction(
            full["worst_case_regret"][action]
        )


def test_unknown_payoff_is_not_treated_as_zero():
    with pytest.raises(TypeError, match="Known finite"):
        assess(["s"], ["act", "wait"], [[None, 0]])


def test_legacy_interval_benchmark_does_not_claim_decision_identification():
    result = run_benchmark()
    assert result["summary"]["decision_identification_assessed"] is False
    assert result["no_total_no_lawful"]["parameter_point_identified"] is False
    assert result["exact_ratios"]["parameter_point_identified"] is True
    assert all("decision_identifiable" not in value for value in result.values())


@pytest.mark.parametrize(
    ("field", "value"), [("states", "s"), ("actions", "a"), ("payoffs", None), ("compatible", "s")]
)
def test_json_container_types_are_not_silently_coerced(field, value):
    packet = {"states": ["s"], "actions": ["a"], "payoffs": [[1]], "compatible": None}
    packet[field] = value
    with pytest.raises((ValueError, TypeError), match=r"required|dimensions|list"):
        assess(**packet)
