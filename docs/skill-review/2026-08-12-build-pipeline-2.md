# Skill review — build-pipeline (the base rule count becomes a pointer)

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-08-12
Reviewer: skill-creator (Anthropic), run by a fresh reviewer with clean context. It did not author the
edit, and it wrote no file but this record.

Verdict: passes as a skill. The frontmatter is untouched and still describes the body, the edited
sentence resolves for a reader in one hop to a fact a test holds, and nothing else in the file
restates the count. One finding is cosmetic and one is a recommendation about what still counts rule
numbers by hand elsewhere. Neither blocks the push.

## What changed

Commit `dc78db9` edited one sentence in the terms paragraph at line 73 of
`skills/build-pipeline/SKILL.md`. The sentence said a base rule N points into
`skills/live-spec-base/SKILL.md`, which carries thirty-four. It now says a base rule N points into
that file, and its own frontmatter states how many it carries. This is roadmap row 593's aim: the
count of the base rulebook's rules gets one home, so the next cut touches one file. Nothing else in
this skill changed in the range.

## Findings

1. **The pointer resolves, and its target is machine-held.** Reviewed and clear. The base's frontmatter
   description does state a count — thirty-four rules in the body — so the sentence sends a reader
   somewhere the fact actually is.
   `tests/test_request_classifier.py::test_base_description_counts_the_rule` derives the count from the
   base's own numbered heads and reds if the description disagrees, and it allows exactly one hole in
   the numbering, at rule 30. So the fact this sentence now points at cannot drift silently. That is a
   better standing than the sentence had before the edit, when the literal number here was read by no
   test. This closes finding 5 of `docs/skill-review/2026-08-12-build-pipeline.md`, which named this
   line as one of four uncounted copies and pointed at base rule 4 for the fix.

2. **A reader still needs the second hop to learn the numbering has a hole.** Noted, no repair asked.
   The sentence gives a count and a place to find it. It does not say that the numbers run past the
   count, which they do — 34 heads numbered 1 to 35. A reader of this page who meets a citation of
   base rule 35 and then reads thirty-four in the base's description now has the answer waiting one
   file away: the base's rulebook head states plainly that rule 30 is cut and its number retired. The
   chain resolves in two hops, so the reviewer asks nothing here.

3. **The line was not re-flowed.** Cosmetic, and this edit made it. Line 73 now runs 119 characters
   against 78 to 101 through the rest of that paragraph, and the sentence "A **communicator rule N**
   points into" now begins mid-line. A re-flow across the paragraph fits it inside the file's own norm.
   This is the same class as finding 4 of the earlier build-pipeline record, and the same class as the
   two long lines the day's rule-7 edit left in the base.

4. **No other copy of the base rule count survives in this skill.** Reviewed and clear. A grep of
   `skills/` for "thirty-four" and "thirty-five" returns exactly one hit, the base's own frontmatter.
   The two remaining literal assertions on that string, in `tests/test_clean_context_review.py:70` and
   `tests/test_resume_rederive.py:56`, both read the base's frontmatter, so they hold the canonical
   home rather than a copy of it. Row 593's aim is met across the pack.

5. **The file's other citation of the day's rewritten rule still reads true.** Reviewed and clear. The
   commit-and-show step at line 471 paraphrases base rule 32 — the number reports what taking the
   release costs a host, the patch does nothing to the host, the minor is taken by re-running the
   catch-up walk, the major forces host action and ships its dated `MIGRATION.md` chapter, and the
   minor-versus-major call is a stated judgment held by no gate. Every clause of that paraphrase
   survives in the shortened rule 32, checked sentence by sentence. The base rule number 32 in the
   citation still resolves, since the cut number was 30.

## The measures this review was held to

The census reads `skills/build-pipeline/SKILL.md` at 255 findings after the edit — 135 sentences past
the word cap, 120 style findings, no register findings — level with the 255 the same file measured at
`e8900d9`, so the edit crossed no cap. The file measures 64,028 bytes against 64,007, a rise of 21.

Commands run and their results: `python3 -m pytest tests/test_request_classifier.py` — 14 passed;
`python3 -m pytest tests/test_compaction_discipline.py` — 11 passed, including
`test_build_pipeline_carries_compaction_every_pass`, which now pins the compaction bullet's own
sentence; `python3 -m pytest tests/test_clean_context_review.py tests/test_resume_rederive.py
tests/test_release_tier_rule.py` — 19 passed; `bash guardrails/check-skill-loadability.sh` — OK, 11
skills load; `python3 scripts/preshow-lint.py` and `python3 scripts/preshow-register-lint.py` over the
range's added skill lines — both clean, so the new sentence carries no banned contrast frame and no
coined word. The installed copy at `~/.claude/skills/build-pipeline` is byte-identical to the
repository copy.
