# Plan

- [x] Inventory pandas/xarray use and the Polars/PyArrow boundary.
- [x] Add a failing consumer test for normalized-bundle round trip, then implement.
- [x] Record toolchain exceptions against the shared matrix.
- [~] Triage open Dependabot alerts; fix or dismiss with a recorded reason.
- [~] Installed-artifact evidence; run required hosted gates.
- [ ] Owner approval, then archive after acceptance.

## Consumer verification — 1 November 2026

Chat 01a195fd-7f87-7472-9ff4-3c1e59fe7976 owns the normalized bundle reader,
test, type declaration and qualification notes in voiage-alignment/tobac.
The public interchange extra pins Polars 2.1.0 and PyArrow 26.0.0. Pandas
3.1.0 stays in the longitudinal extra for calibration and verification scripts.
No xarray import was found in src. The reader uses the producer's IPC and
Parquet contracts directly. The toolchain uses Python 3.15.1, uv (local
0.13.6), Ruff 0.17.3 and ty 0.0.94. There is no first-party Rust core in tobac.
The upstream wheel owns its compiled extension.

The test failed on the absent reader before implementation. With the installed
wheels outside the checkout, Python 3.15.1 ran
`python -I -m pytest -q --basetemp cases test_normalized_bundle.py` (exit 0,
two passed). Both imports resolved under .venv/lib/python3.15/site-packages,
at tobac/normalized_bundle.py and voiage/contracts/normalized_input.py.
The fixture uses two timestamp[s] chunks and includes a null. Both formats
recovered the original table, chunk count and expected digest and rejected a
different digest. Evidence at consumer implementation 90ad10e:

| Artifact | SHA-256 |
|---|---|
| tobac wheel | b31ec3c31eca956391543327a67463f9d9208fdd84b62f0f13be8cfd5b62def0 |
| candidate voiage wheel | 1bc511001f8336480efa83902594e1a86f7d5338ccfd6e668e56018f060d299e |
| normalized_input.py (matches upstream revision 3619b1589e3a) | 846dbdf6aee4ec843a7147ba6ba42e3ad8618fcb6c88755332b341150e61b08c |
| IPC bytes | fe015d8390f3ba3aef48611a8b35e88155b5d5c4dbf03310b16d56d095f1c915 |
| Parquet bytes | b3c65b21343d865868a21c072898beaf387414660a081c0e6c31f9b971236982 |
| content digest before and after either read | e0f58a9487dfd7abe2eb23f6b970e1d004496a7bcf84bbd73805d62f6b6ed776 |

GitHub's open-alert endpoint returned HTTP 403, reporting Dependabot alerts
disabled. No alert disposition is asserted. Engineering locks contain Pillow
13.0.0, filelock 4.2.6 and virtualenv 21.15.1; tornado and astro were absent.
The sampled Renovate PR #94 head had a valid verified signature. The main
branch protection API reported required signatures disabled. Settings were
read only. Hosted verification and owner acceptance are tracked separately.

## PR 97 verification

Both local Nox sessions completed on Python 3.15.1: 1,137 tests passed,
15 skipped, 92% coverage, and the complete numerical and publication replay
passed (853 MiB peak sampled RSS). On a974d52 the hosted strict checker
reported a missing-source warning for the optional Voiage import. The reader
now imports Voiage at use time and describes the returned object structurally.
Strict checking in the baseline environment had zero warnings or errors;
the real candidate and cross-workstream tests passed (28). The user authorised
merge after required checks; Dependabot alert-level triage remains blocked.
