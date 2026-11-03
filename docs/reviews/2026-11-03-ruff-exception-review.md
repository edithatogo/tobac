# Source Ruff exception review — 3 November 2026

Scope: project-owned `src/**/*.py` and `.pyi` under the current root `ruff.toml`,
Ruff 0.17.3, Python 3.15.1; not a review of generated output or vendored code.
`ruff check --ignore-noqa --output-format json src` found 91 diagnostics suppressed
at 66 source lines before this review. Multiple codes can apply to one line.
The normal configured source check passes. All 91 remain after the proposed
refactor described below was reverted. These are current observations, not the
historical 175-exception count.

| Retained diagnostics | Count | Decision |
| --- | ---: | --- |
| TRY004 | 17 | Preserve established `ValueError` validation behavior for evidence and longitudinal input contracts; converting exception type would change callers' observable behavior. |
| TRY003, EM101, EM102 | 26 | Preserve inherited exception construction and messages in the independently AST-verified `_core.py` extraction. |
| PLR0913, PLR0917 | 16 | Preserve explicitly dimensioned public arguments and positional compatibility; packaging them into an object or forcing keywords would change interfaces. |
| C901, PLR0912, PLR0915 | 13 | Retain the remaining complex runners, validation and replay flow after review: splitting scientific/control-flow and failure handling requires its own semantic change and verification, not a lint-only claim. |
| PLC0415 | 5 | Preserve deferred optional imports, backend selection and package import behavior. |
| T201 | 4 | Retain direct CLI output, which is an existing user-facing interface. |
| FBT001, FBT002, FBT003 | 5 | Preserve public positional flag semantics and JAX's positional configuration call. |
| TRY301 | 2 | Preserve ordered qualification and failure receipt handling; helper extraction solely to move raises does not improve the evidence contract. |
| N818 | 1 | Preserve the inherited public `LibraryUnavailable` exception name and extraction provenance. |
| S603 | 1 | Retain the explicitly reviewed shell-free replay subprocess boundary. |
| BLE001 | 1 | Retain the research qualification boundary that records failure or blocked status rather than reporting success; it is not a silent fallback. |

`choose_vintage` is one above the complexity threshold. A trial extraction of its
identity-validation loop preserved validation order and messages and removed the
C901 diagnostic without changing its public signature.
The existing focused selection passed 79 tests and `strict_all` passed, but the
qualified native lineage preflight rejected the modified source hash as stale.
Renewing the scientific lineage for this lint-only change is disproportionate, so
the helper was reverted and its C901 exception retained. The original extraction
in `src/tobac/_core.py`, the shared evidence contract, M3 interfaces and lint
policy remain unchanged. Optional backend or scientific scope is not newly
qualified by this review.

After restoration, bounded `nox -s tests` passed 1,229 tests, with seven
capability skips and 92% branch coverage; bounded `nox -s strict_all` passed
Ruff policy fixtures, lint, formatting and BasedPyright with zero diagnostics.
The accepted scientific source is byte-identical to DH1 commit `6ed27af`, whose
numerical and clean-source publication replays passed on this checkout. These
results are local and do not assert a new hosted qualification.
