# Review Report: Native archival lineage record reconciliation

Date: 31 October 2026. Base: `69ab2a2` (`origin/main`).

## Purpose

The track's plan, metadata and `tracks.md` disagreed about which phases were
complete, and a diverged local `main` claimed a completion the evidence does not
support. This change makes the records match the executed evidence. It changes no
software, scientific value, model input or dataset.

## What the evidence supports

| Phase | Disposition | Basis |
|---|---|---|
| 1 | complete | inventory, capability map, ownership baselines |
| 2 | producer-owned, open | receipts verify producer branch `feat/p2-p3-native-lineage-gaps`; producer-main merge, full estate registration and capture-time correction unconfirmed; `integration/archive/native-source-refs.json` absent |
| 3 | producer-owned, open | same producer branch; closure traced only in that branch |
| 4 | complete | MOH + SHINE source-backed operations with native CAS/strict records (`d2a04f5`) |
| 5 | partial | six runner interfaces defined with `exploratory` binding, not executed closure |
| 6 | partial | ten qualification tests pass, but `scripts/qualification_check.py` is not referenced by `noxfile.py` or any workflow, so checks are not wired into qualified paths |
| 7 | partial | same-device recovery rehearsal only; independent-copy recovery not demonstrated |
| 8 | open | no acceptance evidence present; no AC fully verified |

`native_lineage_qualified` and `scientific_qualification` remain **false**.

## Diverged local main

`codex/diverged-local-main-20261031` (`8e63c85`) claimed `phase1-8_complete` and an
AC13 independent-copy restore against `integration/archive/ac13-recovery-receipt.json`.
That file does not exist in any branch or commit; commit `4d0bdd6` changed only
bookkeeping and cited the missing receipt. The line also carries superseded
`migrate_datasets.py` / `qualify_shine_table.py` versions. It is archived (bundle and
patches in private storage) and **not merged**.

## Not reconciled here (external, empirical or owner decisions)

- Voiage 3.0.0 published-release acceptance (upstream release unavailable).
- Managed dependency-graph parser Python 3.15 support and package-to-package edges.
- Issue #3 empirical/data/governance requirements (`conductor/research-gates.md`).
- non-macOS release/audit qualification (deferred roadmap work).
- Renovate PRs #80 and #91, which force Python 3.15.2 against the exact 3.15.1 pin.

These require external releases, data, human decisions or re-qualification. They are
recorded, not claimed.

## Scope

Documentation and receipt only. No `src/`, `tests/`, lock, workflow or scientific
artifact changed.
