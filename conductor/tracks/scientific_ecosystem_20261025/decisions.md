# Ownership and candidate decisions

This is an assessment plan, not a statement of qualification. Read with [spec.md](spec.md)
and [plan.md](plan.md). Exact upstream revisions, local paths, full issue inventories,
scoped instructions and capabilities must be rechecked before track registration there.

## Repository placement

| Repository | Proposed responsibility | Disposition |
| --- | --- | --- |
| tobac | Domain semantics, end-to-end contracts/replay, reference hashes, integration and consumer qualification | Primary owner; master track after plan approval |
| voiage | Reusable weighted/structure-only VOI, shared portfolio costs, array backend contracts | Extend current M3/upstream work after capability audit |
| sourceright | Citation integrity; supported structured interchange at its public boundaries | Assess Arrow/schema need against native APIs; no generic Python data layer forced into Rust |
| citeweft | Scholarly extraction provenance and supported CLI receipts | Extend extraction contracts where needed; general evidence preservation remains with its current owner |
| innovate | Generic uptake/diffusion and fitting interfaces | Qualify existing models, then optional JAX adapters; preserve model semantics |
| kairos | Rust-first generic simulation mechanisms and native bindings | Preserve Rust core; assign timing/decision logic only after semantic fit review; Equinox is not a mandated core rewrite |
| searchright | Optional search provenance, records/reports/studies and reusable evidence contracts | Narrow offline assessment; no whole search platform adoption |
| archive-govt-nz | Existing source capture inventory and provenance mappings | Active owner; dependency of this proposal, not a new duplicate track |
| aegisarchive | Optional archival engine and WARC integrity/replay | Assess via existing archive workstream only for a demonstrated gap |
| mars | Optional reusable VOI surrogate through voiage | Deferred until profiling and decision-error qualification justify it |
| rac-conformance | Independent-oracle and named-consumer design precedent | Reuse patterns; no new runtime dependency |
| template-solo-python / template-solo-rust / conductor-next | Potential later homes for demonstrated generic engineering improvements | Inspect only when a concrete reusable change exists; no blanket rollout or tool replacement |

## Engineering tools

| Candidate | Initial treatment | Qualification / promotion condition |
| --- | --- | --- |
| astral-sh/setup-uv; uv | Retain existing and improve | Explicit runtime, locked installs, source-bound receipts and independent clean build/install |
| astral-sh/ruff-action; ruff | Reuse/extend existing scope through PR #20 | Action and local tool version/config parity; fix real failures; preserve baseline debt |
| j178/prek (and its supported action) | Trial | Existing hooks execute equivalently on Python 3.15; hooks and binaries are pinned; no unnoticed scope changes |
| ty; pyrefly; basedpyright | Retain existing BasedPyright scope; compare newer diagnostics | Real imports and supported Python syntax; measure useful unique findings and noise before selecting required gates |
| actions/attest-build-provenance | Trial on real built artifacts | Check current action support, permissions/entitlements, subject hashes and downstream verification; name only a proven SLSA level |
| step-security/harden-runner | Qualified audit first | Supported runner and entitlement; measured egress; explicit justified allowlist before blocking |
| zizmorcore/zizmor-action; zizmor | Reuse and align | Identical local/hosted policy, reviewed actionable findings, pinned executable/action |
| pypa/gh-action-pip-audit; pip-audit | Reuse and align | Actual supported dependency inventory; distinguish runtime/build/dev exposures; retained finding lifecycle |
| helpers:pinGitHubActionDigests | Retain existing Renovate preset | Full immutable action references, reviewed updates and no automatic scientific dependency promotion |
| ubuntu-24.04-arm | Trial platform lane | Python 3.15 package/BLAS/native-binding availability, real hosted execution and numerical comparison |
| pytest-gremlins | Trial against existing mutation approaches | Actual Python 3.15 install/execution, pytest/plugin compatibility, correct import path, meaningful killed/surviving mutations and measured cost |
| Existing gitleaks, SBOM, security and packaging checks | Preserve/reconcile | Avoid duplicate jobs; record findings, owners, fixes, artifact identity and expiry of exceptions |

Candidate scientific packages remain purpose-qualified: array-api-compat, Polars, PyArrow,
Patito, msgspec, JAX, Equinox, Optimistix, Lineax, Quadax, Interpax, Diffrax, BlackJAX,
jaxtyping and beartype. A resolver success or import smoke is not numerical qualification.
Use the smallest set that implements approved requirements, with documented defer decisions
for packages whose semantics or Python 3.15/native support do not fit.

## Evidence basis for the proposal

Current repository instructions, main and coordination issue were inspected. The upstream
README assessment is discovery evidence, not an executed capability audit:

- [Kairos Rust-first boundary](https://github.com/edithatogo/kairos/blob/main/README.md)
- [Searchright evidence contracts and maturity limits](https://github.com/edithatogo/searchright/blob/main/README.md)
- [AegisArchive capture/replay scope](https://github.com/edithatogo/aegisarchive/blob/main/README.md)
- [mars beta and portable model scope](https://github.com/edithatogo/mars/blob/main/README.md)
- [RaC conformance design precedent](https://github.com/edithatogo/rac-conformance/blob/main/README.md)
- [Python template baseline requiring reconciliation](https://github.com/edithatogo/template-solo-python/blob/main/README.md)
- [uv clean build guidance](https://docs.astral.sh/uv/guides/package/)
- [JAX benchmark methodology](https://docs.jax.dev/en/latest/201/profiling.html)
- [pytest-gremlins documentation](https://pytest-gremlins.readthedocs.io/en/latest/)
