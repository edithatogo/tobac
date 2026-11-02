"""Execute the installed wheel's frozen consumer surface without promoting a producer."""

import argparse
import hashlib
import importlib
import json
import platform
import sys
from importlib.machinery import EXTENSION_SUFFIXES
from importlib.metadata import Distribution, PackageNotFoundError, distribution, version
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import url2pathname
from zipfile import ZipFile

import numpy as np

from tobac._core import DecisionProblem, exact_evpi, exact_partial_information
from tobac.integrations import voiage_evpi
from tobac.research.voiage_adapter import installed_evpi, partition_problem

RTOL = ATOL = 1e-10


def verify_installed_files(wheel: Path, package: Distribution) -> int:
    """Verify every installed archive member except the installer-rewritten RECORD."""
    checked = 0
    with ZipFile(wheel) as archive:
        for info in archive.infolist():
            if info.is_dir() or info.filename.endswith(".dist-info/RECORD"):
                continue
            relative = Path(info.filename)
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or any(part.endswith(".data") for part in relative.parts)
            ):
                msg = "Unsupported wheel member layout"
                raise ValueError(msg)
            installed = Path(str(package.locate_file(info.filename)))
            with archive.open(info) as original, installed.open("rb") as actual:
                original_hasher = hashlib.sha256()
                while chunk := original.read(64 * 1024):
                    original_hasher.update(chunk)
                expected_hash = original_hasher.hexdigest()
                installed_hash = hashlib.file_digest(actual, "sha256").hexdigest()
            if installed_hash != expected_hash:
                msg = f"Installed wheel member differs: {info.filename}"
                raise RuntimeError(msg)
            checked += 1
    if not checked:
        msg = "No installed wheel members verified"
        raise RuntimeError(msg)
    return checked


def qualify_buffer_ownership() -> list[str]:
    """Reject candidate containers that retain mutable caller-owned buffers."""
    schema = importlib.import_module("voiage.schema")
    polars = importlib.import_module("polars")
    passed: list[str] = []
    for kind in ("values", "parameters"):
        container = schema.ValueArray if kind == "values" else schema.ParameterSet
        for route in ("numpy", "polars", "constructor"):
            # Fortran layout supplies contiguous columns that Polars may borrow.
            source = np.array([[1.0, 4.0], [5.0, 2.0]], order="F")
            expected = source.copy()
            names = ["first", "second"]
            if route == "numpy":
                result = (
                    container.from_numpy(source, names)
                    if kind == "values"
                    else container.from_numpy_or_dict(source)
                )
            else:
                frame = polars.DataFrame({name: source[:, i] for i, name in enumerate(names)})
                result = container.from_polars(frame) if route == "polars" else container(frame=frame)
            source[:] = -999.0
            np.testing.assert_array_equal(result.frame.to_numpy(), expected)
            passed.append(f"{kind}:{route}")
    return passed


def installed_versions() -> dict[str, str | None]:
    """Record optional transport packages even when absent from the environment."""
    versions: dict[str, str | None] = {
        name: version(name) for name in ("numpy", "scipy", "polars", "pyarrow")
    }
    for name in ("pandas", "xarray"):
        try:
            versions[name] = version(name)
        except PackageNotFoundError:
            versions[name] = None
    return versions


def qualify(wheel: Path, expected_version: str, *, buffer_ownership: bool = False) -> dict[str, object]:
    """Require exact installed wheel identity, native loading and numerical parity."""
    if sys.version_info[:3] != (3, 15, 1):
        msg = "Qualified Python 3.15.1 is required"
        raise RuntimeError(msg)
    wheel = wheel.resolve(strict=True)
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    package = distribution("voiage")
    origin = json.loads(package.read_text("direct_url.json") or "{}")
    url = origin.get("url")
    if not isinstance(url, str):
        msg = "Installed distribution has no wheel-origin URL"
        raise TypeError(msg)
    parsed = urlsplit(url)
    if (
        package.version != expected_version
        or parsed.scheme != "file"
        or parsed.netloc
        or Path(url2pathname(parsed.path)).resolve() != wheel
        or origin.get("archive_info", {}).get("hashes", {}).get("sha256", digest) != digest
    ):
        msg = "Installed distribution does not match the exact qualification wheel"
        raise RuntimeError(msg)
    checked = verify_installed_files(wheel, package)
    core = importlib.import_module("voiage._core")
    binary = Path(core.__file__ or "")
    if not binary.is_file() or not str(binary).endswith(tuple(EXTENSION_SUFFIXES)):
        msg = "Actual Voiage native extension did not load"
        raise RuntimeError(msg)
    native_member = "voiage/" + binary.name
    with ZipFile(wheel) as archive:
        if (
            native_member not in archive.namelist()
            or binary.resolve() != Path(str(package.locate_file(native_member))).resolve()
        ):
            msg = "Loaded native extension is outside the verified wheel"
            raise RuntimeError(msg)
    rng = np.random.default_rng(931)
    differences: list[float] = []
    for states, actions in [(2, 2), (5, 3), (17, 4)]:
        for _ in range(10):
            values = rng.normal(size=(states, actions)) * 100
            names = tuple(f"action:{i}" for i in range(actions))
            # The production adapter retains the original rtol/atol=1e-10 check.
            uniform = float(np.max(values, axis=1).mean() - np.max(values.mean(axis=0)))
            observed = voiage_evpi(values, list(names))
            differences.append(abs(observed - uniform))
            weights = rng.uniform(size=states)
            weights[0] = 0
            weights /= weights.sum()
            problem = DecisionProblem(values, names, "fixture units", weights)
            labels = [i % 2 for i in range(states)]
            weighted = float(installed_evpi(problem, expected_version=expected_version)["value"])
            partial = float(
                installed_evpi(partition_problem(problem, labels), expected_version=expected_version)["value"]
            )
            expected_weighted = exact_evpi(problem)
            expected_partial = exact_partial_information(problem, labels)
            np.testing.assert_allclose(weighted, expected_weighted, rtol=RTOL, atol=ATOL)
            np.testing.assert_allclose(partial, expected_partial, rtol=RTOL, atol=ATOL)
            differences.extend([abs(weighted - expected_weighted), abs(partial - expected_partial)])
    ownership = qualify_buffer_ownership() if buffer_ownership else []
    return {
        "buffer_ownership_cases": ownership,
        "schema": "tobac.voiage-installed-consumer.v1",
        "status": "passed",
        "python": sys.version,
        "platform": platform.platform(),
        "command": sys.argv,
        "versions": installed_versions(),
        "wheel": wheel.name,
        "wheel_sha256": digest,
        "installed_wheel_members_verified": checked,
        "voiage_version": package.version,
        "requires_dist": package.requires,
        "native_member": native_member,
        "native_binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
        "cases": len(differences),
        "maximum_absolute_difference": max(differences),
        "rtol": RTOL,
        "atol": ATOL,
        "limits": "Exact installed consumer qualification only; no release, EVSI or empirical claim",
    }


def main() -> None:
    """Write a new receipt only after actual installed-wheel checks succeed."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--buffer-ownership", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        msg = "Refusing to overwrite a qualification receipt"
        raise FileExistsError(msg)
    result = qualify(args.wheel, args.expected_version, buffer_ownership=args.buffer_ownership)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
