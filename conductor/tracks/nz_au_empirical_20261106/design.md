# Design

## Data and execution architecture

Searchright protocol/receipts -> external immutable originals -> verified extraction ->
Polars/Arrow harmonisation -> existing evidence contract -> country-specific calibration ->
policy/health/equity simulation -> Innovate uptake/competition -> VOI -> sensitivity and
cluster discovery/prediction -> report and provenance manifest.

Use the existing archive-govt-nz producer and source-reference contract first; qualify
its selected external dataset destination and exact target rather than adding an archive
to tobac. Hugging Face is preferred when the user's existing repository, redistribution
rights and revision/readback semantics are verified. GitHub stores code and permitted
metadata; it is not permission to publish source PDFs or data. Preserve existing bindings.

Each record needs source/study/observation IDs, country, population, product, period,
unit, sampling design, denominator, uncertainty, covariance group, retrieval identity,
source hash, locator, extractor version, verified figure and admission disposition.
Each formula needs ID/version, reference or derivation, assumptions, dimensions,
input/output mappings and independent numerical check. Each run binds all IDs and hashes.

## Policy and health model

Use country-specific policy calendars and a shared interface. Start with one reconciled
NZ baseline and retail/cessation contrast plus Australian observational comparator.
Extend to all R06 domains through separately validated modules. Maintain a model/parameter
coverage matrix for every included predecessor. Combine compatible mechanisms; retain
alternative structures for incompatible mechanisms. More parameters alone are not better.

Choose cohort state-transition versus microsimulation from the required heterogeneity,
history dependence and available evidence. Couple tobacco/vaping transitions to disease
incidence, mortality and HR-QoL with explicit lags, competing risks, comorbidity and
cost perspectives. Report distributions and subgroup consequences before aggregation.

## Information, diffusion and sensitivity

Build the current-evidence posterior before adding a hypothetical measurement channel.
Compare no study, survey improvement, supply reconciliation, calibration, routine WBE,
combined designs and causal evaluation. Shared calibration errors cannot be averaged away
by collecting more samples. Evaluate study timing, adoption, budget, equity and irreversible
policy choices. Innovate must execute against a verified release; no local imitation labelled
as library integration. Add nested simulation/surrogates only with bias/convergence checks
against existing exact finite oracles. Do not sum overlapping EVPPI groups.

Sample joint probabilistic inputs using source-supported distributions and covariance.
Separate epistemic uncertainty, population heterogeneity and normative choices. Include
null/attenuated transport, lawful replacement, leakage, product substitution, measurement
bias, changing enforcement, missing data and country-specific policy combinations.
For clustering, keep country/time/replicate groups intact during splitting; fit preprocessing
only on training data. Assess stability and usefulness before supervised label prediction.
Report predictive performance separately from causal or scientific validity.

## Analytics workflow

Snakemake stages: validate_refs, extract_verified, harmonise, calibrate, simulate,
diffusion, voi, sensitivity, cluster_train, cluster_validate, report, verify_manifest.
Use content-bound prerequisites, atomic outputs, JSONL run/stage logs, deterministic seeds,
per-stage resources and captured stderr. Refuse stale/unverified inputs and incomplete outputs.
Keep heavy execution serial under scripts/run_bounded.py (4 GiB/40 minutes); retain Nox for
engineering checks. Snakemake adoption is expressly requested here and supersedes the older
no-additional-task-runner preference for analytics only. No silent runtime/lock promotion.

## Sequencing and complexity control

Foundation -> decision/protocol/source qualification -> one empirical vertical slice ->
policy/health expansion -> diffusion and extended VOI -> cross-model sensitivity/clustering
-> integration. Read-only source discovery can proceed during foundation work; model execution
requires qualified runtime and data. PSA and validation accompany each module, with the final
phase integrating them. Qualify Innovate early to expose compatibility risks before coupling it.

Preserve exact finite oracles. Introduce microsimulation, Bayesian hierarchies, surrogate VOI
or network diffusion only where the decision question and available evidence justify them.
Benchmark extra complexity against simpler models. Do not label supervised prediction of
simulation-derived clusters as independent evidence that population groupings exist.

Source refreshes produce new immutable editions, not overwritten inputs. Record publication,
observation and retrieval dates separately, data revisions/retractions and affected descendants.
The version census is repeated at promotion; a dated plan cannot guarantee perpetually latest
packages. Every candidate is installed and exercised in isolation before reference promotion.
