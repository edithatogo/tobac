"""Analytical admission rejects stale inputs and never leaves a success receipt."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import context_bundle  # noqa: E402 -- Load the verifier from this checkout.


def stage():
    spec = importlib.util.spec_from_file_location(
        "verify_context_stage", ROOT / "scripts/verify_context_stage.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bundle(tmp_path):
    config = {
        "schema_version": 1,
        "profile": "stage-test",
        "max_bytes": 80000,
        "paths": ["AGENTS.md"],
        "base_commit": None,
    }
    manifest, text = context_bundle.build(ROOT, config)
    folder = tmp_path / "bundle"
    folder.mkdir()
    (folder / "manifest.json").write_text(json.dumps(manifest))
    (folder / "context.md").write_text(text)
    return folder


def test_success_failure_and_recovery(tmp_path):
    module = stage()
    folder = bundle(tmp_path)
    receipt, log = tmp_path / "verified.json", tmp_path / "events.jsonl"
    module.execute(folder, receipt, log)
    assert json.loads(receipt.read_text())["status"] == "passed"
    original = (folder / "context.md").read_text()
    (folder / "context.md").write_text("corrupt")
    with pytest.raises(ValueError, match="context text changed"):
        module.execute(folder, receipt, log)
    assert not receipt.exists()
    (folder / "context.md").write_text(original)
    module.execute(folder, receipt, log)
    assert [json.loads(line)["status"] for line in log.read_text().splitlines()] == [
        "passed",
        "failed",
        "passed",
    ]


def test_changed_source_fingerprint_rejected(tmp_path):
    folder = bundle(tmp_path)
    manifest = json.loads((folder / "manifest.json").read_text())
    manifest["files"][0]["sha256"] = "0" * 64
    (folder / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="content changed"):
        stage().execute(folder, tmp_path / "receipt.json", tmp_path / "events.jsonl")
    assert not (tmp_path / "receipt.json").exists()


def test_empty_source_inventory_rejected(tmp_path):
    folder = bundle(tmp_path)
    manifest = json.loads((folder / "manifest.json").read_text())
    manifest["files"] = []
    (folder / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="nonempty source inventory"):
        stage().inspect_bundle(folder)


def test_log_must_not_overwrite_bundle(tmp_path):
    folder = bundle(tmp_path)
    original = (folder / "context.md").read_bytes()
    with pytest.raises(ValueError, match="overwrite"):
        stage().execute(folder, tmp_path / "receipt.json", folder / "context.md")
    assert (folder / "context.md").read_bytes() == original


def test_admission_read_error_removes_stale_success(tmp_path):
    """A simulated filesystem error cannot leave a successful stage receipt."""
    from unittest.mock import patch  # noqa: PLC0415 -- Standard-library fault injection at the I/O boundary.

    module = stage()
    folder = bundle(tmp_path)
    receipt, log = tmp_path / "verified.json", tmp_path / "events.jsonl"
    receipt.write_text('{"status":"passed"}')
    with patch.object(
        module, "inspect_bundle", autospec=True, side_effect=PermissionError("fixture")
    ) as read:
        with pytest.raises(PermissionError, match="fixture"):
            module.execute(folder, receipt, log)
        read.assert_called_once_with(folder)
    assert not receipt.exists()
    assert json.loads(log.read_text())["status"] == "failed"
