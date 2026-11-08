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

## Owner response and forward ecosystem candidate

Compact owner snapshot confirms its turn is active: no terminal qualified Polars conversion,
verifier remains uncommitted and both longitudinal runners still use pandas. Capsule renewal
requires a frozen integrated source snapshot plus native readbacks/negative controls. No
source edits or bindings borrowed. This is an explicit unresolved dependency, not a live
process handle for the native renewal itself.

Resolved/hash-installed latest inherited ecosystem compatibility candidate, then removed
obsolete direct pandas/xarray pins for a separate Polars-only forward profile with the exact
published Voiage 3.1.0 wheel. Both local input/lock editions retained. The forward candidate
hash-sync removed pandas/xarray; consistency passed 58 packages. Actual Python 3.15.1 and
absence assertions passed; NumPy/SciPy/Polars/Arrow/JAX/Voiage imports and tiny CPU JIT returned
[2.0,5.0]. Tiny smoke is not GPU, full ML or scientific validation. Existing canonical
reference/legacy ecosystem locks are unchanged pending owning-lane integration. Exact installed
Voiage consumer qualification is running in this forward environment before any promotion.

Forward ecosystem Voiage consumer probe reached terminal success: 90 comparisons, max
absolute difference 2.842170943040401e-14, six buffer-ownership cases; sampled peak
261.4 MiB. No reference promotion. Owner returned a terminal incomplete-status report,
confirming no qualified conversion commit and the frozen-source prerequisite. Sent a
same-scope follow-up to execute the already-owned conversion to its requested terminal
handoff, not repeat inventory. Owner chat had archived again; unarchived for approved
delivery. No code ownership or private bindings transferred.

## Forward candidate component and advisory checks

Latest baseline advisory scan passed with no known vulnerabilities (exit 0, sampled peak
85.1 MiB); pandas/xarray-free forward ecosystem advisory scan also passed (58.3 MiB).
Executed core regulatory/information, tests/m2, tests/m3 and workstream integration in the
forward environment: 267 passed in 10.60 seconds, sampled peak 530.1 MiB, exit 0. This is
explicitly selected component compatibility, not full longitudinal/native acceptance or
full coverage. Updated stale library-disposition entries from running to their actual
terminal results. Current full-suite lineage failures remain open until owner renewal.

## Failure-path review and disk-pressure mitigation

Strengthened the existing-output unit test to create a real prior result under the allowed
output root and assert its bytes are preserved. Added explicitly fixture-only final-verifier
failure injection: staged fixture output is never published, temporary staging is cleaned,
and failure is logged. No native/model acceptance inferred from these mocks. Focused stage,
context and integration selection: 34 passed in 2.32 s, sampled peak 122.3 MiB. Ruff clean
after combining equivalent nested context managers; no production source changed.

Owner reported intermittent ENOSPC during conversion. Verified this lane had no processes
using four redundant environments, then removed only .venv-package, .venv-quality,
.venv-test-tools and .venv-voiage-candidate. Preserved every source, lock, original wheel,
receipt/log and all other lanes' native/private state. Moved the qualified Searchright
binary out of its compiler target, rechecked its stored SHA256 and --version, then removed
that rebuildable compiler target only. CLI now at outputs/nz-au-phase0/searchright-bin/searchright.
Cleanup manifest retains the removed-path list and preserved binary identity. Available
space rose from 1.9 to 2.8 GiB. Earlier install/qualification receipts for removed environments
are historical execution evidence, not assertions those environments still exist. Active
baseline/latest/analytics/audit/Polars-ecosystem environments retained. Sent this concrete
resource update under the existing approved handoff scope; no owner files were touched.

## Frozen Polars source integration

Inspected b5610c7fd3ca900aa1fcd87d2f290135490eb80e, parent adb3f81: committed source packet
with documented terminal 85-test qualification, 21-table parsed numerical parity (maximum
difference zero), and 16 byte-identical PNG/SVG figures. Read parity.json from the owner's
frozen local evidence; earlier float-spelling/boolean-case differences remain explicit.
Preflight showed no dirty overlap/staged deletions in this checkout; source had unrelated
uncommitted profile work outside the exact packet, which was not copied.

Cherry-picked immutable packet as 2493aa7. Only docs/WORKSTREAM_SYNC.md append conflict;
resolved by retaining both complete histories. All five runner/verifier/test blobs exactly
match b5610c7; no calculation module under src changed. In our Polars-only environment,
two runner test files plus workstream integration passed 77 tests, 12.10 s, sampled peak
487.2 MiB. No pandas/xarray imports remain in maintained src/scripts/tests by bounded scan.
Canonical dependency/profile routes and native lineage are still pending owner work.

Whole-source strict BasedPyright in the latest audit candidate now finds three
reportUnknownMemberType errors at empirical plot/fill_between and release plot calls;
zero warnings, sampled peak 845.6 MiB. Sent exact log/locations to source owner for a narrow
interface correction without global relaxation or numerical changes. This is an open gate,
not covered by earlier pre-conversion type-check success. No runtime promotion occurred.

## Corrected source and profile integration

Consumed exact owner commits 4178c34 and 5c23107 as efe1b4d and de1c887. Retained both
coordination histories and removed one inherited conflict marker without dropping content.
Generated locks were restored as complete immutable owner blobs, with their matching
inputs; they were not hand merged. Preserved this lane's opt-in analytics profile and
explicit 3.15.1 resolver selection. All six dependency receipts verify. The default
environment was still the earlier installed baseline at this checkpoint.

Lock-receipt, context/M1 stage and workstream tests passed 83/83 in 2.64 seconds, sampled
peak 123.3 MiB. Whole-source strict typing passed with zero errors/warnings, sampled peak
823.7 MiB, using the explicitly selected latest audit interpreter with its SciPy stubs.
Two preliminary type-check invocations used incomplete import/stub environments and failed;
their logs are retained as environment errors, not waived source diagnostics.

Sent the approved owner handoff with this exact combined snapshot and the latest candidate
pin differences. Signed scientific inventory renewal and shared runtime promotion retain
their existing owners. No native keys, journals or bindings were copied. Canonical pins
remain distinct from the newer locally qualified candidates until owner promotion.

Hash-synchronised this lane's inactive default .venv with the integrated runtime lock.
Actual Python 3.15.1 assertion, absence of pandas/xarray imports and uv pip check passed
(36 installed packages). Installer sampled peak 61.1 MiB. Integrated full suite then
completed with 1222 passed, 20 skipped and 16 failures in 55.60 seconds, sampled peak
910.1 MiB. Every failure is in test_hosted_lineage.py and rejects the stale signed
engineering/requirements.lock pin before the workload; inventory renewal is also still
required. No failure was suppressed and no signed reference was edited.

## Integrated numerical replay and final Voiage routes

All eight variants executed serially in the dataframe-free canonical runtime. The existing
reference comparator passed all 82 CSV tables with its unchanged identity/schema/tolerance
checks; sampled group peak 819.7 MiB, exit 0. Full M1 was recomputed rather than copied.
Report: outputs/nz-au-phase0/integrated-replay/full-numerical-reproduction.json. This is
direct software/reference parity, not renewed native or empirical acceptance.

After that run was terminal, clean read-only integration preflight found no dirty overlaps
or staged deletions for owner commit 6b98348. Integrated it as b118592: published-wheel Nox
routes and exact Voiage 3.1.0 JAX guard, retaining rejection of unknown/retired versions.
No numerical formula changed. Affected backend/ecosystem/workstream tests passed 42/42
in 1.67 seconds, sampled peak 118.2 MiB. An initial invocation named a nonexistent workflow
test file and collected no tests (exit 4); the corrected exact existing selection above
provides the evidence. Owner's qualified Nox receipts remain separate and are reused.

Sent b118592 as the combined source/Nox freeze for retained native readback and signing.
No source, lock or Nox edits are planned while issuance runs. Dependency promotion timing
was explicitly requested before issuance; owner/integrator retains that scope. Track-only
evidence updates do not change the frozen scientific source.

The existing clean-package qualifier passed directly on b118592 (133.5 MiB sampled peak).
It built wheel/sdist, rebuilt the wheel from the sdist with equal member contents, checked
Apache-2.0 metadata/notice and dependency-marker contracts, hash-installed into fresh external
Unicode/space paths, verified site-packages imports and finite-oracle/interchange APIs, and
ran the installed quick M1 CLI for both wheels. Both external environments were automatically
removed at terminal exit. Scope is software packaging and quick CLI, not the lineage-gated
Nox clean_package session or full-platform scientific acceptance. Receipt retained under
outputs/nz-au-phase0/integrated-clean-package/receipt.json. Whole maintained-source Ruff
check with the latest qualified 0.17.4 passed (8.8 MiB sampled peak).

The interrupted publication-security process reached terminal success (exit 0, sampled
peak 182.5 MiB). Its log was recovered rather than starting a duplicate scan. It exercised
the maintained public-path/history, pinned Gitleaks and Actionlint checks. The native owner
has an actual active renewal operation on the combined source; this lane has not written
its native objects or copied its credentials. Installed a fresh canonical audit environment
from the integrated hash lock to verify final source typing without the historical latest
audit candidate's former pandas packages. Installation passed at 131.4 MiB sampled peak.

Fresh integrated audit profile: actual Python 3.15.1, 93 compatible packages, no importable
pandas/xarray. Final strict whole-source BasedPyright passed with zero errors/warnings,
733.3 MiB sampled peak. No global type-check relaxation or scientific source change was
used. Current final full-suite, latest-promotion and signed-native gates remain open.

## Held-dependency reconciliation and latest analytics candidate

Reconciled all six integrated locks against the dated 146-package index census. Nineteen
remaining differences have individual primary-source/disposition entries in
library-disposition.md; raw comparison is integrated-held-dependencies.json. Read installed
Snakemake/interface/SQLModel Requires-Dist bounds rather than inferring compatibility from
version numbers. Forced interface-common 1.24.0 resolution failed because its packaging>=26.1
conflicts with Snakemake's packaging<26 (exit 1, 4.6 MiB sampled peak). No bound was relaxed.

Fresh universal Python 3.15.1 analytics resolution changed only Ruff 0.17.3 to 0.17.4.
Hash installation and dependency consistency passed in .venv-analytics-latest (56 packages,
94.5 MiB sampled install peak), with no pandas/xarray. Actual CLI package versions are
Snakemake 9.27.1, Ruff 0.17.4, Polars 2.1.0 and Arrow 26.0.1. The real context DAG passed
on clean a334aa2 (90.0 MiB sampled peak). Its first invocation rejected a stale bundle after
this lane committed the ledger while the run was starting; retained that failure and rebuilt
context at the new HEAD before the successful run. No source guard was weakened. This
candidate is not promoted while the native owner is issuing against the frozen source.

Read-only remote/main reconciliation observed 58a4b2f602f4678ac5be3b59bd8e6b807ff9ae6d.
It is an ancestor of the owner's combined renewal branch, which preserves newer main
workflow pins. Those exact pins and the terminal capsule must be consumed together; do
not overwrite them with this lane's older workflow files. Recheck at final integration.

## Renewal compatibility finding

Bounded public read of the owner's in-progress renewal found that the newly active hosted
checkpoint hash differs from the original numerical-reference archive's checkpoint, while
the comparator imports the active checkpoint identity and requires equality. Reported the
specific mismatch to the native owner before integration. Requested preservation of the
original finite oracle, explicit separation/mapping of checkpoint roles, retained closure
checks and targeted rejection controls. No dirty source or private binding was copied and
no signed reference was edited in this lane. The owner is still qualifying its packet.
Added the final task-card execution order, including source freeze/context/terminal-log/
commit sequencing, so the observed stale-context error is not repeated by the next agent.

## Companion hardening H0 inventory

Completed the companion's H0 baseline inventory while the native owner finished its packet.
CommonMark parsing covered 180 tracked Markdown files, 490 links and 350 local targets.
All 21 missing targets are catalogued local-only authoring documents; none was restored.
Corrected five README destinations/labels and its obsolete active Voiage wording using the
qualified published-wheel receipt, retaining historical qualification and scientific limits.
Subsequent inventory has 16 remaining historical/technical references, with none in README.
External HTTP, anchors, HTML and rendering are explicitly untested. Baseline and subsequent
inventories are distinct retained artifacts.

Live GitHub metadata matched public visibility, Apache-2.0 and research description/topics;
no native setting changed. Structural inventory of 15 workflows found no unpinned remote
action; four named jobs carry feature-specific write scopes. Newer main pins remain in the
owner's pending packet. Reused package/security/resource receipts at their actual scopes.
Recorded severity, ownership, allowed files, focused commands and H1/H2 follow-ups in the
hardening index; marked only H0 complete. Staged publication-boundary validation passed
(56.2 MiB sampled peak). No source, lock, signed object or workflow was changed here.

## Integrated renewal and real-DAG defect

Merged the owner's immutable b3f3130 packet as cd147ba after preflight: clean target, no
overlap/staged deletions; dirty owner Conductor edits were not copied. All 33 signed pin
blobs match that packet. Attested admission verifies all eight runner closures; the original
numerical archive remains byte-identical (SHA256 083fa07f838499b73f05f76205c7bf35b9f1263874da06cb565335ca2eaee5f9).
This lane's renewed full suite passed 1245 tests, with 20 capability skips, in 49.13 seconds
(744.2 MiB sampled peak). Owner native bindings separately passed 1258 / 7 skipped.

The real M1 Snakemake invocation then failed before scientific execution: a file output
at m1/manifest.json made Snakemake precreate m1, which the atomic stage correctly rejects.
Direct stage success and unit tests had not covered that scheduler boundary. Preserved the
failure logs and the stage's existing-output guard. Changed the DAG to a protected directory
output, validates output containment and reopens existing source/output manifests before
cache selection. No calculation, source data or numerical tolerance changed.

The actual maintained rule was executed with real Snakemake 9.27.1 and an explicitly labelled
fixture writer: fresh destination success, cache no-op, protected rerun refusal with previous
bytes retained. A separate actual-workflow invocation rejects an outside destination before
reading inputs. These fixture checks do not bypass or qualify native admission. Explicit
TOBAC_SNAKEMAKE plus stage/context/workstream tests: 36 passed, 5.96 seconds, 207.2 MiB sampled
peak. Ruff/format pass. Tests require the real optional analytics capability, with a reasoned
skip when it is absent. Current signed DAG identity is now stale until owner renewal.

Asked the retained dependency/native owner to qualify remaining compatible latest profile
pins before the next combined freeze/signature, preserving Python 3.15.1, original oracles,
upstream constraints and global hooks. This closes the outstanding newest-qualified runtime
requirement in the correct sequence. Actual M1 DAG, final full suite and latest promotion
remain open; no current Phase 0 completion claim is made.

Receiving main has since advanced to eca4e8a (Python 3.15.2). The retained owner is qualifying
that integrated native runtime; it is now the receiving baseline to reconcile before final
acceptance. The scheduler correction above was tested on the earlier qualified 3.15.1
snapshot and must be exercised on the qualified receiving patch after integration. Preserved
the isolated Ruff 0.17.4 analytics candidate/receipt, but did not adopt its 3.15.1 resolver
artifact into a moving runtime baseline. Final profile resolution and signing must use the
combined source and newest qualified patch, with prior execution receipts kept historical.

## Current 3.15.2 runtime and scheduler qualification

Integrated receiving runtime d0e9fdd as c14cf1b, then immutable signature packet 0008b43 as
ae6d5fb. The latter includes the protected-directory correction. Its progress-file merge
proposed deleting 98 lines of owned historical receipts and no new text; preserved this
lane's complete history after exact stage comparison. No dirty owner files were copied.

Created and hash-installed repo-local .venv3152, verified actual Python 3.15.2 and dependency
consistency, then confirmed no live process referenced this lane's old default environment.
Moved that inactive environment to outputs/nz-au-phase0/retired-env3151 and recreated the
default .venv on the verified 3.15.2 interpreter. Its 36-package hash install, consistency
and no-pandas/xarray assertions pass. The relocated environment is historical and not an
active runner; previous execution receipts remain valid at their recorded scope.

Regenerated the owned analytics profile through maintained lock_receipt.py on 3.15.2.
Only Ruff changes (0.17.3 to 0.17.4); all upstream-constrained transitive versions are retained.
Adopted complete generated lock/receipt, not a hand merge. Fresh .venv-analytics3152 hash
installation passes (56 compatible packages; 212.5 MiB sampled peak), actual Snakemake 9.27.1,
Ruff 0.17.4, Polars 2.1.0 and Arrow 26.0.1, with no pandas/xarray. All six lock receipts verify.

Explicit real 3.15.2 scheduler plus affected stage/context/workstream tests passed 36/36 in
19.10 seconds (261.3 MiB sampled peak). New attested admission passes all eight runner
closures and 140 expected outputs. It remains an attested/current-input check, not direct
native byte readback in this lane. Active specification, plan, execution contract and
workflow guidance now select the qualified 3.15.2 patch; earlier receipts remain historical.
Real scientific DAG, remaining compatible dependency promotions and final checkpoint are open.

## Latest compatible profile candidate — frozen acceptance preparation

Real M1 DAG at b027688 passed on 3.15.2 (218.3 MiB sampled peak), post-publish verification
and cached no-op passed, and an isolated corrupted copy was rejected before calculation.
Original protected bytes and its single stage event remain unchanged. The immutable
m1-dag3152-qualification.json records environments, locks, workflow, context and log hashes.
The current baseline suite passed 1251 / 20 skipped (58.12 s; 927.2 MiB sampled peak).

Prepared an isolated 13-input graph for the eleven compatible held dependency updates.
The first resolver rejected a missed duplicate Hypothesis pin; corrected both declarations,
retained v1 failure/manifest and generated all five v2 profiles through lock_receipt.py.
Review found only intended version changes, with no additions/removals or pandas/xarray.
Latest ecosystem hash install/consistency passed (57 installed packages); full compatibility
suite passed 1256 / 15 skipped (99.13 s; 1005.0 MiB peak). JAX/interchange passed (337.0 MiB).
The registry install initially lacked wheel-origin metadata; the maintained Voiage probe
rejected it. Explicit hash-bound original-wheel installation preserved dependency validation;
198 wheel members, 90 comparisons and six ownership cases then passed (228.9 MiB peak).

Latest audit installation/consistency passed (93 packages), strict whole-source typing had
zero errors/warnings (858.6 MiB), and whole-source Ruff/format plus offline pedantic Zizmor
passed. Installed ecosystem/audit advisory scans covered 57/93 packages without skipped
coverage or known vulnerabilities (126.5 MiB peak). These are advisory-database scopes.

All eight latest-candidate computations and 82 tables reached persisted comparison success.
The final original resource-guard summary was lost on interruption, so no replay peak is
claimed. Rechecked all saved tables using the maintained comparator under a fresh guard
(107.8 MiB, exit 0). Original reference archive/checkpoint roles and tolerances are unchanged.

Adopted seven matching candidate inputs and five complete generated lock/receipt pairs into
this isolated branch; all six receipts verify. Updated only the exact admitted Ty/Pyrefly
version tuple. Their actual eleven fixture/crash cases and full diagnostic reports completed
(309.6 MiB); diagnostic exits remain visible and are not zero-error claims. Default .venv
was hash-synced from the latest runtime lock using a different controller environment.
Clean wheel/sdist-rebuild, external install/API and installed quick CLI passed (164.7 MiB).
Focused adopted-input tests passed 111, with one expected committed-snapshot rejection
because the reviewed lock bytes were not yet committed. Freeze, then rerun that exact node.

Removed only eight confirmed inactive, owned reproducible environments after disk pressure;
retained all inputs, wheels, source, results, receipts and other owners' native bindings.
Cleanup manifest records each path/process check; free space remains an external live state.
Latest native admission, coherent final suite and final staged security remain open.

## Frozen latest packet and receiving-main readback

Latest profile candidate is committed as 4015cc3 after staged boundary validation passed
(54.0 MiB sampled peak). The exact committed-snapshot failure-only rerun executed and
passed one test (0.22 s; 55.4 MiB). New lock admission correctly rejects the stale signed
engineering/requirements.lock (exit 2), preserving the existing guard. Sent one terminal
qualified dependency handoff to the retained native/integration owner; latest native
readback/signature and final coherent local acceptance remain required.

Integrated verified receiving 3021e55 as 1ed5c9d after clean source/target preflight. This
retains PR139's exact context bytes across Windows newline conventions and associated
signed provenance. It does not change numerical source or the latest dependency inputs.
Affected context/stage/snapshot/workstream tests passed 37/37 (6.60 s; 213.6 MiB). No old
qualification is relabelled as hosted success for the newer dependency packet.

Final local publication/security check on the frozen latest packet and receiving-main merge
passed at exit 0 (224.9 MiB sampled peak), including the staged document handoff. Ordinary
hooks and source publication boundaries remain intact. The retained native owner is still
finishing receiving-main CI; its latest reported macOS test job is queued. That older
hosted qualification is separate from latest-lock native admission for 4015cc3. No queued
job or pending signature is recorded as complete.

## Conductor publication and latest dependency admission — 6 November 2026

The requested Conductor publication is complete: expected main 93b019e advanced
by normal fast-forward to 2e6534d; exact receiving tree readback matched. All twelve
PR workflows and ten receiving workflows succeeded. The failed local ps monitor
sample remains in its log; one diagnosed retry passed with unchanged hook/limits.

Frozen b027688/4015cc3 are now integrated locally as eb8c8a5/6b1822a, with
six valid lock receipts and a fresh hash-installed native Python 3.15.2 environment.
Eight new native executions, independent byte/source readback and a fresh signed
capsule qualify 140 outputs; all 82 scientific CSVs equal the original accepted
bytes. Old admission correctly rejected the changed material. Native and attested
commands, atomic M1 stage, input/output/signature/runtime rejection controls and
post-negative native reopening pass. The integrated suite passes 1262 tests / 9
skips, sampled peak 988.5 MiB; focused changed-source lint passes. Existing latest
library, audit, typing and clean-package receipts were reused rather than rerun.

Receipt: integration/archive/dependency-admission_20261106.json. The accepted
original checkpoint/archive and prior attempts are preserved. This establishes
software/native lineage acceptance, not empirical calibration or outside scientific
endorsement. The dependency integration is local; its hosted checks/publication
and originating-lane real-scheduler handoff remain separate from the verified
Conductor receiving commit. No new empirical inputs or scientific scope were added.


## Integrated Phase 0 checkpoint — 7 November 2026

Phase 0 is complete locally for the frozen 0c4fbc8 packet integrated at 9cccc96.
Fresh native acceptance is committed at 41b6e11; qualified production source is
e88befc. Receipt: integration/archive/empirical-phase0-checkpoint_20261107.json.
All seven source-bound lock receipts verify on actual repo-local Python 3.15.2.
Eight fresh profiles reopen 140 outputs and original-source links; all 82 scientific
CSVs are byte-identical to accepted originals. Normal native and attested commands
pass after negative testing; prior attempts, source objects and the numerical oracle
are preserved. Real M1 and synthetic Snakemake execution, cache/no-op and corrupt-copy
rejection pass, preserving completed outputs. M1's eight CSVs also equal native bytes.

The final Nox tests session passes 1286 tests / 8 capability skips, with 92% full-source
coverage and 1089.0 MiB sampled peak. Clean wheel/sdist rebuild, isolated installs/API
and Unicode-path M1 CLI pass; clustering's 49 tests and packet verification pass.
Unchanged source-owner strict typing/static, offline reconstruction, Voiage/advisory
and installed-audit receipts are reused at their actual scope. The audit covers 96
registry dependencies; the unpublished editable project is explicitly unavailable to
PyPI auditing. This is not a first-party security or empirical validity certificate.
Final tree/outgoing-history publication checks, full-history/staged secret scanning
and Actionlint pass (245.2 MiB sampled peak); focused changed-file lint/format pass.

Two integration corrections retain their failed evidence. H1 navigation edits touched
capture-pinned README/index bytes; frozen editions are now restored exactly, with
current navigation maintained separately in docs/engineering/SOURCE_MAP_NAVIGATION.md.
The first complete suite exposed a fixture that accidentally extracted the optional
clustering rule along with M1. The fixture now isolates the maintained M1 rule;
all protection assertions remain. Its exact failed-node rerun and final complete Nox
tests pass. No signature, source receipt, oracle or tolerance was bypassed.

Closed coordination history is preserved byte-for-byte (94019 bytes, SHA256
78ee67f6d3d147aafb7c8e5d084fb17dece2849c00376bfb0dcf7ea8b23a7a2d) under
docs/coordination/WORKSTREAM_SYNC_through_20261107.md. Current context stays compact.
The root integrator will fast-forward the idle clean empirical checkout to the final
public checkpoint and read back attested admission, retaining its private environment
and bindings. Native original-byte verification remains with the root owner.

Phase 1–6 empirical acceptance, the changed packet's hosted/guarded publication and
receiving checks, and H2's empirical/release/recovery prerequisites remain open.
The accepted main 8b48e22 closure is retained. No new empirical data, current national
posterior, field efficacy or funding recommendation is established by this checkpoint.
