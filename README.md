# tobac

[![Engineering qualification](https://github.com/edithatogo/tobac/actions/workflows/engineering.yml/badge.svg)](https://github.com/edithatogo/tobac/actions/workflows/engineering.yml)
[![Scientific reproduction](https://github.com/edithatogo/tobac/actions/workflows/scientific-reproduction.yml/badge.svg)](https://github.com/edithatogo/tobac/actions/workflows/scientific-reproduction.yml)
[![Publication and source security](https://github.com/edithatogo/tobac/actions/workflows/publication-security.yml/badge.svg)](https://github.com/edithatogo/tobac/actions/workflows/publication-security.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/edithatogo/tobac/badge)](https://scorecard.dev/viewer/?uri=github.com/edithatogo/tobac)

[How to cite](CITATION.cff) · [Apache-2.0 licence](LICENSE) · [Security reporting](SECURITY.md) · [Actions](https://github.com/edithatogo/tobac/actions)

NZ tobacco-regulation uncertainty and wastewater value-of-information research.

**Primary sequence:** regulatory EVPI -> grouped EVPPI -> targeted scientific learning -> study EVSI -> conditional ENBS. Testing, alternative research and no additional study are all permissible conclusions.

## Current status — 8 November 2026

Accepted main at `d735896` uses **Python 3.15.2**. The
[engineering run](https://github.com/edithatogo/tobac/actions/runs/42424926119)
passed 1,250 tests with 21 explicit skips and 92% measured coverage. Its 98.5%
mutation score covers `src/tobac/supply.py`, not the entire scientific model.
Historical receipts below retain their original runtime and scope.

The [dynamic/evidence roadmap](conductor/tracks/dynamic_frontier_20261108/index.md)
adds a **candidate** closed-cohort projection and a versioned
[public comparison-data pack](evidence/public_data_20261108/README.md).
These additions need fresh native scientific qualification. They do not establish
a current NZ posterior, fitted policy effects or an adaptive policy recommendation.
The companion track specifies systematic-review integration with Searchright,
causal/measurement evidence requirements, broader policy decisions and benchmarks.

## Implemented decision methods: M3

The six approved additions are implemented under [`src/tobac/research`](src/tobac/research/): exact weighted Voiage adaptation and structure-only information; complementary information portfolios and shared costs; unweighted prior/structure robustness; implementation-adjusted decisions; and pilot/continue/stop with matched timing. Uptake and delay materiality is tested before requiring Innovate or Kairos.

Read the [method contract](docs/research/M3_CONTRACT.md), [six-item status](integration/m3_requirement_status.csv) and [execution receipt](integration/m3_local_verification.json). The authoring report is local-only under the [publication boundary](docs/engineering/PUBLICATION_BOUNDARY.md). **Bounded published Voiage 3.1.0 qualification has historical Python 3.15.1 evidence** for equal/weighted EVPI and finite partitions; it does not establish generic EVSI or structural API certification. See the [published-wheel receipt](integration/voiage_published_20261106.json). The earlier [source-built compatibility receipt](integration/voiage_python315_compatibility_20261026.json) is historical. [Current Python 3.15.2 finite-library qualification](conductor/tracks/nz_au_empirical_20261106/phase4-progress.md) is separate. Innovate remains blocked by its pandas dependencies; Kairos remains optional and unexecuted. All new cost/value calculations are conditional normalised units, not NZ procurement estimates.

The [NZ/AU empirical and wastewater VOI track](conductor/tracks/nz_au_empirical_20261106/index.md) has evidence-feasibility results and synthetic software qualifiers; empirical admission and fitting remain open. Its runtime/workflow qualification does not establish a current NZ/AU empirical fit or a wastewater funding recommendation.

For fresh setup and the hash-locked Nox frontend, follow [Reproduce](#reproduce).
After the native owner supplies qualified lineage prerequisites, run the bounded M3 gate:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv-clustering-bootstrap3152/bin/python -m nox -s research_m3 --force-python .venv/bin/python
```

The saved M3 archive can be checked without re-estimation in a new directory:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv/bin/python scripts/unpack_m3_results.py --out outputs/saved_m3
.venv/bin/python scripts/verify.py outputs/saved_m3/full
.venv/bin/python scripts/verify.py outputs/saved_m3/refined
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

Read [the policy contract](docs/m2_retail_contract.md), [the evidence interface](docs/evidence_interface.md), [source applicability](evidence/m2/source_review.json) and [task status](conductor/tracks.md). The authoring report is local-only under the publication boundary above.

**These milestones are not a fitted current NZ posterior, an observed regulatory effect, or a funding recommendation.** M2a's published prior component was itself constructed in another model, for a different retailer reduction. Costs, harm weights, source transport and study performance remain explicitly conditional. Synthetic conditioning fixtures are not NZ observations. No individual criminality or ethnicity is inferred from wastewater.

## Incorporated longitudinal component: M2b

The v2.8 reported-release and v2.9 historical survey/supply components now reside in
[`src/tobac_supply/`](src/tobac_supply/), alongside the unchanged regulatory package.
Read the [integration and reproduction guide](docs/empirical_longitudinal/INTEGRATION.md),
[historical model configuration](configs/empirical_longitudinal_v2.9.0/model.json),
[compact results](results/longitudinal/) and [local verification receipt](integration/longitudinal_local_verification.json).

The import has 151 locally passing component tests and two completed full reruns. It fits
historical reported releases and observation-scale ratios, not a current illicit-market
posterior. Its forecasts and posterior paths are not automatically inserted into the
regulatory evidence interface. Shared underlying sources must condition existing evidence once.

After qualified native admission, the bounded Nox reproduction session below runs the
longitudinal variants together with the preserved reference analyses. Use their existing
source/output verifiers; do not interpret a historical receipt as current-head acceptance.

The commands regenerate all tables, joint paths and eight captioned PNG/SVG figure pairs.
Compact result tables are checked in; larger generated artifacts are produced locally or by
the separate longitudinal Actions workflow. Hosted success is not assumed.

## Reproduce

The source requires Python 3.15.2. These commands are for a fresh checkout and unused
environment path; preserve any existing environment owned by a running operation.
Use the qualified uv 0.13.7 frontend and verify the actual selected interpreter:

```sh
uv --version
uv venv --python 3.15.2 .venv
.venv/bin/python -c 'import sys; print(sys.executable, sys.version); assert sys.version_info[:3] == (3, 15, 2)'
.venv/bin/python scripts/lock_receipt.py verify --profile runtime --path engineering/requirements.lock
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  uv pip sync --python .venv/bin/python --require-hashes engineering/requirements.lock
uv pip check --python .venv/bin/python
```

Use the [analytical workflow guide](workflow/README.md) for the portable hash-locked
Nox frontend at `.venv-clustering-bootstrap3152`, offline reconstruction and the synthetic
Snakemake target. That synthetic route does not admit empirical evidence.

Scientific test/reproduction/package sessions additionally require the existing owner's
qualified lineage interpreter and native or signed portable admission. See
[native prerequisites](docs/engineering/READINESS.md#native-lineage-prerequisites-for-qualified-workloads).
Do not copy private bindings or bypass failed admission. Current local dependency/helper
changes require renewed admission; clean packaging is blocked until then.

With those prerequisites established, run:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv-clustering-bootstrap3152/bin/python -m nox -s tests reproduce --force-python .venv/bin/python
```

The existing reference, optional and canary profiles retain their distinct roles. The
[Phase 6 evidence](conductor/tracks/nz_au_empirical_20261106/phase6-progress.md) distinguishes
actual local software checks from blocked native/package/empirical and hosted acceptance.

Use new output directories. M2a `--quick` selects one case/weight; `--quit-points` changes only one quadrature axis. Exact finite enumeration is not evidence of continuous convergence. Full outputs and source/output hashes are regenerated by both CLIs; checked-in M2a tables cover all five cases and three normative weights.

## Earlier screening and source migration

The M1 authoring report and protocol are local-only under the [publication boundary](docs/engineering/PUBLICATION_BOUNDARY.md). The [next empirical milestone](docs/next_milestone.md) remains available. M1 evaluates 4,096 hypotheses, nine prior/dependence scenarios, four normative weights and thirteen study designs. The earlier cessation-allocation example is secondary. Nine inherited numerical/physical definitions remain unchanged; see [baseline provenance](integration/baseline.json).

This focused repository is not a wholesale migration of the earlier project archives or their Git history. Historical archives and optional health/fiscal engines remain preserved separately. The bounded `tobac_supply` source integration is documented above; issue #1 retains historical coordination context. No parallel regulatory code was replaced.

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
.venv/bin/python scripts/verify_prior_work.py
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv/bin/python -m pytest -q tests/incorporation/test_prior_work.py
```

For maintained-library choices, source-bound dependency locks and execution qualification,
use the [engineering readiness guide](docs/engineering/READINESS.md). Historical bootstrap examples in old receipts do not qualify a release.
[Contribution guidance](CONTRIBUTING.md) describes focused checks, ownership and safe reporting.
Issue #1 retains historical coordination; current ownership is in WORKSTREAM_SYNC and Conductor.

The macOS Python 3.15.1 engineering hardening scope is complete. Full-SHA Action
pins are retained; the rejected tag-based lock proposal is closed. Current scope,
verification and non-blocking follow-ups are recorded in the
[completion receipt](integration/engineering_macos_completion_20261026.json) and
[Conductor registry](conductor/tracks.md). Linux and Windows tests, packaging and scientific reproduction are qualified for their declared scopes; see [Conductor](conductor/status.md) for current results and remaining research limits.

Current [public source-map navigation](docs/engineering/SOURCE_MAP_NAVIGATION.md) preserves the original captured evidence editions.
