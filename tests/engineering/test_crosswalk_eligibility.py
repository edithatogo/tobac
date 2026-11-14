"""Check that candidate crosswalks preserve evidence and source boundaries."""

import ast
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "crosswalk_eligibility", ROOT / "scripts/crosswalk_eligibility.py"
)


def module():
    assert SPEC
    assert SPEC.loader
    result = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(result)
    return result


def test_existing_dispositions_do_not_admit_observations() -> None:
    crosswalk = module()
    rows = crosswalk.build_crosswalk(crosswalk.load_matrix(crosswalk.MATRIX))
    assert len(rows) == 41
    assert any(row["disposition"] == "adopted" for row in rows)
    assert all(row["empirical_admission"] is False for row in rows)
    assert crosswalk.eligibility_for("unrecognised") == "eligibility_undetermined"
    assert crosswalk.code_element_for({"object_type": "unknown", "object_id": "unknown"}) is None


def test_mapped_code_locations_exist() -> None:
    crosswalk = module()
    rows = crosswalk.build_crosswalk(crosswalk.load_matrix(crosswalk.MATRIX))
    for row in rows:
        location = row["code_element"]
        if location is None:
            continue
        name, separator, member = location.partition("::")
        source = ROOT / name
        assert source.is_file(), location
        if separator:
            nodes = ast.walk(ast.parse(source.read_text(encoding="utf-8")))
            definitions = {node.name for node in nodes if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
            assert member in definitions, location


def test_selected_matrix_identity_is_written(tmp_path: Path) -> None:
    crosswalk = module()
    selected = tmp_path / "selected.csv"
    selected.write_bytes(crosswalk.MATRIX.read_bytes())
    output = tmp_path / "crosswalk.json"
    crosswalk.write_crosswalk(output, crosswalk.build_crosswalk(crosswalk.load_matrix(selected)), selected)
    record = json.loads(output.read_text(encoding="utf-8"))
    assert record["matrix_source"] == selected.name
    assert record["matrix_sha256"] == hashlib.sha256(selected.read_bytes()).hexdigest()
