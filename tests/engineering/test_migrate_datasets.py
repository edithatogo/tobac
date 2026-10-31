"""Independent controls for the P4.3 dataset-accounting migration.

Synthetic inventory labels do not qualify any native lineage or scientific result.
"""

import hashlib
import json
lazy from pathlib import Path

from scripts.migrate_datasets import migrate_datasets


def entry(path: str, category: str, payload: bytes, *, source_refs: bool = False) -> dict:
    return {
        "path": path,
        "category": category,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "source_references": [{"source_id": "s"}] if source_refs else [],
    }


def build(tmp_path: Path) -> tuple[Path, Path]:
    files = {
        "legacy.txt": (b"legacy bytes", "preserved_legacy_evidence"),
        "reference.csv": (b"reference", "reference_output_not_observation"),
        "extract.csv": (b"extract", "evidence_metadata_or_extract"),
        "param.json": (b"{}", "parameter_or_scenario_declaration"),
        "bib.json": (b"[]", "bibliography_not_observation"),
    }
    inventory = {"files": []}
    for name, (payload, category) in files.items():
        (tmp_path / name).write_bytes(payload)
        inventory["files"].append(entry(name, category, payload))
    inventory["files"].append(entry("missing.csv", "evidence_metadata_or_extract", b"absent"))
    (tmp_path / "tampered.json").write_bytes(b"changed")
    inventory["files"].append(
        {**entry("tampered.json", "parameter_or_scenario_declaration", b"original"), "sha256": "a" * 64}
    )
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(json.dumps(inventory))
    return tmp_path, inventory_path


def test_every_category_is_accounted_and_missing_items_are_blocked(tmp_path) -> None:
    root, inventory_path = build(tmp_path)
    result = migrate_datasets(root, inventory_path)
    assert result["total_items"] == 7
    assert result["migrated_count"] == 5
    assert result["unresolved_count"] == 0
    assert result["blocked_count"] == 2
    statuses = {item["path"]: item["migration_status"] for item in result["migrated"]}
    assert statuses["legacy.txt"] == "preserved_legacy"
    assert statuses["reference.csv"] == "verified_reference_output"
    assert statuses["extract.csv"] == "verified_evidence"
    assert statuses["param.json"] == "verified_parameter"
    assert statuses["bib.json"] == "verified_bibliography"


def test_legacy_evidence_is_labelled_reconstructed_with_a_date(tmp_path) -> None:
    root, inventory_path = build(tmp_path)
    result = migrate_datasets(root, inventory_path)
    legacy = next(item for item in result["migrated"] if item["path"] == "legacy.txt")
    assert legacy["lineage_status"] == "reconstructed"
    assert legacy["reconstruction_date"] == "2026-10-31"


def test_hash_mismatch_and_absent_source_are_blocked_never_verified(tmp_path) -> None:
    root, inventory_path = build(tmp_path)
    result = migrate_datasets(root, inventory_path)
    blocked = {item["path"]: item["migration_status"] for item in result["blocked"]}
    assert blocked["missing.csv"] == "missing_evidence"
    assert blocked["tampered.json"] == "missing_parameter"
    assert all(item["native_lineage_qualified"] is False for item in result["blocked"])


def test_migration_never_claims_native_or_scientific_qualification(tmp_path) -> None:
    root, inventory_path = build(tmp_path)
    result = migrate_datasets(root, inventory_path)
    assert result["native_lineage_qualified"] is False
    assert result["scientific_qualification"] is False
    assert result["automatically_conditions_live_model"] is False
    assert result["extraction_pilots"]["moh_workbook"]["native_source_registered"] is False
    assert result["extraction_pilots"]["shine_table2"]["native_receipts"] is True


def test_unknown_category_is_retained_as_blocked(tmp_path) -> None:
    (tmp_path / "mystery.bin").write_bytes(b"x")
    inventory = {
        "files": [entry("mystery.bin", "unclassified_asset", b"x")],
    }
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(json.dumps(inventory))
    result = migrate_datasets(tmp_path, inventory_path)
    assert result["total_items"] == 1
    assert result["blocked_count"] == 1
    assert result["blocked"][0]["lineage_status"] == "unknown"
