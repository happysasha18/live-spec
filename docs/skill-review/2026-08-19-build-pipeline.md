# `SKILL-REVIEW` — build-pipeline, the named skill-review-step gate bullet

Skill: build-pipeline. Date: 2026-08-19. Range: 8a920ee6..cd2010f0 (skill's own last change is
`b4799774`; HEAD at review time is `cd2010f0`, unchanged under `skills/build-pipeline/` since
`b4799774`).

Verdict: ALLOW.

## Why this record exists

`guardrails/check-skill-review.sh` (gate s, SPEC INV-208) reds this push: commit `b4799774` changed
`skills/build-pipeline/SKILL.md` with a non-stamp content line and no committed review record under
`docs/skill-review/` named `build-pipeline` was fresher than that commit. I ran the gate myself
before writing anything, to see the real failure, not a summary of it:

    FAIL (skill review): skill 'build-pipeline' is substantively changed in this push but no committed
      skill-creator review record under docs/skill-review/ names it with a verdict at least as new as
      the skill's own last change (SPEC INV-208). skill 'build-pipeline' last changed in
      b479977453f9742b490b371ea4514f91a56425b6.

## What `b4799774` actually changed here

I read `git show b4799774 -- skills/build-pipeline/SKILL.md` directly, not the commit message.
It adds one bullet to the "Gates worth remembering" list (current file, lines 699-703):

    - **A substantive skill change earns a skill-creator review before it ships (SPEC INV-208, gate s).**
      A push that meaningfully changes a skill under `skills/` needs a committed record under
      `docs/skill-review/`. That record names the skill and carries a `SKILL-REVIEW` marker with a
      `Verdict:` line, at least as new as the skill's own last change. `guardrails/check-skill-review.sh`
      reds a push that lacks one.

Net: `SKILL.md` 726 lines (was 721 before `b4799774`), and `guardrails/rule-census.json`'s
`skills/build-pipeline/SKILL.md` entry moved 55468 to 55887 bytes — I checked this against the file
on disk with `wc -c`, and it matches the census entry exactly (55887 both places), so the census is
not stale for this file.

## The review itself, applying skill-creator's method

**Frontmatter and description.** Untouched by `b4799774`. Read in full: `name: build-pipeline`,
unambiguous against the other nine skills the pack names in its own "How it relates" section.
`description` names the specific triggers (feature/bug/behavior-change/refactor/docs-only/removal
through the pipeline; the setup walk; five spoken phrases for attach/adopt/onboard/found/update) and
closes with an explicit negative boundary ("a tiny reversible edit and pure research stay outside the
pipeline") — this is the near-miss discrimination skill-creator's guidance asks for, and it is
unaffected by this commit, so I did not re-litigate it beyond confirming the new bullet introduces no
new trigger claim that the description would need to cover (it doesn't — it's an internal gate note,
not a new capability).

**Does the new bullet contradict anything beside it?** This is the finding I actually chased,
because the file already carries an older, different duty with an overlapping name. Line 302 of the
same file (in "The work-kind table" section, untouched by `b4799774`) reads: "...the skill-review
duty (SPEC INV-99)." I checked what INV-99 actually requires by reading `TEST_MATRIX.md`'s M-235 and
M-303 rows directly: INV-99 fires only on a skill-KIND landing's verify-by-deed step, and its outcome
"land[s] in the landing record's accounting rather than a dated class file" — M-303 names this
explicitly as "the one named difference" among the pack's review-record classes. INV-208, the new
bullet's subject, is unconditional on every substantively-changed skill file regardless of the work's
declared kind, and its outcome is the opposite of INV-99's: a dedicated file under `docs/skill-review/`
checked mechanically at push, not a landing-record line. I confirmed the two invariants are already
spec-documented as deliberately distinct (M-303's "named difference" sentence predates this commit),
so the new bullet is not restating INV-99 under a new number, and reads as a second, later-added,
narrower-triggered, harder-enforced duty layered next to an existing one — not a contradiction. The
"Gates worth remembering" list's own convention (checked against all eight of its other bullets) is
to state each gate standalone with no cross-references to sibling bullets or to earlier sections, so
the new bullet not cross-noting INV-99 matches the list's established style rather than breaking it.

**Is the new bullet's own content accurate?** I verified every claim it makes against the actual
mechanism, not the commit message's paraphrase: `guardrails/check-skill-review.sh` exists and is the
file whose behavior I ran above; `guardrails/pre-push` line 227 and `guardrails/README.md` line 45
both label it "gate s"; `docs/skill-review/` exists as a real directory; and `TEST_MATRIX.md` row
M-389 cites the same `SPEC INV-208` id for this exact law (committed record, `SKILL-REVIEW` marker,
`Verdict:` line, freshness rule). Nothing in the bullet overstates or misstates the mechanism.

**Shape and readability.** The bullet is formatted exactly like its eight neighbors in the same list:
a bold lead clause naming the gate and its SPEC id, one to three plain sentences on what it requires,
and (where relevant) the enforcing script named by path. A reader meeting this list for the first
time gets what fires, what it requires, and what checks it — the same information density as every
other bullet on the list, no jargon introduced beyond terms the list already uses elsewhere
(`SPEC INV-`, `guardrails/`).

**Reference integrity.** Confirmed every `[references/...]` link named anywhere in the file still
resolves on disk (`test -f` over all twelve reference files named in `SKILL.md`) — `b4799774` did not
touch any reference file under `skills/build-pipeline/references/`, and none needed to for this
change.

## No defect found — what would have counted as one

I looked for: a restated-not-pointed duplicate (none — this is new content, not a trim); a broken or
ambiguous file reference (none — checked above); a byte-count or rule-census mismatch (none — checked
above); a contradiction with a neighboring rule (checked the INV-99 overlap specifically, found it
deliberate and spec-documented, not a defect); an SPEC id or gate-letter citation that doesn't match
the actual mechanism (checked, matches). None of these turned up a real flaw, so nothing in the skill
was changed by this review.

## What I ran

`git show b4799774 -- skills/build-pipeline/SKILL.md`; `wc -c skills/build-pipeline/SKILL.md` against
the `rule-census.json` entry (via a `python3 -c` JSON read); `grep -n` for `INV-99`, `INV-208`,
`skill-creator`, `skill-review` across `skills/build-pipeline/SKILL.md` and its `references/`
directory; `grep -n` for `INV-99` and `INV-208` in `PRODUCT_SPEC.index.md` and `TEST_MATRIX.md` (rows
M-235, M-303, M-389 read in full); `grep -n "gate s"` in `guardrails/pre-push` and
`guardrails/README.md`; `test -f` over every `references/*.md` path named in `SKILL.md`; `git log
--oneline -- skills/build-pipeline/SKILL.md` to confirm `b4799774` is the skill's last change; `bash
guardrails/check-skill-review.sh` run directly, output pasted above; and
`python3 -m pytest tests/ -q -k "skill_review or skill_count or build_pipeline or publish"` — 75
passed, 0 failed. No file under `skills/` was modified during this review.

Reviewer: this session, reading `~/.claude/skills/skill-creator/SKILL.md` for method (what a
description must trigger on and not on, frontmatter shape, body clarity, reference-file resolution)
and applying it directly to the changed and surrounding text of `skills/build-pipeline/SKILL.md` at
HEAD.
