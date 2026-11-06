"""Scientific orchestration must stop before calculation on admission failure."""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
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


@pytest.fixture
def snakemake_binary():
    """Select the real scheduler from the optional qualified analytics profile."""
    selected = os.environ.get("TOBAC_SNAKEMAKE") or shutil.which("snakemake")
    if selected is None:
        pytest.skip("Real Snakemake requires the separately qualified analytics profile")
    binary = Path(selected).resolve()
    assert binary.is_file(), "Configured Snakemake executable is missing"
    return str(binary)


def test_scheduler_preserves_atomic_destination_and_completed_outputs(tmp_path, snakemake_binary):
    """Exercise the actual M1 rule with a labelled fixture writer, not native evidence."""
    script = tmp_path / "scripts/run_m1_stage.py"
    script.parent.mkdir()
    script.write_text(
        "import pathlib,sys\n"
        "out=pathlib.Path(sys.argv[-1])\n"
        "assert not out.exists(), 'scheduler precreated atomic destination'\n"
        "out.mkdir(parents=True)\n"
        "(out/'manifest.json').write_text('fixture-only, no native/model acceptance')\n"
        "with pathlib.Path('calls.txt').open('a') as f: f.write('called\\n')\n"
    )
    admission = tmp_path / "outputs/fixture/verified.json"
    admission.parent.mkdir(parents=True)
    admission.write_text('{"fixture":true}')
    config = tmp_path / "configs/regulatory.json"
    config.parent.mkdir()
    config.write_text('{"fixture":true}')
    # Reuse the maintained rule, including its actual output declaration and
    # command. The isolated fixture deliberately has no scientific admission.
    rule = (ROOT / "workflow/Snakefile").read_text().split("\nrule m1:", 1)[1]
    prefix = (
        "from pathlib import Path\n"
        f"PYTHON={str(Path(sys.executable).absolute())!r}\n"
        "OUT='outputs/fixture'\n"
        "rule all:\n    input: OUT+'/m1'\n"
    )
    (tmp_path / "Snakefile").write_text(prefix + "\nrule m1:" + rule)
    command = [snakemake_binary, "--cores", "1", "--scheduler", "greedy"]

    def run():
        return subprocess.run(  # noqa: S603 -- Qualified scheduler, isolated labelled fixture, no shell.
            command, cwd=tmp_path, capture_output=True, text=True, check=False, timeout=60
        )

    first = run()
    assert first.returncode == 0, first.stdout + first.stderr
    manifest = admission.parent / "m1/manifest.json"
    original = manifest.read_bytes()
    assert manifest.stat().st_mode & 0o222 == 0
    cached = run()
    assert cached.returncode == 0, cached.stdout + cached.stderr
    assert (tmp_path / "calls.txt").read_text() == "called\n"
    admission.write_text('{"fixture":"changed input"}')
    refused = run()
    assert refused.returncode != 0
    assert "protected" in refused.stderr.lower()
    assert manifest.read_bytes() == original
    assert (tmp_path / "calls.txt").read_text() == "called\n"


def test_workflow_rejects_outside_destination_before_input_reads(tmp_path, snakemake_binary):
    outside = tmp_path / "outside"
    command = [
        snakemake_binary,
        "--snakefile",
        str(ROOT / "workflow/Snakefile"),
        "--cores",
        "1",
        "--scheduler",
        "greedy",
        "--config",
        "profile=deliberately-missing-profile",
        "bundle=deliberately-missing-bundle",
        f"out={outside}",
        f"python={Path(sys.executable).absolute()}",
    ]
    result = subprocess.run(  # noqa: S603 -- Qualified scheduler and exact owned repository paths, no shell.
        command, cwd=ROOT, capture_output=True, text=True, check=False, timeout=60
    )
    assert result.returncode != 0
    assert "below repository outputs" in result.stderr
    assert not outside.exists()


def test_existing_output_is_never_overwritten(tmp_path, monkeypatch):
    module = load()
    monkeypatch.setattr(module, "ROOT", tmp_path)
    out = tmp_path / "outputs" / "existing"
    out.mkdir(parents=True)
    original = out / "manifest.json"
    original.write_text('{"fixture":"previous verified result"}')
    with pytest.raises(ValueError, match="new analysis directory"):
        module.execute(out)
    assert original.read_text() == '{"fixture":"previous verified result"}'


def test_final_verifier_failure_never_publishes(tmp_path, monkeypatch):
    """Fixture-only subprocess responses test publication, not native/model validity."""
    module = load()
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module.sys, "prefix", str(tmp_path / ".venv"))
    out = tmp_path / "outputs" / "model"
    calls = []

    def fixture_command(command, **_kwargs):
        calls.append(command)
        if "tobac.run" in command:
            staged = Path(command[-1])
            staged.mkdir()
            (staged / "manifest.json").write_text('{"fixture":"not verified"}')
        if str(tmp_path / "scripts/verify.py") in command:
            raise subprocess.CalledProcessError(1, command)

    with (
        patch.object(module.subprocess, "run", autospec=True, side_effect=fixture_command),
        pytest.raises(subprocess.CalledProcessError),
    ):
        module.execute(out)
    assert len(calls) == 3
    assert not out.exists()
    assert not list(out.parent.glob("m1-stage-*"))
    assert json.loads((out.parent / "analysis-events.jsonl").read_text())["status"] == "failed"
