# Parameter candidates — 9 November 2026

**65 numeric candidates / 12 public sources. No production parameters or admitted observations changed.**

This is a targeted evidence edition for the gaps discussed in `tobac`, not a completed systematic review, a full code-parameter inventory, or an updated NZ posterior. The existing first-comparison evidence cutoff (6 November 2026), source-use decisions, public-only scope and validation rules remain unchanged. Retrieval on 9 November does not change a study's observation dates.

## Contents and interpretation

- `registry.json` is the canonical structured source/parameter record.
- `parameters.csv` and `sources.csv` are exact tabular views of that record.
- `gaps.csv` distinguishes 20 unresolved or partly resolved quantities, data requirements and value choices.
- The companion Conductor plan is `conductor/tracks/dynamic_frontier_20261108/parameter_research_20261109.md`.

Each numeric entry retains its source, original units, time/population scope, statistical interval type, shared-data group and use limits. `distribution: null` means no probability distribution has been fitted. `candidate_only` means this catalogue is not a parallel admission route: use existing `Scope`, `EvidencePacket`, `SupplyBasis`, source handoff and source-to-target review before conditioning. Source keys are catalogue aliases to reconcile, not new independent observations.

## What has been sourced

| Block | Records | Permissible initial use |
|---|---:|---|
| Historical NZ product demand | 4 | Product-specific and directional elasticity sensitivities, not a current-market posterior |
| NZ excise from January 2026 | 6 | Dated fiscal reference settings, excluding GST; check relevant product and later amendments |
| PHARMAC discounting | 3 | Named cost-utility reference case and required sensitivity alternatives, not an empirical prior |
| Australian PBO April 2026 model | 11 | External-model comparison only, not independent empirical calibration |
| NZ cessation trial | 5 | Trial-population six-month endpoints; use counts OR contrasts |
| Australian withdrawal-service cessation trial | 3 | Specialised-population challenge case, not automatic general-population transport |
| Australian mortality and cancer cohorts | 8 | Relative-effect candidates requiring compatible absolute baseline hazards |
| Nicotine-reduction trial | 5 | Intervention specifications and short-term biomarker effects, not disease-risk proportionality |
| Queensland disease utilities | 8 | Australian-value-set scenario means with overlapping conditions retained |
| Queensland ED use/cost | 6 | Observational annual burden candidates; price year is unresolved |
| Australian denicotinisation elicitation | 6 | Preprint expert-belief sensitivity, not observed efficacy or retailer-cap effects |

## Important source distinctions

The Tait elasticity study reports historical NZ regression estimates, without uncertainty intervals in the reviewed abstract. PBO's costing framework instead supplies assumed elasticities. They must not be pooled as independent studies. The opened PBO page has a **28 April 2026** footer and manufactured/loose-leaf own-price values **−1.477/−1.417**. An earlier retrieval in the session described a later edition and −0.9. That discrepancy is retained as an edition warning: this packet uses the explicitly opened April version and does **not** certify it as the latest November assumption set. Table directions and zero/absent cross terms are not inferred.

The NZ excise weight threshold is a legal product-classification threshold, not an estimate of grams of tobacco in a cigarette. PBO's 0.6 g roll-your-own setting is likewise a comparator assumption, not a measured NZ conversion.

Walker trial arm fractions are computed directly from published numerators and denominators; the published risk differences are separate summaries of the same trial. The Bonevski interval is a **credible interval**. Howe's preprint intervals are **interquartile ranges of pooled expert judgements**. None is converted to a standard error or a prior here. No trial endpoint is silently annualised into a transition probability.

Banks and Weber share the NSW 45 and Up cohort family. The Queensland utility and ED-cost papers share the QPHS 2022–2023 linked-cohort family. These groupings flag likely overlap, not measured covariance. Do not count the whole population, subgroups, marginal conditions and published contrasts as independent evidence.

The Queensland ED difference between current and never smokers is an association. It is not automatically an avoidable cost of smoking or a saving caused by cessation. The abstract does not establish the cost price year; it remains null. Utility deficits must not be summed across comorbidities, and smoker hazard ratios must not simply multiply population life-table rates that already include smokers.

Howe et al. elicit Australian nicotine-standard effects, not effects of the prospective approximately 600-retailer restriction. The authors also discuss ambiguity in the illicit-switching denominator. That quantity is therefore not supplied as a fitted diversion parameter.

## What remains genuinely missing

The first policy comparison still lacks matched consumption/supply cells, dated wastewater flow/population and effective censoring information, target biological/product calibration, a credible policy-response bridge and eligible independent outcomes. These are not resolved by better citations for health effects or by importing an external model's assumptions. The broader dynamic model additionally needs initial joint states, age/history transitions, relapse, absolute disease hazards, risk decay, incremental policy/study costs and justified dependence. See `gaps.csv`.

## Source and verification boundary

Source content was reviewed via public web pages or the PubMed connector. Numerical extraction locations and reviewed extent are recorded; abstract-only and truncated full-text review are explicit. **No original-source byte checksum or canonical archive readback is claimed.** Hashes in the delivery bundle verify our generated files only. This pack republishes attributed facts, not full third-party texts or licensed utility-scoring algorithms.

Some candidate sources overlap earlier repo reviews. Alias resolution must reuse those identities. The existing NZHS and Kim packs are referenced rather than recopied as independent evidence. The broader Searchright screening programme is not completed by this targeted sourcing pass.

The bundle's standard-library checks test field consistency, uncertainty labels, supports, counts, dependency identities and JSON/CSV parity. They neither validate causal transport nor substitute for repository-wide, native or hosted qualification. No new data request, contact, restricted access, paid commitment, submission or collection was made.
