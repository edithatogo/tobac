"""Full numerical output preservation; no re-estimation or data assimilation."""

import hashlib
import importlib.util
import io
import json
import shutil
import tarfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def helper():
    path = ROOT / "scripts/unpack_m3_results.py"
    assert path.is_file(), "Saved-results unpacker not implemented"
    spec = importlib.util.spec_from_file_location("m3_unpack", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_complete_saved_outputs_restore_and_match_manifests(tmp_path) -> None:
    count = helper().unpack(ROOT / "results/milestone3/archive", tmp_path / "restored")
    assert count == 24
    for group in ("full", "refined"):
        out = tmp_path / "restored" / group
        manifest = json.loads((out / "manifest.json").read_text())
        for name, digest in manifest["outputs"].items():
            assert hashlib.sha256((out / name).read_bytes()).hexdigest() == digest


def test_modified_archive_part_is_rejected(tmp_path) -> None:
    source = tmp_path / "archive"
    shutil.copytree(ROOT / "results/milestone3/archive", source)
    path = source / "part-001"
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(
        ValueError,
        match=(r"^(?:Archive\ part\ mismatch)"),
    ):
        helper().unpack(source, tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_existing_destination_is_never_overwritten(tmp_path) -> None:
    with pytest.raises(FileExistsError):
        helper().unpack(ROOT / "results/milestone3/archive", tmp_path)


@pytest.mark.parametrize("name", ["../escape.csv", "/tmp/escape.csv", "full/../../escape.csv"])  # noqa: S108 -- Malicious absolute path fixture; never opened.
def test_unsafe_member_rejected_before_write(tmp_path, name) -> None:  # noqa: ARG001 -- Keep the injected fixture or execution-double call signature.
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as tar:
        info = tarfile.TarInfo(name)
        info.size = 1
        tar.addfile(info, io.BytesIO(b"x"))
    with pytest.raises(
        ValueError,
        match=(r"^(?:Unsafe\ or\ duplicate\ archive\ member)"),
    ):
        helper().safe_members(stream.getvalue())
