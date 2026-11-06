# NZ and Australia tobacco policy and incremental wastewater information

Requested 6 November 2026. Status: requirements recorded; empirical implementation open.
Owner: chat 01a1af53-2093-7f70-b761-e5f6cb7b769c, branch codex/nz-au-empirical.
Base adb3f81. No native mutation scope claimed. Existing Polars migration and shared
Conductor integration retain their owners. This isolated packet requires reconciliation.

## Purpose and claims

Deliver a comprehensive NZ tobacco-policy decision model with an Australian empirical
comparator and incremental wastewater VOI over existing surveillance. Permit no-study,
null-effect and policy-disagreement findings. Country differences are explanatory inputs,
not nuisance differences to erase. Completeness is assessed against an explicit coverage
matrix, not parameter count. Software execution is not empirical or policy acceptance.

## Requirements and acceptance

| ID | Requirement | Acceptance evidence |
|---|---|---|
| R01 | Systematic search using edithatogo/searchright | Versioned protocol, queries, provider receipts, dates, deduplication, inclusion/exclusion reasons, study links, updates and source coverage; no systematic-search claim from web discovery alone |
| R02 | External source preservation | Qualified existing GitHub/Hugging Face/archive producer destination; immutable revisions, original-byte hashes, licences, retrieval timestamps, readback and recovery; source documents/data excluded from tobac code |
| R03 | Verified extraction | Every numerical input links to source page/table/cell and original hash, units, denominator, dates, geography, product and extraction version; independently reconcile extracted totals/intervals and quarantine mismatches |
| R04 | NZ/AU evidence integration | Health surveys, tobacco/vaping returns, trade, prices, Customs, Police, Justice, WHO, wastewater, health outcomes, cessation and costs each have an explicit admitted/context-only/unavailable/excluded disposition |
| R05 | Model comparison | Search and appraise NZ BODE3/SHINE/endgame, retail-access, excise, cessation and Australian tobacco models; enumerate every identified parameter and equation with adopt/adapt/reject/defer rationale; never blindly pool overlapping estimates |
| R06 | Comprehensive policy scope | Dated current baseline plus excise/price, retail access, nicotine limits, cohort sales restrictions, vaping/other nicotine, cessation, enforcement/illicit substitution and combined interventions; country-specific eligibility, implementation, compliance, horizon and counterfactual |
| R07 | Health and distribution | Age/sex/deprivation and appropriate population strata; smoking histories, initiation, cessation, relapse, dual use and disease lags; deaths, morbidity, HR-QoL/QALYs where justified, costs and uncertainty; no ethnicity inferred from wastewater |
| R08 | Multiple perspectives | Health-system, societal, fiscal, enforcement, consumer and equity results separately; transfers distinguished from resources; equity weights and discount rates explicit scenarios, not estimated preferences |
| R09 | AU programme comparator | ACIC actual analytes, coverage, frequency, methods, calibration, publication delay, governance and costs where available; distinguish nicotine from tobacco and illicit origin; compare NZ sampling infrastructure and transportability |
| R10 | VOI | EVPI, grouped EVPPI, EVSI, ENBS, targeted entropy/variance reduction, opportunity loss and implementation-adjusted information; incremental value conditional on existing evidence, shared bias and real programme costs; finite oracles retained |
| R11 | Innovate | Qualify actual installed library/API for diffusion, competing policies, uptake, saturation, delays, networks and spillovers; distinguish empirical adoption fit from hypothetical trajectories; explicit unavailable-library gate |
| R12 | Uncertainty | Correlated probabilistic sensitivity, parameter/structural/prior/value/scenario uncertainty, country heterogeneity, interactions, missingness, measurement error, thresholds, global sensitivity and decision robustness with convergence evidence |
| R13 | Clustering and prediction | Unsupervised discovery on training simulations; choose scaling/distance/cluster count and assess bootstrap stability; supervised prediction of frozen cluster labels on held-out simulations, country/time splits where applicable; no reuse of discovery data as validation |
| R14 | Workflow and provenance | Snakemake DAG, structured logs, resource limits, seeds, failures and resume receipts; version inputs, formulae, model code, environment and output manifests; immutable external input references; Nox engineering gates retained |
| R15 | Runtime | Repo-local Python 3.15.1 and newest qualified dependencies; Polars/Arrow not pandas/xarray; exact locks and candidate compatibility evidence; incompatible latest dependencies remain blocked, no forced bypass |
| R16 | Validation | Unit dimensional checks, independent numerical oracles, external/temporal validation, posterior predictive checks, calibration, affected and workstream tests, full coherent-milestone replay, receiving-ref readback |

## Scientific boundaries

Do not treat seizures as consumption, legal releases as same-period consumption,
WHO republished NZHS as independent evidence, Australian estimates as NZ observations,
forecasts as new data, or tax receipts as societal benefits. Do not import incompatible
policy-effect estimands. Use a shared-source covariance/dependence graph and condition once.
Published HR-QoL utilities require instrument/value-set, age, condition, country, year,
comorbidity mapping and uncertainty; no invented QALY conversion from normalised scores.
A public source can remain unusable for a target likelihood. Missing matched assays,
calibration, causal contrasts, costs and governance remain explicit gates.

## Refinements from sequencing review — 6 November 2026

| ID | Requirement | Acceptance evidence |
|---|---|---|
| R17 | Mature before extending | Inventory and triage existing code; reuse contracts/calculations; baseline parity, strict validation, deterministic RNG and actionable errors; scoped fixes with regression evidence before new modules |
| R18 | Identifiability and decision relevance | Assess structural/practical identification before fitting; separate parameter uncertainty from heterogeneity; prespecified validation splits; simpler-model benchmarks, predictive calibration, decision regret and explicit non-identification findings |
| R19 | Living inputs and controlled upgrades | Dated latest-version census, latest-qualified comparison and blocked-version reasons; source revision/retraction and schema-change detection; impact analysis, new immutable output editions and recovery tests |

Dependencies must be updated through executable qualification tasks, not merely mentioned
in prose. The latest stable compatible release is the promotion target; bleeding-edge
prereleases/development commits remain separately identified canaries until qualified.
Python remains the explicitly verified repo-local 3.15.1 unless a newer patch is qualified
through the owning lane. Never silently downgrade Python to obtain dependency compatibility.
