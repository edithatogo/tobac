"""Negative receipt identities are rejected before executing candidate code."""

import hashlib
import importlib.util
import json
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def load():
    spec = importlib.util.spec_from_file_location(
        "consumer_probe", ROOT / "scripts/qualify_voiage_consumer.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("tamper", ["version", "hash", "url", "missing"])
def test_probe_rejects_a_different_installed_wheel(tmp_path, monkeypatch, tamper) -> None:
    module = load()
    wheel = tmp_path / "fixture.whl"
    wheel.write_bytes(b"negative fixture; not a valid wheel")
    origin = {
        "url": wheel.as_uri(),
        "archive_info": {"hashes": {"sha256": hashlib.sha256(wheel.read_bytes()).hexdigest()}},
    }
    version = "2.2.0"
    if tamper == "version":
        version = "different"
    elif tamper == "hash":
        origin["archive_info"]["hashes"]["sha256"] = "0" * 64
    elif tamper == "url":
        origin["url"] = "https://invalid.example/fixture.whl"
    else:
        origin.pop("url")
    package = types.SimpleNamespace(version=version, read_text=lambda _name: json.dumps(origin))
    monkeypatch.setattr(module, "distribution", lambda _name: package)
    error = TypeError if tamper == "missing" else RuntimeError
    with pytest.raises(error, match=r"wheel-origin URL|exact qualification wheel"):
        module.qualify(wheel, "2.2.0")


def test_probe_rejects_an_unqualified_python_before_reading_wheel(tmp_path, monkeypatch) -> None:
    module = load()
    monkeypatch.setattr(module.sys, "version_info", (3, 14, 9))
    with pytest.raises(RuntimeError, match=r"Python 3\.15\.1"):
        module.qualify(tmp_path / "missing.whl", "2.2.0")


@pytest.mark.parametrize("replacement", [b"value = 2\n", b"value = 1\r\n"])
def test_probe_checks_installed_member_bytes_even_without_installer_archive_hash(
    tmp_path, replacement
) -> None:
    from zipfile import ZipFile  # noqa: PLC0415 -- Synthetic archive boundary, not candidate execution.

    module = load()
    wheel = tmp_path / "fixture.whl"
    with ZipFile(wheel, "w") as archive:
        archive.writestr("package/module.py", b"value = 1\n")
        archive.writestr("fixture.dist-info/RECORD", "installer rewrites this")
    installed = tmp_path / "installed"
    member = installed / "package/module.py"
    member.parent.mkdir(parents=True)
    member.write_bytes(b"value = 1\n")
    package = types.SimpleNamespace(locate_file=lambda name: installed / name)
    assert module.verify_installed_files(wheel, package) == 1
    member.write_bytes(replacement)
    with pytest.raises(RuntimeError, match="Installed wheel member differs"):
        module.verify_installed_files(wheel, package)


def test_probe_rejects_a_shadowed_native_module(tmp_path, monkeypatch) -> None:
    from zipfile import ZipFile  # noqa: PLC0415 -- A negative source-identity fixture, not native execution.

    module = load()
    wheel = tmp_path / "fixture wheel.whl"
    filename = "_core" + module.EXTENSION_SUFFIXES[0]
    with ZipFile(wheel, "w") as archive:
        archive.writestr("voiage/" + filename, b"negative fixture")
    installed = tmp_path / "installed"
    member = installed / "voiage" / filename
    member.parent.mkdir(parents=True)
    member.write_bytes(b"negative fixture")
    shadow = tmp_path / filename
    shadow.write_bytes(b"negative fixture")
    origin = {"url": wheel.as_uri(), "archive_info": {}}
    package = types.SimpleNamespace(
        version="2.2.0",
        read_text=lambda _name: json.dumps(origin),
        locate_file=lambda name: installed / name,
    )
    monkeypatch.setattr(module, "distribution", lambda _name: package)
    monkeypatch.setattr(
        module.importlib, "import_module", lambda _name: types.SimpleNamespace(__file__=str(shadow))
    )
    with pytest.raises(RuntimeError, match="outside the verified wheel"):
        module.qualify(wheel, "2.2.0")


@pytest.mark.parametrize("copy_buffers", [False, True])
def test_buffer_probe_rejects_aliasing_and_accepts_snapshots(monkeypatch, copy_buffers) -> None:
    import polars as pl  # noqa: PLC0415 -- Local synthetic container fixture.

    module = load()

    class Container:
        def __init__(self, *, frame) -> None:
            self.frame = pl.DataFrame(frame.to_numpy().copy()) if copy_buffers else frame

        @classmethod
        def from_numpy(cls, values, _names=None) -> Container:
            return cls(frame=pl.DataFrame({str(i): values[:, i] for i in range(values.shape[1])}))

        from_numpy_or_dict = from_numpy

        @classmethod
        def from_polars(cls, frame) -> Container:
            return cls(frame=frame)

    schema = types.SimpleNamespace(ValueArray=Container, ParameterSet=Container)
    monkeypatch.setattr(
        module.importlib, "import_module", lambda name: schema if name == "voiage.schema" else pl
    )
    if copy_buffers:
        assert len(module.qualify_buffer_ownership()) == 6
    else:
        with pytest.raises(AssertionError):
            module.qualify_buffer_ownership()
