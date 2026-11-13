"""Finite decision-identification benchmark.

Runs bounded decision-sufficiency checks using the existing partial_identification
bounds (restriction_bounds, accounting_bounds) to show whether any unresolved
parameter can change the decision/action. No likelihood, posterior, or fitted
policy effect is produced. Unavailable inputs yield bounded/no-use findings,
not fabricated priors or labels.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]

from tobac.partial_identification import (  # noqa: E402 -- Select this checkout for direct CLI execution.
    Interval,
    accounting_bounds,
    restriction_bounds,
)

UNIT = Interval(1.0, 1.0)


def check_restriction_sufficiency(total: Interval | None, lawful: Interval | None) -> dict[str, Any]:
    """Test whether restriction bounds identify quitting/switching given available inputs."""
    result = restriction_bounds(total, lawful, total_bias=UNIT, lawful_bias=UNIT)
    return {
        "feasible": result.feasible,
        "quitting_lower": result.quitting.lower if result.quitting else None,
        "quitting_upper": result.quitting.upper if result.quitting else None,
        "switching_lower": result.switching.lower if result.switching else None,
        "switching_upper": result.switching.upper if result.switching else None,
        "quitting_span": (result.quitting.upper - result.quitting.lower if result.quitting else None),
        "switching_span": (result.switching.upper - result.switching.lower if result.switching else None),
        "parameter_point_identified": bool(
            result.feasible
            and result.quitting is not None
            and result.switching is not None
            and result.quitting.upper == result.quitting.lower
            and result.switching.upper == result.switching.lower
        ),
    }


def check_accounting_sufficiency(  # noqa: PLR0913, PLR0917 -- Explicit dimensioned accounting components.
    releases: Interval,
    reporting_bias: Interval,
    unrecorded: Interval,
    stock: Interval,
    outbound: Interval,
    wastage: Interval,
) -> dict[str, Any]:
    """Test whether accounting bounds identify lawful consumption given available inputs."""
    result = accounting_bounds(
        releases,
        reporting_bias=reporting_bias,
        unrecorded=unrecorded,
        stock=stock,
        outbound=outbound,
        wastage=wastage,
    )
    span = result.upper - result.lower
    return {
        "lawful_lower": result.lower,
        "lawful_upper": result.upper,
        "lawful_span": span,
        "parameter_point_identified": bool(span == 0),
    }


def run_benchmark() -> dict[str, Any]:
    """Run the finite decision-identification benchmark across all input scenarios."""
    results: dict[str, Any] = {}

    # Scenario 1: No total, no lawful observation (blocked baseline)
    results["no_total_no_lawful"] = check_restriction_sufficiency(None, None)

    # Scenario 2: Total only, no lawful (partial)
    results["total_only"] = check_restriction_sufficiency(Interval(0.8, 0.9), None)

    # Scenario 3: Lawful only, no total (partial)
    results["lawful_only"] = check_restriction_sufficiency(None, Interval(0.8, 0.8))

    # Scenario 4: Exact matched ratios (ideal but unavailable)
    results["exact_ratios"] = check_restriction_sufficiency(Interval(0.9, 0.9), Interval(0.72, 0.72))

    # Scenario 5: Incompatible model (empty, not clipped)
    results["incompatible"] = check_restriction_sufficiency(Interval(0.5, 0.6), Interval(0.8, 0.9))

    # Scenario 6: Accounting with known gaps (stock/lawful flow bridges missing)
    results["accounting_gapped"] = check_accounting_sufficiency(
        releases=Interval(90, 110),
        reporting_bias=Interval(0.9, 1.1),
        unrecorded=Interval(0, 2),
        stock=Interval(-5, 10),
        outbound=Interval(0, 3),
        wastage=Interval(0, 1),
    )

    # Scenario 7: Accounting with zero gaps (unavailable calibration)
    results["accounting_zero_gaps"] = check_accounting_sufficiency(
        releases=Interval(100, 100),
        reporting_bias=UNIT,
        unrecorded=Interval(0, 0),
        stock=Interval(0, 0),
        outbound=Interval(0, 0),
        wastage=Interval(0, 0),
    )

    # Summary: parameter point identification is separate from action identification.
    identifiable_count = sum(1 for v in results.values() if v.get("parameter_point_identified", False))
    total_scenarios = len(results)

    results["summary"] = {
        "total_scenarios": total_scenarios,
        "parameter_point_identified_scenarios": identifiable_count,
        "not_point_identified_scenarios": total_scenarios - identifiable_count,
        "parameter_point_identification_fraction": identifiable_count / total_scenarios
        if total_scenarios
        else 0.0,
        "decision_identification_assessed": False,
        "reason": "No action set or payoff function supplied; use decision_sufficiency.py",
    }

    return results


def write_benchmark(path: Path, results: dict[str, Any]) -> None:
    """Write the benchmark results as JSON."""
    output = {
        "schema": "tobac.decision_identification_benchmark.v2",
        "generated_by": "scripts/decision_identification_benchmark.py",
        "method": "restriction_bounds + accounting_bounds from tobac.partial_identification",
        "no_likelihood_posterior_fitted": True,
        "results": results,
    }
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(output, indent=2) + "\n")


def main() -> None:
    """Run the finite decision-identification benchmark."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Output benchmark JSON path")
    args = parser.parse_args()

    results = run_benchmark()
    write_benchmark(args.out, results)


if __name__ == "__main__":
    main()
