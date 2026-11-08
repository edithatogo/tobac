"""Reopen synthetic qualification inputs and outputs; never grant empirical admission."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]
from lock_receipt import verify as verify_lock  # noqa: E402 -- Select existing checkout verifier.
from source_handoff import checked, read, same_hash  # noqa: E402 -- Reuse canonical path/hash guards.


def qualification_inputs(root: Path) -> dict[str, str]:
    """Bind the complete exercised code/type/dependency input set, not just its mtimes."""
    names = {
        "noxfile.py",
        "workflow/Snakefile",
        "engineering/requirements.lock",
        "engineering/clustering.in",
        "engineering/clustering.lock.json",
        "scripts/verify_sensitivity_clustering.py",
        "scripts/source_handoff.py",
        "scripts/lock_receipt.py",
        "engineering/typings/threadpoolctl.pyi",
        *[
            f"engineering/typings/sklearn/{name}.pyi"
            for name in (
                "__init__",
                "cluster",
                "dummy",
                "linear_model",
                "metrics",
                "pipeline",
                "preprocessing",
            )
        ],
        *[p.relative_to(root).as_posix() for p in (root / "engineering/typings/sklearn").glob("*.pyi")],
    }
    return {name: hashlib.sha256(checked(root, name).read_bytes()).hexdigest() for name in sorted(names)}


def verify_packet(root: Path, out: Path, lock: Path) -> dict[str, object]:
    """Reject incomplete, stale or altered packets before any scheduler cache decision."""
    root = root.resolve()
    relative = out.absolute().relative_to(root).as_posix()
    manifest = read(checked(root, relative + "/manifest.json"))
    lock_relative = lock.absolute().relative_to(root).as_posix()
    verify_lock(root, checked(root, lock_relative), "clustering")
    if (
        manifest.get("schema") != "tobac.synthetic-qualification-packet.v2"
        or manifest.get("formula_version") != "synthetic-sensitivity-clustering-v1"
    ):
        msg = "Unknown synthetic formula contract"
        raise ValueError(msg)
    members = {p.name for p in out.iterdir()}
    marker = ".snakemake_timestamp"
    if marker in members:
        if checked(out, marker).stat().st_size:
            msg = "Scheduler marker must be an empty regular file"
            raise ValueError(msg)
        members.remove(marker)
    if members != {"summary.json", "stability.csv", "manifest.json"}:
        msg = "Packet contains missing or extra members"
        raise ValueError(msg)
    if set(manifest["files"]) != {"summary.json", "stability.csv"}:
        msg = "Packet output inventory differs"
        raise ValueError(msg)
    for name, sha in manifest["files"].items():
        same_hash(out, name, sha)
    same_hash(root, "scripts/qualify_sensitivity_clustering.py", manifest["script_sha256"])
    same_hash(root, lock_relative, manifest["lock_sha256"])
    if manifest["qualification_inputs"] != qualification_inputs(root):
        msg = "Synthetic qualification inputs are stale"
        raise ValueError(msg)
    summary = read(checked(out, "summary.json"))
    if (
        summary.get("success") is not True
        or summary.get("source") != "synthetic_only"
        or summary.get("empirical_qualification") is not False
    ):
        msg = "Packet does not declare a successful synthetic-only qualification"
        raise ValueError(msg)
    return {"status": "passed", "files": 2, "synthetic_only": True, "empirical_qualification": False}


def main() -> None:
    """Verify an existing immutable packet without fetching data or running a model."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--lock", type=Path, default=ROOT / "engineering/clustering.lock")
    args = parser.parse_args()
    sys.stdout.write(json.dumps(verify_packet(ROOT, args.out, args.lock)) + "\n")


if __name__ == "__main__":
    main()
