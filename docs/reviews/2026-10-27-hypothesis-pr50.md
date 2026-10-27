# Review Report: Hypothesis PR #50 and complete ecosystem lock binding

## Summary

Qualify Hypothesis 6.170.9 on Python 3.15.1, preserve all other resolved package
versions/markers, and close an uncovered ecosystem dependency-input binding gap.
PR #50 is updated through a normal fast-forward, retaining its original commit and
current main. No force push, scientific dependency change or security waiver.

## Verification checks

- [x] Plan compliance: regenerate all four profiles through the real uv helper.
- [x] Style compliance: Ruff and formatting pass for the changed Python files.
- [x] New tests: ecosystem receipt binds its source, included Voiage inputs and rejects undeclared includes.
- [x] Existing checks retained: committed-source snapshot identity is unchanged.
- [~] Final qualification: rerun full tests after committing lock bytes, then require
  existing hosted checks and guarded receiving-main verification; actual results
  are linked from PR #50 and integration/hypothesis_pr50_20261027.json.

## Iterative self-review

The diff exceeds 300 lines because four generated locks contain the release's hash
inventory. Reviewed declarations separately from genuine resolver hash output;
all non-Hypothesis package/version/marker declarations equal main b012758. The sole
version change is 6.170.8 to 6.170.9, consistently declared in reference/test inputs.
Receipts are genuine generator output, not hand-edited success assertions.

The previous ecosystem receipt bound only six common inputs and omitted its own
source and nested Voiage input. An explicit per-profile input map retains the exact
runtime/audit/Voiage bindings and adds the missing ecosystem files. Five additional
cases cover valid ecosystem receipts, three changed-input rejections and a closed
nested include graph. Existing path/symlink/duplicate-key/failure cleanup guards stay.
No second resolver, generic environment framework or changed scientific calculation.

Forty-three focused lock tests passed. The first full pass reached 908 passed/five
capability skips with one deliberate failure because dependency_snapshot rejects
uncommitted lock bytes. Quality, whole-source typing/lint/format, security,
reproduction, packaging and mutation passed. Commit the reviewed candidates and rerun
without weakening that identity gate. Initial failure logs are retained.

Conductor summaries now reference PR #51's actual receiving-main acceptance,
108-file Ruff coverage and resource controls. Optional mutation follow-up uses its
12 survivors; old counts remain dated evidence. Draft #41 and scientific/data gates
remain separate. The external managed parser remains open, so the track is retained.
