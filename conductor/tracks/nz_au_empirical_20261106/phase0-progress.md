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

## User-requested test-tool review

Isolated xdist 3.8.0 / pytest-cov 7.1.0 trial: 30 numerical tests passed with two workers,
6.17 s / 293.8 MiB. Same selection serial: 30 passed, 1.57 s / 106.7 MiB; selected module
executed/missing lines and branches match. No default adoption: slower on this selection.
pytest-newer exact PyPI identity unresolved (404); pytest-changed filename/no-match semantics
and pytest-mock wrapper appraised in test-tool-review.md. Existing coverage.py gate retained.
Added standard-library autospec mock only for a filesystem-error boundary. No mocked empirical
or native success receipts. Baseline dependency vulnerability audit passed: no known findings
for the 38-package target environment; analytics audit is still pending.

## Full numerical replay, security and expanded census

After interruption the original session handle was missing. Process inspection showed no
live replay. Every listed numerical runner and validator had finished; the orchestration
failed only at final comparator import (parent PYTHONPATH missing). Corrected comparison
first revealed its expected single-child replay-container layout. Moved this lane's local
replay outputs under replay-container/baseline, recorded original executed paths in the
command ledger, and compared existing outputs without rerunning calculations.

Terminal comparison passed all 8 variants / 82 CSV tables against accepted native-byte
references using existing family tolerances. Receipt full-numerical-reproduction.json
explicitly limits scope to direct software replay/listed validators, with identical-source
M1 reused; no Nox native-preflight, producer mutation or empirical acceptance is claimed.
The original interrupted outer guard has no terminal resource receipt; no full-run peak or
exit is invented. Final comparator had sampled peak 114.5 MiB, exit 0.

pip-audit 2.10.1 actual baseline and analytics site-package audits both returned no known
vulnerabilities, exit 0 (sampled peaks 107.0/93.0 MiB). This is dependency advisory evidence,
not a complete security assurance. Current all-profile PyPI census covers 146 locked package
identities with zero lookup errors and identifies stable/prerelease status of reported index
versions; packages outside locks/direct URL revisions remain separate.

Python.org release pages identify available 3.15.2, while actual qualified project runtime
remains 3.15.1 by current contract. Availability alone does not qualify patch promotion or
permit changing the other owner's environment. Sources:
https://www.python.org/downloads/release/python-3152/
https://www.python.org/downloads/release/python-3151/

## Latest baseline compatibility candidate

Generated an isolated dated candidate from the baseline's 38 installed package identities
using the all-profile index census. Eight changed versions: coverage 7.17.2, Hypothesis
6.170.14, pandas 3.1.1, PyArrow 26.0.1, Pydantic 2.14.3, pydantic-core 2.50.4,
python-dateutil 4.0.0 and typing-inspection 0.4.5. Resolution succeeded with hashes and
installed into .venv-latest-candidate; pip check passed 38 packages. Full suite is running
under the unchanged 4096 MiB/2400-second guard. No terminal test result claimed yet.

This candidate tests compatibility of the existing longitudinal implementation; pandas is
not accepted for the target Polars-only runtime. The existing environment and four reference
profiles are untouched. Raw inputs/lock/diff/hashes and logs remain in outputs/nz-au-phase0.
The candidate does not have a promoted canonical lock receipt; integration remains owned by
the reference/Polars lane. Do not conflate newest metadata, successful resolution, install,
full tests, scientific replay and final promotion.

Latest candidate full suite reached exit 0: 1232 passed, 20 skipped in 98.73 seconds;
sampled peak group RSS 654.9 MiB. New full eight-variant numerical replay started in
.venv-latest-candidate under unchanged resource limits. It reruns M1 as well as all other
variants, retains per-stage logs/commands, then compares all accepted reference tables.
Its process handle must be polled before further heavy execution; no replay success yet.

## Latest candidate numerical result

The existing latest-candidate replay reached terminal exit 0: all eight variants reran and
all 82 accepted CSV tables matched using existing tolerances. Sampled peak group RSS
640.6 MiB. Receipt is outputs/nz-au-phase0/latest-replay/full-numerical-reproduction.json;
per-stage commands/logs and actual latest candidate lock remain local. This establishes
software parity for those eight package updates, not reference/runtime promotion or native
lineage acceptance. Source main/Polars integration remains owned by its existing lane.

Runtime inventory now records 15 tracked CI workflows, 19 dependency/runtime declarations,
seven owned local environments and no tracked notebooks/container recipes. Exact path lists
are in outputs/nz-au-phase0/runtime-inventory.json; declaration matches are retained separately.
Security tool installer verified pinned archive hashes for native Gitleaks 8.30.1 and
Actionlint 1.7.12. Existing publication security gate started under the resource guard;
no terminal scanner success is claimed here until its process is read back.

Publication security process reached terminal exit 0: existing tree/outgoing boundary,
checksum-qualified scanner identities, full-history/staged secret scanning and Actions
syntax checks completed. Scanner output is retained locally in publication-security.log;
no secret matches are echoed to chat. This does not establish empirical/native acceptance.

## Native admission and scientific DAG stage

Actual default native M1 preflight failed exit 2 because TOBAC_LINEAGE_ATTEMPTS is absent
in this checkout. Inspected the maintained attested route and qualified runtime profiles;
read-only hosted_lineage.py -I -S --runner m1 passed before the new wrapper was introduced.
No native binding/cache or private journal was moved or rewritten.

Added run_m1_stage.py plus optional analysis=m1 DAG target: fixed attested preflight,
unchanged M1 runner and output verifier, per-attempt logs/terminal event, staging and atomic
directory publication. New output paths only; no arbitrary workload/config arguments.
The real DAG rejected before execution because the added run_* wrapper changes the pinned
scientific inventory. Reopened attested route confirms `Scientific inventory differs from
native acceptance`. Do not alter hashes or rename operations to evade this check. Owning
native-lineage scope must renew acceptance before the stage can execute successfully.

Targeted stage/context/workstream tests passed: 33 tests. Tests include preflight failure
preventing calculation/publication and rejecting existing/out-of-scope output paths. Native
success is not mocked as evidence. Static Ruff passed; strict typing result retained in
m1-stage-types.log. This change is unqualified for native runtime until inventory renewal.

## Latest audit candidate and handoff

Built an isolated latest audit candidate combining the 38-package latest baseline with
current-census direct audit-tool pins. Hash resolution/install passed; pip check passed
95 packages. Actual whole-source Ruff 0.17.4 passed; strict whole-source BasedPyright
1.40.2 reported 0 errors/warnings, sampled peak 809.6 MiB; zizmor 1.32.0 offline/pedantic
reported no findings. These are native macOS candidate checks, not Linux audit promotion.

Read-only integration preflight found the source packet overlaps only the shared dirty
coordination file, with differing bytes and no staged deletions. Prepared scoped handoff;
no integration or inter-chat message executed. Searchright exact source revision cloned
locally for CLI qualification; locked two-job Cargo build is running under the usual limits.
No search, screening, provider acceptance or publication is inferred from source checkout.

## Searchright local CLI qualification

Locked build of searchright-cli at af8c282f4c0e92a958027ca352e82f1cc7180c57 completed
with cargo/rustc 1.99.1 (above package MSRV 1.97.1), two compiler jobs, 1m11s build time,
sampled peak 764.5 MiB, guard exit 0. No shared toolchain override or producer mutation.
Actual binary reports searchright 0.1.0-alpha.1; --help, provider listing and maintained
example-plan validation execute successfully. Example returns no findings and readiness
for strategy design; it is a supplied demonstration, not the NZ/AU review protocol.
Default CLI lists five fixture-backed providers and does not establish live acquisition.
Source tree remains clean; binary/Cargo.lock/context-boundary hashes and outputs retained
in searchright-qualification.json. No systematic search, screening or provider acceptance
claim. Full Searchright upstream test/verification matrix was not executed for this CLI probe.

A fresh full tobac suite is running after adding the scientific stage and its two tests,
using the latest baseline candidate. Previous full-suite evidence precedes that code addition
and is not substituted for this run. Native inventory renewal still blocks the real M1 DAG.

## Fresh full suite and approved owner handoff

Post-M1-stage full suite reached terminal exit 1: 16 failed, 1218 passed, 20 skipped
in 51.60 s, sampled peak 662.1 MiB. All failures are hosted-lineage tests stopped by
Scientific inventory differs from native acceptance before intended downstream checks.
This supersedes any implication that the current operation inventory has a green full suite;
earlier baseline/candidate passes remain valid historical evidence at their recorded source.
Do not suppress tests or weaken the guard. Renewed native acceptance is a required gate.

User explicitly authorized sending the prepared handoff to owner chat
01a19a6e-2e47-7b10-8a35-4e7d7fedb965. First send was rejected because the chat was
archived; unarchived it solely to perform the approved delivery. Second send succeeded.
Message includes exact packet, Polars terminal-commit request, native inventory renewal,
16 failing tests, preserved bindings and coordination-file overlap. No external email,
GitHub mutation or recurring coordination created. Await event-driven owner evidence.
