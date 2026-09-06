"""INV-242 — NEXT_STEPS is transient resume state, never a second task board."""

import os
import subprocess

from conftest import ROOT


CHECK = os.path.join(ROOT, "guardrails", "check-next-steps-boundary.py")


def run_check(*paths):
    return subprocess.run(["python3", CHECK, *map(str, paths)], capture_output=True, text=True)


def test_task_id_reds(tmp_path):
    resume = tmp_path / "NEXT_STEPS.md"
    resume.write_text("# Resume\n\n## Tasks\n- q-12 — fix it\n", encoding="utf-8")
    result = run_check(resume)
    assert result.returncode != 0
    assert "INV-242" in result.stdout
    assert "task" in result.stdout


def test_transient_execution_state_passes(tmp_path):
    resume = tmp_path / "NEXT_STEPS.md"
    resume.write_text(
        "# Resume\n\nTasks live only in PLAN.md.\n\n"
        "## TRANSIENT EXECUTION STATE (2026-09-05)\n\n"
        "Unfinished write-set: skills/director/SKILL.md\n",
        encoding="utf-8",
    )
    result = run_check(resume)
    assert result.returncode == 0, result.stdout + result.stderr


# Three of the four shapes the gate names had no proof of their own until 2026-09-06, and the
# board-row one had never matched a real board mark: its icon set read ✅🟡⏳🧊⛔, while the
# board writes ⬜ 🔄 🔁 ⛔ ✅ 👁️. Each test below was red against that set or against an empty
# TASK_SHAPES; the in-hand row is the one the old set could not see at all.

def test_a_copied_task_section_reds(tmp_path):
    resume = tmp_path / "NEXT_STEPS.md"
    resume.write_text("# Resume\n\n## Forward queue\n\nDraft the footer next.\n",
                      encoding="utf-8")
    result = run_check(resume)
    assert result.returncode != 0
    assert "task section" in result.stdout


def test_a_copied_board_row_reds_for_every_mark_the_board_writes(tmp_path):
    for i, mark in enumerate("⬜ 🔄 🔁 ⛔ ✅ 👁️".split()):
        resume = tmp_path / ("NEXT_STEPS-%d.md" % i)
        resume.write_text(
            "# Resume\n\n### %s The board shows what is in hand — id: qq-2\n" % mark,
            encoding="utf-8")
        result = run_check(resume)
        assert result.returncode != 0, mark
        assert "board row" in result.stdout, mark


def test_a_copied_task_state_line_reds(tmp_path):
    resume = tmp_path / "NEXT_STEPS.md"
    resume.write_text("# Resume\n\nPriority: normal\n", encoding="utf-8")
    result = run_check(resume)
    assert result.returncode != 0
    assert "task state" in result.stdout


def test_real_resume_and_template_stay_taskless():
    result = run_check()
    assert result.returncode == 0, result.stdout + result.stderr
