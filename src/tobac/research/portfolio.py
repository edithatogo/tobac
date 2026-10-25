"""Complementary reports with shared costs and once-only observed evidence."""
from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from collections.abc import Mapping, Sequence
import numpy as np
from tobac.evidence import Belief
from tobac.information import _likelihood, joint_likelihood, evaluate


def ids(xs, name, *, empty=False):
    if isinstance(xs,str):raise ValueError(f'{name} is a sequence, not one string')
    v=tuple(xs)
    if ((not empty and not v) or any(not isinstance(x,str) or not x.strip() for x in v)
            or len(v)!=len(set(v))):raise ValueError(f'Invalid {name}')
    return v


@dataclass(frozen=True)
class Source:
    name: str
    likelihood: np.ndarray
    data_ids: tuple[str,...]
    state_ids: tuple[str,...]
    assets: tuple[str,...]=()

    def __post_init__(self):
        if not isinstance(self.name,str) or not self.name.strip():raise ValueError('Source name required')
        for k in ('data_ids','state_ids','assets'):
            object.__setattr__(self,k,ids(getattr(self,k),k,empty=k=='assets'))
        l=np.array(_likelihood(self.likelihood,len(self.state_ids)),copy=True)
        l.setflags(write=False);object.__setattr__(self,'likelihood',l)


@dataclass(frozen=True)
class Costs:
    value_unit: str
    direct: Mapping[str,float]
    shared: Mapping[str,float]

    def __post_init__(self):
        if not isinstance(self.value_unit,str) or not self.value_unit.strip():raise ValueError('Declare cost unit')
        for name in ('direct','shared'):
            d=dict(getattr(self,name))
            if any(not isinstance(k,str) or not k for k in d):raise ValueError('Cost IDs required')
            for x in d.values():
                if isinstance(x,bool) or not np.isfinite(x) or x<0:raise ValueError('Finite nonnegative costs required')
            object.__setattr__(self,name,MappingProxyType(d))

    def price(self, sources: Sequence[Source], existing_assets: Sequence[str]=()) -> float:
        existing=set(ids(existing_assets,'existing_assets',empty=True))
        if existing-set(self.shared):raise ValueError('Unknown existing asset')
        names=[s.name for s in sources]
        if len(names)!=len(set(names)):raise ValueError('A source cannot be bought twice')
        assets=set().union(*(set(s.assets) for s in sources)) if sources else set()
        if set(names)-set(self.direct) or assets-set(self.shared):raise ValueError('Missing cost components')
        return float(sum(self.direct[n] for n in names)+sum(self.shared[a] for a in assets-existing))


def joint_report(sources: Sequence[Source], n: int, joint=None) -> np.ndarray:
    """Validate a joint tensor's marginals; otherwise assume conditional independence."""
    if not sources:
        if joint is not None:raise ValueError('No-source experiment has no joint tensor')
        return np.ones((1,n))
    if joint is None:return joint_likelihood(*(s.likelihood for s in sources))
    shape=tuple(len(s.likelihood) for s in sources)+(n,)
    a=np.asarray(joint,float)
    if a.shape!=shape or a.size>30_000_000 or not np.isfinite(a).all() or (a<0).any():
        raise ValueError('Finite nonnegative tensor matching all source outcomes required')
    for k,s in enumerate(sources):
        axes=tuple(j for j in range(len(sources)) if j!=k)
        marginal=a.sum(axis=axes) if axes else a
        if not np.allclose(marginal,s.likelihood,rtol=0,atol=1e-11):
            raise ValueError('Joint marginal differs from the declared source likelihood')
    return _likelihood(a.reshape(-1,n),n)


def portfolio_value(belief: Belief, sources: Sequence[Source], costs: Costs,
                    *, existing_assets: Sequence[str]=(), joint=None, targets=None) -> dict:
    if costs.value_unit!=belief.problem.value_unit:raise ValueError('Information and costs require the same declared unit')
    if len({s.name for s in sources})!=len(sources):raise ValueError('Duplicate source name')
    data=[]
    for s in sources:
        if s.state_ids!=belief.state_ids:raise ValueError('Physical state identity/order mismatch')
        belief.require_new_data(s.data_ids);data.extend(s.data_ids)
    if len(data)!=len(set(data)):raise ValueError('Overlapping underlying data; declare one joint source instead')
    report=joint_report(sources,len(belief.state_ids),joint)
    result=evaluate(belief.problem,report,targets)
    cost=costs.price(sources,existing_assets)
    result.update(cost=cost,enbs=result['evsi']-cost,
                  source_ids=[s.name for s in sources],prospective_data_ids=data,
                  existing_data_ids=list(belief.used_data_ids),
                  dependence='explicit joint tensor' if joint is not None else 'independent conditional on the full shared state')
    return result
