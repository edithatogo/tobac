# Decision: Merge producer branch `feat/p2-p3-native-lineage-gaps` into `archive-govt-nz/main`

Date: 2026-10-31 (recorded 2026-11-01)
Owner: tobac integration owner; producer owner: archive-govt-nz
Status: **Approved (Option A)**
Conductor track: `conductor/tracks/native_archival_lineage_20261026`

---

## Decision

**Merge branch `feat/p2-p3-native-lineage-gaps` (`89def194`) into `archive-govt-nz/main` now.**

This is the highest-priority decision for the native archival lineage track.

---

## Options Considered

| Option | Description |
|---|---|
| **A (Selected)** — Merge now | Owner approves and merges the PR in `archive-govt-nz`; producer `main` advances, P2.3 output `native-source-refs.json` is produced, and `tobac` Phases 2/3 become unblocked. |
| B — Defer until Phase 5/6 wiring ready | Keep producer branch as-is; advance `tobac` Phase 5/6 against frozen wheel; merge producer later. |
| C — Re-scope producer work | Split branch: merge minimal gap fixes now; defer estate registration and capture-time correction. |

---

## Rationale for Option A

1. **The producer branch is ready and verified.** It passes 20 provenance tests and resolved all 4 probe gaps (duplicate-ID rejection, incomplete receipt, strict-record interop, WARC-Date header).
2. **`tobac` Phases 2/3 are explicitly producer-owned and cannot advance without this merge.** The P2.3 output `integration/archive/native-source-refs.json` is absent; source registration is unconfirmed; capture-time correction remains open.
3. **Every downstream phase depends on it.** Phase 5 runner closure needs native source IDs; Phase 6 qualification wiring needs producer interfaces; Phase 7 recovery needs complete manifests; Phase 8 acceptance needs all prior phases closed.
3. **The producer repo has no conflicting in-flight work.** This branch is its primary active track.
4. **Delaying only compounds the "producer-owned open" gap** in `tobac`'s records; no parallel workstream is waiting on this merge.

---

## Tradeoffs

| Dimension | Option A (Merge now) | Option B (Defer) | Option C (Re-scope) |
|---|---|---|---|
| **Unblocking speed** | Immediate | Slow — Phase 5/6 also open | Partial — estate registration still open |
| **Producer review burden** | One coherent PR | Multiple smaller PRs later | Requires splitting/rewriting history |
| **Risk of stale CI** | Low — branch passes all tests | Medium — producer `main` may drift | Medium — splitting may introduce regressions |
| **Downstream impact** | All `tobac` phases unblocked in sequence | `tobac` stays on frozen wheel | Partial API; still no `native-source-refs.json` |
| **Archival integrity** | Full estate registration + capture-time correction together | Estate registration delayed | Estate registration still deferred |

---

## Contingencies

| If… | Then… |
|---|---|
| **Producer review finds a regression** | Revert the merge in `archive-govt-nz`; `tobac` retains the frozen `79004409` wheel (already qualified). |
| **`archive-govt-nz` owner lacks capacity** | Fall back to Option C: extract and merge only the gap-fix commits (duplicate-ID, WARC-Date, URI scheme, adapters) as a minimal PR; defer estate registration to a tracked follow-up. |
| **`tobac` needs runner wiring before producer is ready** | Proceed with Phase 5/6 against the frozen `79004409` wheel (as was done for MOH/SHINE); re-base when producer merges. |
| **Stakeholder objects to full estate registration** | Document the objection in Conductor; keep Phase 2 open; Phase 4 (already complete) remains valid for the two source-backed operations. |
| **Upstream dependency changes** (e.g., Python 3.15.2, new ruff) | Lock the producer to the current 3.15.1 environment; the reconciliation records exact Python 3.15.1 requirement. |

---

## Next Actions

1. **Producer owner reviews and merges** `archive-govt-nz` PR for `feat/p2-p3-native-lineage-gaps`.
2. After merge, CI on `archive-govt-nz/main` produces the release wheel + `native-source-refs.json`.
3. In `tobac`: run `scripts/derive_native_source_refs.py` to generate `integration/archive/native-source-refs.json`; tick P2.3/P2.4 in plan; proceed to Phase 5.

---

## Affected Conductor Records (to update after merge)

- `conductor/tracks/native_archival_lineage_20261026/metadata.json` — remove `blocked_phases` for 2/3; add `p2_3_output_present: true`, `producer_remaining_tasks: "none (merged)"`.
- `conductor/tracks/native_archival_lineage_20261026/plan.md` — tick P2.3, P2.4, P3.3, P3.4.
- `conductor/tracks.md` — update status line.
- `conductor/index.md` — update track description.

---

## Records

- Decision recorded in Conductor: `docs/decisions/native_lineage_producer_merge_20261031.md`
- Conductor track: `conductor/tracks/native_archival_lineage_20261026`
- Producer branch: `archive-govt-nz feat/p2-p3-native-lineage-gaps` (`89def194`)
- Producer receipts: `integration/archive/p2-phase-verification_20261031.json`, `p3-phase-verification_20261031.json`, `p3.3-verification_20261031.json`
- `tobac` Phase 4 evidence: `integration/archive/shine-native-extraction_20261031.json`, `p4-phase-verification_20261031.json`

---

## Approval

- **Approved by:** [Owner] on 2026-11-01
- **Conductor track:** `native_archival_lineage_20261026`
- **Next Conductor update:** after producer merge completes