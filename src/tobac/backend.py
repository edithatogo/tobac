"""Explicit optional producer backend; NumPy remains the scientific reference."""

from __future__ import annotations

import importlib
import importlib.metadata

import numpy as np

from tobac._core import DecisionProblem, exact_evpi
from tobac.research.voiage_adapter import uniform_equivalent


def evpi(problem: DecisionProblem, *, backend: str = "numpy") -> float:
    """Use qualified Voiage JAX EVPI only on the exact weighted transform.

    Missing dependencies and unsupported versions fail; no fallback or generic
    EVSI/structural API qualification is implied by this operation.
    """
    if backend == "numpy":
        return exact_evpi(problem)
    if backend != "jax":
        msg = "Unsupported numerical backend"
        raise ValueError(msg)
    if importlib.metadata.version("voiage") != "2.2.0+tobac3151.1":
        msg = "Unqualified Voiage artifact for optional JAX EVPI"
        raise RuntimeError(msg)
    jax = importlib.import_module("jax")
    jax.config.update("jax_enable_x64", True)  # noqa: FBT003  # JAX uses a positional config value.
    array = jax.numpy.asarray(uniform_equivalent(problem), dtype="float64")
    if str(array.dtype) != "float64" or not jax.config.x64_enabled:
        msg = "JAX float64 qualification required"
        raise RuntimeError(msg)
    producer = importlib.import_module("voiage.main_backends")
    value = float(producer.JaxBackend().evpi(array))
    if not np.isfinite(value):
        msg = "Optional backend returned a nonfinite value"
        raise ArithmeticError(msg)
    return value
