# BF1 finite credal certificate amendment

Frozen 13 November 2026 before implementation or new BF1 results. Question: for
finite named states and fixed action payoffs, which explicitly declared linear
restrictions on state probabilities establish an action's weak dominance over a
comparator, and which candidate restrictions are inclusion-minimal for that proof?

This first deliverable concerns a finite probability simplex with linear upper
inequalities. It does not claim nonlinear parameter-set, continuous-state, empirical
coverage or universal causal identification. Reuse the existing `Belief`, scope,
ordered state IDs and `DecisionProblem` payoffs; no new observation or posterior
conditioning is performed. Each restriction states its own name and identical
ordered state IDs. A prior is a comparison point, not an automatic restriction.

Use installed SciPy/HiGHS for lower and upper optimisations. Retain rational,
independently checkable witnesses: for any nonpositive vector y and simplex p
with `A p <= b`, `c p >= b y + min_i(c_i - (A^T y)_i)`. Convert the supplied
finite binary64 coefficients and chosen dual vector to exact rational values
before evaluating this bound. A nonnegative exact bound certifies weak dominance;
a strictly positive one certifies strict dominance. A valid exact feasible
probability vector with negative advantage disproves dominance. A numerical
solver estimate, a near-zero tolerance or an empty support is not a proof.
Indeterminate cases remain indeterminate. Provide solver estimates separately
from the exact rational certificate and feasible witnesses.

Enumerate at most eight named candidate restrictions. Return a set only when it
has a valid feasible witness and its exact dual bound certifies weak dominance;
it is inclusion-minimal only when each one-restriction deletion has a valid
negative-advantage witness. Empty baseline support is incompatible, never a
vacuous certificate. If numerical solving cannot establish feasibility or a proof,
record the unknown status rather than assuming a result. Minimality is only
relative to the enumerated candidate restrictions, not all possible evidence.

Prespecified analytic checks cover no-restriction extrema and the existing finite
oracle, a strict and a tied boundary, one- and two-restriction certificates,
multiple distinct minimal subsets, contradictory supports, state-ID reordering,
no duplicate source/conditioning operation, and a near-zero negative case.
Retain exact rational certificate verification in tests independent of SciPy's
reported objective. Compare the configured prior's decision separately from the
set result. Do not claim that a synthetic test establishes empirical validity.
