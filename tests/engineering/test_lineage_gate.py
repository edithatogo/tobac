"""Command gates must fail before qualification, including for structurally valid legacy data."""

import json
import os
import subprocess
import sys
from pathlib import Path

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
