# Stack and reuse

Reference calculation: Python 3.15.1, NumPy 2.5.4, SciPy 1.18.1. Longitudinal exports use pandas
3.1.0 and matplotlib 3.11.2. Regulatory/evidence contracts live in tobac; longitudinal accounting/model
components in tobac_supply. M3 owns the additive research portfolio and weighted-library work.

Nox/uv orchestrate isolated engineering checks. Pytest/coverage/Hypothesis test code; Ruff,
BasedPyright, zizmor and pip-audit have distinct scopes. Profiles use jsonschema. Mutmut and
Scalene are bounded deep-check tools. Candidate pins are in engineering/*-requirements.txt;
only a generated/reviewed hash lock qualifies a reproducible release environment.

No second statistical engine, Rust rewrite or universal agent framework without an identified
need, maintained alternative review and acceptance evidence. Read docs/engineering/READINESS.md.

An advisory lane mirrors the reference checks with ruff-action, ty, pyrefly, prek, gitleaks,
harden-runner, zizmor-action and gh-action-pip-audit. ty and pyrefly are separate checkers from
BasedPyright and report diagnostics only; prek is the Rust pre-commit runner, not pre-commit
itself. Renovate's pinGitHubActionDigests preset preserves the existing full-SHA posture. Only a
generated/reviewed hash lock qualifies a release environment.

The optional `interchange` extra uses PyArrow 26.0.0, Polars 2.0.0, Patito 0.8.6
and msgspec 0.22.0 to transport the existing evidence contract. Required test and
clean-package environments exercise it; the numerical runtime remains unchanged.
See docs/engineering/EVIDENCE_INTERCHANGE.md for schema, ownership and hash limits.

Renovate is the sole dependency-update PR provider. It detects the four .in
profiles and groups evidence-transport compatibility updates; all four manual
lock candidates are generated through the existing verified helper. See
docs/engineering/DEPENDENCY_MAINTENANCE.md. GitHub's internal Dependabot graph
parser is separate; graph submission and security audits remain intact.

Ruff ALL-rule linting and stable formatting cover maintained source, scripts, tests
and Nox tooling. Five exact preview rules are qualified independently; pytest-specific
exceptions are documented in docs/engineering/RUFF_POLICY.md. macOS verification runs
under sampled process-group RSS/time budgets with owned-child cleanup; mutation is
limited to two workers. Budgets do not establish absence of memory leaks.
