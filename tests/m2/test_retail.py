"""Regression tests for retail."""

from pathlib import Path

import numpy as np
import pytest
from scipy.stats import beta

from tobac._core import exact_evpi
from tobac.information import evaluate
from tobac.regulation import load_config, studies, study_channels
from tobac.retail_case import build_retail_states, retail_components, retail_problem

C = load_config(Path(__file__).parents[2] / "configs/regulatory.json")


def test_distribution_is_published_model_input_not_likelihood() -> None:
    s, p, case = build_retail_states(C, quit_points=4, null_weight=0.2)
    q = np.unique(s["net_cessation"])
    assert q[0] == 0
    assert q[1:] == pytest.approx(beta.ppf((np.arange(4) + 0.5) / 4, 23.4, 97.2))
    assert p[s["net_cessation"] == 0].sum() == pytest.approx(0.2)
    assert p.sum() == pytest.approx(1)
    assert case["evidence_status"] == "transported_published_model_input_not_causal_observation"
    assert "restriction" not in s
    assert "restriction" in {a["id"] for a in C["axes"]}  # input untouched


def test_null_and_attenuated_source_shape() -> None:
    s, _p, _c = build_retail_states(C, quit_points=2, transport=0, null_weight=0.2)
    assert np.all(s["net_cessation"] == 0)
    s2, _, _ = build_retail_states(C, quit_points=2, transport=0.5, null_weight=0)
    assert max(s2["net_cessation"]) == pytest.approx(0.5 * beta.ppf(0.75, 23.4, 97.2))


def test_source_input_mean_and_ui_are_reproducible() -> None:
    assert beta.mean(23.4, 97.2) == pytest.approx(0.19403, abs=1e-5)
    assert beta.ppf([0.025, 0.975], 23.4, 97.2) == pytest.approx([0.129, 0.269], abs=0.001)


def example():
    return {
        "tobacco": np.array([100.0]),
        "illicit": np.array([0.2]),
        "net_cessation": np.array([0.2]),
        "diversion": np.array([0.5]),
        "mitigation": np.array([0.5]),
        "cessation": np.array([0.1]),
        "health": np.array([1.0]),
        "crime": np.array([1.0]),
    }


def test_net_quitting_and_legal_origin_change_are_separate() -> None:
    r = retail_components(example(), C, lawful_replacement=0)
    assert r["total"][0] == pytest.approx([100.0, 80.0, 56.0, 90.0])
    assert r["legal"][0] == pytest.approx([80.0, 32.0, 32.0, 72.0])
    assert r["illicit"][0] == pytest.approx([20.0, 48.0, 24.0, 18.0])
    assert np.allclose(r["total"], r["legal"] + r["illicit"])


def test_lawful_substitution_is_not_quitting() -> None:
    r = retail_components(example(), C, lawful_replacement=1)
    assert r["total"][0, 2] == pytest.approx(80.0)
    assert r["illicit"][0, 2] == pytest.approx(24.0)
    assert r["legal"][0, 2] == pytest.approx(56.0)
    assert r["health_gain"][0, 2] == pytest.approx(r["health_gain"][0, 1])


def test_illicit_share_can_increase_as_volume_decreases() -> None:
    s = example()
    s["net_cessation"] = np.array([0.8])
    s["diversion"] = np.array([0.1])
    r = retail_components(s, C)
    assert r["illicit_share"][0, 1] > 0.2
    assert r["illicit"][0, 1] < 20.0


@pytest.mark.parametrize(
    "changes",
    [
        {"quit_points": 0},
        {"quit_points": 2.5},
        {"null_weight": 1.1},
        {"transport": -1},
        {"transport": 2},
        {"source_beta": (0, 1)},
    ],
)
def test_invalid_prior_contract(changes) -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Declare\ finite\ bounded\ transport/null\ weight\ and\ 1\.\.16\ quantile"
            r"\ nodes"
            r"|"
            r"Positive\ beta\ shape\ parameters\ required"
            r")"
        ),
    ):
        build_retail_states(C, **changes)


def test_measurement_path_uses_correct_counterfactual_ratio() -> None:
    s, p, c = build_retail_states(C, quit_points=2)
    d = retail_components(s, c)
    ch = study_channels(s, c, policy_ratio=d["total"][:, 1] / s["tobacco"])
    pr = retail_problem(s, p, c)
    r = evaluate(pr, studies(ch)["panel_supply"], {"net_quitting": s["net_cessation"], "crime": s["crime"]})
    assert r["targets"]["net_quitting"]["eig_nats"] == pytest.approx(0, abs=1e-12)
    assert r["targets"]["crime"]["eig_nats"] == pytest.approx(0, abs=1e-12)
    assert r["evsi"] <= exact_evpi(pr) + 1e-12


def test_invalid_policy_inputs() -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:Lawful\ replacement\ fraction\ must\ be\ between\ zero\ and\ one)"),
    ):
        retail_components(example(), C, lawful_replacement=-1)
    s = example()
    s["net_cessation"] = np.array([1.2])
    with pytest.raises(
        ValueError,
        match=(r"^(?:Finite\ state\-aligned\ physical\ quantities/fractions\ required)"),
    ):
        retail_components(s, C)


def test_causal_total_response_does_not_identify_legal_origin() -> None:
    from tobac.retail_case import retail_channels, retail_studies  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    s, p, c = build_retail_states(C, quit_points=2)
    pr = retail_problem(s, p, c)
    designs = retail_studies(retail_channels(s, c))
    a = evaluate(pr, designs["causal_policy_study"], {"diversion": s["diversion"]})
    b = evaluate(pr, designs["causal_matched_total_and_lawful"], {"diversion": s["diversion"]})
    assert a["targets"]["diversion"]["eig_nats"] == pytest.approx(0, abs=1e-12)
    assert b["targets"]["diversion"]["eig_nats"] > 0
    assert b["evsi"] >= a["evsi"] - 1e-12
