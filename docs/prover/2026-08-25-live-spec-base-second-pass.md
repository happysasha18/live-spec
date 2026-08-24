# Prover record — 2026-08-25 live-spec-base second extraction pass

PUSH-REVIEW

Range: uncommitted working tree on `director/2026-08-21-package-1` (worktree
`/private/tmp/ls-director/wt`), two modified files, 70 insertions / 25 deletions. Reviewed
against `HEAD` via `git show HEAD:<path>`. Nothing committed, amended, reset, or edited by
this review except this record.

Files read: `git diff -U6 -- skills/live-spec-base/` in full, every hunk of both files;
`skills/live-spec-base/SKILL.md` in full at both `HEAD` (607 lines) and the working tree
(606 lines), read top to bottom as a fresh loader would, not hunk-in-isolation;
`skills/live-spec-base/references/worked-examples.md` in full at both revisions (53 → 99
lines); `tests/test_live_spec_base_body_thinned.py` (the ratchet, `CURRENT_MAX_LINES` at
line 50); `scripts/spec-style-lint.py` header and check table; `docs/spec-style.md` R15;
`docs/lenses.md` header and its 50 code-keyed entries; `tests/test_convergence_locks.py:74-110`
(which documents gate the style floor at zero); `docs/prover/2026-08-25-parts-map-lint-fixes.md`
and `docs/prover/2026-08-24-checkpoint-mechanism.md` for record shape.

Checks run: every number below re-derived by this reviewer directly, not taken from any
worker's report.

- `wc -lc` on both revisions. `SKILL.md` went **607 lines / 52,202 bytes → 606 lines /
  52,145 bytes**: −1 line, −57 bytes (~14 tokens). The brief's stated "606 → 606" is wrong
  on the before-side by one line; the "essentially no reduction" headline is otherwise
  accurate. `worked-examples.md` grew 53 → 99 lines / +1,606 bytes.
- Per-hunk byte accounting, computed from `git diff -U0` by script. Eleven edits. **Six grew
  `SKILL.md`**: rule 2 **+32**, rule 9 **+13**, rule 17 **+83**, rule 18 **+8**, rule 31
  **+10**, rule 34 **+60**. Five shrank it: rule 13 −55, rule 22 −6, rule 24 −1, rule 33
  −126, rule 35 −71. The nine edits that replaced text with a pointer sentence **net +144
  bytes**; the two edits that deleted without adding a pointer (rules 33, 35) net **−197
  bytes**. The entire reduction, and then some, came from the two edits that did not follow
  the instructed pattern.
- `python3 -m pytest tests/test_live_spec_base_body_thinned.py -v` — **6 passed**, all six
  sub-tests, run fresh with the tree stable.
- The full 16-file surface named in the brief — **511 passed, 5 skipped**, 13.72s. No failures.
- `python3 scripts/spec-style-lint.py --tier full skills/live-spec-base/SKILL.md` — the
  script does accept a skill-file path. **15 errors now; 14 at `HEAD`.** The one new error is
  a **`scissors`** ERROR at `SKILL.md:210`, reproduced identically under `--gate`. Same lint
  on `worked-examples.md`: clean at both revisions.
- Heading sweep of `worked-examples.md`: sections run thinking-rule, 2, 9, 13, 17, 18, 22,
  23, 24, 31, 32, 33, 34, 35 — strictly ascending, **no duplicate `## Rule N` heading, no
  truncated or garbled text, no cross-rule splicing**. Line-length sweep (`awk length>110`)
  against `HEAD`: no line broke, doubled, or lost a word; the only width change is `SKILL.md:80`,
  a new over-width line the rule-2 worker left unrewrapped.
- Every removed line judged against its surrounding paragraph in the *current* file, not the
  diff hunk. All eleven removals are genuinely non-binding — dated citations, worked
  illustrations, or restatements whose normative content survives verbatim in the rule's own
  bold lead-in or body. **No normative clause, no `INV-` code, and no definition was removed.**
  Rule 17's `(2026-07-05: money yes, deletion yes, a push no.)` and rule 24's closing analogy
  looked closest to the line; both are fully restated at `SKILL.md:259-262` and `348-350`
  respectively. That check is clean.

Findings: the concurrency risk did not materialize as corruption — no race damage of any
kind is present — but the pass has one register regression, four pointer-integrity defects,
and a method error that explains the null result.

- **`SKILL.md:210` — new `scissors` register ERROR, introduced by this change.** The rule-13
  pointer reads "Why the read-back, **not that mechanical check**, is the load-bearing
  defence is written out under rule 13 in …". That is the contrast frame that names a thing
  by denying its neighbour — `docs/spec-style.md`'s globally and permanently banned form,
  and the pack's most foundational file now carries one where it did not before. It reds no
  test only because `tests/test_convergence_locks.py:74-110` floors the style gate at zero
  for `PRODUCT_SPEC.md` and `ARCHITECTURE.md` alone; `SKILL.md` has no such floor, so the
  regression is invisible to the suite. Recommended fix: "Rule 13's own worked case for the
  read-back's standing is written out under rule 13 in …" — no contrast frame. Recommended
  follow-up, separately: give `SKILL.md` a style floor at its current 14, so the next one reds.
- **The nine dated citations went to the wrong home.** `docs/spec-style.md` R15 states that
  provenance "lives in a docs home keyed by the rule's code (`docs/lenses.md`), the JOURNAL,
  or a dated prover record". `docs/lenses.md` opens by naming itself "The provenance home for
  the pack's rules … the date and the motivating case that gave each rule its shape … keyed
  by the rule's code". `references/worked-examples.md` is, by its own preamble, the home for
  *worked cases*. Six of tonight's eleven new sections contain no worked case at all — only a
  dated stamp — and `docs/lenses.md` currently holds **zero** entries for any of the nine
  codes involved (INV-207, INV-237, INV-302, INV-247, INV-98, INV-183, INV-189, INV-135,
  INV-108, all checked individually against its 50 entries). This is the pass's central
  method error, and it is also why it saved nothing: `docs/lenses.md` is a repo doc that no
  skill session ever loads, so provenance filed there needs **no pointer sentence at all** —
  the body simply states the mechanism in present tense. That is exactly what the rules 33
  and 35 edits did by accident, and they produced 197 of the 259 bytes saved.
- **`worked-examples.md:82-83` — orphaned, misfiled, and a sentence fragment.** The rule-33
  worker moved "The owner's word, 2026-07-18, after a fresh web review caught self-referential
  defects the in-context 2.7.0 prover missed." into the reference file and added **no pointer**.
  The pre-existing pointer at `SKILL.md:527-529` covers a different clause — the 2.7.0 breach
  story — not the clean-context-review-record paragraph at `SKILL.md:533-536` that this
  citation actually grounds. So nothing in `SKILL.md` points a reader at it, and sitting under
  the heading "Rule 33 — the 2.7.0 release's own breach" it now reads as provenance for the
  breach rather than for the gate. It is also a bare fragment with no main verb.
- **`worked-examples.md:99` — orphaned, and it falsifies an existing pointer.**
  `SKILL.md:553-556` enumerates exactly two items: "This rule's worked failure … **and** the
  note on the script … are **both** written out under rule 35". Three paragraphs now live
  there. "both" is stale, and the third paragraph has nothing pointing at it.
- **`worked-examples.md:18` duplicates `SKILL.md:79` verbatim** — "The original term is free
  to trail in parentheses like any anchor." — a breach of the pack's own rule 4, one canonical
  home per fact, introduced by this change. The rule-2 worker copied the host sentence along
  with the citation instead of moving the citation alone. The pointer at `SKILL.md:80` compounds
  it: it promises "Its dated origin", but the entry leads with a non-dated sentence already in
  the body, and "Its" reads as belonging to *the original term* rather than to the no-calques rule.
- **`SKILL.md:355-356` and `364-366` — rule 24 now carries two pointers to the same file.**
  The pre-existing "See [references/worked-examples.md] for the per-kind illustration of both"
  already sends the reader there; the new "The closing analogy … is written out under rule 24
  in [references/worked-examples.md]" sends them again, ten lines later, to the same section,
  for a net saving of **one byte**. Recommendation: drop the second pointer and let the first
  absorb the moved analogy.
- **Pointer wording diverged four ways across the four workers** — "Its dated origin is in
  rule N's entry in …" (rules 2, 31, 34), "The dated citation behind this criterion is in rule
  17's entry in …", "The worked illustration of … is written out under rule 9 in …", "The
  owner's dated word behind this rule is written out under rule 22 in …". The established
  pattern already in the file (rules 23, 32, 33, 35) is "… is written out under rule N in …
  Open it when …". Two workers invented a second family. This is the real cost the four-way
  split imposed — not corrupted bytes, but four uncoordinated dialects of one convention in
  the file that rule 3 ("one surface = one name, everywhere") governs.
- **The ratchet was not tightened.** `CURRENT_MAX_LINES` is still 615 with the file at 606,
  and `tests/` is untouched in this diff. Rule 22's own named mechanism — "a cap that only
  ratchets down" — went unapplied, so nine lines of slack remain and tonight's gain is
  unlocked. Whatever else is decided, the cap should go to 606 in the same commit.
- **Coherence read, full file, fresh-loader pass: the rulebook still reads correctly.** Every
  rule 1-35 (30 retired, stated at `SKILL.md:58`) stands as a complete thought. No dangling
  reference, no rule left as an incomplete sentence, no orphaned "It is written out …" whose
  antecedent was cut with it. The four pointer-integrity defects above are all on the
  *reference* side; the rulebook body itself is sound.
- **On whether "almost nothing further to extract" is credible: no — the workers were both
  too cautious and pointed at the wrong target.** Three things they left: (1) The four slices
  were 1-9, 10-19, 20-27, 28-35, so **6,102 bytes of `SKILL.md` were in nobody's scope** — the
  frontmatter, the preamble at lines 8-18, the two pointer sections at 20-36, the rule of
  thinking at 38-54, "Work that belongs elsewhere" at 571-579, the settings ladder at 581-593,
  and the closing roster at 595-606. `SKILL.md:578-579`, "That decided sentence closes the
  recurring scope question for good", is pure meta-commentary with zero normative content and
  was never looked at by anyone. (2) The last remaining dated provenance in the body,
  `SKILL.md:577` ("recorded 2026-07-16"), sits in that unowned region and is the same class of
  content four workers spent the night extracting. (3) The real cost is structural, not
  citational: `SKILL.md:149` is a **1,566-byte single line** — 3% of the file in one
  sub-rule — and rules 6, 7, 14, 19, 29, and 31 each run 20-50 lines of dense normative prose.
  Meaningful thinning has to come from there or from moving whole rules to reference modules,
  under a plan, not from harvesting parentheticals. A 42K-token eager cost will not be moved
  by dated citations; they are worth roughly 800 bytes in total across the whole file, which
  is the ceiling this method was ever going to hit.

Blocking: yes, three items, all cheap to fix and none requiring a redesign. (1) `SKILL.md:210`
introduces a `scissors` register ERROR into the pack's foundational file — a permanent, global
ban — and the suite cannot see it; reword before commit. (2) `worked-examples.md:82-83` and
`:99` are orphaned additions no pointer reaches, and `:99` additionally falsifies the "both"
at `SKILL.md:553-556`; either add pointers or, preferably, move both to `docs/lenses.md` keyed
by INV-237 and INV-302 and leave the bodies as they now stand. (3) `worked-examples.md:18`
duplicates `SKILL.md:79` verbatim, breaching rule 4; delete the duplicated sentence from the
reference entry. Recommended alongside, not blocking: drop the redundant second rule-24 pointer
at `SKILL.md:364-366`, ratchet `CURRENT_MAX_LINES` to 606, and — before any third pass — re-home
the provenance to `docs/lenses.md` per R15 rather than extending the pointer pattern, since the
pointer pattern is byte-negative for short citations by construction and this pass measured it.

## Orchestrator's decision: reverted, not fixed-forward

`git checkout -- skills/live-spec-base/SKILL.md skills/live-spec-base/references/worked-examples.md`
— both files restored to `HEAD` (`bd303913`). This record ships alone; no code/skill change
lands from tonight's fourth attempt at the live-spec-base install-cost item.

Reasoning: the three blocking defects above are individually cheap, but the review's byte
accounting proves the underlying strategy — extracting short dated citations into
`references/worked-examples.md` behind a pointer sentence — is byte-negative by construction
for anything shorter than the pointer itself, and the file's own real weight (SKILL.md:149's
1,566-byte single line; rules 6/7/14/19/29/31 at 20-50 dense lines each) was never in scope
for any of tonight's four workers. Patching the three defects would ship a change that is
net near-zero at best and still points at the wrong home (`docs/lenses.md`, not
`worked-examples.md`, per R15) — worth doing once, correctly, not worth doing twice. This
matches this session's own §5.16 rule (scope local verification to a change's reach) in
spirit: a fix this narrow doesn't answer the question the owner actually asked.

**Carried forward to the handoff, not closed:** live-spec-base's eager-load cost (~13K
tokens) is real and the easy 800-byte ceiling on dated citations doesn't move it. A real fix
needs one owner, one sitting, and a different design: either compress the dense normative
rules themselves (rules 6/7/14/19/29/31, and the 1,566-byte rule-7 sub-rule specifically) or
restructure which rules a given skill invocation actually needs eagerly versus which could
gate on the skill being called at all — a bigger architectural question this session did not
have the room to answer safely tonight. Recommend a dedicated future session, single-owner,
starting from this record's findings rather than re-deriving them.
