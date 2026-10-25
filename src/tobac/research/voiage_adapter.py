"""Exact weighted adapter to Voiage EVPI; installed execution is fail-closed.

The transform is valid for expected-value EVPI ONLY. It is not a new PSA sample,
a probability model, or a valid input to risk/entropy/CEAC calculations.
"""
from __future__ import annotations
from collections.abc import Sequence
from importlib.metadata import version
import numpy as np
from tobac._core import DecisionProblem


def uniform_equivalent(problem: DecisionProblem) -> np.ndarray:
    """n*p_s*(V_sa-V_s0) converts weighted EVPI to uniform EVPI exactly.

    Zero-weight states remain zero rows. No integer replication, rounding or
    resampling is used. Values retain the input unit and are already scaled.
    """
    x=(len(problem.prior_weights)*problem.prior_weights[:,None])*(problem.values-problem.values[:,0,None])
    if not np.isfinite(x).all():
        raise ValueError('Weighted EVPI transform overflow')
    return x


def partition_problem(problem: DecisionProblem, labels: Sequence[object]) -> DecisionProblem:
    if len(labels)!=len(problem.prior_weights):raise ValueError('One partition label per state required')
    groups={}
    for i,label in enumerate(labels):
        try:groups.setdefault(label,[]).append(i)
        except TypeError as exc:raise ValueError('Partition labels must be hashable') from exc
    p=problem.prior_weights;v=problem.values-problem.values[:,0,None]
    masses=[];means=[]
    for indices in groups.values():
        mass=float(p[indices].sum())
        if mass>0:
            masses.append(mass);means.append(p[indices]@v[indices]/mass)
    return DecisionProblem(means,problem.action_names,problem.value_unit,masses)


def installed_evpi(problem: DecisionProblem, *, expected_version: str='2.2.0') -> dict:
    """Execute the actual released API; an unavailable package is an error."""
    installed=version('voiage')
    if installed!=expected_version:
        raise RuntimeError(f'Unqualified voiage version {installed}; expected {expected_version}')
    from voiage.methods.basic import evpi
    value=float(evpi(uniform_equivalent(problem)))
    if not np.isfinite(value):raise ArithmeticError('Voiage returned a nonfinite value')
    return {'value':value,'value_unit':problem.value_unit,'voiage_version':installed,
            'backend':'voiage.methods.basic.evpi','adapter':'exact nonnegative weighted-contrast transform',
            'population_scaling':'none; input already carries the decision scale'}


def installed_partial(problem: DecisionProblem, labels: Sequence[object]) -> dict:
    result=installed_evpi(partition_problem(problem,labels))
    result['estimand']='exact finite-partition EVPPI; not continuous regression EVPPI'
    return result
