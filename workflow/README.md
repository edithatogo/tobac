# Analytical foundation

NZ/AU context profiles contain repository instructions, current coordination and the track
index. Before editing, follow the index to the selected phase task card, specification and
plan; these remain separate reads so the mandatory coordination history fits the bounded
context budget. Rebuild the bundle after source or ownership changes.

Run from the repository root using repo-local Python 3.15.2. Build a new context bundle
for the current HEAD/source state before invoking the retained analytics environment:

```sh
.venv/bin/python scripts/context_bundle.py \
  --profile engineering/context/nz-au-integration.json \
  --out outputs/analysis-context
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv-analytics3152/bin/snakemake -s workflow/Snakefile --cores 1 --scheduler greedy \
  --config profile=engineering/context/nz-au-integration.json \
  bundle=outputs/analysis-context out=outputs/context-dag python=.venv/bin/python
```

The explicit user request selects Snakemake for analytical orchestration; Nox remains the
engineering runner. This reconciles the earlier Nox preference within this analytical scope.
The supported greedy scheduler is required by the qualified Apple Silicon candidate because
the installed default CBC solver is Intel-only. No solver binary workaround is applied.

The current controller and analytics interpreters are repo-local Python 3.15.2. The analytics
environment is hash-synchronised from engineering/analytics.lock, separately from the core
runtime. Earlier 3.15.1 environments and receipts are historical, not active defaults.

Supply a reviewed context profile and a bundle from scripts/context_bundle.py. Existing
bundles are immutable inputs; failed verification requires correcting the source or generating
a new reviewed bundle. verified.json is context acceptance only. Logs and receipts are local
outputs; no source data is added to this code repository. The scientific target retains
separate attested input admission; the context receipt does not replace native input verification.

## Scientific M1 target

Set `analysis=m1` to require a completed M1 directory containing its manifest. Admission reopens the
existing attested source capsule before cache selection and again inside run_m1_stage.py.
The wrapper uses the unchanged M1 runner and verifier, deterministic process settings,
per-attempt logs and a temporary analysis directory. It publishes the completed directory
by rename only after all checks pass; existing outputs are never overwritten. Failed
attempt logs remain for diagnosis; partial staged directories are not accepted outputs.

The completed directory is a protected Snakemake directory output. Declaring the inner
manifest as a file output would cause Snakemake to precreate the destination and conflict
with atomic publication. A cached invocation verifies the existing source/output manifest
before scheduler selection; directory timestamps alone cannot detect corrupted members.
Use a new output root for a changed analysis. Protected results are not automatically
overwritten when inputs change. See the [Snakemake output rules](https://github.com/snakemake/snakemake/blob/main/docs/snakefiles/rules.rst).

The integrated 3.15.2 renewal includes the directory correction and passes attested input
admission. Real-scheduler fixture tests pass on 3.15.2; the complete scientific DAG still
requires its own terminal qualification receipt. Do not bypass signature checks, rename
scripts out of inventory or copy private bindings. Context-only qualification is separate.

The scheduler regression in tests/engineering/test_m1_stage.py uses a clearly labelled
fixture writer and the actual maintained M1 rule. It proves scheduling, cache and output
preservation behavior, not native or scientific acceptance. Supply the actual qualified
Snakemake executable through TOBAC_SNAKEMAKE; an environment without the optional analytics
tool reports that capability as skipped rather than substituting a fake scheduler.

## Synthetic sensitivity/clustering qualification

This target generates synthetic fixtures only. It accepts no empirical dataset argument,
does not grant native/empirical admission and cannot create NZ/AU population policy groups.
The original M1 attestation gates remain in place. Core/runtime promotion remains separate.

The opt-in source-bound engineering/clustering.lock includes the reviewed Nox frontend,
scientific reference/test/build stack and scikit-learn. For a fresh, unused environment:

```sh
uv venv --python .venv/bin/python .venv-clustering-bootstrap3152
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  uv pip sync --python .venv-clustering-bootstrap3152/bin/python \
  --require-hashes engineering/clustering.lock
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv-clustering-bootstrap3152/bin/python -m nox -s clustering \
  --force-python .venv/bin/python
```

Do not replace an environment in use. Verify actual Python 3.15.2 and pip consistency;
Nox also verifies the lock receipt and selected interpreter. Its output/log identifies the
actual session interpreter and unique completed packet under outputs/engineering.
After wheel/interpreter caches are populated, UV_OFFLINE=1 with a new Nox --envdir tests
fresh offline reconstruction; a cache miss is a failed check, not permission to fetch.

For Snakemake select analysis=synthetic_clustering and the actual qualified Nox-session
Python path from the preceding log. Keep the analytics controller on its separate lock:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv-analytics3152/bin/snakemake -s workflow/Snakefile --cores 1 --scheduler greedy \
  --config profile=engineering/context/nz-au-integration.json \
  bundle=outputs/analysis-context out=outputs/synthetic-dag \
  python=.nox/clustering-venv-bin-python/bin/python analysis=synthetic_clustering
```

With --force-python .venv/bin/python, the tested Nox session directory is
.nox/clustering-venv-bin-python; inspect the actual log if interpreter selection differs.
Use a new bundle/output root after source or HEAD changes. The protected directory output
is published by rename only after its complete packet verifies. Cache selection reopens
source, input, lock and output hashes even if mtimes are preserved. Missing/extra/corrupt
members, symlinks, unknown schema and stale inputs reject before cached success. Failed
temporary publication is removed while caller logs remain; reruns cannot overwrite a
completed directory. Retractions/source revisions require a new edition and selective
descendant invalidation; no automatic source-refresh watcher is installed.

The v2 packet manifest binds the unchanged v1 synthetic formula, code/orchestration/type
inputs, source-bound lock, installed package inventory and output hashes. Verify an existing
packet with scripts/verify_sensitivity_clustering.py --out PATH --lock engineering/clustering.lock.
The earlier Phase 5 raw candidate locks/receipts remain historical evidence, not the active
setup route. Do not upgrade frozen results in place or describe this packet as scientific
or policy acceptance.

## Issue #3: bounded empirical pipeline extension (not yet implemented)

The maintained [first-comparison audit](../conductor/tracks/nz_au_empirical_20261106/first-comparison-audit-20261109.json) reports 21 reviewed source/use records, 28 handoff rows with zero metadata-compatible observations and **no eligible three-role comparison**. The original Kim measurement pack is a verified source-native sensitivity calculation, **not** a matched independent outcome or a calibrated consumption series. The 2024 NZHS prevalence series has enough earlier descriptive survey editions for a possible source-only temporal check, but this cannot substitute for the prespecified country/product/catchment matched-consumption holdout.

Implement the next Snakemake target by **extending this existing workflow**, not replacing the Nox test runner or adding a second data-admission system. The design is an explicitly gated sequence:

1. **Source and contract verification:** bind the 6 November 2026 evidence cutoff, source originals/archive receipts, licence/rights, source/study aliases, units, complete time support and shared observation groups. Reuse `scripts/source_handoff.py`, `scripts/audit_first_comparison.py` and the existing Scope/EvidencePacket/SupplyBasis contract.
2. **Eligibility report:** produce a versioned, source-bound machine-readable result with required baseline, wastewater and independent-outcome roles; mark each as admitted, ineligible or unverified, with individual failed gates and source hashes. Exit successfully for a correctly documented **blocked research conclusion** while **never triggering fitting** or changing a probability input. Invalid manifests, stale source bytes or missing authority fail the workflow.
3. **Optional baseline/WBE fit:** only when all necessary roles are admitted, compare source-only and source-plus-WBE models with identical populations, products and horizons. Preserve censored values, stock/release constraints and shared-data identity; never import derived national estimates as independent outcomes.
4. **Prespecified external scoring:** preserve the frozen three-prior-complete-years and complete held-out year rule, and at least four comparable catchments for leave-catchment-out validation. Group observations sharing a sampling occasion. If unmet, output `validation_unavailable` rather than weakening thresholds.
5. **Decision analysis:** use the same feasible retail/cessation actions for no study, pilot and wider measurement, with explicit delays, genuine incremental costs and separate value perspectives. Do not turn log predictive scores, information in nats or assumed response effects into monetary ENBS.

Retain the established `--cores 1 --scheduler greedy`, hash-locked analysis controller, `outputs/` subdirectory, pre-cache source rechecks, atomic protected directory outputs and independent numerical oracle. Keep any added target opt-in until positive **and negative** fixtures demonstrate once-only conditioning, exact source readback, refusal on a stale/duplicate/mismatched source, censored-measurement handling and identical held-out folds. Its implementation will itself require a renewed signed native scientific inventory; this prose is **not** a claim that an empirical DAG has already run.
