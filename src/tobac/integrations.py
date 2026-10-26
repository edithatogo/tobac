"""Optional genuine voiage invocation; no silent fallback or resampling."""

import numpy as np

lazy from tobac._typing import FloatArray


def voiage_evpi(values: FloatArray, strategy_names: list[str] | None) -> float:
    """Invoke the optional Voiage backend and verify its finite-state EVPI parity."""
    from voiage.analysis import DecisionAnalysis  # pyright: ignore[reportMissingModuleSource]  # Optional runtime probe.  # noqa: PLC0415  # Keep optional dependencies and backend selection lazy.
    from voiage.schema import ValueArray  # pyright: ignore[reportMissingModuleSource]  # Optional runtime probe.  # noqa: PLC0415  # Keep optional dependencies and backend selection lazy.

    result = float(DecisionAnalysis(ValueArray.from_numpy(values, strategy_names=strategy_names)).evpi())
    expected = float(np.max(values, axis=1).mean() - np.max(values.mean(axis=0)))
    if not np.isclose(result, expected, rtol=1e-10, atol=1e-10):
        msg = "voiage/reference parity failure"
        raise ArithmeticError(msg)
    return result
