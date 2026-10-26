"""A prospective retail-licensing contrast, not a measured NZ causal effect.

Ait Ouakrim et al., doi:10.1136/tc-2022-057655, Table 2, use a
Beta(23.4,97.2) additional net-cessation input for ~300 outlets / 95% reduction.
It mixes previous modelling and stated intentions. It is NOT a likelihood of
current NZ outcomes and is not the M1 gross lawful-demand displacement fraction.
The ~600-outlet prospective case therefore retains explicit null/transport and
lawful-substitution scenarios. Equal smoking-intensity mapping is assumed.
"""

from __future__ import annotations

from copy import deepcopy
from itertools import product
from numbers import Integral
from typing import TYPE_CHECKING, cast

import numpy as np
from scipy.stats import beta

from ._core import DecisionProblem
from .information import joint_likelihood, lognormal_bins
from .regulation import ACTIONS, studies, study_channels

if TYPE_CHECKING:
    from tobac._typing import Config, FloatArray, StateArrays


# Named bounds preserve the existing scientific/data contract.
MAX_QUADRATURE_POINTS = 16


def build_retail_states(
    base_config: Config,
    *,
    quit_points: int = 4,
    transport: float = 1.0,
    null_weight: float = 0.2,
    source_beta: tuple[float, float] = (23.4, 97.2),
) -> tuple[StateArrays, FloatArray, Config]:
    """Expand retail cessation supports under explicit transport and null assumptions."""
    if (
        isinstance(quit_points, bool)
        or not isinstance(quit_points, Integral)
        or not 1 <= quit_points <= MAX_QUADRATURE_POINTS
        or not np.isfinite([transport, null_weight]).all()
        or not 0 <= transport <= 1
        or not 0 <= null_weight <= 1
    ):
        msg = "Declare finite bounded transport/null weight and 1..16 quantile nodes"
        raise ValueError(msg)
    a = np.asarray(source_beta, float)
    if a.shape != (2,) or not np.isfinite(a).all() or (a <= 0).any():
        msg = "Positive beta shape parameters required"
        raise ValueError(msg)
    quantiles = beta.ppf((np.arange(quit_points) + 0.5) / quit_points, float(a[0]), float(a[1])) * transport
    raw_values = np.r_[0.0, quantiles]
    raw_weights = np.r_[null_weight, np.repeat((1 - null_weight) / quit_points, quit_points)]
    values, inv = np.unique(raw_values, return_inverse=True)
    weights = cast("FloatArray", np.bincount(inv, weights=raw_weights))
    keep = weights > 0
    values = values[keep]
    weights = weights[keep]
    c = deepcopy(base_config)
    axes = c["axes"]
    idx = [x["id"] for x in axes].index("restriction")
    axes[idx] = {
        "id": "net_cessation",
        "values": values.tolist(),
        "unit": "additional net cessation fraction",
        "group": "behaviour",
        "status": "transported_model_input_plus_explicit_null",
        "source": "10.1136/tc-2022-057655 Table 2",
        (
            "rationale"
        ): "Equal-intensity consumption mapping; different outlet cap and period; not observed efficacy",
    }
    axes.append(
        {
            "id": "policy_supply_ratio",
            "values": [0.85, 1.15],
            "unit": "differential post/counterfactual lawful-supply bias multiplier",
            "group": "measurement",
            "status": "analyst_assumption",
            "rationale": "Uncertain policy-period supply reconciliation; not measured precision",
        }
    )
    index = np.array(list(product(*(range(len(x["values"])) for x in axes))))
    s = {axis["id"]: np.asarray(axis["values"], float)[index[:, j]] for j, axis in enumerate(axes)}
    p = np.ones(len(index))
    for j, axis in enumerate(axes):
        p *= weights[index[:, j]] if j == idx else 1 / len(axis["values"])
    p /= p.sum()
    c.update(
        schema="tobac.retail-case.v1",
        source_beta=a.tolist(),
        transport=transport,
        null_weight=null_weight,
        evidence_status="transported_published_model_input_not_causal_observation",
        time_scope="one-year prospective response; no lifetime health claim",
        policy_scope="smoked-tobacco retailer cap only; other policy components held constant",
    )
    return s, p, c


def retail_components(s: StateArrays, c: Config, *, lawful_replacement: float = 0.0) -> StateArrays:
    """Compute retail consequences under the declared cessation and replacement assumptions."""
    if not np.isfinite(lawful_replacement) or not 0 <= lawful_replacement <= 1:
        msg = "Lawful replacement fraction must be between zero and one"
        raise ValueError(msg)
    required = (
        "tobacco",
        "illicit",
        "net_cessation",
        "diversion",
        "mitigation",
        "cessation",
        "health",
        "crime",
    )
    arrays = {k: np.asarray(s[k], float) for k in required}
    shape = arrays["tobacco"].shape
    if (
        len(shape) != 1
        or not shape[0]
        or any(x.shape != shape or not np.isfinite(x).all() for x in arrays.values())
        or any((arrays[k] < 0).any() for k in required)
        or any(
            (arrays[k] > 1).any()
            for k in ("illicit", "net_cessation", "diversion", "mitigation", "cessation")
        )
    ):
        msg = "Finite state-aligned physical quantities/fractions required"
        raise ValueError(msg)
    t = arrays["tobacco"]
    i = t * arrays["illicit"]
    lawful = t - i
    remain = 1 - arrays["net_cessation"]
    switched = lawful * remain * arrays["diversion"]
    legal_r = lawful * remain - switched
    illicit_r = i * remain + switched
    removed = illicit_r * arrays["mitigation"]
    legal = np.column_stack(
        [lawful, legal_r, legal_r + removed * lawful_replacement, lawful * (1 - arrays["cessation"])]
    )
    illicit = np.column_stack([i, illicit_r, illicit_r - removed, i * (1 - arrays["cessation"])])
    total = legal + illicit
    norm = float(c["reference_exposure"])
    if not np.isfinite(norm) or norm <= 0:
        msg = "Positive reference exposure required"
        raise ValueError(msg)
    costs = np.broadcast_to([c["policy_costs"][a] for a in ACTIONS], total.shape).copy()
    if not np.isfinite(costs).all() or (costs < 0).any():
        msg = "Finite nonnegative resource scores required"
        raise ValueError(msg)
    return {
        "total": total,
        "legal": legal,
        "illicit": illicit,
        "illicit_share": np.divide(illicit, total, out=np.zeros_like(total), where=total > 0),
        "health_gain": arrays["health"][:, None] * (t[:, None] - total) / norm,
        "criminal_harm_change": arrays["crime"][:, None] * (illicit - i[:, None]) / norm,
        "resource_cost": costs,
        "fiscal_volume_change": legal - lawful[:, None],
    }


def retail_problem(
    states: StateArrays,
    prior: FloatArray,
    config: Config,
    crime_weight: float = 1.0,
    *,
    lawful_replacement: float = 0.0,
) -> DecisionProblem:
    """Construct the retail decision problem on the original consequence scale."""
    if not np.isfinite(crime_weight) or crime_weight < 0:
        msg = "Declare nonnegative normative weight"
        raise ValueError(msg)
    d = retail_components(states, config, lawful_replacement=lawful_replacement)
    values = d["health_gain"] - crime_weight * d["criminal_harm_change"] - d["resource_cost"]
    return DecisionProblem(values, ACTIONS, "normalised decision units; not NZD or QALYs", prior)


def retail_channels(s: StateArrays, c: Config) -> StateArrays:
    """Construct state-conditional retail report likelihoods under the shared contracts."""
    d = retail_components(s, c)
    ch = study_channels(s, c, policy_ratio=d["total"][:, 1] / s["tobacco"])
    # This report presupposes a matched causal comparison and accounting bridge.
    # It is NOT a chemical assay of illegality or an unadjusted release ratio.
    ratio = d["legal"][:, 1] / d["legal"][:, 0] * s["policy_supply_ratio"]
    ch["policy_lawful_comparison"] = lognormal_bins(ratio, 0.2, [0.2, 0.5, 0.8])
    return ch


def retail_studies(ch: StateArrays) -> StateArrays:
    """Combine only the declared coarsened retail report channels."""
    result = studies(ch)
    result["causal_matched_total_and_lawful"] = joint_likelihood(
        ch["policy_comparison"], ch["policy_lawful_comparison"]
    )
    result["panel_supply_and_matched_causal"] = joint_likelihood(
        ch["anabasine"],
        ch["nicotine"],
        ch["legal_supply"],
        ch["policy_comparison"],
        ch["policy_lawful_comparison"],
    )
    return result
