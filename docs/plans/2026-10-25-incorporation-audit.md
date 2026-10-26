# Incorporation audit and preservation plan

Base: live main 886fc08929f8e4e7e34fb6443bbf81545e52c3db.
Goal: keep earlier useful evidence accessible without overwriting current science.
Architecture: copy selected tables/templates into evidence/prior_work/v2.9.0 with original paths, source roles and source/archive hashes. Retain M3 ownership and live evidence contracts. Use standard-library integrity checks, not a new inference engine.

- [x] Inspect live branch, coordination issue, source tree and attached archive bytes.
- [x] Identify archive-only measurement, parameter, survey and costing materials.
- [x] Select reference-only imports; preserve fields and numerical values; normalise CRLF only.
- [x] Test integrity validator before implementation; reject omissions, mutations, unsafe paths and false current-data claims.
- [x] Validate real payload and stage additive entries.
- [ ] Publish with expected-head check; record the receiving commit in Conductor.
- [ ] Verify remote tree hashes and coordinate receiving commit.

No scientific rerun or current empirical recommendation is created by copying evidence. M3, dependency locks, hosted execution, obsolete manuscripts and bulk legacy code have separate statuses.
