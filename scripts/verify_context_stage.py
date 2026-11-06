"""Verify an existing context bundle before analytical work; emit a logged stage receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from context_bundle import ROOT, validate_public_paths, verify


def digest(path: Path) -> str:
    """Return the SHA-256 identity of a bounded context artifact."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inspect_bundle(bundle: Path) -> dict[str, Any]:
    """Check every invocation, including when workflow outputs appear up to date."""
    if sys.version_info[:3] != (3, 15, 1) or not Path(sys.prefix).resolve().is_relative_to(ROOT):
        msg = "Select repo-local Python 3.15.1"
        raise ValueError(msg)
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(manifest.get("files"), list) or not manifest["files"]:
        msg = "Context requires a nonempty source inventory"
        raise ValueError(msg)
    validate_public_paths(ROOT, [item["path"] for item in manifest["files"]])
    errors = verify(ROOT, manifest)
    if digest(bundle / "context.md") != manifest["context_sha256"]:
        errors.append("context text changed")
    if errors:
        raise ValueError("; ".join(errors))
    return manifest


def execute(bundle: Path, receipt: Path, log: Path) -> None:
    """Remove stale acceptance and fail before recording success for invalid inputs."""
    if receipt == log or any(
        path in (bundle / "manifest.json", bundle / "context.md") for path in (receipt, log)
    ):
        msg = "Receipt must not overwrite inputs or logs"
        raise ValueError(msg)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    receipt.unlink(missing_ok=True)
    event = {"stage": "verify_context", "time_utc": datetime.now(UTC).isoformat()}
    try:
        manifest_path = bundle / "manifest.json"
        manifest = inspect_bundle(bundle)
        result = {
            "schema": "tobac.context-stage.v1",
            "status": "passed",
            "commit": manifest["commit"],
            "manifest_sha256": digest(manifest_path),
            "context_sha256": manifest["context_sha256"],
            "python": sys.version,
            "qualification": "Context identity only; no empirical or native lineage acceptance",
        }
        temporary = receipt.with_suffix(receipt.suffix + ".tmp")
        temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        temporary.replace(receipt)
        event["status"] = "passed"
    except Exception as error:
        event.update(status="failed", error_type=type(error).__name__)
        raise
    finally:
        with log.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event) + "\n")


def main() -> None:
    """Run verification without allowing arbitrary analytical commands."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.check_only:
        inspect_bundle(args.bundle.resolve())
    elif args.receipt is None or args.log is None:
        parser.error("--receipt and --log are required unless --check-only")
    else:
        execute(args.bundle.resolve(), args.receipt.resolve(), args.log.resolve())


if __name__ == "__main__":
    main()
