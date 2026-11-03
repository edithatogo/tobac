# Bounded lane implementation and verification

Status: **DCI1–DCI4 complete**.
Reconciled 3 November 2026 against receiving main `672894f70bebd4ba17ba38fe8116c938ad13fe4f`.
The qualified advisory lane was published by guarded fast-forward and its receiving tree verified.

## Completed preparation

- [x] Read main, issue #1, existing workflows, Nox sessions, locks and engineering policy.
- [x] Verify proposed action and tool refs against real tag reads; record tag+commit.
- [x] Record the drop-in misidentifications (prek != pre-commit; ty, pyrefly and
  basedpyright are separate checkers; helpers:pinGitHubActionDigests is a Renovate preset).

## Deferred phase — qualify additional advisory automation

- [x] DCI1 — Selected one ty 0.0.95/Pyrefly 1.4.0 comparison experiment and a Linux
  ARM64 diagnostic leg; omitted duplicate wrappers/hook migration and reverified refs.
  [Decision](selection_20261103.md) · [Pin/delivery metadata](selection_20261103.json).
- [x] DCI2 — Implement the isolated source-bound advisory profile, Nox/report handling,
  selected macOS/Linux x64/Ubuntu ARM diagnostic jobs and checksum-pinned ARM scanner
  support. Renew the orchestration binding; retain every required/reference gate.
- [x] DCI3 — Execute selected local and hosted checks and record actual supported
  behavior, capability limits and any unexecuted jobs.
- [x] DCI4 — Publish the qualified bounded lane with an expected-head check and
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
records incomplete report handling and unexecuted hosted jobs. At that historical checkpoint the Nox session, workflow, ARM execution and
capsule renewal remained open. The checkpoint was not part of the DH1/DH2
publication packet and has since been integrated onto the DCI2 implementation
branch; hosted ARM static execution subsequently passed under DCI3.

The checkpoint is now integrated into the DCI2 implementation branch; its local
[qualification evidence](qualification_20261103.md) is retained here.

DCI2 implementation and local evidence: [implementation receipt](implementation_20261103.md).

DCI3 passed all three hosted diagnostic jobs at `4b6dbf18ca3570b1cb1bd27019d81a4287a1bf50`; [hosted artifact receipt](../../../integration/advisory_typing_qualification_20261103.json) records exact scope and limits. The exact publication head passed 28 hosted checks (two conditional skips), including all three advisory hosts in [run 41623880425](https://github.com/edithatogo/tobac/actions/runs/41623880425). [PR #118](https://github.com/edithatogo/tobac/pull/118) was published by non-force fast-forward from expected main `afec3a48ce7bae14f9602c48d6c30a8b3f8dab29` to `672894f70bebd4ba17ba38fe8116c938ad13fe4f`; GitHub readback reported that commit and tree `b80bc11653d601ce8892a9d617132147f8059163`, matching the qualified local tree. The ARM leg qualifies static diagnostics and scanners, not scientific reproduction.
