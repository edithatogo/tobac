# Dynamic model and decision research design

## What the candidate does

`src/tobac_supply/dynamic.py` is a small independent numerical reference for
expected closed-cohort trajectories. It adds no dependency and does not replace
the accepted regulatory engine or historical longitudinal fits.

For cohort `g`, row-vector population `n[g,t]` evolves as
`n[g,t+1] = n[g,t] @ P[g,t]`. Each supplied transition matrix has origin rows,
destination columns and probabilities summing to one. Death is absorbing; a
person with prior use cannot return to never-use. Separate states for smoking,
vaping and dual use conserve people while allowing product substitution.

Product `p` consumption is
`C[g,t,p] = duration[t] * sum_s n[g,t,s] * rate[g,t,s,p]`.
Rates have explicit product units per person-year. Transitions take place at the
interval end and consumption uses opening occupancy. This is a declared discrete
time convention, not an exact continuous-time exposure calculation. Shorter
intervals require compatible transition probabilities; annual probabilities are
never silently reused as monthly probabilities. Compare discretisations before
policy use. Preserve separate products rather than adding sticks and liquid units.

All transition/rate arrays are supplied assumptions. Policy IDs and an assumption
ID identify scenarios, not estimated causal effects. Populations must be mutually
exclusive cohorts; the overlapping NZHS marginals cannot initialise these states
without a reviewed joint-state estimate. The prototype has no births, migration,
age transitions, NRT/pouch states, stochastic parameter uncertainty, risk memory,
health valuation or evidence-updating machinery. These are explicit next steps,
not latent capabilities inferred from a function name.

Analytic tests show, for example, that an assumed complete cessation transition
after year one versus year two changes cumulative smoked-product exposure while
the final state can be identical. The numbers are synthetic fixtures. A snapshot
model would miss this path-dependent difference.

## Mortality and person-time integration — 9 November 2026

The optional `project_health_cohorts` interface connects this reference to the
existing `tobac.health.exposure_health_step` kernel. It accepts explicitly supplied
annual cause-specific hazards for the five living states and a separate survivor
transition matrix. Each interval first integrates origin-state living person-time
and deaths, then moves survivors between exposure states at the boundary. Product
consumption is the origin-state rate multiplied by that living person-time. Rates
and hazards for a destination state begin in the next interval.

The survivor transition matrix cannot also send living people into death. The
interface rejects that case, avoiding two applications of mortality. Previously
dead people remain in the absorbing state. Hazards are constant within each
declared interval and mutually exclusive causes retain their explicit order.
The returned `HealthProjection` includes interval/cohort/state person-years and
interval/cohort/cause deaths alongside populations and product amounts.

An independent analytic fixture starts with 100 people and annual hazard
`log(2)`. One year produces 50 survivors and `50 / log(2)` living person-years;
consumption follows that exposure rather than 100 full person-years. Zero hazards
recover the original discrete reference when its matrices have no deaths.
This is a tested conditional timing contract. Tobacco hazards, disease memory,
causal transitions, utilities and prices still require their own evidence.

## Progression to an empirical state-space model

1. **Reference dynamics:** the supplied transition/rate schedules above. Preserve
   this small oracle while qualifying any richer implementation.
2. **Measurement and estimation:** latent product consumption, lawful stocks/flows
   and catchment populations evolve through time. Surveys, wastewater and supply
   are noisy observations with their own dates, scope, calibration and dependence.
   A forecast or posterior is never a new independent observation. Retain joint
   draw/state IDs and once-only conditioning of each underlying dataset.
3. **Policy response and health:** introduce reviewed effects on initiation,
   cessation, relapse, intensity and switching, plus implementation/adoption.
   Age, cumulative exposure and time-since-cessation may require extra state or a
   semi-Markov model. Add competing mortality, disease lags and fiscal/resource
   outcomes only with stated conversions and uncertainty.
4. **Adaptive decisions:** policy at time `t` depends only on information available
   then. The objective values the whole remaining trajectory, including study
   delays, learning, uptake and reversibility. Prevent future-data leakage and use
   identical horizons for act-now and learn-then-act comparisons.

Conceptually, `x[t+1] = F(x[t], action[t], response[t], theta) + process_error[t]`
and `y[t] = H(x[t], calibration[t]) + measurement_error[t]`. These equations specify
future design; the current prototype implements only a deterministic cohort part.
Whether filtering, particle methods, hierarchical Bayes or a partially identified
set is appropriate depends on the observation contract and identifiability.

## Broader decisions the model could inform

| Decision | Outcomes to compare | Additional evidence needed |
| --- | --- | --- |
| Excise levels, price floors and tax timing | Total exposure, substitution, affordability, revenue, distributional burden | Price elasticities by product/cohort, pass-through, lawful/unlawful substitution and supply responses |
| Retail density, location, licensing and access | Initiation, cessation, travel/access costs, spatial inequality | Geographic access, implementation, displacement and transportable causal effects |
| Nicotine content, product standards, age/cohort restrictions | Initiation, dependence, consumption intensity, switching and long-run harms | Product-specific behaviour and risk, enforcement, cohort uptake and compensatory use |
| Smoking/vaping/NRT policy combinations | Smoking cessation, dual use, relapse, youth initiation, product-specific health | Joint transitions and intensities; cessation and harm estimates; duration and co-interventions |
| Cessation-service commissioning | Quit attempts and sustained quits, capacity, cost, access, opportunity cost | Service uptake/adherence, incremental effects, relapse, delivery costs and resource constraints |
| Enforcement and illicit-supply disruption | Total harm, source substitution, implementation costs and displacement | Detection processes, supply response and separately valued harms; seizures alone do not identify market size |
| Timing, sequencing, pilots and stopping rules | Cumulative outcomes, reversible costs, delay losses and learning | Time-specific effects, adoption, credible study performance, resource limits and decision triggers |
| Targeted versus universal policy | Population outcomes and distribution across geography, deprivation and age | Mutually exclusive denominators, heterogeneous effects, governance and explicit equity objectives |
| Surveillance and research portfolios | Expected decision improvement per cost, information timing and coverage | Measurement performance, dependence, study costs, recruitment, reporting delays and feasibility |
| Health/fiscal budgeting and disinvestment | QALYs, healthcare costs, tax revenue, household spending and other valued effects | Validated disease/cost pathways, discounting, perspectives, price year and opportunity-cost thresholds |

Ethnicity can describe aggregate inequities where appropriate and governed; it
cannot be inferred from wastewater or used as a proxy for individual criminality.
Fiscal revenue, household transfers, healthcare resources and welfare are kept
separate until a declared perspective specifies how to value them.

## What would justify a claim beyond the current frontier?

Treat these as research hypotheses, not established novelties:

- **Decision value under uncertain measurement and partial identification.** Can
  adaptive surveillance/policy improve robust decisions when product attribution
  and calibration drift remain weakly identified? Compare an identified model,
  uncertainty sets and explicitly prior-sensitive alternatives.
- **Joint policy and learning.** A policy changes both behaviour and which data
  become informative. Test whether accounting for that feedback improves decisions
  over conventional fixed study designs and static staged EVSI.
- **Equity and heterogeneity in learning.** Does targeted evidence reduce decision
  error for underserved groups while satisfying explicit equity constraints, and
  at what cost to other objectives? Report the trade-off rather than hide it in
  one unexamined aggregate utility.
- **Factual versus normative disagreement.** Separate value of new observations
  from value of resolving preferences/perspectives. Do not update a social value
  judgement as if it were a random biomedical parameter without justification.
- **Strategic adaptation.** Test whether plausible legal/illicit supply responses
  overturn a decision. A game model earns inclusion only by improving a decision
  or revealing a material robustness limit relative to an exogenous-response model.

A frontier claim needs a systematic methods review and external empirical or
benchmark evidence. State-space nicotine modelling, wastewater VOI and sequential
research decisions already exist. Relevant starting comparators include the
[ABS experimental model](https://www.abs.gov.au/articles/household-consumption-illicit-tobacco-and-nicotine-products),
[Impalli et al. wastewater VOI](https://doi.org/10.1371/journal.pcbi.1013190), and
[Dymock et al. sequential research decision work](https://pubmed.ncbi.nlm.nih.gov/41826246/).
The value lies in demonstrably better calibrated and more useful decisions, not
in claiming that combining familiar methods is automatically novel.

## Comparative validation and stopping rules

Freeze a benchmark before selecting the most complex model. Compare:

1. Naive matched consumption-minus-lawful-release arithmetic, with stated limits.
2. Published biomarker conversion and ABS-style state-space allocation baselines.
3. Current tobac finite decision/VOI oracle and historical longitudinal baseline.
4. The new cohort reference, then each added observation/health/adaptation layer.

Use simulated ground truth for mass balance, state recovery, censoring, duplicate
sources, mismatched populations and calibration drift. For Bayesian estimation,
add simulation-based calibration and posterior predictive checks; for partial
identification, test set coverage and bound sharpness against independent cases.
Hold out later periods and catchments, retaining temporal ordering and avoiding
leakage from pooled national estimates into nominally held-out local outcomes.

Evaluate interval coverage and proper predictive scores alongside action ranking,
expected regret, robust regret, implementation costs and subgroup outcomes. A new
layer must improve prespecified performance or reveal a material decision risk;
otherwise keep the simpler model. Include ablations, alternative priors, transport
attenuation, null effects, shared-source covariance and missingness stress tests.
Set numerical acceptance tolerances from analytic fixtures and substantive decision
thresholds before looking at comparative outputs. Do not set thresholds to pass a
preferred model. The current three-year historical holdout is insufficient by
itself to demonstrate general dynamic policy validity.

## Provider boundaries

Tobac owns tobacco-specific states, measurements, evidence identities and estimands.
Use Searchright for review/search lifecycle; Sourceright for citation integrity;
optional CiteWeft for document evidence. Reuse Voiage for qualified generic value
of information/perspective methods, Innovate for justified adoption/response
components, Kairos for qualified time/resource orchestration, and Paignia only for
a demonstrated strategic interaction. The existing TP01–TP05 promotion plan in
the roadmap controls migration. No dependency, copied general solver, upstream
readiness claim or automatic cutover is introduced by this candidate.

### Upstream maintained-dependency capabilities warranted by BF1–BF6

Where a frontier requirement is mathematically general rather than tobacco-specific,
implement and qualify the reusable mechanism in its authoritative upstream repository
first (`TP01–TP05`), keeping a small independent reference oracle in `tobac`:

1. **`edithatogo/voiage` (Credal LP dominance, Farkas witnesses, MIR & endogenous/censored VOI):**
   - Polyhedral/credal-set decision sufficiency: primal attaining witnesses $(\theta_{\min}, \theta_{\max})$, dual Farkas certificates identifying binding constraints, and Minimal Identifying Restriction (MIR) computation.
   - Set-valued (upper/lower) EVSI over credal sets and left-censored (Tobit/LOD) observation channels without censored-cell imputation.
   - Action-dependent observation operators $y_t \sim H(x_t, a_t, \eta_t)$ where policy actions alter channel Fisher information or state identifiability, plus exported Hypothesis strategies for Blackwell garbling monotonicity.
2. **`edithatogo/kairos` (Three-clock non-anticipative orchestration):**
   - Separate physical-state, delayed-evidence-arrival and policy-decision clocks with structural non-anticipativity checks preventing future-data leakage in sequential/adaptive rules.
3. **`edithatogo/innovate` & `edithatogo/dapane` (Polars-native cohort memory & perspective microcosting):**
   - Retire legacy `pandas`/`pandasdmx` requirements in `innovate` in favour of Polars/Arrow interchange, and provide reusable semi-Markov tunnel-state / multi-component hazard-decay cohort primitives.
   - Qualify `dapane` consumer contracts for perspective-explicit microcosting and discount schedules that keep healthcare resource costs, delivery capacity and fiscal tax transfers distinct.
4. **`edithatogo/archive-govt-nz`, `searchright`, `sourceright` & `citeweft` (Two-tier Merkle lineage & living invalidation):**
   - Separate the **Runner Closure Merkle Root** (transitive Python AST/imports + declared runner inputs) from the **Candidate Evidence Registry Merkle Root** in `archive-govt-nz`, enabling fine-grained invalidation cones (`source -> extraction -> parameter -> bound -> decision`) without re-executing unaffected runners when staging candidate evidence.
   - Preserve CSL item kinds (`book`, `chapter`, `report`) across `searchright` CSV/CSL round-trips and emit signed retraction/erratum diff manifests across `sourceright`/`citeweft`.
5. **`edithatogo/repository-standards` & `edithatogo/paignia` (Process-group RSS guard & strategic perturbations):**
   - Scope macOS process-group RSS sampling in `repository-standards` / `run_bounded.py` to `ps -g <pgid> -o pgid=,rss=` so uninterruptible system-wide processes cannot stall pre-push or test monitors.
   - Export equilibrium-set inclusion and payoff-perturbation sensitivity certificates from `paignia` when BF6 strategic interaction is invoked.

## Parameter evidence update — 9 November 2026

This is a targeted, source-linked candidate catalogue: **61 numerical entries from
14 source/reuse identities**, including administrative rates, study estimates,
author assumptions, method settings and derived constraints. These are not 61
independent estimates. It supplements, rather than replaces, the existing
`Scope`/`EvidencePacket`/`SupplyBasis` admission and parameter-serialization contracts.
No runtime default, prior, likelihood, accepted output or frozen validation rule
changes. Issue #3 and PR #147 native qualification remain open.

### What can now be populated, and at what scope

| Gap | Supplied evidence | Remaining limitation |
| --- | --- | --- |
| Dated fiscal baseline | NZ excise from 1 January 2026; AU tariff items 5.1/5.5 from 1 September 2026 | Rates are not retail prices, pass-through or actual mass per cigarette; AU original-page readback remains open. |
| Cessation service effects | NZ trial arm counts and two reported six-month risk-difference intervals | Trial eligibility, uptake, attrition and shared controls must be retained; not a causal retailer-cap effect. |
| Product demand | Four historical NZ manufactured/RYO elasticities and two stated-demand cross-price estimates | Historical versus current markets and hypothetical versus realised purchasing differ; coefficient covariance is not extracted. |
| Dynamic constraints | Australian five-year quit/resumption endpoint counts | Endpoint status does not identify annual hazards or all intermediate transitions. |
| Health effects | Australian all-cause and cause-specific mortality HRs with reported 95% intervals | Requires matched baseline hazards, age/history and overlap handling; mortality HRs are not disease incidence. |
| Nicotine-standard response | Six observed trial-arm week-six cigarette-consumption means | Short-term free-product trial, without extracted mean uncertainty; no long-term population or harm equivalence. |
| Biomarker conversion | Preliminary human anabasine factor, explicit inherited dose assumptions and urine-method LOD/LOQ | Urine limits and assumed doses are not local wastewater calibration; source and transport uncertainty remain. |
| Costing and valuation | Three NZ patch pack prices; PHARMAC discount convention and sensitivity settings | Medicine acquisition is only one component; perspective, edition, GST/rebates and complete incremental resource costs need reconciliation. |
| Initial daily-use overlap | Reused NZHS smoking/vaping/union estimates and an exact four-category algebraic crosswalk | Does not split never/former/non-daily use or identify survey covariance. |

**Initial-state refinement.** With daily smoking S = 6.8%, daily vaping V = 11.7%
and their union U = 17.1%, the rounded-point partition is both daily = S+V-U =
1.4%, smoking-only daily = U-V = 5.4%, vaping-only daily = U-S = 10.3%, and neither
daily = 100-U = 82.9%. The catalogue gives marginal rounding envelopes assuming
rounding to the nearest 0.1 percentage point. These are not confidence intervals,
not independent draws, and not a six-state initial population. In particular,
"neither daily" includes former, never and non-daily users. This corrects an overly
broad claim that no overlap crosswalk is possible: the four daily-use categories
are algebraically constrained, while the richer state partition remains missing.

**Use sequence.** First reconcile study aliases with the existing Searchright
corpus and source receipts. Then complete result-specific appraisal, original
edition/capture checks, units/estimand transport and dependence handling. A lawful
rate or method convention can become a declared dated scenario input after its
own checks; that does not constitute observational likelihood admission. Trial
arm counts and contrasts are alternative representations of the same evidence.
The 45 and Up mortality publications also overlap. Never condition on all these
representations as independent observations.

**Evidence date.** The first-comparison cutoff remains 6 November 2026. Retrieval
on 9 November is not an observation date. The November HML edition needs a dated
capture before inclusion in that frozen comparison; it is available here as a
cost-component candidate, not silently backdated. Public-only acquisition remains
in force. No author contact, restricted-data request or new collection occurred.

### Portable catalogue

The JSON block below is the authoritative candidate packet within this companion.
It is kept alongside its interpretation; it is not an executable configuration.
`columns` defines each record's ordered fields. Null interval values are unknown
or inapplicable, not zero uncertainty. `kind` and `uncertainty` distinguish measured
estimates, conventions, source assumptions and arithmetic derivatives. Source IDs
are catalogue aliases: reconcile existing identities before any admission.

Canonical exported JSON uses UTF-8, `ensure_ascii=False`, two-space indentation
and one final newline. SHA-256:
`778777b6a8b703f9764605958d1ac321e0d396f7e5076b9747111d7b9f4ac9bd`.
Local checks passed 104 assertions, including six deliberate invalid-packet
rejections, count/interval/unit checks, source/dependence links and all eight
rounding-box vertices. These are catalogue checks, not the repository test suite,
native acceptance or empirical policy validation.

<details>
<summary>Machine-readable parameter candidates, sources and unresolved gaps</summary>

<!-- TOBAC_PARAMETER_CANDIDATES_V1 -->
```json
{
  "schema": "tobac.candidate-parameter-catalogue.v1",
  "edition": "2026-11-09",
  "base_commit": "e0e5609c77138a32c2f77f14fa8caa687a79cb4b",
  "frozen_first_comparison_cutoff": "2026-11-06",
  "purpose": "Source-linked candidate numbers and constraints; auxiliary catalogue, not a new EvidencePacket or runtime parameter contract.",
  "empirical_admission": false,
  "active_model_parameters_changed": false,
  "archival_status": "Source pages/records read through connectors; no original-byte capture, new archive digest or native acceptance claimed by this packet.",
  "rights": "Attributed numerical facts and original summaries only; no article prose, full texts or third-party graphics redistributed.",
  "uncertainty_policy": "Null bounds mean not extracted or inapplicable, never zero uncertainty. No distributions automatically fitted; no independence inferred from different publications.",
  "sources": {
    "NZ_CUSTOMS_2026": {"title": "New excise duty rates for tobacco products from 1 January 2026", "url": "https://www.customs.govt.nz/about-us/news/important-notices-archive/important-notices-archive-2025/new-excise-duty-rates-for-tobacco-products-from-1-january-2026", "edition": "page updated 2025-11-28; effective 2026-01-01", "review": "official HTML rate table", "population": "NZ taxable releases/imports; product classifications in source", "dependence_group": "NZ_excise_schedule_2026", "allowed_use": "Dated fiscal input for the stated product and unit, excluding GST; not retail price or pass-through.", "limits": "The 0.8 kg/1000 classification threshold is not measured tobacco mass per cigarette. Future indexation and policy end dates are not supplied."},
    "AU_EXCISE_202609": {"title": "Notice of substituted rates of excise duty No. 4 (2026), C2026G00551", "url": "https://www.legislation.gov.au/C2026G00551/asmade/2026-09-01/text/original/epub/OEBPS/document_1/document_1.html", "edition": "effective 2026-09-01", "review": "official register search-index table; direct page fetch failed", "population": "Australia; domestic excise tariff items 5.1 and 5.5", "dependence_group": "AU_excise_schedule_202609", "allowed_use": "Dated statutory-rate candidate; retain tariff-item applicability.", "limits": "Original-page archival readback remains open. The rate ratio is not a measured physical tobacco conversion. Not retail prices or future excise assumptions."},
    "PHARMAC_NRT_202611": {"title": "Hospital Medicines List: nicotine", "url": "https://schedule.pharmac.govt.nz/HMLOnline.php?osq=Nicotine", "edition": "November 2026 HML; accessed 2026-11-09", "review": "official indexed HML entries with pack quantity and pharmacode", "population": "NZ listed hospital medicine acquisition prices; Habitrol 24-hour patches", "dependence_group": "PHARMAC_NRT_price_edition_202611", "allowed_use": "Medicine component of a dated costing scenario only.", "limits": "Not complete treatment or programme cost; no dispensing, counselling, wastage, uptake or confidential rebate inference. Exact historical availability at the frozen 2026-11-06 cutoff and original edition capture require verification."},
    "PHARMAC_PFPA_DISCOUNT": {"title": "Prescription for Pharmacoeconomic Analysis, section 8: Discounting", "url": "https://www.pharmac.govt.nz/medicine-funding-and-supply/the-funding-process/policies-manuals-and-processes/economic-analysis/prescription-for-pharmacoeconomic-analysis-methods-for-cost-utility-analysis/8-discounting", "edition": "official guidance accessed 2026-11-09", "review": "key recommendations and rationale", "population": "PHARMAC cost-utility analysis perspective", "dependence_group": "PHARMAC_method_conventions", "allowed_use": "Declared annual discount convention for both costs and benefits, with separate sensitivity cases.", "limits": "Normative method choice, not an estimated population preference; not automatically transferable to every societal analysis or budget-impact calculation."},
    "TAIT_2015": {"title": "Do consumers of manufactured cigarettes respond differently to price changes compared with their Roll-Your-Own counterparts? Evidence from New Zealand.", "url": "https://pubmed.ncbi.nlm.nih.gov/24259046/", "doi": "10.1136/tobaccocontrol-2013-051010", "edition": "2015; quarterly data 1991-2011", "review": "primary-study PubMed abstract", "population": "NZ aggregate manufactured-cigarette and RYO demand", "dependence_group": "Tait_NZ_SUR_1991_2011", "allowed_use": "Historical product-specific elasticity sensitivity or a calibration comparator.", "limits": "No SE, CI or coefficient covariance extracted. One joint econometric model, not four independent studies. Not contemporary vaping/illicit-market elasticities or cessation probabilities."},
    "GRACE_2015_EC": {"title": "Estimating cross-price elasticity of e-cigarettes using a simulated demand procedure.", "url": "https://pubmed.ncbi.nlm.nih.gov/25548256/", "doi": "10.1093/ntr/ntu268", "edition": "2015", "review": "primary-study PubMed abstract", "population": "210 NZ smokers; hypothetical purchase task after sampling an e-cigarette", "dependence_group": "Grace_simulated_demand_210", "allowed_use": "Experimental stated-demand sensitivity only.", "limits": "Not observed market substitution; older products, no uncertainty estimate extracted; not a policy-effect prior."},
    "TUCKER_2018_VLNC": {"title": "Estimating Demand and Cross-Price Elasticity for Very Low Nicotine Content (VLNC) Cigarettes Using a Simulated Demand Task.", "url": "https://pubmed.ncbi.nlm.nih.gov/28340034/", "doi": "10.1093/ntr/ntx051", "edition": "2018", "review": "primary-study PubMed abstract", "population": "40 NZ smokers; simulated cigarette purchase tasks", "dependence_group": "Tucker_simulated_demand_40", "allowed_use": "Experimental stated-demand sensitivity only.", "limits": "Not realised market demand, adherence or a long-term harm effect; no uncertainty estimate extracted."},
    "WALKER_2020": {"title": "Nicotine patches used in combination with e-cigarettes (with and without nicotine) for smoking cessation: a pragmatic, randomised trial.", "url": "https://pubmed.ncbi.nlm.nih.gov/31515173/", "doi": "10.1016/S2213-2600(19)30269-3", "edition": "2020; recruitment 2016-03-17 to 2017-11-30", "review": "primary results abstract; linked protocol PMID30808668 checked", "population": "NZ adults motivated to quit, e-cigarette naive; 6-month CO-verified continuous abstinence, intention-to-treat", "dependence_group": "Walker_NCT02521662_shared_trial", "allowed_use": "Source-population cessation-service comparison or a transported-effect candidate after explicit appraisal.", "limits": "Not general-population reach, annual quit/relapse rates or a retailer-cap effect. Shared-arm contrasts must not be independently conditioned with their arm counts. Differential loss to follow-up. Abstract versus protocol e-liquid units differ; no liquid-strength parameter is extracted."},
    "TIAN_2017": {"title": "Partnering and parenting transitions associate with changing smoking status: a cohort study in young Australians.", "url": "https://pubmed.ncbi.nlm.nih.gov/28536842/", "doi": "10.1007/s00038-017-0984-3", "edition": "2017; baseline 2004-2006, follow-up approximately five years later", "review": "primary-study PubMed abstract", "population": "1084 Australian smokers/former smokers, age 26-36 at baseline", "dependence_group": "Tian_young_Australian_cohort", "allowed_use": "Five-year endpoint-status constraints for an external dynamic-model comparison.", "limits": "Unobserved intermediate quits/relapses possible. Do not annualise by a probability root or treat as continuously abstinent, current national or six-state transition estimates."},
    "BANKS_2015": {"title": "Tobacco smoking and all-cause mortality in a large Australian cohort study: findings from a mature epidemic with current low smoking prevalence.", "url": "https://pubmed.ncbi.nlm.nih.gov/25857449/", "doi": "10.1186/s12916-015-0281-z", "edition": "2015; enrolment 2006-2009, mortality to mid-2012", "review": "primary-study PubMed abstract", "population": "204953 NSW 45 and Up participants age >=45, with stated baseline disease exclusions; current versus never smoking", "dependence_group": "AU_45_and_Up_overlapping_cohorts", "allowed_use": "Adjusted relative-hazard comparator, conditional on matching baseline hazards and population.", "limits": "Cox HRs are described as RRs in source. Not absolute annual mortality or incidence. Sex-specific and overall estimates overlap. Overlaps Joshy 2025: do not add all-cause and cause-specific mortality or treat as independent cohorts."},
    "JOSHY_2025": {"title": "Relationship of tobacco smoking to cause-specific mortality: contemporary estimates from Australia.", "url": "https://pubmed.ncbi.nlm.nih.gov/39994694/", "doi": "10.1186/s12916-025-03883-9", "edition": "2025-02-25; recruitment 2005-2009, cause-specific outcomes to 2017-11-30", "review": "primary abstract and full-text methods excerpt, first 12000 body characters; not complete supplement review", "population": "178169 cancer/CVD-free 45 and Up participants age >=45; respiratory analyses additionally exclude prior respiratory hospitalisation", "dependence_group": "AU_45_and_Up_overlapping_cohorts", "allowed_use": "Outcome-specific mortality hazard multipliers after baseline/age/history reconciliation.", "limits": "Not disease incidence or exposure-specific baseline hazards. Overall lung cancer and intensity subgroup overlap. Do not multiply mixed-population life-table hazards directly by these HRs or pool with Banks as independent evidence."},
    "DONNY_2015": {"title": "Randomized Trial of Reduced-Nicotine Standards for Cigarettes.", "url": "https://pubmed.ncbi.nlm.nih.gov/26422724/", "doi": "10.1056/NEJMsa1502403", "edition": "2015; 10 US sites, 2013-2014 recruitment, six-week intervention", "review": "primary-study PubMed abstract", "population": "840 randomised adults, >=5 cigarettes/day, not currently interested in quitting; free study cigarettes", "dependence_group": "Donny_NCT01681875_shared_trial", "allowed_use": "Six-week dose/behaviour benchmark; arm identity preserved.", "limits": "Means lack uncertainty in the extracted abstract. Not population implementation, long-run cessation, policy adherence or proportional nicotine-to-disease-risk effects. Nicotine content is per gram of tobacco, not per cigarette."},
    "WENG_2026": {"title": "Exploring anabasine excretion factor in individuals who use tobacco cigarettes: a preliminary estimate.", "url": "https://pubmed.ncbi.nlm.nih.gov/41725392/", "doi": "10.1093/ntr/ntag042", "edition": "2026; Brisbane data March-August 2022", "review": "primary abstract and full-text methods excerpt, first 12000 body characters; reuses existing first-comparison review identity", "population": "72 participants; 22 cigarette users, 20 vape users, 30 nonusers; excretion-factor calculation uses 19 cigarette users", "dependence_group": "Weng2026_human_yield_shared_assumptions", "allowed_use": "Preliminary human-yield sensitivity; source-method assay controls and inherited conversion assumptions separately labelled.", "limits": "Urine after deconjugation is not NZ wastewater. LOD/LOQ values are method-specific, not catchment censoring limits. Assumed absorbed doses and reference excretion are not new measurements. No SE or target calibration distribution inferred; does not imply anabasine-free vaping."},
    "NZHS_2024_25_REUSE": {"title": "Existing verified NZHS 2024/25 national daily-use estimates", "url": "https://github.com/edithatogo/tobac/blob/e0e5609c77138a32c2f77f14fa8caa687a79cb4b/evidence/public_data_20261108/README.md", "edition": "NZHS 2024/25; previously verified official export", "review": "existing committed national smoking, vaping and union rows; no new survey", "population": "NZ national adults age >=15; daily-use indicators", "dependence_group": "NZHS_2024_25_shared_survey", "allowed_use": "Rounded-point four-category daily-use crosswalk only; reuse existing source identity.", "limits": "Neither daily smoking nor daily vaping is NOT never use or former use and includes non-daily users. Joint covariance and six-state initialisation remain unresolved. Rounding envelopes are not confidence intervals or independently observed estimates."}
  },
  "columns": ["id", "value", "unit", "source_id", "kind", "uncertainty", "lower", "upper", "numerator", "denominator", "locator_or_definition"],
  "records": [
    ["nz_excise_fmc_light", 1309.71, "NZD/1000_cigarettes", "NZ_CUSTOMS_2026", "administrative", "not_sampling_uncertainty", null, null, null, null, "Table: manufactured cigarettes <=0.8 kg tobacco per 1000; excludes GST"],
    ["nz_excise_fmc_heavy", 1866.34, "NZD/kg_tobacco", "NZ_CUSTOMS_2026", "administrative", "not_sampling_uncertainty", null, null, null, null, "Table: manufactured cigarettes >0.8 kg tobacco per 1000; excludes GST"],
    ["nz_excise_ryo", 1866.34, "NZD/kg_tobacco", "NZ_CUSTOMS_2026", "administrative", "not_sampling_uncertainty", null, null, null, null, "Table: other smoking tobacco; excludes GST"],
    ["nz_excise_htp_reconstituted", 933.16, "NZD/kg_tobacco", "NZ_CUSTOMS_2026", "administrative", "not_sampling_uncertainty", null, null, null, null, "Table: tobacco heating systems, reconstituted tobacco"],
    ["nz_excise_htp_other", 818.53, "NZD/kg_tobacco", "NZ_CUSTOMS_2026", "administrative", "not_sampling_uncertainty", null, null, null, null, "Table: tobacco heating systems, other than reconstituted tobacco"],
    ["au_excise_item_5_1", 1.55274, "AUD/stick", "AU_EXCISE_202609", "administrative", "not_sampling_uncertainty", null, null, null, null, "Notice table item 5.1"],
    ["au_excise_item_5_5", 2587.9, "AUD/kg_tobacco", "AU_EXCISE_202609", "administrative", "not_sampling_uncertainty", null, null, null, null, "Notice table item 5.5"],
    ["nz_nrt_patch_7mg_pack28", 19.62, "NZD/28_patches", "PHARMAC_NRT_202611", "administrative", "not_sampling_uncertainty", null, null, null, null, "Habitrol 7 mg/24 hours; pharmacode 2381389; HML list price"],
    ["nz_nrt_patch_14mg_pack28", 21.57, "NZD/28_patches", "PHARMAC_NRT_202611", "administrative", "not_sampling_uncertainty", null, null, null, null, "Habitrol 14 mg/24 hours; pharmacode 2381397; HML list price"],
    ["nz_nrt_patch_21mg_pack28", 24.72, "NZD/28_patches", "PHARMAC_NRT_202611", "administrative", "not_sampling_uncertainty", null, null, null, null, "Habitrol 21 mg/24 hours; pharmacode 2381400; HML list price"],
    ["nz_cua_discount_base", 0.035, "annual_fraction", "PHARMAC_PFPA_DISCOUNT", "method_convention", "scenario_not_distribution", null, null, null, null, "Section 8: both costs and benefits; base or specified sensitivity case"],
    ["nz_cua_discount_low", 0.0, "annual_fraction", "PHARMAC_PFPA_DISCOUNT", "method_convention", "scenario_not_distribution", null, null, null, null, "Section 8: both costs and benefits; base or specified sensitivity case"],
    ["nz_cua_discount_high", 0.05, "annual_fraction", "PHARMAC_PFPA_DISCOUNT", "method_convention", "scenario_not_distribution", null, null, null, null, "Section 8: both costs and benefits; base or specified sensitivity case"],
    ["nz_mc_own_price_elasticity", -1.033, "elasticity", "TAIT_2015", "empirical", "not_extracted", null, null, null, null, "MC demand with respect to MC price"],
    ["nz_ryo_own_price_elasticity", -0.441, "elasticity", "TAIT_2015", "empirical", "not_extracted", null, null, null, null, "RYO demand with respect to RYO price"],
    ["nz_ryo_mc_cross_price_elasticity", 0.867, "elasticity", "TAIT_2015", "empirical", "not_extracted", null, null, null, null, "RYO demand with respect to MC price"],
    ["nz_ryo_income_elasticity", -0.8, "elasticity", "TAIT_2015", "empirical", "not_extracted", null, null, null, null, "RYO demand with respect to average weekly income; rounded abstract value"],
    ["nz_ec_stated_cross_price", 0.16, "elasticity", "GRACE_2015_EC", "empirical", "not_extracted", null, null, null, null, "E-cigarette stated demand with respect to cigarette price; N=210"],
    ["nz_vlnc_stated_cross_price", 0.32, "elasticity", "TUCKER_2018_VLNC", "empirical", "not_extracted", null, null, null, null, "VLNC stated demand with respect to regular cigarette price; N=40"],
    ["nz_patch_nicotine_ec_quit6m", 0.07, "probability_6_month_endpoint", "WALKER_2020", "derived_from_counts", "counts_available_no_ci_assigned", null, null, 35, 500, "Patch plus nicotine e-cigarette; CO-verified continuous abstinence, ITT"],
    ["nz_patch_nonnic_ec_quit6m", 0.04008016032064128, "probability_6_month_endpoint", "WALKER_2020", "derived_from_counts", "counts_available_no_ci_assigned", null, null, 20, 499, "Patch plus nicotine-free e-cigarette; CO-verified continuous abstinence, ITT"],
    ["nz_patch_only_quit6m", 0.024, "probability_6_month_endpoint", "WALKER_2020", "derived_from_counts", "counts_available_no_ci_assigned", null, null, 3, 125, "Patch only; CO-verified continuous abstinence, ITT"],
    ["nz_ec_vs_nonnic_rd6m", 0.0299, "risk_difference", "WALKER_2020", "empirical", "reported_two_sided_95CI", 0.0017, 0.0581, null, null, "Nicotine EC+patch versus non-nicotine EC+patch; percentage-point values divided by 100"],
    ["nz_ec_vs_patch_rd6m", 0.046, "risk_difference", "WALKER_2020", "empirical", "reported_two_sided_95CI", 0.0111, 0.0809, null, null, "Nicotine EC+patch versus patch; shared treatment arm"],
    ["au_smoker_to_quit_status5y", 0.4087719298245614, "probability_5_year_endpoint", "TIAN_2017", "derived_from_counts", "counts_available_no_ci_assigned", null, null, 233, 570, "No longer smoking at follow-up among baseline smokers"],
    ["au_former_to_smoking_status5y", 0.11284046692607004, "probability_5_year_endpoint", "TIAN_2017", "derived_from_counts", "counts_available_no_ci_assigned", null, null, 58, 514, "Smoking at follow-up among baseline former smokers"],
    ["au_allcause_current_hr", 2.96, "hazard_ratio", "BANKS_2015", "empirical", "reported_two_sided_95CI", 2.69, 3.25, null, null, "Both sexes; current versus never; adjusted Cox HR described as RR"],
    ["au_allcause_current_men_hr", 2.82, "hazard_ratio", "BANKS_2015", "empirical", "reported_two_sided_95CI", 2.49, 3.19, null, null, "Men; current versus never; adjusted Cox HR described as RR"],
    ["au_allcause_current_women_hr", 3.08, "hazard_ratio", "BANKS_2015", "empirical", "reported_two_sided_95CI", 2.63, 3.6, null, null, "Women; current versus never; adjusted Cox HR described as RR"],
    ["au_chronic_lung_death_current_hr", 36.32, "hazard_ratio", "JOSHY_2025", "empirical", "reported_two_sided_95CI", 26.18, 50.4, null, null, "Chronic lung disease mortality versus never smoking; abstract results"],
    ["au_lung_cancer_death_current_hr", 17.85, "hazard_ratio", "JOSHY_2025", "empirical", "reported_two_sided_95CI", 14.38, 22.17, null, null, "Lung cancer mortality versus never smoking; abstract results"],
    ["au_oropharynx_death_current_hr", 7.86, "hazard_ratio", "JOSHY_2025", "empirical", "reported_two_sided_95CI", 4.11, 15.02, null, null, "Oro-pharyngeal cancer mortality versus never smoking; abstract results"],
    ["au_lung_cancer_death_lowintensity_hr", 13.0, "hazard_ratio", "JOSHY_2025", "empirical", "reported_two_sided_95CI", 9.5, 17.8, null, null, "Lung cancer mortality, 1-14 cigarettes/day versus never smoking; abstract results"],
    ["us_vlnc_cpd_week6_usual", 22.2, "cigarettes/person/day", "DONNY_2015", "empirical", "not_extracted", null, null, null, null, "Usual brand; week 6 mean"],
    ["us_vlnc_cpd_week6_15_8", 21.3, "cigarettes/person/day", "DONNY_2015", "empirical", "not_extracted", null, null, null, null, "15.8 mg nicotine/g tobacco; week 6 mean"],
    ["us_vlnc_cpd_week6_5_2", 20.8, "cigarettes/person/day", "DONNY_2015", "empirical", "not_extracted", null, null, null, null, "5.2 mg nicotine/g tobacco; week 6 mean"],
    ["us_vlnc_cpd_week6_2_4", 16.5, "cigarettes/person/day", "DONNY_2015", "empirical", "not_extracted", null, null, null, null, "2.4 mg nicotine/g tobacco; week 6 mean"],
    ["us_vlnc_cpd_week6_1_3", 16.3, "cigarettes/person/day", "DONNY_2015", "empirical", "not_extracted", null, null, null, null, "1.3 mg nicotine/g tobacco; week 6 mean"],
    ["us_vlnc_cpd_week6_0_4", 14.9, "cigarettes/person/day", "DONNY_2015", "empirical", "not_extracted", null, null, null, null, "0.4 mg nicotine/g tobacco; week 6 mean"],
    ["anabasine_excretion_fraction_weng", 0.0902, "fraction_absorbed_dose", "WENG_2026", "empirical", "not_extracted", null, null, null, null, "Abstract/results; factor calculated for 19 of 22 cigarette users"],
    ["weng_absorbed_nicotine_assumption", 0.9, "mg/cigarette", "WENG_2026", "source_assumption", "not_extracted", null, null, null, null, "Methods: inherited assumed absorbed nicotine, not measured cigarette content"],
    ["weng_absorbed_anabasine_assumption", 0.0072, "mg/cigarette", "WENG_2026", "source_assumption", "not_extracted", null, null, null, null, "Methods: inherited assumed absorbed anabasine"],
    ["weng_cot_3hc_reference_fraction", 0.7212, "fraction", "WENG_2026", "source_assumption", "not_extracted", null, null, null, null, "Methods: inherited COT+3HC excretion comparator; not a new independent estimate"],
    ["weng_urine_lod_anabasine", 0.1, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOD, not NZ wastewater limit"],
    ["weng_urine_loq_anabasine", 0.2, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOQ, not NZ wastewater limit"],
    ["weng_urine_lod_anatabine", 0.05, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOD, not NZ wastewater limit"],
    ["weng_urine_loq_anatabine", 0.15, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOQ, not NZ wastewater limit"],
    ["weng_urine_lod_nicotine", 0.1, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOD, not NZ wastewater limit"],
    ["weng_urine_loq_nicotine", 0.2, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOQ, not NZ wastewater limit"],
    ["weng_urine_lod_cotinine", 0.01, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOD, not NZ wastewater limit"],
    ["weng_urine_loq_cotinine", 0.02, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOQ, not NZ wastewater limit"],
    ["weng_urine_lod_3hc", 0.02, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOD, not NZ wastewater limit"],
    ["weng_urine_loq_3hc", 0.05, "ug/L_urine_method", "WENG_2026", "assay_method", "not_population_uncertainty", null, null, null, null, "Urine sample handling and analysis: method LOQ, not NZ wastewater limit"],
    ["weng_conditional_anabasine_yield", 0.64944, "ug/cigarette", "WENG_2026", "derived_from_assumptions", "not_extracted", null, null, null, null, "0.0902 * 0.0072 * 1000; links factor and assumed absorbed dose; not another measurement"],
    ["nzhs_daily_smoking", 6.8, "percent", "NZHS_2024_25_REUSE", "existing_observation_reuse", "use_existing_marginal_intervals", null, null, null, null, "Existing national daily smoking"],
    ["nzhs_daily_vaping", 11.7, "percent", "NZHS_2024_25_REUSE", "existing_observation_reuse", "use_existing_marginal_intervals", null, null, null, null, "Existing national daily vaping"],
    ["nzhs_daily_union", 17.1, "percent", "NZHS_2024_25_REUSE", "existing_observation_reuse", "use_existing_marginal_intervals", null, null, null, null, "Existing daily smoking OR daily vaping OR both"],
    ["nzhs_both_daily_point", 1.4, "percent", "NZHS_2024_25_REUSE", "derived_from_rounded_marginals", "rounding_envelope_not_CI", 1.25, 1.55, null, null, "S+V-U; assumes each published percentage rounded to nearest 0.1 pp; envelopes are marginal extrema, not independent draws"],
    ["nzhs_smoking_only_daily_point", 5.4, "percent", "NZHS_2024_25_REUSE", "derived_from_rounded_marginals", "rounding_envelope_not_CI", 5.3, 5.5, null, null, "U-V; assumes each published percentage rounded to nearest 0.1 pp; envelopes are marginal extrema, not independent draws"],
    ["nzhs_vaping_only_daily_point", 10.3, "percent", "NZHS_2024_25_REUSE", "derived_from_rounded_marginals", "rounding_envelope_not_CI", 10.2, 10.4, null, null, "U-S; assumes each published percentage rounded to nearest 0.1 pp; envelopes are marginal extrema, not independent draws"],
    ["nzhs_neither_daily_point", 82.9, "percent", "NZHS_2024_25_REUSE", "derived_from_rounded_marginals", "rounding_envelope_not_CI", 82.85, 82.95, null, null, "100-U; assumes each published percentage rounded to nearest 0.1 pp; envelopes are marginal extrema, not independent draws"]
  ],
  "unresolved": [
    {"id": "NZ_TARGET_WASTEWATER", "status": "unresolved", "required": "Dated catchment population/flow, effective censoring after processing, sewer loss, product contribution, covariance and matched consumption; urine LODs do not fill these."},
    {"id": "NZ_RETAIL_CAUSAL", "status": "unresolved", "required": "Causal sustained quit, switching/diversion, intensity, implementation and mitigation effects for the declared 600-retailer contrast; trial quit rates are not cap effects."},
    {"id": "STATE_TRANSITIONS", "status": "partial_external_constraints", "required": "Joint six-state baseline, initiation/dual-use/relapse by age and time since quit, non-daily use, migration; five-year endpoints alone do not identify transition hazards."},
    {"id": "DEMAND_TRANSPORT", "status": "historical_candidates_only", "required": "Contemporary own/cross-price matrix, pass-through, illicit substitution and income response covariance; assess historical structural drift."},
    {"id": "MORTALITY_BASELINE", "status": "source_located_not_extracted", "required": "Age/sex/cause never-smoker hazards and smoking-history risks; reconcile population mortality mixtures before applying HRs.", "urls": ["https://www.abs.gov.au/statistics/people/population/life-tables/latest-release", "https://www.stats.govt.nz/topics/life-expectancy/"]},
    {"id": "HEALTH_UTILITIES", "status": "unresolved", "required": "Country tariff, severity/comorbidity utilities and cessation risk-decay; clinical/VAS scores are not utility weights."},
    {"id": "INCREMENTAL_COSTS", "status": "medicine_components_only", "required": "Wastewater sampling/lab, personnel, service delivery, enforcement, healthcare and opportunity costs with currency and price year; tax is a transfer, not societal resource cost."},
    {"id": "EQUITY", "status": "unresolved", "required": "Joint nonoverlapping subgroup denominators, baseline lifetime health, displaced health and explicit normative weights; do not infer ethnicity from wastewater."},
    {"id": "INDEPENDENT_VALIDATION", "status": "unresolved", "required": "Matched independent targets meeting frozen temporal/catchment requirements; model-derived ABS/ATO or reused wastewater estimates cannot serve as independent truth."},
    {"id": "SOURCE_ADMISSION", "status": "pending", "required": "Full-text/result-specific bias review where only abstract read, edition capture, archive checks and existing evidence-contract review before any real likelihood or prior adoption."}
  ],
  "search_scope": "Targeted gap-filling search plus existing repository evidence; not complete screening of the existing Searchright corpus and not an exhaustive systematic review.",
  "search_queries": ["(Australia[Title/Abstract] OR \"New Zealand\"[Title/Abstract]) AND (\"price elasticity\"[Title/Abstract] OR \"price elasticities\"[Title/Abstract]) AND (tobacco OR cigarette)", "Walker[Author] AND patches[Title] AND cigarettes[Title]", "(smoking[Title] OR cigarette[Title]) AND (transition[Title] OR transitions[Title] OR relapse[Title]) AND (\"New Zealand\" OR Australia)", "Banks[Author] AND smoking[Title] AND mortality[Title] AND Australia", "Donny[Author] AND nicotine[Title] AND standards[Title] AND 2015[Date - Publication]"],
  "review_limits": "Searchright strategies and study identities must reconcile these sources with the existing corpus before admission; a new alias is not a new study. The price-elasticity query returned eight records and both pages were read; broader queries were selectively inspected."
}
```

</details>

Export without adding a runtime dependency:

```python
from pathlib import Path
import csv
import hashlib
import json

path = Path("conductor/tracks/dynamic_frontier_20261108/design.md")
section = path.read_text(encoding="utf-8").split("<!-- TOBAC_PARAMETER_CANDIDATES_V1 -->", 1)[1]
packet = json.loads(section.split("```json\n", 1)[1].split("\n```", 1)[0])
raw = json.dumps(packet, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
assert hashlib.sha256(raw.encode()).hexdigest() == "778777b6a8b703f9764605958d1ac321e0d396f7e5076b9747111d7b9f4ac9bd"
out = Path("outputs/parameter-candidates-20261109")
out.mkdir(parents=True, exist_ok=True)
with (out / "parameters.json").open("x", encoding="utf-8") as stream:
    stream.write(raw)
with (out / "parameters.csv").open("x", encoding="utf-8", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(packet["columns"])
    writer.writerows(packet["records"])
```

Keep the JSON alongside the CSV: the CSV alone omits source scope, dependence and
admission restrictions. Existing output files are not overwritten by this example.

## Executable frontier extension — 9 November 2026

The strongest proposed contribution is **decision identification and adaptive
learning when nicotine markets and measurement processes both change over time**.
Adding a Bayesian estimator, more diseases or an agent-based label is insufficient.
The following are falsifiable research tasks, not claims of completed novelty.

### Current comparator boundary

[ABS's experimental model](https://www.abs.gov.au/articles/household-consumption-illicit-tobacco-and-nicotine-products)
already combines wastewater and auxiliary observations using a Kalman filter.
[SHINE's own programme description](https://mspgh.unimelb.edu.au/centres-institutes/centre-for-epidemiology-and-biostatistics/research-group/shine/research/tobacco-control-interventions)
describes automated country parameterisation, cohort intensity/duration and
31 tobacco-related outcomes, with smoking/vaping/illicit switching development.
The page mixes implemented and planned work; do not infer release readiness from
it. [Impalli et al.](https://doi.org/10.1371/journal.pcbi.1013190) already optimise
wastewater surveillance sites/frequency using VOI for infectious pathogens.
Therefore multi-source filtering, life-course modelling and wastewater VOI each
have precedents. A complete methods review and reproducible head-to-head results,
not this targeted source pass, must support any eventual superiority claim.

| Task | Implementable experiment and baseline | Required evidence of value |
| --- | --- | --- |
| BF1: decision-identification certificates | Extend existing partial-identification bounds to action contrasts. Check whether one action dominates over every admissible parameter/structure combination; otherwise report the unresolved contrast and maximum regret. Compare plug-in estimates, one chosen prior and the existing finite oracle. | Analytic/known-truth set coverage and numerical bound sharpness; no false robust-dominance claims. Demonstrate a decision that is stable despite unidentified market volume, or a reproducible no-use result. |
| BF2: calibration versus sampling under drift | Jointly choose human-yield/calibration studies, repeat wastewater sampling or no study while product mixtures, sewer/assay performance and behaviour evolve. Start with two products, two observation channels and a short finite horizon. | Compare equal-cost fixed sampling, fixed calibration and static staged EVSI against adaptive designs. Report expected and worst-case regret, delay losses, coverage and resource use on withheld drift regimes; truth is unavailable to the policy. |
| BF3: transport-aware causal learning | Introduce explicitly bounded source-to-target discrepancies for historical demand, trial cessation and population policy effects. Compare direct pooling, separate country models and qualified partial pooling; retain null policy-response cases. | Show when transport improves target decisions and when it is harmful. Leave out whole studies/countries, preserve shared samples, report prior/transport sensitivity; no trial-to-cap causal shortcut. |
| BF4: value of heterogeneity and perspective | Compare universal versus targeted policy/research under explicit subgroup constraints and alternative value perspectives, reusing Voiage after provider qualification. | Report a Pareto frontier for aggregate health, worst-group outcomes, cost and regret. Separate facts from normative weights and do not invent distributions over social values. |
| BF5: decision-sensitive living evidence | Reuse Searchright study/report identities; replay corrected, duplicated, withdrawn and newly available sources through versioned parameter mappings and affected outputs. | Same bundle is idempotent; withdrawal removes all dependent contributions; unrelated outputs are unchanged; record exactly when and why a recommendation changes. A retracted source is not merely hidden from the bibliography. |
| BF6: strategic response only when consequential | Add bounded supplier/retailer responses through Paignia, with adoption/substitution components from Innovate where qualified. Compare against exogenous elasticities and null response. | The added mechanism must change a consequential robustness conclusion or improve prespecified validation. Otherwise retain the simpler model; never claim calibrated organised-crime behaviour from seizures alone. |

Sequence BF1 before BF2; BF3 can use the candidate catalogue after appraisal;
BF4 and BF5 build on stable evidence identities; BF6 is optional. Preserve the
small numerical oracle, existing health kernel and Kairos time/resource boundary.
No new provider dependency is required for this evidence packet. Dapane may later
supply microcosting interfaces only after its consumer contract is qualified;
medicine list prices are not a replacement for resource-use measurement.

Before each experiment, freeze data editions, folds, decision horizon, comparable
compute budget and practically material loss thresholds. Evaluate uncertainty-set
coverage/proper predictive scores and decision regret separately. Include prior,
drift, product contamination, censoring, duplicate-source and transport ablations.
Known-truth simulation can qualify numerical/method behaviour now; it cannot
satisfy issue #3's missing independent field validation. Retain its existing
three-prior-years/complete-holdout and comparable-catchment rules unchanged.

The first small research output should be BF1 on the existing exact model,
followed by the two-product BF2 benchmark. This is a more discriminating test of
additional capability than expanding every disease, policy and strategic actor
before a first complete comparison.

## Parameter-source and frontier continuation — 9 November 2026

The [parameter-source edition](../../../evidence/parameter_candidates_20261109/README.md)
contains 65 source-scoped numeric candidates from 12 public sources, together with
explicit missing quantities and a [falsifiable research plan](parameter_research_20261109.md).
It distinguishes published estimates, expert elicitation, external-model assumptions,
legal settings and normative choices. Shared source groups, uncertainty types and
transport limits are retained. The packet changes no live configuration, likelihood,
prior, source-admission disposition, frozen validation rule or signed acceptance.

This entry records incorporation of the candidate packet into the proposed PR source,
not a completed fit or native qualification. Original-publication byte readbacks,
full-text appraisal where unavailable, bibliography-alias reconciliation and
model-specific admission remain separate. The existing first-comparison and #147
qualification requirements are not closed by this packet's offline validation.
