"""Reject malformed scientific boundaries without inventing observations or tool execution."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import types

import numpy as np
import pytest

from tobac._core import (BiomarkerParameters, Catchment, DecisionProblem, Exposure,
                         LibraryUnavailable, exact_evpi, exact_partial_information)
from tobac.config_validation import validate_config
from tobac.evidence import Belief, EvidencePacket, Scope, condition, incremental_value, state_identifiers
from tobac.information import evaluate, joint_likelihood, label_codes, same_data_robustness
from tobac.regulation import load_config
from tobac.retail_case import build_retail_states, retail_components, retail_problem
from tobac.research.portfolio import Costs, Source, ids, joint_report, portfolio_value
from tobac.research.robust import envelope

ROOT = Path(__file__).resolve().parents[1]


def problem(weights=None):
    return DecisionProblem(np.array([[10., 0.], [0., 10.]]), ("a", "b"), "fixture units", weights)


@pytest.mark.parametrize("change", ["matrix", "actions", "unit", "weights", "overflow"])
def test_problem_rejects_invalid_shape_identity_units_and_mass(change):
    values = np.array([[10., 0.], [0., 10.]])
    names, unit, weights = ("a", "b"), "fixture units", None
    if change == "matrix": values = np.array([])
    elif change == "actions": names = ("a", "a")
    elif change == "unit": unit = ""
    elif change == "weights": weights = np.zeros(2)
    else: weights = np.array([1e308, 1e308])
    with np.errstate(over="ignore"), pytest.raises(ValueError):
        DecisionProblem(values, names, unit, weights)


@pytest.mark.parametrize("factory,args", [
    (Catchment, (True, 1.)), (Catchment, (1., -1.)),
    (Exposure, (1., .7, .4, 0.)), (BiomarkerParameters, (1., 1.1)),
])
def test_physical_parameters_reject_invalid_domains(factory, args):
    with pytest.raises(ValueError): factory(*args)


def test_partitions_reject_missing_states_and_unhashable_labels():
    for labels in [["a"], [[1], [2]]]:
        with pytest.raises(ValueError): exact_partial_information(problem(), labels)
    with pytest.raises(ValueError): label_codes([1], 2)


@pytest.mark.parametrize("change", ["schema", "unit", "policy", "cuts", "dependence", "missing"])
def test_configuration_rejects_semantic_and_structural_changes(change):
    cfg = json.loads((ROOT / "configs/regulatory.json").read_text())
    if change == "schema": cfg["schema"] = "unknown"
    elif change == "unit": cfg["axes"][0]["unit"] = ""
    elif change == "policy": cfg["policy_costs"].pop(next(iter(cfg["policy_costs"])))
    elif change == "cuts": cfg["measurements"]["anabasine_cuts_ng_l"] = []
    elif change == "dependence": cfg["dependence_scenarios"] = {"bad": float("nan")}
    else: del cfg["constants"]
    with pytest.raises(ValueError): validate_config(cfg)


@pytest.mark.parametrize("kind", ["confidence", "event", "channels", "memory"])
def test_information_checks_confidence_events_and_explicit_memory_guard(kind):
    with pytest.raises(ValueError):
        if kind == "confidence": evaluate(problem(), np.eye(2), confidence=.4)
        elif kind == "event": evaluate(problem(), np.eye(2), event=[0, .2])
        elif kind == "channels": joint_likelihood()
        else:
            # Two valid channels exceed the joint bound without allocating the tensor.
            channel = np.full((4000, 2), 1 / 4000)
            joint_likelihood(channel, channel)


@pytest.mark.parametrize("kind", ["shape", "reference", "candidate", "impossible"])
def test_common_data_robustness_requires_compatible_probabilities(kind):
    values = problem().values
    priors = [np.array([.5, .5]), np.array([.8, .2])]
    ref, likelihood, event = np.array([.5, .5]), np.eye(2), [0, 1]
    if kind == "shape": event = [0]
    elif kind == "reference": ref = np.array([.2, .2])
    elif kind == "candidate": priors[1] = np.array([.2, .2])
    else: priors[1] = np.array([1., 0.])
    with pytest.raises(ValueError): same_data_robustness(values, priors, ref, likelihood, event)


@pytest.mark.parametrize("states", [{}, {"x": [1.], "y": [1., 2.]}, {"x": [float("nan")]}])
def test_state_identity_rejects_missing_nonfinite_or_misaligned_coordinates(states):
    with pytest.raises(ValueError): state_identifiers(states)


def scope():
    return Scope("fixture", "fixture population", "2020-01-01", "2020-12-31", "fixture units")


def test_evidence_requires_typed_scope_and_unique_evidence_receipts():
    with pytest.raises(ValueError): Scope("x", "p", "invalid", "2020-01-01", "u")
    with pytest.raises(ValueError): Belief(problem(), ("one",), scope())
    with pytest.raises(ValueError):
        EvidencePacket("e", ("d",), ("s",), ("one", "two"), np.zeros(2), "bad", scope(), "fixture")
    belief = Belief(problem(), ("one", "two"), scope(), receipts=({"evidence_id": "e"},))
    packet = EvidencePacket("e", ("new data",), ("s",), ("one", "two"), np.zeros(2), scope(), scope(), "fixture")
    with pytest.raises(ValueError, match="identifier reused"): condition(belief, packet)
    with pytest.raises(ValueError): incremental_value(belief, np.eye(2))


def test_zero_probability_reports_keep_the_information_chain_valid():
    belief = Belief(problem(), ("one", "two"), scope())
    first = np.array([[1., 1.], [0., 0.]])
    result = incremental_value(belief, first, np.eye(2))
    assert result["expected_conditional_evsi"] == pytest.approx(5.)
    assert result["outcome_probabilities"][1] == 0.
    assert result["conditional_evsi"][1] == 0.


@pytest.mark.parametrize("kind", ["name", "cost_unit", "cost_ids", "asset", "twice", "missing", "overlap", "states", "tensor", "empty_tensor"])
def test_portfolios_reject_identity_cost_and_joint_tensor_violations(kind):
    b = Belief(problem(), ("one", "two"), scope())
    a = Source("a", np.eye(2), ("data",), b.state_ids)
    costs = Costs("fixture units", {"a": 1.}, {})
    with pytest.raises(ValueError):
        if kind == "name": Source("", np.eye(2), ("data",), b.state_ids)
        elif kind == "cost_unit": Costs("", {}, {})
        elif kind == "cost_ids": Costs("fixture units", {"": 1.}, {})
        elif kind == "asset": costs.price([a], ("missing",))
        elif kind == "twice": costs.price([a, a])
        elif kind == "missing": Costs("fixture units", {}, {}).price([a])
        elif kind == "overlap": portfolio_value(b, [a, Source("b", np.eye(2), ("data",), b.state_ids)], Costs("fixture units", {"a": 0., "b": 0.}, {}))
        elif kind == "states": portfolio_value(b, [Source("a", np.eye(2), ("data",), ("two", "one"))], costs)
        elif kind == "tensor": joint_report([a], 2, np.zeros((1, 2)))
        else: joint_report([], 2, np.eye(2))


@pytest.mark.parametrize("case", ["empty", "probabilities", "units", "duplicate"])
def test_scenario_envelopes_do_not_invent_probabilities_or_pool_incompatible_results(case):
    row = {"scenario": "s", "design": "d", "enbs": 1., "value_unit": "u"}
    rows = [row]
    if case == "empty": rows = []
    elif case == "probabilities": row["scenario_probability"] = .5
    elif case == "units": rows.append(dict(row, scenario="other", value_unit="other"))
    else: rows.append(dict(row))
    with pytest.raises(ValueError): envelope(rows)


@pytest.mark.parametrize("case", ["reference", "cost", "normative"])
def test_retail_consequences_reject_invalid_units_costs_and_normative_weights(case):
    states, prior, cfg = build_retail_states(load_config(ROOT / "configs/regulatory.json"), quit_points=1)
    if case == "reference": cfg["reference_exposure"] = 0.
    elif case == "cost": cfg["policy_costs"][next(iter(cfg["policy_costs"]))] = -1.
    with pytest.raises(ValueError):
        if case == "normative": retail_problem(states, prior, cfg, -1.)
        else: retail_components(states, cfg)


def test_backend_failures_are_explicit_and_protocol_double_checks_parity(monkeypatch):
    """This labelled protocol double is not installed-Voiage qualification."""
    with pytest.raises(ValueError): exact_evpi(problem(), backend="unknown")
    with pytest.raises(ValueError): exact_evpi(problem(np.array([.9, .1])), backend="voiage")
    monkeypatch.setitem(sys.modules, "voiage.analysis", None)
    with pytest.raises(LibraryUnavailable): exact_evpi(problem(), backend="voiage")
    from tobac.integrations import voiage_evpi
    analysis, schema = types.ModuleType("voiage.analysis"), types.ModuleType("voiage.schema")
    class ValueArray:
        @classmethod
        def from_numpy(cls, values, strategy_names=None): return values
    class DecisionAnalysis:
        result = 5.
        def __init__(self, values): self.values = values
        def evpi(self): return self.result
    analysis.DecisionAnalysis, schema.ValueArray = DecisionAnalysis, ValueArray
    monkeypatch.setitem(sys.modules, "voiage.analysis", analysis)
    monkeypatch.setitem(sys.modules, "voiage.schema", schema)
    assert voiage_evpi(problem().values, ["a", "b"]) == 5.
    DecisionAnalysis.result = 0.
    with pytest.raises(ArithmeticError): voiage_evpi(problem().values, ["a", "b"])
