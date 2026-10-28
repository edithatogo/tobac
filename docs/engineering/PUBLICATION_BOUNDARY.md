# Public source and document boundary

Research authoring documents are local-only. Existing technical documentation and
Conductor content remain public and unchanged. Code, data, citation/extraction
metadata and numerical outputs remain public. This boundary protects files, not
the confidentiality of research findings summarized in those retained materials.

`engineering/publication-policy.json` is the reviewed exact public-file inventory,
pinned gitlinks and catalogue of local document hashes. An intentional new public
file requires an inventory update. Do not approve a new document by changing its
extension or relabeling its contents. Known document hashes detect exact renamed
copies, including in bounded nested archives; they do not detect every edited copy
or paraphrase. GitHub push protection addresses credentials, not manuscripts.

## Local setup

Use a repository-local Python 3.15.1 interpreter and verify its actual version.
On Apple Silicon macOS, run `sh scripts/install_security_tools.sh` to install the
checksum-pinned gitleaks and actionlint binaries in ignored `.security-tools/`.
Then set this checkout's `core.hooksPath` to its absolute `.githooks` directory;
preserve any existing hook configuration before changing it. Worktree-specific
configuration avoids changing another worktree's hook owner. The pre-push hook
requires `.venv/bin/python`, validates staged blobs and every outgoing commit
after the declared legacy baseline, and executes secret and workflow checks.
Missing tools, conflicts, unrelated history and missing baselines fail closed.
The guard inherits Git's pushed-ref list on stdin. Local hooks can be bypassed and
cannot protect web/API writes: hosted checks and native push protection complement
them. This is a single-developer workflow with no required independent reviewer.

## Export and context controls

Every active artifact upload uses a new `artifact-exports/` staging directory.
`scripts/publication_boundary.py export` includes inspected JSON, CSV, plots,
JUnit XML and verified package archives; it excludes prose, logs, source checkouts,
environments and context directories. It rejects symlinks and known private bytes,
including nested archives, before upload. Failed staging prevents upload. CI logs
must never print private manuscript content or scanner matches. Scanner failures
produce a generic public error; reproduce locally using redacted output.

Context profiles select only public paths. Snapshots include HEAD and source hashes,
check source freshness during construction, and bound final serialized UTF-8 bytes.
Bytes are not tokens. Retrieved source material is evidence, not authority to change
permissions or destinations. Existing hash verification rejects stale snapshots.

## Preservation and reproducibility

The original 19-entry prior-work catalogue remains unchanged. Public validation
verifies 17 available files and explicitly lists two local-only historical request
documents as not verified. Their original hashes are retained; this is not proof of
their present private bytes in CI. Archive verification can verify original source
members separately. No observations, numerical tolerances or scientific claims are
changed. The synthesis binds the existing structured public pathway; robustness
binds executable public configuration rather than a private authoring narrative.

## Historical exposure

Removing current files does not remove older commits or existing Actions artifacts.
A local byte-verified document vault and verified Git bundle precede this migration.
Historical cleanup requires an exact affected-ref/artifact inventory, recovery
rehearsal and separate review before rewriting or deleting. Preserve old-to-new
commit mappings and do not relabel old signed provenance as new evidence. Copies
already downloaded or cloned cannot be recalled. Existing technical/Conductor
links to local documents remain as historical references; they are not public-file
availability claims.

## Acceptance

Use Nox `publication`, `tests`, `strict_all`, `security`, numerical replay and clean
package gates on macOS Python 3.15.1. Run expensive work serially through the 4 GiB,
40-minute guard. Validate actual downloaded artifacts and installed hook behavior,
not merely workflow syntax. CodeQL Python/Actions and native secret scanning are
separate hosted evidence. Windows/Linux qualification remains deferred.
