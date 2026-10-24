# Regulatory uncertainty milestone implementation plan

**Goal:** Determine which empirical uncertainties can change a specified regulatory choice, then evaluate which information sources can learn them.
**Architecture:** Additive tobac layer uses unchanged DecisionProblem/EVPI/finite-partition and physical signal definitions from the verified predecessor. Exact enumeration over explicit finite hypotheses avoids labelling individual continuous PSA draws as parameter groups. Scientific information and decision value remain separate.
**Tech stack:** NumPy/SciPy; genuine external integrations qualified separately.
**Spec:** docs/protocol.md; user-approved reframing.

## Tasks and gates
- [x] Information contracts: analytic binary, perfect/no-information, entropy, action switches, same-data robustness, invalid inputs.
- [x] Regulatory model: archetypes, mass balance, legality-invariant chemistry, separate consequence ledgers, joint prior scenarios.
- [x] Evidence/design: source and assumption review, current versus causal-study likelihoods, calibration/supply combinations.
- [x] Local milestone: nine priors/dependence cases, four value weights, thirteen experiments, exact oracle and MC integration check.
- [ ] Hosted qualification: run and inspect numerical CI, Sourceright and voiage receipts; a workflow definition is not success.
- [ ] Empirical qualification: real NZ policy contrast, supported response/harm priors, field likelihood, governance, costs and external prediction.

## Constraints
No tuning to a favoured policy or funding result. No source point becomes an invented posterior. Existence differs from magnitude, causation and harm. Quotes are not required for gross VOI. Preserve original archives. Do not claim unseen peer branches merged. The primary finite screen is not a continuous-posterior fit.

## Review focus
Zero-probability signals, common large payoffs, prior dependence masquerading as causation, shared calibration counted twice, and conflation of scientific and decision value. Mathematical and scientific review are separate gates.
