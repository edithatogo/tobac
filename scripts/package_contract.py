"""Check package paths and declared dependency markers with maintained packaging parsers."""

from __future__ import annotations

import hashlib
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Any

from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]
RESERVED = {"con", "prn", "aux", "nul"} | {f"{p}{n}" for p in ("com", "lpt") for n in range(1, 10)}


def portable_members(names: tuple[str, ...]) -> None:
    """Reject traversal, Windows reserved names and case-insensitive collisions."""
    folded: set[str] = set()
    for name in names:
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or "\\" in name or name.casefold() in folded:
            msg = f"Non-portable archive path: {name}"
            raise ValueError(msg)
        folded.add(name.casefold())
        for part in path.parts:
            if (
                part.rstrip(" .") != part
                or part.split(".")[0].casefold() in RESERVED
                or any(c in part for c in '<>:"|?*')
            ):
                msg = f"Non-portable archive component: {name}"
                raise ValueError(msg)


def active_dependencies(requirements: list[str], environment: dict[str, str], extras: list[str]) -> set[str]:
    """Evaluate PEP 508 markers for a target platform and selected extras."""
    active: set[str] = set()
    for raw in requirements:
        req = Requirement(raw)
        if req.marker is None or any(req.marker.evaluate({**environment, "extra": e}) for e in ["", *extras]):
            req.marker = None
            req.name = canonicalize_name(req.name)
            active.add(str(req))
    return active


def dependency_contract(data: bytes, project: dict[str, Any]) -> dict[str, list[str]]:
    """Match wheel dependencies to root declarations on Linux and Windows, including extras."""
    metadata = BytesParser().parsebytes(data)
    if SpecifierSet(metadata["Requires-Python"] or "") != SpecifierSet(project["requires-python"]):
        msg = "Package Python constraint differs from source"
        raise ValueError(msg)
    groups: dict[str, list[str]] = project.get("optional-dependencies", {})
    if set(metadata.get_all("Provides-Extra", [])) != set(groups):
        msg = "Package optional dependencies differ from source"
        raise ValueError(msg)
    requirements = metadata.get_all("Requires-Dist", [])
    selections = {"none": [], **{name: [name] for name in groups}, "all": list(groups)}
    results: dict[str, list[str]] = {}
    for system, os_name, sys_platform in (("Linux", "posix", "linux"), ("Windows", "nt", "win32")):
        environment = {
            **{key: str(value) for key, value in default_environment().items()},
            "platform_system": system,
            "os_name": os_name,
            "sys_platform": sys_platform,
            "platform_machine": "x86_64" if system == "Linux" else "AMD64",
            "python_version": "3.15",
            "python_full_version": "3.15.2",
        }
        for label, extras in selections.items():
            declared = project["dependencies"] + [r for name in extras for r in groups[name]]
            expected = active_dependencies(declared, environment, extras)
            actual = active_dependencies(requirements, environment, extras)
            if actual != expected:
                msg = f"Package dependencies differ from source: {system}/{label}"
                raise ValueError(msg)
            results[f"{system}:{label}"] = sorted(actual)
    return results


def inspect_package(wheel: Path, rebuilt: Path, sdist: Path) -> dict[str, Any]:
    """Check archive portability, module/license bytes and equivalent sdist reconstruction."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    with tarfile.open(sdist) as archive:
        portable_members(tuple(m.name.rstrip("/") for m in archive.getmembers()))
        if any(m.issym() or m.islnk() for m in archive.getmembers()):
            msg = "Package sdist has a non-portable link"
            raise ValueError(msg)
    with zipfile.ZipFile(wheel) as archive:
        portable_members(tuple(archive.namelist()))
        (metadata_name,) = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        metadata = BytesParser().parsebytes(archive.read(metadata_name))
        identity = (
            canonicalize_name(metadata["Name"] or ""),
            metadata["Version"],
            metadata["License-Expression"],
        )
        if identity != (canonicalize_name(project["name"]), project["version"], project["license"]):
            msg = "Packaged project identity or license differs from source"
            raise ValueError(msg)
        dependencies = dependency_contract(archive.read(metadata_name), project)
        for path in (ROOT / "src").rglob("*"):
            if (
                path.is_file()
                and path.suffix in {".py", ".typed"}
                and archive.read(path.relative_to(ROOT / "src").as_posix()) != path.read_bytes()
            ):
                msg = "Packaged module bytes differ from source"
                raise ValueError(msg)
        folder = metadata_name.removesuffix("METADATA")
        for name in ("LICENSE", "NOTICE"):
            if archive.read(folder + "licenses/" + name) != (ROOT / name).read_bytes():
                msg = "Packaged license/notice bytes differ from source"
                raise ValueError(msg)
        contents = {n: hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
    with zipfile.ZipFile(rebuilt) as archive:
        reconstructed = {n: hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
    if reconstructed != contents:
        msg = "Sdist-reconstructed wheel contents differ from direct wheel"
        raise ValueError(msg)
    return {
        "dependency_marker_cases": dependencies,
        "wheel_members_sha256": contents,
        "sdist_rebuilt_contents_equal": True,
    }
