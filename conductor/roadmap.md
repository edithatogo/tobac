# Roadmap

This file records work intentionally deferred from active Conductor tracks. Items here are
planning commitments, not current development tasks, implementation authorization, or evidence
that a platform has passed qualification. There is no target date until the maintainer reprioritizes
the work.

## Cross-platform engineering qualification

Hosted Linux and Windows Python 3.15.1 runtime tests were restored and qualified by
PR #66 at receiving main `62056c5`; macOS remains the full engineering/reference
qualification platform. The following additional work is deferred:

- [ ] DXP1 — Install and execute the source-bound Linux x86_64 audit lock under
  the qualified Python 3.15 runtime.
- [ ] DXP2 — Qualify non-macOS package paths, dependency markers, encodings and
  release behavior beyond the passing runtime tests.
- [ ] DXP3 — Execute platform-specific scientific reproduction on supported
  non-macOS platforms.
- [ ] DXP4 — Reconsider and requalify the deferred manual release and lock-generation
  workflows when non-macOS release/audit work is reprioritised.

Historical owner decision, 28 October 2026: Windows and Linux were not then
acceptance gates. PR #66 supersedes that decision for runtime tests. Retain the same scientific,
security, dependency-graph, provenance and numerical checks there. SourceRight
uses its hash-verified published macOS ARM64 binary on an ARM64 macOS runner;
the upstream asset filename misleadingly says x86_64.

The original Linux-specific manual workflows are retained, inactive, in
`conductor/roadmap/deferred-workflows/`: `release-candidate.yml` and
`dependency-lock.yml`. Their Linux audit-lock and source/hash requirements remain
unchanged. The scheduled `lock` session, which also resolves the Linux audit
profile, is deferred here as well; security/strict/mutation/profile/canary remain
active on macOS. Reconsider and requalify these generators only when non-macOS work
is reprioritised.
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

## Reconciliation — 2 November 2026

The four cross-platform tasks, four advisory-lane tasks and two optional hardening
tasks are the ten deferred tasks across three work groups/phases. None is active.
See [current status](status.md) for completed gates, open dependency-update PRs,
scientific requirements and the disposition of superseded decision drafts.
