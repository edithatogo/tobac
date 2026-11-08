# Implementation plan

Revised 6 November 2026 following sequencing review. Unchecked tasks are not completed.
Dependencies below are acceptance gates, not merely a suggested ordering. Requirements
R01–R19 are defined in spec.md. Existing owners retain runtime and integration promotion.

## Phase 0 — Baseline, runtime and workflow foundation (R14–R17)

- [x] Record actual HEAD, ownership, bounded context hashes and reusable baseline receipts; reconcile with current main before integration. Receiving 3.15.2 source and exact owner packets are integrated; final publication readback remains separate.
- [x] Inventory active source, scripts, notebooks, CI, containers and environments; map existing capabilities, defects, duplicated calculations and pandas/xarray usage. See phase0-inventory.md and its integrated disposition; historical/environment boundaries remain explicit.
- [x] Record a dated upstream version census for direct and transitive dependencies, including Python patch, Searchright, Innovate, Voiage and Snakemake; distinguish release, prerelease and development revisions.
- [x] Coordinate the existing dependency/Polars owner; consume their qualified commits rather than repeat migration or replace their environment. Frozen source/profile/Nox packets integrated through b118592; final lineage and latest-pin promotion remain separate open gates below.
- [x] Resolve newest supported candidates in isolated repo-local Python 3.15.2 environments; use existing lock_receipt.py and reviewed hash locks for all affected profiles, extending coverage for new analytical tools. Five reviewed latest profiles plus analytics resolve; upstream-conflicting holds are explicit. Earlier 3.15.1 qualification remains history.
- [x] Hash-install and verify actual versions, dependency consistency, typing, security, clean packaging and affected numerical parity. Frozen 4015cc3 qualification is reused; integrator fresh native execution/readback and the 1262-pass suite renew admission for the adopted lock. Dated held-back dispositions remain explicit; candidate hosted promotion is separate.
- [x] Mature existing code with bounded fixes, shared-contract reuse, unit/error handling, deterministic RNG, configuration validation and focused regression checks before adding equivalent new machinery. Verified context/cache/error guards reuse existing contracts; numerical reference retained.
- [x] Implement a minimal logged analytical DAG with immutable manifests and fail-closed input admission; qualify Snakemake separately while retaining Nox engineering sessions. Explicit analytical Snakemake selection is reconciled in workflow/README.md; real M1, cache, preservation and corrupt-copy checks passed. Latest signed-lock admission remains a final checkpoint gate.
- [ ] Checkpoint: baseline reproduction and affected/workstream tests pass; no unexplained numerical drift; workflow failure/resume checks pass. Empirical expansion requires this gate.

## Phase 1 — Decision definition and systematic evidence (R01–R06, R18–R19)

- [ ] Freeze initial decision, target populations/products, dated NZ/AU policy baselines, perspectives, horizon, estimands and validation split before fitting.
- [ ] Qualify Searchright CLI/provider routes; run versioned searches with seed checks, source-specific queries, screening, exclusions and update rules.
- [ ] Verify existing external archive/GitHub/Hugging Face identities, rights, exact destinations and readback; save originals outside tobac.
- [ ] Verify every extracted figure against its original location, units and rounding; reconcile source totals, versions and covariance; quarantine discrepancies.
- [ ] Build source/model/parameter/formula matrices with explicit adopted, adapted, alternative, context-only, excluded or unavailable dispositions.
- [ ] Checkpoint: evidence lineage and retrieval/recovery pass; identified gaps constrain claims rather than being filled with invented values.

## Phase 2 — First empirical vertical slice (R03–R10, R16, R18)

### Source-admission review — 8 November 2026

Reviewed the clean owning branch `codex/p2-empirical-slice-20261107` at
`3d1f5e7608cd5a6db4b2a66a640557106a630685` against `c239b18`, including
its reconciliation sections P2.126, P2.222 and P2.237. These dispositions
apply to the reviewed candidates. The admitted observation count is zero.

| Candidate | Disposition and basis |
|---|---|
| NZ historical survey, lawful releases, prices, trade and population | Candidate matching only. Retain the P2.9 Polars audit as a scope and overlap diagnostic. Survey interview windows, annual releases and monthly trade have different time support. Stock and unrecorded lawful flows remain unresolved. |
| Kim NZ wastewater supplement, DOI 10.1016/j.scitotenv.2025.181223 | Measurement-method evidence only. The manifest and six bound files matched their hashes, with 142 unique site/date occasions, 451 quantified cells and 117 censored cells. Hold likelihood admission pending catchment and contributing population identity, dated flow, effective ANBA censoring, processing, paired-assay dependence and calibration. |
| Health NZ July 2026 dispensing extract and technical notes | Historical service context. The v2 manifest, prior manifest, original ZIP and notes matched their hashes, and 20 logical CSV records matched field for field. Initial counts are nested in all dispensings and people can overlap across chemicals and years. Claims counts cannot establish incremental reach, quit response or consumption. The app's CC BY 4.0 statement is recorded in the manifest. Exact downloadable-object rights and destination readback remain open. |
| ACIC regional reports and Wang national and Queensland analyses | Programme and measurement-method context. Eight repeated Queensland site codes and pooled chart means support design review. Daily or pool-level dates, flow and product calibration, a national site crosswalk and comparable catchment support remain unresolved. Retain the denominator discrepancy in quarantine. The national estimate reuses NWDMP data and modelled lawful supply. |
| ATO tax gap, ITEC and ABS experimental series | ATO is contextual modelled post-seizure supply on a fiscal-year boundary. ITEC inherits the ATO baseline and uses wastewater. ABS is an alternative model using ACIC and administrative/survey inputs. Keep shared dependencies together and exclude all three from the independent consumption score. |
| AIHW NDSHS tobacco workbook, Table 1.33 | Independent purchase diagnostic. The original workbook and replay script matched their pins and Python 3.15.2 reproduced floors of 75.6 and 200.1 packets per 100 current smokers and conditional thresholds of 43.2 and 21.8 packets. The survey outcome has different units, timing and geographic support from the consumption estimand. The [AIHW licence](https://www.aihw.gov.au/copyright) provides CC BY 4.0 subject to attribution and exceptions. Exact workbook rights and archive-object readback remain open. |

The checks above are local intake readbacks. GitHub CLI confirmed the identity and
public visibility of the existing NZ government archive, whose stated scope is NZ
government records. This is repository metadata. The reviewed packet supplies
zero qualified canonical archive-object readbacks or source-admission receipts.
For each candidate proposed for admission, bind its exact edition and hash to
verified object-specific rights, an in-scope destination and an independent
byte-matching readback before creating the source receipt.

Before a fit, freeze an admitted, hash-bound observation manifest with matched
policy dates, populations, products, units and dependence groups. Resolve the
stock and lawful-flow bridge and product-specific wastewater calibration. The
contrast requires independent support for a retail or cessation policy response
on that same scope, including the bridge from medication offers and service use
to population demand for a cessation contrast.

Before scoring, freeze an independent outcome with matching consumption units,
dates and geographic support. Apply the prespecified latest complete year with
at least three earlier complete years, and leave-one-catchment-out folds only
where at least four comparable catchments have adequate coverage. Group shared
measurement occasions and derivative series. Neither split qualifies on this
packet. Paired predictions, incremental information and a decision ceiling
remain open. The finite-state numerical reference stays separate. The
non-identification finding is recorded locally. Publication remains open.

- [ ] Integrate qualified NZ survey, lawful releases, prices, trade and denominators using Polars; add actual Australian wastewater programme design and measurement evidence.
- [ ] Reconcile dates, products, catchments, lawful unrecorded flows, stock, shared sources and calibration. Assess identifiability before fitting; retain partial-identification bounds where needed.
- [ ] Fit the supported baseline and one existing retail/cessation contrast; preserve original finite-state reference results separately.
- [ ] Evaluate held-out predictions and incremental wastewater information over existing evidence; report unpriced cost ceilings when actual costs are absent.
- [ ] Checkpoint: publish a reproducible bounded result or explicit non-identification finding before expanding policy mechanisms; no national funding claim without supporting evidence.

## Phase 3 — Policy, health and equity expansion (R05–R08, R12, R18)

- [ ] Add accepted excise, retail, nicotine, cohort, cessation, enforcement and product-substitution modules incrementally with independent reference checks.
- [ ] Add health histories, disease lags, competing risks, HR-QoL and costs only where justified; preserve separate perspectives and subgroup outputs.
- [ ] Run module-level PSA, structural sensitivity and predictive checks at each addition, not only after expansion.
- [ ] Checkpoint: verify subgroup aggregation, double-counting prevention, horizon/discounting, external validation and incremental explanatory value against the simpler baseline.

## Phase 4 — Diffusion, competition and extended VOI (R10–R12)

- [ ] Qualify actual Innovate release/API early via Phase 0; now integrate only accepted policy mechanisms and adoption evidence.
- [ ] Execute uptake, competition, spillover and delay scenarios with empirical and hypothetical inputs labelled separately.
- [ ] Evaluate EVPI/EVPPI/EVSI/ENBS, implementation-adjusted and staged studies; check simulation bias and convergence against finite oracles and avoid adding overlapping information values.
- [ ] Checkpoint: costs, timing and actions are consistent across comparators; empirical and software acceptance remain separate.

## Phase 5 — Cross-model sensitivity and clustering (R12–R13, R18)

- [ ] Execute joint correlated PSA, global/structural/prior/value sensitivity, thresholds, interactions and decision regret on validated models.
- [ ] Discover clusters on training simulations only; select scaling/features/cluster count and assess bootstrap stability and interpretability.
- [ ] Train supervised predictors of frozen cluster labels; validate on held-out seeds/parameter regions and country/time groups where applicable. Compare simple baselines and report imbalance/calibration.
- [ ] Checkpoint: no train/test leakage or causal interpretation of clusters; unstable clusters yield a no-use finding, not forced labels.

## Phase 6 — Reproducibility, refresh and integration (R14–R19)

- [ ] Execute full suite, relevant numerical replay, clean-package, security and declared platform gates at the coherent milestone; reuse unchanged receipts.
- [ ] Verify full source-to-formula-to-output manifests, offline reconstruction, missing/corrupt input rejection and recovery after interrupted execution.
- [ ] Recheck latest versions at release decision; changed candidates repeat affected gates without silently refreshing frozen results.
- [ ] Add new dependencies to existing Renovate/lock coverage; retain sole updater, no automatic scientific merges and separate experimental canary.
- [ ] Verify source revisions/retractions trigger impact analysis and new output versions; preserve old editions and human interpretations.
- [ ] Reconcile shared Conductor files with the integrator; guarded publication and receiving ref/file readback, then terminal evidence handoff.

## Execution controls applying to every phase

- [ ] Instantiate bounded task cards from execution.md before implementation; resolve exact commands/paths and prerequisite receipts.
- [ ] Implement and exercise medallion promotion/receipt validators in E2/E3; do not treat the design tables as executable gates.
- [ ] Complete applicable standards.md checklist evidence with each scientific/software checkpoint.
- [ ] Execute companion hardening H0/H1 alongside phases and H2 before release.
