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
