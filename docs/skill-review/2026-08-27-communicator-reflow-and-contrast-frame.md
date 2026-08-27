# Skill review — communicator

SKILL-REVIEW

Skill: communicator

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: both changes are sound and correctly placed. This record supersedes
`2026-08-27-communicator-fact-stated-rule9-pointer.md`, which was fresh only up to `4f7b3851`;
`skills/communicator/SKILL.md` changed twice more since (`bd11dfb6`, `4889b58d`). Of that earlier
review's two open criticisms: the size-ideal one is now resolved; the overlap one still stands,
unaddressed by either of these two commits.

## What changed

`git diff 4f7b3851..HEAD -- skills/communicator/SKILL.md`. Two commits, both inside the same rule-7
sub-rule the earlier review found:

1. **`bd11dfb6` — reflow onto denser lines.** The new "fact is stated, never announced, and never
   staged" sub-rule and its four nested bullets, plus a handful of nearby paragraphs elsewhere in
   the file, were rewrapped onto fewer, longer lines. Confirmed by reading the diff: no word added,
   removed, or reordered anywhere in the touched hunks — only line-break placement changed. 516
   lines down to 499.
2. **`4889b58d` — one contrast frame dropped.** Inside the same sub-rule's fourth bullet, "It is
   not a blogger's, not a narrator's, not a colleague's anecdote" (an "X, not Y, not Z" frame)
   became "reporting to the client who pays for it" — the positive statement the sentence needed,
   with the negations cut rather than folded elsewhere.

## Findings

**Open criticism 1 (file over its ~500-line ideal) — resolved.** `wc -l skills/communicator/SKILL.md`
now reads 499, at the ideal `tests/test_communicator_body_thinned.py` holds (row 280); confirmed
also by running that test directly (`python3 -m pytest tests/test_communicator_body_thinned.py -q`,
5 passed). `bd11dfb6`'s own commit message states the same number and states no wording was
removed to get there — checked against the diff, true: every change in the hunk is a line-break
move, not a cut. This closes the finding cleanly; nothing here trades brevity for a lost word.

**Open criticism 2 (overlap with the "honestly / no sugar-coating" bullet immediately above) — still
stands.** Neither `bd11dfb6` (pure reflow) nor `4889b58d` (one contrast-frame edit, inside the
fourth nested bullet only) touches the first nested bullet — "no sentence whose only job is to
introduce the next sentence, and no label on a fact before the reader has it" — which is the half
that overlaps rule 7's opening bullet, "drop the 'honestly / no sugar-coating' preambles and let
the result speak." Both still ban pre-framing a finding before the reader gets it, from two
adjacent entries under the same rule. Carrying this open rather than closing it on the back of an
unrelated fix: the size pass and the contrast-frame edit each did exactly what their own commit
message claims, and neither claims to touch this bullet.

**The `4889b58d` edit on its own merits — sound.** The removed sentence was a three-way negation
naming what the voice is NOT (blogger's / narrator's / colleague's) before ever saying what it IS;
the replacement states the voice positively in the same clause ("a professional running a technical
project, reporting to the client who pays for it"). This is the shape the skill's own rule 7 already
asks writing to take elsewhere in the file (state the thing, not its rejected neighbors), so the
edit brings this sentence into line with a convention the skill already enforces on the human-facing
text it governs — it was not previously enforcing that convention on its own body.

**Frontmatter / Progressive Disclosure / Anatomy** — unaffected by either commit; both changes stay
inside the same rule-7 bullet block, add no new file, and change no frontmatter line.
