# Working on tobac

Read AGENTS.md, the selected Conductor task card and docs/WORKSTREAM_SYNC.md before editing.
One chat writes each checkout; isolate parallel lanes and retain the existing integrator
for shared main, dependency promotion and native admission. Independent review is optional.

Use actual repo-local Python 3.15.2 and the hash-locked bootstrap in the
[workflow guide](workflow/README.md). Never replace an environment in use. Expensive
commands on macOS use scripts/run_bounded.py with 4096 MiB sampled group RSS and a
2400-second ceiling; keep native numerical threads bounded and run heavy commands serially.
Nox is the engineering runner and Snakemake orchestrates analytics. Do not add another runner.

Run affected tests and tests/test_workstream_integration.py; preserve complete integration,
numerical reproduction, coverage, clean-package and security gates at coherent milestones.
Keep pytest's per-worktree cache enabled. Use --lf --last-failed-no-failures=none only for
failure-only reruns; an empty cache verifies no tests. Default to zero retries. Do not turn
skips, mocks, workflow definitions or a synthetic qualification into native/empirical proof.
Consult the [current evidence and open gates](conductor/tracks/nz_au_empirical_20261106/phase6-progress.md).

Preserve Scope, EvidencePacket and SupplyBasis, units, dates, covariance and shared data IDs.
Keep observed data separate from posteriors/forecasts; shared sources condition only once.
Record source, formula and output versions and the rationale for assumptions. A policy
conclusion needs empirical evidence beyond passing software tests.

Project-owned code is Apache-2.0; retain upstream licences and notices. External data,
papers, private authoring documents and original evidence retain their own rights. Keep
those originals in approved external stores, with admitted references in this project.
Do not commit private bindings, credentials, native originals or sensitive operational data.
Use the existing publication boundary and ordinary Git hooks; never bypass a failed gate.

For a bug, provide the revision, actual interpreter, exact command, redacted error and a
minimal synthetic reproduction. Use the [security policy](SECURITY.md) for vulnerabilities.
In a change description, distinguish executed checks, failures, unavailable checks and
remaining empirical gaps. Preserve current work and use guarded publication with receiving
ref/file readback. A local commit does not establish hosted or release acceptance.
