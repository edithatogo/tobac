"""Coverage audit rejects changed bytes and malformed annual inventories."""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("case", ["valid", "changed_bytes", "duplicate_year", "wrong_columns"])
def test_coverage_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, case: str) -> None:
    spec = importlib.util.spec_from_file_location(
        "coverage_audit", ROOT / "scripts/audit_empirical_coverage.py"
    )
    assert spec
    assert spec.loader
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    names = [
        "data/empirical_intake_20261024/nz_historical_legal_supply.csv",
        "data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv",
    ]
    entries = []
    for name in names:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "year,unit,source_id,limitations\n"
            "2020,test/year,synthetic,test only\n2021,test/year,synthetic,test only\n"
        )
        if case == "duplicate_year":
            path.write_text(path.read_text().replace("2021", "2020"))
        entries.append(
            {
                "path": name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "rows": 2,
                "columns": ["year", "unit", "source_id", "limitations"],
                "role": "synthetic_test_only",
            }
        )
    if case == "changed_bytes":
        (tmp_path / names[0]).write_text("changed\n")
    if case == "wrong_columns":
        entries[0]["columns"] = ["unrelated_column"]
    inventory = tmp_path / "integration/archive/consumer-inputs.json"
    inventory.parent.mkdir(parents=True)
    inventory.write_text(json.dumps({"inputs": entries}))
    output = tmp_path / "result.json"
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["audit", "--out", str(output)])
    if case == "valid":
        audit.main()
        result = json.loads(output.read_text())
        assert len(result["sources"]) == 2
        assert all(row["new_observations_admitted"] is False for row in result["sources"])
        assert all(row["units"] == ["test/year"] for row in result["sources"])
    else:
        match = {
            "changed_bytes": "Input hash mismatch",
            "duplicate_year": "Duplicate or missing annual periods",
            "wrong_columns": "Inventory structure mismatch",
        }[case]
        with pytest.raises(ValueError, match=match):
            audit.main()
        assert not output.exists()
