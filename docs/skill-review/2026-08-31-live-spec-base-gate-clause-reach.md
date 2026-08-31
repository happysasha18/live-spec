# Skill review — live-spec-base, rule 13's gate clause after the adversarial repair

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-31
Reviewer: skill-creator quality lens, run over the committed diff of rule 13's second edit
(Anthropic's skill-creator writing guide — Progressive Disclosure, Anatomy of a Skill, frontmatter
accuracy — plus this pack's own register bars in `skills/communicator/references/writing-register.md`)

Verdict: PASS. One correction was already applied inside the range under review; nothing further is
owed before this push.

## Why a second record exists for one day

The earlier record, `2026-08-31-live-spec-base-instruction-authority.md`, covered rule 13's new
paragraph. The lane then edited rule 13 again, in its own adversarial repair commit, after that
record was written. A review that predates the change it is supposed to cover proves nothing, so this
record covers the later edit. This is the same rule the eval README gained in this range: a partial
record certifies whatever it did not look at.

## What changed in the skill since the earlier record

`skills/live-spec-base/SKILL.md`, rule 13, one clause. No other rule, no frontmatter, no other file.

The clause describes the mechanical check that hard-blocks an attribution. It had read that the check
blocks "anywhere else in the tree", which the adversarial read measured as wrong by 86 percent: most
of the tree is spared by design, because the spared pages are dated records narrating what already
happened. The clause now says the block reaches every live text page outside the project's history
and archive directories, and it sends the reader to the check's own opening for the full list of what
is left out.

## Checks that passed

- **The claim is now true of the code.** The clause's reach matches what the check's own surface
  selection does: a tracked text page, outside the spared set, that is not itself a decision record.
  Confirmed by reading the selection in `guardrails/check-authority-anchor.py` rather than its prose.
- **Rule count unchanged.** `grep -cE '^[0-9]+\. \*\*' skills/live-spec-base/SKILL.md` returns 22,
  matching the frontmatter's "twenty-two rules in the body". The edit adds and retires no rule.
- **One home holds.** The edit restates no rule that lives elsewhere; it describes a check.
  `python3 -m pytest tests/test_one_home_per_rule.py -q` passes with `instruction-authority` in its
  floor.
- **Placement.** The clause sits in the rule whose law the check enforces, which is where a reader
  looking up the law will meet it.
- **Register.** No contrast frame, no coined name, no empty intensifier, no code carrying the meaning.
- **The reader is not asked to hold a number.** The clause names no count. The measured counts live
  in the check's own opening, where they carry the date they were taken on, so the rulebook does not
  go stale when the tree grows a file.

## Findings from this review, and where they went

- **The clause described a reach that moved again in the same session.** After this record's range,
  the check gained a narrower reading of what counts as a dated claim: a date standing anywhere on the
  line now anchors the claim on it, which stops the check reddening the project's own dated-entry
  style. The clause survives that change unedited, because it speaks of a claim "that names no date"
  and says nothing about where on the line the date has to sit. Checked deliberately rather than
  assumed, since a clause that had spelled out the sentence-level reading would have gone stale.

## Carried forward, not this change's

The frontmatter's line 3 claims "three on-demand reference modules under `references/`"; the
directory holds five and the body links four. Pre-existing, untouched here, and named again so it is
not lost between records.
