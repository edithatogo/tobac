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

## Final checkpoint execution order

1. Consume the owner's terminal immutable renewal packet, preserving its qualified main
   workflow pins and signed input closure. Never copy its dirty checkout or private bindings.
2. Confirm this checkout's HEAD/status and all six lock receipts. Record actual interpreters
   and distinguish the canonical profiles from unpromoted latest candidates.
3. Freeze source before building context. Run one bounded command at a time; do not commit
   while a context-bound command is starting or running. Inspect its terminal status/log
   before editing, committing or beginning the next expensive operation.
4. Run renewed lineage admission, affected/workstream tests and the coherent full-suite
   gate. Execute the real M1 DAG with its attested preflight, then verify the published output.
   Retain prior negative/recovery evidence where its exact implementation is unchanged.
5. Inspect each required receipt and update the acceptance audit. A signature, a green
   subset or the owner's status message does not replace this lane's actual readback.
6. Commit evidence only after commands are terminal. Rebuild context after every HEAD or
   included-source change before the next context-bound command. Reconcile current main
   again at final integration; retain the existing integrator's shared promotion scope.

Current independent numerical oracle remains the original accepted finite reference.
Renewing active lineage must not silently replace that oracle's checkpoint identity.
