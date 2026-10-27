"""Regression tests for runner."""

import csv
import hashlib
import json
import shutil
from pathlib import Path

import numpy as np

import tobac.run as runner
from tobac.information import evaluate
from tobac.regulation import (
    build_states,
    load_config,
    make_problem,
    policy_components,
    studies,
    study_channels,
)

ROOT = Path(__file__).parents[1]


def test_installed_runner_records_executed_sources(tmp_path, monkeypatch) -> None:
    project = tmp_path / "project"
    (project / "configs").mkdir(parents=True)
    shutil.copy(ROOT / "configs/regulatory.json", project / "configs/regulatory.json")
    installed = tmp_path / "venv/lib/python/site-packages/tobac"
    shutil.copytree(ROOT / "src/tobac", installed, ignore=shutil.ignore_patterns("__pycache__"))
    monkeypatch.setattr(runner, "__file__", str(installed / "run.py"))
    monkeypatch.chdir(project)
    runner.run("configs/regulatory.json", "outputs/check", quick=True)
    manifest = json.loads((project / "outputs/check/manifest.json").read_text())
    assert "configs/regulatory.json" in manifest["inputs"]
    assert (
        manifest["inputs"]["src/tobac/information.py"]
        == hashlib.sha256((installed / "information.py").read_bytes()).hexdigest()
    )


def test_runner_uses_configured_resolution_confidence(tmp_path, monkeypatch) -> None:
    (tmp_path / "configs").mkdir()
    c = load_config(ROOT / "configs/regulatory.json")
    c["scientific_event"]["confidence"] = 0.75
    path = tmp_path / "configs/regulatory.json"
    path.write_text(json.dumps(c))
    monkeypatch.chdir(tmp_path)
    runner.run(path, "outputs/check", quick=True)
    s, p = build_states(c)
    d = policy_components(s, c)
    event = (d["illicit"][:, 1] - d["illicit"][:, 0]) / s["tobacco"] >= 0.05
    expected = evaluate(
        make_problem(s, p, c),
        studies(study_channels(s, c))["causal_policy_study"],
        event=event,
        confidence=0.75,
    )
    with (tmp_path / "outputs/check/study_value.csv").open() as f:
        actual = next(row for row in csv.DictReader(f) if row["design"] == "causal_policy_study")
    assert np.isclose(float(actual["resolution_probability"]), expected["resolution_probability"])
