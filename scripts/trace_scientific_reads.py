"""Execute one normal runner while observing repository input opens in its process."""

from __future__ import annotations

import hashlib
import json
import runpy
import sys
from pathlib import Path


def main() -> None:
    """Retain observed inputs after a successful normal entry point."""
    log, kind, target, *args = sys.argv[1:]
    root = Path.cwd()
    reads: dict[str, str] = {}
    hashing = False
    roots = {"configs", "data", "evidence", "integration", "engineering", "docs", "src", "scripts"}

    def observe(event: str, fields: tuple[object, ...]) -> None:
        nonlocal hashing
        if hashing or event != "open" or not isinstance(fields[0], str):
            return
        path = Path(fields[0]).absolute()
        if not path.is_relative_to(root):
            return
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] in roots and "__pycache__" not in rel.parts and path.is_file():
            key = rel.as_posix()
            if key not in reads:
                hashing = True
                try:
                    with path.open("rb") as source:
                        reads[key] = hashlib.file_digest(source, "sha256").hexdigest()
                finally:
                    hashing = False

    sys.addaudithook(observe)
    sys.argv = [target, *args]
    if kind == "-m":
        runpy.run_module(target, run_name="__main__", alter_sys=True)
    else:
        runpy.run_path(target, run_name="__main__")
    for module in tuple(sys.modules.values()):
        origin = getattr(module, "__file__", None)
        if isinstance(origin, str) and origin != __file__ and origin.endswith(".py"):
            observe("open", (origin,))
    with Path(log).open("x", encoding="utf-8") as stream:
        json.dump(reads, stream, sort_keys=True)


if __name__ == "__main__":
    main()
