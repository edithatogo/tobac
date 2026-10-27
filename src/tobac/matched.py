"""Audit matched consumption metadata; never infer causal or empirical qualification.

This is an ingress feasibility check for M2, using the shared Scope contract. It
constructs no likelihood, EvidencePacket or posterior. A joint measurement model,
accounting corrections, counterfactual and held-out prediction remain external.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING

lazy from .evidence import Scope

if TYPE_CHECKING:
    from collections.abc import Sequence

CELLS = ("treated_before", "treated_after", "comparator_before", "comparator_after")
QUANTITIES = ("total_consumption", "lawful_consumption")


@dataclass(frozen=True)
class MatchedObservation:
    """Source identity and native scope; unknown scope stays explicitly absent."""

    observation_id: str
    cell: str
    quantity: str
    scope: Scope | None
    products: tuple[str, ...]
    data_ids: tuple[str, ...]
    role: str

    def __post_init__(self) -> None:
        """Reject ambiguous identities and unsupported cell/quantity labels."""
        if not self.observation_id.strip() or self.cell not in (*CELLS, "unassigned"):
            msg = "Declare an observation ID and supported cell"
            raise ValueError(msg)
        if self.quantity not in (*QUANTITIES, "prevalence", "releases"):
            msg = "Declare a supported native quantity"
            raise ValueError(msg)
        if not self.data_ids or any(not value.strip() for value in self.data_ids):
            msg = "Declare underlying data identities"
            raise ValueError(msg)
        if any(not value.strip() for value in self.products):
            msg = "Product labels must be nonempty"
            raise ValueError(msg)
        if len(set(self.data_ids)) != len(self.data_ids) or len(set(self.products)) != len(self.products):
            msg = "Data identities and product labels must be unique"
            raise ValueError(msg)


def _row_gaps(row: MatchedObservation) -> list[str]:
    gaps: list[str] = []
    for failed, label in (
        (row.scope is None, "scope_unknown"),
        (not row.products, "products_unknown"),
        (row.quantity not in QUANTITIES, "quantity_not_consumption"),
        (row.role != "observation", "role_not_observation"),
        (row.cell == "unassigned", "causal_cell_unassigned"),
        (
            row.scope is not None
            and date.fromisoformat(row.scope.start) == date.fromisoformat(row.scope.end),
            "empty_period",
        ),
    ):
        if failed:
            gaps.append(f"{row.observation_id}:{label}")
    return gaps


def _pair_gaps(index: dict[tuple[str, str], MatchedObservation]) -> list[str]:
    gaps: list[str] = []
    for cell in CELLS:
        total, lawful = (index.get((cell, quantity)) for quantity in QUANTITIES)
        if total is not None and lawful is not None:
            if total.scope != lawful.scope:
                gaps.append(f"{cell}:scope_mismatch")
            if set(total.products) != set(lawful.products):
                gaps.append(f"{cell}:product_mismatch")
    return gaps


def _longitudinal_gaps(index: dict[tuple[str, str], MatchedObservation]) -> list[str]:
    gaps: list[str] = []
    for arm in ("treated", "comparator"):
        for quantity in QUANTITIES:
            before, after = (index.get((f"{arm}_{period}", quantity)) for period in ("before", "after"))
            if before is not None and after is not None and before.scope and after.scope:
                a, b = before.scope, after.scope
                if date.fromisoformat(a.end) > date.fromisoformat(b.start):
                    gaps.append(f"{arm}:before_after_overlap_or_reverse")
                if (a.geography, a.population, a.unit, set(before.products)) != (
                    b.geography,
                    b.population,
                    b.unit,
                    set(after.products),
                ):
                    gaps.append(f"{arm}:longitudinal_scope_mismatch")
    return gaps


def _comparison_gaps(index: dict[tuple[str, str], MatchedObservation]) -> list[str]:
    gaps: list[str] = []
    for period in ("before", "after"):
        for quantity in QUANTITIES:
            treated, comparator = (
                index.get((f"{arm}_{period}", quantity)) for arm in ("treated", "comparator")
            )
            if treated is not None and comparator is not None and treated.scope and comparator.scope:
                a, b = treated.scope, comparator.scope
                same_window = tuple(map(date.fromisoformat, (a.start, a.end))) == tuple(
                    map(date.fromisoformat, (b.start, b.end))
                )
                if same_window and (a.geography, a.population, a.unit) == (b.geography, b.population, b.unit):
                    gaps.append(f"{period}:comparison_scope_identical")
                if not same_window:
                    gaps.append(f"{period}:comparison_window_mismatch")
                if (a.population, a.unit, set(treated.products)) != (
                    b.population,
                    b.unit,
                    set(comparator.products),
                ):
                    gaps.append(f"{period}:comparison_population_products_or_unit_mismatch")
    return gaps


def audit_pathway(rows: Sequence[MatchedObservation]) -> dict[str, object]:
    """Report metadata gaps without approving scientific declarations.

    All periods are half-open. Shared IDs are blocked here; a future justified
    joint likelihood must reconcile them through the existing evidence interface.
    Different labels cannot prove absence of undisclosed source overlap.
    """
    if len({row.observation_id for row in rows}) != len(rows):
        msg = "Observation IDs must be unique"
        raise ValueError(msg)
    index: dict[tuple[str, str], MatchedObservation] = {}
    gaps = [gap for row in rows for gap in _row_gaps(row)]
    used: set[str] = set()
    for row in rows:
        if used.intersection(row.data_ids):
            gaps.append("shared_data_requires_joint_model")
        used.update(row.data_ids)
        if row.cell != "unassigned" and row.quantity in QUANTITIES:
            key = (row.cell, row.quantity)
            if key in index:
                msg = "Duplicate cell/quantity; declare one joint observation representation"
                raise ValueError(msg)
            index[key] = row
    missing = [
        f"{cell}:{quantity}" for cell in CELLS for quantity in QUANTITIES if (cell, quantity) not in index
    ]
    gaps.extend(_pair_gaps(index))
    gaps.extend(_longitudinal_gaps(index))
    gaps.extend(_comparison_gaps(index))
    return {
        "status": "blocked" if gaps or missing else "metadata_compatible",
        "gaps": sorted(set(gaps)),
        "missing_cells": missing,
        "empirically_qualified": False,
        "conditioned": False,
        "limitation": "Metadata only; no causal identification, fitted covariance, governance or posterior",
    }
