#!/usr/bin/env python3
"""PreToolUse(Task/Agent): deny a worker spawn that no admitted row stands behind.

WHAT THIS REFUSES.  A subagent started on work that is not on the board: no row, or a row with no
definition of done, or a row with no acceptance command anybody could run afterwards.  Those three
legs are the pre-spawn rule, and until this hook they lived only inside `task-admission.py brief`
— a command an orchestrator was free never to call.  A rule enforced only by the caller who
chooses to consult it is a note, not a gate; the tlvphotos defect of 2026-09-06 is a night of work
spawned first and given a row afterwards.

WHERE THE ROW ID COMES FROM.  The prompt the spawn carries.  A brief written by `brief` opens with
the row's own heading, so the id is already in the text; a prompt that names none is a spawn nobody
can trace to the board, which is the act being refused.  The first `q-<n>` / `plan-<n>` token in
the prompt is read as the row, and every leg is then judged against the plan of the tree the
session is standing in.

WHAT IT DOES NOT REFUSE, said rather than left to be discovered:

  - A spawn outside a live-spec tree.  No PLAN.md at `cwd` or above it, no board to judge against,
    and this hook says nothing.  A host attaches the board first, then this gate means something.
  - A prompt that names an admitted row and then asks the worker for something else entirely.  The
    hook reads the board, not the worker's conscience.  What it guarantees is that work has a row,
    a done, and a check before anybody starts — never that the worker obeys the row.
  - Whether the recorded acceptance command is a MEANINGFUL check.  It reads that the row has one,
    never what it tests: a key reading `true` clears this gate and every gate after it, and the
    only reader of that is a person looking at the diff.
  - A spawn from a session that does not run this hook.  It is wired in `.claude/settings.json`
    beside the tree it guards, so it binds the sessions that open this project.  An agent started
    by another program, or by a session with the hook removed, is outside its reach; that is the
    ceiling of a hook-based gate and no wording here changes it.
"""

import importlib.util
import json
import os
import re
import sys
from pathlib import Path

# The tools that start another agent. A name this list does not carry passes untouched.
SPAWN_TOOLS = ("Task", "Agent")
ROW_ID = re.compile(r"\b((?:q|plan)-\d+)\b")


def _row_id(payload):
    """The first row id the spawn's own prompt names, or None."""
    tool_input = payload.get("tool_input") or {}
    text = " ".join(str(tool_input.get(field) or "")
                    for field in ("prompt", "description", "message"))
    found = ROW_ID.search(text)
    return found.group(1) if found else None


def _admission(root):
    """The pack's own admission module, loaded out of the tree being guarded."""
    script = Path(root) / "scripts" / "task-admission.py"
    if not script.exists():
        return None
    sys.path.insert(0, str(script.parent))
    spec = importlib.util.spec_from_file_location("task_admission", script)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:  # noqa: BLE001 - a module that does not load judges nothing
        return None
    return module


def decide(payload):
    """The refusal reason for this spawn, or None to say nothing."""
    if payload.get("tool_name") not in SPAWN_TOOLS:
        return None
    # The board is looked for at the cwd and above it: a session standing in `scripts/` is in the
    # same tree as one standing at its root, and reading only the cwd stood the guard down for
    # every spawn from a subdirectory (the adversarial read of 2026-09-06).
    here = Path(payload.get("cwd") or os.getcwd()).resolve()
    root = next((d for d in (here, *here.parents) if (d / "PLAN.md").exists()), None)
    if root is None:
        return None  # not a live-spec tree: no board to judge against
    plan = root / "PLAN.md"
    admission = _admission(root)
    if admission is None:
        return None
    task_id = _row_id(payload)
    try:
        admission.pre_spawn_check(plan, root / ".live-spec" / "checkpoints", task_id or "")
    except Exception as exc:  # noqa: BLE001 - AdmissionError, and anything the plan read threw
        return (
            "worker-admission-guard: this spawn does not stand on an admitted row. %s\n"
            "Admit the work first (`python3 scripts/task-admission.py admit --route <route.json>`), "
            "write the row's acceptance command into scripts/plan_checks.py keyed by its id, then "
            "hand the worker `python3 scripts/task-admission.py brief <id>` and name that id in "
            "the prompt." % exc)
    return None


def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        return 0
    if not isinstance(payload, dict):
        return 0
    reason = decide(payload)
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
