"""Keep local source claims provisional until the evidence contract admits them."""

import csv
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "candidate_source_register", ROOT / "scripts/build_candidate_source_register.py"
)


def module():
    assert SPEC
    assert SPEC.loader
    result = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(result)
    return result


def test_candidate_catalogue_retains_claims_without_admission(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    source.write_text("source_id,licence,sha256\nexample,reported licence,abc\n", encoding="utf-8")
    output = tmp_path / "candidate.csv"
    module().build(source, output)
    with output.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert rows == [
        {
            "source_id": "example",
            "reported_licence": "reported licence",
            "reported_sha256": "abc",
            "source_review_status": "pending",
            "empirical_admission": "false",
        }
    ]


def test_duplicate_identity_preserves_existing_output(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    source.write_text("source_id,licence\nexample,a\nexample,b\n", encoding="utf-8")
    output = tmp_path / "candidate.csv"
    output.write_text("preserved", encoding="utf-8")
    with pytest.raises(ValueError, match="nonempty and unique"):
        module().build(source, output)
    assert output.read_text(encoding="utf-8") == "preserved"


def test_recorded_catalogue_keeps_known_source_discrepancy_open() -> None:
    path = ROOT / "conductor/tracks/nz_au_empirical_20261106/candidate-source-register_20261114.csv"
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 28
    assert all(row["source_review_status"] == "pending" for row in rows)
    assert all(row["empirical_admission"] == "false" for row in rows)
    aihw = next(row for row in rows if row["source_id"] == "aihw-ndshs-2025")
    assert "wastewater_page.html" in aihw["reported_local_raw_path"]
