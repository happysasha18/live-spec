# Skill review — live-spec-base (rule 32 rewritten, rule 7's four restorations, the retired number named at the head)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-12
Reviewer: skill-creator (Anthropic), run by a fresh reviewer with clean context. It authored neither
the rewrite nor the restorations, and it wrote no file but this record. Base rule 33 asks for that
freshness.

Verdict: passes as a skill. The frontmatter description still agrees with the body, all ten of rule
32's requirements survive the rewrite word for word, every pointer inside the changed text resolves,
and neither lint reads a coined word or a contrast frame in the added lines. Three findings are
recommendations. Two ARCHITECTURE.md pins into this file went five lines stale under the day's growth
and stand green only on an accidental word match, and rule 32's new size level is held by no machine
while rule 7's is. Neither blocks the push.

## What changed

Two commits in the range `e8900d9..HEAD` touch this file.

`0ac3b19` rewrote base rule 32, the release-tier law (SPEC INV-217). The body fell from 2,205 bytes to
1,449, measured on the live file at lines 560-574. What went: the three worked examples (the 1.0.0
major, the row-247 inbox-remote minor, the patch example), the dated provenance note naming the
owner's 2026-07-17 ~15:45 ask, the sentence about earlier releases picking their number by feel, and
the closing sentence about why the rule is written now. What stayed: every normative sentence, and the
2.0.0 boundary case.

`e17eea9` added a sentence at the head of "The shared rules" naming rule 30's retired number, and put
four small restorations back into rule 7 — the lead-in that names the parallel-lanes bullets as one
family, the phrase "convergence point" on the shared document, the pointer to `scripts/open-lane.sh`'s
own on-disk preconditions, and the actor on the independence-judging sentence.

## Findings

1. **All ten of rule 32's requirements carry, verbatim.** Reviewed and clear. The reviewer opened
   `.live-spec/batch2-s1-rule32-2026-08-12.md`, took its ten quoted requirement lines, and searched
   each against the rewritten rule at lines 560-573. Every one is present with its wording untouched:
   the head question about host cost, the sentence saying what the number reports, the patch clause,
   the two-sentence minor clause with its catch-up walk [INV-91], the major clause with its four
   earning cases, the dated `MIGRATION.md` chapter sentence, the patch-by-default pair, the
   held-by-no-machine judgment sentence, the minor-versus-major sentence with its design-review
   standing [INV-141], and the 2.0.0 boundary sentence. No requirement is missing a carrying sentence.
   The two prohibitions inside requirements 8 and 9 reach the same actors in the same cases, since
   their words did not move. Cross-checked against the spec: all seven acceptance criteria at
   `PRODUCT_SPEC.md:6588-6598` still find their sentence in the shortened rule, and criterion 7 —
   home the rule in the base rulebook, in build-pipeline's commit-and-show step, and in the spec —
   still holds on all three homes.

2. **Two ARCHITECTURE.md pins into this file are five lines stale, and the pin gate passes them on a
   word that means nothing.** Recommended repair, two line numbers. `e8c4a3a` moved thirteen pins for
   the day's rule-32 shrink and rule-7 growth and left two behind.
   `ARCHITECTURE.md:88` pins `skills/live-spec-base/SKILL.md:195` for rule 7's worker-restore sub-rule
   (INV-298); that sub-rule now opens at line 200, and line 195 is the tail of the worktree-isolation
   bullet. `ARCHITECTURE.md:89` pins `skills/live-spec-base/SKILL.md:599` for rule 35 (INV-302); rule
   35's head is at line 604, and line 599 sits inside rule 34. Both are off by exactly the five lines
   `e17eea9` added above them, three for the head sentence and two for the rule-7 lead-in.
   `guardrails/check-pin-drift.sh` reports green over 209 pins, because its five-line window finds one
   naming word of four characters or more: the word "holds" on line 195, from "a lane holds open", and
   the word "session" on line 601, from "a session never designs a fix". Neither word is about the
   pinned thing. The repair is `:195` to `:200` and `:599` to `:604`; the gate's own tolerance rule is
   a separate question for its owner.

3. **Rule 32's new level is held by no machine, while rule 7's is.** Recommended. Batch 1 locked its
   gain: `tests/test_compaction_discipline.py::test_rule7_batch1_locked_its_level` asserts rule 7's
   body stays under 5,477 bytes and asserts the restored pointer sentence is present. Batch 2 shipped
   no such lock. A grep of `tests/` and `guardrails/` for the rule-32 figures finds nothing, and
   `.live-spec/batch2-verdicts-2026-08-12.md` names no lock as owed. Rule 32 can grow back to 2,205
   bytes and every gate stays green. The same test file also leaves three of rule 7's four
   restorations unheld — only the `open-lane.sh` pointer sentence is asserted, and the lead-in, the
   phrase "convergence point" and the restored actor are not.

4. **The head sentence lands where a reader meets it, and it agrees with the body's shape.** Reviewed
   and clear. "Rule 30 was cut whole from this rulebook; its number is retired and stays open" stands
   directly under the `## The shared rules` heading, before rule 1. The body holds 34 numbered heads
   running 1 to 35 with 30 absent, and the frontmatter description says thirty-four rules in the body,
   so the count, the numbering and the new sentence agree. This closes finding 1 of
   `docs/skill-review/2026-08-12-live-spec-base.md`, which said no sentence in the skill told a reader
   why the numbering had a hole. The sentence travels to an adopting host, which the earlier record's
   three other homes did not.

5. **Every term in the added text is resolved before it is used, with one term stretched.** Reviewed,
   with a note. "A lane" and "the pen" are defined in the glossary at lines 66 and 68, well above rule
   7. "The fence" is rule 7's own head, immediately above the lead-in that borrows it. The phrase
   "convergence point" is now this file's first use at line 183, about 185 lines above the convergence
   principle at rule 22, but the clause carries its own gloss — a convergence point the pen reconciles
   at integration — so a reader is not left holding an unexplained name. The term is established pack
   vocabulary, appearing in the same sense in `skills/product-prover/SKILL.md:837` and
   `skills/build-pipeline/SKILL.md:582`.

6. **No pointer in the changed text dangles.** Reviewed and clear, each looked up. `scripts/open-lane.sh`
   exists and its header does state what it expects on disk, in a Usage block and a Preconditions
   block, so the restored sentence tells the truth. `MIGRATION.md` exists at the repository root.
   Every code named in the changed lines resolves to a Formal-index row in `PRODUCT_SPEC.md`: INV-217
   at 8098, INV-91 at 7972, INV-141 at 8022, INV-49 at 7930, INV-105 at 7986, INV-214 at 8095, E-13 at
   7859, T-18 at 8216. `skills/build-pipeline/SKILL.md:471`, the commit-and-show step's paraphrase of
   this rule, still reads true against the shortened text.

7. **One live pointer to the cut rule survives outside this skill.** Carried forward, still open.
   `MIGRATION.md:125`, in the 2.0.0 chapter, tells a host the method rule is rule 30 in
   `skills/live-spec-base/SKILL.md`. The earlier record named it on the same terms. The new head
   sentence sharpens the contradiction, since the rulebook now states plainly that the number is
   retired while the migration chapter still sends a host to it.

## The measures this review was held to

The census reads `skills/live-spec-base/SKILL.md` at 68 findings after the two commits — 54 sentences
past the word cap, 14 style findings, no register findings — against 70 before, so the rewrite took
two over-cap sentences out and added none. The file measures 64,728 bytes against 65,191 at
`e8900d9`, a fall of 463, which matches the 72,929-to-72,466 figure the batch's own commit records for
the narrower body. Rule 32's body measures 1,449 bytes on the live file, matching the figure the
rewrite claims.

Commands run and their results: `python3 -m pytest tests/test_release_tier_rule.py
tests/test_clean_context_review.py tests/test_resume_rederive.py` — 19 passed;
`python3 -m pytest tests/test_request_classifier.py` — 14 passed, including
`test_base_description_counts_the_rule`, which derives the count from the body and allows the single
hole at 30; `python3 -m pytest tests/test_compaction_discipline.py` — 11 passed;
`bash guardrails/check-skill-loadability.sh` — OK, 11 skills load, named, versioned, negative-scoped;
`bash guardrails/check-pin-drift.sh` — OK over 209 pins, green for the reason finding 2 gives;
`python3 guardrails/check-language-rules.py` — OK, 66 rows scanned, no match;
`python3 scripts/preshow-lint.py` and `python3 scripts/preshow-register-lint.py` over the range's
added skill lines — both clean, so the added text carries no banned contrast frame and no coined
metaphor. The installed copy at `~/.claude/skills/live-spec-base` is byte-identical to the repository
copy.

One measure outside this skill's subject, found while running the gates and reported so it is not met
cold at the push: `python3 guardrails/check-doc-findings-bound.py` reds on `guardrails/README.md`,
risen from 48 to 55 findings under the fourteen lines this range adds to it. No skill file is above
its record.

## What the orchestrator did with this record

Finding 2 was verified at the seat and repaired in the same landing: `ARCHITECTURE.md:88` now pins
`:200` and `ARCHITECTURE.md:89` now pins `:604`, and the freeze baseline was rebuilt. The gate's own
tolerance — a five-line window satisfied by any word of four characters or more — is a separate
defect and takes a queue row. Findings 3 and 7 take queue rows. The rest are recorded as read.
