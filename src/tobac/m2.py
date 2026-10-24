"""Reproduce M2a: source-inspired retail structures and evidence-boundary checks."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from ._core import exact_evpi, exact_partial_information
from .regulation import load_config, grouped_labels, ACTIONS
from .retail_case import build_retail_states, retail_components, retail_problem, retail_channels, retail_studies
from .information import evaluate
from .evidence import Scope, Belief, EvidencePacket, condition, incremental_value, predictive, state_identifiers
from .supply import expected_releases, release_loglikelihood
from .run import write_csv


def run(config_path, out, *, quit_points=4, quick=False, grid_check=False):
    root=Path.cwd().resolve();path=Path(config_path).resolve();spec=json.loads(path.read_text())
    if spec['schema']!='tobac.m2.retail.v1':raise ValueError('Unknown M2 schema')
    base=load_config(root/spec['base_config'])
    sourcepath=root/'evidence/m2/source_review.json'
    source=json.loads(sourcepath.read_text())['sources'][0]
    if spec['source_id']!=source['id'] or spec['source_beta']!=[source['finding']['alpha'],source['finding']['beta']]:
        raise ValueError('Source-prior values differ from the extracted parameter record')
    out=Path(out)
    if out.exists() and any(out.iterdir()):raise FileExistsError('Use a new output directory')
    out.mkdir(parents=True,exist_ok=True)
    cases=spec['cases'][2:3] if quick else spec['cases']
    weights=[1.] if quick else spec['crime_weights']
    rows=[];partial=[];learning=[];summary=[];increments=[];checks=[];reference=None
    groups=['market','behaviour','criminal_harm','health_consequences','implementation','measurement','baseline_reachable']
    for case in cases:
        s,p,c=build_retail_states(base,quit_points=quit_points,transport=case['transport'],
                                null_weight=case['null_weight'],source_beta=spec['source_beta'])
        channels=retail_channels(s,c);designs=retail_studies(channels)
        components=retail_components(s,c,lawful_replacement=case['lawful_replacement'])
        event=(components['illicit'][:,1]-components['illicit'][:,0])/s['tobacco']>=base['scientific_event']['minimum_absolute_growth_fraction']
        for weight in weights:
            pr=retail_problem(s,p,c,weight,lawful_replacement=case['lawful_replacement'])
            evpi=exact_evpi(pr);key={'case':case['id'],'crime_weight':weight}
            summary.append(dict(key,states=len(p),quit_nodes=quit_points,mean_net_cessation=float(p@s['net_cessation']),
                evpi=evpi,preferred_action=ACTIONS[np.argmax(p@pr.values)],
                value_unit=pr.value_unit,scope=spec['scientific_status']))
            values={}
            for group in groups:
                val=exact_partial_information(pr,grouped_labels(s,c,group))
                partial.append(dict(key,group=group,evppi=val));values[group]=val
                checks.append(-1e-11<=val<=evpi+1e-11)
            for name,likelihood in designs.items():
                targets={'net_cessation':s['net_cessation'],'diversion':s['diversion'],
                         'current_illicit_share':s['illicit'],'criminal_harm':s['crime']} if weight==1 else None
                r=evaluate(pr,likelihood,targets,event=event,confidence=base['scientific_event']['confidence'])
                rows.append(dict(key,design=name,evsi=r['evsi'],evpi=evpi,
                    probability_action_changes=r['probability_action_changes'],
                    mean_effective_states=r['mean_effective_states'],minimum_effective_states=r['minimum_effective_states'],
                    resolution_probability=r['resolution_probability']))
                for target,stats in r['targets'].items():learning.append(dict(key,design=name,target=target,**stats))
                checks.extend([r['evsi']>=-1e-11,r['evsi']<=evpi+1e-11,r['posterior_martingale_max_error']<1e-11])
                if name=='panel_supply':checks.append(r['evsi']<=values['baseline_reachable']+1e-11)
            if case['id']=='source_shape_partial_replacement' and weight==1:
                reference=(s,p,c,pr,channels,designs)
    if reference is None:raise ValueError('A reference case/weight is required')
    s,p,c,pr,ch,designs=reference
    scope=Scope('synthetic representative catchment','all-resident exposure denominator',
                '2025-01-01','2025-12-31','cigarette_equivalents/1000/day')
    identities=state_identifiers(s)
    belief=Belief(pr,identities,scope)
    for first,second in [('legal_supply','anabasine'),('calibration','anabasine'),('policy_comparison','policy_lawful_comparison')]:
        result=incremental_value(belief,ch[first],ch[second])
        increments.append({'first':first,'next':second,**{k:v for k,v in result.items() if not isinstance(v,list)}})
        checks.extend([result['chain_error']<1e-11,abs(result['expected_remaining_evpi']-(result['initial_evpi']-result['first_evsi']))<1e-11])
    # Synthetic accounting/update fixture: NEVER label these as NZ observations.
    means=expected_releases(s['tobacco'],s['illicit'],s['tobacco']*s['unrecorded_lawful'],
                            reporting_multiplier=s['supply_ratio'])[:,None]
    synthetic=[]
    for observation in (250.,500.):
        packet=EvidencePacket(evidence_id=f'synthetic-release-{observation}',data_ids=(f'synthetic:{observation}',),
            source_ids=('constructed_fixture_not_field_data',),state_ids=identities,
            log_likelihood=release_loglikelihood([observation],means,[[80.**2]]),
            source_scope=scope,target_scope=scope,likelihood_model='synthetic Gaussian reporting error SD80',
            dependence_note='one observation conditional on shared state')
        after=condition(belief,packet)
        res=evaluate(after.problem,designs['panel'],{'diversion':s['diversion']})
        same=predictive(after,designs['panel'])
        synthetic.append({'synthetic_observation':observation,'assumed_sd':80.,'qualification':'synthetic fixture; NOT an empirical NZ update',
            'posterior_mean_illicit_share':float(after.problem.prior_weights@s['illicit']),
            'posterior_mean_diversion':float(after.problem.prior_weights@s['diversion']),
            'prior_mean_diversion':float(p@s['diversion']),
            'realised_panel_evsi_after_D0':res['evsi'],'remaining_evpi':exact_evpi(after.problem),
            'predictive_probability_sum':float(same.sum()),'receipt':after.receipts[0]})
        checks.extend([abs(after.problem.prior_weights@s['diversion']-p@s['diversion'])<1e-11,abs(same.sum()-1)<1e-11])
    grid=[]
    if grid_check:
        for nodes in (2,4,8):
            ss,pp,cc=build_retail_states(base,quit_points=nodes,source_beta=spec['source_beta'])
            prr=retail_problem(ss,pp,cc,lawful_replacement=.5);dd=retail_studies(retail_channels(ss,cc))
            for name in ('panel','panel_supply','causal_policy_study','causal_matched_total_and_lawful'):
                r=evaluate(prr,dd[name]);grid.append(dict(quit_nodes=nodes,states=len(pp),design=name,evpi=exact_evpi(prr),evsi=r['evsi']))
    outputs={'summary.csv':summary,'grouped_evppi.csv':partial,'study_value.csv':rows,
             'scientific_learning.csv':learning,'incremental_information.csv':increments,'grid_check.csv':grid}
    for name,data in outputs.items():write_csv(out/name,data)
    (out/'conditioning_fixtures.json').write_text(json.dumps(synthetic,indent=2)+'\n')
    validation={'passed':bool(all(checks)),'checks':len(checks),'cases':len(cases),'designs':len(designs),
                'quit_nodes':quit_points,'scientific_event':base['scientific_event'],'state_count_reference':len(p),'python':platform.python_version(),
                'numpy':np.__version__,'scipy':scipy.__version__,
                'scope':'exact conditional finite calculation; transported model input; no empirical posterior, national funding or continuous-convergence claim'}
    (out/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    package=Path(__file__).resolve().parent
    inputs={str(Path('src/tobac')/f.relative_to(package)):hashlib.sha256(f.read_bytes()).hexdigest() for f in package.glob('*.py')}
    for f in (path,root/spec['base_config'],sourcepath):inputs[str(f.relative_to(root))]=hashlib.sha256(f.read_bytes()).hexdigest()
    hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir() if f.is_file()}
    (out/'manifest.json').write_text(json.dumps({'schema':'tobac.run.v1','inputs':inputs,'outputs':hashes},indent=2)+'\n')
    if not all(checks):raise ArithmeticError('M2 invariant failed')
    return validation


def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default='configs/m2_retail.json');p.add_argument('--out',required=True)
    p.add_argument('--quit-points',type=int,default=4);p.add_argument('--quick',action='store_true');p.add_argument('--grid-check',action='store_true')
    a=p.parse_args();print(json.dumps(run(a.config,a.out,quit_points=a.quit_points,quick=a.quick,grid_check=a.grid_check),indent=2))

if __name__=='__main__':main()
