"""Condition finite joint beliefs on identified evidence exactly once.

Metadata checks establish compatibility, not scientific validity. Log likelihoods
may be densities. A forecast or posterior is not a new observed-data likelihood.
Shared errors belong in the supplied joint likelihood, not duplicate source rows.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

import numpy as np
from scipy.special import logsumexp

from ._core import DecisionProblem, exact_evpi
from .information import _likelihood, evaluate


def _ids(values: Sequence[str], name: str, *, empty: bool = False) -> tuple[str, ...]:
    if isinstance(values, str):
        raise ValueError(f"{name} must be a sequence of identifiers")
    result = tuple(values)
    if (
        (not empty and not result)
        or any(not isinstance(x, str) or not x.strip() for x in result)
        or len(set(result)) != len(result)
    ):
        raise ValueError(f"{name} must contain unique nonempty identifiers")
    return result


def state_identifiers(states) -> tuple[str, ...]:
    """Stable IDs bind each row to all named physical/latent values, not an index."""
    if not isinstance(states, dict) or not states or any(not isinstance(k, str) or not k for k in states):
        raise ValueError("Named state arrays required")
    names = sorted(states)
    arrays = [np.asarray(states[k], dtype=float) for k in names]
    if (
        any(a.ndim != 1 or not len(a) or not np.isfinite(a).all() for a in arrays)
        or len({len(a) for a in arrays}) != 1
    ):
        raise ValueError("State arrays must be finite and aligned")
    matrix = np.column_stack(arrays).astype("<f8")
    matrix[matrix == 0] = 0.0  # canonicalise signed zero
    prefix = json.dumps(names, separators=(",", ":"), ensure_ascii=False).encode() + b"\0"
    ids = tuple("state:" + hashlib.sha256(prefix + row.tobytes()).hexdigest() for row in matrix)
    return _ids(ids, "state_ids")


@dataclass(frozen=True)
class Scope:
    geography: str
    population: str
    start: str
    end: str
    unit: str

    def __post_init__(self):
        if any(not isinstance(x, str) or not x.strip() for x in (self.geography, self.population, self.unit)):
            raise ValueError("Declare geography, population and unit")
        try:
            start, end = date.fromisoformat(self.start), date.fromisoformat(self.end)
        except (ValueError, TypeError) as exc:
            raise ValueError("Use ISO observation-period dates") from exc
        if start > end:
            raise ValueError("Observation period is reversed")


@dataclass(frozen=True)
class EvidencePacket:
    evidence_id: str
    data_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    state_ids: tuple[str, ...]
    log_likelihood: np.ndarray
    source_scope: Scope
    target_scope: Scope
    likelihood_model: str
    role: str = "observation"
    transport_note: str = ""
    dependence_note: str = ""

    def __post_init__(self):
        if self.role != "observation":
            raise ValueError("Only observed-data likelihoods can condition a belief")
        for name in ("evidence_id", "likelihood_model"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"Declare {name}")
        for name in ("data_ids", "source_ids", "state_ids"):
            object.__setattr__(self, name, _ids(getattr(self, name), name))
        if not isinstance(self.source_scope, Scope) or not isinstance(self.target_scope, Scope):
            raise ValueError("Typed source and target scopes required")
        if self.source_scope != self.target_scope and not self.transport_note.strip():
            raise ValueError("A changed scope requires an explicit transport model note")
        logl = np.array(self.log_likelihood, dtype=float, copy=True)
        if logl.shape != (len(self.state_ids),) or np.isnan(logl).any() or np.isposinf(logl).any():
            raise ValueError("Log likelihood must match states, allowing only finite values or -inf")
        logl.setflags(write=False)
        object.__setattr__(self, "log_likelihood", logl)


@dataclass(frozen=True)
class Belief:
    problem: DecisionProblem
    state_ids: tuple[str, ...]
    scope: Scope
    used_data_ids: tuple[str, ...] = ()
    receipts: tuple[dict, ...] = ()

    def __post_init__(self):
        object.__setattr__(self, "state_ids", _ids(self.state_ids, "state_ids"))
        object.__setattr__(self, "used_data_ids", _ids(self.used_data_ids, "used_data_ids", empty=True))
        if len(self.state_ids) != len(self.problem.prior_weights) or not isinstance(self.scope, Scope):
            raise ValueError("State identities and scope must match the decision problem")

    def require_new_data(self, data_ids: Sequence[str]) -> tuple[str, ...]:
        ids = _ids(data_ids, "data_ids")
        if set(ids) & set(self.used_data_ids):
            raise ValueError("Underlying data reused; a new citation does not create new evidence")
        return ids


def condition(belief: Belief, packet: EvidencePacket) -> Belief:
    """Bayesian joint-state update; never reorder, resample or silently transport."""
    if packet.state_ids != belief.state_ids:
        raise ValueError("Evidence state identities/order do not match the prior")
    if packet.target_scope != belief.scope:
        raise ValueError("Evidence target scope differs from the decision scope")
    belief.require_new_data(packet.data_ids)
    if any(r["evidence_id"] == packet.evidence_id for r in belief.receipts):
        raise ValueError("Evidence identifier reused")
    if belief.receipts and not packet.dependence_note.strip():
        raise ValueError("Declare conditional dependence on previously used evidence")
    prior = belief.problem.prior_weights
    logp = np.full(len(prior), -np.inf)
    positive = prior > 0
    logp[positive] = np.log(prior[positive])
    log_mass = float(logsumexp(logp + packet.log_likelihood))
    if not np.isfinite(log_mass):
        raise ValueError("Observation has no support under this prior/likelihood")
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
        belief.receipts + (receipt,),
    )


def predictive(belief: Belief, likelihood) -> np.ndarray:
    return _likelihood(likelihood, len(belief.state_ids)) @ belief.problem.prior_weights


def prospective_value(belief: Belief, likelihood, data_ids: Sequence[str], **kwargs) -> dict:
    """Evaluate incremental NEW observations after the actual D0 update."""
    belief.require_new_data(data_ids)
    return evaluate(belief.problem, likelihood, **kwargs)


def incremental_value(belief: Belief, first, second=None, *, joint=None) -> dict:
    """Preposterior marginal information, not value conditional on realised D0.

    With second supplied, errors are independent GIVEN the complete joint state.
    For correlated reports, supply joint[first_outcome, next_outcome, state].
    The exact chain identity is checked without summing separate marginal EVSIs.
    """
    if (second is None) == (joint is None):
        raise ValueError("Provide either a conditional-independent second report or a joint report")
    p = belief.problem
    first = _likelihood(first, len(belief.state_ids))
    if joint is None:
        second = _likelihood(second, len(belief.state_ids))
        tensor = first[:, None, :] * second[None, :, :]
    else:
        tensor = np.asarray(joint, dtype=float)
    if (
        tensor.ndim != 3
        or tensor.shape[0] != len(first)
        or tensor.shape[2] != first.shape[1]
        or tensor.shape[1] < 1
        or not np.isfinite(tensor).all()
        or (tensor < 0).any()
        or not np.allclose(tensor.sum(axis=1), first, atol=1e-11, rtol=0)
    ):
        raise ValueError("Joint report must have the declared first-report marginal")
    q = first @ p.prior_weights
    values, remaining = [], []
    for y, probability in enumerate(q):
        if probability <= 0:
            values.append(0.0)
            remaining.append(0.0)
            continue
        weights = first[y] * p.prior_weights / probability
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
