"""Explicit regulatory hypotheses and measurement paths for research screening.

All response, harm, cost and prior probabilities are scenarios, not fitted NZ
parameters. The unchanged predecessor's dimensioned signal function is reused.
Health/resource/criminal/fiscal components are separate; only an explicitly
chosen normative weight combines health and criminal consequences in a score.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

from tobac._core import BiomarkerParameters, Catchment, DecisionProblem, Exposure, predict_signals

from .config_validation import validate_config
from .information import joint_likelihood, lognormal_bins

ACTIONS = ("reference", "retail_restriction", "restriction_plus_support", "expanded_cessation")


def load_config(path: str | Path) -> dict:
    return validate_config(json.loads(Path(path).read_text(encoding="utf-8")))


def build_states(config: dict, scenario: dict | None = None, association: float = 0.0):
    axes = config["axes"]
    ids = [a["id"] for a in axes]
    overrides = scenario or {}
    if set(overrides) - set(ids):
        raise ValueError("Unknown prior axis")
    probs = np.array([overrides.get(n, 0.5) for n in ids], float)
    if (
        not np.isfinite(probs).all()
        or (probs <= 0).any()
        or (probs >= 1).any()
        or not np.isfinite(association)
    ):
        raise ValueError("Interior finite probabilities and association required")
    bits = np.array(list(product((0, 1), repeat=len(axes))))
    states = {a["id"]: np.asarray(a["values"], float)[bits[:, i]] for i, a in enumerate(axes)}
    weights = np.prod(np.where(bits, probs, 1 - probs), axis=1)
    # Joint dependence is a declared sensitivity; no correlation is fitted.
    z1 = 2 * bits[:, ids.index("illicit")] - 1
    z2 = 2 * bits[:, ids.index("diversion")] - 1
    logw = np.log(weights) + association * z1 * z2
    weights = np.exp(logw - logw.max())
    weights /= weights.sum()
    return states, weights


def policy_components(s: dict, c: dict) -> dict:
    t = s["tobacco"]
    i = t * s["illicit"]
    l = t - i
    removed = l * s["restriction"]
    diverted = removed * s["diversion"]
    illegal_restricted = i + diverted
    legal = np.column_stack([l, l - removed, l - removed, l * (1 - s["cessation"])])
    illicit = np.column_stack(
        [i, illegal_restricted, illegal_restricted * (1 - s["mitigation"]), i * (1 - s["cessation"])]
    )
    total = legal + illicit
    norm = c["reference_exposure"]
    health = s["health"][:, None] * (t[:, None] - total) / norm
    crime = s["crime"][:, None] * (illicit - i[:, None]) / norm
    costs = np.broadcast_to([c["policy_costs"][a] for a in ACTIONS], total.shape).copy()
    return {
        "total": total,
        "legal": legal,
        "illicit": illicit,
        "illicit_share": np.divide(illicit, total, out=np.zeros_like(total), where=total > 0),
        "health_gain": health,
        "criminal_harm_change": crime,
        "resource_cost": costs,
        # Cigarette-volume tax base only, NOT cash or a social resource gain.
        "fiscal_volume_change": legal - l[:, None],
    }


def make_problem(states, prior, config, crime_weight=1.0) -> DecisionProblem:
    if not np.isfinite(crime_weight) or crime_weight < 0:
        raise ValueError("Nonnegative normative weight required")
    d = policy_components(states, config)
    nb = d["health_gain"] - crime_weight * d["criminal_harm_change"] - d["resource_cost"]
    return DecisionProblem(nb, ACTIONS, "normalised decision units; not NZD or QALYs", prior)


def grouped_labels(states, config, group):
    if group == "baseline_reachable":
        ids = ["tobacco", "illicit", "other_nicotine", "yield", "supply_ratio", "unrecorded_lawful"]
    elif group == "all":
        ids = [a["id"] for a in config["axes"]]
    else:
        ids = [a["id"] for a in config["axes"] if a["group"] == group]
    if not ids:
        raise ValueError("Unknown uncertainty group")
    # Tuples deliberately repeat for all nuisance-state combinations.
    return list(zip(*(states[n].tolist() for n in ids), strict=True))


def study_channels(s, c, *, policy_ratio=None):
    k = c["constants"]
    m = c["measurements"]
    n = len(s["tobacco"])
    catchment = Catchment(k["population"], k["population"] * k["flow_l_per_person_day"])
    ana = np.empty(n)
    nic = np.empty(n)
    sales = np.empty(n)
    for j in range(n):
        exposure = Exposure(
            float(s["tobacco"][j]),
            float(s["illicit"][j]),
            float(s["unrecorded_lawful"][j]),
            float(s["other_nicotine"][j]),
            k["nicotine_mg_per_cigarette"],
        )
        parameters = BiomarkerParameters(
            float(s["yield"][j]), k["anabasine_survival"], k["nicotine_recovery"], 1.0
        )
        pred = predict_signals(exposure, catchment, parameters)
        ana[j] = pred["anabasine_ng_l"]
        nic[j] = pred["nicotine_equivalent_ng_l"]
        sales[j] = pred["recorded_legal_cigarettes_1000_day"] * s["supply_ratio"][j]
    ratio = (
        policy_components(s, c)["total"][:, 1] / s["tobacco"]
        if policy_ratio is None
        else np.asarray(policy_ratio, dtype=float)
    )
    if ratio.shape != (n,) or not np.isfinite(ratio).all() or (ratio <= 0).any():
        raise ValueError("Supply a positive state-aligned counterfactual consumption ratio")
    highcrime = s["crime"] == max(s["crime"])
    acc = m["harm_classification_accuracy"]
    highother = s["other_nicotine"] == max(s["other_nicotine"])
    harmpositive = np.where(highcrime, acc, 1 - acc)
    comp_positive = np.where(highother, 0.85, 0.15)  # assumed composition-survey accuracy
    return {
        "anabasine": lognormal_bins(ana, m["log_sd"], m["anabasine_cuts_ng_l"]),
        "anabasine_improved": lognormal_bins(ana, m["log_sd"], m["improved_anabasine_cuts_ng_l"]),
        "nicotine": lognormal_bins(nic, m["log_sd"], m["nicotine_equivalent_cuts_ng_l"]),
        "legal_supply": lognormal_bins(sales, m["supply_log_sd"], m["legal_cuts_cigarettes_1000_day"]),
        "calibration": lognormal_bins(s["yield"], m["calibration_log_sd"], m["yield_cuts_ug_cigarette"]),
        "policy_comparison": lognormal_bins(ratio, m["policy_ratio_log_sd"], m["policy_ratio_cuts"]),
        "criminal_harm_research": np.vstack([1 - harmpositive, harmpositive]),
        "product_composition": np.vstack([1 - comp_positive, comp_positive]),
    }


def studies(ch):
    """Each study returns one coarsened report; not a fitted sample-size design.

    policy_comparison presupposes an identifying counterfactual design. It is
    expressly NOT baseline wastewater, nor proof of identification in the field.
    Criminal-harm research has assumed classification performance, not an assay.
    """
    designs = {
        "none": [],
        "nicotine": ["nicotine"],
        "anabasine": ["anabasine"],
        "panel": ["anabasine", "nicotine"],
        "supply": ["legal_supply"],
        "panel_supply": ["anabasine", "nicotine", "legal_supply"],
        "better_quantification_supply": ["anabasine_improved", "nicotine", "legal_supply"],
        "calibration_panel_supply": ["calibration", "anabasine", "nicotine", "legal_supply"],
        "composition_panel_supply": ["product_composition", "anabasine", "nicotine", "legal_supply"],
        "causal_policy_study": ["policy_comparison"],
        "criminal_harm_study": ["criminal_harm_research"],
        "causal_and_harm": ["policy_comparison", "criminal_harm_research"],
        "linked_market_and_causal": ["anabasine", "nicotine", "legal_supply", "policy_comparison"],
    }
    n = np.asarray(next(iter(ch.values()))).shape[1]
    return {
        name: joint_likelihood(*(ch[k] for k in keys)) if keys else np.ones((1, n))
        for name, keys in designs.items()
    }
