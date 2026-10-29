# MOH workbook extraction and native records

This consumer operation re-extracts the identified original workbook and compares
all sixteen values with the preserved consumer CSV. It records exact `Sheet1`
cells `A2:B17`, native CAS objects, and strict native transformation/validation
records. It leaves the consumer CSV, producer checkout and canonical estate intact.
Its fixed mode is **exploratory**: native source registration, full manifest
closure, original capture time, runner integration and recovery remain open.

## Qualified interface and ownership

`integration/archive/native-producer-interface.json` binds a consumer-built,
unreleased archive-govt-nz 0.1.0 wheel to frozen revision
`790044096f6946ff9a21662108f4d924cbad0ba2` and selected module hashes. The
producer's active writer retains all source and native operations. A tracked-only
Git archive supplies the build; dirty producer files and environments are not copied.

The consumer verifies the wheel's actual hash, its installed package files and
the imported native module bytes. Editable producer sources are rejected. The
private environment uses Python 3.15.1 and a generated hash lock constraining the
existing scientific pins. Its dependency resolution and installed-package check
do not qualify the entire producer CLI, all its tests, or a published release.

Build with `uv build --wheel --no-sources` using the selected repo-local Python,
then generate a private hash lock from `engineering/requirements.in` and that
wheel, constrained by `engineering/requirements.lock`. Install with `uv pip sync
--require-hashes` into a new consumer-owned environment and run `uv pip check`.
Include the existing audit tool's qualified `cyclonedx-python-lib` version in
that private profile. Produce a complete CycloneDX 1.6 inventory through its
maintained model/output APIs, retaining the unpublished wheel's actual hash.
The command validates its schema through that library and compares every Python
component with the actual execution import context, including the declared
consumer source distribution. A pip-audit SBOM alone omits unpublished
packages; its auditable-dependency result is retained separately.
Keep the wheel, generated lock and command logs in ignored private storage. The
interface descriptor must match the reviewed artifact before execution.

## Explicit execution

Use the existing Nox orchestrator under the normal resource guard:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  uvx --python 3.15.1 --from nox==2026.10.20 nox -s native_moh_lineage -- \
  /absolute/consumer/repo/.venv-native-lineage/bin/python \
  --wheel /absolute/private/archive_govt_nz-0.1.0-py3-none-any.whl \
  --environment-lock /absolute/private/native.lock \
  --environment-sbom /absolute/private/complete-environment-sbom.json \
  --workbook /absolute/private/verified-original \
  --out outputs/engineering/NEW-PRIVATE-ATTEMPT
```

The consumer helper deliberately imports this checkout's consumer code; the
producer imports must resolve to the verified installed wheel. This is not a
clean installed consumer/replay qualification. The original must match the existing
reconciliation hash. No capture or network request occurs. All source, reference
and metadata bytes are snapshotted before use. The workbook parser consumes the
same snapshot stored in native CAS. Input reads are capped at 16 MiB, and attempts
must use a new directory beneath this repository's private `outputs/` namespace.

Native record timestamps describe this execution. Historical capture time remains
as recorded, including null. WARC hashes are inherited metadata, explicitly not
verified by this command. Changed legacy CSV bytes fail before execution; extraction
does not overwrite or reclassify them. Native failed transformation records retain
the failed state during extraction; command logs retain the exception; an incomplete attempt cannot emit a successful receipt.

## Remaining acceptance gates

The producer's source/capture records and strict-record-to-manifest adapter still
need complete object/relationship validation. A per-record `passed` validation
covers only the named checks. It cannot qualify original preservation, a complete
source-to-result graph, future data additions, scientific applicability or an
independent-copy restore. No `receipt_id` shim or second provenance engine is added.
Second-operation, runner, qualification-mode and recovery tasks stay open in the
existing native-lineage plan. Scientific ecosystem remains separately open for
native managed-parser acceptance.

## Executed checkpoint — 29 October 2026

Implementation `6fa2306` passed the explicit native Nox operation: sixteen exact
rows, nine verified CAS objects, strict transformation and validation records
reopened from disk and CAS. Five actual native negative controls rejected corrupt
source bytes, a missing output, missing SBOM, duplicate inputs and invalid state.
Controls used disposable copies/in-memory records; successful originals remain intact.
The execution inventory contains 82 components (81 installed plus declared consumer
source). See [public technical summary](../../integration/archive/moh-native-extraction_20261029.json);
original bytes, complete records/argv and private runtime artifacts stay ignored.
