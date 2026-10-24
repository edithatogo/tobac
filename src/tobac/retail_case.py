"""A prospective retail-licensing contrast, not a measured NZ causal effect.

Ait Ouakrim et al., doi:10.1136/tc-2022-057655, Table 2, use a
Beta(23.4,97.2) additional net-cessation input for ~300 outlets / 95% reduction.
It mixes previous modelling and stated intentions. It is NOT a likelihood of
current NZ outcomes and is not the M1 gross lawful-demand displacement fraction.
The ~600-outlet prospective case therefore retains explicit null/transport and
lawful-substitution scenarios. Equal smoking-intensity mapping is assumed.
"""
from __future__ import annotations
from copy import deepcopy
from itertools import product
from numbers import Integral
import numpy as np
from scipy.stats import beta
from ._core import DecisionProblem
from .regulation import ACTIONS, study_channels, studies
from .information import lognormal_bins, joint_likelihood


def build_retail_states(base_config, *, quit_points=4, transport=1., null_weight=.2,
                        source_beta=(23.4,97.2)):
    if (isinstance(quit_points,bool) or not isinstance(quit_points,Integral)
            or not 1<=quit_points<=16 or not np.isfinite([transport,null_weight]).all()
            or not 0<=transport<=1 or not 0<=null_weight<=1):
        raise ValueError('Declare finite bounded transport/null weight and 1..16 quantile nodes')
    a=np.asarray(source_beta,float)
    if a.shape!=(2,) or not np.isfinite(a).all() or (a<=0).any():
        raise ValueError('Positive beta shape parameters required')
    quantiles=beta.ppf((np.arange(quit_points)+.5)/quit_points,*a)*transport
    raw_values=np.r_[0.,quantiles]
    raw_weights=np.r_[null_weight,np.repeat((1-null_weight)/quit_points,quit_points)]
    values,inv=np.unique(raw_values,return_inverse=True)
    weights=np.bincount(inv,weights=raw_weights)
    keep=weights>0;values=values[keep];weights=weights[keep]
    c=deepcopy(base_config);axes=c['axes'];idx=[x['id'] for x in axes].index('restriction')
    axes[idx]={'id':'net_cessation','values':values.tolist(),'unit':'additional net cessation fraction',
               'group':'behaviour','status':'transported_model_input_plus_explicit_null',
               'source':'10.1136/tc-2022-057655 Table 2',
               'rationale':'Equal-intensity consumption mapping; different outlet cap and period; not observed efficacy'}
    axes.append({'id':'policy_supply_ratio','values':[.85,1.15],
                 'unit':'differential post/counterfactual lawful-supply bias multiplier',
                 'group':'measurement','status':'analyst_assumption',
                 'rationale':'Uncertain policy-period supply reconciliation; not measured precision'})
    ids=[x['id'] for x in axes]
    index=np.array(list(product(*(range(len(x['values'])) for x in axes))))
    s={axis['id']:np.asarray(axis['values'],float)[index[:,j]] for j,axis in enumerate(axes)}
    p=np.ones(len(index))
    for j,axis in enumerate(axes):
        p*=weights[index[:,j]] if j==idx else 1/len(axis['values'])
    p/=p.sum()
    c.update(schema='tobac.retail-case.v1',source_beta=a.tolist(),transport=transport,null_weight=null_weight,
             evidence_status='transported_published_model_input_not_causal_observation',
             time_scope='one-year prospective response; no lifetime health claim',
             policy_scope='smoked-tobacco retailer cap only; other policy components held constant')
    return s,p,c


def retail_components(s,c,*,lawful_replacement=0.):
    if not np.isfinite(lawful_replacement) or not 0<=lawful_replacement<=1:
        raise ValueError('Lawful replacement fraction must be between zero and one')
    required=('tobacco','illicit','net_cessation','diversion','mitigation','cessation','health','crime')
    arrays={k:np.asarray(s[k],float) for k in required}
    shape=arrays['tobacco'].shape
    if (len(shape)!=1 or not shape[0] or any(x.shape!=shape or not np.isfinite(x).all() for x in arrays.values())
            or any((arrays[k]<0).any() for k in required)
            or any((arrays[k]>1).any() for k in ('illicit','net_cessation','diversion','mitigation','cessation'))):
        raise ValueError('Finite state-aligned physical quantities/fractions required')
    t=arrays['tobacco'];i=t*arrays['illicit'];l=t-i
    remain=1-arrays['net_cessation']
    switched=l*remain*arrays['diversion']
    legal_r=l*remain-switched
    illicit_r=i*remain+switched
    removed=illicit_r*arrays['mitigation']
    legal=np.column_stack([l,legal_r,legal_r+removed*lawful_replacement,l*(1-arrays['cessation'])])
    illicit=np.column_stack([i,illicit_r,illicit_r-removed,i*(1-arrays['cessation'])])
    total=legal+illicit
    norm=float(c['reference_exposure'])
    if not np.isfinite(norm) or norm<=0:raise ValueError('Positive reference exposure required')
    costs=np.broadcast_to([c['policy_costs'][a] for a in ACTIONS],total.shape).copy()
    if not np.isfinite(costs).all() or (costs<0).any():raise ValueError('Finite nonnegative resource scores required')
    return {'total':total,'legal':legal,'illicit':illicit,
            'illicit_share':np.divide(illicit,total,out=np.zeros_like(total),where=total>0),
            'health_gain':arrays['health'][:,None]*(t[:,None]-total)/norm,
            'criminal_harm_change':arrays['crime'][:,None]*(illicit-i[:,None])/norm,
            'resource_cost':costs,'fiscal_volume_change':legal-l[:,None]}


def retail_problem(states,prior,config,crime_weight=1.,*,lawful_replacement=0.):
    if not np.isfinite(crime_weight) or crime_weight<0:raise ValueError('Declare nonnegative normative weight')
    d=retail_components(states,config,lawful_replacement=lawful_replacement)
    values=d['health_gain']-crime_weight*d['criminal_harm_change']-d['resource_cost']
    return DecisionProblem(values,ACTIONS,'normalised decision units; not NZD or QALYs',prior)


def retail_channels(s,c):
    d=retail_components(s,c)
    ch=study_channels(s,c,policy_ratio=d['total'][:,1]/s['tobacco'])
    # This report presupposes a matched causal comparison and accounting bridge.
    # It is NOT a chemical assay of illegality or an unadjusted release ratio.
    ratio=d['legal'][:,1]/d['legal'][:,0]*s['policy_supply_ratio']
    ch['policy_lawful_comparison']=lognormal_bins(ratio,.2,[.2,.5,.8])
    return ch


def retail_studies(ch):
    result=studies(ch)
    result['causal_matched_total_and_lawful']=joint_likelihood(ch['policy_comparison'],ch['policy_lawful_comparison'])
    result['panel_supply_and_matched_causal']=joint_likelihood(ch['anabasine'],ch['nicotine'],ch['legal_supply'],ch['policy_comparison'],ch['policy_lawful_comparison'])
    return result
