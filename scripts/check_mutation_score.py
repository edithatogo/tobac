#!/usr/bin/env python
"""Fail when the mutation score falls below an explicit floor.

mutmut prints its results and exits 0 no matter how many mutants survived,
so a Nox session that only runs ``mutmut run`` and ``mutmut results`` reports
success even when most mutants live. This script reads the per-source-file
``mutants/<path>.meta`` records that ``mutmut run`` writes and turns the survivor
count into a non-zero exit status.

The status vocabulary and its exit-code mapping are mutmut's own
(``status_by_exit_code``, currently defined in ``mutmut/stats.py``); this script
reads the recorded exit codes rather than re-deriving pass/fail itself.

The floor is a regression alarm, not a claim of test adequacy: the measured score
on ``src/tobac/supply.py`` was 61.7% at main ``5ab361b``.

Usage: python scripts/check_mutation_score.py --minimum 60
Exit status is non-zero when the score is below the floor or no results exist.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# mutmut's own exit-code -> status mapping (mutmut/stats.py, status_by_exit_code).
# Exit code 3 is "internal error in pytest means a kill", so it counts as killed.
# Codes not listed here map to mutmut's "suspicious" default, as it does for unknown codes.
# The timeout/segfault codes are asymmetric in mutmut and are mirrored faithfully rather
# than "corrected": -24 is classed as timeout while +24 is SIGXCPU, which reads like a sign
# error upstream, but the killed set below is unaffected either way.
STATUS_BY_EXIT_CODE = {
    1: "killed",
    3: "killed",
    0: "survived",
    5: "no tests",
    2: "check was interrupted by user",
    None: "not checked",
    33: "no tests",
    34: "skipped",
    35: "suspicious",
    36: "timeout",
    37: "caught by type check",
    -24: "timeout",
    24: "timeout",
    152: "timeout",
    255: "timeout",
    -11: "segfault",
    -9: "segfault",
}
KILLED_STATUSES = {"killed"}
# Mutants that could not be assessed are excluded from the denominator rather than
# silently counted as either a kill or a survivor. The mutation set is
# ``src/tobac/supply.py`` (``[tool.mutmut] only_mutate``), which contains only value and
# control-flow logic, so "caught by type check" does not arise here and stays a non-kill.
EXCLUDED_STATUSES = {"not checked", "check was interrupted by user"}


def read_statuses(mutants_dir: Path) -> Counter[str]:
    """Count mutant statuses across every ``*.meta`` file mutmut wrote."""
    counts: Counter[str] = Counter()
    for meta_path in sorted(mutants_dir.rglob("*.meta")):
        counts.update(_statuses_in(meta_path))
    return counts


def _statuses_in(meta_path: Path) -> Counter[str]:
    """Return the status counts recorded in one mutmut ``.meta`` file."""
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL unreadable mutation record {meta_path}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    recorded = meta.get("exit_code_by_key", {})
    return Counter(STATUS_BY_EXIT_CODE.get(code, "suspicious") for code in recorded.values())


def main(argv: list[str]) -> int:
    """Compare the recorded mutation score with the requested floor."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimum", type=float, required=True,
                        help="minimum acceptable mutation score in percent")
    parser.add_argument("--mutants-dir", type=Path, default=Path("mutants"),
                        help="directory written by 'mutmut run'")
    args = parser.parse_args(argv)

    counts = read_statuses(args.mutants_dir)
    assessed = sum(n for status, n in counts.items() if status not in EXCLUDED_STATUSES)
    if assessed == 0:
        print(f"FAIL no mutation results under {args.mutants_dir}; run the mutation session first",
              file=sys.stderr)
        return 1

    killed = sum(n for status, n in counts.items() if status in KILLED_STATUSES)
    score = killed / assessed * 100
    detail = ", ".join(f"{status}={n}" for status, n in sorted(counts.items()))
    print(f"mutation score {score:.1f}% ({killed}/{assessed} killed)")
    print(f"statuses: {detail}")

    survived = counts.get("survived", 0)
    if score < args.minimum:
        print(f"FAIL mutation score {score:.1f}% is below the minimum {args.minimum:.1f}% "
              f"({survived} survived)", file=sys.stderr)
        return 1
    print(f"OK mutation score meets the {args.minimum:.1f}% floor ({survived} survived)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
