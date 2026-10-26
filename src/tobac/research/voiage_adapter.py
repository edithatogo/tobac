"""Exact weighted adapter to Voiage EVPI; installed execution is fail-closed.

The transform is valid for expected-value EVPI ONLY. It is not a new PSA sample,
a probability model, or a valid input to risk/entropy/CEAC calculations.
"""

from __future__ import annotations

from importlib.metadata import version
from typing import TYPE_CHECKING, cast
lazy from collections.abc import Sequence

import numpy as np

from tobac._core import DecisionProblem

if TYPE_CHECKING:
    from tobac._typing import FloatArray, Report


def uniform_equivalent(problem: DecisionProblem) -> FloatArray:
    """n*p_s*(V_sa-V_s0) converts weighted EVPI to uniform EVPI exactly.

    Zero-weight states remain zero rows. No integer replication, rounding or
    resampling is used. Values retain the input unit and are already scaled.
    """
    x = (
        len(cast("FloatArray", problem.prior_weights)) * cast("FloatArray", problem.prior_weights)[:, None]
    ) * (problem.values - problem.values[:, 0, None])
    if not np.isfinite(x).all():
        msg = "Weighted EVPI transform overflow"
        raise ValueError(msg)
    return x


def partition_problem(problem: DecisionProblem, labels: Sequence[object]) -> DecisionProblem:
    """Collapse each finite partition group before computing expected-value information."""
    if len(labels) != len(cast("FloatArray", problem.prior_weights)):
        msg = "One partition label per state required"
        raise ValueError(msg)
    groups: dict[object, list[int]] = {}
    for i, label in enumerate(labels):
        try:
            groups.setdefault(label, []).append(i)
        except TypeError as exc:
            msg = "Partition labels must be hashable"
            raise ValueError(msg) from exc
    p = cast("FloatArray", problem.prior_weights)
    v = problem.values - problem.values[:, 0, None]
    masses: list[float] = []
    means: list[FloatArray] = []
    for indices in groups.values():
        mass = float(p[indices].sum())
        if mass > 0:
            masses.append(mass)
            means.append(p[indices] @ v[indices] / mass)
    return DecisionProblem(np.asarray(means), problem.action_names, problem.value_unit, np.asarray(masses))


def installed_evpi(problem: DecisionProblem, *, expected_version: str = "2.2.0") -> Report:
    """Execute the actual released API; an unavailable package is an error."""
    installed = version("voiage")
    if installed != expected_version:
        msg = f"Unqualified voiage version {installed}; expected {expected_version}"
        raise RuntimeError(msg)
    from voiage.methods.basic import evpi  # pyright: ignore[reportMissingModuleSource]  # Optional runtime probe.  # noqa: PLC0415  # Keep optional dependencies and backend selection lazy.

    value = float(evpi(uniform_equivalent(problem)))
    if not np.isfinite(value):
        msg = "Voiage returned a nonfinite value"
        raise ArithmeticError(msg)
    return {
        "value": value,
        "value_unit": problem.value_unit,
        "voiage_version": installed,
        "backend": "voiage.methods.basic.evpi",
        "adapter": "exact nonnegative weighted-contrast transform",
        "population_scaling": "none; input already carries the decision scale",
    }


def installed_partial(problem: DecisionProblem, labels: Sequence[object]) -> Report:
    """Evaluate the declared finite-partition EVPPI through the installed backend."""
    result = installed_evpi(partition_problem(problem, labels))
    result["estimand"] = "exact finite-partition EVPPI; not continuous regression EVPPI"
    return result
