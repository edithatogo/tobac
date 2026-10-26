# Native GitHub Dependency Graph manifest discovery

The managed `Dependency Graph` job failed in `/engineering` while evaluating
`-r ../requirements.lock`: the referenced file was absent from its temporary
checkout. The inspected upstream Dependabot fetcher follows requirements includes
ending in `.txt` or `.in`; it does not fetch the custom `.lock` filename.
Original observed failure: run `40272768074` (also present on earlier main revisions).

The canonical version list now lives in `engineering/reference-requirements.txt`.
`engineering/requirements.in` includes it directly. The root `requirements.lock`
remains a compatibility include for existing install commands, so there is one
source of version pins. The canonical file preserves the previous version list
byte-for-byte. Runtime/audit/Voiage hash locks are regenerated and input-bound to
the canonical file; all 29/91/49 resolved version entries remain unchanged.

This changes manifest discovery, not the Python runtime or security policy.
`.python-version`, package constraints, Nox interpreters, CI jobs and native build
selection remain Python 3.15.1. GitHub's own metadata-parser implementation runtime
is service-owned; its static scan is not a project build/test qualification.
Dependency Graph, vulnerability alerts, security audits and repository settings
are not disabled or relaxed. No failing job becomes optional or ignored.

Regression checks verify native-compatible include closure for all three profiles,
compatibility of the legacy entrypoint, unique pins and consistency with the
package's runtime dependencies. Lock tests cover the new input's hash binding.
These local contract tests do not substitute for native execution. The managed
job must actually succeed after a default-branch manifest publication; its run,
receiving commit and graph readback are recorded in
`integration/dependency_graph_20261026.json`.

Upstream implementation inspected:
https://github.com/dependabot/dependabot-core/blob/main/python/lib/dependabot/python/shared_file_fetcher.rb

## Verified publication

PR #35 passed all 15 checks before merging at `666dd8c`. The genuine managed
`update-pip-graph` job passed in run `40275206942`. Native SBOM export increased
from 27 to 42 package identifiers, adding the missing reference and Voiage
dependencies while retaining all previous entries. Repository visibility and
security settings were read back unchanged. The hosted macOS full suite passed
731 tests with four optional-environment skips at 93% coverage.

## Root parser boundary and supported submission — 26 October 2026

After PR #43 changed package metadata, the service also attempted the root pyproject.
Run 40316535031 rejected `>=3.15.1,<3.16`: its service-owned Python manager currently
supports only through 3.14. This is a genuine managed-service limitation, distinct from
the earlier engineering include-closure repair. Upstream issue:
https://github.com/dependabot/dependabot-core/issues/16524.

The project requirement stays Python 3.15.1. No constraint is loosened, manifest hidden,
security setting disabled, or failing managed job reclassified as successful.
The existing graph remains readable. GitHub's supported dependency-submission API supplies
an additive route for resolved dependencies while the managed parser limitation remains open:
https://docs.github.com/en/rest/dependency-graph/dependency-submission.

`scripts/dependency_snapshot.py` checks its actual interpreter, exact checkout SHA,
all four lock receipts and each lock's committed bytes. It emits every resolved package
as an exact PURL, with lock hash and source identity. Unknown dependency edges, directness
and runtime/development scope are omitted rather than invented. This is a complete resolved
profile inventory, not an installed-import or scientific qualification claim.

The trusted macOS job hash-syncs the reference environment, creates a new snapshot, submits
through the supported API and retains the response. Contents write is scoped to that job
because GitHub requires it for this endpoint; no checkout credential persistence or repository
settings writes are introduced. All existing audits, graph jobs and alerts remain intact.
Actual API acceptance and default-branch SBOM readback must be verified independently.

Native default-branch closeout: PR #44 merged at 0940c595ce06f4142467de3f687dea881dae8ea2. Snapshot 114186314 returned SUCCESS. Native export contains all 113 submitted PURLs among 123 total, with every prior PURL retained. Visible repository/security settings are unchanged. Receipt: integration/ecosystem/dependency-submission_20261026.json. The managed parser's unsupported-runtime failure remains an upstream gate.
