# Prover record — 2026-08-24 director-acting-ci-fix

PUSH-REVIEW

Range: 1add2fe2..72b15120
- 72b15120 director: revert frontmatter version to 5.0.0 — version is one pack fact (INV-178)

Files read: `git show 72b15120` in full (both hunks); `skills/director/SKILL.md`'s current
frontmatter; `VERSION`; `tests/test_version_is_one_fact.py` in full, current state (not just its
name); `JOURNAL.md`'s corrected heading line and the entry body below it (untouched by this
commit); `git show 72b15120 --stat` to confirm file scope; `git log --oneline -1 --
scripts/sync-skills.sh` to confirm that script's own file is untouched by this commit (the
commit message's "sync-skills.sh re-run to match" describes running the script against an
external install target, not a change to the script file itself).

Checks run: confirmed the diff is exactly the claimed two-line fix, confirmed the frontmatter
now matches VERSION, ran the actual test CI caught this on.
- `git show 72b15120 --stat` — exactly `JOURNAL.md | 2 +-` and `skills/director/SKILL.md | 2
  +-`, 2 files changed, 2 insertions(+), 2 deletions(-): nothing beyond the claimed revert plus
  heading correction.
- `skills/director/SKILL.md`'s frontmatter, read directly: `version: 5.0.0`. `cat VERSION`:
  `5.0.0`. The two now match, which is the entire substance of the fix.
- `python3 -m pytest tests/test_version_is_one_fact.py -q` (backgrounded, exact path, per the
  standing hard rule) — `5 passed in 0.13s`. Read the test file in full rather than trusting the
  name: `test_every_skill_frontmatter_version_equals_pack_version` walks every pack-owned
  `skills/*/SKILL.md` (via `_skills()`, which fences out any skill dir carrying its own `.git` —
  an external clone, not this pack's fact to stamp) and asserts each frontmatter `version:` line
  equals the root `VERSION` file's contents exactly; this is the assertion `director`'s `6.0.0`
  frontmatter value broke and `72b15120`'s revert fixes, confirmed passing now, not merely
  assumed from the file's docstring. Also checked `test_every_base_reference_equals_pack_version`
  or a potential dangling in-text version reference: `grep -n "live-spec-base"
  skills/director/SKILL.md` shows two bare mentions of `live-spec-base`, neither carrying a `(v...
  )` version suffix, so this file had nothing for that second assertion to catch either way — not
  a gap this fix needed to touch. `test_spec_states_the_law` (part of the same 5 passed) confirms
  `PRODUCT_SPEC.md` still states "version is one fact" and carries the `| INV-178 |` row the
  commit message cites, independent of anything in this range (untouched by it).
  `tests/test_guardrails.py::TestGateB_Tests::test_real_content_passes` (the other test the
  orchestrator's report named as having gone red in CI alongside `test_version_is_one_fact.py`,
  since it reruns the full suite in a scratch copy and would have inherited the same failure) was
  not independently re-run this round — per this project's own standing, previously-recorded
  caveat (`docs/prover/2026-08-24-redundancy-coverage-fix.md` and others in this history) that
  this specific test carries a separate, pre-existing, machine-local pin-drift failure mode
  unrelated to any content change and is excluded from routine local reruns for that reason; the
  root-cause test named in the orchestrator's own report (`test_version_is_one_fact.py`) is the
  one this commit's fix actually targets, and it is independently confirmed green above without
  relying on that wrapper.
- `git log --oneline -1 -- scripts/sync-skills.sh` — last change is an unrelated, older commit
  (`7b2980df`), confirming the commit message's "sync-skills.sh re-run to match" describes
  running the existing script against an external skills-mirror target (outside this repo's
  tracked tree), not a change to the script's own source — consistent with the empty diff for
  that file.

Findings: this is a small, mechanical fix and holds up as described. `ad851b7d` bumped
`skills/director/SKILL.md`'s frontmatter `version:` from `5.0.0` to `6.0.0`, treating a real
functional change as grounds for an independently incrementing per-skill version number.
`tests/test_version_is_one_fact.py` (INV-178) — a pre-existing test, unmodified by this
commit or by anything in the range my prior record (`docs/prover/2026-08-24-director-acting.md`,
covering `b870c51b..996a3001`) reviewed — holds that a skill's frontmatter version is a stamped
copy of the one pack-wide `VERSION` fact, not a per-skill semantic version; substantive-change
review already lives in gate s (skill-review), orthogonal to the version number. This is a
distinct kind of check from anything an adversarial code/prose review would catch: it is a
mechanical cross-file consistency rule with a name-and-value form, not a behavioral or
structural defect in the reviewed prose or code, and my prior record's `Blocking: none` verdict
for `b870c51b..996a3001` was correct for the scope it covered — the version-stamp convention
runs in CI's full suite, not the fast local gate, so it caught this one push cycle late, exactly
as the orchestrator's report describes. `72b15120` reverts the frontmatter line to `5.0.0`
(now matching `VERSION`, confirmed by direct read of both), corrects `JOURNAL.md`'s entry
heading from the false "5.0.0 -> 6.0.0" claim to "shadow mode ends (version stays 5.0.0 — one
pack fact, INV-178)" (read against the entry body below it, which was not itself touched and
does not claim a version bump anywhere else), and — per the commit message, confirmed by the
`sync-skills.sh` file itself being untouched — re-ran the existing sync tool against the
external skills-mirror target rather than changing any tracked file for that step. The actual
failing test named by the orchestrator's report, `test_version_is_one_fact.py`, is confirmed
green: 5 passed, run directly rather than assumed from the commit message.

Blocking: none
