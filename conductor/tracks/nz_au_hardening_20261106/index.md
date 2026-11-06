# NZ/AU repository and analytical hardening

Status: H0 inventoried; H1.1 local corrections/verification are recorded in progress.md;
H2 release/native/empirical gates remain open. Owner: current empirical lane for scoped candidate work;
shared integration/runtime/native GitHub settings retain their existing owners.

- [Specification and acceptance](spec.md)
- [Plan](plan.md)
- [Metadata](metadata.json)
- [Incremental hardening task card](task-card.md)
- [Current execution evidence and dispositions](progress.md)

## H0 evidence and findings — 6 November 2026

Baseline: empirical worktree at 016fd45; receiving main observed at 58a4b2f. The root
renewal owner retains native signing and newer main workflow pins. No dirty source or
private binding was copied. Exact receipts remain in outputs/nz-au-phase0; this is a
bounded baseline inventory, not release or methodological acceptance.

CommonMark inventory covered all 180 tracked Markdown files: 490 links, including 350
local targets. All 21 missing targets are explicitly catalogued local-only authoring
documents in the publication policy. README navigation was corrected without restoring
those files; the subsequent scan has 16 remaining references in historical/technical
documents. HTTP endpoints, anchors, raw HTML, Markdown extensions and rendered navigation
were not tested. Original and subsequent inventories are retained separately.

Live GitHub metadata confirms the existing public visibility, main default branch,
Apache-2.0 licence and research-software description/topics. Issues are enabled; wiki is
disabled; the repository is not archived. No metadata/settings mutation was needed.

The 15-workflow structural inventory found no remote action without a full 40-character
SHA. Write scopes are confined to the named artifact-attestation, dependency-submission,
CodeQL and Scorecard jobs. This observation does not itself qualify those permissions,
remote action contents or hosted runs. Reuse existing security receipts at their recorded
scope and compare the incoming renewal workflow blobs before integration.

The current clean-package receipt verifies approved package members, Apache-2.0/NOTICE,
wheel/sdist-rebuild equality, isolated import/API and quick CLI execution. Publication
security and measured resource receipts already obtained in empirical Phase 0 are reused.

| Finding | Severity / disposition | Owner and allowed files | Focused acceptance |
|---|---|---|---|
| README local-only report links and obsolete active Voiage candidate wording | P2; scoped correction prepared, retaining historical receipt and scientific limits | Empirical lane: README.md | CommonMark local-target scan; current published-wheel receipt; publication-path check |
| Sixteen remaining links to intentionally local-only documents | P2 navigation follow-up; keep authoring bytes private and historical evidence intact | Future H1 scoped document owner | Classify against publication policy; correct labels/destinations without restoring withheld content |
| Older setup examples use bootstrap/unbounded commands | P2; H1 follow-up after final baseline, not release instructions | Empirical lane: README.md / workflow guidance | Match qualified repo-local runtime, hash-sync and bounded Nox/CLI commands; inspect existing receipts |
| Renewed active lineage versus original numerical oracle | P1 acceptance gate; native owner qualifying explicit checkpoint-role checks | Native owner: signed renewal packet | Normal admission, original archive immutability, identical CSV object closure and negative controls |
| Newer receiving-main workflow pins absent from this earlier snapshot | P2 integration dependency; consume qualified immutable owner packet | Existing integrator / native owner | Exact blob/signature readback, relevant workflow/security checks |
| GitHub description/topics/licence/visibility | Informational; consistent, no change | Existing owner; no native writes | Saved exact-target metadata readback |

No branch/issue deletion, visibility change, hook replacement or security weakening was
performed. H2 remains after empirical milestone acceptance.

Executed focused commands use this lane's qualified Python 3.15.1 environments:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv-audit-integrated/bin/python outputs/nz-au-phase0/hardening-link-inventory.py
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv-audit-integrated/bin/python outputs/nz-au-phase0/hardening-link-inventory-after-readme.py
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python scripts/publication_boundary.py index
gh repo view edithatogo/tobac --json nameWithOwner,url,visibility,description,licenseInfo,defaultBranchRef,repositoryTopics,isArchived,hasIssuesEnabled,hasWikiEnabled
```

The one-off link helpers and complete inventories are local execution artifacts, not a new
shared quality framework. Replaying them requires those retained helpers; existing public
publication/package/security tools remain the maintained gates. The staged boundary check
passed at 56.2 MiB sampled peak. No new automated test was added for these document edits.
