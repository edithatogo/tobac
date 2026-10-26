"""Source-preserving extraction of the verified predecessor numerical/physical core.

Numerical definitions retain the original AST after explicit static maintenance.
The original source bytes and permitted changes are verified by scripts/verify.py. See
integration/baseline.json for source archive, commit and per-function hashes.
Optional historical health/fiscal engines remain in the preserved full archive.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import cast
lazy from collections.abc import Sequence

import numpy as np

lazy from tobac._typing import FloatArray

# Named bounds preserve the existing scientific/data contract.
MATRIX_NDIM = 2


class LibraryUnavailable(RuntimeError):  # noqa: N818  # Preserve the inherited public exception name and source provenance.
    """The requested external backend could not be loaded; no silent fallback."""


@dataclass(frozen=True)
class DecisionProblem:
    values: FloatArray
    action_names: Sequence[str]
    value_unit: str
    prior_weights: FloatArray | None = None

    def __post_init__(self) -> None:
        values = np.array(self.values, dtype=float, copy=True)
        names = tuple(self.action_names)
        if values.ndim != MATRIX_NDIM or min(values.shape) < 1 or not np.isfinite(values).all():
            raise ValueError("Values must be a non-empty finite state-by-action matrix")  # noqa: EM101, TRY003  # Preserve the byte/AST-verified inherited exception contract.
        if len(names) != values.shape[1] or len(set(names)) != len(names) or any(not n for n in names):
            raise ValueError("Action names must be unique and match value columns")  # noqa: EM101, TRY003  # Preserve the byte/AST-verified inherited exception contract.
        if not isinstance(cast("object", self.value_unit), str) or not self.value_unit.strip():
            raise ValueError("Declare a value unit")  # noqa: EM101, TRY003  # Preserve the byte/AST-verified inherited exception contract.
        weights = (
            np.ones(values.shape[0])
            if self.prior_weights is None
            else np.array(self.prior_weights, dtype=float, copy=True)
        )
        if (
            weights.shape != (values.shape[0],)
            or not np.isfinite(weights).all()
            or (weights < 0).any()
            or not weights.sum() > 0
        ):
            raise ValueError("Prior weights must be nonnegative, finite and have positive mass")  # noqa: EM101, TRY003  # Preserve the byte/AST-verified inherited exception contract.
        if not math.isfinite(float(weights.sum())):
            raise ValueError("Weight sum overflow")  # noqa: EM101, TRY003  # Preserve the byte/AST-verified inherited exception contract.
        weights /= weights.sum()
        values.setflags(write=False)
        weights.setflags(write=False)
        object.__setattr__(self, "values", values)
        object.__setattr__(self, "action_names", names)
        object.__setattr__(self, "prior_weights", weights)


def exact_evpi(problem: DecisionProblem, backend: str = "reference") -> float:
    """Exact EVPI under the finite joint prior; values are already population-scaled."""
    if backend == "voiage":
        if not np.allclose(
            cast("FloatArray", problem.prior_weights),
            1 / len(cast("FloatArray", problem.prior_weights)),
            rtol=0,
            atol=1e-14,
        ):
            raise ValueError(  # noqa: TRY003  # Preserve the byte/AST-verified inherited exception contract.
                "This voiage adapter supports equally weighted states only; no implicit resampling"  # noqa: EM101  # Preserve the byte/AST-verified inherited exception contract.
            )
        from .integrations import voiage_evpi  # noqa: PLC0415  # Keep optional dependencies and backend selection lazy.

        try:
            return voiage_evpi(problem.values, list(problem.action_names))
        except (ImportError, OSError) as error:
            raise LibraryUnavailable(  # noqa: TRY003  # Preserve the byte/AST-verified inherited exception contract.
                "voiage could not be imported; install a compatible released build"  # noqa: EM101  # Preserve the byte/AST-verified inherited exception contract.
            ) from error
    if backend != "reference":
        raise ValueError(f"Unknown backend {backend!r}")  # noqa: EM102, TRY003  # Preserve the byte/AST-verified inherited exception contract.
    current_action = int(np.argmax(cast("FloatArray", problem.prior_weights) @ problem.values))
    # Algebraically identical expected regret avoids cancellation of nearly
    # equal large totals. This is not clipping a negative estimate to zero.
    return float(
        cast("FloatArray", problem.prior_weights)
        @ (np.max(problem.values, axis=1) - problem.values[:, current_action])
    )


def exact_partial_information(problem: DecisionProblem, group_labels: Sequence[object]) -> float:
    """Exact value of observing a finite state partition.

    A discretised parameter partition is not full continuous-parameter EVPPI.
    Naming every PSA row uniquely would disclose the entire state and return
    EVPI, not a valid single-parameter EVPPI estimate.
    """
    if len(group_labels) != len(cast("FloatArray", problem.prior_weights)):
        raise ValueError("Group labels must match the state count")  # noqa: EM101, TRY003  # Preserve the byte/AST-verified inherited exception contract.
    groups: dict[object, list[int]] = {}
    for i, label in enumerate(group_labels):
        try:
            groups.setdefault(label, []).append(i)
        except TypeError as error:
            raise ValueError("Partition labels must be hashable") from error  # noqa: EM101, TRY003  # Preserve the byte/AST-verified inherited exception contract.
    current_action = int(np.argmax(cast("FloatArray", problem.prior_weights) @ problem.values))
    gains: list[float] = []
    for indices in groups.values():
        joint_group_values = cast("FloatArray", problem.prior_weights)[indices] @ problem.values[indices]
        gains.append(float(np.max(joint_group_values) - joint_group_values[current_action]))
    return math.fsum(gains)


def _finite(
    value: float,
    name: str,
    lower: float = 0.0,
    upper: float | None = None,
    positive: bool = False,  # noqa: FBT001, FBT002  # Preserve the established public positional flag convention.
) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")  # noqa: EM102, TRY003  # Preserve the byte/AST-verified inherited exception contract.
    if (value <= lower if positive else value < lower) or (upper is not None and value > upper):
        raise ValueError(f"{name} is outside its permitted range")  # noqa: EM102, TRY003  # Preserve the byte/AST-verified inherited exception contract.


@dataclass(frozen=True)
class Catchment:
    population: float
    flow_l_day: float

    def __post_init__(self) -> None:
        _finite(self.population, "population", positive=True)
        _finite(self.flow_l_day, "flow_l_day", positive=True)


@dataclass(frozen=True)
class Exposure:
    smoked_cigarettes_per_1000_day: float
    illicit_share: float
    unrecorded_legal_share: float
    other_nicotine_mg_per1000_day: float
    nicotine_dose_mg_per_cigarette: float = 0.9
    other_nicotine_anabasine_ratio_ug_per_mg: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "smoked_cigarettes_per_1000_day",
            "other_nicotine_mg_per1000_day",
            "other_nicotine_anabasine_ratio_ug_per_mg",
        ):
            _finite(getattr(self, name), name)
        _finite(self.nicotine_dose_mg_per_cigarette, "nicotine dose", positive=True)
        _finite(self.illicit_share, "illicit_share", upper=1.0)
        _finite(self.unrecorded_legal_share, "unrecorded_legal_share", upper=1.0)
        if self.illicit_share + self.unrecorded_legal_share > 1.0:
            raise ValueError("Illicit plus unrecorded lawful shares exceed one")  # noqa: EM101, TRY003  # Preserve the byte/AST-verified inherited exception contract.


@dataclass(frozen=True)
class BiomarkerParameters:
    # Zheng 2023 point estimate, not an NZ-validated distribution.
    anabasine_ug_per_cigarette: float = 0.9
    # Survival=1 is an explicit no-loss reference, not empirical sewer recovery.
    anabasine_survival: float = 1.0
    nicotine_excretion_fraction: float = 0.74
    nicotine_survival: float = 1.0

    def __post_init__(self) -> None:
        _finite(self.anabasine_ug_per_cigarette, "anabasine yield", positive=True)
        for name in ("anabasine_survival", "nicotine_excretion_fraction", "nicotine_survival"):
            _finite(getattr(self, name), name, upper=1.0, positive=True)


def predict_signals(
    exposure: Exposure, catchment: Catchment, parameters: BiomarkerParameters
) -> dict[str, float]:
    """Predict biomarker concentrations and recorded lawful consumption.

    Predicting wastewater depends on total exposure, not illicit share. The
    optional non-smoked nicotine cross-signal is an excreted anabasine yield.
    Recorded sales must be adjusted to consumption and matched to the catchment
    before use as observations; national release volumes are not local intake.
    """
    scale = catchment.population / 1000.0
    e, p = exposure, parameters
    anabasine_ug_day = (
        scale
        * (
            e.smoked_cigarettes_per_1000_day * p.anabasine_ug_per_cigarette
            + e.other_nicotine_mg_per1000_day * e.other_nicotine_anabasine_ratio_ug_per_mg
        )
        * p.anabasine_survival
    )
    nicotine_mg_day = (
        scale
        * (
            e.smoked_cigarettes_per_1000_day * e.nicotine_dose_mg_per_cigarette
            + e.other_nicotine_mg_per1000_day
        )
        * p.nicotine_excretion_fraction
        * p.nicotine_survival
    )
    return {
        "anabasine_ng_l": anabasine_ug_day * 1000.0 / catchment.flow_l_day,
        "nicotine_equivalent_ng_l": nicotine_mg_day * 1_000_000.0 / catchment.flow_l_day,
        "recorded_legal_cigarettes_1000_day": e.smoked_cigarettes_per_1000_day
        * (1.0 - e.illicit_share - e.unrecorded_legal_share),
    }
