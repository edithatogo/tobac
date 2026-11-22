"""Build the checked-out Tobac wheel and record its installation hash."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Build without fetching dependencies and bind pip to the resulting bytes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    destination = parser.parse_args().destination.resolve()
    destination.mkdir(mode=0o700)
    subprocess.run(  # noqa: S603 -- Invoke the selected interpreter with fixed pip arguments.
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-index",
            "--no-deps",
            "--no-build-isolation",
            "--wheel-dir",
            str(destination),
            ".",
        ],
        cwd=ROOT,
        check=True,
    )
    (wheel,) = destination.glob("*.whl")
    with wheel.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    (destination / "requirements.txt").write_text(
        f"{wheel.as_uri()} --hash=sha256:{digest}\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
