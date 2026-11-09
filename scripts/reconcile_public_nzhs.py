"""Reconcile the public NZHS extracts against one reviewed official CSV edition.

This checks source consistency, not empirical admission or independent evidence.
The source digest is deliberately fixed: a changed edition requires a new review.
Original source bytes stay outside the public repository. Repeated representations
retain the same source-cell identity and survey-dependence group.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple, cast

if TYPE_CHECKING:
    from collections.abc import Iterator

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]
from audit_empirical_coverage import NZHS_COLUMNS  # noqa: E402
from source_handoff import checked, read, same_hash  # noqa: E402

QUALIFIED_SOURCE_SHA256 = "6d3e0a019d7e32030147f128c21098f074683cd3cfef41b0dcfff85b74b6b915"
SOURCE_URL = (
    "https://minhealthnz.shinyapps.io/nz-health-survey-2024-25-annual-data-explorer/"
    "data/nz-health-survey-2024-25-prevalences.csv"
)
PACK = "evidence/public_data_20261108"
DEPENDENCE_GROUP = "NZHS_2024_25_shared_survey"
MOH_SOURCE = "nzhs_2024_25_smoking_vaping_moh_20251119"
INDICATORS = {
    "daily_smoking": "Daily smokers",
    "daily_vaping": "Daily vaping",
    "current_vaping_at_least_monthly": "Monthly vaping",
    "daily_smoking_or_vaping_or_both": "Daily smoker and/or daily vaper",
}
COMMON_COLUMNS = ("source_id", "survey_period", "geography", "age_scope")
STRATUM_COLUMNS = ("stratum_type", "stratum")
SUMMARY_COLUMNS = ("indicator", "value", "unit", "uncertainty", "source_section")
CI_COLUMNS = (
    "indicator",
    "value",
    "ci95_lower",
    "ci95_upper",
    "unit",
    "caution_rse_over_30_percent",
    "source_section",
)
TOTAL = (("all_adults", "all"),)
GENDER = (("gender", "men"), ("gender", "women"))
ETHNICITY = tuple(("ethnic_group", value) for value in ("Maori", "Pacific", "European_Other", "Asian"))
DEPRIVATION = tuple(("deprivation", f"NZDep_quintile_{value}") for value in range(1, 6))
AGE = tuple(
    ("age", value) for value in ("15_17", "18_24", "25_34", "35_44", "45_54", "55_64", "65_74", "75_plus")
)


class FileSpec(NamedTuple):
    """Frozen scope of one existing public extraction."""

    source_id: str
    columns: tuple[str, ...]
    strata: tuple[tuple[str, str], ...]
    indicators: tuple[str, ...]
    unit: str
    caution: str


SPECS = {
    "nzhs_counts_2024_25.csv": FileSpec(
        MOH_SOURCE,
        COMMON_COLUMNS + SUMMARY_COLUMNS,
        (("", ""),),
        ("daily_smoking", "daily_vaping"),
        "estimated_people",
        "absent",
    ),
    "nzhs_prevalence_2024_25.csv": FileSpec(
        MOH_SOURCE,
        COMMON_COLUMNS + STRATUM_COLUMNS + SUMMARY_COLUMNS,
        TOTAL + GENDER + (DEPRIVATION[0], DEPRIVATION[-1]) + ETHNICITY,
        ("daily_smoking", "daily_vaping"),
        "percent",
        "absent",
    ),
    "nzhs_vaping_union_ci_2024_25.csv": FileSpec(
        "nzhs_2024_25_phcc_vaping_edwards_20251203",
        COMMON_COLUMNS + STRATUM_COLUMNS + CI_COLUMNS,
        TOTAL + AGE + ETHNICITY + DEPRIVATION,
        ("current_vaping_at_least_monthly", "daily_vaping", "daily_smoking_or_vaping_or_both"),
        "percent",
        "explicit",
    ),
    "nzhs_smoking_ci_2024_25.csv": FileSpec(
        "nzhs_2024_25_phcc_smoking_nip_20251126",
        COMMON_COLUMNS + STRATUM_COLUMNS + CI_COLUMNS,
        TOTAL + ETHNICITY + DEPRIVATION + (AGE[1], AGE[-2], AGE[-1]) + GENDER,
        ("daily_smoking",),
        "percent",
        "not_reported",
    ),
}


def _table(
    path: Path, columns: tuple[str, ...], *, encoding: str = "utf-8"
) -> Iterator[tuple[int, dict[str, str]]]:
    """Read exact headers and reject malformed row widths; ordinals exclude header."""
    with path.open(encoding=encoding, newline="") as stream:
        reader = csv.reader(stream, strict=True)
        if next(reader, None) != list(columns):
            msg = f"Unexpected CSV schema: {path.name}"
            raise ValueError(msg)
        for ordinal, row in enumerate(reader, 1):
            if len(row) != len(columns):
                msg = f"Malformed CSV record {ordinal}: {path.name}"
                raise ValueError(msg)
            yield ordinal, dict(zip(columns, row, strict=True))


def _manifest(root: Path) -> list[dict[str, Any]]:
    """Verify the four extract inventories and their same-survey declarations."""
    manifest = read(checked(root, f"{PACK}/manifest.json"))
    if type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        msg = "Unreviewed public-pack manifest schema"
        raise ValueError(msg)
    if not isinstance(manifest["files"], list) or not isinstance(manifest["sources"], list):
        msg = "Manifest files and sources must be lists"
        raise TypeError(msg)
    files = cast("list[dict[str, Any]]", manifest["files"])
    sources = cast("list[dict[str, Any]]", manifest["sources"])
    inventory = {entry["path"]: entry for entry in files}
    declarations = {entry["source_id"]: entry for entry in sources}
    if len(inventory) != len(files) or len(declarations) != len(sources):
        msg = "Duplicate manifest file or source identity"
        raise ValueError(msg)
    names = {name for name in inventory if name.startswith("nzhs")}
    present = {path.name for path in (root / PACK).glob("nzhs*.csv")}
    if names != set(SPECS) or present != set(SPECS):
        msg = "Unexpected or missing NZHS extract inventory"
        raise ValueError(msg)
    inputs: list[dict[str, Any]] = []
    for name, spec in SPECS.items():
        item = inventory[name]
        source = declarations.get(spec.source_id, {})
        if (
            item.get("columns") != list(spec.columns)
            or type(item.get("rows")) is not int
            or item["rows"] != len(spec.strata) * len(spec.indicators)
            or item.get("source_id") != spec.source_id
            or item.get("empirical_admission") is not False
            or item.get("role") != "descriptive_context"
            or source.get("empirical_admission") is not False
            or source.get("dependence_group") != DEPENDENCE_GROUP
            or (spec.source_id != MOH_SOURCE and source.get("underlying_survey_source_id") != MOH_SOURCE)
        ):
            msg = f"Unreviewed extract manifest or source declaration: {name}"
            raise ValueError(msg)
        path = f"{PACK}/{name}"
        same_hash(root, path, item["sha256"])
        inputs.append(
            {"path": path, "sha256": item["sha256"], "rows": item["rows"], "columns": item["columns"]}
        )
    return inputs


def _source_index(source: Path) -> tuple[dict[tuple[str, str], tuple[int, dict[str, str]]], int]:
    """Bind the official edition and index target survey records with native ordinals."""
    same_hash(source.parent, source.name, QUALIFIED_SOURCE_SHA256)
    selected: dict[tuple[str, str], tuple[int, dict[str, str]]] = {}
    count = 0
    for ordinal, row in _table(source, NZHS_COLUMNS, encoding="utf-8-sig"):
        count = ordinal
        if (
            row["population"] != "adults"
            or row["year"] != "2024"
            or row["short.description"] not in INDICATORS.values()
        ):
            continue
        key = (row["short.description"], row["group"])
        if key in selected:
            msg = f"Duplicate official NZHS source identity: {key}"
            raise ValueError(msg)
        selected[key] = ordinal, row
    return selected, count


def _decimal(value: str, *, name: str) -> Decimal:
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        msg = f"Invalid numeric {name}"
        raise ValueError(msg) from exc
    if not number.is_finite():
        msg = f"Nonfinite {name}"
        raise ValueError(msg)
    return number


def _location(row: dict[str, str], spec: FileSpec) -> tuple[str, str]:
    if spec.unit == "estimated_people":
        return "Total", "estimated.number"
    kind, stratum = row["stratum_type"], row["stratum"]
    if kind == "all_adults":
        return "Total", "total"
    if kind == "gender":
        return "Total", {"men": "male", "women": "female"}[stratum]
    if kind == "age":
        return stratum.replace("_plus", "+").replace("_", "-"), "total"
    if kind == "deprivation":
        return "Quintile " + stratum.removeprefix("NZDep_quintile_"), "total"
    return {"Maori": "Māori", "European_Other": "European/Other"}.get(stratum, stratum), "total"


def _validate_extract(row: dict[str, str], spec: FileSpec) -> tuple[str, str, str]:
    key = (row.get("stratum_type", ""), row.get("stratum", ""), row["indicator"])
    expected = {(kind, stratum, indicator) for kind, stratum in spec.strata for indicator in spec.indicators}
    if (
        key not in expected
        or row["source_id"] != spec.source_id
        or row["survey_period"] != "2024/25"
        or row["geography"] != "NZ_national"
        or row["age_scope"] != "15_plus"
        or row["unit"] != spec.unit
        or not row["source_section"].strip()
        or (spec.caution == "absent" and row["uncertainty"] != "not_provided_in_summary_text")
    ):
        msg = "Extract identity, subgroup, source or scope is unreviewed"
        raise ValueError(msg)
    return key


def _check_values(row: dict[str, str], original: dict[str, str], field: str) -> tuple[str, str, str, str]:
    low, high = field + ".low.CI", field + ".high.CI"
    value = _decimal(original[field], name="source estimate")
    lower, upper = (_decimal(original[column], name="source confidence interval") for column in (low, high))
    if not Decimal(0) <= lower <= value <= upper or (row["unit"] == "percent" and upper > Decimal(100)):
        msg = "Invalid source confidence interval or scale"
        raise ValueError(msg)
    if _decimal(row["value"], name="extract estimate") != value:
        msg = "Extract point estimate does not exactly match official source"
        raise ValueError(msg)
    ci_status = "source_annotation_only"
    if "ci95_lower" in row:
        if (
            _decimal(row["ci95_lower"], name="extract lower confidence interval") != lower
            or _decimal(row["ci95_upper"], name="extract upper confidence interval") != upper
        ):
            msg = "Extract confidence interval does not exactly match official source"
            raise ValueError(msg)
        ci_status = "matched"
    return original[field], original[low], original[high], ci_status


def _check_flag(
    row: dict[str, str], original: dict[str, str], field: str, spec: FileSpec
) -> tuple[str, str, str]:
    flag_field = (
        "flag_for_publishing" if field in ("total", "estimated.number") else field + "_flag_for_publishing"
    )
    flag = original[flag_field]
    if flag not in ("", "e", "S"):
        msg = "Unknown source publication flag"
        raise ValueError(msg)
    if flag == "S":
        msg = "Suppressed source cells cannot be reconciled as numeric observations"
        raise ValueError(msg)
    reported = row.get("caution_rse_over_30_percent", "not_reported")
    if spec.caution == "explicit":
        if reported not in ("true", "false") or (reported == "true") != (flag == "e"):
            msg = "Extract caution flag does not match official source"
            raise ValueError(msg)
        return flag_field, flag, "matched"
    if reported != "not_reported":
        msg = "Unreviewed extract caution flag"
        raise ValueError(msg)
    return flag_field, flag, "not_reported_in_extract"


def _reconcile_row(
    name: str,
    ordinal: int,
    row: dict[str, str],
    spec: FileSpec,
    source_index: dict[tuple[str, str], tuple[int, dict[str, str]]],
) -> dict[str, str]:
    group, field = _location(row, spec)
    key = (INDICATORS[row["indicator"]], group)
    if key not in source_index:
        msg = f"No official source record for extract: {key}"
        raise ValueError(msg)
    source_ordinal, original = source_index[key]
    flag_field, flag, flag_status = _check_flag(row, original, field, spec)
    value, lower, upper, ci_status = _check_values(row, original, field)
    return {
        "extract_path": f"{PACK}/{name}",
        "extract_record_ordinal": str(ordinal),
        "source_id": spec.source_id,
        "survey_period": row["survey_period"],
        "geography": row["geography"],
        "age_scope": row["age_scope"],
        "stratum_type": row.get("stratum_type", "all_adults"),
        "stratum": row.get("stratum", "all"),
        "indicator": row["indicator"],
        "unit": row["unit"],
        "extract_value": row["value"],
        "extract_ci95_lower": row.get("ci95_lower", ""),
        "extract_ci95_upper": row.get("ci95_upper", ""),
        "extract_caution_rse_over_30_percent": row.get("caution_rse_over_30_percent", "not_reported"),
        "source_record_ordinal": str(source_ordinal),
        "source_population": original["population"],
        "source_indicator": original["short.description"],
        "source_year_label": original["year"],
        "source_group": group,
        "source_field": field,
        "source_value": value,
        "source_ci95_lower": lower,
        "source_ci95_upper": upper,
        "source_ci95_lower_field": field + ".low.CI",
        "source_ci95_upper_field": field + ".high.CI",
        "source_flag_field": flag_field,
        "source_publication_flag": flag,
        "point_check": "matched",
        "ci_check": ci_status,
        "caution_check": flag_status,
        "underlying_cell_id": f"{QUALIFIED_SOURCE_SHA256}:record:{source_ordinal}:field:{field}",
        "dependence_group": DEPENDENCE_GROUP,
        "empirical_admission": "false",
    }


def reconcile(source: Path, *, root: Path = ROOT) -> tuple[list[dict[str, str]], dict[str, Any]]:
    """Check all 89 existing extract rows before returning source-bound annotations."""
    inputs = _manifest(root)
    source_index, source_count = _source_index(source)
    records: list[dict[str, str]] = []
    for name, spec in SPECS.items():
        identities: set[tuple[str, str, str]] = set()
        for ordinal, row in _table(checked(root, f"{PACK}/{name}"), spec.columns):
            key = _validate_extract(row, spec)
            if key in identities:
                msg = f"Duplicate extract identity in {name}"
                raise ValueError(msg)
            identities.add(key)
            records.append(_reconcile_row(name, ordinal, row, spec, source_index))
        if len(identities) != len(spec.strata) * len(spec.indicators):
            msg = f"Incomplete extract rows: {name}"
            raise ValueError(msg)
    report: dict[str, Any] = {
        "schema_version": "tobac.public-nzhs-reconciliation.v1",
        "status": "all_extract_rows_match_official_source",
        "original": {
            "url": SOURCE_URL,
            "sha256": QUALIFIED_SOURCE_SHA256,
            "bytes": source.stat().st_size,
            "columns": list(NZHS_COLUMNS),
            "encoding": "utf-8-sig",
            "record_ordinal_convention": "one-based data record excluding header",
        },
        "pack_manifest": f"{PACK}/manifest.json",
        "verified_extracts": inputs,
        "implementation_sha256": {
            f"scripts/{name}": hashlib.sha256((ROOT / "scripts" / name).read_bytes()).hexdigest()
            for name in ("reconcile_public_nzhs.py", "audit_empirical_coverage.py", "source_handoff.py")
        },
        "verification": {
            "point_estimates": len(records),
            "confidence_interval_pairs": sum(row["ci_check"] == "matched" for row in records),
            "explicit_caution_flags": sum(row["caution_check"] == "matched" for row in records),
            "unreported_caution_flags": sum(
                row["extract_path"].endswith("nzhs_smoking_ci_2024_25.csv") for row in records
            ),
            "summary_rows_without_caution_field": sum(
                row["ci_check"] == "source_annotation_only" for row in records
            ),
            "unique_source_cells": len({row["underlying_cell_id"] for row in records}),
            "unique_source_records": len({row["source_record_ordinal"] for row in records}),
            "source_records": source_count,
        },
        "dependence_group": DEPENDENCE_GROUP,
        "independent_observations_added": 0,
        "empirical_admission": False,
        "native_lineage_qualification": False,
        "automatically_conditions_live_model": False,
        "limits": [
            "Source-value verification is separate from archive acceptance and observation admission.",
            "Repeated source cells and counts share the same survey; subgroup estimates also overlap.",
            "Marginal intervals do not identify joint covariance or an exclusive dynamic-state partition.",
            "Source uncertainty annotates summary-only rows without rewriting the original extracts.",
            "This does not establish catchment consumption, transitions, policy effects or illicit origin.",
        ],
    }
    return records, report


def write_reconciliation(source: Path, out: Path, *, root: Path = ROOT) -> dict[str, Any]:
    """Write deterministic derived CSV/JSON only after all input checks succeed."""
    if out.exists() or out.is_symlink():
        msg = "Refusing to overwrite reconciliation output"
        raise ValueError(msg)
    records, report = reconcile(source, root=root)
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    csv_bytes = stream.getvalue().encode("utf-8")
    report["output"] = {
        "path": "nzhs-reconciliation.csv",
        "sha256": hashlib.sha256(csv_bytes).hexdigest(),
        "rows": len(records),
    }
    json_bytes = (json.dumps(report, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    out.mkdir(parents=True, exist_ok=False)
    (out / "nzhs-reconciliation.csv").write_bytes(csv_bytes)
    (out / "nzhs-reconciliation.json").write_bytes(json_bytes)
    return report


def main() -> None:
    """Verify the frozen official source and export reviewable annotations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, required=True, help="Original official NZHS CSV; fixed reviewed digest"
    )
    parser.add_argument(
        "--out", type=Path, required=True, help="New output directory; existing paths are refused"
    )
    args = parser.parse_args()
    try:
        write_reconciliation(args.source, args.out)
    except (ValueError, KeyError, TypeError, OSError, csv.Error) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
