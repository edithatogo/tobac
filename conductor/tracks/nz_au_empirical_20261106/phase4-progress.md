# Diffusion, competition and extended VOI — 6 November 2026

P4.1 source/API discovery, scenario contracts and existing finite-component qualification
are implemented locally. Empirical Phase 4 remains incomplete. No new diffusion engine,
competition fit, empirical EVSI/ENBS or Innovate adapter was added. M3 source/tests,
scientific inputs, dependencies and native bindings are unchanged.

## Actual execution and library boundary

The existing installed Voiage qualifier ran on the retained repo-local ecosystem
environment: Python 3.15.2, Voiage 3.1.0, success true, status passed, five finite checks.
The four weighted cases reported maximum absolute error 6.077470925670262e-16; the fifth
checks the structure-only counterexample. Its unchanged acceptance tolerance is 1e-11.
Bounded process-group RSS peaked at 225.6 MiB; command exit 0. Logs/receipt:
outputs/nz-au-phase4/voiage-qualification.log and voiage-qualification.json. This is actual
installed-library execution on synthetic fixtures, not NZ/AU observations or generic EVSI
certification. The task card's initial tolerance transcription was corrected from 1e-10
to the actual source constant 1e-11; no numerical threshold changed.

Innovate main b9998addf32717438df92b23a306903e4db51620 and current PyPI 0.6.0 metadata
were read directly. Both require pandas/pandasdmx despite the optional Polars extra.
The Python requirement is compatible; the no-pandas boundary is not. Source inspection
identified BassModel (predict, cumulative_adoption, predict_adoption_rate) and
LotkaVolterraCompetition (compute_interaction_rates, predict_states,
get_parameters_schema). Actual imports, calls, fit recovery and numerical parity remain
unexecuted; source API names do not establish adapter compatibility.

Four original source/metadata files were externally staged with exact hashes and readback,
recorded in phase4-source-receipts.json. They are not empirical datasets or durable native
archive admission. No installation, --no-deps bypass, code copy, upload or external message
was performed. Existing ownership of M3 and native latest-lock admission is preserved.

## Delivered requirements and remaining evidence

phase4-design.md binds state/intended/realised action kernels, temporal uptake limitations,
incremental conditional EVSI/ENBS, information/implementation interaction, shared assets,
correlated reports and matched-timing adaptive studies. phase4-scenarios.csv declares ten
boundary/structural comparisons with their current execution scope. Existing test fixtures
are explicitly separated from unexecuted empirical competition and transport scenarios.
No scenario row implies that a calibrated NZ/AU trajectory was simulated.

Remaining gates: Phase 0–3 acceptance; compatible installed Innovate; measured adoption
denominators, networks, spillovers and causal competition; matched current policy payoffs,
likelihoods, real programme costs and timing; country-specific validation. The current
normalised payoff scale cannot produce a monetary funding claim without justified valuation.
The owner's current status still reports dependency candidate unapplied; queued receiving
checks are not native admission. No shared source was changed to interrupt that work.

Focused M3/reference, workstream and publication-boundary tests passed: 82 in 4.90 s on
Python 3.15.2; bounded sampled process-group RSS 334.6 MiB; exit 0. Receipt:
outputs/nz-au-phase4/focused-tests.log. This includes saved finite references and synthetic
negative/dependence/branch cases; it is not a new empirical fit. External byte/hash readback,
publication-path existence/uniqueness and git diff --check pass. No new dependencies or
numerical source were added; existing unchanged engineering evidence is retained.
No new full-suite, clean-package, native/hosted execution or empirical fit
success is claimed. Next: complete upstream admission and the matched empirical slice,
then qualify a compatible Innovate adapter and accepted policy mechanisms before empirical
diffusion/competition/extended VOI. No original Phase 4 task is closed by this preparation.
