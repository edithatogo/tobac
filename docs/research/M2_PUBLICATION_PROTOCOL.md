# Conditional publication analysis protocol

Dated 28 October 2026, before this track's value-grid execution. This is not a
preregistration. Existing M1/M2/M3 development, source review, the five retail cases,
crime-weight scenarios and original VOI/bounds results predate this protocol.

## Question and contribution

Under what combinations of empirical/structural assumptions and value trade-offs do
retail restriction, restriction with support, expanded cessation or the reference
remain preferred? Which information could change that choice under each declared
objective? Distinguish variation in consequences from disagreement about valuing them.
The contribution is an auditable robustness/frontier analysis and conditional research
prioritisation, not an estimated effect of an implemented NZ600-retailer policy.

Target discussion: NZ residents15+ using cigarettes/roll-your-own; existing synthetic
representative-catchment model and equal-intensity transport remain explicitly
unqualified for that target. The numerical model is a one-year comparative response,
not a lifetime health model. No QALYs,deaths or NZ-dollar conversions are inferred.

## Locked analysis choices

Reuse configs/m2_retail.json's five cessation/null/transport/replacement cases and
configs/regulatory.json's state axes, source-model Beta input and finite state weights.
These are assumptions or transported source-model inputs, not observed effects or
source-informed probability distributions for the current NZ target. Do not attach
probabilities to the five competing structures.

New normative grid:health weight1;crime and real-resource-score weights independently
0,0.5,1,2,4. Health is the common scale anchor;this does not represent measured social
preferences. Zero crime valuation differs from the existing empirical zero marginal
harm state. Zero resource weight ignores resource scores in this objective,not actual
resource requirements. The support endpoints are analyst choices,not elicited bounds.

U = H - w_crime*C - w_resource*R,where C is incremental signed criminal harm and R
is the existing illustrative real-resource score. Fiscal-volume changes remain a
separate descriptive quantity;do not add tax transfers as social resource losses.
Report the four action consequences and all co-optimal actions using absolute
numerical tolerance1e-11. The reference is always retained.

For each of125case/value combinations,compute exact finite EVPI and the seven
existing grouped EVPPI partitions,then EVSI for the six predeclared report designs.
A design includes a no-information comparator;gross EVSI is a same-objective study-cost
ceiling,not a priced study,net benefit or commissioning recommendation. Causal report
channels presuppose identification not supplied by baseline wastewater.

Compute isolated crime-weight upper-envelope intersections at every declared resource
weight. Ignore intersections of dominated actions;preserve persistent co-optimal ties.
For fixed prior/structure and health1,expected-value differences are affine in the two
normative weights. An action co-optimal at every rectangle vertex is co-optimal across
the whole continuous rectangle. Intersect these sets across all five structures for
a joint robustness claim. An empty intersection means no common expected-utility
optimum on this support,not universal policy inferiority or public disagreement rates.
Do not count grid rows as probabilities or average utilities/VOI across value profiles.

## Evidence use and verification

The public map supplies provenance,method limitations and applicability challenges.
Validate manifest hashes,document/extraction references and all no-adoption flags.
Record every source's role in source_use.csv. No new source is automatically conditioned
on or fitted as a likelihood/prior;the inherited published model-input provenance is
separate from the current public-map observations and shared MOH/NZHS/calibration groups.
National supply alternatives can be reproduced descriptively;they do not calibrate a
catchment or turn signed accounting discrepancies into observed illicit consumption.

Use existing NumPy/SciPy finite VOI and decision contracts;no new statistical backend.
Check independent scalar VOI arithmetic,known switching/tie cases,continuous-box
interior points,invalid inputs and reference-weight parity. Run affected integration,
full suite,strict checks,numerical reproduction,clean package and security under the
existing bounded macOS Python3.15.1 workflow. Preserve source and output hashes.

## Publication limits and outputs

Produce consequence,decision,group-information,study-value and frontier tables plus
figures and a findings report tied to actual output hashes. State where source/target
and structural assumptions drive results. No equity-weighted subgroup benefit can be
estimated without distributional data;Māori-specific effects are not reconstructed
from national aggregates. Equity constraints remain a research limitation,not a
fictitious completed analysis or consultation.

The ethics document is a desk assessment only. Institutional setting and journal
requirements are unknown;neither exemption,approval,consultation nor community
endorsement is asserted. No journal/ethics registration or submission,no requests,
restricted linkage,purchase or operational recommendation. Original issue#3 empirical
acceptance remains open. Manuscript submission and final author decisions are separate.


## Implementation amendment 1

After the first125-profile pilot,but before final execution,add a diagnostic of
expected information gain about net cessation,diversion and criminal harm for each
case/report design. Compute it once per case because the prior and report likelihoods
do not depend on normative weights. Report nats separately from decision value;no
monetary conversion. This diagnostic is an implementation amendment,not preregistered.
The inherited Table2 Beta input is also rechecked against a newly saved full PMC
original;it remains a transported model input,not an observed policy response.


## Implementation amendment 2

After the pilot,but before final execution,challenge all declared value profiles
with2,4(primary),8cessation quantile nodes. Hold all non-grid inputs fixed,verify
output hashes and compare complete unique decision/study tables. Report changed
co-optimal sets and maximum absolute EVPI/EVSI differences. This is a finite-grid
diagnostic,not a proof of continuous convergence or field validity. No primary
weights,cases,prior construction or outcome assumptions were selected by this check.


## Interpretation safeguards

The inherited case ID null_effect means zero additional cessation caused by the
retail restriction;diversion and support responses remain in the model. It is not
a claim that every policy consequence is zero. The0..4weight rectangle is an
illustrative stress support extending zero to four times the reference weight,
not elicited or empirically plausible population-preference bounds. Additive
weighting does not cover every ethical position,nonlinear objective,rights constraint
or hard budget. Positive gross EVSI is not an instruction to collect information.
Any study cost must be mapped to the same declared objective before comparison;
no division by a zero resource weight or conversion to NZD is performed.
Consequence summaries average state-specific illicit fractions separately from
volume averages;these are not national illicit-market shares.

The resolution diagnostic also compares co-optimal gross-EVSI design sets and grouped
EVPPI priorities,including ties. These are gross-information rankings before study
costs,not funding decisions. The coarse2-node pilot differed from4nodes at one
near-zero-value design comparison;this is reported rather than hidden.
