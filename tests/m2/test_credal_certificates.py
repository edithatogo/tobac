"""Analytic BF1 checks; exact certificates are independently re-evaluated."""

from fractions import Fraction

import numpy as np
import pytest
from scipy.optimize import OptimizeResult

from scripts.decision_sufficiency import assess
from tobac._core import DecisionProblem
from tobac.credal import LinearRestriction, assess_contrast, assess_decision, minimal_identifying_restrictions
from tobac.evidence import Belief, Scope


def belief(differences=(-1.0, 1.0), prior=None):
    states = tuple(f"s{i}" for i in range(len(differences)))
    values = np.column_stack((np.array(differences, dtype=float), np.zeros(len(differences))))
    problem = DecisionProblem(values, ("act", "wait"), "synthetic score", prior)
    return Belief(problem, states, Scope("synthetic", "test", "2026-01-01", "2026-01-01", "score"))


def restriction(name, b, coefficients, upper):
    return LinearRestriction(name, b.state_ids, coefficients, upper)


def verify_lower(result, b, restrictions):
    cert = result["lower_certificate"]
    y = [Fraction(item) for item in cert["multipliers"]]
    assert len(y) == len(restrictions)
    assert all(value <= 0 for value in y)
    lam = Fraction(cert["simplex_offset"])
    for i in range(len(b.state_ids)):
        lhs = lam + sum(Fraction(float(r.coefficients[i])) * y[j] for j, r in enumerate(restrictions))
        c = Fraction(float(b.problem.values[i, 0])) - Fraction(float(b.problem.values[i, 1]))
        assert lhs <= c
    bound = lam + sum(Fraction(float(r.upper)) * y[j] for j, r in enumerate(restrictions))
    assert bound == Fraction(cert["bound"])
    return bound


def verify_witness(witness, b, restrictions):
    p = [Fraction(item) for item in witness["weights"]]
    assert sum(p) == 1
    assert all(x >= 0 for x in p)
    for r in restrictions:
        assert sum(Fraction(float(x)) * w for x, w in zip(r.coefficients, p, strict=True)) <= Fraction(
            float(r.upper)
        )
    advantage = sum(
        (Fraction(float(row[0])) - Fraction(float(row[1]))) * w
        for row, w in zip(b.problem.values, p, strict=True)
    )
    assert advantage == Fraction(witness["advantage"])
    return advantage


def test_unrestricted_simplex_matches_finite_state_oracle_and_prior_is_separate():
    b = belief(prior=[0.25, 0.75])
    result = assess_contrast(b, "act", "wait")
    assert result["status"] == "not_dominant"
    assert result["lower_estimate"] == pytest.approx(-1)
    assert result["upper_estimate"] == pytest.approx(1)
    assert result["prior_advantage"] == pytest.approx(0.5)
    assert verify_lower(result, b, ()) == -1
    assert verify_witness(result["lower_witness"], b, ()) == -1
    assert verify_witness(result["upper_witness"], b, ()) == 1
    assert b.used_data_ids == ()


def test_nonnegative_dual_certificate_proves_weak_dominance_with_a_tie():
    b = belief()
    limit = restriction("negative-state-at-most-half", b, (1, 0), 0.5)
    result = assess_contrast(b, "act", "wait", (limit,))
    assert result["status"] == "weak_dominance"
    assert verify_lower(result, b, (limit,)) == 0
    assert verify_witness(result["lower_witness"], b, (limit,)) == 0


def test_strict_dominance_certificate_has_positive_bound():
    b = belief()
    limit = restriction("negative-state-at-most-quarter", b, (1, 0), 0.25)
    result = assess_contrast(b, "act", "wait", (limit,))
    assert result["status"] == "strict_dominance"
    assert verify_lower(result, b, (limit,)) == Fraction(1, 2)
    assert verify_witness(result["lower_witness"], b, (limit,)) == Fraction(1, 2)


def test_near_zero_negative_is_not_rounded_to_dominance():
    b = belief((-1e-14, 1.0))
    result = assess_contrast(b, "act", "wait")
    assert result["status"] == "not_dominant"
    assert verify_lower(result, b, ()) < 0
    assert verify_witness(result["lower_witness"], b, ()) < 0


def test_two_joint_restrictions_are_minimal_and_each_deletion_has_counterexample():
    b = belief((-1.0, -1.0, 1.0, 1.0))
    limits = (restriction("first", b, (1, 0, 0, 0), 0.25), restriction("second", b, (0, 1, 0, 0), 0.25))
    result = minimal_identifying_restrictions(b, "act", "wait", limits)
    assert result["search_complete"]
    assert [x["restrictions"] for x in result["minimal_sets"]] == [["first", "second"]]
    item = result["minimal_sets"][0]
    assert verify_lower(item["proof"], b, limits) == 0
    for removed, witness in item["deletion_witnesses"].items():
        assert verify_witness(witness, b, tuple(r for r in limits if r.name != removed)) < 0


def test_distinct_singleton_minimal_restrictions_are_both_retained():
    b = belief()
    limits = (
        restriction("negative-at-most-half", b, (1, 0), 0.5),
        restriction("positive-at-least-half", b, (0, -1), -0.5),
    )
    result = minimal_identifying_restrictions(b, "act", "wait", limits)
    assert result["search_complete"]
    assert [x["restrictions"] for x in result["minimal_sets"]] == [
        ["negative-at-most-half"],
        ["positive-at-least-half"],
    ]


def test_empty_baseline_is_incompatible_and_has_no_vacuous_dominance():
    b = belief()
    limits = (
        restriction("p0-at-most-quarter", b, (1, 0), 0.25),
        restriction("p0-at-least-three-quarters", b, (-1, 0), -0.75),
    )
    result = assess_contrast(b, "act", "wait", limits)
    assert result["status"] == "incompatible"
    assert result["lower_certificate"] is None
    cert = result["infeasibility_certificate"]
    y = [Fraction(item) for item in cert["multipliers"]]
    assert all(x >= 0 for x in y)
    smallest_left = min(
        sum(Fraction(float(r.coefficients[i])) * y[j] for j, r in enumerate(limits))
        for i in range(len(b.state_ids))
    )
    upper_right = sum(Fraction(float(r.upper)) * y[j] for j, r in enumerate(limits))
    assert smallest_left > upper_right
    assert minimal_identifying_restrictions(b, "act", "wait", (), base=limits)["minimal_sets"] == []


def test_empty_candidate_is_the_unique_minimum_when_baseline_already_proves_dominance():
    b = belief((0.0, 1.0))
    limit = restriction("unneeded", b, (1, 0), 0.5)
    result = minimal_identifying_restrictions(b, "act", "wait", (limit,))
    assert [x["restrictions"] for x in result["minimal_sets"]] == [[]]


def test_state_identity_unknown_action_and_duplicate_names_fail_closed():
    b = belief()
    wrong = LinearRestriction("wrong", tuple(reversed(b.state_ids)), (1, 0), 0.5)
    with pytest.raises(ValueError, match="state"):
        assess_contrast(b, "act", "wait", (wrong,))
    with pytest.raises(ValueError, match="action"):
        assess_contrast(b, "unknown", "wait")
    r = restriction("same", b, (1, 0), 0.5)
    with pytest.raises(ValueError, match="unique"):
        minimal_identifying_restrictions(b, "act", "wait", (r, r))
    with pytest.raises(ValueError, match="finite"):
        LinearRestriction("bad", b.state_ids, (float("nan"), 0), 0.5)


def test_restriction_search_limit_is_explicit():
    b = belief()
    limits = tuple(restriction(f"r{i}", b, (1, 0), 0.5) for i in range(9))
    with pytest.raises(ValueError, match="eight"):
        minimal_identifying_restrictions(b, "act", "wait", limits)


def test_multi_action_comparison_retains_ties_and_exact_worst_regret_bounds():
    states = ("s0", "s1")
    problem = DecisionProblem(
        np.array([[0, 0, -2], [1, 1, 3]], float), ("first", "second", "third"), "score", [0.5, 0.5]
    )
    b = Belief(problem, states, Scope("synthetic", "test", "2026-01-01", "2026-01-01", "score"))
    limit = restriction("negative-state-most-quarter", b, (1, 0), 0.25)
    result = assess_decision(b, (limit,))
    assert result["status"] == "identified"
    assert result["common_optimal_actions"] == ["third"]
    assert result["action_status"]["first"] == "not_robust"
    assert result["worst_case_regret"]["first"]["lower"] == "2"
    assert result["worst_case_regret"]["first"]["upper"] == "2"
    assert result["worst_case_regret"]["third"]["lower"] == "0"
    assert result["worst_case_regret"]["third"]["upper"] == "0"


def test_multi_action_weakly_optimal_ties_are_preserved():
    b = belief((0.0, 0.0))
    result = assess_decision(b)
    assert result["common_optimal_actions"] == ["act", "wait"]
    assert result["worst_case_regret"]["act"]["upper"] == "0"


def test_solver_failure_retains_unknown_status_and_no_minimality_claim(monkeypatch):
    monkeypatch.setattr(
        "tobac.credal.linprog", lambda *_args, **_kwargs: OptimizeResult(success=False, status=4)
    )
    b = belief()
    result = assess_contrast(b, "act", "wait")
    assert result["status"] == "unresolved"
    assert result["lower_certificate"] is None
    searched = minimal_identifying_restrictions(b, "act", "wait", ())
    assert not searched["search_complete"]
    assert searched["minimal_sets"] == []


def test_unrestricted_credal_decision_matches_existing_exact_finite_oracle():
    values = [[3, 0, 1], [0, 3, 1], [1, 1, 1]]
    names = ("first", "second", "middle")
    b = Belief(
        DecisionProblem(np.array(values, dtype=float), names, "score"),
        ("s0", "s1", "s2"),
        Scope("synthetic", "test", "2026-01-01", "2026-01-01", "score"),
    )
    finite = assess(list(b.state_ids), list(names), values)
    result = assess_decision(b)
    assert result["common_optimal_actions"] == finite["common_optimal_actions"]
    for action in names:
        expected = finite["worst_case_regret"][action]
        assert result["worst_case_regret"][action] == {"lower": expected, "upper": expected}


@pytest.mark.parametrize(
    ("name", "ids", "coefficients", "upper"),
    [
        ("", ("s0", "s1"), (1, 0), 1),
        ("bad", ("s0", "s0"), (1, 0), 1),
        ("bad", ("s0", "s1"), ("unmeasured", 0), 1),
        ("bad", ("s0", "s1"), (1,), 1),
    ],
)
def test_malformed_restrictions_fail_before_optimization(name, ids, coefficients, upper):
    with pytest.raises(ValueError, match="Restriction"):
        LinearRestriction(name, ids, coefficients, upper)


def test_aggregate_decision_rejects_empty_support_and_reports_failed_solver_as_unknown(monkeypatch):
    b = belief()
    incompatible = (restriction("upper", b, (1, 0), 0.25), restriction("lower", b, (-1, 0), -0.75))
    assert assess_decision(b, incompatible)["status"] == "incompatible"
    monkeypatch.setattr(
        "tobac.credal.linprog", lambda *_args, **_kwargs: OptimizeResult(success=False, status=4)
    )
    unknown = assess_decision(b)
    assert unknown["status"] == "unresolved"
    assert unknown["common_optimal_actions"] == []
    assert unknown["worst_case_regret"] == {"act": None, "wait": None}


def test_untyped_belief_and_single_action_are_rejected():
    with pytest.raises(TypeError, match="Belief"):
        assess_contrast(None, "act", "wait")
    b = belief()
    one = Belief(DecisionProblem(np.zeros((2, 1)), ("alone",), "score"), b.state_ids, b.scope)
    with pytest.raises(ValueError, match="two actions"):
        assess_decision(one)
