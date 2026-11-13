"""Source-bound reconciliation rejects false equivalences and stale editions."""

import copy
import csv
import hashlib
import json
from pathlib import Path

import pytest

from scripts.reconcile_public_parameters import (
    MARKER,
    _article_dois,
    check_extracts,
    reconcile,
    run,
    verify_hashes,
)

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "evidence/parameter_candidates_20261109"
DESIGN = ROOT / "conductor/tracks/dynamic_frontier_20261108/design.md"


def inputs():
    registry = json.loads((PACK / "registry.json").read_text())
    found = MARKER.search(DESIGN.read_text())
    assert found is not None
    embedded = json.loads(found.group(1))
    with (PACK / "alias_crosswalk.csv").open(newline="") as stream:
        aliases = list(csv.DictReader(stream))
    return registry, embedded, aliases


def test_all_entries_have_matched_or_unresolved_disposition():
    result = reconcile(*inputs())
    assert len(result["aliases"]) == 20
    assert len(result["unmatched_candidate_ids"]) == 45
    assert len(result["unmatched_embedded_ids"]) == 41
    assert result["independent_observations_added"] == 0
    assert result["empirical_admission"] is False


@pytest.mark.parametrize("change", ["duplicate", "conversion", "source", "uncertainty", "value", "promoted"])
def test_false_equivalence_is_rejected(change):
    registry, embedded, aliases = copy.deepcopy(inputs())
    if change == "duplicate":
        aliases.append(aliases[0])
    elif change == "conversion":
        next(r for r in aliases if r["candidate_id"] == "WALKER_RD_NONNIC")[
            "candidate_to_embedded_multiplier"
        ] = "1"
    elif change == "source":
        aliases[0]["embedded_source"] = "ANOTHER_STUDY"
    else:
        row = next(r for r in registry["parameters"] if r["parameter_id"] == "BANKS_CURRENT")
        row[{"uncertainty": "interval_type", "value": "value", "promoted": "admission_status"}[change]] = {
            "uncertainty": "credible_interval_95",
            "value": 99,
            "promoted": "admitted",
        }[change]
    with pytest.raises(ValueError, match=r"Duplicate|Alias|boundary|uncertainty|Missing|Bind"):
        reconcile(registry, embedded, aliases)


def test_source_bytes_must_match_and_paths_stay_within_root(tmp_path):
    source = tmp_path / "source.json"
    source.write_text("original")
    expected = {"source.json": hashlib.sha256(source.read_bytes()).hexdigest()}
    verify_hashes(tmp_path, expected)
    source.write_text("changed")
    with pytest.raises(ValueError, match="stale"):
        verify_hashes(tmp_path, expected)
    with pytest.raises(ValueError, match=r"Duplicate|Alias|boundary|uncertainty|Missing|Bind"):
        verify_hashes(tmp_path, {"../outside.json": "0" * 64})
    with pytest.raises(ValueError, match=r"Duplicate|Alias|boundary|uncertainty|Missing|Bind"):
        run(tmp_path, {})


def test_extract_check_requires_exact_original_and_source_identity(tmp_path):

    registry, _, _ = inputs()
    entry = next(p for p in registry["parameters"] if p["parameter_id"] == "BANKS_CURRENT")
    original = tmp_path / "source.html"
    original.write_text('<html><meta name="citation_doi" content="10.1186/s12916-015-0281-z"></html>')
    row = dict(
        entry,
        original_file=original.name,
        original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
        doi="10.1186/s12916-015-0281-z",
        code_interface="src/tobac/health.py",
    )
    packet = {"records": [row]}
    assert check_extracts(ROOT, tmp_path, packet)["empirical_admission"] is False
    row["doi"] = "wrong-doi"
    with pytest.raises(ValueError, match="DOI"):
        check_extracts(ROOT, tmp_path, packet)
    row["doi"] = "10.1186/s12916-015-0281-z"
    row["value"] = 999
    with pytest.raises(ValueError, match="extraction conflict"):
        check_extracts(ROOT, tmp_path, packet)


def test_bibliography_doi_cannot_substitute_for_article_identity():

    original = '<html><meta name="citation_doi" content="wrong-doi"><p>10.1186/s12916-015-0281-z</p></html>'
    assert _article_dois(original) == {"wrong-doi"}


def test_matching_fractions_cannot_erase_changed_arm_counts():
    registry, embedded, aliases = inputs()
    arm = next(r for r in registry["parameters"] if r["parameter_id"] == "WALKER_PATCH")
    arm["numerator"], arm["denominator"] = 6, 250
    with pytest.raises(ValueError, match="count representation"):
        reconcile(registry, embedded, aliases)
