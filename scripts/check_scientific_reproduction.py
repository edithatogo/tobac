"""Compare all eight current runner variants with native-byte-verified numerical references."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import platform
import zipfile
from pathlib import Path
from typing import Any

from check_longitudinal_results import ATOL, RTOL
from hosted_lineage import CHECKPOINT, CHECKPOINT_SHA
from qualify_publication_replay import IDENTITY_COLUMNS, TOLERANCE

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "integration/scientific_reference_20261103.zip"
REFERENCE_CHECKPOINT = "integration/archive/scientific-lineage-checkpoint_20261102.json"
REFERENCE_CHECKPOINT_SHA = "63eaf457ae3ff03fc688f830f24ebb640f01dbbf8dc2e912887c10ec7f6e090a"
RUNS = {
    "m1": "m1",
    "m2_retail": "m2",
    "m2_publication": "m2_publication",
    "m2_robustness": "m2_robustness",
    "m3": "m3",
    "longitudinal": "empirical_longitudinal",
    "release_calibration": "release_calibration",
}
IDENTITIES = IDENTITY_COLUMNS | {
    "year",
    "test_year",
    "train_end_year",
    "latest_year",
    "last_year",
    "first_change_year",
    "model",
    "model_ids",
    "observation_id",
    "path_id",
    "scenario",
    "states",
}


def reference_tables() -> dict[str, dict[str, dict[str, str]]]:
    """Require exactly the accepted runner/table closure and each original output digest."""
    checkpoint = (ROOT / CHECKPOINT).read_bytes()
    if hashlib.sha256(checkpoint).hexdigest() != CHECKPOINT_SHA:
        msg = "Accepted numerical checkpoint changed"
        raise ValueError(msg)
    active = json.loads(checkpoint)["runner_results"]
    original = (ROOT / REFERENCE_CHECKPOINT).read_bytes()
    if hashlib.sha256(original).hexdigest() != REFERENCE_CHECKPOINT_SHA:
        msg = "Original numerical reference checkpoint changed"
        raise ValueError(msg)
    accepted = json.loads(original)["runner_results"]
    with zipfile.ZipFile(REFERENCE) as archive:
        reference = json.loads(archive.read("reference.json"))
    if (
        reference["checkpoint_sha256"] != REFERENCE_CHECKPOINT_SHA
        or set(reference["runners"]) != set(accepted)
        or set(active) != set(accepted)
    ):
        msg = "Reference runner/checkpoint closure changed"
        raise ValueError(msg)
    tables: dict[str, dict[str, dict[str, str]]] = reference["runners"]
    for name, rows in tables.items():
        expected = {p: key for p, key in accepted[name]["artifacts"].items() if p.endswith(".csv")}
        current = {p: key for p, key in active[name]["artifacts"].items() if p.endswith(".csv")}
        if current != expected:
            msg = "Active numerical closure differs from the frozen reference"
            raise ValueError(msg)
        if set(rows) != set(expected):
            msg = "Reference CSV inventory changed"
            raise ValueError(msg)
        for path, record in rows.items():
            actual = "sha256:" + hashlib.sha256(record["utf8"].encode("utf-8")).hexdigest()
            if actual != expected[path] or record["object_id"] != expected[path]:
                msg = "Reference CSV differs from the accepted native bytes"
                raise ValueError(msg)
    return tables


def compare_cell(left: str, right: str, column: str, *, relative: bool) -> float:
    """Keep identifiers/text exact; use the existing runner-family numerical tolerances."""
    if column in IDENTITIES or column.endswith("_id"):
        if left != right:
            msg = f"Scientific identity changed: {column}"
            raise ValueError(msg)
        return 0.0
    try:
        a, b = float(left), float(right)
    except ValueError as exc:
        if left != right:
            msg = f"Scientific text changed: {column}"
            raise ValueError(msg) from exc
        return 0.0
    if not math.isfinite(a) or not math.isfinite(b):
        msg = f"Nonfinite scientific output: {column}"
        raise ValueError(msg)
    same = math.isclose(a, b, rel_tol=RTOL, abs_tol=ATOL) if relative else abs(a - b) <= TOLERANCE
    if not same:
        msg = f"Scientific numerical mismatch: {column}: {a} != {b}"
        raise ValueError(msg)
    return abs(a - b)


def compare_table(text: str, actual: Path, *, relative: bool) -> dict[str, Any]:
    """Require every row/column and retain the maximum observed numerical difference."""
    first = list(csv.reader(io.StringIO(text)))
    with actual.open(encoding="utf-8", newline="") as stream:
        second = list(csv.reader(stream))
    if not first or not second or first[0] != second[0] or len(first) != len(second):
        msg = f"Scientific table schema/row count changed: {actual.name}"
        raise ValueError(msg)
    maximum = 0.0
    for left, right in zip(first[1:], second[1:], strict=True):
        if len(left) != len(first[0]) or len(right) != len(first[0]):
            msg = "Malformed scientific table row"
            raise ValueError(msg)
        for column, a, b in zip(first[0], left, right, strict=True):
            maximum = max(maximum, compare_cell(a, b, column, relative=relative))
    return {"rows": len(first) - 1, "maximum_absolute_difference": maximum}


def verify(replays: Path, no_grid: Path) -> dict[str, Any]:
    """Read exactly one fresh Nox reproduction and the additional accepted no-grid variant."""
    (replay,) = [p for p in replays.iterdir() if p.is_dir()]
    runs = {name: replay / directory for name, directory in RUNS.items()}
    runs["m2"] = no_grid
    reports: dict[str, Any] = {}
    for name, rows in reference_tables().items():
        root = runs[name]
        if {p.relative_to(root).as_posix() for p in root.rglob("*.csv")} != set(rows):
            msg = f"Regenerated CSV inventory differs: {name}"
            raise ValueError(msg)
        relative = name not in {"m2", "m2_publication", "m2_robustness"}
        reports[name] = {
            "tables": {p: compare_table(r["utf8"], root / p, relative=relative) for p, r in rows.items()},
            "tolerance": {"rtol": RTOL, "atol": ATOL} if relative else {"rtol": 0, "atol": TOLERANCE},
        }
    return {
        "schema": "tobac.scientific-reproduction.v1",
        "status": "passed",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "reference_sha256": hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
        "checkpoint_sha256": CHECKPOINT_SHA,
        "reference_checkpoint_sha256": REFERENCE_CHECKPOINT_SHA,
        "runners": reports,
        "scope": (
            "All eight runner variants and 82 CSV tables; existing Nox validators also run; "
            "software reproduction, not empirical validation"
        ),
    }


def main() -> None:
    """Write a new successful report only after all comparisons pass."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replays", type=Path, required=True)
    parser.add_argument("--no-grid", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        msg = "Use a new reproduction report path"
        raise FileExistsError(msg)
    result = verify(args.replays, args.no_grid)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
