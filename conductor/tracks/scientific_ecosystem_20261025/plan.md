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
- [x] Task C3: Write schema, no-coercion, ordering, null/NaN, lifetime, chunking and migration/rollback tests.
- [x] Task C4: Implement qualified Polars/Arrow/Patito/msgspec boundaries without replacing the shared evidence contract.
  - [x] Verify buffer identity/lifetime/allocation for each zero-copy claim and distinguish logical versus raw-byte hashing.
- [x] Task C5: Wire exact upstream artifacts or editable development sources into tobac with explicit versions and independent package boundaries.
- [x] Task C6: Phase verification and checkpoint: execute upstream native suites and tobac consumer/integration checks; retain real API/runtime receipts and changed-interface notes.

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
- [x] Task F5: Implement the security findings lifecycle, artifact-linked SBOM and downstream attestation verification.
  - [x] Retain owner, component, rationale, remediation proof and expiring exceptions; do not hide unresolved findings.
  - [x] Qualify harden-runner audit and supported egress policy without changing account entitlements.
Deferred to conductor/roadmap.md: F6 — ARM diagnostics are outside current macOS development; no execution claimed.
- [x] Task F7: Phase verification and checkpoint: inspect actual hosted job logs/artifacts, prove attestation verification, and promote only qualified checks; record unresolved debt.

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
- [x] Task H3: Review final diffs and scientific assumptions, reconcile current main/issue #1, and publish only within authorised scope using guarded expected-head checks.
- [x] Task H4: Verify remote refs/files and hosted outcomes; post receiving commits, actual test scopes, interface changes and open gaps on #1.
- [x] Task H5: Phase verification and checkpoint: deliver repository paths, issue URLs, track paths, artifact identities and verification status; distinguish local, hosted, upstream and scientific acceptance.

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
- C: C3/C4/C6 domain interchange is implemented and qualified against Voiage 2.2.0+tobac3151.1. Full source/state/scope/covariance/supply provenance, UTC/null capture times, strict schema/order, lifetime/chunking, logical/physical hashes and retained-v1 rollback checks pass. PR #41 remains a separately owned future migration; no Voiage 3.0 acceptance is inferred.
- D: weighted/permuted/offset float64 parity, actual CPU device, cold/transfer/warm endpoint and separately compiled public matmul-operand measurements. NumPy remains default; current JAX endpoint is slower, so no surrogate or speculative kernel rewrite is justified. No backend-specific stochastic equivalence is inferred.
- E: input/model/environment-bound immutable receipts; actual quick M1/M2 interruption/resume versus uninterrupted CSV comparison; real clean installed API/M1 CLI and sdist reconstruction outside checkouts; context required-contract and stale-source gates. Recovery is between stages; partial kernels are retained and rejected for unsafe resume.
- F: strict reference checks, actual ty/pyrefly/prek, 68/68 bounded gremlins detection, redacted source/script/engineering/workflow secret scans, security-disposition checks and supported pinned macOS audit/provenance jobs. Prior final-main artifact signing/audit and downstream verification passed; the current publication still requires its own hosted readback. F6’s non-macOS ARM execution remains in the existing roadmap; no macOS completion claim covers it.
- G: consume existing source/native contracts. No demonstrated current consumer gap warrants Innovate/Kairos/Searchright/AegisArchive adapters or new upstream tracks. This is an evidenced assessment/defer disposition, not an implemented integration. No adapter is added before duplicate-study/lineage tests or producer qualification.
- H: current local full test/security/package/reproduction and native scopes are in integration/ecosystem/verification_20261026.json. Final-head hosted checks and guarded receiving-ref readback remain pending. Issue #1 is historical context under current AGENTS.md; no comment or independent review is a gate.

Seven other bounded completed tracks are reviewed and archived in conductor/archive/index.md.
Scientific gaps remain in conductor/research-gates.md; no data or empirical parameters are invented.

## Phase: Review Fixes

- [x] Task: Apply review suggestions f617307 and 5bc6ae9; final hosted qualification remains in H3/H4.

Review: docs/reviews/2026-10-26-conductor-autonomous.md. Fixed coverage-store contamination,
recovery log reuse, nested unknown parameters, archive registry validation and macOS path aliasing.

## Publication and native close-out

PR #43 merged at `a9e247416fe71932118ca92b1b04e93cb8e42267` after 15 successful checks and one expected PR-only provenance skip. Trusted dispatch `40315911202` passed all six engineering jobs, including audit/provenance. All four signed subjects passed exact-source/ref/workflow downstream verification. Hosted macOS: 838 passed, four capability skips, 92% coverage; mutmut 102/131 killed. No SLSA level or empirical qualification is inferred.

At the PR #43 checkpoint C3/C4/C6 remained unchecked. The later close-out below implements the domain contract against the current qualified producer, while retaining PR #41 separately. Final receiving-ref checks are read back on GitHub and linked from PR #43.

## Managed dependency graph follow-up

- [x] Add and verify the supported Python 3.15.1 resolved-lock snapshot submission route; retain the root managed parser's upstream runtime failure explicitly. Native run 40316535031 supports only through Python 3.14 and cannot satisfy the unchanged package constraint. No check or security setting is waived.

PR #44 merged at `0940c595ce06f4142467de3f687dea881dae8ea2` after 15 successful PR checks and two expected trusted-write skips. Native default-branch snapshot `114186314` returned SUCCESS; 113 submitted PURLs appear in the 123-PURL native export, with every previous PURL retained. Receipt: `integration/ecosystem/dependency-submission_20261026.json`.

- [ ] External service gate: managed root Dependabot parser Python 3.15 support (upstream issue 16524). The supported submission route is qualified; the failed managed run is not hidden or called successful.

## Implementation resume — 26 October 2026

Implement domain-owned transport against the currently qualified producer and installed artifacts. The original specification does not require Voiage 3.0.0; its separate future migration in PR #41 is preserved. Full metadata, covariance provenance, timestamp/null, ordering, chunking, schema evolution and ownership tests precede implementation. No prior, observation or published numerical result changes.

## C3/C4/C6 implementation and review close-out — 26 October 2026

Implemented in c347f82 against the current qualified Voiage 2.2.0+tobac3151.1
artifact, preserving PR #41's separate Voiage 3 migration. Domain transport lives
in src/tobac/interchange.py and reuses EvidencePacket, Scope and SupplyBasis.
No existing scientific contract or M3 implementation changed. Strict metadata,
UTC/null timestamps, covariance provenance, ordering, dtype, chunking, caller
isolation, buffer lifetime/effective addresses, logical/physical hashes and
unsupported-version/retained-IPC rollback cases execute in 36 native tests.

Local full suite: 880 passed, five real capability skips, 92% branch coverage.
Native transport/workstream/M3: 97 passed, zero skipped. Ruff ALL/BasedPyright:
zero diagnostics. Actual numerical reproduction, security audit and clean
wheel/sdist/API/IPC/M1 checks passed. All original reference baseline hashes match.
Other workstream's iniconfig 2.3.1 and pluggy 1.7.0 merges are retained; all four
locks are genuinely regenerated against their canonical inputs.

Review: docs/reviews/2026-10-26-evidence-interchange.md. Execution:
integration/ecosystem/interchange_20261026.json. Hosted final-head checks and
receiving-ref verification follow publication; no unexecuted job is called passed.

- [x] Task: Apply interchange review fixes c347f82 (metadata sidecar, canonical
  decoding, supply scope match, sliced buffer offsets and canonical dependency pins).

Only the external managed Dependabot Python 3.15 service gate remains unchecked.
Do not archive this track as fully complete while that gate remains open. No new
completed track is awaiting archival; the seven prior archives remain preserved.

Current-main reconciliation also retains pandas 3.1.0, Pygments 2.21.0 and pytest
9.1.1 from PRs #36/#45/#46. The combined pandas/Pygments checkout passed the full
880-test/92% suite, strict checks, reproduction, clean-package and security gates.
The final full suite with pytest 9.1.1 also passed: 880 tests, five real capability
skips, 92% coverage. Native producer/workstream/M3 tests passed 97/97 with the
final locks. Hosted checks must qualify the final PR head before merge. The root managed parser still fails on Python 3.15 (run 40325526891);
engineering-directory graph run 40326897087 passed but does not close that root gate.

Publication: PR #47. All local implementation, review and reconciliation evidence
is recorded above; exact-head hosted results are required before guarded merge.

Hosted qualification: PR #47 head a702ac571aba59cf53146efd4678c9deeb7a75e6
passed all 15 executable PR checks, including full macOS Python 3.15.1
qualification; two trusted-write jobs are intentionally main/dispatch-only.
Downloaded macOS JUnit/coverage: 880 passed, five capability skips, 91.8033%
branch-inclusive coverage (displayed 92%). The freshly built native Voiage wheel
and domain interchange receipt pass, with the exact adapter source hash retained.
The final receipt-only update receives the same checks before guarded merge.
Receiving ref and trusted default-branch jobs are linked from PR #47. The external
root-parser gate remains open; no new track is falsely archived as complete.

## Polars 2 upgrade follow-up — 27 October 2026

PR #48 initially updated two declarations without regenerating source-bound
locks and left the Voiage/ecosystem inputs pinned to Polars 1.44.2. The existing
Voiage compatibility wheel also required polars<2. Align all declared profiles
on 2.0.0, regenerate four locks, and qualify a new metadata-only Voiage
2.2.0+tobac3151.2 build from the unchanged pinned source. Original .1 evidence
remains immutable. No numerical implementation, parity tolerance, security gate
or Python 3.15.1 requirement changes.

- [x] Implement, review and locally qualify the Polars 2 fix c8ca3cf: 882 passed,
  five capability skips, 92% coverage; 99 native producer tests and all six local
  Nox gates passed. Hosted macOS and all existing PR checks remain required
  before guarded merge; the receiving ref and actual outcomes are linked from PR #48.

Review: docs/reviews/2026-10-27-polars2-pr48.md. Artifact and verification:
integration/voiage_polars2_compatibility_20261027.json. The root managed parser
service gate remains open; no track is falsely archived or check waived.

## Renovate provider policy — 27 October 2026

- [x] Explicitly retain Renovate as the sole update-PR provider; cover all four
  .in profiles, group compatibility-sensitive transport libraries, preserve
  manual merge/release-age/SHA controls and expand manual lock candidates to
  all four profiles with an actual Python 3.15.1 assertion.

Native Renovate 44.186.4/Node 24.11.0/RE2 validation and extract-only detection
passed. Local tests: 884 passed, five capability skips, 92% coverage; quality
and security passed. Receipt: integration/renovate_policy_20261027.json.
No security or visibility setting changes. The internal managed graph parser
is distinct from the update bot and remains an external gate; switching update
policy is not evidence that it supports Python 3.15. All existing hosted checks
and the four-profile candidate workflow must pass before guarded publication.

## Ruff coverage and resource controls — 27 October 2026

- [x] Implement and self-review Ruff/resource controls in commit 8a444b6.
- [x] Extend ALL-rule linting and stable formatter checks to tests and Nox tooling;
  provide root discovery, document pytest-specific exceptions and qualify five
  exact preview rules with real counterexamples.
- [x] Fix findings, strengthen 153 exception contexts, preserve source formulas,
  reference inputs and Python 3.15.1; self-review the large mechanical diff.
- [x] Add macOS process-group RSS/time budgets, termination/descendant cleanup,
  two-worker mutation limits and real memory/cleanup tests; no leak claim from
  snapshots or successful tests alone.
- [x] Local tests: 903 passed, five skips, 92% coverage; all nine Nox sessions
  qualified, plus nine real Ruff policy tests. Mutation: 114/131 killed. Receipt:
  integration/ruff_resource_controls_20261027.json.
- [x] Publish the reviewed implementation as [PR #51](https://github.com/edithatogo/tobac/pull/51).
  Required hosted and receiving-main verification, guarded merge identity and
  final execution results are maintained in that PR publication record.
  This dated local-acceptance entry does not assert an unexecuted hosted job.

Policy: docs/engineering/RUFF_POLICY.md. Review:
docs/reviews/2026-10-27-ruff-and-resource-controls.md. The existing external
managed-parser gate remains open; this scope does not archive the active track.
