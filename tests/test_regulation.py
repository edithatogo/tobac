"""Regression tests for regulation."""

from pathlib import Path

import numpy as np
import pytest

from tobac._core import exact_partial_information
from tobac.information import evaluate
from tobac.regulation import (
    build_states,
    grouped_labels,
    load_config,
    make_problem,
    policy_components,
    studies,
    study_channels,
)

CFG = Path(__file__).parents[1] / "configs/regulatory.json"


@pytest.fixture(scope="module")
def world():
    c = load_config(CFG)
    s, p = build_states(c)
    return c, s, p


def test_factored_state_counts_and_weights(world) -> None:
    c, s, p = world
    assert len(p) == 4096
    assert np.isclose(p.sum(), 1)
    assert np.all(p > 0)
    assert set(s) == {a["id"] for a in c["axes"]}


def test_policy_mass_balance_and_no_hidden_transfers(world) -> None:
    c, s, _p = world
    d = policy_components(s, c)
    assert np.allclose(d["total"], d["legal"] + d["illicit"])
    assert np.all(d["total"] >= 0)
    assert np.all(d["legal"] >= 0)
    assert np.all(d["illicit"] >= 0)
    assert np.allclose(d["total"][:, 0], s["tobacco"])
    assert np.allclose(d["illicit"][:, 0], s["tobacco"] * s["illicit"])
    assert np.all(d["illicit"][:, 1] >= d["illicit"][:, 0])
    assert np.all(d["total"][:, 1] <= d["total"][:, 0])
    assert np.allclose(d["health_gain"][:, 0], 0)
    assert not np.allclose(d["fiscal_volume_change"], d["criminal_harm_change"])


def test_chemistry_invariant_to_illicit_origin(world) -> None:
    c, s, p = world
    likelihood = study_channels(s, c)
    modified = {k: v.copy() for k, v in s.items()}
    modified["illicit"] = np.full(len(p), 0.18)
    l2 = study_channels(modified, c)
    assert np.array_equal(likelihood["anabasine"], l2["anabasine"])
    assert np.array_equal(likelihood["nicotine"], l2["nicotine"])
    assert not np.allclose(likelihood["legal_supply"], l2["legal_supply"])


def test_baseline_data_does_not_identify_independent_future_response(world) -> None:
    c, s, p = world
    likelihood = study_channels(s, c)
    pr = make_problem(s, p, c, crime_weight=1.0)
    result = evaluate(
        pr,
        studies(likelihood)["panel_supply"],
        {"behaviour": grouped_labels(s, c, "behaviour"), "crime": s["crime"]},
    )
    assert abs(result["targets"]["behaviour"]["eig_nats"]) < 1e-10
    assert abs(result["targets"]["crime"]["eig_nats"]) < 1e-10
    bound = exact_partial_information(pr, grouped_labels(s, c, "baseline_reachable"))
    assert result["evsi"] <= bound + 1e-10


def test_calibration_information_independently_does_not_choose_policy(world) -> None:
    c, s, p = world
    pr = make_problem(s, p, c, crime_weight=1.0)
    assert evaluate(pr, study_channels(s, c)["calibration"])["evsi"] == pytest.approx(0, abs=1e-10)


def test_lower_loq_is_a_refinement_not_magic_new_origin_channel(world) -> None:
    c, s, _p = world
    ch = study_channels(s, c)
    assert np.allclose(ch["anabasine_improved"][:2].sum(0), ch["anabasine"][0])
    assert np.allclose(ch["anabasine_improved"][2:], ch["anabasine"][1:])


def test_dependence_is_explicit(world) -> None:
    c, s, p = world
    _, p2 = build_states(c, association=0.7)
    assert not np.allclose(p, p2)
    assert np.isclose(p2.sum(), 1)
    for k in s:
        assert np.array_equal(s[k], build_states(c, association=0.7)[0][k])


def test_illicit_share_can_rise_while_absolute_quantity_falls() -> None:
    before_quantity, before_total = 10, 100
    after_quantity, after_total = 8, 50
    assert after_quantity / after_total > before_quantity / before_total
    assert after_quantity < before_quantity


def test_no_nzd_in_primary_value_unit(world) -> None:
    c, s, p = world
    assert make_problem(s, p, c).value_unit == "normalised decision units; not NZD or QALYs"


def test_bad_prior_rejected(world) -> None:
    c, _, _ = world
    with pytest.raises(
        ValueError,
        match=(r"^(?:Interior\ finite\ probabilities\ and\ association\ required)"),
    ):
        build_states(c, scenario={"illicit": 1.2})
    with pytest.raises(
        ValueError,
        match=(r"^(?:Unknown\ prior\ axis)"),
    ):
        build_states(c, scenario={"unknown": 0.2})


def test_null_criminal_harm_and_null_diversion_are_allowed(world) -> None:
    _, s, _ = world
    # Documented criminal participation does not establish positive marginal harm
    # under every policy; a restriction need not cause illicit switching.
    assert min(s["crime"]) == 0
    assert min(s["diversion"]) == 0
