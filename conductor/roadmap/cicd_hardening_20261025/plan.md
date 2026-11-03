# Bounded lane implementation and verification

Status: **DCI1 selection complete; DCI2–DCI4 deferred**.
Reconciled 3 November 2026 at receiving base `6830891`.
The owner authorized selection only; no new lane is installed or qualified.

## Completed preparation

- [x] Read main, issue #1, existing workflows, Nox sessions, locks and engineering policy.
- [x] Verify proposed action and tool refs against real tag reads; record tag+commit.
- [x] Record the drop-in misidentifications (prek != pre-commit; ty, pyrefly and
  basedpyright are separate checkers; helpers:pinGitHubActionDigests is a Renovate preset).

## Deferred phase — qualify additional advisory automation

- [x] DCI1 — Selected one ty 0.0.95/Pyrefly 1.4.0 comparison experiment and a Linux
  ARM64 diagnostic leg; omitted duplicate wrappers/hook migration and reverified refs.
  [Decision](selection_20261103.md) · [Pin/delivery metadata](selection_20261103.json).
- [ ] DCI2 — Implement the isolated source-bound advisory profile, Nox/report handling,
  selected macOS/Linux x64/Ubuntu ARM diagnostic jobs and checksum-pinned ARM scanner
  support. Renew the orchestration binding; retain every required/reference gate.
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
