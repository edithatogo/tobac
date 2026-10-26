"""Unweighted scenario envelopes, not probabilities assigned to viewpoints."""

from __future__ import annotations

import math

lazy from tobac._typing import Report

# Named bounds preserve the existing scientific/data contract.
INVARIANT_ATOL = 1e-12


def envelope(rows: list[Report]) -> list[Report]:
    """Summarise unweighted scenario ranges and regret without assigning scenario probabilities."""
    if not rows:
        msg = "Complete scenario-by-design results required"
        raise ValueError(msg)
    if any("scenario_probability" in r for r in rows):
        msg = "Scenario probabilities do not belong in an unweighted envelope"
        raise ValueError(msg)
    units = {r["value_unit"] for r in rows}
    if len(units) != 1:
        msg = "Same value unit and decision scale required"
        raise ValueError(msg)
    scenarios = sorted({r["scenario"] for r in rows})
    designs = sorted({r["design"] for r in rows})
    table: dict[tuple[str, str], float] = {}
    for r in rows:
        key = (r["scenario"], r["design"])
        v = float(r["enbs"])
        if key in table or not math.isfinite(v):
            msg = "Duplicate or nonfinite scenario result"
            raise ValueError(msg)
        table[key] = v
    if len(table) != len(scenarios) * len(designs):
        msg = "Each scenario must evaluate the same designs"
        raise ValueError(msg)
    best = {s: max(table[s, d] for d in designs) for s in scenarios}
    return [
        {
            "design": d,
            "minimum_enbs": min(table[s, d] for s in scenarios),
            "maximum_enbs": max(table[s, d] for s in scenarios),
            "maximum_regret": max(best[s] - table[s, d] for s in scenarios),
            "positive_in_all_scenarios": all(table[s, d] > 0 for s in scenarios),
            "optimal_in_all_scenarios": all(abs(table[s, d] - best[s]) < INVARIANT_ATOL for s in scenarios),
            "optimal_scenarios": [s for s in scenarios if abs(table[s, d] - best[s]) < INVARIANT_ATOL],
            "value_unit": next(iter(units)),
            "scenario_weighting": "none",
        }
        for d in designs
    ]
