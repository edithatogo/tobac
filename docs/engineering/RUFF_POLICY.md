# Ruff policy and bounded verification

Ruff 0.17.2 targets Python 3.15. Nox `strict_all` lints and checks formatting of
`src`, `scripts`, `tests`, `noxfile.py` and `engineering/typings`; it also executes real Ruff counterexamples
and the existing whole-source BasedPyright gate. Root `ruff.toml` exposes the same
policy to editors. Historical extraction bytes in `evidence`, generated outputs and
upstream `vendor` checkouts are not reformatted or treated as project-owned code.

`ALL` remains enabled. Existing global exclusions D203/D213 (alternative docstring
conventions), COM812 (formatter compatibility) and CPY001 remain unchanged.
Test-only exceptions permit pytest assertions, literal numerical oracles, namespace
discovery, dynamically injected fixture/parameter arguments, heterogeneous fixture
factory returns and descriptive test names instead of duplicate docstrings. Most test
functions now explicitly return `None`. These exceptions do not apply to source or
scripts. Local inline exceptions explain capability imports, fixed subprocess argv,
upstream execution-double signatures and deliberate rejection fixtures.

Broad exception checks now match observed diagnostic messages, and jsonschema
rejections require `ValidationError`. No blind `Exception` catch remains in these
tests. This strengthens failure identification without changing the scientific inputs.

## Qualified preview rules

Preview linting requires exact rule selection (`explicit-preview-rules = true`):

| Rule | Scope and qualification |
| --- | --- |
| PLW1514 | Explicit encoding for text reads and subprocess decoding; retained inputs are UTF-8. |
| RUF039 | Raw regular-expression literals; matching behaviour retained. |
| RUF031 | Consistent tuple subscripts; index tuples remain the same. |
| PLC1901 | Empty-string truth checks, after verifying affected CSV cells are strings. |
| FURB113 | Consecutive list appends batched in order; expressions do not observe the intermediate list. |

Each has a real failing counterexample in `test_ruff_policy.py`. Other experimental
rules remain unselected, including floating-point equality, private-member access,
complexity and docstring-section policies that require separate context-sensitive
review. Enabling preview is not blanket qualification. Formatter preview remains off.
No blanket unsafe fix is part of the workflow; reviewed targeted fixes and full
numerical reproduction are required for promotion.

## Resource controls

Run expensive local commands serially through the repo-local Python 3.15.1 guard:

```sh
.nox/tests/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- \
  uvx --python 3.15.1 --from nox==2026.10.20 nox -r -s tests strict_all reproduce
```

The same wrapper protects macOS hosted tests and qualification. It samples total RSS
for the newly created process group every 0.5 seconds, fails with status 137 over
4 GiB or 124 on timeout, streams output without retaining it, reports sampled peak
RSS, and terminates/reaps owned children on normal exit, failure, interruption or
termination. Mutation uses at most two children. Existing CI concurrency cancellation
and job deadlines remain in place. No automatic retry is introduced.

The guard is an execution budget, not proof of a memory leak or a kernel allocation
limit. Allocation can overshoot between samples, RSS can count shared pages more than
once, and deliberately daemonized children that leave the process group are unsupported.
It fails closed when native monitoring fails and never targets unrelated process groups.
SIGKILL of the guard itself cannot run cleanup; hosted job teardown remains the backstop.
The guard is POSIX-only; non-macOS development remains deferred. Tests exercise real
memory/timeout termination, normal-parent-exit cleanup and SIGTERM handling.

A bounded baseline recorded 657.4 MiB peak sampled group RSS, with 885 passed and five
capability skips. That measurement is not evidence of a leak or a general memory plateau.
See the dated Ruff review and integration receipt for the final acceptance scope.
