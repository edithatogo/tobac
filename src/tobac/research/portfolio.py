"""Complementary reports with shared costs and once-only observed evidence."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, cast

import numpy as np
lazy from numpy.typing import ArrayLike

from tobac.information import evaluate, joint_likelihood, validate_likelihood
lazy from tobac.evidence import Belief

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from tobac._typing import FloatArray, Report


# Named bounds preserve the existing scientific/data contract.
MAX_JOINT_CELLS = 30000000


def ids(xs: Sequence[str], name: str, *, empty: bool = False) -> tuple[str, ...]:
    """Validate and freeze a sequence of unique nonempty identifiers."""
    if isinstance(xs, str):
        msg = f"{name} is a sequence, not one string"
        raise ValueError(msg)  # noqa: TRY004  # Retain the established ValueError domain-validation contract.
    v = tuple(xs)
    if (
        (not empty and not v)
        or any(not isinstance(cast("object", x), str) or not x.strip() for x in v)
        or len(v) != len(set(v))
    ):
        msg = f"Invalid {name}"
        raise ValueError(msg)
    return v


@dataclass(frozen=True)
class Source:
    """Prospective report likelihood bound to physical states, data identities and assets."""

    name: str
    likelihood: FloatArray
    data_ids: tuple[str, ...]
    state_ids: tuple[str, ...]
    assets: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate construction invariants and normalize the stored values."""
        if not isinstance(cast("object", self.name), str) or not self.name.strip():
            msg = "Source name required"
            raise ValueError(msg)
        for k in ("data_ids", "state_ids", "assets"):
            object.__setattr__(self, k, ids(getattr(self, k), k, empty=k == "assets"))
        likelihood_matrix = np.array(validate_likelihood(self.likelihood, len(self.state_ids)), copy=True)
        likelihood_matrix.setflags(write=False)
        object.__setattr__(self, "likelihood", likelihood_matrix)


@dataclass(frozen=True)
class Costs:
    """Direct and shared resource costs in one explicitly declared value unit."""

    value_unit: str
    direct: Mapping[str, float]
    shared: Mapping[str, float]

    def __post_init__(self) -> None:
        """Validate construction invariants and normalize the stored values."""
        if not isinstance(cast("object", self.value_unit), str) or not self.value_unit.strip():
            msg = "Declare cost unit"
            raise ValueError(msg)
        for name in ("direct", "shared"):
            d = dict(getattr(self, name))
            if any(not isinstance(k, str) or not k for k in d):
                msg = "Cost IDs required"
                raise ValueError(msg)
            for x in d.values():
                if isinstance(x, bool) or not np.isfinite(x) or x < 0:
                    msg = "Finite nonnegative costs required"
                    raise ValueError(msg)
            object.__setattr__(self, name, MappingProxyType(d))

    def price(self, sources: Sequence[Source], existing_assets: Sequence[str] = ()) -> float:
        """Price selected sources and shared assets exactly once."""
        existing = set(ids(existing_assets, "existing_assets", empty=True))
        if existing - set(self.shared):
            msg = "Unknown existing asset"
            raise ValueError(msg)
        names = [s.name for s in sources]
        if len(names) != len(set(names)):
            msg = "A source cannot be bought twice"
            raise ValueError(msg)
        assets: set[str] = set[str]().union(*(set(s.assets) for s in sources)) if sources else set[str]()
        if set(names) - set(self.direct) or assets - set(self.shared):
            msg = "Missing cost components"
            raise ValueError(msg)
        return float(sum(self.direct[n] for n in names) + sum(self.shared[a] for a in assets - existing))


def joint_report(sources: Sequence[Source], n: int, joint: ArrayLike | None = None) -> FloatArray:
    """Validate a joint tensor's marginals; otherwise assume conditional independence."""
    if not sources:
        if joint is not None:
            msg = "No-source experiment has no joint tensor"
            raise ValueError(msg)
        return np.ones((1, n))
    if joint is None:
        return joint_likelihood(*(s.likelihood for s in sources))
    shape = (*tuple(len(s.likelihood) for s in sources), n)
    a = np.asarray(joint, float)
    if a.shape != shape or a.size > MAX_JOINT_CELLS or not np.isfinite(a).all() or (a < 0).any():
        msg = "Finite nonnegative tensor matching all source outcomes required"
        raise ValueError(msg)
    for k, s in enumerate(sources):
        axes = tuple(j for j in range(len(sources)) if j != k)
        marginal = a.sum(axis=axes) if axes else a
        if not np.allclose(marginal, s.likelihood, rtol=0, atol=1e-11):
            msg = "Joint marginal differs from the declared source likelihood"
            raise ValueError(msg)
    return validate_likelihood(a.reshape(-1, n), n)


def portfolio_value(  # noqa: PLR0913  # Preserve explicit dimensioned inputs and the established API.
    belief: Belief,
    sources: Sequence[Source],
    costs: Costs,
    *,
    existing_assets: Sequence[str] = (),
    joint: ArrayLike | None = None,
    targets: Mapping[str, ArrayLike] | None = None,
) -> Report:
    """Evaluate new portfolio reports after checking shared states, data and cost units."""
    if costs.value_unit != belief.problem.value_unit:
        msg = "Information and costs require the same declared unit"
        raise ValueError(msg)
    if len({s.name for s in sources}) != len(sources):
        msg = "Duplicate source name"
        raise ValueError(msg)
    data: list[str] = []
    for s in sources:
        if s.state_ids != belief.state_ids:
            msg = "Physical state identity/order mismatch"
            raise ValueError(msg)
        belief.require_new_data(s.data_ids)
        data.extend(s.data_ids)
    if len(data) != len(set(data)):
        msg = "Overlapping underlying data; declare one joint source instead"
        raise ValueError(msg)
    report = joint_report(sources, len(belief.state_ids), joint)
    result = evaluate(belief.problem, report, targets)
    cost = costs.price(sources, existing_assets)
    result.update(
        cost=cost,
        enbs=result["evsi"] - cost,
        source_ids=[s.name for s in sources],
        prospective_data_ids=data,
        existing_data_ids=list(belief.used_data_ids),
        dependence="explicit joint tensor"
        if joint is not None
        else "independent conditional on the full shared state",
    )
    return result
