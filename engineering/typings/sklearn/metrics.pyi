# ruff: noqa: N803 -- Preserve the exercised upstream public X keyword.
from typing import Any

import numpy as np
from numpy.typing import NDArray

def silhouette_score(X: NDArray[np.float64], labels: NDArray[np.integer[Any]]) -> float: ...
def adjusted_rand_score(
    labels_true: NDArray[np.integer[Any]], labels_pred: NDArray[np.integer[Any]]
) -> float: ...
def balanced_accuracy_score(y_true: NDArray[np.integer[Any]], y_pred: NDArray[np.integer[Any]]) -> float: ...
def log_loss(
    y_true: NDArray[np.integer[Any]], y_proba: NDArray[np.float64], *, labels: NDArray[np.integer[Any]]
) -> float: ...
