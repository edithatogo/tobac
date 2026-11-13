# Hardening plan

## H0 — Baseline inventory (with empirical Phase 0)

- [x] Inspect current main, ownership and existing receipts; identify actual gaps without repeating unchanged audits. Baseline/receiving refs and retained owners are recorded in index.md.
- [x] Inventory documentation links, package contents, GitHub metadata and workflow boundaries. Scope and untested link/rendering behavior are explicit in index.md.
- [x] Record findings, severity, allowed files, owner and focused acceptance commands. See the H0 findings table; inventory does not imply H1/H2 completion.

## H1 — Incremental hardening (with each analytical package)

The checks below close the bounded H1.1 source/document package only. Repeat affected
hardening when a future analytical package changes semantics or execution inputs.

- [x] Correct stale docs/examples and reconcile setup/runtime declarations for H1.1. Current 3.15.2 source and blocked latest-lock promotion are distinct; maintained navigation labels withheld targets, while original capture README/index editions retain their pinned bytes and use separate current navigation. See progress.md.
- [x] Qualify meaningful contract/property/regression checks, structured error/logging and corrupt-input/resume behavior for the current analytical package. Reuse unchanged Phase 6 atomic/packet/offline/scheduler controls; 85 affected H1.1 checks pass. No mirrored tests added for prose edits.
- [x] Check locks, dependency licence metadata, secrets exposure, CI permissions/action pins and artifact provenance for H1.1. Inventory and exact scan scope are in progress.md; no legal/hosted certification inferred.
- [x] Measure bounded runtime/RSS and diagnose regressions without automatically increasing budgets. Current affected tests: 5.39 s, 124.8 MiB; unchanged analytical performance receipts retained.
- [x] Verify each scoped H1.1 change and retain evidence; preserve unchanged checks. Local software/document scope only; release and empirical gates below remain open.

## H2 — Release and repository tidy-up (after empirical milestone acceptance)

- [ ] Verify clean package/install, maintained entry points, full integration/reproduction and security gates.
- [x] Prepare README, citation, licence/notices, capability and Conductor reconciliation. H1.1 local consistency checks pass; release acceptance remains separate.
- [x] Prepare owner-scoped GitHub metadata fixes and stale-item disposition inventory; no blind deletion/closure. Current metadata require no changes; four PR/branch and three issue dispositions are recorded in progress.md without mutations.
- [ ] Verify source/data publication boundary, restore/recovery and exact receiving ref/files after guarded integration.
- [ ] Record terminal evidence handoff with unresolved findings and empirical limitations.
- [x] Scope `scripts/run_bounded.py` macOS process-group RSS sampling (`ps -g <pgid> -o pgid=,rss=`) in alignment with `repository-standards` so uninterruptible third-party processes cannot stall system-wide `ps -axo` scans during test or `pre-push` execution.
- [ ] Separate the Runner Closure Merkle Root from the Candidate Evidence Registry Merkle Root in `hosted_lineage.py` / `lineage_preflight.py` (with `archive-govt-nz`) so staging candidate evidence packs does not invalidate unchanged runner closures.
- [x] Expand deterministic Hypothesis metamorphic property checks across `dynamic.py`, `health.py`, `partial_identification.py` and `information.py` (time-subdivision convergence, constraint monotonicity and Blackwell garbling monotonicity).
