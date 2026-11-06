"""Scientific orchestration must stop before calculation on admission failure."""

import importlib.util
import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[2]


def load():
    spec = importlib.util.spec_from_file_location("run_m1_stage", ROOT / "scripts/run_m1_stage.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_preflight_failure_never_starts_model_or_publishes(tmp_path, monkeypatch):
    module = load()
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module.sys, "prefix", str(tmp_path / ".venv"))
    out = tmp_path / "outputs" / "model"
    error = subprocess.CalledProcessError(2, ["fixture-preflight"])
    with patch.object(module.subprocess, "run", autospec=True, side_effect=error) as run:
        with pytest.raises(subprocess.CalledProcessError):
            module.execute(out)
        assert run.call_count == 1
        assert "hosted_lineage.py" in str(run.call_args.args[0])
    assert not out.exists()
    assert not list(out.parent.glob("m1-stage-*"))
    assert json.loads((out.parent / "analysis-events.jsonl").read_text())["status"] == "failed"


def test_existing_output_is_never_overwritten(tmp_path):
    module = load()
    with pytest.raises(ValueError, match="new analysis directory"):
        module.execute(tmp_path)
