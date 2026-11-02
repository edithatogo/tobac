"""Measure the effects of a fictional one-year change using a completed longitudinal attempt."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import scientific_lineage as lineage
from source_handoff import checked

YEAR = "2014"
MULTIPLIER = 2
COUNTS = (
    "legal_sales_cigarette_equivalent",
    "reported_signed_gap",
    "reported_upper_smoker_bound_consumption",
    "reported_lower_smoker_bound_consumption",
)


def changed_source(original: bytes, table: bytes) -> tuple[bytes, bytes]:
    """Double the integer counts within the single 2014 row. Percentages stay fixed."""
    lineage.compare_phyo(original, table)
    start = original.index(b'id="T2"')
    end = original.index(b"</table>", start)
    matches = list(re.finditer(rb"<tr[^>]*>\s*<td[^>]*>2014</td>.*?</tr>", original[start:end], re.DOTALL))
    if len(matches) != 1:
        msg = "Counterfactual requires exactly one 2014 source row"
        raise ValueError(msg)
    row = matches[0]

    def multiply(match: re.Match[str]) -> str:
        count = int(match.group().replace("\u2009", ""))
        return f"{MULTIPLIER * count:,}".replace(",", "\u2009")

    changed = re.sub(r"\d{1,3}(?:\u2009\d{3})+", multiply, row.group().decode()).encode()
    article = original[: start + row.start()] + changed + original[start + row.end() :]
    reader = csv.DictReader(io.StringIO(table.decode()))
    rows = list(reader)
    for entry in rows:
        if entry["year"] == YEAR:
            for field in COUNTS:
                entry[field] = str(MULTIPLIER * int(entry[field]))
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    derived = buffer.getvalue().encode()
    lineage.compare_phyo(article, derived)
    return article, derived


def execute(attempts: Path, wheel: Path, destination: Path) -> dict[str, Any]:
    """Re-execute only the scientifically affected runner in an independent directory."""
    _, factory, _ = lineage.moh.producer(wheel, lineage.ARCHIVE / "transformation-interface.json")
    runs = {name: lineage.load_run(attempts / name, factory) for name in lineage.RUNS}
    selected = lineage.affected_results(runs, lineage.PHYO)
    if set(selected) != {"longitudinal"}:
        msg = "Phyo original has an unexpected forward impact set"
        raise ValueError(msg)
    run = runs["longitudinal"]
    store = factory(attempts / "longitudinal/cas")
    original = store.verify(run["originals"][lineage.PHYO]).path.read_bytes()
    table = store.verify(run["inputs"][lineage.SUPPLY]).path.read_bytes()
    article, derived = changed_source(original, table)
    destination.mkdir(parents=True, exist_ok=False)
    for name, key in run["inputs"].items():
        source = checked(lineage.ROOT, name)
        target = destination / source.relative_to(lineage.ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(derived if name == lineage.SUPPLY else store.verify(key).path.read_bytes())
    script = destination / lineage.RUNS["longitudinal"][0]
    output = destination / "outputs"
    env = {
        **os.environ,
        "PYTHONPATH": str(destination / "src"),
        "GIT_CEILING_DIRECTORIES": str(destination.parent),
    }
    subprocess.run(  # noqa: S603 -- Reviewed runner bytes, selected interpreter, fixed arguments.
        [sys.executable, str(script), "--out", str(output)],
        cwd=destination,
        env=env,
        timeout=1800,
        check=True,
        stdout=subprocess.DEVNULL,
    )
    _, resulting = lineage.manifest_io(output)
    prior = run["outputs"]
    if prior.keys() != resulting.keys():
        msg = "Counterfactual produced a different output inventory"
        raise ValueError(msg)
    changed = sorted(path for path, sha in resulting.items() if prior[path] != "sha256:" + sha)
    if not any(p.endswith(".csv") for p in changed):
        msg = "The source perturbation changed no numerical table"
        raise ValueError(msg)
    return {
        "type": "fictional_source_sensitivity",
        "source": lineage.PHYO,
        "year": int(YEAR),
        "count_multiplier": MULTIPLIER,
        "original_object": run["originals"][lineage.PHYO],
        "changed_original_sha256": hashlib.sha256(article).hexdigest(),
        "changed_input_sha256": hashlib.sha256(derived).hexdigest(),
        "baseline_attempt": run["attempt_id"],
        "changed_outputs": changed,
        "identical_outputs": sorted(set(prior) - set(changed)),
        "changed_numeric_tables": [p for p in changed if p.endswith(".csv")],
        "scientific_qualification": False,
    }


def main() -> None:
    """Write the result only after the independent numerical execution succeeds."""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("attempts", "wheel", "out"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    receipt = execute(args.attempts.resolve(), args.wheel, args.out.resolve())
    with (args.out / "counterfactual.json").open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
