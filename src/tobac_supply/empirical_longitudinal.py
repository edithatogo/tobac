"""Historical summary-data likelihood, not direct identification of illicit consumption.

A finite quadrature grid integrates annual process SD in a Gaussian random walk
with uncertain intercept and slope. It fits a survey-reported / matched-supply
log ratio. Underreporting/stock interpretations remain external sensitivity
mappings. No current NZ assay rows or unobserved policy effects are invented.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from numbers import Integral, Real
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import brentq
from scipy.special import logsumexp, ndtr, ndtri

Array = NDArray[np.float64]


def _value(x: Real, name: str, positive: bool = False) -> float:
    if isinstance(x, (bool, np.bool_)) or not isinstance(x, Real) or not math.isfinite(x):
        raise ValueError(f"{name} must be finite and numeric")
    v = float(x)
    if positive and v <= 0:
        raise ValueError(f"{name} must be positive")
    return v


def _vec(values: Iterable[Real], name: str) -> Array:
    try:
        a = np.asarray([_value(x, name) for x in values], dtype=float)
    except TypeError as exc:
        raise ValueError(f"{name} must be a sequence") from exc
    if not a.size:
        raise ValueError(f"{name} is empty")
    return a


def reconstruct_interval(lower: Real, upper: Real, source_uplift: Real) -> dict[str, Any]:
    """Undo source uplift, then reconstruct a working log-normal summary likelihood.

    The midpoint is a geometric midpoint of published bounds, NOT an observed
    central estimate. Width covers reported smoker-count uncertainty only; extra
    intensity/alignment terms must be supplied separately. This approximation
    is audited against arithmetic-midpoint and bound-centred alternatives.
    """
    lo, hi = _value(lower, "lower", True), _value(upper, "upper", True)
    uplift = _value(source_uplift, "source_uplift", True)
    if hi <= lo:
        raise ValueError("upper must be greater than lower")
    log_centre = (math.log(lo) + math.log(hi)) / 2 - math.log(uplift)
    return dict(
        median_proxy=math.exp(log_centre),
        log_median=log_centre,
        log_se=(math.log(hi) - math.log(lo)) / (2 * float(ndtri(0.975))),
        source_uplift_removed=uplift,
        is_published_point_estimate=False,
        role="interval_reconstructed_working_likelihood_not_raw_data",
    )


@dataclass(frozen=True)
class TemporalSpec:
    level_mean: float = 0.0
    level_sd: float = 0.7
    slope_sd: float = 0.10
    process_grid: tuple[float, ...] = tuple(np.geomspace(0.005, 0.35, 41).tolist())
    process_prior_scale: float = 0.10
    intensity_cv: float = 0.10
    alignment_cv: float = 0.05
    residual_half_life_years: float = 0.0

    def __post_init__(self) -> None:
        _value(self.level_mean, "level_mean")
        for key in ("level_sd", "slope_sd", "process_prior_scale"):
            _value(getattr(self, key), key, True)
        for key in ("intensity_cv", "alignment_cv", "residual_half_life_years"):
            if _value(getattr(self, key), key) < 0:
                raise ValueError(f"{key} cannot be negative")
        q = _vec(self.process_grid, "process_grid")
        if np.any(q <= 0) or np.any(np.diff(q) <= 0):
            raise ValueError("process_grid must be positive, unique, increasing")


def prior_kernel(t: Iterable[Real], s: Iterable[Real], process_sd: Real, spec: TemporalSpec) -> Array:
    """Cov[a + b*t + W_q(t), a + b*s + W_q(s)] for nonnegative relative times."""
    x, y = _vec(t, "times"), _vec(s, "times")
    q = _value(process_sd, "process_sd", True)
    if np.any(x < 0) or np.any(y < 0):
        raise ValueError("relative times cannot precede origin")
    return spec.level_sd**2 + spec.slope_sd**2 * np.outer(x, y) + q * q * np.minimum.outer(x, y)


def observation_covariance(times: Array, log_se: Array, spec: TemporalSpec) -> Array:
    """Count-interval SE plus independent intensity error and optional correlated alignment error."""
    n = len(times)
    if spec.residual_half_life_years == 0:
        corr = np.eye(n)
    else:
        corr = np.exp(-math.log(2) * np.abs(times[:, None] - times[None, :]) / spec.residual_half_life_years)
    return np.diag(log_se**2 + math.log1p(spec.intensity_cv**2)) + math.log1p(spec.alignment_cv**2) * corr


@dataclass(frozen=True)
class TemporalFit:
    times: Array
    observations: Array
    log_se: Array
    spec: TemporalSpec
    weights: Array
    log_evidence: float
    observation_ids: tuple[str, ...]


def fit_temporal(
    times: Iterable[Real],
    observations: Iterable[Real],
    log_se: Iterable[Real],
    spec: TemporalSpec = TemporalSpec(),
    *,
    observation_ids: Iterable[str] | None = None,
) -> TemporalFit:
    """Fit the observed-ratio process; no response is imputed at absent years.

    A common starting origin is fixed by the first observation. Priors and CI
    reconstruction are explicit model choices. Grid weights integrate SD, not
    inverse variance; no MCMC convergence or parameter-identification claim.
    """
    t, y, se = _vec(times, "times"), _vec(observations, "observations"), _vec(log_se, "log_se")
    if len(t) < 2 or len(y) != len(t) or len(se) != len(t) or np.any(np.diff(t) <= 0) or np.any(se <= 0):
        raise ValueError("Need aligned unique increasing times, finite values and positive SEs")
    if not isinstance(spec, TemporalSpec):
        raise ValueError("spec must be a TemporalSpec")
    ids = tuple(str(x) for x in (observation_ids if observation_ids is not None else range(len(t))))
    if len(ids) != len(t) or any(not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("Missing or duplicate source observation IDs")
    rel = t - t[0]
    error = observation_covariance(t, se, spec)
    q = np.asarray(spec.process_grid)
    cells = np.ones(len(q))
    if len(q) > 1:
        cells[0] = (q[1] - q[0]) / 2
        cells[-1] = (q[-1] - q[-2]) / 2
        cells[1:-1] = (q[2:] - q[:-2]) / 2
    logprior = -0.5 * (q / spec.process_prior_scale) ** 2 + np.log(cells)
    logprior -= logsumexp(logprior)
    residual = y - spec.level_mean
    loglik = []
    for sd in q:
        cov = prior_kernel(rel, rel, float(sd), spec) + error
        fac = cho_factor(cov, lower=True)
        logdet = 2 * np.log(np.diag(fac[0])).sum()
        loglik.append(-0.5 * (len(t) * math.log(2 * math.pi) + logdet + residual @ cho_solve(fac, residual)))
    logmass = logprior + np.array(loglik)
    z = float(logsumexp(logmass))
    return TemporalFit(t.copy(), y.copy(), se.copy(), spec, np.exp(logmass - z), z, ids)


def posterior_components(fit: TemporalFit, query: Iterable[Real]) -> dict[str, Array]:
    """Gaussian components of latent trajectory posterior on the requested times."""
    x = _vec(query, "query")
    if np.any(np.diff(x) <= 0) or np.any(x < fit.times[0]):
        raise ValueError("Query times must be unique, increasing, and not precede origin")
    t = fit.times - fit.times[0]
    xr = x - fit.times[0]
    error = observation_covariance(fit.times, fit.log_se, fit.spec)
    means = []
    covs = []
    for q in fit.spec.process_grid:
        cross = prior_kernel(xr, t, q, fit.spec)
        fac = cho_factor(prior_kernel(t, t, q, fit.spec) + error, lower=True)
        mean = fit.spec.level_mean + cross @ cho_solve(fac, fit.observations - fit.spec.level_mean)
        cov = prior_kernel(xr, xr, q, fit.spec) - cross @ cho_solve(fac, cross.T)
        cov = (cov + cov.T) / 2
        if np.linalg.eigvalsh(cov).min() < -1e-9:
            raise ValueError("Posterior covariance is not positive semidefinite")
        means.append(mean)
        covs.append(cov)
    return {
        "times": x,
        "means": np.asarray(means),
        "covariances": np.asarray(covs),
        "weights": fit.weights.copy(),
    }


def summarise_temporal(
    fit: TemporalFit, query: Iterable[Real], *, observation_se: Real = 0.0
) -> list[dict[str, float]]:
    """Mixture moments/quantiles, with optional stated future-observation SD.

    observation_se is a total future-observation log SD supplied by the caller;
    do not additionally include the same technical/alignment uncertainty elsewhere.
    """
    obs_sd = _value(observation_se, "observation_se")
    if obs_sd < 0:
        raise ValueError("observation_se cannot be negative")
    c = posterior_components(fit, query)
    result = []
    for j, time in enumerate(c["times"]):
        means = c["means"][:, j]
        var = np.maximum(c["covariances"][:, j, j] + obs_sd**2, 1e-15)
        sd = np.sqrt(var)
        w = fit.weights
        mean = float(w @ means)
        variance = float(w @ (var + means**2) - mean**2)
        left = float(np.min(means - 12 * sd))
        right = float(np.max(means + 12 * sd))

        def quantile(p: float) -> float:
            return float(brentq(lambda x: float(w @ ndtr((x - means) / sd)) - p, left, right))

        result.append(
            dict(
                time=float(time),
                mean_log=mean,
                sd_log=math.sqrt(max(variance, 0)),
                median_ratio=math.exp(quantile(0.5)),
                lower_95_log=quantile(0.025),
                upper_95_log=quantile(0.975),
                lower_95_ratio=math.exp(quantile(0.025)),
                upper_95_ratio=math.exp(quantile(0.975)),
            )
        )
    return result


def predictive_log_density(fit: TemporalFit, query_time: Real, value: Real, observation_sd: Real) -> float:
    """One held-out summary density; caller supplies past-based anticipated precision."""
    c = posterior_components(fit, [_value(query_time, "query_time")])
    obs_sd = _value(observation_sd, "observation_sd", True)
    val = _value(value, "value")
    var = np.maximum(c["covariances"][:, 0, 0] + obs_sd**2, 1e-15)
    terms = -0.5 * (math.log(2 * math.pi) + np.log(var) + (val - c["means"][:, 0]) ** 2 / var)
    return float(logsumexp(np.log(fit.weights) + terms))


def sample_temporal(fit: TemporalFit, query: Iterable[Real], draws: int, seed: int) -> Array:
    """Draw one process parameter per full trajectory; retain cross-time covariance."""
    if isinstance(draws, (bool, np.bool_)) or not isinstance(draws, Integral) or draws < 1:
        raise ValueError("draws must be a positive integer")
    c = posterior_components(fit, query)
    rng = np.random.default_rng(seed)
    indices = rng.choice(len(fit.weights), int(draws), p=fit.weights)
    output = np.empty((int(draws), len(c["times"])))
    for index in np.unique(indices):
        where = np.flatnonzero(indices == index)
        cov = c["covariances"][index]
        vals, vecs = np.linalg.eigh(cov)
        root = vecs @ np.diag(np.sqrt(np.maximum(vals, 0.0)))
        output[where] = c["means"][index] + rng.standard_normal((len(where), cov.shape[0])) @ root.T
    return output


def map_discrepancy(
    log_paths: Array,
    matched_releases: Iterable[Real],
    lawful_consumption: Iterable[Real],
    uplift_median: Real,
    shared_log_sd: Real,
    *,
    seed: int = 0,
) -> dict[str, Any]:
    """Map historical proxy paths under a stated common uplift, keeping signed gaps.

    One uplift per trajectory is shared across all years. It is not re-estimated
    from the same release/survey evidence. The source's fixed uplift may be partly
    derived from those data, so treat it as sensitivity, not an independent datum.
    """
    p = np.asarray(log_paths, dtype=float)
    r = _vec(matched_releases, "matched_releases")
    l = _vec(lawful_consumption, "lawful_consumption")
    u = _value(uplift_median, "uplift_median", True)
    s = _value(shared_log_sd, "shared_log_sd")
    if (
        p.ndim != 2
        or not p.shape[0]
        or p.shape[1] != len(r)
        or len(l) != len(r)
        or not np.isfinite(p).all()
        or np.any(r <= 0)
        or np.any(l < 0)
        or s < 0
    ):
        raise ValueError("Incompatible finite positive path/basis inputs")
    bias = np.random.default_rng(seed).lognormal(math.log(u), s, size=p.shape[0])
    with np.errstate(over="raise"):
        try:
            proxy = np.exp(p) * r[None, :] * bias[:, None]
        except FloatingPointError as exc:
            raise ValueError("Proxy overflow") from exc
    gap = proxy - l[None, :]
    return dict(
        survey_proxy=proxy,
        signed_gap=gap,
        uplift=bias,
        calibrated_illicit_volume=False,
        status="assumption_conditional_signed_discrepancy_not_origin_or_crime",
    )
