"""Rebuild the metadata-only source view from pinned receipts and installed producer APIs."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import io
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_moh_lineage import NativeStore, encoded, producer, verified_bytes
from source_handoff import ORIGINAL_STATUSES, archive_index, checked, digest, read

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "integration/archive"
OUTPUT = ARCHIVE / "native-source-refs.json"
PIN = ARCHIVE / "native-registration-interface.json"


def capture_index(evidence: Path, expected: list[str]) -> dict[str, dict[str, Any]]:
    """Index only exact historical receipt bytes, with unambiguous target URIs."""
    found: set[str] = set()
    targets: dict[str, dict[str, Any]] = {}
    for receipt in sorted(evidence.glob("*/capture.json")):
        checksum = digest(receipt)
        if checksum not in expected:
            continue
        if checksum in found:
            msg = "Duplicate capture receipt"
            raise ValueError(msg)
        found.add(checksum)
        for target in read(receipt)["targets"]:
            uri = target["uri"]
            if uri in targets:
                msg = "Duplicate capture target"
                raise ValueError(msg)
            targets[uri] = target
    if found != set(expected):
        msg = "Missing pinned capture receipt"
        raise ValueError(msg)
    return targets


def check_capture(
    capture: dict[str, Any], target: dict[str, Any], evidence: Path, store: NativeStore
) -> bytes | None:
    """Verify the response object and original WARC; preserve failed retrievals."""
    if target["status"] == "failed":
        if capture["status"] != "retrieval_failed" or capture.get("error") != target["error"]:
            msg = "Failed capture differs from binding"
            raise ValueError(msg)
        return None
    sha = capture["sha256"]
    warc = target["warc"]
    if (target["status"], target["sha256"], target["byte_count"], warc["sha256"]) != (
        "captured",
        sha,
        capture["byte_count"],
        capture["warc_sha256"],
    ):
        msg = "Native capture identity differs from binding"
        raise ValueError(msg)
    body = verified_bytes(store.verify("sha256:" + sha).path, sha)
    prefix = "build/tobac/"
    if not warc["path"].startswith(prefix):
        msg = "WARC outside the capture root"
        raise ValueError(msg)
    raw = verified_bytes(checked(evidence, warc["path"][len(prefix) :]), warc["sha256"])
    iterator = iter(importlib.import_module("warcio.archiveiterator").ArchiveIterator(io.BytesIO(raw)))
    record = next(iterator)
    if (
        len(raw) != warc["byte_count"]
        or len(body) != capture["byte_count"]
        or record.rec_headers.get_header("WARC-Record-ID") != "<" + warc["record_id"] + ">"
        or record.content_stream().read() != body
        or next(iterator, None) is not None
    ):
        msg = "WARC readback differs from captured bytes or record ID"
        raise ValueError(msg)
    return body


def persist(store: NativeStore, document: dict[str, Any]) -> str:
    """Write native output into the private evidence store and reopen identical bytes."""
    raw = encoded(document)
    receipt = store.put_bytes(raw)
    if verified_bytes(store.verify(receipt.object_id).path) != raw:
        msg = "Persisted registration evidence differs"
        raise ValueError(msg)
    return receipt.object_id


def register_capture(
    binding: dict[str, Any], capture: dict[str, Any], body: bytes, store: NativeStore
) -> dict[str, str]:
    """Use the producer to register only matched source bytes in the qualification store."""
    native = importlib.import_module("archive_govt_nz.source_registration")
    identity = importlib.import_module("archive_govt_nz.core.identity")
    archive_id = binding["archive_id"]
    reg = native.register_source(
        source_id=archive_id,
        source_uri=identity.canonical_source_uri("web", "tobac", capture["uri"]),
        source_type="web",
        agency_slug="tobac",
        archive_id=archive_id,
        object_bytes=body,
        object_id="sha256:" + capture["sha256"],
        redistribution_authorized=binding["redistribution_authorized"],
    )
    manifest = native.build_source_manifest(reg)
    original_id = store.put_bytes(body).object_id
    if store.verify(original_id).sha256 != capture["sha256"] or manifest["objects"] != [
        {"object_id": original_id}
    ]:
        msg = "Native manifest does not resolve the original"
        raise ValueError(msg)
    return {
        "object_id": original_id,
        "observation_id": manifest["observations"][0]["observation_id"],
        "version_id": manifest["versions"][0]["version_id"],
        "registration_object_id": persist(store, reg.to_dict()),
        "manifest_object_id": persist(store, manifest),
    }


def derive_native_source_refs(wheel: Path, evidence: Path, destination: Path) -> dict[str, Any]:
    """Account for every bibliography alias and capture via the exact installed producer."""
    if sys.version_info[:3] != (3, 15, 1):
        msg = "Python 3.15.1 required"
        raise RuntimeError(msg)
    _, make_store, pin = producer(wheel, PIN)
    aliases, bindings, _ = archive_index(ROOT)
    legacy = read(ARCHIVE / "source-bindings.json")
    targets = capture_index(evidence, legacy["capture_receipt_sha256"])
    factory = importlib.import_module("archive_govt_nz.object_store").ContentAddressedStore
    originals = factory(evidence / "cas", create=False)
    destination.mkdir(parents=True, exist_ok=False)
    store = make_store(destination)
    refs: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for archive_id, binding in sorted(bindings.items()):
        captures: list[dict[str, Any]] = []
        for capture in binding["captures"]:
            target = targets[capture["uri"]]
            body = check_capture(capture, target, evidence, originals)
            registration = None
            if body is not None and capture["status"] in ORIGINAL_STATUSES:
                registration = register_capture(binding, capture, body, store)
            captures.append(
                {
                    **capture,
                    "warc_record_id": target.get("warc", {}).get("record_id"),
                    "bytes_verified": body is not None,
                    "native_registration": registration,
                }
            )
            counts[capture["status"]] += 1
        refs.append(
            {
                "archive_id": archive_id,
                "consumer_aliases": binding["references"],
                "redistribution_authorized": binding["redistribution_authorized"],
                "captures": captures,
            }
        )
    return {
        "schema_version": "tobac.native-source-refs.v2",
        "authority": "derived_view_not_authoritative",
        "producer_revision": pin["producer_revision"],
        "wheel_sha256": pin["wheel_sha256"],
        "source_register_sha256": legacy["register_sha256"],
        "source_bindings_sha256": digest(ARCHIVE / "source-bindings.json"),
        "capture_receipt_sha256": legacy["capture_receipt_sha256"],
        "source_count": len(refs),
        "alias_count": len(aliases),
        "capture_status_counts": dict(counts),
        "native_source_refs": refs,
        "registration_scope": (
            "Private qualification store; preserved bytes only. "
            "Bibliographic metadata and challenge pages are not registered originals."
        ),
        "native_lineage_qualified": False,
        "scientific_qualification": False,
        "automatically_conditions_live_model": False,
    }


def main() -> None:
    """Generate a new export, or compare an existing export with an independent replay."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path, help="New private qualification store")
    parser.add_argument("--out", type=Path, default=OUTPUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = derive_native_source_refs(args.wheel, args.evidence, args.store)
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.verify:
        if verified_bytes(args.out) != raw:
            parser.error("Existing export differs from replay")
    else:
        with args.out.open("xb") as stream:
            stream.write(raw)
    sys.stdout.write(f"{result['source_count']} sources; SHA-256 {hashlib.sha256(raw).hexdigest()}\n")


if __name__ == "__main__":
    main()
