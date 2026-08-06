# Skill review — build-pipeline and spec-author (the spoken setup entry)

SKILL-REVIEW

Skill: build-pipeline
Skill: spec-author

Date: 2026-08-06
Reviewer: a worker session raised for this review alone. It did not author the change under review,
and it read every file and every command's output from its own reading. It ran the parts of
Anthropic's skill-creator guidance that read the artifact: the description field as the primary
triggering surface and its pushiness rule, progressive disclosure and the reference-file pattern,
SKILL.md body length, imperative form, explain-the-why over heavy MUSTs, and the principle of lack
of surprise. The stages that need a person and a browser did not run, and they are named below.

Verdict: the delta passes on skill-creator's bar for description writing and progressive
disclosure — the new arm names the sentences a person actually says, the body section is ten lines
that hand the detail to a reference file, and the reference file holds routing with the walk phases
left in the walks. Three findings were raised as blocking and all three are answered: two repairs
landed in the skill surface in this same session, and one is the spec identifiers that the
orchestrating session lands with the shared documents. Six recommendations and notes stand, of which
two are taken and the rest are recorded with their reasons.

## What changed

`skills/build-pipeline/SKILL.md` — the `description:` field gained an arm covering three spoken setup
entries, and one body section, "Setting a project up on the pack", was added after "Work that belongs
elsewhere".

`skills/build-pipeline/references/project-setup.md` — new. The routing card: six ordered reads that
resolve the pack's own tree, then a table picking one of three setup walks.

`skills/build-pipeline/references/request-kind-table.md` — three rows appended to the closed request
set, with one sentence naming the card and the tree those three entry documents sit in.

`skills/spec-author/SKILL.md` — the `description:` field gained one clause naming build-pipeline's
setup entry as the earlier door.

## What did not run, and why

The skill-creator loop's later stages need a person in the loop and a browser: the with-skill and
baseline subagent runs feeding the eval viewer, the human feedback pass, and the description
optimizer, which drives `claude -p` over twenty trigger queries the person signs off on. Neither the
person nor a browser was available to this session. The triggering claim is therefore unmeasured, and
the delta says so in its own artifact: `evals/build-pipeline.md` gained Scenario C, ten scored
phrases with a stated method, every result cell reading "to be scored". Finding 6 records that state.

## Finding 1 — `SPEC INV-307` resolves to nothing today. Raised as blocking; answered.

The reviewer grepped every markdown file for `INV-307` and found two hits: the sentence appended to
`references/request-kind-table.md` and the docstring of `tests/test_setup_entry.py`. `PRODUCT_SPEC.md`
carries INV-300 through INV-304 and stops. The same test docstring cites Requirement 308, matrix rows
M-512 through M-518, and queue row 557, and none of those stands in `PRODUCT_SPEC.md`,
`TEST_MATRIX.md`, or `ROADMAP.md`.

Answer: those identifiers were assigned to this work and the documents that carry them are landed by
the orchestrating session, which owns `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `TEST_MATRIX.md`,
`ROADMAP.md`, `JOURNAL.md`, and `NEXT_STEPS.md` in this change. The citation is forward-facing by
construction, and it resolves when those documents land in the same push. The landing gate is where
that is checked: a push carrying the skill surface without the spec side would leave the anchor
dangling, and the orchestrator holds both halves.

## Finding 2 — `pack.tree` was a settings key with no ladder row. Raised as blocking; repaired.

The card offered the resolved path for the person's own profile as a `pack.tree` line. A grep across
every markdown file returned that one occurrence: the settings ladder in `skills/live-spec-base/SKILL.md`
carries no such row, so a line written on that instruction is read by nothing.

Repair, landed: the card now states plainly that the line is a note the person keeps, that the ladder
carries no `pack.tree` row yet, and that making it a recognised setting is a change of its own. The
design this build follows had already set that work aside as a later row; the card no longer implies
a mechanism that does not exist. The follow-up row is owed by the orchestrating session, which owns
the queue.

## Finding 3 — the card contradicted its own scope and wrote into a directory that may not exist. Raised as blocking; repaired.

The card opened by claiming it does two things and no more, then instructed a record write under
`.live-spec/`. On the founding path that directory does not exist at that moment: `adopt/START.md`
records founding progress at `.live-spec/adopt/found.md` and `adopt/ADOPT.md` describes `.live-spec/`
as the record directory a run establishes.

Repair, landed: the opening now states what the card does — it finds the tree, says what it found,
and names the walk — and the record paragraph says that the line is spoken first, that the walk
carries it into its own record under `.live-spec/`, and that on a fresh project the walk creates that
directory at the phase which writes the record.

## Finding 4 — the body section's second path pointer worked against the card's own reason. Recommendation; taken.

The body section named the card twice: once as `references/project-setup.md` and once as the absolute
`skills/build-pipeline/references/project-setup.md` in the pack's own tree. `install.sh` copies
`skills/*` into `~/.claude/skills/` and touches nothing else, which is the route the card exists for,
and on that route the second path names a location that may be absent while the first resolves beside
the SKILL.md.

Repair, landed: the second clause is dropped. The test that pins this criterion moved with it, from
the absolute path to the path a session actually reads the card at.

## Finding 5 — the description is 477 characters, the longest of eleven. Recommendation; recorded, not taken.

Measured over all eleven shipped fields: text-audit 122 characters, test-author 128, design-reviewer
202, publish 209, feedback-collector 246, feedback-intake 251, product-prover 293, spec-author 302,
communicator 328, live-spec-base 383, build-pipeline 477. The field grew from 204 characters. The
guidance names the description as the primary triggering mechanism, asks for both what the skill does
and the contexts it is for, and asks for pushy phrasing against undertriggering, so the five spoken
variants are the coverage that guidance calls for and the length buys something.

The reviewer's recommendation: the closing exclusion, "A tiny reversible edit and pure research stay
outside it", now sits after the setup arm, and the word "it" has two candidate referents. Naming the
pipeline explicitly would settle it.

Recorded rather than taken: the design under build states this field's text verbatim, so changing its
closing sentence is a decision for the design's owner. It goes to the orchestrating session with this
record.

## Finding 6 — the triggering claim is unmeasured, and the artifact says so. Note.

`evals/build-pipeline.md` gained Scenario C on the same day: eight phrases that shall load the skill,
two near-misses that shall miss it, one fresh session per phrase with the phrase as the whole first
message, and every result cell reading "to be scored". The scenario also records the length
comparison and says to score it again after any later growth of the field. That is the correct parked
state while the optimizer and the human review are out of reach, and the claim stands unverified
until it runs.

## Finding 7 — spec-author's clause does its job. Note.

The clause is "Setting a project up on live-spec comes earlier, at build-pipeline's setup entry." The
field grew from 220 characters to 302. It sits between the trigger list and the existing exclusion
list, which is where this field puts an exclusion, and it names the destination rather than only
refusing the work. None of spec-author's own three trigger phrasings was touched. The one contested
sentence is "start a new project with live-spec", which the eval scores against the bare "start a new
project" to measure whether the pack's name is what does the picking.

## Finding 8 — the card is well formed, with two shape deviations from its siblings. Recommendation; both taken.

The reviewer read all six sibling files under `skills/build-pipeline/references/`. Each opens with one
line naming the SKILL.md section that refers to it, and the card skipped that back-pointer; the card
now carries it. The reviewer also found the sibling link written as `references/project-setup.md`
from inside `references/`, where the plain sibling form resolves; that link is now
`[project-setup.md](project-setup.md)`.

On content the reviewer confirmed the card holds no phase, no copy table, and no done-condition, so
no walk material leaked into it, and it checked the card's machine claims against this machine's real
`~/.claude/plugins/installed_plugins.json`: the entry key is `<plugin>@<marketplace>`, the value is an
array of objects each carrying `installPath`, and the real install path sits three levels under
`cache/` — the shapes reads 3 and 4 assume.

## Finding 9 — three walk paths named with no tree. Recommendation; taken.

The three appended request-kind rows name `adopt/ADOPT.md`, `adopt/START.md`, and `MIGRATION.md`,
while the skill's own path convention assigns neither `adopt/` nor a bare `MIGRATION.md` to either
repository, and a host project may carry a `MIGRATION.md` of its own. The sentence under the table now
says all three sit in the resolved pack tree and warns that a host file of the same name means
something else.

## Finding 10 — an unverifiable supporting claim in read 2. Note; repaired.

Read 2's justification cited other plugins' hook files as using `${CLAUDE_PLUGIN_ROOT}` for the same
purpose. A grep across this machine's plugin cache returns nothing, and the one cached plugin carries
no hooks directory. The sentence now states only what holds here: the harness sets that variable to a
plugin's own root while the plugin runs.

## Finding 11 — the clone's tag route is the exception on this repository today. Note.

`git tag` returns v1.0.0, v2.7.0, v2.8.0 and two named saves, while `VERSION` and every SKILL.md read
4.3.0, so no tag matches the installed version and every clone taken today lands on the card's
fallback. The fallback is written and it says both numbers aloud, so nothing breaks; the instruction
reads as though the tag were the ordinary case. Left as written, because the design states this route.

## Finding 12 — the installed copy carries neither the arm nor the card. Note.

`~/.claude/skills/build-pipeline/references/` holds the six older files, and the installed SKILL.md
still carries the 204-character description. Until the installed-copy sync runs, the spoken sentence
loads nothing on this machine. That sync is the landing's own step, and it goes to the orchestrating
session with this record.

## Finding 13 — SKILL.md stands at 672 lines against a 500-line guide. Recommendation on a standing problem.

`wc -l` reads 672 lines for `skills/build-pipeline/SKILL.md`; this change added 10 of them. The
guidance asks for a body under 500 lines and, past that, another layer of hierarchy with pointers.
Four skills in the pack already exceed it: product-prover 1054 lines, live-spec-base 742,
spec-author 739, build-pipeline 672. This change handled its own material the way the guidance asks —
ten lines in the body against sixty-eight in a reference file — so it adds the least its content
allows. The standing overrun deserves a queue row of its own.

## Checks run

- `git diff -- skills/`, and `git show HEAD:` on both SKILL.md files for the pre-change fields.
- A Python pass over all eleven `skills/*/SKILL.md` frontmatters, extracting each description and
  counting its characters and words.
- `wc -l` over every skill body and over the seven files in build-pipeline's `references/`.
- `grep -rn "INV-307"` and `grep -n "Requirement 308\|M-51[2-8]"` over the working tree; the highest
  invariant in `PRODUCT_SPEC.md` read out with `grep -oE 'INV-[0-9]+' | sort -n | tail`.
- `grep -rn "pack\.tree"` over every markdown file; the settings ladder in
  `skills/live-spec-base/SKILL.md` read at its defaults table.
- `cat` of all six sibling reference files, for register and opening shape.
- `cat install.sh`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `VERSION`,
  `git tag`.
- This machine's `~/.claude/plugins/installed_plugins.json` and `~/.claude/plugins/cache/` read for
  the registry's real shape and depth; `grep -rl "CLAUDE_PLUGIN_ROOT"` over the cache.
- `ls ~/.claude/skills/build-pipeline/references/` and the first lines of its installed SKILL.md.
- After the repairs: `python3 -m pytest tests/test_setup_entry.py tests/test_catchup_walk.py -q` —
  36 passed.
