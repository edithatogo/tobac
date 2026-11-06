# P0.1 — Baseline and upgrade evidence

Owner: chat 01a1af53-2093-7f70-b761-e5f6cb7b769c, isolated codex/nz-au-empirical.
Base: adb3f8127355f210c1df959d629730873b381fc2.
Allowed scope: track records, local outputs/nz-au-phase0, owned .venv and exact publication
inventory entries for the new planning files. No native writes or shared runtime promotion.

Inputs: engineering/requirements.lock, engineering/context.schema.json, existing context
builder and bounded runner. Preserve existing numerical formulas and shared evidence IDs.

Executed commands:
- uv venv --python /Users/doughnut/Documents/tobac/.venv/bin/python .venv
- .venv/bin/python -c 'import sys; print(sys.version); assert sys.version_info[:3] == (3,15,1)'
- .venv/bin/python scripts/context_bundle.py --profile outputs/nz-au-phase0/profile.json --out outputs/nz-au-phase0/context
- .venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- uv pip sync --python .venv/bin/python --require-hashes engineering/requirements.lock
- uv pip check --python .venv/bin/python
- .venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q

Acceptance: actual interpreter assertion, context manifest, hash installation, dependency
consistency, terminal full-suite result. No retry, no raised resource limit, no empirical
validity claim. A failure stops dependent upgrade promotion; inspect exact log first.
Local logs: outputs/nz-au-phase0/baseline-install.log and baseline-tests.log.
Version census: outputs/nz-au-phase0/version-census.json (dated PyPI metadata, not qualification).
