"""Fit and challenge the annual reported-release component; never compute policy value."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure

import argparse
import csv
import hashlib
import json
import math
import platform
import subprocess
import sys
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import numpy as np  # noqa: E402  # Standalone CLI establishes its local src path before project imports.
import polars as pl  # noqa: E402  # Standalone CLI establishes its local src path before project imports.
import scipy  # noqa: E402  # Standalone CLI establishes its local src path before project imports.
lazy from numpy.typing import NDArray  # noqa: E402  # Standalone CLI establishes its local src path before project imports.

from tobac_supply.longitudinal import rolling_origin_forecasts  # noqa: E402  # Standalone CLI establishes its local src path before project imports.
from tobac_supply.release_calibration import (  # noqa: E402  # Standalone CLI establishes its local src path before project imports.
    ReleaseGrid,
    boundary_mass,
    fit_release_process,
    forecast_summary,
    log_predictive_density,
    parse_release_export,
    sample_release_paths,
)

WINDOWS: dict[str, int | None] = {
    "all_changes": None,
    "recent_4_changes": 4,
    "recent_8_changes": 8,
}
SELECTION_RULE = "mean_log_predictive_density maximised over the exploratory stage; ties broken by row order"
SELECTION_STATISTICS = ("mean_log_predictive_density", "rmse_tonnes", "coverage_95", "mean_interval_score_95")


def write_table(table: pl.DataFrame, path: Path) -> None:
    """Retain the release export's 12-significant-digit, empty-missing CSV contract."""
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(table.columns)
        for row in table.iter_rows():
            writer.writerow(
                ""
                if value is None or (isinstance(value, float) and math.isnan(value))
                else format(value, ".12g")
                if isinstance(value, float)
                else value
                for value in row
            )


def window_names(specs: list[int | None]) -> dict[str, int | None]:
    """Map declared window specifications to the stable model names used in outputs."""
    return {("all_changes" if spec is None else f"recent_{int(spec)}_changes"): spec for spec in specs}


def configured_windows(cfg: dict[str, Any]) -> dict[str, int | None]:
    """Return the model names for the declared windows, rejecting collapsed specs.

    Args:
      cfg: Calibration config holding a `windows` list of change counts or None.

    Returns:
      Model-name to window mapping, in declaration order.

    Raises:
      ValueError: If two declared specifications share one model name.

    """
    declared = cfg["windows"]
    named = window_names(declared)
    if len(named) != len(declared):
        msg = (
            f"Config declares {len(declared)} windows but {len(named)} distinct model "
            f"names result from {declared!r}; window specifications must be distinct"
        )
        raise ValueError(msg)
    return named


def stage_names(
    start_year: int,
    selection_end: int,
    years: NDArray[np.int_],
) -> tuple[str, str]:
    """Return the exploratory and reserved labels implied by the split arguments."""
    return (
        f"exploratory_selection_{start_year}_{selection_end}",
        f"reserved_diagnostic_{selection_end + 1}_{int(years[-1])}",
    )


def provenance() -> dict[str, Any]:
    """Record the executed revision and command; unavailable git reports None/False."""

    def git(*args: str) -> str | None:
        try:
            done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)  # noqa: S603, S607  # Reviewed fixed executable/argv, bounded invocation, no shell.; Fixed git subcommand in the trusted local tool environment, no shell.
        except OSError:
            return None
        return done.stdout.strip() if done.returncode == 0 else None

    commit = git("rev-parse", "HEAD")
    status = git("status", "--porcelain")
    return {
        "commit": commit,
        "command": " ".join(sys.argv),
        "worktree_dirty": bool(status) if status is not None else False,
    }


def sha(path: Path | str) -> str:
    """Return the SHA-256 digest of the supplied source bytes."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path: Path | str, obj: dict[str, Any]) -> None:
    """Write the supplied report as formatted JSON."""
    Path(path).write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def reconcile_sources(root: Path | str, cfg: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the supplied completion against the accepted series, echoing cfg scope.

    Args:
      root: Repository root holding both the accepted series and the completion.
      cfg: Executed calibration config; its exclusions and unresolved items are
        carried into the receipt so the receipt cannot disagree with the config.

    Returns:
      Reconciliation receipt for `source_reconciliation.json`.

    Raises:
      ValueError: If the completion disagrees with the accepted series, or if the
        config omits `exclusions` or `unresolved`.

    """
    root = Path(root)
    for key in ("exclusions", "unresolved"):
        if key not in cfg:
            msg = f"Config must declare {key!r}; got keys {sorted(cfg)}"
            raise ValueError(msg)
    old = root / "data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv"
    raw = root / "data/calibration_20261024/raw/tobacco_returns_completion.txt"
    extracted = parse_release_export(raw.read_text(), range(2010, 2026))
    existing = pl.read_csv(old)
    expected = [
        {"year": int(year), "tonnes": int(value)}
        for year, value in zip(
            np.asarray(existing["year"], dtype=np.int64),
            np.asarray(existing["value"], dtype=np.int64),
            strict=True,
        )
    ]
    if extracted != expected:
        msg = "Supplied completion conflicts with accepted series; investigate, do not overwrite"
        raise ValueError(msg)
    return {
        "status": "matched_all_rows",
        "rows": len(extracted),
        "new_independent_observations": 0,
        "accepted_table": str(old.relative_to(root)),
        "accepted_sha256": sha(old),
        "completion_receipt": str(raw.relative_to(root)),
        "completion_sha256": sha(raw),
        "workbook_independently_read": False,
        "source_kind": "conversation-supplied browser numerical-table extraction",
        "source_run_id": "d26e9dec-6327-41f7-a08e-ff95cb3fee3a",
        "exclusions": list(cfg["exclusions"]),
        "unresolved": list(cfg["unresolved"]),
        "note": "Separate from rejected NZHS extraction; no workbook equivalence claim",
    }


def absolute_percentage_error(observed: float, predicted: float) -> float:
    """Percent error of a point prediction against a reported positive level.

    Args:
      observed: Reported level; must be positive for the ratio to exist.
      predicted: Point prediction on the same scale.

    Returns:
      Absolute percent error of `predicted` relative to `observed`.

    Raises:
      ValueError: If `observed` is not greater than zero (including NaN).

    """
    if not observed > 0:
        msg = f"observed must be > 0 for MAPE; got {observed!r}"
        raise ValueError(msg)
    return 100 * abs(predicted - observed) / observed


def interval_score(observed: float, lower: float, upper: float, alpha: float) -> float:
    """Weighted interval score; `alpha` is the nominal tail mass, strictly inside (0, 1).

    Raises:
      ValueError: If `alpha` is not strictly between zero and one.

    """
    if not 0 < alpha < 1:
        msg = f"alpha must be in (0,1); got {alpha!r}"
        raise ValueError(msg)
    return float(upper - lower + (2 / alpha) * (max(lower - observed, 0) + max(observed - upper, 0)))


def hindcasts(  # noqa: PLR0913, PLR0917  # Preserve explicit dimensioned inputs and the established API.; Preserve the established positional calling convention.
    years: NDArray[np.int_],
    values: NDArray[np.float64],
    grid: ReleaseGrid,
    start_year: int,
    selection_end: int,
    windows: dict[str, int | None] | None = None,
) -> list[dict[str, Any]]:
    """Evaluate the declared rolling-origin designs using only their prior observations."""
    rows: list[dict[str, Any]] = []
    exploratory, reserved = stage_names(start_year, selection_end, years)
    for name, window in (WINDOWS if windows is None else windows).items():
        for index, year in enumerate(years):
            if year < start_year:
                continue
            posterior = fit_release_process(
                years, values, window=window, through_year=int(year) - 1, grid=grid
            )
            pred = forecast_summary(posterior, [1])[0]
            observed = float(values[index])
            rows.append(
                dict(
                    model=name,
                    train_end_year=posterior.last_year,
                    first_change_year=posterior.first_change_year,
                    n_training_changes=posterior.n_changes,
                    test_year=int(year),
                    observed_tonnes=observed,
                    **{
                        k: pred[k] for k in ("mean", "median", "lower_95", "upper_95", "lower_80", "upper_80")
                    },
                    absolute_percentage_error=absolute_percentage_error(observed, pred["median"]),
                    squared_error=(pred["median"] - observed) ** 2,
                    log_predictive_density=log_predictive_density(posterior, observed),
                    interval_score_95=interval_score(observed, pred["lower_95"], pred["upper_95"], 0.05),
                    covered_95=pred["lower_95"] <= observed <= pred["upper_95"],
                    stage=(exploratory if year <= selection_end else reserved),
                    vintage="single_2026_release_retrospective_not_realtime",
                )
            )
    return rows


def figures(  # noqa: PLR0913, PLR0915, PLR0917  # Preserve explicit dimensioned inputs and the established API.; Keep the declared numerical/report sequence visible and ordered.; Preserve the established positional calling convention.
    out: Path,
    years: NDArray[np.int_],
    values: NDArray[np.float64],
    forecasts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
    selected: str,
) -> None:
    """Render release projections and retrospective diagnostics with their scope caveats."""
    import matplotlib as mpl  # noqa: PLC0415  # Keep optional dependencies and backend selection lazy.

    mpl.use("Agg")
    import matplotlib.pyplot as plt  # noqa: PLC0415  # Keep optional dependencies and backend selection lazy.
    from matplotlib.ticker import MaxNLocator  # noqa: PLC0415  # Keep optional dependencies and backend selection lazy.

    mpl.rcParams["svg.hashsalt"] = "tobac-release-calibration-2.8.0"
    folder = out / "figures"
    folder.mkdir()

    def save(fig: Figure, stem: str) -> None:
        fig.tight_layout()
        fig.savefig(folder / (stem + ".png"), dpi=220)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
        fig.savefig(folder / (stem + ".svg"), metadata={"Date": None})  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
        plt.close(fig)

    df = pl.DataFrame(forecasts)
    h = pl.DataFrame(checks, infer_schema_length=None)
    chosen = df.filter(pl.col("model") == selected)

    fig, ax = plt.subplots(figsize=(10, 5.7))
    ax.plot(years, values, "o-", label="Published releases, 2010\u20132025")  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.plot(  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
        chosen["year"], chosen["median"], "o--", label=f"Conditional median: {selected.replace('_', ' ')}"
    )  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.fill_between(  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
        chosen["year"], chosen["lower_95"], chosen["upper_95"], alpha=0.14, label="95% predictive interval"
    )
    ax.fill_between(  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
        chosen["year"], chosen["lower_80"], chosen["upper_80"], alpha=0.22, label="80% predictive interval"
    )
    ax.axvline(2025.5, linestyle=":", alpha=0.6)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.set(
        xlabel="Calendar year",
        ylabel="Reported releases (tonnes/year)",
        title="NZ lawful smoked-tobacco releases: observations and conditional projection",
    )
    ax.legend(fontsize=8, loc="upper right")  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.grid(axis="y", alpha=0.2)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(bottom=0)
    fig.text(  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
        0.01,
        0.01,
        "Reported releases are not total consumption or illicit supply. Later years are exploratory.",
        fontsize=8,
    )
    fig.subplots_adjust(bottom=0.16)
    save(fig, "01_reported_release_projection")

    fig, ax = plt.subplots(figsize=(9, 4.8))
    one = df.filter(pl.col("horizon") == 1)
    for i, r in enumerate(one.iter_rows(named=True)):
        ax.errorbar(  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
            r["median"],
            i,
            xerr=[[r["median"] - r["lower_95"]], [r["upper_95"] - r["median"]]],
            fmt="o",
            capsize=5,
        )
    ax.set_yticks(range(len(one)), [m.replace("_", " ") for m in one["model"]])  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.axvline(values[-1], linestyle=":", label="2025 reported value")  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.set(
        xlabel="Projected 2026 reported releases (tonnes/year)",
        title="Structural sensitivity: 2026 release projection",
    )
    ax.grid(axis="x", alpha=0.2)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.legend(fontsize=8)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    save(fig, "02_window_sensitivity")

    fig, ax = plt.subplots(figsize=(10, 5.3))
    observed = h.filter(pl.col("model") == selected)
    ax.plot(observed["test_year"], observed["observed_tonnes"], "o-", label="Held-out reported releases")  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.plot(observed["test_year"], observed["median"], "s--", label="One-year-ahead predictive median")  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.fill_between(  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
        observed["test_year"],
        observed["lower_95"],
        observed["upper_95"],
        alpha=0.2,
        label="95% predictive interval",
    )
    ax.axvline(2022.5, linestyle=":", label="Exploratory selection / reserved diagnostic split")  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.set(
        xlabel="Held-out observation year",
        ylabel="Reported releases (tonnes/year)",
        title="Retrospective predictive checks, using only earlier observations",
    )
    ax.grid(axis="y", alpha=0.2)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.legend(fontsize=8)  # pyright: ignore[reportUnknownMemberType]  # Matplotlib kwargs lack types.
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    save(fig, "03_rolling_predictive_checks")

    (out / "FIGURE_CAPTIONS.md").write_text("""# Figure captions — release 2.8.0

1. **NZ reported lawful smoked-tobacco releases and conditional projection.** Observations
are the official numerical-table values, 2010\u20132025. The displayed candidate is chosen by
an exploratory 2015\u20132022 log-score comparison. Bands are conditional posterior-predictive
80% and 95% intervals, not uncertainty about illegal consumption or policy effects. 2026
is the primary horizon; 2027\u20132030 extrapolate constant transition parameters without shocks.

2. **Recency-window sensitivity for 2026.** Dots show posterior-predictive medians; whiskers
show 95% intervals for all-history, four-change and eight-change models. A window of four
changes uses five annual levels. Models are alternatives, not independent evidence.

3. **Retrospective one-step predictive checks.** Each target year is withheld from its own
fit. The source is one 2026 publication vintage, and the split was selected after the series
had been seen. This is not real-time validation, preregistration or blinded testing.

All figures: unit = reported tonnes/year. Excludes cigars/cigarillos and heated tobacco.
The domestic/duty-free and mass-conversion bases remain unresolved. NZ = New Zealand.
Predictive intervals include fitted drift and innovation uncertainty conditional on the
model/prior; not stock, source-definition, measurement-bias or future policy uncertainty.
Source: data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv.
""")


def selection_report(
    select: pl.DataFrame,
    start_year: int,
    end_year: int,
) -> dict[str, Any]:
    """Summarise the exploratory ranking and the margin over the runner-up.

    Args:
      select: Exploratory-stage score rows sorted by descending
        mean_log_predictive_density, with row order breaking ties.
      start_year: First exploratory selection year.
      end_year: Last exploratory selection year.

    Returns:
      Additive selection-receipt fields: the ranking, the margin over the
      runner-up, an interpretation of that margin and the selection rule.

    Raises:
      ValueError: If a reported statistic is non-finite.

    """
    scores: list[dict[str, Any]] = []
    for row in select.iter_rows(named=True):
        record: dict[str, Any] = {"model": str(row["model"])}
        for statistic in SELECTION_STATISTICS:
            value = float(row[statistic])
            if not math.isfinite(value):
                msg = (
                    f"Non-finite {statistic} for model {row['model']!r}: {value!r}; "
                    "cannot report a selection margin"
                )
                raise ValueError(msg)
            record[statistic] = value
        scores.append(record)
    margin = None
    if len(scores) > 1:
        margin = scores[0]["mean_log_predictive_density"] - scores[1]["mean_log_predictive_density"]
    return {
        "selection_scores": scores,
        "margin_over_runner_up": margin,
        "margin_interpretation": (
            f"Exploratory comparison on {start_year}-{end_year}, not a "
            "model-selection result; a small margin does not distinguish models."
        ),
        "selection_rule": SELECTION_RULE,
    }


def run(  # noqa: PLR0915  # Keep the declared numerical/report sequence visible and ordered.
    out: Path | str,
    quick: bool = False,  # noqa: FBT001, FBT002  # Preserve the established public positional flag convention.
    draws: int | None = None,
    skip_figures: bool = False,  # noqa: FBT001, FBT002  # Preserve the established public positional flag convention.
) -> dict[str, Any]:
    """Run the declared analysis and write provenance-bound outputs."""
    out = Path(out).resolve()
    if out.exists() and any(out.iterdir()):
        msg = (
            f"Output directory must be empty: {out} already contains files; "
            "a fresh, unused directory is required"
        )
        raise ValueError(msg)
    out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((ROOT / "configs/calibration_v2.8.0/model.json").read_text())
    windows = configured_windows(cfg)
    grid = ReleaseGrid(**cfg["grid"])
    if quick:
        grid = replace(grid, mu_points=51, sigma_points=25)
    n = draws if draws is not None else (256 if quick else cfg["path_draws"])
    receipt = reconcile_sources(ROOT, cfg)
    save_json(out / "source_reconciliation.json", receipt)
    data = pl.read_csv(ROOT / cfg["source_table"])
    years = data["year"].cast(pl.Int64).to_numpy()
    values = data["value"].cast(pl.Float64).to_numpy()
    exploratory_stage, _ = stage_names(cfg["hindcast_start"], cfg["selection_end"], years)
    clean = pl.DataFrame(
        {
            "year": years,
            "reported_tonnes": values.astype(int),
            "year_on_year_percent": np.r_[np.nan, 100 * (values[1:] / values[:-1] - 1)],
            "source_id": data["source_id"],
            "unit": data["unit"],
        }
    )
    write_table(clean, out / "reported_release_series.csv")
    checks = hindcasts(years, values, grid, cfg["hindcast_start"], cfg["selection_end"], windows)
    checkdf = pl.DataFrame(checks, infer_schema_length=None)
    write_table(checkdf, out / "rolling_predictive_checks.csv")
    score = (
        checkdf.group_by(["model", "stage"])
        .agg(
            pl.len().alias("n"),
            pl.col("log_predictive_density").mean().alias("mean_log_predictive_density"),
            pl.col("absolute_percentage_error").mean().alias("mape_percent"),
            pl.col("squared_error").mean().sqrt().alias("rmse_tonnes"),
            pl.col("covered_95").mean().alias("coverage_95"),
            pl.col("interval_score_95").mean().alias("mean_interval_score_95"),
        )
        .sort(["model", "stage"])
        .select(
            "model",
            "stage",
            "n",
            "mean_log_predictive_density",
            "mape_percent",
            "coverage_95",
            "mean_interval_score_95",
            "rmse_tonnes",
        )
    )
    write_table(score, out / "predictive_scores.csv")
    select = score.filter(pl.col("stage") == exploratory_stage).sort(
        "mean_log_predictive_density", descending=True, maintain_order=True
    )
    selected = str(select["model"][0])
    receipt = {
        "selected_for_display": selected,
        "selection_years": [cfg["hindcast_start"], cfg["selection_end"]],
        "reserved_diagnostic_years": list(cfg["reserved_diagnostic_years"]),
        "qualification": cfg["selection_qualification"],
        "optimality_claim": False,
        "all_candidates_retained": list(windows),
    }
    receipt.update(selection_report(select, cfg["hindcast_start"], cfg["selection_end"]))
    save_json(out / "selection_receipt.json", receipt)
    references = [
        row
        for method, window in [("last", None), ("loglinear", 4)]
        for row in rolling_origin_forecasts(years, values, min_train=5, window=window, method=method)
    ]
    write_table(pl.DataFrame(references), out / "point_reference_hindcasts.csv")

    forecasts: list[dict[str, Any]] = []
    parameters: list[dict[str, Any]] = []
    posterior_cells: list[pl.DataFrame] = []
    sensitivity: list[dict[str, Any]] = []
    convergence: list[dict[str, Any]] = []
    path_stats: list[dict[str, Any]] = []

    for offset, (name, window) in enumerate(windows.items()):
        p = fit_release_process(years, values, window=window, grid=grid)
        summaries = forecast_summary(p, cfg["forecast_horizons"])
        forecasts.extend([dict(model=name, **r) for r in summaries])
        parameters.append(
            {
                "model": name,
                "n_changes": p.n_changes,
                "first_change_year": p.first_change_year,
                "last_year": p.last_year,
                "mean_mu": float(p.weights @ p.mu),
                "mean_sigma": float(p.weights @ p.sigma),
                "outer_grid_mass": boundary_mass(p),
            }
        )
        posterior_cells.append(
            pl.DataFrame({"model": name, "mu": p.mu, "sigma": p.sigma, "posterior_mass": p.weights})
        )
        paths = sample_release_paths(p, 5, n, cfg["seed"] + offset)
        pathdf = pl.DataFrame(paths["values"], orient="row", schema=[str(y) for y in paths["years"]])
        pathdf.insert_column(0, pl.Series("posterior_sigma", paths["sigma"]))
        pathdf.insert_column(0, pl.Series("posterior_mu", paths["mu"]))
        pathdf.insert_column(0, pl.Series("path_id", np.arange(n)))
        write_table(pathdf, out / (name + "_joint_paths.csv"))
        for i, row in enumerate(summaries):
            simulation_mean = float(paths["values"][:, i].mean())
            mcse = float(paths["values"][:, i].std(ddof=1) / np.sqrt(n)) if n > 1 else None
            path_stats.append(
                {
                    "model": name,
                    "year": row["year"],
                    "draws": n,
                    "analytic_mean": row["mean"],
                    "simulation_mean": simulation_mean,
                    "mcse_mean": mcse,
                }
            )
        for attr in ["mu_prior_sd", "sigma_prior_scale"]:
            for scale in cfg["prior_scale_sensitivity"]:
                alt = replace(grid, **{attr: scale})
                fit = fit_release_process(years, values, window=window, grid=alt)
                sensitivity.append(
                    dict(model=name, varied=attr, prior_scale=scale, **forecast_summary(fit, [1])[0])
                )
        fine = replace(grid, mu_points=2 * grid.mu_points - 1, sigma_points=2 * grid.sigma_points - 1)
        finepost = fit_release_process(years, values, window=window, grid=fine)
        for coarse, refined in zip(
            forecast_summary(p, [1, 5]), forecast_summary(finepost, [1, 5]), strict=True
        ):
            convergence.extend(
                {
                    "model": name,
                    "horizon": coarse["horizon"],
                    "measure": measure,
                    "coarse": coarse[measure],
                    "fine": refined[measure],
                    "relative_difference": abs(coarse[measure] - refined[measure]) / abs(refined[measure]),
                }
                for measure in ["mean", "median", "lower_95", "upper_95"]
            )
    write_table(pl.DataFrame(forecasts), out / "forecast_summary.csv")
    write_table(pl.DataFrame(parameters), out / "posterior_parameter_summary.csv")
    write_table(pl.concat(posterior_cells), out / "posterior_cells.csv")
    write_table(pl.DataFrame(sensitivity), out / "prior_sensitivity.csv")
    write_table(pl.DataFrame(convergence), out / "grid_convergence.csv")
    write_table(pl.DataFrame(path_stats), out / "monte_carlo_checks.csv")
    save_json(
        out / "fit_scope.json",
        {
            "status": "partial_empirical_reported_release_calibration",
            "country": cfg["country"],
            "version": cfg["version"],
            "analysis_date": cfg["analysis_date"],
            "observed_annual_levels": len(years),
            "observation_years": [int(years[0]), int(years[-1])],
            "fitted_likelihood": cfg["likelihood"],
            "grid_prior": asdict(grid),
            "reported_values_treatment": cfg["reported_values_treatment"],
            "unit": cfg["unit"],
            "estimand": cfg["estimand"],
            "consumption_bridge": {
                "enabled": False,
                "requires": [
                    "source_scope_reconciliation",
                    "stock_and_visitor_adjustments",
                    "catchment_allocation",
                    "lawful_unrecorded_supply",
                ],
            },
            "current_joint_wastewater_model_fitted": False,
            "illicit_consumption_fitted": False,
            "price_quote_received": False,
            "funding_recommendation": False,
        },
    )
    if not skip_figures:
        figures(out, years, values, forecasts, checks, selected)
    source_paths = [
        cfg["source_table"],
        cfg["source_completion"],
        "configs/calibration_v2.8.0/model.json",
        "scripts/run_release_calibration.py",
        "src/tobac_supply/release_calibration.py",
        "src/tobac_supply/longitudinal.py",
    ]
    save_json(
        out / "run_manifest.json",
        {
            "version": cfg["version"],
            "analysis_date": cfg["analysis_date"],
            "status": "partial_empirical_reported_release_calibration",
            "funding_recommendation": False,
            **provenance(),
            "quick_mode": quick,
            "figures_generated": not skip_figures,
            "draws_per_model": n,
            "seed": cfg["seed"],
            "environment": {
                "python": platform.python_version(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "polars": pl.__version__,
            },
            "sources": [{"path": p, "sha256": sha(ROOT / p)} for p in source_paths],
            "files": [
                {"path": str(p.relative_to(out)), "sha256": sha(p)}
                for p in sorted(out.rglob("*"))
                if p.is_file()
            ],
        },
    )
    return {
        "out": str(out),
        "selected_for_display": selected,
        "observations": 16,
        "files": len(list(out.rglob("*"))),
        "funding_recommendation": False,
    }


def main() -> None:
    """Parse command-line options, execute the selected operation and report its result."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--draws", type=int)
    parser.add_argument("--skip-figures", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.out, args.quick, args.draws, args.skip_figures), indent=2))  # noqa: T201  # CLI emits the requested structured result on stdout.


if __name__ == "__main__":
    main()
