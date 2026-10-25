# M3 — research portfolios, structure-only information and staged decisions

25 October 2026. Receiving base: `5218d831f8b2452c7937da91ee00bf9b96183b2d`, including the longitudinal, engineering and prior-work incorporation changes. This is conditional research software, not a fitted current NZ posterior or a funding recommendation. No political position is an acceptance criterion.

## Completion against the six approved additions

| Addition | Delivered | Remaining qualification |
|---|---|---|
| Weighted Voiage and structure-only EVPPI | Exact weighted-contrast adapter, finite-partition averaging, units/action guards, independent fixtures and a genuine installed-library probe | Voiage 2.2.0 is not installed locally; its execution gate remains blocked. Mathematical parity is not installed-package parity. |
| Joint-source portfolios and calibration | Joint-report marginals, dependence, complementary calibration, redundant reports, shared assets, signed ENBS and once-only D0 | Study performance and costs are explicit scenarios, not qualified NZ estimates. |
| Robust priors and structures | Five structural cases, three current-market prior probabilities and three normative weights; unweighted envelopes and regret | No probabilities are assigned to competing viewpoints; no empirically established robust optimum. |
| Implementation-adjusted VOI | State/intended/realised-action kernel, four information/implementation cells and uptake profiles | Trajectories are assumptions, not fitted Innovate outputs or observed evidence-to-policy adoption. |
| Pilot–continue–stop | Exact two-stage policy compared with matched no-study, pilot-only and fixed-both; shared costs and timing | Static-world reference, not a calibrated changing-market surveillance controller. |
| Innovate/Kairos where justified | Uptake/delay materiality shown; explicit future adapter contracts | Neither package was executed or made mandatory. Empirical uptake/queue data must justify that extension. |

## Scientific and numerical definitions

The calculation reuses the existing `DecisionProblem`, `Belief`, `condition`, `evaluate` and M2 policy/assay channels. Learning a structure averages residual parameter uncertainty before maximising. Two identical uncertain structures therefore have structure-only EVPPI zero, while joint parameter/structure EVPI can be five in the test example. The chain `joint EVPI = structure-only EVPPI + expected within-structure EVPI` is checked.

The Voiage adapter applies the exact transform `n*p_s*(V_sa-V_s0)` to the released expected-value EVPI function. It does not resample, round weights, multiply population twice or pretend the transformed values are PSA draws suitable for entropy/risk methods. The actual library receipt is blocked, not replaced with a fake implementation.

Prospective sources retain physical-state IDs and future underlying-data IDs. Already used evidence cannot be sold again. Shared infrastructure is charged once, while new-sample costs remain payable. Explicit joint outcome tensors preserve report dependence; otherwise independence is conditional on the complete latent state. The small complementary-calibration fixture gives zero value to either source alone and positive value to the pair. This is a mathematical fixture, not a tobacco assay performance claim.

## Run scope

The complete run contains 45 scenario/weight decisions and 12 study designs: 540 portfolio rows, 270 grouped-information rows, 135 conditional-increment rows, 36 robustness summaries, 11 structure-probability sensitivities, four uptake profiles and six staged designs. The reference prior has 12,288 states. A separate four-node reference refinement has 20,480 states. All 2,105 full-run invariants passed. Model-probability sensitivity curves remain separate from the unweighted robustness envelope.

**All study costs and values in these runs are normalised decision units, not NZD or QALYs.** Their prices are illustrative research-design scenarios, not replacements for the preserved empirical cost ledger. One cannot use the numerical ENBS signs as an NZ procurement recommendation.

## Findings under the reference assumptions

### Calibration and quantification
Calibration alone has zero decision value. Added to the panel plus lawful-supply information it adds approximately 0.000234 gross decision value at two nodes, or 0.000254 at four. Its assumed extra cost is 0.000300, so its incremental ENBS is negative in this particular scenario. Across other declared structures the preferred information programme differs. This is why calibration must be valued conditionally, not discarded because standalone EVPPI is zero.

Better quantification has zero incremental decision value in the reference case despite a changed observation channel. This is not evidence that assay improvement has no scientific value or no value at other detection limits/prior supports.

### Uptake can reverse a decision
For the matched causal total-and-lawful study:

| Uptake profile | Effective uptake | EVSI | Assumed cost | ENBS |
|---|---:|---:|---:|---:|
| Immediate complete | 1.00 | 0.022002 | 0.011000 | 0.011002 |
| Gradual | 0.54 | 0.011881 | 0.011000 | 0.000881 |
| Delayed | 0.36 | 0.007921 | 0.011000 | -0.003079 |
| Limited | 0.20 | 0.004400 | 0.011000 | -0.006600 |

These profiles apply to five subperiods of the existing valued horizon, not five additional years or a lifetime extrapolation. The unimplemented portion realises the declared reference policy. Sunk launch costs, evidence-dependent adoption and changing background states would require additional modelling.

### Stopping can save costs without justifying the pilot
At the reference follow-up cost, prompt reporting gives adaptive ENBS 0.005977. Slower reporting gives -0.000386, compared with -0.002760 for mandatory follow-up. Under the slower schedule continuation occurs after about 36.1% of pilot results. Adaptive stopping improves on a forced programme, but no new study is still preferred at those assumptions. All designs have matching action opportunities and timing; follow-up is charged only when purchased.

### No invented consensus
At normative crime weight one, no purchased design has positive ENBS in every tested prior/structure scenario. The preferred option changes between no research, matched causal work and combined programmes. The minimum-ENBS, maximum-regret and preferred-scenario tables are retained rather than averaging opposing viewpoints into an invented probability distribution. A null-effect scenario legitimately reduces the value of some research.

## Evidence and prior work preserved

No historical supply posterior or forecast was relabelled as a current observation. The D0 table contains possible synthetic lawful-supply report outcomes, not new NZ field evidence. Source records, the 19 prior-work reference files, the longitudinal code/results, Conductor gitlink and engineering gates are preserved through the receiving base tree. The larger old archives remain historical references rather than automatically active models.

## Reproduce and inspect all saved outputs

    python -m tobac.research.runner --out outputs/m3
    python scripts/verify.py outputs/m3
    python -m tobac.research.runner --config configs/m3_research_refinement.json --quick --out outputs/m3_refined
    python scripts/verify.py outputs/m3_refined

Or restore the exact saved full/refinement outputs without rerunning:

    python scripts/unpack_m3_results.py --out outputs/m3_saved
    python scripts/verify.py outputs/m3_saved/full
    python scripts/verify.py outputs/m3_saved/refined

The three binary archive parts concatenate to a 22,740-byte tar.xz; SHA-256 `6249990f4b8c4e499c446966d693d5681bab9b7af64cd3df4b0078f8f0e5875f`. The standard-library unpacker checks each part and complete hash, bounds decompression, rejects unsafe paths/links and refuses to overwrite. It restores all 24 original CSV/JSON files and their run manifests. Compact tables accompany this report.

## Verification and explicit limits

162 scoped tests passed: the 101 regulatory/M2 tests, 26 real cross-workstream tests and 35 M3/preservation tests. This is not a fresh run of all longitudinal, engineering or incorporation tests in the full live checkout. All unchanged numerical-module blob IDs were compared with current GitHub source; the reviewed concurrent commit changed evidence/docs only. M3's full replay and both saved-run manifests passed again immediately before publication. The M1 replay retains 974 passed invariants and nine inherited definitions unchanged.

Actual local Voiage qualification failed with PackageNotFoundError; pip and release downloads did not resolve an installable package in this runtime. Source/release inspection does not substitute for execution. Nox/uv and genuine installed-library jobs are configured but not declared executed locally. Sourceright/CiteWeft qualification remains open. Hosted run status and publication commit are recorded separately after the guarded update. No independent third-party scientific review, full dependency lock qualification or fitted NZ market model is claimed.

The next scientific work is to qualify the likelihoods, empirical/elicited priors, implementation and timing inputs for a feasible matched consumption/supply comparison. More software features cannot replace those definitions.
