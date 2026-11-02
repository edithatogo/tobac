"""Command gates must fail before qualification, including for structurally valid legacy data."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_inventory_gate_preserves_missing_evidence_failure(tmp_path: Path) -> None:
    output = tmp_path / "result.json"
    env = {key: value for key, value in os.environ.items() if not key.startswith("TOBAC_LINEAGE_")}
    command = [sys.executable, "scripts/qualify_integrations.py", "--mode", "lineage", "--out", str(output)]
    result = subprocess.run(command, cwd=ROOT, env=env, check=False, capture_output=True)  # noqa: S603 -- Fixed local test CLI.
    assert result.returncode != 0
    receipt = json.loads(output.read_bytes())
    assert receipt["success"] is False
    assert "TOBAC_LINEAGE_" in receipt["error"]


def test_legacy_manifest_cannot_be_promoted_through_cli(tmp_path: Path) -> None:
    manifest = tmp_path / "legacy.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "archive-govt-nz.manifest/v1",
                "archive_id": "old",
                "objects": [{"object_id": "legacy"}],
                "observations": [{"observation_id": "old"}],
                "versions": [],
                "receipts": {},
                "context": {},
            }
        )
    )
    command = [sys.executable, "scripts/qualification_check.py", "--manifest", str(manifest)]
    for mode in ("legacy", "exploratory", "qualified"):
        result = subprocess.run([*command, "--mode", mode], cwd=ROOT, capture_output=True, check=False)  # noqa: S603 -- Fixed local test CLI.
        receipt = json.loads(result.stdout)
        assert receipt["qualified"] is False
        assert (result.returncode != 0) == (mode == "qualified")
        assert receipt["execution_mode"] == mode


@pytest.mark.skipif(
    not all(os.environ.get("TOBAC_LINEAGE_" + key) for key in ("ATTEMPTS", "PYTHON", "WHEEL")),
    reason="requires the installed native wheel and private accepted attempts",
)
@pytest.mark.parametrize(
    ("case", "reason"),
    [
        ("missing", "object_missing"),
        ("tampered", "object_corrupt"),
        ("incomplete", "Output inventory differs"),
    ],
)
def test_rejection_precedes_runner_claim(tmp_path: Path, case: str, reason: str) -> None:
    """Exercise the normal scientific CLI using only an isolated copy of an accepted attempt."""
    attempts = tmp_path / "evidence"
    source = Path(os.environ["TOBAC_LINEAGE_ATTEMPTS"]) / "m1"
    folder = attempts / "m1"
    shutil.copytree(source, folder)
    terminal = json.loads((folder / "terminal").read_bytes())
    sha = terminal["result"]["transformation"].removeprefix("sha256:")
    record = folder / "cas" / "sha256" / sha[:2] / sha
    if case == "missing":
        record.unlink()
    elif case == "tampered":
        record.write_bytes(b"{}")
    else:
        next((folder / "outputs").glob("*.csv")).unlink()
    destination = tmp_path / "new-run"
    env = {**os.environ, "TOBAC_LINEAGE_ATTEMPTS": str(attempts), "PYTHONPATH": str(ROOT / "src")}
    command = [
        env["TOBAC_LINEAGE_PYTHON"],
        "scripts/scientific_lineage.py",
        "--run",
        "m1",
        "--out",
        str(destination),
        "--wheel",
        env["TOBAC_LINEAGE_WHEEL"],
        "--store",
        str(tmp_path / "unused"),
    ]
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=120, check=False)  # noqa: S603 -- Qualified native test runtime and fixed scientific CLI.
    assert result.returncode != 0
    assert reason in result.stderr.decode()
    assert not destination.exists()


@pytest.mark.skipif(
    not all(os.environ.get("TOBAC_LINEAGE_" + key) for key in ("ATTEMPTS", "PYTHON", "WHEEL")),
    reason="requires the installed native wheel and private accepted attempts",
)
def test_candidate_cannot_use_its_own_receipt_as_acceptance(tmp_path: Path) -> None:
    """An explicitly requested replacement can be generated before independent approval."""
    store = Path(os.environ["TOBAC_LINEAGE_ATTEMPTS"]) / "m1/cas"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "TOBAC_LINEAGE_ATTEMPTS": str(tmp_path / "absent")}
    command = [
        env["TOBAC_LINEAGE_PYTHON"],
        "scripts/scientific_lineage.py",
        "--candidate",
        "m1",
        "--store",
        str(store),
        "--wheel",
        env["TOBAC_LINEAGE_WHEEL"],
        "--out",
        str(tmp_path / "candidate"),
    ]
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=180, check=False)  # noqa: S603 -- The pinned native interpreter runs the fixed M1 candidate.
    assert result.returncode == 0, result.stderr.decode()
    assert "candidate_unqualified" in result.stdout.decode()
    folder = tmp_path / "candidate/m1"
    ids = json.loads((folder / "terminal").read_bytes())["result"]
    record_sha = ids["receipt"].removeprefix("sha256:")
    record = json.loads((folder / "cas/sha256" / record_sha[:2] / record_sha).read_bytes())
    assert record["execution_mode"] == "candidate_unqualified"
    sha = ids["manifest"].removeprefix("sha256:")
    reject = subprocess.run(  # noqa: S603 -- Check the public manifest CLI with the generated candidate.
        [
            sys.executable,
            "scripts/qualification_check.py",
            "--manifest",
            str(folder / "cas/sha256" / sha[:2] / sha),
        ],
        cwd=ROOT,
        capture_output=True,
        check=False,
        timeout=120,
    )
    assert reject.returncode == 2
    assert "no matching accepted native execution" in reject.stdout.decode()
