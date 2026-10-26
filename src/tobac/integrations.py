"""Optional genuine voiage invocation; no silent fallback or resampling."""

import numpy as np


def voiage_evpi(values, strategy_names):
    from voiage.analysis import DecisionAnalysis
    from voiage.schema import ValueArray

    result = float(DecisionAnalysis(ValueArray.from_numpy(values, strategy_names=strategy_names)).evpi())
    expected = float(np.max(values, axis=1).mean() - np.max(values.mean(axis=0)))
    if not np.isclose(result, expected, rtol=1e-10, atol=1e-10):
        raise ArithmeticError("voiage/reference parity failure")
    return result
