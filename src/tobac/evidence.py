"""Condition finite joint beliefs on identified evidence exactly once.

Metadata checks establish compatibility, not scientific validity. Log likelihoods
may be densities. A forecast or posterior is not a new observed-data likelihood.
Shared errors belong in the supplied joint likelihood, not duplicate source rows.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, cast
lazy from collections.abc import Mapping, Sequence

import numpy as np
from scipy.special import logsumexp
lazy from numpy.typing import ArrayLike

from ._core import DecisionProblem, exact_evpi
from .information import evaluate, validate_likelihood

if TYPE_CHECKING:
    from tobac._typing import FloatArray, Report, StateArrays


# Named bounds preserve the existing scientific/data contract.
JOINT_TENSOR_NDIM = 3


def _ids(values: Sequence[str], name: str, *, empty: bool = False) -> tuple[str, ...]:
    if isinstance(values, str):
        msg = f"{name} must be a sequence of identifiers"
        raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
    result = tuple(values)
    if (
        (not empty and not result)
        or any(not isinstance(cast("object", x), str) or not x.strip() for x in result)
        or len(set(result)) != len(result)
    ):
        msg = f"{name} must contain unique nonempty identifiers"
        raise ValueError(msg)
    return result


def state_identifiers(states: StateArrays) -> tuple[str, ...]:
    """Stable IDs bind each row to all named physical/latent values, not an index."""
    if (
        not isinstance(cast("object", states), dict)
        or not states
        or any(not isinstance(cast("object", k), str) or not k for k in states)
    ):
        msg = "Named state arrays required"
        raise ValueError(msg)
    names = sorted(states)
    arrays = [np.asarray(states[k], dtype=float) for k in names]
    if (
        any(a.ndim != 1 or not len(a) or not np.isfinite(a).all() for a in arrays)
        or len({len(a) for a in arrays}) != 1
    ):
        msg = "State arrays must be finite and aligned"
        raise ValueError(msg)
    matrix = np.column_stack(arrays).astype("<f8")
    matrix[matrix == 0] = 0.0  # canonicalise signed zero
    prefix = json.dumps(names, separators=(",", ":"), ensure_ascii=False).encode() + b"\0"
    ids = tuple("state:" + hashlib.sha256(prefix + row.tobytes()).hexdigest() for row in matrix)
    return _ids(ids, "state_ids")


@dataclass(frozen=True)
class Scope:
    """Declared geography, population, period and units for an evidence exchange."""

    geography: str
    population: str
    start: str
    end: str
    unit: str

    def __post_init__(self) -> None:
        """Validate construction invariants and normalize the stored values."""
        if any(
            not isinstance(cast("object", x), str) or not x.strip()
            for x in (self.geography, self.population, self.unit)
        ):
            msg = "Declare geography, population and unit"
            raise ValueError(msg)
        try:
            start, end = date.fromisoformat(self.start), date.fromisoformat(self.end)
        except (ValueError, TypeError) as exc:
            msg = "Use ISO observation-period dates"
            raise ValueError(msg) from exc
        if start > end:
            msg = "Observation period is reversed"
            raise ValueError(msg)


@dataclass(frozen=True)
class EvidencePacket:
    """Identified observed-data likelihood with explicit source and target scope."""

    evidence_id: str
    data_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    state_ids: tuple[str, ...]
    log_likelihood: FloatArray
    source_scope: Scope
    target_scope: Scope
    likelihood_model: str
    role: str = "observation"
    transport_note: str = ""
    dependence_note: str = ""

    def __post_init__(self) -> None:
        """Validate construction invariants and normalize the stored values."""
        if self.role != "observation":
            msg = "Only observed-data likelihoods can condition a belief"
            raise ValueError(msg)
        for name in ("evidence_id", "likelihood_model"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                msg = f"Declare {name}"
                raise ValueError(msg)
        for name in ("data_ids", "source_ids", "state_ids"):
            object.__setattr__(self, name, _ids(getattr(self, name), name))
        if not isinstance(cast("object", self.source_scope), Scope) or not isinstance(
            cast("object", self.target_scope), Scope
        ):
            msg = "Typed source and target scopes required"
            raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
        if self.source_scope != self.target_scope and not self.transport_note.strip():
            msg = "A changed scope requires an explicit transport model note"
            raise ValueError(msg)
        logl = np.array(self.log_likelihood, dtype=float, copy=True)
        if logl.shape != (len(self.state_ids),) or np.isnan(logl).any() or np.isposinf(logl).any():
            msg = "Log likelihood must match states, allowing only finite values or -inf"
            raise ValueError(msg)
        logl.setflags(write=False)
        object.__setattr__(self, "log_likelihood", logl)


@dataclass(frozen=True)
class Belief:
    """Finite decision belief with once-only underlying-data conditioning receipts."""

    problem: DecisionProblem
    state_ids: tuple[str, ...]
    scope: Scope
    used_data_ids: tuple[str, ...] = ()
    receipts: tuple[Report, ...] = ()

    def __post_init__(self) -> None:
        """Validate construction invariants and normalize the stored values."""
        object.__setattr__(self, "state_ids", _ids(self.state_ids, "state_ids"))
        object.__setattr__(self, "used_data_ids", _ids(self.used_data_ids, "used_data_ids", empty=True))
        if len(self.state_ids) != len(cast("FloatArray", self.problem.prior_weights)) or not isinstance(
            cast("object", self.scope), Scope
        ):
            msg = "State identities and scope must match the decision problem"
            raise ValueError(msg)

    def require_new_data(self, data_ids: Sequence[str]) -> tuple[str, ...]:
        """Reject evidence identities already used to condition this belief."""
        ids = _ids(data_ids, "data_ids")
        if set(ids) & set(self.used_data_ids):
            msg = "Underlying data reused; a new citation does not create new evidence"
            raise ValueError(msg)
        return ids


def condition(belief: Belief, packet: EvidencePacket) -> Belief:
    """Bayesian joint-state update; never reorder, resample or silently transport."""
    if packet.state_ids != belief.state_ids:
        msg = "Evidence state identities/order do not match the prior"
        raise ValueError(msg)
    if packet.target_scope != belief.scope:
        msg = "Evidence target scope differs from the decision scope"
        raise ValueError(msg)
    belief.require_new_data(packet.data_ids)
    if any(r["evidence_id"] == packet.evidence_id for r in belief.receipts):
        msg = "Evidence identifier reused"
        raise ValueError(msg)
    if belief.receipts and not packet.dependence_note.strip():
        msg = "Declare conditional dependence on previously used evidence"
        raise ValueError(msg)
    prior = cast("FloatArray", belief.problem.prior_weights)
    logp = np.full(len(prior), -np.inf)
    positive = prior > 0
    logp[positive] = np.log(prior[positive])
    log_mass = float(logsumexp(logp + packet.log_likelihood))
    if not np.isfinite(log_mass):
        msg = "Observation has no support under this prior/likelihood"
        raise ValueError(msg)
    posterior = np.exp(logp + packet.log_likelihood - log_mass)
    problem = DecisionProblem(
        belief.problem.values, belief.problem.action_names, belief.problem.value_unit, posterior
    )
    receipt = {
        "evidence_id": packet.evidence_id,
        "data_ids": list(packet.data_ids),
        "source_ids": list(packet.source_ids),
        "likelihood_model": packet.likelihood_model,
        "log_predictive_density": log_mass,
        "effective_states": float(1 / np.sum(posterior**2)),
        "transport_note": packet.transport_note,
        "dependence_note": packet.dependence_note,
        "qualification": "metadata checked; scientific validity not certified",
    }
    return Belief(
        problem,
        belief.state_ids,
        belief.scope,
        belief.used_data_ids + packet.data_ids,
        (*belief.receipts, receipt),
    )


def predictive(belief: Belief, likelihood: ArrayLike) -> FloatArray:
    """Compute report probabilities under the currently conditioned finite belief."""
    return validate_likelihood(likelihood, len(belief.state_ids)) @ cast(
        "FloatArray", belief.problem.prior_weights
    )


def prospective_value(  # noqa: PLR0913  # Preserve explicit dimensioned inputs and the established API.
    belief: Belief,
    likelihood: ArrayLike,
    data_ids: Sequence[str],
    *,
    targets: Mapping[str, ArrayLike] | None = None,
    event: ArrayLike | None = None,
    confidence: float = 0.9,
) -> Report:
    """Evaluate incremental NEW observations after the actual D0 update."""
    belief.require_new_data(data_ids)
    return evaluate(belief.problem, likelihood, targets, event=event, confidence=confidence)


def incremental_value(
    belief: Belief, first: ArrayLike, second: ArrayLike | None = None, *, joint: ArrayLike | None = None
) -> Report:
    """Preposterior marginal information, not value conditional on realised D0.

    With second supplied, errors are independent GIVEN the complete joint state.
    For correlated reports, supply joint[first_outcome, next_outcome, state].
    The exact chain identity is checked without summing separate marginal EVSIs.
    """
    if (second is None) == (joint is None):
        msg = "Provide either a conditional-independent second report or a joint report"
        raise ValueError(msg)
    p = belief.problem
    first = validate_likelihood(first, len(belief.state_ids))
    if joint is None:
        second = validate_likelihood(cast("ArrayLike", second), len(belief.state_ids))
        tensor = first[:, None, :] * second[None, :, :]
    else:
        tensor = np.asarray(joint, dtype=float)
    if (
        tensor.ndim != JOINT_TENSOR_NDIM
        or tensor.shape[0] != len(first)
        or tensor.shape[2] != first.shape[1]
        or tensor.shape[1] < 1
        or not np.isfinite(tensor).all()
        or (tensor < 0).any()
        or not np.allclose(tensor.sum(axis=1), first, atol=1e-11, rtol=0)
    ):
        msg = "Joint report must have the declared first-report marginal"
        raise ValueError(msg)
    q = first @ cast("FloatArray", p.prior_weights)
    values: list[float] = []
    remaining: list[float] = []
    for y, probability in enumerate(q):
        if probability <= 0:
            values.append(0.0)
            remaining.append(0.0)
            continue
        weights = first[y] * cast("FloatArray", p.prior_weights) / probability
        after = DecisionProblem(p.values, p.action_names, p.value_unit, weights)
        # At states impossible given y, any proper conditional distribution works.
        l2 = np.full(tensor[y].shape, 1 / tensor.shape[1])
        np.divide(tensor[y], first[y][None, :], out=l2, where=first[y][None, :] > 0)
        values.append(evaluate(after, l2)["evsi"])
        remaining.append(exact_evpi(after))
    first_evsi = evaluate(p, first)["evsi"]
    joint_evsi = evaluate(p, tensor.reshape(-1, len(belief.state_ids)))["evsi"]
    extra = float(q @ values)
    return {
        "first_evsi": first_evsi,
        "joint_evsi": joint_evsi,
        "expected_conditional_evsi": extra,
        "chain_error": abs(extra - (joint_evsi - first_evsi)),
        "initial_evpi": exact_evpi(p),
        "expected_remaining_evpi": float(q @ remaining),
        "outcome_probabilities": q.tolist(),
        "conditional_evsi": values,
        "scope": "prospective sequence under the declared finite model",
    }
