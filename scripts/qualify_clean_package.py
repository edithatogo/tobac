"""Build with source overrides disabled and execute the real installed CLI outside the checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def qualify(out: Path) -> dict[str, Any]:
    """Keep artifacts and execution records; isolate import paths and dependencies."""
    if sys.version_info[:3] != (3, 15, 1):
        msg = "Select repo-local Python 3.15.1"
        raise RuntimeError(msg)
    out = out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    uv = shutil.which("uv")
    if not uv:
        msg = "uv is required for clean-package qualification"
        raise RuntimeError(msg)
    records: list[dict[str, Any]] = []
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env.update(OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg", PYTHONHASHSEED="0")

    def run(args: list[str], cwd: Path) -> None:
        result = subprocess.run(  # noqa: S603  # Internal argv; resolved uv and isolated Python.
            args, cwd=cwd, env=env, capture_output=True, text=True, check=False
        )
        records.append(
            {
                "command": args,
                "exit": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        (out / "commands.json").write_text(
            json.dumps(records, indent=2) + "\n", encoding="utf-8"
        )
        result.check_returncode()

    run(
        [
            uv,
            "build",
            "--no-sources",
            "--no-build-isolation",
            "--python",
            sys.executable,
            "--out-dir",
            str(out / "dist"),
        ],
        ROOT,
    )
    (wheel,) = (out / "dist").glob("*.whl")
    (sdist,) = (out / "dist").glob("*.tar.gz")
    run(
        [
            uv,
            "build",
            "--no-sources",
            "--no-build-isolation",
            "--python",
            sys.executable,
            "--wheel",
            str(sdist),
            "--out-dir",
            str(out / "reconstructed"),
        ],
        ROOT,
    )
    with tempfile.TemporaryDirectory(prefix="tobac-clean-package-") as name:
        external = Path(name)
        clean = external / "venv"
        python = clean / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        run([uv, "venv", "--python", sys.executable, str(clean)], external)
        run(
            [
                uv,
                "pip",
                "sync",
                "--python",
                str(python),
                "--require-hashes",
                str(ROOT / "engineering/requirements.lock"),
            ],
            external,
        )
        run(
            [
                uv,
                "pip",
                "install",
                "--python",
                str(python),
                "--no-deps",
                "--no-index",
                str(wheel),
            ],
            external,
        )
        run([uv, "pip", "check", "--python", str(python)], external)
        probe = (
            "import pathlib,sys,tobac; from tobac._core import DecisionProblem,exact_evpi; "
            "import numpy as np; p=pathlib.Path(tobac.__file__).resolve(); "
            "assert p.is_relative_to(pathlib.Path(sys.prefix).resolve()); "
            "assert sys.version_info[:3]==(3,15,1); "
            "assert exact_evpi(DecisionProblem(np.array([[0.,4.],[3.,0.]]),"
            "('a','b'),'score',np.array([.75,.25])))==.75; print(p)"
        )
        run([str(python), "-I", "-c", probe], external)
        shutil.copytree(ROOT / "configs", external / "configs")
        run(
            [str(python), "-I", "-m", "tobac.run", "--quick", "--out", "result"],
            external,
        )
        validation = json.loads(
            (external / "result/validation.json").read_text(encoding="utf-8")
        )
        shutil.copytree(external / "result", out / "installed-cli-result")
    result = {
        "schema": "tobac.clean-package.v1",
        "status": "passed",
        "python": sys.version,
        "source_overrides": False,
        "artifacts": {
            str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in out.rglob("*")
            if p.is_file()
        },
        "installed_cli_validation": validation,
        "scope": "wheel install/API/quick M1 CLI and sdist-to-wheel build; no external scientific approval",
    }
    (out / "receipt.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    """Retain a new qualification generation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    qualify(args.out)
    sys.stdout.write("Clean-package install, API and M1 CLI passed\n")


if __name__ == "__main__":
    main()
