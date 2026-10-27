"""Regression tests for research."""

import importlib
import math
from itertools import product
from typing import Never

import numpy as np
import pytest

from tobac._core import DecisionProblem, exact_evpi
from tobac.evidence import Belief, EvidencePacket, Scope, condition
from tobac.information import evaluate

SCOPE = Scope("fixture", "all", "2025-01-01", "2025-12-31", "exposure")


def problem(weights=(0.5, 0.5)):
    return DecisionProblem([[10.0, 0.0], [0.0, 10.0]], ("a", "b"), "unit", weights)


def module(name):
    assert importlib.util.find_spec("tobac.research") is not None, "M3 package not implemented"
    return importlib.import_module("tobac.research." + name)


def test_structure_only_identical_structures() -> None:
    m = module("structure")
    r = m.structure_value({"one": problem(), "two": problem()}, [0.3, 0.7])
    assert r["structure_only"] == pytest.approx(0)
    assert r["joint_perfect"] == pytest.approx(5)
    assert r["remaining_parameter_value"] == pytest.approx(5)


def test_structure_information_and_joint_chain() -> None:
    m = module("structure")
    q = DecisionProblem([[0, 8], [0, 8]], ("a", "b"), "unit", [0.1, 0.9])
    r = m.structure_value({"one": problem([0.9, 0.1]), "two": q}, [0.25, 0.75])
    assert r["structure_only"] > 0
    assert r["structure_only"] + r["remaining_parameter_value"] == pytest.approx(r["joint_perfect"])


@pytest.mark.parametrize("bad", ["unit", "actions", "weights"])
def test_structure_contract(bad) -> None:
    m = module("structure")
    q = problem()
    if bad == "unit":
        q = DecisionProblem(q.values, q.action_names, "different", q.prior_weights)
    if bad == "actions":
        q = DecisionProblem(q.values, ("b", "a"), "unit", q.prior_weights)
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Explicit\ normalised\ model\ probabilities\ required"
            r"|"
            r"Same\ ordered\ feasible\ actions\ and\ value\ units\ required"
            r")"
        ),
    ):
        m.structure_value({"one": problem(), "two": q}, [0.2, 0.2] if bad == "weights" else [0.5, 0.5])


@pytest.mark.parametrize("p", [[0.5, 0.5], [0.9, 0.1], [1.0, 0.0], [1e-8, 1 - 1e-8]])
def test_exact_weight_transform(p) -> None:
    m = module("voiage_adapter")
    x = problem(p)
    a = m.uniform_equivalent(x)
    oracle = float(np.mean(np.max(a, axis=1)) - np.max(np.mean(a, axis=0)))
    assert oracle == pytest.approx(exact_evpi(x), abs=1e-12)
    # This tests mathematics, not the installed library.
    assert a.shape == x.values.shape


def test_state_offsets_and_split_state_invariance() -> None:
    m = module("voiage_adapter")
    p = problem([0.8, 0.2])
    v = p.values + np.array([[1e8], [-1e8]])
    q = DecisionProblem(v, p.action_names, p.value_unit, p.prior_weights)
    a = m.uniform_equivalent(q)
    assert np.mean(a.max(1)) - a.mean(0).max() == pytest.approx(2.0)
    split = DecisionProblem([[10, 0], [10, 0], [0, 10]], ("a", "b"), "unit", [0.4, 0.4, 0.2])
    z = m.uniform_equivalent(split)
    assert np.mean(z.max(1)) - z.mean(0).max() == pytest.approx(2.0)


def portfolio_fixture():
    mod = module("portfolio")
    b = Belief(problem(), ("s0", "s1"), SCOPE)
    a = mod.Source("A", np.array([[0.8, 0.2], [0.2, 0.8]]), ("future_A",), ("s0", "s1"), ("lab",))
    c = mod.Source("B", np.array([[0.9, 0.1], [0.1, 0.9]]), ("future_B",), ("s0", "s1"), ("lab",))
    costs = mod.Costs("unit", {"A": 0.1, "B": 0.2}, {"lab": 0.5})
    return mod, b, a, c, costs


def test_portfolio_costs_and_negative_enbs() -> None:
    m, b, a, c, k = portfolio_fixture()
    r = m.portfolio_value(b, [a, c], k)
    assert r["cost"] == pytest.approx(0.8)
    assert r["enbs"] == pytest.approx(r["evsi"] - 0.8)
    r2 = m.portfolio_value(b, [a, c], k, existing_assets=("lab",))
    assert r2["cost"] == pytest.approx(0.3)
    assert m.portfolio_value(b, [], k)["enbs"] == 0
    costly = m.Costs("unit", {"A": 100, "B": 100}, {"lab": 0})
    assert m.portfolio_value(b, [a], costly)["enbs"] < 0


def test_correlated_duplicate_report_not_independent_replication() -> None:
    m, b, a, c, k = portfolio_fixture()
    dup = m.Source("B", a.likelihood, ("future_B",), a.state_ids, ("lab",))
    j = np.zeros((2, 2, 2))
    j[0, 0] = a.likelihood[0]
    j[1, 1] = a.likelihood[1]
    r = m.portfolio_value(b, [a, dup], k, joint=j)
    assert r["evsi"] == pytest.approx(m.portfolio_value(b, [a], k)["evsi"])
    with pytest.raises(
        ValueError,
        match=(r"^(?:Joint\ marginal\ differs\ from\ the\ declared\ source\ likelihood)"),
    ):
        m.portfolio_value(b, [a, c], k, joint=j)


def test_existing_evidence_cannot_be_sold_again() -> None:
    m, b, a, c, k = portfolio_fixture()
    packet = EvidencePacket(
        "e", a.data_ids, ("fixture",), b.state_ids, np.log(a.likelihood[0]), SCOPE, SCOPE, "binary"
    )
    post = condition(b, packet)
    with pytest.raises(
        ValueError,
        match=(r"^(?:Underlying\ data\ reused;\ a\ new\ citation\ does\ not\ create\ new\ evidence)"),
    ):
        m.portfolio_value(post, [a], k)
    assert m.portfolio_value(post, [c], k)["evsi"] == pytest.approx(
        evaluate(post.problem, c.likelihood)["evsi"]
    )


def test_calibration_complementarity_xor() -> None:
    m = module("portfolio")
    bits = np.array(list(product((0, 1), repeat=2)))
    truth = bits[:, 0]
    bias = bits[:, 1]
    b = Belief(
        DecisionProblem(np.column_stack([1 - truth, truth]), ("a", "b"), "unit"),
        tuple(f"s{i}" for i in range(4)),
        SCOPE,
    )
    chem = np.vstack([truth ^ bias == 0, truth ^ bias == 1]).astype(float)
    cal = np.vstack([bias == 0, bias == 1]).astype(float)
    a = m.Source("assay", chem, ("assay",), b.state_ids, ())
    c = m.Source("calibration", cal, ("cal",), b.state_ids, ())
    k = m.Costs("unit", {"assay": 0.0, "calibration": 0.0}, {})
    assert m.portfolio_value(b, [a], k)["evsi"] == pytest.approx(0.0)
    assert m.portfolio_value(b, [c], k)["evsi"] == pytest.approx(0.0)
    assert m.portfolio_value(b, [a, c], k)["evsi"] == pytest.approx(0.5)


def test_portfolio_scope_guards() -> None:
    m, b, a, _c, k = portfolio_fixture()
    with pytest.raises(
        ValueError,
        match=(r"^(?:Duplicate\ source\ name)"),
    ):
        m.portfolio_value(b, [a, a], k)
    with pytest.raises(
        ValueError,
        match=(r"^(?:Information\ and\ costs\ require\ the\ same\ declared\ unit)"),
    ):
        m.portfolio_value(b, [a], m.Costs("dollars", {"A": 0.1}, {}))
    with pytest.raises(
        ValueError,
        match=(r"^(?:Invalid\ state_ids)"),
    ):
        m.Source("bad", a.likelihood, ("d",), ("s0", "s0"), ())
    with pytest.raises(
        ValueError,
        match=(r"^(?:Finite\ nonnegative\ costs\ required)"),
    ):
        m.Costs("unit", {"A": -1}, {})


def test_unweighted_robust_envelope() -> None:
    m = module("robust")
    rows = [
        {"scenario": s, "design": d, "enbs": v, "value_unit": "unit"}
        for s, d, v in [("p", "a", 2), ("p", "b", 1), ("q", "a", -1), ("q", "b", 3)]
    ]
    r = m.envelope(rows)
    a = next(x for x in r if x["design"] == "a")
    b = next(x for x in r if x["design"] == "b")
    assert a["minimum_enbs"] == -1
    assert a["maximum_regret"] == 4
    assert b["positive_in_all_scenarios"]
    assert b["maximum_regret"] == 1
    with pytest.raises(
        ValueError,
        match=(r"^(?:Each\ scenario\ must\ evaluate\ the\ same\ designs)"),
    ):
        m.envelope(rows[:-1])


def test_implementation_four_cells() -> None:
    m = module("implementation")
    p = problem([0.8, 0.2])
    identity = np.broadcast_to(np.eye(2), (2, 2, 2)).copy()
    assert m.implementation_values(p, identity).values == pytest.approx(p.values)
    none = m.adoption_kernel(p, 0.0)
    z = m.implementation_values(p, none)
    assert exact_evpi(z) == pytest.approx(0)
    partial = m.implementation_values(p, m.adoption_kernel(p, 0.5))
    assert exact_evpi(partial) == pytest.approx(0.5 * exact_evpi(p))
    r = m.decomposition(p, m.adoption_kernel(p, 0.5))
    assert r["joint_gain"] == pytest.approx(
        r["information_at_current_implementation"]
        + r["implementation_at_current_information"]
        + r["interaction"]
    )


def test_uptake_trajectory_and_errors() -> None:
    m = module("implementation")
    assert m.discounted_uptake([1, 1, 1], [1, 1, 1]) == 1
    assert m.discounted_uptake([0, 0, 1], [1, 1, 1]) == pytest.approx(1 / 3)
    with pytest.raises(
        ValueError,
        match=(r"^(?:Matching\ uptake\ probabilities\ and\ nonnegative\ time\ weights\ required)"),
    ):
        m.discounted_uptake([0, 2], [1, 1])
    with pytest.raises(
        ValueError,
        match=(r"^(?:State/intended/realised\ probabilities\ must\ be\ stochastic)"),
    ):
        m.implementation_values(problem(), np.ones((2, 2, 2)))


def test_pilot_continue_stop_dominates_matched_fixed_options() -> None:
    m = module("staged")
    p = problem([0.8, 0.2])
    a = np.array([[0.8, 0.2], [0.2, 0.8]])
    b = np.array([[0.95, 0.05], [0.05, 0.95]])
    r = m.two_stage(p, a, b, pilot_cost=0.1, followup_cost=0.25, pilot_remaining=0.9, followup_remaining=0.7)
    assert r["adaptive_enbs"] >= r["pilot_only_enbs"] - 1e-12
    assert r["adaptive_enbs"] >= r["fixed_both_enbs"] - 1e-12
    assert r["best_with_no_study"] >= 0
    # exhaustive continuation subsets independently verify adaptive recursion
    branches = r["branches"]
    best = -math.inf
    for choices in product([False, True], repeat=len(branches)):
        val = -0.1 + sum(
            x["probability"] * (x["continue_value"] if c else x["stop_value"])
            for c, x in zip(choices, branches, strict=False)
        )
        best = max(best, val)
    assert r["adaptive_enbs"] == pytest.approx(best)


def test_staged_no_signal_and_repeat_report() -> None:
    m = module("staged")
    p = problem()
    r = m.two_stage(p, np.ones((1, 2)), np.ones((1, 2)), pilot_cost=0.1, followup_cost=0.1)
    assert r["adaptive_enbs"] == pytest.approx(-0.1)
    assert r["continue_probability"] == 0
    assert r["best_with_no_study"] == 0
    a = np.array([[0.8, 0.2], [0.2, 0.8]])
    j = np.zeros((2, 2, 2))
    j[0, 0] = a[0]
    j[1, 1] = a[1]
    r = m.two_stage(p, a, a, pilot_cost=0, followup_cost=0.1, joint=j)
    assert r["continue_probability"] == 0
    with pytest.raises(
        ValueError,
        match=(r"^(?:Nonnegative\ costs\ and\ chronological\ remaining\ fractions\ required)"),
    ):
        m.two_stage(p, a, a, pilot_cost=0, followup_cost=0, pilot_remaining=0.5, followup_remaining=0.8)


def test_partition_adapter_integrates_nuisance_before_maximising() -> None:
    m = module("voiage_adapter")
    p = DecisionProblem([[10, 0], [0, 10], [10, 0], [0, 10]], ("a", "b"), "unit", [0.15, 0.15, 0.35, 0.35])
    q = m.partition_problem(p, ["s1", "s1", "s2", "s2"])
    assert exact_evpi(q) == pytest.approx(0)
    assert exact_evpi(p) == pytest.approx(5)
    with pytest.raises(
        ValueError,
        match=(r"^(?:One\ partition\ label\ per\ state\ required)"),
    ):
        m.partition_problem(p, ["s1"])


def test_runner_smoke_and_nonoverwrite(tmp_path) -> None:
    m = module("runner")
    out = tmp_path / "m3"
    r = m.run("configs/m3_research.json", out, quick=True)
    assert r["all_invariants_passed"]
    assert (out / "manifest.json").is_file()
    assert r["external_libraries_executed"] is False
    with pytest.raises(FileExistsError):
        m.run("configs/m3_research.json", out, quick=True)


def test_genuine_qualification_reports_missing_library_without_substitution(tmp_path, monkeypatch) -> None:
    m = module("qualification")

    def absent(*args, **kwargs) -> Never:  # noqa: ARG001 -- Keep the injected fixture or execution-double call signature.
        from importlib.metadata import PackageNotFoundError  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

        raise PackageNotFoundError("voiage")  # noqa: EM101 -- Synthetic failure message in an execution double.

    monkeypatch.setattr(m, "installed_evpi", absent)
    result = m.qualify(tmp_path / "receipt.json")
    assert result["success"] is False
    assert result["installed_library_executed"] is False
    assert result["status"] == "blocked"
    assert (tmp_path / "receipt.json").is_file()


def test_staged_boolean_and_large_product_are_rejected() -> None:
    m = module("staged")
    p = problem()
    a = np.ones((1, 2))
    with pytest.raises(
        ValueError,
        match=(r"^(?:Numeric\ costs/times\ cannot\ be\ booleans)"),
    ):
        m.two_stage(p, a, a, pilot_cost=True, followup_cost=0)
    with pytest.raises(
        ValueError,
        match=(r"^(?:Exact\ staged\ outcome\ tensor\ exceeds\ memory\ contract)"),
    ):
        m.two_stage(p, np.ones((4000, 2)) / 4000, np.ones((4000, 2)) / 4000, pilot_cost=0, followup_cost=0)


def test_staged_value_matches_actual_selected_branches_near_tie() -> None:
    m = module("staged")
    p = problem()
    a = np.ones((1, 2))
    b = np.eye(2)
    r = m.two_stage(p, a, b, pilot_cost=0.0, followup_cost=5.0 - 5e-13)
    actual = sum(
        x["probability"] * (x["continue_value"] if x["continue"] else x["stop_value"]) for x in r["branches"]
    )
    assert r["adaptive_enbs"] == actual


def test_partition_and_structure_invariance_under_state_offsets() -> None:
    m = module("structure")
    p = problem([0.3, 0.7])
    q = DecisionProblem(p.values + np.array([[1e6], [-1e6]]), p.action_names, p.value_unit, p.prior_weights)
    a = m.structure_value({"x": p, "y": p}, [0.2, 0.8])
    b = m.structure_value({"x": q, "y": q}, [0.2, 0.8])
    assert b["structure_only"] == pytest.approx(a["structure_only"])
    assert b["joint_perfect"] == pytest.approx(a["joint_perfect"])


def test_state_dependent_implementation_can_have_signed_interaction() -> None:
    m = module("implementation")
    p = DecisionProblem([[10, 0], [9, 8]], ("a", "b"), "unit", [0.5, 0.5])
    k = np.array([[[1, 0], [0, 1]], [[0, 1], [1, 0]]], dtype=float)
    d = m.decomposition(p, k)
    assert d["implementation_at_current_information"] > 0
    assert d["interaction"] < 0
    assert d["joint_gain"] == pytest.approx(
        d["information_at_current_implementation"]
        + d["implementation_at_current_information"]
        + d["interaction"]
    )


def test_portfolio_stage_wrapper_charges_shared_assets_once_and_rejects_d0() -> None:
    _m, b, a, c, k = portfolio_fixture()
    st = module("staged")
    r = st.staged_portfolio(b, [a], [c], k)
    assert r["pilot_cost"] == pytest.approx(0.6)
    assert r["followup_incremental_cost"] == pytest.approx(0.2)
    packet = EvidencePacket(
        "e", a.data_ids, ("fixture",), b.state_ids, np.log(a.likelihood[0]), SCOPE, SCOPE, "binary"
    )
    with pytest.raises(
        ValueError,
        match=(r"^(?:Underlying\ data\ reused;\ a\ new\ citation\ does\ not\ create\ new\ evidence)"),
    ):
        st.staged_portfolio(condition(b, packet), [a], [c], k)


def test_cost_contract_cannot_be_mutated_after_validation() -> None:
    _m, _b, _a, _c, k = portfolio_fixture()
    with pytest.raises(TypeError):
        k.direct["A"] = -1.0
