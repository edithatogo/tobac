# Public evidence and finite decision sufficiency — 13 November 2026

Implemented in an isolated standard Git worktree at base `4655364`. This is a
bounded methods/software package, with no paper text, active configuration or
observation-admission change. The four-report selection and stopping rule are in
[the protocol](public-evidence-protocol-20261113.md).

## Evidence and identity result

Four main full texts are appraised at named result/method/limitation locators.
Fourteen already catalogued quantities agree with the located source values:
one overall mortality hazard ratio, five nicotine-specification/biomarker entries
and eight utility means. These are attributed extracted facts; no full text or
utility-scoring algorithm is distributed. Source receipts bind exact downloaded
bytes outside Git, with the rejected wrong-DOI capture retained. There is no new
canonical archive or independent-preservation claim.

The reconciliation helper verifies all three existing catalogue/crosswalk hashes
before reading. Twenty declared numeric aliases agree, including explicit Walker
percentage-point conversion and the PHARMAC source alias. Uncertainty terminology
is checked separately; agreement does not establish equivalent population scope
or independent observations. All 65 newer and 61 embedded entries are accounted
for: 45 and 41 respectively remain unmatched. The two counts cannot be added into
an independent evidence sample. No distribution is fitted and no runtime parameter
is promoted. `public-result-extracts-20261113.json` connects each checked result to
its existing target and an existing health interface where applicable. There is
no validated runtime adapter for the nicotine-standard/biomarker quantities.

The source checker verifies hash, DOI, candidate identity, unit, interval type,
dependence group, value and bounds. It compares a single manually located
extraction with the catalogue; it does not claim two independent source extractors.
The earlier empirical audit still reports zero compatible observations in each
required comparison role. Four appraisals and 14 values do not close that gap.

## Decision result and compatibility change

`scripts/decision_sufficiency.py` uses standard-library rational arithmetic on
explicit finite state-by-action payoffs. It reports exact pairwise advantage
bounds, attaining states, common optimal actions, worst-case regret and witnesses.
These are exact over the enumerated states and their probability mixtures;
continuous nonlinear support requires a separate completeness argument.
No independent parameter margins are silently crossed into impossible joint states.
Unknown payoffs are errors and empty compatible support is incompatibility.
Minimax regret is explicitly a separate convention, not proof of a common optimum.

The committed synthetic example has payoffs act=(-2, 3), wait=(0, 0). Waiting wins
in the first state and acting in the second; neither is uniformly optimal. Their
worst-case regrets are 2 and 3 common hypothetical units. This is a witness-based
software demonstration, not measured NZ benefit, cost, monetary VOI or a policy
recommendation. Real target payoffs remain unspecified; no empirical decision
calculation is claimed.

The earlier `decision_identification_benchmark.py` incorrectly used interval width
below one as a decision-identification criterion. Its v2 output now records
**parameter point identification** and explicitly says decisions were not assessed.
Consumers of the v1 JSON keys must migrate. Existing archived outputs stay intact.
The CLI now refuses to overwrite a previous output.

Library decision: retain existing `restriction_bounds`/`accounting_bounds` and
finite-state scientific engines. `DecisionProblem` requires floating payoffs and a
normalised prior; this small support-only rational oracle intentionally supplies
neither and does not replace it or the M3 Voiage provider. No new dependency.

## Reproduction

Use this checkout's verified repo-local Python 3.15.2 and retained source hashes.
The external originals directory is owner-local; absence or changed bytes must
fail the source check. Create new output names on subsequent executions.

```sh
.venv/bin/python scripts/reconcile_public_parameters.py \
  --bindings conductor/tracks/nz_au_empirical_20261106/public-parameter-bindings-20261113.json \
  --extracts conductor/tracks/nz_au_empirical_20261106/public-result-extracts-20261113.json \
  --originals /Users/doughnut/Documents/tobac-evidence-intake-20261113-public \
  --out outputs/public-evidence/source-reconciliation.json
.venv/bin/python scripts/decision_sufficiency.py \
  --input conductor/tracks/nz_au_empirical_20261106/public-decision-scenario-20261113.json \
  --out outputs/public-evidence/decision-result.json
.venv/bin/python scripts/decision_identification_benchmark.py \
  --out outputs/public-evidence/interval-benchmark.json
```

## Validation and acceptance

The final source-bound receipt records executed checks and their limitations.
No failed native preflight, skipped test, missing tool or diagnostic-only suite is
presented as successful native qualification. The root native owner retains signed
bindings and runtime promotion. Shared-main integration and publication are separate.

Assistant self-review covers exact arithmetic, attaining witnesses, malformed and
missing inputs, ties, support restriction, duplicate identities, false source/unit/
uncertainty equivalence, stale hashes and candidate-only boundaries. It establishes
bounded software evidence. No named human scientific acceptance or submission
authority is inferred. Full systematic-review screening, unresolved source identity,
transport, calibration, held-out validation and empirical policy effects remain open.

Final affected checks: **106 passed**, with zero Ruff diagnostics and zero strict
Basedpyright errors/warnings on the affected scripts. The complete diagnostic
suite before the final container/DOI/count controls returned **1,445 passed,
29 failed, 23 skipped and 26 setup errors** in 253.82 s, at 663.0 MiB peak sampled
RSS. Failures concern absent ignored source inputs and the resulting native
inventory mismatch. The final affected suite was rerun after those controls.
Standard Nox `tests` and `reproduce` stop at `Missing TOBAC_LINEAGE_PYTHON`;
no binding or native original was copied. The core verifier checks nine preserved
definitions and explicitly reports `run_verified: false`; it is not a numerical
runner replay. New finite and interval example CLIs executed successfully.

[Hash-bound validation receipt](public-evidence-validation-20261113.json) retains
exact runtime/tool identities and local log hashes. The tooling environment was
resolved natively with the repository's pinned Nox/Basedpyright versions; it is
not a new locked release environment. This source packet needs integrator review
of new publication-policy paths before external publication. No remote write,
shared-main promotion, native renewal or release acceptance occurred.
