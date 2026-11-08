"""Audit source-native period coverage without admitting or joining observations."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from calendar import monthrange
from dataclasses import asdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]
from audit_empirical_coverage import nzhs_candidates  # noqa: E402
from source_handoff import checked, digest, read, same_hash  # noqa: E402

from tobac.evidence import Scope  # noqa: E402

SOURCE_NAMES = ("nzhs", "methods", "price", "population", "trade_imports", "trade_exports")
RELEASE = "data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv"
QUARTER = re.compile(r"[0-9]{4}Q[1-4]")
MONTH = re.compile(r"[0-9]{6}")
QUARTERS_PER_YEAR = 4
PRICE_HEADER_ROWS = 2
POPULATION_HEADER_ROWS = 4
TRADE_BASE = ("Month", "Harmonised System Code", "Harmonised System Description", "Unit Qty")
TRADE_IMPORT = ("Imports ($NZD vfd)", "Imports ($NZD cif)", "Imports Qty")
TRADE_EXPORT = (
    "Exports ($NZD fob)",
    "Exports Qty",
    "Re-exports ($NZD fob)",
    "Re-exports Qty",
    "Total Exports ($NZD fob)",
    "Total Exports Qty",
)


def source(entry: dict[str, Any]) -> tuple[Path, str]:
    """Resolve a CLI file pin through the existing path/hash guards."""
    if set(entry) != {"root", "file", "sha256"} or not all(isinstance(v, str) for v in entry.values()):
        msg = "Specify exactly root, file and sha256 for each source"
        raise ValueError(msg)
    root = Path(entry["root"])
    if not root.is_absolute() or root.is_symlink():
        msg = "Use an absolute nonsymlink source root"
        raise ValueError(msg)
    path = checked(root, entry["file"])
    same_hash(root, entry["file"], entry["sha256"])
    return path, entry["sha256"]


def native_csv(path: Path, headers: int) -> tuple[list[list[str]], list[list[str]], list[str]]:
    """Separate Infoshare header/data/footer records before columnar analysis."""
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.reader(stream))
    end = rows.index(["Table information:"])
    if end <= headers:
        msg = "Empty or malformed Infoshare data section"
        raise ValueError(msg)
    return rows[:headers], [r for r in rows[headers:end] if any(r)], [r[0] for r in rows[end:] if r]


def quarter_bounds(label: str) -> tuple[date, date]:
    """Calendar bounds of a source quarter label, not interview dates."""
    if QUARTER.fullmatch(label) is None:
        msg = f"Invalid calendar quarter: {label}"
        raise ValueError(msg)
    year, end_month = int(label[:4]), int(label[-1]) * 3
    return date(year, end_month - 2, 1), date(year, end_month, monthrange(year, end_month)[1])


def overlap(start: date, end: date, scope: Scope) -> bool:
    """Test interval overlap without assuming identical measurement periods."""
    return start <= date.fromisoformat(scope.end) and end >= date.fromisoformat(scope.start)


def quarters(labels: list[str]) -> list[str]:
    """Reject malformed and duplicate native quarters; preserve absent occasions."""
    for label in labels:
        quarter_bounds(label)
    if not labels or len(labels) != len(set(labels)):
        msg = "Native quarters must be nonempty and unique"
        raise ValueError(msg)
    return sorted(labels)


def positive_decimal(value: str) -> Decimal:
    """Reject nonfinite or nonpositive numeric values rather than coercing them."""
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        msg = "Invalid numeric source field"
        raise ValueError(msg) from exc
    if not result.is_finite() or result <= 0:
        msg = "Expected a finite positive source value"
        raise ValueError(msg)
    return result


def price_coverage(path: Path, scope: Scope) -> dict[str, Any]:
    """Reconcile the exact source price series without allocating a fieldwork price."""
    header, rows, footer = native_csv(path, PRICE_HEADER_ROWS)
    if (
        header[1] != ["", "CPIQ.SAP0240"]
        or "CPI019AA" not in footer
        or not any("Unit = $" in line and "pk of 25" in line for line in footer)
        or not any("applying index movements" in line for line in footer)
        or any(len(row) != PRICE_HEADER_ROWS for row in rows)
    ):
        msg = "SAP0240 source series, units, method or layout changed"
        raise ValueError(msg)
    labels = quarters([row[0] for row in rows])
    for row in rows:
        positive_decimal(row[1])
    return {
        "series": "CPIQ.SAP0240",
        "unit": "source_dollars_per_pack_of_25",
        "role": "index_derived_price_proxy",
        "quarters": len(labels),
        "overlapping_quarters": [q for q in labels if overlap(*quarter_bounds(q), scope)],
        "fieldwork_weighted_price_available": False,
    }


def fill_labels(row: list[str]) -> list[str]:
    """Expand repeated Infoshare column headings, never data cells."""
    result: list[str] = []
    last = ""
    for label in row:
        if label.strip():
            last = label.strip()
        result.append(last)
    return result


def population_coverage(path: Path, survey_label: str) -> dict[str, Any]:
    """Check nominal benchmark occasions, retaining raw missingness and flags."""
    header, rows, footer = native_csv(path, POPULATION_HEADER_ROWS)
    width = len(header[3])
    if "DPE054AA" not in footer or any(len(row) != width for row in header + rows):
        msg = "DPE054AA identity or population layout changed"
        raise ValueError(msg)
    estimate, sex = (fill_labels(header[i]) for i in (1, 2))
    matches = [
        i
        for i, age in enumerate(header[3])
        if age == "15 Years and Over" and estimate[i] == "As at" and sex[i] == "Total"
    ]
    if len(matches) != 1 or matches[0] + 1 >= width or header[3][matches[0] + 1]:
        msg = "Expected one age15plus total As-at value and its native flag column"
        raise ValueError(msg)
    index = matches[0]
    quarters([row[0] for row in rows])
    table = pl.DataFrame(
        {
            "quarter": [r[0] for r in rows],
            "value": [r[index] for r in rows],
            "flag": [r[index + 1] for r in rows],
        }
    )
    if any(flag.strip() not in ("", "C", "E", "P", "R", "S") for flag in table["flag"]):
        msg = "Unknown native population status flag"
        raise ValueError(msg)
    year = int(survey_label)
    nominal = [f"{year}Q3", f"{year}Q4", f"{year + 1}Q1", f"{year + 1}Q2"]
    chosen = table.filter(pl.col("quarter").is_in(nominal)).sort("quarter")
    absent = sorted(set(nominal) - set(chosen["quarter"]))
    unavailable = chosen.filter(
        pl.col("value").is_in(["", ".."]) | pl.col("flag").str.strip_chars().is_in(["C", "S"])
    )
    available = chosen.join(unavailable.select("quarter"), on="quarter", how="anti")
    values = [positive_decimal(v) for v in available["value"]]
    return {
        "table_reference": "DPE054AA",
        "selection": "NZ_total_age15plus_quarter_end_As_at",
        "nominal_quarters": nominal,
        "absent_quarters": absent,
        "unavailable_quarters": unavailable["quarter"].to_list(),
        "nonfinal_flags": chosen.filter(pl.col("flag").str.strip_chars().str.len_chars() > 0)
        .select("quarter", "flag")
        .to_dicts(),
        "quarter_end_mean_diagnostic": str(sum(values) / QUARTERS_PER_YEAR)
        if len(values) == QUARTERS_PER_YEAR
        else None,
        "substitutes_for_published_survey_benchmark": False,
    }


def trade_coverage(path: Path, scope: Scope, *, exports: bool) -> dict[str, Any]:
    """Preserve HS10 products and separate export/re-export fields."""
    table = pl.read_csv(path, infer_schema_length=0, empty_string_is_null=False)
    fields = TRADE_EXPORT if exports else TRADE_IMPORT
    keys = ["Month", "Harmonised System Code"]
    if tuple(table.columns) != TRADE_BASE + fields + ("Status",) or table.is_empty():
        msg = "Unexpected original HS10 CSV columns or no rows"
        raise ValueError(msg)
    if table.select(pl.struct(keys).n_unique()).item() != table.height:
        msg = "Duplicate HS10 product/month"
        raise ValueError(msg)
    if not table[keys[1]].str.contains(r"^[0-9]{10}$").all():
        msg = "HS10 identifiers must retain ten digits"
        raise ValueError(msg)
    candidates = table.filter(pl.col(keys[1]).str.starts_with("24"))
    months = table["Month"].unique().sort().to_list()
    matching: list[str] = []
    for label in months:
        if MONTH.fullmatch(label) is None:
            msg = f"Invalid trade month: {label}"
            raise ValueError(msg)
        year, month = int(label[:4]), int(label[-2:])
        if overlap(date(year, month, 1), date(year, month, monthrange(year, month)[1]), scope):
            matching.append(label)
    return {
        "original_rows": table.height,
        "hs24_candidates": candidates.height,
        "source_months": months,
        "overlapping_months": matching,
        "overlapping_hs24_months": [m for m in matching if m in set(candidates["Month"])],
        "source_quantity_units": candidates["Unit Qty"].unique().sort().to_list(),
        "source_statuses": candidates["Status"].unique().sort().to_list(),
        "original_flow_fields": list(fields),
        "consumption_conversion_available": False,
    }


def release_coverage(scope: Scope) -> dict[str, Any]:
    """Reuse the existing consumer inventory for the calendar-year series."""
    inventory = read(checked(ROOT, "integration/archive/consumer-inputs.json"))
    matches = [row for row in inventory["inputs"] if row["path"] == RELEASE]
    if len(matches) != 1:
        msg = "Registered release input not unique"
        raise ValueError(msg)
    item = matches[0]
    same_hash(ROOT, RELEASE, item["sha256"])
    table = pl.read_csv(checked(ROOT, RELEASE))
    same_hash(ROOT, RELEASE, item["sha256"])
    if table.height != item["rows"] or table.columns != item["columns"]:
        msg = "Registered release CSV structure mismatch"
        raise ValueError(msg)
    years = table["year"].sort().to_list()
    if years != list(range(years[0], years[-1] + 1)):
        msg = "Release years must be contiguous and unique"
        raise ValueError(msg)
    return {
        "path": RELEASE,
        "sha256": item["sha256"],
        "rows": table.height,
        "unit": table["unit"].unique().sort().to_list(),
        "overlapping_calendar_years": [y for y in years if overlap(date(y, 1, 1), date(y, 12, 31), scope)],
        "allocated_to_survey_fieldwork": False,
    }


def reconcile(inputs: dict[str, Any]) -> dict[str, Any]:
    """Run a bounded candidate report; never issue a data or admission contract."""
    if set(inputs) != {*SOURCE_NAMES, "survey_scope", "survey_start_label"}:
        msg = "Provide the six file pins, survey scope and survey-start label"
        raise ValueError(msg)
    sources = {name: source(inputs[name]) for name in SOURCE_NAMES}
    scope = Scope(**inputs["survey_scope"])
    if (scope.geography, scope.population, scope.unit) != (
        "NZ_national",
        "NZHS_adults_15plus",
        "percent_adults_15plus",
    ):
        msg = "Declare the supported NZ adult prevalence scope; no cross-country or unit transport"
        raise ValueError(msg)
    with sources["methods"][0].open("rb") as stream:
        if stream.read(5) != b"%PDF-":
            msg = "Expected the pinned survey methods PDF"
            raise ValueError(msg)
    label = inputs["survey_start_label"]
    if (
        not isinstance(label, str)
        or re.fullmatch(r"[0-9]{4}", label) is None
        or int(label) != date.fromisoformat(scope.start).year
        or int(label) + 1 != date.fromisoformat(scope.end).year
    ):
        msg = "Declared fieldwork must retain its matching survey-start label"
        raise ValueError(msg)
    nzhs, candidates = nzhs_candidates(*sources["nzhs"])
    selected = candidates.filter(pl.col("year") == label)
    if selected.is_empty():
        msg = "Declared survey-start label has no NZHS candidates"
        raise ValueError(msg)
    result = {
        "purpose": "candidate_period_compatibility_audit_not_observation_admission",
        "scope": asdict(scope),
        "scope_status": "declared_and_bound_to_methods_bytes_not_semantic_or_native_admission",
        "survey_start_label": label,
        "source_sha256": {name: sha for name, (_, sha) in sources.items()},
        "nzhs": {
            "all_candidates": nzhs["candidate_records"],
            "selected_label_candidates": selected.height,
            "source_series_units": {row["indicator"]: row["unit"] for row in nzhs["series"]},
            "flagged_selected_rows": selected.filter(
                pl.col("flag_for_publishing").str.len_chars() > 0
            ).height,
        },
        "price": price_coverage(sources["price"][0], scope),
        "population": population_coverage(sources["population"][0], label),
        "trade_imports": trade_coverage(sources["trade_imports"][0], scope, exports=False),
        "trade_exports": trade_coverage(sources["trade_exports"][0], scope, exports=True),
        "releases": release_coverage(scope),
        "dependence": [
            "ERP informs NZHS calibration; counts and prevalence are not independent",
            "SAP0240 levels use index movements; no independent paid-price observation",
            "Export, re-export and total export fields are related, not independent flows",
            "Release mass, trade quantities and survey measures require distinct product and period bridges",
        ],
        "joined_observations": 0,
        "new_observations_admitted": False,
        "likelihood_or_fit_executed": False,
    }
    for path, sha in sources.values():
        same_hash(path.parent, path.name, sha)
    return result


def main() -> None:
    """Write one exclusive, deterministic audit report from explicit file pins."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if sys.version_info[:3] != (3, 15, 2):
        msg = "This audit is qualified only on repository Python 3.15.2"
        raise ValueError(msg)
    config_hash = digest(args.inputs)
    result = reconcile(read(args.inputs))
    same_hash(args.inputs.parent, args.inputs.name, config_hash)
    result.update(
        input_config_sha256=config_hash, reconciler_sha256=digest(Path(__file__)), polars=pl.__version__
    )
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
