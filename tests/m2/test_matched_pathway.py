"""Matched metadata must not promote unmatched public summaries to causal data."""

from dataclasses import replace

import pytest

from tobac.evidence import Scope
from tobac.matched import MatchedObservation, audit_pathway

CELLS = ("treated_before", "treated_after", "comparator_before", "comparator_after")


def fixtures():
    rows = []
    for cell in CELLS:
        after = cell.endswith("after")
        scope = Scope(
            cell.split("_")[0],
            "resident15plus",
            "2025-01-01" if after else "2024-01-01",
            "2026-01-01" if after else "2025-01-01",
            "grams/year",
        )
        rows.extend(
            MatchedObservation(
                f"{cell}:{quantity}",
                cell,
                quantity,
                scope,
                ("cigarettes", "RYO"),
                (f"{cell}:{quantity}",),
                "observation",
            )
            for quantity in ("total_consumption", "lawful_consumption")
        )
    return rows


def test_complete_metadata_is_not_empirical_qualification() -> None:
    report = audit_pathway(fixtures())
    assert report["status"] == "metadata_compatible"
    assert report["empirically_qualified"] is False
    assert report["conditioned"] is False


def test_public_prevalence_and_releases_do_not_supply_causal_cells() -> None:
    rows = [
        replace(fixtures()[0], cell="unassigned", quantity="prevalence"),
        replace(fixtures()[1], cell="unassigned", quantity="releases"),
    ]
    report = audit_pathway(rows)
    assert report["status"] == "blocked"
    assert len(report["missing_cells"]) == 8
    assert "treated_before:total_consumption:quantity_not_consumption" in report["gaps"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("population", "all purchasers"),
        ("unit", "percent"),
        ("geography", "other"),
        ("start", "2024-02-01"),
    ],
)
def test_pair_must_match_scope(field, value) -> None:
    rows = fixtures()
    rows[1] = replace(rows[1], scope=replace(rows[1].scope, **{field: value}))
    assert "treated_before:scope_mismatch" in audit_pathway(rows)["gaps"]


def test_products_role_and_shared_observation_rejection() -> None:
    rows = fixtures()
    rows[1] = replace(rows[1], products=("cigarettes",), role="posterior", data_ids=rows[0].data_ids)
    gaps = audit_pathway(rows)["gaps"]
    assert "treated_before:product_mismatch" in gaps
    assert f"{rows[1].observation_id}:role_not_observation" in gaps
    assert "shared_data_requires_joint_model" in gaps


def test_unknown_scope_and_empty_products_remain_gaps() -> None:
    rows = fixtures()
    rows[0] = replace(rows[0], scope=None, products=())
    assert f"{rows[0].observation_id}:scope_unknown" in audit_pathway(rows)["gaps"]
    assert f"{rows[0].observation_id}:products_unknown" in audit_pathway(rows)["gaps"]


def test_before_after_may_not_overlap_or_reverse() -> None:
    rows = fixtures()
    rows[2] = replace(rows[2], scope=rows[0].scope)
    rows[3] = replace(rows[3], scope=rows[1].scope)
    assert "treated:before_after_overlap_or_reverse" in audit_pathway(rows)["gaps"]


def test_comparator_must_use_same_windows() -> None:
    rows = fixtures()
    rows[4] = replace(rows[4], scope=replace(rows[4].scope, start="2024-02-01"))
    assert "before:comparison_window_mismatch" in audit_pathway(rows)["gaps"]


def test_duplicate_ids_and_cells_are_invalid_not_more_evidence() -> None:
    with pytest.raises(ValueError, match="unique"):
        audit_pathway(fixtures() + fixtures())
    with pytest.raises(ValueError, match="Duplicate cell"):
        audit_pathway([*fixtures(), replace(fixtures()[0], observation_id="new")])


def test_nonpositive_window_is_not_accepted() -> None:
    rows = fixtures()
    rows[0] = replace(rows[0], scope=replace(rows[0].scope, end="2024-01-01"))
    assert f"{rows[0].observation_id}:empty_period" in audit_pathway(rows)["gaps"]


def test_real_manifest_reports_all_missing_cells_and_no_update(monkeypatch) -> None:
    from pathlib import Path  # noqa: PLC0415 -- Keep runner imports at the tested boundary.

    monkeypatch.syspath_prepend(str(Path(__file__).parents[2] / "scripts"))
    import qualify_m2_pathway as runner  # noqa: PLC0415 -- Standalone script boundary.

    report = runner.build_report(runner.ROOT)
    assert report["status"] == "blocked"
    assert len(report["missing_cells"]) == 8
    assert not report["conditioned"]
    assert len(report["research_gaps"]) == 7


@pytest.mark.parametrize(
    "updates",
    [
        {"cell": "invented"},
        {"quantity": "profit"},
        {"data_ids": ()},
        {"data_ids": ("",)},
        {"products": ("",)},
        {"products": ("RYO", "RYO")},
        {"data_ids": ("same", "same")},
    ],
)
def test_malformed_declarations_fail(updates) -> None:
    with pytest.raises(ValueError, match=r"Declare|unique|nonempty"):
        replace(fixtures()[0], **updates)


def test_same_population_cannot_be_its_own_comparator() -> None:
    rows = fixtures()
    for i in range(4):
        rows[i + 4] = replace(rows[i + 4], scope=rows[i].scope)
    assert "before:comparison_scope_identical" in audit_pathway(rows)["gaps"]


def test_equivalent_iso_date_spellings_do_not_invert_period_order() -> None:
    rows = fixtures()
    for i in (2, 3):
        rows[i] = replace(rows[i], scope=replace(rows[i].scope, start="20250101"))
    assert "treated:before_after_overlap_or_reverse" not in audit_pathway(rows)["gaps"]


@pytest.fixture
def runner_case(tmp_path, monkeypatch):
    import json  # noqa: PLC0415 -- Standalone runner fixture.
    import shutil  # noqa: PLC0415 -- Copy only source-bound fixture inputs.
    from pathlib import Path  # noqa: PLC0415 -- Standalone runner fixture.

    root = Path(__file__).parents[2]
    monkeypatch.syspath_prepend(str(root / "scripts"))
    import qualify_m2_pathway as runner  # noqa: PLC0415 -- Standalone runner boundary.

    case = json.loads((root / runner.DEFAULT).read_text())
    names = [
        runner.DEFAULT,
        runner.SCHEMA,
        case["protocol"],
        "src/tobac/matched.py",
        "scripts/qualify_m2_pathway.py",
        *case["input_sha256"],
    ]
    for name in names:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target)
    return runner, case, tmp_path


def test_changed_source_bytes_fail_closed(runner_case) -> None:
    runner, case, root = runner_case
    (root / next(iter(case["input_sha256"]))).write_text("changed source")
    with pytest.raises(ValueError, match="hash mismatch"):
        runner.build_report(root)


def test_schema_rejects_silent_fields_and_duplicate_keys(runner_case) -> None:
    import json  # noqa: PLC0415 -- Test invalid ingress representations.

    import jsonschema  # noqa: PLC0415 -- Validate the actual runner schema.

    runner, case, root = runner_case
    case["observations"][0]["fitted"] = True
    path = root / runner.DEFAULT
    path.write_text(json.dumps(case))
    with pytest.raises(jsonschema.ValidationError, match="Additional properties"):
        runner.build_report(root)
    path.write_text('{"schema_version":1,"schema_version":2}')
    with pytest.raises(ValueError, match="Duplicate JSON"):
        runner.build_report(root)


def test_unknown_source_and_traversal_fail_closed(runner_case) -> None:
    import json  # noqa: PLC0415 -- Test declared source integrity.

    runner, case, root = runner_case
    case["observations"][0]["source_id"] = "not_declared"
    (root / runner.DEFAULT).write_text(json.dumps(case))
    with pytest.raises(ValueError, match="undeclared source"):
        runner.build_report(root)
    with pytest.raises(ValueError, match="Noncanonical"):
        runner.build_report(root, "../outside.json")


def test_command_refuses_overwrite(runner_case, monkeypatch) -> None:
    runner, _, root = runner_case
    output = root / "receipt.json"
    monkeypatch.setattr(runner, "ROOT", root)
    monkeypatch.setattr(runner, "checkout_identity", lambda _: {"commit": "synthetic", "tracked_status": ""})
    monkeypatch.setattr("sys.argv", ["qualify_m2_pathway", "--out", str(output)])
    runner.main()
    before = output.read_bytes()
    with pytest.raises(FileExistsError):
        runner.main()
    assert output.read_bytes() == before


def test_date_spelling_cannot_disguise_a_self_comparator() -> None:
    rows = fixtures()
    for i in range(4):
        scope = rows[i].scope
        rows[i + 4] = replace(rows[i + 4], scope=replace(scope, start=scope.start.replace("-", "")))
    assert "before:comparison_scope_identical" in audit_pathway(rows)["gaps"]
