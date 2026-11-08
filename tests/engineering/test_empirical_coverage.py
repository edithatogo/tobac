"""Coverage audit rejects changed bytes and malformed annual inventories."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
import pytest

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]


def _audit_module() -> ModuleType:
    """Load the maintained audit without running its command line."""
    spec = importlib.util.spec_from_file_location(
        "coverage_audit", ROOT / "scripts/audit_empirical_coverage.py"
    )
    assert spec
    assert spec.loader
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    return audit


@pytest.mark.parametrize("case", ["valid", "changed_bytes", "duplicate_year", "wrong_columns"])
def test_coverage_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, case: str) -> None:
    audit = _audit_module()
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


def _nzhs_table(audit: ModuleType) -> pl.DataFrame:
    """Construct only synthetic marginal triplets with explicit source fields."""
    rows = []
    for indicator in audit.NZHS_INDICATORS:
        for year in range(2020, 2024):
            row = dict.fromkeys(audit.NZHS_COLUMNS, "")
            row.update(
                {
                    "population": "adults",
                    "group": "Total",
                    "year": str(year),
                    "short.description": indicator,
                    "total": "2.0",
                    "total.low.CI": "1.0",
                    "total.high.CI": "3.0",
                    "estimated.number": "1000",
                }
            )
            rows.append(row)
    return pl.DataFrame(rows)


def _write_nzhs(tmp_path: Path, table: pl.DataFrame) -> tuple[Path, str]:
    """Return the exact synthetic original and its independently computed hash."""
    source = tmp_path / "synthetic-survey.csv"
    table.write_csv(source)
    return source, hashlib.sha256(source.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    ("updates", "flagged", "missing"),
    [
        ({}, [], []),
        ({"flag_for_publishing": "S", "total": "9999"}, [2020], []),
        ({"flag_for_publishing": "e"}, [2020], []),
        ({"total": "NA"}, [], [2020]),
    ],
)
def test_nzhs_source_reconciliation(
    tmp_path: Path,
    updates: dict[str, str],
    flagged: list[int],
    missing: list[int],
) -> None:
    """Keep flags, missingness and distinct units before any likelihood exists."""
    audit = _audit_module()
    rows = _nzhs_table(audit).to_dicts()
    rows[0].update(updates)
    source, sha = _write_nzhs(tmp_path, pl.DataFrame(rows))
    summary, candidates = audit.nzhs_candidates(source, sha)
    assert summary["source_family"] == "NZHS"
    assert summary["candidate_records"] == 32
    assert summary["new_observations_admitted"] is False
    assert summary["joint_covariance_available"] is False
    assert summary["iso_observation_dates_verified"] is False
    assert summary["holdout_manifest_frozen"] is False
    assert candidates["source_record_ordinal"].n_unique() == 32
    mean = next(row for row in summary["series"] if row["indicator"] == "Mean number of cigarettes")
    assert mean["unit"] != summary["series"][0]["unit"]
    first = summary["series"][0]
    assert first["flagged_for_review"] == flagged
    assert first["missing_triplets"] == missing
    assert set(first["unflagged_complete_triplets"]).isdisjoint(flagged + missing)
    retained = candidates.filter(pl.col("source_record_ordinal") == 1).to_dicts()[0]
    assert all(retained[key] == value for key, value in updates.items())


@pytest.mark.parametrize(
    ("updates", "message"),
    [
        ({"total.high.CI": "1.0"}, "Invalid NZHS"),
        ({"total": "101.0", "total.high.CI": "102.0"}, "Invalid NZHS"),
        ({"total": "NaN"}, "Invalid NZHS"),
        ({"flag_for_publishing": "unknown"}, "Unknown NZHS"),
        ({"year": "2020/21"}, "four-digit"),
        ({"year": "2025"}, "four-digit"),
    ],
)
def test_nzhs_invalid_marginals(tmp_path: Path, updates: dict[str, str], message: str) -> None:
    """Reject impossible intervals, unqualified flags and incompatible year conventions."""
    audit = _audit_module()
    rows = _nzhs_table(audit).to_dicts()
    rows[0].update(updates)
    source, sha = _write_nzhs(tmp_path, pl.DataFrame(rows))
    with pytest.raises(ValueError, match=message):
        audit.nzhs_candidates(source, sha)


@pytest.mark.parametrize("case", ["duplicate", "schema", "hash", "indicator"])
def test_nzhs_changed_source_contract(tmp_path: Path, case: str) -> None:
    """A new source edition cannot silently duplicate, omit or reshape source records."""
    audit = _audit_module()
    table = _nzhs_table(audit)
    if case == "duplicate":
        table = pl.concat([table, table.head(1)])
    if case == "schema":
        table = table.with_columns(pl.lit("unreviewed").alias("new_column"))
    if case == "indicator":
        table = table.slice(4)
    source, sha = _write_nzhs(tmp_path, table)
    if case == "hash":
        source.write_text(source.read_text() + "changed bytes")
    messages = {
        "duplicate": "Duplicate NZHS",
        "schema": "schema changed",
        "hash": "Input hash mismatch",
        "indicator": "indicator absent",
    }
    with pytest.raises(ValueError, match=messages[case]):
        audit.nzhs_candidates(source, sha)


def test_nzhs_absent_survey_year_is_not_filled(tmp_path: Path) -> None:
    """Unmeasured occasions stay absent rather than becoming interpolated observations."""
    audit = _audit_module()
    table = _nzhs_table(audit).filter(
        ~((pl.col("short.description") == "Current smokers") & (pl.col("year") == "2021"))
    )
    source, sha = _write_nzhs(tmp_path, table)
    summary, candidates = audit.nzhs_candidates(source, sha)
    assert summary["series"][0]["absent_year_labels"] == [2021]
    assert candidates.height == 31


@pytest.mark.parametrize("case", ["existing", "inside_repository"])
def test_nzhs_candidate_output_is_protected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    case: str,
) -> None:
    """Preserve prior editions and keep new observation tables outside the repository."""
    audit = _audit_module()
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    monkeypatch.setattr(audit, "ROOT", checkout)
    destination = tmp_path / "existing.csv" if case == "existing" else checkout / "new.csv"
    if case == "existing":
        destination.write_text("preserve this edition")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "audit",
            "--out",
            str(tmp_path / "summary.json"),
            "--nzhs-csv",
            str(tmp_path / "source.csv"),
            "--nzhs-sha256",
            "0" * 64,
            "--candidate-out",
            str(destination),
        ],
    )
    with pytest.raises(SystemExit) as exc:
        audit.main()
    assert exc.value.code == 2
    if case == "existing":
        assert destination.read_text() == "preserve this edition"
    else:
        assert not destination.exists()
