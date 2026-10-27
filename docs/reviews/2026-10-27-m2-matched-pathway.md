# Review Report: M2 matched evidence pathway

## Summary
The bounded metadata implementation and prospective protocol are ready for committed-source
verification; issue #3's empirical acceptance remains open.

## Verification Checks
- [x] **Plan Compliance**: Yes for bounded implementation/source-feasibility scope; partial for the applied issue.
- [x] **Style Compliance**: Pass; unchanged whole-source Ruff/formatter/BasedPyright policies.
- [x] **New Tests**: Yes; 26 cases covering scientific metadata rejection and real ingress behavior.
- [x] **Test Coverage**: Full suite 950 passed, five capability skips, 92%; focused/integration 109 passed before expanded cases.
- [x] **Test Results**: Tests, strict_all, reproduce and clean_package passed under Python 3.15.1;
  final strict_all/security also passed after receipt-provenance fixes. Committed-source rerun follows.

## Findings and fixes

Reviewed iteratively by file because the change exceeds 300 lines. Owner authorised autonomous
implementation/review, so no additional review confirmation or independent reviewer was required.

- `src/tobac/matched.py`: parsed-date ordering replaces lexical comparison; same-scope self-comparators,
  duplicate identities/cells, empty products, inconsistent populations/products/units/windows and
  derived roles are rejected or reported. Exact shared IDs require a joint representation.
- `scripts/qualify_m2_pathway.py`: validates strict JSON schema, rejects duplicate JSON keys and unsafe
  repository references through existing helpers, verifies source-bound bytes and source references.
  Receipt creation is exclusive and now records exact checkout/actual command. Typed protocol isolates
  the untyped jsonschema boundary without changing checker policy. No posterior or likelihood is created.
- `engineering/schemas/m2-pathway.schema.json`: unknown fields rejected; null scope remains explicit.
- `evidence/m2/matched_pathway_20261027.json`: actual public prevalence/releases stay unassigned to causal
  cells, with native units/unknown scope intact. Previous verified workbook receipt remains immutable.
- `docs/research/M2_MATCHED_PATHWAY.md`: prospective 600-outlet contrast retained separately from current
  authority; no historical nationwide treatment assigned. Conditional counterfactual, spillover,
  raw-scale assay, signed discrepancy, shared errors, no-study and null effects are retained.
- `tests/m2/test_matched_pathway.py`: fixtures test compatibility only. Real manifest returns blocked,
  eight cells missing, no conditioning. Malformed input/hash drift/overwrite tests execute real ingress.
- `noxfile.py`: audit runs before unchanged numerical reproduction in a fresh replay directory.
- `engineering/context/regulatory.json` and Conductor: new contract included in bounded context;
  issue-level empirical/field/transport/mitigation/crime/cost/governance gates remain explicit.

No unresolved software finding was identified. Metadata compatibility is not empirical qualification;
unknown source dependencies cannot be detected from dishonest/aliased IDs. No new statistical engine,
scientific prior, raw observation, normative weight, M3 interface, numerical tolerance or security waiver
is introduced. Primary-source rendered review is distinct from raw capture; denied downloads are recorded.

## Verification record

Initial bounded milestone: tests/strict_all/reproduce/clean_package passed, sampled peak827.9MiB.
Post-review strict_all/security passed, sampled peak756.7MiB. Full runs use 4GiB/2400-second budgets;
these are execution controls, not proof of absence of leaks. Final committed-source tests, strict_all, reproduce, clean_package and security passed at
0bdb6ad: 950 passed/five skips, 92% coverage, zero strict diagnostics, peak681.0MiB.
M2 passed 805 invariants; 482 retained-table numerical comparisons pass rtol=atol=1e-10.
CSV line endings and expected floating roundoff differ; no numerical claim of byte equality.
Results and receipts: integration/m2_matched_pathway_20261027.json. Hosted final-head and
receiving-main verification remain required before publication is described as complete.

Conductor close-out check found a missing title on the new archive metadata and a
pre-existing Voiage registry pointer/title mismatch. Corrected both without
changing either track's scientific or release scope. Native naming check:12/12
tracks consistent. These documentation repairs introduce no runtime changes.
