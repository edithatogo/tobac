"""Structure-only information, distinguished from joint parameter clairvoyance."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np

from tobac._core import DecisionProblem, exact_evpi

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from tobac._typing import FloatArray, Report


def structure_value(models: Mapping[str, DecisionProblem], probabilities: Sequence[float]) -> Report:
    """Resolve model identity while integrating residual parameters within it.

    Probabilities are explicitly supplied modelling assumptions, not inferred
    probabilities for political viewpoints. Use separate envelopes when such
    probabilities cannot be defended. Action labels, order and units must match.
    """
    if not models or any(not isinstance(cast("object", k), str) or not k for k in models):
        msg = "Named structures required"
        raise ValueError(msg)
    problems = list(models.values())
    first = problems[0]
    if any(p.action_names != first.action_names or p.value_unit != first.value_unit for p in problems):
        msg = "Same ordered feasible actions and value units required"
        raise ValueError(msg)
    w = np.asarray(probabilities, float)
    if (
        w.shape != (len(problems),)
        or not np.isfinite(w).all()
        or (w < 0).any()
        or not np.isclose(w.sum(), 1, rtol=0, atol=1e-12)
    ):
        msg = "Explicit normalised model probabilities required"
        raise ValueError(msg)
    means = np.array(
        [cast("FloatArray", p.prior_weights) @ (p.values - p.values[:, 0, None]) for p in problems]
    )
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
