# Roadmap

This file records work intentionally deferred from active Conductor tracks. Items here are
planning commitments, not current development tasks, implementation authorization, or evidence
that a platform has passed qualification. There is no target date until the maintainer reprioritizes
the work.

## Cross-platform engineering qualification

Hosted Linux and Windows Python 3.15.1 runtime tests were restored and qualified by
PR #66 at receiving main `62056c5`; macOS remains the full engineering/reference
qualification platform. DXP1, DXP2 and DXP3 are complete; DXP4 manual release work is in progress:

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
- [~] DXP4 — Restore and qualify manual release and four-profile lock candidates.
  All four lock candidates are generated, hash-installed and read back from
  [run 41567710835](https://github.com/edithatogo/tobac/actions/runs/41567710835).
  Release correctly rejected Ubuntu 24.04's unqualified OpenSSH before execution;
  the Ubuntu 26.04 route and retained preflight evidence await actual main execution.
  [Progress receipt](../integration/manual_workflows_20261103.json).

Historical owner decision, 28 October 2026: Windows and Linux were not then
acceptance gates. PR #66 supersedes that decision for runtime tests. Retain the same scientific,
security, dependency-graph, provenance and numerical checks there. SourceRight
uses its hash-verified published macOS ARM64 binary on an ARM64 macOS runner;
the upstream asset filename misleadingly says x86_64.

DXP4 restores the manual workflows under `.github/workflows/` using current
source locks, qualified Python, lineage checks, bounded execution and inspected
exports. Actual manual run/artifact readback remains pending. The scheduled `lock`
session remains deferred; this task does not enable automatic lock adoption.
The native macOS audit lane is not the Linux hash-locked release profile; no
locked-release acceptance is inferred from this platform deferral. Existing locks
and their receipts remain committed and verified by the active macOS checks.

Superseded mixed-platform runs for 94c4712 were cancelled where still active;
the already completed longitudinal run is preserved. Cancellation is not a pass.
Current acceptance requires fresh macOS runs of the revised workflows. No branch
protection or repository ruleset changes are made.

## Advisory CI/CD, automation, quality and security lane

Track: `conductor/roadmap/cicd_hardening_20261025/`.

Deferred pending separate maintainer prioritisation; the reference macOS strict checks
are now qualified. The proposed Linux arm runner and
additional automation tools are roadmap work; no job or entitlement is claimed as qualified.

## Optional macOS hardening follow-ups

These are improvements beyond the completed 26 October macOS acceptance scope, not
open execution gates or automatic implementation authorisation:

- [ ] DH1 — Triage the 12 surviving supply mutants from PR #51's receiving-main macOS
  119/131 (90.8%) measurement;
  distinguish equivalent mutations from worthwhile missing assertions.
- [ ] DH2 — Reconsider retained source/API Ruff exceptions where a change preserves public
  interfaces, validation behavior and scientific meaning. Test/tooling lint, formatting
  and five explicit preview rules are implemented by PR #51, not deferred work.
  See `docs/engineering/RUFF_POLICY.md` for the current scoped policy.

The earlier 100/131 and 102/131 mutation measurements and the 26 October inventory
of 175 source/style exceptions remain dated evidence, not current outstanding counts.
The separate bounded gremlins
campaign detected 68/68; its denominator does not replace mutmut. F6's non-macOS ARM
diagnostic execution remains deferred here; it is not an unchecked current macOS task.

## Reconciliation — 3 November 2026

DXP1–DXP3 are complete. One release/lock task is in progress; four advisory-lane tasks and two
optional hardening tasks remain deferred: seven remaining tasks across three work groups/phases.
DXP4 is in progress; six other tasks remain deferred.
See [current status](status.md) for completed gates, open dependency-update PRs,
scientific requirements and the disposition of superseded decision drafts.
