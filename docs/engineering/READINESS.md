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
Checkout and host activation must be verified separately. Official gh-actions-lock remains the
route for a future transitive action lock; no imitation lock was generated. Private-repository
entitlements, attestations, branch rules and independent review remain explicit prerequisites,
not automatically enabled or claimed. Preserve the M3-owned research namespace when synchronising.

## 6. Current evidence

`integration/engineering_hardening_execution_20261025.json` records the 25 October pass at
`044c9951`, where the previously blocked gates were genuinely re-attempted on a network-enabled
macOS checkout. Real Nox executed `tests` (495 passed, 0 failed/skipped, 91% coverage) and
`reproduce` (M1, M2 `--grid-check`, M3 and longitudinal regenerated and verified). Genuine uv
0.13.5 resolution produced receipt-verified `runtime` and `audit` candidates; the runtime lock
installed under `--require-hashes` and the audit lock hash-checked for its Linux/3.13 target.

Two results matter more than the passes. First, **the Linux-only audit guard was hiding real
failures rather than a platform limit**. Ruff, BasedPyright, zizmor and pip-audit all install and
run natively on macOS arm64; executing them found two strict-lint errors, four strict-type errors
and four `artipacked` findings that no session had ever reported. They are fixed and the checks
are now green, but the guard itself is unchanged: it protects Linux-scoped lock installation, not
tool capability, and this repository should add a separate non-Linux native audit lane rather than
relax it.

Second, **the reviewed-lock gate now clears on advisories but is still not promoted**. The first
resolution produced 7 advisories in 3 packages. Review led to remediation of pytest, Pygments and
setuptools, a new explicit `virtualenv` pin, and a `packaging` move from 25.0 to 26.3 that
`virtualenv>=21.14.9` required. Both profiles now report zero advisories. The candidates remain in
`outputs/engineering/lock-candidate` because copying them into `engineering/` is an explicit human
review action, not an automated consequence of a clean scan.

Every Nox session still ran in explicit **bootstrap** mode, so `uv pip sync --require-hashes` was
never exercised inside a session and transitive-lock qualification is still not claimed. `package`
aborts on the missing reviewed lock; mutmut and Scalene were installed but not executed; hosted
matrix, licensed attestations and independent review are unchanged open gates.

See `integration/engineering_followthrough.json` for the earlier 24 October pass and its actual
failed offline resolution attempt. Command-planning tests there use a labelled Nox test double;
that limitation no longer applies to the sessions named above. No completed transitive lock,
strict/static/security tool pass, hosted success, signed release or empirical funding result is
claimed. Earlier receipts remain historical evidence.

Official documentation consulted:
- https://docs.astral.sh/uv/pip/compile/
- https://nox.thea.codes/en/stable/usage.html
- https://cli.github.com/manual/gh_api
- https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies
