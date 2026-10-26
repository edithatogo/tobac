# Bounded macOS ecosystem qualification

This implementation preserves the NumPy reference model, parameters, data and published
results. It adds software contracts and actual native execution, not an empirical posterior.
Conductor's earlier implementation hold was released by the owner's autonomous implementation,
review, fixes and archival instruction on 26 October 2026.

## Existing interfaces and ownership

`tobac.parameters` serializes the existing validated regulatory config in a versioned,
content-hashed envelope. Units, assumptions, rationales and scenario values are preserved;
unknown root/constant/measurement/event/axis fields and nonfinite values are rejected.
The model schema is explicit. There is no coercing or executable configuration language.
Observation covariance and provenance remain in the existing evidence/supply contract;
this M1 config envelope does not create another observation contract.

`tobac.backend.evpi(problem, backend="numpy")` retains the reference calculation.
An explicit `backend="jax"` uses the qualified Voiage compatibility artifact's public JAX
EVPI implementation on M3's existing exact weighted transform. It enables and checks float64;
missing/unqualified libraries fail. This is EVPI only, not generic EVSI or structural APIs.
The default reference runners and their scientific outputs are unchanged.

The installed Arrow/Polars probe establishes float64 buffer sharing and lifetime on the tested
column path, logical chunk-content preservation, Patito type rejection and strict msgspec
numeric decoding. It does not qualify arbitrary metadata/timestamp/null semantics, a new
observational ingress or Voiage 3.0.0. That producer release is absent from PyPI at inspection.
PR #41 owns its distinct migration plan; its worktree and contents are preserved. The directory
named voiage inspected during discovery had an unexpected astro-polyglot remote, so it was not
used as authority for a producer revision. The actual wheel is hash-bound to its prior native
source/build receipt. No upstream source, native binding or existing owner was modified.

## Replay and clean packages

```sh
uvx --python 3.15.1 --from nox==2026.10.20 nox -s tests strict_all reproduce security clean_package
.nox/tests/bin/python -m tobac.replay --out /path/to/NEW-run --stages m1 m2 m3
.nox/tests/bin/python -m tobac.replay --out /path/to/same-run --stages m1 m2 m3 --resume
```

Use the explicitly selected repo-local Python 3.15.1 for direct commands. Replay identities
separate config/data hashes, package source hashes, lock identities and execution environment
(Python/libraries, architecture, BLAS configuration, threads, precision and backend). Completed
stage receipts and logs are immutable. Checkpoints can advance; incompatible input, environment
or option changes are rejected. Resume skips only verified completed stages. An interrupted
kernel's existing output is retained and requires a new run directory; this is stage-boundary
recovery. Native quick M1/M2 interrupted/resumed and uninterrupted CSVs matched exactly.

Clean-package qualification uses `uv build --no-sources`, reconstructs a wheel from the sdist,
then hash-syncs dependencies in an environment outside the source/sibling checkouts. It proves
imports resolve to the installed wheel, executes the API and real quick M1 CLI with explicitly
supplied config inputs, and retains commands, failures and artifacts. This is not a claim that
research data/configs are bundled defaults in the distribution. Apache-2.0 package metadata and
complete licence/notice files align project-owned code; existing source/data provenance and
third-party rights remain separate. Re-resolved lock versions are unchanged.

## Optional native qualification

```sh
uvx --python 3.15.1 --from nox==2026.10.20 nox -s ecosystem -- /path/to/qualified-macos-voiage.whl
```

This session checks the wheel digest against the retained compatibility-build receipt and
hash-syncs its separate ecosystem lock. The reference lock remains unchanged in versions.
The actual JAX, Arrow, Polars, Patito and msgspec versions/devices are in the execution receipt.
The Polars pin remains compatible with the existing qualified producer; an initial latest
candidate install is not its downstream qualification.

JAX parity passes at rtol=atol=1e-12 for weighted, zero-weight, permuted and large-offset cases.
Measured 4,096/262,144-state workloads retain NumPy as default: the Voiage JAX endpoint was slower
on both. Host transfer, cold/warm producer operations and a separately lowered/compiled public
JAX matmul operand are measured; the operand compile measurement is not presented as whole-VOI
compilation. Peak RSS is process-wide, not a per-array GPU allocator measure. No mars surrogate,
new statistical engine or speculative optimisation is warranted by these measurements.

## Security and test effectiveness

The existing required audits remain fail-closed. The findings registry supplements scanning;
open findings, expired exceptions and closure without matching artifact proof fail validation.
No finding is concealed by an empty registry. Actual pip-audit/SBOM, zizmor and bounded redacted
gitleaks scans are retained. Completed fixed findings need owner, component, rationale,
verification and exact artifact identities. Security exceptions expire.

The pinned macOS provenance job is limited to trusted main pushes or explicit dispatch; it
retains read-only contents, narrowly scoped OIDC/attestation writes and disabled checkout
credential persistence. Harden-Runner uses supported public-repository macOS audit mode.
An installed action is not signed-artifact or egress-blocking proof: actual hosted execution and
downstream attestation verification remain separate gates. No SLSA level is asserted.

Ty/Pyrefly and prek were executed on qualified imports. BasedPyright remains required; no
redundant checker was promoted. Existing hook versions now match the required tools and an
executed runtime hook enforces 3.15.1. The fresh gremlins campaign detects 68/68 mutations in
its bounded supply target after adding independent domain/accounting assertions. This is not
the same denominator as the older 100/131 mutmut result. Reference coverage gets a unique
per-run data store so mutation statement coverage cannot contaminate branch coverage.

## Remaining boundaries

Voiage 3.0.0/Polars producer-consumer qualification, full metadata/timestamp/nullable ingress,
non-macOS/ARM qualification and empirical applicability remain explicit. Optional Innovate,
Kairos, Searchright and AegisArchive integration assessments identified no required new adapter
for the current finite decision and source-handoff use cases. Existing native/source owners are
retained; no duplicate capture, search service, upstream track or background automation is added.
Open scientific requirements are in conductor/research-gates.md. See the active plan, review
report and integration/ecosystem/verification_20261026.json for the actual scopes and results.
