# Skill review — communicator (the base rule count becomes a pointer, in the body header and in words.md)

SKILL-REVIEW

Skill: communicator

Date: 2026-08-12
Reviewer: skill-creator (Anthropic), run by a fresh reviewer with clean context. It did not author the
edit, and it wrote no file but this record.

Verdict: passes as a skill. The frontmatter is untouched and still describes the body, both edited
sentences resolve to a fact a test holds, and the eight base rules this skill cites by number all
still exist. One finding is cosmetic and one records an asymmetry the reviewer judges correct. Neither
blocks the push.

## What changed

Commit `dc78db9` edited two sentences, both saying the same thing.

`skills/communicator/SKILL.md`, the pack blockquote at lines 10-15, said the base file carries
thirty-four numbered rules. It now says the base's own frontmatter states how many numbered rules it
carries.

`skills/communicator/references/words.md`, the "Base rules" paragraph at line 30, carried the same
literal count and now carries the same pointer. Its list of the eight base rules this skill cites is
unchanged. Nothing else in the skill changed in the range, and the frontmatter description is
untouched.

## Findings

1. **Both pointers resolve, and their target is machine-held.** Reviewed and clear. The base's
   frontmatter description states thirty-four rules in the body, so both sentences send a reader to a
   place the fact actually sits.
   `tests/test_request_classifier.py::test_base_description_counts_the_rule` derives that number from
   the base's own numbered heads and reds if the description disagrees. Neither of these two sentences
   can now go stale on its own, because neither states a number.

2. **The eight base rules cited by number all still exist.** Reviewed and clear.
   `references/words.md` names base rules 1, 2, 4, 6, 10, 13, 16 and 18 with a phrase each. Every one
   of those numbers is a live head in `skills/live-spec-base/SKILL.md`, and none is the retired 30, so
   the paragraph's numbered list survives the day's cut untouched. The pack blockquote in `SKILL.md`
   names no rule number at all.

3. **The paragraph now counts its own rules and points at the foreign one, which is the right split.**
   Reviewed, recorded for the reader who notices it. Two paragraphs above the edit, `words.md` still
   states literal counts — the body's twenty-two rules and the writing register's seventeen. Those are
   this skill's own facts, homed on its own page, and the reviewer verified the first: the body carries
   `(rule N)` tags numbered 1 through 22 with no gap. Base rule 4 asks for one canonical home per fact
   and a pointer everywhere else, so counting what this skill owns and pointing at what the base owns
   is the shape the rule asks for. No repair.

4. **Neither line was re-flowed.** Cosmetic, and this edit made it. `SKILL.md` line 12 now runs 116
   characters against 94 to 102 through the rest of the blockquote, and `references/words.md` line 31
   runs 113 against 97 to 101 through its paragraph. In both, the following sentence begins mid-line.
   A re-flow of the two paragraphs fits them inside the file's own norm. This is the same class the
   earlier build-pipeline record raised as its finding 4.

5. **No other copy of the base rule count survives in this skill.** Reviewed and clear. A grep of
   `skills/` for "thirty-four" and "thirty-five" returns exactly one hit, the base's own frontmatter.
   Both of this skill's copies were the ones removed here.

## The measures this review was held to

The census reads `skills/communicator/SKILL.md` at 175 findings after the edit — 84 sentences past the
word cap, 91 style findings, no register findings — level with the 175 the same file measured at
`e8900d9`. `skills/communicator/references/words.md` reads 4 findings after and 4 before. The files
measure 45,848 and 6,865 bytes against 45,831 and 6,844, rises of 17 and 21.

Commands run and their results: `python3 -m pytest tests/test_request_classifier.py` — 14 passed;
`python3 -m pytest tests/test_clean_context_review.py tests/test_resume_rederive.py
tests/test_release_tier_rule.py` — 19 passed; `python3 -m pytest tests/test_compaction_discipline.py`
— 11 passed; `bash guardrails/check-skill-loadability.sh` — OK, 11 skills load, named, versioned,
negative-scoped; `python3 scripts/preshow-lint.py` and `python3 scripts/preshow-register-lint.py` over
the range's added skill lines — both clean, so the two new sentences carry no banned contrast frame
and no coined word. The installed copy at `~/.claude/skills/communicator` is byte-identical to the
repository copy.
