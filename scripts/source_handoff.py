"""Report source/observation compatibility without constructing a likelihood or posterior."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any, cast

import jsonschema

from tobac.evidence import Scope
from tobac_supply.consumption_ledger import SupplyBasis

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "engineering/schemas/observation-handoff.schema.json"
PROPOSAL = "integration/archive/observation-handoff.json"
ORIGINAL_STATUSES = {"source_html_identity_observed", "source_workbook_values_matched"}


def digest(path: Path) -> str:
    """Hash actual file bytes, including raw objects when explicitly available."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(root: Path, name: str) -> Path:
    """Reject absolute paths, traversal and symlinks in repository input references."""
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name or path.as_posix() != name:
        msg = "Noncanonical repository path"
        raise ValueError(msg)
    result = root
    for part in path.parts:
        result /= part
        if result.is_symlink():
            msg = "Symlink input forbidden"
            raise ValueError(msg)
    if not result.is_file():
        msg = f"Missing input: {name}"
        raise ValueError(msg)
    return result


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject ambiguous duplicate JSON object keys."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            msg = f"Duplicate JSON key: {key}"
            raise ValueError(msg)
        result[key] = value
    return result


def read(path: Path) -> dict[str, Any]:
    """Read one JSON object; raw field shapes are subsequently validated."""
    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    if not isinstance(result, dict):
        msg = "JSON object required"
        raise TypeError(msg)
    return cast("dict[str, Any]", result)


def same_hash(root: Path, name: str, expected: str) -> None:
    """Fail closed on absent or changed inventoried bytes."""
    if digest(checked(root, name)) != expected:
        msg = f"Input hash mismatch: {name}"
        raise ValueError(msg)


def archive_index(
    root: Path,
) -> tuple[dict[tuple[str, str], str], dict[str, Any], dict[str, Any]]:
    """Verify inventories and resolve bibliography aliases through the existing register."""
    register, bindings, inputs = (
        read(checked(root, f"integration/archive/{name}.json"))
        for name in ("source-register", "source-bindings", "consumer-inputs")
    )
    same_hash(root, "integration/archive/source-register.json", bindings["register_sha256"])
    aliases: dict[tuple[str, str], str] = {}
    for source in register["sources"]:
        for ref in source["references"]:
            key = (ref["collection"], ref["source_id"])
            if key in aliases:
                msg = f"Duplicate bibliography alias: {key}"
                raise ValueError(msg)
            aliases[key] = source["archive_id"]
    expected: set[tuple[str, str]] = set()
    for name, sha in register["collection_sha256"].items():
        same_hash(root, name, sha)
        records = json.loads(checked(root, name).read_text(encoding="utf-8"), object_pairs_hook=unique)
        expected.update((name, item["id"]) for item in records)
    if set(aliases) != expected or bindings["collection_sha256"] != register["collection_sha256"]:
        msg = "Bibliography/register identities differ"
        raise ValueError(msg)
    captures = {item["archive_id"]: item for item in bindings["sources"]}
    if len(captures) != len(bindings["sources"]) or set(captures) != set(aliases.values()):
        msg = "Capture/register identities differ"
        raise ValueError(msg)
    for item in bindings["sources"]:
        if item["references"] != next(
            s["references"] for s in register["sources"] if s["archive_id"] == item["archive_id"]
        ):
            msg = "Capture alias drift"
            raise ValueError(msg)
    return aliases, captures, verify_inventory(root, inputs)


def verify_inventory(root: Path, inputs: dict[str, Any]) -> dict[str, Any]:
    """Require a complete, byte-bound CSV and supporting-file inventory."""
    inventory = {item["path"]: item for item in inputs["inputs"]}
    for item in inputs["inputs"] + inputs["supporting_files"]:
        same_hash(root, item["path"], item["sha256"])
    for name, item in inventory.items():
        with checked(root, name).open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            if len(rows) != item["rows"] or reader.fieldnames != item["columns"]:
                msg = f"Input structure mismatch: {name}"
                raise ValueError(msg)
    # Do not silently omit files newly added to either maintained input tree.
    actual = {
        p.relative_to(root).as_posix()
        for pattern in ("data/**/*.csv", "evidence/prior_work/**/*.csv")
        for p in root.glob(pattern)
    }
    if set(inventory) != actual:
        msg = "Consumer input inventory incomplete"
        raise ValueError(msg)
    return inventory


def lineage_file(root: Path, name: str, legacy: dict[str, Any]) -> dict[str, Any]:
    """Describe approved bytes and explicit row metadata without inferring observation status."""
    path = checked(root, name)
    category = "evidence_metadata_or_extract"
    if name.startswith("results/"):
        category = "reference_output_not_observation"
    elif name.startswith("configs/"):
        category = "parameter_or_scenario_declaration"
    elif name.startswith("evidence/prior_work/"):
        category = "preserved_legacy_evidence"
    elif name.endswith(".csl.json"):
        category = "bibliography_not_observation"
    item: dict[str, Any] = {
        "path": name,
        "sha256": digest(path),
        "bytes": path.stat().st_size,
        "category": category,
        "source_references": legacy.get(name, {}).get("source_references", []),
        "native_lineage_verified": False,
    }
    if path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            item.update(rows=len(rows), columns=reader.fieldnames)
        item["declared_row_metadata"] = {
            field: sorted({row[field] for row in rows if row.get(field)})
            for field in ("source_id", "role", "evidence_status", "dependency_group", "source_dependency")
            if rows and field in rows[0]
        }
    return item


def lineage_inventory(root: Path = ROOT) -> dict[str, Any]:
    """Export a current inventory from the existing register and reviewed public tree.

    The export is a coverage superset, not a second source authority or an executed
    dependency graph. Missing registered bytes fail; new approved evidence assets
    remain visible even where their native source relationships are unknown.
    """
    aliases, captures, legacy = archive_index(root)
    policy = read(checked(root, "engineering/publication-policy.json"))
    names = policy["public_paths"]
    files = [
        lineage_file(root, name, legacy)
        for name in sorted(names)
        if name.startswith(("data/", "configs/", "evidence/", "results/"))
    ]
    implementation = {
        name: digest(checked(root, name))
        for name in sorted(names)
        if name.endswith(".py") and (name.startswith(("src/", "scripts/")) or name == "noxfile.py")
    }
    return {
        "schema_version": "tobac.lineage-foundation-inventory.v1",
        "register": "integration/archive/source-register.json",
        "register_sha256": digest(checked(root, "integration/archive/source-register.json")),
        "source_identities": len(captures),
        "bibliography_aliases": len(aliases),
        "legacy_csv_inputs": len(legacy),
        "source_states": [
            {
                "archive_id": identity,
                "recorded_capture_statuses": sorted({item["status"] for item in source["captures"]}),
                "native_objects_verified_this_run": False,
            }
            for identity, source in sorted(captures.items())
        ],
        "files": files,
        "implementation_sha256": implementation,
        "scope": "approved_local_assets_and_implementation_superset_not_executed_dependency_closure",
        "native_lineage_verified": False,
        "scientific_qualification": False,
        "automatically_conditions_live_model": False,
    }


def object_verified(objects: Path | None, sha: str) -> bool:
    """Check an explicitly staged flat digest-named object directory; never fetch data."""
    if objects is None or re.fullmatch(r"[0-9a-f]{64}", sha) is None:
        return False
    path = objects / sha
    return path.is_file() and not path.is_symlink() and digest(path) == sha


def source_gaps(source: dict[str, Any], objects: Path | None) -> list[str]:
    """Distinguish original-object verification, identity-only HTML and absent timestamps."""
    originals = [c for c in source["captures"] if c["status"] in ORIGINAL_STATUSES]
    if not originals:
        return ["original_source_capture_missing"]
    verified = [
        c
        for c in originals
        if object_verified(objects, c.get("sha256", ""))
        and object_verified(objects, c.get("warc_sha256", ""))
    ]
    gaps: list[str] = []
    if not verified:
        gaps.append("capture_bytes_not_verified")
    if not any(c.get("captured_at") for c in verified):
        gaps.append("capture_date_unverified")
    if not any(c["status"] == "source_workbook_values_matched" for c in verified):
        gaps.append("source_values_not_reconciled")
    return gaps


def observation_record(
    root: Path,
    obs: dict[str, Any],
    proposal: dict[str, Any],
    index: tuple[dict[tuple[str, str], str], dict[str, Any], dict[str, Any]],
    objects: Path | None,
) -> dict[str, Any]:
    """Bind one declared row to retained bytes and the shared Scope/SupplyBasis contracts."""
    aliases, captures, inventory = index
    name = obs["path"]
    if name not in inventory:
        msg = "Observation path is not inventoried"
        raise ValueError(msg)
    with checked(root, name).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    selected = [r for r in rows if r.get("year") == str(obs["year"])]
    if len(selected) != 1 or selected[0].get("source_id") != obs["source_id"]:
        msg = "Observation must identify exactly one source/year row"
        raise ValueError(msg)
    row = selected[0]
    archive_id = aliases.get((obs["collection"], obs["source_id"]))
    if archive_id is None or not any(
        r.get("archive_id") == archive_id and r["source_id"] == obs["source_id"]
        for r in inventory[name]["source_references"]
    ):
        msg = "Observation source is not bound to this input"
        raise ValueError(msg)
    period = (obs["period_start"], obs["period_end"])
    start, end = (date.fromisoformat(p) for p in period)
    if start >= end:
        msg = "Require nonempty half-open observation period"
        raise ValueError(msg)
    declared_scope = obs["source_scope"]
    if declared_scope is not None:
        Scope(**declared_scope)
    basis = SupplyBasis(source_ids=(obs["source_id"],), observation_years=(obs["year"],))
    gaps = source_gaps(captures[archive_id], objects)
    gaps.extend(scope_gaps(obs, row, proposal, period, start))
    dependency = row.get("dependency_group", row.get("source_dependency", ""))
    groups = proposal["dependency_mappings"].get(dependency)
    if not groups:
        msg = f"Unmapped underlying-data dependency: {dependency}"
        raise ValueError(msg)
    data_ids = [f"{group}:{period[0]}/{period[1]}" for group in groups]
    if used_overlap(groups, period, proposal["used_data_ids"]):
        gaps.append("underlying_data_already_conditioned")
    return {
        "observation_id": obs["observation_id"],
        "path": name,
        "input_sha256": inventory[name]["sha256"],
        "source_id": basis.source_ids[0],
        "observation_year": basis.observation_years[0],
        "archive_id": archive_id,
        "period": list(period),
        "source_scope": declared_scope,
        "products": obs["products"],
        "source_locator": row.get("source_locator"),
        "role": obs["role"],
        "source_declared_role": row.get("role", row.get("evidence_status")),
        "source_limitations": row.get("limitations"),
        "dependency_groups": groups,
        "data_ids": data_ids,
        "gaps": gaps,
        "captures": captures[archive_id]["captures"],
    }


def used_overlap(groups: list[str], period: tuple[str, str], used: list[str]) -> bool:
    """Reject partially overlapping D0 periods as well as exact identity reuse."""
    overlap = False
    for value in used:
        try:
            group, dates = value.rsplit(":", 1)
            left, right = dates.split("/")
            start, end = date.fromisoformat(left), date.fromisoformat(right)
        except ValueError as exc:
            msg = "Used data IDs require group:start/end half-open ISO periods; reconcile legacy IDs first"
            raise ValueError(msg) from exc
        if start >= end or (start.isoformat(), end.isoformat()) != (left, right):
            msg = "Used data ID period must be nonempty, ordered and canonical ISO"
            raise ValueError(msg)
        if group in groups and left < period[1] and period[0] < right:
            overlap = True
    return overlap


def scope_gaps(
    obs: dict[str, Any], row: dict[str, str], proposal: dict[str, Any], period: tuple[str, str], start: date
) -> list[str]:
    """Retain missing scope/model declarations as gaps, never inferred defaults."""
    gaps: list[str] = []
    declared_scope = obs["source_scope"]
    if obs["role"] != "observation":
        gaps.append("role_not_observation")
    if not declared_scope:
        gaps.append("source_scope_unqualified")
    elif declared_scope["unit"] != row["unit"] or (declared_scope["start"], declared_scope["end"]) != period:
        gaps.append("source_scope_row_mismatch")
    if (
        row.get("period_start", period[0]),
        row.get("period_end", period[1]),
    ) != period or start.year != obs["year"]:
        gaps.append("observation_period_mismatch")
    if "period_start" not in row:
        gaps.append("source_period_convention_unqualified")
    if not obs["products"] or obs["products"] != proposal["target_products"]:
        gaps.append("product_coverage_or_conversion_unqualified")
    gaps.extend(
        f"{field}_unqualified"
        for field in ("likelihood_model", "covariance_model", "transport_model")
        if not obs[field]
    )
    if row["unit"] != proposal["target_scope"]["unit"]:
        gaps.append("unit_conversion_requires_separate_qualification")
    if proposal["target_scope_status"] != "declared":
        gaps.append("target_scope_unqualified")
    if row.get("role") and row["role"] != "observation":
        gaps.append("source_role_not_observation")
    return gaps


def shared_data_gaps(records: list[dict[str, Any]]) -> None:
    """Reject overlapping reuse across aliases; prose independence cannot waive shared data."""
    for i, first in enumerate(records):
        for second in records[i + 1 :]:
            if (
                set(first["dependency_groups"]) & set(second["dependency_groups"])
                and first["period"][0] < second["period"][1]
                and second["period"][0] < first["period"][1]
            ):
                for row in (first, second):
                    row["gaps"].append("shared_underlying_data_requires_joint_likelihood")


def build_report(
    root: Path = ROOT,
    proposal: dict[str, Any] | None = None,
    objects: Path | None = None,
) -> dict[str, Any]:
    """Validate a proposal and report gaps; compatibility is never a conditioning operation."""
    root = root.resolve()
    proposal = read(checked(root, PROPOSAL)) if proposal is None else proposal
    try:
        jsonschema.Draft202012Validator(read(SCHEMA)).validate(proposal)  # pyright: ignore[reportUnknownMemberType]  # jsonschema has no type stubs.
    except jsonschema.ValidationError as exc:
        msg = f"Invalid handoff proposal: {exc.message}"
        raise ValueError(msg) from exc
    Scope(**proposal["target_scope"])
    ids = [o["observation_id"] for o in proposal["observations"]]
    if len(set(ids)) != len(ids):
        msg = "Duplicate observation identity"
        raise ValueError(msg)
    index = archive_index(root)
    records = [observation_record(root, obs, proposal, index, objects) for obs in proposal["observations"]]
    shared_data_gaps(records)
    for row in records:
        row["gaps"] = sorted(set(row["gaps"]))
        row["metadata_compatible"] = not row["gaps"]
    return {
        "schema_version": "tobac.observation-handoff-report.v1",
        "status": "metadata_compatible" if all(r["metadata_compatible"] for r in records) else "blocked",
        "automatically_conditions_live_model": False,
        "scientific_qualification": False,
        "target_scope": proposal["target_scope"],
        "target_scope_status": proposal["target_scope_status"],
        "target_products": proposal["target_products"],
        "proposal_sha256": hashlib.sha256(json.dumps(proposal, sort_keys=True).encode()).hexdigest(),
        "binding_sha256": digest(checked(root, "integration/archive/source-bindings.json")),
        "dependency_mapping_status": "explicit consumer declaration; not independently established",
        "observations": records,
    }


def main() -> None:
    """Write a reviewable report; expected scientific gaps are distinct from invalid inputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory", action="store_true", help="Export current lineage foundation inventory"
    )
    parser.add_argument("--proposal", type=Path, default=ROOT / PROPOSAL)
    parser.add_argument(
        "--objects",
        type=Path,
        help="Optional flat digest-named raw/WARC staging directory",
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.inventory and (args.objects is not None or args.proposal != ROOT / PROPOSAL):
        parser.error("--inventory cannot be combined with observation proposal or object staging")
    if args.out.exists() or args.out.is_symlink():
        parser.error("Refusing to overwrite an existing handoff receipt")
    report = (
        lineage_inventory(ROOT) if args.inventory else build_report(ROOT, read(args.proposal), args.objects)
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2, allow_nan=False) + "\n")
    if args.inventory:
        sys.stdout.write(f"Inventory: {len(report['files'])} files; no native or scientific qualification\n")
    else:
        sys.stdout.write(
            f"{report['status']}: {len(report['observations'])} rows; no conditioning performed\n"
        )


if __name__ == "__main__":
    main()
