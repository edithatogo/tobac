# P4.1 — Diffusion, competition and extended VOI qualification

Requirements R10–R12. Deliverables: current Innovate dependency/API disposition,
scenario/acceptance contracts and actual qualification of existing finite VOI components.
Phase 0–3 empirical gates remain open. This task is source discovery and synthetic software
qualification, not empirical E5 execution, policy adoption fitting or research procurement.

Owner: chat 01a1af53-2093-7f70-b761-e5f6cb7b769c; base 79050c4; branch
codex/nz-au-empirical; /Users/doughnut/.codex/worktrees/tobac-nz-au-empirical/tobac.
Allowed files: this track, engineering/context/nz-au-diffusion.json, exact publication-policy
entries, append-only docs/WORKSTREAM_SYNC.md; ignored outputs/nz-au-phase4 and external
source staging /Users/doughnut/Documents/tobac-evidence-intake-20261106. M3 source/tests,
scientific inputs, reference outputs, locks, native bindings and other checkouts are unchanged.
Existing integrator retains ongoing native admission for 4015cc3. No external messages,
uploads, source vendoring, new library installation or dependency omissions.

Reuse: M3 implementation.py, portfolio.py, staged.py, structure.py, robust.py and the
actual Voiage adapter/qualification; existing Scope/EvidencePacket and finite oracle. Do
not add a duplicate diffusion engine or claim a scenario trajectory was fitted by Innovate.

Exact commands from root; heavy commands serial, logs under outputs/nz-au-phase4:

```sh
.venv/bin/python scripts/context_bundle.py --profile engineering/context/nz-au-diffusion.json --out outputs/nz-au-phase4/context
.venv-ecosystem3152-latest/bin/python -c 'import sys; assert sys.version_info[:3] == (3,15,2)'
PYTHONPATH=src .venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv-ecosystem3152-latest/bin/python -m tobac.research.qualification --out outputs/nz-au-phase4/voiage-qualification.json
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/m3/test_research.py tests/m3/test_saved_results.py tests/test_workstream_integration.py tests/engineering/test_publication_boundary.py
git diff --check
```

The selected existing ecosystem environment was verified as actual Python 3.15.2 with
Voiage 3.1.0; do not replace it or promote it. Newest qualified locks remain separate from
the pending native admission. Qualifier checks weighted EVPI and finite partition transforms
only, at its existing 1e-11 absolute tolerance; do not extend its API certification to EVSI,
continuous EVPPI, risk or CEAC. Read terminal receipt success/status, not just command exit.

Positive/negative acceptance reuses exact tests for unequal/zero state weights, offsets,
non-stochastic uptake, signed interaction, repeated correlated reports, reused evidence,
shared setup costs, negative ENBS and matched-timing adaptive branch enumeration. No
empirical diffusion, competition, cost or likelihood parameters are invented. Stop dependent
integration on unavailable library, changed source, invalid units/identity or failed check.
Budget 4 GiB sampled process-group RSS / 40 minutes / zero blind retries. Preserve original
outputs; rollback only owned metadata. Results/gaps belong in phase4-progress.md.
