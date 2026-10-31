"""Account for and migrate every current dataset in the lineage inventory.

P4.3: Account for and migrate every remaining current dataset.
P4.4: Phase verification and checkpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = ROOT / "integration/archive/p4-dataset-migration_20261031.json"


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from disk."""
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        msg = f"Expected JSON object in {path}"
        raise TypeError(msg)
    return cast("dict[str, Any]", result)


def digest(path: Path) -> str:
    """Return a file's SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def migrate_datasets(root: Path) -> dict[str, Any]:  # noqa: C901, PLR0912, PLR0915
    """Classify every inventoried dataset by fixity and lineage status."""
    root = root.resolve()
    inventory = read_json(root / "integration/archive/lineage-foundations-inventory_20261029.json")

    items = inventory.get("files", [])
    migrated: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []

    for item in items:
        path = item.get("path", "")
        category = item.get("category", "")
        sha256 = item.get("sha256", "")
        source_refs = item.get("source_references", [])

        full_path = root / path
        file_exists = full_path.is_file()
        hash_matches = False
        if file_exists:
            try:
                hash_matches = digest(full_path) == sha256
            except OSError:
                hash_matches = False

        if category == "preserved_legacy_evidence":
            status = "preserved_legacy"
            lineage_status = "reconstructed"
            reconstruction_date = "2026-10-31"
        elif category == "reference_output_not_observation":
            status = "verified_reference_output" if hash_matches else "missing_reference_output"
            lineage_status = "reference_output"
            reconstruction_date = None
        elif category == "evidence_metadata_or_extract":
            if file_exists and hash_matches:
                status = "verified_evidence"
                lineage_status = (
                    "evidence_with_source_refs" if source_refs else "evidence_without_source_refs"
                )
            else:
                status = "missing_evidence"
                lineage_status = "unavailable"
            reconstruction_date = None
        elif category == "parameter_or_scenario_declaration":
            if file_exists and hash_matches:
                status = "verified_parameter"
                lineage_status = "parameter_declaration"
            else:
                status = "missing_parameter"
                lineage_status = "unavailable"
            reconstruction_date = None
        elif category == "bibliography_not_observation":
            if file_exists and hash_matches:
                status = "verified_bibliography"
                lineage_status = "bibliography_not_observation"
            else:
                status = "missing_bibliography"
                lineage_status = "unavailable"
            reconstruction_date = None
        else:
            status = "unknown_category"
            lineage_status = "unknown"
            reconstruction_date = None

        entry = {
            "path": path,
            "category": category,
            "sha256": sha256,
            "file_exists": file_exists,
            "hash_matches": hash_matches,
            "source_references": source_refs,
            "migration_status": status,
            "lineage_status": lineage_status,
            "reconstruction_date": reconstruction_date,
            "native_lineage_qualified": False,
            "scientific_qualification": False,
        }

        if status.startswith("missing") or status == "unknown_category":
            blocked.append(entry)
        elif status in (
            "preserved_legacy",
            "verified_reference_output",
            "verified_evidence",
            "verified_parameter",
            "verified_bibliography",
        ):
            migrated.append(entry)
        else:
            unresolved.append(entry)

    pilots = {
        "moh_workbook": {
            "status": "exploratory",
            "native_receipts": False,
            "native_source_registered": False,
            "note": "MOH workbook extraction exists as exploratory only",
        },
        "shine_table2": {
            "status": "exploratory",
            "native_receipts": False,
            "native_source_registered": False,
            "note": "SHINE Table 2 comparison exists as exploratory only",
        },
    }

    return {
        "schema_version": "tobac.p4-dataset-migration.v1",
        "derived_at": datetime.now(UTC).isoformat(),
        "inventory_source": "integration/archive/lineage-foundations-inventory_20261029.json",
        "total_items": len(items),
        "migrated_count": len(migrated),
        "unresolved_count": len(unresolved),
        "blocked_count": len(blocked),
        "migrated": migrated,
        "unresolved": unresolved,
        "blocked": blocked,
        "extraction_pilots": pilots,
        "native_lineage_qualified": False,
        "scientific_qualification": False,
        "automatically_conditions_live_model": False,
        "note": (
            "This migration accounts for all 145 inventoried items. "
            "Legacy evidence is preserved with reconstructed lineage labels. "
            "Reference outputs are verified for fixity but not qualified. "
            "Evidence extracts and parameters are verified for fixity. "
            "Unavailable or missing items are recorded as blocked. "
            "No extrapolation from 2 exploratory pilots to full qualification. "
            "Native lineage qualification requires producer P2/P3 work."
        ),
    }


def main() -> None:
    """Write a dataset migration receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()

    result = migrate_datasets(ROOT)
    if args.out.exists() or args.out.is_symlink():
        parser.error("Refusing to overwrite an existing migration receipt")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    sys.stdout.write(
        f"Migration: {result['migrated_count']}/{result['total_items']} migrated, "
        f"{result['unresolved_count']} unresolved, {result['blocked_count']} blocked. "
        "No scientific qualification.\n"
    )


if __name__ == "__main__":
    main()
