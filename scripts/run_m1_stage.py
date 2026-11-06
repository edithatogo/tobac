"""Run the existing M1 analysis after attested input admission, publishing atomically."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


def execute(out: Path) -> None:
    """Preserve failed attempts and never expose partial output as completed work."""
    out = out.resolve()
    if not out.is_relative_to(ROOT / "outputs") or out == ROOT / "outputs" or out.exists():
        msg = "Select a new analysis directory under repository outputs"
        raise ValueError(msg)
    if sys.version_info[:3] != (3, 15, 1) or not Path(sys.prefix).resolve().is_relative_to(ROOT):
        msg = "Select repo-local Python 3.15.1"
        raise ValueError(msg)
    out.parent.mkdir(parents=True, exist_ok=True)
    attempt = uuid4().hex
    event = {"stage": "m1", "attempt": attempt, "time_utc": datetime.now(UTC).isoformat()}
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), OPENBLAS_NUM_THREADS="1", PYTHONHASHSEED="0")
    try:
        with tempfile.TemporaryDirectory(prefix="m1-stage-", dir=out.parent) as temporary:
            staged = Path(temporary) / "analysis"
            commands = [
                [sys.executable, "-I", "-S", str(ROOT / "scripts/hosted_lineage.py"), "--runner", "m1"],
                [sys.executable, "-m", "tobac.run", "--out", str(staged)],
                [sys.executable, str(ROOT / "scripts/verify.py"), str(staged)],
            ]
            for index, command in enumerate(commands):
                log = out.parent / f"m1-{attempt}-{index}.log"
                with log.open("w", encoding="utf-8") as stream:
                    subprocess.run(  # noqa: S603 -- Fixed repository entry points, selected local interpreter, no shell.
                        command, cwd=ROOT, env=env, check=True, stdout=stream, stderr=subprocess.STDOUT
                    )
            staged.rename(out)
        event["status"] = "passed"
    except Exception as error:
        event.update(status="failed", error_type=type(error).__name__)
        raise
    finally:
        with (out.parent / "analysis-events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event) + "\n")


def main() -> None:
    """Run one bounded caller-selected M1 output, with no arbitrary workload arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    execute(args.out)


if __name__ == "__main__":
    main()
