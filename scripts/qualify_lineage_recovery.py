"""Seal, copy and restore a finite private generation with an independently held SHA-256 pin."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

MANIFEST = "closure.json"


def digest(path: Path) -> str:
    """Hash actual file bytes without loading a large wheel into memory."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inventory(root: Path) -> dict[str, tuple[int, str]]:
    """Inventory regular files; reject links and filesystem-special entries."""
    files = {}
    for item in sorted(root.rglob("*")):
        if item.is_symlink() or not (item.is_dir() or item.is_file()):
            msg = f"Unsupported recovery entry: {item.relative_to(root)}"
            raise ValueError(msg)
        name = item.relative_to(root).as_posix()
        if item.is_file() and name != MANIFEST:
            files[name] = (item.stat().st_size, digest(item))
    return files


def canonical(root: Path) -> bytes:
    """Produce the exact canonical manifest from all restored contents."""
    files = inventory(root)
    if not files:
        msg = "Empty recovery inventory"
        raise ValueError(msg)
    return (
        json.dumps({"schema": "tobac.recovery-closure.v1", "files": files}, sort_keys=True, indent=2) + "\n"
    ).encode()


def seal(root: Path) -> str:
    """Exclusively create the manifest after all inputs are assembled."""
    raw = canonical(root)
    with (root / MANIFEST).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return hashlib.sha256(raw).hexdigest()


def verify(root: Path, pin: str) -> None:
    """Reject stale manifests, dropped or additional files, or same-size substitutions."""
    manifest = root / MANIFEST
    if manifest.is_symlink() or digest(manifest) != pin:
        msg = "Recovery manifest differs from pinned SHA-256"
        raise ValueError(msg)
    if hashlib.sha256(canonical(root)).hexdigest() != pin:
        msg = "Recovery inventory differs from the pinned bytes"
        raise ValueError(msg)


def copy_generation(source: Path, destination: Path, pin: str) -> None:
    """Copy across devices; an interrupted destination has no completion manifest."""
    verify(source, pin)
    if source.stat().st_dev == destination.parent.stat().st_dev:
        msg = "Independent recovery cannot use the same filesystem"
        raise ValueError(msg)
    destination.mkdir(mode=0o700, exist_ok=False)
    for name, (size, checksum) in json.loads((source / MANIFEST).read_bytes())["files"].items():
        target = destination / name
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with (source / name).open("rb") as incoming, target.open("xb") as output:
            shutil.copyfileobj(incoming, output)
            output.flush()
            os.fsync(output.fileno())
        if target.stat().st_size != size or digest(target) != checksum:
            msg = f"Copy readback mismatch: {name}"
            raise ValueError(msg)
    if hashlib.sha256(canonical(destination)).hexdigest() != pin:
        msg = "Destination inventory did not match before sealing"
        raise ValueError(msg)
    if seal(destination) != pin:
        msg = "Destination manifest changed"
        raise ValueError(msg)
    verify(destination, pin)


def main() -> None:
    """Use a fresh destination and supply the source pin separately for each copy."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    for name in ("seal", "verify", "copy"):
        item = sub.add_parser(name)
        item.add_argument("source", type=Path)
        if name == "copy":
            item.add_argument("destination", type=Path)
        if name != "seal":
            item.add_argument("pin")
    args = parser.parse_args()
    if args.action == "seal":
        sys.stdout.write(seal(args.source) + "\n")
    elif args.action == "verify":
        verify(args.source, args.pin)
    else:
        copy_generation(args.source, args.destination, args.pin)


if __name__ == "__main__":
    main()
