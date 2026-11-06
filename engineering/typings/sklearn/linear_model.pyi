from typing import Any

import numpy as np
from numpy.typing import NDArray

class LogisticRegression:
    coef_: NDArray[np.float64]
    intercept_: NDArray[np.float64]
    classes_: NDArray[np.integer[Any]]
    def __init__(self, *, max_iter: int, random_state: int) -> None: ...
