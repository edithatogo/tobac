# Review Report: M2 conditional publication and value sensitivity

## Summary

Iterative single-developer self-review finds the conditional analysis and claim
boundaries coherent after the fixes below; final qualification is recorded below.

## Verification Checks

- [x] **Plan Compliance**: Yes — executed value grid, continuous-box/threshold checks,
  source roles, methods report, figures and documentary ethics assessment.
- [x] **Style Compliance**: Pass — existing ALL Ruff/format and BasedPyright rules;
  no dependency, security-policy, CI-pin or reference-core changes.
- [x] **New Tests**: Yes — 27 additional tests including parametrised cases;
  independent scalar VOI arithmetic, signed harm, dominance, ties, malformed inputs,
  reference-weight parity, frozen assumptions, source eligibility and tampered outputs.
- [x] **Test Coverage**: Yes — component and workstream integration plus full suite,
  numerical reproduction and clean-package/security checks as recorded below.
- [x] **Test Results**: Passed — 1008 full-suite tests / 5 capability skips,
  93% coverage; all five local Nox sessions pass after the context-profile fix.

## Review scope and applied corrections

Base e35b5abc5bf184c66b8d5c7540735bd0175f15ed through implementation cc2fbd1,
then manuscript/results/context/Conductor packaging and SVG serialization fix
7990b78. The >300-line change was
reviewed iteratively by file group under the owner's autonomous review/fix direction.
No independent reviewer or external scientific endorsement is implied.

1. Numerical module and tests: retained signed criminal-harm changes, normalised
   priors, all optimal ties, upper-envelope-only thresholds and continuous affine
   box certificates. Confirmed reference-weight parity and independent scalar VOI.
2. Runner/schema/Nox/tests: source/document/group relationships and no-adoption
   flags are checked beyond hashes. Resolution diagnostics verify outputs, identical
   non-grid supports, unique keys and all co-optimal study/group sets. The one
   2→4-node near-zero gross-design tie difference is retained, not hidden.
3. Source/provenance/config: inherited Beta model input checked against Table 2
   original text. It remains transported modelling/stated-intention evidence;
   neither a new observation nor target efficacy. Catalogue/hash checking is
   distinguished from possession of raw originals on a fresh checkout. The report
   now details finite priors, dependence assumptions, report channels and formulas.
4. Protocol/manuscript/ethics: fixed the misleading interpretation of `null_effect`,
   gross-vs-net study rankings and illicit-share averaging. Grid frequencies are
   not probabilities or preferences; EIG is distinct from action value. No formal
   ethics scope ruling, exemption, approval, cultural review or equity finding is
   claimed. Prior analyses and post-pilot amendments are dated transparently.
5. Figures/results: inspected both figures. Fixed the legend overlap on panel five;
   grid points and connecting lines do not imply continuous EVSI frontiers. Source
   values, policy examples, threshold, table counts and resolution deltas cross-check.
6. Final asset diff: Matplotlib SVG path lines had trailing whitespace. Normalised
   serialization in the exporter and regenerated all bound outputs. All numerical
   tables, scientific report values and PNGs are byte-identical to the preceding
   run; six SVGs parse and have no trailing whitespace.
7. Full-suite context contract: the new profile initially omitted the mandatory
   workstream-contract path. Restored the path within the existing 80,000-byte
   budget. Original failing evidence is preserved; tests and limits unchanged.

No unresolved critical/high implementation finding. Empirical identification,
external validation, distributional governance and formal submission readiness
remain explicit scientific/author gates, not passing software assertions.

## Qualification and repository publication

Final local and native outcomes are appended after execution. Exact-head hosted
checks must pass before guarded merge. Receiving-main jobs, graph submission and
artifact provenance must be read back independently. No unexecuted job is successful.
No requests, contacts, applications, registrations or journal submissions.


Final local macOS Python 3.15.1 acceptance: strict_all, reproduce, clean_package and
security passed in the original five-session run (sampled peak 728.2 MiB, exit 1
because of the context test). After correction, the focused cache rerun passed
1 test / 10 deselected, then the complete tests session passed 1008 / 5 capability
skips with 93% coverage (671.3 MiB, exit 0). No automatic retries or budget changes.
The first failure is preserved in outputs/engineering/m2-publication-local.log;
final tests in m2-publication-tests-final.log. Primary declared analysis completed
at 503.8 MiB, exit 0; output and 60-file package hashes verify. These sampled peaks
do not establish absence of a memory leak. Original source/target limitations and
formal ethics requirements remain unresolved exactly as stated in the report.

The associated PR is the native acceptance record for its exact reviewed head,
guarded merge, receiving-main qualification, graph snapshot and provenance. Those
outcomes are verified after this local commit, not assumed in advance.


Final post-SVG five-session qualification also passes in full on macOS Python
3.15.1: tests 1008 passed / 5 capability skips, 93% coverage; strict_all, reproduce,
clean_package and security pass. Guard peak 806.0 MiB, exit 0, unchanged 4096 MiB /
2400-second limits. Log: outputs/engineering/m2-publication-qualification-final.log.
Final refreshed analysis is bound to computational commit 7990b78, not the earlier
cc2fbd1 snapshot. All numerical CSVs, scientific report values and PNGs are unchanged;
SVG whitespace is normalised and XML parses. Final asset-inclusive diff-check passes.
Native publication acceptance: https://github.com/edithatogo/tobac/pull/58.


Hosted fixture correction: PR head e053dbe passed macOS tests but the existing
Windows job exposed OS-native backslashes in a new synthetic manifest. Corrected
only the test fixture to emit canonical POSIX manifest paths with as_posix();
production source validation and the rejection assertions remain unchanged.
This is a fixture correction, not new platform development. Scientific outputs,
computational commit 7990b78 and all previously passing local production checks
remain unchanged; the package binding is refreshed for the edited test file.
Focused runner/integration verification: 31 passed, peak 248.6 MiB, exit 0.
Ruff/format pass after wrapping the canonical-path comprehension. Native final-head
checks are required again; no failure is treated as a pass.
