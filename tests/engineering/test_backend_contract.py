"""The optional backend must be explicit and fail rather than silently fall back."""

import importlib.metadata

import numpy as np
import pytest

from tobac._core import DecisionProblem
from tobac.backend import evpi


def problem():
    return DecisionProblem(np.array([[0.0, 4.0], [3.0, 0.0]]), ("a", "b"), "score", np.array([0.75, 0.25]))


def test_default_backend_retains_reference_and_unknown_names_fail() -> None:
    assert evpi(problem()) == 0.75
    with pytest.raises(
        ValueError,
        match=(r"^(?:Unsupported\ numerical\ backend)"),
    ):
        evpi(problem(), backend="auto")


def test_unqualified_optional_library_is_rejected(monkeypatch) -> None:
    monkeypatch.setattr(importlib.metadata, "version", lambda _: "unknown")
    with pytest.raises(RuntimeError, match="Unqualified"):
        evpi(problem(), backend="jax")
