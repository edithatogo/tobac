# Finite BF1 and BF2 implementation checkpoint

13 November 2026. The current work is on the local
`codex/bf1-bf2-implementation-20261113` branch in
`/Users/doughnut/Documents/tobac-methods-integration-20261113`.

## BF1 certificates and minimal restrictions

The new `tobac.credal` API accepts the existing `Belief` and named linear
restrictions with identical ordered state IDs. `assess_contrast` returns
numerical extrema, rational feasible witnesses and exact rational dual bounds.
`assess_decision` compares every action and brackets worst-case regret.
`minimal_identifying_restrictions` enumerates up to eight candidate restrictions
and requires a negative feasible witness for each single-restriction deletion.
Exact infeasibility certificates and unresolved solver outcomes have explicit
statuses. Input coefficients have their exact binary64 interpretation.

The executed four-state example has two separate restrictions limiting each
negative-payoff state's probability to one quarter. Together they establish
weak dominance with a zero lower bound. Either deletion leaves a negative
counterexample, so the pair is inclusion-minimal among these candidates. The
unrestricted example has no common optimum. The source-bound result is in
`/Volumes/PortableSSD/tobac-bf1-bf2-20261113/bf1-results.json`.

The [amendment](bf1-credal-amendment-20261113.md) defines this finite linear
scope. The tests compare unrestricted results with the existing exact finite
oracle and retain ties, malformed inputs, near-zero negative cases and solver
failures. The installed SciPy/HiGHS implementation supplies numerical solutions.
Upstream provider promotion and general nonlinear or continuous-state extensions
remain open in the broader frontier plan.

## BF2 finite comparison

`scripts/bf2_benchmark.py` executes the
[frozen specification](bf2-benchmark-spec-20261113.md) and
[execution clarification](bf2-execution-amendment-20261113.md). It enumerates
all state and report paths over three decision periods. Sample time and report
availability differ by one period. The existing evidence contract validates
report identities and conditioning. The equal-spend sensitivity charges added
wastewater samples and measures their additional information in a research belief.

The completed calculation includes all six drift regimes and four sensitivity
families, covering a lower detection limit, uninformative calibration, absent
product signal and shared innovations. The held-out predictive report has ID
`evaluation-only-W-t2` and enters the scoring calculation. The final result is
`/Volumes/PortableSSD/tobac-bf1-bf2-20261113/bf2-results-final.json`.

| Matched-regime design | Gross score | Expected study units | Net score |
| --- | ---: | ---: | ---: |
| No study | 0.500000 | 0.000000 | 0.500000 |
| Fixed sampling | 0.500000 | 2.000000 | 0.440000 |
| Fixed calibration | 0.500000 | 2.000000 | 0.440000 |
| Static staged | 0.547824 | 1.722519 | 0.496148 |
| Adaptive | 0.500000 | 0.000000 | 0.500000 |
| Adaptive with equal spending | 0.500000 | 2.000000 | 0.440000 |

The adaptive planning solution chooses no study under the declared costs and
drift law. It fails the prespecified gross-regret improvement criterion on the
withheld regimes. Its 100% state-set coverage accompanies set size two, retaining
both mixture states. The benchmark therefore reaches its stopping rule without
supporting an adaptive improvement claim. These quantities use the synthetic
score and declared model. Empirical calibration, field validation, intervention-
dependent measurement and Kairos integration remain open.

## Verification and retained gaps

Repo-local Python 3.15.2 executed the new numerical examples and focused tests
under `scripts/run_bounded.py`. The final focused selection passed 81 tests,
including workstream integration. Maintained Nox `strict_all` passed lint,
formatting, nine Ruff-policy tests and whole-source strict typing with zero
errors or warnings. The calculation refactor changed the recorded numerical
results by at most `1.12e-16` across all primary and sensitivity outputs.

The final complete direct test run recorded 1,534 passes, 22 capability skips and
20 failures in hosted-native-lineage tests. The maintained Nox test session
stopped at `Scientific inventory differs from native acceptance`. The accepted
capsule predates these source additions. Native renewal remains with its existing
owner and is required for the complete acceptance workflow. The complete source coverage calculation reached 90.43% and passed the existing
90% gate. The new scientific inventory member is exactly `src/tobac/credal.py`.
A read-only comparison confirms that the preceding inventory matches the accepted
capsule. The precise logs and final-byte hashes are retained in the external
evidence directory and its terminal receipt.


## Reproduction

The BF2 entry point accepts a fresh output path. Run it in the qualified local
Python environment with the bounded runner.

```sh
PYTHONPATH=src .venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python scripts/bf2_benchmark.py --out outputs/bf2-replay.json
```

For BF1, construct `LinearRestriction(name, belief.state_ids, coefficients, upper)`
and call `assess_decision(belief, restrictions)` or
`minimal_identifying_restrictions(belief, action, comparator, restrictions)`.
The independent analytic tests and exact fraction checks are in
`tests/m2/test_credal_certificates.py`. The local numerical demonstration script
is retained under `outputs/bf1-bf2-20261113/reproduce-bf1.py`.


## Native acceptance renewal — 13 November 2026

The owner authorised native renewal and merge after the finite implementation
checkpoint. The scientific execution contract now registers the added module.
Eight fresh native executions and independent readback verified 335 input
references, 140 outputs and 82 exact numerical CSV comparisons. Source queries
and a corrupt-output control passed. The new signed capsule binds the
[checkpoint](../../../integration/archive/scientific-lineage-checkpoint_bf1_bf2_20261113.json)
and [methods-source acceptance](../../../integration/archive/bf1-bf2-source-acceptance_20261113.json).

The failure-only reruns passed the original lineage failures and the additional
native controls. The complete Nox test session passed 1,562 tests, with 18
capability skips and 90.43% source coverage. This supersedes the pending-native
status in the earlier checkpoint above. The new methods-source rejection tests
cover both native and hosted verification. The integration receipt under
`outputs/native-renewal-20261113` records exact candidate and receiving refs.
