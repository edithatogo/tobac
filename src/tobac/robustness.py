"""Finite assumption challenges; no observations, fitting or social preferences."""

from __future__ import annotations

import math
from itertools import product
from numbers import Real
from typing import TYPE_CHECKING, cast

import numpy as np

from tobac._core import DecisionProblem
from tobac.information import joint_likelihood, validate_likelihood

if TYPE_CHECKING:
    from collections.abc import Sequence

    from numpy.typing import NDArray

    from tobac._typing import FloatArray


def _interval(value: float, lower: float, upper: float) -> None:
    if (
        isinstance(value, bool)
        or not isinstance(value, Real)
        or not math.isfinite(value)
        or not lower <= value <= upper
    ):
        msg = "Finite challenge parameter outside declared interval"
        raise ValueError(msg)


def _prior(prior: FloatArray) -> FloatArray:
    p = np.asarray(prior, float)
    if p.ndim != 1:
        msg = "One-dimensional prior required"
        raise ValueError(msg)
    return cast("FloatArray", DecisionProblem(np.zeros((len(p), 1)), ("a",), "score", p).prior_weights)


def _mask(high: NDArray[np.bool_], p: FloatArray) -> None:
    if high.dtype != np.dtype(bool) or high.shape != p.shape:
        msg = "Boolean state-aligned mask required"
        raise ValueError(msg)


def binary_prior(prior: FloatArray, high: NDArray[np.bool_], probability: float) -> FloatArray:
    """Change a binary marginal; retain within-stratum conditional prior weights."""
    _interval(probability, 0, 1)
    p = _prior(prior)
    _mask(high, p)
    mass = float(p[high].sum())
    if not 0 < probability < 1 or not 0 < mass < 1:
        msg = "Positive mass on both support strata required"
        raise ValueError(msg)
    return p * np.where(high, probability / mass, (1 - probability) / (1 - mass))


def frechet_prior(
    prior: FloatArray, first: NDArray[np.bool_], second: NDArray[np.bool_], strength: float
) -> FloatArray:
    """Replace binary joint association toward a Fréchet bound, preserving margins.

    Strength zero targets independence. It is a fraction of the feasible joint-
    probability interval, not Pearson correlation. No unsupported state is invented.
    """
    _interval(strength, -1, 1)
    p = _prior(prior)
    _mask(first, p)
    _mask(second, p)
    a, b = float(p[first].sum()), float(p[second].sum())
    independent = a * b
    endpoint = min(a, b) if strength >= 0 else max(0.0, a + b - 1)
    joint = independent + abs(strength) * (endpoint - independent)
    desired = np.maximum(np.array([[1 - a - b + joint, b - joint], [a - joint, joint]]), 0)
    result = p.copy()
    for i, j in product(range(2), repeat=2):
        selected = (first == bool(i)) & (second == bool(j))
        mass = float(p[selected].sum())
        if mass <= 0:
            msg = "All binary joint support cells require positive prior mass"
            raise ValueError(msg)
        result[selected] *= desired[i][j] / mass
    return _prior(result)


def dependent_joint(channels: Sequence[FloatArray], strength: float) -> FloatArray:
    """Mix independent and common-uniform ordered-bin reports conditional on states."""
    _interval(strength, 0, 1)
    if not channels:
        msg = "At least one report channel required"
        raise ValueError(msg)
    independent = joint_likelihood(*channels)
    if strength == 0 or len(channels) == 1:
        return independent
    cumulative = [np.vstack([np.zeros((1, c.shape[1])), np.cumsum(c, axis=0)]) for c in channels]
    common = np.empty_like(independent)
    for row, indices in enumerate(product(*(range(c.shape[0]) for c in channels))):
        upper = np.minimum.reduce([c[index + 1] for c, index in zip(cumulative, indices, strict=True)])
        lower = np.maximum.reduce([c[index] for c, index in zip(cumulative, indices, strict=True)])
        common[row] = np.maximum(upper - lower, 0)
    return validate_likelihood((1 - strength) * independent + strength * common, independent.shape[1])


def garble(likelihood: FloatArray, prior: FloatArray, retained: float) -> FloatArray:
    """Mix a report with an unobserved independent prior-predictive replacement."""
    _interval(retained, 0, 1)
    p = _prior(prior)
    channel = validate_likelihood(likelihood, len(p))
    marginal = channel @ p
    return retained * channel + (1 - retained) * marginal[:, None]


def tie_regret(expected: FloatArray, baseline_optima: Sequence[int]) -> tuple[float, float]:
    """Return current-objective regret range over all baseline-co-optimal actions."""
    values = np.asarray(expected, float)
    if (
        values.ndim != 1
        or not len(values)
        or not np.isfinite(values).all()
        or not baseline_optima
        or any(
            isinstance(i, bool) or not isinstance(cast("object", i), int) or not 0 <= i < len(values)
            for i in baseline_optima
        )
    ):
        msg = "Finite action values and valid nonempty baseline optima required"
        raise ValueError(msg)
    regret = values.max() - values[list(baseline_optima)]
    return float(regret.min()), float(regret.max())
