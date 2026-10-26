# Bounded incorporation plan

- [x] Inspect live main 886fc08, shared issue #1 and the provided archive.
- [x] Verify source archive SHA-256 and identify useful reference-only files missing on main.
- [x] Preserve 18 tables/templates plus 28 exact inherited reference records; document transforms.
- [x] Add tests before the verifier and execute missing/altered/unsafe/overclaim cases.
- [x] Run 21 scoped tests, the actual archive comparison and compilation checks.
- [x] Match uploaded snapshot content to the tested local subtree.
- [x] Document current, prior-reference, generated, archive-only and pending work separately.
- [x] Confirm final receiving commit on main and post the publication receipt on issue #1.
      Receiving commit `5218d83`; publication comment on issue #1 (6382778234 acknowledgement,
      publication comment naming the guarded expected-head publication). Follow-up preservation
      content change: `090d07c` canonicalised one CSL DOI and `193f6bb` declared that transform,
      so the preserved subtree on current main differs from the pinned snapshot tree by exactly
      that tracked DOI case. A review of this track on 26 October 2026 (0 critical / 0 high /
      0 medium after the receipt and test fixes; see integration/incorporation_audit_review_20261026.json)
      re-confirmed the 19-file / 298-row / 28-record payload and the 21-test suite.

The final issue comment records guarded publication. Full archive migration, scientific
replay, M3 implementation and external execution are not closed by these preservation checks.
