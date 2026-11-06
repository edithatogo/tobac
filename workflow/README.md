# Analytical foundation

Run from the repository root using the Phase 0 qualified candidate environment:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  .venv-analytics/bin/snakemake -s workflow/Snakefile --cores 1 --scheduler greedy \
  --config profile=outputs/nz-au-phase0/profile.json \
  bundle=outputs/nz-au-phase0/context out=outputs/nz-au-phase0/dag python=.venv/bin/python
```

The explicit user request selects Snakemake for analytical orchestration; Nox remains the
engineering runner. This reconciles the earlier Nox preference within this analytical scope.
The supported greedy scheduler is required by the qualified Apple Silicon candidate because
the installed default CBC solver is Intel-only. No solver binary workaround is applied.

Supply a reviewed context profile and a bundle from scripts/context_bundle.py. Existing
bundles are immutable inputs; failed verification requires correcting the source or generating
a new reviewed bundle. verified.json is context acceptance only. Logs and receipts are local
outputs; no source data is added to this code repository. The workflow currently has a single
admission stage; scientific stages must retain existing lineage_preflight.py and native input
verification rather than treating this receipt as their replacement.

## Scientific M1 target (pending renewed lineage acceptance)

Set `analysis=m1` to require an M1 manifest in the `all` target. Admission reopens the
existing attested source capsule before cache selection and again inside run_m1_stage.py.
The wrapper uses the unchanged M1 runner and verifier, deterministic process settings,
per-attempt logs and a temporary analysis directory. It publishes the completed directory
by rename only after all checks pass; existing outputs are never overwritten. Failed
attempt logs remain for diagnosis; partial staged directories are not accepted outputs.

Adding the wrapper changed the scientific operation inventory. The existing attested gate
currently rejects it with `Scientific inventory differs from native acceptance`. This is
an open integration requirement, not permission to rename the script to evade inventory,
edit capsule hashes, copy private bindings or claim a successful scientific DAG. Renew the
lineage contract through its owning lane before qualification. Context-only mode is separate.
