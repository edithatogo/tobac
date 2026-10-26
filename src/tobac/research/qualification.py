"""Execute genuine installed-Voiage parity. No unavailable-package fallback."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import numpy as np

from tobac._core import DecisionProblem, exact_evpi, exact_partial_information
lazy from tobac._typing import Report

from .voiage_adapter import installed_evpi, installed_partial

# Named bounds preserve the existing scientific/data contract.
INVARIANT_ATOL = 1e-11


def qualify(path: str | Path) -> Report:
    """Record actual installed-library parity or an explicit blocked/failing result."""
    destination = Path(path)
    if destination.exists():
        msg = "Use a new qualification receipt"
        raise FileExistsError(msg)
    receipt: Report = {
        "schema": "tobac.voiage-qualification.v1",
        "expected_version": "2.2.0+tobac3151.2",
        "success": False,
        "installed_library_executed": False,
        "python": platform.python_version(),
        "status": "blocked",
        "checks": [],
        ("scope"): (
            "source-built compatibility EVPI on exact weighted and finite-partition transforms "
            "only; no generic EVSI or structural API certification"
        ),
    }
    cases = [
        ("uniform", [0.5, 0.5]),
        ("unequal", [0.9, 0.1]),
        ("zero_mass", [1.0, 0.0]),
        ("small_mass", [1e-8, 1 - 1e-8]),
    ]
    try:
        for name, weights in cases:
            p = DecisionProblem(
                np.asarray([[10.0, 0.0], [0.0, 10.0]]),
                ("a", "b"),
                "normalised fixture units",
                np.asarray(weights),
            )
            actual = installed_evpi(p)
            receipt["installed_library_executed"] = True
            error = abs(actual["value"] - exact_evpi(p))
            receipt["checks"].append(
                {"case": name, "error": error, "value": actual["value"], "unit": actual["value_unit"]}
            )
            if error > INVARIANT_ATOL or actual["value_unit"] != p.value_unit:
                msg = "Weighted Voiage parity failed"
                raise ArithmeticError(msg)  # noqa: TRY301  # Record failure or clean incomplete receipts in the enclosing handler.
        p = DecisionProblem(
            np.asarray([[10, 0], [0, 10], [10, 0], [0, 10]], dtype=float),
            ("a", "b"),
            "normalised fixture units",
            np.asarray([0.15, 0.15, 0.35, 0.35]),
        )
        labels = ["first", "first", "second", "second"]
        actual = installed_partial(p, labels)
        expected = exact_partial_information(p, labels)
        if abs(actual["value"] - expected) > INVARIANT_ATOL or expected != 0:
            msg = "Structure-only counterexample failed"
            raise ArithmeticError(msg)  # noqa: TRY301  # Record failure or clean incomplete receipts in the enclosing handler.
        receipt["checks"].append(
            {
                "case": "identical_structure_only",
                "value": actual["value"],
                "joint_perfect": exact_evpi(p),
                "expected_structure_only": 0.0,
            }
        )
        receipt.update(success=True, status="passed", version=actual["voiage_version"])
    except Exception as exc:  # noqa: BLE001  # Persist an explicit failing receipt; this path never reports success.
        receipt.update(
            error=repr(exc), status="failed" if receipt["installed_library_executed"] else "blocked"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return receipt


def main() -> None:
    """Parse command-line options, execute the selected operation and report its result."""
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    a = p.parse_args()
    result = qualify(a.out)
    print(json.dumps(result, indent=2))  # noqa: T201  # CLI emits the requested structured result on stdout.
    raise SystemExit(0 if result["success"] else 2)


if __name__ == "__main__":
    main()
