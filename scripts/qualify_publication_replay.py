"""Regenerate the paper's finite outputs from a clean committed source archive."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import TYPE_CHECKING, cast

from source_handoff import digest, read

if TYPE_CHECKING:
    from tobac._typing import Report

ROOT = Path(__file__).resolve().parents[1]
TOLERANCE = 1e-10
IDENTITY_COLUMNS = frozenset(
    {
        "case",
        "challenge",
        "action",
        "group",
        "design",
        "target",
        "cooptimal_actions",
        "cooptimal_across_continuous_box",
        "source_id",
        "document_id",
        "underlying_data_group",
        "model_use",
        "limitation",
    }
)
EXPECTED_CHECKS: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("results/m2_publication_20261028", "primary", "scripts/run_m2_publication.py", ("--grid-check",)),
    ("results/m2_readiness_20261028", "robustness", "scripts/run_m2_robustness.py", ()),
)


def compare_values(expected: object, actual: object, *, location: str = "root") -> float:
    """Compare scientific JSON recursively; exclude only top-level checkout metadata."""
    if isinstance(expected, bool) or isinstance(actual, bool):
        same = type(cast("object", expected)) is type(cast("object", actual)) and expected == actual
    elif isinstance(expected, (float, int)) and isinstance(actual, (float, int)):
        if not math.isfinite(expected) or not math.isfinite(actual):
            msg = f"Nonfinite scientific value at {location}"
            raise ValueError(msg)
        delta = abs(float(expected) - float(actual))
        if delta > TOLERANCE:
            msg = f"Numerical mismatch at {location}: {delta}"
            raise ValueError(msg)
        return delta
    elif isinstance(expected, dict) and isinstance(actual, dict):
        expected = cast("dict[str, object]", expected)
        actual = cast("dict[str, object]", actual)
        keys = set(expected) - ({"checkout"} if location == "root" else set())
        if keys != set(actual) - ({"checkout"} if location == "root" else set()):
            msg = f"Scientific JSON fields differ at {location}"
            raise ValueError(msg)
        return max(
            (compare_values(expected[k], actual[k], location=f"{location}.{k}") for k in keys), default=0
        )
    elif isinstance(expected, list) and isinstance(actual, list):
        expected = cast("list[object]", expected)
        actual = cast("list[object]", actual)
        if len(expected) != len(actual):
            msg = f"Scientific list length mismatch at {location}"
            raise ValueError(msg)
        return max(
            (
                compare_values(a, b, location=f"{location}[{i}]")
                for i, (a, b) in enumerate(zip(expected, actual, strict=True))
            ),
            default=0,
        )
    else:
        same = type(cast("object", expected)) is type(actual) and expected == actual
    if not same:
        msg = f"Scientific identity/value mismatch at {location}"
        raise ValueError(msg)
    return 0


def compare_table(expected: Path, actual: Path) -> Report:
    """Compare all table identities and finite numeric cells at an absolute tolerance."""
    with expected.open(encoding="utf-8", newline="") as stream:
        first = list(csv.reader(stream))
    with actual.open(encoding="utf-8", newline="") as stream:
        second = list(csv.reader(stream))
    if not first or not second or first[0] != second[0] or len(first) != len(second):
        msg = f"Table schema/row count mismatch: {expected.name}"
        raise ValueError(msg)
    maximum = 0.0
    for left, right in zip(first[1:], second[1:], strict=True):
        if len(left) != len(first[0]) or len(right) != len(first[0]):
            msg = "Malformed table row"
            raise ValueError(msg)
        for column, a, b in zip(first[0], left, right, strict=True):
            if column in IDENTITY_COLUMNS:
                compare_values(a, b, location=expected.name)
                continue
            try:
                x, y = float(a), float(b)
            except ValueError:
                compare_values(a, b, location=expected.name)
            else:
                maximum = max(maximum, compare_values(x, y, location=expected.name))
    return {"table": expected.name, "rows": len(first) - 1, "maximum_absolute_difference": maximum}


def compare_run(expected: Path, actual: Path) -> Report:
    """Verify new output hashes and all primary/nested scientific tables and reports."""
    manifest = read(actual / "manifest.json")
    for name, sha in manifest["outputs"].items():
        if digest(actual / name) != sha:
            msg = f"Regenerated output hash mismatch: {name}"
            raise ValueError(msg)
    if {p.relative_to(expected) for p in expected.rglob("*.csv")} != {
        p.relative_to(actual) for p in actual.rglob("*.csv")
    }:
        msg = "Regenerated table inventory differs"
        raise ValueError(msg)
    rows = [
        dict(compare_table(p, actual / p.relative_to(expected)), path=p.relative_to(expected).as_posix())
        for p in sorted(expected.rglob("*.csv"))
    ]
    deltas = [
        compare_values(read(p), read(actual / p.relative_to(expected))) for p in expected.rglob("report.json")
    ]
    return {"tables": rows, "maximum_report_difference": max(deltas, default=0)}


def command(args: list[str], *, cwd: Path, env: dict[str, str], log: Path) -> None:
    """Run one owned child with a retained command/output log and no retry."""
    with log.open("w", encoding="utf-8") as stream:
        stream.write(json.dumps(args) + "\n")
        stream.flush()
        subprocess.run(args, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, check=True)  # noqa: S603 -- Fixed repository commands, explicit interpreter and source snapshot.


def run(root: Path, out: Path) -> Report:
    """Extract committed sources, verify import isolation and replay without source downloads."""
    if platform.python_version() != "3.15.1":
        msg = "Publication replay requires actual Python 3.15.1"
        raise RuntimeError(msg)
    if out.exists() and any(out.iterdir()):
        msg = "Use a new output directory"
        raise FileExistsError(msg)
    git = shutil.which("git")
    if git is None:
        msg = "Git executable is required for committed source isolation"
        raise RuntimeError(msg)
    dirty = subprocess.check_output(  # noqa: S603 -- Resolved Git executable and fixed local read-only arguments.
        [git, "status", "--porcelain", "--untracked-files=no"], cwd=root, text=True
    )
    if dirty.strip():
        msg = "Commit tracked changes before a clean-source publication replay"
        raise ValueError(msg)
    commit = subprocess.check_output([git, "rev-parse", "HEAD"], cwd=root, text=True).strip()  # noqa: S603 -- Fixed local Git query.
    out.mkdir(parents=True, exist_ok=True)
    out = out.resolve()
    archive = out / "source.tar"
    with archive.open("wb") as stream:
        subprocess.run([git, "archive", "HEAD"], cwd=root, stdout=stream, check=True)  # noqa: S603 -- Fixed committed source archive.
    source = out / "source"
    source.mkdir()
    with tarfile.open(archive) as stream:
        stream.extractall(source, filter="data")
    if (source / ".git").exists() or (source / ".nox").exists() or (source / "outputs").exists():
        msg = "Source archive unexpectedly contains checkout/runtime artifacts"
        raise ValueError(msg)
    env = dict(
        os.environ,
        PYTHONPATH=str(source / "src"),
        PYTHONDONTWRITEBYTECODE="1",
        MPLBACKEND="Agg",
        OPENBLAS_NUM_THREADS="1",
    )
    imported = subprocess.check_output(
        [sys.executable, "-c", "import tobac;print(tobac.__file__)"], cwd=source, env=env, text=True
    ).strip()
    if not Path(imported).is_relative_to(source):
        msg = "Publication replay imported outside the committed source snapshot"
        raise ValueError(msg)
    comparisons: dict[str, Report] = {}
    for reference, name, script, extra in EXPECTED_CHECKS:
        destination = out / name
        command(
            [sys.executable, script, "--out", str(destination), *extra],
            cwd=source,
            env=env,
            log=out / f"{name}.log",
        )
        command(
            [sys.executable, "scripts/verify.py", str(destination)],
            cwd=source,
            env=env,
            log=out / f"{name}-verify.log",
        )
        comparisons[name] = compare_run(source / reference, destination)
    report: Report = {
        "passed": True,
        "source_commit": commit,
        "source_archive_sha256": digest(archive),
        "python": platform.python_version(),
        "interpreter": sys.executable,
        "imported_source": imported,
        "absolute_tolerance": TOLERANCE,
        "comparisons": comparisons,
        "scope": (
            "Fresh committed sources; no source-download command during replay. "
            "Reuses qualified dependencies; not a fresh/offline install or OS network isolation."
        ),
        "no_requests_or_submissions": True,
    }
    (out / "receipt.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return report


def main() -> None:
    """Run clean-source publication reproduction under the calling process-group budget."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(ROOT, args.out), indent=2, allow_nan=False))  # noqa: T201 -- Structured CLI receipt.


if __name__ == "__main__":
    main()
