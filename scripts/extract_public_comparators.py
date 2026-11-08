"""Re-extract six published ABS comparison tables from an exact source snapshot.

The snapshot is downloaded separately into ignored scratch storage. This script
does not fetch data, fit a model, condition evidence or accept a revised source.
Source numbers retain their published precision and rounding differences.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from html.parser import HTMLParser
from pathlib import Path
from typing import override

ABS_HTML_SHA256 = "5c44569d62d15e840c8f8014d78d00bc296d32cf1f804141a8778767756a8379"
TABLE_NAMES = (
    "abs_nicotine_kg_quarterly.csv",
    "abs_expenditure_aud_million_quarterly.csv",
    "abs_expenditure_scenarios_quarterly.csv",
    "abs_price_indices_quarterly.csv",
    "abs_volume_indices_quarterly.csv",
    "abs_total_hfce_growth_annual.csv",
)
TABLE_COLUMNS = (6, 6, 5, 4, 3, 3)
QUARTERLY_ROWS = 38  # One header plus December 2016 through December 2025.
ANNUAL_ROWS = 9  # One header plus 2018 through 2025.


class PublishedTables(HTMLParser):
    """Collect HTML table cells without inferring chart values from images."""

    def __init__(self) -> None:
        """Start an empty table collection."""
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self.table: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Open table, row or cell scopes; ignore presentation attributes."""
        if tag == "table":
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in {"td", "th"} and self.row is not None:
            self.cell = []

    @override
    def handle_data(self, data: str) -> None:
        """Preserve displayed text from nested cell markup."""
        if self.cell is not None:
            self.cell.append(data)

    @override
    def handle_endtag(self, tag: str) -> None:
        """Close each scope and retain all completed table rows."""
        if tag in {"td", "th"} and self.cell is not None and self.row is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None and self.table is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def extract(source: Path, output: Path) -> None:
    """Verify original bytes and emit canonical CSVs, refusing existing files."""
    original = source.read_bytes()
    if hashlib.sha256(original).hexdigest() != ABS_HTML_SHA256:
        msg = "Source snapshot hash differs; review the source as a new version before extracting"
        raise ValueError(msg)
    parser = PublishedTables()
    parser.feed(original.decode("utf-8"))
    parser.close()
    if len(parser.tables) != len(TABLE_NAMES):
        msg = "Unexpected number of ABS tables"
        raise ValueError(msg)
    output.mkdir(parents=True, exist_ok=True)
    for index, (name, columns, table) in enumerate(
        zip(TABLE_NAMES, TABLE_COLUMNS, parser.tables, strict=True)
    ):
        expected_rows = ANNUAL_ROWS if index == len(TABLE_NAMES) - 1 else QUARTERLY_ROWS
        if len(table) != expected_rows or any(len(row) != columns for row in table):
            msg = f"Unexpected shape for {name}"
            raise ValueError(msg)
        table[0][0] = "period_as_published"
        for row in table[1:]:
            row[1:] = [cell.replace(",", "") for cell in row[1:]]
        with (output / name).open("x", encoding="utf-8", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerows(table)


def main() -> None:
    """Extract a versioned original snapshot to a new output directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--abs-html", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    extract(args.abs_html, args.out)


if __name__ == "__main__":
    main()
