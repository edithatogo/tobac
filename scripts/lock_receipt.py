"""Bind genuine uv lock output to its dependency inputs; not an approval or attestation.

uv remains responsible for dependency resolution, hash syntax and installation.
This helper only prevents reuse of a missing, altered or stale resolver artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
INPUTS = (
    "pyproject.toml",
    "requirements.lock",
    "engineering/requirements.in",
    "engineering/test-requirements.txt",
    "engineering/build-requirements.txt",
)
PROFILES = {
    "runtime": ("engineering/requirements.in", "requirements.lock"),
    "audit": ("engineering/audit.in", "audit.lock"),
}


# Named bounds preserve the existing scientific/data contract.
INCLUDE_PARTS = 2


def safe_path(root: Path, path: Path) -> Path:
    """Require an existing repository path without traversed symlinks."""
    root = root.resolve()
    candidate = path if path.is_absolute() else root / path
    if ".." in candidate.parts or not candidate.is_relative_to(root):
        msg = "Path must stay inside the repository"
        raise ValueError(msg)
    cursor = root
    for part in candidate.relative_to(root).parts:
        cursor /= part
        if cursor.is_symlink():
            msg = "Dependency/receipt symlink is not allowed"
            raise ValueError(msg)
    if not candidate.is_file():
        msg = f"Required file missing: {candidate.relative_to(root)}"
        raise ValueError(msg)
    return candidate


def digest(path: Path) -> str:
    """Return the SHA-256 digest of the selected file bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_hashes(root: Path, profile: str) -> dict[str, str]:  # noqa: C901  # Keep ordered model validation and report assembly in one visible operation.
    """Bind the declared dependency profile to its complete input file hashes."""
    if profile not in PROFILES:
        msg = "Unknown dependency profile"
        raise ValueError(msg)
    paths = INPUTS + (
        ("engineering/audit.in", "engineering/tools-requirements.txt") if profile == "audit" else ()
    )
    snapshots = {name: digest(safe_path(root, Path(name))) for name in paths}
    # Closed input profile: a new include needs an explicit addition here, not silent reuse.
    for name in paths:
        if name == "pyproject.toml":
            continue
        for line in (root / name).read_text(encoding="utf-8").splitlines():
            tokens = shlex.split(line, comments=True)
            if not tokens:
                continue
            target = None
            if tokens[0] in {"-r", "-c", "--requirement", "--constraint"}:
                if len(tokens) != INCLUDE_PARTS:
                    msg = "Malformed dependency include"
                    raise ValueError(msg)
                target = tokens[1]
            elif tokens[0].startswith(("--requirement=", "--constraint=")):
                target = tokens[0].split("=", 1)[1]
            elif tokens[0].startswith(("-r", "-c")):
                target = tokens[0][2:]
            if target is not None:
                included = (root / name).parent / target
                canonical = included.resolve()
                if (
                    not canonical.is_relative_to(root.resolve())
                    or canonical.relative_to(root.resolve()).as_posix() not in snapshots
                ):
                    msg = "Undeclared dependency include; extend the reviewed input profile"
                    raise ValueError(msg)
    return snapshots


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys while preserving their decoded values."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            msg = f"Duplicate JSON key: {key}"
            raise ValueError(msg)
        result[key] = value
    return result


def verify(root: Path, lock: Path, profile: str) -> dict[str, Any]:
    """Check exact dependency-input and lock bytes; does not prove human review."""
    current = input_hashes(root, profile)
    path = safe_path(root, lock)
    receipt_path = safe_path(root, path.with_suffix(".lock.json"))
    receipt: dict[str, Any] = json.loads(
        receipt_path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs
    )
    if (
        not isinstance(cast("object", receipt), dict)
        or receipt.get("schema") != "tobac.lock-receipt.v1"
        or receipt.get("profile") != profile
        or type(receipt.get("resolver_exit_code")) is not int
        or receipt.get("resolver_exit_code") != 0
    ):
        msg = "Invalid or unsuccessful resolver receipt"
        raise ValueError(msg)
    command = receipt.get("command")
    if (
        not isinstance(command, list)
        or not command
        or "compile" not in command
        or not isinstance(receipt.get("resolver"), str)
        or not receipt["resolver"].startswith("uv ")
    ):
        msg = "Missing uv resolver identity/command"
        raise ValueError(msg)
    if receipt.get("inputs") != current:
        msg = "Dependency input hashes differ; regenerate and review the lock"
        raise ValueError(msg)
    if receipt.get("lock_sha256") != digest(path):
        msg = "Lock hash mismatch"
        raise ValueError(msg)
    if "--hash=sha256:" not in path.read_text(encoding="utf-8"):
        msg = "Empty/unhashed candidate; uv must validate the full hash syntax on sync"
        raise ValueError(msg)
    return {
        "status": "pass",
        "profile": profile,
        "lock_sha256": digest(path),
        "inputs_verified": len(current),
        "resolver": receipt["resolver"],
        "qualification": "byte/input consistency only; not approval, install success or signed provenance",
    }


def recorded_command(command: list[str], root: Path) -> list[str]:
    """Store repo-relative paths so the recorded provenance is reproducible on any checkout."""
    resolved = root.resolve()
    recorded: list[str] = []
    for item in command:
        path = Path(item)
        if path.is_absolute():
            try:
                recorded.append(path.resolve().relative_to(resolved).as_posix())
                continue
            except ValueError:
                pass
        recorded.append(item)
    return recorded


def generate(root: Path, out: Path, profile: str) -> Path:
    """Create a fresh candidate through real uv; a failed process cannot issue a receipt."""
    root = root.resolve()
    before = input_hashes(root, profile)
    uv = shutil.which("uv")
    if uv is None:
        msg = "Install the official uv executable to resolve dependencies"
        raise ValueError(msg)
    out = out if out.is_absolute() else root / out
    if ".." in out.parts or not out.is_relative_to(root):
        msg = "Candidate output must stay inside the repository"
        raise ValueError(msg)
    cursor = root
    for part in out.relative_to(root).parts:
        cursor /= part
        if cursor.is_symlink():
            msg = "Candidate output symlink is not allowed"
            raise ValueError(msg)
    out.mkdir(parents=True, exist_ok=True)
    source, name = PROFILES[profile]
    target = out / name
    receipt_path = target.with_suffix(".lock.json")
    if target.exists() or receipt_path.exists():
        msg = "Refusing to overwrite an existing candidate or reviewed lock"
        raise ValueError(msg)
    command = [
        uv,
        "--no-config",
        "pip",
        "compile",
        str(root / source),
        "--generate-hashes",
        "--output-file",
        str(target),
    ]
    if profile == "runtime":
        command += ["--universal", "--python-version", "3.15"]
    else:
        # Audit utilities include Linux-specific tools; they are not a Windows test dependency.
        command += ["--python-version", "3.15", "--python-platform", "x86_64-unknown-linux-gnu"]
    try:
        version = subprocess.run(  # noqa: S603  # Reviewed fixed executable/argv, bounded invocation, no shell.
            [uv, "--version"], check=True, text=True, capture_output=True, timeout=30
        ).stdout.strip()
        subprocess.run(command, cwd=root, check=True, timeout=600)  # noqa: S603  # Reviewed fixed executable/argv, bounded invocation, no shell.
        if input_hashes(root, profile) != before:
            msg = "Dependency inputs changed during resolution"
            raise ValueError(msg)  # noqa: TRY301  # Record failure or clean incomplete receipts in the enclosing handler.
        if not target.is_file() or "--hash=sha256:" not in target.read_text(encoding="utf-8"):
            msg = "uv did not produce a hashed lock"
            raise ValueError(msg)  # noqa: TRY301  # Record failure or clean incomplete receipts in the enclosing handler.
        receipt = {
            "schema": "tobac.lock-receipt.v1",
            "profile": profile,
            "resolver": version,
            "command": recorded_command(command, root),
            "resolver_exit_code": 0,
            "inputs": before,
            "lock_sha256": digest(target),
            "qualification": "candidate; review before committing; not approval or signed provenance",
        }
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        verify(root, target, profile)
    except OSError, ValueError, subprocess.SubprocessError:
        target.unlink(missing_ok=True)
        receipt_path.unlink(missing_ok=True)
        raise
    return target


def main() -> None:
    """Parse command-line options, execute the selected operation and report its result."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["generate", "verify"])
    parser.add_argument("--profile", choices=PROFILES, required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--path", type=Path, required=True, help="Candidate directory for generate; lock file for verify"
    )
    args = parser.parse_args()
    if args.operation == "generate":
        path = generate(args.root, args.path, args.profile)
        result = verify(args.root, path, args.profile)
    else:
        result = verify(args.root, args.path, args.profile)
    print(json.dumps(result, indent=2))  # noqa: T201  # CLI emits the requested structured result on stdout.


if __name__ == "__main__":
    main()
