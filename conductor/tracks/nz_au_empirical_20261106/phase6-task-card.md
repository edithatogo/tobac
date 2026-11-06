# P6.1 — Reproducible qualification and source integration

R14–R19. Base eb3a3d5, chat 01a1af53-2093-7f70-b761-e5f6cb7b769c,
codex/nz-au-empirical at /Users/doughnut/.codex/worktrees/tobac-nz-au-empirical/tobac.
Deliverable: source-bound clustering/audit dependency coverage, Nox/Snakemake execution,
complete packet verification, failure/recovery controls and a terminal integration packet.
Empirical Phase 0–5 gaps remain explicit; no scientific admission or main publication is
inferred from software qualification. The existing integrator's dirty renewal is not copied.

Owned local source-candidate paths: scripts/lock_receipt.py,
scripts/qualify_sensitivity_clustering.py, scripts/verify_sensitivity_clustering.py,
scripts/audit_empirical_coverage.py for whole-source typing annotations only,
tests/engineering/test_lock_receipts.py, tests/engineering/test_clustering_qualification.py,
tests/engineering/test_clustering_packet.py, noxfile.py, workflow/Snakefile,
workflow/README.md, engineering/clustering.in and its generated lock/receipt,
engineering/tools-requirements.txt, engineering/audit.lock and receipt, renovate.json,
engineering/reference-requirements.txt, engineering/test-requirements.txt,
engineering/voiage.in, engineering/ecosystem.in, engineering/advisory.in,
matching runtime/voiage/ecosystem/advisory lock/receipt pairs and scripts/advisory_types.py
for newly observed compatible releases; this track, engineering/context/nz-au-integration.json,
exact publication-policy entries
and append-only docs/WORKSTREAM_SYNC.md. This is a reviewable source packet, not promotion
of shared main/runtime or permission to alter the integrator's environment/native bindings.
Existing core numerical modules, empirical inputs, reference outputs and M3 are unchanged.

Reuse lock_receipt closed graphs, source_handoff checked/read/same_hash guards, existing
context verification, protected directory/cache rules, qualifier, Nox environments and
Renovate as sole updater. Extend existing machinery; no second lake or task runner.

Exact execution commands are in workflow/README.md. Use repository-root cwd and
scripts/run_bounded.py with --max-rss-mib 4096 --timeout 2400 for every heavy command.
Generate clustering/audit candidates with scripts/lock_receipt.py generate --profile
PROFILE --path NEW_DIRECTORY. Run Nox clustering, affected component tests and the full
suite using the actual qualified Python 3.15.2 interpreters; record their resolved paths
and logs in phase6-progress.md. Run git diff --check and normal publication-security gates.

Generate into new candidate directories, verify/review changed package graphs, then copy
only these owned candidate lock/receipt pairs to engineering. Final Nox output is unique;
exact invocation/manifest/log paths go in phase6-progress.md. Recheck profile versions at
integration decision without floating the accepted scientific baseline. Analytics interpreter
is the retained .venv-analytics3152/bin/snakemake; selected task Python is the new clustering
Nox environment. Exact scheduler commands are documented after that interpreter is resolved.

Acceptance: old four-profile contract preserved; both new/changed receipts bind actual
resolver inputs; hashes/install consistency and no pandas/xarray pass. Cached output reopens
all declared bytes and source/lock identity. Missing/extra/corrupt files, traversal, symlinks,
stale source and failed partial publication reject; interrupted work never looks complete.
Failure cleanup/recovery and completed-output preservation have positive/negative tests.
Keep context, synthetic software, native lineage and empirical acceptance distinct.

Budget 4 GiB sampled process-group RSS / 40 minutes / one native thread / zero blind retries.
Do not replace an environment in use, delete others' files/locks, copy private bindings,
weaken gates or automatically refresh old results. If the integrator supplies a terminal
immutable source packet, compare revisions and conflicts before guarded integration;
otherwise retain exact native/hosted/publication gaps. Full suite and relevant reproduction,
package/security checks are actual gates, not inferred from focused successes. Rollback
only owned changes. Native failures stay failed until the authorised owner renews them.
