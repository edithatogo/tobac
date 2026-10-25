# Scientific ecosystem modernisation

Status: consolidated specification for plan review; not a registered or implemented track.
Date: 25 October 2026 (Australia/Brisbane).
Type: architecture refactor. Primary beneficiary: tobac.
Planning base: `59bb0e4ebaf1881158849df1702a1d3101aad58f`.

## Purpose and delivery boundary

Improve tobac's scientific reproducibility, evidence traceability, runtime performance and
maintainability through qualified libraries and engineering controls. Reusable changes belong
in their owning repository; tobac owns its domain decisions, integration and end-to-end proof.
The five original sister-repository scopes are candidates, not mandatory rewrites. Register
upstream tracks only when inspection establishes a needed capability and its proper owner.
Reuse matching tracks/issues before creating new ones. This proposal does not create tracks,
change scientific inputs, implement libraries, publish packages or qualify scientific conclusions.

The user accepted the architecture-refactor direction, the upstream ownership rule, the
expanded tool assessment and the additional recommendations. This specification incorporates
those choices; the accompanying implementation plan remains subject to Conductor review.

## Existing work and coordination

- Preserve [workstream ownership](../../../docs/WORKSTREAM_SYNC.md) and
  [the registry](../../tracks.md). M3 owns `src/tobac/research` and `tests/m3`.
- Follow [library reuse review](../../../docs/engineering/LIBRARY_REUSE_REVIEW.md),
  [readiness](../../../docs/engineering/READINESS.md) and [workflow](../../workflow.md).
- Reconcile [PR #20](https://github.com/edithatogo/tobac/pull/20), the existing advisory CI/CD
  proposal, before adding engineering tasks. It is not on this planning base; do not duplicate
  it or assume its configuration has executed. Preserve its owner's branch.
- Coordinate runtime/lock work with [PR #19](https://github.com/edithatogo/tobac/pull/19).
  An open PR or prior canary is not Python 3.15 qualification of the final dependency set.
- The [archive source-binding workstream](https://github.com/edithatogo/tobac/issues/1#issuecomment-6397394234)
  owns archive-govt-nz mappings and tobac archive references. Consume that contract; do not
  create a competing source registry or duplicate capture. AegisArchive is an optional engine
  assessment only where the existing route has a demonstrated gap.
- This [planning scope declaration](https://github.com/edithatogo/tobac/issues/1#issuecomment-6397463739)
  owns only this proposal directory. Re-read issue #1 and main before registration/publication.

## Requirements and acceptance criteria

### R01 — Runtime, packaging and rights

Every active Python path must use an explicitly selected repo-local Python 3.15 interpreter,
currently 3.15.1 as required by the user, verified by execution. Qualify the newest suitable
patch and dependencies before promotion. Align constraints, locks, Nox, CI, containers,
helpers and setup instructions; remove older active compatibility/default runners at cutover.
Preserve historical evidence and an in-flight environment until its operation terminates.
No downgrade or unsupported build bypass resolves a blocker. Preserve existing reference
results and hashes if runtime/dependency qualification fails; record the unresolved gate.
Project-owned code uses complete Apache-2.0 terms and aligned package/NOTICE metadata;
retain third-party terms and separate source-document/data rights.

### R02 — NumPy reference and JAX qualification

Default `--backend=numpy` with `OPENBLAS_NUM_THREADS=1` preserves every existing canonical
SHA-256 assertion in the reference verifiers. Capture the exact baseline artifact set,
serialization, runtime and BLAS identity before changes. Do not rewrite expected hashes to
accept drift. Separate stable scientific output hashes from variable run metadata.

JAX is explicit and optional. Enable `jax_enable_x64` before creating arrays or compiling;
verify actual dtypes, device and backend. Deterministic matched-input comparisons require
`rtol=1e-12`, `atol=1e-12`, shape/order checks and explicit nonfinite handling. Evidence/source
hash verification stays exact in tolerance mode. Stochastic paths use shared frozen draws
where meaningful and separate distributional/convergence checks; a matching seed alone does
not imply matching NumPy/JAX random streams. Missing JAX must fail explicit JAX requests,
never silently fall back. Qualify each named JAX library against a needed operation before
adding it; do not substitute approximate inference for an exact finite calculation.

### R03 — Producer–consumer and data contracts

Extend the existing Scope/EvidencePacket/state identity contract. Preserve population, physical
product basis, units, dates, covariance, missingness, ordering and source identity. Forecasts
and posteriors remain distinct from observations; condition shared MOH/NZHS data once.
Test consumer compatibility against exact producer revisions and installed artifacts, including
weighted states, structures, shared portfolio costs, invalid inputs and schema evolution.
Record API/schema versions and migration/rollback rules without creating another VOI engine.

Polars/PyArrow/Patito/msgspec are candidates for supported boundaries. Test no-coercion behavior,
nulls versus NaNs, timestamps, chunking and metadata preservation. Arrow `__arrow_c_stream__`
zero-copy claims require buffer ownership, lifetime and allocation evidence on the actual path.
Distinguish byte-buffer hashes from canonical logical-content hashes; record the canonicalization
version and do not expect different valid chunk layouts to have identical raw bytes.

### R04 — Independent scientific test effectiveness

Extend small independent reference oracles and affected tests before changing semantics.
Cover simultaneous state/data permutation, equivalent unit transformations, normalisation,
nonnegative information value and EVSI/EVPI bounds under their stated assumptions, data-once
conditioning, shared-cost accounting and near-tie decisions. Test error paths and boundaries.
Mutations must touch the code actually imported; retain source/import identities and first
failures. Compare pytest-gremlins with existing mutmut and targeted scientific mutations in a
Python 3.15 environment before adoption; no mutation score substitutes for scientific review.

### R05 — Run identity, replay and recovery

Extend existing receipts with source/config/data hashes, producer revisions, lock identities,
Python/library versions, BLAS/XLA configuration, architecture/device, precision, RNG algorithm
and streams, command, exit status and artifact identities. Separate deterministic content
from timestamps/host paths. Completed receipts are immutable and schema-versioned.
Verify replay and interrupted-run recovery where long-running execution warrants checkpoints;
reject stale or incompatible checkpoint inputs, schemas and environments. Never count a partial
run as a complete replay or overwrite a previous receipt during a rerun.

### R06 — Clean-package and cross-repository release qualification

Use editable/workspace sources for development only. Build source distributions and wheels;
check builds with `uv build --no-sources`, then install and exercise artifacts in a clean
environment outside source/sibling checkouts. Verify imports resolve to the installed artifact.
For unreleased upstream packages use explicitly identified built artifacts and record that
boundary; registry resolution remains open until those releases exist. Check dependency and
licence closure, exported APIs, packaged schemas/data and source-distribution reconstruction.
Keep independent repositories independently versioned; a workspace must not become an
undeclared distribution requirement. Preserve upstream native bindings.

### R07 — Measured performance

Define representative small/exact and large workloads before optimisation. Measure accuracy,
wall time and peak memory; record hardware, threads and cache state. For JAX separate compile,
transfer and warm execution and synchronise completion. Agree baseline-derived regression
budgets before implementation; no arbitrary unmeasured speedup promise. Rust/GPU kernels and
mars surrogates require a demonstrated bottleneck and decision-relevant parity/error evidence.

### R08 — CI/CD, quality and security management

Assess every tool in decisions.md as adopt, trial, retain-existing or defer with evidence.
Nox remains the task orchestrator; uv manages qualified environments and locks. Existing gates
stay effective. New diagnostic tools begin advisory and gain required status only with a
reviewed scope, demonstrated reliability, actionable diagnostics and recorded promotion.
Avoid making three overlapping type checkers mandatory without demonstrated incremental value.

Use least privilege, pinned actions, safe untrusted-PR boundaries, deliberate cache identities,
retained logs and reproducible build inputs. Track vulnerabilities/findings with an ID, owner,
affected component/artifact, severity/rationale, disposition, fix verification and expiry for
exceptions. SBOMs describe actual artifacts. Verify attestation subject digests and identity;
installing an attestation action alone does not establish a SLSA level or reproducible build.
Assess harden-runner support/entitlements and egress audit before a supported blocking policy.
Qualify ubuntu-24.04-arm independently; it does not replace the canonical reference platform.

### R09 — Context and acceptance evidence

Extend the existing bounded context builder and Conductor records. Map acceptance IDs to
owned paths, tests/native commands, expected evidence, actual exit/results and source revisions.
Detect stale HEAD/content, missing artifacts, incomplete required checks and status claims
above the evidence obtained. Test context selection against a small task corpus with required
contracts and budget limits; test source changes, ownership boundaries and untrusted retrieved
text. Do not add a generic agent framework, background worker or automatic track promotion.

### R10 — Optional ecosystem integrations

Assess Searchright for search/update provenance and record–report–study identity, preserving
CiteWeft's extraction and Sourceright's citation-integrity ownership. tobac retains applicability,
parameter extraction and likelihood decisions. Audit a narrow offline consumer slice first.
Source/README claims do not qualify downstream runtime or scientific use.

Assess AegisArchive through the existing archive-govt-nz/source-binding owner for permitted
source snapshot preservation, digests and offline replay where needed. Capture date, source
edition and extraction version remain separate. No duplicate crawler or automatic evidence
refresh is implied. Retain earlier snapshots and unresolved source rights.

Assess mars through voiage only if profiling justifies a surrogate: cross-fitting, held-out
error, decision-ranking/regret assessment, edge cases and comparison with exact calculations
are required. Keep exact reference behavior available; training fit alone is insufficient.

Reuse rac-conformance's independent-oracle and named-consumer design patterns without adding
its policy domain as a runtime dependency. Reusable engineering improvements may later be
proposed to the user's templates after qualification in real consumers; inspect their runtime,
licences and ownership first. No universal template rollout is part of this work.

## Out of scope and completion rule

No empirical calibration, new observed-data claim, publication, deployment, new account or
security entitlement, visibility change, runtime Rust-to-Python rewrite, autonomous background
monitoring, or unconditional adoption of every library. Scope changes remain explicit.

Completion requires current producer and consumer receipts, canonical reproduction, full
integration/clean-package/security gates at coherent milestones, verified hosted outcomes for
changed workflows and remote readback for published changes. A declared capability, fixture,
track checkbox or agent acknowledgment cannot close a runtime or scientific gate. Optional
assessments can close with an evidenced defer decision; they cannot be marked implemented.
