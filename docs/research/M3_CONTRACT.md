# M3: information portfolios, implementation and staged research

Date: 25 October 2026. Approved scope: six additions to `tobac`, not a new empirical NZ policy conclusion. The executed numerical path reuses `DecisionProblem`, `Belief`, `condition`, `evaluate` and the unchanged M2 policy/measurement functions. Existing source identifiers, observed-data boundaries and historical results are preserved.

## 1. Weighted Voiage and structure-only information

For finite weights p_s, transform action contrasts as n*p_s*(V_sa-V_s0). An unweighted expected-value EVPI function applied to this array returns the exact weighted EVPI. Zero weights stay zero; there is no resampling or approximate integer replication. The transformed array is an adapter for this expectation functional only: it is NOT PSA data and must not be used for entropy, risk preferences, CEACs or covariate inference. Inputs already carry the decision scale; no additional population/time multiplication is applied.

Partition the joint prior and average remaining parameters within each group before maximising. Model-structure-only information therefore differs from perfect information about both model and parameter state. Identical structures with uncertain payoffs have zero structure-only value but can have positive joint EVPI. The chain `joint EVPI = structure-only EVPPI + weighted within-structure EVPI` is tested. Structure probability curves are explicitly conditional sensitivity analyses; no preferred prior over political viewpoints is invented. The main robustness analysis never averages scenarios.

`qualification.py` calls the actual released `voiage.methods.basic.evpi` at verified release 2.2.0, then the same call on collapsed groups. It fails closed if unavailable/wrong/mismatched. Mathematical adapter tests, mocked failure-path tests, an upstream package release and an actual installed-package run are distinct evidence. This scope does not certify Voiage's generic EVSI or its structural function. The latter's naming/estimand concern remains separate; no upstream fix was made.

## 2. Joint reports, calibration and shared costs

Each prospective Source retains physical state identities/order and underlying future-data IDs. A previously observed data ID cannot be purchased again. Distinct sources are conditionally independent only GIVEN the complete shared latent state unless an explicit joint tensor is provided. Joint tensors must have all declared marginals. Duplicate reports can be perfectly redundant, while calibration and chemical measurements can be jointly informative despite having no standalone decision value. The exact XOR test demonstrates this logic without pretending it is observed NZ performance.

Shared infrastructure is charged once across selected sources. Already-owned assets offset only their declared future fixed cost, not the cost of new samples. Conditional calibration value is joint EVSI minus EVSI without calibration; negative incremental ENBS is retained. A declared asset or source cost remains an assumption until supported by evidence.

Existing evidence uses the common `EvidencePacket` and `condition` route. The M3 D0 table enumerates possible synthetic supply outcomes; it is not a new current NZ posterior. Expected later information value equals joint-minus-first value before observing D0, but value after a particular result need not equal that preposterior average.

## 3. Robustness

Evaluate the same set of designs under every declared prior/structural scenario. Report minimum/maximum ENBS, worst scenario regret and where each design is preferred. No scenario probabilities are required or silently supplied. Normative crime weights are reported separately, not pooled with empirical uncertainty. Equal unit labels are a necessary computational check, not proof that population/horizon/perspective have been scientifically harmonised.

The M3 runner uses five existing M2 structural cases, three high-illicit prior probabilities and three normative crime weights. Costs are illustrative NORMALISED DECISION UNITS, not NZD, QALYs, quotes or a priced programme. The twelve designs are an evaluated subset, not all possible surveillance networks. No-study is always included.

## 4. Imperfect implementation

A kernel maps state and intended action to probabilities over realised actions. This allows state/action-dependent implementation, not merely a universal scalar. Four cells distinguish current/perfect information and current/perfect implementation. Their interaction can be signed and is not truncated.

The demonstration uses explicit uptake profiles over five equally weighted subperiods of the already-valued horizon. Non-implementation realises the declared reference policy. These profiles are assumptions, not fitted Innovate predictions. Multiplying a whole payoff by uptake is valid here only because the kernel delays/reduces the corresponding realised action and its costs together. Independent fixed launch costs or changing background states require an extended contract.

## 5. Pilot, continue or stop

The exact two-stage calculation retains the current best action while waiting. Fixed and adaptive designs can both revise action after the pilot and after the follow-up; no-information has the same feasible action set and horizon. Pilot costs are paid once; follow-up is paid only if purchased. Shared assets are not repurchased. An explicit joint tensor can represent dependent reports. Values and realised continuation branches are consistent, including near ties.

Remaining-time fractions apply to one fixed value horizon. This is a static-world reference, not a full dynamic market/control model. It does not manufacture annual EVSI by summing repeated uncertainty reductions. A forced pilot can have negative ENBS; the no-study alternative can still win even when adaptive stopping improves on a fixed research plan.

## 6. Optional Innovate/Kairos boundary

Uptake and reporting-delay scenarios materially change conditional funding results, so implementation trajectories and operational delay deserve investigation. They do not yet justify mandatory dependencies. Innovate could supply qualified uptake/substitution trajectories; Kairos could supply event/queue/delay distributions. Neither is executed or fitted by this module. Current equations are sufficient reference cases against which future adapters must show parity and incremental value.

Any exported extension must retain scenario/draw IDs, timing, units, current-data IDs, provenance and whether uncertainty is empirical, elicited or assumed. Forecast paths are not new observations. No algorithm identifies legal origin, policy causality or ethnicity merely from wastewater. Governance, independent review, field calibration and matched causal comparisons remain external scientific requirements.

## Execution

    PYTHONPATH=src python -m pytest -q tests/m3 tests/test_workstream_integration.py
    PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -m tobac.research.runner --out outputs/m3
    python scripts/verify.py outputs/m3
    PYTHONPATH=src python -m tobac.research.runner --config configs/m3_research_refinement.json --quick --out outputs/m3_refined
    PYTHONPATH=src python -m tobac.research.qualification --out outputs/actual_voiage.json

The existing Nox environment is reused by `nox -s research_m3`. The last command is a genuine external gate and exits nonzero while Voiage is unavailable. Source/manifest checks do not certify a successful hosted run or fresh dependency installation.
