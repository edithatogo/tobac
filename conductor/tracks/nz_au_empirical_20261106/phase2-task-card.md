# P2.1 — First NZ/AU empirical feasibility analysis

Requirements: R03–R10, R16, R18. Deliverable: reproducible source coverage audit,
verified AU programme comparator and explicit identification finding for the proposed slice.
This task does not fit a model or promote unaccepted inputs to Gold.

Owner: chat 01a1af53-2093-7f70-b761-e5f6cb7b769c, branch codex/nz-au-empirical,
/Users/doughnut/.codex/worktrees/tobac-nz-au-empirical/tobac, base 848da48 with owned P1.1
drafts retained. Allowed files: this track, scripts/audit_empirical_coverage.py,
tests/engineering/test_empirical_coverage.py, exact new publication inventory entries and
ignored outputs/nz-au-phase1 and outputs/nz-au-phase2. No native writes, archive ingestion,
external upload, shared dependency promotion or scientific source/input changes.

Prerequisites and stop: latest-lock native admission remains owner-held and incomplete;
Phase 1 source acceptance and exact policy baseline are incomplete. Only independent
read-only feasibility work proceeds. No current illicit estimate, fitted policy effect,
held-out predictive score or monetary EVSI may be fabricated in their absence.

Inputs: existing source_record.json and historical lawful-supply CSV, annual tonne series,
Phase 1 publisher download receipt and external ACIC report PDF SHA256
8e1dd8cfb754ea8fd577ee086a98e336384ffd10d8a1c5829e7f47bc72c1e741.
Reuse Polars for inventory/coverage, existing SupplyBasis and observation-handoff semantics,
existing source_handoff verifier; no parallel empirical likelihood is introduced.

Exact commands (repository root):

```sh
.venv/bin/python scripts/context_bundle.py --profile engineering/context/nz-au-evidence.json --out outputs/nz-au-phase2/context
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python scripts/audit_empirical_coverage.py --out outputs/nz-au-phase2/coverage.json
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/engineering/test_context_bundle.py tests/engineering/test_source_handoff.py tests/test_workstream_integration.py
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/engineering/test_empirical_coverage.py
git diff --check
```

The tracked scripts/audit_empirical_coverage.py contains no fitting: it checks existing extracted CSVs
against the consumer inventory using source_handoff path/hash guards and Polars to inventory
their scope. It does not verify them anew against publisher originals. Its source/hash and
terminal receipt are retained in the analysis output.
PDF text extraction uses installed pdftotext; visual verification uses a rendered PDF page,
with text/figure disagreements left unresolved. Local derived text/images remain outside
the source repository or under ignored outputs. Bounds proof uses dimensional equations,
not estimated conversion parameters or synthetic observations.

Acceptance: actual historical coverage reported with its source caveats; AU design fields
have exact PDF locations and verification mode; incompatible units cannot be subtracted;
shared-source ABS/ACIC records cannot establish independent corroboration. Missing costs
remain null/unpriced. Negative outcomes are valid results, not completed fitting tasks.
Budget: 4 GiB sampled group RSS, 40 minutes, serial heavy commands, zero blind retries.
Stop on changed source hash or ambiguous units. Rollback only owned metadata. Results,
actual exits and next prerequisites go in phase2-feasibility.md and plan/status updates.

## P2.2 continuation — 7 November 2026

Actual owner: chat 01a1b3ac-76ef-7b12-a919-91fcb05de339, managed worktree
/Users/doughnut/.codex/worktrees/tobac-p1-evidence/tobac, branch
codex/p2-empirical-slice-20261107, base 403600b. Phase 0 is qualified locally;
P1 source/baseline and empirical-admission gates remain open. This card continues
those enabling requirements for the real P2 slice; it does not redefine completion
as another inventory or a synthetic fit.

First resolve current original-source scope against existing frozen workbook evidence,
then retrieve public NZ survey/intensity, releases and denominator candidates into
/Users/doughnut/Documents/tobac-evidence-intake-20261107-p2. Reuse original source IDs,
Scope/EvidencePacket/SupplyBasis, consumer inventory and existing workbook reconciler.
No private binding transfer, new canonical observation table, native producer mutation,
external upload or empirical fit until the prerequisite gates pass. Record public
acquisitions as candidates with their exact URL, UTC time, status/type/hash and rights;
a search snippet or acquisition success is not accepted input.

Outputs: ignored outputs/nz-au-phase2-20261107 for context, command logs and receipts;
metadata and reconciliation under this track. Runtime: actual existing repo-local
.venv Python 3.15.2, unchanged qualified lock. Expensive commands are serial through
scripts/run_bounded.py at 4096 MiB / 2400 seconds. Native owners retain their objects.
Before fitting, require the matched observation/holdout manifest, original verification,
dimensions/dependence reconciliation and accepted current policy contrast. Preserve the
original finite-state oracle. Run affected tests plus tests/test_workstream_integration.py;
retain unexecuted empirical/release gates explicitly.

P2.2 owns scripts/audit_empirical_coverage.py and
 tests/engineering/test_empirical_coverage.py for the narrow optional NZHS candidate
reconciliation, plus engineering/context/nz-au-evidence.json and exact new metadata
classifications. The existing historical-only CLI remains supported. New rows retain
all original fields and logical record ordinals outside tobac; a candidate table is
not a second canonical observation or an EvidencePacket. Fail on changed source bytes,
columns, duplicate indicator/year keys, unknown flags and invalid marginal intervals.
Retain suppression, missing occasions, survey-year labels and distinct intensity units.
No covariance, exact dates, population denominator or independence is inferred.

Actual source: 6d3e0a019d7e32030147f128c21098f074683cd3cfef41b0dcfff85b74b6b915,
NZHS 2024/25 prevalence/mean export observed through its official download panel.
The direct canonical application/data URL returns identical bytes and is qualified
for subsequent CLI acquisition; Ministry health.govt.nz downloads' 403s are a separate route.

Executed command additions:

```sh
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python scripts/audit_empirical_coverage.py --nzhs-csv /Users/doughnut/Documents/tobac-evidence-intake-20261107-p2/NZHS_prevalences-6d3e0a019d7e32030147f128c21098f074683cd3cfef41b0dcfff85b74b6b915.csv --nzhs-sha256 6d3e0a019d7e32030147f128c21098f074683cd3cfef41b0dcfff85b74b6b915 --candidate-out /Users/doughnut/Documents/tobac-evidence-intake-20261107-p2/nzhs-adult-total-candidates-v2.csv --out outputs/nz-au-phase2-20261107/slice-source-reconciliation-v2.json
.venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- .venv/bin/python -m pytest -q tests/engineering/test_empirical_coverage.py tests/engineering/test_source_handoff.py tests/test_workstream_integration.py
env TOBAC_LINEAGE_ROUTE=attested TOBAC_LINEAGE_PYTHON=/Users/doughnut/.codex/worktrees/tobac-p1-evidence/tobac/.venv/bin/python .venv/bin/python scripts/run_bounded.py --max-rss-mib 4096 --timeout 2400 -- uvx --python .venv/bin/python --from nox==2026.10.20 nox -r -s tests
```

The first real candidate extraction was inadvertently run without the guard; its v1
edition is retained as unbounded evidence. The subsequent guarded v2 uses the reviewed
helper, and candidate CSV bytes match v1 exactly. Do not attribute a sampled resource
peak to the first run or overwrite it. The default Nox native route stops on the absent
owner-held TOBAC_LINEAGE_PYTHON binding. The supported attested route is separate and
uses only this worktree's qualified .venv; no private bindings are copied.

## P2.3 public matching-source continuation — 7 November 2026

Same owner/worktree and branch, clean base b1cb8f4. The prior P2.2 packet stays frozen;
its proposed cross-chat handoff is unanswered and no message is authorised. Continue
independent source work for P2's missing population, price and trade requirements.
Own only this track's task/evidence notes, exact metadata classifications and ignored
outputs/nz-au-phase2-context-20261107. No scientific code/input, lock, M3, native/archive
or shared-main mutation. Retain originals in a new external intake edition; use actual
publisher links/qualified CLI reads and hash/status/content-type receipts. Preserve
estimate-versus-projection, point population-versus-survey denominator, price index-
versus-price, and re-export/transit-versus-consumption distinctions. Do not infer a
calendar-period bridge or a causal price response from these acquisitions. Reuse the
unchanged P2.2 full test/typing/reproduction receipts; qualify any new extraction at its
actual scope before source admission or fitting.
