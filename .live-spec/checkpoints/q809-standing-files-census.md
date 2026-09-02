# q-809 — standing-files census: does every kept document earn its place

Owner's question, 2026-09-02: "зачем decision если есть доска и journal? нам точно все файлы
нужны?... я понимаю что куча твоей бухгалтерии внутренняя но и она если избыточна то надо чинить."
Read-only census. Methodology: for Part 1, grep each filename across `scripts/`, `tests/`,
`guardrails/`, `skills/`, root `.md` files, and `~/.claude/skills/`. For Part 2, grep is not enough
— DECISIONS.md and JOURNAL.md paraphrase each other, so each of the 56 on-record entries was checked
by reading the JOURNAL text for its date/topic, not just keyword-matching. For Part 3, every dated
file was grepped individually (not as a group) across the live tree.

## Part 1 — standing documents

### Root-level files

| path | bytes | modified | what breaks if gone |
|---|---|---|---|
| PLAN.md | 232,679 | 09-02 | `scripts/plan-step.sh`, `scripts/state-probe.sh` and 32 tests read it by name; it is the single entry point CLAUDE.md points every session at. |
| JOURNAL.md | 432,309 | 09-02 | `scripts/session-extract.py` appends to it, 10 tests assert on its shape, `skills/live-spec-base/references/session-handover.md` tells a fresh session to read it. |
| DECISIONS.md | 60,365 | 09-02 | `guardrails/check-authority-anchor.py` is a wired push gate that scans this file by name and reds an undated entry; `tests/test_authority_anchor.py` and `tests/test_opening_decision_sweep.py` assert on it. See Part 2. |
| NEXT_STEPS.md | 19,097 | 09-02 | 10 tests, `scripts/plan_checks.py`, and 14 skill references read it; it is the file `tests/test_traceability.py` and `test_skill_count_agrees.py` pin. |
| PRODUCT_SPEC.md | 51,094 | 09-02 | 147 tests read it, `scripts/plan_checks.py`, 13 other scripts, 2 hooks; it is the requirement-code source every `INV-`/`E-`/`T-` anchor resolves against. |
| PRODUCT_SPEC.index.md | 28,396 | 09-02 | 9 tests assert it is generated (never hand-written) from PRODUCT_SPEC.md; `scripts/` has 1 consumer. |
| ARCHITECTURE.md | 5,675 | 08-31 | 74 tests, 5 scripts, 15 pack skills read it; it is the node/pin structure the fitness tests check code against. |
| ARCHITECTURE.index.md | 10,355 | 09-02 | `tests/conftest.py` and `tests/test_architecture_reference.py` read it by name as the generated gate-z anchor table; a hand-edit here is caught by a red test. |
| TEST_MATRIX.md | 17,032 | 08-31 | 62 tests, 5 scripts, 42 pack-skill references; the M-row source the matrix reference test checks. |
| TEST_MATRIX.index.md | 9,528 | 09-02 | `scripts/plan_checks.py`'s q-591 check runs `check-matrix-reference.py TEST_MATRIX.md TEST_MATRIX.index.md`; `tests/test_matrix_reference.py` reads it as the committed, never-hand-written index. |
| MIGRATION.md | 40,235 | 09-02 | 5 tests, 2 scripts, 4 skill references; `tests/` checks the current VERSION owns a migration chapter here or a changelog line saying it owes nothing. |
| README.md | 10,079 | 09-02 | 31 tests, 3 scripts, 10 skill references; `tests/test_readme_stance.py` and `test_skill_count_agrees.py` assert on its text. |
| OVERVIEW.md | 9,211 | 08-28 | `tests/test_skill_count_agrees.py` reads its skill-count section by name and fails if the heading is lost; `tests/test_traceability.py` greps its reader prose. No script or skill consumer found — test-only. |
| SURFACES.md | 779 | 08-26 | `tests/test_scaffold_guardrails.py` reads and rewrites it inside a fixture tree; `tests/test_readme_stance.py` cites it as precedent. Test-only, no script/skill consumer. |
| WAITING.md | 1,420 | 08-26 | `tests/test_board.py` reads it as the literal board file; `scripts/render-board.sh` renders it. |
| FEEDBACK.md | 10,487 | 08-26 | 1 test, 3 pack-skill references (feedback-collector/feedback-intake open it by name). |
| CLAUDE.md | 1,208 | 08-31 | 9 tests, 3 scripts, 12 skill references; it is the file every session reads first per its own text, and tests assert its content stays a thin pointer. |
| CONTRIBUTING.md | — | — | does not exist in this tree. Not counted. |

**Count of root-level standing documents with no consumer found: 0.** Every file above has at least
one script, test, or skill that reads it by name.

### `.live-spec/` core (non-dated) standing files

| path | bytes | modified | what breaks if gone |
|---|---|---|---|
| PROBLEMS.md | 28,483 | 08-26 | `scripts/plan_checks.py`'s plan-3 check asserts this file exists; `tests/test_traceability.py`, `tests/test_behavioural_break_one_home.py`, and `skills/director`'s delegation-protocol reference read it. |
| agent.md | 4,000 | 08-31 | `scripts/founding-questions.json`, `tests/test_agent_card_gate.py`, `tests/test_deletion_only_push.py`, `tests/test_agent_channels.py`, `tests/test_founding_set_version.py` all check for this exact path — a host tree without it reds by name (INV-184). |
| profile.md | 7,192 | 08-26 | `scripts/check-pack-update.sh`, `tests/test_traceability.py`, `test_composition_axes.py`, `test_design_principles.py`, `test_founding_layers_proofs.py`, `test_setup_entry.py`, `test_config_surface.py` all read this path directly (distinct from the personal `~/.claude/live-spec/profile.md`, which a different set of scripts reads). |
| snapshot/MANIFEST.md, snapshot/baseline.py | 857 + 5,970 | 09-01 | `scripts/plan_checks.py`, `tests/test_snapshot_baseline.py`, `tests/test_traceability.py` read these. |

**Count of `.live-spec/` core standing files with no consumer found: 0.**

One script, not a document, is worth flagging here since it lives beside these files:
`.live-spec/check-plan-delta.sh` is wired live in `guardrails/pre-commit` (line 102) — but it only
ever fires when a commit stages a change to the single hardcoded path
`.live-spec/culling-plan-v3-2026-08-10.md`, a file from a cutting campaign that closed in August. The
guard is not dead code, but its trigger is dead: nobody will edit that file again, so this is running
machinery serving a condition that cannot recur. See Part 3.

### Scope note — not censused

`docs/` holds 941 files across 20 subdirectories, 12 MB total (`docs/prover/` alone is 515 files /
5.7 MB, `docs/skill-review/` 154 files / 996 KB, `docs/queue-archive/` 38 files / 1.5 MB). This is
"another directory of prose the repo maintains" by the task's own definition, but a file-by-file
consumer trace at that scale is a separate, much larger census than this one — it was not run here.
Flagging its existence and size rather than silently skipping it or silently absorbing 10x the scope.

## Part 2 — DECISIONS.md vs JOURNAL.md

**Size and entry count.** DECISIONS.md: 60,365 bytes, 56 entries under "On record" + 1 under
"Struck" + 1 open block (6 D-numbered questions under "Stage 3 C2"). JOURNAL.md: 432,309 bytes
(7.2x DECISIONS.md), 148 `##`-headed session entries spanning 2026-07-07 to 2026-09-02 (DECISIONS.md
has two entries, 07-05 and 07-06, from before the journal existed at all).

**What DECISIONS.md holds that JOURNAL.md does not, structurally:**
- The owner's own words verbatim, Russian where he wrote Russian, with an English rendering beside
  it — JOURNAL.md narrates in the pack's own prose and rarely quotes him at length.
  (`guardrails/check-authority-anchor.py` requires the dated exchange; nothing requires the quote.)
- A **Struck** section — a place he can retract an entry with one line, leaving the record but
  marking it retracted. JOURNAL.md has no retraction mechanism; a session record stands as written.
- An **Open** section — D-numbered questions still awaiting his word (currently the six Stage-3 C2
  checks, sourced from `.live-spec/stage3-verdicts-2026-08-12.md`). JOURNAL.md records what happened,
  not what is pending.
- A direct explicit consequence line per entry ("Consequence: ..."), naming exactly what changed as a
  result — JOURNAL.md's paragraphs mix the decision into the session narrative and don't always spell
  out the consequence as its own clause.

**Every script, test, skill, and hook that reads DECISIONS.md by name:**
scripts: `scripts/plan_checks.py`, `scripts/session-extract.py`, `scripts/measurements-table.py`,
`scripts/check-shipped-language.py`. tests: `tests/test_traceability.py`,
`tests/test_authority_anchor.py`, `tests/test_formal_index.py`, `tests/test_opening_decision_sweep.py`,
`tests/test_measurement_law_homes.py`, `tests/test_no_inline_provenance_citation.py`,
`tests/test_one_home_per_rule.py`. guardrails: `guardrails/check-worker-restore.py`,
`guardrails/check-authority-anchor.py` (the wired push gate — a decision recorded as his must name a
dated exchange or the push reds), `guardrails/pre-commit`. skills:
`skills/live-spec-base/SKILL.md`, `skills/live-spec-base/references/glossary.md`,
`skills/live-spec-base/references/session-handover.md`, `skills/communicator/references/writing-register.md`
(same four files exist both in-repo and installed under `~/.claude/skills/`). JOURNAL.md has no
comparable gate — nothing greps it for a required shape or refuses a push over its content.

**What would have to change for DECISIONS.md's content to live inside JOURNAL.md:** the push gate
`guardrails/check-authority-anchor.py` would need to scan JOURNAL.md instead (today it is written to
expect DECISIONS.md's "On record" bullet shape with a leading date); JOURNAL.md would need a
strike/retract mechanism, since it has none today; and the six other consumers above would need their
hardcoded path changed. Nothing here is a technical blocker — it is a shape DECISIONS.md has today
that JOURNAL.md's rotating, append-only session-log format doesn't.

**Overlap fraction.** Every one of the 56 on-record entries was checked against JOURNAL.md by reading
the journal text at the entry's own date (not just grepping the entry's exact wording, since the two
files paraphrase each other — e.g. the DECISIONS.md board-widening entries at 19:28–21:49 on 08-06
are compressed into one JOURNAL.md paragraph naming the same nine timestamps and topics).

- **28 of 56 (50%)** have a JOURNAL.md passage, verified by reading, that states the same fact — some
  word-for-word cross-referenced ("recorded in DECISIONS.md" appears inside the JOURNAL text itself
  for several: the line-count-boast strike, the cost-audit rulings, the plan-v3 sitting rulings), most
  paraphrased into the session's own narrative.
- **26 of 56 (46%)** were checked against the JOURNAL.md entry for their own date and topic and found
  genuinely absent — the clearest case: the 2026-08-13 08:51 cluster (4 entries — rule 31's "owner",
  the six stage-3 questions, D7 postponed, frozen task wording) has exactly one JOURNAL.md entry for
  that date, and it is about the 5.0.0 migration chapter, an unrelated topic. These read as quick
  chat rulings answered in passing during a session whose journal write-up covered the session's
  actual deliverable, not the aside.
- **2 of 56 (4%)** were not resolved either way in this pass.

## Part 3 — dated one-off notes in `.live-spec/`

50 dated files, 775,045 bytes total (`.live-spec/` as a whole is 1.1 MB). Grouped, with whether
anything in the live tree (root `.md` files, `scripts/`, `tests/`, `guardrails/`, `skills/`, `hooks/`)
references each file by name — checked per file, not per group, since group patterns overstate hits.

| group | files | bytes | latest date | referenced? |
|---|---|---|---|---|
| batch* (verdicts/rule32) | 5 | 41,593 | 2026-08-13 | 2 of 5 named in JOURNAL.md narrative only (batch1-verdicts, batch2-verdicts); 3 of 5 zero hits. |
| crisis-audit-2026-08-08.md | 1 | 9,722 | 2026-08-08 | zero hits anywhere. |
| culling-plan-* | 4 | 78,425 | 2026-08-10 | only culling-plan-v3-2026-08-10.md is referenced (DECISIONS.md, JOURNAL.md narrative, plus the live `check-plan-delta.sh` guard — see Part 1 note, its trigger is dead). The other 3 (2026-08-08, 2026-08-08-review, v2-2026-08-09): zero hits. |
| day1-*/day2-*/day3-* | 8 | 259,316 | 2026-08-09 (mtime for undated names: 08-26) | only day3-opening-2026-08-09.md named in JOURNAL.md narrative; the other 7 (including day1-census-rules.md at 196,421 bytes, the single largest file in this census): zero hits. |
| escort-inventory-R7-2026-08-11.md | 1 | 30,662 | 2026-08-11 | JOURNAL.md narrative only. |
| goals-under-watch-2026-08-13.md | 1 | 10,229 | 2026-08-13 | **active** — PLAN.md points at it live: "seven goals, each with the command that measures it." |
| handover-2026-08-09.md | 1 | 8,185 | 2026-08-09 | JOURNAL.md narrative only. |
| next-phase-prompt-turnkey-productization.md | 1 | 9,769 | mtime 09-02 | **active, current** — NEXT_STEPS.md and PLAN.md both point at it as the live source for the in-progress phase ("Read it whole before starting"). Not a past-session leftover despite living in this bucket. |
| overnight-prompt-2026-09-01.md | 1 | 7,163 | 2026-09-01 | **active, current** — NEXT_STEPS.md cites it as the scope source for tonight's work. |
| plan-v3-delta-* | 13 | 31,258 | 2026-08-13 | only 2 of 13 referenced (plan-v3-delta-2026-08-11.md, plan-v3-delta-2026-08-11-2.md, both in DECISIONS.md/JOURNAL.md narrative); the other 11: zero hits. |
| plan-v3-sweep-2026-08-10.md | 1 | 9,329 | 2026-08-10 | JOURNAL.md narrative only. |
| r2-repetition-2026-08-11.md | 1 | 8,111 | 2026-08-11 | zero hits anywhere. |
| r3-rule-fires-2026-08-11.md | 1 | 28,479 | 2026-08-11 | one PLAN.md prose mention, not a functional consumer. |
| r5-rule-prices-2026-08-11.md | 1 | 42,598 | mtime 09-01 | **active, functional** — `guardrails/check-pin-drift.sh` reads this exact path, wired as a pre-push gate leg (`guardrails/pre-push`); `tests/test_guardrails_unit.py` and `scripts/plan_checks.py` also pin it by name. Not clutter. |
| rule-verdicts-redrawn-2026-08-09.md | 1 | 7,541 | 2026-08-09 | zero hits anywhere. |
| s1-rule-* | 4 | 76,105 | 2026-08-13 | zero hits anywhere, all 4. |
| stage3-check-evidence-2026-08-12.md | 1 | 31,357 | 2026-08-12 | zero hits anywhere. |
| stage3-verdicts-2026-08-12.md | 1 | 25,805 | 2026-08-12 | **active** — DECISIONS.md's own Open section sources the six still-pending Stage-3 C2 questions from this exact file. |
| turnkey-contract-composed.md | 1 | 32,690 | mtime 09-02 | **active, current** — PLAN.md's live source for the in-progress turnkey contract, under product-prover review right now. |
| turnkey-contract-draft-fable.md, turnkey-contract-draft-orchestrator.md | 2 | 26,708 | mtime 09-02 | zero hits anywhere — both drafts were composed into turnkey-contract-composed.md above and superseded; recent by mtime but functionally dead already. |

**Total: 499,089 bytes of `.live-spec/` dated-note material that nothing in the live tree references
by name** (34 files, computed by checking each file individually, not by group pattern). This excludes
the 6 files above marked active/current and the handful with a narrative-only JOURNAL.md mention,
which are referenced even if nothing depends on them.
