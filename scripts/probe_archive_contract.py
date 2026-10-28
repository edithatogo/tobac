"""Probe frozen native archive APIs with synthetic records, without touching producer state."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
lazy from types import ModuleType


def frozen_bytes(repository: Path, revision: str, name: str) -> bytes:
    """Read committed source only; mutable refs and working files are never executed."""
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        msg = "Producer revision must be a full immutable commit hash"
        raise ValueError(msg)
    executable = shutil.which("git")
    if executable is None:
        msg = "Git is required for frozen producer inspection"
        raise RuntimeError(msg)
    return subprocess.run(  # noqa: S603 -- Resolved Git, explicit argv, pinned revision; no shell.
        [executable, "-C", str(repository), "show", f"{revision}:{name}"],
        check=True,
        capture_output=True,
        timeout=30,
    ).stdout


def load_frozen(path: Path, name: str) -> ModuleType:
    """Load an explicitly selected native source snapshot for local software probes."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        msg = "Cannot load frozen native module"
        raise RuntimeError(msg)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def assess(repository: Path, revision: str) -> dict[str, Any]:
    """Execute native implementations; synthetic success never qualifies real lineage."""
    paths = {
        "manifest": "src/archive_govt_nz/provenance.py",
        "records": "src/archive_govt_nz/records.py",
        "warc": "src/archive_govt_nz/warc.py",
    }
    hashes: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="tobac-native-contract-") as directory:
        root = Path(directory)
        modules: dict[str, ModuleType] = {}
        for name, source in paths.items():
            data = frozen_bytes(repository, revision, source)
            hashes[source] = hashlib.sha256(data).hexdigest()
            path = root / f"{name}.py"
            path.write_bytes(data)
            modules[name] = load_frozen(path, f"tobac_probe_{name}")
        native = modules["manifest"]
        baseline: dict[str, Any] = {
            "archive_id": "synthetic-probe",
            "observations": [{"observation_id": "observation"}],
            "objects": [{"object_id": "object"}],
            "versions": [{"version_id": "version", "observation_id": "observation"}],
        }
        first = native.build_manifest(**baseline)
        cases: dict[str, dict[str, Any]] = {}
        dangling = copy.deepcopy(baseline)
        dangling["versions"][0]["observation_id"] = "missing"
        cases["dangling_observation_rejected"] = dangling
        duplicate = copy.deepcopy(baseline)
        duplicate["objects"] *= 2
        cases["duplicate_object_id_rejected"] = duplicate
        receipt_only = dict(baseline, receipts={"transformations": [{"receipt_id": "only-an-id"}]})
        cases["incomplete_transformation_receipt_rejected"] = receipt_only
        strict_record: dict[str, Any] = {
            "schema_version": "archive-govt-nz.transformation/v1",
            "record_id": "transformation",
            "observed_at": "2026-10-29T00:00:00Z",
            "state": "succeeded",
            "evidence": [],
            "name": "synthetic-probe",
            "version": "1",
            "implementation_revision": revision,
            "input_object_ids": ["object"],
            "output_object_ids": ["derived-object"],
            "parameters": {},
            "environment_sbom_id": "synthetic-environment",
            "started_at": "2026-10-29T00:00:00Z",
            "ended_at": "2026-10-29T00:00:00Z",
            "information_loss": "synthetic fixture",
            "deterministic": True,
        }
        modules["records"].validate_archive_record(strict_record)
        outcomes: dict[str, Any] = {
            "deterministic_manifest": first.canonical_json
            == native.build_manifest(**baseline).canonical_json,
            "strict_transformation_record_valid": True,
        }
        for label, parameters in cases.items():
            try:
                native.build_manifest(**parameters)
            except native.ProvenanceError as exc:
                outcomes[label] = {"rejected": True, "error_class": exc.error_class}
            else:
                outcomes[label] = {"rejected": False}
        try:
            native.build_manifest(**dict(baseline, receipts={"transformations": [strict_record]}))
        except native.ProvenanceError as exc:
            outcomes["strict_record_manifest_interoperability"] = {
                "accepted": False,
                "error_class": exc.error_class,
            }
        else:
            outcomes["strict_record_manifest_interoperability"] = {"accepted": True}
        warc = root / "synthetic.warc"
        modules["warc"].write_response_record(
            warc,
            url="https://example.invalid/synthetic",
            status_code=200,
            headers={},
            body=b"synthetic fixture",
        )
        outcomes["warc_has_capture_date"] = b"WARC-Date:" in warc.read_bytes().split(b"\r\n\r\n", 1)[0]
    return {
        "scope": "frozen_native_code_synthetic_records_not_real_source_or_full_package_qualification",
        "producer_revision": revision,
        "producer_source_sha256": hashes,
        "python": sys.version,
        "outcomes": outcomes,
        "native_lineage_qualified": False,
        "network_capture_performed": False,
    }


def main() -> None:
    """Write a new capability receipt; the producer checkout remains read-only."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists() or args.out.is_symlink():
        parser.error("Refusing to overwrite a capability receipt")
    report = assess(args.repository, args.revision)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2, allow_nan=False) + "\n")
    sys.stdout.write("Native capability assessment recorded; real lineage remains unqualified\n")


if __name__ == "__main__":
    main()
