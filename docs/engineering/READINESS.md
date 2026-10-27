# Engineering execution, dependency locks and qualification

## Current development platform

Current engineering development is focused on macOS. Linux, Windows and other non-macOS
qualification work is deferred to [`conductor/roadmap.md`](../../conductor/roadmap.md). Existing
workflow definitions and checks remain intact; they may still execute, and their results must be
reported accurately. This scope change does not mark deferred checks as passed or remove them
from repository protection settings.

## Ruff expansion and resource controls — 27 October 2026

Maintained tests, Nox tooling and type stubs now share source/script linting and
stable formatting enforcement. Five exact preview rules and bounded macOS process
groups are documented in [RUFF_POLICY.md](RUFF_POLICY.md). Dated acceptance evidence
is recorded separately; historical counts below retain their original scope.

## Current macOS acceptance — complete, 26 October 2026

The owner selected retaining full-SHA GitHub Actions pins and closing the rejected
generated tag-based lock proposal. All 40 current external Action references use
full commit SHAs; no generated Actions lock is adopted. No workflows, required
checks, audit policies, dependency pins or security settings change in this close-out.

At inspected base `f11d491`, hosted Python 3.15.1 qualification passed 745 tests with
four optional-environment skips and 93% coverage. All macOS engineering sessions
pass, including whole-source strict checks, reproduction, packaging, security and
mutation. Mutation detects 100/131 (76.3%); 31 survivors and the 175 documented
style/API exceptions are retained as non-blocking follow-ups. Bounded installed
Voiage compatibility and native Dependency Graph repair are verified separately.

Current receipt: `integration/engineering_macos_completion_20261026.json`. Both
engineering tracks are complete for macOS; other platforms and advisory expansion
remain in `conductor/roadmap.md`. The dated sections below preserve earlier failed
and intermediate measurements; they do not reopen resolved macOS gates. Scientific
calibration and external validity remain separate from software qualification.

Dylan A Mordaunt | 24 October 2026

This updates the engineering recommendations at main 711705c. Scientific inputs, models and
published results are unchanged. Implementation, local contract tests, actual tool execution,
hosted execution and scientific validity are separate states. This single-developer repository
does not require independent review as an engineering gate.

## 1. Existing-library policy
Use the maintained stack before another custom engine. SciPy owns the production Gaussian
reporting density; its old calculation remains an independent test oracle. jsonschema validates
context profiles. Nox/uv own orchestration, resolution and installation; the new lock helper
only checks source/artifact identity. It is not a package resolver or a custom lock format.

The M3 workstream retains ownership of weighted voiage, portfolio and staged-design work.
Do not introduce a competing VOI adapter. NumPyro/JAX/ArviZ are candidates for the eventual
hierarchical censored observation model; mars-earth is a candidate for demonstrably necessary
surrogates. No automatic replacement of small exact calculations with approximate inference.
Pint/Pandera/Pydantic do not establish the scientific compatibility of dates, products, units,
source identities or populations. Rust acceleration requires a measured bottleneck and parity.
The detailed decision record remains in LIBRARY_REUSE_REVIEW.md.

For every proposed swap: record the old/new interface, scientific invariants and version,
benchmark representative inputs, test domain edges and independent parity, rerun affected models,
then promote through a reviewed dependency change. A newer version is not itself an improvement.

## 2. Separate portable and audit environments

- `engineering/requirements.in`: reference research, test and explicit local-build dependencies.
  The root `requirements.lock` is a compatibility include for the version list in
  `engineering/reference-requirements.txt`, not a transitive hash lock.
- `engineering/audit.in`: adds the existing audit-tool pins. Its resolved lock is scoped to
  Linux x86_64 and Python 3.15.1. Linux-oriented mutmut/Scalene are not Windows matrix dependencies.
- `engineering/build-requirements.txt`: explicit setuptools pin. Local project installation
  uses `--no-deps --no-build-isolation`, so it cannot fetch an unreviewed build backend.

Generate real candidates on a network-enabled checkout:

```sh
python scripts/lock_receipt.py generate --profile runtime --path outputs/lock-candidate
python scripts/lock_receipt.py generate --profile audit --path outputs/lock-candidate
```

Alternatively dispatch **Reviewable dependency-lock candidates**. Its two jobs resolve
independently with uv and upload successful candidates; they never commit, merge or publish.
A resolver failure removes partial lock/receipt files. Existing files are never overwritten.

Review versions, platform markers, package origins and advisories. Copy the reviewed
candidate pairs into `engineering/`: `requirements.lock` with `requirements.lock.json`, and
`audit.lock` with `audit.lock.json`. Commit them through normal review. The JSON files bind
exact dependency-input and lock bytes to the resolver command and version. They are neither
human approval nor signed provenance. uv checks full hash syntax and dependency consistency
when installing; the helper does not replace those checks. Newly introduced include files must
be added to the explicit reviewed input profile rather than silently escaping the receipt.

```sh
python scripts/lock_receipt.py verify --profile runtime --path engineering/requirements.lock
python scripts/lock_receipt.py verify --profile audit --path engineering/audit.lock
```

Source changes, altered/missing receipts, changed lock bytes, undeclared includes and symlinked
inputs fail closed. With a valid lock, Nox uses `uv pip sync --require-hashes`, not an additive
install. No tool package is added after that sync. Without either lock, ordinary development
sessions explicitly report bootstrap mode. A partial/stale lock never permits fallback.

## 3. Execution and reports

```sh
uvx --python 3.15.1 --from nox==2026.10.20 nox -s tests quality
uvx --python 3.15.1 --from nox==2026.10.20 nox -s reproduce
uvx --python 3.15.1 --from nox==2026.10.20 nox -s strict_all security
```

Tests require a genuine Hypothesis import before collection; absent property-test tooling
cannot silently produce a passing engineering qualification. Every scientific runner retains
its own source/output checks and fresh-output-directory rule. Strict lint and type checks run
independently and produce an overall failure if either fails. Workflow and dependency security
checks also both run, with no ignored advisories. Failed setup cannot be called an executed scan.

CI preserves Nox JSON reports, JUnit, environment, coverage and available audit outputs on
failure. Python 3.15.1 is the required runtime across development, build, tests and CI. The
Linux/macOS/Windows matrix uses the portable profile. The latest/pre-release canary remains
source-only, requires its test dependencies and cannot promote itself.
Direct Actions remain full-SHA pinned, read-only, credential-free after checkout and bounded
by concurrency, timeouts and retention. No pull_request_target or automatic scientific merging.
Renovate's pending upgrades still require review; this change does not merge them.

The internal-candidate workflow requires both lock/receipt pairs to be committed and verifies
all their input hashes, then sets `TOBAC_REQUIRE_LOCK=1`. Tests, quality, whole-source strict
lint/type audit, security, complete M1/M2/longitudinal replay and packaging must succeed.
Failure evidence and successful packages have different artifact names. No PyPI upload,
research submission, account permission change or claim of external package qualification.
The uv/Nox bootstrap executable pins are separate from the resolved environments; a checksum
receipt alone is not a complete toolchain attestation or reproducible-build certification.

## 4. Diagnose pre-runner failure from actual evidence

The live connector can retrieve run/job summaries but rejects direct check-run annotation
requests. The cause of the pre-runner failures is not established. On an authenticated machine
with the official GitHub CLI, run this outside hosted Actions (so it does not need a runner):

```sh
python scripts/actions_diagnostics.py --repo edithatogo/tobac --run 40080148087 --out outputs/actions-diagnostic.json
```

The script uses GET only, reads all job pages, retrieves annotations from each returned
check_run_url, records missing annotation access and distinguishes absent execution from failed
steps. It exits nonzero for unsuccessful/incomplete job evidence and never guesses billing or
changes settings. Annotation content is untrusted data, not a command. Actual human/administrator
action may be required once the upstream annotation identifies the reason; issue #4 remains open.
Do not weaken checks, make the repository public, or use a self-hosted runner to bypass controls.

## 5. Context and coordination

AGENTS.md, WORKSTREAM_SYNC.md and Conductor remain authoritative. Context bundles bind
explicit role profiles to source hashes and Git state; stale/missing/traversing/symlinked inputs
and byte-budget overflow fail instead of silently truncating. They are not a token optimiser,
secret scanner or prompt-injection sandbox. No persistent background agent is created.

Conductor is still a real pinned submodule, with separate project-owned context in conductor/.
Checkout and host activation must be verified separately. Official `gh-actions-lock` was run on
25 October 2026 and its output **rejected**: it wrote `.github/workflows/actions.lock` only by
replacing all 37 full-SHA action pins with mutable tags, which contradicts the full-SHA posture
this repository already enforces. No generated transitive action lock is adopted. The owner
closed the decision on
26 October: retain full-SHA references and reject the tag-based proposal. The repository
currently has one
collaborator (the owner), no branch protection or repository rulesets, and no required-review
policy. No additional collaborator, reviewer or branch rule is needed for this project. Preserve
the M3 research namespace when making shared changes.

## 6. Historical execution evidence

`integration/engineering_hardening_execution_20261025.json` records the first 25 October pass at
`044c9951`; `integration/engineering_hardening_gap_closure_20261025.json` records the second pass
at `5ab361b`. Together they cover the following, all executed on a network-enabled macOS arm64
checkout.

**Locked qualification now exists.** Both reviewed profiles were promoted into `engineering/`
after a review of versions, origins and advisories (0). With `TOBAC_REQUIRE_LOCK=1`, Nox ran
`uv pip sync --require-hashes` and then:
`tests` 495 passed, 0 failed, 0 skipped, 91% coverage; `reproduce` verified all five replays
(M1, M2 `--grid-check`, M3, release calibration, empirical longitudinal); `package` built the
sdist and wheel under `--no-build-isolation`. The built wheel installed into a clean Python 3.13
venv and imported `tobac`, `tobac_supply` and `tobac.research`. This is historical execution
evidence; Python 3.15.1 qualification is recorded separately below. Bootstrap was not used.

**The Linux-only audit guard was hiding real failures rather than a platform limit.** Ruff,
BasedPyright, zizmor and pip-audit all run natively on macOS arm64; executing them found two
strict-lint errors, four strict-type errors and four `artipacked` findings that no session had
ever reported. They are fixed and `quality`/`security` are green. `noxfile.py` now routes audit
sessions through `audit_tools()`: Linux keeps the locked audit profile as authoritative, other
hosts resolve the same reviewed pins natively and log `NATIVE AUDIT ... NOT release
qualification`. The guard in `environment()` is unchanged and still fails closed.

**Two defects surfaced only because the gates actually ran.** First, `strict_all` has never been
green: 4,168 ruff `--select ALL` errors and 3,584 BasedPyright-all errors across the whole source.
That is measured, not fixed, and remains an open gate. Second, three engineering contract tests
failed under `TOBAC_REQUIRE_LOCK=1` because the harness fixture inherited the release flag with an
empty `ROOT`; `.github/workflows/release-candidate.yml` sets exactly that flag, so the release
gate itself was broken. The fixture is now hermetic.

**Mutation was executed but weak at the 25 October gap-closure pass.** mutmut 3.7.0 ran natively
on `src/tobac/supply.py`: 128 mutants, 79 killed, 49 survived (61.7%). The session reports
success because mutmut enforces no threshold; the survivor count is a coverage finding, not a
pass. Scalene profiling was unexecuted at that pass; the 26 October profile is recorded below.

**The Windows leg failure was a checkout defect, not a code defect.** Windows converted text to
CRLF, so the recorded SHA-256 of `evidence/prior_work/v2.9.0/data/empirical_intake_20261024/
measurement_evidence.csv` no longer matched (LF `144cded7…` vs CRLF `a47dea28…`). `.gitattributes`
now sets `* text=auto eol=lf` and `evidence/** -text`; `git add --renormalize .` changed nothing,
confirming the tree was already LF. Hosted confirmation is still required.

See `integration/engineering_followthrough.json` for the earlier 24 October pass and its actual
failed offline resolution attempt. Command-planning tests there use a labelled Nox test double;
that limitation no longer applies to the sessions named above. Hosted runs on the pre-migration
base are historical and do not qualify Python 3.15.1. No post-migration hosted success, signed
release, strict-all pass or empirical funding result is claimed. Earlier receipts remain
historical evidence.

## Historical Python 3.15.1 migration pass — 26 October 2026

The repository now requires CPython 3.15.1 for active development, test, build, automation and CI
paths. The source tree selects NumPy 2.5.4, SciPy 1.18.1, pandas 3.0.6 and Matplotlib 3.11.2;
these replace pins that could not install on Python 3.15.1. Runtime and Linux x86_64 audit lock
candidates were generated by uv 0.13.5, input-bound, hash-checked and installed for the runtime
profile. The new audit lock resolves for Linux/Python 3.15 but was not installed or executed on
Linux in this worktree.

On a repository-local Nox environment running Python 3.15.1, `nox -s tests` passed **611 tests**
at **90% coverage**. `nox -s reproduce` passed M1, M2 with grid check, M3, release calibration
and empirical longitudinal verifiers; the four regenerated longitudinal tables matched their
checked-in results within the existing tolerance. The locked internal package session built the
sdist and wheel; the wheel installed into a clean 3.15.1 environment, passed `uv pip check` and
imported all three public package namespaces. Native macOS arm64 Nox `quality` and `security`
passed; pip-audit found no known vulnerabilities and zizmor reported no findings.

The bounded Scalene 2.4.0 quick profile also completed on Python 3.15.1. Its local JSON artifact
is 8,216,717 bytes, elapsed time 19.63 seconds, SHA-256
`67f93dd57256d8e889d8bcfc5ff470deb6fe9ed8f57b53931f916e9fb2d8be26`; the runner reported 21
artifacts, 6 source files and its historical-partial-fit scope. The artifact remains in ignored
local outputs; its checksum and summary are retained here and in
`integration/engineering_hardening_python315_20261026.json`.

At this historical migration pass, whole-source `strict_all` was red; its corrected Nox run
reported 1,248 Ruff and 2,208
BasedPyright errors. Direct JSON BasedPyright readback reports 2,052, so that discrepancy is
recorded for follow-up at that time. Hosted macOS and strict checks were subsequently
qualified in the receipts below; this pass did not establish attestations. Independent review is
not a repository gate.
Linux hash-locked audit execution and non-macOS hosted matrix qualification are deferred to
`conductor/roadmap.md`. The generated Actions-lock proposal was rejected because it replaced
full-SHA pins
with mutable tags; the owner has now closed that decision in favour of full-SHA pinning.

Official documentation consulted:
- https://docs.astral.sh/uv/pip/compile/
- https://nox.thea.codes/en/stable/usage.html
- https://cli.github.com/manual/gh_api
- https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies

## Historical PR #25 reconciliation passes — 26 October 2026

The 916a41e parallel profile attempt was uninformative and is retained in history. It does
not overwrite the Python 3.15.1 receipt above. The focused longitudinal checker now uses
qualified stubs and the actual Nox session interpreter, with no cached cross-environment path.
The mutation gate requires complete results and a fresh source/tool-bound receipt.

The latest implementation supersedes the historical red strict counts above. All active source
and CLI modules now report zero BasedPyright errors and zero configured Ruff findings on the
session's actual Python 3.15.1 interpreter. The zero Ruff result includes 175 explicitly retained
style/API exceptions; these are policy choices, not defects repaired. Scientific stubs describe
static contracts, not optional-library runtime qualification. See LINT_POLICY.md and the exception
ledger. No global unknown, missing-import or argument-type diagnostics were disabled.

Mutation preparation now removes both selected generated source and metadata: mutmut's mtime
cache otherwise skips regeneration after metadata removal. A fresh run and a repeat run detect
92/131 mutants (70.2%); 39 survive. The 60% floor is a regression alarm, not complete test proof.
Boundary tests cover each physical channel's finiteness/sign, legal zero endpoints, reporting
shape/domain and strict covariance symmetry. Numerical likelihood parity uses the independent
Cholesky oracle. The clean wheel imports from site-packages outside this checkout on 3.15.1.

Original core bytes are retained and verified against unchanged extraction hashes. The active
core has a constrained AST maintenance check covering annotations, cast identity and explicit
literal bindings; tampering tests reject changed formulas, defaults, fields and bindings.
Reproductions write fresh directories and retain earlier receipts. PR #25 and subsequent main
coverage/scientific-planning/incorporation-review changes are preserved. The scientific ecosystem
track remains planning-only. Current execution details are in
`integration/engineering_reconciliation_20261026.json`; the pending hosted checks
at that intermediate pass were subsequently reported successful there. No optional Voiage
runtime or new scientific calibration is claimed.

The subsequent main Ruff 0.17.2 update is retained and its native quality, strict_all and security
sessions pass. The legacy hosted optional Voiage 2.1.0 probe fails installation on Python 3.15.1:
its SciPy <1.17 requirement selects an unsupported source build. The released 2.2.0 wheel was
also inspected and attempted in an isolated macOS environment; it retains SciPy <1.17 and
pandas <3 requirements, and pyarrow 25.0.1 has no cp315 wheels. Installation failed. Those
optional-library probes remain fail-closed; this is a genuine upstream qualification blocker,
not a passing macOS reference check or permission to bypass dependency metadata.

Hosted macOS qualification is now obtained at `c645028` in run `40269769566`: the actual Python
3.15.1 assertion passed, 721 tests passed with two optional-tool skips and 93% coverage, and
quality/strict_all/reproduce/package/security/mutation all passed. Hosted mutation killed
100/131 (76.3%), with 31 survivors; local 92/131 remains a separate observation. The final
receipt-only update publishes through PR #29 after checking its current head. The receiving
`main` ref and merge commit are readable from that PR. Voiage probes were still blocked at that
intermediate pass; their later successful
compatibility qualification is recorded below. This earlier receipt is not an all-jobs pass.

## Voiage dependency compatibility follow-up

The historical blocker above is addressed by a distinctly versioned, metadata-only
source build, with normal dependency resolution and a separate input-bound hash lock.
Both installed-library probes and Arrow/native checks pass locally on Python 3.15.1.
See `VOIAGE_PYTHON315.md` and `integration/voiage_python315_compatibility_20261026.json`
for scope and current hosted outcomes. The reference scientific pins are unchanged.

Voiage follow-up completed through PR #33 at `f06eed6`: all 15 hosted checks pass
on its exact qualified head, including both formerly failing installed-library
jobs. Python remains 3.15.1. The compatibility receipt records receiving commit,
source/patch/wheel identity and actual hosted equal/weighted/native/Arrow scope.

## Native Dependency Graph manifest discovery

The canonical version list is `engineering/reference-requirements.txt`; the root
`requirements.lock` remains a compatible include. This fixes the managed fetcher's
unsupported custom include suffix without changing any version pins, Python 3.15.1
selection, audit settings or required checks. All three hash-lock receipts bind the
new canonical input. See `DEPENDENCY_GRAPH.md` and
`integration/dependency_graph_20261026.json` for actual native execution status.

Native Dependency Graph qualification is now obtained: run `40275206942` passed
after PR #35 merged at `666dd8c`. Native readback retained every previous package
identifier and added 15 missing entries. No Python selection, dependency versions,
required checks, repository visibility or security settings changed.

## Current evidence interchange qualification — 26 October 2026

The optional Arrow/Polars boundary now preserves the existing EvidencePacket,
Scope and SupplyBasis contract, including supplied covariance provenance and
UTC/null timestamps. See EVIDENCE_INTERCHANGE.md and
integration/ecosystem/interchange_20261026.json for actual software evidence.
Required tests and clean installed-package checks exercise it; existing scientific
models, data and reference outputs remain unchanged. Native Voiage 2.2 compatibility
qualification is distinct from the future Voiage 3 migration in PR #41.

The earlier native graph success above is historical. The root managed parser
still lacks Python 3.15 support (run 40325526891, upstream issue 16524); a later
engineering-directory graph success does not prove root-parser compatibility.
The supported resolved-lock snapshot submission and complete native graph readback
remain qualified. No check or runtime requirement is waived.
