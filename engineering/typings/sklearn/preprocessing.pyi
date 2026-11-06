# ruff: noqa: N803 -- Preserve the exercised upstream public X keyword.
from typing import Self

import numpy as np
from numpy.typing import NDArray

class StandardScaler:
    mean_: NDArray[np.float64]
    scale_: NDArray[np.float64]
    def fit(self, X: NDArray[np.float64]) -> Self: ...
    def transform(self, X: NDArray[np.float64]) -> NDArray[np.float64]: ...
