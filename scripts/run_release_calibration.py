"""Fit and challenge the annual reported-release component; never compute policy value."""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
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
from tobac_supply.release_calibration import (
    ReleaseGrid, boundary_mass, fit_release_process, forecast_summary,
    log_predictive_density, parse_release_export, sample_release_paths,
)
from tobac_supply.longitudinal import rolling_origin_forecasts

WINDOWS={'all_changes':None,'recent_4_changes':4,'recent_8_changes':8}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def reconcile_sources(root):
    root=Path(root)
    old=root/'data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv'
    raw=root/'data/calibration_20261024/raw/tobacco_returns_completion.txt'
    extracted=parse_release_export(raw.read_text(),range(2010,2026))
    existing=pd.read_csv(old)
    expected=[dict(year=int(r.year),tonnes=int(r.value)) for r in existing.itertuples()]
    if extracted!=expected:
        raise ValueError('Supplied completion conflicts with accepted series; investigate, do not overwrite')
    return dict(status='matched_all_rows',rows=len(extracted),
                new_independent_observations=0,
                accepted_table=str(old.relative_to(root)),accepted_sha256=sha(old),
                completion_receipt=str(raw.relative_to(root)),completion_sha256=sha(raw),
                workbook_independently_read=False,
                source_kind='conversation-supplied browser numerical-table extraction',
                source_run_id='d26e9dec-6327-41f7-a08e-ff95cb3fee3a',
                exclusions=['cigars','cigarillos','heated_tobacco'],
                unresolved=['mass_conversion','domestic_duty_free_basis'],
                note='Separate from rejected NZHS extraction; no workbook equivalence claim')


def interval_score(observed,lower,upper,alpha):
    return float(upper-lower + (2/alpha)*(max(lower-observed,0)+max(observed-upper,0)))


def hindcasts(years,values,grid,start_year,selection_end):
    rows=[]
    for name,window in WINDOWS.items():
        for index,year in enumerate(years):
            if year<start_year: continue
            posterior=fit_release_process(years,values,window=window,
                                          through_year=int(year)-1,grid=grid)
            pred=forecast_summary(posterior,[1])[0]
            observed=float(values[index])
            rows.append(dict(model=name,train_end_year=posterior.last_year,
                             first_change_year=posterior.first_change_year,
                             n_training_changes=posterior.n_changes,test_year=int(year),
                             observed_tonnes=observed,**{k:pred[k] for k in
                             ('mean','median','lower_95','upper_95','lower_80','upper_80')},
                             absolute_percentage_error=100*abs(pred['median']-observed)/observed,
                             squared_error=(pred['median']-observed)**2,
                             log_predictive_density=log_predictive_density(posterior,observed),
                             interval_score_95=interval_score(observed,pred['lower_95'],pred['upper_95'],.05),
                             covered_95=pred['lower_95']<=observed<=pred['upper_95'],
                             stage=('exploratory_selection_2015_2022' if year<=selection_end else 'reserved_diagnostic_2023_2025'),
                             vintage='single_2026_release_retrospective_not_realtime'))
    return rows


def figures(out,years,values,forecasts,checks,selected):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    matplotlib.rcParams['svg.hashsalt']='tobac-release-calibration-2.8.0'
    folder=out/'figures';folder.mkdir()
    def save(fig,stem):
        fig.tight_layout()
        fig.savefig(folder/(stem+'.png'),dpi=220)
        fig.savefig(folder/(stem+'.svg'),metadata={'Date':None})
        plt.close(fig)
    df=pd.DataFrame(forecasts);h=pd.DataFrame(checks)
    chosen=df[df.model==selected]
    fig,ax=plt.subplots(figsize=(10,5.7))
    ax.plot(years,values,'o-',label='Published releases, 2010–2025')
    ax.plot(chosen.year,chosen['median'],'o--',label=f'Conditional median: {selected.replace("_"," ")}')
    ax.fill_between(chosen.year,chosen.lower_95,chosen.upper_95,alpha=.14,label='95% predictive interval')
    ax.fill_between(chosen.year,chosen.lower_80,chosen.upper_80,alpha=.22,label='80% predictive interval')
    ax.axvline(2025.5,linestyle=':',alpha=.6)
    ax.set(xlabel='Calendar year',ylabel='Reported releases (tonnes/year)',
           title='NZ lawful smoked-tobacco releases: observations and conditional projection')
    ax.legend(fontsize=8,loc='upper right');ax.grid(axis='y',alpha=.2)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True)); ax.set_ylim(bottom=0)
    fig.text(.01,.01,'Reported releases are not total consumption or illicit supply. Later years are exploratory.',fontsize=8)
    fig.subplots_adjust(bottom=.16)
    save(fig,'01_reported_release_projection')
    fig,ax=plt.subplots(figsize=(9,4.8))
    one=df[df.horizon==1].reset_index(drop=True)
    for i,r in one.iterrows():
        ax.errorbar(r['median'],i,xerr=[[r['median']-r.lower_95],[r.upper_95-r['median']]],fmt='o',capsize=5)
    ax.set_yticks(range(len(one)),[m.replace('_',' ') for m in one.model])
    ax.axvline(values[-1],linestyle=':',label='2025 reported value')
    ax.set(xlabel='Projected 2026 reported releases (tonnes/year)',title='Structural sensitivity: 2026 release projection')
    ax.grid(axis='x',alpha=.2);ax.legend(fontsize=8)
    save(fig,'02_window_sensitivity')
    fig,ax=plt.subplots(figsize=(10,5.3))
    observed=h[h.model==selected]
    ax.plot(observed.test_year,observed.observed_tonnes,'o-',label='Held-out reported releases')
    ax.plot(observed.test_year,observed['median'],'s--',label='One-year-ahead predictive median')
    ax.fill_between(observed.test_year,observed.lower_95,observed.upper_95,alpha=.2,label='95% predictive interval')
    ax.axvline(2022.5,linestyle=':',label='Exploratory selection / reserved diagnostic split')
    ax.set(xlabel='Held-out observation year',ylabel='Reported releases (tonnes/year)',
           title='Retrospective predictive checks, using only earlier observations')
    ax.grid(axis='y',alpha=.2);ax.legend(fontsize=8)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    save(fig,'03_rolling_predictive_checks')
    (out/'FIGURE_CAPTIONS.md').write_text('''# Figure captions — release 2.8.0

1. **NZ reported lawful smoked-tobacco releases and conditional projection.** Observations
are the official numerical-table values, 2010–2025. The displayed candidate is chosen by
an exploratory 2015–2022 log-score comparison. Bands are conditional posterior-predictive
80% and 95% intervals, not uncertainty about illegal consumption or policy effects. 2026
is the primary horizon; 2027–2030 extrapolate constant transition parameters without shocks.

2. **Recency-window sensitivity for 2026.** Dots show posterior-predictive medians; whiskers
show 95% intervals for all-history, four-change and eight-change models. A window of four
changes uses five annual levels. Models are alternatives, not independent evidence.

3. **Retrospective one-step predictive checks.** Each target year is withheld from its own
fit. The source is one 2026 publication vintage, and the split was selected after the series
had been seen. This is not real-time validation, preregistration or blinded testing.

All figures: unit = reported tonnes/year. Excludes cigars/cigarillos and heated tobacco.
The domestic/duty-free and mass-conversion bases remain unresolved. NZ = New Zealand.
Predictive intervals include fitted drift and innovation uncertainty conditional on the
model/prior; not stock, source-definition, measurement-bias or future policy uncertainty.
Source: data/longitudinal_20261024/nz_tobacco_release_tonnes_2010_2025.csv.
''')


def run(out,quick=False,draws=None,skip_figures=False):
    out=Path(out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('A fresh, empty output directory is required')
    out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((ROOT/'configs/calibration_v2.8.0/model.json').read_text())
    grid=ReleaseGrid(**cfg['grid'])
    if quick: grid=replace(grid,mu_points=51,sigma_points=25)
    n=draws if draws is not None else (256 if quick else cfg['path_draws'])
    receipt=reconcile_sources(ROOT);save_json(out/'source_reconciliation.json',receipt)
    data=pd.read_csv(ROOT/cfg['source_table'])
    years=data.year.to_numpy(dtype=int);values=data.value.to_numpy(dtype=float)
    clean=pd.DataFrame({'year':years,'reported_tonnes':values.astype(int),
                        'year_on_year_percent':np.r_[np.nan,100*(values[1:]/values[:-1]-1)],
                        'source_id':data.source_id,'unit':data.unit})
    clean.to_csv(out/'reported_release_series.csv',index=False,float_format='%.12g')
    checks=hindcasts(years,values,grid,cfg['hindcast_start'],cfg['selection_end'])
    checkdf=pd.DataFrame(checks);checkdf.to_csv(out/'rolling_predictive_checks.csv',index=False,float_format='%.12g')
    score=(checkdf.groupby(['model','stage']).agg(n=('test_year','size'),
        mean_log_predictive_density=('log_predictive_density','mean'),
        mape_percent=('absolute_percentage_error','mean'),mse=('squared_error','mean'),
        coverage_95=('covered_95','mean'),mean_interval_score_95=('interval_score_95','mean')).reset_index())
    score['rmse_tonnes']=np.sqrt(score.pop('mse'))
    score.to_csv(out/'predictive_scores.csv',index=False,float_format='%.12g')
    select=score[score.stage=='exploratory_selection_2015_2022'].sort_values('mean_log_predictive_density',ascending=False)
    selected=str(select.iloc[0].model)
    save_json(out/'selection_receipt.json',dict(selected_for_display=selected,
        selection_years=[2015,2022],reserved_diagnostic_years=[2023,2024,2025],
        qualification=cfg['selection_qualification'],optimality_claim=False,
        all_candidates_retained=list(WINDOWS)))
    references=[]
    for method,window in [('last',None),('loglinear',4)]:
        for row in rolling_origin_forecasts(years,values,min_train=5,window=window,method=method):
            references.append(row)
    pd.DataFrame(references).to_csv(out/'point_reference_hindcasts.csv',index=False,float_format='%.12g')
    forecasts=[];parameters=[];posterior_cells=[];sensitivity=[];convergence=[];path_stats=[]
    for offset,(name,window) in enumerate(WINDOWS.items()):
        p=fit_release_process(years,values,window=window,grid=grid)
        summaries=forecast_summary(p,cfg['forecast_horizons'])
        forecasts.extend([dict(model=name,**r) for r in summaries])
        parameters.append(dict(model=name,n_changes=p.n_changes,first_change_year=p.first_change_year,
            last_year=p.last_year,mean_mu=float(p.weights@p.mu),mean_sigma=float(p.weights@p.sigma),
            outer_grid_mass=boundary_mass(p)))
        posterior_cells.append(pd.DataFrame({'model':name,'mu':p.mu,'sigma':p.sigma,'posterior_mass':p.weights}))
        paths=sample_release_paths(p,5,n,cfg['seed']+offset)
        pathdf=pd.DataFrame(paths['values'],columns=[str(y) for y in paths['years']])
        pathdf.insert(0,'posterior_sigma',paths['sigma']);pathdf.insert(0,'posterior_mu',paths['mu'])
        pathdf.insert(0,'path_id',np.arange(n));pathdf.to_csv(out/(name+'_joint_paths.csv'),index=False,float_format='%.12g')
        for i,row in enumerate(summaries):
            simulation_mean=float(paths['values'][:,i].mean())
            mcse=float(paths['values'][:,i].std(ddof=1)/np.sqrt(n)) if n>1 else None
            path_stats.append(dict(model=name,year=row['year'],draws=n,analytic_mean=row['mean'],
                simulation_mean=simulation_mean,mcse_mean=mcse))
        for attr in ['mu_prior_sd','sigma_prior_scale']:
            for scale in cfg['prior_scale_sensitivity']:
                alt=replace(grid,**{attr:scale})
                fit=fit_release_process(years,values,window=window,grid=alt)
                sensitivity.append(dict(model=name,varied=attr,prior_scale=scale,
                    **forecast_summary(fit,[1])[0]))
        fine=replace(grid,mu_points=2*grid.mu_points-1,sigma_points=2*grid.sigma_points-1)
        finepost=fit_release_process(years,values,window=window,grid=fine)
        for coarse,refined in zip(forecast_summary(p,[1,5]),forecast_summary(finepost,[1,5])):
            for measure in ['mean','median','lower_95','upper_95']:
                convergence.append(dict(model=name,horizon=coarse['horizon'],measure=measure,
                    coarse=coarse[measure],fine=refined[measure],
                    relative_difference=abs(coarse[measure]-refined[measure])/abs(refined[measure])))
    pd.DataFrame(forecasts).to_csv(out/'forecast_summary.csv',index=False,float_format='%.12g')
    pd.DataFrame(parameters).to_csv(out/'posterior_parameter_summary.csv',index=False,float_format='%.12g')
    pd.concat(posterior_cells).to_csv(out/'posterior_cells.csv',index=False,float_format='%.12g')
    pd.DataFrame(sensitivity).to_csv(out/'prior_sensitivity.csv',index=False,float_format='%.12g')
    pd.DataFrame(convergence).to_csv(out/'grid_convergence.csv',index=False,float_format='%.12g')
    pd.DataFrame(path_stats).to_csv(out/'monte_carlo_checks.csv',index=False,float_format='%.12g')
    save_json(out/'fit_scope.json',dict(status='partial_empirical_reported_release_calibration',
        country='NZ',observed_annual_levels=16,observation_years=[2010,2025],
        fitted_likelihood=cfg['likelihood'],grid_prior=asdict(grid),
        reported_values_treatment=cfg['reported_values_treatment'],
        unit=cfg['unit'],estimand=cfg['estimand'],
        consumption_bridge={'enabled':False,'requires':['source_scope_reconciliation','stock_and_visitor_adjustments','catchment_allocation','lawful_unrecorded_supply']},
        current_joint_wastewater_model_fitted=False,illicit_consumption_fitted=False,
        price_quote_received=False,funding_recommendation=False))
    if not skip_figures: figures(out,years,values,forecasts,checks,selected)
    source_paths=[cfg['source_table'],cfg['source_completion'],'configs/calibration_v2.8.0/model.json',
                  'scripts/run_release_calibration.py','src/tobac_supply/release_calibration.py',
                  'src/tobac_supply/longitudinal.py']
    save_json(out/'run_manifest.json',dict(version='2.8.0',analysis_date='2026-10-24',
        status='partial_empirical_reported_release_calibration',funding_recommendation=False,
        quick_mode=quick,figures_generated=not skip_figures,draws_per_model=n,seed=cfg['seed'],
        environment={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'pandas':pd.__version__},
        sources=[{'path':p,'sha256':sha(ROOT/p)} for p in source_paths],
        files=[{'path':str(p.relative_to(out)),'sha256':sha(p)} for p in sorted(out.rglob('*')) if p.is_file()]))
    return dict(out=str(out),selected_for_display=selected,observations=16,
                files=len(list(out.rglob('*'))),funding_recommendation=False)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--quick',action='store_true')
    parser.add_argument('--draws',type=int)
    parser.add_argument('--skip-figures',action='store_true')
    args=parser.parse_args()
    print(json.dumps(run(args.out,args.quick,args.draws,args.skip_figures),indent=2))


if __name__=='__main__':main()
