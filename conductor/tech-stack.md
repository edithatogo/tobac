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

The optional `interchange` extra uses PyArrow 26.0.0, Polars 1.44.2, Patito 0.8.6
and msgspec 0.22.0 to transport the existing evidence contract. Required test and
clean-package environments exercise it; the numerical runtime remains unchanged.
See docs/engineering/EVIDENCE_INTERCHANGE.md for schema, ownership and hash limits.
