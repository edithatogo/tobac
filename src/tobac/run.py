"""Reproduce the regulatory uncertainty milestone without modifying old outputs."""
from __future__ import annotations
import argparse, csv, hashlib, json, platform
from pathlib import Path
import numpy as np
import scipy
from tobac._core import exact_evpi, exact_partial_information
from .regulation import load_config, build_states, policy_components, make_problem, study_channels, studies, grouped_labels, ACTIONS
from .information import evaluate, scalar_oracle, same_data_robustness


def write_csv(path, rows):
    if not rows:return
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)


def run(config_path, out, quick=False):
    c=load_config(config_path);out=Path(out)
    if out.exists() and any(out.iterdir()):raise FileExistsError('Use a new empty output directory')
    out.mkdir(parents=True,exist_ok=True)
    s,p0=build_states(c);d=policy_components(s,c);channels=study_channels(s,c);designs=studies(channels)
    event=(d['illicit'][:,1]-d['illicit'][:,0])/s['tobacco']>=c['scientific_event']['minimum_absolute_growth_fraction']
    current_event=s['tobacco']*s['illicit']>=150.  # explicitly illustrative scientific magnitude
    groups=['market','behaviour','criminal_harm','health_consequences','implementation','measurement','baseline_reachable']
    targets={'current_illicit_share':s['illicit'],'current_illicit_volume':s['tobacco']*s['illicit'],
             'current_total_tobacco':s['tobacco'],'future_diversion':s['diversion'],'criminal_externality':s['crime']}
    cases=[(name,params,0.) for name,params in c['prior_scenarios'].items()]
    if not quick:
        cases += [(name,{},a) for name,a in c['dependence_scenarios'].items() if a]
    else:cases=cases[:1]
    summaries=[];partials=[];infos=[];science=[];ledgers=[];prices=[];incremental=[]
    checks=[];by_reference={}
    for name,prior_args,association in cases:
        _,p=build_states(c,prior_args,association)
        for weight in ([1.] if quick else c['crime_weights']):
            pr=make_problem(s,p,c,weight);a0=int(np.argmax(p@pr.values));ep=exact_evpi(pr)
            base={'prior':name,'crime_weight':weight}
            summaries.append(dict(base,prior_action=ACTIONS[a0],evpi=ep,**{a:float(p@pr.values[:,j]) for j,a in enumerate(ACTIONS)}))
            for j,a in enumerate(ACTIONS):
                ledgers.append(dict(base,action=a,**{k:float(p@v[:,j]) for k,v in d.items()}))
            pv={}
            for group in groups:
                pv[group]=exact_partial_information(pr,grouped_labels(s,c,group))
                partials.append(dict(base,parameter_group=group,evppi=pv[group],scope='exact EVPPI for declared finite variables, not estimated continuous EVPPI'))
            scores={}
            for design,l in designs.items():
                r=evaluate(pr,l,targets if weight==1 else None,event=event)
                scores[design]=r['evsi']
                infos.append(dict(base,design=design,**{k:v for k,v in r.items() if k not in ('targets','method','value_unit')}))
                if weight==1:
                    rc=evaluate(pr,l,event=current_event)
                    for target,v in r['targets'].items():science.append(dict(base,design=design,target=target,**v))
                    science.append(dict(base,design=design,target='current_illicit_volume_ge_150',resolution_probability=rc['resolution_probability'],prior_event_probability=rc['prior_event_probability'],event_brier_risk=rc['event_brier_risk']))
                    science.append(dict(base,design=design,target='policy_causes_material_absolute_illicit_growth',resolution_probability=r['resolution_probability'],prior_event_probability=r['prior_event_probability'],event_brier_risk=r['event_brier_risk']))
                if name=='balanced' and weight==1:
                    by_reference[design]=r
                    for scale in c['monetary_scales_nzd_per_unit']:
                        for cost in c['conditional_study_cost_grid_nzd']:
                            prices.append(dict(design=design,assumed_nzd_per_normalised_unit=scale,gross_value_nzd=r['evsi']*scale,assumed_study_cost_nzd=cost,enbs_nzd=r['evsi']*scale-cost,scope='normative monetary scale and hypothetical price; not NZ benefit estimate or quote'))
                checks.append(r['evsi']>=-1e-10 and r['evsi']<=ep+1e-10)
                checks.append(r['posterior_martingale_max_error']<1e-10)
            for first,second in [('panel','panel_supply'),('supply','panel_supply'),('panel_supply','better_quantification_supply'),('panel_supply','calibration_panel_supply'),('causal_policy_study','causal_and_harm')]:
                incremental.append(dict(base,existing_information=first,combined_information=second,incremental_evsi=scores[second]-scores[first],scope='prospective marginal information; for observed baseline data condition prior once first'))
            checks.append(scores['panel_supply']<=pv['baseline_reachable']+1e-10)
    # Common-data robustness, not a comparison of different simulated datasets.
    pr=make_problem(s,p0,c);priors=[build_states(c,{'diversion':q})[1] for q in (.2,.5,.8)]
    robust=[]
    for design,l in designs.items():
        robust.append(dict(design=design,**same_data_robustness(pr.values,priors,p0,l,event)))
    oracle=scalar_oracle(pr,designs['panel_supply'])
    vector=evaluate(pr,designs['panel_supply'])['evsi']
    checks.append(abs(oracle-vector)<1e-12)
    # Independent Monte Carlo over *exact outcome* probabilities: integration check.
    l=designs['panel_supply'];j=l*p0;prob=j.sum(1);post=j/prob[:,None]
    a0=np.argmax(p0@pr.values);g=np.max(post@(pr.values-pr.values[:,a0,None]),axis=1)
    draws=np.random.default_rng(20261024).choice(len(prob),size=50000,p=prob)
    mc=g[draws];se=mc.std(ddof=1)/np.sqrt(len(mc));checks.append(abs(mc.mean()-vector)<5*se+1e-12)
    outputs={'decision_summary.csv':summaries,'grouped_evppi.csv':partials,'study_value.csv':infos,'scientific_learning.csv':science,'same_data_robustness.csv':robust,'consequence_ledgers.csv':ledgers,'conditional_price_frontier.csv':prices,'incremental_information.csv':incremental}
    for f,rows in outputs.items():write_csv(out/f,rows)
    validation={'passed':bool(all(checks)),'checks':len(checks),'states':len(p0),'cases':len(cases),'designs':len(designs),'exact_oracle_error':abs(oracle-vector),'mc_check_estimate':float(mc.mean()),'mc_check_se':float(se),'exact_reference_evsi':vector,'method':'exact finite prior and coarsened outcomes; MC used only as independent check','scope':'conditional research; not current NZ posterior or policy recommendation','python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__}
    (out/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    root=Path(__file__).resolve().parents[2]
    inputs={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for pattern in ('src/**/*.py','configs/*.json') for p in root.glob(pattern)}
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file()}
    (out/'manifest.json').write_text(json.dumps({'schema':'tobac.run.v1','inputs':inputs,'outputs':hashes},indent=2)+'\n')
    if not all(checks):raise ArithmeticError('A numerical invariant failed; inspect outputs')
    return validation


def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default='configs/regulatory.json');p.add_argument('--out',required=True);p.add_argument('--quick',action='store_true')
    a=p.parse_args();print(json.dumps(run(a.config,a.out,a.quick),indent=2))

if __name__=='__main__':main()
