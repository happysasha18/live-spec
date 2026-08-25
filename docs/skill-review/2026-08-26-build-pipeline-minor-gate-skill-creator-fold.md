# Skill review — build-pipeline

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-08-26
Reviewer: skill-creator quality lens applied by hand for THIS one-sentence prose addition
(Progressive Disclosure, frontmatter-description accuracy, house citation convention) — this
record is separate from Полоса B п.10's own real skill-creator eval/iterate run (subagent-driven,
with-skill/baseline benchmarking, objective assertions), which is what SURFACED this finding in
the first place. That run is documented in the working handoff and its full artifacts (test
prompts, benchmark.json, static HTML viewers) live at `/private/tmp/ls-director/
skill-eval-workspaces/` (outside git, not pushed).

Verdict: no blocking findings after two rounds of independent adversarial review; frontmatter
unchanged, body content added to close a real, spec-verified gap.

## What changed

Полоса B п.10's real skill-creator eval (one honest measurement round, no human present tonight
to run the full interactive iterate loop — see handoff for the headless-mode adaptation) ran
with-skill vs. baseline subagents against `build-pipeline`'s MINOR-bump-gate scope. One eval
independently found and cited `spec/push-gate-milestone-audit.md`'s Requirement 130 (SPEC M-1),
whose acceptance criteria 3-4 require the milestone/MINOR gate to re-run the skill evals and walk
every skill in the pack through skill-creator's craft review — neither mentioned anywhere in
`skills/build-pipeline/references/minor-bump-gate.md`, which covered only the 3-pass audit,
design review, cross-cut counter, and code compaction. Verified independently (not taken on the
eval's word): `git show` confirmed zero occurrences of "skill evals"/"skill-creator" in the
pre-fix file, and `spec/push-gate-milestone-audit.md`'s Requirement 130 text was read directly.
A second finding from the same eval run — that build-pipeline never mentions the release-tier law
(INV-217) or fresh-seat certification (INV-237) — was checked and found to be a false positive:
both already live in full in `skills/director/references/landing-law.md`, moved there earlier in
the build-pipeline cutover; the eval tested build-pipeline in isolation from director, which real
usage never does. Left untouched.

Fix: added one paragraph to `minor-bump-gate.md` naming the skill-creator craft review and the
skill-evals re-run, citing SPEC M-1 in the file's own established bare-anchor style. Updated
`skills/build-pipeline/SKILL.md`'s "Gates worth remembering" bullet — which exhaustively lists the
gate procedure's contents — to add the fifth item, so the two files stay in sync.

## Findings

None blocking, after two rounds of independent adversarial review (both required, both real —
this was not a rubber-stamp). Round 1: **BLOCK**, two defects: (a) the fix updated
`minor-bump-gate.md` but left `build-pipeline/SKILL.md`'s own exhaustive bullet-list summary of
that same file's contents one item short — the exact class of drift this pack's own machinery
exists to catch, sitting one file away, uncaught by any test; (b) the new paragraph cited
`(Requirement 130, SPEC M-1)`, a citation form used nowhere else in any skill body/reference file
in the pack (it's exclusive to `docs/prover/*.md` audit records) — every other citation in the
same file uses a bare `SPEC INV-NNN`/`SPEC M-N` form, and the correct precedent
(`skills/live-spec-base/SKILL.md:410`) confirmed the bare form. Both fixed: the SKILL.md bullet
now names the skill-creator craft review as its fifth item, and the citation dropped the
"Requirement 130," prefix to read `(SPEC M-1)` alone. Round 2 (same reviewer, re-verifying its own
prior findings independently, not on trust): **ALLOW** — re-read the diff directly, grepped both
changed files for zero remaining "Requirement 130" occurrences, re-ran the same test target (227
passed, 1 skipped) and both guardrail scripts, confirmed no regression.

Per-skill check: **build-pipeline** — frontmatter `description` (unchanged) still accurately
describes the narrow transitional-adapter scope; the addition is pure content (a real Requirement
130 obligation the reference file was missing), not a scope change, and now correctly cross-links
with the SKILL.md summary that points to it. A 5-word n-gram check against
`spec/push-gate-milestone-audit.md`'s Requirement 130 text found zero verbatim overlap — the new
paragraph is independently phrased in the file's own voice, not copied.
