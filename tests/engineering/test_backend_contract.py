"""The optional backend must be explicit and fail rather than silently fall back."""
import importlib.metadata
import numpy as np
import pytest
from tobac._core import DecisionProblem
from tobac.backend import evpi


def problem():
    return DecisionProblem(np.array([[0.,4.],[3.,0.]]),('a','b'),'score',np.array([.75,.25]))


def test_default_backend_retains_reference_and_unknown_names_fail():
    assert evpi(problem()) == .75
    with pytest.raises(ValueError): evpi(problem(),backend='auto')


def test_unqualified_optional_library_is_rejected(monkeypatch):
    monkeypatch.setattr(importlib.metadata,'version',lambda _: 'unknown')
    with pytest.raises(RuntimeError,match='Unqualified'): evpi(problem(),backend='jax')
