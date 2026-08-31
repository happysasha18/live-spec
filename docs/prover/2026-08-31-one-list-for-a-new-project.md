# Prover record — 2026-08-31 one list for a new project

PUSH-REVIEW

Range: 6cbec19d..176b1cef
- 176b1cef The row-format page still carries the retired document's name — a Blockers line
- cee24867 The matrix row for the footprint note follows the template to its new name
- e87c6656 Release 6.1.0: the one-list teaching, and the nothing it asks of a host
- ccb0773e The separate queue template retires, and its readers follow the one list
- e1769937 A new project starts on one list, and the skills stop naming a queue file
- 6cbec19d Prover record: the server's prover pin follows the clone to 1.6.0 (the base)

Files read: PRODUCT_SPEC.md (its whole title-and-glossary head, plus spec/guardrails-freshness.md's
Requirement on the release tier and spec/doc-order-generated.md's Requirements 286 and 287),
ARCHITECTURE.md via architecture/host-adoption.md, MIGRATION.md, VERSION, .claude-plugin/plugin.json,
adopt/ADOPT.md, adopt/START.md, docs/adoption.md, docs/roadmap-format.md, attic/MANIFEST.md,
attic/ROADMAP.template.md, templates/PLAN.template.md, templates/test_scaffold.template.py,
TEST_MATRIX.md, matrix/build-pipeline.md, the six changed skills and their reference pages,
guardrails/check-doc-rotation.py, guardrails/check-skill-review.sh, guardrails/check-prover-record.sh,
tests/test_traceability.py, tests/test_setup_entry.py, tests/test_footprint_note.py.

Checks run: the suite, gate (s), gate (g), the three generated-index gates, the language and
shipped-language gates, the board gate, the register lint on the new template, and the acceptance grep.

- `python3 -m pytest -q` — 2,562 passed, 57 skipped, 2 failed, on the tree this record closes.
  The run before it read 2,561 passed and 3 failed; the third was gate (a) itself, which this
  record answers.
- `bash guardrails/check-skill-review.sh` — OK for all six substantively changed skills.
- `bash guardrails/check-pin-drift.sh` — OK, 180 pins and 39 range pins.
- `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md TEST_MATRIX.index.md` — OK, 551 rows.
- `python3 guardrails/check-architecture-reference.py ARCHITECTURE.md ARCHITECTURE.index.md` — OK.
- `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — OK.
- `python3 guardrails/check-language-rules.py` — OK. `bash guardrails/check-shipped-language.sh` — OK.
- `python3 guardrails/check-board.py` — OK. `python3 scripts/spec-style-lint.py templates/PLAN.template.md` — OK.
- `git grep -n "in this pack" -- skills/ templates/ adopt/` — four lines, none naming a queue file.

Findings: six, none blocking — the release tier, a format page still named for the retired
document, the archive filename in the new template, the three suite reds and who owns them, a line
pin under a prose edit, and a sweep of what the word queue still names.

**F1 — the release tier.** Read against the pack's own tier law before accepting the number. A release
that grows what a host may adopt without rewriting what the host already carries is a minor; a release
the host cannot take without changing what it carries is a major. Decision 2 of this change is
precisely that nothing is asked of a standing host, so 6.1.0 is the honest tier and the 6.1.0 chapter
says in its first line that the host action is none. Held: the tier is not raised to major merely
because a shipped template retired, since no host reads the pack's `templates/` at rest.

**F2 — the format page keeps the retired document's name.** `templates/PLAN.template.md` points its
reader at `docs/roadmap-format.md` for the row shape. Every rule on that page still holds unchanged —
the row shape, the class and status vocabularies, the live-body law, the row lint — and the pointer
resolves to the right rules. The page's own framing does not: it opens by defining "the format the
roadmap is written in", and Requirement 286 names `ROADMAP.md` as the family's third member. Renaming
the page therefore moves a spec requirement too, which is outside this row's own acceptance. Recorded
as a §Blockers line on `PLAN.md` rather than fixed here. Non-blocking: a reader who follows the
pointer gets correct rules, and the cost is one puzzled minute.

**F3 — the archive filename in the new template.** The template's rotated-manifest example names
`docs/queue-archive/rotated-PLAN-[YYYY-MM].md`. Checked against `guardrails/check-doc-rotation.py`,
which matches manifest lines by `rows N → <path>` and scans orphan archives under
`docs/queue-archive/rotated-*.md`. The new name matches both, so a host following the template does
not red on its first rotation. No change needed.

**F4 — the suite reds, and which of them this change owns.** Two are environment drift that
predates this branch: `test_config_health` compares the machine's installed skills at
`~/.claude/skills/` against this worktree, and those installed copies already carry a rule
(the instruction-authority paragraph in `live-spec-base`) that the base commit 6cbec19d does not, so
the gate reported drift before this branch's first commit. Running `scripts/sync-skills.sh` would
clear them by installing this branch's unpushed skills machine-wide over another lane's newer copies,
which this lane refused to do. The third is `TestGateA_ProverRecord::test_real_repo_passes`, which
this record closes: `scripts/stamp-versions.py` writes the pack version into `PRODUCT_SPEC.md`'s
title at every bump, and gate (a) carries no version-stamp carve-out, so any bump makes the standing
prover record stale by construction. Named here rather than worked around, and green on the final
run, which leaves the two environment reds alone.

**F5 — line pins under a prose edit.** `adopt/ADOPT.md` carries five architecture line pins, and the
canonical-set bullet grew two lines. The first draft of that bullet was collapsed to one 244-character
line to keep the pins still, which traded a readable guide for a green gate. Reverted: the bullet
wraps like its neighbours and the five pins were repointed, which is the fix the gate's own message
names. `check-pin-drift.sh` reads green over all 180.

**F6 — what the word "queue" still names.** Swept every surviving use of *queue* across `skills/`,
`adopt/` and `templates/`: queue row, queue-take, queue archive, queued. Each names a row, a moment,
or the `docs/queue-archive/` directory, and none of the three moved. No orphaned use of the word
naming the retired file remains outside one worked-example citation of a real archive file, which is
a historical pointer and correct as written.

Blocking: none
