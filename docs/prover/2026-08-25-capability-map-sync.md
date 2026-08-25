# Prover record — 2026-08-25 capability-map-sync

PUSH-REVIEW

Range: 41cf2a04..24d7a0bd (1 commit, docs/director/capability-map.md only — a design manifest,
nothing reads it at runtime per its own opening line)
- 24d7a0bd capability-map: fix row 14's stale path, record the step-3 premise finding

Files read: `docs/director/capability-map.md` full diff — row 14's path corrected to the
post-move location, and a new dated section recording this session's finding that the cutover
plan's step 3 (delete build-pipeline lines 113-596) rests on a false premise for a substantial
part of that range. Cross-checked the new section's claims against
`docs/prover/2026-08-25-build-pipeline-cutover-slice-1.md` (steps 1-2 landed, commits/CI cited
match) and against this session's own research findings (line-range classification already
independently produced and reviewed earlier this session, not re-derived here).

Checks run: previous records this session clean (`2026-08-25-build-pipeline-cutover-slice-1.md`,
`2026-08-25-readme-turnkey-goal.md`, both Blocking: none). This is a prose/manifest-only delta,
no new surface, no structure change (SHORT-FORM per build-pipeline's own process-bookkeeping
scaling rule) — no code or test touched, so no test run owed beyond confirming the file is
prose-only: `git diff --stat` shows only `docs/director/capability-map.md`.

Findings: none — a documentation-accuracy correction and a research-finding record, not a
functional change.

Blocking: none
