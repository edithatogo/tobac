# Review Report: M2 selected decisions and unsent record requests

## Summary

The bounded preparation is ready for guarded publication; sending, access, collection,
normative weights and empirical issue #3 acceptance remain explicitly unresolved.

## Verification Checks

- [x] **Plan Compliance**: Yes — six selected directions recorded with rationale,
  trade-offs and contingencies; four local unsent metadata drafts prepared in sequence.
- [x] **Style Compliance**: Pass — Conductor context/style guides and scientific
  evidence boundaries reviewed. All changed files reviewed individually (>300 lines).
- [x] **New Tests**: No — no executable behavior or model changes; direct checks
  verify documentary fixity/state/links instead of implementation-mirroring tests.
- [x] **Test Coverage**: Yes for software — 92%; not empirical or governance acceptance.
- [x] **Test Results**: Passed — 981 passed/five capability skips; tests, strict_all,
  reproduce, clean_package, security passed. Zero strict errors/warnings/notes;
  nine real Ruff policy tests passed. No checks/tolerances/security settings weakened.

## Findings

### Medium — Analysis requirements could be mistaken for an immediate extract request (fixed)

- **Files**: `requests/m2_20261027/README.md`, `fields.csv` and the four letters.
- **Context**: A required-for-analysis field is not proof of availability or permission
  to disclose row-level records. Pseudonymous labels do not prove safe use.
- **Fix**: Letters ask metadata/coverage first, explicitly defer restricted transfer,
  and explain aggregate fallbacks; README makes field-schedule precedence explicit.
  Current output is public aggregate conditional research; no received data committed.

### Low — Existing summaries versus future custodian analysis and acronyms (fixed)

- **Files**: R1–R4 and README.
- **Context**: Preparation must not commission fresh analyses or imply existing quotes.
  Letters must remain intelligible outside repository context.
- **Fix**: Distinguish existing summaries from options for later custodian analyses,
  retain no-paid-work wording and expand assay/survey/company abbreviations.

## Review scope and source evidence

Base main:443cf4d297b8f21da58fb9b3b95b87ce34678873.
Registration:ea39e2f. Implementation/reviewed content:c1e86e5.
Reviewed track spec/plan/metadata/index, Conductor decisions/index/registry/gates,
research decision pointer, R1/R2/R3/R4, README, CSV field schedule and JSON manifest.
No unresolved finding remains within this bounded preparation scope.

R1 public author contact verified from PubMed PMID41447812; R2 corresponding-author
contact verified from publisher DOI10.1093/ntr/ntag042,27 October 2026. These are
published routing candidates, not custody/delivery proof. R3/R4 exact recipients
remain unset because they are contingent and no sending is authorised. Current raw
field/vintage access, sender affiliation/eligibility and Māori governance are not inferred.

The preferred structured-document route was evaluated against repository-owned offline
review drafts: maintained Markdown/CSV specifications meet this task; no issued Word
output or alternative generator is needed. No native draft/document or sender created.
No external message, application, purchase, new model, dependency or background task.

## Executed verification

Repo-local `.nox/tests/bin/python` actual version3.15.1. Command:

```sh
.nox/tests/bin/python scripts/run_bounded.py --timeout 2400 -- uvx --python .nox/tests/bin/python --from nox==2026.10.20 nox -r -s tests strict_all reproduce clean_package security
```

Log:`outputs/engineering/m2-requests-local.log` (ignored local evidence).
Sampled owned process-group peak783.0MiB,default4096MiB/2400s,exit0. Heavy commands
ran serially; a bounded peak does not establish absence of leaks. Full tests include
M2 and cross-workstream integration. Existing model/reproduction inputs remain unchanged.
The run spans documentary commits; only prose/manifest review refinements changed
after its start. Final exact-head hosted qualification remains mandatory separately.

Direct checks verified13 content hashes,four unsent request IDs,24 unique field rows,
null collection requirement,false authority/receipt flags,relative links and14/14
track-name consistency. Manifest state is documentary,not a sending interlock.
Source predecessor specs and the prior assessment/receipt remain unchanged.

Final-head hosted results, guarded merge and receiving-main proof are maintained in
this publication's PR. They must not be inferred from local qualification. Original
untracked .DS_Store files are preserved and excluded from commits.
