"""The shell-boundary arm denies destructive git commands before Bash runs them."""
import json
import os
import subprocess
import sys

import pytest

from conftest import ROOT


HOOK = os.path.join(ROOT, "hooks", "worker-restore-guard.py")

FORBIDDEN = [
    "git checkout -- TEST_MATRIX.md",
    "git checkout -q .",
    "git checkout HEAD TEST_MATRIX.md",
    "git restore PRODUCT_SPEC.md",
    "git restore --staged --worktree PRODUCT_SPEC.md",
    "git stash",
    "git stash push -- PRODUCT_SPEC.md",
    "git stash create",
    "git reset --hard HEAD",
    "git reset --merge HEAD",
    "git reset --keep HEAD",
    "git clean -fd",
    "env -- git checkout -- TEST_MATRIX.md",
    "command -- git checkout -- TEST_MATRIX.md",
    "sudo -u root git checkout -- TEST_MATRIX.md",
]

ALLOWED = [
    "git status",
    "git checkout main",
    "git checkout -b fix/example main",
    "git restore --staged PRODUCT_SPEC.md",
    "git stash list",
    "git stash show",
    "git stash pop",
    "git reset --soft HEAD~1",
    "git clean -fn",
    "grep 'git checkout -- TEST_MATRIX.md' notes.md",
]


def _run(command):
    payload = {"tool_name": "Bash", "tool_input": {"command": command}}
    return subprocess.run([sys.executable, HOOK], input=json.dumps(payload), capture_output=True,
                          text=True, timeout=10)


@pytest.mark.parametrize("command", FORBIDDEN)
def test_each_forbidden_form_is_denied(command):
    result = _run(command)
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)["hookSpecificOutput"]
    assert output["hookEventName"] == "PreToolUse"
    assert output["permissionDecision"] == "deny"
    assert command in output["permissionDecisionReason"]


@pytest.mark.parametrize("command", ALLOWED)
def test_each_safe_form_passes_silently(command):
    result = _run(command)
    assert result.returncode == 0, result.stderr
    assert result.stdout == ""


def test_the_deny_teaches_worker_and_orchestrator_roles_separately():
    result = _run("git checkout -- TEST_MATRIX.md")
    reason = json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "own saved bytes" in reason.lower()
    assert "halt" in reason.lower()
    assert "orchestrator" in reason.lower()


def test_malformed_input_never_crashes_the_hook():
    result = subprocess.run([sys.executable, HOOK], input="not json", capture_output=True,
                            text=True, timeout=10)
    assert result.returncode == 0
    assert result.stdout == ""
