# Skill review — text-audit, the whole skill after the day's repairs

`SKILL-REVIEW`

Skills: text-audit.

Date: 2026-08-05 14:14
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes, with one correction owed. The day's commits closed every blocking stop that rounds
30 and 31 raised, and they broke nothing the tests pin. Two of those repairs wrote new claims that no
source holds, and one rename gave a defined role a second job.

## What the day changed

Eight commits touched `skills/text-audit/` on 2026-08-05. Four of them carry this review's focus.

`dce526c` repaired three stops both readers found, and it fixed two roles. The reading record under
`docs/language-reads/` and `docs/language-defects.md` now hold separate jobs, stated in separate
sentences. The design-review pointer moved from product-prover to design-reviewer. The old-vs-new
meaning check, run after a spec section is repaired, was handed from "a second reader" to "a cold
reader". The blocking test stopped being a closed list of three kinds and became one test with three
common cases.

`5a41cf5` rewrote the sentence describing what design-reviewer does. The new wording names grouping
and consistency, which is what that skill's own body and summary line claim.

`b6eb51a` closed the eight blocking stops of round 31. It cited the record behind the measurement
numbers, and corrected 38 kinds of stop to 39. It gave the neighbour-denying class a printed example.
It removed a second measurement's uncited counts, and replaced the per-document averages with totals.

`26719d9` closed the two remaining blocking stops of round 30. The spec-only lints now number three
rather than one, and step 3 states where refutation runs.

## What the review looked at

**Does the summary line still trigger correctly?** The description is untouched by every commit today.
The body carries the trigger phrases under "When it fires", and the frontmatter carries none of them.
That split is the pack's shape across all eleven skills, so this review leaves it alone.

**Do the day's numbers survive their sources?** Mostly. 227, 135, 36, 128, 87 and 21 stand in the
cited record word for word. The two thrown-out shares, 40.5% and 32.0%, follow from those counts.
Finding 1 and finding 2 below hold what does not survive.

**Is every path on the page real?** Yes. All 35 paths named in the body resolve on disk, including the
three skill-review records the day's commits added as citations.

**Does the body still fit the progressive-disclosure pattern?** Yes, with less room than before. The
body runs 468 lines against the guidance of 500, up from 445 at the last review. "What the pass costs"
and "What each reader is handed" are the two sections that would move to a reference file first.

**Do the roles hold one name each?** No. Finding 3 holds the case.

**Does the count of stop kinds match its source?** Yes. `references/reader-prompt.md` prints 39
bulleted kinds, and its own line 7 says 39 of the 66 rules. The body now says 39.

**Does the design-reviewer sentence describe design-reviewer?** Yes. That skill's summary line names
checking whether similar features behave consistently. It also names flagging ungrouped same-kind
items the spec missed. Its body assigns the wording to the prover.

**Do the three spec-only lints refuse as the body says?** Yes. Run over `README.md`, each of
`check-vocabulary.py`, `check-weak-words.py` and `check-requirement-shape.py` exits 1 and prints that
its input set is empty.

## Findings

### 1. The skill says its cited record holds no per-document average, and that record prints one

Line 398 of `skills/text-audit/SKILL.md` reads: "That record states no per-document average, and it
does not name the three documents."

The record it cites is `docs/skill-review/2026-08-05-audit-runs-two-readers.md`. Line 80 of that
record says one reading brings back about 26 stops per document, and the pair about 71.

That line opens with a pronoun standing for the skill body as it stood before today. So the record
reports a figure the skill used to print, rather than measuring one. A reader who opens the citation
to check the claim meets the numbers 26 and 71 on the page. The second half of the skill's sentence
holds: the record names no document.

This is the class step 5 of the loop already names. Round 31 raised the per-document math as a
blocking stop, `b6eb51a` closed it by deleting the averages, and the closing sentence went to no
reader.

Recommendation: say what the record carries. One wording is that the record quotes a per-document
figure from an earlier draft of this skill, and that no measurement stands behind it.

### 2. Three figures in "What the pass costs" are this skill's own arithmetic

The paragraph names the record where the figures stand, then states 355 stops, 222 survived and 57
blocked. None of those three numbers appears in that record. Each is the sum of the two per-reader
lines printed above it, and each sum is correct.

Two things follow from stating them as the record's.

The pair's 355 counts about thirty passages twice. The same record says about thirty passages came
back from both readers. The pair's distinct stops therefore number nearer 325.

The multiplier takes the smaller reader as its baseline. The body reads: "Against the unprompted
reader alone, the pair brings back 2.8 times as many stops." That is 355 divided by 128. Before today
this skill ran the prompted reader alone, so the baseline a reader carries is 227. Against 227 the
pair brings back 1.56 times as many stops. The claim that the judging work nearly triples holds only
against the baseline nobody ran.

Recommendation: mark the totals as sums of the two lines above. Say that the overlap is counted twice,
and give the multiplier the baseline this change replaced.

### 3. One role name covers two jobs, and the file holding the second job goes unlinked

`dce526c` renamed the old-vs-new meaning check's reader from "a second reader" to "a cold reader".
That check runs after a spec section is repaired. Line 26 of the body defines a cold reader. That
reader holds no earlier draft, no author's intent, and no project background beyond the words on the
page. The meaning check hands its reader both drafts and asks for every difference in meaning. So one file
gives the same role two definitions, which is the class `check-one-name.py` owns.

That check already has a home in this skill. `skills/text-audit/references/rewrite-meaning-check.md`
holds its eight fields and its steps, and it was written after a rewrite of eleven skill files dropped
phrases the tests required. The body links `reader-prompt.md`, `unprompted-reader-brief.md` and
`human-prose-rules.md`, and it links this fourth reference file nowhere. A reader of the body reaches
the eight fields only by listing the directory.

Commit `d3384a4` today repaired the same class the file exists for: shortened summary lines had
dropped what the tests require.

Recommendation: link `references/rewrite-meaning-check.md` from that bullet, and give its reader a
name of its own, since that reader works from both drafts.

### Observations for a later pass

The refutation step sits outside step 3's ordered bullets, in a paragraph opening "Before step 4
begins". A reader who scans the six bullets alone carries the merge without it.

Line 52 says a stop one reader found alone still blocks when it meets that test. The test it names
stands six lines earlier, in a different paragraph.

The body's measurement numbers rest on one record, and no reading record under `docs/language-reads/`
holds the 227 and 128 counts. The two readings filed today are cold reads of this skill itself.

The full skill-creator eval loop did not run for these commits. That loop compares a skill against a
baseline over test prompts and asks the person to review the outputs. This review is the reading pass
and the source check, and the record says so rather than implying a benchmark that never ran.

## Checks run

`python3 scripts/rule-census.py skills/text-audit/SKILL.md` — 0 findings, longest prose sentence at 25
words, holding the zero the file's census entry records.

`python3 scripts/preshow-register-lint.py skills/text-audit/SKILL.md` — clean.

`python3 -m pytest tests/test_config_health.py tests/test_reader_prompt_shape.py
tests/test_text_audit_fixtures.py -q` — 50 passed.

`sh guardrails/check-skill-loadability.sh` — 11 skills load, named, versioned, negative-scoped.

`diff -r skills/text-audit/ ~/.claude/skills/text-audit/` — no output. The repository copy and the
installed copy hold the same bytes.

Each of the three spec-only lints was run over `README.md` to test the refusal the body describes.
Each exited 1 and named its input set as empty.

Every path named in the body was resolved on disk, and every number stated from a source was read
against that source.
