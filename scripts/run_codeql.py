"""Run supported CodeQL CLI extraction and queries inside the caller's resource guard."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("python", "actions")


def validate_sarif(report: dict[str, Any]) -> None:
    """Do not equate an uploaded SARIF file with clean, complete analysis."""
    runs = report.get("runs", [])
    if not runs:
        msg = "Missing CodeQL analysis runs"
        raise ValueError(msg)
    for run in runs:
        if run.get("results"):
            msg = "CodeQL findings require resolution before publication"
            raise ValueError(msg)
        invocations = run.get("invocations", [])
        if not invocations:
            msg = "Missing CodeQL execution evidence"
            raise ValueError(msg)
        for invocation in invocations:
            if invocation.get("executionSuccessful") is not True or any(
                note.get("level") in {"warning", "error"}
                for note in invocation.get("toolExecutionNotifications", [])
            ):
                msg = "Incomplete CodeQL analysis requires investigation"
                raise ValueError(msg)


def run(codeql: Path) -> None:
    """Extract both interpreted languages, then analyze them serially without a build."""
    output = ROOT / "outputs/codeql-results"
    output.mkdir(parents=True, exist_ok=False)

    def command(*args: str) -> None:
        subprocess.run(  # noqa: S603 -- Qualified absolute CLI and explicit argv; no shell.
            [str(codeql), *args], cwd=ROOT, check=True, timeout=1800
        )

    command("version")
    command(
        "database",
        "create",
        "outputs/codeql-databases",
        "--db-cluster",
        "--language=" + ",".join(LANGUAGES),
        "--source-root=.",
        "--threads=2",
        "--ram=3072",
    )
    reports: list[dict[str, Any]] = []
    for language in LANGUAGES:
        path = output / f"{language}.sarif"
        command(
            "database",
            "analyze",
            f"outputs/codeql-databases/{language}",
            f"codeql/{language}-queries:codeql-suites/{language}-security-and-quality.qls",
            "--format=sarif-latest",
            f"--output={path}",
            "--threads=2",
            "--ram=3072",
            f"--sarif-category={language}",
        )
        reports.append(json.loads(path.read_text(encoding="utf-8")))
    for report in reports:
        validate_sarif(report)


def main() -> None:
    """Accept the CLI path returned by the SHA-pinned official setup action."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codeql", type=Path, required=True)
    args = parser.parse_args()
    if not args.codeql.is_absolute() or not args.codeql.is_file():
        parser.error("An installed absolute CodeQL CLI path is required")
    run(args.codeql)


if __name__ == "__main__":
    main()
