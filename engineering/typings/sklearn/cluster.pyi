# ruff: noqa: N803 -- Preserve the exercised upstream public X keyword.
from typing import Any, Self

import numpy as np
from numpy.typing import NDArray

class KMeans:
    labels_: NDArray[np.integer[Any]]
    cluster_centers_: NDArray[np.float64]
    def __init__(self, *, n_clusters: int, n_init: int, random_state: int) -> None: ...
    def fit(self, X: NDArray[np.float64]) -> Self: ...
    def predict(self, X: NDArray[np.float64]) -> NDArray[np.integer[Any]]: ...
