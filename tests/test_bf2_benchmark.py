"""BF2 synthetic clock, measurement and comparison checks."""

import math

import numpy as np
import pytest

from scripts.bf2_benchmark import (
    BF2Model,
    categorical_log_loss,
    evaluate_regime,
    filter_report,
    initial_belief,
    transition_matrix,
    wastewater_likelihood,
)


def test_transition_models_keep_marginals_and_extreme_is_memoryless():
    ordinary = transition_matrix(0.35, 0.1)
    shared = transition_matrix(0.35, 0.1, shared=True)
    assert np.allclose(ordinary.sum(axis=1), 1)
    assert np.allclose(shared.sum(axis=1), 1)
    for matrix in (ordinary, shared):
        assert matrix[0, 2:].sum() == pytest.approx(0.35)
        assert matrix[0, [1, 3]].sum() == pytest.approx(0.1)
    assert np.allclose(transition_matrix(0, 0), np.eye(4))
    assert np.allclose(transition_matrix(0.5, 0.5), 0.25)


def test_wastewater_censored_bin_is_the_integrated_lognormal_cdf():
    w = wastewater_likelihood()
    exact = 0.5 * (1 + math.erf((math.log(1) - math.log(0.8)) / (0.4 * math.sqrt(2))))
    assert w.shape == (3, 4)
    assert w[0, 0] == pytest.approx(exact)
    assert np.allclose(w.sum(axis=0), 1)
    lower_limit = wastewater_likelihood(lower_limit=True)
    assert lower_limit.shape == (4, 4)
    assert np.allclose(lower_limit[0] + lower_limit[1], w[0])


def test_duplicate_report_id_is_rejected_by_shared_evidence_contract():
    model = BF2Model()
    posterior = filter_report(model, initial_belief(), "W", 0, "sample-0")
    assert posterior.problem.prior_weights.sum() == pytest.approx(1)
    with pytest.raises(ValueError, match="reused"):
        filter_report(model, posterior, "W", 0, "sample-0")


def test_matched_and_extreme_regimes_compare_common_objective_and_budget():
    model = BF2Model()
    matched = evaluate_regime(model, 0.1, 0.1)
    assert set(matched) == {"no_study", "fixed_sampling", "fixed_calibration", "static_staged", "adaptive"}
    assert matched["fixed_sampling"]["expected_studies"] == pytest.approx(2)
    assert matched["fixed_calibration"]["expected_studies"] == pytest.approx(2)
    for result in matched.values():
        assert result["gross_score"] + result["mean_regret"] == pytest.approx(1)
        assert result["net_score"] == pytest.approx(result["gross_score"] - 0.03 * result["expected_studies"])
        assert 0 <= result["expected_studies"] <= 2
        assert all(0 <= result["coverage"][str(t)] <= 1 for t in (1, 2))
    assert matched["adaptive"]["net_score"] >= max(x["net_score"] for x in matched.values()) - 1e-12
    extreme = evaluate_regime(model, 0.5, 0.5)
    for result in extreme.values():
        assert result["gross_score"] == pytest.approx(0.5)


def test_no_product_signal_gives_no_correct_classification_gain():
    model = BF2Model(no_signal=True)
    outcomes = evaluate_regime(model, 0.1, 0.1)
    assert outcomes["adaptive"]["expected_studies"] == pytest.approx(0)
    for result in outcomes.values():
        assert result["gross_score"] == pytest.approx(0.5)


def test_equal_spend_sensitivity_preserves_adaptive_decisions_and_reports_extra_information():
    outcomes = evaluate_regime(BF2Model(), 0.1, 0.1, include_equal_spend=True)
    adaptive = outcomes["adaptive"]
    forced = outcomes["adaptive_equal_spend"]
    assert forced["expected_studies"] == pytest.approx(2)
    assert forced["gross_score"] == pytest.approx(adaptive["gross_score"])
    assert forced["research_brier_t2"] <= forced["brier"]["2"] + 1e-12


def test_static_adaptive_is_at_least_as_good_as_static_staged():
    outcomes = evaluate_regime(BF2Model(p_x=0, p_h=0), 0, 0)
    assert outcomes["adaptive"]["net_score"] >= outcomes["static_staged"]["net_score"] - 1e-12


def test_impossible_report_and_zero_probability_prediction_fail_opening_no_data():
    model = BF2Model(calibration_accuracy=1.0)
    with pytest.raises(ValueError, match="no support"):
        filter_report(model, initial_belief(np.array([0.5, 0, 0.5, 0])), "C", 1, "impossible")
    assert categorical_log_loss(np.array([0.5, 0.5]), np.array([1.0, 0.0])) == math.inf


def test_static_staged_value_matches_an_independent_analytic_calculation():
    low_cdf = 0.5 * (1 + math.erf(-math.log(0.8) / (0.4 * math.sqrt(2))))
    high_cdf = 0.5 * (1 + math.erf(-math.log(2.5) / (0.4 * math.sqrt(2))))
    useful_report_probability = low_cdf + high_cdf
    expected_gain = 0.4 * (low_cdf - high_cdf) / 3
    expected_cost = 0.03 * (1 + useful_report_probability)
    outcome = evaluate_regime(BF2Model(p_x=0, p_h=0), 0, 0)["static_staged"]
    assert outcome["net_score"] == pytest.approx(0.5 + expected_gain - expected_cost, abs=1e-12)
