"""Regression tests for information."""

import numpy as np
import pytest

from tobac._core import DecisionProblem, exact_evpi, exact_partial_information
from tobac.information import (
    _likelihood,
    evaluate,
    joint_likelihood,
    lognormal_bins,
    same_data_robustness,
    scalar_oracle,
    validate_likelihood,
)


def test_established_likelihood_import_retains_identity_and_validation() -> None:
    assert _likelihood is validate_likelihood
    np.testing.assert_array_equal(_likelihood([[0.25, 0.75], [0.75, 0.25]], 2), [[0.25, 0.75], [0.75, 0.25]])
    with pytest.raises(ValueError, match="stochastic"):
        _likelihood([[0.25, 0.25]], 2)


def problem():
    return DecisionProblem(np.array([[0.0, 2.0], [2.0, 0.0]]), ("a", "b"), "illustrative loss units")


def test_perfect_and_uninformative() -> None:
    p = problem()
    assert evaluate(p, np.eye(2), {"truth": [0, 1]})["evsi"] == pytest.approx(1)
    r = evaluate(p, np.ones((1, 2)), {"truth": [0, 1]})
    assert r["evsi"] == pytest.approx(0)
    assert r["targets"]["truth"]["eig_nats"] == pytest.approx(0)
    assert r["posterior_martingale_max_error"] < 1e-12


def test_exact_noisy_binary() -> None:
    p = problem()
    likelihood = np.array([[0.8, 0.2], [0.2, 0.8]])
    r = evaluate(p, likelihood, {"truth": [0, 1]}, event=np.array([False, True]), confidence=0.75)
    assert r["evsi"] == pytest.approx(0.6)
    assert r["probability_action_changes"] == pytest.approx(0.5)
    assert r["targets"]["truth"]["eig_nats"] == pytest.approx(
        np.log(2) + 0.8 * np.log(0.8) + 0.2 * np.log(0.2)
    )
    assert r["resolution_probability"] == pytest.approx(1)
    assert r["correct_resolution_probability"] == pytest.approx(0.8)
    assert r["event_brier_risk"] == pytest.approx(0.16)
    assert scalar_oracle(p, likelihood) == pytest.approx(r["evsi"])


def test_scientific_gain_without_decision_value() -> None:
    p = DecisionProblem(np.array([[1.0, 0.0], [1.0, 0.0]]), ("a", "b"), "units")
    r = evaluate(p, np.eye(2), {"truth": [0, 1]})
    assert r["evsi"] == pytest.approx(0)
    assert r["targets"]["truth"]["eig_nats"] == pytest.approx(np.log(2))


def test_cross_targets_do_not_receive_independent_information() -> None:
    p = DecisionProblem(np.array([[0.0, 2.0], [2.0, 0.0], [0.0, 2.0], [2.0, 0.0]]), ("a", "b"), "units")
    likelihood = np.array([[0.9, 0.9, 0.1, 0.1], [0.1, 0.1, 0.9, 0.9]])
    r = evaluate(p, likelihood, {"signal": [0, 0, 1, 1], "unrelated": [0, 1, 0, 1]})
    assert r["evsi"] == pytest.approx(0)
    assert r["targets"]["unrelated"]["eig_nats"] == pytest.approx(0, abs=1e-12)
    assert r["targets"]["signal"]["eig_nats"] > 0


def test_zero_mass_states_and_impossible_outcomes() -> None:
    p = DecisionProblem(np.array([[0.0, 2.0], [2.0, 0.0]]), ("a", "b"), "units", np.array([1.0, 0.0]))
    likelihood = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])
    r = evaluate(p, likelihood, {"truth": [0, 1]})
    assert r["evsi"] == pytest.approx(0)
    assert r["targets"]["truth"]["eig_nats"] == pytest.approx(0)


@pytest.mark.parametrize(
    "likelihood",
    [np.array([[1.0, 0.8]]), np.array([[1.0, -1.0], [0.0, 2.0]]), np.array([[1.0, np.nan]]), np.ones((2, 3))],
)
def test_invalid_likelihood_rejected(likelihood) -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:Require\ a\ finite\ stochastic\ outcome\-by\-state\ likelihood)"),
    ):
        evaluate(problem(), likelihood)


def test_joint_likelihood_and_diminishing_uncertainty() -> None:
    likelihood = np.array([[0.8, 0.2], [0.2, 0.8]])
    joined = joint_likelihood(likelihood, likelihood)
    assert joined.shape == (4, 2)
    assert np.allclose(joined.sum(0), 1)
    assert evaluate(problem(), joined)["evsi"] >= evaluate(problem(), likelihood)["evsi"] - 1e-12
    assert evaluate(problem(), joined)["evsi"] <= exact_evpi(problem()) + 1e-12


def test_lognormal_bins_censoring_and_refinement() -> None:
    med = np.array([1.0, 3.0, 9.0])
    coarse = lognormal_bins(med, 0.3, [3.0, 6.0])
    fine = lognormal_bins(med, 0.3, [1.0, 3.0, 6.0])
    assert np.allclose(fine[:2].sum(0), coarse[0])
    assert np.allclose(fine.sum(0), 1)
    p = DecisionProblem(np.array([[0.0, 1.0], [0.0, 0.5], [1.0, 0.0]]), ("a", "b"), "u")
    assert evaluate(p, fine)["evsi"] >= evaluate(p, coarse)["evsi"] - 1e-12


@pytest.mark.parametrize(("sd", "cuts"), [(0, [1]), (0.2, [0]), (0.2, [2, 1]), (0.2, [1, 1])])
def test_invalid_bins_rejected(sd, cuts) -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Positive\ medians,\ positive\ SD\ and\ strictly\ increasing\ positive\ c"
            r"uts\ required"
            r")"
        ),
    ):
        lognormal_bins(np.array([1.0, 2.0]), sd, cuts)


def test_shift_and_uniform_replication_invariance() -> None:
    p = problem()
    likelihood = np.array([[0.8, 0.2], [0.2, 0.8]])
    expected = evaluate(p, likelihood)["evsi"]
    shift = DecisionProblem(p.values + 1e10, p.action_names, p.value_unit)
    assert evaluate(shift, likelihood)["evsi"] == pytest.approx(expected)
    duplicate = DecisionProblem(np.repeat(p.values, 2, axis=0), p.action_names, p.value_unit)
    assert evaluate(duplicate, np.repeat(likelihood, 2, axis=1))["evsi"] == pytest.approx(expected)


def test_grouped_partial_information() -> None:
    p = DecisionProblem(np.array([[0.0, 1.0], [0.0, 1.0], [1.0, 0.0], [1.0, 0.0]]), ("a", "b"), "u")
    assert exact_partial_information(p, [0, 0, 1, 1]) == pytest.approx(0.5)
    assert exact_partial_information(p, [0, 1, 0, 1]) == pytest.approx(0)


def test_same_data_robustness_uses_common_reference_distribution() -> None:
    likelihood = np.eye(2)
    r = same_data_robustness(
        problem().values,
        [np.array([0.2, 0.8]), np.array([0.8, 0.2])],
        np.array([0.5, 0.5]),
        likelihood,
        np.array([0, 1], bool),
    )
    assert r["expected_probability_range"] == pytest.approx(0)
    assert r["decision_agreement_probability"] == pytest.approx(1)
    assert r["confident_agreement_probability"] == pytest.approx(1)
