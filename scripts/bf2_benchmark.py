"""Run the frozen finite synthetic BF2 benchmark; no empirical admission.

Every latent trajectory and report sequence is enumerated. Study policies only
receive available reports, while the evaluation loop alone accesses true states.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import platform
import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any, cast

import numpy as np

from tobac._core import DecisionProblem
from tobac.evidence import Belief, EvidencePacket, Scope, condition
from tobac.information import lognormal_bins
from tobac.research.staged import two_stage

STATES = ((0, 0), (0, 1), (1, 0), (1, 1))
STATE_IDS = ("mix0-cal0", "mix0-cal1", "mix1-cal0", "mix1-cal1")
POLICIES = ("no_study", "fixed_sampling", "fixed_calibration", "static_staged", "adaptive")
SCOPE = Scope("synthetic", "two-product mixture", "2026-01-01", "2026-01-03", "synthetic score")
VALUES = np.array([[float(action == x) for action in (0, 1)] for x, _h in STATES])
COST = 0.03
FINAL_PERIOD = 2
CONFIDENCE = 0.9
MIN_IMPROVEMENT = 0.01
MIN_COVERAGE = 0.85
LOGGER = logging.getLogger(__name__)
REGIMES = {
    "matched": (0.1, 0.1),
    "stable": (0.0, 0.0),
    "mixture_drift": (0.35, 0.1),
    "calibration_drift": (0.1, 0.35),
    "both_drift": (0.35, 0.35),
    "extreme": (0.5, 0.5),
}


def transition_matrix(p_x: float, p_h: float, *, shared: bool = False) -> np.ndarray:
    """Independent flips, or maximal shared flips retaining both marginals."""
    if not all(math.isfinite(p) and 0 <= p <= 1 for p in (p_x, p_h)):
        msg = "Finite flip probabilities in [0,1] required"
        raise ValueError(msg)
    matrix = np.zeros((4, 4))
    for i, (x, h) in enumerate(STATES):
        for j, (next_x, next_h) in enumerate(STATES):
            fx, fh = x != next_x, h != next_h
            if shared:
                both = min(p_x, p_h)
                probs = {
                    (False, False): 1 - max(p_x, p_h),
                    (True, False): p_x - both,
                    (False, True): p_h - both,
                    (True, True): both,
                }
                matrix[i, j] = probs[fx, fh]
            else:
                matrix[i, j] = (p_x if fx else 1 - p_x) * (p_h if fh else 1 - p_h)
    return matrix


def wastewater_likelihood(*, lower_limit: bool = False, no_signal: bool = False) -> np.ndarray:
    """Integrated outcome-by-state probabilities, with one left-censored bin."""
    medians = [0.8 if no_signal or x ^ h == 0 else 2.5 for x, h in STATES]
    return lognormal_bins(medians, 0.4, [0.25, 1.0, 2.0] if lower_limit else [1.0, 2.0])


@dataclass(frozen=True)
class BF2Model:
    """The planning model; true drift regimes remain outside policy code."""

    p_x: float = 0.1
    p_h: float = 0.1
    lower_limit: bool = False
    no_signal: bool = False
    calibration_accuracy: float = 0.9

    def __post_init__(self) -> None:
        """Validate the planning transition and measurement accuracy."""
        transition_matrix(self.p_x, self.p_h)
        if not math.isfinite(self.calibration_accuracy) or not 0 <= self.calibration_accuracy <= 1:
            msg = "Calibration accuracy must be between zero and one"
            raise ValueError(msg)

    def likelihood(self, channel: str) -> np.ndarray:
        """Return the declared outcome-by-state observation probabilities."""
        if channel == "W":
            return wastewater_likelihood(lower_limit=self.lower_limit, no_signal=self.no_signal)
        if channel == "C":
            return np.array(
                [
                    [
                        self.calibration_accuracy if y == h else 1 - self.calibration_accuracy
                        for _x, h in STATES
                    ]
                    for y in (0, 1)
                ]
            )
        msg = "Unknown observation channel"
        raise ValueError(msg)

    def transition(self) -> np.ndarray:
        """Return the state transition used by the policy."""
        return transition_matrix(self.p_x, self.p_h)


def initial_belief(probabilities: np.ndarray | None = None, used_ids: tuple[str, ...] = ()) -> Belief:
    """Construct the synthetic decision belief using the shared state contract."""
    problem = DecisionProblem(VALUES, ("target0", "target1"), "synthetic score", probabilities)
    return Belief(problem, STATE_IDS, SCOPE, used_ids)


def filter_report(model: BF2Model, before: Belief, channel: str, outcome: int, data_id: str) -> Belief:
    """Apply a distinct report through the shared evidence contract."""
    likelihood = model.likelihood(channel)
    if not isinstance(cast("object", outcome), int) or not 0 <= outcome < len(likelihood):
        msg = "Unknown report outcome"
        raise ValueError(msg)
    with np.errstate(divide="ignore"):
        log_likelihood = np.log(likelihood[outcome])
    packet = EvidencePacket(
        evidence_id=f"report-{data_id}",
        data_ids=(data_id,),
        source_ids=(f"synthetic-{channel}",),
        state_ids=STATE_IDS,
        log_likelihood=log_likelihood,
        source_scope=SCOPE,
        target_scope=SCOPE,
        likelihood_model=f"synthetic {channel} on sampled state",
        dependence_note="Independent given the complete synthetic state trajectory",
    )
    return condition(before, packet)


def _plain_update(prior: np.ndarray, likelihood: np.ndarray, outcome: int) -> tuple[float, np.ndarray]:
    weighted = prior * likelihood[outcome]
    probability = float(weighted.sum())
    if probability <= 0:
        msg = "Report has no support under the planning model"
        raise ValueError(msg)
    return probability, weighted / probability


def _action(prior: np.ndarray) -> int:
    """Choose from information available at this period, breaking ties toward zero."""
    return int(float(prior[2] + prior[3]) > float(prior[0] + prior[1]))


def _success_probability(prior: np.ndarray) -> float:
    return max(float(prior[0] + prior[1]), float(prior[2] + prior[3]))


class _Planner:
    def __init__(self, model: BF2Model) -> None:
        self.model = model
        self.matrix = model.transition()
        self.likelihood = {name: model.likelihood(name) for name in ("W", "C")}
        self.static = BF2Model(0, 0, model.lower_limit, model.no_signal, model.calibration_accuracy)
        self.static_plan = self._static_plan()
        self.future_cache: dict[tuple[int, tuple[float, ...]], float] = {}

    def _static_plan(self) -> tuple[str | None, str | None, dict[int, bool]]:
        problem = DecisionProblem(VALUES, ("target0", "target1"), "synthetic score")
        best = 0.0
        selected: tuple[str | None, str | None, dict[int, bool]] = (None, None, {})
        for first, second in (("W", "C"), ("C", "W")):
            result = two_stage(
                problem,
                self.likelihood[first],
                self.likelihood[second],
                pilot_cost=COST,
                followup_cost=COST,
                pilot_remaining=2 / 3,
                followup_remaining=1 / 3,
            )
            if float(result["adaptive_enbs"]) > best:
                best = float(result["adaptive_enbs"])
                selected = (
                    first,
                    second,
                    {int(x["pilot_outcome"]): bool(x["continue"]) for x in result["branches"]},
                )
        return selected

    def _future(self, time: int, key: tuple[float, ...]) -> float:
        cache_key = (time, key)
        if cache_key in self.future_cache:
            return self.future_cache[cache_key]
        prior = np.array(key)
        immediate = _success_probability(prior) / 3
        if time == FINAL_PERIOD:
            return immediate
        candidates = [self._future(time + 1, tuple(prior @ self.matrix))]
        for channel in ("W", "C"):
            likelihood = self.likelihood[channel]
            future = 0.0
            for outcome in range(len(likelihood)):
                probability = float(likelihood[outcome] @ prior)
                if probability > 0:
                    _, posterior = _plain_update(prior, likelihood, outcome)
                    future += probability * self._future(time + 1, tuple(posterior @ self.matrix))
            candidates.append(future - COST)
        value = immediate + max(candidates)
        self.future_cache[cache_key] = value
        return value

    def choice(
        self, policy: str, time: int, prior: np.ndarray, history: tuple[tuple[str, int], ...]
    ) -> str | None:
        fixed = {"no_study": None, "fixed_sampling": "W", "fixed_calibration": "C"}
        if policy in fixed:
            return fixed[policy]
        if policy == "static_staged":
            return self._staged_choice(time, history)
        if policy != "adaptive":
            msg = "Unknown study policy"
            raise ValueError(msg)
        best = self._future(time + 1, tuple(prior @ self.matrix))
        choice = None
        for channel in ("W", "C"):
            expected = -COST
            likelihood = self.likelihood[channel]
            for outcome in range(len(likelihood)):
                probability = float(likelihood[outcome] @ prior)
                if probability > 0:
                    _, posterior = _plain_update(prior, likelihood, outcome)
                    expected += probability * self._future(time + 1, tuple(posterior @ self.matrix))
            if expected > best:
                best, choice = expected, channel
        return choice

    def _staged_choice(self, time: int, history: tuple[tuple[str, int], ...]) -> str | None:
        first, second, continuation = self.static_plan
        if time == 0:
            return first
        if first is not None and history and continuation.get(history[0][1], False):
            return second
        return None


def _set_and_brier(prior: np.ndarray, truth: int) -> tuple[int, int, float]:
    p1 = float(prior[2] + prior[3])
    p0 = 1 - p1
    if p0 >= CONFIDENCE:
        included = {0}
    elif p1 >= CONFIDENCE:
        included = {1}
    else:
        included = {0, 1}
    return int(truth in included), len(included), (p1 - truth) ** 2


def categorical_log_loss(truth: np.ndarray, prediction: np.ndarray) -> float:
    """Compute log loss and retain infinity for an impossible prediction."""
    if (
        truth.shape != prediction.shape
        or np.any(truth < 0)
        or np.any(prediction < 0)
        or not np.all(np.isfinite(truth))
        or not np.all(np.isfinite(prediction))
        or not math.isclose(float(truth.sum()), 1.0, abs_tol=1e-11)
        or not math.isclose(float(prediction.sum()), 1.0, abs_tol=1e-11)
    ):
        msg = "Finite aligned probability distributions required"
        raise ValueError(msg)
    return sum(
        -float(p) * math.log(float(q)) if q > 0 else math.inf
        for p, q in zip(truth, prediction, strict=True)
        if p > 0
    )


def _empty_metrics() -> dict[str, Any]:
    return {
        "gross_score": 0.0,
        "immediate_gross_score": 0.0,
        "expected_studies": 0.0,
        "forced_studies": 0.0,
        "research_brier_t2": 0.0,
        "period_regret": [0.0, 0.0, 0.0],
        "coverage": {"1": 0.0, "2": 0.0},
        "set_size": {"1": 0.0, "2": 0.0},
        "brier": {"1": 0.0, "2": 0.0},
        "heldout_log_loss": 0.0,
        "probability_mass": 0.0,
    }


@dataclass(frozen=True)
class _Information:
    probabilities: np.ndarray
    research_probabilities: np.ndarray
    used_ids: tuple[str, ...] = ()
    research_used_ids: tuple[str, ...] = ()
    history: tuple[tuple[str, int], ...] = ()


@dataclass(frozen=True)
class _ReportOutcome:
    following: _Information
    probability: float
    acquired: int
    forced: int
    immediate_action: int


class _PolicyEvaluation:
    def __init__(self, model: BF2Model, policy: str, planner: _Planner) -> None:
        self.policy = policy
        self.planning_policy = "adaptive" if policy == "adaptive_equal_spend" else policy
        self.model = planner.static if policy == "static_staged" else model
        self.transition = self.model.transition()
        self.likelihoods = {name: model.likelihood(name) for name in ("W", "C")}
        self.planner = planner
        self.metrics = _empty_metrics()

    def _advance(self, information: _Information) -> _Information:
        return _Information(
            information.probabilities @ self.transition,
            information.research_probabilities @ self.transition,
            information.used_ids,
            information.research_used_ids,
            information.history,
        )

    def reports(self, time: int, information: _Information, state: int) -> list[_ReportOutcome]:
        """Enumerate reports while withholding forced acquisitions from decisions."""
        channel = self.planner.choice(
            self.planning_policy, time, information.probabilities, information.history
        )
        forced = self.policy == "adaptive_equal_spend" and channel is None
        if forced:
            channel = "W"
        if channel is None:
            return [_ReportOutcome(self._advance(information), 1.0, 0, 0, _action(information.probabilities))]
        outcomes: list[_ReportOutcome] = []
        for outcome, probability in enumerate(self.likelihoods[channel][:, state]):
            if probability <= 0:
                continue
            data_id = f"synthetic-{time}-{channel}"
            research_belief = filter_report(
                self.model,
                initial_belief(information.research_probabilities, information.research_used_ids),
                channel,
                outcome,
                data_id,
            )
            research = np.asarray(research_belief.problem.prior_weights)
            research_used = research_belief.used_data_ids
            posterior, used, history = information.probabilities, information.used_ids, information.history
            if not forced:
                updated = filter_report(
                    self.model,
                    initial_belief(information.probabilities, information.used_ids),
                    channel,
                    outcome,
                    data_id,
                )
                posterior, used = np.asarray(updated.problem.prior_weights), updated.used_data_ids
                history = (*history, (channel, outcome))
            following = self._advance(_Information(posterior, research, used, research_used, history))
            outcomes.append(_ReportOutcome(following, float(probability), 1, int(forced), _action(posterior)))
        return outcomes

    def _record(
        self, path: tuple[int, int, int], reports: tuple[_ReportOutcome, _ReportOutcome], weight: float
    ) -> None:
        first, second = reports
        probabilities = (np.full(4, 0.25), first.following.probabilities, second.following.probabilities)
        truths = [STATES[state][0] for state in path]
        actions = [_action(prior) for prior in probabilities]
        instant_actions = (first.immediate_action, second.immediate_action, actions[FINAL_PERIOD])
        metrics = self.metrics
        metrics["probability_mass"] += weight
        metrics["gross_score"] += weight * sum(
            float(action == x) / 3 for action, x in zip(actions, truths, strict=True)
        )
        metrics["immediate_gross_score"] += weight * sum(
            float(action == x) / 3 for action, x in zip(instant_actions, truths, strict=True)
        )
        metrics["expected_studies"] += weight * (first.acquired + second.acquired)
        metrics["forced_studies"] += weight * (first.forced + second.forced)
        metrics["research_brier_t2"] += (
            weight * _set_and_brier(second.following.research_probabilities, truths[FINAL_PERIOD])[2]
        )
        for time in range(3):
            metrics["period_regret"][time] += weight * float(actions[time] != truths[time]) / 3
        for time in (1, 2):
            hit, size, brier = _set_and_brier(probabilities[time], truths[time])
            metrics["coverage"][str(time)] += weight * hit
            metrics["set_size"][str(time)] += weight * size
            metrics["brier"][str(time)] += weight * brier
        prediction = self.likelihoods["W"] @ probabilities[FINAL_PERIOD]
        truth = self.likelihoods["W"][:, path[FINAL_PERIOD]]
        metrics["heldout_log_loss"] += weight * categorical_log_loss(truth, prediction)

    def add_path(self, path: tuple[int, int, int], probability: float) -> None:
        """Evaluate both study periods on one known-truth state trajectory."""
        initial = np.full(4, 0.25)
        information = _Information(initial, initial)
        for first in self.reports(0, information, path[0]):
            for second in self.reports(1, first.following, path[1]):
                weight = probability * first.probability * second.probability
                self._record(path, (first, second), weight)

    def finish(self) -> dict[str, Any]:
        """Verify complete path mass and return its normalized finite expectations."""
        metrics = self.metrics
        mass = metrics["probability_mass"]
        if not math.isclose(mass, 1, rel_tol=0, abs_tol=1e-11):
            msg = "Finite path probabilities do not sum to one"
            raise ArithmeticError(msg)
        for key in (
            "gross_score",
            "immediate_gross_score",
            "expected_studies",
            "forced_studies",
            "research_brier_t2",
            "heldout_log_loss",
        ):
            metrics[key] /= mass
        metrics["period_regret"] = [value / mass for value in metrics["period_regret"]]
        for key in ("coverage", "set_size", "brier"):
            metrics[key] = {time: value / mass for time, value in metrics[key].items()}
        metrics["mean_regret"] = sum(metrics["period_regret"])
        metrics["expected_cost"] = COST * metrics["expected_studies"]
        metrics["net_score"] = metrics["gross_score"] - metrics["expected_cost"]
        metrics["paired_immediate_minus_delayed"] = metrics["immediate_gross_score"] - metrics["gross_score"]
        return metrics


def evaluate_regime(
    model: BF2Model, p_x: float, p_h: float, *, shared: bool = False, include_equal_spend: bool = False
) -> dict[str, dict[str, Any]]:
    """Enumerate finite trajectories using policies fixed by their planning law."""
    truth_matrix = transition_matrix(p_x, p_h, shared=shared)
    planner = _Planner(model)
    policies = (*POLICIES, "adaptive_equal_spend") if include_equal_spend else POLICIES
    output: dict[str, dict[str, Any]] = {}
    for policy in policies:
        evaluation = _PolicyEvaluation(model, policy, planner)
        for path in product(range(4), repeat=3):
            probability = float(0.25 * truth_matrix[path[0], path[1]] * truth_matrix[path[1], path[2]])
            if probability > 0:
                evaluation.add_path((path[0], path[1], path[2]), probability)
        output[policy] = evaluation.finish()
    return output


def _json_safe(value: object) -> object:
    """Preserve an infinite score explicitly; reject NaN rather than clipping."""
    if isinstance(value, float) and not math.isfinite(value):
        if value == math.inf:
            return "infinity"
        msg = "Non-finite benchmark output"
        raise ValueError(msg)
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in cast("dict[str, object]", value).items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in cast("list[object] | tuple[object, ...]", value)]
    return value


def main() -> None:
    """Write a new source-bound benchmark result with the prespecified controls."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    model = BF2Model()
    # Choose the comparator using the declared planning law, before evaluating
    # any of the withheld regimes in this execution.
    matched = evaluate_regime(model, *REGIMES["matched"], include_equal_spend=True)
    comparators = ("fixed_sampling", "fixed_calibration", "static_staged")
    reference = max(comparators, key=lambda p: matched[p]["net_score"])
    LOGGER.info("Planning comparator %s", reference)
    results = {"matched": matched}
    for name, drift in REGIMES.items():
        if name != "matched":
            results[name] = evaluate_regime(model, *drift, include_equal_spend=True)
            LOGGER.info("Completed primary regime %s", name)
    withheld = [name for name in REGIMES if name != "matched"]
    improvements = {
        name: results[name][reference]["mean_regret"] - results[name]["adaptive"]["mean_regret"]
        for name in withheld
    }
    signal = (
        any(improvements[x] >= MIN_IMPROVEMENT for x in withheld if x != "extreme")
        and all(improvements[x] >= -MIN_IMPROVEMENT for x in withheld)
        and all(results[x]["adaptive"]["coverage"][str(t)] >= MIN_COVERAGE for x in withheld for t in (1, 2))
        and all(results[x]["adaptive"]["expected_studies"] <= 2 + 1e-12 for x in withheld)
    )
    worst = {
        policy: max(results[name][policy]["mean_regret"] for name in REGIMES) for policy in results["matched"]
    }
    ablations: dict[str, Any] = {}
    for label, changed, shared in (
        ("lower_detection_limit", BF2Model(lower_limit=True), False),
        ("uninformative_calibration", BF2Model(calibration_accuracy=0.5), False),
        ("no_product_signal", BF2Model(no_signal=True), False),
        ("shared_innovations", model, True),
    ):
        ablations[label] = {}
        for name, drift in REGIMES.items():
            ablations[label][name] = evaluate_regime(changed, *drift, shared=shared)
        LOGGER.info("Completed ablation %s", label)
    payload = {
        "status": "synthetic finite benchmark; no empirical calibration or scientific acceptance",
        "spec_sha256": hashlib.sha256(
            Path("conductor/tracks/dynamic_frontier_20261108/bf2-benchmark-spec-20261113.md").read_bytes()
        ).hexdigest(),
        "heldout_data_id": "evaluation-only-W-t2",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version,
        "platform": platform.platform(),
        "regimes": REGIMES,
        "planning_comparator": reference,
        "adaptive_regret_improvement": improvements,
        "predefined_usefulness_signal": signal,
        "worst_regime_mean_regret": worst,
        "results": results,
        "ablations": ablations,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(_json_safe(payload), stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
