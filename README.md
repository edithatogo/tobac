# tobac

NZ tobacco-regulation uncertainty and wastewater value-of-information research.

**Primary sequence:** regulatory EVPI -> grouped EVPPI -> targeted scientific learning -> study EVSI -> conditional ENBS. Testing, alternative research and no additional study are all permissible conclusions.

## Current milestone: M3 research methods

The six approved additions are implemented under [`src/tobac/research`](src/tobac/research/): exact weighted Voiage adaptation and structure-only information; complementary information portfolios and shared costs; unweighted prior/structure robustness; implementation-adjusted decisions; and pilot/continue/stop with matched timing. Uptake and delay materiality is tested before requiring Innovate or Kairos.

Read the [M3 findings](results/milestone3/report.md), [method contract](docs/research/M3_CONTRACT.md), [six-item status](integration/m3_requirement_status.csv) and [execution receipt](integration/m3_local_verification.json). **Actual installed Voiage qualification remains blocked.** Passing adapter mathematics is not a library execution receipt. Innovate and Kairos remain optional and unexecuted. All new cost/value calculations are conditional normalised units, not NZ procurement estimates.

```sh
nox -s research_m3
# Or use the already-qualified reference environment:
OPENBLAS_NUM_THREADS=1 python -m tobac.research.runner --out outputs/my_m3
python scripts/verify.py outputs/my_m3
# Restore all 24 saved full/refinement output files without re-estimation:
python scripts/unpack_m3_results.py --out outputs/saved_m3
python scripts/verify.py outputs/saved_m3/full
python scripts/verify.py outputs/saved_m3/refined
```

The full saved CSV/JSON tables and input/output manifests are losslessly packed in `results/milestone3/archive/`; the bounded unpacker verifies hashes and refuses overwrite. The new Actions workflow separates numerical reproduction from genuine released-Voiage execution. Workflow configuration is not hosted success. M3 preserves all parallel longitudinal, engineering and prior-evidence files through the current main base.

## Preserved milestone: M2a

M1's broad regulatory screening is preserved. M2a adds:

- a specified prospective smoked-tobacco retailer-cap contrast, with a published **net-cessation model input** kept separate from M1's gross displacement mechanism;
- null and attenuated transport, and explicit lawful replacement after illicit-supply disruption;
- matched causal total/lawful-consumption information, distinguished from baseline chemistry and unadjusted market releases;
- a strict observed-evidence interface with underlying data IDs, physical-state fingerprints, date/geography/population/unit scopes and dependence/transport checks;
- release accounting with signed stock change, lawful unrecorded supply, outbound flows and joint reporting error;
- exact incremental-information identities, invalid-input regression tests and source-effect quadrature checks.

Read [M2a findings](results/milestone2/report.md), [the policy contract](docs/m2_retail_contract.md), [the evidence interface](docs/evidence_interface.md), [source applicability](evidence/m2/source_review.json) and [task status](conductor/tracks.md).

**These milestones are not a fitted current NZ posterior, an observed regulatory effect, or a funding recommendation.** M2a's published prior component was itself constructed in another model, for a different retailer reduction. Costs, harm weights, source transport and study performance remain explicitly conditional. Synthetic conditioning fixtures are not NZ observations. No individual criminality or ethnicity is inferred from wastewater.

## Incorporated longitudinal component: M2b

The v2.8 reported-release and v2.9 historical survey/supply components now reside in
[`src/tobac_supply/`](src/tobac_supply/), alongside the unchanged regulatory package.
Read the [integration and reproduction guide](docs/empirical_longitudinal/INTEGRATION.md),
[historical methods](docs/empirical_longitudinal/METHODS_AND_ASSUMPTIONS_v2.9.0.md),
[compact results](results/longitudinal/) and [local verification receipt](integration/longitudinal_local_verification.json).

The import has 151 locally passing component tests and two completed full reruns. It fits
historical reported releases and observation-scale ratios, not a current illicit-market
posterior. Its forecasts and posterior paths are not automatically inserted into the
regulatory evidence interface. Shared underlying sources must condition existing evidence once.

```sh
OPENBLAS_NUM_THREADS=1 python scripts/run_release_calibration.py --out outputs/my_releases
python scripts/verify_release_calibration.py outputs/my_releases
OPENBLAS_NUM_THREADS=1 python scripts/run_empirical_longitudinal.py --out outputs/my_empirical
python scripts/verify_empirical_longitudinal.py outputs/my_empirical
```

The commands regenerate all tables, joint paths and eight captioned PNG/SVG figure pairs.
Compact result tables are checked in; larger generated artifacts are produced locally or by
the separate longitudinal Actions workflow. Hosted success is not assumed.

## Reproduce

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip install --no-deps .
python -m pytest -q
python scripts/verify.py
OPENBLAS_NUM_THREADS=1 python -m tobac.run --out outputs/my_m1
python scripts/verify.py outputs/my_m1
OPENBLAS_NUM_THREADS=1 python -m tobac.m2 --out outputs/my_m2 --grid-check
python scripts/verify.py outputs/my_m2
```

Use new output directories. M2a `--quick` selects one case/weight; `--quit-points` changes only one quadrature axis. Exact finite enumeration is not evidence of continuous convergence. Full outputs and source/output hashes are regenerated by both CLIs; checked-in M2a tables cover all five cases and three normative weights.

## Earlier screening and source migration

[M1 findings](results/milestone1/report.md), [protocol](docs/protocol.md) and [next empirical milestone](docs/next_milestone.md) remain available. M1 evaluates 4,096 hypotheses, nine prior/dependence scenarios, four normative weights and thirteen study designs. The earlier cessation-allocation example is secondary. Nine inherited numerical/physical definitions remain unchanged; see [baseline provenance](integration/baseline.json).

This focused repository is not a wholesale migration of the earlier project archives or their Git history. Historical archives and optional health/fiscal engines remain preserved separately. The bounded `tobac_supply` source integration is coordinated in issue #1 and documented above; no parallel regulatory code was replaced.

## Execution boundaries

The executed numerical stack is NumPy/SciPy. Genuine Sourceright and voiage jobs remain mandatory separate checks with explicit receipts. Their workflow definitions are not successful execution or scientific claim validation. CiteWeft is not executed. Read [M2a execution status](integration/m2_local_verification.json), [M3 execution status](integration/m3_local_verification.json), Actions and issue #4 before claiming hosted qualification. No workflow gate, private visibility or account setting was weakened to obtain a passing badge.

Absolute illicit volume differs from share. Baseline observations do not identify future policy response or additional organised-crime harm. Health, criminal, resource and fiscal outputs remain separate, and information gain in nats is not money. Independent source-applicability review, a matched current NZ evidence model, qualified causal effects and governance remain open.

## Incorporation audit and preserved prior work

The [incorporation index](docs/INCORPORATION_STATUS.md) distinguishes active models,
reference-only evidence, reproducible outputs, archive-only material and work awaiting qualification.
Nineteen selected earlier files are now preserved under [evidence/prior_work](evidence/prior_work/),
with exact archive/member hashes and checks for omission, mutation and source-ID linkage.
This includes measurement/calibration summaries, survey versions, planning cost/uncertainty
inputs, candidate actions/studies and request templates. They do not automatically enter the
current model and are not newly observed data or quoted prices.

```sh
python scripts/verify_prior_work.py
python -m pytest -q tests/incorporation/test_prior_work.py
```

For maintained-library choices, source-bound dependency locks and execution qualification,
use the [engineering readiness guide](docs/engineering/READINESS.md). The commands above
without reviewed transitive locks are development bootstrap, not release qualification.
M3 receiving-commit coordination and precise execution scope are recorded through issue #1.
