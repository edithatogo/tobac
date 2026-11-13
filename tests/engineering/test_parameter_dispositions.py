"""Complete disposition accounting cannot create independent observations."""

import copy
import csv
import json
from pathlib import Path

import pytest

from scripts.reconcile_public_parameters import check_dispositions, run

ROOT = Path(__file__).resolve().parents[2]
TRACK = ROOT / "conductor/tracks/nz_au_empirical_20261106"


def packet():
    with (TRACK / "parameter-dispositions-20261113.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    bindings = json.loads((TRACK / "public-parameter-bindings-20261113.json").read_text())
    return rows, run(ROOT, bindings)


def test_every_unmatched_entry_has_one_source_preserving_disposition():
    rows, reconciliation = packet()
    result = check_dispositions(ROOT, rows, reconciliation["result"])
    assert result["candidate_entries"] == 45
    assert result["embedded_entries"] == 41
    assert result["independent_observations_added"] == 0


@pytest.mark.parametrize("change", ["missing", "duplicate", "wrong_source", "promoted", "different_value"])
def test_incomplete_or_false_reconciliation_fails(change):
    rows, reconciliation = copy.deepcopy(packet())
    if change == "missing":
        rows.pop()
    elif change == "duplicate":
        rows.append(rows[0])
    else:
        rows[0][
            {"wrong_source": "source_id", "promoted": "admission", "different_value": "value"}[change]
        ] = "wrong"
    with pytest.raises(ValueError, match=r"disposition|Disposition"):
        check_dispositions(ROOT, rows, reconciliation["result"])
