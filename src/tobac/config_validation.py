"""Fail early on invalid M1 scenario configuration; no empirical certification."""

from __future__ import annotations

import itertools
import math
from numbers import Real
from typing import cast

lazy from tobac._typing import Config

AXES = {
    "tobacco",
    "illicit",
    "other_nicotine",
    "restriction",
    "diversion",
    "cessation",
    "crime",
    "health",
    "mitigation",
    "yield",
    "supply_ratio",
    "unrecorded_lawful",
}
FRACTIONS = {"illicit", "restriction", "diversion", "cessation", "mitigation", "unrecorded_lawful"}
ACTIONS = {"reference", "retail_restriction", "restriction_plus_support", "expanded_cessation"}
CUTS = {
    "anabasine_cuts_ng_l",
    "improved_anabasine_cuts_ng_l",
    "nicotine_equivalent_cuts_ng_l",
    "legal_cuts_cigarettes_1000_day",
    "yield_cuts_ug_cigarette",
    "policy_ratio_cuts",
}
SDS = {"log_sd", "supply_log_sd", "calibration_log_sd", "policy_ratio_log_sd"}


# Named bounds preserve the existing scientific/data contract.
MIN_OBSERVATIONS = 2
MIN_DECISION_CONFIDENCE = 0.5


def number(x: float, name: str, *, positive: bool = False, upper: float | None = None) -> None:
    """Require a finite numeric value within the declared parameter domain."""
    if (
        isinstance(x, bool)
        or not isinstance(x, Real)
        or not math.isfinite(x)
        or (x <= 0 if positive else x < 0)
        or (upper is not None and x > upper)
    ):
        msg = f"Invalid {name}"
        raise ValueError(msg)


def validate_config(c: Config) -> Config:  # noqa: C901, PLR0912, PLR0915  # Keep ordered model validation and report assembly in one visible operation.; Keep explicit fail-closed validation branches together.; Keep the declared numerical/report sequence visible and ordered.
    """Validate the declared model configuration and supported parameter domains."""
    try:
        if c["schema"] != "tobac.regulatory-milestone.v1":
            msg = "Unknown regulatory schema"
            raise ValueError(msg)
        axes = c["axes"]
        ids = [a["id"] for a in axes]
        if len(ids) != len(set(ids)) or set(ids) != AXES:
            msg = "Unexpected/missing axes"
            raise ValueError(msg)
        supports: dict[str, list[float]] = {}
        for a in axes:
            values = a["values"]
            name = a["id"]
            if len(values) != MIN_OBSERVATIONS or values[0] == values[1]:
                msg = "Require distinct binary supports"
                raise ValueError(msg)
            for x in values:
                number(
                    x,
                    name,
                    positive=name in {"tobacco", "yield", "supply_ratio"},
                    upper=1 if name in FRACTIONS else None,
                )
            if not a["unit"].strip() or not a["group"].strip():
                msg = "Declare units and groups"
                raise ValueError(msg)
            supports[name] = values
        if max(supports["illicit"]) + max(supports["unrecorded_lawful"]) > 1:
            msg = "Illicit and unrecorded-lawful shares cannot exceed one"
            raise ValueError(msg)
        number(c["reference_exposure"], "reference exposure", positive=True)
        k = c["constants"]
        for name in ("population", "flow_l_per_person_day", "nicotine_mg_per_cigarette"):
            number(k[name], name, positive=True)
        for name in ("nicotine_recovery", "anabasine_survival"):
            number(k[name], name, positive=True, upper=1)
        if set(c["policy_costs"]) != ACTIONS:
            msg = "Policy cost/action mismatch"
            raise ValueError(msg)
        for name, x in c["policy_costs"].items():
            number(x, name + " resource cost")
        for name in CUTS:
            v = c["measurements"][name]
            if not isinstance(v, list) or not v:
                msg = "At least one cutpoint required"
                raise ValueError(msg)
            v = cast("list[float]", v)
            for x in v:
                number(x, name, positive=True)
            if any(b <= a for a, b in itertools.pairwise(v)):
                msg = "Cutpoints must increase strictly"
                raise ValueError(msg)
        for name in SDS:
            number(c["measurements"][name], name, positive=True)
        number(c["measurements"]["harm_classification_accuracy"], "classification accuracy", upper=1)
        for scenario in c["prior_scenarios"].values():
            if set(scenario) - AXES:
                msg = "Unknown prior axis"
                raise ValueError(msg)
            for x in scenario.values():
                number(x, "prior probability", positive=True, upper=1)
                if x == 1:
                    msg = "M1 requires interior prior probability"
                    raise ValueError(msg)
        for x in c["dependence_scenarios"].values():
            if isinstance(x, bool) or not isinstance(x, Real) or not math.isfinite(x):
                msg = "Invalid dependence"
                raise ValueError(msg)
        for x in c["crime_weights"]:
            number(x, "normative crime weight")
        for x in c["monetary_scales_nzd_per_unit"]:
            number(x, "monetary scale", positive=True)
        for x in c["conditional_study_cost_grid_nzd"]:
            number(x, "conditional study cost")
        number(c["scientific_event"]["minimum_absolute_growth_fraction"], "scientific threshold")
        if not MIN_DECISION_CONFIDENCE < c["scientific_event"]["confidence"] < 1:
            msg = "Invalid confidence threshold"
            raise ValueError(msg)
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        msg = "Malformed regulatory configuration"
        raise ValueError(msg) from exc
    return c
