"""Exact bounds on explicit finite action payoffs, without a prior or likelihood."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, cast


def _names(names: list[str], label: str) -> None:
    if (
        not isinstance(cast("object", names), list)
        or not names
        or any(not isinstance(cast("object", n), str) or not n.strip() for n in names)
        or len(set(names)) != len(names)
    ):
        msg = f"Nonempty unique {label} required"
        raise ValueError(msg)


def _number(value: object) -> Fraction:
    # Binary floats are deliberately excluded: supply decimal strings or integers.
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        msg = "Known finite rational payoffs required as integers or strings"
        raise TypeError(msg)
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        msg = "Known finite rational payoffs required"
        raise ValueError(msg) from error


def assess(
    states: list[str],
    actions: list[str],
    payoffs: list[list[int | str]],
    *,
    compatible: list[str] | None = None,
) -> dict[str, Any]:
    """Bound regret and advantage exactly on enumerated states and their mixtures.

    Payoffs are maximised, rows are named states and columns are named actions.
    No common optimum means no action is optimal for every probability distribution
    on this support; minimax regret is a separate declared decision convention.
    Empty compatible support is an incompatibility result, never vacuous dominance.
    The caller must establish scope, units and completeness of the finite support.
    """
    _names(states, "states")
    _names(actions, "actions")
    if (
        not isinstance(cast("object", payoffs), list)
        or len(payoffs) != len(states)
        or any(not isinstance(cast("object", row), list) or len(row) != len(actions) for row in payoffs)
    ):
        msg = "Payoffs must match state and action dimensions"
        raise ValueError(msg)
    values = [[_number(value) for value in row] for row in payoffs]
    selected = states if compatible is None else compatible
    if not isinstance(cast("object", selected), list):
        msg = "Compatible states must be a list"
        raise TypeError(msg)
    if selected:
        _names(selected, "compatible states")
    if any(state not in states for state in selected):
        msg = "Unknown compatible state"
        raise ValueError(msg)
    rows = [states.index(state) for state in selected]
    result: dict[str, Any] = {
        "status": "incompatible",
        "common_optimal_actions": [],
        "state_optima": {},
        "pairwise": [],
        "worst_case_regret": {},
        "regret_witnesses": {},
        "minimax_regret_actions": [],
        "support": selected,
        "empirical_admission": False,
    }
    if not rows:
        return result
    best = {i: max(values[i]) for i in rows}
    common = [a for j, a in enumerate(actions) if all(values[i][j] == best[i] for i in rows)]
    result["common_optimal_actions"] = common
    result["status"] = (
        "unique_common_optimum"
        if len(common) == 1
        else "common_optimum_with_ties"
        if common
        else "not_identified"
    )
    result["state_optima"] = {
        states[i]: [a for j, a in enumerate(actions) if values[i][j] == best[i]] for i in rows
    }
    regrets: list[Fraction] = []
    for j, action in enumerate(actions):
        worst = max(rows, key=lambda i: best[i] - values[i][j])
        regret = best[worst] - values[worst][j]
        regrets.append(regret)
        result["worst_case_regret"][action] = str(regret)
        result["regret_witnesses"][action] = states[worst]
        for k, comparator in enumerate(actions):
            if j == k:
                continue
            low = min(rows, key=lambda i: values[i][j] - values[i][k])
            high = max(rows, key=lambda i: values[i][j] - values[i][k])
            result["pairwise"].append(
                {
                    "action": action,
                    "comparator": comparator,
                    "lower": str(values[low][j] - values[low][k]),
                    "upper": str(values[high][j] - values[high][k]),
                    "lower_state": states[low],
                    "upper_state": states[high],
                }
            )
    result["minimax_regret_actions"] = [a for a, r in zip(actions, regrets, strict=True) if r == min(regrets)]
    return result


def main() -> None:
    """Write a new finite-scenario receipt without overwriting prior evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(packet.get("value_unit"), str) or not packet["value_unit"].strip():
        msg = "Declare one common payoff unit"
        raise ValueError(msg)
    result = assess(
        packet["states"], packet["actions"], packet["payoffs"], compatible=packet.get("compatible")
    )
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(
            {
                "value_unit": packet["value_unit"],
                "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
                "result": result,
            },
            stream,
            indent=2,
        )
        stream.write("\n")


if __name__ == "__main__":
    main()
