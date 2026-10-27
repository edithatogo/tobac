# Review Report: Renovate dependency policy

## Summary

Renovate is explicitly the sole updater, with previously missed profile inputs
covered and all existing security/runtime/merge controls retained.

## Verification Checks

- [x] **Plan Compliance**: Yes — no duplicate updater, Python or scientific change.
- [x] **Style Compliance**: Valid JSON/YAML; official strict Renovate validator passed.
- [x] **New Tests**: Two provider/profile and workflow-coverage regression cases.
- [x] **Test Coverage**: Full suite; 92% displayed branch-inclusive coverage.
- [x] **Test Results**: 884 passed, five capability skips; quality/security passed.

## Findings

### High — Profile inputs were absent from updater discovery (resolved)

The native prior dashboard listed requirements text files but omitted the .in
producer profiles. Add root-scoped pip_requirements manager patterns; the official
extract-only run now detects all four .in files and preserves existing defaults.
No generated lock or historical source is edited by the updater configuration.

### Medium — Lock candidate workflow covered only two profiles (resolved)

Expand the read-only manual workflow to runtime/audit/Voiage/ecosystem and assert
its real Python 3.15.1 interpreter. Existing source-bound helpers and pinned Actions
remain unchanged. Native four-job execution is required during publication.

### Scope distinction — Updater versus internal graph parser

Renovate already operates as a GitHub App. Dependabot version configuration is
absent and security-update PRs are already disabled. GitHub's graph parser runs
when the graph is enabled; removing that capability would not be an equivalent
updater switch. Retain the graph, supported submission and explicit external gate.
Vulnerability-alert automation was disabled at inspection and is not claimed active.
Scientific/data gates, the roadmap and draft PR #41 remain open in their own scopes.

### High — setup-uv selection did not select bare python (resolved)

The first native four-profile dispatch failed its new version assertion. The
existing workflow declared Python 3.15.1 but invoked the runner's bare python.
Create .venv-lock with uv's explicit 3.15.1 selection and invoke its interpreter
for both the assertion and resolver helper. A regression case protects the
explicit interpreter. First failure: native run 40428239594; no assertion removed.
