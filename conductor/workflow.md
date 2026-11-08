# Shared workflow

1. Read the current base, AGENTS.md and affected scientific contracts. State the intended scope.
2. Choose a bounded context profile; record commit, source hashes and dirty state. Do not ingest
   all prior archives. A changed HEAD or source invalidates a prior context receipt.
3. Write the scientific/engineering scope and tests. Compare an existing library before new
   generic code. Preserve reference oracles, input units, shared identities and data-once rules.
4. Execute affected and cross-workstream tests. On a complete checkout run full test/reproduction
   sessions. Record unavailable checks without substituting a mock or self-authored receipt.
5. Self-review diffs, assumptions, failure cases and actual commands. Keep empirical calibration,
   metadata, software and security gates apart. Independent review is optional and is not a gate.
6. Re-read current main, reconcile any changes, then use guarded publication and verify remote
   readback. Never force-update or weaken CI to get green.

The pinned vendor/conductor submodule is upstream tooling, not these project plans. Its host
checkout/activation must be verified separately. No automatic background worker is installed.

## Manuscript checkpoint

Use the existing paper records and the [open research gates](research-gates.md). Keep a
versioned, source-linked contract for each paper. Preserve original and co-author feedback,
its disposition and rationale, the research question, estimands and protocol chronology.
Verify the journal and article type against current official instructions and record the
source and check date. Record panel counting, formatting exceptions, declarations and
submission files. Keep unknown portal requirements open and mark the graphical abstract
required, optional or unconfirmed. Maintain separate inventories for analysis production,
main text, supplement and workbook, with exact editions or explicit non-applicability.

Before revising prose, record named subgroup display priorities, the rationale and results
already seen. Apply analytic support and privacy rules separately. Distinguish descriptive
comparisons from supported effect modification and retain unsupported or suppressed
dispositions. Preserve all reportable results in the supplement or workbook. Select displays
without using significance. Record where subgroup or causal analysis does not apply.

For headline and material causal or subgroup claims, register exact wording, the estimand
and population, frozen source and row, assumptions, diagnostics, sensitivity results,
limitations, permitted wording, downgrade or withdrawal triggers and final locations.
Retain null and conflicting findings. Compare studies by design, estimand and population.
If source or identification checks fail, downgrade or withdraw the affected claim and
retain supported descriptive results. Record a question-driven protocol amendment before
adding methods.

Record the exact edition reviewed, reviewer name, role and date for the applicable
scientific, methods, domain and reporting reviews. Roles may overlap. Record unresolved
objections, distinguish claim blockers from permissible limitations, and state the
accepted, conditional or no-go outcome. Keep pending roles explicit and attribute decisions
only to actual reviewers. A successful run or checklist is software or reporting evidence.
Author approval and authority to submit or publish are separate decisions.

### DOCX delivery validation

List every final paper and supplement DOCX in the delivery inventory, including clean,
tracked, review and journal variants. After the last save, metadata scrub, Word Compare
or packaging edit, follow the maintained
[manuscript DOCX delivery skill](/Users/doughnut/.codex/skills/manuscript-docx-delivery/SKILL.md).
Run its read-only validator with a new receipt path and the explicit final file list,
or use a qualified repository equivalent.

Require zero errors for ZIP integrity and CRC, XML parsing, internal relationships,
and Microsoft Open XML SDK schema and semantic validation. Keep the diagnostics, tool
and runtime versions, and SHA-256 for each file. Match the receipt hashes to the final
files before delivery. Reuse valid receipts for identical bytes and repeat validation
after any byte change. Missing tools, missing or stale receipts, exceptions and validation
errors block delivery. Preserve failed evidence and repair a versioned copy.

Verify content and property fidelity, fields, comments, revisions and repeating table
headers separately. Review the rendering of every page and retain any required native
Word save, reopen or Compare evidence. Scientific acceptance, privacy, author approval
and submission authority retain their own gates.

## Actions pinning decision — 26 October 2026

Retain full 40-character commit-SHA references for external GitHub Actions and
reusable workflows. The generated tag-based Actions-lock proposal is rejected and
closed; do not trade these immutable references for mutable tags to adopt a lockfile.
Version updates remain reviewable changes to full-SHA references. Existing security
checks, dependency locks, audits and failure policies remain required.
