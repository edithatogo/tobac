"""Exact two-stage static-world research with matched action timing.

While waiting, retain the best action under currently available information.
After pilot, both fixed and adaptive designs may change action, and change it
again after follow-up. Remaining fractions refer to one already-valued horizon;
no extra population multiplication or implicit lifetime extrapolation occurs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast
lazy from collections.abc import Sequence

import numpy as np
lazy from numpy.typing import ArrayLike

from tobac.information import validate_likelihood
lazy from tobac._core import DecisionProblem
lazy from tobac.evidence import Belief

if TYPE_CHECKING:
    from tobac._typing import FloatArray, Report

    from .portfolio import Costs, Source


# Named bounds preserve the existing scientific/data contract.
MAX_JOINT_CELLS = 30000000


def two_stage(  # noqa: PLR0913  # Preserve explicit dimensioned inputs and the established API.
    problem: DecisionProblem,
    pilot: ArrayLike,
    followup: ArrayLike,
    *,
    pilot_cost: float,
    followup_cost: float,
    pilot_remaining: float = 1.0,
    followup_remaining: float = 1.0,
    joint: ArrayLike | None = None,
) -> Report:
    """Compare fixed and adaptive two-stage designs with matched action timing."""
    n = len(cast("FloatArray", problem.prior_weights))
    a = validate_likelihood(pilot, n)
    b = validate_likelihood(followup, n)
    raw = [pilot_cost, followup_cost, pilot_remaining, followup_remaining]
    if any(isinstance(x, (bool, np.bool_)) for x in raw):
        msg = "Numeric costs/times cannot be booleans"
        raise ValueError(msg)
    numbers = np.asarray(raw, float)
    if (
        not np.isfinite(numbers).all()
        or min(pilot_cost, followup_cost) < 0
        or not 0 <= followup_remaining <= pilot_remaining <= 1
    ):
        msg = "Nonnegative costs and chronological remaining fractions required"
        raise ValueError(msg)
    if len(a) * len(b) * n > MAX_JOINT_CELLS:
        msg = "Exact staged outcome tensor exceeds memory contract"
        raise ValueError(msg)
    j: FloatArray = a[:, None, :] * b[None, :, :] if joint is None else np.asarray(joint, float)
    if (
        j.shape != (len(a), len(b), n)
        or not np.isfinite(j).all()
        or (j < 0).any()
        or not np.allclose(j.sum(axis=1), a, atol=1e-11, rtol=0)
        or not np.allclose(j.sum(axis=0), b, atol=1e-11, rtol=0)
    ):
        msg = "Joint report must match both declared marginals"
        raise ValueError(msg)
    p = cast("FloatArray", problem.prior_weights)
    baseline = int(np.argmax(p @ (problem.values - problem.values[:, 0, None])))
    contrasts = problem.values - problem.values[:, baseline, None]
    q = a @ p
    branches: list[Report] = []
    for y, prob in enumerate(q):
        if prob <= 0:
            continue
        post = a[y] * p / prob
        immediate = float(np.max(post @ contrasts))
        conditional: FloatArray = (j[y] * p[None, :] / float(prob)) @ contrasts
        future = float(conditional.max(axis=1).sum())
        stop = pilot_remaining * immediate
        go = (pilot_remaining - followup_remaining) * immediate + followup_remaining * future - followup_cost
        branches.append(
            {
                "pilot_outcome": y,
                "probability": float(prob),
                "stop_value": stop,
                "continue_value": go,
                "continue": bool(go > stop),
                "conditional_gross_increment": followup_remaining * (future - immediate),
            }
        )
    only = -pilot_cost + sum(x["probability"] * x["stop_value"] for x in branches)
    fixed = -pilot_cost + sum(x["probability"] * x["continue_value"] for x in branches)
    adaptive = -pilot_cost + sum(
        x["probability"] * max(x["stop_value"], x["continue_value"]) for x in branches
    )
    return {
        "no_study_enbs": 0.0,
        "pilot_only_enbs": only,
        "fixed_both_enbs": fixed,
        "adaptive_enbs": adaptive,
        "best_with_no_study": max(0.0, adaptive),
        "adaptive_increment_over_best_fixed": adaptive - max(only, fixed),
        "continue_probability": sum(x["probability"] for x in branches if x["continue"]),
        "expected_followup_cost": followup_cost * sum(x["probability"] for x in branches if x["continue"]),
        "pilot_cost": pilot_cost,
        "followup_incremental_cost": followup_cost,
        "pilot_remaining": pilot_remaining,
        "followup_remaining": followup_remaining,
        "value_unit": problem.value_unit,
        "branches": branches,
        "scope": "exact static-world two-stage policy; no forced study and no automatic state dynamics",
    }


def staged_portfolio(  # noqa: PLR0913  # Preserve explicit dimensioned inputs and the established API.
    belief: Belief,
    pilot_sources: Sequence[Source],
    followup_sources: Sequence[Source],
    costs: Costs,
    *,
    existing_assets: Sequence[str] = (),
    pilot_remaining: float = 1.0,
    followup_remaining: float = 1.0,
    followup_cost_multiplier: float = 1.0,
    joint: ArrayLike | None = None,
) -> Report:
    """Evidence-aware wrapper; followup charges only newly acquired shared assets.

    Stage reports must represent distinct prospective underlying data. An explicit
    stage-level joint tensor is required when conditional independence is false.
    """
    from .portfolio import joint_report, portfolio_value  # noqa: PLC0415  # Keep optional dependencies and backend selection lazy.

    all_sources = list(pilot_sources) + list(followup_sources)
    # Reuse the shared evidence/identity validation, including rejection of D0 reuse.
    for sources in (pilot_sources, followup_sources):
        portfolio_value(belief, sources, costs, existing_assets=existing_assets)
    data = [d for source in all_sources for d in source.data_ids]
    if len(data) != len(set(data)):
        msg = "Stages cannot rebuy overlapping data"
        raise ValueError(msg)
    if (
        isinstance(followup_cost_multiplier, (bool, np.bool_))
        or not np.isfinite(followup_cost_multiplier)
        or followup_cost_multiplier < 0
    ):
        msg = "Finite nonnegative followup price multiplier required"
        raise ValueError(msg)
    first = costs.price(pilot_sources, existing_assets)
    extra = costs.price(all_sources, existing_assets) - first
    n = len(belief.state_ids)
    result = two_stage(
        belief.problem,
        joint_report(pilot_sources, n),
        joint_report(followup_sources, n),
        pilot_cost=first,
        followup_cost=extra * followup_cost_multiplier,
        pilot_remaining=pilot_remaining,
        followup_remaining=followup_remaining,
        joint=joint,
    )
    result.update(
        existing_data_ids=list(belief.used_data_ids),
        future_data_ids=data,
        dependence="explicit stage joint tensor"
        if joint is not None
        else "independent given complete shared state",
    )
    return result
