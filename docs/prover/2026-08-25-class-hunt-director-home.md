# Prover record — 2026-08-25 class-hunt-director-home

PUSH-REVIEW

Range: 6ff7f9d1..e963bb8d (3 commits) — widened to cover the tests-present follow-up too, per the
gate a self-naming arm (one record names the base plus every non-exempt commit together)
- b056c28a Give the bug class hunt a home in Director (batch-2b 12th item)
- 28352591 Skill-review record for the class-hunt Director home
- e963bb8d Add the missing test for class-hunt's Director home

Files read: full diff of b056c28a (2 files, 32 insertions); `skills/director/references/
class-hunt.md`, `skills/director/SKILL.md` (current state, not just the diff); the source text
in `skills/build-pipeline/SKILL.md` ("A confirmed bug drives a class hunt before it closes");
`skills/live-spec-base/SKILL.md` rule 14 (confirmed untouched by this range — its cross-reference
still names only `build-pipeline/SKILL.md`, correctly, since the fast-follow hasn't landed yet);
`tests/test_class_hunt.py` in full (the closed-home-set test this fact is pinned to today).

Checks run: an earlier investigation this session found `docs/director/capability-map.md`'s
cutover-plan notes (written before today's batch-2b work landed) named the confirmed-bug 4-move
class hunt as homeless, but the fact never made it onto the 11-item batch-2b list this session
actually worked from. Re-checked against `tests/test_class_hunt.py`, confirmed it pins the fact
to `skills/build-pipeline/SKILL.md` alone (`test_build_pipeline_bug_entry_drives_the_hunt`), with
`skills/live-spec-base/SKILL.md` rule 14 cross-referencing that same location as "the full
four-move law" — genuinely homeless everywhere else, including Director, which this range fixes.

Two independent adversarial review rounds, each catching a real, different defect:
- Round 1: a near-verbatim 5-word lift ("a boundary drawn wrong or") from build-pipeline's source,
  and a stray literal "door" surviving inside an unrelated idiom ("false next door") — Director's
  own vocabulary deliberately excludes that word. Both reworded.
- Round 2, after the round-1 reword: the replacement phrasing ("an assumption that holds in one
  spot and breaks in a neighbouring one") turned out to share a fresh 6-word verbatim run with
  BOTH the build-pipeline source and live-spec-base's own rule 14 ("an assumption that holds in
  one"). Reworded a second time to "a premise safe here but false one step over," verified clean
  by a programmatic 5-gram overlap check against both source texts (not eyeballing — the first
  reword's own overlap had passed a visual check and still failed a fresh automated scan).
  Round 2 also caught a broken inline code span from an intermediate edit to rule 14 (a Markdown
  line-wrap had split `` `skills/build-pipeline/SKILL.md` `` across two lines, which renders with
  a stray space per CommonMark's line-collapse rule) — moot once that edit was reverted per the
  next finding, but confirmed fixed at the point it existed.

A third finding, from a DIFFERENT reviewer working an unrelated concurrent task (A.7's rule
compression, which also touches `live-spec-base/SKILL.md`): a draft of this change had rewritten
rule 14's cross-reference sentence to add `class-hunt.md` as a second home, while that sentence's
home file was still mid-review and could have been rejected or reworded. The A.7 reviewer
correctly flagged this as coupling a stable, already-twice-reviewed rulebook to a same-session,
unstable file — exactly the sequencing risk this session's own working method exists to catch.
Reverted `live-spec-base/SKILL.md` to its pre-existing wording (confirmed byte-identical by the
A.7 reviewer independently); the class-hunt reviewer then re-scoped its own approval to exactly
the two files in this range and confirmed dropping the cross-reference resolved its own concern
for this specific commit, since `class-hunt.md` never claims to be the fact's only home. The rule
14 cross-reference is deferred to its own fast-follow commit, landing only now that this range is
itself committed and stable — not before.

The local push gate's `gate h` (tests-present) caught a real gap on the first push attempt: the
`director/SKILL.md`/`class-hunt.md` commit changed a user-facing skill file with no accompanying
change under `tests/`. Fixed properly, not just to satisfy the gate: `tests/test_class_hunt.py`
already lists this fact's homes in its own module docstring, so a new test function,
`test_director_has_its_own_home_for_the_hunt`, was added there — the same file, same convention
as the existing `test_build_pipeline_bug_entry_drives_the_hunt` — asserting Director's SKILL.md
points at `references/class-hunt.md` and that file states all four moves plus the closing
INV-26 citation. This closes a real traceability gap the docstring's own "Homes:" line would
otherwise have left silently stale.

Independently: `python3 -m pytest -q tests/test_class_hunt.py tests/test_traceability.py
tests/test_director_scenarios.py` — 206 passed, 3 skipped (external product-prover canon clone
absent locally, expected), run independently by two different reviewers across three review
rounds with matching results each time. `scripts/spec-style-lint.py --tier universal` on both
touched files: 0 errors (class-hunt.md 0 warnings too; director/SKILL.md's 29 pre-existing errors
and 9 warnings unchanged in count, confirmed by diff against the pre-edit baseline).
`bash guardrails/check-pin-drift.sh`: exits 0, no FAIL lines. `bash scripts/sync-skills.sh`:
nothing to sync, director's installed copy already matched. `bash guardrails/
check-config-health.sh`: clean.

Findings: three real defects caught across two adversarial review rounds and one cross-task
coordination check, all fixed and independently re-verified (described above). No other defect
found.

This closes the 12th, previously-unlisted batch-2b item. Combined with the earlier 3-slice batch-
2b work (`docs/prover/2026-08-25-batch-2b-slice-1-lane-kind-reach.md`,
`-slice-2-changelog-removal.md`, `-slice-3-and-a5.md`): of the original 11 items plus this
late-discovered 12th, 7 real facts now have homes (INV-131, INV-12+safety-net, INV-45,
CHANGELOG-vs-journal, removal-of-shipped-feature, recurring-bug-redoor, the class hunt), 5 were
confirmed already fully spec'd and needed nothing (INV-70, INV-114, Step 7 INV-62/63,
push-mechanics INV-82/106, docs-layout pass INV-111). One small fast-follow remains: wiring
`live-spec-base/SKILL.md` rule 14's cross-reference to `class-hunt.md` now that it's real and
committed — a one-sentence edit, its own tiny commit, not a design question.

Blocking: none
