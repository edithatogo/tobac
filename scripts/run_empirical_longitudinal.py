"""Reproducible historical summary-data bridge; does not create current assay observations."""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import date
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import pandas as pd
import scipy
# from scipy.special import ndtri  # unused

from tobac_supply.consumption_ledger import (
    SupplyBasis, lawful_ledger, annualised_supply, stock_scenario,
)
from tobac_supply.empirical_longitudinal import (
    TemporalSpec, reconstruct_interval, fit_temporal, summarise_temporal,
    sample_temporal, map_discrepancy, predictive_log_density, observation_covariance,
)


def digest(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git(*args: str) -> str | None:
    """Best-effort provenance; absence is recorded as None rather than invented."""
    try:
        result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, check=False)
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def save_json(path: str | Path, data: Any) -> None:
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def source_table(root: Path = ROOT) -> pd.DataFrame:
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


ALIGNMENTS=('nominal_survey_year','calendar_replication','documented_collection_sensitivity')
CENTRES=('geometric_interval_midpoint','arithmetic_interval_midpoint',
         'published_upper_stress','published_lower_stress')
# Month-resolution bounds recorded in docs/empirical_longitudinal/METHODS_AND_ASSUMPTIONS_v2.9.0.md.
# They are half-open [start, end) windows: September 2020-August 2021 and July 2021-July 2022.
DOCUMENTED_WINDOWS={2021:('2020-09-01','2021-09-01'),2022:('2021-07-01','2022-08-01')}


def period(year: int, alignment: str) -> tuple[str, str]:
    if alignment == 'calendar_replication':
        return f'{year}-01-01', f'{year+1}-01-01'
    if alignment == 'documented_collection_sensitivity' and year in DOCUMENTED_WINDOWS:
        return DOCUMENTED_WINDOWS[year]
    if alignment not in {'nominal_survey_year', 'documented_collection_sensitivity'}:
        raise ValueError(f'Unknown alignment {alignment!r}')
    return f'{year-1}-07-01', f'{year}-07-01'


def period_origin(year: int, alignment: str) -> str:
    """Label which pairing convention produced a row; the arm name alone is ambiguous."""
    if alignment == 'calendar_replication':
        return 'calendar_year'
    if alignment == 'documented_collection_sensitivity' and year in DOCUMENTED_WINDOWS:
        return 'documented_window'
    return 'nominal_july_june_fallback'


def assembled_inputs(
    table: pd.DataFrame, *, alignment: str, centre: str
) -> list[dict[str, Any]]:
    """No synthetic rows: reconstruct each working summary from one published pair of limits.

    Both selectors are keyword-only and validated so an omitted argument cannot
    silently select a different scientific input.
    """
    if alignment not in ALIGNMENTS:
        raise ValueError(f'Unknown alignment {alignment!r}')
    if centre not in CENTRES:
        raise ValueError(f'Unknown centre {centre!r}')
    ledger = lawful_ledger(
        table.year.tolist(),
        table.legal_sales_cigarette_equivalent.tolist(),
        np.zeros(len(table) + 1),
        basis=SupplyBasis(),
    )
    rows: list[dict[str, Any]] = []
    previous_end: date | None = None
    for row in table.itertuples():
        start, end = period(row.year, alignment)
        # A period starting before the first release year has no annual total to
        # allocate. This only omits 2012 for windows that open in 2011; the
        # calendar replication of 2012 is fully supported and is retained.
        if int(start[:4]) < int(table.year.min()):
            continue
        aligned = annualised_supply(ledger, start, end)
        lo, hi = float(row.reported_lower_smoker_bound_consumption), float(row.reported_upper_smoker_bound_consumption)
        r = reconstruct_interval(lo, hi, row.uplift_factor)
        central = r['median_proxy']
        if centre == 'arithmetic_interval_midpoint':
            central = (lo + hi) / 2 / row.uplift_factor
        elif centre == 'published_upper_stress':
            central = hi / row.uplift_factor
        elif centre == 'published_lower_stress':
            central = lo / row.uplift_factor
        a, b = date.fromisoformat(start), date.fromisoformat(end)
        # Adjacent documented windows overlap, so their release denominators are
        # mechanically dependent. Record the size of the reuse instead of letting
        # the rows read as independent observations.
        overlap = 0 if previous_end is None else max(0, (previous_end - a).days)
        previous_end = b
        t = ((a.toordinal() + b.toordinal()) / 2 - date(2000, 1, 1).toordinal()) / 365.2425 + 2000
        rows.append(dict(
            year=int(row.year),
            time=t,
            period_start=start,
            period_end=end,
            alignment=alignment,
            centre_method=centre,
            period_origin=period_origin(row.year, alignment),
            overlap_days_with_previous_period=overlap,
            source_id=row.source_id,
            source_locator=row.source_locator,
            observation_id=f'Phyo2025_NZHS_MOH_{row.year}',
            source_lower_after_uplift=lo,
            source_upper_after_uplift=hi,
            source_uplift_removed=float(row.uplift_factor),
            reported_calendar_release=float(row.legal_sales_cigarette_equivalent),
            matched_annual_release=aligned['value'],
            reconstruction_median=central,
            reconstruction_log_se=r['log_se'],
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


CONFIG_KEYS=('version','analysis_date','source','estimand','primary_alignment','primary_centre',
             'source_uplift','source_ci_level','source_annual_days','ryo_grams_per_equivalent',
             'external_uplift_medians','shared_uplift_log_sd','base_shared_uplift_log_sd',
             'stock_days','unrecorded_lawful_fractions_of_releases',
             'net_visitor_fraction_sensitivity','hindcast_start_year','forecast_to',
             'draws','seed','assumptions','temporal')


def _finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)) \
            or not np.isfinite(value):
        raise ValueError(f'{name} must be a finite number; got {value!r}')
    return float(value)


def _unique(values, name, low=None, high=None, high_inclusive=False):
    """Validate a declared scenario list and reject duplicates instead of collapsing them."""
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
        raise ValueError(f'{name} must be a list of numbers; got {type(values).__name__}')
    out=[]
    for value in values:
        x=_finite(value, name)
        if low is not None and x<low:
            raise ValueError(f'{name} value {x!r} is below {low!r}')
        if high is not None and (x>high if high_inclusive else x>=high):
            raise ValueError(f'{name} value {x!r} must be '
                             + ('at most' if high_inclusive else 'strictly below') + f' {high!r}')
        out.append(x)
    if len(set(out))!=len(out):
        raise ValueError(f'{name} contains duplicate values: {values!r}')
    return out


def validate_config(cfg):
    """Fail before any write when a declared scientific input is missing or inconsistent."""
    if not isinstance(cfg, dict):
        raise ValueError('Configuration must be a JSON object')
    missing=[key for key in CONFIG_KEYS if key not in cfg]
    if missing:
        raise ValueError(f'Configuration is missing required keys: {", ".join(missing)}')
    if cfg['primary_alignment'] not in ALIGNMENTS:
        raise ValueError(f'primary_alignment={cfg["primary_alignment"]!r} is not one of {ALIGNMENTS}')
    if cfg['primary_centre'] not in CENTRES:
        raise ValueError(f'primary_centre={cfg["primary_centre"]!r} is not one of {CENTRES}')
    _finite(cfg['source_uplift'],'source_uplift')
    _finite(cfg['source_ci_level'],'source_ci_level')
    _finite(cfg['source_annual_days'],'source_annual_days')
    _finite(cfg['ryo_grams_per_equivalent'],'ryo_grams_per_equivalent')
    uplift=_unique(cfg['external_uplift_medians'],'external_uplift_medians',0)
    sds=_unique(cfg['shared_uplift_log_sd'],'shared_uplift_log_sd',0)
    _unique(cfg['stock_days'],'stock_days',0)
    _unique(cfg['unrecorded_lawful_fractions_of_releases'],
            'unrecorded_lawful_fractions_of_releases',0,1)
    _unique(cfg['net_visitor_fraction_sensitivity'],
            'net_visitor_fraction_sensitivity',-1,1)
    if float(cfg['source_uplift']) not in uplift:
        raise ValueError(f'source_uplift={cfg["source_uplift"]!r} must be one of '
                         f'external_uplift_medians={uplift!r}')
    if float(cfg['base_shared_uplift_log_sd']) not in sds:
        raise ValueError(f'base_shared_uplift_log_sd={cfg["base_shared_uplift_log_sd"]!r} '
                         f'must be one of shared_uplift_log_sd={sds!r}')
    if float(cfg['source_annual_days'])!=365.:
        raise ValueError(f'source_annual_days={cfg["source_annual_days"]!r} is not implemented; '
                         'annualised_supply and stock_scenario use the source 365-day convention')
    if float(cfg['source_ci_level'])!=.95:
        raise ValueError(f'source_ci_level={cfg["source_ci_level"]!r} is not implemented; '
                         'reconstruct_interval uses the 95% two-sided normal factor')
    if isinstance(cfg['forecast_to'],bool) or not isinstance(cfg['forecast_to'],int):
        raise ValueError(f'forecast_to must be an integer year; got {cfg["forecast_to"]!r}')
    if isinstance(cfg['hindcast_start_year'],bool) or not isinstance(cfg['hindcast_start_year'],int):
        raise ValueError('hindcast_start_year must be an integer year')
    if isinstance(cfg['draws'],bool) or not isinstance(cfg['draws'],int) or cfg['draws']<1:
        raise ValueError('draws must be a positive integer')
    if isinstance(cfg['seed'],bool) or not isinstance(cfg['seed'],int):
        raise ValueError('seed must be an integer')


def validate_horizon(cfg,last_year):
    if int(cfg['forecast_to'])<=int(last_year):
        raise ValueError(f'forecast_to={cfg["forecast_to"]!r} must exceed the last paired observation '
                         f'year {last_year}; otherwise there is no extrapolation to report')
    if int(cfg['hindcast_start_year'])>int(last_year):
        raise ValueError(f'hindcast_start_year={cfg["hindcast_start_year"]!r} is after the last '
                         f'paired observation year {last_year}')


def scenario_arms(cfg):
    """Build the declared accounting arms and prove none was dropped or duplicated."""
    stock=_unique(cfg['stock_days'],'stock_days',0)
    fractions=_unique(cfg['unrecorded_lawful_fractions_of_releases'],
                      'unrecorded_lawful_fractions_of_releases',0,1)
    visitors=_unique(cfg['net_visitor_fraction_sensitivity'],
                     'net_visitor_fraction_sensitivity',-1,1)
    arms=[('no_adjustment',0,0.,0.)]
    arms+=[(f'stock{days:g}',days,0.,0.) for days in stock if days]
    arms+=[(f'unrecorded{fraction*100:g}pct',0,float(fraction),0.)
           for fraction in fractions if fraction]
    arms+=[(f'visitor_{"minus" if visitor<0 else "plus"}{abs(visitor)*100:g}pct',
            0,0.,float(visitor)) for visitor in visitors if visitor]
    names=[arm[0] for arm in arms]
    if len(set(names))!=len(names):
        raise ValueError(f'scenario names collide: {names!r}; use distinct declared values')
    # The identity arm ('no_adjustment') is the declared zero of all three axes.
    emitted_stock={arm[1] for arm in arms};emitted_fraction={arm[2] for arm in arms}
    emitted_visitor={arm[3] for arm in arms}
    for declared,emitted,name in [(stock,emitted_stock,'stock_days'),
                                  (fractions,emitted_fraction,'unrecorded_lawful_fractions_of_releases'),
                                  (visitors,emitted_visitor,'net_visitor_fraction_sensitivity')]:
        if set(declared)!=emitted:
            raise ValueError(f'{name}={declared!r} was not reproduced by the emitted arms {sorted(emitted)!r}')
    return arms


def plots(out,frames,latent,contrasts,base_uplift,base_shared,primary_alignment,latest_year,version):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.rcParams['svg.hashsalt']=f'tobac-empirical-longitudinal-{version}'
    folder=out/'figures';folder.mkdir()
    def save(fig,name):
        fig.tight_layout(rect=(0,.055,1,1))
        fig.savefig(folder/(name+'.png'),dpi=240)
        fig.savefig(folder/(name+'.svg'),metadata={'Date':None})
        plt.close(fig)
    if primary_alignment not in frames:
        raise ValueError(f'primary_alignment={primary_alignment!r} has no assembled frame')
    f=frames[primary_alignment]
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
    fig.text(.02,.015,f'{int(fc.year.min())}\u2013{int(fc.year.max())} ratios are model extrapolations only; no compatible current volume is reported.',fontsize=8)
    save(fig,'02_historical_ratio_posterior')
    fig,ax=plt.subplots(figsize=(9.5,5.3))
    base=contrasts[contrasts.scenario==f'uplift_{base_uplift:g}_shared_{base_shared:g}']
    expected=len(latent[latent.period_role=='historical'])
    if len(base)!=expected or len(base)==0:
        raise ValueError(f'Base scenario uplift_{base_uplift:g}_shared_{base_shared:g} produced '
                         f'{len(base)} rows; expected {expected}. Check that source_uplift and '
                         'base_shared_uplift_log_sd are declared sensitivity values.')
    ax.plot(base.year,base.signed_gap_median/1e6,'o-',label='Median signed discrepancy')
    ax.fill_between(base.year,base.signed_gap_lower95/1e6,base.signed_gap_upper95/1e6,alpha=.18,label='95% conditional interval')
    ax.axhline(0,linestyle=':')
    ax.set(xlabel='Survey-ending year',ylabel='Million cigarette equivalents / 365 days',
           title=f'Conditional discrepancy, not illicit consumption: uplift {base_uplift:g}; common log SD {base_shared:.2f}')
    ax.grid(axis='y',alpha=.2);ax.legend(fontsize=8)
    fig.text(.02,.015,'Negative discrepancies are retained. Uplift and stock/channel corrections are not identified by these data.',fontsize=8)
    save(fig,'03_signed_discrepancy')
    end=contrasts[contrasts.year==latest_year].copy()
    if end.empty:
        raise ValueError(f'No discrepancy rows for latest paired year {latest_year}')
    fig,ax=plt.subplots(figsize=(10,8))
    y=np.arange(len(end));med=end.signed_gap_median.to_numpy()/1e6
    ax.errorbar(med,y,xerr=np.vstack([med-end.signed_gap_lower95.to_numpy()/1e6,
                    end.signed_gap_upper95.to_numpy()/1e6-med]),fmt='o',capsize=3)
    ax.set_yticks(y,end.scenario.str.replace('_',' ',regex=False),fontsize=8)
    ax.axvline(0,linestyle=':');ax.grid(axis='x',alpha=.2)
    ax.set(xlabel=f'{latest_year} signed discrepancy (million cigarette equivalents per 365-day equivalent)',
           title=f'Signed discrepancy in {latest_year} under alternative accounting and reporting assumptions')
    fig.text(.02,.015,'Scenarios are alternatives, not extra observations. Points and bars are conditional medians and 95% intervals.',fontsize=8)
    save(fig,'04_assumption_sensitivity')
    fig,ax=plt.subplots(figsize=(10,5.4))
    for name,ff in frames.items():
        ax.plot(ff.year,np.exp(ff.log_reported_ratio),'o-',label=name.replace('_',' '))
    ax.set(xlabel='Survey-ending year',ylabel='Raw survey proxy / aligned recorded supply',
           title='Raw ratio under three period-pairing conventions')
    ax.legend(fontsize=8);ax.grid(axis='y',alpha=.2)
    fig.text(.02,.015,'Within-year uniform allocation is an assumption; collection windows are approximate, not monthly observations.',fontsize=8)
    save(fig,'05_calendar_sensitivity')


def run(out,root=ROOT,quick=False):
    root=Path(root);out=Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError(f'Output directory {out} is not empty; choose a new --out or remove it deliberately')
    # Validate every declared input before creating the directory or writing anything.
    config_path=root/'configs/empirical_longitudinal_v2.9.0/model.json'
    cfg=json.loads(config_path.read_text());c=cfg['temporal']
    validate_config(cfg)
    spec=TemporalSpec(level_mean=c['level_mean'],level_sd=c['level_sd'],slope_sd=c['slope_sd'],
        process_grid=tuple(np.geomspace(c['process_grid_min'],c['process_grid_max'],c['process_grid_points'])),
        process_prior_scale=c['process_prior_scale'],intensity_cv=c['intensity_cv'],alignment_cv=c['alignment_cv'],
        residual_half_life_years=c['residual_half_life_years'])
    base_uplift=float(cfg['source_uplift'])
    base_shared=float(cfg['base_shared_uplift_log_sd'])
    table=source_table(root)
    # The config and the source table must agree; neither may silently override the other.
    if set(table.uplift_factor.unique())!={base_uplift}:
        raise ValueError(f'source_uplift={base_uplift!r} does not match source table '
                         f'uplift_factor={sorted(set(table.uplift_factor.unique()))!r}')
    if set(table.ryo_conversion_g_per_stick.unique())!={float(cfg['ryo_grams_per_equivalent'])}:
        raise ValueError('ryo_grams_per_equivalent does not match the source table convention '
                         f'{sorted(set(table.ryo_conversion_g_per_stick.unique()))!r}')
    frames={name:assembled_inputs(table,alignment=name,centre=cfg['primary_centre'])
            for name in ALIGNMENTS}
    primary=frames[cfg['primary_alignment']]
    last_year=int(primary.year.iloc[-1])
    validate_horizon(cfg,last_year)
    out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames.values(),ignore_index=True).to_csv(out/'aligned_observations.csv',index=False)
    fit=fit_frame(primary,spec)
    future_years=list(range(last_year+1,int(cfg['forecast_to'])+1))
    query_times=np.r_[primary.time.to_numpy(),primary.time.iloc[-1]+np.arange(1,len(future_years)+1)]
    summary=pd.DataFrame(summarise_temporal(fit,query_times))
    summary.insert(0,'year',list(primary.year)+future_years)
    summary['period_role']=['historical']*len(primary)+['extrapolation']*len(future_years)
    summary.to_csv(out/'latent_ratio_summary.csv',index=False)
    n=512 if quick else cfg['draws']
    paths=sample_temporal(fit,primary.time.tolist(),n,cfg['seed'])
    pd.DataFrame(paths,columns=[f'log_ratio_{y}' for y in primary.year]).to_csv(out/'joint_historical_paths.csv',index_label='path_id')
    pd.DataFrame({'annual_process_log_sd':spec.process_grid,'posterior_mass':fit.weights}).to_csv(out/'process_sd_posterior.csv',index=False)
    stock_rows=[];discrepancies=[]
    allreleases=table.legal_sales_cigarette_equivalent.to_numpy(float)
    # Scenario arms are declared in the config and reconciled against the emitted
    # names, so an edited configuration cannot silently leave the runner on stale
    # assumptions or drop a declared arm.
    ledger_scenarios=scenario_arms(cfg)
    ledgers={}
    for name,days,unrecorded,visitor in ledger_scenarios:
        ledger=lawful_ledger(table.year.tolist(),allreleases,stock_scenario(allreleases,days),
                             unrecorded=unrecorded*allreleases,net_visitors=visitor*allreleases,
                             basis=SupplyBasis())
        aligned=np.array([annualised_supply(ledger,r.period_start,r.period_end)['value'] for r in primary.itertuples()])
        ledgers[name]=aligned
        for j,y in enumerate(table.year):
            stock_rows.append(dict(scenario=name,year=int(y),release=ledger.releases[j],
                opening_stock=ledger.stocks[j],closing_stock=ledger.stocks[j+1],
                lawful_unrecorded=ledger.unrecorded[j],net_visitors=ledger.net_visitors[j],
                lawful_consumption=ledger.consumption[j],unit='cigarette_equivalents/calendar_year',
                evidence_status='published_release_plus_assumed_corrections'))
        if name!='no_adjustment':
            mapped=map_discrepancy(paths,primary.matched_annual_release,aligned,base_uplift,base_shared,seed=cfg['seed']+1)
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
              ('arithmetic_midpoint',assembled_inputs(table,alignment=cfg['primary_alignment'],
                                                      centre='arithmetic_interval_midpoint'),spec),
              ('upper_centre_stress',assembled_inputs(table,alignment=cfg['primary_alignment'],
                                                      centre='published_upper_stress'),spec),
              ('lower_centre_stress',assembled_inputs(table,alignment=cfg['primary_alignment'],
                                                      centre='published_lower_stress'),spec),
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
    for alignment in ALIGNMENTS:
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
        paired_fit_rows_by_alignment={name:len(frame) for name,frame in frames.items()},
        period_overlap_days_by_alignment={
            name:int(frame.overlap_days_with_previous_period.max()) for name,frame in frames.items()},
        period_overlap_status='Overlapping periods reuse the same release tonnage; those rows are '
                              'not independent and no cross-period error term is fitted.',
        omitted_2012='Only windows opening before 2012 are omitted: no 2011 cigarette-equivalent '
                     'supply exists to allocate. The calendar replication of 2012 is retained.',
        source_2014_lower_count_arithmetic=dict(published=published_lower,
            stated_smokers_times_intensity=recomputed_lower,difference=published_lower-recomputed_lower,
            action='Preserved publication values; exclusion sensitivity run; no silent correction'),
        upper_bounds_not_points=True,fixed_source_uplift_removed_before_fit=True,
        raw_paired_nz_assays_added=0,published_monthly_supply_added=0,
        current_tonne_series_used_as_cigarette_equivalents=False,
        duplicate_survey_gap_and_intensity_likelihoods=False,
        consumption_origin_identified=False))
    save_json(out/'fit_scope.json',dict(estimand=cfg['estimand'],latest_paired_year=last_year,
        primary_alignment=cfg['primary_alignment'],primary_centre=cfg['primary_centre'],
        version=cfg['version'],assumptions=cfg['assumptions'],
        current_joint_nz_posterior=False,current_assay_panel_fitted=False,
        likelihood='Gaussian summary approximation on raw survey proxy / matched release log ratio',
        accounting='Source conventions retained; timing/stock/scope corrections are assumptions',
        funding_recommendation=False,source_positive_gap_is_illicit=False,
        reference_uplift_status='source scenario partly anchored to same baseline; not independent evidence',
        spec=asdict(spec)))
    plots(out,frames,summary,gaps,base_uplift,base_shared,cfg['primary_alignment'],last_year,cfg['version'])
    (out/'FIGURE_CAPTIONS.md').write_text(f'''# Historical consumption bridge figures — {cfg['version']}

All figures are generated from the checked-in source table and declared configuration.
PNG and vector SVG versions are supplied. No panel contains newly observed current assays.

1. **Historical source alignment.** Annual-equivalent lawful releases are allocated uniformly
within calendar years to the declared primary alignment ({cfg['primary_alignment']}). Shading is the published count-bound
range after removing the fixed {base_uplift:g} uplift, not complete consumption uncertainty. The dashed
centre is reconstructed from bounds; it is not an originally reported point estimate.
2. **Observation-scale trajectory fit.** Posterior median and 95% latent intervals for the
survey-reported / matched-supply ratio. {future_years[0]}\u2013{future_years[-1]} are unobserved extrapolations, not measurements
or a current consumption-volume estimate. Shared reporting bias is not identified by this fit.
3. **Signed discrepancy.** Posterior mapping with median uplift {base_uplift:g} and one shared log-SD {base_shared:.2f}
multiplier per path. No inventory/visitor correction in this figure. Negative values remain.
This is not an illicit-market probability or a measured illegal volume.
4. **Accounting and reporting sensitivity.** {last_year} median and 95% conditional intervals under
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
    manifest=dict(version=cfg['version'],analysis_date=cfg['analysis_date'],quick=quick,
        primary_alignment=cfg['primary_alignment'],primary_centre=cfg['primary_centre'],
        source_uplift=base_uplift,base_shared_uplift_log_sd=base_shared,
        funding_recommendation=False,draws=n,seed=cfg['seed'],
        latest_paired_observation_year=last_year,
        commit=_git('rev-parse','HEAD'),command=' '.join(sys.argv),
        worktree_dirty=bool(_git('status','--porcelain')),
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
