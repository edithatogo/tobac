"""Fail closed on scanner failures; suppress matches from public logs."""

from __future__ import annotations

import argparse
import subprocess
import sys
lazy from pathlib import Path

from publication_boundary import ROOT, validate_outgoing, validate_tree


def checked(command: list[str], root: Path = ROOT) -> bytes:
    """Execute a qualified tool without echoing potentially sensitive diagnostics."""
    result = subprocess.run(  # noqa: S603 -- Explicit tool argv; no shell and bounded execution.
        command, cwd=root, capture_output=True, check=False, timeout=1800
    )
    if result.returncode:
        msg = "Security tool failed; inspect locally with redacted output before publication"
        raise ValueError(msg)
    return result.stdout


def main() -> None:
    """Check the tree, outgoing commits, full-history secrets and Actions syntax."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pre-push", action="store_true")
    args = parser.parse_args()
    validate_tree(ROOT)
    tips: list[str] = []
    if args.pre_push:
        for line in sys.stdin:
            _local_ref, local_oid, _remote_ref, _remote_oid = line.split()
            if set(local_oid) != {"0"}:
                tips.append(local_oid)
        validate_outgoing(ROOT, tips)
    tools = ROOT / ".security-tools"
    gitleaks = str(tools / "gitleaks")
    actionlint = str(tools / "actionlint")
    if checked([gitleaks, "version"]).decode().strip() != "8.30.1":
        msg = "Unqualified gitleaks version"
        raise ValueError(msg)
    if not checked([actionlint, "-version"]).decode().startswith("1.7.12\n"):
        msg = "Unqualified actionlint version"
        raise ValueError(msg)
    checked(
        [
            gitleaks,
            "git",
            ".",
            "--log-opts=--all",
            "--redact",
            "--no-banner",
            "--ignore-gitleaks-allow",
            "--max-archive-depth",
            "3",
            "--config",
            str(ROOT / "engineering/gitleaks.toml"),
            "--gitleaks-ignore-path",
            "/dev/null",
        ]
    )
    checked(
        [
            gitleaks,
            "git",
            ".",
            "--staged",
            "--redact",
            "--no-banner",
            "--ignore-gitleaks-allow",
            "--config",
            str(ROOT / "engineering/gitleaks.toml"),
            "--gitleaks-ignore-path",
            "/dev/null",
        ]
    )
    checked([actionlint])


if __name__ == "__main__":
    main()
