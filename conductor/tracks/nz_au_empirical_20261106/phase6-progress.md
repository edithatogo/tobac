# Reproducibility, refresh and integration — 7 November 2026

P6.1 is local source integration and software qualification. This phase is in progress;
whole-track, shared-main, native/hosted release and empirical acceptance are separate gates.
Existing scientific inputs/core numerical source/reference outputs and M3 are unchanged.

## Implemented source controls

- Added the opt-in clustering dependency profile through existing lock_receipt machinery;
  its reviewed hash lock includes the pinned Nox frontend for a portable bootstrap.
  The original four-profile snapshot remains unchanged; opt-in profiles are explicit.
- Added scikit-learn to reviewed audit tools and regenerated the audit lock/receipt. The
  graph adds joblib, narwhals, scikit-learn and threadpoolctl without removing packages.
  The owned native audit environment was checked inactive before those four
  hash-bound additions; it now has 97 compatible packages. No other environment was changed.
- Added Nox clustering and Snakemake analysis=synthetic_clustering. Both are explicitly
  synthetic-only. M1's native admission is retained. Renovate coverage includes the new
  profile/tool source and has no automerge or second updater.
- Added complete packet verification using existing canonical path/hash/JSON guards and
  source-bound lock verification. Unknown schemas, unsafe paths, symlinks, missing/extra/
  altered members and stale inputs reject. New v2 packet manifests version the unchanged
  v1 synthetic formula and bind orchestration/code/type inputs, environment and outputs.
- The qualifier stages output temporarily, verifies it, then publishes by rename. Unit
  failure injection proves no completed output appears and a corrected rerun can succeed;
  existing output preservation is retained. One writer per output is required.
- workflow/README.md supplies tracked context/profile and portable bootstrap instructions,
  replacing the old example's local-only Phase 0 profile. Earlier packets are retained as
  historical editions; no source/data watcher or automatic scientific refresh is installed.

## Executed evidence so far

Initial component selection exposed missing sibling-script imports under dynamic loading;
explicit checkout-relative imports fixed that route. The corrected selection passed 68
tests in 5.31 s at 211.6 MiB sampled process-group RSS. No test was skipped or weakened to
hide this failure. An initial lock CLI invocation used --out; help showed --path and the
corrected genuine resolver runs passed. Original failed logs remain local.

Normal Nox clustering execution passed 44 tests, generated a real synthetic packet and
reopened its full manifest; session completed in 38 seconds at 280.5 MiB. This predates the
portable profile's added Nox frontend; the subsequent fresh offline run is recorded below.
The optional profile's frontend additions do not alter existing scientific dependency pins.

Local logs/packets are under outputs/nz-au-phase6 and outputs/engineering. Candidate resolver
receipts distinguish input/byte consistency from installation and scientific acceptance.
The final refreshed profiles adopt Hypothesis 6.170.15, Ty 0.0.99 and Typer 0.28.0 after
a primary PyPI census of 143 unique packages (zero retrieval errors). Response originals
are losslessly saved outside this repository with SHA-256 readback; see the dependency
disposition ledger for eight remaining supported upstream constraints. Six affected locks
and source-bound receipts were regenerated through the resolver. Frozen earlier outputs
were not silently refreshed. Renovate remains the sole updater, with no automerge.

Refreshed Nox clustering passed 47 tests; installed Voiage qualification passed 99 tests;
Ty 0.0.99 and Pyrefly 1.4.1 advisory runs passed. The first strict run exposed three old
metadata-list annotation errors in audit_empirical_coverage.py. Adding explicit types
preserved behavior; the focused strict rerun passed nine Ruff-policy tests, all source
Ruff checks, formatting for 179 files and BasedPyright with zero errors or warnings
(862.6 MiB sampled peak). This supersedes Phase 5's missing-runtime typing warnings.

A fresh UV_OFFLINE=1 bootstrap from the final hash lock and separate Nox environment
passed 49 tests and reopened its generated packet (33 s; 286.8 MiB). Actual Snakemake
completed all three steps (2.48 s; 246.9 MiB). Its numeric summary and stability CSV were
byte-identical to the fresh offline run. A second scheduler run reported nothing to do;
a corrupted copy rejected before cache selection, preserving the original output. Missing,
altered, stale, unsafe and unknown packet members reject; failed staged publication cleans
up and permits a corrected rerun. Snakemake's empty regular timestamp marker is explicitly
permitted, while a nonempty marker or symlink rejects. These are synthetic software tests.

The final installed audit inspected 97 distributions with zero known vulnerabilities:
96 registry dependencies were audited and the unpublished editable project was explicitly
unavailable to PyPI auditing. This is dependency evidence, not a source-security certificate.
Logs and replay comparisons are in outputs/nz-au-phase6. Full-suite, clean-package,
publication-security and final integration outcomes are recorded at the terminal checkpoint.

The first complete suite executed: 1265 passed, 17 skipped, 21 failed (80.73 s;
728.4 MiB). Nineteen failures reject stale signed native requirements.lock identity;
one dependency-snapshot test correctly rejects uncommitted lock bytes. One genuine source
defect was the new context profile missing the mandatory coordination document; the same
test subsequently exposed that omission in the four earlier phase profiles. All five now
load AGENTS.md, the coordination document and track index within the 100000-byte budget. Read the named
phase task card separately; its instructions and commands remain tracked. This avoids
silently exceeding the budget as integration appends ownership history. Actual P6 bundle
creation passes. Snapshot acceptance is rechecked after the source commit.
No test/assertion was relaxed, and native failures remain open pending owner renewal.

## Integration/native boundary

Source checkpoint 0644b52 records the implementation. Read-only exact-range preflight
found clean source/target, no staged deletions or missing files, and no equivalent commit
on target. Immutable renewal 413f7b2 and documentation closeout 8b48e22 were consumed as
832c7e3 and 2733c50. Five documentation/inventory conflicts preserved both histories and
the union of exact allowed public paths. Signed payload/signature and native scripts were
consumed unchanged; no owner environment or private binding was copied. Earlier acceptance
records retain their original source/runtime epoch. Receiving hosted jobs were still
running at the last compact observation; no pending job is treated as successful.

The current profile changes signed requirements.lock and scripts/lock_receipt.py, so old
admission cannot qualify this extended head. After integration the affected selection ran
94 passes, five skips and 20 failures: nineteen stale native pin failures plus the older
context-profile omission corrected above. A mistyped initial test filename ran zero tests
and is not verification. Clean-package first rejected a missing explicit lineage interpreter;
with the required actual repo-local interpreter and attested route it rejected the stale
requirements.lock pin before building. Clean-package is therefore BLOCKED, not passed or
bypassed. Final native renewal remains with existing chat
01a19a6e-2e47-7b10-8a35-4e7d7fedb965. Signatures are never hash-only promoted.

The full-history/staged secret scan, exact publication boundary and Actionlint passed on
the initial source packet (231.5 MiB sampled peak). Final integrated security readback and
focused corrected-context results are recorded below. No push, shared main mutation,
GitHub settings change or current-head hosted qualification is claimed.

Terminal corrected-source selection: 147 tests pass (3.98 s; 207.4 MiB), including
committed dependency snapshots, harness/context contracts, clustering packet/recovery,
lock receipts and workstream integration. Integrated full source strict checks pass:
nine policy tests, Ruff, 179 formatted files and BasedPyright zero errors/warnings
(9 s; 896.7 MiB). The full suite's nineteen native failures remain unresolved;
empirical gates and clean-package remain open. Final context/publication checks follow
the terminal source/document checkpoint; no unchanged broad suite is repeated.

Integrated publication boundary, full-history/staged secret scans and Actionlint pass
(226.8 MiB sampled peak). Remaining disposition is the existing owner's current-head
native renewal, then clean-package/full acceptance and guarded receiving publication.
This lane's empirical/code changes are committed locally; no cross-chat message is sent
without the user's explicit authorization for that final packet.

Earlier empirical gaps remain: original rights/destinations, verified current observations,
policy baseline/causal effects, calibration/product-origin identification, HR-QoL/costs,
subgroup applicability and compatible Innovate. Synthetic reconstruction does not establish
Bronze/Silver dataset recovery or a complete NZ/AU model. Phase 6 stays open until applicable
full/native/hosted/publication gates pass, with exact receiving ref/file readback.
