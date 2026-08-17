# `SKILL-REVIEW` — communicator, re-review after 94ae4c3

Skill: communicator. Date: 2026-08-17. Range: 9efe559..HEAD.

This record supersedes the first-pass `docs/skill-review/2026-08-17-communicator-slimdown.md` (commit
3905f7f) for this skill. That record reviewed the body as it stood at cb26b70. Commit 94ae4c3, landed
afterward, changed `skills/communicator/SKILL.md` and `skills/communicator/references/rule-histories.md`
again — the push gate's freshness rule (SPEC INV-208) requires a review record at or after a skill's
last change, and 3905f7f is now behind that change, so it no longer covers the current body. This
record re-reviews the current state from scratch and rules on whether 94ae4c3 cured the first pass's
findings.

Verdict: ALLOW WITH FINDINGS. 94ae4c3 correctly cured finding (a) of the first-pass review — the
harness-panel prohibition is back in the body as an imperative, word for word, with no copy left
behind in the reference file. Finding (b), the pointers' over-claim, still stands for three of the
four pointers exactly as before, and the fourth pointer (rule 13's) now has a new, sharper problem of
the same family: it names a piece of content, "the harness panel's standing," that 94ae4c3 pulled back
out of the reference file without updating the pointer that promises it is there.

## Finding (a), checked against the diff itself

I ran `git show 94ae4c3 -- skills/communicator/` and confirmed the shape the task described: the body
gained three lines at what is now SKILL.md:121-129 (the live-status tooth, rule 13), and
`references/rule-histories.md` lost the corresponding two lines (the sentence plus its trailing blank
line) from its rule-13 section. The restored sentence, in full: "Do NOT rely on the harness's own task
list or spinner for this: a browser-seated session never shows them, and even locally they stop
updating through a long run of tool calls." A `python3` grep-count against the working tree confirms it
appears exactly once in `SKILL.md`, zero times in `rule-histories.md`, and exactly once in the
pre-slimdown body at `9efe559:skills/communicator/SKILL.md` — so the returned text matches the original
verbatim and is not duplicated anywhere in the skill. `guardrails/rule-census.json`'s entry for this
file states the same move in its own words ("found an imperative filed as history... It returns word
for word, so this body rises 167 to 169 while references/rule-histories.md falls 9 to 7. An instruction
is not provenance") and its recorded byte count, 45070, matches `wc -c` on the file exactly.

The "So" the task asked me to check, at SKILL.md:125, now reads correctly: "Do NOT rely on the
harness's own task list or spinner... So refresh a short NOW/NEXT line at every step change." The
imperative supplies the reason the "So" needs; before 94ae4c3 the "So" dangled from the weaker
sentence above it ("the one surface every seat shows"), which the first-pass review flagged as reading
worse for the cut. That defect is gone. Finding (a) is cured, cleanly, with no collateral duplication.

## Finding (b), re-tested against the current body

The four pointers are unchanged by 94ae4c3 — the commit touched none of them, only the rule-13
paragraph above pointer at line 138 and the reference file. Confirmed by diffing `94ae4c3^` against
`94ae4c3` on `skills/communicator/SKILL.md`: the only hunk is the three-line insertion in the rule-13
paragraph. The pointers still read:

- line 73 (rule 12) — "Where this rule came from — the dated words behind the echo and its honest
  range — is in `references/rule-histories.md`."
- line 138 (rule 13) — "Where each tooth came from — the asks, the lost runs, the harness panel's
  standing — is in `references/rule-histories.md`."
- line 271 (rule 6) — "Where this rule came from — the calque trap and the task-list case — is in
  `references/rule-histories.md`."
- line 310 (rule 10) — "Where this rule came from — the filename's project name and the day it was
  born — is in `references/rule-histories.md`."

Checked against the body that remains: rule 13 still carries dated provenance at line 99-100
("SPEC INV-35; his word 2026-07-06, on saying when the human can step away") and again at line 156
("Born 2026-07-07: a seventeen-row night ended in what read as silence"); rule 6 still carries two dated
notes at lines 256 and 262 ("2026-07-04", "2026-07-05"); rule 10 still carries one at line 301
("(2026-07-05)"). The first-pass finding that three of the four rules keep dated provenance in the body
while their pointer implies the reference file holds the whole of it is unchanged and still true today
— 94ae4c3 did not touch it.

The rule-13 pointer at line 138 has a second, new problem that the first-pass review could not have
caught because it did not exist yet: the pointer's own parenthetical names three things as living in
`rule-histories.md` — "the asks, the lost runs, the harness panel's standing." I read the current
rule-13 section of `rule-histories.md` (lines 16-24): it names "his third ask in the family" (matches
"the asks") and "twice he lost a multi-minute suite run this way" (matches "the lost runs"), but nothing
about the harness panel remains there — that content is exactly what 94ae4c3 moved back into the body.
The pointer was left unedited when the sentence it half-describes was pulled back out from under it.
A reader who follows this pointer specifically to learn "the harness panel's standing" finds no such
material at the far end. This is not a hypothetical: I grepped `rule-histories.md` for "harness" and
"panel" and both return nothing. The pointer over-claims in a stricter sense now than the general
finding (b) — not merely incomplete, but naming content that is provably absent from its target.

## Nothing else lost or duplicated

I re-ran a whitespace-normalized comparison of the full body against `9efe559` and the reference file's
non-heading lines, the same check the first-pass review describes running: the eleven passages that
remain in `rule-histories.md` (one of the original twelve now lives back in the body) still read
verbatim against both the pre-slimdown body and their current home; nothing was reworded in either
direction. The file's own preamble claim, "the operational text of every rule stays in SKILL.md," is
now true for the harness-panel sentence where it was not before — that sentence was the one
counterexample the first-pass review found, and it no longer is one.

## The rest of the picture, unchanged since the first pass

Frontmatter is untouched by 94ae4c3: `name: communicator`, and the description still states what the
skill does, five triggering situations, and three explicit non-reasons to load it — still a strong
description by skill-creator's bar (description carries all "when to use" information; this one also
does the rarer job of saying when NOT to fire). `metadata.version` stays 5.0.0 across a second
substantive body change in the same day, which the house's own convention (per the prior record and
the prover discipline) does not treat as exempt from the version-stamp bump gate, though that is not
this review's gate to enforce.

Body length: 490 lines (`wc -l`), up from 488 after cb26b70 and up from 499 before the original
slimdown — still comfortably under skill-creator's 500-line bar, with 10 lines of headroom rather than
12. All five reference files (`field-examples.md`, `page-lifecycle.md`, `rule-histories.md`, `words.md`,
`writing-register.md`) have live pointers into them from the body; none is orphaned. I checked each
resolves as a relative path from `skills/communicator/` and each target file exists.

`ARCHITECTURE.md`'s seven pins into this body (lines 35, 291, 343, 227, 431, 278, 177, plus the
design-sync wiring pin) were renumbered in the same commit (94ae4c3 touches `ARCHITECTURE.md` too,
outside the communicator-only diff the task pointed at — confirmed by `git show --stat 94ae4c3`) to
account for the three-line shift. I read the content at each of the seven line numbers directly against
the current file and each lands on the passage its label names. The pins are correct.

## The net

94ae4c3 did exactly what its own commit message and the rule-census reason claim: it returned the
harness-panel imperative to the body word for word, fixed the "So" that dangled without it, left no
duplicate behind, and renumbered every downstream pin correctly. Finding (a) is resolved. Finding (b)
is not — the three-of-four provenance gap the first pass named is untouched, and the fourth pointer
(rule 13's) now carries a small but real new defect: it still names "the harness panel's standing" as
living in the reference file, and that phrase is no longer true. The fix is narrow: either drop "the
harness panel's standing" from the rule-13 pointer's description (rule-histories.md now holds only the
asks and the lost runs for that rule) or restate it to name what actually remains there. Neither this
nor the older over-claim finding blocks the push gate — the record exists, the twelve-passages claim is
still word for word intact, and the machine (ARCHITECTURE.md, rule-census.json) is consistent with the
tree — but both are owed a cleanup pass before the pointers can be trusted at face value.

Reviewer: an independent adversarial read of commit 94ae4c3 against the state reviewed at 3905f7f, and
against 9efe559 for the full-range word-for-word claim, performed by a dedicated reviewer agent working
from the skill-creator discipline installed at `~/.claude/skills/skill-creator`. No file under `skills/`,
`ARCHITECTURE.md`, `guardrails/`, or `tests/` was modified during this review; no git-write command was
run.
