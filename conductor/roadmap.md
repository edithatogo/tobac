# Roadmap

This file records work intentionally deferred from active Conductor tracks. Items here are
planning commitments, not current development tasks, implementation authorization, or evidence
that a platform has passed qualification. There is no target date until the maintainer reprioritizes
the work.

## Cross-platform engineering qualification

Hosted Linux and Windows Python 3.15.1 runtime tests were restored and qualified by
PR #66 at receiving main `62056c5`; macOS remains the full engineering/reference
qualification platform. DXP1–DXP4 are complete for their declared workloads:

- [x] DXP1 — Installed and executed the source-bound Linux x86_64 audit lock on
  Python 3.15.1 in GitHub Actions run [41534684953](https://github.com/edithatogo/tobac/actions/runs/41534684953).
  All 96 locked packages match the installed inventory; strict/security sessions,
  96 focused tests and inspected artifact export pass. [Receipt](../integration/linux_audit_lock_20261103.json).
- [x] DXP2 — Qualified Linux/Windows package paths, dependency/extra markers,
  Unicode encodings and source/wheel build/install behavior in GitHub
  [run 41542664379](https://github.com/edithatogo/tobac/actions/runs/41542664379).
  Both direct and sdist-rebuilt wheels pass isolated imports/API/transport/quick CLI
  smokes and inspected export. [Receipt](../integration/package_portability_20261103.json).
- [x] DXP3 — Executed full scientific reproduction on Linux and Windows with
  Python 3.15.1 in [run 41557415490](https://github.com/edithatogo/tobac/actions/runs/41557415490).
  All eight runner variants and 82 scientific CSV tables match the accepted
  references within their declared policies; 29 isolated publication replay tables
  also pass on each host. [Receipt](../integration/scientific_reproduction_20261103.json).
- [x] DXP4 — Restored and qualified manual release and four-profile lock candidates.
  [Release run 41570769167](https://github.com/edithatogo/tobac/actions/runs/41570769167)
  passes seven Nox sessions, all eight scientific variants / 82 CSV tables,
  clean-package replay and inspected package upload on qualified Ubuntu 26.04.
  [Lock run 41567710835](https://github.com/edithatogo/tobac/actions/runs/41567710835)
  passes generation, source receipts, hash installation and exact installed-inventory
  readback for runtime, audit, Voiage and ecosystem. Six deliberate stale-source jobs
  reject before execution. [Receipt](../integration/manual_workflows_20261103.json).
  Candidates are review artifacts and have not replaced the committed locks.

Historical owner decision, 28 October 2026: Windows and Linux were not then
acceptance gates. PR #66 supersedes that decision for runtime tests. Retain the same scientific,
security, dependency-graph, provenance and numerical checks there. SourceRight
uses its hash-verified published macOS ARM64 binary on an ARM64 macOS runner;
the upstream asset filename misleadingly says x86_64.

The manual workflows are active under `.github/workflows/`, require explicit
source commits and export inspected evidence. The original definitions remain in
Git history. Scheduled lock generation stays disabled as optional automation;
DXP4 does not enable automatic adoption. macOS and Linux qualifications retain
separate receipts and platform scopes.

Superseded October runs and the first DXP4 failures remain historical evidence,
not passes. Fresh hosted qualifications above supersede the platform deferral
for these declared workloads. Branch protection and repository visibility are unchanged.

## Advisory CI/CD, automation, quality and security lane

Track: `conductor/roadmap/cicd_hardening_20261025/`.

DCI1 selection is complete: a bounded ty 0.0.95/Pyrefly 1.4.0 comparison and
Linux ARM64 static-diagnostic leg are selected; duplicate security/lint/action
wrappers and hook migration are omitted. [Decision](roadmap/cicd_hardening_20261025/selection_20261103.md).
DCI2 is implemented and locally verified on `codex/dci2-implementation`; DCI3
hosted qualification passed and DCI4 publication remains pending. The earlier published checkpoint is
integrated on that branch, not merged to main. ARM qualification covers static
diagnostics and scanner execution only; scientific verifier profiles are unchanged.

## Optional macOS hardening follow-ups

These are improvements beyond the completed 26 October macOS acceptance scope, not
open execution gates or automatic implementation authorisation:

- [x] DH1 — Triaged all 12 supply survivors from PR #51; focused tests detect ten,
  and two are equivalent for the qualified SciPy call. A fresh local run detected
  129/131. [Evidence](../docs/reviews/2026-11-03-supply-mutant-triage.md).
- [x] DH2 — Reviewed the retained source/API Ruff exceptions; documented the reasons to
  retain them, including the scientific lineage impact of a tested refactor.
  [Review](../docs/reviews/2026-11-03-ruff-exception-review.md).

The earlier 100/131 and 102/131 mutation measurements and the 26 October inventory
of 175 source/style exceptions remain dated evidence, not current outstanding counts.
The separate bounded gremlins
campaign detected 68/68; its denominator does not replace mutmut. F6's non-macOS ARM
diagnostic execution remains deferred here; it is not an unchecked current macOS task.

## Reconciliation — 3 November 2026

DXP1–DXP4 and DCI1 selection are complete. One advisory-lane task remains: DCI4 publication.
The two optional hardening tasks are complete.
The DCI implementation is on a separate branch pending qualification and publication.
See [current status](status.md) for completed gates, open dependency-update PRs,
scientific requirements and the disposition of superseded decision drafts.
