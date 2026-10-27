"""Reproduce source-bound partial identification without fitting a target posterior."""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path
from typing import Any, Protocol, cast

import jsonschema
from qualify_m2_pathway import checkout_identity
from source_handoff import checked, digest, read, same_hash

from tobac.partial_identification import Interval, restriction_bounds

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "evidence/m2/synthesis_20261027.json"
SCHEMA = "engineering/schemas/m2-synthesis.schema.json"
COHORT_YEAR = 2025


class _Validator(Protocol):
    def validate(self, instance: object) -> None: ...


def supply_summary(root: Path) -> dict[str, Any]:
    """Retain native units and mutually exclusive source interpretations."""
    report = read(checked(root, "integration/reconciliation_2025/generated/report.json"))
    rows = report["rows"]
    known: dict[str, Decimal] = {"factory_made": Decimal(0), "ryo": Decimal(0)}
    for row in rows:
        if row["product"] in known and row["measure"] == "sales_volume" and row["included_in_subtotals"]:
            expected_unit = "sticks" if row["product"] == "factory_made" else "tonnes"
            if row["normalized_unit"] != expected_unit or row["year"] != COHORT_YEAR:
                msg = "Unexpected native-unit source subtotal"
                raise ValueError(msg)
            known[row["product"]] += Decimal(row["normalized_quantity"])
    index = {row["id"]: row for row in rows}
    if any(
        index[name]["included_in_subtotals"]
        for name in ("RS-cigarettes-table", "RS-cigarettes-note", "BAT-ryo-domestic", "BAT-ryo-duty-free")
    ):
        msg = "Conflicting source alternatives must not already enter the known subtotal"
        raise ValueError(msg)
    rs = [
        Decimal(index[name]["normalized_quantity"]) for name in ("RS-cigarettes-table", "RS-cigarettes-note")
    ]
    bat = sum(Decimal(index[name]["quantity"]) for name in ("BAT-ryo-domestic", "BAT-ryo-duty-free"))
    return {
        "scope": (
            "Audited reported subset under existing nonoverlap declarations; not national consumption bounds"
        ),
        "factory_made_known_sticks": str(known["factory_made"]),
        "factory_made_with_one_RS_interpretation_sticks": [
            str(known["factory_made"] + x) for x in sorted(rs)
        ],
        "RS_interpretation_width_sticks": str(max(rs) - min(rs)),
        "ryo_known_tonnes": str(known["ryo"]),
        "ryo_if_BAT_2025_year_confirmed_tonnes": str(known["ryo"] + bat),
        "national_upper_bound": None,
        "national_lower_bound": None,
        "national_cigarette_equivalents": None,
        "reason": (
            "Unknown coverage/channels, BAT year and physical conversions; do not sum RS "
            "alternatives or replace null with zero"
        ),
        "underlying_data_group": "NZ_MOH_tobacco_returns",
    }


def csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a generated CSV without changing its units, ordering or scientific values."""
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _complete_table(rows: list[dict[str, str]], scenarios: set[tuple[str, float]], column: str) -> None:
    keys = [(row["case"], float(row["crime_weight"]), row[column]) for row in rows]
    expected = {(*scenario, item) for scenario in scenarios for item in {r[column] for r in rows}}
    if len(keys) != len(set(keys)) or set(keys) != expected:
        msg = "Complete unique scenario table required"
        raise ValueError(msg)


def conditional_voi(root: Path, replay: Path) -> dict[str, Any]:
    """Summarise existing M2 gross cost ceilings; never relabel them as costed ENBS."""
    validation = read(replay / "m2/validation.json")
    if validation.get("passed") is not True:
        msg = "M2 numerical invariants must pass before summarising study values"
        raise ValueError(msg)
    summary = csv_rows(replay / "m2/summary.csv")
    grouped = csv_rows(replay / "m2/grouped_evppi.csv")
    studies = csv_rows(replay / "m2/study_value.csv")
    if not summary or not grouped or not studies:
        msg = "Complete M2 reference outputs required"
        raise ValueError(msg)
    config = read(checked(root, "configs/m2_retail.json"))
    expected = {(c["id"], float(w)) for c in config["cases"] for w in config["crime_weights"]}
    actual = [(r["case"], float(r["crime_weight"])) for r in summary]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        msg = "Full configured M2 scenario set required"
        raise ValueError(msg)
    _complete_table(studies, expected, "design")
    _complete_table(grouped, expected, "group")
    if len({row["design"] for row in studies}) != validation["designs"]:
        msg = "All validated M2 study designs required"
        raise ValueError(msg)
    units = {row["value_unit"] for row in summary}
    if len(units) != 1:
        msg = "A single consequence unit is required"
        raise ValueError(msg)
    values: dict[str, list[float]] = {}
    for row in studies:
        value = float(row["evsi"])
        if not math.isfinite(value):
            msg = "Finite study values required"
            raise ValueError(msg)
        values.setdefault(row["design"], []).append(value)
    return {
        "value_unit": next(iter(units)),
        "summary_rows": len(summary),
        "grouped_evppi_rows": len(grouped),
        "study_rows": len(studies),
        "gross_cost_ceiling_ranges": {name: [min(v), max(v)] for name, v in sorted(values.items())},
        "qualification": (
            "Existing conditional finite priors/structures; no probabilities across "
            "scenarios, no NZD conversion, no study optimisation or fitted field "
            "likelihood"
        ),
        "cost_rule": (
            "Same-unit incremental study cost must be below applicable EVSI; this "
            "ceiling assumes the existing outcome/adoption model"
        ),
    }


def historical_prediction(replay: Path) -> dict[str, Any]:
    """Expose genuine leave-future-out computation, retaining retrospective vintage limits."""
    rows = csv_rows(replay / "release_calibration/rolling_predictive_checks.csv")
    if not rows or any(int(r["train_end_year"]) >= int(r["test_year"]) for r in rows):
        msg = "Historical prediction must exclude its future test observation"
        raise ValueError(msg)
    reserved = [r for r in rows if r["stage"].startswith("reserved_diagnostic")]
    if not reserved or any(r["covered_95"].lower() not in {"true", "false"} for r in rows):
        msg = "Declared reserved diagnostics and boolean coverage required"
        raise ValueError(msg)
    return {
        "rows": len(rows),
        "reserved_rows": len(reserved),
        "reserved_covered_95": sum(r["covered_95"].lower() == "true" for r in reserved),
        "reserved_unique_years": sorted({int(r["test_year"]) for r in reserved}),
        "row_interpretation": "Model-year rows reuse outcomes across models; not independent observations",
        "vintages": sorted({r["vintage"] for r in rows}),
        "qualification": (
            "Existing national-release retrospective diagnostics, not raw-assay or "
            "cap-effect held-out field validation; historical source scopes remain "
            "qualified separately"
        ),
    }


def build_report(root: Path, replay: Path) -> dict[str, Any]:
    """Bind documentary sources and executed reference outputs to a bounded synthesis."""
    case = read(checked(root, MANIFEST))
    validator = cast("_Validator", jsonschema.Draft202012Validator(read(checked(root, SCHEMA))))
    validator.validate(case)
    required_inputs = {
        "integration/reconciliation_2025/generated/report.json",
        "integration/reconciliation_2025/product-extractions.json",
        "integration/reconciliation_2025/source-assets.json",
        "integration/archive/moh-workbook-qualification_20261026.json",
        "configs/m2_retail.json",
        "docs/research/M2_MATCHED_PATHWAY.md",
    }
    if set(case["input_sha256"]) != required_inputs:
        msg = "Complete documentary input bindings required"
        raise ValueError(msg)
    for name, expected in case["input_sha256"].items():
        same_hash(root, name, expected)
    for name in ("sources", "scenarios", "residual_requirements"):
        ids = [row["id"] for row in case[name]]
        if len(ids) != len(set(ids)):
            msg = f"Duplicate {name} identities"
            raise ValueError(msg)
    numerical_manifest = read(replay / "m2/manifest.json")
    for name, expected in numerical_manifest["inputs"].items():
        same_hash(root, name, expected)
    for name in ("validation.json", "summary.csv", "grouped_evppi.csv", "study_value.csv"):
        same_hash(replay / "m2", name, numerical_manifest["outputs"][name])
    historical_manifest = read(replay / "release_calibration/run_manifest.json")
    historical_files = {f["path"]: f["sha256"] for f in historical_manifest["files"]}
    name = "rolling_predictive_checks.csv"
    same_hash(replay / "release_calibration", name, historical_files[name])
    bounds: list[dict[str, Any]] = []
    for scenario in case["scenarios"]:
        total = None if scenario["total"] is None else Interval(*scenario["total"])
        lawful = None if scenario["lawful"] is None else Interval(*scenario["lawful"])
        result = restriction_bounds(
            total,
            lawful,
            total_bias=Interval(*scenario["total_bias"]),
            lawful_bias=Interval(*scenario["lawful_bias"]),
        )
        bounds.append({"id": scenario["id"], "role": case["scenario_role"], **asdict(result)})
    inputs = [MANIFEST, SCHEMA, "src/tobac/partial_identification.py", "scripts/qualify_m2_synthesis.py"]
    replay_files = [
        "m2/manifest.json",
        "release_calibration/run_manifest.json",
        "m2/validation.json",
        "m2/summary.csv",
        "m2/grouped_evppi.csv",
        "m2/study_value.csv",
        "release_calibration/rolling_predictive_checks.csv",
    ]
    return {
        "schema_version": "tobac.m2-synthesis-report.v1",
        "python": platform.python_version(),
        "source_count": len(case["sources"]),
        "source_review": MANIFEST,
        "input_sha256": {**case["input_sha256"], **{p: digest(checked(root, p)) for p in inputs}},
        "replay_sha256": {p: digest(replay / p) for p in replay_files},
        "bounds": bounds,
        "bound_interpretation": (
            "Sharp marginal projections under explicit Cartesian supports and M2a "
            "equal-intensity structure; marginal q,d supports are not a joint rectangle"
        ),
        "supply": supply_summary(root),
        "conditional_voi": conditional_voi(root, replay),
        "historical_prediction": historical_prediction(replay),
        "residual_requirements": case["residual_requirements"],
        "conditioned": False,
        "target_empirically_identified": False,
    }


def main() -> None:
    """Write a fresh receipt only after reference outputs and input hashes validate."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    before = checkout_identity(ROOT)
    report = build_report(ROOT, args.replay)
    if checkout_identity(ROOT) != before:
        msg = "Checkout changed during synthesis"
        raise ValueError(msg)
    report.update(checkout=before, command=[sys.executable, *sys.argv])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2, allow_nan=False, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
