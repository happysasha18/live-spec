"""The four ways a done was reachable without doing the work, each one red-proven first.

Every test here was written against the code as it stood on 2026-09-06 and FAILED there — the
bypass it names actually worked. They pass now because the route is shut, and each one fails
again the moment its guard is weakened. The last test is the other half: a task that is really
finished still closes, so none of these guards costs the ordinary road.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import ROOT

SCRIPTS = Path(ROOT) / "scripts"
sys.path.insert(0, str(SCRIPTS))
_spec = importlib.util.spec_from_file_location("task_admission", SCRIPTS / "task-admission.py")
admission = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(admission)

GUARD = Path(ROOT) / "guardrails" / "worker-admission-guard.py"
RECEIPT_GATE = Path(ROOT) / "guardrails" / "check-close-receipt.py"


# ---------------------------------------------------------------- one throwaway live-spec tree

def host(tmp_path, key="true"):
    """A minimal live-spec tree: a git repo, a plan, a check table, a deliverable."""
    (tmp_path / "scripts").mkdir()
    for name in ("task-admission.py", "checkpoint.py", "plan_checks_core.py"):
        shutil.copy(SCRIPTS / name, tmp_path / "scripts" / name)
    write_keys(tmp_path, key)
    plan = tmp_path / "PLAN.md"
    plan.write_text("# Host plan\n\n## Tasks\n\n## Blockers\n\nNone.\n", encoding="utf-8")
    (tmp_path / "deliverable.txt").write_text("v1\n", encoding="utf-8")
    for cmd in (["git", "init", "-q"], ["git", "config", "user.email", "t@example.invalid"],
                ["git", "config", "user.name", "t"], ["git", "add", "-A"],
                ["git", "commit", "-qm", "the tree before the work"]):
        subprocess.run(cmd, cwd=tmp_path, check=True, capture_output=True)
    return plan, tmp_path / ".live-spec" / "checkpoints"


def write_keys(tree, key, task_id="q-1"):
    """The host's own check table, in the shape every reader of a plan expects to import."""
    (tree / "scripts" / "plan_checks.py").write_text(
        "from plan_checks_core import evaluate  # noqa: F401\n"
        "from plan_checks_core import parse_tasks as _parse_tasks\n\n"
        "CHECKS = {%r: %r}\n\n\n"
        "def parse_tasks(text):\n"
        "    return _parse_tasks(text, CHECKS)\n" % (task_id, key), encoding="utf-8")


def route(**over):
    r = {"action": "new", "creates_work": True, "existing_task": None,
         "title": "Ship the thing", "project": "host", "scope": "Core",
         "source": {"kind": "person", "detail": "the person, this turn"},
         "observable_outcome": "the deliverable file says v2",
         "done_when": "deliverable.txt contains v2",
         "verification": "grep v2 deliverable.txt",
         "context_pointers": ["`deliverable.txt`"], "estimate": "2–4 hours"}
    r.update(over)
    return r


def gate(plan, checkpoints, base="HEAD"):
    return subprocess.run(
        [sys.executable, str(RECEIPT_GATE), "--plan", str(plan),
         "--checkpoints", str(checkpoints), "--base", base],
        capture_output=True, text=True, timeout=60)


def spawn(cwd, prompt, tool="Task"):
    payload = {"tool_name": tool, "cwd": str(cwd), "tool_input": {"prompt": prompt}}
    got = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload),
                         capture_output=True, text=True, timeout=60)
    assert got.returncode == 0, got.stderr
    return json.loads(got.stdout) if got.stdout.strip() else None


# ---------------------------------------------------------------- 1. the spawn path itself

def test_a_spawn_naming_no_row_is_denied_on_the_tool_path(tmp_path):
    """The guard sits on the subagent tool, so it fires whether or not anybody calls `brief`."""
    host(tmp_path)
    denied = spawn(tmp_path, "Go and rewrite the renderer, then report back.")
    assert denied is not None
    decision = denied["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert "no worker or subagent starts before an admitted row" in decision[
        "permissionDecisionReason"]


def test_a_spawn_naming_a_row_that_is_not_on_the_board_is_denied(tmp_path):
    host(tmp_path)
    denied = spawn(tmp_path, "Take q-77 and finish it.")
    assert denied["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "q-77" in denied["hookSpecificOutput"]["permissionDecisionReason"]


def test_a_spawn_on_a_row_with_no_acceptance_command_is_denied(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "scripts" / "plan_checks.py").write_text("CHECKS = {}\n", encoding="utf-8")
    denied = spawn(tmp_path, "Take q-1 and finish it.")
    assert "no acceptance command" in denied["hookSpecificOutput"]["permissionDecisionReason"]


def test_a_spawn_on_an_admitted_row_passes(tmp_path):
    """The guard refuses unadmitted work and nothing else: the ordinary brief goes through."""
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    assert spawn(tmp_path, "Take q-1 and finish it.") is None


def test_the_guard_says_nothing_outside_a_live_spec_tree(tmp_path):
    assert spawn(tmp_path, "Do anything at all.") is None


def test_the_guard_judges_only_the_tools_that_start_an_agent(tmp_path):
    host(tmp_path)
    assert spawn(tmp_path, "Do anything at all.", tool="Bash") is None


# ---------------------------------------------------------------- 2a. the hand-typed done

def test_a_done_typed_onto_the_plan_is_refused_before_publication(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "admit"], cwd=tmp_path, check=True,
                   capture_output=True)
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")
    got = gate(plan, checkpoints)
    assert got.returncode == 1
    assert "no acceptance receipt" in got.stdout


def test_a_done_typed_onto_a_row_that_has_no_checkpoint_at_all_is_refused(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "admit"], cwd=tmp_path, check=True,
                   capture_output=True)
    (checkpoints / "q-1.md").unlink()
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")
    got = gate(plan, checkpoints)
    assert got.returncode == 1
    assert "has no checkpoint" in got.stdout


# ---------------------------------------------------------------- 2b. the hollow receipt

def test_the_verifier_runs_the_recorded_acceptance_and_not_the_one_it_was_handed(tmp_path):
    """`--command true` used to be the whole receipt. Now it rides beside the recorded key."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    receipt = admission.verify(plan, checkpoints, "q-1", by="a-friendly-name",
                               commands=["true"])
    assert receipt["verdict"] == "failed"
    assert receipt["checks"][0][0] == "grep -q v2 deliverable.txt"
    with pytest.raises(admission.AdmissionError) as refused:
        admission.close(plan, checkpoints, "q-1")
    assert "failed verdict" in str(refused.value)


def test_a_row_with_no_recorded_acceptance_cannot_be_verified_at_all(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "scripts" / "plan_checks.py").write_text("CHECKS = {}\n", encoding="utf-8")
    with pytest.raises(admission.AdmissionError) as refused:
        admission.verify(plan, checkpoints, "q-1", by="someone", commands=["true"])
    assert "no recorded acceptance command" in str(refused.value)


def test_rewriting_the_acceptance_after_the_receipt_voids_it(tmp_path):
    """Changing the check the evidence was written against is a change the close must see."""
    plan, checkpoints = host(tmp_path, key="grep -q v1 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    admission.verify(plan, checkpoints, "q-1", by="someone")
    write_keys(tmp_path, "true")
    with pytest.raises(admission.AdmissionError) as refused:
        admission.close(plan, checkpoints, "q-1")
    assert "acceptance command changed" in str(refused.value)


# ---------------------------------------------------------------- 3. the contract swap

def test_deleting_the_dod_hash_does_not_accept_a_new_contract(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    text = "\n".join(line for line in plan.read_text(encoding="utf-8").splitlines()
                     if not line.startswith("**DOD hash.**"))
    plan.write_text(text.replace("**Done when:** deliverable.txt contains v2",
                                 "**Done when:** nothing at all is required") + "\n",
                    encoding="utf-8")
    with pytest.raises(admission.AdmissionError) as refused:
        admission.verify(plan, checkpoints, "q-1", by="someone")
    assert "removing the hash is not a new contract" in str(refused.value)


def test_rewriting_the_done_and_its_hash_together_is_still_caught(tmp_path):
    """Both halves rewritten reads consistent with itself; the checkpoint's anchor remembers."""
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    text = plan.read_text(encoding="utf-8")
    fresh = admission.dod_digest("nothing at all is required")
    text = text.replace("**Done when:** deliverable.txt contains v2",
                        "**Done when:** nothing at all is required")
    text = "\n".join(("**DOD hash.** " + fresh) if line.startswith("**DOD hash.**") else line
                     for line in text.splitlines())
    plan.write_text(text + "\n", encoding="utf-8")
    with pytest.raises(admission.AdmissionError) as refused:
        admission.verify(plan, checkpoints, "q-1", by="someone")
    assert "differs from the one q-1 was admitted with" in str(refused.value)


def test_changing_the_verified_files_after_the_receipt_voids_it(tmp_path):
    plan, checkpoints = host(tmp_path, key="grep -q v1 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    admission.verify(plan, checkpoints, "q-1", by="someone")
    (tmp_path / "deliverable.txt").write_text("v1\nand something else\n", encoding="utf-8")
    with pytest.raises(admission.AdmissionError) as refused:
        admission.close(plan, checkpoints, "q-1")
    assert "the tree changed after it was verified" in str(refused.value)


def test_the_board_does_not_publish_a_done_over_a_failed_receipt(tmp_path):
    """The renderer reads the receipt, so it holds on a runner that runs no acceptance command."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    admission.verify(plan, checkpoints, "q-1", by="someone")
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")
    for name in ("render-board.sh", "plan_checks_core.py", "checkpoint.py"):
        shutil.copy(SCRIPTS / name, tmp_path / "scripts" / name)
    # LIVE_SPEC_BOARD_CHECKS=off is the PUBLISHED render: the Pages runner draws the page in a
    # checkout that runs no acceptance command at all and otherwise takes every mark at its word.
    # The receipt is a fact recorded in the tree, so it is the one thing that still holds there.
    env = dict(os.environ, LIVE_SPEC_BOARD_CHECKS="off")
    env.pop("LIVE_SPEC_EVALUATING", None)
    got = subprocess.run(["bash", "scripts/render-board.sh"], cwd=tmp_path, env=env,
                         capture_output=True, text=True, timeout=120)
    assert got.returncode == 0, got.stderr
    page = (tmp_path / "board.html").read_text(encoding="utf-8")
    card = page[page.index("q-1"):][:4000] if "q-1" in page else page
    assert "\U0001f501" in card, card[:600]
    assert "marked done in the plan, but its acceptance receipt is a failed verdict" in card


# ---------------------------------------------------------------- the ordinary road still runs

def test_a_task_that_is_really_finished_still_closes(tmp_path):
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    assert spawn(tmp_path, "Take q-1 and finish it.") is None

    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    receipt = admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    assert receipt["verdict"] == "passed"
    assert receipt["checks"] == [["grep -q v2 deliverable.txt", 0]]

    admission.close(plan, checkpoints, "q-1")
    assert "### ✅ Ship the thing — id: q-1" in plan.read_text(encoding="utf-8")

    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "the work"], cwd=tmp_path, check=True,
                   capture_output=True)
    got = gate(plan, checkpoints)
    assert got.returncode == 0, got.stdout + got.stderr


def test_a_correction_moves_the_anchor_so_the_corrected_row_still_verifies(tmp_path):
    plan, checkpoints = host(tmp_path, key="grep -q v3 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    admission.correct(plan, checkpoints, "q-1", done="deliverable.txt contains v3",
                      source="the person, this turn", reason="the version number moved")
    (tmp_path / "deliverable.txt").write_text("v3\n", encoding="utf-8")
    receipt = admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    assert receipt["verdict"] == "passed"
    admission.close(plan, checkpoints, "q-1")
    assert "### ✅" in plan.read_text(encoding="utf-8")
