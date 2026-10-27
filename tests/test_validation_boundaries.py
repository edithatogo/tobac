"""Reject malformed scientific boundaries without inventing observations or tool execution."""

import json
import sys
import types
from pathlib import Path

import numpy as np
import pytest

from tobac._core import (
    BiomarkerParameters,
    Catchment,
    DecisionProblem,
    Exposure,
    LibraryUnavailable,
    exact_evpi,
    exact_partial_information,
)
from tobac.config_validation import validate_config
from tobac.evidence import Belief, EvidencePacket, Scope, condition, incremental_value, state_identifiers
from tobac.information import evaluate, joint_likelihood, label_codes, same_data_robustness
from tobac.regulation import load_config
from tobac.research.portfolio import Costs, Source, joint_report, portfolio_value
from tobac.research.robust import envelope
from tobac.retail_case import build_retail_states, retail_components, retail_problem

ROOT = Path(__file__).resolve().parents[1]


def problem(weights=None):
    return DecisionProblem(np.array([[10.0, 0.0], [0.0, 10.0]]), ("a", "b"), "fixture units", weights)


@pytest.mark.parametrize("change", ["matrix", "actions", "unit", "weights", "overflow"])
def test_problem_rejects_invalid_shape_identity_units_and_mass(change) -> None:
    values = np.array([[10.0, 0.0], [0.0, 10.0]])
    names, unit, weights = ("a", "b"), "fixture units", None
    if change == "matrix":
        values = np.array([])
    elif change == "actions":
        names = ("a", "a")
    elif change == "unit":
        unit = ""
    elif change == "weights":
        weights = np.zeros(2)
    else:
        weights = np.array([1e308, 1e308])
    with (
        np.errstate(over="ignore"),
        pytest.raises(
            ValueError,
            match=(
                r"^(?:"
                r"Action\ names\ must\ be\ unique\ and\ match\ value\ columns"
                r"|"
                r"Declare\ a\ value\ unit"
                r"|"
                r"Prior\ weights\ must\ be\ nonnegative,\ finite\ and\ have\ positive\ mas"
                r"s"
                r"|"
                r"Values\ must\ be\ a\ non\-empty\ finite\ state\-by\-action\ matrix"
                r"|"
                r"Weight\ sum\ overflow"
                r")"
            ),
        ),
    ):
        DecisionProblem(values, names, unit, weights)


@pytest.mark.parametrize(
    ("factory", "args"),
    [
        (Catchment, (True, 1.0)),
        (Catchment, (1.0, -1.0)),
        (Exposure, (1.0, 0.7, 0.4, 0.0)),
        (BiomarkerParameters, (1.0, 1.1)),
    ],
)
def test_physical_parameters_reject_invalid_domains(factory, args) -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Illicit\ plus\ unrecorded\ lawful\ shares\ exceed\ one"
            r"|"
            r"anabasine_survival\ is\ outside\ its\ permitted\ range"
            r"|"
            r"flow_l_day\ is\ outside\ its\ permitted\ range"
            r"|"
            r"population\ must\ be\ a\ finite\ number"
            r")"
        ),
    ):
        factory(*args)


def test_partitions_reject_missing_states_and_unhashable_labels() -> None:
    for labels in [["a"], [[1], [2]]]:
        with pytest.raises(
            ValueError,
            match=(
                r"^(?:"
                r"Group\ labels\ must\ match\ the\ state\ count"
                r"|"
                r"Partition\ labels\ must\ be\ hashable"
                r")"
            ),
        ):
            exact_partial_information(problem(), labels)
    with pytest.raises(
        ValueError,
        match=(r"^(?:Target\ labels\ require\ one\ scalar\ or\ tuple\ per\ state)"),
    ):
        label_codes([1], 2)


@pytest.mark.parametrize("change", ["schema", "unit", "policy", "cuts", "dependence", "missing"])
def test_configuration_rejects_semantic_and_structural_changes(change) -> None:
    cfg = json.loads((ROOT / "configs/regulatory.json").read_text())
    if change == "schema":
        cfg["schema"] = "unknown"
    elif change == "unit":
        cfg["axes"][0]["unit"] = ""
    elif change == "policy":
        cfg["policy_costs"].pop(next(iter(cfg["policy_costs"])))
    elif change == "cuts":
        cfg["measurements"]["anabasine_cuts_ng_l"] = []
    elif change == "dependence":
        cfg["dependence_scenarios"] = {"bad": float("nan")}
    else:
        del cfg["constants"]
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"At\ least\ one\ cutpoint\ required"
            r"|"
            r"Declare\ units\ and\ groups"
            r"|"
            r"Invalid\ dependence"
            r"|"
            r"Malformed\ regulatory\ configuration"
            r"|"
            r"Policy\ cost/action\ mismatch"
            r"|"
            r"Unknown\ regulatory\ schema"
            r")"
        ),
    ):
        validate_config(cfg)


@pytest.mark.parametrize("kind", ["confidence", "event", "channels", "memory"])
def test_information_checks_confidence_events_and_explicit_memory_guard(kind) -> None:
    def invalid_input() -> None:
        if kind == "confidence":
            evaluate(problem(), np.eye(2), confidence=0.4)
        elif kind == "event":
            evaluate(problem(), np.eye(2), event=[0, 0.2])
        elif kind == "channels":
            joint_likelihood()
        else:
            # Two valid channels exceed the joint bound without allocating the tensor.
            channel = np.full((4000, 2), 1 / 4000)
            joint_likelihood(channel, channel)

    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"At\ least\ one\ channel\ is\ needed"
            r"|"
            r"Confidence\ must\ lie\ strictly\ between\ \.5\ and\ 1"
            r"|"
            r"Joint\ outcome\ space\ exceeds\ the\ explicit\ memory\ guard"
            r"|"
            r"The\ scientific\ event\ must\ be\ a\ Boolean\ state\ vector"
            r")"
        ),
    ):
        invalid_input()


@pytest.mark.parametrize("kind", ["shape", "reference", "candidate", "impossible"])
def test_common_data_robustness_requires_compatible_probabilities(kind) -> None:
    values = problem().values
    priors = [np.array([0.5, 0.5]), np.array([0.8, 0.2])]
    ref, likelihood, event = np.array([0.5, 0.5]), np.eye(2), [0, 1]
    if kind == "shape":
        event = [0]
    elif kind == "reference":
        ref = np.array([0.2, 0.2])
    elif kind == "candidate":
        priors[1] = np.array([0.2, 0.2])
    else:
        priors[1] = np.array([1.0, 0.0])
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Invalid\ candidate\ prior"
            r"|"
            r"Invalid\ robustness\ inputs"
            r"|"
            r"Normalised\ nonnegative\ reference\ prior\ required"
            r"|"
            r"Reference\ data\ impossible\ under\ a\ candidate\ prior"
            r")"
        ),
    ):
        same_data_robustness(values, priors, ref, likelihood, event)


@pytest.mark.parametrize("states", [{}, {"x": [1.0], "y": [1.0, 2.0]}, {"x": [float("nan")]}])
def test_state_identity_rejects_missing_nonfinite_or_misaligned_coordinates(states) -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:Named\ state\ arrays\ required|State\ arrays\ must\ be\ finite\ and\ aligned)"),
    ):
        state_identifiers(states)


def scope():
    return Scope("fixture", "fixture population", "2020-01-01", "2020-12-31", "fixture units")


def test_evidence_requires_typed_scope_and_unique_evidence_receipts() -> None:
    with pytest.raises(
        ValueError,
        match=(r"^(?:Use\ ISO\ observation\-period\ dates)"),
    ):
        Scope("x", "p", "invalid", "2020-01-01", "u")
    with pytest.raises(
        ValueError,
        match=(r"^(?:State\ identities\ and\ scope\ must\ match\ the\ decision\ problem)"),
    ):
        Belief(problem(), ("one",), scope())
    with pytest.raises(
        ValueError,
        match=(r"^(?:Typed\ source\ and\ target\ scopes\ required)"),
    ):
        EvidencePacket("e", ("d",), ("s",), ("one", "two"), np.zeros(2), "bad", scope(), "fixture")
    belief = Belief(problem(), ("one", "two"), scope(), receipts=({"evidence_id": "e"},))
    packet = EvidencePacket(
        "e", ("new data",), ("s",), ("one", "two"), np.zeros(2), scope(), scope(), "fixture"
    )
    with pytest.raises(ValueError, match="identifier reused"):
        condition(belief, packet)
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Provide\ either\ a\ conditional\-independent\ second\ report\ or\ a\ joi"
            r"nt\ report"
            r")"
        ),
    ):
        incremental_value(belief, np.eye(2))


def test_zero_probability_reports_keep_the_information_chain_valid() -> None:
    belief = Belief(problem(), ("one", "two"), scope())
    first = np.array([[1.0, 1.0], [0.0, 0.0]])
    result = incremental_value(belief, first, np.eye(2))
    assert result["expected_conditional_evsi"] == pytest.approx(5.0)
    assert result["outcome_probabilities"][1] == 0.0
    assert result["conditional_evsi"][1] == 0.0


@pytest.mark.parametrize(
    "kind",
    [
        "name",
        "cost_unit",
        "cost_ids",
        "asset",
        "twice",
        "missing",
        "overlap",
        "states",
        "tensor",
        "empty_tensor",
    ],
)
def test_portfolios_reject_identity_cost_and_joint_tensor_violations(kind) -> None:  # noqa: C901 -- Explicit invalid-portfolio matrix.
    b = Belief(problem(), ("one", "two"), scope())
    a = Source("a", np.eye(2), ("data",), b.state_ids)
    costs = Costs("fixture units", {"a": 1.0}, {})

    def invalid_input() -> None:
        if kind == "name":
            Source("", np.eye(2), ("data",), b.state_ids)
        elif kind == "cost_unit":
            Costs("", {}, {})
        elif kind == "cost_ids":
            Costs("fixture units", {"": 1.0}, {})
        elif kind == "asset":
            costs.price([a], ("missing",))
        elif kind == "twice":
            costs.price([a, a])
        elif kind == "missing":
            Costs("fixture units", {}, {}).price([a])
        elif kind == "overlap":
            portfolio_value(
                b,
                [a, Source("b", np.eye(2), ("data",), b.state_ids)],
                Costs("fixture units", {"a": 0.0, "b": 0.0}, {}),
            )
        elif kind == "states":
            portfolio_value(b, [Source("a", np.eye(2), ("data",), ("two", "one"))], costs)
        elif kind == "tensor":
            joint_report([a], 2, np.zeros((1, 2)))
        else:
            joint_report([], 2, np.eye(2))

    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"A\ source\ cannot\ be\ bought\ twice"
            r"|"
            r"Cost\ IDs\ required"
            r"|"
            r"Declare\ cost\ unit"
            r"|"
            r"Finite\ nonnegative\ tensor\ matching\ all\ source\ outcomes\ required"
            r"|"
            r"Missing\ cost\ components"
            r"|"
            r"No\-source\ experiment\ has\ no\ joint\ tensor"
            r"|"
            r"Overlapping\ underlying\ data;\ declare\ one\ joint\ source\ instead"
            r"|"
            r"Physical\ state\ identity/order\ mismatch"
            r"|"
            r"Source\ name\ required"
            r"|"
            r"Unknown\ existing\ asset"
            r")"
        ),
    ):
        invalid_input()


@pytest.mark.parametrize("case", ["empty", "probabilities", "units", "duplicate"])
def test_scenario_envelopes_do_not_invent_probabilities_or_pool_incompatible_results(case) -> None:
    row = {"scenario": "s", "design": "d", "enbs": 1.0, "value_unit": "u"}
    rows = [row]
    if case == "empty":
        rows = []
    elif case == "probabilities":
        row["scenario_probability"] = 0.5
    elif case == "units":
        rows.append(dict(row, scenario="other", value_unit="other"))
    else:
        rows.append(dict(row))
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Complete\ scenario\-by\-design\ results\ required"
            r"|"
            r"Duplicate\ or\ nonfinite\ scenario\ result"
            r"|"
            r"Same\ value\ unit\ and\ decision\ scale\ required"
            r"|"
            r"Scenario\ probabilities\ do\ not\ belong\ in\ an\ unweighted\ envelope"
            r")"
        ),
    ):
        envelope(rows)


@pytest.mark.parametrize("case", ["reference", "cost", "normative"])
def test_retail_consequences_reject_invalid_units_costs_and_normative_weights(case) -> None:
    states, prior, cfg = build_retail_states(load_config(ROOT / "configs/regulatory.json"), quit_points=1)
    if case == "reference":
        cfg["reference_exposure"] = 0.0
    elif case == "cost":
        cfg["policy_costs"][next(iter(cfg["policy_costs"]))] = -1.0

    def invalid_input() -> None:
        if case == "normative":
            retail_problem(states, prior, cfg, -1.0)
        else:
            retail_components(states, cfg)

    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"Declare\ nonnegative\ normative\ weight"
            r"|"
            r"Finite\ nonnegative\ resource\ scores\ required"
            r"|"
            r"Positive\ reference\ exposure\ required"
            r")"
        ),
    ):
        invalid_input()


def test_backend_failures_are_explicit_and_protocol_double_checks_parity(monkeypatch) -> None:
    """Exercise a labelled protocol double without claiming installed-Voiage qualification."""
    with pytest.raises(
        ValueError,
        match=(r"^(?:Unknown\ backend\ 'unknown')"),
    ):
        exact_evpi(problem(), backend="unknown")
    with pytest.raises(
        ValueError,
        match=(
            r"^(?:"
            r"This\ voiage\ adapter\ supports\ equally\ weighted\ states\ only;\ no\ i"
            r"mplicit\ resampling"
            r")"
        ),
    ):
        exact_evpi(problem(np.array([0.9, 0.1])), backend="voiage")
    monkeypatch.setitem(sys.modules, "voiage.analysis", None)
    with pytest.raises(LibraryUnavailable):
        exact_evpi(problem(), backend="voiage")
    from tobac.integrations import voiage_evpi  # noqa: PLC0415 -- Import at the exercised capability or monkeypatch boundary.

    analysis, schema = types.ModuleType("voiage.analysis"), types.ModuleType("voiage.schema")

    class ValueArray:
        @classmethod
        def from_numpy(cls, values, strategy_names=None) -> object:  # noqa: ARG003 -- Mirror the upstream classmethod interface in this execution double.
            return values

    class DecisionAnalysis:
        result = 5.0

        def __init__(self, values) -> None:
            self.values = values

        def evpi(self):
            return self.result

    analysis.DecisionAnalysis, schema.ValueArray = DecisionAnalysis, ValueArray
    monkeypatch.setitem(sys.modules, "voiage.analysis", analysis)
    monkeypatch.setitem(sys.modules, "voiage.schema", schema)
    assert voiage_evpi(problem().values, ["a", "b"]) == 5.0
    DecisionAnalysis.result = 0.0
    with pytest.raises(ArithmeticError):
        voiage_evpi(problem().values, ["a", "b"])
