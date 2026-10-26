"""Fail early on invalid M1 scenario configuration; no empirical certification."""

from __future__ import annotations

import math
from numbers import Real

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


def number(x, name, *, positive=False, upper=None):
    if (
        isinstance(x, bool)
        or not isinstance(x, Real)
        or not math.isfinite(x)
        or (x <= 0 if positive else x < 0)
        or (upper is not None and x > upper)
    ):
        raise ValueError(f"Invalid {name}")


def validate_config(c):
    try:
        if c["schema"] != "tobac.regulatory-milestone.v1":
            raise ValueError("Unknown regulatory schema")
        axes = c["axes"]
        ids = [a["id"] for a in axes]
        if len(ids) != len(set(ids)) or set(ids) != AXES:
            raise ValueError("Unexpected/missing axes")
        supports = {}
        for a in axes:
            values = a["values"]
            name = a["id"]
            if len(values) != 2 or values[0] == values[1]:
                raise ValueError("Require distinct binary supports")
            for x in values:
                number(
                    x,
                    name,
                    positive=name in {"tobacco", "yield", "supply_ratio"},
                    upper=1 if name in FRACTIONS else None,
                )
            if not a["unit"].strip() or not a["group"].strip():
                raise ValueError("Declare units and groups")
            supports[name] = values
        if max(supports["illicit"]) + max(supports["unrecorded_lawful"]) > 1:
            raise ValueError("Illicit and unrecorded-lawful shares cannot exceed one")
        number(c["reference_exposure"], "reference exposure", positive=True)
        k = c["constants"]
        for name in ("population", "flow_l_per_person_day", "nicotine_mg_per_cigarette"):
            number(k[name], name, positive=True)
        for name in ("nicotine_recovery", "anabasine_survival"):
            number(k[name], name, positive=True, upper=1)
        if set(c["policy_costs"]) != ACTIONS:
            raise ValueError("Policy cost/action mismatch")
        for name, x in c["policy_costs"].items():
            number(x, name + " resource cost")
        for name in CUTS:
            v = c["measurements"][name]
            if not isinstance(v, list) or not v:
                raise ValueError("At least one cutpoint required")
            for x in v:
                number(x, name, positive=True)
            if any(b <= a for a, b in zip(v, v[1:])):
                raise ValueError("Cutpoints must increase strictly")
        for name in SDS:
            number(c["measurements"][name], name, positive=True)
        number(c["measurements"]["harm_classification_accuracy"], "classification accuracy", upper=1)
        for scenario in c["prior_scenarios"].values():
            if set(scenario) - AXES:
                raise ValueError("Unknown prior axis")
            for x in scenario.values():
                number(x, "prior probability", positive=True, upper=1)
                if x == 1:
                    raise ValueError("M1 requires interior prior probability")
        for x in c["dependence_scenarios"].values():
            if isinstance(x, bool) or not isinstance(x, Real) or not math.isfinite(x):
                raise ValueError("Invalid dependence")
        for x in c["crime_weights"]:
            number(x, "normative crime weight")
        for x in c["monetary_scales_nzd_per_unit"]:
            number(x, "monetary scale", positive=True)
        for x in c["conditional_study_cost_grid_nzd"]:
            number(x, "conditional study cost")
        number(c["scientific_event"]["minimum_absolute_growth_fraction"], "scientific threshold")
        if not 0.5 < c["scientific_event"]["confidence"] < 1:
            raise ValueError("Invalid confidence threshold")
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise ValueError("Malformed regulatory configuration") from exc
    return c
