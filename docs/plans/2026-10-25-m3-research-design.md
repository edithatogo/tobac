# M3: research design and implementation value

Base: main 886fc08929f8e4e7e34fb6443bbf81545e52c3db. User-approved six additions; no new empirical claims.

Goal: extend the existing finite decision/evidence engine, keeping all source IDs and existing-data contracts. No second incompatible core and no alteration of M1/M2 priors or published outputs.

## Design decisions
- One bounded `tobac.research` layer reuses DecisionProblem, Belief, evaluate and exact_partial_information.
- Exact weighted adapter calls Voiage's released EVPI API on a mathematically transformed value array. It never resamples or duplicates states approximately. Structure-only learning groups parameters before maximisation. Real installed execution is a separate fail-closed probe.
- Joint reports include explicit conditional dependence and shared resource costs. Existing observed data condition Belief once; existing infrastructure offsets only declared costs. Marginal calibration value uses joint minus existing-design value, not standalone EVPPI.
- Prior/structure envelopes do not assign scenario probabilities. Compare complete design sets on one declared value unit; retain negative ENBS.
- Imperfect implementation is a state/intended-action distribution over realised actions. Uptake/delay cases are transparent scenario trajectories, not fitted causal effects.
- Pilot/stopping allows the same actions as fixed/no-study. Interim baseline and posterior decisions use matching timing; costs charged only when bought; optional continuation may be declined.
- Innovate/Kairos remain optional. Materiality of uptake/delay is assessed before importing them; no false claim that scenario curves are their fitted outputs.

## Tasks and tests
- [x] Weighted Voiage transform; zero weights, extreme weights, state duplication, shift/scale, missing library; identical structure counterexample; mismatched action/unit rejection.
- [x] Joint source portfolio; noisy/correlated reports, redundancy, complementary calibration, shared fixed costs, D0 duplicate rejection, marginal cost/value consistency.
- [x] Complete scenario envelope; no invented scenario probabilities, regret and robust preference, missing design/unit rejection.
- [x] Implementation; identity/no implementation/partial cases, four-cell interaction, transparent time weights.
- [x] Pilot/continue/stop; exact branch recursion versus exhaustive choices, sunk cost, zero/repeated signals, delayed matched comparators.
- [x] M2-based runner; result hashes, non-overwrite, qualification receipt and optional package probe; existing methods preserved.

## Verification boundaries
Run failing tests before implementation; rerun original regulatory tests and M1/M2 invariants, new tests and cross-workstream checks where the live files are available. Re-read main/#1 before expected-head publication. Record any incomplete full-checkout/hosted/library execution instead of reporting a pass.

## Execution ruling
The mathematical contracts and bounded M2 study runs passed. Actual installed Voiage remains blocked (PackageNotFoundError and failed release download); the first task is therefore partial at external-integration level, not fully qualified. Current main advanced to 5218d831 during the work; its additions are evidence/docs only and are preserved by the publication base. No historical source or published result is overwritten.
