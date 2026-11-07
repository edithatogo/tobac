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

## P2.4 historical price bridge — 7 November 2026

Same sole owner chat/worktree/branch, clean base 31be90b. Own only this task card,
P2 reconciliation/receipt metadata and WORKSTREAM_SYNC continuation, plus ignored
outputs/nz-au-phase2-price-20261107. Reuse existing maintained code and P2.2 checks.
Acquire the actual SAP0240 historical selected-item cigarette price series through
the official Infoshare selection after the qualified quarterly CLI source proved
current-quarter-only. Keep native CSV/query originals and derived candidates outside
tobac in a new edition; preserve source units/status, source dates and pack-size
revisions. Compare overlapping published current-quarter price and index without
conflating them. Do not estimate elasticity, interpolate, infer a paid-price/consumption
bridge or fit past the still-open P1 admission/rights/policy/validation gates.

## P2.5 survey-period and denominator bridge — 7 November 2026

R03/R04/R16/R18; same chat/worktree/branch, clean base 1e227d6. Own only this
card, existing P2 reconciliation/receipt metadata and WORKSTREAM_SYNC continuation;
ignored outputs/nz-au-phase2-methods-20261107 and a new external intake edition
hold acquisition/extraction artifacts. The existing Ministry CLI annual-page and
method-PDF 403 receipts are retained. Use internal-browser native access for the
concrete inaccessible source, verify source links before downloads, then return to
CLI for exact-byte checks and page/section extraction. Observable deliverable:
source-bound period/frame restrictions and a supported matching/no-matching
assessment, preserving pandemic interruptions, survey-year labels, private-household
eligibility, age and denominator differences. No numerical population calibration,
interpolation, new likelihood/fit, original-owner/archive write or source admission.
Use actual repo-local Python 3.15.2 and the existing 4096 MiB / 2400 s bounded guard
for extraction; stream logs under that ignored output. Stop on access boundaries or
missing source definitions; retain failures and continue independent checks only.
Reuse unchanged maintained-source tests/typing/replay; exact original hashes, PDF
locations, extraction outcome and remaining limits must accompany the result.

P2.5 context-start failed the unchanged 100,000-byte serialized budget. Narrow the
same owned engineering/context/nz-au-evidence.json by removing the two unchanged
P1 model-appraisal documents from this survey-methods task's selected context;
retain them on disk and retain P1 progress/gates, P2 contracts and audit/tests.
No budget increase or archive deletion. Rebuild into a new context edition.

## P2.6 lawful-sales measurement bridge — 7 November 2026

R03/R04/R18; same owner/worktree/branch, clean base 6e32a6a. Own this card,
existing P2 reconciliation/receipt metadata and WORKSTREAM_SYNC continuation; all
source originals and candidate extracts remain in a new external intake edition,
with ignored execution logs under outputs/nz-au-phase2-returns-20261107. Reuse
integration/archive/workbook-reconciliation.json (16 verified values) without
re-running its unchanged numerical comparison. The concrete missing capability is
Ministry source-page access after qualified CLI 403s; use the internal browser to
read actual returns scope and observe publisher download links. Retain exact bytes,
source labels/units, period/product/duty-free caveats and dependences before claiming
compatibility with the NZHS. Do not equate sales to consumption, change existing
scientific inputs or source admission, infer a product mass conversion or perform
native/archive/other-owner writes. Actual Python 3.15.2, 4096 MiB / 2400 s guard and
streamed logs for extraction; zero blind retries. Stop dependent conversions on
ambiguous scope. Qualify originals/coordinates and preserve discrepancies. Reuse
unchanged P2.2 tests/typing/replay; small writes only with low shared-volume headroom.

P2.6 final context exceeded the unchanged 100,000-byte ceiling as source notes grew.
Narrow the owned engineering/context/nz-au-evidence.json to this active P2 task:
remove superseded P2.1 feasibility and frozen P1 progress from selection only. Preserve
both files/history and current admission/identification gates in decision-definition
and current P2 reconciliation. No budget increase. Rebuild a new context edition.

## P2.7 operative retail baseline — 7 November 2026

R03/R06/R18; same owner/worktree/branch, clean base 3494436. Own this card,
existing P2 reconciliation/receipt metadata, decision-definition's narrowly verified
NZ retail/repeal baseline and WORKSTREAM_SYNC continuation. Raw official legal
originals remain outside tobac in a new intake edition; ignored logs under
outputs/nz-au-phase2-policy-20261107. Check supported CLI exact official targets
first; use only internal-browser access if needed. One observable result: source-bound
commencement/repeal and current consolidated retail provisions, distinguishing
6 November 2026 policy cut-off from retrieval and prospective/uncommenced changes.
Do not equate statutes with implementation or causal policy effects. Preserve unknown
excise, cessation/service, enforcement, product/substitution and AU settings. No legal
eligibility assignment, empirical fit, archive/native write or scientific-input change.
Actual repo-local Python 3.15.2, existing 4096 MiB / 2400 s guard for extraction,
streamed logs and zero blind retries. Stop on source-date ambiguity or inaccessible
operative text. Reuse maintained code tests/replays; check source hashes/locations,
context and publication boundary before metadata commit. Small writes only.
