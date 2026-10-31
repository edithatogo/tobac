"""Compare a retained SHINE Table 2 model input with the existing consumer config.

The output is exploratory: it neither registers a native source nor establishes
source-version equivalence, a new observation, or scientific applicability.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "9d8fe4fca0e55129ebc9325edb93e2daf539e5328e48cb11e45ff4dfd943217e"
SOURCE_ID = "SHINE_RETAIL_TABLE2"
DOI = "10.1136/tc-2022-057655"
TRANSITION = "CS→FSFVCS→FSCVDU→FSFVDU→FSCV"
HEADER = "Retail outlet restriction to about 300 outlets"
PRIOR_SHA256 = "c97875c489e6759776aebf1b7d948603120c46914b13440493128ade93bcdd64"
EXPECTED_BETA = [23.4, 97.2]
EXPECTED_MEAN = "19.4"
EXPECTED_MEDIAN = "19.2"
EXPECTED_SD = "3.6"
EXPECTED_UI95 = ["12.9", "26.9"]
ROW_CELLS = 2
MAX_SOURCE_BYTES = 16 * 1024 * 1024


class TableParser(HTMLParser):
    """Collect body rows only in the specifically identified T2 section."""

    def __init__(self) -> None:
        """Initialize the section and cell state."""
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.sections = 0
        self.tables = 0
        self.in_body = False
        self.row: list[str] | None = None
        self.cell: list[str] | None = None
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Enter one T2 section and retain its table-body structure."""
        if tag == "section":
            if self.depth:
                self.depth += 1
            elif dict(attrs).get("id") == "T2":
                self.depth = 1
                self.sections += 1
        if not self.depth:
            return
        if tag == "table":
            self.tables += 1
        elif tag == "tbody":
            self.in_body = True
        elif tag == "tr" and self.in_body:
            self.row = []
        elif tag in {"td", "th"} and self.row is not None:
            self.cell = []

    def handle_data(self, data: str) -> None:
        """Collect text only from a table cell."""
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        """Close cells, body rows and the selected section."""
        if not self.depth:
            return
        if tag in {"td", "th"} and self.cell is not None and self.row is not None:
            self.row.append(re.sub(r"\s+", " ", " ".join(self.cell)).strip())
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        elif tag == "tbody":
            self.in_body = False
        elif tag == "section":
            self.depth -= 1


def _capture(pattern: str, text: str) -> tuple[str, ...]:
    found = list(re.finditer(pattern, text, re.IGNORECASE))
    if len(found) != 1:
        msg = "SHINE row has missing or ambiguous values"
        raise ValueError(msg)
    return found[0].groups()


def extract_table(raw: bytes) -> dict[str, Any]:
    """Extract only the retail cessation row with an independent fixed oracle."""
    text = raw.decode("utf-8", errors="strict")
    if DOI not in text or "Tobacco endgame intervention impacts" not in text:
        msg = "SHINE article identity does not match"
        raise ValueError(msg)
    parser = TableParser()
    parser.feed(text)
    headings = [i for i, row in enumerate(parser.rows) if len(row) == 1 and HEADER in row[0]]
    if parser.sections != 1 or parser.tables != 1 or len(headings) != 1:
        msg = "SHINE table or retail section is missing or ambiguous"
        raise ValueError(msg)
    start = headings[0] + 1
    end = next((i for i in range(start, len(parser.rows)) if len(parser.rows[i]) == 1), len(parser.rows))
    selected = [
        (i, row)
        for i, row in enumerate(parser.rows[start:end], start=start)
        if len(row) == ROW_CELLS and row[0].rstrip().endswith(TRANSITION)
    ]
    if len(selected) != 1:
        msg = "SHINE cessation row is missing or duplicated"
        raise ValueError(msg)
    index, row = selected[0]
    beta = _capture(r"X=beta\s*\(([^,]+),\s*([^)]+)\)", row[1])
    mean = _capture(r"mean at\s+([\d.]+)%", row[1])
    median = _capture(r"median\s+([\d.]+)%", row[1])
    sd = _capture(r"SD=([\d.]+)%", row[1])
    ui = _capture(r"UI:\s*([\d.]+)%\s*to\s*([\d.]+)%", row[1])
    if (
        list(beta) != [str(value) for value in EXPECTED_BETA]
        or mean[0] != EXPECTED_MEAN
        or median[0] != EXPECTED_MEDIAN
        or sd[0] != EXPECTED_SD
        or list(ui) != EXPECTED_UI95
    ):
        msg = "SHINE consumer metadata differs from the retained model input"
        raise ValueError(msg)
    return {
        "source_id": SOURCE_ID,
        "source_beta": list(beta),
        "mean_percent": mean[0],
        "median_percent": median[0],
        "sd_percentage_points": sd[0],
        "ui95_percent": list(ui),
        "locator": {
            "section": "T2",
            "retail_body_row": headings[0] + 1,
            "cessation_body_row": index + 1,
            "transition": TRANSITION,
        },
        "role": "published model input, not observed intervention effectiveness",
    }


def execute(source: Path, output: Path) -> dict[str, Any]:
    """Verify original source and consumer metadata without changing either."""
    if (
        source.is_symlink()
        or output.exists()
        or output.is_symlink()
        or not output.resolve().is_relative_to(ROOT / "outputs")
    ):
        msg = "SHINE requires a new private output and a non-symlink source"
        raise ValueError(msg)
    with source.open("rb") as stream:
        raw = stream.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        msg = "SHINE source bytes differ from the retained identity"
        raise ValueError(msg)
    config_raw = (ROOT / "configs/m2_retail.json").read_bytes()
    bindings_raw = (ROOT / "integration/archive/source-bindings.json").read_bytes()
    prior_raw = (ROOT / "evidence/m2/publication_20261028/model_input_check.json").read_bytes()
    from source_handoff import unique  # noqa: PLC0415

    config = json.loads(config_raw, object_pairs_hook=unique)
    bindings = json.loads(bindings_raw, object_pairs_hook=unique)
    prior = json.loads(prior_raw, object_pairs_hook=unique)
    entries = [x for x in bindings["sources"] if any(r["source_id"] == SOURCE_ID for r in x["references"])]
    if len(entries) != 1:
        msg = "SHINE source binding is missing or ambiguous"
        raise ValueError(msg)
    captures = [x for x in entries[0]["captures"] if x.get("sha256") == SOURCE_SHA256]
    if (
        len(captures) != 1
        or captures[0]["status"] != "source_html_identity_observed"
        or captures[0]["captured_at"] is not None
        or captures[0]["uri"] != "https://pmc.ncbi.nlm.nih.gov/articles/PMC11672025/"
        or entries[0]["redistribution_authorized"] is not False
    ):
        msg = "SHINE capture metadata differs from retained evidence"
        raise ValueError(msg)
    result = extract_table(raw)
    if (
        config["source_id"] != SOURCE_ID
        or config["source_status"] != "published_model_input_not_observed_efficacy"
        or config["source_beta"] != EXPECTED_BETA
        or prior["alpha"] != EXPECTED_BETA[0]
        or prior["beta"] != EXPECTED_BETA[1]
        or prior["current_original_sha256"] != PRIOR_SHA256
    ):
        msg = "SHINE consumer comparison or edition distinction failed"
        raise ValueError(msg)
    result.update(
        source_sha256=SOURCE_SHA256,
        previous_reference_sha256=prior["current_original_sha256"],
        same_source_version_assumed=False,
        original_captured_at=None,
        native_lineage_qualified=False,
        scientific_qualification=False,
        independent_empirical_observation=False,
        metadata_sha256={
            "config": hashlib.sha256(config_raw).hexdigest(),
            "bindings": hashlib.sha256(bindings_raw).hexdigest(),
            "prior_check": hashlib.sha256(prior_raw).hexdigest(),
        },
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    return result


def main() -> None:
    """Execute an explicit, private source comparison."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    execute(args.source, args.out)


if __name__ == "__main__":
    main()
