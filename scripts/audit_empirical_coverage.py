"""Inventory accepted historical CSV bytes; never fit or admit empirical observations."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]
from source_handoff import checked, read, same_hash  # noqa: E402


def main() -> None:
    """Write a hash-bound scope audit from the existing consumer inventory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if sys.version_info[:3] != (3, 15, 2):
        msg = "This audit is qualified only on repository Python 3.15.2"
        raise ValueError(msg)
    inventory = read(checked(ROOT, "integration/archive/consumer-inputs.json"))
    selected = (
        "data/empirical_intake_20261024/nz_historical_legal_supply.csv",
        "data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv",
    )
    rows = []
    for name in selected:
        matches = [r for r in inventory["inputs"] if r["path"] == name]
        if len(matches) != 1:
            msg = f"Ambiguous or missing inventory entry: {name}"
            raise ValueError(msg)
        expected = matches[0]
        same_hash(ROOT, name, expected["sha256"])
        table = pl.read_csv(checked(ROOT, name))
        if table.height != expected["rows"] or table.columns != expected["columns"]:
            msg = f"Inventory structure mismatch: {name}"
            raise ValueError(msg)
        years = table["year"].to_list()
        if sorted(years) != list(range(min(years), max(years) + 1)):
            msg = f"Duplicate or missing annual periods: {name}"
            raise ValueError(msg)
        rows.append(
            {
                "path": name,
                "sha256": expected["sha256"],
                "rows": table.height,
                "years": years,
                "units": table["unit"].unique().sort().to_list(),
                "source_ids": table["source_id"].unique().sort().to_list(),
                "limitations": table["limitations"].unique().sort().to_list(),
                "role": expected["role"],
                "native_admission_checked": False,
                "new_observations_admitted": False,
            }
        )
    result = {
        "schema_version": 1,
        "scope": "historical_input_coverage_only_not_fit_or_scientific_acceptance",
        "timestamp": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "polars": pl.__version__,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "inventory_sha256": hashlib.sha256(
            checked(ROOT, "integration/archive/consumer-inputs.json").read_bytes()
        ).hexdigest(),
        "sources": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    sys.stdout.write(json.dumps({"output": str(args.out), "sources_checked": len(rows)}) + "\n")


if __name__ == "__main__":
    main()
