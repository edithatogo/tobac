# P1.1 — Decision and evidence preparation

Requirements: R01–R06, R18–R19. Observable deliverable: versioned decision definition,
Searchright strategy, source/model appraisal queue and evidence-access disposition.
This is independent preparation and read-only discovery, not E1 empirical execution.

Owner: chat 01a1af53-2093-7f70-b761-e5f6cb7b769c; actual worktree
/Users/doughnut/.codex/worktrees/tobac-nz-au-empirical/tobac; branch codex/nz-au-empirical.
Base: 848da48. Allowed paths: this track, engineering/context/nz-au-evidence.json,
engineering/publication-policy.json (exact new paths only), append-only ownership in
docs/WORKSTREAM_SYNC.md, ignored outputs/nz-au-phase1 and an external acquisition staging
directory /Users/doughnut/Documents/tobac-evidence-intake-20261106. No native signing,
archive ingestion, external upload, fitting, runtime promotion or changes under src.

Prerequisites: clean base verified; core index links exist; actual .venv Python 3.15.2
verified. Phase 0's renewed latest-lock admission remains unavailable, as recorded in
integration-handoff.md. Stop all dependent promotion and fitting until it passes.

Reuse: scripts/context_bundle.py, scripts/run_bounded.py, existing Searchright binary
outputs/nz-au-phase0/searchright-bin/searchright and its upstream strategy contract;
scripts/source_handoff.py, Scope, EvidencePacket, SupplyBasis, existing archive register
and evidence/m2/public_sources_20261027 extraction/parameter/assumption tables. New
matrices are appraisal queues and pointers, never a second observation authority.

Commands from repository root, executed serially for expensive work:

```sh
.venv/bin/python scripts/context_bundle.py --profile engineering/context/nz-au-evidence.json --out outputs/nz-au-phase1/context
outputs/nz-au-phase0/searchright-bin/searchright validate-strategy conductor/tracks/nz_au_empirical_20261106/searchright-strategy.json
outputs/nz-au-phase0/searchright-bin/searchright compile --dialect pubmed conductor/tracks/nz_au_empirical_20261106/searchright-strategy.json
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/engineering/test_context_bundle.py tests/engineering/test_source_handoff.py tests/test_workstream_integration.py
git diff --check
```

Log directory: outputs/nz-au-phase1. Resource ceiling: 4 GiB process-group sampled RSS,
40 minutes per expensive command, zero blind retries. Public publisher originals may be
retrieved into the external staging directory only; retain exact URL, actual retrieval
time, bytes, content type and SHA256. A failed download is not an archived original.

Positive cases: strategy accepted and translated by actual binary; country/product/time,
perspective, missing evidence and validation boundaries explicit; source pointers resolve.
Negative cases: fixture search cannot qualify live recall; unavailable full text cannot
verify a numeric input; ABS/ACIC overlap cannot be treated as independent; no nicotine-only
illicit attribution; no dataset status promoted by this task. No numerical tolerance applies
because numerical model code and inputs are unchanged. New fitting tolerances require a
separate prespecified task before data inspection.

Stop on ownership conflict, failed prerequisite, unidentified source, unresolved rights or
dimension. Preserve all earlier receipts; corrections are new editions. Rollback only this
card's exact owned changes. Terminal outcomes and next task belong in phase1-progress.md;
Phase 1 stays incomplete until all six plan rows have their actual evidence.

## P1.2 continuation — 7 November 2026

Base c239b18; writing chat 01a1b3ac-76ef-7b12-a919-91fcb05de339, managed worktree
/Users/doughnut/.codex/worktrees/tobac-p1-evidence/tobac, codex/p1-evidence-20261107.
Phase 0's local gate is now accepted by its retained checkpoint; hosted and empirical
acceptance remain separate. Own only this phase's protocol/queries/progress and
coordination addition. No source/runtime/native mutation or external upload.

Use actual isolated .venv Python 3.15.2, hash-sync engineering/requirements.lock,
context_bundle with nz-au-evidence profile and new output directories. Requalify
Searchright current main 4ddfbdbc54c500719889e09942783bdc04ee832b from its own
source, retaining fixture/no-network limits. Qualify source-native retrieval if
live execution is unavailable; keep responses outside tobac and metadata only here.
Freeze queries before execution. Check count/cursor completeness and seed identities;
retain errors and pending screening. No arbitrary retrieval cap may imply completeness.

All expensive commands use scripts/run_bounded.py, 4096 MiB / 2400 seconds, serially.
Logs: outputs/nz-au-phase1-20261107. External staging:
/Users/doughnut/Documents/tobac-evidence-intake-20261107-p1.
Verification: exact CLI/import positive/negative cases, affected context and source
handoff tests, tests/test_workstream_integration.py, git diff --check. Numerical
source/inputs unchanged: reuse Phase 0 replay; no new scientific result claimed.
Stop dependent admission on rights/destination, original verification or search gaps;
record terminal receipts and continue independent bounded evidence work.
