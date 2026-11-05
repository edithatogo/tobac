# Reconciled repository status — 3 November 2026

DXP1–DXP4 are complete through actual hosted qualification. The advisory
implementation is qualified and published to main at `672894f`. The retained native-lineage track has
**8/8 phases and 32/32 primary tasks complete**, with zero in progress or pending.
The 18 archived tracks have no active execution tasks. Five historical graph
proposal entries were superseded by bounded inventory acceptance and are explicitly
labelled historical in their archived plan, rather than marked as executed.

## Latest receiving-main verification — 5 November 2026

All nine post-publication workflows completed successfully at receiving main
`135487ea288298e43d5592eda08a7ecbf3e90f0b`: empirical longitudinal (41984676678),
[scientific reproduction](https://github.com/edithatogo/tobac/actions/runs/41984676696),
[engineering qualification](https://github.com/edithatogo/tobac/actions/runs/41984676733),
regulatory uncertainty (41984676743), cross-platform Python (41984676816), M3
research methods (41984676698), publication and source security (41984676808),
Linux audit lock (41984676748), and package portability (41984677169).
Both reproduction platforms, both M3 jobs, and every engineering job passed.
These results bind the cited published commit; they do not qualify later metadata
or dependency candidates. Earlier receiving-main records remain in repository history.

## Latest receiving-main hosted results — 5 November 2026

All nine post-publication workflows completed successfully at receiving main
`669eb8851b89eef91b3b014787639fb2765768ef`: package portability (41967153709),
cross-platform Python (41967153730), M3 research methods (41967153794), Linux
audit lock (41967153737), empirical longitudinal (41967153722), publication and
source security (41967153750), regulatory uncertainty (41967153654), [scientific reproduction](https://github.com/edithatogo/tobac/actions/runs/41967153799)
and [engineering qualification](https://github.com/edithatogo/tobac/actions/runs/41967153705).
Both reproduction platforms and every engineering job passed. These results bind
the cited published commit; they do not qualify later metadata changes or the
separate dependency PRs.

## Receiving-main hosted results — 5 November 2026

All nine push workflows completed successfully at receiving main
`c30cae8d1f37b7335ed8f18dd0383324d625899f`: package portability (41963627981),
M3 research methods (41963627996), Linux audit lock (41963628050), cross-platform
Python (41963628012), empirical longitudinal (41963628023), [scientific reproduction](https://github.com/edithatogo/tobac/actions/runs/41963628010),
publication and source security (41963628078), regulatory uncertainty
(41963628017), and [engineering qualification](https://github.com/edithatogo/tobac/actions/runs/41963628199).
Both reproduction platforms and every engineering job passed. The receiving-main
Voiage parity job used the new OpenSSH binary and verified signed inputs before
passing. The separate setup-python combination with the new binary has passed a
signature/tamper probe but its full signed-input check on that image remains
unobserved; its previously qualified binary passed receiving-main jobs. The
results qualify the cited published revision, not later metadata edits or the
separate dependency PRs.

## Hosted runtime renewal — 5 November 2026

PR #122 source `d8afca1` encountered a new macOS OpenSSH binary
`e9cba2415f13366eb43402ab20218433f585851b4f4a749a6a1e9988e6af9eb5`.
The frozen verifier correctly rejected it before workload execution. Hosted jobs
[127021871259](https://github.com/edithatogo/tobac/actions/runs/41959394253/job/127021871259)
and [127021871304](https://github.com/edithatogo/tobac/actions/runs/41959394384/job/127021871304)
ran actual signing/valid-signature and tamper-rejection controls on the two
observed Python 3.15.1 builds. The candidate adds only those two exact runtime
combinations. All eight accepted native attempts were reopened, the 140 outputs
verified and a fresh digest-only capsule issued; runner records, native readback
and scientific inventory match the previous generation. The previous capsule,
signature, verifier and profiles are preserved in
`integration/archive/hosted-generation_runtime_20261105.zip`.
Local signed verification passed for all eight runners; focused lineage and
workstream checks passed 42 tests with one capability skip, and the selected
qualified verifier passed separately. The full suite passed 1,238 tests with seven
skips; strict checks and clean-source reproduction passed. The first reproduction
attempt correctly stopped at clean-source replay while the renewal was uncommitted;
the committed-source rerun passed. Hosted candidate `3695fd64441c884553ef158a4023df2f82fb0f08`
passed 28 executable PR checks with two conditional skips. The [quality job](https://github.com/edithatogo/tobac/actions/runs/41961257205/job/127027899235)
used the newly observed OpenSSH binary, passed signature/tamper controls and
verified the signed native inputs before execution. The separate setup-python
combination passed the hosted probe; its full verification on the newly observed
image was not separately observed. Final metadata publication requires its own
checks and receiving-ref readback.

## Verified baseline

As checked on 5 November, receiving main `927bfdaacc49421456da0f94dc661fd4ec245579`
completed all nine post-publication workflows successfully: empirical longitudinal
(41641218791), package portability (41641218788), cross-platform Python
(41641218822), [scientific reproduction](https://github.com/edithatogo/tobac/actions/runs/41641218932),
Linux audit lock (41641218703), M3 research methods (41641218714), publication
and source security (41641218611), [engineering qualification](https://github.com/edithatogo/tobac/actions/runs/41641218726)
and regulatory uncertainty (41641218904). Both reproduction platforms and all
engineering jobs passed. PR #121 previously passed 29 checks, with two conditional
skips, and its receiving commit and tree were verified. These results cover that
published revision; they do not qualify later changes or the separate dependency PRs.

Consumer main `35f999a42abb7836fde14c58368bb2f356bda0d1` was read back on
3 November. All nine receiving-main workflows for that exact commit completed
successfully: empirical longitudinal (41636195121), regulatory uncertainty
(41636195096), Linux audit lock (41636195183), publication and source security
(41636195219), M3 research methods (41636195112), cross-platform Python
(41636195135), package portability (41636195126), [scientific reproduction](https://github.com/edithatogo/tobac/actions/runs/41636195079)
and [engineering qualification](https://github.com/edithatogo/tobac/actions/runs/41636195027).
The last two passed on Linux and Windows and in every engineering job respectively.
PR #120 qualified this metadata commit with 29 passing checks and two conditional
skips before the non-force fast-forward. The prior metadata closeout `1961a04` and
advisory source commit `672894f` also each passed all nine receiving-main workflows.
Producer receiving main `c76d78df37ffa89469e8fca5f2db521553525276` was read back
on 2 November. The functional lineage consumer implementation is `14303e4`;
`e88d563` records its earlier Conductor closeout.
[Reconciliation receipt](../integration/reconciliation_20261102.json).

[Native lineage](tracks/native_archival_lineage_20261026/plan.md) closes P1.1–P8.4
and AC01–AC14 for the declared eight-runner closure. The independent USB restore,
interruption recovery, installed replay, hosted verifier and guarded publications
are verified in [final acceptance](../integration/archive/p8-final-acceptance_20261102.json).
Published Voiage 3.0.0 qualified in [PR #104](https://github.com/edithatogo/tobac/pull/104)
and its [receipt](../integration/voiage_published_20261102.json).

Snapshot 117127776 binds `e88d563` and all four committed lock hashes. All 115
submitted PURLs appear in the native 128-PURL aggregate. This is resolved package
inventory coverage. Native package edges, deployment exposure and managed-parser
success remain unqualified. Upstream issue #16524 and PR #16525 are still open.
The archived ecosystem's queued receiving-main and Voiage release gates are resolved.

## Completed DXP1 — Linux audit lock

GitHub [run 41534684953](https://github.com/edithatogo/tobac/actions/runs/41534684953)
on Ubuntu 24.04 x86_64 / Python 3.15.1 installed the unchanged source-bound audit
lock with hash checking. Downloaded evidence matches all 96 locked packages plus
the editable project, with zero unexpected packages. Nox `strict_all` and `security`
pass: Ruff lint/format, whole-source typing with zero errors/warnings, pedantic
workflow audit and pip-audit with no known vulnerabilities. Nine Ruff-policy tests
and 96 focused lock/workstream tests pass. Linux scanner archives match the
publishers' checksum manifests; artifact inspection and secret scanning pass.
[Qualification receipt](../integration/linux_audit_lock_20261103.json) binds source
`a17d90b`, eight lock inputs, actual job/artifact IDs, reports and the initial failed
attempt. DXP2–DXP4 have their own current receipts below; mutation and profiling retain separate scopes.

## Completed DXP2 — package portability

Linux and Windows [run 41542664379](https://github.com/edithatogo/tobac/actions/runs/41542664379)
passed the existing native-gated Nox `package` and `clean_package` commands on
Python 3.15.1 with source-bound hash locks. Each platform built direct and
sdist-reconstructed wheels with identical contents within that platform, then
installed both into fresh environments outside the checkout using Unicode/space
paths. Isolated namespace imports, the independent API oracle, Unicode Arrow/Polars
and IPC identity round trips, and the installed quick CLI all pass. Wheel module,
license/notice bytes and dependency/extra markers match the source declarations.

[Artifact readback](../integration/package_portability_20261103.json) verifies the
retained wheel/sdist/reports and ten dependency-marker cases. Cross-platform member
hashes differ only for METADATA's LF/CRLF encoding and its RECORD hash; METADATA
matches after newline normalization. No cross-platform byte-identical wheel claim
is made. Native scanners pass pinned archive checksums and report their expected
versions; inspected artifact exports pass on both hosts. DXP3 separately qualifies full numerical
reproduction; DXP4 below qualifies the manual release/candidate workflows.

## Completed DXP3 — scientific reproduction

[Run 41557415490](https://github.com/edithatogo/tobac/actions/runs/41557415490)
passed full native-gated, hash-locked Nox reproduction on Linux and Windows.
Each host executed all eight accepted runner variants, including no-grid M2, and
compared all 82 scientific CSV tables against original native-byte-verified results.
Exact schemas, rows and identities pass. Existing publication absolute and scaled
reference tolerance policies are recorded per runner. Each host also passes the
29-table clean committed-source publication replay, longitudinal goldens, input/output
manifest checks and synthesis validators.

[Evidence](../integration/scientific_reproduction_20261103.json) retains measured
differences, raw/view hashes, run/artifact IDs, code pins and both first failures.
Windows uses a separately hash-verified canonical validation view; raw scientific
outputs and the pinned synthesis reader remain unchanged. The hosted capsule was
renewed only after reopening all eight original native attempts; the previous
generation remains preserved for P8 integrity readback. No model, configuration,
scientific input or existing numerical validator changed.

Software reproduction does not supply empirical calibration or external scientific
endorsement.

## Completed DXP4 — manual release and lock workflows

Manual [release run 41570769167](https://github.com/edithatogo/tobac/actions/runs/41570769167)
at `fdd6be0` passed all seven locked Nox sessions: tests, quality, whole-source
strict checks, security, reproduction, package and clean-package qualification.
JUnit records 1,210 passed tests, 19 capability skips, zero errors/failures;
coverage over all `src` reports 92.03% combined coverage
(92.74% statements, 89.64% branches). All eight scientific
variants / 82 CSV tables also pass downloaded-byte comparison under the existing
policies. The wheel matches the clean build byte for byte. Sdist member bytes
match; differing archive timestamps/pax metadata prevent a byte-identical sdist claim.

Manual [lock run 41567710835](https://github.com/edithatogo/tobac/actions/runs/41567710835)
at `3914060` generated and hash-installed all four profiles on Linux. Downloaded
source receipts, member hashes and exact inventories pass: runtime 37, audit 95,
Voiage 50 and ecosystem 58 packages. No candidate is adopted, and Linux candidate
installation does not establish fresh Windows/macOS candidate qualification.

Six deliberately stale-source jobs reject before their workloads. The first
release correctly rejected Ubuntu 24.04's unqualified OpenSSH. The corrected
workflow uses the already-qualified Ubuntu 26.04 image through the established
`ubuntu-latest` label; the frozen verifier profiles remain unchanged. Native
readback reopened all eight original attempts before renewing the workflow pin.
Preflight JSON and exit status are retained. Source promotion used guarded
non-force fast-forwards, with both receiving refs and complete trees read back.
[Final receipt](../integration/manual_workflows_20261103.json) distinguishes the
lock source, release source and metadata closeout. No PyPI release is performed.

## Completed DCI1 — advisory additions and pins

[Selection](roadmap/cicd_hardening_20261025/selection_20261103.md) selects one
bounded ty 0.0.95/Pyrefly 1.4.0 comparison experiment, with macOS/Linux x64 and
Linux ARM64 static diagnostics. GitHub commit refs, release age and six expected
wheel hashes were verified from upstream metadata. Ty 0.0.96 is below the existing
three-day minimum age. Duplicate action wrappers and prek migration are omitted.

Ten active action refs and 14 considered upstream refs were re-read. Original
strict/pre-runner/private-entitlement blockers are historical; issue #4 is closed.
The current reference, locks, hooks, workflow and verifier profiles are unchanged.
No selected checker, new lock, ARM job or advisory runtime is installed/executed
by that metadata-only step. DCI2 was implemented subsequently on a branch;
DCI3 subsequently qualified the hosted advisory matrix; DCI4 published it to main and verified the receiving tree.

## Remaining deferred phases and tasks

DXP1–DXP4, DCI1–DCI4, DH1 and DH2 are complete. The advisory lane reached main at `672894f` after 28 passing hosted checks and receiving-tree verification.

| Group / phase | Tasks remaining |
| --- | --- |
| Advisory CI/CD lane | DCI1–DCI4 complete; advisory promotion remains optional. [Plan](roadmap/cicd_hardening_20261025/plan.md). |
| Optional macOS hardening | DH1 complete: triaged all 12 dated survivors; fresh local mutation run detected 129/131, with two backend-equivalent survivors. DH2 complete: reviewed the retained source/API Ruff exceptions and documented why they remain, including a tested refactor that invalidated scientific lineage. |

Linux/Windows runtime tests and hosted lineage verification already passed.
DXP1 additionally qualifies the Linux hash-locked strict/security audit commands.
DXP2 also qualifies Linux/Windows source/wheel build and clean installation.
Full platform numerical reproduction is qualified by DXP3; DXP4 qualifies the manual
Linux release and lock candidates. DH1 triage and DH2 review are complete locally; the dated hosted mutation count
remains distinct from the later local run.

## Open dependency maintenance

These PRs are outside the completed research tracks. On 5 November, the rebased candidate heads below had failing checks against
receiving main `1759fe7`. The observations are from their recorded jobs and do not qualify any update.

| PR | Observed failure and remaining task |
| --- | --- |
| [#80](https://github.com/edithatogo/tobac/pull/80), `b291bfc` — verified action pins | The candidate changes 14 workflows. Sampled Linux test and macOS qualification jobs reject `.github/workflows/advisory-types.yml` as a stale signed native acceptance pin before execution. Reconcile the candidate with current main, requalify the action changes and renew the signed binding only after the required native readbacks, then run required checks and verify publication. |
| [#91](https://github.com/edithatogo/tobac/pull/91), `37f9984` — Python 3.15.2 | The current candidate changes `.python-version` alone. Its Linux tests and numerical job fail because the canonical version contract remains 3.15.1. Qualify a consistent Python patch migration across development, build, tests, CI, locks and the pinned verifier contract before promotion. |
| [#94](https://github.com/edithatogo/tobac/pull/94), `abaff70` — pytest-gremlins 1.13.2 | The candidate changes `engineering/ecosystem.in`; its Linux tests reject stale ecosystem dependency-input hashes. Regenerate and review the affected source-bound locks and receipts, qualify the tool and run required checks before promotion. |

The #80 export error after failed lineage preflight is a downstream missing-output
error. On the earlier #91 candidate `e445af7`, a separate Voiage parity job failed
on an HTTP 500 while downloading a scanner; its following export could not find
that scanner. The earlier rebased candidate `91bd178` had five failed checks, and its
Voiage parity check passed. The earlier network failure remains historical. None of the candidates is merged;
no security, source-binding or scientific gate has been relaxed.

At these rebased heads, #80 has 21 failed and eight passing checks; #91 and #94
each have five failed and 24 passing checks. Each also has two conditional
skips. Sampled Linux jobs reproduce the [signed-pin rejection](https://github.com/edithatogo/tobac/actions/runs/41980351665/job/127088769200),
[version mismatch](https://github.com/edithatogo/tobac/actions/runs/41980330434/job/127088702256)
and [stale lock receipt](https://github.com/edithatogo/tobac/actions/runs/41980363050/job/127088806496)
respectively. Candidate checks do not establish that these are the only possible
failures after their identified blockers are fixed.

## Scientific and submission requirements

[Research gates](research-gates.md) retain the selected target/legal/counterfactual
facts, source year/unit/channel reconciliation, physical conversions, matched
consumption/measurement and covariance records, source-to-target transport,
policy/biomarker calibration, Māori governance/permissible use/current costs,
and held-out empirical validation. All eight matched consumption cells remain
unavailable. Issue #3 remains open. No empirical national posterior or policy
acceptance follows from software qualification.

Historical capture timestamps and archive coverage beyond the declared runner
closure remain limited. AC13's completed independent restore is no longer an open
current-closure requirement. Remote/wider-estate recovery is separately owned.

The MDM article and NZMJ Viewpoint still require author facts, contributions,
affiliations, actual funding/interests, personal final approval and applicable
institutional/cultural/journal determinations. Public-only/no-request constraints
continue. No external requests, submissions, registrations or deposits are authorized
by this status reconciliation.

## Decision drafts and Git disposition

All three November 1 drafts are retained as superseded historical proposals,
with current acceptance links, original-draft digests and unverified approval
placeholders identified. They create no pending wheel rebase, placeholder source-ID,
media-format or recovery task.

- [Phase 5/6 sequencing](../docs/decisions/phase5_6_sequencing_20261101.md)
- [Phase 5/6 implementation](../docs/decisions/phase5_6_implementation_20261101.md)
- [AC13 independent-copy recovery](../docs/decisions/ac13_independent_copy_recovery_20261101.md)

There was one clean consumer worktree at `main` `1961a04` before this reconciliation. The DCI checkpoint `e007807` is a retained non-ancestor historical branch whose implementation was integrated and subsequently qualified and published; it is not an active unfinished task. Other retained non-ancestor branches include historical/superseded lanes and the saved divergent former main. No changes are discarded or silently merged. The only open repository PRs at this checkpoint
are the three dependency candidates above. This reconciliation changes documentation
and the exact public-path inventory only; scientific inputs, outputs, runtime,
locks, native objects and private authority remain with their existing owners.

## Reconciliation verification

The track-name check passes for all 20 registered track records. All Conductor
metadata JSON parses, and local Markdown targets in the current public status
records resolve. Intentionally excluded manuscripts and requests are explicitly
labelled local-only. The focused archive, publication-boundary and cross-workstream
suite passes 41 tests on repository-local Python 3.15.1 under the 4 GiB/40-minute
guard. Scientific/runtime source is unchanged; the full executed receiving-main
qualification is reused at its exact baseline. The final publication guard and
receiving-ref readback are recorded with the reconciliation commit.
