# M2a — evidence conditioning and a defined retail-policy contrast

24 October 2026. Additive update from GitHub main 10b8c23. **Conditional source-informed research, not a current NZ posterior, policy impact estimate or funding recommendation.** No political result is an acceptance condition.

## What changed

A strict observed-evidence boundary now fingerprints physical state values and checks source/underlying-data identities, scope, transport and dependence. Forecasts and posterior summaries cannot silently become independent measurements. The lawful-supply bridge distinguishes consumption from recorded releases, inventory change, outbound/loss flows and lawful unrecorded supply. Signed stock change and correlated reporting errors are supported; impossible negative accounting results are rejected, not clipped.

M1's arbitrary gross-displacement support remains intact. A separate retail structural case uses the published Beta(23.4,97.2) net-cessation model input from Ait Ouakrim et al. Table 2 (DOI 10.1136/tc-2022-057655). This is a constructed model prior for about 300 outlets/95% reduction, not measured efficacy for a 600-outlet cap. The Ministry's 2023 plan and 2024 suspension/repeal define the historical policy precedent, not a realised national experiment. See `docs/m2_retail_contract.md` and `evidence/m2/source_review.json` for exact meanings and sources.

Cases include null effect, attenuated transport, an 80% source-shaped/20% null mixture, and zero/half/full replacement with lawful cigarettes after illicit-market disruption. Those probabilities and transport factors are assumptions. A total-consumption causal channel is kept distinct from a matched total-and-lawful-consumption channel. The latter presupposes an appropriate counterfactual and supply reconciliation, not an assay of illegal origin.

## Conditional results

Reference: source-shaped mixture, half lawful replacement, crime weight 1. All values below are **normalised decision units, not NZD or QALYs**. Do not compare these as empirical rivals to M1 or add grouped EVPPIs.

| Quantity | Value |
|---|---:|
| EVPI | 0.061815 |
| EVPPI: behavioural response | 0.030261 |
| EVPPI: implementation/mitigation | 0.020017 |
| EVPPI: incremental criminal harm | 0.019452 |
| EVPPI: current market | 0.007020 |
| EVSI: panel plus supply | 0.000333 |
| EVSI: calibration, panel and supply | 0.000587 |
| EVSI: total-consumption causal report alone | 0 |
| EVSI: matched total-and-lawful causal report | 0.022123 |
| EVSI: panel/supply plus matched causal report | 0.022190 |

Total-consumption causal information learns net cessation but cannot identify lawful-to-illicit switching in this structure. Its zero decision value at these assumptions does not mean zero scientific learning. A matched lawful-consumption comparison can make the switching uncertainty decision-relevant. These study-performance assumptions have not been empirically qualified.

The selected action also depends on what follows illicit-supply disruption. With no lawful replacement, restriction plus support is preferred in the source-shaped scenario; with half/full replacement, expanded cessation is preferred. This is a demonstration of structural sensitivity, not a recommended NZ regulatory package.

## Prospective versus realised information

The exact preposterior chain is checked: expected value of the second report after the first equals joint EVSI minus first-report EVSI. Repeating an identical correlated report is tested to add no information. Expected remaining EVPI equals initial EVPI minus first EVSI.

Two **synthetic** release observations (250 and 500, assumed SD 80) demonstrate realised updating. They alter current-market beliefs but leave an independent causal diversion prior unchanged. The second example increases realised remaining EVPI; that is consistent with its expected preposterior decrease. Neither example is an NZ observation. See `conditioning_fixtures.json`.

## Numerical and execution checks

101 tests passed. M2a enumerates five structural cases, three normative weights and 15 designs; 805 invariants passed. The source-effect grid check uses 2/4/8 nodes (reference 12,288/20,480/36,864 states). EVPI changes 0.061358 -> 0.061815 -> 0.062018; matched-causal EVSI changes 0.022002 -> 0.022123 -> 0.022184. This is refinement of one axis, not full convergence of all supports or proof of external validity.

All 974 M1 checks passed again. All eight original M1 CSV outputs are byte-identical and nine inherited numerical definitions remain unchanged. An offline installed-wheel CLI run passed 63 checks with existing dependencies. Genuine local Sourceright and voiage probes failed because the packages/executables were absent. CiteWeft was not executed. Hosted execution must be read separately; a workflow file is not a successful run.

## Integration and remaining work

Issue #1 received an actual coordination comment; the parallel branch still pointed to 4b36ea6 at inspection. No completed `tobac_supply` module or current field data were received/merged. The interface is ready for reviewable dated observations and jointly specified errors, not automatic assimilation of forecasts.

The next scientific task is a qualified matched consumption/supply design around a specified prospective policy, with local assay sensitivity, counterfactual assumptions, policy response, substitution and incremental harm evidence. Registry, dates, governance and independent source-applicability review remain material. Full output tables/hashes are in the delivery archive and regenerated by `python -m tobac.m2 --out outputs/new --grid-check`; this directory contains compact complete summaries and reference-case projections.
