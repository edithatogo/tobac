#!/usr/bin/env python
"""Check that every Conductor track carries one consistent name across layers.

A track's canonical name is the ``title`` in its ``metadata.json``. The
``spec.md`` H1, the ``plan.md`` H1 and the matching ``##`` heading (or a
``Track:`` pointer) in ``conductor/tracks.md`` must agree with it.

Registry headings are matched to tracks by the folder path written in the
section's ``Track:`` line, not by the heading text, so renames stay verifiable.
Headings without a ``Track:`` pointer are reported as non-track sections and
need no title; they are listed rather than failed so that prose sections such as
the open-work list do not block the check.

Usage: python scripts/check_conductor_track_names.py [--verbose]
Exit status is non-zero when any live or archived track fails the check.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TRACK_LINE = re.compile(r"^Track:\s*`conductor/(?:tracks|archive)/([A-Za-z0-9_]+)/`")
HEADING = re.compile(r"^##\s+(?P<text>.+?)\s*$")
DATE_SUFFIX = re.compile(r"\s+[—-]\s+\d{1,2}\s+\w+\s+\d{4}\s*$")


def read_h1(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"{path}: no H1 heading")


def registry_headings(repo: Path) -> tuple[dict[str, str], list[str]]:
    """Map track_id -> registry heading text, using each section's Track: line.

    Returns the track mapping and the headings that carry no Track: pointer
    (non-track prose sections such as the open-work list).
    """
    sections: list[tuple[str | None, str | None]] = []
    pending: str | None = None
    for line in (repo / "conductor" / "tracks.md").read_text(encoding="utf-8").splitlines():
        match = HEADING.match(line)
        if match:
            pending = match.group("text")
            sections.append((pending, None))
            continue
        track = TRACK_LINE.match(line.strip())
        if track and sections and sections[-1][0] == pending:
            sections[-1] = (pending, track.group(1))

    mapping = {tid: text for text, tid in sections if tid is not None}
    unlinked = [text for text, tid in sections if tid is None]
    return mapping, unlinked


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv
    repo = Path(__file__).resolve().parents[1]
    registry, unlinked = registry_headings(repo)

    failures: list[str] = []
    checked = 0
    for base in (repo / "conductor" / "tracks", repo / "conductor" / "archive"):
        for meta_path in sorted(base.glob("*/metadata.json")):
            folder = meta_path.parent.name
            meta = json.loads(meta_path.read_text(encoding="utf-8"))

            declared = meta.get("track_id")
            title = meta.get("title")
            problems: list[str] = []

            if declared != folder:
                problems.append(f"metadata track_id {declared!r} != folder {folder!r}")
            if not title:
                problems.append("metadata has no 'title'")
                failures.append(f"{folder}: " + "; ".join(problems))
                continue

            spec_h1 = read_h1(meta_path.parent / "spec.md")
            if spec_h1 != title:
                problems.append(f"spec.md H1 {spec_h1!r} != metadata title {title!r}")

            heading = registry.get(folder)
            if heading is None:
                problems.append("no registry section has a Track: pointer to this folder")
            elif DATE_SUFFIX.sub("", heading) != title:
                problems.append(
                    f"registry heading {DATE_SUFFIX.sub('', heading)!r} != metadata title {title!r}"
                )

            checked += 1
            if problems:
                failures.append(f"{folder}: " + "; ".join(problems))
            elif verbose:
                print(f"ok  {folder}: {title}")

    for line in failures:
        print(f"FAIL {line}", file=sys.stderr)

    print(
        f"\n{checked - len(failures)}/{checked} tracks consistent; "
        f"{len(unlinked)} non-track registry heading(s): {', '.join(unlinked)}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
