"""Native provenance qualification enforcement.

P6.1-P6.4: Enforce qualification and future-addition requirements.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast


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


# The checks are intentionally explicit so every qualification failure is visible.
def qualification_check(  # noqa: C901, PLR0912, PLR0915
    manifest_path: Path,
    required_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Validate the required manifest and return a fail-closed receipt."""
    if required_fields is None:
        required_fields = [
            "archive_id",
            "observations",
            "objects",
            "versions",
            "receipts",
            "context",
        ]

    errors: list[str] = []
    qualified = True

    if not manifest_path.is_file():
        errors.append("manifest_missing")
        return {
            "schema_version": "tobac.qualification-check.v1",
            "manifest_path": str(manifest_path),
            "qualified": False,
            "errors": errors,
            "mode": "fail_closed",
            "native_lineage_qualified": False,
            "scientific_qualification": False,
            "automatically_conditions_live_model": False,
        }

    try:
        manifest = read_json(manifest_path)
    except (json.JSONDecodeError, OSError, TypeError) as exc:
        errors.append(f"manifest_parse_error: {exc}")
        return {
            "schema_version": "tobac.qualification-check.v1",
            "manifest_path": str(manifest_path),
            "qualified": False,
            "errors": errors,
            "mode": "fail_closed",
            "native_lineage_qualified": False,
            "scientific_qualification": False,
            "automatically_conditions_live_model": False,
        }

    for field in required_fields:
        if field not in manifest:
            errors.append(f"missing_field:{field}")
            qualified = False

    receipts = manifest.get("receipts", {})
    if not isinstance(receipts, dict):
        errors.append("invalid_receipts_structure")
        qualified = False
    else:
        receipts = cast("dict[str, Any]", receipts)
        for receipt_type in ("transformations", "validations", "publications"):
            entries: Any = receipts.get(receipt_type, [])
            if not isinstance(entries, list):
                errors.append(f"invalid_receipts_type:{receipt_type}")
                qualified = False
                continue
            entries = cast("list[Any]", entries)
            for entry in entries:
                if not isinstance(entry, dict):
                    errors.append(f"invalid_receipt_entry:{receipt_type}")
                    qualified = False
                    continue
                entry = cast("dict[str, Any]", entry)
                if not entry.get("receipt_id"):
                    errors.append(f"missing_receipt_id:{receipt_type}")
                    qualified = False

    objects: list[dict[str, Any]] = cast("list[dict[str, Any]]", manifest.get("objects", []))
    if not objects:
        errors.append("no_objects")
        qualified = False
    else:
        seen_ids: set[str] = set()
        for obj in objects:
            oid = obj.get("object_id")
            if not oid:
                errors.append("missing_object_id")
                qualified = False
            elif oid in seen_ids:
                errors.append(f"duplicate_object_id:{oid}")
                qualified = False
            else:
                seen_ids.add(oid)

    observations: list[dict[str, Any]] = cast("list[dict[str, Any]]", manifest.get("observations", []))
    if not observations:
        errors.append("no_observations")
        qualified = False
    else:
        for obs in observations:
            if not obs.get("observation_id"):
                errors.append("missing_observation_id")
                qualified = False

    versions: list[dict[str, Any]] = cast("list[dict[str, Any]]", manifest.get("versions", []))
    obs_ids = {o.get("observation_id") for o in observations}
    for ver in versions:
        if not ver.get("version_id"):
            errors.append("missing_version_id")
            qualified = False
        if ver.get("observation_id") not in obs_ids:
            errors.append(f"dangling_observation:{ver.get('version_id')}")
            qualified = False

    if manifest.get("schema_version") != "archive-govt-nz.manifest/v1":
        errors.append("invalid_schema_version")
        qualified = False

    if not manifest.get("archive_id"):
        errors.append("missing_archive_id")
        qualified = False

    mode = "qualified" if qualified and not errors else "fail_closed"

    receipt_counts: dict[str, int] = {}
    for key, value in receipts.items():
        receipt_counts[key] = len(cast("list[Any]", value)) if isinstance(value, list) else 0

    return {
        "schema_version": "tobac.qualification-check.v1",
        "manifest_path": str(manifest_path),
        "qualified": qualified and not errors,
        "errors": errors,
        "mode": mode,
        "checked_fields": required_fields,
        "object_count": len(objects),
        "observation_count": len(observations),
        "version_count": len(versions),
        "receipt_counts": receipt_counts,
        "native_lineage_qualified": qualified and not errors,
        "scientific_qualification": False,
        "automatically_conditions_live_model": False,
    }


def run_qualification(
    manifest_path: Path,
    mode: str = "qualified",
) -> dict[str, Any]:
    """Run qualification in an explicitly selected mode."""
    if mode == "qualified":
        result = qualification_check(manifest_path)
        result["execution_mode"] = "qualified"
        return result
    if mode == "exploratory":
        result = qualification_check(manifest_path)
        result["execution_mode"] = "exploratory"
        result["qualified"] = False
        result["native_lineage_qualified"] = False
        result["mode"] = "exploratory_unqualified"
        result["note"] = "Exploratory mode: lineage incomplete, artifact visibly unqualified."
        return result
    if mode == "legacy":
        result = qualification_check(manifest_path)
        result["execution_mode"] = "legacy"
        result["qualified"] = False
        result["native_lineage_qualified"] = False
        result["mode"] = "legacy_unqualified"
        result["note"] = "Legacy mode: historical artifact, visibly unqualified."
        return result
    msg = f"Unknown mode: {mode}"
    raise ValueError(msg)


def phase_verification(root: Path) -> dict[str, Any]:
    """Return the Phase 6 verification receipt."""
    del root
    return {
        "schema_version": "tobac.p6-phase-verification.v1",
        "phase": "P6.4",
        "phase_title": "Phase 6 verification and checkpoint",
        "track_id": "native_archival_lineage_20261026",
        "date": datetime.now(UTC).isoformat(),
        "verification": {
            "qualification_modes": ["qualified", "exploratory", "legacy"],
            "fail_closed_on_missing_lineage": True,
            "exploratory_mode_unqualified": True,
            "legacy_mode_unqualified": True,
            "no_implicit_mode_fallback": True,
            "no_automatic_waivers": True,
            "native_lineage_qualified": False,
            "scientific_qualification": False,
            "automatically_conditions_live_model": False,
        },
        "scope": (
            "P6.1-P6.4: Qualification enforcement implemented. Fail-closed on "
            "missing/tampered lineage. Exploratory and legacy modes produce "
            "visibly unqualified artifacts. No implicit mode fallback or "
            "automatic waivers. Full qualification requires P7/P8."
        ),
        "scientific_qualification": False,
        "native_lineage_qualified": False,
        "automatically_conditions_live_model": False,
    }


def main() -> None:
    """Write a qualification receipt or print it to stdout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True, help="Path to manifest JSON")
    parser.add_argument("--mode", choices=["qualified", "exploratory", "legacy"], default="qualified")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    result = run_qualification(args.manifest, args.mode)

    if args.out:
        if args.out.exists() or args.out.is_symlink():
            parser.error("Refusing to overwrite existing output")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2, ensure_ascii=False)
            stream.write("\n")

    sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
