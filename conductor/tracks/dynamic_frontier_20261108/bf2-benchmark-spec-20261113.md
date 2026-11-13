# BF2 benchmark amendment: calibration versus sampling

Status: specification frozen before the pilot calculation below; no dynamic BF2
experiment, field calibration, clinical claim or study recommendation is complete.
Date: 13 November 2026. This amendment is a synthetic, bounded continuation of
[the BF2 question](design.md#executable-frontier-extension--9-november-2026).
It does not replace the unfinished BF1 primal-dual and minimal-identifying-
restriction work in [the plan](plan.md#f05--dynamic-decisions-and-frontier-research).
The existing scalar finite/box calculation is the available BF1 precedent; a
successful example must not be described as the full BF1 certificate programme.

## Question and estimands

When product mixtures and measurement calibration can drift, does a report-
responsive allocation of a two-study budget improve decisions compared with
fixed sampling, fixed calibration and a static staged information design?
Estimate expected and worst-regime decision regret, resource use, timing loss,
90% state-set coverage and held-out predictive scores under the declared
simulator. This is a known-truth numerical experiment, not a model fitted to
New Zealand or Australian measurements. Product, assay, response and cost values
below are synthetic and do not represent measured performance or welfare.

## States, time and information

There are three equal decision periods, `t = 0, 1, 2`, and two product-mixture
regimes, `x_t = 0` or `1`. The other binary latent state `h_t` represents a
calibration/measurement regime, not a second product. The four ordered states
are `(x,h) = (0,0), (0,1), (1,0), (1,1)`, initially equally likely. The two
binary mixture classes are a deliberately coarse two-product approximation;
they do not establish real product-specific excretion or policy effects.

For each subsequent period independently, `x` flips with probability `p_x`
and `h` with probability `p_h`. Their innovations are independent in this
first benchmark; sensitivity to dependence is a separate prespecified ablation.
The planning model uses `p_x = p_h = 0.10`. Choose and freeze the complete
policy using that model before evaluating the following true regimes:

| Evaluation regime | `p_x` | `p_h` | Role |
| --- | ---: | ---: | --- |
| matched | 0.10 | 0.10 | model-matched reference |
| stable | 0.00 | 0.00 | withheld low drift |
| mixture drift | 0.35 | 0.10 | withheld mixture change |
| calibration drift | 0.10 | 0.35 | withheld measurement change |
| both drift | 0.35 | 0.35 | withheld joint change |
| extreme | 0.50 | 0.50 | withheld adversarial boundary |

For each period, select the product-targeting decision using reports available
at the **start** of that period. An observation selected at `t = 0` or `1`
samples that period's state and is reported at the next period's start. Thus
`a_0` uses the prior only, `a_1` may use the first report, and `a_2` may use
the first and second reports. Study decisions at `t = 0, 1` use only the
history then available. `a_2` is the final action and no study begins at `t=2`.
Keep sample time, report-availability time and decision time as separate fields;
no forecast or posterior is admitted as another observation. The simulator's
true state and true drift regime are unavailable to policy code. An outcome
impossible under the declared policy model is an explicit failure, not a silent
posterior repair.

## Observations, values and resources

Two distinct prospective channels are available; acquire at most one per study
period and at most two in total. Each acquisition has synthetic cost 0.03 in the
same dimensionless units as total-horizon decision value. Cost is charged when
acquired, including for a censored result; no real monetary interpretation is
allowed. Both the hard cap and realised expected expenditure must be reported.

- Wastewater `W_t`: generate a positive signal with a lognormal distribution,
  log standard deviation 0.4 and median 0.8 when `x_t XOR h_t = 0`, otherwise
  2.5. All quantities and thresholds use one arbitrary signal unit. Record
  outcome `<1` as **left-censored**, `[1,2)` or `>=2`. Compute the first
  probability by integration over `[0,1)`, not by replacing a nondetect with
  zero, half the limit or a detection. The XOR calibration reversal is an
  intentionally strong identification challenge, not a physical assay claim.
- Calibration `C_t`: return a binary report matching `h_t` with probability
  0.9, otherwise the opposite. This abstracts a calibration/human-yield study;
  it is not an observation of product mixture or a human-participant dataset.

Reports are conditionally independent **only given the complete relevant
state trajectory** and are ordinarily dependent after those states are
marginalised. Give every acquired observation a unique study/data ID and retain
its state, product, unit, population, observation date and availability time.
Reject a duplicated ID or reused baseline; an explicit joint distribution is
required for any shared report error. Use the existing `tobac.evidence.Belief`
and staged portfolio identity contract in an implementation; do not invent a
parallel evidence abstraction.

There are two period actions, `a = 0` and `1`. The period score is `1/3` if
`a = x_t`, otherwise zero; total gross score lies in `[0,1]`. The net score is
gross score minus `0.03` per acquired study. Ties choose action 0, and equal
study values choose in the order no study, W, C; record ties. This is a synthetic
classification payoff, not a real health effect, disease transition or welfare
function. Actions do not change `x`, `h` or observation performance in this
first benchmark; hence this does not complete the separately planned
intervention-dependent observation-operator task.

## Comparators and evaluation

All policies use the same prior, report delays, payoff, study costs and two-unit
hard cap. Report both gross performance and net performance, plus the actual
expected units spent; a shared cap is not a claim of equal realised costs.

1. No study: choose each period from the propagated planning prior.
2. Fixed sampling: acquire W at both study times, regardless of reports.
3. Fixed calibration: acquire C at both study times, regardless of reports.
4. Static staged EVSI: evaluate W then C and C then W under the static-state
   assumption, using `tobac.research.staged.two_stage` with remaining fractions
   `2/3` and `1/3` and both costs 0.03. Select the better ordering once under
   the planning prior, then stop or continue according to its pilot report.
   Propagate that comparator's *static* belief for its actions. Use a valid
   joint report tensor or document independence given the complete state.
5. Dynamic adaptive: choose W, C or no study at each study time by finite
   horizon dynamic programming under the `0.10, 0.10` planning transitions,
   using only available reports; maximise expected net score. No access to the
   held-out regime is permitted. This permits stopping and switching channels.

Policies 2 and 3 use identical two-unit actual budgets. The staged and adaptive
policies may spend less; include an equal-spend sensitivity that prespecifies
any otherwise-unused acquisitions before evaluation, keeps the policy's earlier
choices unchanged and charges all acquisitions. Describe the information from
those additional reports separately, rather than crediting a no-study action
with an observation. Do not claim an adaptive advantage purely from spending less.

For each regime enumerate the joint latent-state paths and outcome paths, or
use an independently qualified calculation producing identical finite sums.
No random seed or Monte Carlo interval is needed for the primary finite design.
Freeze the regimes, planning policy and metric definitions before seeing results.
Also calculate a static (`p_x=p_h=0`) four-state special case as an interface
witness, which is not a dynamic benchmark result.

Report for every policy and regime:

- Gross regret relative to the clairvoyant same-period action, averaged over
  paths; report its maximum **across the six regime means**, not as the maximum
  over zero-probability or artificial paths. Also show each regime separately.
- Gross and net score, expected number and cost of studies, and each period's
  expected regret. For a delay diagnostic, replay the same acquired reports
  and their realised acquisition schedule with each report available immediately;
  recompute decisions with observation-time-correct beliefs and compare gross
  score with the original delayed clock. This paired diagnostic freezes the
  original acquisition decisions and can be negative under misspecification;
  it is not a causal estimate of operational delay costs.
- At `t=1,2`, coverage of a 90% posterior set for `x_t`, formed by adding states
  in descending posterior mass until the cumulative mass is at least 0.9; break
  exact ties by 0 then 1. Evaluate coverage against the simulator's latent
  state, not against the policy's posterior expectation. Report set size.
- Brier score for the predicted `x_t` and log score for an independent,
  evaluation-only wastewater report at `t=2`, generated under that regime and
  never supplied to the policy. Include its own data ID and probability floor
  policy: an assigned zero to a possible outcome gives infinite log loss and is
  reported as a failure, not silently clipped.

A preliminary usefulness signal requires at least 0.01 lower expected gross
regret on **one or more nondegenerate withheld regimes** than the fixed-sampling,
fixed-calibration or static-staged comparator with the best planning-model net
score, chosen once before evaluation (not a per-regime hindsight winner). It
also requires no worsening over 0.01 in any withheld-regime mean regret, coverage
at least 0.85 at both report times, and expected study use no greater than two.
At the extreme `p_x=0.50`, past observations cannot predict the next mixture
state; equal gross decision performance there is an expected negative control,
not a failed demand for impossible improvement. The 0.01 is one percentage point of the
synthetic full-horizon correct-classification score; 0.85 allows a prespecified
five-point deviation from nominal 90% coverage. These are deliberately explicit
engineering screening thresholds, not statistically or clinically established
minimal differences. If any condition fails, retain all results and continue to
prefer the simpler comparator for this declared question. Passing permits only a
candidate numerical-method conclusion; it is not empirical or scientific acceptance.

## Prespecified controls and implementation order

- Check outcome-column sums and every trajectory probability; compare lognormal
  bins against an independent normal-CDF calculation. The baseline censored bin
  must include all values below the limit. For lower-limit sensitivity use
  cutpoints 0.25, 1 and 2, retaining `<0.25` as censored, and evaluate all
  policies on that same observation structure.
- Check analytic posterior and action results for the four-state static witness;
  compare a separate scalar enumerator with `two_stage`. Check the matched-model
  posterior martingale and retain ties. Verify decision times, missing reports,
  duplicate data IDs, impossible reports and changed state ordering fail closed.
- At fixed marginals, add a separately evaluated shared-innovation model with
  `P(flip x, flip h) = min(p_x,p_h)`; maintain correct marginal flip rates and
  provide the full joint tensor. Compare it with the independence assumption.
  It is an ablation, not an empirical estimate of dependence.
- Evaluate calibration uninformative at accuracy 0.5, no product signal
  (`median = 0.8` for all states), and no-report/no-study cases. Retain null or
  negative findings. Use the same outcome horizon and costs for every comparison.
- First qualify the existing finite/box BF1 precedent and the static interface
  witness. Implement the dynamic simulator, policies, oracle and controls in a
  separate question-driven change after the remaining BF1 prerequisites and
  ownership are resolved. Do not modify M3-owned files or assume Kairos clock
  integration is already qualified. Run affected tests and the workstream
  integration suite on the qualified repo-local interpreter; conduct any full
  scientific reproduction only on a checkout with sufficient resources and retain
  actual logs. This document alone is not execution evidence.

The deliverable for a later experiment is a versioned configuration, code,
scalar-reference checks, per-policy/per-regime tables, held-out coverage and
score tables, exact computation logs and an honest account of any threshold
failures. Raw real-world data, empirical admission and external validation remain
outside this benchmark.
