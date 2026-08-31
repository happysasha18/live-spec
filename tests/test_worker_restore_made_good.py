"""A finding the tree shows made good stops blocking every future push (PLAN q-527, SPEC INV-299).

The census arm reads records that stay on disk, so a finding it makes is true forever. Until this
suite existed a finished recovery cleared nothing: every push after an incident waited for the
reading window to roll past it, or for somebody to move the counting start by hand. What counts as
made good is stated once, in `spec/guardrails-freshness.md` Requirement 301 — every file the command
named carries, in the repository that command ran in, a commit dated later than the command.

The fixture below is one incident and one repository, and the test holds both directions over it:
red while the tree has no such commit, clean the moment the commit exists. Nothing else about the
fixture moves between the two readings, so the commit is the whole difference.

The fixture stands up a real repository with the gate's own copy inside it, because the gate reads
its project key from the directory it sits in (`own_repo`). A session recorded in some other
repository is a NEIGHBOUR's finding, which reds nothing for its own separate reason and would prove
nothing here.
"""
import json
import os
import shutil
import subprocess

from conftest import ROOT

# The incident's own moment, the stamp the fixture transcript carries. The baseline commit sits
# before it and a repair commit sits after it, so "later than the command" is the only thing the two
# readings differ on.
INCIDENT_AT = "2026-07-27T20:26:28.001Z"
BEFORE_INCIDENT = "2026-07-27T10:00:00Z"
AFTER_INCIDENT = "2026-07-28T09:00:00Z"

# Before the first finding this fixture makes, so nothing here is carried as history instead.
FIXTURE_COUNTING_FROM = "2026-07-01"

DISCARDED = "TEST_MATRIX.md"


def _commit(repo, message, when):
    """One commit in `repo`, dated exactly `when` so the reading has a fixed boundary to compare."""
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when,
        "GIT_AUTHOR_NAME": "fixture", "GIT_COMMITTER_NAME": "fixture",
        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    })
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", message],
                   check=True, capture_output=True, env=env)


def _project(tmp_path):
    """A repository the gate reads as its own, holding the gate and one committed file.

    The gate's project key is the shared git directory beside its own file, so a copy of the gate
    inside this repository makes every session recorded here THIS project's session — the case that
    reds, and so the case a way out has to clear.
    """
    repo = tmp_path / "fixture-project"
    (repo / "guardrails").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True, capture_output=True)
    for name in ("check-worker-restore.py", "nonempty_input.py"):
        shutil.copy(os.path.join(ROOT, "guardrails", name), str(repo / "guardrails" / name))
    (repo / DISCARDED).write_text("the matrix as it stood before the worker ran\n", encoding="utf-8")
    _commit(repo, "the stage the worker found", BEFORE_INCIDENT)
    return repo


def _transcripts(tmp_path, repo, command):
    """A transcript root holding one worker run that handed a shell `command` inside `repo`."""
    runs = tmp_path / "projects" / "-fixture-project" / "s-0001" / "subagents"
    runs.mkdir(parents=True)
    run = runs / "agent-a1234567890abcdef.jsonl"
    call = {
        "type": "assistant", "isSidechain": True,
        "agentId": "a1234567890abcdef", "sessionId": "s-0001",
        "cwd": str(repo), "timestamp": INCIDENT_AT,
        "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "toolu_0000", "name": "Bash",
             "input": {"command": command}},
        ]},
    }
    answer = {
        "type": "user", "isSidechain": True,
        "agentId": "a1234567890abcdef", "sessionId": "s-0001", "cwd": str(repo),
        "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "toolu_0000", "content": ""},
        ]},
    }
    with open(run, "w", encoding="utf-8") as f:
        f.write(json.dumps(call) + "\n")
        f.write(json.dumps(answer) + "\n")
    return str(tmp_path / "projects"), str(run)


def _acceptance(repo, root):
    """The row's own acceptance command, run inside the fixture project.

    Literally `python3 guardrails/check-worker-restore.py`, with no argument of its own: the
    transcript root and the counting start reach it through the two environment overrides the gate
    already reads, so the fixture needs no option this check did not already have.
    """
    env = dict(os.environ)
    env["LIVE_SPEC_TRANSCRIPT_ROOT"] = root
    env["LIVE_SPEC_WORKER_RESTORE_FROM"] = FIXTURE_COUNTING_FROM
    return subprocess.run(["python3", "guardrails/check-worker-restore.py"],
                          cwd=str(repo), capture_output=True, text=True, env=env)


def _repair(repo):
    """The recovery, as the tree records it: the discarded file written again and committed."""
    (repo / DISCARDED).write_text("the matrix, converted again after the worker discarded it\n",
                                  encoding="utf-8")
    _commit(repo, "the discarded conversion, written again", AFTER_INCIDENT)


def test_the_repair_clears_the_finding_and_its_absence_keeps_it_red(tmp_path):
    """Both directions over one fixture: red without the repair, clean with it.

    The transcript never changes between the two readings. The commit is the whole difference, which
    is what makes this a way out rather than a description of one.
    """
    repo = _project(tmp_path)
    root, run = _transcripts(tmp_path, repo, "git checkout -- %s" % DISCARDED)

    without = _acceptance(repo, root)
    assert without.returncode == 1, (
        "the finding cleared with no repair in the tree:\n%s" % without.stdout)
    assert DISCARDED in without.stdout
    assert "MADE GOOD" not in without.stdout

    _repair(repo)

    with_repair = _acceptance(repo, root)
    assert with_repair.returncode == 0, (
        "a finished recovery still blocks the push:\n%s%s" % (with_repair.stdout,
                                                              with_repair.stderr))
    assert "MADE GOOD" in with_repair.stdout, (
        "the cleared finding was dropped in silence:\n%s" % with_repair.stdout)
    assert run in with_repair.stdout
    assert DISCARDED in with_repair.stdout


def test_a_commit_older_than_the_command_clears_nothing(tmp_path):
    """The boundary is the command's own moment. The file this fixture carries was committed before
    the worker ran, and that commit says nothing about work discarded afterwards."""
    repo = _project(tmp_path)
    root, _ = _transcripts(tmp_path, repo, "git checkout -- %s" % DISCARDED)
    result = _acceptance(repo, root)
    assert result.returncode == 1, result.stdout


def test_an_unbounded_blast_radius_is_never_made_good(tmp_path):
    """A command that names no single file discards a set no commit can show is back, so it keeps
    reddening however much the tree moves afterwards (SPEC Requirement 301, criterion 23)."""
    for command in ("git reset --hard HEAD", "git stash", "git checkout -- .",
                    "git clean -fd guardrails"):
        repo = _project(tmp_path / command.replace(" ", "-").replace("/", "-"))
        root, _ = _transcripts(tmp_path / command.replace(" ", "-").replace("/", "-"),
                               repo, command)
        _repair(repo)
        result = _acceptance(repo, root)
        assert result.returncode == 1, (
            "`%s` cleared on a commit that proves nothing about it:\n%s" % (command, result.stdout))
        assert "MADE GOOD" not in result.stdout


def test_an_unstamped_record_is_never_made_good(tmp_path):
    """No timestamp, no boundary: the check cannot say which commits came after the command, so the
    finding stays red (SPEC Requirement 301, criterion 24)."""
    repo = _project(tmp_path)
    root, run = _transcripts(tmp_path, repo, "git checkout -- %s" % DISCARDED)
    records = [json.loads(line) for line in open(run, encoding="utf-8")]
    records[0].pop("timestamp")
    with open(run, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
    _repair(repo)
    result = _acceptance(repo, root)
    assert result.returncode == 1, result.stdout
    assert "MADE GOOD" not in result.stdout


def test_the_verify_arm_stays_red_after_the_repair(tmp_path):
    """The way out is the census arm's alone. A worker run the verify arm reds stays red for
    acceptance however the tree moves afterwards (SPEC Requirement 301, criterion 25)."""
    repo = _project(tmp_path)
    _, run = _transcripts(tmp_path, repo, "git checkout -- %s" % DISCARDED)
    _repair(repo)
    result = subprocess.run(
        ["python3", "guardrails/check-worker-restore.py", "--run", run],
        cwd=str(repo), capture_output=True, text=True)
    assert result.returncode == 1, (
        "a repair in the tree made a red worker run acceptable:\n%s" % result.stdout)
    assert "MADE GOOD" not in result.stdout
