"""Derive native-record-derived views from existing source bindings.

P2.3: Migrate source-binding exports to native-record-derived views.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = ROOT / "integration/archive/native-source-refs.json"


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from disk."""
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        msg = f"Expected JSON object in {path}"
        raise TypeError(msg)
    return cast("dict[str, Any]", result)


def derive_native_source_refs(
    root: Path,
    interface: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Derive metadata-only native source references from archived bindings."""
    root = root.resolve()
    interface = interface or read_json(root / "integration/archive/native-producer-interface.json")
    register = read_json(root / "integration/archive/source-register.json")
    bindings = read_json(root / "integration/archive/source-bindings.json")

    producer_revision = interface["producer_revision"]
    producer_repo = interface["producer_repository"]
    wheel_sha256 = interface["wheel_sha256"]
    module_sha256 = interface["module_sha256"]

    alias_index: dict[tuple[str, str], dict[str, Any]] = {}
    for source in register.get("sources", []):
        for ref in source.get("references", []):
            key = (ref.get("collection", ""), ref.get("source_id", ""))
            alias_index[key] = source

    native_refs: list[dict[str, Any]] = []
    for binding in bindings.get("sources", []):
        archive_id = binding.get("archive_id", "")
        references = binding.get("references", [])
        captures = binding.get("captures", [])
        redistribution = binding.get("redistribution_authorized", False)

        aliases: list[dict[str, Any]] = []
        for ref in references:
            key = (ref.get("collection", ""), ref.get("source_id", ""))
            source = alias_index.get(key, {})
            aliases.append(
                {
                    "collection": ref.get("collection", ""),
                    "source_id": ref.get("source_id", ""),
                    "archive_id": source.get("archive_id", archive_id),
                }
            )

        capture_refs: list[dict[str, Any]] = []
        for capture in captures:
            status = capture.get("status", "unknown")
            capture_refs.append(
                {
                    "uri": capture.get("uri", ""),
                    "status": status,
                    "sha256": capture.get("sha256"),
                    "byte_count": capture.get("byte_count"),
                    "warc_sha256": capture.get("warc_sha256"),
                    "captured_at": capture.get("captured_at"),
                    "final_uri": capture.get("final_uri", capture.get("uri", "")),
                    "native_source_registered": False,
                    "native_capture_time_verified": capture.get("captured_at") is not None,
                }
            )

        has_verified_capture = any(
            c.get("status") in ("source_html_identity_observed", "source_workbook_values_matched")
            for c in captures
        )
        has_retrieval_failure = any(
            c.get("status") in ("retrieval_failed", "terminal_status") for c in captures
        )

        if has_verified_capture:
            native_status = "metadata_verified"
        elif has_retrieval_failure:
            native_status = "retrieval_failed"
        else:
            native_status = "unverified"

        native_ref = {
            "archive_id": archive_id,
            "consumer_aliases": aliases,
            "captures": capture_refs,
            "redistribution_authorized": redistribution,
            "native_producer_revision": producer_revision,
            "native_producer_repository": producer_repo,
            "native_wheel_sha256": wheel_sha256,
            "native_module_sha256": module_sha256,
            "native_status": native_status,
            "native_source_registered": False,
            "native_capture_time_verified": False,
            "native_manifest_closure": False,
            "native_lineage_qualified": False,
            "scientific_qualification": False,
            "metadata_only": True,
            "automatically_conditions_live_model": False,
        }
        native_refs.append(native_ref)

    return {
        "schema_version": "tobac.native-source-refs.v1",
        "derived_at": datetime.now(UTC).isoformat(),
        "producer_revision": producer_revision,
        "producer_repository": producer_repo,
        "consumer_commit": register.get("consumer_commit", ""),
        "source_count": len(native_refs),
        "native_source_refs": native_refs,
        "authority": "derived_view_not_authoritative",
        "note": (
            "This is a derived view mapping consumer source bindings to native "
            "producer references. It does not introduce a second authority. "
            "Consumer aliases resolve to native record IDs through the producer. "
            "Metadata-only and unavailable states are preserved."
        ),
    }


def main() -> None:
    """Write a derived native source reference receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()

    result = derive_native_source_refs(ROOT)
    if args.out.exists() or args.out.is_symlink():
        parser.error("Refusing to overwrite an existing native source ref receipt")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    sys.stdout.write(f"Derived {result['source_count']} native source refs; no scientific qualification\n")


if __name__ == "__main__":
    main()
