"""Exact multi-affine health-accounting sensitivity; not fitted policy effects."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any, cast

sys.path.insert(0, str(Path(__file__).resolve().parent))
from decision_sufficiency import assess
from reconcile_public_parameters import verify_hashes

ENDPOINT_COUNT = 2


def _support(values: list[str]) -> tuple[Fraction, Fraction]:
    if not isinstance(cast("object", values), list) or len(values) != ENDPOINT_COUNT:
        msg = "Two support endpoints required"
        raise ValueError(msg)
    if any(not isinstance(cast("object", value), str) for value in values):
        msg = "Exact rational string support endpoints required"
        raise TypeError(msg)
    try:
        low, high = map(Fraction, values)
    except (ValueError, ZeroDivisionError) as error:
        msg = "Invalid rational support"
        raise ValueError(msg) from error
    if low < 0 or low > high:
        msg = "Ordered nonnegative support required"
        raise ValueError(msg)
    return low, high


def accounting_box(
    response: list[str] | None,
    gain: list[str] | None,
    burden: list[str] | None,
) -> dict[str, Any]:
    """Bound e*d-c on a declared Cartesian box; extrema occur at its corners.

    Response is an avoided disease-person-year fraction, gain a descriptive
    utility contrast used as an accounting coefficient, burden health-equivalent
    loss over that same hypothetical year. No distributions or causal estimates.
    Unknown supports remain unknown. Joint covariance is not inferred.
    """
    if response is None or gain is None or burden is None:
        return {"status": "not_assessable_missing_restrictions", "empirical_admission": False}
    e, d, c = _support(response), _support(gain), _support(burden)
    if e[1] > 1:
        msg = "Response support must lie in [0,1]"
        raise ValueError(msg)
    corners = list(product(e, d, c))
    names = [f"corner_{i}" for i in range(len(corners))]
    advantage = [
        response_value * gain_value - burden_value for response_value, gain_value, burden_value in corners
    ]
    decision = assess(names, ["act", "wait"], [[str(value), "0"] for value in advantage])
    threshold = str(c[1] / d[0]) if d[0] > 0 else None
    return {
        "status": "conditional_accounting_only",
        "decision": decision,
        "advantage_lower": str(min(advantage)),
        "advantage_upper": str(max(advantage)),
        "minimum_response_for_weak_dominance": threshold,
        "threshold_within_response_domain": threshold is not None and Fraction(threshold) <= 1,
        "zero_gain_case": "zero burden permits weak dominance" if d[0] == 0 and c[1] == 0 else None,
        "corner_values": [
            {"state": name, "response": str(a), "gain": str(b), "burden": str(k), "advantage": str(v)}
            for name, (a, b, k), v in zip(names, corners, advantage, strict=True)
        ],
        "empirical_admission": False,
    }


def run_scenarios(root: Path, packet: dict[str, Any]) -> dict[str, Any]:
    """Bind published coefficients; scenario restrictions are explicitly hypothetical."""
    verify_hashes(root, packet["source_sha256"])
    if packet["utility_source"] not in packet["source_sha256"]:
        msg = "Unbound utility source"
        raise ValueError(msg)
    records = json.loads((root / packet["utility_source"]).read_text())["records"]
    by_id = {row["parameter_id"]: row for row in records}
    reference, disease = by_id["UTILITY_NO_LISTED"], by_id["UTILITY_COPD"]
    if reference["dependency_group"] != disease["dependency_group"]:
        msg = "Utility source dependence changed"
        raise ValueError(msg)
    point = Fraction(str(reference["value"])) - Fraction(str(disease["value"]))
    gains = {
        "published_mean_difference": (point, point),
        "marginal_interval_rectangle": (
            Fraction(str(reference["lower"])) - Fraction(str(disease["upper"])),
            Fraction(str(reference["upper"])) - Fraction(str(disease["lower"])),
        ),
    }
    cases = packet["scenarios"]
    if len({case["id"] for case in cases}) != len(cases):
        msg = "Duplicate scenario identity"
        raise ValueError(msg)
    results: dict[str, Any] = {}
    for case in cases:
        if case["gain_basis"] not in gains or _support(case["gain"]) != gains[case["gain_basis"]]:
            msg = "Scenario coefficient differs from its frozen source definition"
            raise ValueError(msg)
        results[case["id"]] = accounting_box(case["response"], case["gain"], case["burden"])
    return results


def main() -> None:
    """Execute a frozen, prespecified scenario packet and preserve prior outputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8"))
    results = run_scenarios(Path(__file__).resolve().parents[1], packet)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(
            {"input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(), "results": results},
            stream,
            indent=2,
        )
        stream.write("\n")


if __name__ == "__main__":
    main()
