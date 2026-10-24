# tobac

NZ tobacco-regulation uncertainty and wastewater value-of-information research.

**Primary sequence:** regulatory EVPI → grouped EVPPI → targeted scientific learning → study EVSI → conditional ENBS. Testing, a different research programme, or no further study are all permissible conclusions.

## First milestone

The executable screening model asks which unknowns about current consumption, policy-induced switching, mitigation and additional criminal harms can change a regulatory choice, and which evidence can inform them. Four policy archetypes, 4,096 explicit finite hypotheses, nine prior/dependence scenarios, four normative weights and thirteen information designs are evaluated by exact enumeration.

**These are conditional research scenarios, not a fitted current NZ posterior, real regulatory impact estimates, or a funding recommendation.** Assumed support ranges and study performance remain visible. Monetary scales are hypothetical, not estimated NZ losses.

Read [the findings](results/milestone1/report.md), [the protocol](docs/protocol.md), [the next empirical milestone](docs/next_milestone.md), [task status](conductor/tracks.md), and [source applicability](evidence/source_review.json).

## Reproduce

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip install --no-deps .
python -m pytest -q
python scripts/verify.py
OPENBLAS_NUM_THREADS=1 python -m tobac.run --out outputs/my_run
python scripts/verify.py outputs/my_run
```

Use a new output directory. `--quick` keeps only the reference prior/weight; it does not change the finite state set. Full runs write eight CSV tables, validation and source/output hashes. The checked-in report and compact CSV projections are from the completed full local run; CI regenerates the complete tables as an artifact. The full local results are also supplied with the conversation delivery.

## Scope and provenance

Nine numerical/physical definitions are extracted without body changes from the verified v2.3.2 decision-programme archive; see [baseline provenance](integration/baseline.json). This is a focused standalone milestone, not a claim that the entire 51 MB predecessor archive, its Git history, or inaccessible parallel branches have been migrated. The original archive and optional health/fiscal consequence engines remain preserved. The former cessation-allocation example is secondary.

The primary implementation uses NumPy/SciPy. Genuine Sourceright CSL and voiage EVPI jobs are defined separately, with explicit execution receipts. Their existence is not a successful run, full scientific source verification, or qualification of third-party EVPPI/EVSI. See Actions and `integration/` for actual outcomes. CiteWeft remains outside this milestone's executed path.

## Scientific safeguards

Absolute illicit volume differs from illicit share. Chemical signals do not directly encode legality. Baseline observations do not establish causal policy effects or organised-crime harm. Health, criminal, resource and fiscal outputs remain separate; information gain in nats is not money. Zero diversion and zero additional criminal harm are included. Source identification is separate from numerical extraction and applicability. No ethnicity or individual criminality is inferred from sewage.

## Research status

Local numerical qualification: 29 tests passed and 974 full-run invariants passed. This does not establish external validity. Main remaining work is a real regulatory contrast, time-aligned evidence, qualified causal/mitigation priors, longitudinal field calibration and a reviewable incremental-harm model. See the open track before interpreting the illustrative ranking as an empirical research priority.
