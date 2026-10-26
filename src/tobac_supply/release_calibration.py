"""Empirical transition model of reported lawful releases, NOT tobacco consumption.

Annual log changes are conditionally independent Normal(mu, sigma**2). A bounded
quadrature prior supplies finite predictive level moments and makes every prior
assumption inspectable. The code does not fit stock adjustments, illegal supply,
biomarkers, policy consequences or funding value. Observed releases are treated as
reported; source/administrative errors are outside this likelihood.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterable
from dataclasses import dataclass
from numbers import Integral, Real
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq
from scipy.special import logsumexp, ndtr, ndtri

Array = NDArray[np.float64]
SERIES_LABEL = "Total tobacco sold tonnes (excl. cigars/cigarillos)"


def _float(value: Real, name: str, *, positive: bool = False) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number; got {value!r}")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0):
        requirement = "> 0 and finite" if positive else "finite"
        raise ValueError(f"{name} must be {requirement}; got {value!r}")
    return result


def _int(value: Integral, name: str, minimum: int = 1, maximum: int | None = None) -> int:
    permitted = f"[{minimum}, {maximum}]" if maximum is not None else f">= {minimum}"
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
        raise ValueError(f"{name} must be an integer in {permitted}; got {value!r}")
    if value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{name} must be an integer in {permitted}; got {value!r}")
    return int(value)


def _array(values: Iterable[Real], name: str, *, positive: bool = False) -> Array:
    try:
        result = np.asarray([_float(v, name, positive=positive) for v in values])
    except TypeError as exc:
        raise ValueError(f"{name} must be a numeric vector") from exc
    if not len(result):
        raise ValueError(f"{name} cannot be empty")
    return result


def parse_release_export(text: str, expected_years: Iterable[int]) -> list[dict[str, int]]:
    """Repair only the known unquoted-thousands format in the supplied completion.

    This is NOT a generic CSV fixer. It accepts the exact named series and validates
    grouping, one positive integer total per year, and the entire expected coverage.
    Surrounding prose and the CSV header are ignored; unexpected source years fail.
    """
    expected = [_int(y, "expected_year", 1, 9998) for y in expected_years]
    if not expected or len(set(expected)) != len(expected):
        raise ValueError("Expected coverage must contain unique years")
    if not isinstance(text, str):
        raise ValueError("Export must be text")
    observed: dict[int, int] = {}
    pattern = re.compile(re.escape(SERIES_LABEL) + r",([0-9]{4}),([0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)$")
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith(SERIES_LABEL + ","):
            continue
        match = pattern.fullmatch(line)
        if not match:
            raise ValueError(f"Malformed known-series row: {line}")
        year, value = int(match[1]), int(match[2].replace(",", ""))
        if year in observed or year not in expected or value <= 0:
            raise ValueError("Duplicate/unexpected year or nonpositive reported release")
        observed[year] = value
    if set(observed) != set(expected):
        raise ValueError("Incomplete extraction; missing years are not zero")
    return [dict(year=y, tonnes=observed[y]) for y in sorted(observed)]


@dataclass(frozen=True)
class ReleaseGrid:
    """Proper truncated priors; all ranges/scales are analyst choices."""

    mu_min: float = -0.50
    mu_max: float = 0.25
    mu_points: int = 151
    sigma_min: float = 0.005
    sigma_max: float = 0.30
    sigma_points: int = 60
    mu_prior_mean: float = 0.0
    mu_prior_sd: float = 0.10
    sigma_prior_scale: float = 0.10

    def __post_init__(self) -> None:
        for name in ("mu_min", "mu_max", "mu_prior_mean"):
            _float(getattr(self, name), name)
        for name in ("sigma_min", "sigma_max", "mu_prior_sd", "sigma_prior_scale"):
            _float(getattr(self, name), name, positive=True)
        for name in ("mu_points", "sigma_points"):
            _int(getattr(self, name), name, 3, 2001)
        if self.mu_max <= self.mu_min or self.sigma_max <= self.sigma_min:
            raise ValueError("Prior supports must increase")


def make_grid(grid: ReleaseGrid) -> tuple[Array, Array, Array]:
    """Return flattened mu/sigma cells and normalized trapezoidal prior masses."""
    if not isinstance(grid, ReleaseGrid):
        raise ValueError("grid must be ReleaseGrid")
    mu = np.linspace(grid.mu_min, grid.mu_max, grid.mu_points)
    sigma = np.linspace(grid.sigma_min, grid.sigma_max, grid.sigma_points)
    mw, sw = np.ones(len(mu)), np.ones(len(sigma))
    mw[[0, -1]], sw[[0, -1]] = 0.5, 0.5
    mm, ss = np.meshgrid(mu, sigma, indexing="ij")
    log_prior = (
        -0.5 * ((mm - grid.mu_prior_mean) / grid.mu_prior_sd) ** 2
        - 0.5 * (ss / grid.sigma_prior_scale) ** 2
        + np.log(mw[:, None] * sw[None, :])
    )
    weights = np.exp(log_prior - logsumexp(log_prior))
    return mm.ravel(), ss.ravel(), weights.ravel()


@dataclass(frozen=True)
class ReleasePosterior:
    mu: Array
    sigma: Array
    weights: Array
    last_year: int
    last_value: float
    first_change_year: int
    n_changes: int
    window: int | None

    def __post_init__(self) -> None:
        mu = _array(self.mu, "mu")
        sigma = _array(self.sigma, "sigma", positive=True)
        weights = _array(self.weights, "weights")
        if len(mu) != len(sigma) or len(mu) != len(weights):
            raise ValueError("Posterior vector lengths differ")
        if np.any(weights < 0) or not np.isclose(weights.sum(), 1.0, rtol=0, atol=1e-10):
            raise ValueError("Posterior masses must be nonnegative and sum to one")
        _int(self.last_year, "last_year", 1, 9998)
        _int(self.first_change_year, "first_change_year", 1, self.last_year)
        _int(self.n_changes, "n_changes", 2)
        _float(self.last_value, "last_value", positive=True)
        if self.window is not None:
            _int(self.window, "window", 2)
        if self.last_year - self.first_change_year + 1 != self.n_changes:
            raise ValueError("Change-year coverage does not match n_changes")
        for name, arr in [("mu", mu), ("sigma", sigma), ("weights", weights)]:
            arr.setflags(write=False)
            object.__setattr__(self, name, arr)


def fit_release_process(
    years: Iterable[int],
    values: Iterable[Real],
    *,
    window: int | None = None,
    through_year: int | None = None,
    grid: ReleaseGrid | None = None,
) -> ReleasePosterior:
    """Fit observed annual log changes; explicit through_year prevents future leakage.

    A finite window uses at most that many *changes*, needing window+1 levels.
    In early hindcasts a shorter available prefix is used. Gaps are an error, not
    an invitation to create unobserved annual data or silently annualise changes.
    """
    x = np.asarray([_int(y, "year", 1, 9998) for y in years])
    y = _array(values, "release", positive=True)
    if len(x) != len(y) or len(x) < 3 or np.any(np.diff(x) != 1):
        raise ValueError("At least three contiguous annual levels are required")
    if window is not None:
        window = _int(window, "window", 2)
    if through_year is not None:
        cutoff = _int(through_year, "through_year", 1, 9998)
        mask = x <= cutoff
        x, y = x[mask], y[mask]
        if len(x) < 3:
            raise ValueError("Insufficient observations before cutoff")
    change = np.diff(np.log(y))
    if window is not None:
        change = change[-window:]
    if grid is None:
        grid = ReleaseGrid()
    mu, sigma, prior = make_grid(grid)
    n = len(change)
    # Sufficient statistics avoid a potentially large observations-by-grid array.
    sse = np.sum((change - change.mean()) ** 2) + n * (change.mean() - mu) ** 2
    log_like = -n * np.log(sigma) - 0.5 * sse / (sigma**2) - 0.5 * n * math.log(2 * math.pi)
    log_weights = np.log(prior) + log_like
    weights = np.exp(log_weights - logsumexp(log_weights))
    return ReleasePosterior(mu, sigma, weights, int(x[-1]), float(y[-1]), int(x[-1]) - n + 1, n, window)


def _horizon(value: int) -> int:
    return _int(value, "horizon", 1, 50)


def forecast_summary(posterior: ReleasePosterior, horizons: Iterable[int]) -> list[dict[str, Any]]:
    """Analytic mixture moments and deterministic quantiles of future reported levels.

    Parameter uncertainty is common across a trajectory; innovation variance grows
    with horizon. Forecasts condition on the last reported value, not unknown stocks.
    """
    rows: list[dict[str, Any]] = []
    for horizon in horizons:
        h = _horizon(horizon)
        means, scales = h * posterior.mu, math.sqrt(h) * posterior.sigma
        row: dict[str, Any] = dict(year=posterior.last_year + h, horizon=h)
        row["mean"] = float(
            posterior.last_value * np.sum(posterior.weights * np.exp(means + 0.5 * scales**2))
        )
        for name, q in [
            ("lower_95", 0.025),
            ("lower_80", 0.10),
            ("median", 0.5),
            ("upper_80", 0.90),
            ("upper_95", 0.975),
        ]:
            component_q = means + ndtri(q) * scales
            left, right = float(component_q.min()), float(component_q.max())
            if math.isclose(left, right, rel_tol=0, abs_tol=1e-14):
                quantile = left
            else:
                quantile = brentq(
                    lambda v: float(np.dot(posterior.weights, ndtr((v - means) / scales)) - q),
                    left - 1e-10,
                    right + 1e-10,
                    xtol=1e-12,
                )
            row[name] = posterior.last_value * math.exp(quantile)
        row["probability_below_last_reported"] = float(np.dot(posterior.weights, ndtr(-means / scales)))
        row["estimand"] = "reported_lawful_smoked_tobacco_releases"
        row["unit"] = "tonnes/year"
        rows.append(row)
    return rows


def log_predictive_density(posterior: ReleasePosterior, value: Real, horizon: int = 1) -> float:
    """Log density on the reported-level scale, including the logarithm Jacobian."""
    target, h = _float(value, "target", positive=True), _horizon(horizon)
    active = posterior.weights > 0
    scales = math.sqrt(h) * posterior.sigma[active]
    z = (math.log(target / posterior.last_value) - h * posterior.mu[active]) / scales
    return float(
        logsumexp(
            np.log(posterior.weights[active]) - np.log(scales) - 0.5 * z**2 - 0.5 * math.log(2 * math.pi)
        )
        - math.log(target)
    )


def sample_release_paths(posterior: ReleasePosterior, horizon: int, draws: int, seed: int) -> dict[str, Any]:
    """Sample coherent paths, selecting one posterior parameter pair per path."""
    h = _horizon(horizon)
    n = _int(draws, "draws", 1)
    seed = _int(seed, "seed", 0)
    rng = np.random.default_rng(seed)
    cells = rng.choice(len(posterior.weights), n, p=posterior.weights)
    mu, sigma = posterior.mu[cells], posterior.sigma[cells]
    changes = mu[:, None] + sigma[:, None] * rng.normal(size=(n, h))
    levels = posterior.last_value * np.exp(np.cumsum(changes, axis=1))
    return dict(
        years=np.arange(posterior.last_year + 1, posterior.last_year + h + 1),
        values=levels,
        mu=mu,
        sigma=sigma,
        posterior_cell=cells,
        estimand="reported_lawful_smoked_tobacco_releases",
        unit="tonnes/year",
    )


def boundary_mass(posterior: ReleasePosterior) -> float:
    """Mass in outermost quadrature cells; diagnostic, not MCMC effective sample size."""
    edge = (
        (posterior.mu == posterior.mu.min())
        | (posterior.mu == posterior.mu.max())
        | (posterior.sigma == posterior.sigma.min())
        | (posterior.sigma == posterior.sigma.max())
    )
    return float(posterior.weights[edge].sum())
