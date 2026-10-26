"""Golden-file drift check for the checked-in longitudinal result tables.

The two runners write fresh tables into their own run directories. This module
compares the four numeric result tables they produce against the snapshot
committed under ``results/longitudinal``. It is a drift check, not scientific
validation: a pass says the shipped tables still describe what the shipped code
produces within a declared numerical tolerance. A pass does not mean the model,
its assumptions, its scope or any downstream inference is correct, and a failure
does not by itself mean the code is wrong.

The run manifests are deliberately not compared: commit, command, timestamps,
paths and file hashes legitimately vary between runs. Only the substantive
numbers are checked, and only the four modules listed in ``MODULES``.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT / "results/longitudinal"

# Shared by the CLI, the workflow and the tests so the comparison target cannot
# drift between them. Floats and numeric CSV cells use these; JSON integers and
# every non-numeric value are compared exactly.
RTOL = 1e-9
ATOL = 1e-12

# (group under results_dir and the run directory, file name, reader)
MODULES = (
    ("empirical", "latent_ratio_summary.csv", "csv"),
    ("empirical", "source_audit.json", "json"),
    ("releases", "forecast_summary.csv", "csv"),
    ("releases", "predictive_scores.csv", "csv"),
)


def _read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    """Return the header and data rows, rejecting ragged or empty tables.

    Raises:
      ValueError: If the file has no header row or a data row whose field count
        differs from the header.

    """
    rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8"))))
    if not rows:
        msg = "file contains no header row"
        raise ValueError(msg)
    header, body = rows[0], rows[1:]
    for index, row in enumerate(body):
        if len(row) != len(header):
            msg = f"data row {index} has {len(row)} field(s); the header declares {len(header)}"
            raise ValueError(msg)
    return header, body


def _is_numeric_column(*columns: list[str]) -> bool:
    """Check that every non-empty cell parses as a float.

    An empty cell is the pandas CSV spelling of NaN, so it does not by itself
    make a column non-numeric.
    """
    for column in columns:
        for text in column:
            if text == "":
                continue
            try:
                float(text)
            except ValueError:
                return False
    return True


def _as_float(text: str) -> float:
    """Parse a cell already known to be numeric; an empty cell is NaN."""
    return math.nan if text == "" else float(text)


def _cell_difference(expected: str, actual: str) -> tuple[bool, str, float]:
    """Compare one numeric cell.

    Returns:
      (matches, printed difference, sortable magnitude). A NaN matches only a
      NaN; any other non-finite pairing matches only the identical value.

    """
    left, right = _as_float(expected), _as_float(actual)
    if math.isnan(left) or math.isnan(right):
        if math.isnan(left) and math.isnan(right):
            return True, "0", 0.0
        return False, "not comparable (NaN versus a number)", math.inf
    if math.isinf(left) or math.isinf(right):
        if left == right:
            return True, "0", 0.0
        return False, "not comparable (infinite value)", math.inf
    difference = abs(right - left)
    matches = math.isclose(right, left, rel_tol=RTOL, abs_tol=ATOL)
    return matches, f"{difference:.12g}", difference


def _compare_csv(label: str, expected_path: Path, actual_path: Path, errors: list[str]) -> None:  # noqa: C901, PLR0912  # Keep ordered model validation and report assembly in one visible operation.; Keep explicit fail-closed validation branches together.
    """Compare two CSV tables, reporting only the worst failing cell."""
    expected_header, expected_rows = _read_csv(expected_path)
    actual_header, actual_rows = _read_csv(actual_path)
    if expected_header != actual_header:
        missing = [name for name in expected_header if name not in actual_header]
        added = [name for name in actual_header if name not in expected_header]
        if missing or added:
            detail: list[str] = []
            if missing:
                detail.append("missing column(s) " + ", ".join(repr(name) for name in missing))
            if added:
                detail.append("unexpected column(s) " + ", ".join(repr(name) for name in added))
            errors.append(f"{label}: column header differs; " + "; ".join(detail))
        else:
            errors.append(
                f"{label}: column names are identical but their order changed; "
                "the checked-in column order is part of the contract"
            )
        return
    if len(expected_rows) != len(actual_rows):
        errors.append(
            f"{label}: row count differs; checked-in has {len(expected_rows)} "
            f"data row(s) and the run has {len(actual_rows)}"
        )
        return
    expected_columns = [[row[column] for row in expected_rows] for column in range(len(expected_header))]
    actual_columns = [[row[column] for row in actual_rows] for column in range(len(actual_header))]
    numeric = [
        _is_numeric_column(left, right) for left, right in zip(expected_columns, actual_columns, strict=True)
    ]
    failures = 0
    worst: tuple[float, str, int, str, str, str] | None = None
    for index, (expected_row, actual_row) in enumerate(zip(expected_rows, actual_rows, strict=True)):
        for column, (expected_cell, actual_cell) in enumerate(zip(expected_row, actual_row, strict=True)):
            name = expected_header[column]
            if numeric[column]:
                matches, difference, magnitude = _cell_difference(expected_cell, actual_cell)
            else:
                matches = expected_cell == actual_cell
                difference = "values are not numerically comparable"
                magnitude = math.inf if not matches else 0.0
            if not matches:
                failures += 1
                if worst is None or magnitude > worst[0]:
                    worst = (magnitude, name, index, expected_cell, actual_cell, difference)
    if worst is not None:
        _, name, index, expected_cell, actual_cell, difference = worst
        errors.append(
            f"{label}: {failures} cell(s) differ beyond rtol={RTOL:g}, atol={ATOL:g}; worst is "
            f"column {name!r} at data row {index} (0-based): checked-in {expected_cell!r}, "
            f"run {actual_cell!r}, difference {difference}"
        )


def _kind(value: object) -> str:  # noqa: PLR0911  # Return a precise failure receipt at each validation boundary.
    """Return a JSON type name for error messages; bool is not reported as int."""
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if value is None:
        return "null"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    return type(value).__name__


def _child(path: str, key: object) -> str:
    """Extend a JSON path with an object key or an array index."""
    if isinstance(key, int):
        return f"{path}[{key}]"
    return f"{path}.{key}"


def _compare_json_value(label: str, path: str, expected: object, actual: object, errors: list[str]) -> None:  # noqa: C901, PLR0911, PLR0912  # Keep ordered model validation and report assembly in one visible operation.; Return a precise failure receipt at each validation boundary.; Keep explicit fail-closed validation branches together.
    """Recursively compare two decoded JSON values, naming every divergent path."""
    if isinstance(expected, dict) or isinstance(actual, dict):
        if not isinstance(expected, dict) or not isinstance(actual, dict):
            errors.append(
                f"{label}: type changed at {path}; checked-in is "
                f"{_kind(cast('object', expected))}, run is {_kind(cast('object', actual))}"
            )
            return
        expected = cast("dict[str, Any]", expected)
        actual = cast("dict[str, Any]", actual)
        missing = sorted(set(expected) - set(actual))
        added = sorted(set(actual) - set(expected))
        errors.extend(
            f"{label}: missing key {key!r} at {_child(path, key)}; the run must emit every checked-in key"
            for key in missing
        )
        errors.extend(
            (
                f"{label}: added key {key!r} at {_child(path, key)}; the checked-in "
                f"results must be regenerated deliberately"
            )
            for key in added
        )
        for key in sorted(set(expected) & set(actual)):
            _compare_json_value(label, _child(path, key), expected[key], actual[key], errors)
        return
    if isinstance(expected, list) or isinstance(actual, list):
        if not isinstance(expected, list) or not isinstance(actual, list):
            errors.append(
                f"{label}: type changed at {path}; checked-in is "
                f"{_kind(cast('object', expected))}, run is {_kind(cast('object', actual))}"
            )
            return
        expected = cast("list[Any]", expected)
        actual = cast("list[Any]", actual)
        if len(expected) != len(actual):
            errors.append(
                f"{label}: list length differs at {path}; checked-in has "
                f"{len(expected)} item(s), run has {len(actual)}"
            )
        for index in range(min(len(expected), len(actual))):
            _compare_json_value(label, _child(path, index), expected[index], actual[index], errors)
        return
    if isinstance(expected, bool) or isinstance(actual, bool):
        if isinstance(expected, bool) and isinstance(actual, bool) and expected is actual:
            return
        errors.append(
            f"{label}: value differs at {path}; checked-in {expected!r} "
            f"({_kind(cast('object', expected))}), run {actual!r} ({_kind(cast('object', actual))})"
        )
        return
    if isinstance(expected, int) and isinstance(actual, int):
        if expected != actual:
            errors.append(
                f"{label}: integer differs at {path}; checked-in {expected}, "
                f"run {actual}, difference {actual - expected}"
            )
        return
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        left, right = float(expected), float(actual)
        if math.isnan(left) or math.isnan(right) or math.isinf(left) or math.isinf(right):
            if left == right or (math.isnan(left) and math.isnan(right)):
                return
            errors.append(
                f"{label}: non-finite value differs at {path}; checked-in {expected!r}, run {actual!r}"
            )
            return
        if not math.isclose(right, left, rel_tol=RTOL, abs_tol=ATOL):
            errors.append(
                f"{label}: number differs at {path}; checked-in {expected!r}, "
                f"run {actual!r}, difference {abs(right - left):.12g}, "
                f"beyond rtol={RTOL:g}, atol={ATOL:g}"
            )
        return
    if type(expected) is not type(actual):
        errors.append(
            f"{label}: type changed at {path}; checked-in is {_kind(expected)} "
            f"({expected!r}), run is {_kind(actual)} ({actual!r})"
        )
        return
    if expected != actual:
        errors.append(f"{label}: value differs at {path}; checked-in {expected!r}, run {actual!r}")


def _compare_json(label: str, expected_path: Path, actual_path: Path, errors: list[str]) -> None:
    """Compare two JSON documents structurally from the root."""
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    actual = json.loads(actual_path.read_text(encoding="utf-8"))
    _compare_json_value(label, "$", expected, actual, errors)


def _compare_module(
    label: str,
    expected_path: Path,
    actual_path: Path,
    kind: str,
    errors: list[str],
) -> bool:
    """Compare one module; return True when both sides were read and compared."""
    errors.extend(
        (
            f"Missing {label} in the {side}: {path}"
            for path, side in ((expected_path, "checked-in results"), (actual_path, "run directory"))
            if not path.is_file()
        )
    )
    if not expected_path.is_file() or not actual_path.is_file():
        return False
    try:
        if kind == "csv":
            _compare_csv(label, expected_path, actual_path, errors)
        else:
            _compare_json(label, expected_path, actual_path, errors)
    except Exception as exc:  # noqa: BLE001 - a malformed table is a reported failure
        errors.append(f"{label}: could not be read or compared ({type(exc).__name__}): {exc}")
        return False
    return True


def compare(
    empirical_dir: Path | str,
    releases_dir: Path | str,
    results_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Compare a fresh run against the checked-in longitudinal results.

    Args:
      empirical_dir: Run directory holding ``latent_ratio_summary.csv`` and
        ``source_audit.json``.
      releases_dir: Run directory holding ``forecast_summary.csv`` and
        ``predictive_scores.csv``.
      results_dir: Checked-in snapshot holding ``empirical/`` and ``releases/``.
        Defaults to ``<repo_root>/results/longitudinal``.

    Returns:
      ``{'status', 'compared', 'errors', 'tolerance'}``. ``status`` is ``'pass'``
      only when every module was read and every value matched. ``compared``
      lists the modules that were actually read from both sides. CSV row
      indices in ``errors`` are 0-based data rows and exclude the header.

    Raises:
      Nothing for missing or malformed input; those are reported as errors so an
      absent table can never read as agreement.

    """
    results = DEFAULT_RESULTS if results_dir is None else Path(results_dir)
    run_dirs = {"empirical": Path(empirical_dir), "releases": Path(releases_dir)}
    errors: list[str] = []
    compared: list[str] = []

    if not results.is_dir():
        errors.append(
            f"Missing results directory {results}; pass --results pointing at a "
            "directory that holds empirical/ and releases/"
        )
        return {
            "status": "fail",
            "compared": compared,
            "errors": errors,
            "tolerance": {"rtol": RTOL, "atol": ATOL},
        }
    errors.extend(
        (
            f"Missing {group}/ in the results directory {results}; the "
            f"checked-in snapshot must contain both empirical/ and releases/"
        )
        for group in run_dirs
        if not (results / group).is_dir()
    )

    for group, name, kind in MODULES:
        label = f"{group}/{name}"
        if not (results / group).is_dir():
            continue
        if _compare_module(label, results / group / name, run_dirs[group] / name, kind, errors):
            compared.append(label)

    return {
        "status": "fail" if errors else "pass",
        "compared": compared,
        "errors": errors,
        "tolerance": {"rtol": RTOL, "atol": ATOL},
    }


def main() -> None:
    """Run the drift check from the command line; exit 1 on any divergence."""
    parser = argparse.ArgumentParser(
        description="Compare regenerated longitudinal tables with the checked-in results."
    )
    parser.add_argument(
        "--empirical",
        type=Path,
        required=True,
        help="run directory holding latent_ratio_summary.csv and source_audit.json",
    )
    parser.add_argument(
        "--releases",
        type=Path,
        required=True,
        help="run directory holding forecast_summary.csv and predictive_scores.csv",
    )
    parser.add_argument(
        "--results", type=Path, default=None, help="checked-in snapshot (default: results/longitudinal)"
    )
    args = parser.parse_args()
    result = compare(args.empirical, args.releases, args.results)
    print(json.dumps(result, indent=2, allow_nan=False))  # noqa: T201  # CLI emits the requested structured result on stdout.
    raise SystemExit(0 if result["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
