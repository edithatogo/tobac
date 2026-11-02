"""Persist and reopen the native execution linking scientific inputs to the output inventory."""

from __future__ import annotations

import importlib
import importlib.metadata
import json
from typing import Any

from extract_moh_lineage import NativeRecords, NativeStore, now


def put_json(store: NativeStore, document: dict[str, Any]) -> str:
    """Persist one deterministic JSON object and compare its readback with the supplied bytes."""
    raw = json.dumps(document, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    obj = store.put_bytes(raw)
    if store.verify(obj.object_id).path.read_bytes() != raw:
        msg = "Native JSON readback mismatch"
        raise ValueError(msg)
    return obj.object_id


def read_object(store: NativeStore, key: str) -> dict[str, Any]:
    """Parse the actual verified object bytes."""
    return json.loads(store.verify(key).path.read_bytes())


def runtime_sbom() -> dict[str, Any]:
    """Inventory the running distributions in a CycloneDX component list."""
    packages = sorted({(dist.metadata["Name"], dist.version) for dist in importlib.metadata.distributions()})
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "components": [{"type": "library", "name": n, "version": v} for n, v in packages],
    }


def persist_execution(record: dict[str, Any], native: NativeRecords, store: NativeStore) -> dict[str, str]:
    """Use the producer's strict transformation, validation and manifest interfaces."""
    api = importlib.import_module("archive_govt_nz.provenance")
    ended = now()
    receipt = put_json(store, record)
    result = put_json(store, record["outputs"])
    sbom = put_json(store, runtime_sbom())
    inputs = sorted(set(record["inputs"].values()) | set(record["originals"].values()))
    transform = {
        "schema_version": "archive-govt-nz.transformation/v1",
        "record_id": record["attempt_id"],
        "observed_at": ended,
        "state": "succeeded",
        "evidence": [],
        "name": record["runner"],
        "version": "1",
        "implementation_revision": record["model_revision"],
        "input_object_ids": inputs,
        "output_object_ids": [result],
        "parameters": record["material"],
        "environment_sbom_id": sbom,
        "started_at": record["started"],
        "ended_at": ended,
        "information_loss": "Output object is the exact named artifact inventory.",
        "deterministic": False,
    }
    validate = {
        "schema_version": "archive-govt-nz.validation/v1",
        "record_id": record["attempt_id"] + "-check",
        "observed_at": ended,
        "state": "passed",
        "evidence": [],
        "validator_name": "tobac.scientific-lineage",
        "validator_version": "1",
        "subject_ids": [receipt, result],
        "checks": ["original comparison", "input fixity", "output inventory"],
        "findings": [],
        "started_at": record["started"],
        "ended_at": ended,
    }
    strict = [store.put_bytes(native.canonical_record_bytes(r)).object_id for r in (transform, validate)]
    objects = set(inputs) | set(record["outputs"].values()) | {receipt, result, sbom, *strict}
    for refs in record["material"]["inputs"].values():
        for ref in refs:
            objects.update(ref[k] for k in ("registration_object_id", "manifest_object_id"))
    for key in objects:
        store.verify(key)
    manifest = api.build_manifest(
        archive_id=record["attempt_id"],
        objects=[{"object_id": k} for k in sorted(objects)],
        observations=[],
        versions=[],
        receipts=api.build_receipts_from_records([transform], [validate]),
        expected_revisions={record["attempt_id"]: record["model_revision"]},
        context={"execution_receipt": receipt, "transform": strict[0], "validation": strict[1]},
    )
    return {
        "receipt": receipt,
        "manifest": store.put_bytes(manifest.canonical_json).object_id,
        "transformation": strict[0],
        "validation": strict[1],
        "output_inventory": result,
    }


def verify_execution(record: dict[str, Any], terminal: dict[str, Any], store: NativeStore) -> None:
    """Cross-check the terminal pointer, native record IDs and complete output inventory."""
    refs = terminal["result"]
    manifest = read_object(store, refs["manifest"])
    transform = read_object(store, refs["transformation"])
    validation = read_object(store, refs["validation"])
    for entry in manifest["objects"]:
        store.verify(entry["object_id"])
    if (
        manifest["archive_id"] != terminal["attempt_id"]
        or transform["record_id"] != terminal["attempt_id"]
        or manifest["context"]
        != {
            "execution_receipt": refs["receipt"],
            "transform": refs["transformation"],
            "validation": refs["validation"],
        }
        or transform["state"] != "succeeded"
        or validation["state"] != "passed"
        or set(transform["input_object_ids"])
        != set(record["inputs"].values()) | set(record["originals"].values())
        or transform["output_object_ids"] != [refs["output_inventory"]]
        or read_object(store, refs["output_inventory"]) != record["outputs"]
    ):
        msg = "Native transform, validation or output inventory does not match the completed attempt"
        raise ValueError(msg)
