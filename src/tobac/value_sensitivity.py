"""Conditional value frontiers; value weights are not empirical probabilities."""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations, product
from numbers import Real
from typing import TYPE_CHECKING, cast

import numpy as np

from ._core import DecisionProblem

if TYPE_CHECKING:
    from collections.abc import Sequence

    from numpy.typing import ArrayLike

    from tobac._typing import FloatArray

ATOL = 1e-11
CONSEQUENCE_COLUMNS = 3
MATRIX_NDIM = 2
VALUE_UNIT = "normalised decision units; not NZD or QALYs"


@dataclass(frozen=True)
class ValueWeights:
    """Declared trade-offs, with no population-preference interpretation."""

    health: float = 1.0
    crime: float = 1.0
    resource: float = 1.0

    def __post_init__(self) -> None:
        """Validate finite nonnegative trade-offs without a degenerate objective."""
        values = (self.health, self.crime, self.resource)
        if (
            any(
                isinstance(x, bool) or not isinstance(x, Real) or not math.isfinite(x) or x < 0
                for x in values
            )
            or max(values) == 0
        ):
            msg = "Value weights must be finite, nonnegative and not all zero"
            raise ValueError(msg)


DEFAULT_WEIGHTS = ValueWeights()


@dataclass(frozen=True)
class Consequences:
    """State/action-aligned components; no data ingestion or conditioning."""

    health: FloatArray
    crime: FloatArray
    resource: FloatArray

    def __post_init__(self) -> None:
        """Freeze aligned finite component copies and reject negative resources."""
        arrays = [np.array(x, dtype=float, copy=True) for x in (self.health, self.crime, self.resource)]
        if (
            arrays[0].ndim != MATRIX_NDIM
            or not min(arrays[0].shape)
            or any(x.shape != arrays[0].shape or not np.isfinite(x).all() for x in arrays)
        ):
            msg = "Finite nonempty state/action-aligned consequence matrices required"
            raise ValueError(msg)
        if (arrays[2] < 0).any():
            msg = "Nonnegative resource consequences required"
            raise ValueError(msg)
        for name, value in zip(("health", "crime", "resource"), arrays, strict=True):
            value.setflags(write=False)
            object.__setattr__(self, name, value)

    def problem(
        self,
        prior: FloatArray,
        weights: ValueWeights = DEFAULT_WEIGHTS,
        names: Sequence[str] | None = None,
    ) -> DecisionProblem:
        """Reuse the finite decision contract; keep signed criminal-harm changes."""
        labels = tuple(str(i) for i in range(self.health.shape[1])) if names is None else names
        values = weights.health * self.health - weights.crime * self.crime - weights.resource * self.resource
        return DecisionProblem(values, labels, VALUE_UNIT, prior)

    def expected(self, prior: FloatArray) -> FloatArray:
        """Return action-by-component means using the validated normalised prior."""
        weights = cast("FloatArray", self.problem(prior).prior_weights)
        return np.column_stack([weights @ x for x in (self.health, self.crime, self.resource)])


def optimal_indices(expected: ArrayLike) -> tuple[int, ...]:
    """Retain all numerically co-optimal actions, using absolute tolerance only."""
    values = np.asarray(expected, float)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all():
        msg = "A nonempty finite expected-value vector is required"
        raise ValueError(msg)
    return tuple(int(i) for i in np.flatnonzero(np.isclose(values, values.max(), atol=ATOL, rtol=0)))


def _bounds(bounds: tuple[float, float]) -> None:
    if not np.isfinite(bounds).all() or not 0 <= bounds[0] <= bounds[1]:
        msg = "Normative bounds must be finite, ordered and nonnegative"
        raise ValueError(msg)


def _means(means: FloatArray) -> None:
    if (
        means.ndim != MATRIX_NDIM
        or means.shape[1] != CONSEQUENCE_COLUMNS
        or not len(means)
        or not np.isfinite(means).all()
    ):
        msg = "Finite action means with three consequence columns required"
        raise ValueError(msg)


def box_optima(
    means: FloatArray, crime_bounds: tuple[float, float], resource_bounds: tuple[float, float]
) -> tuple[int, ...]:
    """Certify co-optimality across a continuous affine weight box by its vertices.

    Health weight is fixed at one. Each pairwise expected-value difference is
    affine, so its minimum over the rectangle occurs at a vertex. This does
    not certify choices outside the rectangle, across other priors, or under
    nonlinear objectives and equity constraints.
    """
    _means(means)
    _bounds(crime_bounds)
    _bounds(resource_bounds)
    candidates = set(range(len(means)))
    for crime, resource in product(crime_bounds, resource_bounds):
        candidates.intersection_update(optimal_indices(means @ np.array([1, -crime, -resource])))
    return tuple(sorted(candidates))


def crime_thresholds(
    means: FloatArray, resource_weight: float, crime_bounds: tuple[float, float]
) -> list[float]:
    """Find isolated upper-envelope ties, not intersections of dominated actions.

    Persistent parallel ties are represented by the co-optimal action sets,
    not an invented isolated threshold. Endpoints are included when optimal.
    """
    _means(means)
    _bounds(crime_bounds)
    _bounds((resource_weight, resource_weight))
    intercept = means[:, 0] - resource_weight * means[:, 2]
    roots: list[float] = []
    for first, second in combinations(range(len(means)), 2):
        slope = means[first, 1] - means[second, 1]
        if slope == 0:
            continue
        root = float((intercept[first] - intercept[second]) / slope)
        if not crime_bounds[0] <= root <= crime_bounds[1]:
            continue
        active = optimal_indices(intercept - root * means[:, 1])
        if first in active and second in active and not any(abs(root - x) <= ATOL for x in roots):
            roots.append(root)
    return sorted(roots)
