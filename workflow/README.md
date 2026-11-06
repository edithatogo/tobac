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
