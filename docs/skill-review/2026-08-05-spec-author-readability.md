# Skill review — the spec-author skill defines its own words and names the checks it asks for

SKILL-REVIEW

Skills: spec-author.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes. The change adds a definitions block, names the commands and files the page already
asked a reader to use, and corrects four claims that the tree contradicts. It removes no instruction.
Three places add a step, and each one is named below.

## Why it was worth a change

A readability audit read this file with two fresh readers. Pass A worked under the printed stop list
and returned 103 stops; 72 stand. Pass B was handed no rule list, left the page, and checked every
path, script, and number against the tree; it returned 19 stops and 18 stand. Every quote from both
passes appears in the file verbatim.

Thirty-one of the confirmed findings named a step a reader cannot carry out from the page alone. A
session that loads a skill acts on it. A step it cannot perform is skipped with no trace, and the
output still looks complete.

## What changed

**A "Words this skill uses" block near the top.** It defines wish, door, queue row, lane, landing,
host, host profile, kind, surface, spec-delta, facet, regression fence, composition axis, lens, seat,
and the verb red. It names the five markers the page writes and what each one means. It says which
letters the bracket codes use and where each resolves, and it reads `R12.4` as requirement 12,
criterion 4. It states that every path on the page is relative to the live-spec repository root.

Every definition was taken from a source in the tree: the glossary and preamble of `PRODUCT_SPEC.md`,
and the `project.*` lines of `.live-spec/profile.md`.

**The nine named scripts became runnable.** One sentence in that block says to run each script from
the repository root, and that each prints its own usage line when run with no arguments. Every one of
the nine was run with no arguments to confirm it.

**Six pointers completed in place.**

- The opening block now gives the base skill's file path and says what a standalone load loses.
- The requirement-shape bullet lists the five literal line forms `guardrails/specformat.py` parses.
- The index bullet gives the build command and the two-argument gate invocation.
- The preamble bullet points at the code-letter list rather than trailing off at "and the rest".
- The two-way feature check is named: the feature-coverage trace in `tests/test_traceability.py`,
  reading ARCHITECTURE.md's `## Feature coverage` table.
- The fences sentence names `ROADMAP.md` as the file the wish's queue row sits in.

**Four claims corrected against the tree.**

- `guardrails/check-vocabulary.py` was said to red a domain noun used with no glossary entry. Its own
  header states that direction is undecidable and never checked. The page now states the three things
  it does red, and says the cold reader catches the rest.
- The clean-writer leg was cited to `docs/prose-quality-gate-design.md`. That document carries the
  other four legs and not this one. The leg is cited to SPEC INV-84 instead, which is its home.
- The facet list claimed every entry carries its incident. Five of the ten do. The page now says so.
- The design-principle run was called "the verify feel pass". ARCHITECTURE.md names the verify pass
  and the feel pass as two things. The page now names the verify station and points at
  `docs/pipeline.md` station 9.

**Smaller repairs.** The project name is written `tlvphotos` throughout, where three places had
`tlvphoto`. The code-to-location table is called by that one name, where one sentence said
"Formal-index". The one-way fence states the rule it stands for beside its code. The paired-transition
facet declared a "second half" twice for two different things; it now names three parts in order. The
prose-gate paragraph's five legs became a numbered list, which the page's own INV-215 rule asks for.

## What the review looked at

**Does the summary line still trigger correctly?** The frontmatter description is untouched. The
change sits in the body.

**Does the body hold together?** Yes. Each new definition agrees with every later use of the word.
The C-1 floor now resolves into the canonical axis list the page states above it, and the two lists
match. The `[default]` and `[target]` definitions agree with the sections that write those tags.

**Does it instruct anything new?** Three places do, and each is deliberate:

- The parser's five line forms are stated. They were already enforced by
  `guardrails/check-requirement-shape.py`, and a reader who wrote Context as a heading met a red with
  no way to know why.
- The index bullet's two commands are stated. Both are the commands the tree already runs, and
  `docs/handovers/2026-07-27-row496-document-blocks.md` carries the same pair.
- The template sentence names `git clone https://github.com/happysasha18/live-spec` as the way a
  standalone install reaches the templates. The word it replaces, "fetches", named no mechanism.

**Could the change be read as permission to skip a check?** The corrected `check-vocabulary.py`
sentence is the one that invites the reading, since it now says less is caught mechanically. The
sentence closes it by naming who catches the rest: the cold reader, under the comprehension gate this
page already runs.

## Findings

**Three findings were left open, each with its reason.**

- **The named template is in the pre-migration format.** Step 1 says to copy
  `templates/PRODUCT_SPEC.template.md` when starting fresh. That file carries no glossary, no
  `**Context:**` line, no `**User Story:**` line, no `### Acceptance Criteria` heading, and no case
  lines. It closes with a hand-kept "Formal index" table and instructs the opposite section shape. A
  spec started from it fails the gates this page names. `templates/` sits outside this change's
  write-set, so the template is left as it is and the finding is recorded here. The repair above
  softens the cost: the five line forms are now on the page, so a requirement can be written without
  the template.
- **The page carries three declarations of when a section is done.** The completeness pass, the
  comprehension gate, and `scripts/spec-done-gate.py` each claim it, and no sentence orders them.
  Settling that order changes what the skill instructs, so it is recorded rather than written.
- **The `[not a scenario]` marker may be retired.** The INV-132 section tells the author to write it.
  `tests/test_scenario_heading_tag.py` states that the marker retired with the prose shape, and that
  the spec's own R224.3 and R224.4 still carry the old convention. That file records the contradiction
  as a known red awaiting the spec author. Removing the instruction here would settle a question the
  spec owns.

**One observation for a later pass.** The file is 739 lines, and this change added 79. The
skill-creator guide holds 500 lines as the working ideal and asks for a layer of hierarchy past it,
with pointers saying where to go next. The facet list, the fit walk, and the change record are each
self-contained enough to move into a reference file beside the skill. Splitting it is its own
delivery.

**One finding needs the owner's word.** The canonical axis list glosses every axis except **tier**.
The spec's glossary defines *tier* as the model level a unit of work runs at, which is a different
thing from the product axis meant here. Nothing in the tree states the axis sense, so it was left
undefined rather than invented.

## Checks run

`python3 scripts/rule-census.py skills/spec-author/SKILL.md` — 115 findings before, 113 after. The
longest sentence fell from 121 words to 99. The record in `guardrails/rule-census.json` carries 115
for this file, so the count sits below its ceiling.

`python3 scripts/preshow-register-lint.py skills/spec-author/SKILL.md docs/skill-review/2026-08-05-spec-author-readability.md`
— exit 0, no coined metaphor, calque, or transliterated term found.

`python3 scripts/spec-style-lint.py --tier full skills/spec-author/SKILL.md` — 0 errors, 0 warnings.

`python3 guardrails/check-one-name.py skills/spec-author/SKILL.md` — OK, 0 of 13 alias rows matched.

`python3 -m pytest tests/test_config_health.py tests/test_traceability.py -q` — reported in the
audit's own report, together with the fourteen further test files that read this skill's body.

`sh guardrails/check-skill-loadability.sh` — 11 skills load, named, versioned, negative-scoped.

The repository copy and the installed copy under `~/.claude/skills/spec-author/` were compared with
`cmp` and hold the same bytes.
