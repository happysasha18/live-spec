# Skill review — build-pipeline, director, live-spec-base

SKILL-REVIEW

Skill: build-pipeline
Skill: director
Skill: live-spec-base

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is designed for authoring/tuning a skill from test-prompt
benchmarks and would be disproportionate for this slice's small, mechanical reference-file move)
by an agent independent of whoever moved the files and independent of the mechanical adversarial
reviewer (whose findings are recorded separately in
`docs/prover/2026-08-25-work-kind-and-request-kind-homing.md`).

Verdict: PASS, non-blocking notes only.

## What changed

`request-kind-table.md`, `work-kind-table.md`, `footprint-read.md` and `mockup-first-entry.md`
moved from `skills/build-pipeline/references/` to `skills/director/references/` with no content
edits to the files themselves. `skills/build-pipeline/SKILL.md` had 6 in-body citation links
repointed to the new relative path. `skills/live-spec-base/SKILL.md` had one sentence fragment
repointed to name the new home. `director` triggers this gate solely because new files landed
under its `references/` directory — its own `SKILL.md` body was not edited.

## Findings

1. **Non-blocking — citation clarity preserved through the move.** All 6 repointed citations in
   `skills/build-pipeline/SKILL.md` (lines 123, 138, 161, 180, 288, 299) already carry surrounding
   prose explaining what's in the target file and when to open it (e.g. line 138: "for the full
   read: how the footprint composes with the door, and what each footprint grants each step");
   only the relative path changed, none became a bare link. All 4 targets verified to resolve on
   disk. No fix needed.

2. **Non-blocking — `director`'s frontmatter description doesn't enumerate its `references/`
   holdings.** Pre-existing gap (it already held 5 other reference files before this slice);
   `live-spec-base`'s description does list its own reference modules, `director`'s does not. The
   4 newly-moved files add to an existing gap rather than creating a new inaccuracy. Left as-is —
   not something this mechanical slice should fix in passing.

3. **Non-blocking, already documented — `director/SKILL.md`'s own body doesn't yet cite any of
   the 4 newly-landed files.** Confirmed by grep: none of the 4 filenames appear in director's
   prose yet. This is the deliberate, explicitly multi-slice state `docs/director/capability-map.md`
   (the "2026-08-25 — four more class-b files given a home" section) documents: give the content a
   real home first, wire it into director's own body in a later slice, rather than a hasty
   single-slice delete-and-supersede. Not a fresh oversight.

4. **Non-blocking — `build-pipeline` (728 lines) remains well over the pack's ~500-line ideal.**
   Pre-existing, tracked separately by the ongoing cutover; this diff added zero net lines to any
   SKILL.md body (citation lines got longer, not more numerous).

5. **No dangling or decorative citations found.** Affected test suites re-run clean (210 tests,
   `test_setup_entry.py`/`test_skill_kind_review.py`/`test_traceability.py`), and
   `guardrails/check-skill-review.sh` confirmed it correctly flags all three named skills against
   `origin/main` before this record existed.

No finding beyond what `docs/director/capability-map.md` and the mechanical adversarial review
already establish as deliberate or transitional.
