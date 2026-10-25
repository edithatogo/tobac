# Product guidelines

## Voice
Write as a research analyst accountable to a decision-maker, not as an advocate.
State the decision, the evidence, the assumption and the remaining uncertainty in
that order. Prefer plain declarative sentences. No rhetorical framing, no urgency
language, no emotive descriptors attached to a policy position.

Second person is for instructions only. Findings are reported in the third person
or impersonally ("the model implies", "the estimate is unidentified").

## Non-negotiable claim discipline
- Never let configuration, a checksum, a schema, a passing import or an agent
  acknowledgement stand in for successful execution or scientific validity.
- Distinguish, in wording and in structure, four things: observed data, model
  assumptions, normative choices, and extrapolation. They must not be blended in
  one sentence that reads as a finding.
- A no-study, null-effect or non-identification result is a permissible and
  reportable outcome. Never phrase a result so that it implies the funded or
  policy-favoured answer was expected.
- Forecasts and posteriors are not new observations. Do not describe a
  conditional result as if it were evidence.
- Say "not executed", "not obtained" or "open" rather than implying completion.
  Where a check was run in a reduced mode, name the mode.
- Do not attribute a claim to a citation, archive or third party that has not been
  verified against the actual source.

## Terminology
- Use the established identifiers: EVPI, EVPPI, EVSI, ENBS, action archetype,
  state identifier, evidence packet, VOI, receipt, manifest.
- Name states by their physical or latent meaning, never by row index.
- One concept keeps one name across code, JSON keys, receipts and prose. If a
  rename is needed, it changes everywhere in the same change.
- Do not introduce a synonym for an existing term to make prose read better.

## Numbers and uncertainty
- Report a point estimate only with its unit, population, product coverage and
  observation date, or with an explicit statement that one is not identified.
- Never present a derived quantity to more precision than its inputs support.
  Preserve the calculated value in machine-readable output; round only for prose.
- Serialise numbers with `allow_nan=False`; non-finite values are a defect, not a
  formatting choice.
- Where a comparison against a predecessor exists, state the tolerance and the
  observed difference rather than "matches".

## Output surfaces
- Primary surface is the CLI plus JSON/CSV receipts. There is no dashboard to
  hide an assumption in: every headline number must be traceable to a file.
- Any new output directory must refuse to overwrite a non-empty one.
- Receipts name the commit, the input hashes, the command actually run and the
  scope of what the check does and does not establish.
- Error messages state what failed and what the caller must supply. No silent
  fallback, no default that changes a scientific input.

## Documentation
- Lead with what the artefact is and is not, then the method, then the result.
- Keep a short "open gates" list current. Removing an item requires evidence,
  not optimism.
- Do not restate a number in prose that the linked receipt already owns; link it.

## Accessibility and readability
- Tables and lists over dense paragraphs for anything comparative.
- Define an acronym at first use in each document; documents are read standalone.
- Assume a reader who will check the arithmetic.
