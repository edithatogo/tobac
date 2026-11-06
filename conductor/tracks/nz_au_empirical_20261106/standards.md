# Standards crosswalk

Checked 6 November 2026 against primary guidance. This is a targeted mapping, not a completed
item-by-item compliance audit or certification. Applicability and evidence remain to be filled
in task acceptance receipts. CHEERS is reporting guidance, not a methodological quality score.

| Guidance | Application | Required evidence |
|---|---|---|
| ISPOR–SMDM conceptualisation, report 2 | Decision problem, population, comparators, perspective, horizon, model choice and parsimony | Phase 1 conceptual diagram/estimands; Phase 3 justified mechanism and simpler-model comparison |
| ISPOR–SMDM uncertainty, report 6 | Parameter estimation, correlation, heterogeneity, structural uncertainty, PSA and research decisions | Source/distribution mapping, sensitivity and convergence receipts, decision-maker ability to delay/revise/commission research |
| ISPOR–SMDM transparency/validation, report 7 | Face, internal, cross-model, external and predictive validation | Separately labelled evidence for each applicable validation type; unavailable validation remains open |
| CHEERS 2022 | Transparent economic reporting, perspectives, assumptions, uncertainty, distributional effects, engagement and funding | Report checklist with exact sections, not a claim of validity or endorsement |
| NIST SSDF | Prepare, protect software, produce secure software and respond to vulnerabilities | Ownership, threat-informed controls, pinned provenance, secure CI, dependency review, findings/disposition and recovery |

Primary sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4207095/
- https://www.ispor.org/docs/default-source/resources/outcomes-research-guidelines-index/model_parameter_estimation_and_uncertainty-6.pdf
- https://www.ispor.org/docs/default-source/resources/outcomes-research-guidelines-index/model_transparency_and_validation-7.pdf
- https://doi.org/10.1016/j.jval.2021.10.008
- https://csrc.nist.gov/projects/ssdf

State-transition, discrete-event or dynamic model guidance is selected when the model type
is chosen; using all model types is not a best-practice requirement. VOI-specific, distributional
cost-effectiveness and systematic-review reporting guidance must be appraised in Phase 1;
this short crosswalk does not establish comprehensive methodological coverage.

SWE acceptance additionally retains existing strict typing/linting, schema contracts,
property/invariant and independent-oracle tests, focused regression tests, complete milestone
reproduction, immutable lock/input/output manifests, no secret logging, least-privilege CI,
atomic outputs, idempotent reads, controlled native writes and verified clean-package installs.
