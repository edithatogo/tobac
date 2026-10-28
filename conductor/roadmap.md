# Roadmap

This file records work intentionally deferred from active Conductor tracks. Items here are
planning commitments, not current development tasks, implementation authorization, or evidence
that a platform has passed qualification. There is no target date until the maintainer reprioritizes
the work.

## Cross-platform engineering qualification

Current engineering development is focused on macOS. The following work is deferred:

- Install and execute the source-bound Linux x86_64 audit lock under Python 3.15.1.
- Qualify the engineering matrix on Linux and Windows and retain hosted results for each platform.
- Diagnose and repair non-macOS hosted-runner failures using their actual annotations.
- Verify packaging, dependency markers, paths, encodings and scientific reproduction behavior on
  supported non-macOS platforms.
- Reconsider when cross-platform qualification should return to active tracks.

Owner decision, 28 October 2026: Windows and Linux results are not current
acceptance gates. Active hosted jobs target macOS; retain the same scientific,
security, dependency-graph, provenance and numerical checks there. SourceRight
uses its hash-verified published macOS ARM64 binary on an ARM64 macOS runner;
the upstream asset filename misleadingly says x86_64.

The original Linux-specific manual workflows are retained, inactive, in
`conductor/roadmap/deferred-workflows/`: `release-candidate.yml` and
`dependency-lock.yml`. Their Linux audit-lock and source/hash requirements remain
unchanged. Reconsider and requalify them only when non-macOS work is reprioritised.
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

- Triage the 12 surviving supply mutants from PR #51's receiving-main macOS
  119/131 (90.8%) measurement;
  distinguish equivalent mutations from worthwhile missing assertions.
- Reconsider retained source/API Ruff exceptions where a change preserves public
  interfaces, validation behavior and scientific meaning. Test/tooling lint, formatting
  and five explicit preview rules are implemented by PR #51, not deferred work.
  See `docs/engineering/RUFF_POLICY.md` for the current scoped policy.

The earlier 100/131 and 102/131 mutation measurements and the 26 October inventory
of 175 source/style exceptions remain dated evidence, not current outstanding counts.
The separate bounded gremlins
campaign detected 68/68; its denominator does not replace mutmut. F6's non-macOS ARM
diagnostic execution remains deferred here; it is not an unchecked current macOS task.
