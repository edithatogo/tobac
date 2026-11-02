# Bounded lane implementation and verification

Status: **deferred to roadmap**, with no active implementation authorization.
Reconciled 2 November 2026 against the completed macOS reference implementation.

## Completed preparation

- [x] Read main, issue #1, existing workflows, Nox sessions, locks and engineering policy.
- [x] Verify proposed action and tool refs against real tag reads; record tag+commit.
- [x] Record the drop-in misidentifications (prek != pre-commit; ty, pyrefly and
  basedpyright are separate checkers; helpers:pinGitHubActionDigests is a Renovate preset).

## Deferred phase — qualify additional advisory automation

- [ ] DCI1 — Select additions that do not duplicate existing macOS security, strict,
  pinning, publication-attestation and pre-commit checks; reverify current tool refs.
- [ ] DCI2 — Implement the selected advisory Nox/workflow additions, including any
  selected Ubuntu ARM diagnostic leg, with source-bound pins and unchanged required gates.
- [ ] DCI3 — Execute selected local and hosted checks and record actual supported
  behavior, capability limits and any unexecuted jobs.
- [ ] DCI4 — Publish the qualified bounded lane with an expected-head check and
  verify the receiving revision and files.

## Superseded proposal scope

PR #20 is closed. The former seven unchecked proposal bullets overlapped completed
reference automation and included issue #1 announcements. Issue #1 is historical
context and posting is not a gate or an authorized external-message task. Existing
macOS strict, security, dependency inventory and package-attestation execution is
complete for its documented scope. The four tasks above retain only the future
advisory lane's scope selection, implementation, qualification and publication.
No existing attestation result qualifies an unexecuted advisory dispatch or ARM leg.
Historical strict_all diagnostics remain in Git history and are not current defects.
