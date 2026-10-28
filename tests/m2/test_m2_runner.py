"""Regression tests for m2 runner."""

import json
from pathlib import Path

import pytest

import tobac.m2 as module

ROOT = Path(__file__).parents[2]


def test_m2_quick_runner_and_nonoverwrite(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(ROOT)
    out = tmp_path / "run"
    r = module.run("configs/m2_retail.json", out, quick=True, quit_points=2)
    assert r["passed"]
    assert r["designs"] == 15
    assert (out / "manifest.json").is_file()
    data = json.loads((out / "conditioning_fixtures.json").read_text())
    assert all("NOT an empirical" in row["qualification"] for row in data)
    with pytest.raises(FileExistsError):
        module.run("configs/m2_retail.json", out, quick=True, quit_points=2)


def test_source_shape_cannot_drift_from_record(tmp_path) -> None:

    cfg = json.loads(Path("configs/m2_retail.json").read_text(encoding="utf-8"))
    cfg["source_beta"][0] = 1.0
    changed = Path.cwd() / "configs" / "_invalid_m2_test.json"
    try:
        changed.write_text(json.dumps(cfg))
        with pytest.raises(ValueError, match="Source-prior"):
            module.run(changed, tmp_path / "bad", quick=True)
    finally:
        changed.unlink(missing_ok=True)


def test_m2_uses_configured_scientific_threshold_and_confidence(tmp_path, monkeypatch) -> None:
    original_load = module.load_config
    original_evaluate = module.evaluate

    def changed_config(path):
        c = original_load(path)
        c["scientific_event"] = {"minimum_absolute_growth_fraction": 0.17, "confidence": 0.8}
        return c

    def checked_evaluate(*args, **kwargs):
        if kwargs.get("event") is not None:
            assert kwargs.get("confidence") == 0.8
        return original_evaluate(*args, **kwargs)

    monkeypatch.setattr(module, "load_config", changed_config)
    monkeypatch.setattr(module, "evaluate", checked_evaluate)
    value = module.run("configs/m2_retail.json", tmp_path / "custom", quick=True, quit_points=1)
    assert value["scientific_event"]["minimum_absolute_growth_fraction"] == 0.17
