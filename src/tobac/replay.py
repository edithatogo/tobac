"""Input-bound stage recovery around existing runners; no scientific approximation."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any
from uuid import uuid4

import numpy as np

MODULES = {"m1": "tobac.run", "m2": "tobac.m2", "m3": "tobac.research.runner"}


def sha(path: Path) -> str:
    """Hash exact artifact bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identities(root: Path) -> dict[str, Any]:
    """Separate parameter/data, model-source and execution environment identities."""
    root = root.resolve()
    inputs = {}
    for folder in ("configs", "data"):
        for path in sorted((root / folder).rglob("*")):
            if path.is_file():
                if path.is_symlink():
                    msg = "Symlink inputs cannot define a replay identity"
                    raise ValueError(msg)
                inputs[path.relative_to(root).as_posix()] = sha(path)
    package = Path(__file__).resolve().parent
    models = {
        p.relative_to(package).as_posix(): sha(p) for p in sorted(package.rglob("*.py"))
    }
    versions = {d: importlib.metadata.version(d) for d in ("numpy", "scipy")}
    locks = {
        str(p.relative_to(root)): sha(p)
        for p in sorted((root / "engineering").glob("*.lock*"))
    }
    return {
        "inputs": inputs,
        "model_sources": models,
        "locks": locks,
        "execution": {
            "python": platform.python_version(),
            "libraries": versions,
            "machine": platform.machine(),
            "system": platform.system(),
            "threads": os.environ.get("OPENBLAS_NUM_THREADS"),
            "backend": "numpy",
            "precision": "float64",
            "rng": "existing exact finite runners; no new sampling",
            "blas": np.show_config(mode="dicts"),
            "xla_flags": os.environ.get("XLA_FLAGS"),
        },
    }


def artifact_path(folder: Path, name: str) -> Path:
    """Reject escaping or symlink artifact declarations before any read."""
    path = folder / name
    if (
        Path(name).is_absolute()
        or ".." in Path(name).parts
        or "\\" in name
        or path.is_symlink()
        or not path.resolve().is_relative_to(folder.resolve())
    ):
        msg = "Unsafe replay artifact path"
        raise ValueError(msg)
    return path


def verify_receipt(root: Path, folder: Path, receipt: dict[str, Any]) -> list[str]:
    """Fail closed on stale source/environment, partial work or altered outputs."""
    errors: list[str] = []
    if receipt.get("schema") != "tobac.replay.v1":
        errors.append("unsupported receipt schema")
    if receipt.get("status") != "complete":
        errors.append("incomplete execution")
    if receipt.get("identity") != identities(root):
        errors.append("input/environment identity changed")
    artifacts = receipt.get("artifacts", {})
    if not artifacts:
        errors.append("missing artifacts")
    for name, expected in artifacts.items():
        path = artifact_path(folder, name)
        if not path.is_file() or sha(path) != expected:
            errors.append(f"artifact changed or missing: {name}")
    return errors


def execute(  # noqa: C901  # Keep stage persistence and fail-closed recovery in order.
    root: Path,
    out: Path,
    stages: list[str],
    *,
    quick: bool = False,
    resume: bool = False,
) -> dict[str, Any]:
    """Resume completed stages only; interrupted stages retain logs and fail closed."""
    root, out = root.resolve(), out.resolve()
    if not stages or len(set(stages)) != len(stages) or set(stages) - MODULES.keys():
        msg = "Select unique supported replay stages"
        raise ValueError(msg)
    if out.exists() and (not resume or not (out / "checkpoint.json").is_file()):
        msg = "Use a new replay directory or an explicit compatible checkpoint"
        raise FileExistsError(msg)
    out.mkdir(parents=True, exist_ok=True)
    identity = identities(root)
    checkpoint = out / "checkpoint.json"
    state: dict[str, Any] = {
        "schema": "tobac.replay-checkpoint.v1",
        "identity": identity,
        "stages": stages,
        "quick": quick,
        "completed": [],
    }
    if resume:
        state = json.loads(checkpoint.read_text(encoding="utf-8"))
        if (
            state.get("schema") != "tobac.replay-checkpoint.v1"
            or state.get("identity") != identity
            or state.get("stages") != stages
            or state.get("quick") != quick
        ):
            msg = "Incompatible checkpoint inputs, model or execution environment"
            raise ValueError(msg)
    for stage in stages:
        folder = out / stage
        receipt_path = out / f"{stage}.receipt.json"
        if stage in state["completed"]:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if verify_receipt(root, folder, receipt):
                msg = "Completed replay stage no longer verifies"
                raise ValueError(msg)
            continue
        command = [sys.executable, "-m", MODULES[stage], "--out", str(folder)]
        if quick:
            command.append("--quick")
        if folder.exists():
            msg = "Interrupted stage output retained; use a new replay directory"
            raise FileExistsError(msg)
        checkpoint.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        with (out / f"{stage}-{uuid4().hex}.log").open("x", encoding="utf-8") as stream:
            result = subprocess.run(  # noqa: S603  # Fixed module allowlist, shell-free argv.
                command, cwd=root, stdout=stream, stderr=subprocess.STDOUT, check=False
            )
        if result.returncode:
            msg = f"Replay stage {stage} failed with exit {result.returncode}"
            raise RuntimeError(msg)
        if identities(root) != identity:
            msg = "Inputs changed during replay"
            raise RuntimeError(msg)
        artifacts = {
            p.relative_to(folder).as_posix(): sha(p)
            for p in sorted(folder.rglob("*"))
            if p.is_file()
        }
        receipt = {
            "schema": "tobac.replay.v1",
            "status": "complete",
            "identity": identity,
            "command": command,
            "exit": 0,
            "stage": stage,
            "quick": quick,
            "artifacts": artifacts,
        }
        with receipt_path.open("x", encoding="utf-8") as stream:
            json.dump(receipt, stream, indent=2, allow_nan=False)
            stream.write("\n")
        state["completed"].append(stage)
        checkpoint.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return state


def main() -> None:
    """Execute explicit stages without overwriting previous successful receipts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--stages", nargs="+", choices=MODULES, default=list(MODULES))
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    result = execute(
        args.root, args.out, args.stages, quick=args.quick, resume=args.resume
    )
    sys.stdout.write(json.dumps(result, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
