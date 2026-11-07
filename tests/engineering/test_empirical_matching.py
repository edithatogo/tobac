"""Test source-native overlap and the boundary against an unsupported join."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def audit() -> ModuleType:
    """Load the existing script surface without executing its CLI."""
    spec = importlib.util.spec_from_file_location(
        "empirical_matching_audit", ROOT / "scripts/reconcile_empirical_candidates.py"
    )
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin(path: Path) -> dict[str, str]:
    """Bind synthetic fixture bytes using the real CLI input shape."""
    return {
        "root": str(path.parent),
        "file": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def write_csv(path: Path, rows: list[list[str]]) -> dict[str, str]:
    """Keep literal empty fields as quoted source strings."""
    with path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream, quoting=csv.QUOTE_ALL).writerows(rows)
    return pin(path)


@pytest.fixture
def inputs(tmp_path: Path, audit: ModuleType) -> dict[str, Any]:
    """Small invented inputs spanning distinct periods, units and reporting flags."""
    import audit_empirical_coverage as coverage  # noqa: PLC0415

    survey = []
    for indicator in coverage.NZHS_INDICATORS:
        row = dict.fromkeys(coverage.NZHS_COLUMNS, "")
        row.update(
            population="adults",
            year="2024",
            group="Total",
            total="3",
            **{"short.description": indicator, "total.low.CI": "2", "total.high.CI": "4"},
        )
        survey.append([row[k] for k in coverage.NZHS_COLUMNS])
    methods = tmp_path / "methods.pdf"
    methods.write_bytes(b"%PDF-1.7 synthetic marker; not a real survey report")
    return {
        "nzhs": write_csv(tmp_path / "nzhs.csv", [list(coverage.NZHS_COLUMNS), *survey]),
        "methods": pin(methods),
        "price": write_csv(
            tmp_path / "price.csv",
            [
                ["Synthetic price fixture", ""],
                ["", "CPIQ.SAP0240"],
                ["2024Q2", "11.00"],
                ["2024Q3", "12.00"],
                ["2025Q2", "13.00"],
                ["2025Q3", "14.00"],
                ["2025Q4", "15.00"],
                ["Table information:"],
                ["CPI019AA"],
                ["Unit = $, pk of 25"],
                ["Calculated by applying index movements"],
            ],
        ),
        "population": write_csv(
            tmp_path / "population.csv",
            [
                ["Synthetic population fixture", "", "", "", ""],
                ["", "As at", "", "Mean year ended", ""],
                ["", "Total", "", "Total", ""],
                ["", "15 Years and Over", "", "15 Years and Over", ""],
                ["2024Q3", "100", "", "9900", ""],
                ["2024Q4", "200", "", "9900", ""],
                ["2025Q1", "300", " P", "9900", ""],
                ["2025Q2", "400", "", "9900", ""],
                ["2025Q3", "500", "", "9900", ""],
                ["Table information:"],
                ["DPE054AA"],
            ],
        ),
        "trade_imports": write_csv(
            tmp_path / "import.csv",
            [
                [*audit.TRADE_BASE, *audit.TRADE_IMPORT, "Status"],
                ["202609", "2402209000", "Synthetic tobacco", "MIL", "1", "2", "3", "Provisional"],
                ["202506", "0101210015", "Synthetic non-tobacco", "NMB", "1", "2", "3", "Final"],
            ],
        ),
        "trade_exports": write_csv(
            tmp_path / "export.csv",
            [
                [*audit.TRADE_BASE, *audit.TRADE_EXPORT, "Status"],
                [
                    "202609",
                    "2404120011",
                    "Synthetic nicotine liquid",
                    "LTR",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "Provisional",
                ],
            ],
        ),
        "survey_scope": {
            "geography": "NZ_national",
            "population": "NZHS_adults_15plus",
            "start": "2024-07-09",
            "end": "2025-07-20",
            "unit": "percent_adults_15plus",
        },
        "survey_start_label": "2024",
    }


def test_period_coverage_keeps_distinct_measurements(audit: ModuleType, inputs: dict[str, Any]) -> None:
    result = audit.reconcile(inputs)
    assert result["price"]["overlapping_quarters"] == ["2024Q3", "2025Q2", "2025Q3"]
    assert result["population"]["quarter_end_mean_diagnostic"] == "250"
    assert result["population"]["nonfinal_flags"] == [{"quarter": "2025Q1", "flag": " P"}]
    assert result["trade_imports"]["overlapping_months"] == ["202506"]
    assert result["trade_imports"]["overlapping_hs24_months"] == []
    assert result["trade_exports"]["overlapping_months"] == []
    assert "Re-exports Qty" in result["trade_exports"]["original_flow_fields"]
    assert result["releases"]["overlapping_calendar_years"] == [2024, 2025]
    assert not result["new_observations_admitted"]
    assert result["joined_observations"] == 0
    assert not result["likelihood_or_fit_executed"]


def edit_source(inputs: dict[str, Any], key: str, before: str, after: str, *, repin: bool = True) -> None:
    """Alter one synthetic original while optionally retaining the stale pin."""
    path = Path(inputs[key]["root"]) / inputs[key]["file"]
    text = path.read_text(encoding="utf-8")
    assert before in text
    path.write_text(text.replace(before, after), encoding="utf-8")
    if repin:
        inputs[key] = pin(path)


@pytest.mark.parametrize(
    "case",
    [
        ("price", "2024Q2", "2024Q5", "Invalid calendar quarter"),
        ("price", "2024Q2", "2024Q3", "nonempty and unique"),
        ("population", '" P"', '"X"', "Unknown native population status flag"),
        ("trade_exports", "202609", "2026.09", "Invalid trade month"),
    ],
)
def test_invalid_source_fails_even_if_repinned(
    audit: ModuleType, inputs: dict[str, Any], case: tuple[str, str, str, str]
) -> None:
    key, before, after, message = case
    edit_source(inputs, key, before, after)
    with pytest.raises(ValueError, match=message):
        audit.reconcile(inputs)


def test_changed_source_fails_before_reconciliation(audit: ModuleType, inputs: dict[str, Any]) -> None:
    edit_source(inputs, "price", "11.00", "11.01", repin=False)
    with pytest.raises(ValueError, match="Input hash mismatch"):
        audit.reconcile(inputs)


@pytest.mark.parametrize("status", ["absent", "unavailable", "suppressed"])
def test_no_benchmark_mean_for_absent_or_unavailable_quarter(
    audit: ModuleType, inputs: dict[str, Any], status: str
) -> None:
    row = '"2025Q2","400","","9900",""'
    replacement = {
        "absent": "",
        "unavailable": row.replace('"400"', '".."'),
        "suppressed": row.replace(',"",', '," S",', 1),
    }
    edit_source(inputs, "population", row, replacement[status])
    result = audit.reconcile(inputs)["population"]
    assert result["quarter_end_mean_diagnostic"] is None
    assert result["absent_quarters" if status == "absent" else "unavailable_quarters"] == ["2025Q2"]


def test_reject_undeclared_geography_transport(audit: ModuleType, inputs: dict[str, Any]) -> None:
    inputs["survey_scope"]["geography"] = "AU_national"
    with pytest.raises(ValueError, match="no cross-country or unit transport"):
        audit.reconcile(inputs)
