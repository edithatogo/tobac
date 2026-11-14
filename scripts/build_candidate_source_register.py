"""Convert a local source register into an explicitly provisional catalogue."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def build(source: Path, destination: Path) -> None:
    """Retain reported fields while leaving source review and admission open."""
    with source.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        if (
            not fields
            or "source_id" not in fields
            or any(not field for field in fields)
            or len(set(fields)) != len(fields)
        ):
            msg = "A source register needs unique columns and source_id"
            raise ValueError(msg)
        rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        msg = "Source register rows must match their column headings"
        raise ValueError(msg)
    identities = [str(row["source_id"]).strip() for row in rows]
    if any(not identity for identity in identities) or len(set(identities)) != len(identities):
        msg = "Source identifiers must be nonempty and unique"
        raise ValueError(msg)

    reported = [f"reported_{field}" for field in fields if field != "source_id"]
    output_fields = ["source_id", *reported, "source_review_status", "empirical_admission"]
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=output_fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = {"source_id": row["source_id"]}
            output.update({f"reported_{field}": row[field] for field in fields if field != "source_id"})
            output.update(source_review_status="pending", empirical_admission="false")
            writer.writerow(output)


def main() -> None:
    """Write a candidate catalogue from a user-selected source-register CSV."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Source-register CSV")
    parser.add_argument("--out", type=Path, required=True, help="Candidate catalogue CSV")
    args = parser.parse_args()
    build(args.input, args.out)


if __name__ == "__main__":
    main()
