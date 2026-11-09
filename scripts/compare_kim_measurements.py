"""Reproduce source-native Kim measurement checks from one pinned supplement.

This is an edition-specific Poppler layout parser, not a general PDF extractor.
Published loads, duplicate-assay SDs, censoring and absent occasions retain their
meaning. Calibration alternatives are arithmetic sensitivities, not fitted NZ
consumption, a new likelihood, an independent score or empirical admission.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import date
from decimal import Decimal
from itertools import pairwise
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]
from source_handoff import checked, digest, read, same_hash  # noqa: E402

from tobac.partial_identification import Interval  # noqa: E402

PDF_SHA256 = "c2ce1d0c3fcc95e9c49acb5bf403cc2598b999a97b8a9e558557a3aa1614046c"
LAYOUT_SHA256 = "4675a51a4938a717434aa855ce90157a76722c6f2f31be0692793c3df60f7b7a"
SOURCE_URL = "https://ars.els-cdn.com/content/image/1-s2.0-S0048969725028657-mmc1.pdf"
DOI = "10.1016/j.scitotenv.2025.181223"
SITES = (
    "Auckland Central",
    "Auckland North",
    "Auckland South",
    "Auckland West",
    "Hamilton",
    "Gisborne",
    "Wellington",
    "Whangārei",
    "Christchurch",
    "Dunedin",
    "Invercargill",
    "Westport",
)
MONTHS = ("May", "June", "July", "August", "September", "October")
TABLES = {"COT": (34, "S13"), "COT-OH": (37, "S15"), "ANTA": (40, "S17"), "ANBA": (42, "S19")}
UNIT = "mg/day/1000_people_as_reported"
N_SLOTS = 144
N_OCCASIONS = 142
N_ANALYTE_CELLS = 576
N_COLUMNS = 12
NICOTINE_FACTOR = Decimal("1.35")
REVIEW = "conductor/tracks/nz_au_empirical_20261106/first-comparison-review-20261109.md"
AUDIT = "conductor/tracks/nz_au_empirical_20261106/first-comparison-audit-20261109.json"
CONTRACT = "conductor/tracks/nz_au_empirical_20261106/decision-definition.md"
RECONCILIATION = "conductor/tracks/nz_au_empirical_20261106/phase2-reconciliation-20261107.md"
SCENARIOS = (
    {
        "id": "zheng2023_reported",
        "ug_per_cigarette": "0.91",
        "source": "https://doi.org/10.1021/acs.est.3c01510",
        "basis": "assumed_nicotine_dose_and_excretion_times_pooled_urine_ratio",
        "review_location": "P2.30; separate 1.07 sewer correction not applied",
    },
    {
        "id": "bade2020_reported",
        "ug_per_cigarette": "1.13",
        "source": "https://doi.org/10.1002/dta.2874",
        "basis": "ten_smokers_self_reported_cigarettes_and_assumed_1.5L_daily_urine",
        "review_location": "P2.33; printed table/narrative discrepancies retained",
    },
    {
        "id": "weng2026_conditional_dose",
        "ug_per_cigarette": "0.64944",
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13389531/",
        "basis": "0.0902_times_assumed_0.0072mg_absorbed_anabasine_times_1000",
        "review_location": "First-comparison review; 19 selected above-LoQ cigarette users",
    },
)

Row = dict[str, str]


def layout_from_pdf(source: Path, converter: str = "pdftotext") -> tuple[str, dict[str, Any]]:
    """Check original bytes before conversion and require the qualified layout bytes."""
    source = source.absolute()
    same_hash(source.parent, source.name, PDF_SHA256)
    executable = shutil.which(converter)
    if executable is None:
        msg = "The external pdftotext converter is unavailable"
        raise ValueError(msg)
    binary_hash = digest(Path(executable))
    version = subprocess.run(  # noqa: S603 -- Execute an explicitly selected converter without a shell.
        [executable, "-v"],
        capture_output=True,
        check=True,
        timeout=15,
    )
    version_text = (version.stdout + version.stderr).decode("utf-8").splitlines()[0]
    if not version_text.startswith("pdftotext version "):
        msg = "Unexpected converter version response"
        raise ValueError(msg)
    converted = subprocess.run(  # noqa: S603 -- The source and output argument are explicit; no shell.
        [executable, "-layout", "-enc", "UTF-8", str(source), "-"],
        capture_output=True,
        check=True,
        timeout=60,
    )
    if converted.stderr or hashlib.sha256(converted.stdout).hexdigest() != LAYOUT_SHA256:
        msg = "Converter output differs from the qualified layout; review before parsing"
        raise ValueError(msg)
    if digest(Path(executable)) != binary_hash:
        msg = "Converter changed during execution"
        raise ValueError(msg)
    same_hash(source.parent, source.name, PDF_SHA256)
    return converted.stdout.decode("utf-8"), {
        "name": "pdftotext",
        "version": version_text,
        "executable_sha256": binary_hash,
        "arguments": ["-layout", "-enc", "UTF-8", "PINNED_EXTERNAL_PDF", "-"],
        "layout_sha256": LAYOUT_SHA256,
        "layout_bytes": len(converted.stdout),
        "source_bytes": source.stat().st_size,
        "qualification": "Exact output parity, not a portable general-PDF-parser claim",
    }


def table_cells(
    layout: str, page: int, table: str, *, values_above_label: bool = False
) -> dict[str, list[str]]:
    """Read twelve column cells per named plant from the qualified layout edition."""
    pages = layout.split("\f")
    if page > len(pages) or f"Table {table}." not in pages[page - 1]:
        msg = f"Missing source table {table} on PDF page {page}"
        raise ValueError(msg)
    lines = pages[page - 1].splitlines()
    headers = [line for line in lines if len(re.findall(r"\b(?:WED|SUN)\b", line.upper())) == N_COLUMNS]
    if len(headers) != 1:
        msg = f"Ambiguous weekday columns in {table}"
        raise ValueError(msg)
    matches = list(re.finditer(r"\b(?:WED|SUN)\b", headers[0].upper()))
    if [m.group() for m in matches] != ["WED", "SUN"] * len(MONTHS):
        msg = f"Unexpected weekday order in {table}"
        raise ValueError(msg)
    centres = [Decimal(m.start()) + Decimal("1.5") for m in matches]
    cuts = [int(centres[0] - (centres[1] - centres[0]) / 2)]
    cuts += [int((a + b) / 2) for a, b in pairwise(centres)]
    cuts.append(int(centres[-1] + (centres[-1] - centres[-2]) / 2))
    positions: list[tuple[int, str]] = []
    for site in SITES:
        found = [i for i, line in enumerate(lines) if site in line[: cuts[0]]]
        if len(found) != 1:
            msg = f"Missing or duplicate plant row in {table}: {site}"
            raise ValueError(msg)
        positions.append((found[0] - int(values_above_label), site))
    positions.sort()
    result: dict[str, list[str]] = {}
    for index, (start, site) in enumerate(positions):
        end = positions[index + 1][0] if index + 1 < len(positions) else len(lines)
        result[site] = [
            " ".join(" ".join(line[left:right] for line in lines[start:end]).split())
            for left, right in pairwise(cuts)
        ]
    return result


def occasions(layout: str) -> list[Row]:
    """Keep printed dates, nominal columns and every absent occasion separately."""
    cells = table_cells(layout, 8, "S3")
    result: list[Row] = []
    for site in SITES:
        for column, printed in enumerate(cells[site]):
            month, nominal = MONTHS[column // 2], ("WED", "SUN")[column % 2]
            plant_id = site.lower().replace(" ", "_").replace("ā", "a")
            slot = f"kim2025:{plant_id}:2023-{column // 2 + 5:02}:{nominal}"
            row = {
                "slot_id": slot,
                "plant_as_published": site,
                "month_as_published": month,
                "nominal_weekday": nominal,
                "printed_date": printed,
                "collection_date": "",
                "actual_weekday": "",
                "weekday_matches_column": "",
                "occasion_id": "",
                "status": "missing_occasion",
                "source_table": "S3",
                "pdf_page": "8",
            }
            if printed != "-":
                if not re.fullmatch(r"\d{2}/\d{2}/23", printed):
                    msg = f"Unrecognised collection date: {printed}"
                    raise ValueError(msg)
                day = date(2023, int(printed[3:5]), int(printed[:2]))
                if day.month != column // 2 + 5:
                    msg = "Printed collection date is outside its source month"
                    raise ValueError(msg)
                actual = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")[day.weekday()]
                row.update(
                    collection_date=day.isoformat(),
                    actual_weekday=actual,
                    weekday_matches_column=str(actual == nominal).lower(),
                    occasion_id=f"kim2025:{site}:{day.isoformat()}",
                    status="dated_occasion",
                )
            result.append(row)
    dated = [row["occasion_id"] for row in result if row["occasion_id"]]
    absent = [
        (row["plant_as_published"], row["month_as_published"]) for row in result if not row["occasion_id"]
    ]
    if (
        len(result) != N_SLOTS
        or len(set(dated)) != N_OCCASIONS
        or len(dated) != N_OCCASIONS
        or absent != [("Whangārei", "October")] * 2
    ):
        msg = "Occasion identities or missing slots differ from the reviewed source"
        raise ValueError(msg)
    return result


def measurement_cell(printed: str) -> Row:
    """Parse a reported duplicate mean/SD without substituting censored values."""
    result = {"cell_as_published": printed, "mean_as_published": "", "duplicate_sd_as_published": ""}
    if not printed:
        return {**result, "status": "missing_occasion"}
    if printed == "< LoQ":
        return {**result, "status": "between_lod_and_loq"}
    matched = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)\s*±\s*([0-9]+(?:\.[0-9]+)?)", printed)
    if matched is None or Decimal(matched[1]) <= 0:
        msg = f"Unrecognised measurement cell: {printed}"
        raise ValueError(msg)
    return {
        **result,
        "status": "quantified",
        "mean_as_published": matched[1],
        "duplicate_sd_as_published": matched[2],
    }


def measurement_rows(layout: str, dates: list[Row]) -> tuple[list[Row], dict[str, Row]]:
    """Join printed analyte cells by plant/month/column, never by table row order."""
    measurements: list[Row] = []
    totals: dict[str, Row] = {}
    for analyte, (page, table) in {**TABLES, "NICOTINE_DERIVED": (46, "S23")}.items():
        cells = table_cells(layout, page, table, values_above_label=table == "S23")
        for row in dates:
            column = MONTHS.index(row["month_as_published"]) * 2 + int(row["nominal_weekday"] == "SUN")
            cell = measurement_cell(cells[row["plant_as_published"]][column])
            if (cell["status"] == "missing_occasion") != (row["status"] == "missing_occasion"):
                msg = "Measurement missingness disagrees with the occasion table"
                raise ValueError(msg)
            if cell["status"] == "between_lod_and_loq" and analyte != "ANBA":
                msg = "Unexpected censored analyte in this source edition"
                raise ValueError(msg)
            entry = {
                "slot_id": row["slot_id"],
                "occasion_id": row["occasion_id"],
                "plant_as_published": row["plant_as_published"],
                "collection_date": row["collection_date"],
                "month_as_published": row["month_as_published"],
                "nominal_weekday": row["nominal_weekday"],
                "analyte": analyte,
                **cell,
                "unit": UNIT,
                "source_table": table,
                "pdf_page": str(page),
                "dependence_group": row["occasion_id"],
            }
            if analyte == "NICOTINE_DERIVED":
                totals[row["slot_id"]] = entry
            else:
                measurements.append(entry)
    counts = Counter(row["status"] for row in measurements)
    if len(measurements) != N_ANALYTE_CELLS or counts != {
        "quantified": 451,
        "between_lod_and_loq": 117,
        "missing_occasion": 8,
    }:
        msg = "Measurement counts differ from the reviewed source edition"
        raise ValueError(msg)
    return measurements, totals


def decimal_text(value: Decimal) -> str:
    """Retain exact decimal arithmetic without adding apparent source precision."""
    return format(value.normalize(), "f")


def rounding_support(printed: str) -> tuple[Decimal, Decimal]:
    """Nearest-print rounding support is a declared assumption, not a confidence interval."""
    value = Decimal(printed)
    exponent = value.as_tuple().exponent
    if not isinstance(exponent, int) or value < 0:
        msg = "Rounding support requires a finite nonnegative value"
        raise ValueError(msg)
    half = Decimal(1).scaleb(exponent) / 2
    return max(Decimal(0), value - half), value + half


def overlaps(left: tuple[Decimal, Decimal], right: tuple[Decimal, Decimal]) -> bool:
    """Check closed intervals without floating-point tolerance or data repair."""
    return max(left[0], right[0]) <= min(left[1], right[1])


def spread_check(first: str, second: str, total: str) -> Row:
    """Check two paired replicates separately from the wider correlation envelope."""
    a, b, observed = rounding_support(first), rounding_support(second), rounding_support(total)
    difference = (
        NICOTINE_FACTOR * max(Decimal(0), a[0] - b[1], b[0] - a[1]),
        NICOTINE_FACTOR * max(abs(a[0] - b[1]), abs(a[1] - b[0])),
    )
    summed = (NICOTINE_FACTOR * (a[0] + b[0]), NICOTINE_FACTOR * (a[1] + b[1]))
    paired = overlaps(observed, difference) or overlaps(observed, summed)
    envelope = overlaps(observed, (difference[0], summed[1]))
    return {
        "paired_replicate_sd_compatible": str(paired).lower(),
        "broader_sd_envelope_compatible": str(envelope).lower(),
        "sd_compatibility": "paired_endpoint"
        if paired
        else "broader_envelope_only"
        if envelope
        else "outside_broader_envelope",
        "sd_envelope_lower": decimal_text(difference[0]),
        "sd_envelope_upper": decimal_text(summed[1]),
    }


def nicotine_diagnostics(measurements: list[Row], totals: dict[str, Row]) -> list[Row]:
    """Compare S23 to its shared metabolites without adding an independent observation."""
    cot = {row["slot_id"]: row for row in measurements if row["analyte"] == "COT"}
    hydroxy = {row["slot_id"]: row for row in measurements if row["analyte"] == "COT-OH"}
    result: list[Row] = []
    for slot, total in totals.items():
        row = {
            "slot_id": slot,
            "occasion_id": total["occasion_id"],
            "status": total["status"],
            "reported_total_cell": total["cell_as_published"],
            "reported_total_mean": total["mean_as_published"],
            "reported_total_duplicate_sd": total["duplicate_sd_as_published"],
            "reconstructed_mean": "",
            "reported_minus_reconstructed": "",
            "mean_rounding_tolerance": "",
            "mean_compatible_with_rounding": "",
            "paired_replicate_sd_compatible": "",
            "broader_sd_envelope_compatible": "",
            "sd_compatibility": "",
            "sd_envelope_lower": "",
            "sd_envelope_upper": "",
            "unit": UNIT,
            "source_table": "S23",
            "pdf_page": "46",
            "derived_from": "S13;S15",
        }
        if total["status"] == "quantified":
            first, second = cot[slot], hydroxy[slot]
            a, b, observed = (Decimal(item["mean_as_published"]) for item in (first, second, total))
            calculated = NICOTINE_FACTOR * (a + b)
            half_widths = [
                (rounding_support(item["mean_as_published"])[1] - Decimal(item["mean_as_published"]))
                for item in (first, second, total)
            ]
            tolerance = NICOTINE_FACTOR * (half_widths[0] + half_widths[1]) + half_widths[2]
            row.update(
                reconstructed_mean=decimal_text(calculated),
                reported_minus_reconstructed=decimal_text(observed - calculated),
                mean_rounding_tolerance=decimal_text(tolerance),
                mean_compatible_with_rounding=str(abs(observed - calculated) <= tolerance).lower(),
                **spread_check(
                    first["duplicate_sd_as_published"],
                    second["duplicate_sd_as_published"],
                    total["duplicate_sd_as_published"],
                ),
            )
        result.append(row)
    return result


def calibration_rows(measurements: list[Row]) -> list[Row]:
    """Keep each transfer assumption and every censored/absent source slot separate."""
    result: list[Row] = []
    for item in measurements:
        if item["analyte"] != "ANBA":
            continue
        for scenario in SCENARIOS:
            row = {
                "slot_id": item["slot_id"],
                "occasion_id": item["occasion_id"],
                "status": item["status"],
                "scenario": scenario["id"],
                "factor_ug_per_cigarette": scenario["ug_per_cigarette"],
                "reported_load": item["mean_as_published"],
                "load_divided_by_factor": "",
                "rounding_only_lower": "",
                "rounding_only_upper": "",
                "unit": "conditional_cigarette_equivalents/reported_contributing_person/day",
                "interpretation": "measurement_sensitivity_not_admitted_consumption",
            }
            if item["status"] == "quantified":
                factor = Decimal(scenario["ug_per_cigarette"])
                lower, upper = rounding_support(item["mean_as_published"])
                support = Interval(float(lower), float(upper)).divide_positive(
                    Interval(float(factor), float(factor))
                )
                row.update(
                    load_divided_by_factor=format(Decimal(item["mean_as_published"]) / factor, ".12g"),
                    rounding_only_lower=format(support.lower, ".12g"),
                    rounding_only_upper=format(support.upper, ".12g"),
                )
            result.append(row)
    return result


def comparison_report(
    dates: list[Row], measurements: list[Row], diagnostics: list[Row], parser: dict[str, Any]
) -> dict[str, Any]:
    """Report measured-source support and the unchanged first-comparison refusal."""
    audit = read(checked(ROOT, AUDIT))
    if (
        audit["scientific_qualification"]
        or audit["automatically_conditions_live_model"]
        or audit["comparison_readiness"]["status"] != "blocked"
    ):
        msg = "First-comparison review status changed; review this bounded comparison contract"
        raise ValueError(msg)
    dates_present = [row["collection_date"] for row in dates if row["collection_date"]]
    review_hashes = {name: digest(checked(ROOT, name)) for name in (REVIEW, AUDIT, CONTRACT, RECONCILIATION)}
    return {
        "schema_version": "tobac.kim-measurement-comparison.v1",
        "status": "source_native_measurement_sensitivity_and_target_non_identification",
        "original": {"doi": DOI, "url": SOURCE_URL, "sha256": PDF_SHA256, "bytes": parser["source_bytes"]},
        "parser": parser,
        "source_rights": {
            "original_included": False,
            "original_redistribution_permission_established": False,
            "published_material": (
                "Attributed numerical facts and authored derived checks; no article prose or graphics"
            ),
        },
        "source_support": {
            "occasion_slots": len(dates),
            "distinct_plant_labels": len(SITES),
            "dated_occasions": len(dates_present),
            "distinct_calendar_dates": len(set(dates_present)),
            "first_date": min(dates_present),
            "last_date": max(dates_present),
            "nominal_weekday_disagreements": sum(row["weekday_matches_column"] == "false" for row in dates),
            "analyte_cells": len(measurements),
            "analyte_cell_status": dict(Counter(row["status"] for row in measurements)),
            "anba_status": dict(Counter(row["status"] for row in measurements if row["analyte"] == "ANBA")),
            "whole_occasion_grouping": (
                "Four analytes and derived S23 nicotine share each collection occasion"
            ),
        },
        "nicotine_diagnostics": {
            "factor": str(NICOTINE_FACTOR),
            "assumption": "Exact 1.35 times COT plus COT-OH; nearest printed rounding",
            "means_compatible_with_rounding": sum(
                row["mean_compatible_with_rounding"] == "true" for row in diagnostics
            ),
            "means_outside_rounding": sum(
                row["mean_compatible_with_rounding"] == "false" for row in diagnostics
            ),
            "sd_compatibility": dict(
                Counter(row["sd_compatibility"] for row in diagnostics if row["sd_compatibility"])
            ),
            "sd_scope": "Duplicate-assay spread, not population uncertainty or a covariance estimate",
        },
        "calibration_scenarios": list(SCENARIOS),
        "calibration_limits": [
            "Factors are separate transfer assumptions, not independent estimates or a pooled prior.",
            "No sewer-loss, product-attribution or flow/population uncertainty is silently estimated.",
            "mg/day/1000 people divided by ug/cigarette cancels the two factors of 1000.",
            "Rounding-only intervals are not confidence intervals and exclude factor/transport uncertainty.",
            "The Weng 4.95% reported spread is untyped and is not used as SD, SE or a distribution.",
            "Censored/absent cells have no conversion; no selected-subset campaign average is computed.",
        ],
        "first_comparison": {
            "review_audit_status": audit["comparison_readiness"]["status"],
            "qualified_complete_wbe_calendar_years": [],
            "required_earlier_complete_years": 3,
            "required_comparable_catchments": 4,
            "comparable_catchments_qualified": 0,
            "baseline_scope": (
                "National survey-year prevalence/intensity and calendar-year releases; "
                "no matched catchment consumption bridge"
            ),
            "wastewater_scope": (
                "Reported plant-labelled May-October 2023 normalised loads; "
                "unresolved contributing population, flow and censoring"
            ),
            "independent_target_validation": "unavailable",
            "paired_predictive_score": None,
            "policy_response_fitted": False,
            "empirical_voi": None,
            "reason": (
                "Source-native descriptive checks do not qualify the frozen "
                "population/product/period outcome or independent validation"
            ),
        },
        "review_basis_sha256": review_hashes,
        "implementation_sha256": {
            name: digest(checked(ROOT, name))
            for name in (
                "scripts/compare_kim_measurements.py",
                "scripts/source_handoff.py",
                "src/tobac/partial_identification.py",
            )
        },
        "empirical_admission": False,
        "native_lineage_qualification": False,
        "automatically_conditions_live_model": False,
        "independent_observations_added": 0,
    }


def write_csv(path: Path, rows: list[Row]) -> None:
    """Write all declared fields, preserving empty numeric cells and source precision."""
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(source: Path, output: Path, converter: str = "pdftotext") -> dict[str, Any]:
    """Validate and compute before writing a new immutable comparison edition."""
    if output.exists() or output.is_symlink():
        msg = "Refusing to overwrite an existing Kim comparison edition"
        raise ValueError(msg)
    layout, parser = layout_from_pdf(source, converter)
    dates = occasions(layout)
    measurements, totals = measurement_rows(layout, dates)
    diagnostics = nicotine_diagnostics(measurements, totals)
    tables = {
        "occasions.csv": dates,
        "measurements.csv": measurements,
        "nicotine-diagnostics.csv": diagnostics,
        "anabasine-scenarios.csv": calibration_rows(measurements),
    }
    report = comparison_report(dates, measurements, diagnostics, parser)
    for path, sha in report["review_basis_sha256"].items():
        same_hash(ROOT, path, sha)
    output.mkdir(parents=True)
    for name, rows in tables.items():
        write_csv(output / name, rows)
    report["outputs"] = {
        name: {"rows": len(rows), "sha256": digest(output / name)} for name, rows in tables.items()
    }
    with (output / "comparison.json").open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    return report


def main() -> None:
    """Run this pinned-edition comparison with an explicitly supplied external original."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--pdftotext", default="pdftotext")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if sys.version_info[:3] != (3, 15, 2):
        parser.error("Use repository Python 3.15.2 for the qualified comparison")
    report = run(args.pdf, args.out, args.pdftotext)
    sys.stdout.write(
        json.dumps(
            {
                "output": str(args.out),
                "source_support": report["source_support"],
                "empirical_admission": False,
            }
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
