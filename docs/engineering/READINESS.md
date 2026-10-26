# Engineering execution, dependency locks and qualification

Dylan A Mordaunt | 24 October 2026

This updates the engineering recommendations at main 711705c. Scientific inputs, models and
published results are unchanged. Implementation, local contract tests, actual tool execution,
hosted execution, independent review and scientific validity are separate states.

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

For every proposed swap: record the old/new interface, scientific invariants, licence and version,
benchmark representative inputs, test domain edges and independent parity, rerun affected models,
then promote through a reviewed dependency change. A newer version is not itself an improvement.

## 2. Separate portable and audit environments

- `engineering/requirements.in`: reference research, test and explicit local-build dependencies.
  The root `requirements.lock` remains a version list, not a transitive hash lock.
- `engineering/audit.in`: adds the existing audit-tool pins. Its resolved lock is scoped to
  Linux x86_64 and Python 3.13. Linux-oriented mutmut/Scalene are not Windows matrix dependencies.
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

Review versions, platform markers, package origins/licences and advisories. Copy the reviewed
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
uvx --python 3.13 --from nox==2026.10.20 nox -s tests quality
uvx --python 3.13 --from nox==2026.10.20 nox -s reproduce
uvx --python 3.13 --from nox==2026.10.20 nox -s strict_all security
```

Tests require a genuine Hypothesis import before collection; absent property-test tooling
cannot silently produce a passing engineering qualification. Every scientific runner retains
its own source/output checks and fresh-output-directory rule. Strict lint and type checks run
independently and produce an overall failure if either fails. Workflow and dependency security
checks also both run, with no ignored advisories. Failed setup cannot be called an executed scan.

CI preserves Nox JSON reports, JUnit, environment, coverage and available audit outputs on
failure. The Linux/macOS/Windows matrix uses the portable profile. The Python 3.15/latest/pre-
release canary remains source-only, requires its test dependencies and cannot promote itself.
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

AGENTS.md, WORKSTREAM_SYNC.md, Conductor and issue #1 remain authoritative. Context bundles bind
explicit role profiles to source hashes and Git state; stale/missing/traversing/symlinked inputs
and byte-budget overflow fail instead of silently truncating. They are not a token optimiser,
secret scanner or prompt-injection sandbox. No persistent background agent is created.

Conductor is still a real pinned submodule, with separate project-owned context in conductor/.
Checkout and host activation must be verified separately. Official `gh-actions-lock` was run on
25 October 2026 and its output **rejected**: it wrote `.github/workflows/actions.lock` only by
replacing all 37 full-SHA action pins with mutable tags, which contradicts the full-SHA posture
this repository already enforces. No transitive action lock is adopted; choosing tag+lockfile
pinning is a security-policy decision, not a mechanical fix. Private-repository entitlements,
attestations, branch rules and independent review remain explicit prerequisites, not
automatically enabled or claimed. Preserve the M3-owned research namespace when synchronising.

## 6. Current evidence

`integration/engineering_hardening_execution_20261025.json` records the first 25 October pass at
`044c9951`; `integration/engineering_hardening_gap_closure_20261025.json` records the second pass
at `5ab361b`. Together they cover the following, all executed on a network-enabled macOS arm64
checkout.

**Locked qualification now exists.** Both reviewed profiles were promoted into `engineering/`
after a review of versions, origins, licences (89 packages; no copyleft, unknown or proprietary
licence; only MPL-2.0 `certifi`/`hypothesis` and dual-licensed `python-dateutil` need noting) and
advisories (0). With `TOBAC_REQUIRE_LOCK=1`, Nox ran `uv pip sync --require-hashes` and then:
`tests` 495 passed, 0 failed, 0 skipped, 91% coverage; `reproduce` verified all five replays
(M1, M2 `--grid-check`, M3, release calibration, empirical longitudinal); `package` built the
sdist and wheel under `--no-build-isolation`. The built wheel installed into a clean Python 3.13
venv and imported `tobac`, `tobac_supply` and `tobac.research`. Bootstrap was not used.

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

**Mutation is executed but weak.** mutmut ran natively on `src/tobac/supply.py`: 128 mutants, 79
killed, 49 survived (61.7%). The session reports success because mutmut enforces no threshold; the
survivor count is a coverage finding, not a pass. The pinned tool is 3.8.0; the 3.7.0 invocation
recorded in the earlier pass is historical evidence. Scalene profiling remains unexecuted.

**The Windows leg failure was a checkout defect, not a code defect.** Windows converted text to
CRLF, so the recorded SHA-256 of `evidence/prior_work/v2.9.0/data/empirical_intake_20261024/
measurement_evidence.csv` no longer matched (LF `144cded7…` vs CRLF `a47dea28…`). `.gitattributes`
now sets `* text=auto eol=lf` and `evidence/** -text`; `git add --renormalize .` changed nothing,
confirming the tree was already LF. Hosted confirmation is still required.

See `integration/engineering_followthrough.json` for the earlier 24 October pass and its actual
failed offline resolution attempt. Command-planning tests there use a labelled Nox test double;
that limitation no longer applies to the sessions named above. No hosted success, signed release,
strict-all pass, profiling result or empirical funding result is claimed. Earlier receipts remain
historical evidence.

**The hosted `quality` leg was failing on a checker that was never actually checking the file.** The
`review/m2b-longitudinal` rebase fixed the declared venv in `engineering/bp_longitudinal.json`, but
pyright resolves an interpreter by precedence and `venv`/`venvPath` did not take effect as declared.
Two consequences, both measured: (1) with no interpreter pinned, pandas ships **no** type stubs, so
`read_csv` is untyped, every DataFrame value collapses to `Unknown`, and `--select ALL` strict mode
reports 154 `reportUnknown*`/stub errors on one file as a cascade — that is the hosted failure; (2)
with the config's own interpreter resolution absent, basedpyright was resolving `include` relative to
the config file and reporting `File or directory ".../scripts/run_empirical_longitudinal.py" does not
exist` while still printing `0 errors`. The earlier local `0 errors` was therefore **vacuous** — it
described a check that had not analysed the runner. The config now uses an `executionEnvironments`
entry with `extraPaths` pointing at `.nox/quality/lib/python3.13/site-packages`, which resolves
imports under any ambient interpreter, including the inactive-venv case Nox actually creates. Real
defects fixed: `table['source_id']`/`source_locator` and `primary['period_start']`/`period_end` are
now read through the checked `DataFrame` instead of `itertuples` attribute access; `source_id` and
`source_locator` are unchanged in the emitted `aligned_observations.csv` (verified in a fresh run), and
the `<column> = <index>` pattern keeps every value identical. Verified: 152 → 139 remaining errors,
all `reportUnknown*` attributable to pandas having no stubs, with **zero** `reportMissingImports`.

**The 139 residual errors are recorded, not silenced.** Strict type checking of the runner is
`quality`'s actual gate, and it is **not green**: 139 errors remain, every one of them the
pandas-stub gap above. They are left failing rather than suppressed with a blanket config ignore, so
the count stays visible. Closing them means adding `pandas-stubs` to the lock, which is a
dependency-review decision, not a `type: ignore` sweep.

**The member-versus-new-option bug is fixed and cross-checked, not asserted.** Verifying
`scripts/check_mutation_score.py` against mutmut 3.8.0 showed its table declared exit code `-24` as
`killed` (63 surviving mutants were miscounted as kills) while omitting `36`/`24`/`152`/`255`
(timeout), `37`, `-11` and `-9` (segfault). The table is now generated against mutmut's own
`status_by_exit_code`; codes agree exactly, `KILLED_STATUSES` stays `{"killed"}`, and a synthetic
probe confirmed each of the ten status classes is classified as mutmut classifies it. The `-24`
asymmetry (mutmut labels `-24` and `+24` both "timeout" although `+24` is SIGXCPU) is mirrored and
noted rather than silently corrected. If mutmut adds statuses, `suspicious` is the safe default and
is already recorded as such.

**Two checks that passed vacuously or by omission are now enforced.** `noxfile.py` installs
`engineering/tools-requirements.txt` with `-U`, because without it pip reported "Requirement already
satisfied" and a stale local basedpyright 1.39.9 passed against a 1.40.2 pin — a version-dependent
false green. The runner is also now held to `ruff --select E4,E7,E9,F,B`, which immediately found 12
real unused-import/multiple-statement findings in `strict_all`'s blind spot; it previously carried no
ruff gate at all. Hosted confirmation of the `quality` leg is still required.

Official documentation consulted:
- https://docs.astral.sh/uv/pip/compile/
- https://nox.thea.codes/en/stable/usage.html
- https://cli.github.com/manual/gh_api
- https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies
