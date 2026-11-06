"""Execute one scientific replay using wheel-installed packages and restored data and scripts."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import runpy
import sys
import zipfile
from pathlib import Path
from typing import Any

PACKAGES = {
    "archive_govt_nz": "archive-govt-nz",
    "tobac": "tobac-regulatory-research",
    "tobac_supply": "tobac-regulatory-research",
}


def installed_origins() -> dict[str, str]:
    """Reject editable distributions and packages outside this isolated environment."""
    if sys.version_info[:3] != (3, 15, 2) or not sys.flags.isolated or sys.prefix == sys.base_prefix:
        msg = "Select an isolated Python 3.15.2 virtual environment"
        raise RuntimeError(msg)
    prefix = Path(sys.prefix).resolve()
    result: dict[str, str] = {}
    for package, distribution in PACKAGES.items():
        metadata = importlib.metadata.distribution(distribution)
        direct = json.loads(metadata.read_text("direct_url.json") or "{}")
        if direct.get("dir_info", {}).get("editable"):
            msg = f"Editable distribution forbidden: {distribution}"
            raise ValueError(msg)
        mod = importlib.import_module(package)
        origin = Path(str(mod.__file__)).resolve()
        if not origin.is_relative_to(prefix) or not Path(
            str(metadata.locate_file(""))
        ).resolve().is_relative_to(prefix):
            msg = f"Undeclared package origin: {package}"
            raise ValueError(msg)
        result[package] = origin.relative_to(prefix).as_posix()
    for name, module in tuple(sys.modules.items()):
        if name.partition(".")[0] in PACKAGES:
            path = getattr(module, "__file__", None)
            if not path or not Path(path).resolve().is_relative_to(prefix):
                msg = f"Undeclared module origin: {name}"
                raise ValueError(msg)
    return result


def verify_package_wheels(wheels: Path) -> None:
    """Match the package members actually installed to the independently restored wheels."""
    for package, distribution in PACKAGES.items():
        (wheel,) = wheels.glob(distribution.replace("-", "_") + "-*.whl")
        dist = importlib.metadata.distribution(distribution)
        with zipfile.ZipFile(wheel) as archive:
            names = [n for n in archive.namelist() if n.startswith(package + "/") and not n.endswith("/")]
            if not names:
                msg = f"No package members in {wheel.name}: {package}"
                raise ValueError(msg)
            for name in names:
                target = Path(str(dist.locate_file(name)))
                if (
                    target.is_symlink()
                    or not target.resolve().is_relative_to(Path(sys.prefix).resolve())
                    or target.read_bytes() != archive.read(name)
                ):
                    msg = f"Installed bytes differ from recovered wheel: {name}"
                    raise ValueError(msg)


def replay(name: str, destination: Path, accepted: dict[str, Any]) -> dict[str, Any]:
    """Execute the normal entry point, then compare the whole inventory and all numerical tables."""
    import scientific_lineage as scientific  # noqa: PLC0415 -- Loaded from the verified script payload.

    script, _config, extra, _source = scientific.RUNS[name]
    modules = {
        "src/tobac/run.py": "tobac.run",
        "src/tobac/m2.py": "tobac.m2",
        "src/tobac/research/runner.py": "tobac.research.runner",
    }
    if destination.exists():
        msg = "Replay requires a fresh output directory"
        raise FileExistsError(msg)
    sys.argv = [script, "--out", str(destination), *extra]
    if script in modules:
        runpy.run_module(modules[script], run_name="__main__", alter_sys=True)
    else:
        runpy.run_path(str(Path.cwd() / script), run_name="__main__")
    _, files = scientific.manifest_io(destination)
    original = accepted["artifacts"]
    if set(files) != set(original):
        msg = "Recovered output inventory changed"
        raise ValueError(msg)
    changed = sorted(p for p, h in files.items() if original[p] != "sha256:" + h)
    if any(p.endswith(".csv") for p in changed):
        msg = f"Numerical output differs from acceptance: {changed}"
        raise ValueError(msg)
    return {
        "runner": name,
        "files": len(files),
        "exact_csv": sum(p.endswith(".csv") for p in files),
        "changed": changed,
        "installed_origins": installed_origins(),
    }


def main() -> None:
    """Launch with -I from the restored project payload, outside existing implementation checkouts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--runner")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    origins = installed_origins()
    verify_package_wheels(args.wheelhouse)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    if args.runner:
        if args.out is None:
            parser.error("--runner requires --out")
        data = json.loads(
            Path("integration/archive/scientific-lineage-checkpoint_20261102.json").read_bytes()
        )
        result = replay(args.runner, args.out.resolve(), data["runner_results"][args.runner])
    else:
        result = {
            "installed_origins": origins,
            "python": sys.version,
            "isolated": True,
            "interpreter_sha256": hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
        }
    with args.receipt.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
