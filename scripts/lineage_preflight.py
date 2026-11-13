"""Reopen accepted Phase 5 attempts and verify the current inputs before a qualified workload."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any
lazy from collections.abc import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
import scientific_lineage as scientific  # noqa: E402 -- Select checkout sources inside the isolated verifier.
from source_handoff import checked, read  # noqa: E402 -- Select checkout sources inside the isolated verifier.
lazy from extract_moh_lineage import NativeStore  # noqa: E402 -- Producer protocol from this checkout.

CHECKPOINT = "integration/archive/scientific-lineage-checkpoint_bf1_bf2_20261113.json"
CHECKPOINT_SHA = "afc7636e8f2512695c3ab33b224819155539288527e8a11937152821b5cb36b0"
INTERFACE_SHA = "26814436e834c537b86f007669ef03dc8c16d3187eca25eab0b58d222528f373"
INVENTORY_SHA = "38102d5614683c0a65e260538b6823f58b4ed6365c8fe651e737c69e40d37dd7"
METHODS_ACCEPTANCE = "integration/archive/bf1-bf2-source-acceptance_20261113.json"
METHODS_ACCEPTANCE_SHA = "ce6627c100f583f0510e22da6fd6d60e2e18d7d0e73c1c302fb9c0e2be9e4cd6"


def inventory_identity(root: Path) -> str:
    """Bind source, dataset and runner membership, including uncommitted additions."""
    names: set[str] = set()
    for pattern in ("configs/**/*", "data/**/*", "evidence/**/*", "src/**/*.py", "scripts/run_*.py"):
        names.update(
            p.relative_to(root).as_posix()
            for p in root.glob(pattern)
            if (p.is_file() or p.is_symlink()) and "__pycache__" not in p.parts and p.name != ".DS_Store"
        )
    return hashlib.sha256("\n".join(sorted(names)).encode()).hexdigest()


def checked_pins(root: Path) -> dict[str, Any]:
    """Use the reviewed acceptance snapshot as the authority for terminal IDs and bytes."""
    checkpoint = json.loads(scientific.runners.verified_bytes(checked(root, CHECKPOINT), CHECKPOINT_SHA))
    archive = "integration/archive/"
    scientific.runners.verified_bytes(
        checked(root, archive + "scientific-runner-inputs.json"), checkpoint["pinned_contract_sha256"]
    )
    scientific.runners.verified_bytes(checked(root, archive + "transformation-interface.json"), INTERFACE_SHA)
    scientific.runners.verified_bytes(
        checked(root, archive + "native-source-refs.json"),
        "f75582e8362b39d08bc69ef7196131667bb756e39df285189ca478c2a5bd9ed3",
    )
    scientific.runners.verified_bytes(
        checked(root, archive + "runner-material.json"),
        "3137a95416c95a0c0baba00a30cbedc7527dd71a1dd91c6ec4739a86dae0a109",
    )
    if set(checkpoint["runner_results"]) != set(scientific.RUNS):
        msg = "Runner registry differs from the accepted set"
        raise ValueError(msg)
    if inventory_identity(root) != INVENTORY_SHA:
        msg = "Dataset or operation inventory changed; review its lineage before qualification"
        raise ValueError(msg)
    methods = json.loads(
        scientific.runners.verified_bytes(checked(root, METHODS_ACCEPTANCE), METHODS_ACCEPTANCE_SHA)
    )
    if methods["inventory_sha256"] != INVENTORY_SHA:
        msg = "Methods acceptance inventory differs from the reviewed generation"
        raise ValueError(msg)
    for path, expected in methods["source_sha256"].items():
        scientific.runners.verified_bytes(checked(root, path), expected)
    return checkpoint


def verify_attempt(
    name: str, expected: dict[str, Any], folder: Path, factory: Callable[..., NativeStore]
) -> dict[str, Any]:
    """Compare the actual native attempt and all current scientific input bytes with the accepted run."""
    terminal = read(checked(folder, "terminal"))
    pointers = ("manifest", "receipt", "transformation", "validation", "output_inventory")
    if (
        terminal.get("state") != "succeeded"
        or terminal.get("attempt_id") != expected["attempt_id"]
        or terminal.get("result") != {p: expected[p] for p in pointers}
    ):
        msg = f"{name}: terminal identity differs from the accepted completed attempt"
        raise ValueError(msg)
    record = scientific.load_run(folder, factory, runner=name)
    if record["inputs"] != expected["executed_input_objects"] or record["outputs"] != expected["artifacts"]:
        msg = f"{name}: native input or output inventory differs from acceptance"
        raise ValueError(msg)
    for path, object_id in record["inputs"].items():
        if scientific.runners.digest(checked(ROOT, path)) != object_id.removeprefix("sha256:"):
            msg = f"{name}: stale input or operation: {path}"
            raise ValueError(msg)
    script, config, args, source = scientific.RUNS[name]
    material = scientific.runners.execution_material(
        name, ROOT / config, ROOT / script, record["material"]["inputs"], list(args)
    )
    started = read(checked(folder, "started"))
    producer_revision = read(scientific.ARCHIVE / "transformation-interface.json")["producer_revision"]
    initial = {**material, "producer_revision": producer_revision}
    if "execution_mode" in record:
        initial["execution_mode"] = record["execution_mode"]
    if started.get("material") != initial:
        msg = f"{name}: initial material snapshot is stale"
        raise ValueError(msg)
    if material != record["material"] or record["originals"] != expected["originals"]:
        msg = f"{name}: stale operation, configuration, original or verifier environment"
        raise ValueError(msg)
    if source and source not in record["originals"]:
        msg = f"{name}: missing required original"
        raise ValueError(msg)
    return {
        "attempt_id": terminal["attempt_id"],
        "manifest": expected["manifest"],
        "verified_inputs": len(record["inputs"]),
        "verified_outputs": len(record["outputs"]),
    }


def verify(attempts: Path, wheel: Path, names: list[str], manifest: Path | None = None) -> dict[str, Any]:
    """Fail before workload launch unless every selected native execution and current input matches."""
    if sys.version_info[:3] != (3, 15, 2) or not Path(sys.prefix).resolve().is_relative_to(ROOT):
        msg = "Native verification requires a repo-local Python 3.15.2"
        raise ValueError(msg)
    checkpoint = checked_pins(ROOT)
    accepted = checkpoint["runner_results"]
    if manifest is not None:
        key = "sha256:" + scientific.runners.digest(manifest)
        matching = [name for name, run in accepted.items() if run["manifest"] == key]
        if len(matching) != 1:
            msg = "Manifest has no matching accepted native execution"
            raise ValueError(msg)
        if names and names != matching:
            msg = "Manifest does not belong to the requested runner selection"
            raise ValueError(msg)
        names = matching
    selected = names or sorted(accepted)
    if len(set(selected)) != len(selected) or set(selected) - accepted.keys():
        msg = "Unknown or duplicate runner requested"
        raise ValueError(msg)
    _, factory, pin = scientific.moh.producer(wheel, scientific.ARCHIVE / "transformation-interface.json")
    verified = {name: verify_attempt(name, accepted[name], attempts / name, factory) for name in selected}
    return {
        "success": True,
        "execution_mode": "qualified",
        "qualified": True,
        "scope": "accepted native attempts and current scientific inputs before workload launch",
        "checkpoint_sha256": CHECKPOINT_SHA,
        "producer_revision": pin["producer_revision"],
        "native_lineage_qualified": False,
        "scientific_qualification": False,
        "runners": verified,
    }


def main() -> None:
    """Run the native check inside the selected producer environment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runner", action="append", default=[])
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        receipt = verify(
            Path(os.environ["TOBAC_LINEAGE_ATTEMPTS"]),
            Path(os.environ["TOBAC_LINEAGE_WHEEL"]),
            args.runner,
            args.manifest,
        )
    except Exception as exc:  # noqa: BLE001 -- A failing gate must return a machine-readable rejection.
        receipt = {
            "success": False,
            "qualified": False,
            "execution_mode": "qualified",
            "error": str(exc),
            "native_lineage_qualified": False,
            "scientific_qualification": False,
        }
    sys.stdout.write(json.dumps(receipt, sort_keys=True) + "\n")
    raise SystemExit(0 if receipt["success"] else 2)


if __name__ == "__main__":
    main()
