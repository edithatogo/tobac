"""Bounded temporal calculations; no fitted NZ panel or causal effects are implied.

Dates use half-open intervals. Correlation concerns the stationary random component,
not the common calibration error. All planning variances must be supplied explicitly.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from datetime import date
import math
from numbers import Integral, Real
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.special import ndtri


def _date(value: str) -> date:
    if not isinstance(value, str):
        raise ValueError("Dates must be ISO YYYY-MM-DD strings")
    try:
        result = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Invalid date: {value}") from exc
    if result.isoformat() != value:
        raise ValueError("Dates must use YYYY-MM-DD")
    return result


def _number(value: Real, name: str, minimum: float | None = None) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite number, not a boolean")
    result = float(value)
    if not math.isfinite(result) or (minimum is not None and result < minimum):
        raise ValueError(f"Invalid {name}")
    return result


def _vector(values: Iterable[Real], name: str) -> NDArray[np.float64]:
    try:
        data = [_number(v, name) for v in values]
    except TypeError as exc:
        raise ValueError(f"{name} must be a numeric sequence") from exc
    if not data:
        raise ValueError(f"{name} must not be empty")
    return np.asarray(data, dtype=np.float64)


def choose_vintage(records: Sequence[Mapping[str, Any]], as_of: str) -> list[dict[str, Any]]:
    """Choose one available release per series/period, without treating revisions as evidence.

    Publication availability is distinct from the observation period. Callers must
    supply truthful availability dates; a retrieval date is conservative when unknown.
    Equal-date conflicting estimates fail rather than silently taking the last row.
    """
    cutoff = _date(as_of)
    selected: dict[tuple[str, str, str], dict[str, Any]] = {}
    units: dict[str, str] = {}
    for position, source in enumerate(records):
        row = deepcopy(dict(source))
        try:
            raw_series, raw_unit = row['series_id'], row['unit']
        except KeyError as exc:
            raise ValueError(f"Missing vintage field: {exc}") from exc
        # Validate identity before coercion: str(None)/str(nan) would otherwise
        # become truthy labels and merge unrelated series.
        for field, value in (('series_id', raw_series), ('unit', raw_unit)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"Invalid {field} in vintage row {position}: a non-empty "
                    f"string is required, not {value!r}")
        series, unit = raw_series.strip(), raw_unit.strip()
        try:
            start, end = _date(row['period_start']), _date(row['period_end'])
            available = _date(row['available_on'])
            _number(row['value'], 'value')
        except KeyError as exc:
            raise ValueError(f"Missing vintage field: {exc}") from exc
        if end <= start:
            raise ValueError(
                f"Invalid observation period in vintage row {position}: "
                f"period_end must be later than period_start")
        if series in units and units[series] != unit:
            raise ValueError(f"Incompatible unit in {series}")
        units[series] = unit
        if available > cutoff:
            continue
        key = series, start.isoformat(), end.isoformat()
        previous = selected.get(key)
        if previous is None or available > _date(previous['available_on']):
            selected[key] = row
        elif available == _date(previous['available_on']):
            if row['value'] != previous['value']:
                raise ValueError(f"Conflicting estimates for same vintage: {key}")
    return [selected[k] for k in sorted(selected)]


def continuous_correlation(days: Iterable[Real], half_life_days: Real) -> NDArray[np.float64]:
    """Exponential lag correlation using actual elapsed days, not row positions.

    With zero half-life, distinct days are independent but duplicate-day samples
    still share the same daily state. Laboratory replicate errors belong elsewhere.
    """
    t = _vector(days, 'days')
    half = _number(half_life_days, 'half_life_days', 0)
    distance = np.abs(t[:, None] - t[None, :])
    if half == 0:
        return (distance == 0).astype(np.float64)
    return np.exp(-math.log(2) * distance / half)


def effective_sample_size(days: Iterable[Real], half_life_days: Real) -> float:
    """Variance-equivalent n of the arithmetic mean of a stationary daily component.

    This is neither MCMC ESS nor a count of independent people/catchments. Unequal
    weights, nonstationarity and shared calibration require explicit covariance.
    """
    correlation = continuous_correlation(days, half_life_days)
    return float(correlation.shape[0] ** 2 / correlation.sum())


def log_observation_covariance(
    days: Iterable[Real], daily_cv: Real, analytic_cv: Real,
    shared_cv: Real, half_life_days: Real,
) -> NDArray[np.float64]:
    """Covariance for lognormal random-day, technical and shared-error components.

    Each CV represents a separate component. Do not also include a composite CV
    containing the same flow/population/analytical errors. Shared calibration is
    constant across the supplied observations; batch changes need another block.
    """
    d = _number(daily_cv, 'daily_cv', 0)
    a = _number(analytic_cv, 'analytic_cv', 0)
    s = _number(shared_cv, 'shared_cv', 0)
    correlation = continuous_correlation(days, half_life_days)
    n = len(correlation)
    return (math.log1p(d*d) * correlation + math.log1p(a*a) * np.eye(n)
            + math.log1p(s*s) * np.ones((n, n)))


def contrast_log_se(covariance: NDArray[np.float64], weights: Iterable[Real]) -> float:
    """Standard error of a fixed linear contrast on the log scale."""
    c = np.asarray(covariance, dtype=np.float64)
    w = _vector(weights, 'weights')
    if c.shape != (w.size, w.size) or not np.isfinite(c).all():
        raise ValueError("Invalid covariance dimensions or entries")
    if not np.allclose(c, c.T, atol=1e-12, rtol=1e-12):
        raise ValueError("Covariance must be symmetric")
    scale = max(1.0, float(np.max(np.abs(c))))
    if np.linalg.eigvalsh(c).min() < -1e-10 * scale:
        raise ValueError("Covariance must be positive semidefinite")
    return math.sqrt(max(0.0, float(w @ c @ w)))


def aggregate_uniform_years(
    annual_totals: Mapping[int, Real], start: str, end: str,
) -> dict[str, Any]:
    """Allocate annual totals to a half-open window, assuming uniform daily releases.

    `allocated_total` is the window's share of the supplied annual totals and is in
    the same unit as `annual_totals` (for example tonnes or cigarette equivalents).
    It is NOT a per-day or per-365-day rate: convert explicitly with `covered_days`.

    This does not recover monthly observations. Leap-year denominators are exact;
    a year without a supplied total is an error, not an implicit zero.
    """
    begin, finish = _date(start), _date(end)
    if finish <= begin:
        raise ValueError("end must be later than start")
    clean: dict[int, float] = {}
    for year, value in annual_totals.items():
        if isinstance(year, bool) or not isinstance(year, Integral) or not 1 <= year <= 9998:
            raise ValueError("Invalid annual year")
        clean[int(year)] = _number(value, 'annual total', 0)
    total = 0.0
    components: list[dict[str, Any]] = []
    for year in range(begin.year, finish.year + 1):
        left, right = max(begin, date(year, 1, 1)), min(finish, date(year+1, 1, 1))
        days = (right-left).days
        if days <= 0:
            continue
        if year not in clean:
            raise ValueError(f"Missing annual total for {year}")
        denominator = (date(year+1, 1, 1)-date(year, 1, 1)).days
        contribution = clean[year] * days / denominator
        total += contribution
        components.append(dict(year=year, overlap_days=days, year_days=denominator,
                               contribution=contribution))
    return dict(allocated_total=total, covered_days=(finish-begin).days,
                components=components,
                status='uniform_within_year_allocation_assumption')


def rolling_origin_forecasts(
    years: Iterable[Real], values: Iterable[Real], min_train: int = 4,
    window: int | None = None, method: str = 'loglinear',
) -> list[dict[str, Any]]:
    """Expanding/rolling descriptive hindcasts with held-out future observations.

    This does not imply real-time vintage validation. With a latest-vintage input,
    it is a retrospective series check. No forecast interval or causal effect is
    estimated; the last-observation method provides a simple reference.

    `window` counts the most recent training observations (rows), not calendar
    years: with irregular spacing a window of w rows can span more than w years.
    `min_train` likewise counts observations, so the first origin uses the first
    `min_train` rows as training and the next row as the test observation.

    `error` is `predicted - observed` (positive means over-prediction); it is NOT
    the conventional forecast residual `observed - predicted`. The field name is
    fixed because published CSV schemas depend on it.
    """
    x, y = _vector(years, 'years'), _vector(values, 'values')
    if len(x) != len(y) or np.any(np.diff(x) <= 0) or np.any(y <= 0):
        raise ValueError("Years must increase and positive values must align")
    if isinstance(min_train, bool) or not isinstance(min_train, Integral) or min_train < 2:
        raise ValueError("min_train must be an integer of at least two")
    if window is not None and (isinstance(window, bool) or not isinstance(window, Integral) or window < 2):
        raise ValueError("window must be an integer of at least two")
    if method not in {'loglinear', 'last'}:
        raise ValueError("Unknown forecasting method")
    if len(x) <= int(min_train):
        raise ValueError(
            f'min_train={int(min_train)} requires at least {int(min_train)+1} '
            f'observations; got {len(x)}')
    result: list[dict[str, Any]] = []
    for i in range(int(min_train), len(x)):
        j = 0 if window is None else max(0, i-int(window))
        tx, ty = x[j:i], y[j:i]
        if method == 'last':
            predicted = float(ty[-1])
        else:
            slope, intercept = np.polyfit(tx-tx[0], np.log(ty), 1)
            predicted = math.exp(float(intercept+slope*(x[i]-tx[0])))
        observed = float(y[i])
        result.append(dict(train_start=float(tx[0]), train_end=float(tx[-1]),
                           train_n=len(tx), test_year=float(x[i]), observed=observed,
                           predicted=predicted, error=predicted-observed,
                           absolute_percentage_error=100*abs(predicted-observed)/observed,
                           method=method, window=window,
                           status='retrospective_current_vintage_hindcast'))
    return result


def time_bridge(
    anchor_mean: Real, elapsed_years: Real, reference_horizon: Real,
    reference_common_cv: Real, relative_cv: Real, drift_fraction: Real,
    mean_log_slope: Real = 0,
) -> dict[str, Any]:
    """Time-index a declared planning distribution; not an empirical posterior.

    Common log variance = q*t + variance(slope)*t^2, anchored to the supplied CV
    at the reference horizon. The split is analyst-declared. A separate relative
    variance remains at t=0. These are marginals, not independent longitudinal
    samples: use joint state/covariance modelling for repeated-decision VOI.
    """
    mean = _number(anchor_mean, 'anchor_mean', 0)
    t = _number(elapsed_years, 'elapsed_years', 0)
    horizon = _number(reference_horizon, 'reference_horizon', 0)
    common = _number(reference_common_cv, 'reference_common_cv', 0)
    relative = _number(relative_cv, 'relative_cv', 0)
    fraction = _number(drift_fraction, 'drift_fraction', 0)
    slope = _number(mean_log_slope, 'mean_log_slope')
    if mean == 0 or horizon == 0 or fraction > 1:
        raise ValueError("Positive anchor/horizon and drift fraction in [0,1] required")
    variance_ref = math.log1p(common*common)
    process_variance_per_year = (1-fraction)*variance_ref/horizon
    slope_variance = fraction*variance_ref/horizon**2
    common_variance = process_variance_per_year*t + slope_variance*t*t
    variance = common_variance + math.log1p(relative*relative)
    mean *= math.exp(slope*t)
    log_location = math.log(mean)-variance/2
    sd = math.sqrt(variance)
    return dict(mean=mean, median=math.exp(log_location),
                lower95=math.exp(log_location+float(ndtri(.025))*sd),
                upper95=math.exp(log_location+float(ndtri(.975))*sd),
                log_variance=variance, common_log_variance=common_variance,
                process_variance_per_year=process_variance_per_year,
                slope_variance=slope_variance,
                status='time_indexed_planning_distribution_not_fitted')
