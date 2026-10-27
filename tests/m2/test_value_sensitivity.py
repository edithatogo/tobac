"""Check value disagreement separately from finite empirical-state uncertainty."""

import numpy as np
import pytest

from tobac._core import exact_evpi
from tobac.information import evaluate, scalar_oracle
from tobac.value_sensitivity import Consequences, ValueWeights, box_optima, crime_thresholds, optimal_indices


def test_weighted_consequences_preserve_signed_harm_and_resource_cost() -> None:
    table = Consequences(
        np.array([[0, 2], [0, 1.0]]),
        np.array([[0, 1], [0, -1.0]]),
        np.array([[0, 0.5], [0, 0.5]]),
    )
    problem = table.problem(np.array([0.8, 0.2]), ValueWeights(1, 2, 3))
    assert np.allclose(problem.values[:, 1], [-1.5, 1.5])
    assert optimal_indices(problem.prior_weights @ problem.values) == (0,)
    assert exact_evpi(problem) == pytest.approx(0.3)
    channel = np.eye(2)
    assert evaluate(problem, channel)["evsi"] == pytest.approx(scalar_oracle(problem, channel))


def test_expected_components_and_readonly_copy() -> None:
    health = np.array([[0, 2], [0, 1.0]])
    table = Consequences(health, np.zeros((2, 2)), np.zeros((2, 2)))
    health[:] = 0
    assert table.expected(np.array([0.8, 0.2]))[1, 0] == pytest.approx(1.8)
    with pytest.raises(ValueError, match="read-only"):
        table.health[0, 0] = 2


@pytest.mark.parametrize("weights", [(0, 0, 0), (True, 1, 1), (1, -1, 1), (1, np.nan, 1)])
def test_invalid_value_weights_are_rejected(weights) -> None:
    with pytest.raises(ValueError, match="weights"):
        ValueWeights(*weights)


@pytest.mark.parametrize("shape", [(2,), (2, 0), (1, 2, 1)])
def test_misaligned_or_empty_consequences_are_rejected(shape) -> None:
    with pytest.raises(ValueError, match="consequence"):
        Consequences(np.zeros(shape), np.zeros((2, 2)), np.zeros((2, 2)))


def test_nonfinite_and_negative_cost_rejected() -> None:
    with pytest.raises(ValueError, match="consequence"):
        Consequences(np.ones((2, 2)), np.full((2, 2), np.inf), np.zeros((2, 2)))
    with pytest.raises(ValueError, match="resource"):
        Consequences(np.ones((2, 2)), np.zeros((2, 2)), -np.ones((2, 2)))


def test_prior_is_validated_and_normalised_by_existing_contract() -> None:
    table = Consequences(np.array([[0, 2.0], [0, 1.0]]), np.zeros((2, 2)), np.zeros((2, 2)))
    assert np.allclose(table.expected(np.array([8.0, 2.0]))[:, 0], [0, 1.8])
    with pytest.raises(ValueError, match="Prior weights"):
        table.expected(np.array([-1.0, 2.0]))


def test_true_switch_is_reported_but_dominated_pair_tie_is_not() -> None:
    means = np.array([[1, 1, 0], [0, 0, 0.0]])
    assert crime_thresholds(means, 1, (0, 2)) == pytest.approx([1])
    assert crime_thresholds(np.vstack([means, [2, 0, 0]]), 1, (0, 2)) == []
    assert optimal_indices([0, 0]) == (0, 1)


def test_continuous_box_is_not_grid_frequency_or_marginal_union() -> None:
    means = np.array([[1, 1, 0], [0, 0, 0.0]])
    assert box_optima(means, (0, 0.5), (0, 4)) == (0,)
    assert box_optima(means, (0, 2), (0, 4)) == ()
    assert box_optima(np.zeros((2, 3)), (0, 4), (0, 4)) == (0, 1)
    assert crime_thresholds(np.zeros((2, 3)), 1, (0, 4)) == []


@pytest.mark.parametrize("bounds", [(-1, 2), (2, 1), (0, np.inf)])
def test_bad_normative_support_rejected(bounds) -> None:
    with pytest.raises(ValueError, match="bounds"):
        box_optima(np.zeros((2, 3)), bounds, (0, 1))


def test_invalid_expected_vectors_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        optimal_indices([np.nan])
    with pytest.raises(ValueError, match="three"):
        box_optima(np.zeros((2, 2)), (0, 1), (0, 1))


def test_reference_can_be_optimal_between_two_distinct_switches() -> None:
    means = np.array([[0, 0, 0], [1, 2, 0], [-3, -2, 0.0]])
    assert crime_thresholds(means, 1, (0, 2)) == pytest.approx([0.5, 1.5])
    assert optimal_indices(means @ [1, -1, -1]) == (0,)


def test_continuous_certificate_agrees_with_independent_interior_grid() -> None:
    means = np.array([[2, 0.1, 0.2], [0, -0.1, 0.3], [1, 1, 1.0]])
    certificate = box_optima(means, (0, 4), (0, 4))
    interior = set(range(3))
    for crime in np.linspace(0, 4, 17):
        for resource in np.linspace(0, 4, 19):
            values = [h - crime * c - resource * r for h, c, r in means]
            interior.intersection_update(i for i, v in enumerate(values) if abs(v - max(values)) < 1e-11)
    assert certificate == tuple(sorted(interior))


def test_value_changes_do_not_update_prior_or_consequences() -> None:
    table = Consequences(np.array([[0, 2.0], [0, 1.0]]), np.zeros((2, 2)), np.ones((2, 2)))
    prior = np.array([0.8, 0.2])
    first = table.problem(prior, ValueWeights(1, 2, 3))
    second = table.problem(prior, ValueWeights(2, 4, 6))
    assert np.array_equal(first.prior_weights, second.prior_weights)
    assert np.array_equal(prior, [0.8, 0.2])
    assert np.allclose(second.values, 2 * first.values)
    assert exact_evpi(second) == pytest.approx(2 * exact_evpi(first))


def test_target_information_is_unchanged_by_value_weights() -> None:
    table = Consequences(np.array([[0, 2.0], [0, 1.0]]), np.zeros((2, 2)), np.ones((2, 2)))
    prior = np.array([0.8, 0.2])
    channel = np.array([[0.8, 0.3], [0.2, 0.7]])
    targets = {"state": np.array([0, 1])}
    first = evaluate(table.problem(prior), channel, targets)["targets"]
    second = evaluate(table.problem(prior, ValueWeights(1, 4, 0)), channel, targets)["targets"]
    assert first == second


def test_reference_weights_match_the_existing_retail_decision_contract() -> None:
    from pathlib import Path  # noqa: PLC0415 -- Scoped reference-parity fixture.

    from tobac.regulation import load_config  # noqa: PLC0415 -- Scoped reference-parity fixture.
    from tobac.retail_case import build_retail_states, retail_components, retail_problem  # noqa: PLC0415

    base = load_config(Path(__file__).parents[2] / "configs/regulatory.json")
    states, prior, config = build_retail_states(base, quit_points=1)
    components = retail_components(states, config, lawful_replacement=0.5)
    table = Consequences(
        components["health_gain"], components["criminal_harm_change"], components["resource_cost"]
    )
    assert np.array_equal(
        table.problem(prior).values, retail_problem(states, prior, config, lawful_replacement=0.5).values
    )
