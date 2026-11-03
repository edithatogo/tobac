# DCI1 advisory additions and pins — 3 November 2026

DCI1 selects one bounded differential type-diagnostics experiment with ty and
Pyrefly, plus a Linux ARM64 diagnostic leg. Existing BasedPyright remains the
required type gate. DCI2–DCI4 remain deferred; this selection does not install,
execute or qualify the proposed lane. Base: `683089140f34afb8ebfd8c4686705b4ae7a67378`.

[Machine-readable selection](selection_20261103.json) records exact tag/ref
reads, expected wheel digests, active baseline actions and file hashes. A registry
digest is an expected download identity, not proof that an archive was downloaded,
installed or built from the recorded source commit.

## Selected additions

| Addition | Candidate pin | Gap addressed |
| --- | --- | --- |
| ty CLI | `ty==0.0.95`; source `48c5ea1baf6144dc9918ae60040aaa4198b251ce` | Independent type-system/parser diagnostics over `src` and `scripts`, compared with the existing BasedPyright result. |
| Pyrefly CLI | `pyrefly==1.4.0`; canonical source `meta/pyrefly@feeee254e65844f23f973a0a29cae02d09931068` | A second implementation within the same comparison experiment, so unique findings, overlaps and stub gaps can be measured rather than assumed. |
| Linux ARM64 diagnostic delivery | `ubuntu-24.04-arm` | OS/architecture coverage absent from the existing macOS ARM64 and Linux/Windows x64 evidence. Static diagnostics and tool delivery only; no scientific runner or release qualification. |

The comparison runs on `macos-latest`, `ubuntu-latest` and
`ubuntu-24.04-arm`. Start with read-only, non-required pull-request/manual jobs;
no schedule, automatic promotion or additional action wrapper is selected.
DCI3 must report actionable unique findings versus overlap/false positives. If the
two checkers add no useful information, retain that result and reduce/defer the
experiment rather than treating tool accumulation as an improvement.

Ty 0.0.96 was published today and is below the existing three-day release-age
policy. Ty 0.0.95 and Pyrefly 1.4.0 are the newest non-yanked stable PyPI candidates
observed beyond that age threshold. GitHub tags were resolved to commit objects;
the former facebook/Pyrefly alias resolves to the canonical meta repository.
Published wheels exist for macOS ARM64 and glibc Linux x86_64/ARM64. Their metadata
allows Python >=3.8, which does **not** establish Python 3.15.1 parser or runtime
compatibility. Exact pinned CLI behavior remains to be exercised.

Current `engineering/ecosystem.in`/locks remain untouched, including ty 0.0.94,
Pyrefly 1.4.0 and prek 0.5.7. The selected ty 0.0.95 is a future isolated-lane pin,
not a replacement for the current ecosystem or scientific reference environment.

## Omitted duplicate additions

| Original proposal | Decision |
| --- | --- |
| ruff-action | Existing Nox Ruff ALL, format and preview checks cover the responsibility. Omit another wrapper/version source. |
| zizmor-action | Retain existing pinned offline/pedantic CLI checks. |
| gh-action-pip-audit | Retain source-bound strict audit/SBOM generation; no advisory downgrade or second audit wrapper. |
| gitleaks action | Reuse the checksum-pinned CLI and full-history/export guards. |
| attest-build-provenance | Existing main package/SBOM attestation already covers the selected responsibility. No new OIDC/attestation job. |
| harden-runner expansion | Keep the existing audit job and pin unchanged; no new egress block policy or broad rollout. |
| prek/prek-action | Dated prek 0.5.7 hook execution already exists, and current pre-commit/publication hooks remain owned. No measured gap justifies migration or duplicate CI. Latest observed prek 0.5.9 is catalogued only. |

All original proposal refs were re-read, including newer excluded releases.
Those observations do not update any active action or dependency. The active
attestation commit remains its existing immutable SHA even though it differs
from the latest release tag read; no tag-based rollback is inferred.
Renovate's separate action-update PR and existing full-SHA policy remain intact.

## DCI2 implementation packet

1. Use Nox, with a proposed `advisory_types` session and an isolated
   `engineering/advisory.in`/`advisory.lock`/paired receipt. Reuse canonical
   reference dependency and stub/interface declarations; qualify required import
   resolution explicitly. Extend the existing source-bound lock helper for this
   isolated profile while preserving the existing four-profile manual matrix.
   None of the four current locks is replaced or mutated by an advisory run.
2. Select/assert repo-local Python 3.15.1 before execution. Configure ty's syntax
   target as 3.15 and Pyrefly's version as 3.15.1 with the selected interpreter.
   Current docs describe explicit environment/version controls; inspect each
   pinned binary's real `--help` before adopting arguments.
3. Preserve original exit codes, complete structured output, tool versions,
   source/config/environment hashes, exact commands, counts and classification of
   overlap/unique/stub-gap findings. Known report-bearing diagnostics are advisory.
   Unsupported syntax/Python, missing required imports/dependencies, missing or
   malformed reports, crashes and budget breaches fail execution. Never use
   blanket `continue-on-error`, exit-zero flags, suppressions, automatic baselines
   or code rewrites to manufacture a clean result.
4. Keep 4 GiB sampled group RSS and a 40-minute ceiling, heavyweight commands
   serial per job, and zero retries. Export only inspected numerical/diagnostic
   receipts through the existing publication boundary. Do not upload source
   checkouts or private original material.
5. Extend the existing scanner installer for Linux/aarch64. Publisher ARM64
   Gitleaks 8.30.1 and Actionlint 1.7.12 archives/checksums exist and their expected
   digests are recorded in the selection JSON. No archive was downloaded or
   executed in DCI1. ARM export stays blocked until checksum and native execution
   verification pass; do not skip scanners to obtain a green leg.
6. New workflow/Nox bytes require the existing orchestration capsule renewal with
   all eight original native attempts reopened. Preserve frozen verifier profiles,
   scientific inputs and required commands. Static ARM diagnostics do not authorize
   scientific execution on an unqualified ARM verifier.

## DCI3 qualification and DCI4 publication

Run actual pinned version/help checks, Python 3.15 syntax (including lazy-import)
fixtures, known-good/known-bad/crash cases, required import resolution, report/exit
handling, bounded execution and inspected export on each selected host. Record
allocation/library limitations and every unexecuted job. A documented public
runner label is not proof of allocation or repository-specific entitlement.

Keep BasedPyright/strict_all, scientific reproduction, package/security, native
lineage, ordinary Git hooks and branch checks unchanged. DCI4 publishes the
implemented, qualified lane with an expected-head/non-force fast-forward and
receiving-ref/file readback. Publishing this selection packet does not close DCI4.

## Reconciled historical preparation

The original red strict diagnostics are dated evidence; current reference and
DXP1–DXP4 receipts establish the later passing scope. Issue #4 is closed. The
repository is currently public, so old private-entitlement assumptions are not a
current DCI1 blocker. Prior import-scoped ty 0.0.92/Pyrefly 1.4.0 and prek 0.5.7
hook runs in `integration/ecosystem/verification_20261026.json` do not qualify
the selected versions, full source scope or Linux ARM leg. Original proposal,
dirty-lock notes and gates remain preserved as historical metadata.

## Primary sources

- [Ty CLI/environment/version controls](https://docs.astral.sh/ty/reference/cli/) and [exit codes](https://docs.astral.sh/ty/reference/exit-codes/).
- [Pyrefly configuration](https://pyrefly.org/en/docs/configuration/).
- [GitHub runner labels and public-runner scope](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).
- [Ty 0.0.95 registry metadata](https://pypi.org/pypi/ty/0.0.95/json) and [Pyrefly 1.4.0 metadata](https://pypi.org/pypi/pyrefly/1.4.0/json).
- Exact upstream commit URLs and expected wheel/scanner hashes are retained in the selection JSON. Active workflow, hook, Nox and lock declarations were inspected locally at the recorded base.
