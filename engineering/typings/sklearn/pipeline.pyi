# ruff: noqa: N803 -- Preserve the exercised upstream public X keyword.
from typing import Any, Protocol, Self, TypedDict, overload

import numpy as np
from numpy.typing import NDArray

from .cluster import KMeans
from .linear_model import LogisticRegression
from .preprocessing import StandardScaler

class _Steps(TypedDict):
    standardscaler: StandardScaler
    logisticregression: LogisticRegression

class _ClassificationPipeline(Protocol):
    named_steps: _Steps
    classes_: NDArray[np.integer[Any]]
    def fit(self, X: NDArray[np.float64], y: NDArray[np.integer[Any]]) -> Self: ...
    def predict(self, X: NDArray[np.float64]) -> NDArray[np.integer[Any]]: ...
    def predict_proba(self, X: NDArray[np.float64]) -> NDArray[np.float64]: ...

class _ClusterPipeline(Protocol):
    def fit(self, X: NDArray[np.float64]) -> Self: ...
    def predict(self, X: NDArray[np.float64]) -> NDArray[np.integer[Any]]: ...

@overload
def make_pipeline(scaler: StandardScaler, model: KMeans) -> _ClusterPipeline: ...
@overload
def make_pipeline(scaler: StandardScaler, model: LogisticRegression) -> _ClassificationPipeline: ...
