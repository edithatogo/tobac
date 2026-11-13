"""Finite credal action comparisons with independently checkable certificates.

The simplex and all restrictions use the existing belief's ordered state IDs.
Solver estimates are numerical; the returned rational witnesses/certificates are
checked against the exact binary64 inputs. No observations or priors are added.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import TYPE_CHECKING, Any, cast

import numpy as np
from scipy.optimize import linprog

from .evidence import Belief

if TYPE_CHECKING:
    from collections.abc import Sequence

MAX_CANDIDATES = 8
MIN_ACTIONS = 2
INFEASIBLE_STATUS = 2
RATIONAL_LIMIT = 1_000_000_000


def _fraction(value: float) -> Fraction:
    """Interpret a finite binary64 value exactly, never as a rounded decimal."""
    return Fraction(float(value))


@dataclass(frozen=True)
class LinearRestriction:
    """Named upper bound on a linear function of ordered state probabilities."""

    name: str
    state_ids: tuple[str, ...]
    coefficients: tuple[float, ...]
    upper: float

    def __post_init__(self) -> None:
        """Validate the named finite coefficients and preserve state order."""
        if not isinstance(cast("object", self.name), str) or not self.name.strip():
            msg = "Restriction name must be nonempty"
            raise ValueError(msg)
        ids = tuple(self.state_ids)
        if (
            not ids
            or any(not isinstance(cast("object", x), str) or not x.strip() for x in ids)
            or len(set(ids)) != len(ids)
        ):
            msg = "Restriction state IDs must be unique and nonempty"
            raise ValueError(msg)
        try:
            values = np.asarray(self.coefficients, dtype=float)
            upper = float(self.upper)
        except (TypeError, ValueError) as error:
            msg = "Restriction coefficients and upper bound must be finite numbers"
            raise ValueError(msg) from error
        if values.shape != (len(ids),) or not np.isfinite(values).all() or not np.isfinite(upper):
            msg = "Restriction coefficients and upper bound must be finite and aligned"
            raise ValueError(msg)
        object.__setattr__(self, "state_ids", ids)
        object.__setattr__(self, "coefficients", tuple(float(x) for x in values))
        object.__setattr__(self, "upper", upper)


def _validate(
    belief: Belief, action: str, comparator: str, restrictions: Sequence[LinearRestriction]
) -> tuple[int, int]:
    if not isinstance(cast("object", belief), Belief):
        msg = "A shared evidence Belief is required"
        raise TypeError(msg)
    names = tuple(belief.problem.action_names)
    if action == comparator or action not in names or comparator not in names:
        msg = "Choose two distinct known action names"
        raise ValueError(msg)
    if any(
        not isinstance(cast("object", r), LinearRestriction) or r.state_ids != belief.state_ids
        for r in restrictions
    ):
        msg = "Restriction state identities and order must match the belief"
        raise ValueError(msg)
    if len({r.name for r in restrictions}) != len(restrictions):
        msg = "Restriction names must be unique"
        raise ValueError(msg)
    return names.index(action), names.index(comparator)


def _arrays(restrictions: Sequence[LinearRestriction], size: int) -> tuple[np.ndarray, np.ndarray]:
    a = np.asarray([r.coefficients for r in restrictions], dtype=float).reshape((-1, size))
    return a, np.asarray([r.upper for r in restrictions], dtype=float)


def _valid_weights(weights: Sequence[Fraction], restrictions: Sequence[LinearRestriction]) -> bool:
    if any(x < 0 for x in weights) or sum(weights) != 1:
        return False
    return all(
        sum(_fraction(c) * p for c, p in zip(r.coefficients, weights, strict=True)) <= _fraction(r.upper)
        for r in restrictions
    )


def _witness(
    weights: np.ndarray, coefficients: Sequence[Fraction], restrictions: Sequence[LinearRestriction]
) -> dict[str, Any] | None:
    """Turn approximate solutions into exact feasible points, or say unknown."""
    if not all(np.isfinite(x) for x in weights):
        return None
    clipped = [max(0.0, float(x)) for x in weights]
    for exact in (False, True):
        fractions = [
            _fraction(x) if exact else _fraction(x).limit_denominator(RATIONAL_LIMIT) for x in clipped
        ]
        # The final adjusted coordinate enforces simplex equality exactly. Trying
        # every anchor also preserves rational boundary constraints when possible.
        for anchor in range(len(fractions)):
            candidate = fractions.copy()
            candidate[anchor] = Fraction(1) - sum(
                (x for i, x in enumerate(candidate) if i != anchor), Fraction(0)
            )
            if _valid_weights(candidate, restrictions):
                advantage = sum(c * p for c, p in zip(coefficients, candidate, strict=True))
                return {"weights": [str(x) for x in candidate], "advantage": str(advantage)}
    return None


def _dual_certificate(
    coefficients: Sequence[Fraction], restrictions: Sequence[LinearRestriction], marginals: np.ndarray
) -> dict[str, Any]:
    """Construct a lower bound valid for every point of the declared simplex."""
    projected = [min(0.0, float(y)) for y in marginals]
    candidates = [[Fraction(0)] * len(restrictions)]
    candidates.extend(
        [_fraction(y) if exact else _fraction(y).limit_denominator(RATIONAL_LIMIT) for y in projected]
        for exact in (False, True)
    )
    best = (min(coefficients), min(coefficients), candidates[0])
    for y in candidates:
        offset = min(
            c
            - sum(
                _fraction(r.coefficients[i]) * multiplier
                for r, multiplier in zip(restrictions, y, strict=True)
            )
            for i, c in enumerate(coefficients)
        )
        bound = offset + sum(
            _fraction(r.upper) * multiplier for r, multiplier in zip(restrictions, y, strict=True)
        )
        if bound > best[0]:
            best = bound, offset, y
    return {"multipliers": [str(x) for x in best[2]], "simplex_offset": str(best[1]), "bound": str(best[0])}


def _infeasibility_certificate(restrictions: Sequence[LinearRestriction], size: int) -> dict[str, Any] | None:
    """Find a rational positive combination contradicted by simplex membership."""
    if not restrictions:
        return None
    a, b = _arrays(restrictions, size)
    count = len(restrictions)
    result = linprog(
        np.r_[b, -1.0],
        A_ub=np.column_stack((-a.T, np.ones(size))),
        b_ub=np.zeros(size),
        A_eq=np.array([[*([1.0] * count), 0.0]]),
        b_eq=np.array([1.0]),
        bounds=[(0, None)] * count + [(None, None)],
        method="highs",
    )
    if not result.success or result.x is None:
        return None
    solution = np.asarray(result.x, dtype=float)
    for exact in (False, True):
        y = [_fraction(max(0.0, float(v))) for v in solution[:count]]
        if not exact:
            y = [x.limit_denominator(RATIONAL_LIMIT) for x in y]
        if not any(y):
            continue
        low = min(
            sum(
                _fraction(r.coefficients[i]) * multiplier
                for r, multiplier in zip(restrictions, y, strict=True)
            )
            for i in range(size)
        )
        high = sum(_fraction(r.upper) * multiplier for r, multiplier in zip(restrictions, y, strict=True))
        if low > high:
            return {"multipliers": [str(x) for x in y], "minimum_left": str(low), "maximum_right": str(high)}
    return None


def _contrast_status(bound: Fraction, witness: Fraction) -> str:
    """Classify the result using its exact feasible point and bound."""
    if witness < bound:
        msg = "Exact primal witness contradicts dual bound"
        raise ArithmeticError(msg)
    if bound > 0:
        return "strict_dominance"
    if bound == 0:
        return "weak_dominance"
    if witness < 0:
        return "not_dominant"
    return "unresolved"


def assess_contrast(
    belief: Belief,
    action: str,
    comparator: str,
    restrictions: Sequence[LinearRestriction] = (),
) -> dict[str, Any]:
    """Bound expected action advantage and return exact proofs where available.

    `strict_dominance` and `weak_dominance` require a feasible rational witness
    and a nonnegative exact dual lower bound. `not_dominant` requires an exact
    feasible negative-advantage witness. A failed proof stays `unresolved`.
    The existing prior is reported only as a separate point comparison.
    """
    restrictions = tuple(restrictions)
    ai, bi = _validate(belief, action, comparator, restrictions)
    values = belief.problem.values
    c = [_fraction(float(row[ai])) - _fraction(float(row[bi])) for row in values]
    objective = np.array([float(x) for x in c])
    a, b = _arrays(restrictions, len(c))
    low = linprog(
        objective,
        A_ub=a if restrictions else None,
        b_ub=b if restrictions else None,
        A_eq=np.ones((1, len(c))),
        b_eq=np.ones(1),
        bounds=(0, None),
        method="highs",
    )
    result: dict[str, Any] = {
        "status": "unresolved",
        "action": action,
        "comparator": comparator,
        "state_ids": list(belief.state_ids),
        "restriction_names": [r.name for r in restrictions],
        "value_unit": belief.problem.value_unit,
        "prior_advantage": float(cast("np.ndarray", belief.problem.prior_weights) @ objective),
        "lower_estimate": None,
        "upper_estimate": None,
        "lower_witness": None,
        "upper_witness": None,
        "lower_certificate": None,
        "upper_certificate_for_negative_advantage": None,
        "infeasibility_certificate": None,
        "solver_status": int(low.status),
        "empirical_admission": False,
    }
    if not low.success:
        if low.status == INFEASIBLE_STATUS:
            cert = _infeasibility_certificate(restrictions, len(c))
            if cert is not None:
                result.update(status="incompatible", infeasibility_certificate=cert)
        return result
    high = linprog(
        -objective,
        A_ub=a if restrictions else None,
        b_ub=b if restrictions else None,
        A_eq=np.ones((1, len(c))),
        b_eq=np.ones(1),
        bounds=(0, None),
        method="highs",
    )
    if not high.success:
        result["solver_status"] = int(high.status)
        return result
    if low.x is None or high.x is None or low.fun is None or high.fun is None:
        return result
    lower_witness = _witness(np.asarray(low.x, dtype=float), c, restrictions)
    upper_witness = _witness(np.asarray(high.x, dtype=float), c, restrictions)
    lower_cert = _dual_certificate(c, restrictions, low.ineqlin.marginals)
    upper_cert = _dual_certificate([-x for x in c], restrictions, high.ineqlin.marginals)
    result.update(
        lower_estimate=float(low.fun),
        upper_estimate=float(-high.fun),
        lower_witness=lower_witness,
        upper_witness=upper_witness,
        lower_certificate=lower_cert,
        upper_certificate_for_negative_advantage=upper_cert,
    )
    bound = Fraction(lower_cert["bound"])
    if lower_witness is not None:
        witness_advantage = Fraction(lower_witness["advantage"])
        result["status"] = _contrast_status(bound, witness_advantage)
        result["lower_primal_dual_gap"] = str(witness_advantage - bound)
    return result


def _deletion_evidence(
    deletions: dict[int, dict[str, Any]], names: list[str], unknown: list[list[str]]
) -> bool:
    """Classify whether each immediate proper subset has a counterexample."""
    if any(item["status"] in {"weak_dominance", "strict_dominance"} for item in deletions.values()):
        return False
    if any(item["status"] != "not_dominant" for item in deletions.values()):
        unknown.append(names)
        return False
    return True


def minimal_identifying_restrictions(
    belief: Belief,
    action: str,
    comparator: str,
    candidates: Sequence[LinearRestriction],
    *,
    base: Sequence[LinearRestriction] = (),
) -> dict[str, Any]:
    """Find provably inclusion-minimal subsets of up to eight named constraints.

    Every single deletion must have an exact negative witness, so no unknown
    subset is silently treated as insufficient. Minimality is relative only to
    these candidate restrictions, not all imaginable scientific evidence.
    """
    base, candidates = tuple(base), tuple(candidates)
    if len(candidates) > MAX_CANDIDATES:
        msg = "At most eight candidate restrictions may be enumerated"
        raise ValueError(msg)
    _validate(belief, action, comparator, (*base, *candidates))
    cached: dict[frozenset[int], dict[str, Any]] = {}
    minimal: list[dict[str, Any]] = []
    unknown: list[list[str]] = []
    for size in range(len(candidates) + 1):
        for chosen in combinations(range(len(candidates)), size):
            key = frozenset(chosen)
            if any(set(item["indices"]).issubset(key) for item in minimal):
                continue
            active = (*base, *(candidates[i] for i in chosen))
            result = assess_contrast(belief, action, comparator, active)
            cached[key] = result
            names = [candidates[i].name for i in chosen]
            if result["status"] == "unresolved":
                unknown.append(names)
                continue
            if not chosen and result["status"] == "incompatible":
                return {
                    "status": "incompatible",
                    "minimal_sets": [],
                    "search_complete": True,
                    "unresolved_subsets": [],
                    "base_result": result,
                }
            if result["status"] not in {"weak_dominance", "strict_dominance"}:
                continue
            deletions = {i: cached[key - {i}] for i in chosen}
            if not _deletion_evidence(deletions, names, unknown):
                continue
            minimal.append(
                {
                    "indices": list(chosen),
                    "restrictions": names,
                    "proof": result,
                    "deletion_witnesses": {
                        candidates[i].name: x["lower_witness"] for i, x in deletions.items()
                    },
                }
            )
    for item in minimal:
        del item["indices"]
    return {
        "status": "evaluated",
        "minimal_sets": minimal,
        "search_complete": not unknown,
        "unresolved_subsets": unknown,
        "base_result": cached[frozenset()],
    }


def assess_decision(belief: Belief, restrictions: Sequence[LinearRestriction] = ()) -> dict[str, Any]:
    """Compare all actions and bound worst-case regret on one common credal set.

    An action is reported common optimal only when every pairwise lower bound
    is certified. Regret is bracketed by feasible primal counterexamples and
    exact dual bounds; equality of the bracket endpoints establishes sharpness.
    """
    names = tuple(belief.problem.action_names)
    if len(names) < MIN_ACTIONS:
        msg = "At least two actions are required for a decision comparison"
        raise ValueError(msg)
    restrictions = tuple(restrictions)
    _validate(belief, names[0], names[1], restrictions)
    pairwise = {
        (action, other): assess_contrast(belief, action, other, restrictions)
        for action in names
        for other in names
        if action != other
    }
    if any(item["status"] == "incompatible" for item in pairwise.values()):
        return {
            "status": "incompatible",
            "common_optimal_actions": [],
            "action_status": {},
            "worst_case_regret": {},
            "pairwise": list(pairwise.values()),
        }
    statuses: dict[str, str] = {}
    regrets: dict[str, dict[str, str] | None] = {}
    for action in names:
        results = [pairwise[action, other] for other in names if other != action]
        if all(r["status"] in {"weak_dominance", "strict_dominance"} for r in results):
            statuses[action] = "common_optimal"
        elif any(r["status"] == "not_dominant" for r in results):
            statuses[action] = "not_robust"
        else:
            statuses[action] = "unresolved"
        if any(r["lower_certificate"] is None or r["lower_witness"] is None for r in results):
            regrets[action] = None
            continue
        lower = max(Fraction(0), *(-Fraction(r["lower_witness"]["advantage"]) for r in results))
        upper = max(Fraction(0), *(-Fraction(r["lower_certificate"]["bound"]) for r in results))
        if lower > upper:
            msg = "Exact regret witness contradicts dual bound"
            raise ArithmeticError(msg)
        regrets[action] = {"lower": str(lower), "upper": str(upper)}
    common = [name for name in names if statuses[name] == "common_optimal"]
    unknown = any(value == "unresolved" for value in statuses.values())
    return {
        "status": "unresolved" if unknown else "identified" if common else "not_identified",
        "common_optimal_actions": common,
        "action_status": statuses,
        "worst_case_regret": regrets,
        "pairwise": list(pairwise.values()),
    }
