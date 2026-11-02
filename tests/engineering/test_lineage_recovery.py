"""Independent-copy inventory rejects corrupt or incomplete copies."""

lazy from pathlib import Path

import pytest

from scripts.qualify_lineage_recovery import copy_generation, seal, verify


def test_recovery_rejects_altered_and_missing_bytes(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    item = source / "original"
    item.write_bytes(b"original")
    pin = seal(source)
    verify(source, pin)
    with pytest.raises(ValueError, match="same filesystem"):
        copy_generation(source, tmp_path / "nearby", pin)
    item.write_bytes(b"replaced")
    with pytest.raises(ValueError, match="inventory"):
        verify(source, pin)
    item.unlink()
    with pytest.raises(ValueError, match="inventory"):
        verify(source, pin)


def test_recovery_rejects_changed_inventory_and_extra_files(tmp_path: Path) -> None:
    (tmp_path / "receipt").write_bytes(b"record")
    pin = seal(tmp_path)
    (tmp_path / "extra").touch()
    with pytest.raises(ValueError, match="inventory"):
        verify(tmp_path, pin)
    (tmp_path / "extra").unlink()
    (tmp_path / "closure.json").write_text("{}")
    with pytest.raises(ValueError, match="pinned"):
        verify(tmp_path, pin)
