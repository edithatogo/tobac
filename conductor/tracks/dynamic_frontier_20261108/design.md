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
