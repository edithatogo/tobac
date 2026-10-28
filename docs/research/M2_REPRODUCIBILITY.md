# Publication reproduction and source-isolation protocol

Implementation amendment, 28 October 2026, before the first paper replay. The
initial readiness protocol planned extraction of a Git archive without .git. Code
review found that the existing primary runner requires an actual Git identity and
that an archive nested inside the parent checkout could discover the parent's Git
metadata. The implementation instead uses an independent local Git clone with
--no-checkout and --no-hardlinks, then detaches at the exact committed source SHA.
Its commit and complete tree must match the selected original. This changes source
isolation, not the numerical challenge design, supports, priors or consequences.
No remote repository fetch, submodule activation or source-document download occurs.

The clone contains committed files and history. It does not inherit ignored .nox,
outputs or current raw-source captures. Python imports must resolve inside the clone.
The explicitly selected repo-local Python3.15.1 dependency environment is reused;
this is neither an independent dependency installation nor an offline installation
test. It does not enforce operating-system network isolation. The declared numerical
commands contain no source-download step, and no inaccessible original is required
to execute the explicitly assumed model. Original-byte/WARC verification remains a
separate empirical-provenance activity and is not inferred from a clean replay.

The replay regenerates primary2/4/8-node tables/figures and all13 robustness
challenges. New manifests validate every regenerated input/output hash. Every saved
CSV table, row identity, numerical cell and scientific report field is compared;
only top-level checkout metadata is excluded. Absolute tolerance is1e-10 in declared
units; nonfinite values, changed booleans, added/deleted table inventories and
numeric-looking identifier changes fail. PNG/SVG bytes are hashed for the actual
new execution, without a claim of pixel identity across operating systems/fonts.

Run from a complete, committed checkout with qualified dependencies:

```
.nox/tests/bin/python scripts/run_bounded.py --timeout 2400 -- \
  .nox/tests/bin/python scripts/qualify_publication_replay.py \
  --out outputs/paper-replay-NEW
```

Nox reproduce includes this same paper replay after the existing M1/M2/M3,
longitudinal, primary and robustness replays. A nonempty output directory and dirty
tracked checkout are refused. Private untracked metadata is not copied or deleted.
The parent resource guard owns children and retains command logs. A resource breach
is a failed run; sampled peaks are not evidence that memory leaks are impossible.

The first replay at b47b6e5 passed all 24 primary and five robustness CSV tables
and every scientific report field, with zero numerical difference and a sampled
peak of 717.2 MiB. The compact receipt is retained in
[integration](../../integration/m2_readiness_20261028/initial-replay-receipt.json).
A later reviewed robustness run at e950c51 also passed (614.6 MiB); all five
CSV files and scientific report fields matched the initial snapshot exactly.
Final local and hosted qualification are recorded separately after execution.
No original-source request, external service, upload, deposit or submission.
