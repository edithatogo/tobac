# Implementation plan for review

Status: draft; no tasks below are claimed implemented or executed.
Specification: [spec.md](spec.md). Ownership/tools: [decisions.md](decisions.md).
Method: [project workflow](../../workflow.md). Tests for changed semantics precede code.
All phases end with evidence review. Local review is not independent scientific review.

## Phase A — Reconcile and register bounded work (R01–R10)

- [ ] Task A1: Refresh main, issue #1, worktrees and owned paths; rebuild the bounded context receipt.
- [ ] Task A2: Inventory existing sister clones within the requested bounded search, then verify repository remotes/default branches; clone only missing needed repositories.
  - [ ] Read each applicable AGENTS.md, research-change skill and Conductor convention before changes.
  - [ ] Inspect all relevant open/closed issues and tracks with pagination; reuse matches and record exact revisions/capabilities.
- [ ] Task A3: Resolve repository ownership using decisions.md and existing consumers.
  - [ ] Reconcile PR #19, PR #20, M3 and the archive-govt-nz owner without assuming merge or completion.
  - [ ] Keep Kairos Rust-first; decide the correct owner for timing/decision algorithms before defining an adapter.
- [ ] Task A4: After plan approval, register the tobac master track and only warranted upstream tracks/issues, cross-linking reused work and blockers.
  - [ ] Use repo-native registry layouts; bootstrap missing Conductor only after inspection and within accepted scope.
  - [ ] Preserve the accepted specification and numbered tasks; assign one writer to each shared object.
- [ ] Task A5: Phase verification and checkpoint: review ownership, duplicate search, dependency graph and exact base receipts under workflow.md.

## Phase B — Baseline, runtime and contracts (R01–R04)

- [ ] Task B1: Capture canonical verifier inputs/outputs and current artifact hashes in a complete checkout before changes.
- [ ] Task B2: Write consumer-contract and independent-oracle tests for the approved public interfaces, including invalid/missing data and scientific invariants.
- [ ] Task B3: Qualify repo-local Python 3.15.1 and the newest suitable dependencies in isolated environments, recording actual interpreter and package identities.
  - [ ] Resolve supported incompatibilities and integrate existing runtime PRs; record genuine blockers without downgrading or bypassing.
  - [ ] Align constraints, locks, active CI/helpers and Apache-2.0 metadata while preserving third-party rights and in-flight operations.
- [ ] Task B4: Establish reproducible NumPy reference runs under the required runtime; preserve expected hashes and explain every mismatch before proceeding.
- [ ] Task B5: Phase verification and checkpoint: run affected tests and tests/test_workstream_integration.py, then coherent full-suite/reproduction gates; retain failures and evidence.

## Phase C — Upstream capability and structured interchange (R03, R06)

- [ ] Task C1: Write producer and consumer acceptance cases against real installed upstream APIs before modifying them.
- [ ] Task C2: Implement only missing reusable capabilities in their owning repos: VOI/cost interfaces, uptake/diffusion, extraction/citation provenance or generic simulation adapters.
- [ ] Task C3: Write schema, no-coercion, ordering, null/NaN, lifetime, chunking and migration/rollback tests.
- [ ] Task C4: Implement qualified Polars/Arrow/Patito/msgspec boundaries without replacing the shared evidence contract.
  - [ ] Verify buffer identity/lifetime/allocation for each zero-copy claim and distinguish logical versus raw-byte hashing.
- [ ] Task C5: Wire exact upstream artifacts or editable development sources into tobac with explicit versions and independent package boundaries.
- [ ] Task C6: Phase verification and checkpoint: execute upstream native suites and tobac consumer/integration checks; retain real API/runtime receipts and changed-interface notes.

## Phase D — Numerical backends and performance (R02, R04, R07)

- [ ] Task D1: Write matched-input float64 parity, nonfinite/error, state-order, tie-policy and explicit-backend tests.
- [ ] Task D2: Add the opt-in JAX backend and only operation-qualified libraries, keeping NumPy the default.
  - [ ] Verify x64 before arrays/JIT, actual device identity and no silent fallback.
  - [ ] Add tolerance verification without weakening canonical source/evidence hashes or NumPy checks.
  - [ ] Distinguish shared deterministic draws from backend-specific RNG/distribution checks.
- [ ] Task D3: Write representative performance harness cases and agree measured runtime/memory budgets.
- [ ] Task D4: Benchmark cold compilation, transfer and synchronised warm execution; optimise only measured bottlenecks.
- [ ] Task D5: Assess mars through voiage only if warranted; otherwise record an evidenced defer decision.
  - [ ] Require cross-fitting, held-out error and decision-ranking/regret checks against exact cases before surrogate use.
- [ ] Task D6: Phase verification and checkpoint: execute canonical reference reproduction, JAX parity and scientific invariants with actual performance receipts.

## Phase E — Replay, clean packages and evidence/context (R05, R06, R09)

- [ ] Task E1: Write tests for receipt schema/version integrity, stale inputs/environments, interrupted runs and immutable prior receipts.
- [ ] Task E2: Extend existing run metadata and checkpoint/recovery behavior where required; verify uninterrupted versus resumed results.
- [ ] Task E3: Build wheel/sdist with source overrides disabled and install outside the checkout; exercise real CLI/APIs, packaged data and dependency closure.
- [ ] Task E4: Write context/acceptance tests for required-contract retrieval, source-hash and HEAD changes, incomplete evidence, ownership and untrusted source text.
- [ ] Task E5: Extend existing bounded context and Conductor acceptance mapping to reject unsupported or stale completion claims.
- [ ] Task E6: Phase verification and checkpoint: clean-package, replay/recovery and context tests pass with exact revisions and artifact identities; rebuild stale context.

## Phase F — CI/CD, security and test effectiveness (R04, R08)

- [ ] Task F1: Reconcile the existing CI-hardening track; qualify each tool in decisions.md on the required runtime and supported platforms.
- [ ] Task F2: Compare ty/pyrefly/BasedPyright diagnostics and prek hooks; retain explicit dispositions and current required checks.
- [ ] Task F3: Write or select meaningful scientific mutation cases, prove imported code identity, and compare pytest-gremlins with existing mutation checks.
- [ ] Task F4: Extend supported pinned actions, environment/cache controls, least privilege and source-bound locks through Nox/uv.
- [ ] Task F5: Implement the security findings lifecycle, artifact-linked SBOM and downstream attestation verification.
  - [ ] Retain owner, component, rationale, remediation proof and expiring exceptions; do not hide unresolved findings.
  - [ ] Qualify harden-runner audit and supported egress policy without changing account entitlements.
- [ ] Task F6: Execute the ARM diagnostic lane and preserve separate architecture/numerical qualification results.
- [ ] Task F7: Phase verification and checkpoint: inspect actual hosted job logs/artifacts, prove attestation verification, and promote only qualified checks; record unresolved debt.

## Phase G — Optional evidence integrations (R10)

- [ ] Task G1: Evaluate a narrow offline Searchright consumer slice for record/report/study identity and search provenance.
  - [ ] Write duplicate-study, lineage and schema-version tests before adding any adapter; preserve human applicability decisions.
- [ ] Task G2: Consume the archive-govt-nz owner's source-binding contract; assess AegisArchive only for uncovered preservation requirements.
  - [ ] Verify permitted snapshot digests, retained editions and offline replay; source capture is not extraction or likelihood approval.
- [ ] Task G3: Record adopt/trial/defer decisions; upstream tracks require a concrete demonstrated gap and named consumer.
- [ ] Task G4: Phase verification and checkpoint: review actual consumer evidence and rights boundaries; a justified defer can close an assessment but not an implementation claim.

## Phase H — Integrated qualification and handoff (R01–R10)

- [ ] Task H1: Execute affected upstream native suites and the complete tobac suite in a complete qualified checkout, including workstream integration and numerical reproductions.
  - [ ] Verify prior-work bytes, M1/M2/longitudinal/M3 canonical outputs, JAX tolerances and actual upstream execution.
  - [ ] Confirm exact CLI syntax from the implemented entrypoints; the original prompt's example commands are not assumed to exist unchanged.
- [ ] Task H2: Run final clean-package, coverage, security, recovery and performance gates without counting focused/cached tests as a full run.
  - [ ] Preserve per-environment pytest caches; use bounded selectors while editing and zero retries by default.
  - [ ] Restrict any retry to an identified transient read-only case; never retry native mutations or sends through the test runner.
- [ ] Task H3: Review final diffs and scientific assumptions, reconcile current main/issue #1, and publish only within authorised scope using guarded expected-head checks.
- [ ] Task H4: Verify remote refs/files and hosted outcomes; post receiving commits, actual test scopes, interface changes and open gaps on #1.
- [ ] Task H5: Phase verification and checkpoint: deliver repository paths, issue URLs, track paths, artifact identities and verification status; distinguish local, hosted, upstream and scientific acceptance.

## Review and sequencing

Critical path: A → B → C → D/E → F → H. Optional G can be assessed independently after
ownership is clear. The active archive and CI workstreams remain dependencies, not reassigned
work. No parallel agents or new chats are implied. No skill installation is needed from the
Conductor catalog reviewed for this plan.

The Conductor planner requires review of this implementation plan before track registration.
No phase is complete merely because this document exists.
