# P3.1 — Policy, health and equity expansion readiness

Requirements: R05–R08, R12, R18. Deliverable: module-specific evidence, formula and
acceptance contracts, library reuse disposition and actual shared-evidence admission audit.
Empirical expansion is blocked by the incomplete Phase 0–2 gates; this task performs
independent conceptualisation and read-only feasibility work only.

Owner: chat 01a1af53-2093-7f70-b761-e5f6cb7b769c; base 7cd0394; branch
codex/nz-au-empirical; worktree /Users/doughnut/.codex/worktrees/tobac-nz-au-empirical/tobac.
Allowed files: this track, engineering/context/nz-au-expansion.json, exact new publication
policy entries, append-only docs/WORKSTREAM_SYNC.md, ignored outputs/nz-au-phase3 and
external acquisition staging /Users/doughnut/Documents/tobac-evidence-intake-20261106.
No changes to src, model inputs, reference outputs, dependencies or M3. No external writes,
native signing, archive ingestion or shared promotion. Do not change the ongoing owner's
frozen 4015cc3 qualification candidate or treat queued checks as admission.

Reuse: existing Scope/EvidencePacket/SupplyBasis; source_handoff.py; regulation.py,
retail_case.py and value_sensitivity.py; existing finite oracle. These declare conditional
mechanisms and normalised scores, not calibrated lifetime health or QALYs. Historical
optional engines remain archived. Review maintained vop_poc_nz and equity tutorials before
new machinery; no copying third-party code or bypassing Python/dependency constraints.

Commands from repository root, expensive commands serial, logs under outputs/nz-au-phase3:

```sh
.venv/bin/python scripts/context_bundle.py --profile engineering/context/nz-au-expansion.json --out outputs/nz-au-phase3/context
PYTHONPATH=src .venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python scripts/source_handoff.py --out outputs/nz-au-phase3/source-handoff.json
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/m2/test_evidence.py tests/m2/test_retail.py tests/m2/test_value_sensitivity.py tests/test_regulation.py tests/engineering/test_source_handoff.py tests/engineering/test_publication_boundary.py tests/test_workstream_integration.py
git diff --check
```

Acceptance: each requested mechanism has scientific inputs, outcome units, dependency and
negative-case requirements; the actual handoff result remains blocked where source gaps
exist. A CLI exit 0 merely writes a report; inspect its status and scientific_qualification.
No uncertainty distributions or health utilities are invented. Direct publisher retrievals
record time, exact bytes/hash, failures and rights; external staging is not archive admission.
Stop dependent work on missing calibration, incompatible scope, ownership conflict or failure.
Budget: 4 GiB sampled group RSS / 40 minutes / zero blind retries. Preserve all receipts;
do not overwrite existing output directories. Rollback only this task's owned metadata.
Results and next unblocked operation are recorded in phase3-progress.md. No whole-track
completion or standards certification is implied by these preparations.
