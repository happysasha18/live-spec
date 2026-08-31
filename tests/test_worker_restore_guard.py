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

# The same destructive acts, reached by a route the guard did not walk until 2026-08-28. Each one
# passed the q-586 write-target rewrite: shell grouping and the launcher wrappers hid the program
# name, `find -exec` and a `-c` payload carried the command one level down, a substitution supplied
# the repository bytes from inside an innocent-looking command, and a missing `cwd` let an absolute
# path into the tree. None of them is exotic; every one is a shape a shell writes every day.
ROUTES_AROUND = [
    # Shell grouping in front of the program name.
    "( git checkout -- PRODUCT_SPEC.md )",
    "(git checkout .)",
    "{ git checkout -- PRODUCT_SPEC.md; }",
    "! git stash",
    # Launchers that run another program after their own options.
    "timeout 30 git checkout -- PRODUCT_SPEC.md",
    "timeout -s KILL 30 git reset --hard HEAD",
    "nohup git checkout -- PRODUCT_SPEC.md",
    "nice git clean -fd",
    "nice -n 5 git checkout -- PRODUCT_SPEC.md",
    "stdbuf -o0 git restore PRODUCT_SPEC.md",
    "setsid git checkout -- PRODUCT_SPEC.md",
    "xargs -n1 git checkout --",
    # The command carried one level down.
    "find . -name '*.py' -exec git checkout HEAD -- {} \\;",
    "find . -type f -execdir git checkout -- {} +",
    # The second of two -exec clauses: the `;` between them has to stay where it stands, or the
    # two commands read as one and the destructive half hides behind the harmless one.
    "find . -exec grep -l TODO {} \\; -exec git checkout -- {} \\;",
    "bash -c 'git checkout -- PRODUCT_SPEC.md'",
    'sh -c "git reset --hard HEAD"',
    # A substitution supplying the repository bytes.
    "printf '%s' \"$(git show HEAD:PRODUCT_SPEC.md)\" > PRODUCT_SPEC.md",
    'echo "$(git show HEAD:PRODUCT_SPEC.md)" > PRODUCT_SPEC.md',
    "tee PRODUCT_SPEC.md <<< `git show HEAD:PRODUCT_SPEC.md`",
    # An inline program in a language the guard cannot read, fed repository bytes.
    "git show HEAD:PRODUCT_SPEC.md | python3 -c \"import sys; "
    "open('PRODUCT_SPEC.md','w').write(sys.stdin.read())\"",
    "git show HEAD:PRODUCT_SPEC.md | perl -e 'print'",
    "git show HEAD:PRODUCT_SPEC.md | sh -c 'cat > PRODUCT_SPEC.md'",
    # An absolute path with no cwd in the event: the field the hook used to read as permission.
    "git show HEAD:PRODUCT_SPEC.md > /repo/PRODUCT_SPEC.md",
    "git show HEAD:PRODUCT_SPEC.md | tee /anywhere/PRODUCT_SPEC.md",
    # Five more routes, found by the 2026-08-28 adversarial read of the change above and each
    # red-proven against the tree that shipped it: the reader that stripped grouping, launchers and
    # prefix words let every one of these through.
    #
    # `eval` is neither a wrapper nor a launcher — its whole argument list is program text.
    "eval 'git checkout -- PRODUCT_SPEC.md'",
    'eval "git reset --hard HEAD"',
    # A shell's short options cluster, so the `-c` it carries is spelled many ways.
    "bash -lc 'git checkout -- PRODUCT_SPEC.md'",
    "bash -cx 'git checkout -- PRODUCT_SPEC.md'",
    "sh --command 'git checkout -- PRODUCT_SPEC.md'",
    # A single `&` ends a command as surely as `;` does.
    "echo starting & git checkout -- PRODUCT_SPEC.md",
    "echo starting |& git checkout -- PRODUCT_SPEC.md",
    # Process substitution carries the read, and the copy family carries the write.
    "cp <(git show HEAD:PRODUCT_SPEC.md) PRODUCT_SPEC.md",
    "tee PRODUCT_SPEC.md < <(git show HEAD:PRODUCT_SPEC.md)",
    # Six more routes, found by the adversarial read of 2026-08-31 and each red-proven against the
    # tree that shipped it. Every one of them destroys the file for real in a scratch repository.
    #
    # git's own pre-command options were stepped over by a list of five names, so any other one of
    # them stood where the subcommand was read. `--no-pager` is what a script writes to keep git off
    # a tty; the same hole was in guardrails/check-worker-restore.py, so neither arm saw the act.
    "git --no-pager checkout -- PRODUCT_SPEC.md",
    "git -P checkout -- PRODUCT_SPEC.md",
    "git --literal-pathspecs checkout -- PRODUCT_SPEC.md",
    "git --paginate restore PRODUCT_SPEC.md",
    "git --no-pager show HEAD:PRODUCT_SPEC.md > PRODUCT_SPEC.md",
    # A redirection may stand anywhere in a simple command, the front included. The write half was
    # found all along; the program name read as `>`, so the READ half went unseen.
    "> PRODUCT_SPEC.md git show HEAD:PRODUCT_SPEC.md",
    ">PRODUCT_SPEC.md git show HEAD:PRODUCT_SPEC.md",
    # `exec >` re-points the shell's own output for everything after it, inside one event.
    "exec > PRODUCT_SPEC.md; git show HEAD:PRODUCT_SPEC.md",
    # The brace form of a redirected group. `( … ) > f` was caught all along; `{ …; } > f` needs the
    # `;`, and the `;` ended the pipeline, so the read and the write sat in different pipelines.
    "{ git show HEAD:PRODUCT_SPEC.md; } > PRODUCT_SPEC.md",
    # The keyword that OPENS a compound statement was missing where `do` and `then` already stood.
    "if git checkout -- PRODUCT_SPEC.md; then echo ok; fi",
    "while ! git checkout -- PRODUCT_SPEC.md; do sleep 1; done",
    "until git checkout -- PRODUCT_SPEC.md; do sleep 1; done",
    # An append is innocent because the file's own bytes survive it. The same command emptying the
    # path first is what takes that reason away.
    ": > PRODUCT_SPEC.md && git show HEAD:PRODUCT_SPEC.md >> PRODUCT_SPEC.md",
    "rm PRODUCT_SPEC.md && git show HEAD:PRODUCT_SPEC.md >> PRODUCT_SPEC.md",
    "truncate -s 0 PRODUCT_SPEC.md; git show HEAD:PRODUCT_SPEC.md >> PRODUCT_SPEC.md",
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
    # Every prefix the guard now steps over still has to leave ordinary work alone: stepping over
    # `timeout` to find the program must not turn `timeout 30 pytest` into a refusal.
    "timeout 30 git status",
    "nice -n 5 python3 -m pytest -q",
    "nohup python3 scripts/render-board.sh &",
    "( cd tests && python3 -m pytest -q )",
    "{ git status; git log -1; }",
    "find . -name '*.py' -exec grep -l TODO {} \\;",
    "find . -exec grep -l TODO {} \\; -exec wc -l {} \\;",
    "bash -c 'grep -q needle haystack.md'",
    "sh -c \"git status\"",
    "python3 -c \"print(open('PRODUCT_SPEC.md').read())\"",
    "xargs -n1 git log -1 --format=%H",
    "echo \"$(git rev-parse HEAD)\" > /tmp/head.txt",
    # The 2026-08-28 repairs widened what the reader follows, so each widening owes its own
    # ordinary command back. A shell cluster carrying `c` still runs ordinary work; a background
    # `&` still separates two harmless commands; `ruby`'s inline-program flags are a tuple now, so
    # a bare `-` is an argument rather than a match inside a string; and the copy family only ever
    # reaches the write-target reader behind a repository read.
    "bash -lc 'python3 -m pytest -q'",
    "echo starting & echo finished",
    "git show HEAD:PRODUCT_SPEC.md | ruby -",
    "cp README.md /tmp/readme-backup.md",
    "cp /tmp/saved-bytes.md PRODUCT_SPEC.md",
    # Each widening of 2026-08-31 owes its own ordinary command back. Stepping over git's whole
    # pre-command option surface must not swallow a subcommand; a leading redirection must not turn
    # an honest write into a refusal; the compound-statement keywords must leave ordinary loops
    # alone; `exec >` and `{ …; } >` outside the tree are nobody's business; and an append onto a
    # path this command never emptied is still an append.
    "git --no-pager log --oneline",
    "git --no-pager status",
    "git -c core.pager=cat diff HEAD",
    "> out.txt echo hi",
    "if python3 -m pytest -q; then echo ok; fi",
    "while read line; do echo $line; done < notes.md",
    "until python3 -m pytest -q; do sleep 1; done",
    # A sink that holds nothing is not the tree, whatever the event carries for `cwd`. An absolute
    # path is deliberately NOT the ordinary command here: with no `cwd` in the event this corpus
    # runs without, an absolute target counts as the tree by the design stated in `_lands_in_the_tree`.
    "exec > /dev/null; git show HEAD:PRODUCT_SPEC.md",
    "rm scratch.txt && git show HEAD:PRODUCT_SPEC.md >> notes.md",
    # git's index-only restore, spelled short. `-S` touches no working-tree byte, and reading only
    # the long spelling denied it — along with the command that just asks for the help text.
    "git restore -S PRODUCT_SPEC.md",
    "git restore -h",
    "git restore --help",
    "mv scratch-notes.md notes.md",
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


@pytest.mark.parametrize("command", ROUTES_AROUND)
def test_a_route_around_the_write_target_rule_is_denied(command):
    """A shell shape that hides the act is not a different act.

    The write-target rewrite of 2026-08-28 asked the right question and asked it of too little
    text: it read the first token of a segment as the program, and any shape that puts something
    else there — a bracket, a launcher, a `-c` payload, a `find -exec` — walked past. Every command
    here is one of the forms already denied above, wearing one of those shapes.
    """
    result = _run(command)
    assert result.returncode == 0, result.stderr
    assert result.stdout, "the guard allowed %r" % command
    output = json.loads(result.stdout)["hookSpecificOutput"]
    assert output["permissionDecision"] == "deny"


def test_the_refusal_names_the_text_the_caller_typed_not_the_nested_command():
    """A refusal quoting a fragment the caller never wrote is a refusal they cannot act on."""
    reason = _reason("find . -name '*.py' -exec git checkout HEAD -- {} \\;")
    assert "find ." in reason and "-exec" in reason


def test_a_painted_over_element_elsewhere_in_the_command_does_not_silence_the_guard():
    """One innocent stage beside a destructive one never turns the pair innocent."""
    assert _run("git status && ( git checkout -- PRODUCT_SPEC.md )").stdout != ""
    assert _run("ls -la | grep py; timeout 5 git stash").stdout != ""


def test_an_absolute_target_with_no_cwd_is_refused_rather_than_assumed_harmless():
    """The event's `cwd` places an absolute path. A field it did not carry places nothing.

    With no `cwd` the hook used to pass every absolute target, so the same command that reds when
    the event is complete went green when it was not.
    """
    read = "git show HEAD:PRODUCT_SPEC.md"
    assert _run("%s > /repo/PRODUCT_SPEC.md" % read).stdout != ""
    assert _run("%s > /somewhere/else.md" % read).stdout != ""
    # A discard sink still holds nothing, whatever the event carries.
    assert _run("%s > /dev/null" % read).stdout == ""


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
