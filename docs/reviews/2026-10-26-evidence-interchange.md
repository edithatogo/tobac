# Evidence interchange review — 26 October 2026

Scope: the remaining C3/C4/C6 domain transport in scientific_ecosystem_20261025.
Self-review follows conductor-review under the single-developer repository policy;
no independent scientific review is implied. The owner authorized iterative
review and fixes autonomously, including changes above the skill's 300-line size.

Reviewed boundaries: exact Arrow column types/order, mandatory canonical nested
metadata, preservation of Scope/EvidencePacket and SupplyBasis semantics, finite
SPD covariance provenance, explicit UTC/null capture time, no implicit casts,
state-order integrity, data-once conditioning, caller buffer isolation,
Arrow/C-stream/Polars ownership, logical versus physical hashes, unsupported
version rejection and retained IPC rollback. The existing conditioning and M3
producer implementations are reused without edits.

Findings addressed during implementation:

- Polars loses Arrow metadata: require a byte sidecar and validate on restoration.
- Unknown/duplicate/noncanonical metadata could hide drift: closed msgspec structs
  and canonical re-encoding comparison reject it.
- A bare dtype-compatible table could carry incompatible supply provenance:
  reconstruct SupplyBasis and require matching source unit/geography.
- Whole-table zero-copy would overstate the measurement: claim only the tested
  float64 view; record positive Arrow allocation deltas and other-allocator limits.
- Sliced Arrow chunks can rebase buffer pointers: compare effective data
  addresses including element offsets, rather than base pointers alone.
- A future unpublished producer was unnecessarily blocking the original domain
  boundary: use the existing hash-qualified installed producer; preserve PR #41.
- Other work merged dependency updates during implementation: merge current main
  and genuinely regenerate all four input-bound locks, retaining both updates.

Remaining external gate: the managed root Dependabot parser's Python 3.15 support.
The supported dependency snapshot submission remains required and unchanged.
Final executable evidence and publication refs are recorded in the track plan
and integration/ecosystem/interchange_20261026.json after qualification.
