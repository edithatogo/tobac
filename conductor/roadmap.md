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

The existing workflow definitions and repository checks remain unchanged. They may still execute
on non-macOS runners; this roadmap does not waive their failures, assert success, or change branch
protection. Any returned work must use current `main`, preserve in-flight work, and record actual
platform-specific verification.

## Advisory CI/CD, automation, quality and security lane

Track: `conductor/roadmap/cicd_hardening_20261025/`.

Deferred pending separate maintainer prioritisation; the reference macOS strict checks
are now qualified. The proposed Linux arm runner and
additional automation tools are roadmap work; no job or entitlement is claimed as qualified.

## Optional macOS hardening follow-ups

These are improvements beyond the completed 26 October macOS acceptance scope, not
open execution gates or automatic implementation authorisation:

- Triage the 29 surviving supply mutants from PR #43's hosted 102/131 (77.9%) measurement;
  distinguish equivalent mutations from worthwhile missing assertions.
- Reconsider the 175 documented Ruff style/API exceptions where a change preserves
  public interfaces, validation behavior and scientific meaning. They are not 175
  behavioral defects claimed fixed.

The earlier 100/131 measurement remains dated evidence. The separate bounded gremlins
campaign detected 68/68; its denominator does not replace mutmut. F6's non-macOS ARM
diagnostic execution remains deferred here; it is not an unchecked current macOS task.
