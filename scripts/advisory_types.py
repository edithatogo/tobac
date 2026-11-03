"""Run both pinned advisory checkers and retain their original structured reports."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "advisory"


def digest(path: Path) -> str:
    """Hash the bytes of one declared input."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fatal_codes(codes: list[str]) -> list[str]:
    """Reject missing dependencies and syntax failures from either checker."""
    return [
        code
        for code in codes
        if any(
            marker in code.lower()
            for marker in (
                "unresolved-import",
                "missing-import",
                "parse-error",
                "syntax-error",
                "invalid-syntax",
            )
        )
    ]


def run() -> None:
    """Execute the pinned checkers and retain their reports."""
    if sys.version_info[:3] != (3, 15, 1):
        msg = "Python 3.15.1 is required"
        raise RuntimeError(msg)
    OUT.mkdir(parents=True, exist_ok=True)
    binary = Path(sys.executable).parent
    config = OUT / "pyrefly.toml"
    config.write_text(
        f'python-version = "3.15.1"\npython-interpreter = {json.dumps(sys.executable)}\n'
        'search-path = ["../../src", "../../scripts"]\n'
    )
    commands = {
        "ty": [
            str(binary / "ty"),
            "check",
            "--python",
            sys.executable,
            "--python-version",
            "3.15",
            "--output-format",
            "sarif",
            "src",
            "scripts",
        ],
        "pyrefly": [
            str(binary / "pyrefly"),
            "check",
            "--config",
            str(config),
            "--output-format",
            "json",
            "src",
            "scripts",
        ],
    }
    results = {}
    for name, command in commands.items():
        version = subprocess.run(  # noqa: S603 -- Fixed interpreter-local tool and argument.
            [str(binary / name), "--version"], capture_output=True, text=True, check=True, timeout=30
        ).stdout.strip()
        if not version.startswith({"ty": "ty 0.0.95", "pyrefly": "pyrefly 1.4.0"}[name]):
            msg = f"Unexpected {name} version: {version}"
            raise RuntimeError(msg)
        process = subprocess.run(  # noqa: S603 -- Fixed pinned checker arguments; no shell.
            command, cwd=ROOT, capture_output=True, timeout=2100, check=False
        )
        (OUT / f"{name}.json").write_bytes(process.stdout)
        (OUT / f"{name}.stderr.txt").write_bytes(process.stderr)
        if process.returncode not in (0, 1):
            msg = f"{name} failed with exit {process.returncode}"
            raise RuntimeError(msg)
        report = json.loads(process.stdout)
        if name == "ty":
            entries = report["runs"][0]["results"]
            codes = [entry["ruleId"] for entry in entries]
        else:
            entries = report["errors"]
            codes = [entry["name"] for entry in entries]
        if (
            not isinstance(entries, list)
            or (process.returncode == 1 and not entries)
            or (process.returncode == 0 and entries)
        ):
            msg = f"{name} returned an invalid diagnostic report"
            raise RuntimeError(msg)
        fatal = fatal_codes(codes)
        results[name] = {
            "version": version,
            "command": command,
            "exit_code": process.returncode,
            "count": len(entries),
            "codes": sorted(set(codes)),
            "fatal_codes": sorted(set(fatal)),
        }
    files = sorted(p for base in (ROOT / "src", ROOT / "scripts") for p in base.rglob("*.py"))
    inputs = {str(p.relative_to(ROOT)): digest(p) for p in files}
    for path in (
        ROOT / "engineering/advisory.in",
        ROOT / "engineering/advisory.lock",
        ROOT / "engineering/advisory.lock.json",
        ROOT / "pyproject.toml",
        config,
    ):
        inputs[str(path.relative_to(ROOT))] = digest(path)
    environment = sorted((d.metadata["Name"], d.version) for d in importlib.metadata.distributions())
    metadata = {
        "python": sys.version,
        "interpreter": sys.executable,
        "environment": environment,
        "inputs": inputs,
        "results": results,
    }
    (OUT / "receipt.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if any(result["fatal_codes"] for result in results.values()):
        msg = "Required imports or syntax could not be resolved; inspect reports"
        raise RuntimeError(msg)


if __name__ == "__main__":
    run()
