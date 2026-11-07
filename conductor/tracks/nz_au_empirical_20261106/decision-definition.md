# Initial decision definition — version 1, 6 November 2026

Status: pre-fit analysis contract. No new fit or empirical input admission is authorised by
this document. Scope choices below are frozen for the first slice; the complete numeric
policy baseline and validation eligibility remain unverified. Amendments must precede
fitting and record their reason, affected estimands and whether outcomes were inspected.

## Decision and comparators

The NZ research-procurement decision is whether to add nicotine/tobacco wastewater
measurement to existing evidence: no additional study, a bounded pilot, or a wider
programme. Compare the same downstream policy action set and evidence cut-off under each
design; a study creates value only through an achievable change in decision or timing.
Do not force positive study value. Without costs, report break-even cost ceilings rather
than a funded recommendation. Without an identified policy response, report information
gain and decision limitations rather than equating precision with welfare.

The first policy contrast uses the existing retail/cessation representation against a
dated status quo. It is a conditional scenario until NZ effects, implementation and
substitution are justified. Excise, denicotinisation, cohort restrictions, enforcement,
product substitution and diffusion are later modules, each with a separate acceptance
case. Combining all published parameter lists is an appraisal task, not permission to
combine incompatible models or dependent estimates.

Australia is a country-specific programme and measurement comparator. Its observations
are not NZ observations and its policy changes are not a randomised NZ intervention.
Estimate transportability only after population, product, sampling and policy applicability
are assessed. Country-specific likelihoods and nuisance parameters remain separate.

## Scope and time

- Evidence cut-off and policy assessment date: 6 November 2026. Record publication,
  observation and legal commencement dates separately; later retrieval is a new edition.
- Empirical populations: NZ and AU residents with source-defined ages and coverage retained.
  The NZHS adult series cannot silently represent all ages. Catchment WBE denominators
  represent sampled contributing populations, including documented transient effects.
- Products: manufactured cigarettes, roll-your-own and other combustible tobacco, heated
  tobacco, vaping and NRT/other nicotine. Preserve lawful/illicit/unknown origin separately.
  Missing product attribution stays unknown; biomarkers do not establish legality.
- Initial empirical outputs: source-native periods plus annual summaries only when complete
  coverage supports aggregation. No interpolation converts missing periods to observations.
- Analyst-chosen decision horizon: two years for research acquisition/delay; five years for
  the first policy budget scenario. These are tractable planning horizons, not empirical
  parameters. Sensitivity: one/three-year research and ten-year policy horizons.
- Health expansion: lifetime cohort outcomes, with explicit disease latency, competing risks,
  terminal-age truncation checks and country-specific discounting guidance before use.
  Do not truncate QALYs at the five-year budget horizon.

## Perspectives and estimands

Report separately: health-system resource costs and QALYs; societal resource costs and
health; government fiscal revenue/expenditure; enforcement/justice resource use; consumer
spending/access; distributive outcomes. Keep taxes and fines as transfers in societal
accounts. Never sum perspective-specific net benefits into a combined total.

Primary empirical estimands are country/product/time-specific nicotine exposure and
combustible consumption compatible with observed scope, their uncertainty/identified
sets, held-out predictive error and incremental predictive information from WBE. Illicit
share is a secondary estimand only where product conversion, lawful unrecorded flows,
stock and origin attribution support identification. No conversion factor is invented.

Decision outputs are paired incremental outcomes, regret, EVPI, EVPPI, EVSI and ENBS for
the same action set, population, horizon and evidence. EVSI subtracts study costs only at
ENBS; do not sum overlapping information values. Report monetary/QALY thresholds as
explicit sensitivity axes until justified; no default threshold implies a national rule.
Account for delay, implementation and sampling costs when known. Report Monte Carlo
error and finite-oracle comparisons before interpreting small differences.

Equity strata follow available source definitions: Māori, Pacific and other NZ groupings,
age, sex, deprivation and geography; AU Indigenous status and other source-defined strata
are assessed independently. Disclose suppressed/small cells, denominators and uncertainty.
Do not infer ethnicity or individual behaviour from catchments. Specify equity weights and
their value judgement separately from unweighted health. HR-QoL requires instrument,
country tariff, age/condition, year and comorbidity rules; a modelled score is not a QALY.

## Policy baseline: verified context and outstanding fields

The [NZ Ministry smoked-tobacco page](https://www.health.govt.nz/regulation-legislation/smoked-tobacco)
reports repeal of the approved retailer scheme. The
[official repeal material](https://www.health.govt.nz/information-releases/cabinet-and-briefing-material-smokefree-2025-progressing-coalition-agreement-commitments-and)
identifies removal of denicotinisation, retailer reduction and generation restrictions.
Those measures must be coded as counterfactuals rather than current settings. The
7 November source check below verifies selected statutory fields, not the complete
operative policy baseline or causal effects.

The [AU Department reforms page](https://www.health.gov.au/give-up-for-good/reforms)
describes tobacco product changes applying from July 2025 and pharmacy-only vape supply,
with state/territory variation. Retain jurisdiction-specific implementation and enforcement.
It is a publisher summary last updated July 2025, not proof that no later amendment exists.

NZ statutory source check, 7 November 2026: the official principal Act's latest route
returns the consolidation as at 10 July 2026. The 2024 Amendment Act (2024 No 6)
received assent on 5 March; section 2 commences it the next day, 6 March 2024. The
current consolidation marks the approved smoked-tobacco retailer scheme (Part 1B,
subpart 1, including section 20M) and nicotine-limit section 57I as repealed on that
date. Section 40 retains the under-18 sales/delivery restriction. Removed retailer
maxima and that nicotine-limit provision therefore cannot be active status-quo
settings. This does not mean zero retail regulation or an observed outlet count.

Current section 20FA separately prohibits disposable vaping devices, with its insertion
dated 17 June 2025; it is not a blanket ban on all vaping. Annual-reporting requirements
are in section 100, not the legacy section 35 named by the Ministry returns page.
Exact source hashes/section IDs and qualified CLI readbacks are in
phase2-context-receipts-20261107.json and phase2-reconciliation-20261107.md.
The original 2022 generation-provision mapping, regulations, implementation and
compliance remain unqualified. The latest legal route was retrieved after the fixed
6 November cut-off; no live alert state or absence of later/prospective changes is
claimed. These selected statutory facts do not admit a complete numerical baseline.

Both baselines still require exact current excise schedules, indexation, retail rules,
product standards, vaping/NRT access, cessation coverage and enforcement practice, including
later legal changes. These are blocking missing inputs, not zero-valued settings.
The [ABS experimental nicotine estimates](https://www.abs.gov.au/articles/household-consumption-illicit-tobacco-and-nicotine-products)
reuse ACIC WBE: retain shared-source identity and alternative assumptions rather than
conditioning on both as independent observations. Programme methodology and figures await
page-level extraction verification and archive admission.

## Prespecified validation and stop rules

Before fitting, create a hash-bound observation manifest and exclude duplicate editions,
forecasts, derived posteriors and overlapping source representations from likelihoods.
Select the latest complete country-specific year as temporal holdout only if at least
three earlier complete years exist for that estimand; otherwise report temporal validation
unavailable. Never reduce that minimum in response to results. Within eligible WBE data,
leave one catchment out in each fold only with at least four comparable catchments and
adequate time coverage; freeze folds before model selection. Group all editions/products
sharing a measurement occasion together. Country transfer is an additional challenge set,
not a substitute for within-country validation.

Compare source-only/simpler baseline against WBE addition using held-out log predictive
score where a likelihood exists, interval coverage/width and unit-specific error. Report
all selected metrics and Monte Carlo standard errors; define decision-relevant numerical
tolerances in the fitting task before seeing outcomes. No arbitrary precision gain passes
scientific acceptance. Sensitivity varies calibration, product attribution, lawful flows,
dependence, policy effects, missingness and horizon. PSA preserves justified covariance.
Clustering later uses training simulations only; scaling, cluster selection and supervised
labels cannot inspect holdouts. Weak identification, unstable clusters or unavailable
validation yield bounded/no-use findings. They do not trigger fabricated priors or labels.
