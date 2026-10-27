"""Fail-closed checks for the release-calibration integrity verifier."""

import csv
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "forecast_summary.csv",
    "predictive_scores.csv",
    "rolling_predictive_checks.csv",
    "posterior_parameter_summary.csv",
    "source_reconciliation.json",
    "fit_scope.json",
    "grid_convergence.csv",
    "monte_carlo_checks.csv",
]


def load_verifier():
    spec = importlib.util.spec_from_file_location(
        "release_verifier", ROOT / "scripts/verify_release_calibration.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def edit_manifest(run, mutate) -> None:
    path = run / "run_manifest.json"
    manifest = json.loads(path.read_text())
    mutate(manifest)
    path.write_text(json.dumps(manifest, indent=2))


def rehash_artifact(run, name) -> None:
    """Update the manifest digest so a data check, not the hash, is exercised."""
    digest = hashlib.sha256((run / name).read_bytes()).hexdigest()

    def mutate(manifest) -> None:
        for item in manifest["files"]:
            if item["path"] == name:
                item["sha256"] = digest

    edit_manifest(run, mutate)


def edit_csv(run, name, mutate) -> None:
    """Rewrite one output CSV and its manifest digest."""
    path = run / name
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        rows = list(reader)
    mutate(rows)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    rehash_artifact(run, name)


@pytest.fixture(scope="module")
def calibration_run(tmp_path_factory):
    """One real CLI run; every test copies it before mutating."""
    target = tmp_path_factory.mktemp("verify_run") / "run"
    cmd = [
        sys.executable,
        str(ROOT / "scripts/run_release_calibration.py"),
        "--out",
        str(target),
        "--skip-figures",
        "--quick",
        "--draws",
        "32",
    ]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)  # noqa: S603 -- Fixed test/qualification argv and local fixture paths; no shell.
    assert result.returncode == 0, result.stderr
    return target


@pytest.fixture
def run_copy(calibration_run, tmp_path):
    copy = tmp_path / "run"
    shutil.copytree(calibration_run, copy)
    return copy


def test_complete_run_passes(calibration_run) -> None:
    result = load_verifier().verify(calibration_run)
    assert result["status"] == "pass", result["errors"]
    assert result["errors"] == []
    assert result["required_artifacts"] == len(REQUIRED)


def test_required_artifact_missing_from_disk_and_manifest_names_the_artifact(run_copy) -> None:
    (run_copy / "rolling_predictive_checks.csv").unlink()
    edit_manifest(
        run_copy,
        lambda m: m.__setitem__(
            "files", [f for f in m["files"] if f["path"] != "rolling_predictive_checks.csv"]
        ),
    )
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("rolling_predictive_checks.csv" in e for e in result["errors"])


def test_tampered_artifact_reports_hash_mismatch(run_copy) -> None:
    target = run_copy / "forecast_summary.csv"
    target.write_text(target.read_text() + "tampered\n")
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("Hash mismatch" in e and "forecast_summary.csv" in e for e in result["errors"])


def test_manifest_without_provenance_fails(run_copy) -> None:
    def drop(manifest) -> None:
        del manifest["commit"]
        del manifest["command"]

    edit_manifest(run_copy, drop)
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("'commit'" in e for e in result["errors"])
    assert any("'command'" in e for e in result["errors"])


def test_manifest_path_escaping_the_root_fails(run_copy) -> None:
    (run_copy.parent / "escape.csv").write_text("outside\n")
    edit_manifest(run_copy, lambda m: m["files"].append({"path": "../escape.csv", "sha256": "0" * 64}))
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("../escape.csv" in e for e in result["errors"])


def test_missing_manifest_fails_instead_of_raising(tmp_path) -> None:
    empty = tmp_path / "no_manifest"
    empty.mkdir()
    result = load_verifier().verify(empty)
    assert result["status"] == "fail"
    assert result["errors"]
    assert "run_manifest.json" in result["errors"][0]


def test_fit_scope_funding_flag_is_checked(run_copy) -> None:
    path = run_copy / "fit_scope.json"
    scope = json.loads(path.read_text())
    scope["funding_recommendation"] = True
    path.write_text(json.dumps(scope, indent=2))
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("fit_scope" in e and "funding" in e for e in result["errors"])


def test_missing_grid_convergence_fails(run_copy) -> None:
    (run_copy / "grid_convergence.csv").unlink()
    edit_manifest(
        run_copy,
        lambda m: m.__setitem__("files", [f for f in m["files"] if f["path"] != "grid_convergence.csv"]),
    )
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("grid_convergence.csv" in e for e in result["errors"])


def test_missing_monte_carlo_checks_fails(run_copy) -> None:
    (run_copy / "monte_carlo_checks.csv").unlink()
    edit_manifest(
        run_copy,
        lambda m: m.__setitem__("files", [f for f in m["files"] if f["path"] != "monte_carlo_checks.csv"]),
    )
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("monte_carlo_checks.csv" in e for e in result["errors"])


def test_nonconverged_grid_names_model_horizon_and_measure(run_copy) -> None:
    def mutate(rows) -> None:
        row = next(
            r for r in rows if r["model"] == "all_changes" and r["horizon"] == "1" and r["measure"] == "mean"
        )
        row["relative_difference"] = "1.0"

    edit_csv(run_copy, "grid_convergence.csv", mutate)
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    message = next(e for e in result["errors"] if "relative_difference" in e and "exceeds" in e)
    assert "grid_convergence.csv" in message
    assert "model='all_changes'" in message
    assert "horizon=1" in message
    assert "measure='mean'" in message


def test_dropped_grid_row_fails_the_row_count(run_copy) -> None:
    edit_csv(run_copy, "grid_convergence.csv", lambda rows: rows.pop())
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("grid_convergence.csv" in e and "rows; expected" in e for e in result["errors"])


def test_monte_carlo_mean_beyond_sigma_tolerance_fails(run_copy) -> None:
    def mutate(rows) -> None:
        row = rows[0]
        row["simulation_mean"] = str(float(row["analytic_mean"]) - 100 * float(row["mcse_mean"]))

    edit_csv(run_copy, "monte_carlo_checks.csv", mutate)
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    message = next(e for e in result["errors"] if "MCSE" in e)
    assert "analytic_mean=" in message
    assert "simulation_mean=" in message
    assert "mcse_mean=" in message
    assert "100.0" in message
    with (run_copy / "monte_carlo_checks.csv").open(newline="") as handle:
        row = next(csv.DictReader(handle))
    assert f"model={row['model']!r}" in message
    assert f"year={int(row['year'])}" in message


def test_zero_monte_carlo_mcse_fails(run_copy) -> None:
    edit_csv(run_copy, "monte_carlo_checks.csv", lambda rows: rows[0].__setitem__("mcse_mean", "0"))
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("mcse_mean" in e and "> 0" in e for e in result["errors"])


def test_non_finite_monte_carlo_value_fails(run_copy) -> None:
    edit_csv(run_copy, "monte_carlo_checks.csv", lambda rows: rows[0].__setitem__("simulation_mean", "nan"))
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("simulation_mean" in e and "not finite" in e for e in result["errors"])


def test_non_finite_grid_difference_fails(run_copy) -> None:
    edit_csv(run_copy, "grid_convergence.csv", lambda rows: rows[0].__setitem__("relative_difference", "inf"))
    result = load_verifier().verify(run_copy)
    assert result["status"] == "fail"
    assert any("relative_difference" in e and "not finite" in e for e in result["errors"])
