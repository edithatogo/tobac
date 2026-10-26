# Active research tracks

## Scientific ecosystem modernisation

**Status: [~] In progress — implementation/review authorised 26 October 2026.**
Track: `conductor/tracks/scientific_ecosystem_20261025/`.

The macOS implementation adds parameter serialization, stage-bound replay/recovery,
required-context guards, clean installed-package qualification, explicit Voiage/JAX EVPI,
native interchange/tool probes, mutation boundary assertions and security/provenance gates.
PR #43 is merged and the macOS implementation/review and native provenance gates pass.
C3/C4/C6 domain interchange is implemented and locally qualified against the current
Voiage artifact (c347f82); PR #41 retains its separate future producer migration.
PR #47 records 15 successful hosted checks for the domain boundary; its final
receipt update receives the same gates before guarded merge. Only the upstream
managed parser Python 3.15 runtime gate remains open. The supported native dependency-submission route and graph readback pass.
Review: `docs/reviews/2026-10-26-conductor-autonomous.md`.
Execution: `integration/ecosystem/verification_20261026.json` and
`integration/ecosystem/interchange_20261026.json`.

## Completed work

Seven completed tracks were reviewed and moved out of this active registry on 26 October.
See [the archive index](archive/index.md) for their specifications, plans and dated receipts.
The earlier longitudinal integration archive remains preserved there.

## Research gates

[Open research gates](research-gates.md) retain decision scope, source conflicts,
measurement/covariance, transport, empirical calibration and permissible-use requirements.
M1/M2/M3 computational results are conditional research, not a current national posterior
or a commissioning recommendation. Source/forecast identities and data-once guards remain.

## Deferred development

[Roadmap](roadmap.md): non-macOS qualification, optional advisory promotion and prior
mutation/style-policy follow-ups. Existing hosted checks and full-SHA pins remain required.
