"""Exact finite-state/finite-outcome VOI and targeted scientific learning.

No Monte Carlo uncertainty is present in these enumerated results. Numerical
exactness is conditional on the finite model; it does not establish empirical
validity, continuous-parameter convergence or assay performance. Outcomes can
be coarsened continuous measurements, in which case information is discarded.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

import numpy as np
from scipy.special import ndtr, xlogy

from tobac._core import DecisionProblem, exact_evpi


def _likelihood(likelihood, n: int) -> np.ndarray:
    l = np.asarray(likelihood, dtype=float)
    if (
        l.ndim != 2
        or l.shape[1] != n
        or not len(l)
        or not np.isfinite(l).all()
        or (l < 0).any()
        or not np.allclose(l.sum(axis=0), 1, rtol=0, atol=1e-11)
    ):
        raise ValueError("Require a finite stochastic outcome-by-state likelihood")
    return l


def _posterior(prior, likelihood):
    j = likelihood * prior[None, :]
    q = j.sum(axis=1)
    active = q > 0
    return q[active], j[active] / q[active, None]


def label_codes(labels, n):
    a = np.asarray(labels)
    if a.ndim not in (1, 2) or len(a) != n:
        raise ValueError("Target labels require one scalar or tuple per state")
    if a.ndim == 1:
        a = a[:, None]
    _, codes = np.unique(a, axis=0, return_inverse=True)
    return codes


def evaluate(
    problem: DecisionProblem,
    likelihood,
    targets: Mapping | None = None,
    *,
    event=None,
    confidence: float = 0.9,
) -> dict:
    """Exact preposterior value; same actions/objective/comparator for all designs.

    EIG is mutual information in nats about each *specified target*, not an
    amount of money. Resolution is confidence about a specified event, not
    automatic detection of policy causation or agreement by real people.
    """
    if not 0.5 < confidence < 1:
        raise ValueError("Confidence must lie strictly between .5 and 1")
    p = problem.prior_weights
    l = _likelihood(likelihood, len(p))
    q, post = _posterior(p, l)
    a0 = int(np.argmax(p @ problem.values))
    contrast = problem.values - problem.values[:, a0, None]
    conditional = post @ contrast
    choices = np.argmax(conditional, axis=1)
    gains = np.max(conditional, axis=1)
    ess = 1 / np.sum(post * post, axis=1)
    result = {
        "evsi": float(q @ gains),
        "evpi": exact_evpi(problem),
        "prior_action": problem.action_names[a0],
        "probability_action_changes": float(q @ (choices != a0)),
        "mean_effective_states": float(q @ ess),
        "minimum_effective_states": float(ess.min()),
        "posterior_martingale_max_error": float(np.max(np.abs(q @ post - p))),
        "outcomes": len(l),
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
            raise ValueError("The scientific event must be a Boolean state vector")
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


def joint_likelihood(*channels: np.ndarray) -> np.ndarray:
    """Product conditional on all shared latent states, not marginal independence."""
    if not channels:
        raise ValueError("At least one channel is needed")
    n = np.asarray(channels[0]).shape[1]
    joined = np.ones((1, n))
    for channel in channels:
        l = _likelihood(channel, n)
        if joined.shape[0] * l.shape[0] * n > 30_000_000:
            raise ValueError("Joint outcome space exceeds the explicit memory guard")
        joined = (joined[:, None, :] * l[None, :, :]).reshape(-1, n)
    return _likelihood(joined, n)


def lognormal_bins(medians, log_sd: float, cutpoints: Sequence[float]) -> np.ndarray:
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
        raise ValueError("Positive medians, positive SD and strictly increasing positive cuts required")
    cdf = ndtr((np.log(c[:, None]) - np.log(m[None, :])) / log_sd)
    return np.diff(np.vstack([np.zeros(len(m)), cdf, np.ones(len(m))]), axis=0)


def scalar_oracle(problem: DecisionProblem, likelihood) -> float:
    """Independent scalar-loop oracle adapted from the predecessor diagnostic.

    Source v2.3.2 programme/diagnostics.py; all sums use explicit Python loops.
    This is a numerical oracle, not a second production estimator.
    """
    l = _likelihood(likelihood, len(problem.prior_weights))
    p, values = problem.prior_weights, problem.values
    current = max(
        range(values.shape[1]), key=lambda a: math.fsum(float(p[s] * values[s, a]) for s in range(len(p)))
    )
    return math.fsum(
        max(
            math.fsum(float(p[s] * row[s] * (values[s, a] - values[s, current])) for s in range(len(p)))
            for a in range(values.shape[1])
        )
        for row in l
    )


def same_data_robustness(values, priors, reference_prior, likelihood, event, confidence=0.9) -> dict:
    """Compare analysts on the SAME possible data, weighted by one reference law.

    Prior scenarios are not labelled political camps. A common likelihood and
    objective are assumed here; model misspecification/value disagreement are
    distinct exercises. Observations impossible under a candidate are rejected.
    """
    v = np.asarray(values, float)
    ref = np.asarray(reference_prior, float)
    e = np.asarray(event, float)
    if (
        v.ndim != 2
        or ref.shape != (len(v),)
        or e.shape != ref.shape
        or not np.isfinite(v).all()
        or not np.isin(e, [0, 1]).all()
        or not 0.5 < confidence < 1
        or len(priors) < 2
    ):
        raise ValueError("Invalid robustness inputs")
    if not np.isfinite(ref).all() or (ref < 0).any() or not np.isclose(ref.sum(), 1):
        raise ValueError("Normalised nonnegative reference prior required")
    l = _likelihood(likelihood, len(ref))
    q = l @ ref
    active = q > 0
    probs, actions = [], []
    for prior in priors:
        p = np.asarray(prior, float)
        if p.shape != ref.shape or not np.isfinite(p).all() or (p < 0).any() or not np.isclose(p.sum(), 1):
            raise ValueError("Invalid candidate prior")
        j = l[active] * p[None, :]
        mass = j.sum(axis=1)
        if (mass <= 0).any():
            raise ValueError("Reference data impossible under a candidate prior")
        post = j / mass[:, None]
        probs.append(post @ e)
        actions.append(np.argmax(post @ (v - v[:, 0, None]), axis=1))
    probs, actions = np.asarray(probs), np.asarray(actions)
    weights = q[active]
    return {
        "expected_probability_range": float(weights @ np.ptp(probs, axis=0)),
        "decision_agreement_probability": float(weights @ np.all(actions == actions[:1], axis=0)),
        "confident_agreement_probability": float(
            weights @ (np.all(probs >= confidence, axis=0) | np.all(probs <= 1 - confidence, axis=0))
        ),
        "reference_distribution": "common prior-predictive law; not each analysts own law",
    }
