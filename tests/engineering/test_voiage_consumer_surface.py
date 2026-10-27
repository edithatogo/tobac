"""Reject removed symbols without importing candidate code or scanning string fixtures."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def module():
    spec = importlib.util.spec_from_file_location(
        "consumer_surface", ROOT / "scripts/voiage_consumer_surface.py"
    )
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


@pytest.mark.parametrize("symbol", ["dataset", "to_dataset", "from_dataset"])
def test_surface_rejects_removed_container_attributes(tmp_path, symbol) -> None:
    path = tmp_path / "src/tobac/probe.py"
    path.parent.mkdir(parents=True)
    path.write_text(f"container.{symbol}\n")
    with pytest.raises(ValueError, match=f"Removed container symbol {symbol}"):
        module().inventory(tmp_path)


def test_surface_hashes_imports_and_does_not_execute(tmp_path) -> None:
    path = tmp_path / "src/tobac/probe.py"
    path.parent.mkdir(parents=True)
    path.write_text('from voiage.schema import ValueArray\nraise RuntimeError("not executed")\n')
    result = module().inventory(tmp_path)
    assert result["removed_symbol_references"] == 0
    assert result["voiage_imports"][0]["names"] == ["ValueArray"]
    before = result["files"]
    path.write_text(path.read_text() + "# changed bytes\n")
    assert module().inventory(tmp_path)["files"] != before


def test_surface_ignores_removed_names_inside_rejection_fixture_strings(tmp_path) -> None:
    path = tmp_path / "tests/engineering/probe.py"
    path.parent.mkdir(parents=True)
    path.write_text('fixture = "container.dataset"\n')
    assert module().inventory(tmp_path)["removed_symbol_references"] == 0


def test_surface_rejects_literal_dynamic_lookup(tmp_path) -> None:
    path = tmp_path / "src/tobac/probe.py"
    path.parent.mkdir(parents=True)
    path.write_text('getattr(container, "dataset")\n')
    with pytest.raises(ValueError, match="Removed container lookup"):
        module().inventory(tmp_path)


def test_surface_does_not_call_an_empty_tree_qualified(tmp_path) -> None:
    with pytest.raises(ValueError, match="No consumer Python sources"):
        module().inventory(tmp_path)
