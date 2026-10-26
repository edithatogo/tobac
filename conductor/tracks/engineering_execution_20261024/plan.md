# Implementation and evidence

- [x] Inspect current main 711705c, engineering files and shared coordination issue.
- [x] Reproduce unsupported annotation access and local network/tool constraints.
- [x] Write failing tests for lock identity, resolver failure and execution contracts.
- [x] Implement source-bound uv receipts and separate runtime/audit inputs.
- [x] Require exact environment sync and no floating build/tool installation after locks.
- [x] Preserve failure evidence; independent checks retain overall failures.
- [x] Add GET-only gh diagnostic with pagination and explicit missing-access state.
- [x] Run scoped helpers/contracts and actual unsuccessful uv resolution; record limits.
- [~] Complete source-bound lock qualification for the current macOS development target.
  - [x] Runtime lock generated, reviewed, receipt-verified and hash-installed on macOS.
  - [ ] Install and execute the Linux-scoped audit lock; deferred with Linux qualification in
    `conductor/roadmap.md`.
- [~] Complete remaining macOS engineering checks and preserve their actual outcomes.
  - [x] Scientific replay, package build/install, native quality/security tools, mutation and
    bounded profiling were executed on macOS; see the linked receipts and readiness record.
  - [x] Whole-source `strict_all` passes after PR #25 reconciliation; explicit style/API
    exceptions and optional-library static contracts are documented in LINT_POLICY.md.
  - Non-macOS platform-matrix qualification is deferred to `conductor/roadmap.md`.
- [ ] Confirm post-migration hosted macOS checks from actual annotations; diagnose any failure
  without weakening gates. Non-macOS hosted-runner diagnosis is deferred to the roadmap.

Publication receipt is the final receiving commit recorded in the local track. Local helper/command
contracts do not count as Nox, whole-repository or third-party execution. Existing M3 work,
scientific sources, payoff functions, posterior outputs and Conductor pin are preserved.
