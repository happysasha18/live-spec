# Prover record — 2026-08-24 architect-extraction-ci-fix

PUSH-REVIEW

Range: 12d82f74..5448de4a
- 5448de4a tests + skill-review: pin the footer fix and cover its four skills (gate h, INV-208)
- cbdb0d95 prover record: cover the architect-extraction CI fix (12d82f74..62368580)
- 62368580 plugin metadata: reword description to drop accidental "architect" match (INV-44 CI fix)
- b31fc42f skills: sync closing pack-list footers with architect (INV-66 CI fix)
- dfcdccad evals: add architect.md — E-19 binds on every working skill (CI fix)

Files read: `evals/architect.md` in full (own content); `evals/feedback-intake.md` and
`evals/test-author.md` in full, as the most-recently-added convention precedent; `evals/README.md`
in full for the authoring rule and the four-section shape; `skills/architect/SKILL.md` in full,
current state, to ground the eval's scenario in the skill's actual scope; `tests/test_traceability.py`
lines 1020–1362 in full (`TestSkillEvals`, `_pack_list_gaps`, `TestPackListParity`,
`TestPluginMetadata`) to confirm each test's exact assertion before writing a fix for it;
`skills/communicator/SKILL.md`, `skills/design-reviewer/SKILL.md`, `skills/feedback-intake/SKILL.md`,
`skills/test-author/SKILL.md`, and `skills/live-spec-base/SKILL.md`'s closing "pack, whole" block
quotes, current state; `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` in full;
`README.md`, `OVERVIEW.md`, `PRODUCT_SPEC.md` for existing `architect` mentions (confirmed already
present, not touched); `skills/build-pipeline/SKILL.md` (confirmed untouched by this range's diff).

Checks run: ran CI's exact failing selection plus the full traceability file and the two named
regression files, all green; confirmed build-pipeline's diff is empty.
- `python3 -m pytest tests/test_traceability.py -k "test_skill_evals_present or
  test_real_repo_lists_complete or test_descriptions_never_carry_a_partial_skill_list" -v` —
  3 passed (the exact three CI named as failing on `12d82f74`).
- `python3 -m pytest tests/test_traceability.py -q` — 181 passed (the whole file this range
  touches logic in, not just the three named tests).
- `python3 -m pytest tests/test_skill_count_agrees.py tests/test_director_scenarios.py -q` —
  24 passed (the scoped regression check this project's prior CI-fix rounds use).
- `git diff origin/main..HEAD -- skills/build-pipeline/` — empty; build-pipeline is confirmed
  genuinely untouched, matching the "no partial migration" constraint.
- `git diff origin/main..HEAD --stat` — 7 files changed across the three commits
  (`evals/architect.md` new; four `SKILL.md` footers; two `.claude-plugin/*.json` descriptions),
  matching the three commits' own claims with nothing extra riding along.
- Adversarially re-derived each of the three CI failures against the actual test source rather
  than trusting the brief: confirmed `TestSkillEvals.working_skills()` walks `skills/` excluding
  `live-spec-base` and any dir whose frontmatter declares `requires:`, and that
  `test_skill_evals_present` requires `## Scenario`, `## Criteria`, `## The red`, `## Re-run` plus a
  `bare run: \d{4}-\d{2}-\d{2}` match — `evals/architect.md` carries all four sections and the dated
  line. Confirmed `TestPackListParity.footer_bodies()` reads every `skills/*/SKILL.md` carrying
  either roster heading, not just `live-spec-base`'s — grepped `skills/*/SKILL.md` for both headings
  directly and found six carriers (`architect`, `communicator`, `design-reviewer`, `feedback-intake`,
  `live-spec-base`, `test-author`); `architect` and `live-spec-base` already named `architect` from
  `3cc8b47f`, the other four did not until this range's second commit. Confirmed
  `test_descriptions_never_carry_a_partial_skill_list` does a plain substring check per skill
  directory name against each JSON's `description`; read both descriptions directly and found
  "architecture" (ordinary prose, "...spec, prove, architecture, tests, and code...") contains
  "architect" as a prefix substring — the sole cause, not an intentional partial enumeration —
  confirmed no other skill name was a substring either before or after the reword.

Findings: all three failures were genuine drift the local push gates cannot see (the fast gate does
not run `tests/test_traceability.py`'s full suite), not test bugs. (1) `skills/architect/` shipped
with no `evals/architect.md`; fixed with a scenario-based eval, written to the exact four-section
shape and authoring rule `evals/README.md` states, scoped to the skill's real promises (kind-scaffold
node structure, grep-sourced pins, the node-fitness test, budget instrumentation homes/watchers, the
runtime/placement views, the anchor coverage check) rather than filler. (2) `3cc8b47f` updated
`live-spec-base`'s own closing roster but missed the same closing block quote each other working
skill's `SKILL.md` independently carries; `communicator`, `feedback-intake`, and `test-author` gained
the `architect` line in the same slot `live-spec-base` uses (between `design-reviewer` and
`build-pipeline`), and `design-reviewer`'s bulleted form gained the matching bullet in the same slot
— verified against each file's own pre-existing order rather than assumed uniform. `build-pipeline`
deliberately left untouched. (3) Both `.claude-plugin` descriptions' prose word "architecture"
started coincidentally matching the new `architect` skill directory name as a substring once that
directory existed; the descriptions never intentionally enumerated skill names, so the correct fix
was rewording ("architecture" → "structure") rather than completing a 13-skill list or renaming the
skill (out of scope, already decided). Confirmed the reworded text still reads naturally and no skill
name is now a substring of either description.

Extended after the first local pre-push run: fixing `b31fc42f` and `62368580` touched four skills'
`SKILL.md` bodies, which the local push gate (unlike the CI failures themselves) DOES see —
`guardrails/pre-push` reran after those two commits landed and correctly failed three more gates
none of the CI-reported failures named: gate s (`communicator`, `design-reviewer`, `feedback-intake`,
`test-author` each substantively changed with no fresh skill-creator review record, INV-208), gate h
(those same four `SKILL.md` changes carried no accompanying `tests/` change), and gate m
(`~/.claude/skills/`'s installed mirror drifted from the four now-changed source files). Fixed and
re-verified rather than left for the orchestrator to hit fresh:
- Gate s: extended `docs/skill-review/2026-08-24-architect-extraction.md` with a fifth finding
  naming all four skills, their one-line-only diff, and the verification run — committed in
  `5448de4a`, itself newer than `b31fc42f` (the skills' last change), satisfying the gate's own
  freshness check (a record's commit must be at or after the reviewed skill's last change).
- Gate h: added `TestRostersNameArchitect.test_other_working_skills_closing_rosters_name_architect`
  and `test_design_reviewer_closing_roster_names_architect` to
  `tests/test_architect_extraction.py`, pinning each of the four skills' closing-roster line so a
  later regression reds by name — committed in the same `5448de4a`.
- Gate m: ran `bash scripts/sync-skills.sh` (the documented developer freshness tool, SPEC E-23) to
  copy the four changed `SKILL.md` files over their `~/.claude/skills/` mirror; a machine-local
  install action outside the repo, nothing to commit, matching this project's own prior precedent
  (`docs/prover/2026-08-24-director-acting-ci-fix.md`'s finding on `sync-skills.sh` being an install
  step rather than a source change). No version bump accompanied the sync (all four skills stay at
  `5.0.0`, a content-only fix), so no A-7 journal re-read trigger line was owed.
- Re-ran `bash guardrails/pre-push < /dev/null` after all of the above: gates a (this record's
  own prior, now-stale version), s, h, and m all read OK on the second pass (see the final
  full-chain run recorded by the orchestrator's own push-gate log for this range); this record
  itself was then re-extended to this current range to keep gate a's freshness satisfied, since
  gate a requires the newest `docs/prover/` record's commit to be at or after the newest commit in
  the pushed range.

Blocking: none
