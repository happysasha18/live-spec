# Prover record — 2026-08-25 class-hunt-rule14-pointer

PUSH-REVIEW

Range: 3ceafe3e..4a8a0bee (2 commits)
- 85292696 Wire rule 14's cross-reference to class-hunt.md (fast-follow)
- 4a8a0bee Skill-review record for the rule-14 cross-reference fast-follow

Files read: full diff of 85292696 (2 files, 4 insertions / 4 deletions);
`skills/live-spec-base/SKILL.md` lines 216-229 (rule 14, current and pre-diff via `git show`);
`tests/test_class_hunt.py` in full; `skills/director/references/class-hunt.md` and
`skills/build-pipeline/SKILL.md`'s bug entry (both confirmed current, matching the sentence's
claim that both are live homes today).

Checks run: this is the deferred fast-follow flagged in
`docs/prover/2026-08-25-class-hunt-director-home.md` — rule 14's cross-reference sentence was
deliberately left pointing only at `build-pipeline/SKILL.md` when `class-hunt.md` first landed,
since an independent reviewer on a separate concurrent task had correctly rejected an earlier
draft that wired this same sentence to the new file while it was still under adversarial review.
Now that `class-hunt.md` is itself committed and stable (three review rounds, `3ceafe3e` on
`origin/main`), this range completes the wiring: the sentence now reads "The full four-move law's
homes are `skills/director/references/class-hunt.md`, `skills/build-pipeline/SKILL.md`'s bug
entry, and the spec at INV-124."

Independent adversarial review specifically re-checked the exact defect that sank two earlier
drafts of this same sentence — a Markdown code span split across a line-wrap, rendering with a
corrupted stray space in the path (per CommonMark's line-ending-collapse rule). Confirmed by
reading raw file lines directly (not a rendered view): both new code spans sit entirely on one
physical line each. No repeat of that defect. Also confirmed: no test pins either the old or new
phrasing of this sentence (so no coverage regression, though also no new coverage added — a
one-sentence wiring fix, not a behavior change); `test_class_hunt.py`'s own "Homes:" docstring
line, previously stale since Director's home first landed without this line being updated, now
lists all five real homes accurately, closing a genuine, if minor, documentation gap the reviewer
flagged as a real fix rather than cosmetic churn.

Independently: `python3 -m pytest -q tests/test_class_hunt.py tests/test_traceability.py
tests/test_live_spec_base_body_thinned.py` — 202 passed, 3 skipped (pre-existing, unrelated), run
independently by both the implementer and the reviewer with matching results.
`scripts/spec-style-lint.py --tier universal skills/live-spec-base/SKILL.md`: 0 errors, 8
pre-existing warnings unchanged in count and location. `guardrails/check-pin-drift.sh`: exits 0,
no FAIL lines. Line counts unchanged both files (592 and 180 respectively — a clean line-for-line
replacement in each).

Findings: none. This closes the last open thread from today's class-hunt work.

This closes batch-2b's 12th and final item completely — the fact now has a real home in Director
AND a live cross-reference from the base rulebook naming it, matching the precedent already
established for `work-kind-table.md`'s pointer from rule 15. Полоса B item 5 (batch-2b) has no
remaining open threads. Next: item 6 (the build-pipeline transitional adapter), the largest
remaining piece of the whole plan.

Blocking: none
