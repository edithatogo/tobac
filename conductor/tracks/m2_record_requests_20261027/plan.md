# Implementation plan

Status: [x] Bounded decision recording and request preparation/review complete;
publication checks/readback remain mandatory in the PR. Issue #3 stays empirically open.

## A: Selected decisions and preparation
- [x] Record the six owner-selected directions and explicit deferred permissions.
- [x] Prepare metadata-first laboratory requests and contingent survey/supply drafts.
- [x] Preserve source hashes, request IDs and local-unsent status in a manifest.

## B: Review and qualification
- [x] Review each draft, recipient evidence, required fields and sharing boundaries; apply fixes.
- [x] Run full tests, strict_all, reproduction, clean-package and security on macOS Python 3.15.1.
- [x] Verify manifests, Conductor links/titles and absence of send/receipt claims.

## C: Publication
- [x] Commit the preparation and prepare guarded publication; exact-head hosted checks,
  merge and receiving-main outcomes are recorded in the publication PR when executed.

No sending, application, paid work or empirical claim is a completion criterion for
this bounded preparation track. Exact-head and receiving-main evidence is maintained
in the publication PR; it must not be claimed before execution.

## Review fixes and qualification

Registration: ea39e2f. Implementation and reviewed request content: c1e86e5.
File-by-file review clarified acronym definitions, later-analysis field requirements,
public-contact versus custody evidence, and existing summaries versus later analyses.
No sender identity, delivery, restricted access, paid work or new collection is implied.

Local macOS Python 3.15.1: all five Nox sessions passed;981 tests/five capability skips,
92% coverage,zero strict diagnostics and nine native Ruff policy tests passed.
Resource guard:783.0MiB sampled peak,exit0,default4096MiB/2400s.
Direct checks:13 hashes,four unsent drafts,24 unique field rows,local links and14/14
Conductor names. No executable interface,model input,result or security change.
Review:docs/reviews/2026-10-27-m2-record-requests.md.

Publication evidence is a separate mandatory readback,maintained in the PR so local
preparation completion never substitutes for an unexecuted hosted or receiving-main job.
