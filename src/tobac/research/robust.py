"""Unweighted scenario envelopes, not probabilities assigned to viewpoints."""

from __future__ import annotations

import math


def envelope(rows: list[dict]) -> list[dict]:
    if not rows:
        raise ValueError("Complete scenario-by-design results required")
    if any("scenario_probability" in r for r in rows):
        raise ValueError("Scenario probabilities do not belong in an unweighted envelope")
    units = {r["value_unit"] for r in rows}
    if len(units) != 1:
        raise ValueError("Same value unit and decision scale required")
    scenarios = sorted({r["scenario"] for r in rows})
    designs = sorted({r["design"] for r in rows})
    table = {}
    for r in rows:
        key = (r["scenario"], r["design"])
        v = float(r["enbs"])
        if key in table or not math.isfinite(v):
            raise ValueError("Duplicate or nonfinite scenario result")
        table[key] = v
    if len(table) != len(scenarios) * len(designs):
        raise ValueError("Each scenario must evaluate the same designs")
    best = {s: max(table[s, d] for d in designs) for s in scenarios}
    return [
        dict(
            design=d,
            minimum_enbs=min(table[s, d] for s in scenarios),
            maximum_enbs=max(table[s, d] for s in scenarios),
            maximum_regret=max(best[s] - table[s, d] for s in scenarios),
            positive_in_all_scenarios=all(table[s, d] > 0 for s in scenarios),
            optimal_in_all_scenarios=all(abs(table[s, d] - best[s]) < 1e-12 for s in scenarios),
            optimal_scenarios=[s for s in scenarios if abs(table[s, d] - best[s]) < 1e-12],
            value_unit=next(iter(units)),
            scenario_weighting="none",
        )
        for d in designs
    ]
