# Native scientific lineage recovery

The [Phase 7 receipt](../../integration/archive/ac13-recovery-receipt.json)
pins a private, owner-held recovery generation for macOS arm64. Its manifest
lists the relative name, size and SHA-256 of every payload file. Keep the pin
separately from the backup. Source-specific rights continue to apply.

The generation includes the four capture receipts and their CAS/WARC files,
the accepted registrations, retained MOH and SHINE extractions, all eight
scientific attempts, the earlier six material-checked attempts, and the
source files needed for the declared inventory. It also includes the Python
3.15.1 runtime, offline wheelhouse, package licences, consumer source
distribution, producer wheels, verifier and replay recipe.

## Restore

1. Confirm the source and destination are on different physical devices. The
   copy tool also rejects a same-filesystem transfer. Select a fresh internal
   destination outside the working repositories.
2. Read the expected manifest digest from the committed Phase 7 receipt.
   Using the repo-local interpreter, run
   `scripts/qualify_lineage_recovery.py copy USB_GENERATION NEW_DESTINATION EXPECTED_SHA256`
   through `scripts/run_bounded.py --timeout 2400`. This rehashes the source,
   copies and flushes every file, then independently inventories the destination.
   Use `verify DESTINATION EXPECTED_SHA256` for subsequent checks. Keep an
   interrupted destination for diagnosis and use a new destination for retry.
3. From outside the worktrees, run the restored `replay.sh` with the verified
   kit path and a new working directory. Use the documented process-group
   resource limit and deny network access and reads from the implementation
   checkouts, prior native stores and USB source during replay. Allow local
   Apple shell utilities and Git. The script installs only restored wheels.
4. Inspect the native registration and qualification receipts, individual runner
   receipts, and stage-boundary recovery receipt. Compare actual CSVs and
   classify other artifact differences before accepting a replay. The local
   reconstruction has its own Git identity and command paths.

The working replay creates disposable environments and fresh results beside
the verified kit. Preserve the sealed generation and earlier successful
execution records. Replacing a dataset, runtime or wheel requires an explicit
new generation and pin.
