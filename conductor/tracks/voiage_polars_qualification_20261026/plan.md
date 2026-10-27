# Implementation plan: Voiage 3.0.0 Polars consumer qualification

All tasks are pending. Planning registration only; implementation is not authorised. Prerequisite: the Voiage tracks are registered but unimplemented, so AC3 cannot start until Voiage 3.0.0 is published.

## Phase 1: Surface freeze

- [ ] T1.1 — Freeze the qualification revision `f55edb1b`, the derivation command and the expected output for AC1.
- [ ] T1.2 — Re-derive the Voiage surface in `src/tobac`, `scripts/` and `tests/engineering/`, and assert that no removed symbol (`dataset`, `to_dataset`, `from_dataset`) is referenced. (AC1).
- [ ] T1.3 — Validate: the inventory matches the recorded digest; the assertion fails if a removed symbol is introduced; record command and exit status. (AC1).

## Phase 2: Baseline re-qualification

- [ ] T2.1 — Freeze the current wheel hash, interpreter, platform and the exact probe and parity commands.
- [ ] T2.2 — Execute the installed Voiage probe and the EVPI parity check on `2.2.0+tobac3151.1`. (AC2).
- [ ] T2.3 — Validate: the receipt records the wheel hash, environment, command, exit status and observed parity; no tolerance is changed to obtain a pass. (AC2).

## Phase 3: Candidate qualification

- [ ] T3.1 — Record whether Voiage 3.0.0 is published; if not, mark the phase blocked rather than pending success.
- [ ] T3.2 — Install the unpatched upstream 3.0.0 wheel and run the same probe and parity check. (AC3).
- [ ] T3.3 — Validate: the receipt proves the unpatched wheel was used; a patched build is labelled as such and is not presented as upstream qualification. (AC3).

## Phase 4: Patch and dependency base

- [ ] T4.1 — Compare Voiage 3.0.0 declared metadata with the current patch's reason for existing; state whether the patch is still required.
- [ ] T4.2 — Retire or retain the metadata-only patch explicitly, and record whether `pandas` remains in tobac's declared set. (AC4, AC5).
- [ ] T4.3 — Validate: the lock receipt is regenerated and reviewed, not hand-edited; no pin is loosened without a recorded reason; the patch decision is evidenced. (AC5).

## Phase 5: Parity and boundary

- [ ] T5.1 — Confirm the `1e-10` tolerances and the reference calculation are unchanged.
- [ ] T5.2 — Run affected component tests and `tests/test_workstream_integration.py`; confirm no scientific or release claim was introduced. (AC6, AC7).
- [ ] T5.3 — Validate: the receipt states exactly what executed and what did not; no hosted job is marked passed unless it ran; no Voiage issue, release or visibility changed. (AC6, AC7).

## Final acceptance

- [ ] CLOSE.1 — Review every AC against the exact tested wheel and revision; list unexecuted external gates explicitly.
- [ ] CLOSE.2 — Record the outcome in `integration/` and update this track's metadata; do not mark complete while AC3 is unexecuted.
