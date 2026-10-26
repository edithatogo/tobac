# Research tracks

## M1 — Regulatory uncertainty before procurement
**Status: computational screening complete; empirical qualification open.**
The primary order is EVPI, grouped EVPPI, targeted scientific learning, EVSI, then conditional ENBS. No political/funding conclusion is a required test outcome. The original 4,096-state scenarios and published result CSVs are preserved. See `results/milestone1/report.md`, `docs/protocol.md` and `integration/baseline.json`.

## M2a — Evidence boundary and source-informed retail contrast
**Status: locally implemented and exercised; not an empirical commissioning result.**
Plan: `docs/plans/2026-10-24-m2-evidence-and-retail.md`. Contracts: `docs/m2_retail_contract.md` and `docs/evidence_interface.md`. Results: `results/milestone2/`. Local execution receipt: `integration/m2_local_verification.json`.

Implemented: observed-evidence identity/scope guards; finite posterior update; duplicate/forecast rejection; joint reporting-error supply bridge; published net-cessation structural alternative with null/transport cases; lawful replacement sensitivity; matched total/lawful causal report; exact incremental-information identities; config-domain checks; source-effect grid refinement; additive CI steps. Source parameter extraction is manually checked, not independently human-reviewed or approved by a citation tool.

## M2b empirical longitudinal source integration
**Status: incorporated on main, reviewed and hosted-executed; current-NZ empirical qualification open.**
Track: `conductor/archive/longitudinal_integration_20261024/`. Review receipt:
`integration/m2b_review_20261025.json`. Results: `results/longitudinal/`.

A post-archive review found that the imported 151 component tests could not fail on the
scientific core: deleting the `prior_kernel` slope term, removing the trapezoid prior edge
weights, stubbing `boundary_mass`, swapping the `time_bridge` process/slope split and
changing the 365-day stock convention all left the suite green. PR #11 (merged at
`903ca35`) added independent numerical oracles, made configuration validation and both run
verifiers fail closed, required an explicit audited `basis` for `lawful_ledger`, and
corrected several docs/receipt claims that outran their retained evidence. The suite went
from 500 to 582 tests. No scientific input, prior, likelihood, configuration value or
published result changed: the hosted artefacts reproduce `source_audit.json`,
`forecast_summary.csv` and `predictive_scores.csv` byte-identically and
`latent_ratio_summary.csv` to about 4e-13 relative.

The current longitudinal workflow revision has now executed successfully on `main`
(run 40180241081: 582 tests passed, both runners, both verifiers, all steps success). That
closes the previous "no hosted pass" gate but not scientific validity. Later engineering qualification closed `strict_all`, and PR #30 added validated
`SupplyBasis.source_ids` and `observation_years`. CI now checks regenerated longitudinal
tables. Still open: the 2021/2022 documented windows overlap by 62 and 31 days without
a cross-period covariance; scientific source-to-target conditioning; and the archived
42-of-43 predecessor comparison and 499 full-suite count remain unverifiable local claims.

## Cross-workstream synchronisation and regression contracts
**Status: cross-interface regression checks complete; scientific conditioning remains open.**
Guide: `docs/WORKSTREAM_SYNC.md`. Contributor instructions: `AGENTS.md`.
Track: `conductor/tracks/workstream_sync_20261024/`. Receipt: `integration/workstream_sync_verification.json`.

Added 26 tests exercising both real namespaces together, including the accounting sign
translation, dated-period allocation, shared physical-state IDs, once-only underlying-data
conditioning, correlated reporting errors and prospective information identities. These and
151 imported tests passed (177 total) at the pass date of 2026-10-24; the supply_bridge
suite has since grown through the M2b review, release-diagnostic and CI-gate additions
(262 collected at main `75871f1`), so reproduce the count before relying on the older
figure. Two deliberate integration mutations were detected; original sources were restored
and hash-verified, with the restored blob hashes now recorded in the receipt. A follow-up
review (25 October 2026) confirmed the suite remains sensitive to seven further mutation
probes and that every receipt hash still reproduces: `integration/workstream_sync_review_20261025.json`.
No scientific source, policy equation, prior or published result was changed. The entire
regulatory suite was not freshly rerun in this bounded check. Branch/readback and hosted
status belong to the retained execution receipt.

## Open empirical and execution work
1. Agree a prospective decision contrast and actual baseline retailer/catchment scope; the historical cap was not implemented.
2. Qualify the semantic connection from the incorporated `tobac_supply` component to `tobac.evidence`; source receipt is distinct from valid regulatory-prior conditioning.
3. Assemble matched existing field and supply observations with stock/unrecorded supply, dated units, covariance and provenance; distinguish forecasts from evidence and condition D0 once.
4. Qualify the transport of net cessation, legal-to-illicit switching, mitigation and lawful replacement with empirical data or documented elicitation.
5. Identify incremental criminal harms separately from participation, revenue and fiscal transfers; retain null-effect scenarios.
6. Validate near-limit anabasine performance, residual/serial dependence and prospective causal counterfactuals. Improve continuous support and held-out field prediction.
7. Agree Maori governance/permissible use, equitable coverage and actual incremental programme costs.
8. Complete remaining external-tool/source-applicability qualification, including CiteWeft. The macOS engineering, Sourceright and bounded installed-Voiage execution checks now pass; those software receipts do not establish empirical or third-party scientific validity.

Local and hosted software checks are recorded separately from independent scientific endorsement and external agency approval, which remain unclaimed. Receiving commits and actual run outcomes belong in Conductor and their execution receipts.

## Library reuse and qualified engineering harness
**Status: [x] Complete for macOS Python 3.15.1 — 26 October 2026.**
Track: `conductor/tracks/engineering_hardening_20261024/`.
Current acceptance: `integration/engineering_macos_completion_20261026.json`.
Guide: `docs/engineering/READINESS.md`; policy: `docs/engineering/LINT_POLICY.md`.

The inspected base `f11d491` passed 745 tests with four optional-environment skips
and 93% coverage; all macOS engineering sessions pass. Whole-source strict typing
and configured Ruff pass. Hosted mutation detects 100/131 (76.3%); 31 survivors and
175 documented style/API exceptions remain explicit non-blocking follow-ups.
Voiage's bounded installed-library compatibility and native Dependency Graph repair
are qualified in their separate receipts. Full-SHA Actions pinning is retained;
the rejected generated tag-based lock proposal is closed by the owner's decision.
Historical receipts remain intact. Other platforms and advisory work stay in the roadmap.

## Source-bound dependency and execution qualification
**Status: [x] Complete for the macOS scope; non-macOS qualification remains deferred.**
Track: `conductor/tracks/engineering_execution_20261024/`.
Acceptance: `integration/engineering_macos_completion_20261026.json`; earlier lock and
execution receipts remain dated evidence. Runtime/Voiage locks are input-bound and
hash-installed; native macOS audit-tool qualification is distinct from Linux audit
lock execution. No external scientific or empirical validity is inferred.

## Prior-work evidence preservation and incorporation audit
**Status: selected reference snapshot verified; full archive migration and live empirical use are not claimed.**
Track: `conductor/tracks/incorporation_audit_20261025/`.
Index: `docs/INCORPORATION_STATUS.md`; manifest: `integration/prior_work_manifest.json`.
Receipt: `integration/incorporation_verification_20261025.json`.

Preserves 19 previously archive-only evidence/template files: 298 mixed-purpose CSV rows and
28 inherited reference records. Twenty-one scoped preservation tests and the source-archive
comparison passed at the receiving commit `5218d83` (the predecessor ZIP itself is not
retained in this repository, so that comparison is an executed-at-the-time claim, not a
reproducible gate — see the receipt). The uploaded snapshot tree matched the tested local
subtree at `5218d83`; `references.csl.json` was since DOI-case-canonicalised at `090d07c`
with the transform declared at `193f6bb`. A review on 26 October 2026 re-confirmed the
payload and the 21-test suite and anchored the row/bibliography totals in the tests
(receipt: `integration/incorporation_audit_review_20261026.json`). Current code, model
inputs/results, dependencies and gates were unchanged by that audit. No copied assumption
becomes a calibrated parameter, forecast a new observation, template a quotation, or old
manuscript submission-ready. M3 incorporation now follows below.

## M3 research portfolios, implementation and staged decisions
**Status: conditional numerical implementation and bounded installed Voiage/macOS hosted qualification pass; empirical qualification remains open.**
Track: `conductor/tracks/research_m3_20261025/`.
Contract: `docs/research/M3_CONTRACT.md`; results: `results/milestone3/report.md`.
Receipt: `integration/m3_local_verification.json`; six-item status: `integration/m3_requirement_status.csv`.

The additive `src/tobac/research` package implements weighted expected-value adaptation,
structure-only EVPPI, complementary/dependent reports, shared assets, existing-data guards,
unweighted scenario envelopes, state-action implementation and matched pilot/continue/stop.
162 scoped tests and 2,105 full-run invariants passed; this is not the entire live suite.
The real source-built Voiage `2.2.0+tobac3151.1` adapter now passes local weighted/partition
and equal-weight probes on Python 3.15.1. All 15 PR #33 checks passed; merged at `f06eed6`;
see `docs/engineering/VOIAGE_PYTHON315.md`. This does not qualify generic EVSI or structural APIs.
Innovate/Kairos are optional; uptake/delay materiality is demonstrated with declared scenarios,
not fitted external outputs. Full/refinement tables and manifests are preserved as 24 files
in a hashed bounded archive with an unpacker. Existing source/evidence/engineering files are
preserved from base 5218d831. Nox and the separate genuine-library CI lane remain fail-closed;
configuration is not successful execution. Receiving commit and hosted outcomes are recorded in
the local Conductor track and execution receipts.


## Executable integration of preserved evidence
**Status: shared preflight and all-collection validation hosted-executed; scientific/source applicability remains open.**
Track: `conductor/tracks/evidence_execution_20261025/`.
Guide: `docs/EVIDENCE_INTEGRATION.md`; local receipts: `integration/evidence_inventory_20261025.json`
and `integration/evidence_execution_verification_20261025.json`.

The existing integration CLI now calls the preserved-byte verifier and inventories all four
current bibliography collections. Nox tests/reproduction/packaging and the scientific workflows
run the preflight. The genuine Sourceright route covers every collection, retaining all failures;
its availability and scientific applicability are not inferred from an inventory pass.
The 51-case equal-weight voiage probe now rejects nonfinite external values. M3-owned interfaces,
models, priors, input data, reference records and published results are unchanged. No current
empirical posterior, quote, full scientific replay or third-party validation is claimed by this pass.

M3 arrived concurrently at fa39fd36 and is preserved. The evidence gate also covers its
research_m3 Nox session; shared reproduction now includes the M3 runner once. These command
contracts were locally retested; the M3 numerical results were not re-estimated in this pass.

## Reconciled engineering verification — 26 October 2026

PR #25 and the Python 3.15.1 migration were reconciled through PR #29, merged at `104729a`.
The focused runner and whole-source strict checks use qualified stubs and the calling session
interpreter. Both hosted macOS jobs passed at final PR head `1f6b375`; the receiving commit and
execution details are in `integration/engineering_reconciliation_20261026.json`. Voiage compatibility follow-up: the metadata-only source build passes locally and hosted;
see `integration/voiage_python315_compatibility_20261026.json` for current hosted status. Independent review is optional; current
development and hosted qualification target macOS.

## Scientific ecosystem modernisation — 25 October 2026
**Status: approved planning registered; implementation not authorised.**
Track: `conductor/tracks/scientific_ecosystem_20261025/`.
GitHub: https://github.com/edithatogo/tobac/issues/22

Approved Conductor registration only; implementation not authorised. Reuses
existing CI/archive and upstream contracts. No runtime or scientific
qualification claimed.

## Native Dependency Graph repair — 26 October 2026

PR #35 merged at `666dd8c` after all 15 PR checks passed. Managed graph run
`40275206942` passed; native SBOM readback grew from 27 to 42 package identifiers
without losing any existing entry. Python remains 3.15.1, all dependency pins are
unchanged, and security settings/checks are preserved. Receipt:
`integration/dependency_graph_20261026.json`; guide: `docs/engineering/DEPENDENCY_GRAPH.md`.

## Archival source integration — 25 October 2026
**Status: consumer bindings reconciled; bounded consumer handoff hosted-qualified; scientific applicability open.**
Track: `conductor/tracks/archive_sources_20261025/`.
Guide: `docs/ARCHIVAL_SOURCES.md`; immutable snapshot bindings: `integration/archive/`.
Maps 43 CSL records and 18 CSV files (326 rows) into archive-govt-nz. Preserves source
aliases, dependency groups, assumptions and extracted values. Original source bytes,
metadata-only records, HTTP challenge pages and retrieval failures are distinct. No
new likelihood, posterior or independent scientific qualification is claimed.

The bounded source-to-observation report covers 28 rows and preserves shared-data, derived-role,
scope, capture, product and model gaps. Guide: `docs/SOURCE_OBSERVATION_HANDOFF.md`.
No likelihood, posterior or current-NZ empirical qualification is inferred.

PR #21 merged at `cf8295b5c1b649685ba78f4977ec7f1b5883d1a8` after all 15 checks passed.
Receipt: `integration/archive/handoff-verification_20261026.json`.

### MOH workbook pathway — 26 October 2026

Native source verification re-executed: retained CAS/WARC fixity, payload/request identity,
and all 16 workbook/consumer values pass. The dated report closes local source/value gaps
for those rows and records the supported 2025 national retail-release Scope. Original capture
time, historical definitions, aggregate duty-free/product coverage, conversion, calibrated
measurement/covariance and the target catchment/transport remain open. No prior is updated.
Guide: `docs/MOH_OBSERVATION_PATHWAY.md`; specification and execution receipts are under
`integration/archive/moh-*`. Companion archive PR #776 publication/recovery remains separate.

MOH follow-up PR #40 merged at `160c0a5c53e440d9345ad51efc7dca2a7611bf6c` after 15/15 hosted checks passed.
Receipt: `integration/archive/moh-pathway-verification_20261026.json`.

### 2025 product-level return reconciliation

Nine source assets for eight listed issuers are captured and locally verified. The 28-row
consumer table preserves domestic/duty-free/unspecified channels, signed corrections and
separate ingredient/additive/sales measures. Source year and packet/carton conflicts prevent
national closure; missing channel quantities and RYO conversion remain unqualified.
Guide: `docs/2025_PRODUCT_RECONCILIATION.md`; report: `integration/reconciliation_2025/generated/`.
