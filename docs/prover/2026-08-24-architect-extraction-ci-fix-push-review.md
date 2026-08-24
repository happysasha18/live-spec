# Prover record — 2026-08-24 architect-extraction-ci-fix push-review

PUSH-REVIEW

Range: 12d82f74..6fab1705
- 6fab1705 prover record: extend the CI-fix record over the gate-s/h/m follow-up (5448de4a)
- 5448de4a tests + skill-review: pin the footer fix and cover its four skills (gate h, INV-208)
- cbdb0d95 prover record: cover the architect-extraction CI fix (12d82f74..62368580)
- 62368580 plugin metadata: reword description to drop accidental "architect" match (INV-44 CI fix)
- b31fc42f skills: sync closing pack-list footers with architect (INV-66 CI fix)
- dfcdccad evals: add architect.md — E-19 binds on every working skill (CI fix)

Files read: every hunk of all 6 commits (`git show <hash>` each); `evals/architect.md` in full
against `evals/feedback-intake.md` and `evals/test-author.md` as convention precedent; `.claude-plugin/
plugin.json` and `.claude-plugin/marketplace.json` in full, current state; the closing "pack, whole"
roster block quotes in `skills/live-spec-base/SKILL.md`, `skills/architect/SKILL.md`,
`skills/communicator/SKILL.md`, `skills/design-reviewer/SKILL.md`, `skills/feedback-intake/SKILL.md`,
`skills/test-author/SKILL.md` (all six roster-carrying files, not just the four this range's commits
touched); `tests/test_traceability.py`'s `TestPackListParity` (`ROSTER_HEADINGS`, `footer_bodies`) to
confirm what the mechanical parity check actually asserts; `tests/test_architect_extraction.py` in
full, current state; `docs/skill-review/2026-08-24-architect-extraction.md` in full, current state;
`docs/prover/2026-08-24-architect-extraction-ci-fix.md` (the record under review) and
`docs/prover/README.md` and `docs/prover/2026-08-24-architect-extraction-push-review.md` for shape/
precedent; every `SKILL.md` under `skills/*` (all 13) for the "pack, whole"/roster-heading grep;
`guardrails/check-prover-record.sh` in full, the range/reviewed-commit and Checks-run-field arms
specifically, to check the existing record's `Range:` field against the gate's actual logic;
`guardrails/pre-push` gate n's block, to confirm the blank gate-n line is a quiet stand-down and not
a swallowed failure.

Checks run: reran every check independently rather than trusting the prior two records; all green,
plus one proactive-grep pass beyond the task's known-relevant tests. Full transcript below.
- `python3 -m pytest tests/test_traceability.py -q` — 181 passed (full file, not just the 3
  originally-failing selection).
- `python3 -m pytest tests/test_skill_count_agrees.py tests/test_director_scenarios.py
  tests/test_architect_extraction.py -q` — 34 passed, regression check green.
- `bash guardrails/pre-push < /dev/null` — read the FULL transcript top to bottom (131 lines), not
  just the tail: every lettered gate (a, b-note, d, g, f, e, i, j, l, o, p, q, r, s, t, m, k, n, h,
  x, y, z) prints OK/PASS or an explicit stand-down note, no FAIL/ERROR anywhere in the whole run;
  final line `All gates green — push allowed.` Gate n (earned message) prints only its heading with
  no body line for this run — confirmed this is a quiet success (script calls
  `check-earned-message.py inbox`, which exits 0 with empty stdout when the inbox holds no
  deposits, and the `||`-guarded fallback line only fires on nonzero exit), not a swallowed
  failure. Gate r's authority-anchor candidates are read-back material (DECISIONS.md), explicitly
  documented as non-blocking by the gate's own text, unrelated to this range's files.
  `git diff origin/main..HEAD -- skills/build-pipeline/` — empty, confirmed independently.
- Proactive grep sweep (the project's new post-incident rule, applied here rather than trusted to
  the fix-it worker's own report):
  - `grep -rln "skills/architect\|'architect'\|\"architect\"" tests/` → only
    `tests/test_architect_extraction.py`. No other test file references the skill by path or
    quoted name.
  - `grep -rln "len(skills)\|WORKING_SKILL_FLOOR\|working_skills\b" tests/` → only
    `tests/test_traceability.py`. Read `WORKING_SKILL_FLOOR = 8` (line 1030) and
    `working_skills()` (line 1051) directly: both already green in the 181-pass run above, no
    hardcoded count that a 13th skill directory would break.
  - `grep -rln "marketplace.json\|plugin.json" tests/` → `tests/test_traceability.py` and
    `tests/test_minor_gate_reconciliations.py`; both ran clean inside the 181-pass full-file run
    and the pre-push run respectively (the second file is not in the traceability suite; spot-read
    it, no `architect`-relevant assertion in it).
  - `grep -rln "footer\|roster\|closing.*pack\|pack.*whole" tests/ skills/*/SKILL.md` → seven test
    files plus the six roster-carrying `SKILL.md`s and `skills/publish/SKILL.md` (a false positive:
    its one "footer" hit is about README footers, not the pack-list roster — confirmed by reading
    the line, no roster block quote in `publish/SKILL.md`).
  - `grep -rl "pack, whole\|The pack, whole" skills/*/SKILL.md` → `architect`, `communicator`,
    `design-reviewer`, `feedback-intake`, `live-spec-base`, `test-author` — exactly the six files
    already confirmed to name `architect`. Checked all 13 skill directories' `SKILL.md` individually
    (`build-pipeline`, `director`, `feedback-collector`, `product-prover-pack`, `publish`,
    `spec-author`, `text-audit-pack` carry neither roster heading at all — nothing to check on
    those); no 7th roster-carrying skill missing the `architect` line was found.
- Read `evals/architect.md` in full against `evals/feedback-intake.md` and `evals/test-author.md`:
  same four-section shape (`## Scenario`, `## Criteria`, `## The red`, `## Re-run`), a real
  scenario grounded in the skill's actual promises (kind-scaffold node structure, grep-sourced pins,
  the node-fitness test, budget instrumentation homes/watchers, runtime/placement views, anchor
  coverage), a criteria table with genuine RED/GREEN contrasts rather than trivially-true rows, and
  a dated bare-run/with-skill-run pair with concrete, specific failure/success detail — substantive,
  not filler.
- Read both `.claude-plugin` descriptions in full: "...spec, prove, structure, tests, and code..."
  reads naturally, the reword loses no meaning. Checked by hand against all 13 skill directory names
  (`architect`, `build-pipeline`, `communicator`, `design-reviewer`, `director`,
  `feedback-collector`, `feedback-intake`, `live-spec-base`, `product-prover-pack`, `publish`,
  `spec-author`, `test-author`, `text-audit-pack`) — none is a substring of either description,
  before or after the reword, confirmed by reading the text rather than trusting the test alone.
- Read `docs/prover/README.md`'s field-shape rules again and checked
  `docs/prover/2026-08-24-architect-extraction-ci-fix.md` against them: `Checks run:` carries inline
  content right after the colon in both the original and the extended version — no repeat of the
  prior-round bare-heading defect.

Findings: the six committed commits are a correct, well-verified fix of the three CI failures plus
a self-caught second round of local-gate failures (s/h/m) the worker triaged and closed within the
same push, matching what both prior prover records (`cbdb0d95`'s and `5448de4a`'s versions of
`docs/prover/2026-08-24-architect-extraction-ci-fix.md`) claim. Independently re-verified rather
than trusted: all three original CI failures traced to their exact root cause and fix (missing
`evals/architect.md`, four skills' missed closing-roster line, the "architecture"→"architect"
accidental substring match), the four skills' one-line-only diff, `build-pipeline`'s genuine
non-involvement, and the follow-up gate-s/h/m repair's correctness.

One drift found by the proactive-grep pass that neither prior record nor any test surfaces —
**non-blocking, out of this range's own scope, but real**: the six roster-carrying `SKILL.md`
files' `architect` clause is not textually identical across all six. `skills/live-spec-base/
SKILL.md:600-601` (unchanged by this range; its wording dates to `3cc8b47f`, already on
`origin/main`) reads `**architect** writes or updates the architecture from the proven spec`, while
`skills/architect/SKILL.md`'s own footer (also from `3cc8b47f`) and all four skills `b31fc42f`
patched (`communicator`, `design-reviewer`, `feedback-intake`, `test-author`) read `**architect**
writes and updates the structure that carries a proven spec`. Every OTHER roster entry's clause
(spot-checked against `design-reviewer`'s: `judges the design behind it`) is byte-identical across
all six files, so the roster convention this project actually follows is clause-for-clause parity,
not merely name presence — and `architect`'s own entry breaks that parity 5-to-1.
`TestPackListParity.footer_bodies()`/`_pack_list_gaps()` only checks that each skill NAME is a
substring of each footer body, never that the accompanying clause matches, so this is invisible to
every test that ran green above, including the new pinned tests in `5448de4a`
(`test_other_working_skills_closing_rosters_name_architect` asserts the "structure" wording
literally, which further cements the mismatch against `live-spec-base` rather than catching it).
The drift predates the reviewed range (`live-spec-base`'s line is untouched by any of these 6
commits and was already present at `origin/main`'s `12d82f74`), and `b31fc42f`'s own commit message
scoped itself to "sync...with architect" (i.e., with `architect`'s own file), which it did
correctly — reconciling `live-spec-base`'s independently-worded line was never this range's stated
job. Flagging for awareness, matching this project's own precedent for a pre-existing, out-of-scope
quirk (`docs/prover/2026-08-24-architect-extraction-push-review.md`'s "one pre-existing,
out-of-scope quirk noted but not folded" section) rather than holding this push over it.

Blocking: none
