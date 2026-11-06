# Policy, health and equity expansion contract — version 1

Status: conceptualisation and admission requirements, 6 November 2026. Empirical expansion
is not implemented or accepted. Phase 0 renewal and Phase 1–2 evidence/fit gates remain
open. phase3-module-matrix.csv is the coverage and acceptance queue, not a parameter table.

## Existing mechanisms and extension order

Reuse the existing retail/cessation action set and finite decision oracle. Its outcomes
are conditional normalised scores; value_sensitivity.VALUE_UNIT explicitly excludes NZD
and QALYs. Do not relabel them, infer disease incidence from them or restore historical
optional health engines without qualification. No existing source parameter was changed.

After the first matched empirical slice passes, add mechanisms in this order: accepted
retail/cessation response, product switching, excise/pass-through, age/cohort restrictions,
nicotine standards and enforcement. Reconcile their joint causal structure before combined
scenarios. Simultaneous policy changes are not independent additive effects. Every addition
requires a null-effect case, an independent numerical reference, simpler-model comparison,
source/parameter/formula lineage and separate predictive applicability evidence.

For each country retain operative policy dates, legal product/channel, intensity, enforcement,
uptake, delays and effect persistence. Model assignment changes exposure, which changes
product-specific histories, then health hazards and resource use. A seizure count is not
a consumption reduction. A nicotine standard does not automatically imply proportional
toxicity reduction. A legal age/cohort rule cannot retrospectively erase existing exposure.

## Health calculations and parameter admission

F:H1: Q[g,a] = sum_t PY[g,a,t] * u[g,a,t] / (1+r_health)^tau[t].
PY is living person-years within an interval, u is justified HR-QoL utility, tau is years
from the valuation origin. If living person-years are already supplied, do not multiply
by survival a second time. Death contributes zero subsequent person-years. Specify interval
timing and within-cycle integration, and compare coarse steps against a finer-step oracle.
Do not add a half-cycle adjustment twice. Negative utilities are allowed where the verified
instrument/tariff supports them; do not clamp all utilities to zero or impose a generic
instrument-independent minimum. This formula is a contract, not an executed health model.

Health-state trajectories require baseline disease incidence, mortality, competing risks,
smoking/product intensity and duration, time since cessation, risk reversal/latency, age and
sex, migration/entry/exit, and subgroup dependence. Define whether disease states are mutually
exclusive or overlapping. Comorbidity utility/cost rules must be justified and varied; do
not simply sum overlapping disease burdens. Intervention effects must not also be embedded
in baseline hazards or counted again through aggregate attributable fractions.

F:H2: DeltaQ[g,a] = Q[g,a] - Q[g,reference], using paired draws and identical eligible
population definitions. Distinguish total-population QALYs from per-person values. A lifetime
health horizon needs terminal-age, competing mortality and residual-value checks; the initial
five-year budget scenario cannot truncate health effects silently. Never extrapolate an
unvalidated disease model merely to populate a long horizon.

The [PHARMAC health-benefit guidance](https://www.pharmac.govt.nz/medicine-funding-and-supply/the-funding-process/policies-manuals-and-processes/economic-analysis/prescription-for-pharmacoeconomic-analysis-methods-for-cost-utility-analysis/6-estimating-health-benefits)
identifies NZ EQ-5D Tariff 2 as its reference and separates QALYs from other value judgements.
Appraise instrument version, tariff source/licence, health state, age/condition, valuation
population/year, uncertainty and transportability before using any actual utility. No tariff
coefficients or tobacco disease utilities have been extracted/admitted here. Do not equate
an EQ-5D-5L score with a 3L tariff without a supported mapping. AU valuation choices need
their own source and applicability review.

The [PHARMAC discounting guidance](https://www.pharmac.govt.nz/medicine-funding-and-supply/the-funding-process/policies-manuals-and-processes/economic-analysis/prescription-for-pharmacoeconomic-analysis-methods-for-cost-utility-analysis/8-discounting)
specifies 3.5% for its CUA costs and health, with 0% and 5% sensitivity. Record this as a
candidate NZ pharmaceutical reference case; a whole-of-government tobacco-policy or AU
analysis needs an explicit applicable perspective-specific choice. Do not import it as a
universal discount rate or silently discount affordability cash flows the same way.

## Perspective and distributive accounting

F:C1: discounted resource cost = sum_t incremental_resource_cost[t] / (1+r_cost)^tau[t].
Record country/currency, price year, real/nominal basis, inflation/FX sources, setup versus
recurring costs, scale and implementation lag. Keep health-system, societal, fiscal,
enforcement and consumer accounts separately reconcilable. Taxes/fines move between accounts
as transfers; their revenue is not an additional societal resource gain. Consumption
expenditure is not automatically consumer welfare. Avoid double counting productivity,
caregiving, willingness to pay and health utility. Missing costs stay missing.

F:E1: population total = sum_g subgroup total for one explicitly exhaustive, disjoint
partition. A person in overlapping ethnicity/deprivation classifications cannot be counted
twice. Keep country, action, draw, time, age and partition identity throughout Polars joins;
assert key uniqueness and join cardinality before aggregation. Cross-classified partitions
require adequate denominators and covariance; marginal tables do not identify their joint
distribution. AU Indigenous categories are not mappings to NZ ethnicity groups.

F:E2: report unweighted subgroup DeltaQ and resource costs first. Equity-weighted outcomes
sum_g w[g]*DeltaQ[g] only as a separate normative scenario with weight rationale and scale.
Do not change utilities to encode deprivation or need. Display alternative weights, subgroup
opportunity costs and the equity/efficiency frontier without adding perspectives together.
Unknown ethnicity stays unknown; catchments do not identify individual ethnicity or disease.
Disclose suppressed cells and subgroup uncertainty; no rankings from unstable small estimates.

Full distributional CEA also needs the distribution of baseline lifetime health and displaced
health/opportunity costs. Weighted incremental QALYs alone are not full DCEA. Atkinson/Gini
indices require a defined health distribution, population weights and their valid mathematical
domain; negative increments are not positive lifetime health levels. Do not shift values by
an arbitrary constant to make an inequality index computable. The
[ISPOR data-requirements paper](https://www.ispor.org/publications/journals/value-in-health/abstract/Volume-26--Issue-1/Distributional-Cost-Effectiveness-Analysis-of-Health-Technologies--Data-Requirements-and-Challenges)
emphasises subgroup definitions and evidence availability; the full-text appraisal remains
pending. This contract does not establish DCEA validity or standards certification.

## Uncertainty and validation before each promotion

Map every stochastic input to a verified estimate/distribution, covariance/dependency group,
country/time applicability and source hash. Missing empirical uncertainty is not a point mass.
Paired actions use common draws where valid; independent validation uses held-out draws and
observations. Report Monte Carlo error and convergence, rare-event stability and structural
alternatives, including no policy effect, no hazard reversal and alternative comorbidity rules.
Do not assign arbitrary beta distributions to all fractions or infer causal uncertainty
from cross-sectional subgroup variation.

Before implementation freeze test cases for: null effects, stock/population conservation,
probability normalisation, competing-death exclusion, utility integration against hand cases,
discount timing, subgroup totals, overlapping-category rejection, transfer reconciliation,
monotonicity only where biologically warranted, lifetime truncation and missing utility/cost
rejection. Independent hand calculations test software; external validation needs external
observations. No surrogate health engine or empirically labelled PSA is run in P3.1.

## Library reuse disposition

Your [vop_poc_nz manifest at ad84d309](https://github.com/edithatogo/vop_poc_nz/blob/ad84d3090a2d97f2805a86e94a7b9614a3d1ab14/pyproject.toml)
was read directly. It requires Python >=3.12,<3.15, pandas, Polars <2 and Arrow <26. Those
constraints conflict with this repository's Python 3.15.2 / Polars 2.1 / Arrow 26 baseline
and no-pandas requirement. It is a conceptual reuse candidate, not installed or runtime
qualified. No --no-deps, interpreter downgrade or copied statistical implementation is used.
Its README's validation claims do not establish parity here. Qualify compatible upstream
interfaces and independent weighted/discounting/VOI cases before any adapter or promotion.

[tutorial_methods_equity at 3fb9e78](https://github.com/edithatogo/tutorial_methods_equity/tree/3fb9e78a7a068c3b5a3f991deb2c41c31aede3ce)
is a contextual methods candidate. Its README retains a placeholder citation and no root
pyproject was available; no executable qualification, canonical reference or code reuse is
claimed. Preserve its MIT terms if code is later reused. Existing Innovate qualification
and M3's Voiage adapter retain their owners and are not replaced by this task.
