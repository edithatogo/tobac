"""Inventory accepted historical CSV bytes; never fit or admit empirical observations."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]
from source_handoff import checked, read, same_hash  # noqa: E402

NZHS_INDICATORS = (
    "Current smokers",
    "Daily smokers",
    "Mean number of cigarettes",
    "Daily vaping",
    "Daily smoker and daily vaper",
    "Daily smoker only",
    "Daily vaper only",
    "Daily smoker and/or daily vaper",
)
NZHS_COLUMNS = (
    "population",
    "short.description",
    "year",
    "group",
    "total",
    "flag_for_publishing",
    "total.low.CI",
    "total.high.CI",
    "male",
    "male_flag_for_publishing",
    "male.low.CI",
    "male.high.CI",
    "female",
    "female_flag_for_publishing",
    "female.low.CI",
    "female.high.CI",
    "estimated.number",
    "estimated.number.low.CI",
    "estimated.number.high.CI",
)
NZHS_FIRST_YEAR = 2011
NZHS_LAST_YEAR = 2024


def _nzhs_row_status(row: dict[str, Any], indicator: str) -> tuple[int, str]:
    """Separate source flags and missingness from a dimensionally valid marginal triplet."""
    year = row["year"]
    if (
        not isinstance(year, str)
        or len(year) != len(str(NZHS_FIRST_YEAR))
        or not year.isascii()
        or not year.isdigit()
        or not NZHS_FIRST_YEAR <= int(year) <= NZHS_LAST_YEAR
    ):
        msg = "NZHS year must retain a qualified four-digit survey-start label"
        raise ValueError(msg)
    flag = row["flag_for_publishing"]
    if flag not in ("", "S", "e"):
        msg = "Unknown NZHS publication flag; retain source and requalify"
        raise ValueError(msg)
    if flag:
        return int(year), "flagged_for_review"
    strings = [row[name] for name in ("total", "total.low.CI", "total.high.CI")]
    if any(value in (None, "", "NA") for value in strings):
        return int(year), "missing_triplets"
    try:
        estimate, low, high = (Decimal(value) for value in strings)
    except (InvalidOperation, TypeError) as exc:
        msg = "Invalid NZHS estimate or confidence interval"
        raise ValueError(msg) from exc
    if (
        not all(value.is_finite() for value in (estimate, low, high))
        or not Decimal(0) <= low <= estimate <= high
        or (indicator != "Mean number of cigarettes" and high > Decimal(100))
    ):
        msg = "Invalid NZHS estimate or confidence interval"
        raise ValueError(msg)
    return int(year), "unflagged_complete_triplets"


def _nzhs_series(rows: list[dict[str, Any]], indicator: str) -> dict[str, Any]:
    """Report actual coverage without interpolating an absent survey occasion."""
    if not rows:
        msg = f"NZHS indicator absent: {indicator}"
        raise ValueError(msg)
    years: list[int] = []
    statuses: dict[str, list[int]] = {
        "unflagged_complete_triplets": [],
        "flagged_for_review": [],
        "missing_triplets": [],
    }
    for row in rows:
        year, status = _nzhs_row_status(row, indicator)
        years.append(year)
        statuses[status].append(year)
    if len(years) != len(set(years)):
        msg = f"Duplicate NZHS indicator/survey-year: {indicator}"
        raise ValueError(msg)
    return {
        "indicator": indicator,
        "unit": "cigarettes/day/daily_smoker_excluding_mainly_pipes_cigars"
        if indicator == "Mean number of cigarettes"
        else "percent_adults_15plus",
        "survey_start_labels": sorted(years),
        **{key: sorted(values) for key, values in statuses.items()},
        "absent_year_labels": sorted(set(range(min(years), max(years) + 1)) - set(years)),
    }


def nzhs_candidates(source: Path, sha256: str) -> tuple[dict[str, Any], pl.DataFrame]:
    """Reconcile published adult totals without manufacturing a likelihood or calendar panel."""
    same_hash(source.parent, source.name, sha256)
    table = pl.read_csv(checked(source.parent, source.name), infer_schema_length=0)
    same_hash(source.parent, source.name, sha256)
    if tuple(table.columns) != NZHS_COLUMNS:
        msg = "NZHS prevalence export schema changed; requalify its original columns"
        raise ValueError(msg)
    selected = table.with_row_index("source_record_ordinal", offset=1).filter(
        (pl.col("population") == "adults")
        & (pl.col("group") == "Total")
        & pl.col("short.description").is_in(NZHS_INDICATORS)
    )
    summaries: list[dict[str, Any]] = []
    for indicator in NZHS_INDICATORS:
        rows = selected.filter(pl.col("short.description") == indicator).to_dicts()
        summaries.append(_nzhs_series(rows, indicator))
    return {
        "source_file": source.name,
        "source_sha256": sha256,
        "source_family": "NZHS",
        "source_alias": "nz-key-results-2024-25",
        "native_admission_checked": False,
        "new_observations_admitted": False,
        "candidate_records": selected.height,
        "source_export_records": table.height,
        "period_kind": "survey_start_year_label_not_calendar_year",
        "iso_observation_dates_verified": False,
        "joint_covariance_available": False,
        "holdout_manifest_frozen": False,
        "series": summaries,
        "limits": [
            "All original columns and publication flags retained; flagged values are not usable triplets",
            "Estimated numbers, prevalence and time-series exports share NZHS respondents",
            "Cigarette intensity uses range midpoints and a top-coded upper category",
            "Daily-smoking prevalence and intensity do not have identical pipe/cigar coverage",
            "Survey periods cannot be equated to calendar-year releases without a supported bridge",
            "No population reconstructed from rounded estimated counts divided by prevalence",
            "No consumption product, independence assumption, likelihood, fit or predictive score created",
        ],
    }, selected.sort(["short.description", "year"])


def main() -> None:
    """Write a hash-bound scope audit from the existing consumer inventory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--nzhs-csv", type=Path)
    parser.add_argument("--nzhs-sha256")
    parser.add_argument("--candidate-out", type=Path)
    args = parser.parse_args()
    nzhs_args = (args.nzhs_csv, args.nzhs_sha256, args.candidate_out)
    if any(value is not None for value in nzhs_args) and not all(value is not None for value in nzhs_args):
        parser.error("NZHS extraction requires --nzhs-csv, --nzhs-sha256 and --candidate-out together")
    if args.candidate_out is not None and (
        args.candidate_out.resolve().is_relative_to(ROOT.resolve()) or args.candidate_out.exists()
    ):
        parser.error("Use a new external candidate output; preserve originals and existing editions")
    if sys.version_info[:3] != (3, 15, 2):
        msg = "This audit is qualified only on repository Python 3.15.2"
        raise ValueError(msg)
    inventory = read(checked(ROOT, "integration/archive/consumer-inputs.json"))
    selected = (
        "data/empirical_intake_20261024/nz_historical_legal_supply.csv",
        "data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv",
    )
    rows: list[dict[str, Any]] = []
    for name in selected:
        matches = [r for r in inventory["inputs"] if r["path"] == name]
        if len(matches) != 1:
            msg = f"Ambiguous or missing inventory entry: {name}"
            raise ValueError(msg)
        expected = matches[0]
        same_hash(ROOT, name, expected["sha256"])
        table = pl.read_csv(checked(ROOT, name))
        if table.height != expected["rows"] or table.columns != expected["columns"]:
            msg = f"Inventory structure mismatch: {name}"
            raise ValueError(msg)
        years = table["year"].to_list()
        if sorted(years) != list(range(min(years), max(years) + 1)):
            msg = f"Duplicate or missing annual periods: {name}"
            raise ValueError(msg)
        rows.append(
            {
                "path": name,
                "sha256": expected["sha256"],
                "rows": table.height,
                "years": years,
                "units": table["unit"].unique().sort().to_list(),
                "source_ids": table["source_id"].unique().sort().to_list(),
                "limitations": table["limitations"].unique().sort().to_list(),
                "role": expected["role"],
                "native_admission_checked": False,
                "new_observations_admitted": False,
            }
        )
    result: dict[str, Any] = {
        "schema_version": 1,
        "scope": "historical_input_coverage_only_not_fit_or_scientific_acceptance",
        "timestamp": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "polars": pl.__version__,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "inventory_sha256": hashlib.sha256(
            checked(ROOT, "integration/archive/consumer-inputs.json").read_bytes()
        ).hexdigest(),
        "sources": rows,
    }
    if args.nzhs_csv is not None and args.nzhs_sha256 is not None and args.candidate_out is not None:
        summary, candidates = nzhs_candidates(args.nzhs_csv, args.nzhs_sha256)
        result["nzhs_candidates"] = summary
        args.candidate_out.parent.mkdir(parents=True, exist_ok=True)
        with args.candidate_out.open("x", encoding="utf-8", newline="") as stream:
            candidates.write_csv(stream)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    sys.stdout.write(json.dumps({"output": str(args.out), "sources_checked": len(rows)}) + "\n")


if __name__ == "__main__":
    main()
