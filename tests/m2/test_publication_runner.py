"""Exercise source eligibility and the executed conditional publication boundary."""

import csv
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]


@pytest.fixture
def runner(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import run_m2_publication  # noqa: PLC0415 -- Standalone CLI boundary.

    return run_m2_publication


def test_public_source_map_supplies_context_not_observations(runner) -> None:
    audit, rows = runner.source_audit(ROOT, "evidence/m2/public_sources_20261027")
    assert audit["documents"] == 35
    assert audit["extracts"] == 82
    assert audit["conditioned"] is False
    assert len(rows) == 35
    assert all(r["model_use"] == "context_only_not_a_target_likelihood" for r in rows)


def test_rehashed_adoption_or_document_mismatch_is_rejected(runner, tmp_path) -> None:
    folder = tmp_path / "map"
    folder.mkdir()
    for name, text in {
        "source_index.csv": "source_id,document_id,underlying_data_group\ns1,d1,g1\n",
        "source_table.csv": "source_id,target_likelihood_adopted\ns1,false\n",
        "extraction_table.csv": (
            "extraction_id,source_id,document_id,target_input_adopted\ne1,s1,wrong,false\n"
        ),
    }.items():
        (folder / name).write_text(text)
    hashes = {
        str(p.relative_to(tmp_path)): hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir()
    }
    (folder / "manifest.json").write_text(json.dumps({"sha256": hashes}))
    with pytest.raises(ValueError, match="document"):
        runner.source_audit(tmp_path, "map")
    path = folder / "extraction_table.csv"
    path.write_text(path.read_text().replace("wrong,false", "d1,true"))
    hashes[str(path.relative_to(tmp_path))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (folder / "manifest.json").write_text(json.dumps({"sha256": hashes}))
    with pytest.raises(ValueError, match="adoption"):
        runner.source_audit(tmp_path, "map")


def test_full_declared_small_grid_and_refusal_to_overwrite(runner, tmp_path) -> None:
    config = json.loads((ROOT / "configs/m2_publication.json").read_text())
    config.update(crime_weights=[0, 1], resource_weights=[0, 1])
    # Config is deliberately external here; controlled scientific paths remain repo-relative.
    out = tmp_path / "new"
    report = runner.run(ROOT, out, specification=config, quit_points=1)
    assert report["passed"]
    assert report["decision_rows"] == 20
    assert report["study_rows"] == 120
    assert report["conditioned"] is False
    assert report["empirically_validated"] is False
    rows = list(csv.DictReader((out / "decisions.csv").open()))
    assert all(r["cooptimal_actions"] for r in rows)
    with pytest.raises(FileExistsError, match="new output"):
        runner.run(ROOT, out, specification=config, quit_points=1)


def test_unsorted_value_support_cannot_supply_box_claim(runner, tmp_path) -> None:
    config = json.loads((ROOT / "configs/m2_publication.json").read_text())
    config["crime_weights"] = [1, 0]
    with pytest.raises(ValueError, match="increasing"):
        runner.run(ROOT, tmp_path / "invalid", specification=config, quit_points=1)


def test_resolution_diagnostic_checks_keys_hashes_and_fixed_inputs(runner, tmp_path) -> None:
    paths = [tmp_path / "a", tmp_path / "b"]
    for i, path in enumerate(paths):
        path.mkdir()
        (path / "report.json").write_text(json.dumps({"specification": {"quit_points": i + 2, "fixed": 1}}))
        (path / "decisions.csv").write_text(
            "case,crime_weight,resource_weight,cooptimal_actions,evpi\n"
            f"c,1,1,{'a' if i == 0 else 'b'},{1 + i * 0.1}\n"
        )
        (path / "study_value.csv").write_text("case,crime_weight,resource_weight,design,evsi\nc,1,1,none,0\n")
        files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in path.iterdir()}
        (path / "manifest.json").write_text(json.dumps({"outputs": files}))
    result = runner.resolution_comparison(*paths)
    assert result["changed_cooptimal_sets"] == 1
    assert result["maximum_absolute_evpi_difference"] == pytest.approx(0.1)
    with (paths[0] / "decisions.csv").open("a") as stream:
        stream.write("c,1,1,a,1\n")
    with pytest.raises(ValueError, match="hash"):
        runner.resolution_comparison(*paths)
    manifest = json.loads((paths[0] / "manifest.json").read_text())
    manifest["outputs"]["decisions.csv"] = hashlib.sha256(
        (paths[0] / "decisions.csv").read_bytes()
    ).hexdigest()
    (paths[0] / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="unique"):
        runner.resolution_comparison(*paths)
