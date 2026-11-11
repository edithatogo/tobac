"""Check overlapping candidate parameter editions without admitting observations."""

from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence/parameter_candidates_20261109"
DESIGN = ROOT / "conductor/tracks/dynamic_frontier_20261108/design.md"
MARKER = re.compile(
    r"<!-- TOBAC_PARAMETER_CANDIDATES_V1 -->\s*```json\s*(.*?)\s*```",
    re.DOTALL,
)


def catalogues() -> tuple[dict, dict]:
    """Load published editions and keep the active-runtime boundary explicit."""
    registry = json.loads((EVIDENCE / "registry.json").read_text(encoding="utf-8"))
    assert registry["metadata"]["parameter_count"] == len(registry["parameters"]) == 65
    assert registry["metadata"]["source_count"] == len(registry["sources"]) == 12
    assert all(item["admission_status"] == "candidate_only" for item in registry["parameters"])
    assert all(item["runtime_configuration_changed"] is False for item in registry["parameters"])
    assert all(item["distribution"] is None for item in registry["parameters"])

    found = MARKER.search(DESIGN.read_text(encoding="utf-8"))
    assert found is not None
    embedded = json.loads(found.group(1))
    assert embedded["empirical_admission"] is False
    assert embedded["active_model_parameters_changed"] is False
    assert len(embedded["records"]) == 61

    candidate = {item["parameter_id"]: item for item in registry["parameters"]}
    older = {
        item["id"]: item
        for values in embedded["records"]
        for item in [dict(zip(embedded["columns"], values, strict=True))]
    }
    assert len(candidate) == 65
    assert len(older) == 61
    return candidate, older


def verify(rows: list[dict[str, str]], candidate: dict, older: dict) -> None:
    """Only declared source aliases and unit conversions can match two records."""
    assert len(rows) == 20
    assert len({row["candidate_id"] for row in rows}) == len(rows)
    assert len({row["embedded_id"] for row in rows}) == len(rows)
    for row in rows:
        actual = candidate[row["candidate_id"]]
        original = older[row["embedded_id"]]
        assert row["admission"] == "candidate_only"
        assert (row["candidate_source"], row["embedded_source"]) == (
            actual["source_id"],
            original["source_id"],
        )
        assert actual["source_id"] == original["source_id"] or (
            actual["source_id"], original["source_id"]
        ) == ("PHARMAC_DISCOUNT", "PHARMAC_PFPA_DISCOUNT")
        assert (row["candidate_unit"], row["embedded_unit"]) == (
            actual["unit"],
            original["unit"],
        )
        factor = float(row["candidate_to_embedded_multiplier"])
        assert math.isfinite(factor)
        assert factor in (1.0, 0.01)
        if factor == 0.01:
            assert (actual["unit"], original["unit"]) == (
                "percentage_points",
                "risk_difference",
            )
        for key in ("value", "lower", "upper"):
            new, old = actual[key], original[key]
            assert (new is None) == (old is None)
            if new is not None:
                assert math.isclose(new * factor, old, rel_tol=0, abs_tol=1e-12)


def rows() -> list[dict[str, str]]:
    """Open the canonical alias table without discarding its source IDs."""
    with (EVIDENCE / "alias_crosswalk.csv").open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_candidate_aliases_preserve_units_and_intervals() -> None:
    candidate, older = catalogues()
    verify(rows(), candidate, older)


@pytest.mark.parametrize("change", ["missing", "duplicate", "conversion", "wrong_source"])
def test_alias_verifier_rejects_false_equivalence(change: str) -> None:
    candidate, older = catalogues()
    revised = rows()
    if change == "missing":
        revised[0]["candidate_id"] = "UNSOURCED"
    elif change == "duplicate":
        revised[1] = dict(revised[0])
    elif change == "conversion":
        row = next(item for item in revised if item["candidate_id"] == "WALKER_RD_NONNIC")
        row["candidate_to_embedded_multiplier"] = "1"
    else:
        revised[0]["embedded_source"] = "ANOTHER_STUDY"
    with pytest.raises((AssertionError, KeyError)):
        verify(revised, candidate, older)
