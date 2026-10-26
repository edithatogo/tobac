"""Compare actual stage-boundary recovery with uninterrupted native runner outputs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO
from unittest.mock import patch

from tobac import replay

ROOT = Path(__file__).resolve().parents[1]
STAGES = ("m1", "m2")


class BoundaryInterruptError(RuntimeError):
    """Deliberate harness interruption; never suppress a human interrupt."""


def qualify(out: Path) -> None:
    """Interrupt before the second native command; all completed commands are real."""
    out.mkdir(parents=True, exist_ok=False)
    resumed, uninterrupted = out / "resumed", out / "uninterrupted"
    original = subprocess.run
    calls = 0

    def interrupt(
        command: list[str],
        *,
        cwd: Path,
        stdout: TextIO,
        stderr: int,
        check: bool,
    ) -> subprocess.CompletedProcess[bytes]:
        nonlocal calls
        calls += 1
        if calls == len(STAGES):
            msg = "Deliberate interruption before second native stage"
            raise BoundaryInterruptError(msg)
        return original(command, cwd=cwd, stdout=stdout, stderr=stderr, check=check)

    with (
        patch.object(replay.subprocess, "run", interrupt),
        suppress(BoundaryInterruptError),
    ):
        replay.execute(ROOT, resumed, list(STAGES), quick=True)
    before = replay.sha(resumed / "m1.receipt.json")
    state = replay.execute(ROOT, resumed, ["m1", "m2"], quick=True, resume=True)
    if replay.sha(resumed / "m1.receipt.json") != before:
        msg = "Completed receipt changed during resume"
        raise AssertionError(msg)
    replay.execute(ROOT, uninterrupted, ["m1", "m2"], quick=True)
    compared = {}
    for stage in ("m1", "m2"):
        for path in (resumed / stage).glob("*.csv"):
            if path.read_bytes() != (uninterrupted / stage / path.name).read_bytes():
                msg = "Recovered native CSV differs from uninterrupted execution"
                raise AssertionError(msg)
            compared[f"{stage}/{path.name}"] = replay.sha(path)
    if not compared:
        msg = "No native output comparison executed"
        raise AssertionError(msg)
    result = {
        "schema": "tobac.recovery-qualification.v1",
        "completed": state["completed"],
        "scope": "native quick M1/M2 stage-boundary interruption; not mid-kernel recovery",
        "receipt_immutable": True,
        "csv_sha256": compared,
        "identity": replay.identities(ROOT),
        "qualifier_sha256": replay.sha(Path(__file__)),
        "command": [sys.executable, *sys.argv],
    }
    (out / "receipt.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    """Retain a fresh native comparison generation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    qualify(args.out)
    sys.stdout.write("Actual interrupted/resumed and uninterrupted native CSVs match\n")


if __name__ == "__main__":
    main()
