# Measurement, disagreement and conditional worth: analytical scope

Supplementary preparation note, 28 October 2026. This is an analytical explanation
of existing decision value and an explicitly hypothetical uptake bridge. It is not
an executed empirical model of political convergence or a new observation likelihood.

## Existing calculation

Expected value of sample information (EVSI) measures decision value under a fixed
objective. It is distinct from expected net benefit of sampling (ENBS), which also
requires compatible incremental research costs.

For a fixed objective u, prior p(theta), actions a and report Y with an explicitly
specified likelihood:

    V0 = max_a E[u(a, theta)]
    EVSI = E_Y[max_a E[u(a, theta) | Y]] - V0

The engine can report expected physical/model consequences for each action. EVSI
is the scalar utility difference under the declared weights; it is not the
unweighted difference in every outcome, the probability of persuasion, agreement
or an observed policy effect. Changing action may improve one outcome and worsen
another. Changing objectives changes the evaluation, not the evidence itself.
The same underlying data cannot be independently reconditioned under another label.

The 13 challenge specifications are model sensitivity cases, not empirical actor
priors. The 25 value profiles are declared scenarios, not a social preference
sample or an uncertainty distribution over values. Existing policy-set changes do
not count people persuaded, and no posterior belief-distance statistic is computed.

## Prospective uptake/cost bridge and its assumptions

Let a0 be one fixed current optimal action, and a*(Y) an optimal action after Y.
Select ties consistently under the same evaluation objective. Suppose B is an
implementation/response indicator with probability p independent of Y and theta.
The action is a*(Y) when B=1, otherwise a0. Under the same prior, utility and
likelihood, with no other action pathway:

    E[u(action, theta)] - V0 = p * EVSI
    net scenario value = p * EVSI - C_study - C_delay

Costs must use the same utility scale, population and horizon as EVSI and represent
incremental costs rather than double-counting resource consequences already in u.
There is no monetary conversion or applicable national population multiplier in the
existing results. C_delay is a supplied expected opportunity cost; no cost of delay
has been estimated. Negative net values and no-study remain permissible.

When EVSI>0 and C_study+C_delay>=0, break-even p is (C_study+C_delay)/EVSI;
a threshold above one cannot be met within this restricted response scenario.
When EVSI=0, no strictly positive cost can be justified through this pathway. At
zero cost there can be indifference. These identities introduce no fitted parameter.
The p multiplier is not a universal correction or bound: if uptake depends on Y,
theta, actor, action or outcome, integrate the explicit response policy instead:

    E_Y,theta[sum_a P(a | Y, theta) * u(a, theta)] - V0 - costs

Conditioning the action on theta in that expression is a general joint response
model, not an assumption that a decision-maker observes the true state. A practical
response model must use only the information actually available to its actors.
Other institutional or welfare objectives also require explicit specification.

No p, actual study price, delay loss, shared welfare criterion or causal effect of
agreement is estimated here. The algebra does not establish that a wastewater study
is worthwhile. Existing gross EVSI under hypothetical performance is an input to
such an assessment, not a funding recommendation. No synthetic agreement percentage
or NZD value is introduced to fill the gap.

## What would be required for stronger claims

| Stronger claim | Missing link | Current treatment |
| --- | --- | --- |
| Testing narrows beliefs | Actor-specific starting beliefs, trusted report models and report-responsive belief revision | Not estimated; not inferred from challenge-case priors |
| Narrower beliefs reduce policy disagreement | Explicit objectives and a defined decision/agreement measure | Value-sensitivity scenarios retained; no representative preferences claimed |
| Reduced disagreement improves consequences | Evidence-use and implementation mechanism plus a declared evaluation objective | Conditional uptake identity only; no empirical probability |
| Benefits exceed actual research costs | Qualified target performance, compatible incremental costs, delay and scope | No priced empirical ENBS or real commissioning claim |
| The policy caused a consumption change | Matched scope and credible counterfactual | No causal claim from trend or repeal |

These are limits on stronger claims. No new field data, governance outreach,
preference elicitation or access/OIA request is prepared or sent. Author/institutional
facts and any applicable formal requirements remain in the declaration record.
