# P2.1 — First NZ/AU empirical feasibility analysis

Requirements: R03–R10, R16, R18. Deliverable: reproducible source coverage audit,
verified AU programme comparator and explicit identification finding for the proposed slice.
This task does not fit a model or promote unaccepted inputs to Gold.

Owner: chat 01a1af53-2093-7f70-b761-e5f6cb7b769c, branch codex/nz-au-empirical,
/Users/doughnut/.codex/worktrees/tobac-nz-au-empirical/tobac, base 848da48 with owned P1.1
drafts retained. Allowed files: this track, scripts/audit_empirical_coverage.py,
tests/engineering/test_empirical_coverage.py, exact new publication inventory entries and
ignored outputs/nz-au-phase1 and outputs/nz-au-phase2. No native writes, archive ingestion,
external upload, shared dependency promotion or scientific source/input changes.

Prerequisites and stop: latest-lock native admission remains owner-held and incomplete;
Phase 1 source acceptance and exact policy baseline are incomplete. Only independent
read-only feasibility work proceeds. No current illicit estimate, fitted policy effect,
held-out predictive score or monetary EVSI may be fabricated in their absence.

Inputs: existing source_record.json and historical lawful-supply CSV, annual tonne series,
Phase 1 publisher download receipt and external ACIC report PDF SHA256
8e1dd8cfb754ea8fd577ee086a98e336384ffd10d8a1c5829e7f47bc72c1e741.
Reuse Polars for inventory/coverage, existing SupplyBasis and observation-handoff semantics,
existing source_handoff verifier; no parallel empirical likelihood is introduced.

Exact commands (repository root):

```sh
.venv/bin/python scripts/context_bundle.py --profile engineering/context/nz-au-evidence.json --out outputs/nz-au-phase2/context
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python scripts/audit_empirical_coverage.py --out outputs/nz-au-phase2/coverage.json
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/engineering/test_context_bundle.py tests/engineering/test_source_handoff.py tests/test_workstream_integration.py
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/engineering/test_empirical_coverage.py
git diff --check
```

The tracked scripts/audit_empirical_coverage.py contains no fitting: it checks existing extracted CSVs
against the consumer inventory using source_handoff path/hash guards and Polars to inventory
their scope. It does not verify them anew against publisher originals. Its source/hash and
terminal receipt are retained in the analysis output.
PDF text extraction uses installed pdftotext; visual verification uses a rendered PDF page,
with text/figure disagreements left unresolved. Local derived text/images remain outside
the source repository or under ignored outputs. Bounds proof uses dimensional equations,
not estimated conversion parameters or synthetic observations.

Acceptance: actual historical coverage reported with its source caveats; AU design fields
have exact PDF locations and verification mode; incompatible units cannot be subtracted;
shared-source ABS/ACIC records cannot establish independent corroboration. Missing costs
remain null/unpriced. Negative outcomes are valid results, not completed fitting tasks.
Budget: 4 GiB sampled group RSS, 40 minutes, serial heavy commands, zero blind retries.
Stop on changed source hash or ambiguous units. Rollback only owned metadata. Results,
actual exits and next prerequisites go in phase2-feasibility.md and plan/status updates.
