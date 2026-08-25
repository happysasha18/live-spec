# Skill review — architect, build-pipeline, director

SKILL-REVIEW

Skill: architect
Skill: build-pipeline
Skill: director

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is designed for authoring/tuning a skill from test-prompt
benchmarks and would be disproportionate for this slice's small, mechanical reference-file move)

Verdict: changes folded — one blocking finding fixed (a broken cross-skill link); three
non-blocking findings recorded, all either pre-existing or a deliberately documented transitional
state per `docs/director/capability-map.md`.

## What changed

The build-pipeline cutover's first slice moved 5 reference files out of
`skills/build-pipeline/references/`: `architecture-step-detail.md` to
`skills/architect/references/` (new directory), and `delegation-protocol.md`,
`excuses-table.md`, `lanes-and-pen.md`, `guardrails-catalog.md` to
`skills/director/references/`. No skill's own normative content was rewritten — this is a
relocation of existing material plus the citations that point at it.

## Findings

An independent agent (not the mover) read all three skills' current full `SKILL.md` files, every
touched `references/` file, and applied both a general coherence check and the skill-creator
writing guide's concrete criteria (line-count budget against the ~500-line guideline, whether a
reference citation explains *when* to open the file rather than dropping a bare link, whether any
reference file over 300 lines needs a table of contents, and frontmatter `description` accuracy
and length).

1. **Blocking, found and fixed — `skills/build-pipeline/SKILL.md:675`.** A citation to
   `references/delegation-protocol.md` was missed by the mover (the worker that moved this file
   crashed mid-task right before reaching this exact line, per the orchestrator's own recovery
   notes) — it still pointed at the file's old, now-nonexistent local path. Every other citation
   this slice touched was correctly repointed; this was the one exception. Fixed: repointed to
   `../director/references/delegation-protocol.md`. Confirmed no test or guardrail currently
   catches a dangling markdown link of this shape (`check-skill-loadability.sh` validates
   frontmatter only) — this class of bug is caught by review, not mechanically, today.
   Re-verified after the fix: `tests/test_traceability.py`, `test_worker_restore.py`,
   `test_no_dramatization_law.py`, `test_delegation_line.py`, `test_architect_extraction.py` all
   pass (336 passed).

2. **Non-blocking — `skills/architect/SKILL.md`'s 3 new citations to
   `architecture-step-detail.md` (lines 79-81, 111-113, 126-128) are decorative, not
   elaborative.** Each cited passage is a near-verbatim restatement of the sentence immediately
   before it in the body, rather than genuine additional detail the way build-pipeline's own
   `delegation-protocol.md`/`footprint-read.md` citations deliver real elaboration. Not a broken
   link (paths resolve correctly) and not something this slice introduced — it's the wording
   build-pipeline originally used, carried over unchanged by the architect-extraction package
   (row 21, closed 2026-08-24, before this slice). Left as-is: reworking the citation style is a
   content-authorship decision outside this slice's mechanical scope, not a defect this move
   caused.

3. **Non-blocking — 3 of `skills/director/SKILL.md`'s 4 newly-local reference files are
   uncited in its own body.** `excuses-table.md`, `lanes-and-pen.md`, and
   `guardrails-catalog.md` now live in `skills/director/references/` purely because
   `build-pipeline/SKILL.md`'s own citations point there; nothing in director's prose yet
   explains why they're present or when to read them. `docs/director/capability-map.md`'s
   2026-08-25 cutover-slice-plan section documents this as deliberate pre-positioning ahead of
   later slices (steps 3-5 of the same plan, which delete the superseded prose from
   build-pipeline and will need these files wired into director's own body at that point) — a
   known, short-lived transitional state, not an oversight. Left as-is; wiring them into
   director's prose belongs to the later slice that actually retires the content they're
   fall-through targets for.

4. **Non-blocking — `skills/director/SKILL.md:234`'s historical citation now names a
   confusing path.** The sentence ("The fixed protocol this replaces
   [`skills/build-pipeline/references/delegation-protocol.md`] carried tier ladders, escrow law
   and a reporting bureaucracy... none of it survives the cut into this skill") was written,
   before this slice, as a deliberately non-live historical pointer — `capability-map.md`'s own
   cutover-slice-plan note already flags this exact line as prose describing what director
   replaces, "not a live read." The file this sentence names has now physically moved to sit
   right beside this very document, uncited by path, which reads oddly on a fresh pass but does
   not change the sentence's truth value or break any live dependency. Left as-is, per the
   already-recorded prior decision not to treat this citation as a live path.

Both the mechanical file-move correctness (tests, cross-references, `CLAUSE_HOMES`,
`sync-skills.sh`) and this skill-quality pass were reviewed by agents independent of whoever
authored each piece; the mechanical review's full findings and re-verification are recorded
separately in `docs/prover/2026-08-25-build-pipeline-cutover-slice-1.md`.
