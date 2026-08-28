"""The shell-boundary arm denies destructive git commands before Bash runs them."""
import json
import os
import re
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
    "git checkout-index -f -a",
    "git checkout-index --force -- PRODUCT_SPEC.md",
]

# The same loss assembled out of stages that each report themselves as a read. Every one of these
# puts repository bytes back over a path in the working tree, and none of them is any of the git
# verbs above — the class the guard missed until 2026-08-28, with the first line of it the route the
# refusal text itself used to recommend (ROADMAP row 479, PLAN q-586).
ASSEMBLED = [
    "git show HEAD:PRODUCT_SPEC.md > PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md >PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md >| PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md &> PRODUCT_SPEC.md",
    'git show HEAD:PRODUCT_SPEC.md > "PRODUCT_SPEC.md"',
    "git show HEAD~2:docs/OVERVIEW.md > docs/OVERVIEW.md",
    "git show HEAD:PRODUCT_SPEC.md | tee PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md | cat > PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md | dd of=PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md | sponge PRODUCT_SPEC.md",
    "git cat-file -p HEAD:PRODUCT_SPEC.md > PRODUCT_SPEC.md",
    "git cat-file blob 0f1e2d3 > PRODUCT_SPEC.md",
    "git archive HEAD PRODUCT_SPEC.md | tar -x",
    "git archive HEAD | tar xf -",
    "cd tests && git show HEAD:conftest.py > conftest.py",
    "sudo git show HEAD:PRODUCT_SPEC.md > PRODUCT_SPEC.md",
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
    "git checkout-index -a",
    # Reading history is free; the loss needs the bytes to land on a path in the tree.
    "git show HEAD:PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md > /dev/null",
    "git show HEAD:PRODUCT_SPEC.md | diff - PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md | head -20",
    "git archive HEAD | tar -t",
    # Appending leaves what the file holds in place.
    "git show HEAD:PRODUCT_SPEC.md >> notes.md",
    # A worker writing its OWN saved bytes back is the rule's own recovery route.
    "cat /tmp/saved-bytes > PRODUCT_SPEC.md",
    "printf 'x' > PRODUCT_SPEC.md",
    "git status 2>&1 | tee status.txt",
]


def _run(command, cwd=None):
    payload = {"tool_name": "Bash", "tool_input": {"command": command}}
    if cwd is not None:
        payload["cwd"] = cwd
    return subprocess.run([sys.executable, HOOK], input=json.dumps(payload), capture_output=True,
                          text=True, timeout=10)


def _reason(command, cwd=None):
    result = _run(command, cwd)
    assert result.returncode == 0, result.stderr
    assert result.stdout, "the guard allowed %r" % command
    return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]


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


@pytest.mark.parametrize("command", ASSEMBLED)
def test_a_repository_read_landed_on_a_tree_path_is_denied(command):
    """The act is repository bytes reaching a path in the tree, however the shell assembles it.

    Every command here reads history with a verb that only prints, then lands what it printed on a
    working-tree path. Read one stage at a time, each half looks innocent, which is why the guard
    judges the whole pipeline against its write target.
    """
    result = _run(command)
    assert result.returncode == 0, result.stderr
    assert result.stdout, "the guard allowed %r" % command
    output = json.loads(result.stdout)["hookSpecificOutput"]
    assert output["permissionDecision"] == "deny"
    assert "working tree" in output["permissionDecisionReason"]


def test_the_refusal_recommends_only_routes_it_would_itself_allow():
    """A refusal that names a way around itself is worse than no refusal.

    Every command the refusal text puts in backticks — bar the one it is refusing — goes back
    through the guard, and each must pass. This is what the `git show HEAD:<path> > <path>` hole
    was: the guard's own text signposted the read half of the route around it.
    """
    denied = "git checkout -- TEST_MATRIX.md"
    reason = _reason(denied)
    recommended = [span for span in re.findall(r"`([^`]+)`", reason) if span != denied]
    assert recommended, "the refusal recommends no route at all"
    for command in recommended:
        result = _run(command)
        assert result.stdout == "", (
            "the refusal recommends %r and the guard denies it, so its own advice is a route "
            "around itself: %s" % (command, result.stdout))


def test_where_the_bytes_land_is_what_decides():
    """One read, three landing places: the tree reds, a discard sink and another tree do not."""
    read = "git show HEAD:PRODUCT_SPEC.md"
    assert _run("%s > /dev/null" % read, cwd="/repo").stdout == ""
    assert _run("%s > /elsewhere/copy.md" % read, cwd="/repo").stdout == ""
    assert _run("%s > /repo/PRODUCT_SPEC.md" % read, cwd="/repo").stdout != ""
    assert _run("%s > PRODUCT_SPEC.md" % read, cwd="/repo").stdout != ""


def test_the_refusal_names_the_path_the_bytes_would_have_landed_on():
    reason = _reason("git show HEAD:PRODUCT_SPEC.md | tee PRODUCT_SPEC.md")
    assert "PRODUCT_SPEC.md" in reason
    assert "git show HEAD:PRODUCT_SPEC.md | tee PRODUCT_SPEC.md" in reason


def test_malformed_input_never_crashes_the_hook():
    result = subprocess.run([sys.executable, HOOK], input="not json", capture_output=True,
                            text=True, timeout=10)
    assert result.returncode == 0
    assert result.stdout == ""
