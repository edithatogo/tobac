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
- [ ] Hash-install and verify actual versions, dependency consistency, typing, security, clean packaging and affected numerical parity. Record latest available versus latest qualified, incompatibility and disposition for every held-back dependency.
- [x] Mature existing code with bounded fixes, shared-contract reuse, unit/error handling, deterministic RNG, configuration validation and focused regression checks before adding equivalent new machinery. Verified context/cache/error guards reuse existing contracts; numerical reference retained.
- [x] Implement a minimal logged analytical DAG with immutable manifests and fail-closed input admission; qualify Snakemake separately while retaining Nox engineering sessions. Explicit analytical Snakemake selection is reconciled in workflow/README.md; real M1, cache, preservation and corrupt-copy checks passed. Latest signed-lock admission remains a final checkpoint gate.
- [ ] Checkpoint: baseline reproduction and affected/workstream tests pass; no unexplained numerical drift; workflow failure/resume checks pass. Empirical expansion requires this gate.

## Phase 1 — Decision definition and systematic evidence (R01–R06, R18–R19)

Preparation delivered in decision-definition.md, systematic-search.md and
phase1-appraisal.csv; qualification/gaps are in phase1-progress.md. These are partial
deliverables, not closure of the source-admission or systematic-search gates below.

- [ ] Freeze initial decision, target populations/products, dated NZ/AU policy baselines, perspectives, horizon, estimands and validation split before fitting.
- [ ] Qualify Searchright CLI/provider routes; run versioned searches with seed checks, source-specific queries, screening, exclusions and update rules.
- [ ] Verify existing external archive/GitHub/Hugging Face identities, rights, exact destinations and readback; save originals outside tobac.
- [ ] Verify every extracted figure against its original location, units and rounding; reconcile source totals, versions and covariance; quarantine discrepancies.
- [ ] Build source/model/parameter/formula matrices with explicit adopted, adapted, alternative, context-only, excluded or unavailable dispositions.
- [ ] Checkpoint: evidence lineage and retrieval/recovery pass; identified gaps constrain claims rather than being filled with invented values.

## Phase 2 — First empirical vertical slice (R03–R10, R16, R18)

P2.1 feasibility executed: existing NZ coverage audited with Polars, actual AU programme
design checked and an ACIC denominator discrepancy quarantined. See phase2-feasibility.md.
Current illicit consumption and empirical monetary VOI are not identified/admitted; fitting
and held-out comparison remain gated by Phase 0 and Phase 1. No row below is closed by a
scope audit or algebraic argument alone.

- [ ] Integrate qualified NZ survey, lawful releases, prices, trade and denominators using Polars; add actual Australian wastewater programme design and measurement evidence.
- [ ] Reconcile dates, products, catchments, lawful unrecorded flows, stock, shared sources and calibration. Assess identifiability before fitting; retain partial-identification bounds where needed.
- [ ] Fit the supported baseline and one existing retail/cessation contrast; preserve original finite-state reference results separately.
- [ ] Evaluate held-out predictions and incremental wastewater information over existing evidence; report unpriced cost ceilings when actual costs are absent.
- [ ] Checkpoint: publish a reproducible bounded result or explicit non-identification finding before expanding policy mechanisms; no national funding claim without supporting evidence.

## Phase 3 — Policy, health and equity expansion (R05–R08, R12, R18)

P3.1 readiness preparation is in phase3-design.md and phase3-module-matrix.csv. The actual
shared-evidence audit reports 28 blocked rows; see phase3-progress.md. Empirical mechanisms,
health/equity outputs and PSA remain unimplemented pending Phase 0–2 and module-specific
evidence. The contracts and library review do not close the tasks below.

- [ ] Add accepted excise, retail, nicotine, cohort, cessation, enforcement and product-substitution modules incrementally with independent reference checks.
- [ ] Add health histories, disease lags, competing risks, HR-QoL and costs only where justified; preserve separate perspectives and subgroup outputs.
- [ ] Run module-level PSA, structural sensitivity and predictive checks at each addition, not only after expansion.
- [ ] Checkpoint: verify subgroup aggregation, double-counting prevention, horizon/discounting, external validation and incremental explanatory value against the simpler baseline.

## Phase 4 — Diffusion, competition and extended VOI (R10–R12)

P4.1 reuses existing M3 components and qualified installed Voiage on finite synthetic cases;
see phase4-progress.md. Current Innovate still requires pandas/pandasdmx. Scenario and
formula contracts are in phase4-design.md and phase4-scenarios.csv. Empirical diffusion,
competition and monetary VOI remain gated; no task below is closed by source inspection
or synthetic qualification alone.

- [ ] Qualify actual Innovate release/API early via Phase 0; now integrate only accepted policy mechanisms and adoption evidence.
- [ ] Execute uptake, competition, spillover and delay scenarios with empirical and hypothetical inputs labelled separately.
- [ ] Evaluate EVPI/EVPPI/EVSI/ENBS, implementation-adjusted and staged studies; check simulation bias and convergence against finite oracles and avoid adding overlapping information values.
- [ ] Checkpoint: costs, timing and actions are consistent across comparators; empirical and software acceptance remain separate.

## Phase 5 — Cross-model sensitivity and clustering (R12–R13, R18)

P5.1 implements a synthetic SciPy/scikit-learn qualifier with training-only cluster
discovery, bootstrap stability, supervised label prediction and no-use/leakage checks.
See phase5-progress.md. It is an isolated software candidate, not cross-model empirical
PSA, country/group validation or a demographic finding. Original tasks remain open.

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
