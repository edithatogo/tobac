# Dependency maintenance

Renovate is the sole dependency-update PR provider for this repository. The
existing GitHub App owns Dependency Dashboard #7 and produced the reviewed
maintenance PRs, including Polars 2 in PR #48. No Dependabot version-update
configuration exists; Dependabot security-update PRs were already disabled when
this policy was inspected. This change does not introduce a second updater.

`renovate.json` explicitly enables Renovate and its dashboard. Default manager
patterns remain intact; additional pip-requirements patterns cover the four
`engineering/{requirements,audit,voiage,ecosystem}.in` profiles. Compatibility-
sensitive evidence-transport dependencies share a qualification group. Generated
hash locks are resolver artifacts, not manifests to edit by string replacement.

After dependency-input changes, generate and inspect all four locks with
`scripts/lock_receipt.py`, retaining the paired receipts. The manual
`Reviewable dependency-lock candidates` workflow now creates runtime, audit,
Voiage and ecosystem candidates and asserts its actual Python 3.15.1 interpreter.
It has read-only repository permissions and uploads candidates; it does not push,
adopt or merge them. Source-bound verification must still pass before installation.

Automatic merging remains off. Scientific updates, native producer compatibility,
release-age controls, full-SHA Action pins, all existing tests, strict typing,
reproduction, security audits and artifact provenance remain review/verification
requirements. Runtime candidates advertised in the dashboard are not qualified
runtime upgrades. The current qualified Python remains 3.15.1.

## GitHub graph parsing is separate from update PRs

GitHub internally runs Dependabot graph jobs for Python whenever its dependency
graph is enabled. Choosing Renovate does not replace that service. Disabling the
graph to remove the Dependabot name would also remove a security capability and
is not part of this maintenance policy.

Keep the existing trusted, hash-verified dependency-submission job and native graph
readback. The managed parser's Python 3.15 limitation remains an explicit external
Conductor gate; it is not called successful or hidden. GitHub's existing vulnerability
alerts were disabled at inspection, so no claim is made that Renovate vulnerability-
alert PRs are operational. Existing pip-audit and other security gates remain in force;
no repository security or visibility setting is changed here.

## Implementation boundaries

The accepted macOS engineering scope and Polars 2 transport are implemented.
This does not mean every research objective is implemented or empirically qualified.
`conductor/research-gates.md` retains the real decision target, source conflicts,
unit conversions, shared-observation covariance, transport, calibration, governance,
costs, wider method applicability and native archival recovery requirements.
`conductor/roadmap.md` retains deferred work. PR #41 merged bounded macOS baseline
and exact unreleased-candidate consumer qualification; published Voiage 3.0.0
acceptance remains a separate external release gate.

Sources: https://docs.renovatebot.com/modules/manager/pip_requirements/ and
https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph-data.

## Managed-service recheck — 28 October 2026

At reviewed main 1df7680 (PR #60), supported snapshot 115181647 returned SUCCESS.
All 113 submitted locked package identifiers appear in the current 124-PURL native
export. This establishes inventory coverage of the submitted profiles, not unknown
dependency edges, active vulnerability alerts or root managed-parser support.
The first export request timed out server-side; one repeat of the same read-only
endpoint succeeded. Both observations are retained in the recheck receipt.

Latest observed root-inclusive managed run 40446023419 failed on historical head
4ebc4af, rejecting the unchanged >=3.15.1,<3.16 constraint. No fresh current-head
root job is claimed. Upstream PR #16525 is open and out of draft; pinned upstream
main lists through 3.14.9, while the unmerged candidate lists 3.15.2. A source
change or candidate version is not proof of deployed service support or project
qualification on a different patch. The project stays on qualified Python 3.15.1.

[Recheck evidence](../../integration/ecosystem/managed-parser-recheck_20261028.json)
records exact revisions, hashes and closure conditions. The track remains externally
blocked. No old graph-writing run is replayed against obsolete sources, no manifest
is hidden, no runtime constraint is lowered, and no security setting is changed.
