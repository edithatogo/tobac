# Diffusion, competition and extended VOI contract — version 1

6 November 2026. Status: source/API discovery and finite synthetic software qualification.
Empirical Phase 4 remains gated by Phase 0–3. No fitted NZ/AU adoption, competition,
spillover or monetary research-value result is produced by this contract.

## Reuse and actual library boundary

M3 owns src/tobac/research. Reuse implementation_values/adoption_kernel/decomposition,
portfolio Sources/Costs, exact two_stage/staged_portfolio, finite structural information
and the weighted Voiage adapter. Existing tests are numerical references, not calibration.
Their hypothetical uptake trajectories are explicitly not fitted Innovate outputs.

[Innovate main b9998add](https://github.com/edithatogo/innovate/tree/b9998addf32717438df92b23a306903e4db51620)
and published 0.6.0 both still require pandas and pandasdmx; the dataframe extra adds
Polars without removing them. Python >=3.15.1,<3.16 is compatible with this interpreter,
but the dependency graph violates the no-pandas requirement. Source modules for Bass and
Lotka–Volterra were inspected and externally preserved with hashes; source presence does
not establish import/API execution, numerical stability or suitability for policy adoption.
No --no-deps install, downstream copy or parallel diffusion implementation is permitted by
this task. A compatible upstream graph and locked exact installed API must be qualified
before connecting Innovate to the shared state/evidence contract.

## Decision timing, uptake and competition

Keep policy intention, legal commencement, implementation, compliance, product use and
health response as separate processes. Fix country, jurisdiction, eligible population,
action, state and time keys before connecting any trajectory. An Innovate adoption fraction
needs a measured denominator: authorities adopting policy, retailers complying, or people
changing behaviour are different quantities. Wastewater catchments are not automatically
policy-adopting authorities. NZ and AU alone cannot identify network competition effects.

F:D1: implemented payoff U[s,i] = sum_j K[s,i,j] * V[s,j], where K is conditional on state
and intended action, nonnegative and sums to one across realised actions. The existing
implementation_values computes this on the original complete payoff, including resource
consequences. It is a conditional static-world representation, not an epidemic, market or
population transition model. Reference action and costs must have explicit timing.

Bass/logistic curves are candidate uptake mechanisms; competition, saturation, substitution,
withdrawal, delay and spillovers require their own data and identifiable parameters. A
positive spillover is a scenario assumption until supported. Competing mutually exclusive
adoption shares need a joint constraint; dual use or coexisting policies cannot be forced
into that simplex without a defensible state definition. Treat causal competition and
correlated response to shared shocks as structural alternatives.

discounted_uptake returns a normalised weighted mean, not discounted total benefit. Its
scalar substitution into a static kernel is justified only where payoff effects are
separable and the weighting matches that payoff's already-valued horizon. It cannot capture
nonlinear disease latency, path dependence, product switching or study-dependent diffusion.
Such cases need a separately validated temporal model and an independent reference.

## Extended VOI estimands

Condition once on existing evidence D0 using the existing Belief/EvidencePacket data IDs.
For a fixed action set, horizon, objective and implementation regime:

F:V1: EVSI(Y | D0) = E[Y|D0]{max_a E[U(a,theta)|D0,Y]} - max_a E[U(a,theta)|D0].
EVPI replaces the prospective report by complete decision-relevant state information;
grouped EVPPI reveals only the selected component, integrating nuisance uncertainty before
maximising. Preserve dependence between WBE, surveys, lawful flows and calibration. ABS
derived estimates do not independently replicate ACIC observations. Repeated perfectly
correlated reports add no information about that same state. Targeted entropy/variance
reduction is a different estimand and cannot be added to benefit-valued VOI.

F:V2: ENBS = gross study benefit with matched decision timing - expected incremental study
resource cost. Retain no-study and negative net study values. A setup asset used by multiple
reports is charged once; follow-up costs are charged with the continuation probability.
Implementation resource use already inside V cannot be charged again as a study expense.
Actual programme prices, currency/price year, delay and downstream effects are unverified;
there is no empirical NZD ENBS or funding recommendation. A normalised score cost ceiling
cannot be labelled money without a justified valuation model.

F:V3: with W00=current information/current implementation, W10=perfect information/current
implementation, W01=current information/perfect implementation and W11=both perfect,
interaction = W11-W10-W01+W00. Joint gain equals information gain + implementation gain +
interaction. The interaction can be signed. Do not sum overlapping information/implementation
claims or multiply EVSI by arbitrary uptake after changing the payoff or action set.

two_stage is an exact static-world pilot/follow-up calculation with matched action timing:
both fixed and adaptive designs can change actions after the pilot. Its remaining fractions
refer to one already-valued horizon, not extra years/populations to multiply again. Joint
report likelihoods must have the declared marginals; shared data cannot be sold again.
The existing finite memory limit is retained. Dynamic state evolution, study-induced
learning/adoption or irreversible decisions need an explicit extension and new oracle.

## Scenario execution and validation gates

phase4-scenarios.csv prespecifies boundary, dependence, delay, implementation and competition
comparisons. Boundary values 0/1 are mathematical fixtures, not empirical parameter estimates.
Empirical scenarios need accepted source hashes, causal mechanisms, costs and posterior
draws, paired policy seeds and independent validation seeds. Report MC error and nested
simulation bias where approximation is used; exact finite cases remain the small oracle.
EVSI/EVPPI bounds are compared under the same payoff and implementation regime. A bound
under perfect implementation is not automatically the bound for a different uptake model.

Qualify any Innovate adapter on no-change/zero-adoption/full-adoption limits, no competition,
zero spillover, mass/denominator constraints, parameter recovery and held-out prediction.
Run parameter, structural, prior and value sensitivity without treating hypothetical
parameters as estimated probabilities. Networks need documented nodes, edges, interference,
confounding and observation process. Country-specific calibration and transport remain
separate. Scenario disagreement can be a valid result; empirical acceptance stays open.

The executed installed Voiage qualifier covers only weighted EVPI and finite-partition
transforms. Its uniform-equivalent payoff transform is not a PSA sample, entropy input,
generic EVSI adapter or CEAC input. No generic library certification is claimed.
