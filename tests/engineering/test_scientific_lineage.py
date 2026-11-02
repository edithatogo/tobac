"""Scientific lineage edges must distinguish conditional and empirical results."""

import pytest

from scripts.scientific_lineage import affected_results, compare_phyo


def test_impact_uses_execution_identity_with_equal_output_bytes() -> None:
    """Two runners may write identical bytes while depending on different inputs."""
    runs = {
        "m1": {"inputs": {"regulatory": "one"}, "originals": {}, "outputs": {"a.csv": "same"}},
        "m2": {"inputs": {"regulatory": "one"}, "originals": {"SHINE": "two"}, "outputs": {"a.csv": "same"}},
    }
    assert affected_results(runs, "SHINE") == {"m2": ["a.csv"]}
    assert set(affected_results(runs, "regulatory")) == {"m1", "m2"}
    assert affected_results(runs, "unrelated") == {}


def test_missing_published_table_fails_closed() -> None:
    """An article identity alone cannot verify the fitted observations."""
    with pytest.raises(ValueError, match="Table 2"):
        compare_phyo(b"<html/>", b"year\n2012\n")


def test_shared_returns_group_is_distinct_from_specific_originals() -> None:
    """An underlying-data warning reaches two runners; a changed workbook edition reaches one."""
    runs = {
        "release": {
            "inputs": {},
            "originals": {"workbook": "one"},
            "outputs": {"x": "a"},
            "underlying_groups": ["NZ_MOH_tobacco_returns"],
        },
        "paired": {
            "inputs": {},
            "originals": {"table2": "two"},
            "outputs": {"x": "b"},
            "underlying_groups": ["NZ_MOH_tobacco_returns", "NZHS"],
        },
    }
    assert set(affected_results(runs, "NZ_MOH_tobacco_returns")) == {"release", "paired"}
    assert set(affected_results(runs, "workbook")) == {"release"}
    assert set(affected_results(runs, "NZHS")) == {"paired"}
