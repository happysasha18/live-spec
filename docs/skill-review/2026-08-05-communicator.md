# Skill review — the communicator skill renames a word in its body while its own reference files keep the old one

SKILL-REVIEW

Skills: communicator.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes with findings — land it. Every gate this session can run reads green on the skill, and
the 396 tests that read it pass. The review returned six findings. All six are recorded and left
standing, because each one edits text this session does not own, or asks for a call only the owner can
make.

## The delta this review covers

Four commits touched `skills/communicator/` today.

`d105b85` (00:03) replaced the frontmatter summary line with one short sentence, inside a sweep that
wrote the installed copies of eleven skills into the repository.

`d3384a4` (00:38) put back the two clauses the suite pins by string: the narrowed report trigger, and
the list of occasions that are no reason to load the skill.

`a97f95b` (11:56) is the readability repair. It carries its own record at
`docs/skill-review/2026-08-05-communicator-readability.md`, which this review treats as covered and
leaves closed. It rewrote the header banner, added `references/words.md`, corrected four facts, fenced
two quoted passages, and renamed the pipeline vocabulary in rule 9.

`83ebd2d` (13:10) changed one word in rule 13, after the wording check learned to read a phrase broken
across a line break and found the coinage still standing in this file.

The review read the whole skill as it stands, and weighed the four commits above as its delta.

## What the review looked at

**Does the summary line still fire on the right occasions?** It names all five: a decision, a reported
landing or milestone, a done-claim, an ask about what the product does, and a problem that needs the
human's word. It carries the negative scope as well, which is what keeps a passing narration line from
loading the whole skill. `tests/test_traceability.py` pins the negative scope and the report trigger by
string, and both pass. What the line lost today is finding 5.

**Does the body still hold together?** The rules read in one voice and each of the six areas still holds
the rules its heading promises. One thing now carries two names on the page, which is findings 2, 3 and
4.

**Does the delta soften any step?** No. Today's last commit swaps a single noun inside rule 13's opening
sentence and changes no instruction. Every block, every walked step, and every default stands where it
stood.

**Does it instruct anything new?** No. The one sentence added today, back in `a97f95b`, sends the reader
to `references/words.md` before acting on a rule whose words are new. That is a conditional load in the
shape the body already uses for `references/field-examples.md`.

**Progressive disclosure.** The body is 499 lines against the 500-line cap in
`tests/test_communicator_body_thinned.py`. The four reference files run 83, 109, 116 and 157 lines, so
none of them needs a table of contents. The structure is sound, and the headroom is an observation
below.

**Is the skill installed as written?** `diff -rq skills/communicator ~/.claude/skills/communicator`
reports no differences, so the repository copy and the copy each machine runs hold the same bytes.

## Removal accounting (SPEC INV-109)

Today's delta removed substance in two places.

The summary line lost its worked phrasings. `d105b85` cut five parenthetical examples, and `d3384a4`
restored the two clauses the suite demands. The examples themselves stayed cut. This is finding 5, and
the recommendation there returns one of them inside the slimmed style.

Rule 9 and rule 13 lost the coined pipeline vocabulary in favour of the plain word. The owner made that
call in `a97f95b` with a stated reason: the wording check bans a coinage in text a reader meets, and a
skill body is such a text. The rule it carries is unchanged. The removal was partial, which is findings
2, 3 and 4.

## Findings

None blocking. All six are recorded and left standing.

**1. The census scores every file zero in its register column, and the findings-bound gate reads that
zero.** This proves an observation the earlier record filed as unverified. Take the text of this skill
as it stood before today, at `d105b85^`. Today's `scripts/preshow-register-lint.py` reports 10 leaks in
it, including the wrapped one at line 77. `scripts/rule-census.py` measures the same file with the same
lint and prints `register 0`. The cause sits in `run_lint` in `scripts/rule-census.py`: it reads the
lint's JSON record line and returns `errors` plus `warnings`, and the register lint's record carries
`severity`, `code`, `message` and `fix` alone. Both lookups fall to their default, the function returns
zero, and the line-counting fallback below is never reached. The reach is every measured file:
`guardrails/check-doc-findings-bound.py` compares each file's `total`, and `total` is
`long + style + register`, so a push that adds register leaks to any document shows no rise in its
ceiling. Recommendation: have `run_lint` fall through to the line count when a record carries no count
key, then re-measure `guardrails/rule-census.json`. This belongs to whoever next owns `scripts/` and
`guardrails/`.

**2. The rename stopped at the body, and the skill's own reference files still teach the old word.**
`references/words.md` is the glossary the body now points at, and its line 44 defines the coined term
while defining nothing for the plain one, so a reader who meets the plain word in rule 9 and looks it up
finds the word rule 9 dropped. `references/field-examples.md` carries the worked example for that very
rule, and its lines 20, 22 and 23 still show the old form, so the body's own example and its reference
file's example disagree word for word on the same line. Nothing mechanical catches this: the wording
check treats the bare noun as an ordinary industry word by its own header, and every file of the skill
exits 0 on it. Recommendation: sweep both reference files with the body, or give `words.md` one line
saying the two words name one thing.

**3. Rule 13 carries both words inside one rule.** Line 78 now reads the plain word, and lines 82, 86
and 90 read the old one three times in the teeth directly below it. A reader meets the same idea under
two names within twenty lines. Recommendation: settle the rule on one word.

**4. One pointer names the word its target dropped.** Line 370, in rule 14, sends the reader to rule 9's
vocabulary and then uses the word rule 9 no longer carries. Following the pointer lands on the other
word. Lines 125 and 129 carry the same word in the live-status tooth. Recommendation: fold this into the
sweep of finding 2, since it is the same class.

**5. The summary line now carries no literal user phrasing.** The five occasions survive as categories.
The phrasings a person actually types went out at `d105b85` and stayed out. The loudest of them is the
literal ask rule 14 exists to answer, which the body still quotes at line 384 as the human's own word
from 2026-07-06. A summary line is the whole triggering surface, and a category matches a real request
less reliably than the request's own words. Recommendation: return one utterance to the clause about
what the product does, about eight words, which fits the slimmed style the sweep was for. The two pinned
clauses stay untouched.

**6. The matrix row and a test docstring still state the criterion in the old vocabulary.**
`TEST_MATRIX.md` row M-112 spells the departures-board criterion in the coined form throughout, and
`tests/test_report_format.py` states the old form in its docstring at line 4 while its assertion pins
the plain one. Neither reds, because the assertion and the row's test both pass. The drift is in the
text a person reads. Recommendation: sweep at the next matrix pass, by whoever owns `TEST_MATRIX.md`.

## Observations

The body stands at 499 lines against a 500-line cap that a test enforces. One added line reds
`tests/test_communicator_body_thinned.py`. Any repair from the findings above spills to `references/`,
or trades a line for a line.

`guardrails/check-one-name.py` reports 4 violations. All four stand in the text as it was before today,
verified by running the same script against the blob at `d105b85^`, which returns the identical four at
the identical lines. Today's delta added none and removed none.

The coined vocabulary now splits by surface on purpose: the skill bodies carry the plain word, and
`PRODUCT_SPEC.md`, `TEST_MATRIX.md` and `ROADMAP.md` keep the coined one, which the register rule allows
in a document. A reader who moves between the two surfaces meets one thing under two names. The owner
made this call with its reason stated, so it stands here as a record.

## Checks run

`python3 scripts/preshow-register-lint.py skills/communicator/SKILL.md` — exit 0, clean for the first
time. Each of the four reference files and the readme exits 0 as well. Against the blob at `d105b85^`
the same script exits 1 with 10 leaks. The check grew stricter today, and the text still passes it.

`python3 scripts/rule-census.py skills/communicator/SKILL.md` — **175**, against **181** for the blob at
`d105b85^`. Long sentences fell from 86 to 84 and style from 95 to 91. The longest sentence fell from
105 words to 97. The register column reads 0 on both, which is finding 1.

`python3 guardrails/check-one-name.py skills/communicator/SKILL.md` — 4 violations, the same four the
file carried before today.

`sh guardrails/check-skill-loadability.sh` — OK, 11 skills load, named, versioned, negative-scoped.

`diff -rq skills/communicator ~/.claude/skills/communicator` — no differences.

The 23 test files that read this skill — **396 passed, 0 failed**. That set includes
`tests/test_communicator_body_thinned.py`, `tests/test_report_format.py`, `tests/test_traceability.py`
and `tests/test_preshow_register_lint.py`, which are the four the delta touches most closely.
