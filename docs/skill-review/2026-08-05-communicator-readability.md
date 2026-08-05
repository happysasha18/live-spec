# Skill review — the communicator skill defines its own words and names the files its steps need

SKILL-REVIEW

Skills: communicator.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes with findings — land it. The corrections check out and no gate reds on this skill.
The review returned five findings; four were verified and fixed before this record closed, and the
fifth is recorded below. Twelve findings that would change what the skill instructs are recorded and
left standing, for the human's word.

## Why it was worth a change

A readability audit read this skill twice with fresh readers. One held the 38-item stop list at
`skills/text-audit/references/reader-prompt.md`. The other held nothing and checked every named file,
script, code and number against the tree. Pass A returned 108 stops and 93 stand. Pass B returned 20
and 18 stand. Seven passages came back from both.

Twelve of the confirmed stops named a step a reader cannot carry out from the page alone. A session
that loads a skill acts on it. A step it cannot perform is skipped with nothing in the output to show
for it, and the report still looks complete. The full audit is
`~/context-slimdown/reports/audit-communicator-two-reader.md`; the per-claim verification is
`~/context-slimdown/reports/communicator-repair.md`.

## What changed

**A `references/words.md` file, and one sentence in the body pointing at it.** It defines about
twenty-five terms, says which repository a path belongs to, gives the eleven bracket-code letters and
their home, names the eight base rules the body cites, and says which of two numbering systems a
`(rule N)` tag counts. Every definition was taken from a source in the tree: the glossary of
`PRODUCT_SPEC.md`, the words section of `skills/live-spec-base/SKILL.md`, spec criterion `INV-128`,
`adopt/ADOPT.md`, and the settings-ladder table. Two terms carry an inline `[GAP: ...]` note where the
tree is silent.

The file sits under `references/` rather than in the body because
`tests/test_communicator_body_thinned.py` holds the body under 500 lines. It is 499 today.

**The header banner.** It ran sixteen shared-rule slogans together in one sentence, unmarked as
partial, while the base skill carries thirty-five rules and seven "base rule N" citations point past
the sixteen. The banner now names `skills/live-spec-base/SKILL.md`, its rule count, and the four
scopes of the settings ladder, in the shape `skills/design-reviewer/SKILL.md` already uses.

**Four wrong or missing facts, each checked against the tree.** `(rule 12's mined proposal)` became
`(rule 21's mined proposal)`, since rule 12 is the capture echo. Rule 13 said "Three teeth" and
carries six bullets, so it now says six. Step 5 of the pre-report walk gave a contrast floor for large
text and no size, so it now names 24px, and 18.66px when bold, read from
`scripts/preshow-legibility-lint.py`. Step 3 said its script only warns, and the script exits 1, so
the step now says to read its printed lines.

**Two quoted passages fenced.** Rule 8 and step 4 reproduce the phrases
`scripts/preshow-register-lint.py` bans, taken from that script's own pattern list. Both now sit
inside the `<!-- register-lint:quoted-source -->` fence the lint ships for quotation. The lint's hits
on this file fell from nine to two.

**The reference files and the readme.** `README.md` claimed seven rules and a four-skill pack; the
skill has twenty-two rules and the pack ships eleven skills. `field-examples.md` claimed nothing in it
is a new rule, while its far-tier section states a law the body does not carry, and it printed
`check-far-tier.py --report` with no argument, so the command exited 2 as printed. `page-lifecycle.md`
carried a sentence about the push chain's letters that both readers could not parse, and an undefined
"reach map's directory classes". `writing-register.md` sent the writer to a "Formal index" retired at
the 4.0.0 format migration.

## Removal accounting (SPEC INV-109)

The banner rewrite removed one thing: the sixteen shared-rule slogans a reader met without opening the
base file. Eight of the sixteen are named again in `references/words.md`, under the base-rules
paragraph, because the body cites those eight. The other eight are dropped, and the banner now names
the file that holds all thirty-five. Nothing else was cut.

## What the review looked at

**Does the summary line still trigger correctly?** The frontmatter is untouched. Each of its five
occasions still has a home in the body, and no trigger moved to a reference file.

**Does the body still hold together?** Yes. With the definitions in their own file, the body states
nothing twice that it did not state twice before. The reviewer noted that `words.md` restates
enumerations rule 12 and rule 9 already carry. That is what a glossary a reader enters from a term
does, and thinning the rules instead is a separate call.

**Could the change be read as permission to skip a step?** No step was softened. Step 3 keeps its
imperative and only adds how to read the tool's output.

**Does it instruct anything new?** One sentence: read `references/words.md` before acting on a rule
whose words are new to you. That is a conditional load, in the shape the body already uses for
`references/field-examples.md`.

**Is the words file accurate against the tree?** Spot-checked by the reviewer and confirmed. The
letter legend matches `PRODUCT_SPEC.md` line 7. The door, work-kind, footprint and map values match
their spec criteria. The seat's four names match `skills/live-spec-base/SKILL.md`. The eight base
rules named match their titles. `templates/profile.template.md`, `docs/queue-archive/` and
`docs/prover/` all exist.

## What the review sent back

Four findings were verified and fixed before this record closed.

**The adoption-record note was wrong.** It said no document gives the adoption record a location.
`adopt/ADOPT.md` line 27 names `.live-spec/` as the home of the host's records, including the
installed-set record, and its phase 6 says to record installed skill versions there. Rule 11 sends the
agent to walk that record when answering a done-claim, so the false note would have told it there was
nothing to open. The entry now gives the location, and the remaining gap is a naming one: the tree
calls the same file the installed-set record.

**The movement note overclaimed.** The tree does state where a movement ends, in
`skills/live-spec-base/SKILL.md` and the spec glossary, through the breakpoint. The note is narrowed
to what opens one, which is genuinely unstated.

**The teeth count was fixed in the body alone.** `references/field-examples.md` still read "the three
teeth pinned". It now reads six.

**The readme miscounted its own reference files.** It said three, and there are four.

One finding is recorded and left. `skills/spec-author/SKILL.md` still carries the old slogan banner,
so the two skills' banners now disagree in shape. That file belongs to another session today.

## Findings

None blocking. Twelve are recorded and left standing, since repairing any of them would change what
the skill instructs, or needs a call only the owner can make. They are set out in full in the audit
report. The four loudest:

1. **A shipped lint and two shipped tests disagree over one phrase.** Rule 9 tells the writer to name
   a station using a phrase `scripts/preshow-register-lint.py` flags as a pack coinage shown raw.
   `tests/test_report_format.py` and `tests/test_traceability.py` pin the exact wording, so rewording
   it reds both. The lint's own header states that the accepted reader docs carry none of its
   coinages; this file does, and it is the only one of eleven skills that reds on that lint. The phrase
   is fenced here as quotation:
<!-- register-lint:quoted-source -->
   "name the pipeline station" (line 223) and "names its pipeline STATION" (line 224)
<!-- register-lint:/quoted-source -->
   Settling it takes one call: reword the rule and re-pin the two tests, or exempt the phrase in the
   lint.
2. **The pre-report walk both forbids and requires a question.** Step 6 sends an unjustifiable removal
   back as a question. Four lines below, the standing sentence says the walk adds no questions. Both
   are in the source word for word. Already filed as entry 16 of
   `inbox/2026-07-30-communicator-source-findings.md`, and re-verified today.
3. **"The show rule (a new window)" names no rule number.** The sentence exists to settle precedence.
   By title the show rule is rule 1; by behaviour it is rule 5. Entry 3 of the same inbox file,
   re-verified.
4. **The decision page has no artifact and no remote path.** No template ships, no schema is given,
   the archive's twelve files contradict the stated naming law, and the round trip assumes a local
   Downloads folder while rule 5 says a remote seat opens no local window.

Two observations for a later pass.

`scripts/rule-census.py` reports `register 0` for this file while
`scripts/preshow-register-lint.py` exits 1 on it. The census register column reads zero even when the
lint reds, so any census register verdict on this file is empty until that is fixed. This reproduces
entry 12 of the inbox file.

`ARCHITECTURE.md` pins `skills/communicator/SKILL.md:510` against a 499-line file, and the pin and the
line count are identical at `HEAD`, so the break predates this pass. The pre-report walk sits at line
440 today. That document belongs to another session, so the correction is left to its owner.

## Checks run

`python3 scripts/rule-census.py skills/communicator/SKILL.md` — **178**, down from the 180 recorded in
`guardrails/rule-census.json`, so the findings-bound gate reads a fall. Long sentences fell from 85 to
84 and style from 95 to 94. The longest sentence holds at 105 words. The other files hold their
records: `README.md` 3, `field-examples.md` 21, `page-lifecycle.md` 11, `writing-register.md` 10.

`python3 scripts/preshow-register-lint.py skills/communicator/SKILL.md
docs/skill-review/2026-08-05-communicator-readability.md` — exit 1, on the two lines of finding 1
alone. Every other file of the skill exits 0, and so does this record on its own.

`python3 guardrails/check-one-name.py skills/communicator/SKILL.md` — 4 violations, the same four the
file carried before this pass.

`sh guardrails/check-skill-loadability.sh` — OK, 11 skills load.

`diff -rq skills/communicator ~/.claude/skills/communicator` — no differences, so the repository copy
and the installed copy hold the same bytes.

The 21 test files that read this skill — 200 passed, 0 failed. That includes
`tests/test_communicator_body_thinned.py`, whose 500-line ideal the body meets at 499.

`python3 -m pytest tests/test_config_health.py tests/test_traceability.py
tests/test_communicator_register_extracted.py -q` — 210 passed, 3 failed. None names this skill. Two
are local hook overrides and personal settings, failing before this pass began. The third is the
`ARCHITECTURE.md` pin recorded above, which is broken at `HEAD`.

`python3 guardrails/check-doc-findings-bound.py` — one failure, and it is owed work rather than a
regression: `skills/communicator/references/words.md` is new and carries no entry in the census
record. The record lives in `guardrails/`, which another session holds today, and re-measuring it
would also lower the ceilings of files those sessions are actively changing. Whoever next owns
`guardrails/` runs `python3 scripts/rule-census.py --json guardrails/rule-census.json`.
