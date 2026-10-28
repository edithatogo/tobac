# Post-primary robustness results

Executed 13-specification challenge grid, computed with the source commit recorded in
[report.json](report.json). [Current manuscript](../../docs/research/M2_MANUSCRIPT.md),
[protocol](../../docs/research/M2_READINESS_PROTOCOL.md),
[supplement](../../docs/research/M2_MANUSCRIPT_SUPPLEMENT.md).

- decisions.csv: 1625 matched profiles, all current co-optimal actions and min/max regret over baseline ties.
- grouped_evppi.csv: 11375 finite overlapping-partition values, not additive measures.
- study_value.csv: 9750 gross EVSI values before any actual study cost.
- scientific_information.csv: 1170 target-specific EIG rows; no preference-distribution interpretation.
- summary.csv: 13 deterministic finite-grid comparisons, not probabilities of correctness or social preferences.
- manifest.json:actual source/configuration/output hashes for numerical files.

The baseline exactly matches 125 primary decision rows,875 grouped-information rows
and 750 study rows at their saved numerical precision. The primary snapshot is retained.
Regret and information are normalised model scores, not NZD/QALYs or observed NZ effects.
The half_information identifier means 50% state-independent report replacement; it
is not a claim that EVSI or EIG is halved. Combined stress is not a worst-case bound.

README is explanatory packaging added after execution and is not itself listed as a
computational output. The publication-package manifest binds it separately.
