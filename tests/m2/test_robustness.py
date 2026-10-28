"""Independent finite checks for post-primary assumption challenges."""

import numpy as np
import pytest

from tobac._core import DecisionProblem
from tobac.information import evaluate, joint_likelihood, scalar_oracle
from tobac.robustness import binary_prior, dependent_joint, frechet_prior, garble, tie_regret


def test_binary_reweighting_preserves_independent_other_margin() -> None:
    p = binary_prior(np.ones(4), np.array([False, False, True, True]), 0.8)
    assert np.allclose(p, [0.1, 0.1, 0.4, 0.4])
    assert p[[0, 2]].sum() == pytest.approx(0.5)


@pytest.mark.parametrize("probability", [True, -0.1, 0, 1, np.nan])
def test_invalid_probability_rejected(probability) -> None:
    with pytest.raises(ValueError, match=r"interval|support"):
        binary_prior(np.ones(2), np.array([False, True]), probability)


def test_impossible_support_and_bad_masks_rejected() -> None:
    with pytest.raises(ValueError, match="support"):
        binary_prior(np.array([1.0, 0]), np.array([False, True]), 0.8)
    with pytest.raises(ValueError, match="Boolean"):
        binary_prior(np.ones(2), np.array([0, 1]), 0.8)
    with pytest.raises(ValueError, match="Prior weights"):
        binary_prior(np.array([-1.0, 2]), np.array([False, True]), 0.8)


@pytest.mark.parametrize(
    ("strength", "expected"), [(0, [0.25] * 4), (1, [0.5, 0, 0, 0.5]), (-1, [0, 0.5, 0.5, 0])]
)
def test_frechet_coupling_matches_independent_binary_oracle(strength, expected) -> None:
    p = frechet_prior(
        np.ones(4), np.array([False, False, True, True]), np.array([False, True, False, True]), strength
    )
    assert np.allclose(p, expected)
    assert p[:2].sum() == pytest.approx(0.5)
    assert p[[0, 2]].sum() == pytest.approx(0.5)


def test_unequal_frechet_margins_and_strength_domain() -> None:
    p = np.array([0.16, 0.64, 0.04, 0.16])
    first = np.array([False, False, True, True])
    second = np.array([False, True, False, True])
    q = frechet_prior(p, first, second, -0.8)
    assert q[first].sum() == pytest.approx(0.2)
    assert q[second].sum() == pytest.approx(0.8)
    assert q[first & second].sum() == pytest.approx(0.032)
    with pytest.raises(ValueError, match="interval"):
        frechet_prior(p, first, second, 1.1)


def test_common_uniform_joint_preserves_each_conditional_margin() -> None:
    a = np.array([[0.8, 0.1], [0.2, 0.9]])
    b = np.array([[0.3, 0.7], [0.7, 0.3]])
    assert np.allclose(dependent_joint((a, b), 0), joint_likelihood(a, b))
    result = dependent_joint((a, b), 1)
    assert np.allclose(result[:, 0], [0.3, 0.5, 0, 0.2])
    grid = result.reshape(2, 2, 2)
    assert np.allclose(grid.sum(axis=1), a)
    assert np.allclose(grid.sum(axis=0), b)
    assert np.allclose(dependent_joint((a,), 0.8), a)


def test_garbling_reduces_value_and_has_uninformative_endpoint() -> None:
    p = np.array([0.8, 0.2])
    problem = DecisionProblem(np.array([[0, -1.5], [0, 1.5]]), ["a", "b"], "score", p)
    likelihood = np.eye(2)
    full = evaluate(problem, likelihood)["evsi"]
    reduced = garble(likelihood, p, 0.5)
    assert 0 < evaluate(problem, reduced)["evsi"] < full
    assert evaluate(problem, reduced)["evsi"] == pytest.approx(scalar_oracle(problem, reduced))
    assert np.allclose(garble(likelihood, p, 0), [[0.8, 0.8], [0.2, 0.2]])
    assert np.allclose(garble(likelihood, p, 1), likelihood)
    with pytest.raises(ValueError, match="interval"):
        garble(likelihood, p, -1)


def test_regret_reports_range_over_all_original_ties() -> None:
    assert tie_regret(np.array([0.0, 2.0, 1.0]), (0, 2)) == pytest.approx((1, 2))
    assert tie_regret(np.array([0.0, 2.0, 1.0]), (1,)) == pytest.approx((0, 0))
    with pytest.raises(ValueError, match="baseline optima"):
        tie_regret(np.zeros(2), ())


def test_frechet_endpoint_roundoff_does_not_create_negative_mass() -> None:
    p = np.array([0.16, 0.64, 0.04, 0.16])
    first = np.array([False, False, True, True])
    second = np.array([False, True, False, True])
    result = frechet_prior(p, first, second, -1)
    assert (result >= 0).all()
    assert result[first].sum() == pytest.approx(0.2)
    assert result[second].sum() == pytest.approx(0.8)
