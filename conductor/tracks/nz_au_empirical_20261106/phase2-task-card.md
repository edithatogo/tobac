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

## P2.8 retail/cessation source-to-formula bridge — 7 November 2026

R03/R05/R16/R18; same owner/worktree/branch, clean base e57bc02. Own this card,
P2 reconciliation/receipt metadata, append-only P1 NZ model appraisal and scoped
WORKSTREAM_SYNC continuation. Read src/tobac/retail_case.py and tests/m2/test_retail.py
without changing their scientific/reference behavior. Raw supplement/parameter/formula
extracts and numerical diagnostics remain outside tobac in a new external edition;
ignored logs under outputs/nz-au-phase2-contrast-20261107. Reuse the pinned original
PMC11672025 XML and its CC BY-NC rights. Acquire its actual supplement via the
previously qualified official Europe PMC endpoint, check identity/ZIP contents before
extracting only the linked PDF. Observable deliverable: verify retail beta moments,
source transition versus aggregate consumption semantics and unresolved cessation
parameter discrepancy with a small independent Decimal oracle and installed SciPy.
No empirical input adoption, curve fitting, altered distributions/reference results,
causal-effect claim, source/archive/native write or private-binding transfer. Use actual
repo-local Python 3.15.2 and 4096 MiB / 2400 s guard, streamed logs, zero blind retries.
Stop adoption on ambiguous units/estimands or source inconsistency; retain alternatives
and source locations. Reuse unchanged code tests/replay and qualify new diagnostics
at their actual scope. Small writes only with low shared-volume headroom.

P2.8 owns the existing focused context profile adjustment: select the current NZ
model appraisal and retail source/test for this source-to-formula task, replacing
coverage audit/test and the accumulated reconciliation narrative in selection only.
No file/history deletion or context-budget increase. All empirical acceptance gates
remain; the independent arithmetic check is not a replacement fit or validation.

## P2.17 cessation baseline continuation — 7 November 2026

Same sole owner/worktree/branch, clean base 47dc6f9. Own this card,
decision-definition's selected verified cessation context, reconciliation metadata
and the scoped WORKSTREAM_SYNC continuation. Qualify the official 2026 guidance
edition and source-dated medicine/service access before describing the policy
contrast. Public originals, failure bodies and acquisition receipts remain outside
tobac under /Volumes/PortableSSD/tobac-p2-cessation.GtD3YW; ignored command logs
remain under outputs/nz-au-phase2-cessation-20261107. First use exact-target CLI
reads; use only the internal browser for an identified CLI access gap. Preserve
the 6 November evidence cut-off and distinguish publication from retrieval dates.
Do not equate funding eligibility, listed subsidies, clinical guidance or service
availability with uptake, effectiveness, actual delivery cost or source admission.
No native/integrator write, external message, model fit, personal clinical advice
or scientific-input adoption. Actual local Python 3.15.2, existing 4096 MiB /
2400-second guard, serial extraction and no blind retries. Reuse unchanged
software tests; verify source bytes, exact rule locations and publication boundary
for this metadata-only change. Messaging authorization remains unanswered.

## P2.18 prespecified PubMed S4 retrieval — 7 November 2026

Same owner/worktree/branch, clean base 1a96485. Advance the open prerequisite
search for monitoring/public-health value-of-information methods. Translate the
existing S4 title/abstract concept groups directly to PubMed field syntax; retain
the 6 November publication-date cut-off, no language/country restriction and no
outcome-driven query change. Exact request is frozen externally before execution.
Own only this card, systematic-search's executed continuation, P2 reconciliation/
receipt metadata and WORKSTREAM_SYNC. Native connector page responses, bibliographic
transport/import and audit artifacts stay under
/Volumes/PortableSSD/tobac-p2-search-s4.x181rk. Retain cursor/offset, total counts,
field continuations, hashes, query translation and actual terminal status. Use the
existing qualified Searchright source-native import contract, not fixture searches.
Do not label retrieval or deduplication as screening, study inclusion or admission.
All expensive local import/audit work uses actual local Python 3.15.2 and the
4096 MiB / 2400 s guard. No native/other-owner writes or cross-chat messages.
Preserve old search editions; failed/truncated pages remain visible and incomplete.

## P2.19 PubMed S5 retrieval and selected eligibility review — 7 November 2026

Same owner/worktree/branch, clean base 68ca7f2. Translate the existing S5
tobacco AND policy AND (diffusion OR competition OR spillover OR adoption)
title/abstract strategy directly to PubMed. Save the exact request before execution;
retain the publication cut-off of 6 November, with no language/country restriction.
Own only this card, systematic-search continuation, P2 reconciliation/receipt
metadata and WORKSTREAM_SYNC. Originals and per-record screening decisions remain
external under /Volumes/PortableSSD/tobac-p2-search-s5.jLmFdk; logs remain ignored
under outputs/nz-au-phase2-search-s5-20261107. Follow native connector offsets and
field continuations, reconcile the actual ID universe with native NCBI ESearch,
and retain count mismatches and exact-ID recovery attempts. Reuse the supported
Searchright source-native import route; no fixture search or keyword rule is
represented as live retrieval or eligibility review. Inspect actual title/abstract
content for any recorded screening decision, keeping a full-text queue and source
identity; unavailable text stays pending. No inclusion, source admission, model fit,
native writes or messages to the retained integrator are implied. Local expensive
work uses actual Python 3.15.2, serial 4096 MiB / 2400 s guards and zero blind retries.

## P2.20 S1/S3 native PubMed candidate retrieval — 7 November 2026

Same owner/worktree/branch, clean base 66807d1. Advance the remaining source
retrieval prerequisite using the existing S1 and amended S3-v3 concepts.
Searchright's PubMed compiler exposes a cross-dialect human-review warning;
retain it, with no claim of approved PRESS review or completed systematic evidence.
Initial exact native reads return 25,067 S1 and 3,048 S3 IDs/hits; S1 exceeds
the connector's 10,000-result window. Use qualified native NCBI ESearch/EFetch
for explicit inclusive publication-date partitioning and bulk original XML,
retaining every request/response/hash and count. No query vocabulary is changed.
Keep the 6 November cut-off and distinguish candidate retrieval from approval,
screening, study inclusion or empirical admission. Preserve cross-partition ID
overlaps rather than treating them as separate studies. Stop on unknown XML
record types, failed requests, ID/count drift or incomplete returned sets.

Own only this card, systematic-search continuation, P2 reconciliation/context
receipts and WORKSTREAM_SYNC. Originals, scripts and candidate outputs stay
under /Volumes/PortableSSD/tobac-p2-search-s1s3.mV6Dai; logs remain ignored under
outputs/nz-au-phase2-search-s1s3-20261107. No private/native/other-owner write,
runtime change or external message. Local acquisition/import runs serially via
actual Python 3.15.2 and the 4096 MiB / 2400 s guard, below three NCBI requests
per second without API keys. Zero retries; retain failures and completed batches.
Check actual IDs, source kinds, query translation and prespecified seeds before
claiming candidate retrieval completeness; existing scientific gates remain.

P2.20 first acquisition stops after 9,800 verified S1 XML records. The next
HTTP 200 response contains an embedded upstream 503 and lacks a complete XML
root (SHA256 2735badd3243ff65bfee5d226a0a976ad8ee04ebc253be37261e7a1dd7ef5466).
Retain that failed source and terminal status 1 (104.6 MiB sampled peak).
One identified transient read-only recovery is permitted for exactly that
200-ID batch, under a new recovery1 filename. Revalidate and reuse existing
hash/URL-bound requests and complete batches; do not repeat the whole search.
Future failures stop without automatic retry. No resource limit is changed.
