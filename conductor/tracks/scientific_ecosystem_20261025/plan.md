# Scientific ecosystem implementation and review

Status: autonomous macOS implementation, review, fixes and archival authorised on
26 October 2026. Original accepted checklist is retained in approved-plan_20261025.md.
Checked items below mean the stated bounded execution/assessment, not empirical qualification.
Specification: [spec.md](spec.md). Ownership/tools: [decisions.md](decisions.md).
Method: [project workflow](../../workflow.md). Tests for changed semantics precede code.
All phases end with evidence review. Local review is not independent scientific review.

## Phase A — Reconcile and register bounded work (R01–R11)

- [x] Task A1: Refresh main, issue #1, worktrees and owned paths; rebuild the bounded context receipt.
- [x] Task A2: Inventory existing sister clones within the requested bounded search, then verify repository remotes/default branches; clone only missing needed repositories.
  - [x] Read each applicable AGENTS.md, research-change skill and Conductor convention before changes.
  - [x] Inspect all relevant open/closed issues and tracks with pagination; reuse matches and record exact revisions/capabilities.
- [x] Task A3: Resolve repository ownership using decisions.md and existing consumers.
  - [x] Reconcile PR #19, PR #20, M3 and the archive-govt-nz owner without assuming merge or completion.
  - [x] Keep Kairos Rust-first; decide the correct owner for timing/decision algorithms before defining an adapter.
- [x] Task A4: After plan approval, register the tobac master track and only warranted upstream tracks/issues, cross-linking reused work and blockers.
  - [x] Use repo-native registry layouts; bootstrap missing Conductor only after inspection and within accepted scope.
  - [x] Preserve the accepted specification and numbered tasks; assign one writer to each shared object.
- [x] Task A5: Phase verification and checkpoint: review ownership, duplicate search, dependency graph and exact base receipts under workflow.md.

## Phase B — Baseline, runtime and contracts (R01–R04, R11)

- [x] Task B1: Capture canonical verifier inputs/outputs and current artifact hashes in a complete checkout before changes.
- [x] Task B2: Write consumer-contract and independent-oracle tests for the approved public interfaces, including invalid/missing data and scientific invariants.
  - [x] Map current parameters, model definitions, calculation functions and execution/output owners before changing interfaces (R11).
  - [x] Write R11.1–R11.3 cases for validated parameter round-trips, invalid inputs, explicit defaults, scenario-order isolation, input immutability and calculations independent of I/O.
- [x] Task B3: Qualify repo-local Python 3.15.1 and the newest suitable dependencies in isolated environments, recording actual interpreter and package identities.
  - [x] Resolve supported incompatibilities and integrate existing runtime PRs; record genuine blockers without downgrading or bypassing.
  - [x] Align constraints, locks, active CI/helpers and Apache-2.0 metadata while preserving third-party rights and in-flight operations.
- [x] Task B4: Establish reproducible NumPy reference runs under the required runtime; preserve expected hashes and explain every mismatch before proceeding.
- [x] Task B5: Phase verification and checkpoint: run affected tests and tests/test_workstream_integration.py, then coherent full-suite/reproduction gates; retain failures and evidence.

## Phase C — Upstream capability and structured interchange (R03, R06, R11)

- [x] Task C1: Write producer and consumer acceptance cases against real installed upstream APIs before modifying them.
- [x] Task C2: Implement only missing reusable capabilities in their owning repos: VOI/cost interfaces, uptake/diffusion, extraction/citation provenance or generic simulation adapters.
  - [x] Separate scenario values, model definitions and execution settings through existing typed interfaces only where the mapping demonstrates a gap; preserve structural invariants and Rust-native ownership (R11).
  - [x] Demonstrate one bounded extension with compatibility/migration tests and unchanged reference scenarios (R11.4); do not create a generic framework.
- [ ] Task C3: Write schema, no-coercion, ordering, null/NaN, lifetime, chunking and migration/rollback tests.
- [ ] Task C4: Implement qualified Polars/Arrow/Patito/msgspec boundaries without replacing the shared evidence contract.
  - [ ] Verify buffer identity/lifetime/allocation for each zero-copy claim and distinguish logical versus raw-byte hashing.
- [x] Task C5: Wire exact upstream artifacts or editable development sources into tobac with explicit versions and independent package boundaries.
- [ ] Task C6: Phase verification and checkpoint: execute upstream native suites and tobac consumer/integration checks; retain real API/runtime receipts and changed-interface notes.

## Phase D — Numerical backends and performance (R02, R04, R07)

- [x] Task D1: Write matched-input float64 parity, nonfinite/error, state-order, tie-policy and explicit-backend tests.
- [x] Task D2: Add the opt-in JAX backend and only operation-qualified libraries, keeping NumPy the default.
  - [x] Verify x64 before arrays/JIT, actual device identity and no silent fallback.
  - [x] Add tolerance verification without weakening canonical source/evidence hashes or NumPy checks.
  - [x] Distinguish shared deterministic draws from backend-specific RNG/distribution checks.
- [x] Task D3: Write representative performance harness cases and agree measured runtime/memory budgets.
- [x] Task D4: Benchmark cold compilation, transfer and synchronised warm execution; optimise only measured bottlenecks.
- [x] Task D5: Assess mars through voiage only if warranted; otherwise record an evidenced defer decision.
  - [x] Require cross-fitting, held-out error and decision-ranking/regret checks against exact cases before surrogate use.
- [x] Task D6: Phase verification and checkpoint: execute canonical reference reproduction, JAX parity and scientific invariants with actual performance receipts.

## Phase E — Replay, clean packages and evidence/context (R05, R06, R09, R11)

- [x] Task E1: Write tests for receipt schema/version integrity, stale inputs/environments, interrupted runs and immutable prior receipts.
- [x] Task E2: Extend existing run metadata and checkpoint/recovery behavior where required; verify uninterrupted versus resumed results.
  - [x] Bind resolved parameter content, provenance, model/schema versions and execution identity into replay receipts; distinguish scenario, model and backend changes (R11.5).
- [x] Task E3: Build wheel/sdist with source overrides disabled and install outside the checkout; exercise real CLI/APIs, packaged data and dependency closure.
- [x] Task E4: Write context/acceptance tests for required-contract retrieval, source-hash and HEAD changes, incomplete evidence, ownership and untrusted source text.
- [x] Task E5: Extend existing bounded context and Conductor acceptance mapping to reject unsupported or stale completion claims.
- [x] Task E6: Phase verification and checkpoint: clean-package, replay/recovery and context tests pass with exact revisions and artifact identities; rebuild stale context.

## Phase F — CI/CD, security and test effectiveness (R04, R08)

- [x] Task F1: Reconcile the existing CI-hardening track; qualify each tool in decisions.md on the required runtime and supported platforms.
- [x] Task F2: Compare ty/pyrefly/BasedPyright diagnostics and prek hooks; retain explicit dispositions and current required checks.
- [x] Task F3: Write or select meaningful scientific mutation cases, prove imported code identity, and compare pytest-gremlins with existing mutation checks.
- [x] Task F4: Extend supported pinned actions, environment/cache controls, least privilege and source-bound locks through Nox/uv.
- [~] Task F5: Implement the security findings lifecycle, artifact-linked SBOM and downstream attestation verification.
  - [~] Retain owner, component, rationale, remediation proof and expiring exceptions; do not hide unresolved findings.
  - [~] Qualify harden-runner audit and supported egress policy without changing account entitlements.
- [ ] Task F6: Execute the ARM diagnostic lane and preserve separate architecture/numerical qualification results.
- [~] Task F7: Phase verification and checkpoint: inspect actual hosted job logs/artifacts, prove attestation verification, and promote only qualified checks; record unresolved debt.

## Phase G — Optional evidence integrations (R10)

- [x] Task G1: Evaluate a narrow offline Searchright consumer slice for record/report/study identity and search provenance.
  - [x] Write duplicate-study, lineage and schema-version tests before adding any adapter; preserve human applicability decisions.
- [x] Task G2: Consume the archive-govt-nz owner's source-binding contract; assess AegisArchive only for uncovered preservation requirements.
  - [x] Verify permitted snapshot digests, retained editions and offline replay; source capture is not extraction or likelihood approval.
- [x] Task G3: Record adopt/trial/defer decisions; upstream tracks require a concrete demonstrated gap and named consumer.
- [x] Task G4: Phase verification and checkpoint: review actual consumer evidence and rights boundaries; a justified defer can close an assessment but not an implementation claim.

## Phase H — Integrated qualification and handoff (R01–R11)

- [x] Task H1: Execute affected upstream native suites and the complete tobac suite in a complete qualified checkout, including workstream integration and numerical reproductions.
  - [x] Verify prior-work bytes, M1/M2/longitudinal/M3 canonical outputs, JAX tolerances and actual upstream execution.
  - [x] Confirm exact CLI syntax from the implemented entrypoints; the original prompt's example commands are not assumed to exist unchanged.
  - [x] Map R11.1–R11.5 to executed acceptance evidence, including parameter round-trip, isolation, I/O independence, extension compatibility and replay traceability.
- [x] Task H2: Run final clean-package, coverage, security, recovery and performance gates without counting focused/cached tests as a full run.
  - [x] Preserve per-environment pytest caches; use bounded selectors while editing and zero retries by default.
  - [x] Restrict any retry to an identified transient read-only case; never retry native mutations or sends through the test runner.
- [~] Task H3: Review final diffs and scientific assumptions, reconcile current main/issue #1, and publish only within authorised scope using guarded expected-head checks.
- [~] Task H4: Verify remote refs/files and hosted outcomes; post receiving commits, actual test scopes, interface changes and open gaps on #1.
- [~] Task H5: Phase verification and checkpoint: deliver repository paths, issue URLs, track paths, artifact identities and verification status; distinguish local, hosted, upstream and scientific acceptance.

## Review and sequencing

Critical path: A → B → C → D/E → F → H. Optional G can be assessed independently after
ownership is clear. The active archive and CI workstreams remain dependencies, not reassigned
work. No parallel agents or new chats are implied. No skill installation is needed from the
Conductor catalog reviewed for this plan.

The original registration-only approval was superseded by the owner’s explicit autonomous implementation instruction on 26 October 2026.
No phase is complete merely because this document exists.

## Current acceptance and boundaries — 26 October 2026

- A: current main/worktrees/PRs and nine upstream issue inventories inspected (gh pagination through 5,000); no duplicate producer change or owner reassignment. PR #19/#20 are closed; PR #41 remains separately owned and planning-only. The directory named voiage had an unexpected remote and was not used as producer authority; the actual installed artifact is hash-bound to the prior source/build receipt.
- B: actual Python 3.15.1, reference source/data/output baseline, parameter round-trip/schema/isolation/I/O and bounded action/scenario extension tests, full tests and numerical reproduction. Apache-2.0 metadata is aligned; re-resolved lock versions are unchanged. Reference pins remain qualified; optional latest candidates do not replace them automatically.
- C: actual installed current Voiage EVPI/JAX and strict primitive interchange probes pass. C3/C4/C6 remain open for the full producer/consumer metadata, timestamp, nullable and migration contract. Tested float64 buffer sharing is narrower than a qualified observational interchange. Voiage 3.0.0 is not published; PR #41’s distinct candidate gate is preserved. No competing shared evidence contract is introduced.
- D: weighted/permuted/offset float64 parity, actual CPU device, cold/transfer/warm endpoint and separately compiled public matmul-operand measurements. NumPy remains default; current JAX endpoint is slower, so no surrogate or speculative kernel rewrite is justified. No backend-specific stochastic equivalence is inferred.
- E: input/model/environment-bound immutable receipts; actual quick M1/M2 interruption/resume versus uninterrupted CSV comparison; real clean installed API/M1 CLI and sdist reconstruction outside checkouts; context required-contract and stale-source gates. Recovery is between stages; partial kernels are retained and rejected for unsafe resume.
- F: strict reference checks, actual ty/pyrefly/prek, 68/68 bounded gremlins detection, redacted source/script/engineering/workflow secret scans, security-disposition checks and supported pinned macOS audit/provenance jobs. Hosted artifact signing/audit and downstream verification remain pending until actually executed. F6’s non-macOS ARM execution remains in the existing roadmap; no macOS completion claim covers it.
- G: consume existing source/native contracts. No demonstrated current consumer gap warrants Innovate/Kairos/Searchright/AegisArchive adapters or new upstream tracks. This is an evidenced assessment/defer disposition, not an implemented integration. No adapter is added before duplicate-study/lineage tests or producer qualification.
- H: current local full test/security/package/reproduction and native scopes are in integration/ecosystem/verification_20261026.json. Final-head hosted checks and guarded receiving-ref readback remain pending. Issue #1 is historical context under current AGENTS.md; no comment or independent review is a gate.

Seven other bounded completed tracks are reviewed and archived in conductor/archive/index.md.
Scientific gaps remain in conductor/research-gates.md; no data or empirical parameters are invented.

## Phase: Review Fixes

- [~] Task: Apply review suggestions; record implementation commit and final hosted qualification.

Review: docs/reviews/2026-10-26-conductor-autonomous.md. Fixed coverage-store contamination,
recovery log reuse, nested unknown parameters, archive registry validation and macOS path aliasing.
