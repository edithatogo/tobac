"""Structure-only information, distinguished from joint parameter clairvoyance."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np

from tobac._core import DecisionProblem, exact_evpi


def structure_value(models: Mapping[str, DecisionProblem], probabilities: Sequence[float]) -> dict:
    """Resolve model identity while integrating residual parameters within it.

    Probabilities are explicitly supplied modelling assumptions, not inferred
    probabilities for political viewpoints. Use separate envelopes when such
    probabilities cannot be defended. Action labels, order and units must match.
    """
    if not models or any(not isinstance(k, str) or not k for k in models):
        raise ValueError("Named structures required")
    problems = list(models.values())
    first = problems[0]
    if any(p.action_names != first.action_names or p.value_unit != first.value_unit for p in problems):
        raise ValueError("Same ordered feasible actions and value units required")
    w = np.asarray(probabilities, float)
    if (
        w.shape != (len(problems),)
        or not np.isfinite(w).all()
        or (w < 0).any()
        or not np.isclose(w.sum(), 1, rtol=0, atol=1e-12)
    ):
        raise ValueError("Explicit normalised model probabilities required")
    means = np.array([p.prior_weights @ (p.values - p.values[:, 0, None]) for p in problems])
    grouped = DecisionProblem(means, first.action_names, first.value_unit, w)
    structure_only = exact_evpi(grouped)
    remaining = float(w @ np.array([exact_evpi(p) for p in problems]))
    return {
        "structure_only": structure_only,
        "remaining_parameter_value": remaining,
        "joint_perfect": structure_only + remaining,
        "value_unit": first.value_unit,
        "model_ids": list(models),
        "model_probabilities": w.tolist(),
        "estimand": "value of model identity only, residual parameters averaged before maximisation",
    }
