# Implementation plan — 8 November 2026

## Scope and acceptance

Make actionable engineering fixes, supply available public comparison data, add a
small dynamic reference, and specify the path to empirically supported dynamic
decisions. Preserve accepted M1/M2/M3 and longitudinal results and the shared
evidence contract. A public source table, a prototype and a passed software test
establish different kinds of evidence; none is a fitted current NZ policy model.

The implementation starts from main `d735896360805e88155069e4f7bd32e4e7b689a2`.
Changed `src`, `data` or `evidence` membership invalidates the accepted scientific
inventory. New native execution and signed qualification must precede acceptance.
No old receipt or signature is rewritten to represent this candidate as verified.

## F00 — engineering and status fixes

- [x] Reconcile README/runtime assertions and readiness text to accepted Python
  3.15.2; distinguish dated receipts and the new candidate.
- [x] Replace README links to intentionally local-only authoring documents with
  public numerical outputs and a clear publication-boundary reference.
- [x] Add bounded retries and a connection timeout for transient scanner download
  failures; preserve fixed versions, archive checksums and fail-closed extraction.
- [x] Complete local source-security and publication checks on the candidate.
- [ ] Complete native scientific admission and hosted qualification.

## F01 — public data candidate

- [x] Extract all six ABS tables from the exact downloaded HTML: 193 records,
  including five 37-quarter series and one eight-year series.
- [x] Transcribe 18 current NZHS prevalence values and two estimated counts from
  official published text. Record that the original HTTP bytes were not obtained.
- [x] Supply 69 additional published estimates with 95% intervals and daily-use
  union values from linked PHCC reporting of the same NZHS. Preserve dependence,
  source-specific attribution, two sampling-error flags and original-capture gaps.
- [x] Record source dates, population, units, dependence, licences, source/extract
  hashes where available, uncertainty gaps and `empirical_admission: false`.
- [x] Supply a reproducible ABS extractor and focused data checks.
- [ ] Transfer the ABS original to the canonical external archive and verify
  destination bytes. Obtain and independently check the NZHS original snapshot.
- [ ] Complete survey covariance/state-partition evidence and matched catchment/date flow,
  population, censoring, processing and calibration. Record explicit failures and
  unresolved fields rather than imputing undocumented observations.
- [ ] Admit any usable observations through the parent evidence contract and
  renew native lineage. Keep source-derived comparisons separate from likelihoods.

## F02 — bounded dynamic reference

- [x] Implement closed-cohort, time-varying transitions for never-use, exclusive
  smoking, exclusive vaping, dual use, former use and absorbing death.
- [x] Support distinct cohort transitions, interval-specific policies and explicit
  product consumption rates/units; expose boundary populations and interval totals.
- [x] Check static and analytic limits, cessation, product substitution, timing,
  conservation, death, input ownership, invalid probabilities, units metadata and shapes.
- [x] Execute affected tests plus `tests/test_workstream_integration.py` on
  repository Python 3.15.2 / NumPy 2.5.4 / SciPy 1.18.1: 88 passed.
- [ ] Complete the qualified full suite and scientific replays after native
  admission. The focused candidate checks do not satisfy that separate gate.
- [ ] Review the discretisation and state sufficiency against the intended policy
  estimand before adding births, migration, age progression or health memory.

## F03 — systematic evidence review, incrementally through Searchright

- [x] Inspect Searchright's actual source contracts at
  `f6aa483e6ff729dd337d0c0149c660afcddc41cd`; retain its technical-alpha evidence ceiling.
- [ ] SR1: create a narrow pilot review plan and database-native strategies;
  validate against the pinned Searchright schemas and CLI, with exact receipts.
- [ ] SR2: execute documented searches and imports, record provider coverage,
  retrieval failures, deduplication, screening and report-to-study links.
- [ ] SR3: extract eligible study results, assess result-specific bias and transport,
  reconcile shared datasets and create an auditable parameter-evidence table.
- [ ] SR4: qualify one immutable Searchright export-to-tobac evidence handoff on
  fixtures; then admit eligible real evidence through the existing contract.
- [ ] SR5: run an incremental update and show which evidence, parameters, uncertainty
  and decisions changed. Preserve prior review and model versions.

See [the integration plan](searchright.md) for questions, interfaces and acceptance.
Existing web discovery and this public-data pack are not a completed systematic review.

## F04 — empirical dynamic model

- [ ] Specify one NZ policy contrast, horizon, population and decision perspective.
  Freeze source identities and a training/validation split before model fitting.
- [ ] Build a joint observation model for wastewater, survey and lawful supply,
  including uncertain calibration, censoring, shared sources and stock boundaries.
  Reuse `consumption_ledger.py` and existing evidence contracts rather than copy them.
- [ ] Calibrate a parsimonious dynamic baseline. Test identifiability; retain
  partial-identification sets or explicitly prior-sensitive results where needed.
- [ ] Add transported policy effects, adoption/delay and age/cohort heterogeneity.
  Separate gradual implementation from repeated purchasing and consumption.
- [ ] Add health risks and lags, competing mortality, costs and fiscal outcomes
  using reviewed evidence; keep NZD, QALYs, budgets and distributional outcomes distinct.
- [ ] Validate against held-out times/catchments and the comparative benchmarks in
  `design.md`. Forecast calibration and decision performance are separate tests.

## F05 — dynamic decisions and frontier research

- [ ] Compare act-now, defer, phased implementation, pilot, adapt and stop policies
  over the same calendar horizon, resource limits and outcome definitions.
- [ ] Couple evidence arriving over time to belief updates and decision rules;
  value the study duration, affected population, opportunity costs and implementation.
- [ ] Test robust dynamic value of information under measurement drift, partial
  identification and model misspecification against simpler fixed policies.
- [ ] Compare targeted versus population-wide policy and surveillance under explicit
  equity constraints; distinguish preference disagreement from factual uncertainty.
- [ ] Add strategic industry/illicit-supply responses only when they change a
  decision materially and have defensible calibration or bounded sensitivity sets.
- [ ] Demonstrate improvement in held-out prediction or decision regret, uncertainty
  coverage and robustness; retain ablations and publish limitations. Do not infer
  scientific novelty or usefulness from additional machinery alone.

## Verification record

Executed local checks:

- Python 3.15.2, NumPy 2.5.4 and SciPy 1.18.1: **88 passed** across the dynamic
  reference, public-data tests and existing workstream integration tests. The
  reference environment used exact version pins; this invocation is a focused
  candidate check, not the complete native-qualified Nox test session.
- Nox `strict_all`: **passed** with verified Linux audit-lock inputs and a
  hash-checked installation; nine Ruff policy tests passed, all 177 maintained
  Python files passed lint/format checks, and strict typing reported no errors or
  warnings. The audit environment reported 94 compatible installed packages.
- Six ABS re-extractions matched the checked-in candidate CSV bytes exactly.
- Scanner installation encountered an actual HTTP 503, retried successfully and
  verified both pinned archive checksums; gitleaks 8.30.1 and actionlint 1.7.12 ran.
- Nox `publication`: passed using the verified runtime lock and hash-checked
  installation; 21 publication-boundary tests passed, with staged/full-history
  gitleaks scans and Actionlint. Both Nox sessions passed again after the final
  282-record evidence update. Outgoing-commit validation and branch readback follow
  publication.
- Nox `tests`: **blocked before suite execution** at the unchanged native-lineage
  preflight (`Missing TOBAC_LINEAGE_PYTHON`). Native producer/archive configuration
  and renewed scientific inventory/signature are not available in this environment.
  No full-suite, coverage, mutation or scientific-replay success is claimed.

An earlier Python 3.12 portability run passed 57 candidate tests, but the existing
integration module could not parse Python 3.15 syntax. Installing the repository's
pinned uv 0.13.7 resolved interpreter acquisition; the 88-test Python 3.15.2 result
above supersedes that runtime limitation. It does not resolve native admission.
## Published candidate and receiving readback

[Draft PR #147](https://github.com/edithatogo/tobac/pull/147) publishes implementation
commit `6d6ee4ce84bf1a4366280d481711df40f72f262d`, based on main `d735896`.
The received complete Git tree, `d4ecf645852127171c5352bd57880e973bde42ce`, matches
all inspected local index/worktree files. The outgoing-commit publication-boundary
check also passed after fetching the branch. This record is a subsequent
Conductor-only update; it changes no scientific source, data or accepted outputs.

Observed hosted results at that implementation commit include passing Linux audit,
advisory typing and Scorecard workflows. Cross-platform tests, package portability
and M3 jobs reject the candidate with **"Scientific inventory differs from native
acceptance"** before their scientific workloads. Example logs:
[cross-platform](https://github.com/edithatogo/tobac/actions/runs/42476484878/job/128718868001),
[package](https://github.com/edithatogo/tobac/actions/runs/42476484965/job/128718867924),
and [M3](https://github.com/edithatogo/tobac/actions/runs/42476484904/job/128718867823).
Secondary export failures occur because the rejected workloads produced no source
output directory. No rejected gate was disabled, relabelled as passed or replaced
with an unsigned receipt. Other hosted jobs are not claimed successful here.

Changed interfaces are the new opt-in `tobac_supply.dynamic.project_cohorts`
reference and `Projection` result, the public comparison-pack schema, and its
standalone exact-snapshot ABS extractor. Existing evidence-conditioning and lawful
supply interfaces are unchanged. Remaining work is F01 original capture/admission,
F02 native/full-suite qualification and F03–F05 systematic review, empirical
calibration and decision research. No merge or current NZ policy recommendation
has been made.

## CI repair follow-up

The review of PR head `0af81f14a8c9fe9f8aacef272f7a2bf272ae3c20`
confirmed that all eight failed workflow families stop at signed scientific
inventory validation before their scientific workloads. The additional export
errors arise because `always()` invokes the exporter even when preflight failed
before any output directory was created. This is distinct from a numerical test
failure. Representative original logs are the
[engineering job](https://github.com/edithatogo/tobac/actions/runs/42476815311/job/128719903935)
and [verifier job](https://github.com/edithatogo/tobac/actions/runs/42476815294/job/128719903992).

The repair integrates current main `d0e832b02b8b9e6791903f987245e8f6332e943a`,
including PR #148's Phase 3 acceptance and expanded health/equity interfaces.
Documentation and publication inventories preserve both sets of additions.
The upstream native checkpoint remains unchanged; it does not attest this PR's
new `dynamic.py` or comparison pack.

Nineteen scanner/export pairs across nine workflows now use
`!cancelled() && (success() || hashFiles('SOURCE/**') != '')`, with the actual
source directory substituted per workflow. After a successful workload, exports
still run and fail if their required directory is missing. After a failed
workload, an absent/empty source skips export; existing diagnostics still pass
through the unchanged publication inspector and secret scanner. Upload conditions
and fail-closed scanners remain unchanged. The internal release workflow retains
its separate unconditional evidence-export contract.

Local validation uses actual Python 3.15.2. Nox `strict_all` passed after the
integration using the verified audit lock: nine policy tests, lint/format of 186
Python files, and strict typing with zero errors/warnings. Nox `publication`
passed with the verified runtime lock and 21 publication tests. Actionlint accepts
the changed conditions. These are software/publication checks, not native renewal.

The first direct full test collection reported 1376 passed, 20 skipped and 22
failed. Nineteen failures were hosted-lineage authentication: this execution
host's OpenSSH binary is not one of the pinned qualified verifier binaries.
One dependency-snapshot failure correctly detected that integrated locks were not
yet committed at HEAD. Two workflow-contract failures identified the special
internal-release export requirement; that workflow change was removed, preserving
the original contract. The committed-tree rerun and hosted repair readback are
recorded below when available. No failing test is removed, skipped or relaxed.

The normal Nox `tests` entry point still fails before suite execution with
`Missing TOBAC_LINEAGE_PYTHON`. This environment has no configured native producer
wheel or accepted-attempt estate. It also lacks the owner-held signing setup.
To close the remaining gate, the existing native environment must re-execute and
verify the final candidate's eight runners and original/input/output closure,
produce the corresponding native acceptance and regenerate the signed hosted
capsule. The new scientific inventory and changed workflow pins both need that
renewal. Existing receipts, signing authority, runtime profiles and gate code
are retained; changing a digest or suppressing the check is not acceptance.

### Committed repair verification

Repair/merge commit `4f105c9d542a1e85205706f0d6d9590c1bc0f48a` has parents
`0af81f14a8c9fe9f8aacef272f7a2bf272ae3c20` and
`d0e832b02b8b9e6791903f987245e8f6332e943a`. Its received full tree
`a00d2bd935b04d3b88e4271ba89ff83970b9d569` matched the inspected index/worktree
exactly. Staged/full-history secret scanning, Actionlint and outgoing-history
publication validation passed. The branch update used the expected old head and
no force. No accepted native checkpoint, signature, verifier, original data or
scientific implementation from either branch was changed during this repair.

- Focused rerun: **148 passed**, covering dynamic/data, workstream integration,
  execution contracts and publication boundaries.
- Direct full diagnostic collection on that committed tree and the source-bound,
  hash-locked audit environment: **1379 passed, 20 skipped, 19 failed**, with no
  collection errors. Actual Python 3.15.2; 49.37 seconds; sampled process-group
  peak 666.7 MiB under the 4096 MiB / 2400 second guard. This was a diagnostic
  pytest execution, not a successful native-qualified Nox test session.
- The dependency snapshot and release-contract assertions now pass. All remaining
  failed cases are in `tests/engineering/test_hosted_lineage.py`; authentication
  stops because this host's OpenSSH binary is outside the pinned qualified
  profiles. They are retained failures, not capability skips:
  `test_actual_signed_native_acceptance_and_all_inputs`;
  `test_rejection_precedes_hosted_workload` (missing, signature, payload, source,
  inventory, runtime, authority, stage, stage_context, dag);
  `test_valid_object_substitution_is_not_accepted` (artifacts, originals,
  executed_input_objects, manifest); `test_wrong_runner_manifest_selection`;
  `test_failed_native_readback_cannot_qualify`;
  `test_alternate_executable_cannot_report_its_own_success`; and
  `test_runtime_profile_substitution_is_rejected`.
- Actual hosted readback confirms the original secondary failure is repaired in
  both [Linux](https://github.com/edithatogo/tobac/actions/runs/42528424605/job/128877046343)
  and [Windows](https://github.com/edithatogo/tobac/actions/runs/42528424605/job/128877046196)
  package jobs: preflight fails, then both scanner/export steps are **skipped**,
  with no absent-source exception. The remaining primary error is
  `Stale native acceptance pin: .github/workflows/advisory-types.yml`, because
  the unchanged signed capsule also binds the workflow edits. Inventory renewal
  remains required as well; bypassing the first stale pin would not close it.

The PR remains draft. Native qualification, full qualified coverage/reproduction
and overall hosted success are not claimed. This receiving record updates only
Conductor documentation; its publication does not itself renew native acceptance.
