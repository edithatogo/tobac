# Library reuse and engineering review

Dylan A Mordaunt | 24 October 2026 | Base: bb81a4bd596b2560a85e0cd10e9f9c8656408492

This targeted review inspected the live repository tree, scientific supply/evidence/configuration
interfaces, longitudinal implementations, declared dependencies, workflows and issue #1/#4.
The local test checkout is scoped and hash-matched, not a clone of every live file. Repository
facts below differ from recommendations and externally documented library capabilities.

## Decisions, not dependency accumulation

| Existing responsibility | Maintained alternative | Decision and acceptance condition |
|---|---|---|
| Hand-written Gaussian reporting density in tobac.supply | scipy.stats.multivariate_normal.logpdf with Covariance.from_cholesky | Implemented. Preserve the SPD and physical-domain checks and one-output-per-state shape. Tiny positive eigenvalues must not acquire a new pseudo-inverse cutoff. Tests retain the old formula as an independent oracle. |
| Finite EVPI, partition information, exact finite outcomes | Dylan's voiage, NumPy/SciPy | Retain small exact reference calculations. M3 owns the weighted voiage adapter. Require installed-library execution, weighted/state-order parity and equivalent error/normalisation semantics before replacing a production path. Do not approximate small exact cases with a surrogate. |
| Small integrated Gaussian/random-walk and bounded-grid model | NumPyro/JAX; statsmodels state-space for independent comparisons | Defer wholesale migration. Existing scipy.linalg/optimize/special do the numerical work. A toolkit with different priors/kernel/likelihood is a structural alternative, not a drop-in equivalent. Use NumPyro plus ArviZ when raw repeated, censored, hierarchical observations justify it; qualify posterior recovery, diagnostics and runtime first. |
| Time/source/units/identity, inventory and lawful-channel accounting | Pydantic/Pandera/Pint and schemas | Retain domain invariants. Add schema validation at new machine-ingress boundaries; JSON Schema is used for context profiles now. A dimensional-units package cannot verify population, period, RYO convention or once-only MOH/NZHS evidence. Plan tabular schema migration with no-coercion tests before accepting it. |
| Costly nested VOI regression | Dylan's mars-earth/pymars or established sklearn estimators | Conditional candidate only, not installed. The repository identifies active beta status. Use cross-fitting and independent decision/regret error, not training R-squared, before adoption. |
| Citation identity/extraction | Dylan's Sourceright/CiteWeft | Keep existing genuine executable qualification jobs. Structural CSL validity is not DOI/provider resolution, claim support, numerical extraction or empirical applicability. Do not replace missing executions with a similarly named local helper. |
| Custom task/environment orchestration | Nox with uv | New isolated sessions and bounded workflows; nox/uv are tools, not another scientific inference layer. Local and hosted macOS Nox/uv lock verification, numerical replay and clean-package execution are qualified; current receipts are in Conductor. |
| Handwritten property/mutation harnesses | Hypothesis, mutmut, pytest/coverage | Retain real property tests and bounded mutmut campaigns. Local and hosted macOS Hypothesis/mutmut execution is qualified; dated mutation measurements retain their exact scope and denominator. No mutation score is fabricated. |
| Performance guesses / blanket Rust rewrite | Scalene; existing Rust-backed uv/Ruff/zizmor and qualified voiage kernels | Profile first. Do not build a second Rust statistical engine solely for novelty. PyO3/maturin becomes relevant only for a measured kernel with parity/error/provenance tests. |
| Ad hoc context stuffing | Small scoped AGENTS/skill profiles, jsonschema, hash-bound envelopes | Implemented/tested. Explicit local allowlists, budgets, stale-content detection, no automatic external fetching or model calls. It is not a secret scanner, prompt-injection proof or agent sandbox. |

No policy parameters, priors, action payoffs or empirical source values are changed by the
Gaussian backend substitution. The logarithmic determinant/whitening arithmetic is delegated,
not the scientific meaning of the covariance. End-to-end full scientific replay remains required
on the complete checkout; local interface tests are not a new funding analysis.

## Why the reference scientific pins are retained
Latest software belongs in a separate compatibility lane before it becomes the reproducible
scientific baseline. The Python 3.15.1 reference stack uses NumPy 2.5.4, SciPy 1.18.1,
pandas 3.1.0 and Matplotlib 3.11.2. Newer/pre-release numerical packages remain in a separate source-only
scheduled canary. It cannot silently update reference results, lockfiles or published conclusions.
An observed compatible release can be promoted in a reviewed change with output tolerances,
platform logs and changelog.

The present tools are verified candidate versions, not an assurance that every cached upstream
page reflects the absolute latest patch. Use Renovate proposals, no automatic scientific merges.

## Source notes (checked 24 October 2026)
- Live repository: src/tobac/supply.py, evidence.py, config_validation.py; src/tobac_supply/;
  pyproject.toml; .github/workflows/; AGENTS.md; issue #1 and open execution issue #4.
- SciPy covariance/log density: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.Covariance.from_cholesky.html
- voiage capability/status: https://github.com/edithatogo/voiage/blob/main/README.md
- mars beta/API: https://github.com/edithatogo/mars/blob/main/README.md
- Nox UV backend/sessions: https://nox.thea.codes/en/stable/config.html
- uv genuine locking: https://docs.astral.sh/uv/pip/compile/
- NumPyro: https://num.pyro.ai/en/stable/ ; ArviZ: https://python.arviz.org/
- Current Conductor host packaging: https://github.com/gemini-cli-extensions/conductor/blob/6e8f9a860bcdd6a2c423473c12e745200688c633/README.md

README capability claims inform candidates, not independent validation of those libraries or
assurance of this project's empirical validity. M3 ownership and shared interfaces
are recorded in docs/WORKSTREAM_SYNC.md; issue #1 is historical context, not a gate.

## Current acceptance note — 28 October 2026

Older implementation notes are dated evidence, not current tool-unavailability
claims. macOS Python 3.15.1 tests, strict checks, reproduction, package/security,
mutation and recovery have executed; PR #60 verifies the current checked base.
The remaining ecosystem gate is GitHub's externally managed root parser, whose
service runtime is not controlled by the project. See DEPENDENCY_MAINTENANCE.md
and the managed-parser recheck receipt. Deployment of that service's Python support remains an upstream responsibility.
