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
- [ ] Complete actual source-security, publication and hosted checks on this candidate.

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
Publication readback and the exact candidate commit will be appended after the
branch and PR are created.
