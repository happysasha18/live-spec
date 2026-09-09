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

import checkpoint  # noqa: E402 — the checkpoint half of the same state machine

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
         "context_pointers": ["`deliverable.txt`"], "estimate": "2–4 hours",
         # Requirement 321: the route carries what was read off the record. A throwaway
         # host has nothing on its own record, so the list is empty and the finding says so.
         "prior_record": {"read": [], "finding": "nothing on this host's record covers it"}}
    r.update(over)
    return r


def gate(plan, checkpoints, base="HEAD"):
    return subprocess.run(
        [sys.executable, str(RECEIPT_GATE), "--plan", str(plan),
         "--checkpoints", str(checkpoints), "--base", base],
        capture_output=True, text=True, timeout=60)


def token_for(tmp_path, checkpoints, task_id="q-1"):
    """The spawn token `brief` prints — the only thing that opens the guard."""
    brief = admission.worker_brief(tmp_path / "PLAN.md", checkpoints, task_id)
    return brief.splitlines()[2].strip()


def spawn(cwd, prompt, tool="Task"):
    payload = {"tool_name": tool, "cwd": str(cwd), "tool_input": {"prompt": prompt}}
    got = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload),
                         capture_output=True, text=True, timeout=60)
    assert got.returncode == 0, got.stderr
    return json.loads(got.stdout) if got.stdout.strip() else None


# ---------------------------------------------------------------- 1. the spawn path itself

def test_a_spawn_carrying_no_token_is_denied_on_the_tool_path(tmp_path):
    """The guard sits on the subagent tool, so it fires whether or not anybody calls `brief`."""
    host(tmp_path)
    denied = spawn(tmp_path, "Go and rewrite the renderer, then report back.")
    assert denied is not None
    decision = denied["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert "no live brief token" in decision["permissionDecisionReason"]


def test_a_row_id_typed_into_the_prompt_is_not_a_token(tmp_path):
    """An id is something anybody can type. Naming a real, open, admitted row is not admission."""
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    denied = spawn(tmp_path, "Take q-1 and finish it.")
    assert denied is not None
    assert "no live brief token" in denied["hookSpecificOutput"]["permissionDecisionReason"]


def test_a_token_cut_for_another_row_does_not_open_this_one(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    real = token_for(tmp_path, checkpoints)
    forged = "0" * 32
    assert spawn(tmp_path, "Work on this: %s" % forged) is not None
    assert spawn(tmp_path, "Work on this: %s" % real) is None


def test_a_brief_token_dies_when_the_done_it_was_cut_against_moves(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    token = token_for(tmp_path, checkpoints)
    assert spawn(tmp_path, "Work on this: %s" % token) is None
    admission.correct(plan, checkpoints, "q-1", done="deliverable.txt contains v9",
                      source="the person, this turn", reason="the target moved")
    denied = spawn(tmp_path, "Work on this: %s" % token)
    assert denied is not None
    assert "no live brief token" in denied["hookSpecificOutput"]["permissionDecisionReason"]


def test_a_brief_token_dies_when_the_acceptance_it_was_cut_against_moves(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    token = token_for(tmp_path, checkpoints)
    write_keys(tmp_path, "grep -q something-else deliverable.txt")
    assert spawn(tmp_path, "Work on this: %s" % token) is not None


def test_a_spawn_on_an_admitted_row_with_its_own_token_passes(tmp_path):
    """The guard refuses unadmitted work and nothing else: the ordinary brief goes through."""
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    assert spawn(tmp_path, token_for(tmp_path, checkpoints)) is None


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
    """`--command true` used to be the whole receipt. It rode beside the recorded key from
    2026-09-06, and from 2026-09-09 (q-833) it is refused outright: a row run covers the one
    recorded check. Either way the road it opened is shut — a handed command never decides."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    with pytest.raises(admission.AdmissionError) as refused:
        admission.verify(plan, checkpoints, "q-1", by="a-friendly-name", commands=["true"])
    assert "row run covers that command alone" in str(refused.value)
    # The row's own recorded check is what decides, and here it fails: the deliverable still
    # says v1, so no close is reachable.
    receipt = admission.verify(plan, checkpoints, "q-1", by="a-friendly-name")
    assert receipt["verdict"] == "failed"
    assert receipt["checks"][0][0] == "grep -q v2 deliverable.txt"
    with pytest.raises(admission.AdmissionError) as blocked:
        admission.close(plan, checkpoints, "q-1")
    assert "failed verdict" in str(blocked.value)


def test_a_row_with_no_recorded_acceptance_cannot_be_verified_at_all(tmp_path):
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "scripts" / "plan_checks.py").write_text("CHECKS = {}\n", encoding="utf-8")
    with pytest.raises(admission.AdmissionError) as refused:
        admission.verify(plan, checkpoints, "q-1", by="someone", commands=["true"])
    assert "no recorded acceptance command" in str(refused.value)


# ------------------------------- the acceptance is fixed at admission, and re-run by a machine
# that wrote no receipt (the owner's word, 2026-09-07)

RERUN = Path(ROOT) / "guardrails" / "check-acceptance-rerun.py"


def rerun(plan, checkpoints):
    # The run names its kind, the way the gates workflow's own step does: this gate refuses a run
    # that named none (Requirement 322 criterion 1), and that refusal is held in
    # tests/test_acceptance_rerun_reach.py. Every call below is the release road, which is where a
    # forged receipt is meant to meet it.
    env = dict(os.environ, LIVE_SPEC_RUN_MODE="release")
    env.pop("LIVE_SPEC_PUSH_FULL", None)
    return subprocess.run(
        [sys.executable, str(RERUN), "--plan", str(plan), "--checkpoints", str(checkpoints)],
        capture_output=True, text=True, timeout=120, env=env)


def test_a_row_cannot_be_admitted_without_an_acceptance_command(tmp_path):
    """The check that will judge the work is named before the work, or the row is not admitted."""
    plan, checkpoints = host(tmp_path)
    (tmp_path / "scripts" / "plan_checks.py").write_text("CHECKS = {}\n", encoding="utf-8")
    with pytest.raises(admission.AdmissionError) as refused:
        admission.admit(route(), plan, checkpoints)
    assert "admitted with one or not at all" in str(refused.value)
    assert "— id: q-1" not in plan.read_text(encoding="utf-8")

    # And a check that reads the machine rather than the tree is refused too: no run on a commit
    # could ever judge it.
    write_keys(tmp_path, "test -f $HOME/.claude/CLAUDE.md")
    with pytest.raises(admission.AdmissionError) as refused:
        admission.admit(route(), plan, checkpoints)
    assert "reaches outside the tree" in str(refused.value)


def test_an_acceptance_changed_after_admission_is_refused_everywhere(tmp_path):
    """`verify`, `close` and the re-run each read the command the row was ADMITTED with."""
    plan, checkpoints = host(tmp_path, key="grep -q v1 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    admission.verify(plan, checkpoints, "q-1", by="someone")

    write_keys(tmp_path, "true")
    with pytest.raises(admission.AdmissionError) as at_verify:
        admission.verify(plan, checkpoints, "q-1", by="someone")
    assert "not the one it was admitted with" in str(at_verify.value)
    with pytest.raises(admission.AdmissionError) as at_close:
        admission.close(plan, checkpoints, "q-1")
    assert "not the one it was admitted with" in str(at_close.value)

    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")
    got = rerun(plan, checkpoints)
    assert got.returncode == 1
    assert "not the one it was admitted with" in got.stdout


def test_a_forged_passed_receipt_does_not_survive_the_acceptance_rerun(tmp_path):
    """A receipt is text in a checkpoint the tree hash leaves out, so it can be typed. The
    machine that re-runs the row's own command reads no receipt at all."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    cp = checkpoints / "q-1.md"
    body = checkpoint.read_checkpoint(cp)["sections"].get("DONE", "")
    forged = ('RECEIPT: {"by": "a name anybody can type", "verdict": "passed", '
              '"dod_hash": "%s", "acceptance": "grep -q v2 deliverable.txt", '
              '"checks": [["grep -q v2 deliverable.txt", 0]]}'
              % admission.dod_digest("deliverable.txt contains v2"))
    checkpoint.update_checkpoint(cp, done=(body + "\n" + forged).strip())
    # The whole forgery a hand can perform: the receipt, the sheet closed over it, the mark.
    checkpoint.close_checkpoint(cp)
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")

    # The receipt gate reads the receipt and is satisfied — which is the whole defect.
    assert gate(plan, checkpoints).returncode == 0
    # The re-run runs the deliverable's own check instead, and the deliverable still says v1.
    got = rerun(plan, checkpoints)
    assert got.returncode == 1
    assert "its acceptance command failed here" in got.stdout

    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    assert rerun(plan, checkpoints).returncode == 0


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


# --------------------------------------------- what the adversarial read of the fix itself found

def test_a_token_dies_with_the_row_it_was_cut_for(tmp_path):
    """A finished row opens nothing, token or no token."""
    plan, checkpoints = host(tmp_path, key="true")
    admission.admit(route(), plan, checkpoints)
    token = token_for(tmp_path, checkpoints)
    admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    admission.close(plan, checkpoints, "q-1")
    denied = spawn(tmp_path, "%s — and rewrite all of scripts/ while you are there." % token)
    assert denied is not None
    assert "no live brief token" in denied["hookSpecificOutput"]["permissionDecisionReason"]


def test_the_guard_finds_the_board_from_a_subdirectory(tmp_path):
    """A session standing in scripts/ is in the same tree as one standing at its root."""
    host(tmp_path)
    denied = spawn(tmp_path / "scripts", "Go and rewrite the renderer.")
    assert denied is not None
    assert denied["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_deleting_the_hash_after_the_close_is_caught_before_publication(tmp_path):
    """`verify` never runs again on a closed row, so the gate is the only reader left of the
    anchor. Without this arm the row published green against a done nobody verified."""
    plan, checkpoints = host(tmp_path, key="true")
    admission.admit(route(), plan, checkpoints)
    admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    admission.close(plan, checkpoints, "q-1")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "closed"], cwd=tmp_path, check=True,
                   capture_output=True)
    plan.write_text("\n".join(line for line in plan.read_text(encoding="utf-8").splitlines()
                              if not line.startswith("**DOD hash.**")) + "\n", encoding="utf-8")
    got = gate(plan, checkpoints)
    assert got.returncode == 1
    assert "removing the hash is not a new contract" in got.stdout


def test_an_empty_or_zero_base_does_not_stand_the_new_done_arm_down(tmp_path):
    """`LIVE_SPEC_DIFF_BASE: ${{ github.event.before }}` is EMPTY on a pull request, and forty
    zeros on a branch's first push. An empty base left `git show :PLAN.md` reading the index and
    exiting 0, so the base marks equalled the current marks and no row was ever newly done."""
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "admit"], cwd=tmp_path, check=True,
                   capture_output=True)
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=tmp_path,
                   check=True, capture_output=True)
    (checkpoints / "q-1.md").unlink()
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")
    for base in ("", "0" * 40):
        got = gate(plan, checkpoints, base=base)
        assert got.returncode == 1, "base %r stood the newly-done arm down: %s" % (base, got.stdout)
        assert "has no checkpoint" in got.stdout


def test_deleting_the_key_of_an_admitted_row_reds_the_rerun(tmp_path):
    """The one deleted line that used to turn a forged done into a row this gate merely reported."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "scripts" / "plan_checks.py").write_text("CHECKS = {}\n", encoding="utf-8")
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")
    got = rerun(plan, checkpoints)
    assert got.returncode == 1
    assert "A removed check is not a passed one" in got.stdout


def test_a_check_table_that_does_not_load_reds_instead_of_passing(tmp_path):
    """Fail-open on the one file the whole gate stands on turned every row keyless and green."""
    plan, checkpoints = host(tmp_path)
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "scripts" / "plan_checks.py").write_text("CHECKS = {\n", encoding="utf-8")
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")
    got = rerun(plan, checkpoints)
    assert got.returncode == 1
    assert "unreadable" in got.stdout


def test_an_anchor_rewritten_since_the_base_is_caught_at_the_push(tmp_path):
    """The anchors live in the same file as the receipt, so a hand can move them. What a hand
    cannot move is the copy the remote already holds."""
    plan, checkpoints = host(tmp_path, key="true")
    admission.admit(route(), plan, checkpoints)
    admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    admission.close(plan, checkpoints, "q-1")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "closed"], cwd=tmp_path, check=True,
                   capture_output=True)
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True,
                          text=True).stdout.strip()

    cp = checkpoints / "q-1.md"
    cp.write_text(cp.read_text(encoding="utf-8").replace(
        "ACCEPT: " + admission.dod_digest("true"), "ACCEPT: " + admission.dod_digest("false")),
        encoding="utf-8")
    got = gate(plan, checkpoints, base=base)
    assert got.returncode == 1
    assert "ACCEPT anchor has moved since the base" in got.stdout


def test_the_board_never_prints_a_spawn_token(tmp_path):
    """A token opens the guard for as long as its row stands, and the DONE trail is drawn onto a
    public page verbatim."""
    plan, checkpoints = host(tmp_path, key="true")
    admission.admit(route(), plan, checkpoints)
    token = token_for(tmp_path, checkpoints)
    for name in ("render-board.sh", "plan_checks_core.py", "checkpoint.py"):
        shutil.copy(SCRIPTS / name, tmp_path / "scripts" / name)
    env = dict(os.environ, LIVE_SPEC_BOARD_CHECKS="off")
    env.pop("LIVE_SPEC_EVALUATING", None)
    got = subprocess.run(["bash", "scripts/render-board.sh"], cwd=tmp_path, env=env,
                         capture_output=True, text=True, timeout=120)
    assert got.returncode == 0, got.stderr
    page = (tmp_path / "board.html").read_text(encoding="utf-8")
    assert token not in page
    assert "BRIEF-TOKEN" not in page


# ---------------------------------------------------------------- the ordinary road still runs

def test_a_task_that_is_really_finished_still_closes(tmp_path):
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    assert spawn(tmp_path, token_for(tmp_path, checkpoints)) is None

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


def test_a_second_closed_row_does_not_crash_on_the_firsts_leftover_anchor(tmp_path):
    """`faults()` holds the base-marks map in a variable named `was`, read again by every task's
    `newly` check — and the anchor-comparison loop a few lines down reuses that same name for a
    plain string, in the same function scope. The first closed row with a checkpoint leaves `was`
    holding its ACCEPT anchor string; the next closed row's `newly` check then calls `.get` on a
    string and crashes (AttributeError: 'str' object has no attribute 'get'), never reaching a
    verdict on either row. Two closed rows, each with a checkpoint, is the ordinary shape of a
    plan with any history — the gate must judge them, not crash."""
    plan, checkpoints = host(tmp_path)
    (tmp_path / "scripts" / "plan_checks.py").write_text(
        "from plan_checks_core import evaluate  # noqa: F401\n"
        "from plan_checks_core import parse_tasks as _parse_tasks\n\n"
        "CHECKS = {'q-1': 'true', 'q-2': 'true'}\n\n\n"
        "def parse_tasks(text):\n"
        "    return _parse_tasks(text, CHECKS)\n", encoding="utf-8")
    for task_id, title in (("q-1", "Ship the thing"), ("q-2", "Ship the other thing")):
        admission.admit(route(task_id=task_id, title=title), plan, checkpoints)
        receipt = admission.verify(plan, checkpoints, task_id, by="a-second-pair-of-eyes")
        assert receipt["verdict"] == "passed"
        admission.close(plan, checkpoints, task_id)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "two closed rows"], cwd=tmp_path, check=True,
                   capture_output=True)
    got = gate(plan, checkpoints)
    assert got.returncode == 0, got.stdout + got.stderr
    assert "Traceback" not in got.stderr


def test_a_hand_typed_done_mark_is_caught_when_an_earlier_row_closed_in_the_same_push(tmp_path):
    """The same shadow's other face. Where the first closed row's checkpoint does not exist at
    the diff base — the ordinary shape of a push that closes a row — `anchors_at` returns None
    for it, so the old code's shadowed `was = (before or {}).get(name)` sets the OUTER `was` (the
    base-marks map) to None rather than to a string. Nothing crashes. But `newly` then reads
    `was is not None and was.get(...)`, and with `was` now None that is False for every row after
    the first — so a done mark typed straight onto the board with no checkpoint at all, right
    after a row that closed honestly in the same push, passed uncaught. Base predates both rows."""
    plan, checkpoints = host(tmp_path)
    (tmp_path / "scripts" / "plan_checks.py").write_text(
        "from plan_checks_core import evaluate  # noqa: F401\n"
        "from plan_checks_core import parse_tasks as _parse_tasks\n\n"
        "CHECKS = {'q-1': 'true', 'q-2': 'true'}\n\n\n"
        "def parse_tasks(text):\n"
        "    return _parse_tasks(text, CHECKS)\n", encoding="utf-8")
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True,
                          text=True).stdout.strip()

    admission.admit(route(task_id="q-1", title="Ship the thing"), plan, checkpoints)
    admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    admission.close(plan, checkpoints, "q-1")

    admission.admit(route(task_id="q-2", title="Ship the other thing"), plan, checkpoints)
    (checkpoints / "q-2.md").unlink()
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ⬜", "### ✅"),
                    encoding="utf-8")

    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "one closed row, one hand-typed"], cwd=tmp_path,
                   check=True, capture_output=True)
    got = gate(plan, checkpoints, base=base)
    assert got.returncode == 1, got.stdout + got.stderr
    assert "q-2" in got.stdout and "has no checkpoint" in got.stdout


# ------------------------------------- 5. the acceptance a close rests on is the recorded one
# Added 2026-09-09 (q-833). Until then `verify` took any `--command` as an extra check, wrote it
# into the receipt `close` reads, and asked nothing about the mode the run was made under — so a
# broad run nobody scoped in advance could become a row's closing evidence, and a manual run could
# write a receipt at all. Both facts were already recorded in this tree and unread by the executor:
# run_modes.row says no check outside the one task runs, and run_modes.manual decides no verdict.

def plant_run_modes(tree):
    """The run-mode contract, in the throwaway tree, exactly as a host carries it."""
    (tree / "guardrails").mkdir(exist_ok=True)
    shutil.copy(Path(ROOT) / "guardrails" / "run_modes.py", tree / "guardrails" / "run_modes.py")
    shutil.copy(Path(ROOT) / "guardrails.config.json", tree / "guardrails.config.json")


def test_a_command_handed_beside_the_recorded_acceptance_is_refused(tmp_path):
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    with pytest.raises(admission.AdmissionError) as refusal:
        admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes",
                         commands=["python3 -m pytest -q"])
    said = str(refusal.value)
    assert "row run covers that command alone" in said
    assert "manual run" in said
    assert admission.read_receipt(checkpoints / "q-1.md") is None, \
        "a refused verify writes no receipt at all"


def test_the_recorded_command_may_be_handed_back_verbatim(tmp_path):
    """Handing the row its own recorded check is not a second check, so it is not a refusal."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    receipt = admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes",
                               commands=["grep -q v2 deliverable.txt"])
    assert receipt["verdict"] == "passed"
    assert [c for c, _code in receipt["checks"]] == ["grep -q v2 deliverable.txt"], \
        "the receipt carries the recorded acceptance once and nothing beside it"


def test_a_run_under_a_mode_that_decides_no_verdict_writes_no_receipt(tmp_path, monkeypatch):
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    plant_run_modes(tmp_path)
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "manual")
    with pytest.raises(admission.AdmissionError) as refusal:
        admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    said = str(refusal.value)
    assert "names mode 'manual'" in said
    assert "deciding no verdict" in said
    assert "closes no row" in said
    assert admission.read_receipt(checkpoints / "q-1.md") is None
    # And with the mode cleared, the same row verifies and closes on its own recorded check.
    monkeypatch.delenv("LIVE_SPEC_RUN_MODE")
    assert admission.verify(plan, checkpoints, "q-1",
                            by="a-second-pair-of-eyes")["verdict"] == "passed"
    admission.close(plan, checkpoints, "q-1")
    assert "### ✅" in plan.read_text(encoding="utf-8")


def test_a_mode_that_does_decide_a_verdict_still_verifies(tmp_path, monkeypatch):
    """The guard reads the contract rather than a list of mode names: `row` decides a verdict."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    plant_run_modes(tmp_path)
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "row")
    assert admission.verify(plan, checkpoints, "q-1",
                            by="a-second-pair-of-eyes")["verdict"] == "passed"


def test_a_named_mode_with_no_contract_in_the_tree_is_refused(tmp_path, monkeypatch):
    """A tree carrying no run-mode reader cannot say what a named mode may decide, and a receipt
    nobody can judge is not evidence. A run naming no mode is the ordinary road and passes."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "manual")
    with pytest.raises(admission.AdmissionError) as refusal:
        admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    assert "is not in this tree" in str(refusal.value)
    monkeypatch.delenv("LIVE_SPEC_RUN_MODE")
    assert admission.verify(plan, checkpoints, "q-1",
                            by="a-second-pair-of-eyes")["verdict"] == "passed"


def test_a_reader_that_will_not_load_is_named_apart_from_one_that_is_absent(tmp_path, monkeypatch):
    """A tree that HAS the reader and cannot load it is a different fault from one that has none,
    and a refusal naming the wrong fault sends a person looking in the wrong place."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    (tmp_path / "guardrails").mkdir(exist_ok=True)
    (tmp_path / "guardrails" / "run_modes.py").write_text("raise RuntimeError('broken')\n",
                                                          encoding="utf-8")
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "manual")
    with pytest.raises(admission.AdmissionError) as refusal:
        admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    said = str(refusal.value)
    assert "does not load" in said and "broken" in said
    assert "is not in this tree" not in said


def test_a_contract_that_cannot_answer_writes_no_receipt(tmp_path, monkeypatch):
    """A config whose named mode carries no `decides_verdict` used to escape as a refusal about a
    route, on a run that has no route. It is a refusal about the contract now, and still no
    receipt."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    plant_run_modes(tmp_path)
    config = json.loads((tmp_path / "guardrails.config.json").read_text(encoding="utf-8"))
    config["run_modes"]["manual"].pop("decides_verdict", None)
    (tmp_path / "guardrails.config.json").write_text(json.dumps(config), encoding="utf-8")
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "manual")
    with pytest.raises(admission.AdmissionError) as refusal:
        admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    said = str(refusal.value)
    assert "does not say what mode 'manual' may decide" in said
    assert "route" not in said
    assert admission.read_receipt(checkpoints / "q-1.md") is None


def test_a_typo_in_the_mode_name_is_refused_as_a_typo(tmp_path, monkeypatch):
    """A caller's typo and a tree's broken contract are two faults, and a refusal naming the wrong
    one sends a person to the wrong file."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    plant_run_modes(tmp_path)
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "nightly")
    with pytest.raises(admission.AdmissionError) as refusal:
        admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    said = str(refusal.value)
    assert "unknown run mode 'nightly'" in said
    assert "row, integration, release, manual" in said
    assert "guardrails.config.json" not in said, \
        "a typed mode name is the caller's own fault, so the refusal sends nobody to the config"


def test_the_no_verdict_refusal_names_the_mode_that_was_asked_for(tmp_path, monkeypatch):
    """The refusal used to describe the manual run whichever mode had been named. It reads the
    tree's own contract, so it says what the named mode records about itself."""
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    plant_run_modes(tmp_path)
    config = json.loads((tmp_path / "guardrails.config.json").read_text(encoding="utf-8"))
    config["run_modes"]["release"]["decides_verdict"] = False
    (tmp_path / "guardrails.config.json").write_text(json.dumps(config), encoding="utf-8")
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "release")
    with pytest.raises(admission.AdmissionError) as refusal:
        admission.verify(plan, checkpoints, "q-1", by="a-second-pair-of-eyes")
    assert "names mode 'release'" in str(refusal.value)
    assert admission.read_receipt(checkpoints / "q-1.md") is None


def test_a_whitespace_mode_names_nothing_on_both_roads(tmp_path, monkeypatch):
    """`named_mode` strips, so an all-whitespace value names no mode. The road taken when the
    reader is absent reads the same two variables the same way, so the two agree."""
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "   ")
    for planted in (True, False):
        tree = tmp_path / ("with" if planted else "without")
        tree.mkdir()
        plan, checkpoints = host(tree, key="grep -q v2 deliverable.txt")
        if planted:
            plant_run_modes(tree)
        admission.admit(route(), plan, checkpoints)
        (tree / "deliverable.txt").write_text("v2\n", encoding="utf-8")
        assert admission.verify(plan, checkpoints, "q-1",
                                by="a-second-pair-of-eyes")["verdict"] == "passed"
