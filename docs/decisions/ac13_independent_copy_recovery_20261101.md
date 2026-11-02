# Decision: Independent-copy recovery for AC13 (P7.3) — USB external drive

## Reconciliation — 2 November 2026

Status: **superseded historical proposal**. This document was an untracked draft
when the implemented track closed. Its original approval placeholder supplies no
verified approval. The retained text below records the proposal, assumptions and
estimated next steps as written; those statements do not describe current status
or authorize a new operation. Original draft digests are retained in
[integration reconciliation](../../integration/reconciliation_20261102.json).

The USB independent-copy route was executed and byte-verified for the full
declared closure of 1,680 files / 257,432,397 bytes. The draft's approximate
50 MB / nine-object scope and wheel are superseded. No formatting of media is
required by this reconciliation. [Actual recovery receipt](../../integration/archive/ac13-recovery-receipt.json)
records the physical copy, restore and checks. All eight installed scientific
runners replayed offline. P7.1–P7.4 and AC13 are complete for that closure.

[Final acceptance](../../integration/archive/p8-final-acceptance_20261102.json)
closes all eight phases for the declared current runner closure, with producer
`c76d78df` and consumer implementation `14303e4` received. Scientific qualification
remains separate. See [current status](../../conductor/status.md).

## Historical draft — superseded

Date: 2026-11-01
Owner: tobac integration owner
Conductor track: `conductor/tracks/native_archival_lineage_20261026`

---

## Decision

**Execute the independent-copy recovery using a USB external drive (Option A).**

This satisfies AC13 ("A rights-appropriate second-copy recovery of the declared closure succeeds with byte verification") and is the only acceptance criterion that can be fully verified without external releases, empirical data, or human decisions.

---

## Options Considered

| Option | Description |
|---|---|
| **A (Selected)** — USB external drive | Copy the full native closure to a physically distinct USB drive, then restore and verify on a clean host directory. |
| B — Network share / NAS | Copy to a network-mounted share or NAS, then restore. |
| C — Cloud object storage (S3/GCS/Azure Blob) | Upload to a cloud bucket with versioning, then download to a clean host. |
| D — Separate host (CI runner or another machine) | Spin up a fresh macOS runner or another Mac, SCP the closure, restore. |
| E — Defer / mark AC13 as "not demonstrated" | Keep AC13 as "not demonstrated"; Phase 7/8 remain partial. |

---

## Rationale for Option A

1. **Meets AC13's core requirement** — "separate failure domain" is satisfied by a physically distinct USB drive (disk failure, controller failure, filesystem corruption are independent from internal SSD).
2. **Lowest friction** — No network configuration, cloud credentials, CI runner setup, or second machine needed. Executable locally in ~30 minutes with the existing closure.
3. **Reproducible and auditable** — The USB drive can be physically labelled, stored, and re-verified later. The process is fully documented in the receipt.
3. **Meets AC13's evidence bar** — The criterion requires "A rights-appropriate second-copy recovery of the declared closure succeeds with byte verification; inaccessible or unqualified destinations remain open gates." USB satisfies "rights-appropriate" (no upload/consent needed) and "byte verification" (CAS hashes verified on restore).
4. **Unblocks Phase 8** — AC13 is the only criterion that currently has a path to "verified" without external releases or human decisions. Completing it moves the track from "all partial" to "one verified, rest partial" — a meaningful milestone.

---

## Tradeoffs

| Dimension | Option A (USB) | Option B (NAS) | Option C (Cloud) | Option D (Separate host) | Option E (Defer) |
|---|---|---|---|---|---|
| **Meets "separate failure domain"** | ✅ (disk/controller) | ✅ (network + storage) | ✅ (provider + network + geo) | ✅ (hardware + OS) | ❌ |
| **Execution time** | ~30 min | ~1-2 hrs (config) | ~2-4 hrs (creds, upload) | ~1-2 hrs (CI queue) | 0 |
| **Credential/permission burden** | None | Network access | Cloud creds + IAM | CI runner access | None |
| **Auditability** | Physical artefact, labelled | Network logs | Cloud versioning logs | CI logs | None |
| **Cost** | USB drive (~$20) | NAS share | Cloud egress/storage | CI minutes | $0 |
| **Unblocks Phase 8** | Yes | Yes | Yes | Yes | No |

---

## Contingencies

| If… | Then… |
|---|---|
| **USB drive fails during copy/verify** | Retry with a second drive; the closure is still on the primary disk. |
| **Restore fails (CAS hash mismatch)** | The failure itself is evidence — document it. AC13 would remain "not verified." Investigate CAS corruption. |
| **No USB drive available** | Fall back to Option B (NAS/network share) if accessible, or Option D (CI runner). |
| **Owner policy forbids external media** | Option B or D; document the constraint. |
| **Closure size exceeds USB capacity** | Current closure is ~50 MB (9 CAS objects + manifests); any USB drive works. If it grows, use larger drive or split across multiple. |
| **Owner wants a more "production-like" domain** | Do Option A first (minimal gate), then Option C/D as a follow-up hardening exercise. |

---

## Next Actions

1. **Prepare the declared closure** — collect all CAS objects, manifests, receipts, the frozen producer wheel (`206e6474...`), and the `native-source-refs.json` (once producer merges) into a single directory tree with a manifest listing every object and its expected SHA-256.
2. **Copy to USB** — format USB drive (APFS or exFAT), copy the closure tree, compute and record SHA-256 of the entire tree.
3. **Restore on clean host path** — create a fresh directory (e.g., `/tmp/native-lineage-restore-20261101`), copy from USB, verify every file's SHA-256 matches the manifest.
3. **Replay verification** — run the Phase 7 replay checks (replay MOH and SHINE extractions from the restored CAS, verify 16 MOH values + SHINE beta row).
4. **Record receipt** — emit `integration/archive/ac13-recovery-receipt.json` with: USB drive label/serial, copy/restore timestamps, manifest of verified objects, replay results, `ac13_verified: true`.
4. **Update Conductor** — tick AC13 as "verified" in `p8-acceptance-evidence_*.json`, update `metadata.json` with `ac13_verified: true`, `ac13_recovery_receipt` path, `ac13_failure_domain: "USB external drive"`.

---

## Affected Conductor Records

- `integration/archive/ac13-recovery-receipt.json` (new)
- `integration/archive/p8-acceptance-evidence_20261031.json` — AC13 status → `verified: true`
- `conductor/tracks/native_archival_lineage_20261026/metadata.json` — `ac13_independent_copy_restore: "verified"`, `ac13_recovery_receipt` path, `ac13_failure_domain: "USB external drive"`
- `conductor/tracks/native_archival_lineage_20261026/plan.md` — tick P7.3
- `conductor/tracks.md` — update status line
- `conductor/index.md` — update track description

---

## Records

- Conductor track: `conductor/tracks/native_archival_lineage_20261026`
- AC13 receipt: `integration/archive/ac13-recovery-receipt.json`
- Phase 7 receipt: `integration/archive/moh-recovery-rehearsal_20261029.json` (same-device only)
- Frozen producer wheel: `archive-govt-nz` 0.1.0, `79004409`, SHA-256 `206e6474d155a6e0f7e0b6f70b5b59747fda473b8643193dc2a580bb7e98c640`

---

## Original draft approval placeholder — unverified

- **Original unverified placeholder:** [Owner] on 2026-11-01
- **Conductor track:** `native_archival_lineage_20261026`
- **Next Conductor update:** after AC13 recovery receipt recorded
