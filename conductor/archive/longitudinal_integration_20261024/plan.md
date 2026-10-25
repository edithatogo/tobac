# Bounded integration plan and evidence

- [x] Read live main, source tree, evidence contract and issue #1 coordination comments.
- [x] Stage a sibling tobac_supply package; preserve regulatory code and results.
- [x] Rename import/source paths and adjust nested test roots; document LF normalization.
- [x] Run 151 imported tests and both full analyses; verify six sources per run.
- [x] Compare generated files with predecessor: 42/43 exact, remaining diagnostic within 2.45e-15.
- [x] Add data, methods, protocol, compact results and full-output CI workflow.
- [x] Verify remote source and test content-tree hashes against tested local files.
- [x] Publish implementation commit a71d803763638cd5ebed3e8ac17a45542a4a80fb to main with an expected-head check; re-read main to confirm.
- [x] Inspect hosted longitudinal run 40064143521: failure before runner assignment, zero executed steps; no hosted pass claimed.

Publication evidence: `integration/longitudinal_publication.json`; coordination is recorded
on issue #1. Scientific calibration, automatic regulatory conditioning, hosted execution
and third-party software qualification are not closed by source incorporation.

## Phase: Review Fixes
- [x] Task: Apply review suggestions `0589587` (deletion `431be04`); on current `main` the
  equivalent commit is `3ed3ea5` — the original pair is not reachable from `main` after a rebase.
  Component outputs were compared with predecessor output and reported byte-identical apart from
  the run-manifest self hash, and 151 supply_bridge and 499 full-suite tests were reported
  passing in a local run; the full-suite count has no receipt retained in this repository and is
  recorded here as a local claim, not a reproducible check.
