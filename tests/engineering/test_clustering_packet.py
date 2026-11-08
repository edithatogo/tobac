"""Byte-bound synthetic packet checks reject stale source and unsafe members."""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
import test_lock_receipts as fixtures

ROOT = Path(__file__).resolve().parents[2]


def module():
    spec = importlib.util.spec_from_file_location(
        "verify_cluster_packet", ROOT / "scripts/verify_sensitivity_clustering.py"
    )
    assert spec
    assert spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def mutate_packet(out: Path, root: Path, manifest: dict, mutation: str) -> None:
    changed_paths = {
        "corrupt": out / "stability.csv",
        "stale_source": root / "scripts/qualify_sensitivity_clustering.py",
        "stale_input": root / "engineering/typings/threadpoolctl.pyi",
        "stale_lock": root / "engineering/clustering.lock",
        "new_type_input": root / "engineering/typings/sklearn/new_module.pyi",
    }
    if mutation in changed_paths:
        changed_paths[mutation].write_text("changed fixture\n", encoding="utf-8")
    elif mutation == "missing":
        (out / "stability.csv").unlink()
    elif mutation == "extra":
        (out / "extra.txt").write_text("unexpected")
    elif mutation == "traversal":
        manifest["files"] = {"../outside.csv": "0" * 64}
    elif mutation == "symlink":
        original = out / "stability.csv"
        target = root / "outside.csv"
        original.rename(target)
        original.symlink_to(target)
    elif mutation == "schema":
        manifest["schema"] = "unknown"
    elif mutation in {"scheduler_marker", "bad_scheduler_marker"}:
        (out / ".snakemake_timestamp").write_text("" if mutation == "scheduler_marker" else "unexpected")


@pytest.mark.parametrize(
    "mutation",
    [
        "none",
        "corrupt",
        "missing",
        "extra",
        "stale_source",
        "stale_input",
        "traversal",
        "symlink",
        "schema",
        "stale_lock",
        "new_type_input",
        "scheduler_marker",
        "bad_scheduler_marker",
    ],
)
def test_packet_contract(tmp_path: Path, mutation: str) -> None:
    verifier = module()
    _, lock = fixtures.fixture(tmp_path, "clustering")
    (tmp_path / "noxfile.py").write_text("# synthetic fixture\n")
    (tmp_path / "workflow").mkdir()
    (tmp_path / "workflow/Snakefile").write_text("# synthetic fixture\n")
    (tmp_path / "engineering/requirements.lock").write_text("# fixture runtime snapshot\n")
    for name in [
        "qualify_sensitivity_clustering",
        "verify_sensitivity_clustering",
        "source_handoff",
        "lock_receipt",
    ]:
        path = tmp_path / f"scripts/{name}.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# synthetic verifier fixture only\n")
    for name in ["__init__", "cluster", "dummy", "linear_model", "metrics", "pipeline", "preprocessing"]:
        path = tmp_path / f"engineering/typings/sklearn/{name}.pyi"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# synthetic fixture only\n")
    (tmp_path / "engineering/typings/threadpoolctl.pyi").write_text("# fixture\n")
    out = tmp_path / "outputs/completed"
    out.mkdir(parents=True)
    (out / "summary.json").write_text(
        json.dumps({"success": True, "source": "synthetic_only", "empirical_qualification": False})
    )
    (out / "stability.csv").write_text("fixture_only\n")
    manifest = {
        "schema": "tobac.synthetic-qualification-packet.v2",
        "formula_version": "synthetic-sensitivity-clustering-v1",
        "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()},
        "script_sha256": hashlib.sha256(
            (tmp_path / "scripts/qualify_sensitivity_clustering.py").read_bytes()
        ).hexdigest(),
        "lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest(),
        "qualification_inputs": verifier.qualification_inputs(tmp_path),
    }
    mutate_packet(out, tmp_path, manifest, mutation)
    (out / "manifest.json").write_text(json.dumps(manifest))
    if mutation in {"none", "scheduler_marker"}:
        assert verifier.verify_packet(tmp_path, out, lock)["empirical_qualification"] is False
    else:
        with pytest.raises(ValueError, match=r"Packet|hash mismatch|stale|Symlink|Unknown|Scheduler"):
            verifier.verify_packet(tmp_path, out, lock)
