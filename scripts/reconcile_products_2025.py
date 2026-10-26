"""Reconcile identified sales extracts without guessing periods, channels or mass/count mappings."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_handoff import checked, digest, read

ROOT = Path(__file__).resolve().parents[1]
YEAR = 2025
FOLDER = "integration/reconciliation_2025"
UNITS = {
    "sticks": ("1", "sticks"),
    "thousand_sticks": ("1000", "sticks"),
    "packs_20": ("20", "sticks"),
    "cartons_200": ("200", "sticks"),
    "kg": ("0.001", "tonnes"),
    "tonnes": ("1", "tonnes"),
}
BLOCKING = {
    "period_conflict",
    "quantity_conflict",
    "not_reported",
    "product_basis_unresolved",
    "excluded_product",
    "not_in_this_intake",
}
MEASURES = {"sales_volume", "ingredient_mass", "additive_mass", "all_product_mass"}
PRODUCTS = {"factory_made", "ryo", "pipe", "cigars", "cigarillos", "unclassified_smoked", "heated"}
CHANNELS = {"domestic", "duty_free", "all_channels", "unspecified"}
DATA_IDS = ["NZ_MOH_tobacco_returns:2025-01-01/2026-01-01"]


def number(value: object) -> Decimal:
    """Require finite textual quantities; preserve signed return adjustments."""
    if not isinstance(value, str):
        msg = "Quantities must be explicit decimal strings"
        raise TypeError(msg)
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        msg = "Invalid decimal quantity"
        raise ValueError(msg) from exc
    if not result.is_finite():
        msg = "Nonfinite quantity"
        raise ValueError(msg)
    return result


def normalize(value: str, unit: str) -> tuple[Decimal, str]:
    """Convert explicit metric and package units; never infer a mass per cigarette."""
    if unit not in UNITS:
        msg = f"Unknown physical unit: {unit}"
        raise ValueError(msg)
    factor, canonical = UNITS[unit]
    return number(value) * Decimal(factor), canonical


def row_result(row: dict[str, Any]) -> dict[str, Any]:
    """Retain source quantities, conflicts and locators beside canonical quantities."""
    if (
        row["product"] not in PRODUCTS
        or row["channel"] not in CHANNELS
        or row["measure"] not in MEASURES
        or type(row["year"]) is not int
    ):
        msg = "Unsupported product/channel/measure/period declaration"
        raise ValueError(msg)
    issues = list(row["issues"])
    if row["year"] != YEAR:
        issues.append("period_conflict")
    value, unit = None, None
    if row["quantity"] is not None:
        value, unit = normalize(row["quantity"], row["unit"])
        components = row["components"]
        if not components or sum((number(v) for v in components), Decimal(0)) != number(row["quantity"]):
            msg = "Source component sum differs from extraction quantity"
            raise ValueError(msg)
    else:
        issues.append("not_reported")
    included = value is not None and not (set(issues) & BLOCKING)
    # Factory-made counts already are sticks. RYO conversion requires an audited 2025 convention.
    equivalent = (
        value
        if included
        and row["product"] == "factory_made"
        and unit == "sticks"
        and row["measure"] == "sales_volume"
        else None
    )
    if row["product"] == "ryo" and row["measure"] == "sales_volume":
        issues.append("ryo_conversion_not_qualified_for_2025")
    return dict(
        row,
        issues=sorted(set(issues)),
        normalized_quantity=None if value is None else str(value),
        normalized_unit=unit,
        included_in_subtotals=included,
        cigarette_equivalents=None if equivalent is None else str(equivalent),
        data_ids=[] if "period_conflict" in issues or value is None else DATA_IDS.copy(),
        can_condition_live_model=False,
    )


def check_overlap(rows: list[dict[str, Any]]) -> None:
    """Reject duplicate/overlapping measurements even under a new citation label."""
    ids: set[str] = set()
    seen: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["id"] in ids:
            msg = "Duplicate extraction row"
            raise ValueError(msg)
        ids.add(row["id"])
        key = (row["issuer"], row["product"], row["measure"])
        for previous in seen[key]:
            overlap = row["channel"] == previous["channel"] or bool(
                {"all_channels", "unspecified"} & {row["channel"], previous["channel"]}
            )
            alternatives = "quantity_conflict" in row["issues"] and "quantity_conflict" in previous["issues"]
            if overlap and not alternatives:
                msg = "Overlapping source measurements; labels cannot create new supply"
                raise ValueError(msg)
        seen[key].append(row)


def reconcile(data: dict[str, Any]) -> dict[str, Any]:
    """Generate dimensionally separated descriptive subtotals and an explicitly open comparison."""
    if data["schema"] != "tobac.product-extractions.v1" or data["year"] != YEAR:
        msg = "Unsupported reconciliation scope"
        raise ValueError(msg)
    if data["ryo_grams_per_stick"] is not None:
        msg = "RYO convention must be separately qualified before adoption"
        raise ValueError(msg)
    check_overlap(data["rows"])
    rows = [row_result(r) for r in data["rows"]]
    totals: dict[tuple[str, str, str, str], Decimal] = defaultdict(Decimal)
    for row in rows:
        if row["included_in_subtotals"]:
            key = (row["product"], row["channel"], row["measure"], row["normalized_unit"])
            totals[key] += number(row["normalized_quantity"])
    by_id = {r["id"]: r for r in rows}
    pm_net = number(by_id["PM-RYO-ingredient"]["normalized_quantity"]) - number(
        by_id["PM-RYO-additives"]["normalized_quantity"]
    )
    pm_sales = number(by_id["PM-ryo-domestic"]["normalized_quantity"])
    return {
        "schema": "tobac.product-reconciliation-report.v1",
        "status": "incomplete_source_conflicts",
        "rows": rows,
        "subtotals": [
            {"product": k[0], "channel": k[1], "measure": k[2], "unit": k[3], "quantity": str(v)}
            for k, v in sorted(totals.items())
        ],
        "aggregate_reference_tonnes": data["aggregate_reference_tonnes"],
        "reconstructed_national_mass_tonnes": None,
        "aggregate_residual_tonnes": None,
        "national_cigarette_equivalents": None,
        "cross_checks": {
            "PM_RYO_gross_minus_additives_matches_sales": pm_net == pm_sales,
            "PM_RYO_net_tonnes": str(pm_net),
            "interpretation": (
                "Arithmetic equality; missing duty-free sales remain unknown. "
                "The national mass definition remains unqualified."
            ),
        },
        "remaining_gates": [
            "BAT RYO document year 2024 conflicts with 2025 listing",
            "R&S King cigarette packet/carton conflict",
            "Unspecified and unreported channels remain unknown",
            "Factory-made tobacco mass and aggregate additive/product definitions unresolved",
            "2025 RYO stick conversion not qualified",
            "Original capture timestamps absent; remote raw-object recovery not claimed",
            "Measurement covariance, target scope and transport remain unqualified",
        ],
        "measurement_parameters_changed": False,
        "automatically_conditions_live_model": False,
        "scientific_qualification": False,
    }


def build_report(root: Path = ROOT) -> dict[str, Any]:
    """Verify frozen extraction provenance before computing any descriptive subtotal."""
    root = root.resolve()
    receipt = read(checked(root, f"{FOLDER}/extraction-receipt.json"))
    for name, sha in receipt["sha256"].items():
        if digest(checked(root, name)) != sha:
            msg = f"Extraction/source metadata hash mismatch: {name}"
            raise ValueError(msg)
    assets = read(checked(root, f"{FOLDER}/source-assets.json"))["sources"]
    identities = {a["id"]: a for a in assets}
    if len(identities) != len(assets):
        msg = "Duplicate source asset"
        raise ValueError(msg)
    data = read(checked(root, f"{FOLDER}/product-extractions.json"))
    for row in data["rows"]:
        if (
            row["source_asset"] not in identities
            or identities[row["source_asset"]]["issuer"] != row["issuer"]
        ):
            msg = "Extraction issuer/source identity mismatch"
            raise ValueError(msg)
    native = read(checked(root, f"{FOLDER}/native-verification_20261026.json"))
    if native["manifest_sha256"] != digest(checked(root, f"{FOLDER}/source-assets.json")):
        msg = "Native source verification belongs to another manifest"
        raise ValueError(msg)
    verified = {item["asset_id"]: item for item in native["assets"]}
    for asset in assets:
        item = verified.get(asset["id"], {})
        if (
            item.get("status") != "verified"
            or item.get("sha256") != asset["sha256"]
            or item.get("warc_sha256") != asset["warc_sha256"]
        ):
            msg = "Missing native source-object verification"
            raise ValueError(msg)
    reference = read(checked(root, data["aggregate_reference_receipt"]))
    value = next(r["value_tonnes"] for r in reference["matched_rows"] if r["year"] == YEAR)
    if value != data["aggregate_reference_tonnes"]:
        msg = "Aggregate reference differs from the verified workbook"
        raise ValueError(msg)
    report = reconcile(data)
    report.update(
        source_asset_count=len(assets),
        issuer_count=len({s["issuer"] for s in assets}),
        source_assets=assets,
        provenance_status=(
            "Dated manual/openpyxl extraction; native fixity executed locally; remote recovery unqualified"
        ),
    )
    return report


def main() -> None:
    """Write JSON and a flat review table; no model, dependency or source mutation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = build_report()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    columns = [
        "id",
        "issuer",
        "product",
        "channel",
        "year",
        "measure",
        "quantity",
        "unit",
        "normalized_quantity",
        "normalized_unit",
        "cigarette_equivalents",
        "included_in_subtotals",
        "issues",
        "source_asset",
        "locator",
    ]
    with (args.out / "table.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(dict(r, issues=";".join(r["issues"])) for r in report["rows"])
    sys.stdout.write(f"{len(report['rows'])} source-bound rows; national comparison remains incomplete\n")


if __name__ == "__main__":
    main()
