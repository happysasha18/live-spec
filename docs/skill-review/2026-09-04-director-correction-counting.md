# Skill review — director

SKILL-REVIEW

Skill: director

Date: 2026-09-04
Reviewer: Anthropic's skill-creator — `scripts/quick_validate.py` run directly against
`skills/director/`, plus the skill-creator SKILL.md's own Skill Writing Guide (Progressive
Disclosure, Anatomy of a Skill, frontmatter-description accuracy, Writing Style) applied by hand.
The eval/iterate loop (spawn with-skill vs. baseline subagents, grade assertions against a
gradeable file output, benchmark) does not fit here: director is a prose-and-methodology skill —
a decision-and-delegation protocol for an agent orchestrating a project — with no file artifact a
grader could check, the same shape build-pipeline's own 2026-09-04 record already found. The
structural review below is what skill-creator actually supports for a skill of this shape.

Verdict: PASS (`quick_validate.py`, quoted below) — structure, progressive disclosure, and
frontmatter-description accuracy all check out clean. One cosmetic finding: today's edit left one
paragraph's line-wrapping uneven against the file's own convention. Not fixed here — this record's
write-set is `docs/skill-review/` only, and the task this review runs under forbids editing
`skills/director/` itself.

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/director
Skill is valid!
(exit 0)
```

`quick_validate.py` is Anthropic's own packaging validator (the same check `package_skill.py` runs
before producing a `.skill` file): frontmatter YAML parses, only allowed keys are present, `name` is
kebab-case, `description` is ≤1024 characters with no angle brackets. All pass; no scriptable defect
found.

## What changed

Today's edit (commit `a94cea98`, PLAN q-820) rewrote the correction rule in `skills/director/SKILL.md`
along four lines the director's own logged scenarios showed failing: it now says, in the numbers a
verdict carries, that a correction replans work already running and the turn's own count of new
pieces of work stays zero — no row opens beside the one being replanned; it names the two clauses
that ride inside a correction and belong to it — the repair stated aloud, and the part of the goal
being withdrawn — so neither gets mistaken for a fresh instruction reopening what the correction
just changed; it splits a standing clause by which half of it is new — a fact about the product is
an observation, a rule for what happens from here on is a decision, and a clause carrying both goes
to whichever half the person is telling you for the first time; and it says a turn that accepted no
work names no dimension and calls no specialist, since naming either routes a piece of work nobody
took on (the one exception being a correction, which changes work already running and so must say
what that work now touches). A fifth, smaller repair in the same commit fixed a stale field
description unrelated to this rule (the `shelves_idea` field naming a retired idea shelf); it moves
no fixture's expected value and is not part of what this review covers.

## Findings

1. **Frontmatter `description:` still matches what the body does.** The description lists all
   seven acts (question/musing → "asked, mused"; idea → "offered an idea"; observation → "reported
   something"; decision → "decided"; correction → "corrected running work"; instruction →
   "instructed"; halt → "called a halt") and the downstream flow (dimensions → "name what it
   touches"; specialists → "call the specialists it needs"; execution → "checkpoint, verify,
   close"; the report-back section → "report"). Today's edit changed rule text, not the act list or
   the flow the description names — no drift between the two. **No finding.**
2. **Progressive Disclosure checks out clean.** `SKILL.md` body runs 477 lines below the frontmatter
   (483 total with it), under the ~500-line ideal ceiling, with 13 reference files (542 lines
   total, largest 110 lines) carrying detail out of the body — none of them near the ~300-line
   threshold that would call for a table of contents. **Considered and rejected as a defect**: the
   body sits closer to that 500-line ceiling than most skills in this pack (build-pipeline's own
   2026-09-04 record found it at 67 lines); this is headroom to watch on the next edit that grows
   the body further, not a present violation, and moving content into a reference file with nothing
   currently over the line would be manufacturing a change this review has no mandate to make.
3. **A line left unwrapped by today's edit.** Line 75 of `SKILL.md` ("idea has answered the
   condition twice. Picking one branch and dropping the other silently discards an instruction") runs
   113 characters — the file's own prose wraps at 82–99 characters everywhere else (checked across
   every paragraph today's commit touched); table rows and the frontmatter description are the only
   other lines over 100, and both are expected to run long. Comparing against the commit's own diff,
   this is exactly the line the edit rewrote (`a verdict marking both \`creates_work\` and
   \`shelves_idea\` true` → `a verdict saying the work was taken on and that the idea half was
   handled as an idea`), spliced in without reflowing the paragraph to the file's wrap width.
   **Folded-candidate, not applied**: cosmetic only, changes no instruction a reader follows
   differently — flagged for whoever next has a real reason to touch this paragraph, not fixed here,
   since this review carries no edit authority over `skills/director/SKILL.md`.
4. **Writing Style checks out clean.** No `MUST`, `NEVER`, or `ALWAYS` (checked by grep, whole
   file) — the skill explains why a rule matters ("Rewriting a sheet costs a session real thought,
   and the effort is no evidence that anything new was created") rather than issuing bare
   capitalized imperatives, consistent with the guide's preference for theory-of-mind explanation
   over heavy-handed musts. **No finding.**

## Size

```
$ wc -c skills/director/SKILL.md
   33294 skills/director/SKILL.md
```

```
$ find skills/director -type f -print0 | xargs -0 wc -c | tail -1
   78126 total
```

`skills/director/SKILL.md`: 33,294 bytes (483 lines). `skills/director/` (whole directory,
`wc -c` summed over `SKILL.md` and all 13 files under `references/`): 78,126 bytes.
