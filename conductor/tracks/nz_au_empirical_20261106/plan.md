# Implementation plan

## Active public-only boundary and next executable slices — 11 November 2026

This section is the **current work definition**; older continuation and exploratory access tasks below are preserved as historical progress/evidence rather than overriding this scope. The [11 November issue #3 reconciliation](https://github.com/edithatogo/tobac/issues/3) distinguishes a present, completable public-evidence feasibility/identifiability methods result from a later, potentially access-dependent matched NZ/AU comparison. Subscriptions, unpublished records, raw non-public assay/catchment data, custodian applications, new collection and external contact are [deferred](../../roadmap.md#deferred-access-dependent-empirical-expansion--11-november-2026), not permitted active work.

- [x] Source-native retrieval, DOI/report deduplication and title/abstract screening recorded for 26,571 deduplicated records: 9,760 forwarded and 16,811 excluded; neither number represents completed full-text eligibility.
- [x] Record 2,183 PMC-accessible full-text routes and 7,577 access-dependent records as **access dispositions** only. The public-only active review should select and justify a bounded decision-relevant subset; deferred access-dependent sources are not an all-or-nothing milestone.
- [x] Independently hash-read back 33 external Bronze artifacts, preserving rights/eligibility distinctions; no automatic Silver/Gold observation promotion or all-source licence approval.
- [x] Preserve the executed first-comparison audit's three blocked data roles and 28 non-compatible source-handoff rows. No empirical likelihood, policy effect or paired held-out score was produced.
- [ ] Screen/appraise the bounded, public-accessible full-text subset with report-study linkage, result locators, uncertainty/transport assessment and shared-data IDs; explicitly report the selection rule and unreviewed residual corpus.
- [ ] Reconcile source-to-parameter-to-code identity and implement exact bounded decision-sufficiency checks on public facts/declared scenarios, with negative controls for duplicate, stale, inaccessible and incompatible evidence.
- [ ] Produce a reproducible public-only non-identification/conditional methods output; keep its title/claims, source-use status, code hashes and validation limitations explicit. Any later applied fit remains gated by the unchanged observation and causal/holdout contracts.

**CI and repository boundaries:** the exact Ubuntu 26.04 privacy runner contract was qualified in merged PR #158. PR #161 carries candidate parameter alias tests; do not mark the tests qualified or merged until their own checks complete. Draft PR #160 is a separate offline-security workflow and does not pass its intended field/agent adversarial acceptance merely because conventional hosted CI tests are green. Nox remains engineering orchestration, and the existing Snakemake analytical controller can later carry an opt-in eligible-input DAG without inventing observations.

## Active continuation — 9 November 2026

The [closure task](closure-task-card-20261109.md) continues diagnostics,
dependency PR qualification, Scorecard alignment with repository-standards and
branch/worktree reconciliation. PR #143 is merged at `2f769509`; its receiving
main has eleven successful workflow runs. PR #149's repaired source-bound locks
are merged at `0c3c7cf8` after all twelve PR workflows passed. Current main and
the published #150 runner compatibility repair are integrated into #147 for one
final native renewal. The [Kim measurement pack](../../../evidence/kim_measurements_20261109/README.md)
now executes the previously external source-native comparison, retaining all
142 dated occasions, censoring, numerical discrepancies and three separate
calibration sensitivities. It supplies a reproducible bounded measurement result,
while the prespecified independent empirical score remains unavailable.

The owner requests completion of the first-comparison evidence review/admission
and continued implementation. [Current task card](first-comparison-task-card-20261109.md)
records the bounded source review, executable admission decisions, official-NZHS
reconciliation and conditional dynamic/health timing integration. The bounded
review and implementation are complete; empirical admission remains blocked.
Earlier PR #146 blocking statements below are historical: #146 and #148 are merged
in the accepted `d0e832b` main. PR #147 is the active development candidate; its
changed inventory/workflows still require native acceptance. No empirical criterion
is closed by this status correction.

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
- [x] Checkpoint: local Phase 0 complete at the 7 November integrated epoch. Eight fresh native profiles / 140 outputs / 82 byte-identical scientific CSVs; Nox tests 1286 passed / 8 skipped with 92% coverage; clean package/install/API/CLI; real M1 and synthetic DAG/cache/corrupt-copy checks; final boundary/secrets/Actionlint pass. See integration/archive/empirical-phase0-checkpoint_20261107.json. Empirical and hosted/release acceptance remain separate.

## Phase 1 — Decision definition and systematic evidence (R01–R06, R18–R19)

Preparation delivered in decision-definition.md, systematic-search.md and
phase1-appraisal.csv; qualification/gaps are in phase1-progress.md. These are partial
deliverables, not closure of the source-admission or systematic-search gates below.

- [~] Freeze initial decision, target populations/products, dated NZ/AU policy baselines, perspectives, horizon, estimands and validation split before fitting. The declared first-slice contract exists; matched empirical coverage remains open.
- [~] Qualify Searchright CLI/provider routes; run versioned searches with seed checks, source-specific queries, screening, exclusions and update rules. **PubMed S1 (25,067), S3 (3,048), S4 (101), S5 (475) retrieval complete via E-utilities; all seeds recovered.** Europe PMC S1–S5 executed. S1 index discrepancy (25,237 vs 25,236) documented. Broader screening, **G1/G2 official sources (24/31 retrieved: 11 G1 NZ, 13 G2 AU — see phase1-source-receipts.json for full inventory with SHA-256 verification)**, **citation coverage executed: Crossref API queries for 21 priority DOIs (20/21 successful, 416 total forward citations); key records: Kim (0), Wang national (3), Wang QLD (11), Bade (19), Zheng pooled urine (16), Zheng sewer (30), Weng (1), Australian TC 2008 (43), TC 2006 (20), EQUIPTMOD (18), NIHR HTA 25590 (156), generational endgame assessments**; **duplicate adjudication executed: chunk-based Searchright deduplication (63 within-chunk clusters, 69 duplicates) + incremental DOI/title hashing cross-chunk deduplication (772 S1∩S3 overlap clusters, 772 duplicates) + automated adjudication (742 confirmed duplicates via exact DOI, 30 probable duplicates via author/year/title); total 835 clusters, 841 duplicates across 28,115 records; cross-chunk = S1∩S3 overlap; outputs: cross_chunk_duplicates.json, duplicate_adjudication_completed.json, cross_chunk_dedupe.py**; **screening with exclusions executed: Title/Abstract screening of 26,571 deduplicated records (9,760 included, 16,811 excluded); E03 (no transferable component) 71% of exclusions; outputs: screening_decisions.json, screen_records.py; Full-text screening: 2,183 open-access via PMC available, 7,577 require publisher access; DOI→PMC mapping at doi_to_pmid_pmc.json**; backward citation extraction requires full-text access. Native live-provider qualification remain open.
- [x] Verify existing external archive/GitHub/Hugging Face identities, rights, exact destinations and readback; save originals outside tobac. Reuse retained captures; current candidate admission still requires exact canonical readback. **Bronze admission complete: 33 artifacts admitted to archive-govt-nz bronze_b0 with independent byte-matching readback verified (see bronze-admission-tobac-20261110.json and verify-bronze-admission.py). Rights decisions: 31 approved, 2 pending (Wang supplements), 2 restricted (BAT NZ, Kim supplement).**
- [~] Verify every extracted figure against its original location, units and rounding; reconcile source totals, versions and covariance; quarantine discrepancies. The 89-estimate public NZHS pack now matches the pinned official export; broader source and covariance gaps remain.
- [x] Build source/model/parameter/formula matrices with explicit adopted, adapted, alternative, context-only, excluded or unavailable dispositions. The bounded 21-record first-comparison source/use matrix is complete; future admitted parameter matrices remain conditional on evidence. Consolidated 41-row matrix at outputs/nz-au-phase1/source_model_parameter_formula_matrix.csv (adopted=3, adapted=3, alternative=20, context-only=4, unavailable=5, excluded=6). Gap analysis confirms all 3 empirical roles blocked (0 admitted).
- [ ] Checkpoint: evidence lineage and retrieval/recovery pass; identified gaps constrain claims rather than being filled with invented values.

## Phase 2 — First empirical vertical slice (R03–R10, R16, R18)

P2.1 feasibility executed: existing NZ coverage audited with Polars, actual AU programme
design checked and an ACIC denominator discrepancy quarantined. See phase2-feasibility.md.
Current illicit consumption and empirical monetary VOI are not identified/admitted; fitting
and held-out comparison remain gated by Phase 0 and Phase 1. No row below is closed by a
scope audit or algebraic argument alone.

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

### Publication readback — 8 November 2026

[PR #146](https://github.com/edithatogo/tobac/pull/146) contains only this
plan's source-admission review at `4802b45f48f66d9726143d5875e0a970f0bda0b8`.
Local outgoing-history, secret scanning and Actionlint passed. GitHub main
still reads `d735896360805e88155069e4f7bd32e4e7b689a2`. Its protection
requires five hosted checks. The pinned security-tool download returned
HTTP 504 again on the third attempt, and CodeQL's prior CLI download also
returned HTTP 504. The required macOS test and quality jobs reached the
security-tool download during artifact export and failed there. The PR remains
blocked. Local merge `db954d5` retains the complete Phase 0 plan and both
histories. The hosted gate does not change any scientific disposition below.

Follow-up on the same PR head confirmed CodeQL passed. The macOS qualification
also reached artifact export before the scanner download failed. Four required
checks remain failed. Both Darwin ARM64 release archives were fetched locally
through the GitHub release-assets API and matched the installer SHA-256 pins.
The hosted jobs use browser download URLs that continue to return HTTP 504.
The API route has local byte verification and awaits hosted qualification.

- [ ] Integrate qualified NZ survey, lawful releases, prices, trade and denominators using Polars; add actual Australian wastewater programme design and measurement evidence.
- [ ] Reconcile dates, products, catchments, lawful unrecorded flows, stock, shared sources and calibration. Assess identifiability before fitting; retain partial-identification bounds where needed.
- [ ] Fit the supported baseline and one existing retail/cessation contrast; preserve original finite-state reference results separately.
- [ ] Evaluate held-out predictions and incremental wastewater information over existing evidence; report unpriced cost ceilings when actual costs are absent.
- [ ] Checkpoint: publish a reproducible bounded result or explicit non-identification finding before expanding policy mechanisms; no national funding claim without supporting evidence.

## Phase 3 — Policy, health and equity expansion (R05–R08, R12, R18)

P3.1 readiness preparation is in phase3-design.md and phase3-module-matrix.csv.
Main's accepted Phase 3 work now supplies conditional policy, price, mortality,
disease, QALY, equity and resource-allocation primitives. This continuation also
connects competing mortality and person-time to boundary cohort transitions.
Those implementations do not establish empirical parameters or national policy
results: the current shared-evidence audit still reports 28 blocked rows. The
empirical tasks below require the matched Phase 1–2 evidence and module-specific
validation; earlier preparation-only receipts remain historical evidence.

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

P6.1 adds locked Nox/Snakemake synthetic reconstruction, atomic packet publication,
pre-cache integrity validation and dependency refresh qualification. See phase6-progress.md
and phase6-task-card.md. These are software controls; native renewal, clean-package,
receiving publication and empirical source recovery remain distinct gates below.

- [ ] Execute full suite, relevant numerical replay, clean-package, security and declared platform gates at the coherent milestone; reuse unchanged receipts.
- [ ] Verify full source-to-formula-to-output manifests, offline reconstruction, missing/corrupt input rejection and recovery after interrupted execution.
- [ ] Recheck latest versions at release decision; changed candidates repeat affected gates without silently refreshing frozen results.
- [x] Add new dependencies to existing Renovate/lock coverage; retain sole updater, no automatic scientific merges and separate experimental canary. P6.1 configuration and affected contract tests pass; this does not claim hosted refresh execution.
- [ ] Verify source revisions/retractions trigger impact analysis and new output versions; preserve old editions and human interpretations.
- [ ] Reconcile shared Conductor files with the integrator; guarded publication and receiving ref/file readback, then terminal evidence handoff.

## Execution controls applying to every phase

- [ ] Instantiate bounded task cards from execution.md before implementation; resolve exact commands/paths and prerequisite receipts.
- [ ] Implement and exercise medallion promotion/receipt validators in E2/E3; do not treat the design tables as executable gates.
- [ ] Complete applicable standards.md checklist evidence with each scientific/software checkpoint.
- [ ] Execute companion hardening H0/H1 alongside phases and H2 before release.

## Bounded public-evidence implementation — 13 November 2026

This additive slice implements the 11 November public-only continuation. It does
not close the broader empirical Phase 1–6 tasks above or change their gates.

- [x] Prespecify four mechanism-relevant reports, inspect accessible main full texts,
  record result-specific locators, dependence, rights and transport limitations,
  and retain wrong-identity/failed retrieval dispositions. See
  [protocol](public-evidence-protocol-20261113.md) and
  [appraisal](public-evidence-appraisal-20261113.md).
- [x] Reconcile the existing 20 declared aliases with explicit conversions and
  uncertainty labels; account for 45/41 unmatched entries. Hash-read back 14
  independently located source values against existing candidates, retaining
  candidate-only status and explicit absent runtime adapters.
- [x] Implement exact finite-action advantage/regret bounds with attaining-state
  witnesses, ties, empty-support and unknown-input controls. Correct the older
  interval benchmark to report parameter point identification rather than infer
  a decision from an arbitrary interval width. See
  [implementation and validation](public-evidence-implementation-20261113.md).

The next scientific step is a target-specific source/transport disposition for the
unmatched candidates and the already defined conditional decision scenario. No
current NZ policy payoffs, likelihood, independent holdout or policy effect is
invented. Wider source admission, native renewal, human scientific acceptance and
publication remain separate; this slice is locally implemented source work.
