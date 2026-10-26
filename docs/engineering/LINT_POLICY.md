# Strict lint and static interface policy

The strict session checks every active source/CLI module with Ruff's ALL selection and
BasedPyright strict mode on the actual calling Python 3.15.1 interpreter. Source and script
roots are explicit; no cached environment's site-packages are used as an import shortcut.

The zero Ruff result includes 175 individually recorded compatibility/style findings treated
as intentional exceptions, plus the standalone-CLI package-marker rule. These are policy
choices, not 175 code defects fixed. Each inline exception states its reason and remains
subject to Ruff's unused-noqa check. The original raw counts must not be compared as if every
reduction were a behavioral correction. Details: `integration/ruff_policy_exceptions_20261026.json`.

Exceptions retain public positional flags and dimensioned arguments, the original extracted
core's exception text/name, explicit ordered validation and report assembly, lazy optional
imports, direct CLI bootstrapping/stdout, and reviewed shell-free subprocess argument lists.
The two broad exception handlers write explicit failing receipts. Raw JSON decoders retain
an Any return because their root shape is checked by their callers. No whole-project unknown,
argument-type, missing-annotation or missing-import diagnostic is disabled.

Numerical bounds have names; zip length policies are explicit; quantile callbacks bind their
iteration values; generic arrays and numeric input contracts are annotated; structured report
containers are explicit. Config/Report describe heterogeneous validated/serialized JSON, not a
static scientific schema. Static checks do not establish units, covariance or empirical validity.

Pandas/SciPy/jsonschema stubs are tool dependencies, locked separately from scientific runtime
pins. Narrow Matplotlib member ignores cover its untyped kwargs. The optional Voiage stubs
record only the previously selected 2.2.0 API contract; source-availability ignores are attached
to runtime probes, which still fail closed. A stub is not an installed-package execution receipt.

The original inherited core is retained byte-for-byte in `evidence/core_extraction_20261024.py`
and verified against the original extraction hashes. The active core is compared against that
snapshot after normalising only static annotations, no-op typing casts and the explicitly bound
literal constants in the maintenance receipt. Defaults, fields and numerical expressions remain
checked. The original baseline manifest is not rewritten to fit the edited source.
