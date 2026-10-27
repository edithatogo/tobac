# Review Report: M2 evidence synthesis and partial identification

## Summary
The bounded source synthesis and identified-set implementation preserve existing scientific
inputs; final committed-source qualification and hosted publication remain pending.

## Verification Checks
- [x] **Plan Compliance**: Yes for targeted source synthesis/conditional identified sets; no applied empirical closure claimed.
- [x] **Style Compliance**: Ruff passes after fixing line lengths; initial BasedPyright returned zero diagnostics.
- [x] **New Tests**: Yes; independent SciPy linear-programming oracle, containment and real source/provenance failure cases.
- [x] **Test Coverage**: Final full suite981 passed/five capability skips,92% coverage.
- [x] **Test Results**: 150 targeted M2/workstream cases pass; final five-session Nox milestone passes at `c8af5c1`.

## Findings and fixes

Reviewed iteratively by source/configuration/documentation file because the change exceeds300 lines.
Owner explicitly authorised autonomous review and fixes; independent review is not required.

- `src/tobac/partial_identification.py`: sharp marginal supports have an explicit Cartesian input
  contract; zero-total consumption makes switching irrelevant/unidentified. Empty incompatible
  sets remain empty; negative accounting discrepancies are not clipped. M2a equal-intensity,
  restriction-alone and no-consumption-increase assumptions remain explicit. Joint q,d dependence
  is not replaced by the rectangle of their marginal supports.
- `scripts/qualify_m2_synthesis.py`: verifies exact documentary input bindings, source/code and
  generated-reference hashes; validates complete unique configured scenario/design tables. Added
  guards for failed numerical validation, future leakage, missing reserved diagnostics and
  nonfinite study values. Historical model-year rows are explicitly not independent observations.
- `evidence/m2/synthesis_20261027.json`: thirteen documentary sources have locators, access level,
  actual endpoint, limitations and dependence group. CVS studies share one policy event; human
  anabasine yield shares inherited calibration inputs. No target likelihood is adopted. The
  source's reported plus/minus dispersion is not assumed to be CI/SE; selected observed range
  is not target population coverage. All nonmissing ratio cases are synthetic demonstrations.
- `engineering/schemas/m2-synthesis.schema.json`: unknown fields are rejected and all source
  adoption flags remain false; native numeric extractions are documentary, not configuration priors.
- New tests: an independent transformed linear-programming problem checks sharp endpoints;
  grid containment, zero/missing distinctions, bias widening, signed residuals, incomplete/duplicate
  reference tables, modified outputs, invalid scenarios and overwrite rejection are exercised.
- Nox: synthesis executes only after the original M1/M2/M3 and longitudinal reproduction/verifiers.
  Reference scientific formulas, priors, observations, M3 interfaces and tolerances are unchanged.
- Context: retained80kB budget; narrowed the existing regulatory profile after a real budget
  rejection, rather than increasing it or ingesting archives. Source hashes are rebuilt on changes.
- Documentation: the initial matched-pathway/receipts are preserved. Updated research gates
  distinguish data access/clarification from new collection and human governance/value decisions.

No new inference framework, unqualified physical conversion, monetary calibration or operational
permission is introduced. Source access is rendered/indexed unless a previously verified object
is explicitly named. No missing record, unreported channel, null effect or no-study option is
converted into evidence of a preferred policy. No external contact/data-access application occurs.

## Final verification

To be filled from actual committed-source Nox execution and native PR/receiving-main readback.
The initial strict run failed on one line-length diagnostic; that was fixed, not suppressed.

## Additional primary-source review

A fresh official BAT PDF still prints2024 despite the2025 link. Historical ActionPlan
RIS costs are package-wide prospective estimates,not current target/study costs.
The2022 baseline report shares MOH/NZHS inputs with Phyo; a new Decimal-based
source-arithmetic/uplift sensitivity check reproduces its gap while preserving
negative discrepancies and refusing mismatched source quantities. The original
366f37b milestone passed978 tests/five skips,92% coverage and all five Nox gates
(peak797.6MiB). Final verification must include this added source-arithmetic code.

Final committed-source verification at `c8af5c1` passed all five Nox sessions:
981 tests/five capability skips,92% coverage;zero strict diagnostics;clean-package
and security pass. All 805 M2 invariants and 482 retained-table comparisons pass
rtol=atol=1e-10. Peak 815.1MiB under 4 GiB/2400seconds. Source-bound synthesis
reproduces13 source records,15 conditional scenarios/225 study rows,source 2022
gap arithmetic and signed uplift sensitivity. Historical coverage5/9 model-year
rows over 3 distinct years does not establish nominal95% calibration.

Receipt: integration/m2_evidence_synthesis_20261027.json. All runtime source changes
were reviewed before publication; hosted final-head/receiving-main proof remains
mandatory and is maintained in the publication PR. Issue #3 stays empirically open.
