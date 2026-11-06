# Sensitivity and clustering — 6 November 2026

P5.1 adds an executable synthetic software qualifier; empirical Phase 5 remains incomplete.
No NZ/AU data, posterior, policy payoff or population subgroup is supplied to clustering.
No existing scientific source, inputs, canonical locks, M3 or native bindings changed.

## Implemented workflow

scripts/qualify_sensitivity_clustering.py uses maintained SciPy/scikit-learn APIs:

1. Independent-input Sobol first/total-order indices for f(x)=x1+2*x2, checked against
   analytical variance shares 0.2/0.8. A separate correlated normal PSA checks variance
   1+4+4*0.6=7.4 using 65,536 draws. The correlation is synthetic, not estimated; classical
   independent Sobol indices are not applied to it. These checks are not a global sensitivity
   analysis of the tobacco model and do not establish convergence for future models.
2. Independently seeded synthetic training/test features, with unique disjoint IDs and
   finite/nondegenerate validation. Scaling, KMeans candidate k=2/3/4 selection by silhouette,
   and 12 bootstrap stability fits use training data only. Adjusted Rand stability handles
   arbitrary cluster-label permutations. Weak silhouette/stability or undersized clusters
   return no_use before supervised fitting. Thresholds are fixture acceptance values,
   not validated empirical cluster-use criteria.
3. Logistic regression predicts the frozen discovery labels on separate test rows, compared
   with a majority classifier using balanced accuracy and log loss. A holdout missing
   discovery clusters is reported without those scores. Test rows do not influence scaling,
   k selection, bootstrap selection or classifier fitting. This evaluates imitation of the
   frozen clustering rule, not independent substantive truth or disease-risk calibration.
4. Polars CSV diagnostics, JSON summary and a hash manifest bind synthetic seeds/features,
   selected model parameters, code, candidate lock, qualification inputs, installed packages
   and outputs. The CLI refuses existing outputs. Logging and bounded resource receipts
   remain separate from empirical/scientific acceptance.

## Dependencies and typing

scikit-learn 1.9.1 was the current PyPI release with a cp315 macOS arm64 wheel. The new
isolated .venv-clustering3152 hash-installs the core reference lock plus this opt-in candidate;
it is actual Python 3.15.2, with no pandas/xarray. Initial installation had 41 packages;
the final candidate adds scipy-stubs/optype/numpy-typing-compat for 44. pip check passes.
SALib 1.6.0 requires pandas and was not installed. Nothing was promoted to shared profiles.
The local generated qualification-v2.lock/resolve/install logs are isolated candidate
evidence; a canonical new profile, Renovate coverage and hosted/release qualification remain
future integration work, not implied by this source-only candidate.

Strict typing initially exposed absent/incomplete external stubs. The maintained
scipy-stubs 1.18.1.1 is installed in the candidate. Repository declarations under
engineering/typings/sklearn and threadpoolctl.pyi cover only the exercised NumPy subset,
including integer-label widths and the two actual pipeline compositions. They do not
certify the complete libraries. Their naming exceptions preserve upstream X/class names;
no numerical test or type-checker rule was disabled. scipy-stubs' scalar-only ppf protocol
requires a narrow cast at the frozen-uniform boundary; analytical reference checks exercise
that call. No environment stub was edited. Initial type failures are retained as history.

Primary method references: [scikit-learn leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html),
[clustering evaluation](https://scikit-learn.org/stable/modules/clustering.html) and
[SciPy Sobol API](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.sobol_indices.html).
Five original methods/metadata responses are externally staged with hash readback in
phase5-source-receipts.json. Rights/durable archive admission remain separate; they are not
empirical tobacco inputs or a completed systematic methods review.

## Empirical sensitivity and clustering requirements

After Phase 0–4 pass, build a hash-bound ensemble with country, parameter-draw family,
scenario/model, action and seed identities. Preserve justified covariance across parameters
and observations. Use parameter, structural, prior, value/weight, horizon, missingness,
calibration, transport and policy-interaction scenarios; report regret, thresholds and
Monte Carlo error as well as expected outcomes. The existing value_sensitivity and M3 robust
envelope remain the reference paths. Correlated global attribution needs a justified
conditional/grouped method; independence cannot be silently imposed to obtain Sobol indices.

Freeze train/validation/test splits by underlying draw family, country/time and shared
source groups as appropriate; paired actions and reused seeds stay together. The synthetic
qualifier checks row IDs only: it is not a production group-split/admission validator.
Choose input features and transformations on training data, document scaling sensitivity,
bootstrap cluster stability and alternative distances/algorithms, and permit a no-use finding.
Any supervised predictor must use features available at intended prediction time, not the
outcomes used to construct cluster labels. Tune on training/internal validation only;
reserve independent grouped holdout for final evaluation, with imbalance and calibration
assessment. Predicting a frozen label is not external validation of whether clusters matter.
Simulation clusters are not causal effects or demographic/clinical policy target groups.

## Actual verification and remaining gates

The initial synthetic run passed with Sobol first-order indices 0.19997/0.79988,
correlated variance 7.35572, selected k=3, minimum bootstrap ARI 1.0 and held-out balanced
accuracy 1.0 versus majority 0.33333. The fixture is deliberately easy; these metrics are
software checks, not model performance estimates. First-run process-group peak 181.4 MiB.
The initial seven tests passed but a deliberately single-cluster holdout emitted metric
warnings. The implementation now explicitly withholds those scores and has a regression
case; no warning filter was added. Final logs/results are recorded at the terminal checkpoint.

Current candidate pip-audit reports no known vulnerabilities (exit 0; 93.9 MiB); this is
the installed candidate's advisory scan, not full-history publication/security acceptance.
Final affected selection passed 107 tests in 5.32 s with no warnings, at 396.1 MiB
sampled group RSS (final-tests.log). It includes all nine new tests plus existing value,
M3, integration and publication-boundary checks. Ruff and formatting pass for the qualifier,
tests and eight stub files. The final candidate strict type check passed with zero errors
and warnings at 406.5 MiB (typing-candidate-final.log).

Final synthetic packet: outputs/nz-au-phase5/qualified-v2, qualification-v2.log; exit 0,
153.3 MiB sampled group RSS. The numerical diagnostics retain the values above. Exact
script/lock/input/output hash readback passed. The manifest lists all 44 installed packages;
all were covered by pip-audit with zero known vulnerabilities and zero skipped packages.
Existing-output preservation is tested; earlier completed outputs/logs remain intact.

The existing audit environment does not install the optional clustering runtime. Its
strict check correctly fails with zero errors and seven missing-module-source warnings
(typing-final.log, exit 1). A type-only import probe confirms that this does not resolve
runtime-source availability. No warning/checker rule was disabled and no shared profile
was altered to conceal the missing packages. This is an open reference-profile integration
gate, distinct from the passing isolated candidate check. Do not describe this branch as
ready for default CI/release or promote the candidate without resolving it.

Next integration packet: use the existing integrator to add the approved clustering graph
to the appropriate engineering/qualification profile, regenerate source-bound locks and
Renovate coverage, expose a Nox/Snakemake route where appropriate, rerun that profile's
strict/security/package/CI checks and renew any affected native identity. Preserve the
currently frozen runtime owner's work. No full-suite, clean-package, hosted/native or
empirical success is claimed. Empirical clustering and cross-model joint PSA remain blocked by earlier
evidence and model acceptance; none of Phase 5's original plan rows is closed here.
