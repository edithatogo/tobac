"""Information versus implementation, with explicit state-action kernels.

Scenario uptake curves are not fitted Innovate outputs. Realised actions retain
all components of the original payoff, including resource consequences.
"""

from __future__ import annotations

import numpy as np

from tobac._core import DecisionProblem


def implementation_values(problem: DecisionProblem, kernel) -> DecisionProblem:
    n, a = problem.values.shape
    k = np.asarray(kernel, float)
    if (
        k.shape != (n, a, a)
        or not np.isfinite(k).all()
        or (k < 0).any()
        or not np.allclose(k.sum(axis=2), 1, rtol=0, atol=1e-12)
    ):
        raise ValueError("State/intended/realised probabilities must be stochastic")
    return DecisionProblem(
        np.einsum("sij,sj->si", k, problem.values),
        problem.action_names,
        problem.value_unit,
        problem.prior_weights,
    )


def adoption_kernel(problem: DecisionProblem, uptake, reference_action: int | None = None) -> np.ndarray:
    n, a = problem.values.shape
    u = np.broadcast_to(np.asarray(uptake, float), (n,))
    if not np.isfinite(u).all() or (u < 0).any() or (u > 1).any():
        raise ValueError("Uptake must be a probability")
    ref = (
        int(np.argmax(problem.prior_weights @ problem.values))
        if reference_action is None
        else reference_action
    )
    if isinstance(ref, bool) or not isinstance(ref, (int, np.integer)) or not 0 <= ref < a:
        raise ValueError("Invalid realised reference action")
    k = np.broadcast_to(np.eye(a), (n, a, a)).copy() * u[:, None, None]
    k[:, :, ref] += 1 - u[:, None]
    return k


def discounted_uptake(uptake, time_weights) -> float:
    u = np.asarray(uptake, float)
    w = np.asarray(time_weights, float)
    if (
        u.ndim != 1
        or not len(u)
        or w.shape != u.shape
        or not np.isfinite(u).all()
        or not np.isfinite(w).all()
        or (u < 0).any()
        or (u > 1).any()
        or (w < 0).any()
        or w.sum() <= 0
    ):
        raise ValueError("Matching uptake probabilities and nonnegative time weights required")
    return float(u @ w / w.sum())


def decomposition(problem: DecisionProblem, current_kernel) -> dict:
    # Centre before combining cells to avoid an irrelevant state-specific offset.
    centred = DecisionProblem(
        problem.values - problem.values[:, 0, None],
        problem.action_names,
        problem.value_unit,
        problem.prior_weights,
    )
    actual = implementation_values(centred, current_kernel)
    p = problem.prior_weights
    v00 = float(np.max(p @ actual.values))
    v10 = float(p @ np.max(actual.values, axis=1))
    v01 = float(np.max(p @ centred.values))
    v11 = float(p @ np.max(centred.values, axis=1))
    return {
        "current_information_current_implementation": v00,
        "perfect_information_current_implementation": v10,
        "current_information_perfect_implementation": v01,
        "perfect_information_perfect_implementation": v11,
        "information_at_current_implementation": v10 - v00,
        "implementation_at_current_information": v01 - v00,
        "joint_gain": v11 - v00,
        "interaction": v11 - v10 - v01 + v00,
        "value_unit": problem.value_unit,
    }
