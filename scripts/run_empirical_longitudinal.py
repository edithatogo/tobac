"""Reproducible historical summary-data bridge; does not create current assay observations."""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import date
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
import scipy
from scipy.special import ndtri

from tobac_supply.consumption_ledger import lawful_ledger, annualised_supply, stock_scenario
from tobac_supply.empirical_longitudinal import (
    TemporalSpec, reconstruct_interval, fit_temporal, summarise_temporal,
    sample_temporal, map_discrepancy, predictive_log_density, observation_covariance,
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False)+'\n',encoding='utf-8')


def source_table(root=ROOT):
    p=Path(root)/'data/empirical_intake_20261024/nz_historical_legal_supply.csv'
    table=pd.read_csv(p)
    if table.year.tolist()!=list(range(2012,2024)):
        raise ValueError('Source years must be complete and unique: 2012–2023')
    if not (table.unit=='cigarette_equivalents/year').all():
        raise ValueError('Do not substitute a tonne series into the cigarette-equivalent source')
    if not (table.uplift_factor==1.23).all() or not (table.ryo_conversion_g_per_stick==.7).all():
        raise ValueError('Source convention changed; review rather than silently recalculate')
    if not np.array_equal(table.reported_upper_smoker_bound_consumption-table.legal_sales_cigarette_equivalent,
                          table.reported_signed_gap):
        raise ValueError('Source signed-gap arithmetic does not reconcile')
    return table


def period(year, alignment):
    if alignment=='calendar_replication':
        return f'{year}-01-01',f'{year+1}-01-01'
    if alignment=='documented_collection_sensitivity':
        if year==2021: return '2020-09-01','2021-09-01'
        if year==2022: return '2021-07-01','2022-08-01'
    if alignment not in {'nominal_survey_year','documented_collection_sensitivity'}:
        raise ValueError('Unknown alignment')
    return f'{year-1}-07-01',f'{year}-07-01'


def assembled_inputs(table, alignment='nominal_survey_year', centre='geometric_interval_midpoint'):
    """No synthetic rows: reconstruct each working summary from one published pair of limits."""
    ledger=lawful_ledger(table.year.tolist(),table.legal_sales_cigarette_equivalent.tolist(),np.zeros(len(table)+1))
    rows=[]
    for row in table.itertuples():
        # Common support for calendar comparisons: 2012 would need unavailable 2011 stick releases.
        if row.year==2012: continue
        start,end=period(row.year,alignment)
        aligned=annualised_supply(ledger,start,end)
        lo,hi=float(row.reported_lower_smoker_bound_consumption),float(row.reported_upper_smoker_bound_consumption)
        r=reconstruct_interval(lo,hi,row.uplift_factor)
        central=r['median_proxy']
        if centre=='arithmetic_interval_midpoint': central=(lo+hi)/2/row.uplift_factor
        elif centre=='published_upper_stress': central=hi/row.uplift_factor
        elif centre=='published_lower_stress': central=lo/row.uplift_factor
        elif centre!='geometric_interval_midpoint': raise ValueError('Unknown centre')
        a,b=date.fromisoformat(start),date.fromisoformat(end)
        t=((a.toordinal()+b.toordinal())/2-date(2000,1,1).toordinal())/365.2425+2000
        rows.append(dict(year=int(row.year),time=t,period_start=start,period_end=end,
                         alignment=alignment,centre_method=centre,
                         source_id=row.source_id,source_locator=row.source_locator,
                         observation_id=f'Phyo2025_NZHS_MOH_{row.year}',
                         source_lower_after_uplift=lo,source_upper_after_uplift=hi,
                         source_uplift_removed=float(row.uplift_factor),
                         reported_calendar_release=float(row.legal_sales_cigarette_equivalent),
                         matched_annual_release=aligned['value'],
                         reconstruction_median=central,reconstruction_log_se=r['log_se'],
                         log_reported_ratio=float(np.log(central/aligned['value'])),
                         unit='cigarette_equivalents/365_day_equivalent',
                         monthly_releases_observed=False,published_central_estimate=False,
                         covariance_status='count_interval_approximation_plus_declared_extra_error',
                         source_dependency='NZHS_and_MOH_derived_source_once',
                         source_interval='as_published_not_raw_sample_data'))
    return pd.DataFrame(rows)


def fit_frame(frame,spec):
    return fit_temporal(frame.time.tolist(),frame.log_reported_ratio.tolist(),
                        frame.reconstruction_log_se.tolist(),spec,
                        observation_ids=frame.observation_id.tolist())


def summarise_gap(name, frame, values, stock_days, unrecorded_fraction, visitor_fraction):
    rows=[]
    for index,row in enumerate(frame.itertuples()):
        gaps=values['signed_gap'][:,index]
        totals=values['survey_proxy'][:,index]
        q=np.quantile(gaps,[.025,.5,.975])
        rows.append(dict(scenario=name,year=row.year,
                         signed_gap_mean=float(np.mean(gaps)),signed_gap_median=float(q[1]),
                         signed_gap_lower95=float(q[0]),signed_gap_upper95=float(q[2]),
                         prob_positive_discrepancy=float(np.mean(gaps>0)),
                         proxy_median=float(np.median(totals)),
                         stock_days=stock_days,unrecorded_fraction=unrecorded_fraction,
                         visitor_fraction=visitor_fraction,
                         unit='cigarette_equivalents/365_day_equivalent',
                         interpretation='conditional_measurement_discrepancy_NOT_illicit_consumption'))
    return rows


def plots(out,frames,primary,latent,contrasts,sensitivity):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.rcParams['svg.hashsalt']='tobac-empirical-longitudinal-2.9.0'
    folder=out/'figures';folder.mkdir()
    def save(fig,name):
        fig.tight_layout(rect=(0,.055,1,1))
        fig.savefig(folder/(name+'.png'),dpi=240)
        fig.savefig(folder/(name+'.svg'),metadata={'Date':None})
        plt.close(fig)
    f=frames['nominal_survey_year']
    fig,ax=plt.subplots(figsize=(10,5.6))
    ax.plot(f.year,f.matched_annual_release/1e9,'o-',label='Period-matched recorded lawful supply')
    ax.plot(f.year,f.reconstruction_median/1e9,'s--',label='Reconstructed unadjusted survey centre')
    ax.fill_between(f.year,f.source_lower_after_uplift/f.source_uplift_removed/1e9,
                    f.source_upper_after_uplift/f.source_uplift_removed/1e9,alpha=.17,
                    label='Published count-bound range, fixed uplift removed')
    ax.set(xlabel='Survey-ending year',ylabel='Billion cigarette equivalents / 365 days',
           title='NZ historical consumption proxies and matched lawful releases')
    ax.grid(axis='y',alpha=.2);ax.legend(fontsize=8)
    fig.text(.02,.015,'The reconstructed centre is not a published point estimate. No current assay values are imputed.',fontsize=8)
    save(fig,'01_historical_source_alignment')
    fig,ax=plt.subplots(figsize=(10,5.6))
    ax.plot(f.year,np.exp(f.log_reported_ratio),'o',label='Interval-derived raw ratio')
    h=latent[latent.period_role=='historical']
    ax.plot(h.year,h.median_ratio,'-',label='Latent historical ratio, data-conditioned')
    ax.fill_between(h.year,h.lower_95_ratio,h.upper_95_ratio,alpha=.2,label='95% latent interval')
    fc=latent[latent.period_role=='extrapolation']
    ax.plot(fc.year,fc.median_ratio,'--',label='Unobserved extrapolation')
    ax.fill_between(fc.year,fc.lower_95_ratio,fc.upper_95_ratio,alpha=.12)
    ax.axhline(1,linestyle=':',label='Equal proxy and recorded supply')
    ax.set(xlabel='Year',ylabel='Survey-reported proxy / matched recorded supply',
           title='Historical observation-scale fit: no automatic inference of illegal origin')
    ax.grid(axis='y',alpha=.2);ax.legend(fontsize=8)
    fig.text(.02,.015,'2024–2026 ratios are model extrapolations only; no compatible current volume is reported.',fontsize=8)
    save(fig,'02_historical_ratio_posterior')
    fig,ax=plt.subplots(figsize=(9.5,5.3))
    base=contrasts[contrasts.scenario=='uplift_1.23_shared_0.2']
    ax.plot(base.year,base.signed_gap_median/1e6,'o-',label='Median signed discrepancy')
    ax.fill_between(base.year,base.signed_gap_lower95/1e6,base.signed_gap_upper95/1e6,alpha=.18,label='95% conditional interval')
    ax.axhline(0,linestyle=':')
    ax.set(xlabel='Survey-ending year',ylabel='Million cigarette equivalents / 365 days',
           title='Conditional discrepancy, not illicit consumption: uplift 1.23; common log SD 0.20')
    ax.grid(axis='y',alpha=.2);ax.legend(fontsize=8)
    fig.text(.02,.015,'Negative discrepancies are retained. Uplift and stock/channel corrections are not identified by these data.',fontsize=8)
    save(fig,'03_signed_discrepancy')
    end=contrasts[contrasts.year==2023].copy()
    fig,ax=plt.subplots(figsize=(10,8))
    y=np.arange(len(end));med=end.signed_gap_median.to_numpy()/1e6
    ax.errorbar(med,y,xerr=np.vstack([med-end.signed_gap_lower95.to_numpy()/1e6,
                    end.signed_gap_upper95.to_numpy()/1e6-med]),fmt='o',capsize=3)
    ax.set_yticks(y,end.scenario.str.replace('_',' ',regex=False),fontsize=8)
    ax.axvline(0,linestyle=':');ax.grid(axis='x',alpha=.2)
    ax.set(xlabel='2023 signed discrepancy (million cigarette equivalents)',
           title='Accounting and reporting assumptions change the discrepancy')
    fig.text(.02,.015,'Scenarios are alternatives, not extra observations. Points and bars are conditional medians and 95% intervals.',fontsize=8)
    save(fig,'04_assumption_sensitivity')
    fig,ax=plt.subplots(figsize=(10,5.4))
    for name,ff in frames.items():
        ax.plot(ff.year,np.exp(ff.log_reported_ratio),'o-',label=name.replace('_',' '))
    ax.set(xlabel='Survey-ending year',ylabel='Raw survey proxy / aligned recorded supply',
           title='A half-year calendar shift changes the historical comparison')
    ax.legend(fontsize=8);ax.grid(axis='y',alpha=.2)
    fig.text(.02,.015,'Within-year uniform allocation is an assumption; collection windows are approximate, not monthly observations.',fontsize=8)
    save(fig,'05_calendar_sensitivity')


def run(out,root=ROOT,quick=False):
    root=Path(root);out=Path(out)
    if out.exists() and any(out.iterdir()): raise ValueError('Output directory must be empty')
    out.mkdir(parents=True,exist_ok=True)
    config_path=root/'configs/empirical_longitudinal_v2.9.0/model.json'
    cfg=json.loads(config_path.read_text());c=cfg['temporal']
    spec=TemporalSpec(level_mean=c['level_mean'],level_sd=c['level_sd'],slope_sd=c['slope_sd'],
        process_grid=tuple(np.geomspace(c['process_grid_min'],c['process_grid_max'],c['process_grid_points'])),
        process_prior_scale=c['process_prior_scale'],intensity_cv=c['intensity_cv'],alignment_cv=c['alignment_cv'],
        residual_half_life_years=c['residual_half_life_years'])
    table=source_table(root)
    alignments=['nominal_survey_year','calendar_replication','documented_collection_sensitivity']
    frames={name:assembled_inputs(table,name) for name in alignments}
    pd.concat(frames.values(),ignore_index=True).to_csv(out/'aligned_observations.csv',index=False)
    primary=frames[cfg['primary_alignment']]
    fit=fit_frame(primary,spec)
    query_times=np.r_[primary.time.to_numpy(),primary.time.iloc[-1]+np.arange(1,4)]
    summary=pd.DataFrame(summarise_temporal(fit,query_times))
    summary.insert(0,'year',list(primary.year)+[2024,2025,2026])
    summary['period_role']=['historical']*len(primary)+['extrapolation']*3
    summary.to_csv(out/'latent_ratio_summary.csv',index=False)
    n=512 if quick else cfg['draws']
    paths=sample_temporal(fit,primary.time.tolist(),n,cfg['seed'])
    pd.DataFrame(paths,columns=[f'log_ratio_{y}' for y in primary.year]).to_csv(out/'joint_historical_paths.csv',index_label='path_id')
    pd.DataFrame({'annual_process_log_sd':spec.process_grid,'posterior_mass':fit.weights}).to_csv(out/'process_sd_posterior.csv',index=False)
    stock_rows=[];discrepancies=[]
    allreleases=table.legal_sales_cigarette_equivalent.to_numpy(float)
    ledger_scenarios=[('no_adjustment',0,0.,0.),('stock30',30,0.,0.),('stock60',60,0.,0.),
                      ('unrecorded2pct',0,.02,0.),('unrecorded5pct',0,.05,0.),
                      ('visitor_minus5pct',0,0.,-.05),('visitor_plus5pct',0,0.,.05)]
    ledgers={}
    for name,days,unrecorded,visitor in ledger_scenarios:
        ledger=lawful_ledger(table.year.tolist(),allreleases,stock_scenario(allreleases,days),
                             unrecorded=unrecorded*allreleases,net_visitors=visitor*allreleases)
        aligned=np.array([annualised_supply(ledger,r.period_start,r.period_end)['value'] for r in primary.itertuples()])
        ledgers[name]=aligned
        for j,y in enumerate(table.year):
            stock_rows.append(dict(scenario=name,year=int(y),release=ledger.releases[j],
                opening_stock=ledger.stocks[j],closing_stock=ledger.stocks[j+1],
                lawful_unrecorded=ledger.unrecorded[j],net_visitors=ledger.net_visitors[j],
                lawful_consumption=ledger.consumption[j],unit='cigarette_equivalents/calendar_year',
                evidence_status='published_release_plus_assumed_corrections'))
        if name!='no_adjustment':
            mapped=map_discrepancy(paths,primary.matched_annual_release,aligned,1.23,.2,seed=cfg['seed']+1)
            discrepancies.extend(summarise_gap(name,primary,mapped,days,unrecorded,visitor))
    for median in cfg['external_uplift_medians']:
        for sd in cfg['shared_uplift_log_sd']:
            name=f'uplift_{median:g}_shared_{sd:g}'
            mapped=map_discrepancy(paths,primary.matched_annual_release,ledgers['no_adjustment'],median,sd,seed=cfg['seed']+1)
            discrepancies.extend(summarise_gap(name,primary,mapped,0,0.,0.))
    pd.DataFrame(stock_rows).to_csv(out/'lawful_stock_ledgers.csv',index=False)
    gaps=pd.DataFrame(discrepancies);gaps.to_csv(out/'signed_discrepancy_sensitivity.csv',index=False)
    variants=[('primary',primary,spec),
              ('calendar',frames['calendar_replication'],spec),
              ('collection_calendar',frames['documented_collection_sensitivity'],spec),
              ('arithmetic_midpoint',assembled_inputs(table,centre='arithmetic_interval_midpoint'),spec),
              ('upper_centre_stress',assembled_inputs(table,centre='published_upper_stress'),spec),
              ('lower_centre_stress',assembled_inputs(table,centre='published_lower_stress'),spec),
              ('exclude_source_2014_arithmetic_issue',primary[primary.year!=2014],spec),
              ('intensity_cv_0',primary,replace(spec,intensity_cv=0)),
              ('intensity_cv_0.2',primary,replace(spec,intensity_cv=.2)),
              ('alignment_cv_0.15',primary,replace(spec,alignment_cv=.15)),
              ('correlated_alignment_1year',primary,replace(spec,alignment_cv=.15,residual_half_life_years=1.)),
              ('process_prior_scale_0.05',primary,replace(spec,process_prior_scale=.05)),
              ('process_prior_scale_0.2',primary,replace(spec,process_prior_scale=.2)),
              ('fine_grid',primary,replace(spec,process_grid=tuple(np.geomspace(.005,.35,81)))),
              ('extended_grid',primary,replace(spec,process_grid=tuple(np.geomspace(.001,.7,81))))]
    sens=[]
    for name,frame,s in variants:
        f=fit_frame(frame,s);result=summarise_temporal(f,[float(frame.time.iloc[-1])])[0]
        sens.append(dict(scenario=name,latest_year=int(frame.year.iloc[-1]),n_observations=len(frame),
                         **result,log_evidence=f.log_evidence,
                         endpoint_process_mass=float(f.weights[0]+f.weights[-1]),
                         interpretation='working_likelihood_sensitivity_not_model_probability'))
    sensitivity=pd.DataFrame(sens);sensitivity.to_csv(out/'fit_sensitivity.csv',index=False)
    checks=[]
    for alignment in alignments:
        ff=frames[alignment]
        for i,row in enumerate(ff.itertuples()):
            if row.year<cfg['hindcast_start_year']: continue
            train=ff.iloc[:i];p=fit_frame(train,spec)
            # Only prior observations supply anticipated precision for the held-out observation.
            predsd=float(np.sqrt(observation_covariance(train.time.to_numpy(),train.reconstruction_log_se.to_numpy(),spec)[-1,-1]))
            pred=summarise_temporal(p,[row.time],observation_se=predsd)[0]
            checks.append(dict(alignment=alignment,train_end=int(train.year.iloc[-1]),test_year=row.year,
                observed_log_ratio=row.log_reported_ratio,**pred,
                log_predictive_density=predictive_log_density(p,row.time,row.log_reported_ratio,predsd),
                covered95=pred['lower_95_log']<=row.log_reported_ratio<=pred['upper_95_log'],
                note='retrospective_current_vintage; shared calendar-supply inputs; not blinded or independent validation'))
    pd.DataFrame(checks).to_csv(out/'rolling_hindcasts.csv',index=False)
    # Preserve published values and flag the original Table 1 arithmetic inconsistency.
    published_lower=2149262500
    recomputed_lower=539000*3978.5
    save_json(out/'source_audit.json',dict(
        source_table_rows=len(table),paired_fit_rows=len(primary),
        omitted_2012='No 2011 cigarette-equivalent supply to align preceding survey half-year',
        source_2014_lower_count_arithmetic=dict(published=published_lower,
            stated_smokers_times_intensity=recomputed_lower,difference=published_lower-recomputed_lower,
            action='Preserved publication values; exclusion sensitivity run; no silent correction'),
        upper_bounds_not_points=True,fixed_source_uplift_removed_before_fit=True,
        raw_paired_nz_assays_added=0,published_monthly_supply_added=0,
        current_tonne_series_used_as_cigarette_equivalents=False,
        duplicate_survey_gap_and_intensity_likelihoods=False,
        consumption_origin_identified=False))
    save_json(out/'fit_scope.json',dict(estimand=cfg['estimand'],latest_paired_year=2023,
        current_joint_nz_posterior=False,current_assay_panel_fitted=False,
        likelihood='Gaussian summary approximation on raw survey proxy / matched release log ratio',
        accounting='Source conventions retained; timing/stock/scope corrections are assumptions',
        funding_recommendation=False,source_positive_gap_is_illicit=False,
        reference_uplift_status='source scenario partly anchored to same baseline; not independent evidence',
        spec=asdict(spec)))
    plots(out,frames,primary,summary,gaps,sensitivity)
    (out/'FIGURE_CAPTIONS.md').write_text('''# Historical consumption bridge figures — 2.9.0

All figures are generated from the checked-in source table and declared configuration.
PNG and vector SVG versions are supplied. No panel contains newly observed current assays.

1. **Historical source alignment.** Annual-equivalent lawful releases are allocated uniformly
within calendar years to the nominal survey interval. Shading is the published count-bound
range after removing the fixed 1.23 uplift, not complete consumption uncertainty. The dashed
centre is reconstructed from bounds; it is not an originally reported point estimate.
2. **Observation-scale trajectory fit.** Posterior median and 95% latent intervals for the
survey-reported / matched-supply ratio. 2024–2026 are unobserved extrapolations, not measurements
or a current consumption-volume estimate. Shared reporting bias is not identified by this fit.
3. **Signed discrepancy.** Posterior mapping with median uplift 1.23 and one shared log-SD 0.20
multiplier per path. No inventory/visitor correction in this figure. Negative values remain.
This is not an illicit-market probability or a measured illegal volume.
4. **Accounting and reporting sensitivity.** 2023 median and 95% conditional intervals under
alternative common uplift, inventory, lawful-unrecorded and visitor assumptions. The same
latent paths are reused; scenarios are not extra evidence. Assumptions are alternatives.
5. **Calendar sensitivity.** Raw derived ratios under calendar-year pairing, nominal survey
windows and documented collection-window sensitivity. No monthly series was inferred.

Abbreviations: NZ, New Zealand; NZHS, New Zealand Health Survey; RYO, roll-your-own; SD,
standard deviation; CI, confidence interval. Units use the source 365-day convention and
0.7 g per RYO equivalent; the administrative tonne series is not converted here.
''',encoding='utf-8')
    sources=[config_path,root/cfg['source'],Path(__file__),
             root/'src/tobac_supply/consumption_ledger.py',root/'src/tobac_supply/empirical_longitudinal.py',
             root/'src/tobac_supply/longitudinal.py']
    files=[p for p in sorted(out.rglob('*')) if p.is_file()]
    manifest=dict(version='2.9.0',analysis_date=cfg['analysis_date'],quick=quick,
        funding_recommendation=False,draws=n,seed=cfg['seed'],latest_paired_observation_year=2023,
        sources=[dict(path=str(p.relative_to(root)),sha256=digest(p)) for p in sources],
        files=[dict(path=str(p.relative_to(out)),sha256=digest(p)) for p in files],
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    save_json(out/'run_manifest.json',manifest)
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--quick',action='store_true')
    args=parser.parse_args();result=run(args.out,quick=args.quick)
    print(json.dumps({'artifacts':len(result['files']),'source_files':len(result['sources']),
                      'status':'historical_partial_empirical_bridge_not_current_illicit_or_funding_fit'},indent=2))
