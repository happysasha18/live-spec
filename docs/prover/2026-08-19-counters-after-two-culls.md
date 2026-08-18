# Prover record — 2026-08-19 counters after two culls

PUSH-REVIEW

Range: 942b8cd2..2b9676a3
- 2b9676a3 The record carries the drift both culls left behind
- 777f8606 Two hand-kept lists catch up with yesterday's two culls
Files read: tests/test_progress_report.py, scripts/progress-report.py, docs/PROGRESS.md, guardrails/progress-baseline.json, ARCHITECTURE.md, docs/roadmap-format.md, tests/test_skill_count_agrees.py, OVERVIEW.md, README.md, skills/live-spec-base/SKILL.md, guardrails/check-prover-record.sh, guardrails/pre-push, docs/prover/README.md
Checks run: `python3 -m pytest tests/test_progress_report.py tests/test_skill_count_agrees.py -q` — 31 passed. The full suite ran separately, on the server side of this push; this pass did not re-run it locally.
Findings: two hand-kept lists had not caught up with two intentional deletions; the class repeats whenever an entity is retired and its record is split across several hand-kept lists
Blocking: none

Root: yesterday two cuts landed, and both were correct. Commit 2e2f167c retired the invented byte
ceilings as a class, and `scripts/progress-report.py` stopped printing the "share of the byte
ceiling used" row. Separately, the `text-audit` skill moved out of the pack; its folder under
`skills/` is gone, leaving ten working skill folders beside the shared rulebook,
`live-spec-base`. Neither cut was wrong on its own terms.

What went stale: each cut left a hand-kept list a step behind it. `tests/test_progress_report.py`
still pinned "share of the byte ceiling used" among Table C's measures, so the test read a row the
document no longer prints. `OVERVIEW.md`'s heading still read "Eleven working skills", carried over
from before the `text-audit` folder left, while every other home of the count — `README.md`,
`ARCHITECTURE.md`, `skills/live-spec-base/SKILL.md` — already said ten. Both lists are maintained by
hand, not derived from the thing they describe, so removing the thing did not touch the list that
names it.

Why the local guardrail missed it and the server caught it: the fast local push chain
(`guardrails/pre-push`, 2026-08-18) stopped running the full pytest suite on every push and left
that to the server's gates workflow, to keep an ordinary push fast. A drift that only a full suite
run surfaces — a stale pin, a stale count — therefore now reaches the server before it reaches the
pusher, exactly as it did here: run 32180947981 turned red on these four tests, none of them in the
scope the fast local chain still checks.

Fix: `tests/test_progress_report.py::TestProgressReportShape::test_table_c_has_its_stated_columns`
no longer pins "share of the byte ceiling used" among the measures — the row was checked against
`scripts/progress-report.py::build_table_c`, which has not printed it since 2e2f167c, and against
every other document that could plausibly restate it (`docs/PROGRESS.md`, `docs/roadmap-format.md`,
`ARCHITECTURE.md`); none does, so nothing else needed the same edit.
`OVERVIEW.md`'s heading now reads "Ten working skills, plus the one shared rulebook they all load",
matching the count `tests/test_skill_count_agrees.py::working_skill_count()` reads off disk and the
count the other three homes already stated. Both edits are removals or one-word corrections to a
list; neither test that failed was loosened or weakened — each pinned exactly the thing the prior
day's cull had already, correctly, taken away.

Findings, in full: the recurring shape is that a deletion is judged correct on its own file, and the
lists that state a count or an inventory derived from that file are edited by hand, separately, in a
different commit or by a different person. Nothing ties the list to the thing it counts except a
test that runs late enough to catch the drift. Four tests caught it this time because the
progress-report script and the skill-count test both derive their expectation from a live
measurement (the rendered table, `os.listdir(skills_dir)`) rather than from another hand-kept
number, and compare that measurement against the hand-kept lists in the surrounding documents. The
fix here is narrow — bring the two stale lists forward to match what was already, correctly,
deleted. The class itself (a cull's effect scattered across hand-kept registers with no single
owner) is left as a finding, not something this pass closes.
