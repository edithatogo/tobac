"""Versioned serialization of the existing regulatory parameters, not a new model."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from tobac.config_validation import validate_config

FIELDS = {
    "measurements",
    "constants",
    "crime_weights",
    "reference_exposure",
    "scientific_event",
    "schema",
    "scope",
    "axes",
    "conditional_study_cost_grid_nzd",
    "measurement_status",
    "dependence_scenarios",
    "monetary_scales_nzd_per_unit",
    "prior_scenarios",
    "policy_costs",
}


SECTION_FIELDS = {
    "constants": {
        "flow_l_per_person_day",
        "population",
        "nicotine_mg_per_cigarette",
        "nicotine_recovery",
        "anabasine_survival",
    },
    "scientific_event": {"name", "minimum_absolute_growth_fraction", "confidence"},
    "measurements": {
        "anabasine_cuts_ng_l",
        "improved_anabasine_cuts_ng_l",
        "nicotine_equivalent_cuts_ng_l",
        "legal_cuts_cigarettes_1000_day",
        "yield_cuts_ug_cigarette",
        "log_sd",
        "supply_log_sd",
        "calibration_log_sd",
        "policy_ratio_cuts",
        "policy_ratio_log_sd",
        "harm_classification_accuracy",
    },
}
AXIS_FIELDS = {"id", "values", "unit", "group", "status", "rationale"}


def canonical(config: dict[str, Any]) -> bytes:
    """Validate and encode supplied parameters without mutating caller values."""
    if set(config) != FIELDS:
        msg = "Unexpected regulatory parameter fields"
        raise ValueError(msg)
    for name, fields in SECTION_FIELDS.items():
        if not isinstance(config[name], dict) or set(config[name]) != fields:
            msg = f"Unexpected {name} parameter fields"
            raise ValueError(msg)
    if any(set(axis) != AXIS_FIELDS for axis in config["axes"]):
        msg = "Unexpected axis parameter fields"
        raise ValueError(msg)
    # JSON serialization rejects nonfinite values and executable configuration.
    raw = json.dumps(config, sort_keys=True, allow_nan=False)
    result = validate_config(json.loads(raw))
    return json.dumps(
        result, sort_keys=True, allow_nan=False, separators=(",", ":")
    ).encode("utf-8")


def save_parameters(config: dict[str, Any], path: Path) -> str:
    """Write a new parameter generation; preserve existing files and metadata."""
    content = canonical(copy.deepcopy(config))
    record = {
        "schema": "tobac.parameters.v1",
        "model": "tobac.regulatory-milestone.v1",
        "parameters": json.loads(content),
        "parameter_sha256": hashlib.sha256(content).hexdigest(),
    }
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(record, stream, indent=2, allow_nan=False)
        stream.write("\n")
    return record["parameter_sha256"]


def load_parameters(path: Path) -> dict[str, Any]:
    """Reject unknown envelopes, changed content and unsupported schema versions."""
    record = json.loads(Path(path).read_text(encoding="utf-8"))
    expected = {"schema", "model", "parameters", "parameter_sha256"}
    if set(record) != expected:
        msg = "Unexpected parameter envelope fields"
        raise ValueError(msg)
    if (
        record["schema"] != "tobac.parameters.v1"
        or record["model"] != "tobac.regulatory-milestone.v1"
    ):
        msg = "Unsupported parameter/model schema"
        raise ValueError(msg)
    content = canonical(record["parameters"])
    if hashlib.sha256(content).hexdigest() != record["parameter_sha256"]:
        msg = "Parameter content hash mismatch"
        raise ValueError(msg)
    return json.loads(content)
