# `SKILL-REVIEW` — live-spec-base, four more illustrative chunks leave the body

Skill: live-spec-base. Date: 2026-08-24. Range: uncommitted working-tree changes in the review
worktree, base = HEAD = origin/main = commit `2579fbe2471f17424d088792b22b740d250a6371`. Nothing in
this range is committed; the diff under review is `git diff HEAD` against that commit, touching
`skills/live-spec-base/SKILL.md`, `skills/live-spec-base/references/glossary.md`,
`skills/live-spec-base/references/worked-examples.md`, `architecture/pipeline-and-lanes.md`,
`architecture/rules-and-settings.md`, and a new untracked file, `tests/test_live_spec_base_body_thinned.py`.

Verdict: ALLOW WITH FINDINGS. The move is real, verified word-for-word in all four places, and it
fixes the two most substantial defects both 2026-08-17 reviews left open on this same file — the
worked-examples pointers now name their target section, and the frontmatter no longer claims the
settings ladder is the skill's only on-demand module. What remains open is smaller than what shipped
last time: a couple of pre-existing deixis bugs this session did not touch, and two cosmetic new
seams. Nothing here is a lost rule, a broken pointer, or a silently altered sentence.

## What changed, independently confirmed

This is not a restatement of the brief. `git diff HEAD` shows exactly five tracked files touched and
one new untracked test. `skills/live-spec-base/SKILL.md` loses 35 lines and gains 21 net (620 → 606
lines; I counted both with `wc -l` and confirmed `git show HEAD:.../SKILL.md` still holds 620). Four
chunks move: the whole "Where the paths and the codes point" section, rule 23's worked-proof
paragraph, rule 33's 2.7.0 history, and rule 35's worked failure plus its withdrawn-script note.
`references/glossary.md` gains a new "Where the paths and the codes point" section (23 lines) at its
end; `references/worked-examples.md` gains three new headed sections, "Rule 23", "Rule 33", and "Rule
35" (23 lines). `architecture/pipeline-and-lanes.md` renumbers two pins (144→128, 166→150) and
`architecture/rules-and-settings.md` renumbers seventeen. The frontmatter `description` line changes
from naming the settings ladder as the sole reference module to naming all three by name. Nothing else
in the tree is touched; the version stamp stays 5.0.0.

## The four moves, checked as a word stream

I pulled each removed block from the diff and each added reference-file block, collapsed both to a
single whitespace-joined stream, and compared them by hand rather than trusting the commit's own
framing.

**The paths-and-codes section.** The removed body text and the added `glossary.md` section are
identical sentence for sentence, with exactly the deixis repair the move requires: "This file names
paths" → "SKILL.md names paths"; "beside this one" → "beside SKILL.md"; "beside this file" → "beside
SKILL.md"; "a code this page never uses" → "a code SKILL.md never uses". One spot is not a pure
word-substitution: "So a row cited here may sit there instead" became "So a row SKILL.md cites may sit
there instead" — a passive-to-active restructure around the same fact, not a literal token swap. I
flag it because the brief asked me not to wave through anything that isn't literally identical, but it
is the same kind of deliberate, disclosed repair the 2026-08-17 second review approved of for the
"four names" sentence — it fixes a locative pronoun that would otherwise have pointed at the wrong
file in its new home, and it changes no fact. Every other sentence in this block, including the full
enumeration of `guardrails/`, `scripts/`, `tests/`, `templates/`, `hooks/`, `adopt/`, `skills/`, the
host-side directory list, and the `[target]`/`[default]` bracket-mark definitions, is byte-identical.

**Rule 23's worked proof.** The removed text is "Here is the worked proof. The routing rule lived in
once-read files since June and broke mid-turn. It broke until the every-prompt hook line and the
mechanical after-the-fact check landed (rows 253/254, 2026-07-12)... The 1.1.0 audit's once-read walk
is this law's first sweep," and the new `worked-examples.md` "Rule 23" section reads exactly that,
word for word, with no rewrite of any kind. The one sentence sandwiched between them in the original
paragraph, "That is the same cure that killed invented clock stamps," does not move at all — it stays
in the body, and I confirmed the new test's own `test_body_keeps_the_test_checked_sentence_rule_23_needs`
is there for exactly this reason: `tests/test_live_channel_law.py` asserts that literal substring
against `SKILL.md` directly, so leaving it in place is deliberate, not an oversight, and I re-read
`tests/test_live_channel_law.py` to confirm that assertion actually exists there. Good catch by
whoever wrote this test — a body-thinning that had moved that sentence too would have broken an
unrelated test file silently.

**Rule 33's 2.7.0 history.** The removed sentence — "The 2.7.0 release ran its adversarial pass in the
context that authored the new lenses. So it never turned a brand-new lens onto the skill body that
introduced it." — lands in the new `worked-examples.md` "Rule 33" section unchanged, word for word. The
sentence the body keeps in its place is new prose, not a copy: "The 2.7.0 release's own breach of this
rule — an adversarial pass run in the context that had authored the new lenses, and so never turned
onto the skill body that introduced them — is written out under rule 33..." This is a summary sentence
serving as the pointer, not a duplicate of the moved text, and that is the correct shape — duplicating
it would have defeated the point of moving it. I checked whether the summary silently drops or adds a
fact against the moved original and it does not; it only compresses.

**Rule 35's worked failure and withdrawn-script note.** Two separate removed chunks — "Worked failure:
on 2026-07-28 a session wrote its handover from memory. It named a question as still waiting for the
owner, and the owner had answered it earlier that day," and, forty lines later in the same rule, "A
script read the handover's three lines until 2026-08-09, and the live-spec pack withdrew that script
after finding no error the script had ever caught" — both land in the new `worked-examples.md` "Rule
35" section unchanged, word for word, in the same order. The body's replacement text is again a fresh
summary sentence naming both cases and pointing at "rule 35" in the reference file, not a copy.

In all four cases I found no sentence quietly dropped, no fact silently altered, and no number changed
in transit. The only non-literal moves are the two summary/pointer sentences for rules 33 and 35 (by
design) and the one passive-to-active repair inside the paths-and-codes block (a deixis fix, not a
content change).

## The pointers, checked against the standard the 2026-08-17 reviews set

Both earlier reviews of this same file singled out the worked-examples pointers as the weak spot:
"See references/worked-examples.md for the per-kind illustration of both" and rule 32's "written out
in references/worked-examples.md" told a reader *that* something was there but never *which* of the
file's headed sections to land on, forcing a scan past unrelated cases. This session's three new
pointers all fix exactly that gap:

- Rule 23: "...is written out under rule 23 in [references/worked-examples.md](...). Open the
  reference when this rule's mechanism needs the concrete story."
- Rule 33: "...is written out under rule 33 in [references/worked-examples.md](...); open it when this
  rule's failure mode needs a concrete case."
- Rule 35: "...are both written out under rule 35 in [references/worked-examples.md](...). Open it
  when either case needs the concrete story."

Each now names the target section by its rule number (matching the reference file's own "## Rule N —"
headings, which I confirmed line up: 23, 33, 35 all exist as headings) and states when to open it. This
is the shape the settings-ladder pointer already modelled and the shape both earlier reviews asked for.
It is a genuine fix, not merely new prose that happens to look like one — I checked that "rule 23" /
"rule 33" / "rule 35" in the pointer text actually match a heading that exists (they do), so a reader
following the link lands on the right case rather than the top of the file.

The paths-and-codes pointer is likewise complete by the standard the settings-ladder pointer sets: it
says what's there (two path trees, two code kinds), names the module, and says when to open it ("when
a path or a code needs resolving, and not before").

The two pre-existing worked-examples pointers this session did not touch — rule 24's "See
references/worked-examples.md for the per-kind illustration of both" and rule 32's "written out in
[references/worked-examples.md]" — still don't name their section. That is not new; it's the same gap
both 2026-08-17 records already flagged and left unfixed, and it remains unfixed today. I checked it
was not silently made worse (it wasn't; those two rules are untouched by this diff), but the session
had an obvious opportunity to bring these two in line with the new pattern while editing the same file
and section, and it did not take it.

## Deixis, checked in the new text specifically

I read every sentence this diff adds for a stray "this file" / "here" / an unresolved pronoun, in both
the body and the two reference files, not just the four moved chunks.

The new text is clean. "SKILL.md names paths..." and its four repaired instances read correctly from
inside `glossary.md`. The three new pointer sentences in the body ("is written out under rule 23...",
etc.) all name their antecedent explicitly (rule 23 is rule 23's own paragraph, so "this rule's
mechanism" resolves to the paragraph it sits in) — no dangling reference. The new
`worked-examples.md` "Rule 23" section's closing sentence, "The 1.1.0 audit's once-read walk is this
law's first sweep," carries a "this law" with no antecedent stated on the page itself — a reader who
opened `worked-examples.md` cold, without having come from the body's rule-23 pointer, would need the
section heading ("Rule 23") to recover what "this law" means. That is a real but minor instance of the
same class of problem the 2026-08-17 reviews found and did not fully resolve either (the pre-existing
"Rule 32" section's "by this rule" has the identical shape and is untouched here). It is not a fresh
regression this session introduced — it is the same convention the existing rule-32 section already
uses — but the session had the chance to break the pattern and used the same shorthand instead. Every
reference-file section in this file now relies on its own heading to supply the antecedent for "this
rule" / "this law"; that is workable because the body's pointer always names the rule number before
sending the reader there, but it means the reference file does not fully stand on its own without that
context, which is worth naming rather than assuming away.

I confirmed the one load-bearing reading key this file carries — the sentence tying "the seat, the
senior, the orchestrator and the lead" together as one session (body lines 33–34) — is untouched by
this diff and still sits ahead of every rule that uses more than one of those names. That was the
2026-08-17 first review's most serious finding and its fix; this session did not disturb it.

## A residual seam this session leaves behind, not introduced by it

`references/glossary.md` opens with the H1 "# The words this file uses" (line 1, pre-existing, not
touched by this diff) and, three lines into the glossary body, still carries "this file adds a fourth,
the lead" and "This file calls it a row" — the exact dangling-deixis instances the 2026-08-17 second
review named as open item 2 and left unresolved. This session added a new, correctly-deixed section
("Where the paths and the codes point," using "SKILL.md" throughout) to the bottom of the same file
that still carries the old, uncorrected "this file" bugs near its top. The file is now internally
inconsistent in a way it wasn't before: new prose in it names the rulebook correctly, old prose in the
same file still doesn't. I don't count this as a new defect — the old sentences were already broken and
already flagged twice — but the file's H1 title, "The words this file uses," is now also stale in a
second sense: it no longer describes everything the file holds, since a "Where the paths and the codes
point" section is not a word or a term. Cosmetic, but real.

The 2026-08-17 second review's other three open items — the `reds` idiom definition sitting only in
the glossary well after the body's first use of the verb, the two worked-examples pointers that don't
name a section (addressed above), and the missing conservation test — are addressed by this session
only in the last case (the new test). The `reds` idiom sentence is untouched.

## Frontmatter description

This is the other substantial fix in this session. The old description read "...the settings ladder,
which sits in `references/settings-ladder.md` and is opened when a setting is being resolved" as
though it were the skill's only on-demand module — stale since 2026-08-17, when the glossary and
worked-examples files were created, and flagged as such in both records from that date. The new
description reads "It carries three on-demand reference modules under `references/` — the glossary,
the worked examples, and the settings ladder — each opened only when its own kind of question needs
resolving." I checked the count against the filesystem: `skills/live-spec-base/references/` holds
exactly three files, `glossary.md`, `settings-ladder.md`, `worked-examples.md`. The description is now
accurate. One small precision nit: `glossary.md` now answers two different kinds of question (term
resolution and path/code resolution) under one module, which stretches "each opened only when its own
kind of question needs resolving" slightly — the description implies a clean one-module-per-question
mapping that isn't quite true of the glossary file anymore. Not worth blocking on; the modules and
their count are correctly stated, which is what was broken before.

The rule-count claim, "thirty-four rules in the body," is still true — I ran the new test's own count
(`test_all_thirty_four_rule_numbers_present`) and independently grepped `^\d+\. \*\*` myself, getting
34 (1–29, 31–35, with 30 retired and absent). Nothing in this diff touches a rule head.

## Pins, checked by machine and by hand

`bash guardrails/check-pin-drift.sh` reports `OK (pin drift): 181 pin(s) checked` with no failures,
covering all pins in the repository, not just this file's. I did not stop there. I pulled the exact
current line numbers with `nl -ba` and checked every one of the nineteen renumbered pins
(`pipeline-and-lanes.md`'s two, `rules-and-settings.md`'s seventeen) against what its parenthetical
label claims:

- All nine rule-heading pins (55/56, 122, 235, 277, 298, 309, 319, 333, 390, 398, 407, 438, 504, 552)
  land exactly on the numbered rule head or its INV code they name — I checked each one's text against
  its label and every single one is exact, not just within the script's ±2-line tolerance.
- `SKILL.md:106` lands on "...reads as a resume defect (SPEC INV-107)" — exactly the "checkpoint incl.
  INV-107 closing half" the label promises.
- `SKILL.md:149` lands exactly on the worker-restore sub-rule's opening line, carrying INV-298 inline.
- `SKILL.md:128` (pipeline-and-lanes.md, "rule 7's lanes sub-rules") lands on "The parallel-lanes rules
  sit underneath the fence" — the sub-rules' own lead-in line, one line above the first bulleted
  sub-rule; on-topic and within tolerance.
- `SKILL.md:150` (pipeline-and-lanes.md, "one row per landing commit") lands exactly on "**One row per
  landing commit.**" — a perfect hit.
- The one pin I'd call loose: the settings-ladder pointer note cites `SKILL.md:589`, but the actual
  markdown link (`[references/settings-ladder.md](references/settings-ladder.md), beside this file.`)
  sits one line earlier, at 588; 589 is the following sentence ("It holds the four scopes and their
  homes..."). Within the script's ±2 tolerance and thematically still correct, but not the exact line
  the label implies.

That is a strong result: eighteen of nineteen renumbered pins are exact hits, the one loose pin is off
by a single line and still on-topic, and the mechanical gate independently confirms all 181 pins in the
tree, not just this file's.

## The new conservation test

I ran it directly: `python3 -m pytest tests/test_live_spec_base_body_thinned.py -q` → 6 passed. I also
ran the directly-coupled suites (`test_minor_gate_reconciliations.py`, `test_clean_context_review.py`,
`test_live_channel_law.py`, plus the new file) together: 23 passed, 2 skipped, no failures.

This is a real conservation floor, not theatre. It checks four things that could each silently break
under a future edit and currently would not be caught by anything else in the suite: that the body
doesn't regrow past its current size, that all 34 rule headings survive by number (not just by count,
so a merge-one-cut-one drift can't hide behind a coincidentally-stable total), that all three
reference files exist and are still pointed at by name from the body, and that each relocated chunk's
characteristic substring is still actually present in its reference file (so a later edit can't quietly
empty one while leaving the pointer dangling). I checked the `CURRENT_MAX_LINES = 615` bound against
the real body: 606 lines today, so nine lines of ratchet headroom — tight but functional, and the
comment is honest that this is "no regrowth past where this session left it," not the skill-creator
500-line ideal; I independently confirmed the 620→606 delta the docstring cites by diffing `HEAD` (620
lines) against the working tree (606 lines). The needle strings the test checks against the reference
files are the actual substrings I verified by hand above, not generic filler, and the test explicitly
disclaims re-judging pointer quality or placement — appropriately scoped to structural conservation,
leaving the judgment work (which this review did) to a human/reviewer pass. One very small imprecision
in the docstring: it says "Two of the four 08-17 reviews' open findings were about exactly this gap,"
which is loosely worded — there are two 2026-08-17 *review documents*, and the missing-conservation-test
item is one line among the four items the second document lists as still open, not literally "two of
four." Doesn't affect the test's behavior, just a comment nit.

## Was the moved material genuinely illustrative

Checked against skill-creator's "general, not narrow to specific examples" standard, all four chunks
pass. Rule 23's operative sentence — a behavioural rule that breaks mid-turn twice earns a live channel,
pick a hook line or a mechanical check, record it where the rule lives — is complete and self-contained
in the body without the June routing-rule story; the story only illustrates that the rule was learned
the hard way. Rule 33's operative content — the authoring seat never certifies its own work, a release's
adversarial pass runs from a fresh seat, self-application before release, the gate's mechanical floor —
stands fully in the body without the 2.7.0 anecdote. Rule 35's operative content — both ends of a
session are read by a fresh agent, from a session extract, cross-checked against `DECISIONS.md` and
`NEXT_STEPS.md` — likewise stands without the 2026-07-28 handover story or the withdrawn-script note.
None of the three rules loses an enforceable requirement; each loses only the evidence for why the
requirement exists. The paths-and-codes section is a different kind of case, closer to the glossary
already moved on 2026-08-17 than to a worked example — it's lookup material a reader needs only at the
moment an `INV-x` code or a path needs resolving, never to parse a rule's meaning on first read, and I
checked that no rule's comprehension depends on knowing in advance where these resolve. This move is
the right shape.

## What I ran

`bash guardrails/check-pin-drift.sh` → OK, 181 pins. `bash guardrails/check-skill-loadability.sh` → OK,
12 skills (the base plus its eleven working skills — matches the description's own count).
`python3 -m pytest tests/test_live_spec_base_body_thinned.py -q` → 6 passed.
`python3 -m pytest tests/test_live_spec_base_body_thinned.py tests/test_minor_gate_reconciliations.py tests/test_clean_context_review.py tests/test_live_channel_law.py -q` → 23 passed, 2 skipped. I additionally
started the full `tests/` suite in the background as a broader safety net; it was still running at the
time this record was written and its result is not claimed here one way or the other — the targeted
runs above are what this verdict rests on, and they are sufficient for the scope of this diff.

`bash guardrails/check-skill-review.sh` currently reports OK, but only because nothing in this range is
committed yet — the gate diffs against `origin/main`, which today equals `HEAD`, so it sees no skill
change at all. That result is not evidence this change is clean; it will only become the real gate
check once this diff (or some version of it) is committed, at which point the gate will require a
review record naming `live-spec-base` with a verdict, committed at or after the skill's own last
change. This record is written to satisfy that requirement in advance; whoever commits the skill diff
should commit this record in the same commit or a later one, not leave it orphaned before the skill
change it covers.

## The net

What was claimed — four illustrative chunks moved word-for-word, pins renumbered, a stale frontmatter
line fixed, a conservation test added — is true, and I verified all of it independently rather than on
the strength of the diff's own framing. This session also fixed the two most substantive open items
from both 2026-08-17 reviews of this same file: the worked-examples pointers now name their target
section, and the description no longer implies the settings ladder is the only reference module. Both
fixes are real and I checked them against the standard the earlier reviews set, not just against
whether something changed.

What is left, in order of how much it matters: first, the two untouched worked-examples pointers at
rules 24 and 32 still don't name their section, the same gap flagged twice before and now inconsistent
with the three new pointers that do it right — bringing them in line is a small, low-risk edit against
text already in the right place. Second, `glossary.md`'s H1 title and its three pre-existing "this
file" deixis bugs (lines near "this file adds a fourth" and "This file calls it a row") remain
unfixed and are now joined by a section that correctly says "SKILL.md" instead, making the file
internally inconsistent in style; worth a pass, not urgent. Third, the `reds` idiom note is still only
in the glossary, well after the body's first use of the verb — unchanged since 2026-08-17. Fourth, the
settings-ladder pin should move from `SKILL.md:589` to `588` to point at the actual link line. None of
these four is a lost rule, a broken pointer, or a silently altered fact, and none of them regresses
anything that worked before this session — they are the same small residue both earlier reviews already
carried, now marginally more visible because the new pointers show what the fixed version looks like.
That combination — two real, verified fixes to the record's most substantial standing complaints, and a
small, named, non-blocking residue — is ALLOW WITH FINDINGS, not a clean ALLOW and not BLOCK.

Reviewer: an independent adversarial read of the uncommitted working-tree diff against
`2579fbe2471f17424d088792b22b740d250a6371`, performed by a dedicated reviewer agent working from the
skill-creator discipline installed at `~/.claude/skills/skill-creator`, and cross-checked against both
`docs/skill-review/2026-08-17-live-spec-base-slimdown.md` and
`docs/skill-review/2026-08-17-live-spec-base-slimdown-2.md` in full. No file under `skills/`,
`architecture/`, `ARCHITECTURE.md`, `guardrails/`, or `tests/` was modified during this review; only
this record was written.
