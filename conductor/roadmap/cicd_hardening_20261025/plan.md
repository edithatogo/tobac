# Bounded lane implementation and verification

Status: **DCI1 complete; DCI2 and DCI3 in progress on a separate checkpoint; DCI4 pending**.
Reconciled 3 November 2026 against main `b6fcf45` and checkpoint `e007807`.
The advisory lane is not hosted-qualified or merged to main.

## Completed preparation

- [x] Read main, issue #1, existing workflows, Nox sessions, locks and engineering policy.
- [x] Verify proposed action and tool refs against real tag reads; record tag+commit.
- [x] Record the drop-in misidentifications (prek != pre-commit; ty, pyrefly and
  basedpyright are separate checkers; helpers:pinGitHubActionDigests is a Renovate preset).

## Deferred phase — qualify additional advisory automation

- [x] DCI1 — Selected one ty 0.0.95/Pyrefly 1.4.0 comparison experiment and a Linux
  ARM64 diagnostic leg; omitted duplicate wrappers/hook migration and reverified refs.
  [Decision](selection_20261103.md) · [Pin/delivery metadata](selection_20261103.json).
- [~] DCI2 — Implement the isolated source-bound advisory profile, Nox/report handling,
  selected macOS/Linux x64/Ubuntu ARM diagnostic jobs and checksum-pinned ARM scanner
  support. Renew the orchestration binding; retain every required/reference gate.
- [~] DCI3 — Execute selected local and hosted checks and record actual supported
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

## Separate implementation checkpoint

Branch [codex/dci-advisory-checkpoint-20261103](https://github.com/edithatogo/tobac/tree/codex/dci-advisory-checkpoint-20261103)
at `e0078071af2fb6c2e47c32e2da3369c07175be57` retains the isolated lock,
prototype runner and local Voiage/checker evidence. Its
[qualification note](https://github.com/edithatogo/tobac/blob/e0078071af2fb6c2e47c32e2da3369c07175be57/conductor/roadmap/cicd_hardening_20261025/qualification_20261103.md)
records incomplete report handling and unexecuted hosted jobs. The Nox session,
workflow, native ARM scanner execution and orchestration capsule renewal remain.
That branch is not part of the DH1/DH2 publication packet and must be reconciled
against receiving main before its own integration.

The checkpoint is now integrated into the DCI2 implementation branch; its local
[qualification evidence](qualification_20261103.md) is retained here.
