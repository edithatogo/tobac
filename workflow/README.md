# Analytical foundation

Run from the repository root using the Phase 0 qualified candidate environment:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv-analytics3152/bin/snakemake -s workflow/Snakefile --cores 1 --scheduler greedy \
  --config profile=outputs/nz-au-phase0/profile.json \
  bundle=outputs/nz-au-phase0/context out=outputs/nz-au-phase0/dag python=.venv/bin/python
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
