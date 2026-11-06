# P5.1 — Synthetic sensitivity and clustering qualification

R12–R13, R15–R18. Base 1596819, chat 01a1af53-2093-7f70-b761-e5f6cb7b769c,
codex/nz-au-empirical at /Users/doughnut/.codex/worktrees/tobac-nz-au-empirical/tobac.
Deliverable: an executable synthetic qualifier for sensitivity reference cases and
unsupervised discovery followed by supervised prediction of frozen cluster labels.
Empirical Phase 5 remains blocked by Phase 0–4; no posterior or country data are ingested.

Allowed: scripts/qualify_sensitivity_clustering.py, tests/engineering/test_clustering_qualification.py,
this track, engineering/context/nz-au-clustering.json, exact publication policy entries,
engineering/typings/sklearn/*.pyi and engineering/typings/threadpoolctl.pyi for the exact
NumPy API subset exercised here (not complete library certification),
append-only docs/WORKSTREAM_SYNC.md; isolated new .venv-clustering3152 and ignored
outputs/nz-au-phase5. Existing source, scientific inputs, locks, M3 and native bindings are
unchanged. No other checkout/environment or shared runtime promotion. No external writes.

Reuse SciPy sobol_indices and scikit-learn StandardScaler/KMeans/LogisticRegression,
silhouette/adjusted Rand metrics and DummyClassifier. Polars writes diagnostics. No manual
clustering/statistical engine or pandas/xarray. SALib 1.6.0 remains incompatible because
its published graph requires pandas. scikit-learn 1.9.1 has a cp315 macOS arm64 wheel and
a pandas-free graph; its isolated installation/qualification is not reference promotion.

Commands from root, heavy commands serial, logs under outputs/nz-au-phase5:

```sh
.venv/bin/python scripts/context_bundle.py --profile engineering/context/nz-au-clustering.json --out outputs/nz-au-phase5/context
uv venv --python .venv/bin/python .venv-clustering3152
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- uv pip compile engineering/requirements.lock conductor/tracks/nz_au_empirical_20261106/phase5-qualification.in --python .venv-clustering3152/bin/python --generate-hashes --output-file outputs/nz-au-phase5/qualification-v2.lock
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- uv pip sync --python .venv-clustering3152/bin/python --require-hashes outputs/nz-au-phase5/qualification-v2.lock
uv pip check --python .venv-clustering3152/bin/python
.venv-clustering3152/bin/python -c 'import sys; assert sys.version_info[:3] == (3,15,2)'
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv-clustering3152/bin/python scripts/qualify_sensitivity_clustering.py --out outputs/nz-au-phase5/qualified-v2 --lock outputs/nz-au-phase5/qualification-v2.lock
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv-clustering3152/bin/python -m pytest -q tests/engineering/test_clustering_qualification.py tests/m2/test_value_sensitivity.py tests/m3/test_research.py tests/test_workstream_integration.py tests/engineering/test_publication_boundary.py
git diff --check
```

Synthetic oracles: independent additive Sobol indices 0.2/0.8, absolute tolerance 0.01;
correlated linear PSA variance 7.4, relative tolerance 0.025 at 65,536 seeded draws.
Correlation 0.6 is a fixture, not estimated. Do not apply classical independent Sobol
indices to the correlated case. Three well-separated blobs are a numerical challenge:
training-only k selection/scaling, 12 training bootstrap stability fits, separate test RNG,
supervised labels frozen from discovery. Fixture acceptance: k=3, minimum bootstrap ARI
0.9, held-out balanced accuracy 0.95; these are not empirical cluster-use thresholds.
Also reject scoring when holdout omits training clusters; test no-use on unstructured
noise and preserve completed outputs. Report majority baseline/log loss and preserve the distinction between imitation of
cluster labels and independent substantive validation. Test overlap, nonfinite inputs,
degenerate features and held-out influence on training selection/scaling.

Native threads are limited to one, 4 GiB sampled group RSS / 40 minutes, zero blind retries.
Refuse output overwrite; manifest binds code/lock, actual versions, synthetic seeds and output
hashes. Stop on installation incompatibility, failed reference or leakage; no empirical gate
is bypassed. Results, limitations and remaining country/group validation go in phase5-progress.md.
