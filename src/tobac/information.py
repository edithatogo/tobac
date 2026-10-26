"""Exact finite-state/finite-outcome VOI and targeted scientific learning.

No Monte Carlo uncertainty is present in these enumerated results. Numerical
exactness is conditional on the finite model; it does not establish empirical
validity, continuous-parameter convergence or assay performance. Outcomes can
be coarsened continuous measurements, in which case information is discarded.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, cast

import numpy as np
from scipy.special import ndtr, xlogy

from tobac._core import DecisionProblem, exact_evpi

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from numpy.typing import ArrayLike, NDArray

    from tobac._typing import FloatArray, Report


# Named bounds preserve the existing scientific/data contract.
MATRIX_NDIM = 2
MIN_DECISION_CONFIDENCE = 0.5
MAX_JOINT_CELLS = 30000000
MIN_PRIOR_SCENARIOS = 2


def validate_likelihood(likelihood: ArrayLike, n: int) -> FloatArray:
    """Validate a stochastic outcome-by-state likelihood matrix."""
    likelihood_matrix = np.asarray(likelihood, dtype=float)
    if (
        likelihood_matrix.ndim != MATRIX_NDIM
        or likelihood_matrix.shape[1] != n
        or not len(likelihood_matrix)
        or not np.isfinite(likelihood_matrix).all()
        or (likelihood_matrix < 0).any()
        or not np.allclose(likelihood_matrix.sum(axis=0), 1, rtol=0, atol=1e-11)
    ):
        msg = "Require a finite stochastic outcome-by-state likelihood"
        raise ValueError(msg)
    return likelihood_matrix


def _posterior(prior: FloatArray, likelihood: FloatArray) -> tuple[FloatArray, FloatArray]:
    j = likelihood * prior[None, :]
    q = j.sum(axis=1)
    active = q > 0
    return q[active], j[active] / q[active, None]


def label_codes(labels: ArrayLike, n: int) -> NDArray[np.int64]:
    """Encode aligned scalar or tuple state labels as finite partition indices."""
    a = np.asarray(labels)
    if a.ndim not in (1, 2) or len(a) != n:
        msg = "Target labels require one scalar or tuple per state"
        raise ValueError(msg)
    if a.ndim == 1:
        a = a[:, None]
    _, codes = np.unique(a, axis=0, return_inverse=True)
    return codes


def evaluate(
    problem: DecisionProblem,
    likelihood: ArrayLike,
    targets: Mapping[str, ArrayLike] | None = None,
    *,
    event: ArrayLike | None = None,
    confidence: float = 0.9,
) -> Report:
    """Exact preposterior value; same actions/objective/comparator for all designs.

    EIG is mutual information in nats about each *specified target*, not an
    amount of money. Resolution is confidence about a specified event, not
    automatic detection of policy causation or agreement by real people.
    """
    if not MIN_DECISION_CONFIDENCE < confidence < 1:
        msg = "Confidence must lie strictly between .5 and 1"
        raise ValueError(msg)
    p = cast("FloatArray", problem.prior_weights)
    likelihood_matrix = validate_likelihood(likelihood, len(p))
    q, post = _posterior(p, likelihood_matrix)
    a0 = int(np.argmax(p @ problem.values))
    contrast = problem.values - problem.values[:, a0, None]
    conditional = post @ contrast
    choices = np.argmax(conditional, axis=1)
    gains = np.max(conditional, axis=1)
    ess = 1 / np.sum(post * post, axis=1)
    result: Report = {
        "evsi": float(q @ gains),
        "evpi": exact_evpi(problem),
        "prior_action": problem.action_names[a0],
        "probability_action_changes": float(q @ (choices != a0)),
        "mean_effective_states": float(q @ ess),
        "minimum_effective_states": float(ess.min()),
        "posterior_martingale_max_error": float(np.max(np.abs(q @ post - p))),
        "outcomes": len(likelihood_matrix),
        "positive_probability_outcomes": len(q),
        "value_unit": problem.value_unit,
        "targets": {},
        "method": "exact enumeration of declared finite prior and coarsened outcomes",
    }
    for name, labels in (targets or {}).items():
        codes = label_codes(labels, len(p))
        k = int(codes.max()) + 1
        prior_target = np.bincount(codes, weights=p, minlength=k)
        posterior_target = np.column_stack([post[:, codes == j].sum(axis=1) for j in range(k)])
        entropy0 = -float(np.sum(xlogy(prior_target, prior_target)))
        entropy1 = -np.sum(xlogy(posterior_target, posterior_target), axis=1)
        result["targets"][name] = {
            "prior_entropy_nats": entropy0,
            "expected_posterior_entropy_nats": float(q @ entropy1),
            "eig_nats": float(entropy0 - q @ entropy1),
        }
    if event is not None:
        e = np.asarray(event)
        if e.shape != p.shape or not np.isin(e, [0, 1]).all():
            msg = "The scientific event must be a Boolean state vector"
            raise ValueError(msg)
        h = post @ e.astype(float)
        resolved = (h >= confidence) | (h <= 1 - confidence)
        prior_h = float(p @ e.astype(float))
        result.update(
            {
                "prior_event_probability": prior_h,
                "resolution_probability": float(q @ resolved),
                "prior_resolved": bool(prior_h >= confidence or prior_h <= 1 - confidence),
                "correct_resolution_probability": float(q @ (resolved * np.maximum(h, 1 - h))),
                "event_brier_risk": float(q @ (h * (1 - h))),
                "prior_event_brier_risk": prior_h * (1 - prior_h),
            }
        )
    return result


def joint_likelihood(*channels: FloatArray) -> FloatArray:
    """Product conditional on all shared latent states, not marginal independence."""
    if not channels:
        msg = "At least one channel is needed"
        raise ValueError(msg)
    n = np.asarray(channels[0]).shape[1]
    joined = np.ones((1, n))
    for channel in channels:
        likelihood_matrix = validate_likelihood(channel, n)
        if joined.shape[0] * likelihood_matrix.shape[0] * n > MAX_JOINT_CELLS:
            msg = "Joint outcome space exceeds the explicit memory guard"
            raise ValueError(msg)
        joined = (joined[:, None, :] * likelihood_matrix[None, :, :]).reshape(-1, n)
    return validate_likelihood(joined, n)


def lognormal_bins(medians: ArrayLike, log_sd: float, cutpoints: Sequence[float]) -> FloatArray:
    """Integrated lognormal probabilities, including [0, first/LOQ) censoring.

    Medians and cutpoints must use the same physical unit. Moving the first
    threshold is not a conversion of extract-scale to influent-scale LOQ.
    """
    m = np.asarray(medians, float)
    c = np.asarray(cutpoints, float)
    if (
        m.ndim != 1
        or not len(m)
        or not np.isfinite(m).all()
        or (m <= 0).any()
        or not math.isfinite(log_sd)
        or log_sd <= 0
        or c.ndim != 1
        or not np.isfinite(c).all()
        or (c <= 0).any()
        or (np.diff(c) <= 0).any()
    ):
        msg = "Positive medians, positive SD and strictly increasing positive cuts required"
        raise ValueError(msg)
    cdf = ndtr((np.log(c[:, None]) - np.log(m[None, :])) / log_sd)
    return np.diff(np.vstack([np.zeros(len(m)), cdf, np.ones(len(m))]), axis=0)


def scalar_oracle(problem: DecisionProblem, likelihood: ArrayLike) -> float:
    """Independent scalar-loop oracle adapted from the predecessor diagnostic.

    Source v2.3.2 programme/diagnostics.py; all sums use explicit Python loops.
    This is a numerical oracle, not a second production estimator.
    """
    likelihood_matrix = validate_likelihood(likelihood, len(cast("FloatArray", problem.prior_weights)))
    p, values = cast("FloatArray", problem.prior_weights), problem.values
    current = max(
        range(values.shape[1]), key=lambda a: math.fsum(float(p[s] * values[s, a]) for s in range(len(p)))
    )
    return math.fsum(
        max(
            math.fsum(float(p[s] * row[s] * (values[s, a] - values[s, current])) for s in range(len(p)))
            for a in range(values.shape[1])
        )
        for row in likelihood_matrix
    )


def same_data_robustness(  # noqa: PLR0913, PLR0917  # Preserve explicit dimensioned inputs and the established API.; Preserve the established positional calling convention.
    values: FloatArray,
    priors: Sequence[FloatArray],
    reference_prior: FloatArray,
    likelihood: ArrayLike,
    event: ArrayLike,
    confidence: float = 0.9,
) -> Report:
    """Compare analysts on the SAME possible data, weighted by one reference law.

    Prior scenarios are not labelled political camps. A common likelihood and
    objective are assumed here; model misspecification/value disagreement are
    distinct exercises. Observations impossible under a candidate are rejected.
    """
    v = np.asarray(values, float)
    ref = np.asarray(reference_prior, float)
    e = np.asarray(event, float)
    if (
        v.ndim != MATRIX_NDIM
        or ref.shape != (len(v),)
        or e.shape != ref.shape
        or not np.isfinite(v).all()
        or not np.isin(e, [0, 1]).all()
        or not MIN_DECISION_CONFIDENCE < confidence < 1
        or len(priors) < MIN_PRIOR_SCENARIOS
    ):
        msg = "Invalid robustness inputs"
        raise ValueError(msg)
    if not np.isfinite(ref).all() or (ref < 0).any() or not np.isclose(ref.sum(), 1):
        msg = "Normalised nonnegative reference prior required"
        raise ValueError(msg)
    likelihood_matrix = validate_likelihood(likelihood, len(ref))
    q = likelihood_matrix @ ref
    active = q > 0
    prob_rows: list[FloatArray] = []
    action_rows: list[NDArray[np.int64]] = []
    for prior in priors:
        p = np.asarray(prior, float)
        if p.shape != ref.shape or not np.isfinite(p).all() or (p < 0).any() or not np.isclose(p.sum(), 1):
            msg = "Invalid candidate prior"
            raise ValueError(msg)
        j = likelihood_matrix[active] * p[None, :]
        mass = j.sum(axis=1)
        if (mass <= 0).any():
            msg = "Reference data impossible under a candidate prior"
            raise ValueError(msg)
        post = j / mass[:, None]
        prob_rows.append(post @ e)
        action_rows.append(np.argmax(post @ (v - v[:, 0, None]), axis=1))
    probs, actions = np.asarray(prob_rows), np.asarray(action_rows)
    weights = q[active]
    return {
        "expected_probability_range": float(weights @ np.ptp(probs, axis=0)),
        "decision_agreement_probability": float(weights @ np.all(actions == actions[:1], axis=0)),
        "confident_agreement_probability": float(
            weights @ (np.all(probs >= confidence, axis=0) | np.all(probs <= 1 - confidence, axis=0))
        ),
        "reference_distribution": "common prior-predictive law; not each analysts own law",
    }


# Preserve the established private import for external callers.
_likelihood = validate_likelihood
