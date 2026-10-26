"""Bounded temporal calculations; no fitted NZ panel or causal effects are implied.

Dates use half-open intervals. Correlation concerns the stationary random component,
not the common calibration error. All planning variances must be supplied explicitly.
"""

from __future__ import annotations

import math
from copy import deepcopy
from datetime import date
from numbers import Integral, Real
from typing import TYPE_CHECKING, Any, cast

import numpy as np
from scipy.special import ndtri
lazy from numpy.typing import NDArray

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence


# Named bounds preserve the existing scientific/data contract.
MAX_YEAR_BEFORE_CLOSING = 9998
PAIR_SIZE = 2


def _date(value: str) -> date:
    if not isinstance(cast("object", value), str):
        msg = "Dates must be ISO YYYY-MM-DD strings"
        raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
    try:
        result = date.fromisoformat(value)
    except ValueError as exc:
        msg = f"Invalid date: {value}"
        raise ValueError(msg) from exc
    if result.isoformat() != value:
        msg = "Dates must use YYYY-MM-DD"
        raise ValueError(msg)
    return result


def _number(value: float, name: str, minimum: float | None = None) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(cast("object", value), Real):
        msg = f"{name} must be a finite number, not a boolean"
        raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
    result = float(value)
    if not math.isfinite(result) or (minimum is not None and result < minimum):
        msg = f"Invalid {name}"
        raise ValueError(msg)
    return result


def _vector(values: Iterable[float], name: str) -> NDArray[np.float64]:
    try:
        data = [_number(v, name) for v in values]
    except TypeError as exc:
        msg = f"{name} must be a numeric sequence"
        raise ValueError(msg) from exc
    if not data:
        msg = f"{name} must not be empty"
        raise ValueError(msg)
    return np.asarray(data, dtype=np.float64)


def choose_vintage(records: Sequence[Mapping[str, Any]], as_of: str) -> list[dict[str, Any]]:  # noqa: C901  # Keep ordered model validation and report assembly in one visible operation.
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
            raw_series, raw_unit = row["series_id"], row["unit"]
        except KeyError as exc:
            msg = f"Missing vintage field: {exc}"
            raise ValueError(msg) from exc
        # Validate identity before coercion: str(None)/str(nan) would otherwise
        # become truthy labels and merge unrelated series.
        for field, value in (("series_id", raw_series), ("unit", raw_unit)):
            if not isinstance(value, str) or not value.strip():
                msg = (
                    f"Invalid {field} in vintage row {position}: a non-empty "
                    f"string is required, not {value!r}"
                )
                raise ValueError(msg)
        series, unit = raw_series.strip(), raw_unit.strip()
        try:
            start, end = _date(row["period_start"]), _date(row["period_end"])
            available = _date(row["available_on"])
            _number(row["value"], "value")
        except KeyError as exc:
            msg = f"Missing vintage field: {exc}"
            raise ValueError(msg) from exc
        if end <= start:
            msg = (
                f"Invalid observation period in vintage row {position}: "
                f"period_end must be later than period_start"
            )
            raise ValueError(msg)
        if series in units and units[series] != unit:
            msg = f"Incompatible unit in {series}"
            raise ValueError(msg)
        units[series] = unit
        if available > cutoff:
            continue
        key = series, start.isoformat(), end.isoformat()
        previous = selected.get(key)
        if previous is None or available > _date(previous["available_on"]):
            selected[key] = row
        elif available == _date(previous["available_on"]) and row["value"] != previous["value"]:
            msg = f"Conflicting estimates for same vintage: {key}"
            raise ValueError(msg)
    return [selected[k] for k in sorted(selected)]


def continuous_correlation(days: Iterable[float], half_life_days: float) -> NDArray[np.float64]:
    """Exponential lag correlation using actual elapsed days, not row positions.

    With zero half-life, distinct days are independent but duplicate-day samples
    still share the same daily state. Laboratory replicate errors belong elsewhere.
    """
    t = _vector(days, "days")
    half = _number(half_life_days, "half_life_days", 0)
    distance = np.abs(t[:, None] - t[None, :])
    if half == 0:
        return (distance == 0).astype(np.float64)
    return np.exp(-math.log(2) * distance / half)


def effective_sample_size(days: Iterable[float], half_life_days: float) -> float:
    """Variance-equivalent n of the arithmetic mean of a stationary daily component.

    This is neither MCMC ESS nor a count of independent people/catchments. Unequal
    weights, nonstationarity and shared calibration require explicit covariance.
    """
    correlation = continuous_correlation(days, half_life_days)
    return float(correlation.shape[0] ** 2 / correlation.sum())


def log_observation_covariance(
    days: Iterable[float],
    daily_cv: float,
    analytic_cv: float,
    shared_cv: float,
    half_life_days: float,
) -> NDArray[np.float64]:
    """Covariance for lognormal random-day, technical and shared-error components.

    Each CV represents a separate component. Do not also include a composite CV
    containing the same flow/population/analytical errors. Shared calibration is
    constant across the supplied observations; batch changes need another block.
    """
    d = _number(daily_cv, "daily_cv", 0)
    a = _number(analytic_cv, "analytic_cv", 0)
    s = _number(shared_cv, "shared_cv", 0)
    correlation = continuous_correlation(days, half_life_days)
    n = len(correlation)
    return (
        math.log1p(d * d) * correlation + math.log1p(a * a) * np.eye(n) + math.log1p(s * s) * np.ones((n, n))
    )


def contrast_log_se(covariance: NDArray[np.float64], weights: Iterable[float]) -> float:
    """Compute the standard error of a fixed linear contrast on the log scale."""
    c = np.asarray(covariance, dtype=np.float64)
    w = _vector(weights, "weights")
    if c.shape != (w.size, w.size) or not np.isfinite(c).all():
        msg = "Invalid covariance dimensions or entries"
        raise ValueError(msg)
    if not np.allclose(c, c.T, atol=1e-12, rtol=1e-12):
        msg = "Covariance must be symmetric"
        raise ValueError(msg)
    scale = max(1.0, float(np.max(np.abs(c))))
    if np.linalg.eigvalsh(c).min() < -1e-10 * scale:
        msg = "Covariance must be positive semidefinite"
        raise ValueError(msg)
    return math.sqrt(max(0.0, float(w @ c @ w)))


def aggregate_uniform_years(
    annual_totals: Mapping[int, float],
    start: str,
    end: str,
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
        msg = "end must be later than start"
        raise ValueError(msg)
    clean: dict[int, float] = {}
    for year, value in annual_totals.items():
        if (
            isinstance(year, bool)
            or not isinstance(year, Integral)
            or not 1 <= year <= MAX_YEAR_BEFORE_CLOSING
        ):
            msg = "Invalid annual year"
            raise ValueError(msg)
        clean[int(year)] = _number(value, "annual total", 0)
    total = 0.0
    components: list[dict[str, Any]] = []
    for year in range(begin.year, finish.year + 1):
        left, right = max(begin, date(year, 1, 1)), min(finish, date(year + 1, 1, 1))
        days = (right - left).days
        if days <= 0:
            continue
        if year not in clean:
            msg = f"Missing annual total for {year}"
            raise ValueError(msg)
        denominator = (date(year + 1, 1, 1) - date(year, 1, 1)).days
        contribution = clean[year] * days / denominator
        total += contribution
        components.append(
            {"year": year, "overlap_days": days, "year_days": denominator, "contribution": contribution}
        )
    return {
        "allocated_total": total,
        "covered_days": (finish - begin).days,
        "components": components,
        "status": "uniform_within_year_allocation_assumption",
    }


def rolling_origin_forecasts(
    years: Iterable[float],
    values: Iterable[float],
    min_train: int = 4,
    window: int | None = None,
    method: str = "loglinear",
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
    x, y = _vector(years, "years"), _vector(values, "values")
    if len(x) != len(y) or np.any(np.diff(x) <= 0) or np.any(y <= 0):
        msg = "Years must increase and positive values must align"
        raise ValueError(msg)
    if isinstance(min_train, bool) or not isinstance(min_train, Integral) or min_train < PAIR_SIZE:
        msg = "min_train must be an integer of at least two"
        raise ValueError(msg)
    if window is not None and (
        isinstance(window, bool) or not isinstance(window, Integral) or window < PAIR_SIZE
    ):
        msg = "window must be an integer of at least two"
        raise ValueError(msg)
    if method not in {"loglinear", "last"}:
        msg = "Unknown forecasting method"
        raise ValueError(msg)
    if len(x) <= int(min_train):
        msg = f"min_train={int(min_train)} requires at least {int(min_train) + 1} observations; got {len(x)}"
        raise ValueError(msg)
    result: list[dict[str, Any]] = []
    for i in range(int(min_train), len(x)):
        j = 0 if window is None else max(0, i - int(window))
        tx, ty = x[j:i], y[j:i]
        if method == "last":
            predicted = float(ty[-1])
        else:
            slope, intercept = cast("NDArray[np.float64]", np.polyfit(tx - tx[0], np.log(ty), 1))
            predicted = math.exp(float(intercept + slope * (x[i] - tx[0])))
        observed = float(y[i])
        result.append(
            {
                "train_start": float(tx[0]),
                "train_end": float(tx[-1]),
                "train_n": len(tx),
                "test_year": float(x[i]),
                "observed": observed,
                "predicted": predicted,
                "error": predicted - observed,
                "absolute_percentage_error": 100 * abs(predicted - observed) / observed,
                "method": method,
                "window": window,
                "status": "retrospective_current_vintage_hindcast",
            }
        )
    return result


def time_bridge(  # noqa: PLR0913, PLR0917  # Preserve explicit dimensioned inputs and the established API.; Preserve the established positional calling convention.
    anchor_mean: float,
    elapsed_years: float,
    reference_horizon: float,
    reference_common_cv: float,
    relative_cv: float,
    drift_fraction: float,
    mean_log_slope: float = 0,
) -> dict[str, Any]:
    """Time-index a declared planning distribution; not an empirical posterior.

    Common log variance = q*t + variance(slope)*t^2, anchored to the supplied CV
    at the reference horizon. The split is analyst-declared. A separate relative
    variance remains at t=0. These are marginals, not independent longitudinal
    samples: use joint state/covariance modelling for repeated-decision VOI.
    """
    mean = _number(anchor_mean, "anchor_mean", 0)
    t = _number(elapsed_years, "elapsed_years", 0)
    horizon = _number(reference_horizon, "reference_horizon", 0)
    common = _number(reference_common_cv, "reference_common_cv", 0)
    relative = _number(relative_cv, "relative_cv", 0)
    fraction = _number(drift_fraction, "drift_fraction", 0)
    slope = _number(mean_log_slope, "mean_log_slope")
    if mean == 0 or horizon == 0 or fraction > 1:
        msg = "Positive anchor/horizon and drift fraction in [0,1] required"
        raise ValueError(msg)
    variance_ref = math.log1p(common * common)
    process_variance_per_year = (1 - fraction) * variance_ref / horizon
    slope_variance = fraction * variance_ref / horizon**2
    common_variance = process_variance_per_year * t + slope_variance * t * t
    variance = common_variance + math.log1p(relative * relative)
    mean *= math.exp(slope * t)
    log_location = math.log(mean) - variance / 2
    sd = math.sqrt(variance)
    return {
        "mean": mean,
        "median": math.exp(log_location),
        "lower95": math.exp(log_location + float(ndtri(0.025)) * sd),
        "upper95": math.exp(log_location + float(ndtri(0.975)) * sd),
        "log_variance": variance,
        "common_log_variance": common_variance,
        "process_variance_per_year": process_variance_per_year,
        "slope_variance": slope_variance,
        "status": "time_indexed_planning_distribution_not_fitted",
    }
