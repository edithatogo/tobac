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
Track: `conductor/archive/longitudinal_integration_20261024/` (archived after incorporation).
Evidence: `docs/empirical_longitudinal/INTEGRATION.md`, `integration/longitudinal_local_verification.json`,
`integration/longitudinal_publication.json`, `integration/m2b_review_20261025.json`,
`results/longitudinal/`.

Imported the previously tested v2.8 reported-release and v2.9 historical consumption/supply
modules under the `tobac_supply` namespace, with sources, config, reproduction commands, 151
imported tests and compact results. Generated files matched the predecessor archive 42-of-43
exactly, with the remaining diagnostic within 2.45e-15.

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
closes the previous "no hosted pass" gate but not scientific validity. Still open:
`strict_all`; the 2021/2022 documented windows overlap by 62 and 31 days without a
cross-period covariance; `SupplyBasis` carries no source IDs or observation dates; and the
archived 42-of-43 predecessor comparison and 499 full-suite count remain unverifiable local
claims. CI now diffs regenerated tables against `results/longitudinal/` (`56322e4`), which
closes the previously listed regeneration-drift gap.

Scope boundary: historical observed-summary components only. The release series and historical
ratio are separate estimands, not a fused current NZ exposure/origin posterior. No current joint
WBE/origin/causal/funding posterior, measured inventory or agency approval is claimed.

## Cross-workstream synchronisation and regression contracts — 24 October 2026
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
status belong to the receipt on issue #1.

## Open empirical and execution work
1. Agree a prospective decision contrast and actual baseline retailer/catchment scope; the historical cap was not implemented.
2. Qualify the semantic connection from the incorporated `tobac_supply` component to `tobac.evidence`; source receipt is distinct from valid regulatory-prior conditioning.
3. Assemble matched existing field and supply observations with stock/unrecorded supply, dated units, covariance and provenance; distinguish forecasts from evidence and condition D0 once.
4. Qualify the transport of net cessation, legal-to-illicit switching, mitigation and lawful replacement with empirical data or documented elicitation.
5. Identify incremental criminal harms separately from participation, revenue and fiscal transfers; retain null-effect scenarios.
6. Validate near-limit anabasine performance, residual/serial dependence and prospective causal counterfactuals. Improve continuous support and held-out field prediction.
7. Agree Maori governance/permissible use, equitable coverage and actual incremental programme costs.
8. Resolve issue #4's hosted execution failures without weakening gates. Execute genuine Sourceright/CiteWeft/voiage and record precise scope. Current numerical parity is internal reference parity, not third-party qualification.

Source code review and tests are local; independent scientific review and external agency approval remain unclaimed. Update this registry and the issue comments with receiving commits and actual run outcomes.

### Engineering gates that are open, not passing
`quality` is green — ruff `E9,F63,F7,F82`, ruff under `engineering/ruff.toml` on
`scripts/context_bundle.py`, and basedpyright under `engineering/basedpyright.json`. It does
**not** include `engineering/bp_longitudinal.json`: that strict check was briefly wired into
`quality`, could never pass (pandas ships no `py.typed` stubs), and now runs only as the
separate `types_longitudinal` session below. Any earlier statement that `quality` covers
`bp_longitudinal.json` is superseded. These gates are measured and still failing, and must
not be read as passing:

- `strict_all`: 4,168 ruff `--select ALL` errors (2,281 fixable) and 3,584 basedpyright
  errors across the whole source tree, measured 25 October 2026. The release workflow runs
  this session before packaging, so packaging is blocked on it. No count has been reduced
  since; re-measure before quoting. Both counts are pin/host dependent and were superseded on
  26 October 2026 by a macOS measurement on the Python 3.15 target: 4,861 ruff and 2,456
  basedpyright (issue #1 comment `6406854120`). The earlier basedpyright figure was taken on a
  stale 3.12 target, so cross-version figure comparisons are not valid.
- `types_longitudinal`: the strict check on `scripts/run_empirical_longitudinal.py`
  (`engineering/bp_longitudinal.json`) is **expected to fail** with 133 errors that are all the
  pandas-stub `reportUnknown*` cascade (0 `reportMissingImports`, 0 `reportArgumentType`,
  0 `reportAssignmentType`). It was briefly wired into `quality` and made that session
  unachievable; it is now a separate session and is not part of `quality`. Closing it needs
  `pandas-stubs` in `engineering/audit.lock`, a reviewed lock regeneration and a receipt.
- mutation: 49 of 128 mutants survive on `src/tobac/supply.py` (61.7%). A 60% floor now
  fails the session on regression, which is a guard, not evidence of adequate coverage.
- profile (Scalene): session now succeeds, but the measurement establishes almost nothing about
  where solver cost is, so it is **not** a closed gate. Executed 26 October 2026 at `a7d0e8d`
  via `nox -s profile`; artifact `outputs/engineering/scalene.json` (CPU-only, 8.5 MB, valid
  JSON). On the reduced 512-draw run: `import pandas` and `import numpy` are the two most
  expensive lines (~4.4–8.3% each), above the 4.1–4.8% attributed to the whole `plots()`
  function; ~16–20% of samples are in C extensions a Python profiler reports only as one opaque
  number; and the only attributed files are the runner script plus `<exec@_internal.py:64>`.
  Two runs at the same commit agreeing on the *ranking* still disagreed on magnitude
  (`plots()` 4.83% then 4.13%; `import pandas` 8.30% then 4.41%) and even on which functions
  received samples, so the per-line percentages are not a stable basis for a claim at this
  duration. Start-up dominates, the run is reduced, and nothing here profiles the full-draw run
  or the test suite. Profiling the 8,192-draw run and profiling unit-test hotspots both remain
  open.
- The official Actions transitive lock and the hosted all-legs matrix remain open; the
  hosted run quoted above covers one CI invocation, not every OS/Python leg.

## Library reuse and qualified engineering harness — 24 October 2026
**Status: [~] locks promoted and locked-mode tests/replay/packaging green at 5ab361b; hosted matrix confirmation, strict_all, profiling and independent review remain open.**
Track: `conductor/tracks/engineering_hardening_20261024/`.
Review: `docs/engineering/LIBRARY_REUSE_REVIEW.md`; use/status: `docs/engineering/READINESS.md`.
Receipt: `integration/engineering_verification.json`; execution receipts:
`integration/engineering_hardening_execution_20261025.json` and
`integration/engineering_hardening_gap_closure_20261025.json`.

The Gaussian reporting density delegates to SciPy while physical/state/data contracts stay
unchanged. New Nox/uv, schema-validated context profiles, secure bounded CI/deep/canary lanes,
Renovate/pre-commit configuration and pinned Conductor gitlink are explicit engineering layers.
`uv pip sync --require-hashes` now drives `tests` (495 passed at the 25 October 2026 locked pass;
618 passed / 2 skipped at the 26 October 2026 `review/m2b-longitudinal` head, `c8b070f`, which is
a different tree — do not compare the two), `reproduce` (five
replays verified) and `package`, and the built wheel installs and imports. Mutation is executed
and weak (61.7% killed); `strict_all` is measured (4,168 ruff and 3,584 BasedPyright at the
original measurement; 4,861 and 2,456 at the 26 October 2026 macOS/Python 3.15 re-measurement) and
is not green. The Windows leg failure was a CRLF checkout defect now fixed by `.gitattributes`.
Do not turn configuration or a checksum into a claim of successful execution or scientific
validity; hosted confirmation and independent review are not obtained.

## Source-bound dependency and execution qualification — 24 October 2026
**Status: implemented at 886fc08; genuine locks and external qualification remain open.**
Track: `conductor/tracks/engineering_execution_20261024/`.
Receipt: `integration/engineering_followthrough.json`; current instructions: `docs/engineering/READINESS.md`.
This links the already published source-bound locks, portable/audit environment separation,
read-only hosted diagnostic and strict internal release gates; it is not new execution evidence.

## Prior-work evidence preservation and incorporation audit — 25 October 2026
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
**Status: conditional numerical implementation complete; actual Voiage and hosted qualification remain open.**
Track: `conductor/tracks/research_m3_20261025/`.
Contract: `docs/research/M3_CONTRACT.md`; results: `results/milestone3/report.md`.
Receipt: `integration/m3_local_verification.json`; six-item status: `integration/m3_requirement_status.csv`.

The additive `src/tobac/research` package implements weighted expected-value adaptation,
structure-only EVPPI, complementary/dependent reports, shared assets, existing-data guards,
unweighted scenario envelopes, state-action implementation and matched pilot/continue/stop.
162 scoped tests and 2,105 full-run invariants passed; this is not the entire live suite.
The mathematical weighted adapter is tested but the real Voiage 2.2.0 probe remains blocked.
Innovate/Kairos are optional; uptake/delay materiality is demonstrated with declared scenarios,
not fitted external outputs. Full/refinement tables and manifests are preserved as 24 files
in a hashed bounded archive with an unpacker. Existing source/evidence/engineering files are
preserved from base 5218d831. Nox and the separate genuine-library CI lane remain fail-closed;
configuration is not successful execution. Receiving commit and hosted outcomes: issue #1/#4.


## Executable integration of preserved evidence — 25 October 2026
**Status: shared preflight and all-collection validation wired; external/hosted qualification remains open.**
Track: `conductor/tracks/evidence_execution_20261025/`.
Guide: `docs/EVIDENCE_INTEGRATION.md`; local receipts: `integration/evidence_inventory_20261025.json`
and `integration/evidence_execution_verification_20261025.json`.

The existing integration CLI now calls the preserved-byte verifier and inventories all four
current bibliography collections. Nox tests/reproduction/packaging and the scientific workflows
run the preflight. The genuine Sourceright route covers every collection, retaining all failures;
its availability and scientific applicability are not inferred from an inventory pass.
The 51-case equal-weight voiage probe now rejects nonfinite external values. M3-owned interfaces,
models, priors, input data, reference records and published results are unchanged. No current
empirical posterior, quote, full scientific replay or independent review is claimed by this pass.

M3 arrived concurrently at fa39fd36 and is preserved. The evidence gate also covers its
research_m3 Nox session; shared reproduction now includes the M3 runner once. These command
contracts were locally retested; the M3 numerical results were not re-estimated in this pass.
## Advisory CI/CD, automation, quality and security lane — 25 October 2026
**Status: track created; not implemented; hosted execution and entitlements open.**
Track: `conductor/tracks/cicd_hardening_20261025/`.

A bleeding-edge tooling lane is specified beside the frozen reference lane: setup-uv/uv,
ruff-action, ty, pyrefly, basedpyright, j178/prek, gitleaks, harden-runner, zizmor-action,
gh-action-pip-audit, attest-build-provenance and an ubuntu-24.04-arm diagnostic leg. Every
lane job is non-required and report-only. The reference NumPy/SciPy pins, engineering locks
and receipts, `strict_all` counts and all existing required Nox sessions are unchanged.
`strict_all` remains measured-not-fixed (4,168 ruff and 3,584 basedpyright-all at the original
measurement; 4,861 and 2,456 at the 26 October 2026 macOS/Python 3.15 re-measurement), so no
lane result is a gate. Attestation entitlements, runner-level egress blocking, arm64
qualification and all hosted jobs remain open. Configuration is not execution.

---

## Scientific ecosystem modernisation — 25 October 2026
**Status: approved planning registered; implementation not authorised.**
Track: `conductor/tracks/scientific_ecosystem_20261025/`.
GitHub: https://github.com/edithatogo/tobac/issues/22

Approved Conductor registration only; implementation not authorised. Reuses
existing CI/archive and upstream contracts. No runtime or scientific
qualification claimed.
