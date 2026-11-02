# Decision: Sequencing Phase 5 (runner integration) and Phase 6 (qualification wiring) relative to producer merge

## Reconciliation — 2 November 2026

Status: **superseded historical proposal**. This document was an untracked draft
when the implemented track closed. Its original approval placeholder supplies no
verified approval. The retained text below records the proposal, assumptions and
estimated next steps as written; those statements do not describe current status
or authorize a new operation. Original draft digests are retained in
[integration reconciliation](../../integration/reconciliation_20261102.json).

Phases 5 and 6 are complete against qualified native producer contracts and
actual registered source identities. Placeholder source IDs and the proposed
`79004409` wheel/rebase are no longer pending work. The implemented route uses
`scripts/scientific_lineage.py`, `scripts/lineage_preflight.py`, and the qualified
Nox/runner commands. [Phase 5](../../integration/archive/scientific-lineage-checkpoint_20261102.json)
traces all 140 outputs from eight runners to their originals and tests changed-source
impact. [Phase 6](../../integration/archive/qualified-command-enforcement_20261102.json)
proves valid-input acceptance and rejection before launch for missing, stale and
tampered inputs. The draft's timing estimates and placeholder-interface assumptions
were proposals, not executed acceptance evidence.

[Final acceptance](../../integration/archive/p8-final-acceptance_20261102.json)
closes all eight phases for the declared current runner closure, with producer
`c76d78df` and consumer implementation `14303e4` received. Scientific qualification
remains separate. See [current status](../../conductor/status.md).

## Historical draft — superseded

Date: 2026-11-01
Owner: tobac integration owner
Conductor track: `conductor/tracks/native_archival_lineage_20261026`

---

## Decision Required

How to sequence Phase 5 (runner provenance integration) and Phase 6 (qualification enforcement wiring) relative to the producer-main merge.

---

## Options

| Option | Description |
|---|---|
| **A (Recommended)** — Start Phase 5/6 against frozen wheel now, re-base on producer merge | Begin Phase 5 runner integration and Phase 6 qualification wiring immediately against the current frozen `archive-govt-nz` 0.1.0 wheel (`79004409`). When producer merges, re-base the work onto the new wheel and native source IDs. |
| **B** — Wait for producer merge, then do Phase 5/6 | Pause Phase 5/6 until `archive-govt-nz` merges and publishes the new wheel with native source IDs. Phase 5/6 then use actual native source IDs from the start. |
| **C** — Do Phase 6 now, Phase 5 after merge | Wire qualification enforcement (P6) now against frozen wheel; defer Phase 5 runner integration until after producer merge so runner bindings use real native source IDs from the start. |
| **D** — Parallel tracks | Split into two workstreams: one team/person does Phase 5/6 against frozen wheel; another prepares the producer merge and re-base plan. |

---

## Recommendation: **Option A**

**Rationale:**

1. **No new blocker:** The current frozen wheel (`79004409`, SHA-256 `206e6474...`) is already qualified for MOH and SHINE native operations. Phase 5/6 work *can* proceed against it — it was used for MOH/SHINE extraction and the P6 enforcement tests already pass.
2. **Re-base is routine, not rework:** The Phase 5/6 contracts (`runner_provenance.py`, `qualification_check.py`) bind through producer interfaces. When the new producer wheel arrives, the re-base is a controlled wheel swap + source-ID remapping, not a redesign.
3. **Time to value:** Phase 5 (runner interfaces) and Phase 6 (qualification wiring) are the *longest-pole* implementation tasks remaining. Starting them now gains weeks/months of parallel progress.
3. **Producer merge timing is uncertain.** Waiting (Option B) surrenders agency to an external owner's timeline. Option A keeps `tobac` moving.
4. **Re-base scope is bounded.** The Phase 5 interface contracts (`runner_provenance.py`) already use abstract `NativeRecords`/`NativeStore` protocols. Phase 6 (`qualification_check.py`) validates presence of required records. The new producer wheel will expose the same protocols with native source IDs populated — the contract signatures don't change.
4. **Risk mitigation:** If producer merge delays, `tobac` has a working Phase 5/6 on the frozen wheel that can be demonstrated and reviewed. If producer merge accelerates, the re-base is a short branch.

---

## Tradeoffs

| Dimension | Option A (Start now, re-base) | Option B (Wait) | Option C (P6 now, P5 later) | Option D (Parallel) |
|---|---|---|---|---|
| **Calendar time to Phase 5/6 done** | Shortest — starts immediately | Longest — blocked on external | Medium — P5 blocked | Medium — requires coordination |
| **Engineering risk** | Low — re-base is a wheel swap | None — no rework | Low — P5 uses real IDs | Medium — coordination overhead |
| **Re-base scope** | Bounded: wheel swap + ID remapping | None | P5 only | Both tracks |
| **Reviewability** | Two clean diffs (pre-merge, re-base) | One diff (but delayed) | Two diffs | Three diffs + merge |
| **Producer owner dependency** | None for Phase 5/6 start | Full | Partial (P5) | Partial (P5) |

---

## Contingencies

| If… | Then… |
|---|---|
| **Producer merge arrives while Phase 5/6 in progress** | Pause Phase 5/6, do the re-base (1-2 day task: wheel swap, update source IDs in `runner_provenance.py` bindings, re-run tests), resume. |
| **Producer merge never arrives (owner delay)** | Phase 5/6 on frozen wheel is the long-term state. Document that native source IDs are placeholder (e.g., `tobac-placeholder-...`) and will remap when producer arrives. |
| **Re-base reveals interface mismatch** | Roll back to frozen wheel, patch the interface in Phase 5/6 code, re-test. The `NativeRecords`/`NativeStore` protocols are versioned; mismatch would be a producer breaking change, caught by existing tests. |
| **Producer merge adds new required fields** | Extend Phase 5/6 bindings incrementally; the protocols are extensible. |
| **New producer wheel fails CI** | Revert to frozen wheel; Phase 5/6 continue on frozen wheel until producer is stable. |

---

## Next Actions (if Option A approved)

1. **Phase 5:** Implement runner bindings for M1, M2, M2-publication, M2-robustness, longitudinal, M3 in `scripts/runner_provenance.py` using current frozen wheel. Use placeholder native source IDs (`tobac-placeholder-...`) with a clear remapping plan.
2. **Phase 6:** Wire `scripts/qualification_check.py` into `noxfile.py` (new `qualification` session) and `.github/workflows/engineering.yml` (gate). Use frozen wheel for validation.
3. **When producer merges:** Create re-base branch, swap wheel, remap placeholder source IDs → actual native source IDs from `native-source-refs.json`, re-run Phase 5/6 tests, merge.

---

## Affected Conductor Records

- `conductor/tracks/native_archival_lineage_20261026/plan.md` — note Phase 5/6 started on frozen wheel, re-base after producer merge.
- `conductor/tracks/native_archival_lineage_20261026/metadata.json` — add `phase5_started_on_frozen_wheel: true`, `rebase_planned: true`.
- `conductor/tracks.md` — update status line.

---

## Records

- Conductor track: `conductor/tracks/native_archival_lineage_20261026`
- Phase 5 receipt: `integration/archive/p5-phase-verification_20261031.json`
- Phase 6 receipt: `integration/archive/p6-phase-verification_20261031.json`
- Frozen producer wheel: `archive-govt-nz` 0.1.0, `79004409`, SHA-256 `206e6474d155a6e0f7e0b6f70b5b59747fda473b8643193dc2a580bb7e98c640`

---

## Original draft approval placeholder — unverified

- **Original unverified placeholder:** [Owner] on 2026-11-01
- **Conductor track:** `native_archival_lineage_20261026`
- **Next Conductor update:** after Phase 5/6 initial pass complete
