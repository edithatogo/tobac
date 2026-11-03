"""Create an auditable canonical validation view without altering raw runner outputs."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from source_handoff import digest, read, same_hash

ROOT = Path(__file__).resolve().parents[1]


def canonical_inputs(root: Path, inputs: dict[str, str]) -> dict[str, str]:
    """Normalize Windows separators while retaining strict repository/hash checks."""
    result: dict[str, str] = {}
    for name, expected in inputs.items():
        if ":" in name:
            msg = "Drive-qualified runtime input path is forbidden"
            raise ValueError(msg)
        canonical = name.replace("\\", "/")
        if canonical in result:
            msg = "Duplicate canonical runtime input"
            raise ValueError(msg)
        same_hash(root, canonical, expected)
        result[canonical] = expected
    return result


def prepare(root: Path, replay: Path, out: Path) -> dict[str, Any]:
    """Copy validated output bytes, canonicalize only manifest input keys, and retain provenance."""
    out.mkdir(parents=True, exist_ok=False)
    raw = replay / "m2/manifest.json"
    raw_sha = digest(raw)
    manifest = read(raw)
    normalized = canonical_inputs(root, manifest["inputs"])
    for name, expected in manifest["outputs"].items():
        same_hash(replay / "m2", name, expected)
    for name in ("m2", "release_calibration"):
        shutil.copytree(replay / name, out / name)
    manifest["inputs"] = normalized
    view = out / "m2/manifest.json"
    view.write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if digest(raw) != raw_sha:
        msg = "Raw runner manifest changed during preparation"
        raise ValueError(msg)
    report = {
        "schema": "tobac.synthesis-validation-view.v1",
        "status": "passed",
        "raw_manifest_sha256": raw_sha,
        "view_manifest_sha256": digest(view),
        "inputs": normalized,
        "output_hashes": manifest["outputs"],
        "raw_outputs_unchanged": True,
        "scope": "Validation view only; native model inputs and original runner outputs remain unchanged",
    }
    (out / "view.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    """Use a new validation-view directory for one completed reproduction generation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    prepare(ROOT, args.replay, args.out)


if __name__ == "__main__":
    main()
