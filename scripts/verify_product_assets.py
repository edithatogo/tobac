"""Read back consumer-held objects using the existing native WARC library; never acquire or publish."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def verify(store: Path, warcs: Path) -> dict[str, Any]:
    """Require actual CAS/WARC bytes and URL-bound payload agreement for all nine assets."""
    if sys.version_info[:3] != (3, 15, 1) or importlib.metadata.version("warcio") != "1.8.1":
        msg = "Select the qualified native-provider Python 3.15.1 / warcio 1.8.1 environment"
        raise RuntimeError(msg)
    reader = importlib.import_module("warcio.archiveiterator")
    manifest = ROOT / "integration/reconciliation_2025/source-assets.json"
    assets = json.loads(manifest.read_text(encoding="utf-8"))["sources"]
    results: list[dict[str, Any]] = []
    for index, asset in enumerate(assets):
        sha = asset["sha256"]
        body = store / "sha256" / sha[:2] / sha
        warc = warcs / f"tobac-products-2025-{index}.warc"
        if (
            hashlib.sha256(body.read_bytes()).hexdigest() != sha
            or hashlib.sha256(warc.read_bytes()).hexdigest() != asset["warc_sha256"]
        ):
            msg = "Native source object hash mismatch"
            raise ValueError(msg)
        with warc.open("rb") as stream:
            iterator = iter(reader.ArchiveIterator(stream))
            record = next(iterator)
            payload = record.content_stream().read()
            request = record.rec_headers.get_header("WARC-Request-URL-SHA256")
            date = record.rec_headers.get_header("WARC-Date")
            if (
                payload != body.read_bytes()
                or request != hashlib.sha256(asset["uri"].encode()).hexdigest()
                or next(iterator, None) is not None
            ):
                msg = "Native WARC payload or request identity mismatch"
                raise ValueError(msg)
        results.append(
            {
                "asset_id": asset["id"],
                "sha256": sha,
                "warc_sha256": asset["warc_sha256"],
                "native_capture_timestamp": date,
                "status": "verified",
            }
        )
    return {
        "schema": "tobac.product-assets-verification.v1",
        "verified_at": datetime.now(UTC).isoformat(),
        "python": sys.version,
        "warcio": "1.8.1",
        "assets": results,
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "scope": "local object integrity and request binding; not source interpretation or remote recovery",
    }


def main() -> None:
    """Write a new execution receipt while preserving previous verification generations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--warcs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.store, args.warcs)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    sys.stdout.write(
        f"Verified {len(result['assets'])} local CAS/WARC assets; original timestamps preserved\n"
    )


if __name__ == "__main__":
    main()
