# Skill review — communicator

SKILL-REVIEW

Skill: communicator

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: PASS — no blocking findings. The non-stamp content is the seat/senior rename plus one
retired-rule citation removed and one glossary entry restructured; all three checked for pack-wide
consistency and hold.

## What changed

`git diff origin/main..HEAD -- skills/communicator/` is not stamp-only. Beyond the version bump, three
things changed:

1. **"senior" → "seat"** at four spots in `SKILL.md` (a worker-closed step becomes "the seat's beat";
   the session-13 report "bounced by its reader" line renamed "the seat's own chat") — matches the
   pack-wide rename this same push carries in `live-spec-base` and `director`.
2. **The one-collision-law citation** in `SKILL.md` and `references/page-lifecycle.md` drops "base rule
   18" (retired tonight, see `live-spec-base`'s own review) and states the law by description instead.
   `grep -rn "base rule 18" skills/` after the change: no hits.
3. **`references/words.md`'s "Seat" glossary entry** is restructured: instead of asserting the rules
   below use "all four" names for the seat (senior, orchestrator, lead, seat), it now says
   `references/glossary.md` records the other three as the *source's* alternate names while the base
   skill's own rules use one name, and it adds a note distinguishing `PRODUCT_SPEC.md`'s separate
   **remote seat** sense (a session sharing no filesystem with the assigned one) from this entry's
   sense (which session orchestrates). Checked `PRODUCT_SPEC.md:203` — the remote-seat definition
   quoted matches exactly ("a session that shares no filesystem with the assigned session and reaches
   the repository only through git").

## Findings

None blocking.

- **Rename completeness, checked pack-wide, not just this file** — `grep -rn "senior" skills/` still
  turns up four instances outside `communicator`: two in `skills/director/references/
  delegation-protocol.md` (untouched by tonight's rename in that same file, flagged in this session's
  `director` review as that skill's own non-blocking finding) and two pre-existing instances that
  predate tonight's rename entirely (`skills/live-spec-base/SKILL.md:220`, `references/
  settings-ladder.md:52`, both `git blame`-dated 2026-07-09 and 2026-08-14 — flagged in this session's
  `live-spec-base` review). `communicator`'s own files carry no leftover "senior" outside the two
  places `references/words.md` and `references/glossary.md` cite it deliberately as the source's other
  name — this skill's own rename is complete; the remaining instances are other skills' debt, already
  named there rather than repeated as a finding against `communicator`.
- **Bare `(rule N)` citations, including `(rule 18)` at `SKILL.md:154`, `references/words.md:63`, and
  `references/writing-register.md:54`, are unrelated to the retired `live-spec-base` rule 18** —
  `SKILL.md:42` states explicitly that this skill anchors "its own number as a quiet anchor (rule N)"
  for its own internal numbering, distinct from `live-spec-base`'s. Confirmed rule 18 here is "The
  stretch's end is unmissable," not the name-collision law — a different rule set, correctly untouched.
  Checked because the coincidence of the same number was worth ruling out; it is not a defect.
- **Frontmatter / Progressive Disclosure / Anatomy** — unaffected by tonight's changes; the prior
  passes (`2026-08-26-communicator.md` and earlier slimdown records) already checked these clean and
  nothing in this diff reopens them.
