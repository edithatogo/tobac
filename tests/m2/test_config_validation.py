"""Regression tests for config validation."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from tobac.regulation import load_config

BASE = json.loads((Path(__file__).parents[2] / "configs/regulatory.json").read_text())


@pytest.mark.parametrize(
    "kind",
    [
        "negative_tobacco",
        "fraction_above_one",
        "negative_harm",
        "nonfinite_cost",
        "negative_cost",
        "duplicate_support",
        "missing_axis",
        "invalid_share_sum",
        "descending_cuts",
        "zero_sd",
        "invalid_prior",
        "unknown_prior",
        "invalid_confidence",
        "zero_norm",
        "boolean_population",
    ],
)
def test_invalid_config_rejected_before_calculation(tmp_path, kind) -> None:  # noqa: C901, PLR0912 -- Explicit parametrized invalid-configuration matrix.
    c = deepcopy(BASE)
    a = {x["id"]: x for x in c["axes"]}
    if kind == "negative_tobacco":
        a["tobacco"]["values"][0] = -1
    elif kind == "fraction_above_one":
        a["diversion"]["values"][1] = 1.2
    elif kind == "negative_harm":
        a["crime"]["values"][0] = -0.1
    elif kind == "nonfinite_cost":
        c["policy_costs"]["reference"] = float("nan")
    elif kind == "negative_cost":
        c["policy_costs"]["reference"] = -1
    elif kind == "duplicate_support":
        a["yield"]["values"] = [1.0, 1.0]
    elif kind == "missing_axis":
        c["axes"] = c["axes"][:-1]
    elif kind == "invalid_share_sum":
        a["unrecorded_lawful"]["values"] = [0.1, 0.8]
    elif kind == "descending_cuts":
        c["measurements"]["yield_cuts_ug_cigarette"] = [2, 1]
    elif kind == "zero_sd":
        c["measurements"]["log_sd"] = 0
    elif kind == "invalid_prior":
        c["prior_scenarios"]["bad"] = {"crime": 1.0}
    elif kind == "unknown_prior":
        c["prior_scenarios"]["bad"] = {"unsupported": 0.5}
    elif kind == "invalid_confidence":
        c["scientific_event"]["confidence"] = 1.0
    elif kind == "zero_norm":
        c["reference_exposure"] = 0
    elif kind == "boolean_population":
        c["constants"]["population"] = True
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(c))
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Cutpoints\ must\ increase\ strictly"
            r"|"
            r"Illicit\ and\ unrecorded\-lawful\ shares\ cannot\ exceed\ one"
            r"|"
            r"Invalid\ confidence\ threshold"
            r"|"
            r"Invalid\ crime"
            r"|"
            r"Invalid\ diversion"
            r"|"
            r"Invalid\ log_sd"
            r"|"
            r"Invalid\ population"
            r"|"
            r"Invalid\ reference\ exposure"
            r"|"
            r"Invalid\ reference\ resource\ cost"
            r"|"
            r"Invalid\ tobacco"
            r"|"
            r"M1\ requires\ interior\ prior\ probability"
            r"|"
            r"Require\ distinct\ binary\ supports"
            r"|"
            r"Unexpected/missing\ axes"
            r"|"
            r"Unknown\ prior\ axis"
            r")"
        ),
    ):
        load_config(path)
