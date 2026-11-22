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

## Game capability intake

UOGTO owns game-theoretic semantics and Paignia owns reusable game
representations and solvers. Every newly identified, added or materially changed
game must have linked records under both upstream contracts:

- [UOGTO semantic coverage and extension intake](https://github.com/edithatogo/UOGTO/blob/main/docs/contracts/downstream-game-intake.md).
- [Paignia generic capability and fixture intake](https://github.com/edithatogo/paignia/blob/main/docs/integrations/downstream-game-intake.md).

Use the same intake key in both records and link them from the local plan or
pull request. Identify the originating source path and immutable revision,
players, actions, information, timing, payoff meaning and requested solution.
Record the semantic and implementation dispositions separately:

| Upstream | Allowed dispositions |
| --- | --- |
| UOGTO | `reuse_existing`, `extension_required`, `unsupported`, `mapping_review_pending` |
| Paignia | `reuse_existing`, `extension_required`, `unsupported`, `domain_only`, `assessment_pending` |

For `reuse_existing`, add or refine the UOGTO mapping/example with full term
IRIs and link the supported Paignia API/profile, its limits and fixture evidence.
For `extension_required`, link the upstream proposal, a minimal synthetic example
and independently expected results. `unsupported` records the missing requirement
and its effect on claims or execution. Paignia's `domain_only` records why the
change needs no generic implementation. Pending assessments need a reason,
owner and next action; they do not establish semantic or executable support.

Inspect existing upstream work before proposing another term, solver or fixture.
An unchanged game with new parameters can reuse its intake key and add an
application example. Data, assumptions, payoff construction and calibration
remain here; Paignia receives only reusable representations, algorithms and
conformance fixtures. Preserve source revision, licence and attribution for
any transferred example or implementation.

On adoption, record the exact UOGTO revision/profile and full IRIs, Paignia
revision or artifact hash, fixture identity, and focused semantic/native/consumer
checks actually run, including independent expected results and invalid or
unsupported cases. Ontology conformance and numerical verification are separate.
A record or dependency pin alone does not complete a migration.

Existing local or pedagogical implementations may remain while migration is
assessed, with their scope and limitations labelled. New game changes still
require intake. This policy does not replace algorithms, change model assumptions
or promote heuristic outputs to verified equilibria.
