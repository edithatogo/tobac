# Phase 0 execution — 6 November 2026

Implementation began in the owned managed worktree on codex/nz-au-empirical, base adb3f81.
Previous goal turn: not applicable (first execution turn).

Verified actual isolated .venv interpreter: CPython 3.15.1, assertion passed. Created with
uv using the existing interpreter without replacing the other lane's environment.
Installed jsonschema 4.26.0 and its resolved dependencies for context tooling bootstrap;
this is not a qualified or locked analytical environment. Context tool initially failed
because jsonschema was absent, then --help passed after explicit bootstrap installation.

Read current Conductor core documents and Phase 0 plan. Local origin/main points to
b1ccfd549665a69f0412daf3ef39b5509861caa1; remote freshness not yet checked. Existing
worktrees include active Polars and qualification lanes. No source changes borrowed.

Active pandas/xarray references remain in pyproject.toml, noxfile.py and longitudinal
runner/verifier/consumer scripts. Conversion and environment promotion must consume the
existing owner's terminal evidence. Existing code cannot yet be claimed Polars-only.

Next: build full active dependency/version census and baseline capability inventory,
qualify analytical environment through the existing locks, then implement logged DAG
and negative/resume checks. Phase 0 remains incomplete. No native writes or publication.

The existing evidence context profile exceeded its 80 KB budget. Replaced it for this
execution with an explicitly narrowed local profile covering AGENTS, core workflow/product/
stack and this track's specification/plan, retaining the same budget. The narrowed profile was rejected because new track paths are not yet classified public. No context manifest was generated. Next action: qualify the publication inventory for these owned planning paths before rerunning; do not bypass the guard.

## Continuation — baseline qualification

Previous goal turn classified progress: isolated interpreter established and actual context
failures identified. Reviewed new track documents and registered their exact planning paths
in the existing public-path inventory; retained private-document rules. Narrow context now
succeeds (6 files, base adb3f8127355f210c1df959d629730873b381fc2, dirty checkout recorded).

Hash-locked engineering/requirements.lock installation passed under the bounded runner,
57.7 MiB sampled group RSS, exit 0. uv pip check passed for 38 packages. Full pytest run
started under the same 4096 MiB/2400-second guard, output baseline-tests.log; terminal
result must be read before any baseline test success claim or further heavyweight execution.

A dated PyPI census queried 42 package identities with zero request errors. Newer index
versions exist for coverage, hypothesis, pandas, pyarrow, pydantic/core, python-dateutil and
typing-inspection. Snakemake 9.27.1, Voiage 3.1.0 and Innovate 0.6.0 were indexed; author
identity and actual compatibility are not established by names or index metadata. Census
is local evidence, not a promoted lock. Existing owner still controls dependency promotion.

Full baseline pytest reached terminal exit 0: 1225 passed, 20 skipped, 86.76 seconds;
bounded sampled peak 704.7 MiB. Candidate analytics environment .venv-analytics uses
Python 3.15.1 and a separately generated hash lock for Snakemake 9.27.1, Polars 2.1.0,
PyArrow 26.0.1. Resolution succeeded (87.5 MiB sampled group peak); no pandas/xarray
entries in that lock. Installation and real workflow checks remain separate gates.

Analytics candidate hash-install passed (206.4 MiB sampled group peak, exit 0).
Actual interpreter assertion passed at 3.15.1; imports report Polars 2.1.0 and PyArrow
26.0.1; Snakemake --version reports 9.27.1. Runtime assertions confirm neither pandas
nor xarray is installed in this candidate. uv pip check passed for 55 packages.
This proves basic candidate installation/import/CLI compatibility only, not workflow,
recovery, scientific adapter or dependency-promotion acceptance.

## Logged analytical admission implementation

Previous turn classified progress: baseline tests and isolated analytics candidate installed.
Added workflow/Snakefile and scripts/verify_context_stage.py using existing context_bundle
verification. A receipt binds source-manifest/context hashes, commit and actual interpreter;
JSONL events record terminal stage status; stale success is removed before validation and
replacement is atomic. This is context admission, not empirical/native source admission.

Initial default Snakemake scheduling failed because bundled CBC is an Intel binary on this
Apple Silicon host (Bad CPU type). Supported --scheduler greedy avoids that solver and
executed the DAG. An initial interpreter path resolve followed the venv symlink into the
base installation, causing missing jsonschema; corrected to preserve the venv path.
Both failures are retained in local logs. Corrected DAG succeeded; unchanged second run
reported nothing to do. Interrupted-process recovery and scientific-stage replay remain open.

New failure/recovery and changed-fingerprint tests plus workstream integration: 28 passed.
Ruff 0.17.3 format/check passed for both new Python files. Candidate analytics environment
now also contains this diagnostic Ruff install beyond the prior analytics hash lock; no
claim of an exactly locked final analytics environment is made. Updated lock coverage remains
required. Default ILP scheduling is not qualified; use greedy for this bounded single-core DAG.

## Cache and admission hardening

Added unconditional context admission before Snakemake cache selection, so a cached output
cannot bypass verification after a source/HEAD change. Reuse existing public-path checks,
reject empty source inventories, protect input files from log-output overlap, and ignore
local .snakemake metadata. Focused tests now include these failure cases; lint passes.

Current GitHub Innovate pyproject declares pandas and pandasdmx, statsmodels and other
runtime dependencies. This conflicts with the requested pandas/xarray-free runtime and
requires an upstream qualified Polars-compatible release/port or an explicitly justified
integration boundary; no --no-deps bypass or local imitation is accepted. Its source also
records existing ruptures/ArviZ compatibility holds. Voiage main declares Polars/Arrow and
Python >=3.15.1,<3.16; source metadata is not installation/API proof. Searchright main
observed af8c282f4c0e92a958027ca352e82f1cc7180c57 (commit date 2026-11-04).

Terminal hardened-workflow qualification passed: normal DAG exit 0, unchanged resume exit 0,
cached corrupted context exit 1 as required, restored input recovery exit 0. Receipt in
outputs/nz-au-phase0/workflow-qualification.json; individual logs retained. Outer guard peak
141.3 MiB, exit 0. Focused/workstream suite now 30 passed (1.02 s), sampled peak 114.7 MiB.
These tests prove corrupted-input recovery, not interrupted native-operation recovery.

## Baseline and published library candidate

Full M1 baseline (not --quick) executed successfully under the bounded runner, sampled peak
106.8 MiB. Existing verify.py passed all nine core definitions and output manifest verification.
A separate reference-table comparison failed during import (src absent from PYTHONPATH),
before comparison. Corrected comparison remains pending; no output mismatch is asserted.

Downloaded published Voiage 3.1.0 cp315 abi3 macOS arm64 wheel using PyPI metadata, verified
SHA256 ca1a625ea2e0f6c63ffd306f19cb62c1c69242643164553d5ca633e94146eb5b, resolved
candidate hash lock, hash-installed into .venv-voiage-candidate; pip check passed 29 packages.
The existing qualify_voiage_consumer.py probe is running under 4096 MiB/2400 seconds.
Do not restart it or claim its API/native/parity/buffer results until terminal readback.

Terminal Voiage candidate qualification passed: 90 equal/weighted EVPI/partition numerical
comparisons, maximum absolute difference 2.842170943040401e-14; six NumPy/Polars/constructor
buffer-ownership cases passed. Native extension and installed wheel members verified by the
existing probe. Sampled peak 189.9 MiB, exit 0. Scope remains exact consumer surface, not EVSI,
release promotion or empirical acceptance. Corrected M1 reference comparison passed all eight
tables using the existing accepted native-byte reference and existing numerical tolerances.

## Managed analytics profile and interruption recovery

Added opt-in analytics profile to existing lock_receipt.py without changing PROFILES or
reference inputs. Canonical analytics.in pins Snakemake/Polars/Arrow/jsonschema/Ruff and
Renovate includes it. Generated universal hash candidate and source receipt via real uv;
reviewed no pandas/xarray entries, hash-synced .venv-analytics, pip check passed 56 packages.
Candidate engineering/analytics.lock + paired receipt verifies exact bytes/input (SHA256
a658fa75ffdddb5761d5e123e1d4f64d2f9b2bc02aa138f14e1e0e0950a542a4).
This isolated profile does not promote scientific reference versions or claim other platforms.

Lock-profile, context admission and workstream tests: 79 passed (1.56 s); Ruff passes.
The first test run found an obsolete ALL_PROFILES assertion (78 passed/1 failed); updated
expected opt-in membership while retaining the invariant that PROFILES has exactly four.

Labelled no-data scheduler fixture intentionally exceeded a two-second test timeout and
failed exit 124, 109.7 MiB sampled peak. After terminal readback, --rerun-incomplete completed
its checkpoint successfully (exit 0, 89.4 MiB). No native mutations or unrelated processes.
This is controlled fixture fault injection, not a scientific-operation budget retry or a
proof of native-store transaction recovery. Ordinary scientific limits remain unchanged.

## Post-implementation baseline and software packaging

Updated full suite terminal result: 1231 passed, 20 skipped, 47.75 seconds; sampled peak
649.5 MiB, exit 0. Strict BasedPyright 1.40.2 targeted both changed implementation modules
under existing strict configuration: initial missing dict type argument corrected; final
0 errors/0 warnings. Final annotation-only change does not change numerical behaviour.
Ruff check passed. Full tests do not prove native provenance or empirical adequacy.

uv build with actual repo-local Python 3.15.1, no sources and no build isolation produced
sdist/wheel successfully; sampled peak 61.5 MiB. Separate clean package environment is
being hash-synced from the unchanged reference lock before wheel install/import checks.
This is direct software package qualification; Nox native-lineage preflight remains a
separate gate requiring the owning native inputs and current inventory acceptance.

Clean wheel install/import reached terminal success. Hash-synced .venv-package, installed
only the built wheel with --no-deps, uv pip check passed 39 packages. Python -I imports
resolved tobac/tobac_supply under site-packages, not the source tree, with actual Python
3.15.1 asserted. No installed numerical replay or security/native acceptance inferred.
