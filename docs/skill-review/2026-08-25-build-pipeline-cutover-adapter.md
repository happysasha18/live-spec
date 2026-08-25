# Skill review — build-pipeline, communicator, publish, test-author, director, architect

SKILL-REVIEW

Skill: build-pipeline
Skill: communicator
Skill: publish
Skill: test-author
Skill: director
Skill: architect

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is designed for authoring/tuning a skill from test-prompt
benchmarks and is reserved for Полоса B п.10, after the whole build-pipeline cutover completes,
per the owner's explicit instruction not to skip that step)

Verdict: no blocking findings; body/frontmatter coherence checked skill by skill below, all pass.

## What changed

`build-pipeline/SKILL.md` shrunk from 728 to ~65 lines (transitional adapter: craft ladder +
setup-walk pointer + MINOR-bump-gate pointer + "Work that belongs elsewhere" section, added in a
fast-follow commit once the local push gate's loadability check (gate f, row 80) caught its
absence; frontmatter description rewritten to match). `build-pipeline/README.md` rewritten to
match the same new scope. New reference file
`director/references/build-craft.md` (build-smallest-first, source-reopens, norm-pointered
building — Step 7 content with no other home). Small additive sections in `publish/SKILL.md`
(push mechanics) and `communicator/SKILL.md` (defaults-telling). One table-cell edit in
`director/SKILL.md` (Developer row, adds the build-craft.md pointer). Two-line stale-reference
fix in `test-author/SKILL.md`, one-sentence stale-caveat removal in `architect/SKILL.md`.

## Findings

None blocking. Per-skill check:

- **build-pipeline** — frontmatter `description` now accurately states the narrow scope (setup
  walk + MINOR-bump gate, explicitly says it is not the pipeline's entry point). Body reads
  coherently standalone; no dangling references to the removed door/work-kind/footprint/
  request-kind tables or the old nine-step sequence. Progressive disclosure intact:
  `project-setup.md` and `minor-bump-gate.md` stay as reference-file pointers, not inlined. The
  added "Work that belongs elsewhere" section names `director` as the sole destination for any
  accepted change, matching the rest of the page; no new dangling reference introduced.
- **communicator** — the 6-line addition sits inside the existing rule-10 decision-page bullet
  list, matches the surrounding voice ("silence is consent... never re-asked") verbatim in
  register. No frontmatter touch needed; scope (carrying decisions to the human) already covers
  this addition.
- **publish** — the new "Reaching the remote — push mechanics" subsection sits directly after the
  existing shopfront-walk section it's thematically adjacent to (publish already owns push-time
  README freshness). No frontmatter touch needed; publish's existing scope ("checks a publication
  owes its reader") already covers push mechanics as a natural extension.
- **test-author** — two isolated one-line factual fixes (director now named as the caller,
  matching its own "pack, whole" line and director's own specialist table), no structural or
  frontmatter change.
- **director** — exactly one table cell touched (Developer row), format matches the table's
  existing convention (other rows already carry bracketed reference-file links, e.g. Independent
  verifier). No frontmatter change; this is the only touch to `director/SKILL.md` in the whole
  cutover slice, per the standing rule against re-touching this file without need.
- **architect** — removed a now-false caveat (build-pipeline no longer carries an inline copy of
  the architecture method — its own step 3 is gone). The surrounding paragraph reads cleanly
  without it; no replacement content needed.

Not blocking, noted for the record (already named in the commit message and the handoff, not
silent): three further stale build-pipeline references survive elsewhere in the tree
(`skills/live-spec-base/SKILL.md` rule 14's cross-reference; `architecture/pipeline-and-lanes.md`'s
`[node: build-pipeline]` responsibility/owns-list; the "pack, whole" roster lines in
`test-author/SKILL.md` and `architect/SKILL.md`) — out of scope for this slice (live-spec-base is
closed for this cutover; the roster lines and the architecture node's identity need their own
dedicated pass, not a piecemeal touch here or they risk the closing-roster trap §5.16/§5.17 warns
against).

## CI red-fix addendum (dadb67db)

The full suite (gate b, CI-only) found 25 more tests across ~20 files this session's local runs
never covered, all asserting facts build-pipeline's old surface used to carry as a second witness.
Fixed by: a new reference file, `director/references/landing-law.md` (eight push/commit-time
facts, near-verbatim from the pre-cutover text — genuine relocation, not duplication); one more
`director/SKILL.md` pointer paragraph (Execution section, after "Closing the work closes the
checkpoint..."); an extension to `publish/SKILL.md`'s existing push-mechanics section (the fuller
original wording, needed verbatim by two tests); a one-line compression in `communicator/SKILL.md`
(504 -> 499 lines, back under its own 500-line size ideal, row 280). No new `Skill:` beyond the six
already named above — `director`, `communicator`, `publish` are the ones re-touched, all covered.
Verdict unchanged: no blocking findings. Re-checked `director/SKILL.md`'s structure after the
second pointer paragraph — still exactly two touches total to that file across this whole cutover
slice (the Developer table-cell edit, and this landing-law pointer), both minimal and reviewed.
`publish/SKILL.md`'s push-mechanics section and the new `landing-law.md` file cover genuinely
different ground (remote/README/CI-verdict mechanics vs. tripwire/merge-gate/compaction/
release-tier/skill-review/verify-station/docs-layout/removal-accounting) — no duplication between
them, confirmed by independent review. 476 passed, 9 skipped, 0 failed on the full targeted
re-run; `check-pin-drift.sh`, `check-skill-loadability.sh`, `check-config-health.sh` all clean.

`scripts/sync-skills.sh` re-run after all edits: build-pipeline, director, test-author, architect,
communicator, publish all installed-copy-matches-source, no drift.
