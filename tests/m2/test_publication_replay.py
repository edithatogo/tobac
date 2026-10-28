"""Reject scientifically changed identities, booleans, rows and numerical outputs."""

from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]


@pytest.fixture
def replay(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import qualify_publication_replay  # noqa: PLC0415 -- CLI comparison boundary.

    return qualify_publication_replay


def test_only_checkout_metadata_is_excluded(replay) -> None:
    assert (
        replay.compare_values(
            {"checkout": {"commit": "old"}, "x": [1.0, True]},
            {"checkout": {"commit": None}, "x": [1 + 1e-12, True]},
        )
        < 1e-10
    )
    with pytest.raises(ValueError, match="mismatch"):
        replay.compare_values({"conditioned": False}, {"conditioned": 0})
    with pytest.raises(ValueError, match="mismatch"):
        replay.compare_values({"posterior": {"checkout": "source"}}, {"posterior": {"checkout": "changed"}})
    with pytest.raises(ValueError, match="Numerical"):
        replay.compare_values(1.0, 1.01)
    with pytest.raises(ValueError, match="Nonfinite"):
        replay.compare_values(float("nan"), float("nan"))


def test_table_comparison_checks_all_identifiers_rows_and_numbers(replay, tmp_path) -> None:
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    a.write_text("action,value\na,0.1\n")
    b.write_text("action,value\na,0.100000000001\n")
    assert replay.compare_table(a, b)["rows"] == 1
    b.write_text("action,value\nb,0.1\n")
    with pytest.raises(ValueError, match="identity"):
        replay.compare_table(a, b)
    b.write_text("action,value\na,0.1\na,0.1\n")
    with pytest.raises(ValueError, match="row count"):
        replay.compare_table(a, b)


def test_numeric_looking_identifiers_are_not_relabelled(replay, tmp_path) -> None:
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    a.write_text("case,value\n1,0.1\n")
    b.write_text("case,value\n1.0,0.1\n")
    with pytest.raises(ValueError, match="identity"):
        replay.compare_table(a, b)
