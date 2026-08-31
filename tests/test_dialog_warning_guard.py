"""A session is warned before a command that can raise a macOS security dialog runs (PLAN q-581).

The deposit this row answers (2026-08-07, `docs/queue-archive/2026-08-07-from-tlvphotos-system-
dialogs-need-announcing.md`): the owner was interrupted twice in one session by a dialog he always
answers Deny, and the session never saw the dialog coming. The absorbed neighbour (PLAN q-542,
folded in 2026-08-28): a server bound to every interface raises the same class of dialog the moment
it binds, not only once left running.

`hooks/dialog-warning-guard.py` holds the one flat list beside the one rule sentence (PLAN q-581's
own words: "listed in one place beside the rule that governs them"). This suite hands the guard
every command the list names — imported from the module itself, so appending an entry to
KNOWN_DIALOG_COMMANDS there is the only edit a new case needs; nothing here is a second copy of the
list — and reds unless the guard's warning goes out before the command would run. It also proves an
ordinary command passes silently, and that the rule's own sentence lives in exactly one file in the
tree.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

import pytest

from conftest import ROOT

HOOK = os.path.join(ROOT, "hooks", "dialog-warning-guard.py")


def _load_guard():
    spec = importlib.util.spec_from_file_location("dialog_warning_guard", HOOK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = _load_guard()

# Every command an entry on the list must catch, read straight off the module's own list — the only
# place this suite would need a second edit is if an entry's own "example" stopped matching its own
# "pattern", which the parametrized test below would red on directly.
KNOWN_EXAMPLES = [(entry["name"], entry["example"]) for entry in guard.KNOWN_DIALOG_COMMANDS]

# Ordinary commands a session runs constantly. None of these may ever be warned about.
ORDINARY = [
    "ls -la",
    "git status",
    "python3 -m pytest -q",
    "git commit -m 'x'",
    "curl https://example.com",
    "python3 -m http.server 8080",  # no --bind/--host at all: defaults to loopback, no warning owed
    "python3 -m http.server 8080 --bind 127.0.0.1",
]


def _run(command):
    payload = {"tool_name": "Bash", "tool_input": {"command": command}}
    return subprocess.run([sys.executable, HOOK], input=json.dumps(payload), capture_output=True,
                           text=True, timeout=10)


@pytest.mark.parametrize("name,command", KNOWN_EXAMPLES)
def test_each_listed_command_is_warned_before_it_runs(name, command):
    result = _run(command)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip(), (
        "%s: the guard let %r through with no warning — a listed command must be announced before "
        "it runs" % (name, command)
    )
    output = json.loads(result.stdout)["hookSpecificOutput"]
    assert output["hookEventName"] == "PreToolUse"
    assert output["permissionDecision"] == "ask"
    reason = output["permissionDecisionReason"]
    entry = next(e for e in guard.KNOWN_DIALOG_COMMANDS if e["name"] == name)
    assert entry["dialog"] in reason
    assert guard.RULE in reason


@pytest.mark.parametrize("command", ORDINARY)
def test_ordinary_commands_pass_silently(command):
    result = _run(command)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "", "an ordinary command was warned about: %r -> %r" % (
        command, result.stdout)


def test_malformed_input_stands_down_rather_than_guessing():
    result = subprocess.run([sys.executable, HOOK], input="not json", capture_output=True,
                             text=True, timeout=10)
    assert result.returncode == 0
    assert result.stdout == ""


def test_a_non_bash_tool_is_ignored():
    payload = {"tool_name": "Edit", "tool_input": {"command": "security find-generic-password -w"}}
    result = subprocess.run([sys.executable, HOOK], input=json.dumps(payload), capture_output=True,
                             text=True, timeout=10)
    assert result.returncode == 0
    assert result.stdout == ""


def test_the_rule_sentence_lives_in_exactly_one_file_in_the_tree():
    """PLAN q-581's own acceptance: grep finds the rule stated once and nowhere twice."""
    proc = subprocess.run(
        ["git", "-C", ROOT, "grep", "--untracked", "-l", "-F", guard.RULE],
        capture_output=True, text=True,
    )
    # `git grep` exits 1 when nothing matches, which would itself be a failure worth seeing plainly
    # rather than folded into the assert below.
    assert proc.returncode in (0, 1), proc.stderr
    hits = [line for line in proc.stdout.splitlines() if line.strip()]
    assert hits == ["hooks/dialog-warning-guard.py"], (
        "the rule's own sentence must live in exactly one file, this one; found: %r" % hits
    )
