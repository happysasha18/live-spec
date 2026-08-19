"""A worker never restores a working tree with a git command (ROADMAP row 479).

Two destructions of uncommitted work landed on 2026-07-23 — an applier's `-o` clobber, and a
caps-sweep worker's `git checkout -- TEST_MATRIX.md` that discarded an uncommitted format
conversion. A third came within three minutes of costing a night on 2026-07-27, when a worker in the
tlvphotos tree mutated a shipped client bundle to prove a test row red, restored it with
`git checkout -- engine/assets/exhibition.js`, and a sibling lane began writing the sources that
assemble into that same file.

The law: a worker holds a file's bytes before it mutates it and writes those bytes back, and runs no
command that discards uncommitted work, in any tree. A restore is a different act from a write — its
blast radius is a path, so it lands on files the worker never wrote and its brief never named, and
the brief-time write-set disjointness that fences concurrent edits gives no cover. A worker holding
no saved bytes halts and reports; the orchestrator restores the file from the last committed stage,
re-briefs the worker with that file's current bytes, and commits a finished build stage before the
next worker touches its files.

Two machines hold it. The clause stands in every home a worker learns its contract from, sentence by
sentence, so a home that drifts to its own wording or its own command list reds below.
`guardrails/check-worker-restore.py` reads the worker runs' own transcripts for the command, since
the `git status` a careful worker pastes afterwards reads "clean" in the safe case and the
destructive one alike — prose cannot separate them, the command can. The gate is armed at the verify
step of the pipeline skill and once more here, against this machine's own transcript root.
"""
import json
import os
import subprocess

import pytest

from conftest import ROOT, read_flat

GATE = os.path.join(ROOT, "guardrails", "check-worker-restore.py")

# Every home a worker learns its contract from. A drop in any one of them reds.
CLAUSE_HOMES = [
    "skills/live-spec-base/SKILL.md",
    "skills/build-pipeline/SKILL.md",
    "skills/build-pipeline/references/delegation-protocol.md",
    "templates/agent.template.md",
    "scripts/open-lane.sh",
]

# The clause, sentence by sentence, in the one wording every home carries. The saving step opens it,
# because a worker with no saved bytes has no way back. The command list is the list the gate reds
# on. The scope sentence answers the worktree question a lane worker would otherwise answer for
# itself. The halt names what the worker does and the recovery names what the orchestrator does, so
# the failure branch has an exit.
CLAUSE_SENTENCES = [
    "Before a worker mutates a file it means to put back, it reads that file and holds its bytes.",
    "A worker puts a file back by WRITING ITS OWN SAVED BYTES.",
    "A worker runs no command that discards uncommitted work, in any tree: `git checkout -- "
    "<path>`, `git checkout .`, `git restore` outside `--staged`, `git stash` and its `push`, "
    "`save`, `create` and `store` forms, `git reset` with `--hard`, `--merge` or `--keep`, and "
    "`git clean` with `-f` or `-x`.",
    "Such a command's blast radius is a PATH, so its damage lands on files the worker never wrote "
    "and its brief never named.",
    "This rule binds a worker in every tree, including its own isolated worktree, since a worktree "
    "shares one repository with the lanes beside it and a worker cannot read off its brief what "
    "else that repository holds.",
    "A worker that holds no saved bytes for a file it mutated, or that believes a file needs a "
    "git-level restore, HALTS and reports the file and the mutation it made, and it writes no "
    "further file and runs no further command.",
    "The orchestrator owns recovery: it restores the named file from the last committed stage, "
    "hands the worker a fresh brief carrying that file's current bytes, and records the halt in the "
    "row's delivery report, and the halted work resumes under that new brief.",
    "`guardrails/check-worker-restore.py` reads the worker runs' transcripts for the command and "
    "runs at the verify step.",
]

# The orchestrator's own half, stated where row 479 states it.
ORCHESTRATOR_HALF = "a finished build stage is committed before the next worker touches its files"

# Every command form the rule names, each in a form a worker would plausibly type.
DISCARDING = {
    "git checkout --": "git checkout -- engine/assets/exhibition.js",
    "git restore": "git restore engine/assets/exhibition.js",
    "git stash": "git stash push -- engine/assets/exhibition.js",
    "git reset --hard": "git reset --hard HEAD",
    "git clean": "git clean -fd engine/assets",
}

# The forms the prose names beside those, each read by the same gate arm.
ALSO_DISCARDING = [
    "git checkout .",
    "git reset --merge HEAD",
    "git reset --keep HEAD",
    "git clean -xdf",
    "git stash save wip",
]


# The fixture runs below carry the lived incident's own stamp, 2026-07-27, which falls before the
# gate's shipped counting start. Every fixture case therefore hands the gate a start date early
# enough to read the whole fixture; the cases that judge the counting start pass their own.
FIXTURE_COUNTING_FROM = "2026-07-01"


def _gate(*args, counting_from=FIXTURE_COUNTING_FROM):
    argv = list(args)
    if counting_from and "--counting-from" not in argv:
        argv += ["--counting-from", counting_from]
    return subprocess.run(["python3", GATE, *argv], capture_output=True, text=True)


def _run_record(command, agent="a1234567890abcdef", session="s-0001",
                cwd="/Users/someone/exhibition-engine", tool_id="toolu_0000"):
    """One assistant record carrying a Bash tool_use, the shape a real worker transcript carries.

    `tool_id` is the call's own id, which the shell's answer repeats in its `tool_use_id`."""
    return {
        "type": "assistant",
        "isSidechain": True,
        "agentId": agent,
        "sessionId": session,
        "cwd": cwd,
        "timestamp": "2026-07-27T20:26:28.001Z",
        "message": {"role": "assistant", "content": [
            {"type": "text", "text": "putting the bundle back"},
            {"type": "tool_use", "id": tool_id, "name": "Bash", "input": {"command": command}},
        ]},
    }


def _result_record(tool_use_id, denial_kind=None, shell_error=False, stdout="", session="s-0001",
                   agent="a1234567890abcdef", cwd="/Users/someone/exhibition-engine"):
    """The shell's answer to one Bash call, at the shape the harness writes it.

    A call the harness refused carries `toolDenialKind` on the record and `is_error` on the block,
    and its text is a refusal notice rather than anything a shell produced. A call that ran carries
    no denial key, whether the shell was happy with it (`shell_error` false) or the command exited
    non-zero (`shell_error` true, the shell's own complaint as the text).
    """
    if denial_kind:
        content = ("Permission for this action was denied by the Claude Code auto mode classifier. "
                   "Reason: Blocked by classifier.")
        result = "Error: " + content
    elif shell_error:
        content = "error: pathspec did not match any file known to git"
        result = "Error: Exit code 1 " + content
    else:
        content = stdout
        result = {"stdout": stdout, "stderr": "", "interrupted": False, "isImage": False}
    record = {
        "type": "user",
        "isSidechain": True,
        "agentId": agent,
        "sessionId": session,
        "cwd": cwd,
        "timestamp": "2026-07-27T20:26:29.001Z",
        "toolUseResult": result,
        "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_use_id, "content": content,
             "is_error": bool(denial_kind) or shell_error},
        ]},
    }
    if denial_kind:
        record["toolDenialKind"] = denial_kind
    return record


def _transcript_root(tmp_path, commands, project="-Users-someone-exhibition-engine",
                     session="s-0001", agent="a1234567890abcdef",
                     cwd="/Users/someone/exhibition-engine", answers=None):
    """A transcript root holding one worker run, at the layout the harness writes:
    <root>/<project-dir>/<session-id>/subagents/agent-<id>.jsonl

    `cwd` is the directory the harness recorded for the run. A case that turns on a FAILED `cd`
    hands a real git repository here, since that is where the shell stayed.

    `answers` runs parallel to `commands` and says what the shell did with each call: None writes no
    answer at all, which is the run cut off mid-call, `"ran"` writes an ordinary shell answer,
    `"ran-error"` writes one from a command the shell ran and that exited non-zero, and any other
    string writes a refusal carrying that denial kind."""
    runs = tmp_path / "projects" / project / session / "subagents"
    runs.mkdir(parents=True)
    path = runs / ("agent-%s.jsonl" % agent)
    answers = answers if answers is not None else [None] * len(commands)
    with open(path, "w", encoding="utf-8") as f:
        for i, (c, answer) in enumerate(zip(commands, answers)):
            tool_id = "toolu_%04d" % i
            f.write(json.dumps(_run_record(c, agent=agent, session=session, cwd=cwd,
                                           tool_id=tool_id)) + "\n")
            if answer is None:
                continue
            denial = None if answer in ("ran", "ran-error") else answer
            f.write(json.dumps(_result_record(tool_id, denial_kind=denial,
                                              shell_error=answer == "ran-error", stdout="",
                                              session=session, agent=agent, cwd=cwd)) + "\n")
    return str(tmp_path / "projects"), str(path)


def _repo(tmp_path, name="worktree"):
    """A directory that reads as a git repository at scan time."""
    repo = tmp_path / name
    repo.mkdir(parents=True)
    (repo / ".git").mkdir()
    return repo


class TestGateRedsOnADiscardingCommand:

    def test_the_lived_case_reds_and_names_its_path(self, tmp_path):
        """The tlvphotos restore, read back out of a worker run."""
        root, run = _transcript_root(tmp_path, ["git checkout -- engine/assets/exhibition.js"])
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout + res.stderr
        assert "engine/assets/exhibition.js" in res.stdout
        assert "git checkout --" in res.stdout
        assert run in res.stdout, "the red names the worker run it read the command from"

    @pytest.mark.parametrize("which,command", sorted(DISCARDING.items()))
    def test_each_named_command_reds(self, tmp_path, which, command):
        root, _ = _transcript_root(tmp_path, [command])
        res = _gate("--root", root)
        assert res.returncode == 1, "%s passed the gate: %s" % (which, res.stdout)
        assert which in res.stdout

    @pytest.mark.parametrize("command", ALSO_DISCARDING)
    def test_the_other_forms_the_prose_names_red_too(self, tmp_path, command):
        """The prose and the gate carry one list, so every form the clause names reds here."""
        root, _ = _transcript_root(tmp_path, [command])
        res = _gate("--root", root)
        assert res.returncode == 1, "%s passed the gate: %s" % (command, res.stdout)

    def test_a_command_buried_after_a_cd_still_reds(self, tmp_path):
        """A forbidden command run after a `cd` still reds when the directory it moved into is
        a real git repository right now — the gate places the command, it does not excuse it."""
        repo = tmp_path / "tree"
        repo.mkdir()
        (repo / ".git").mkdir()
        root, _ = _transcript_root(tmp_path, ["cd %s && git restore src/app.js" % repo])
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout
        assert "src/app.js" in res.stdout
        assert str(repo) in res.stdout, "the red names the directory the command really ran in"

    @pytest.mark.parametrize("command", ["command git checkout -- .", "sudo git checkout -- ."])
    def test_a_wrapper_prefix_does_not_hide_the_command(self, tmp_path, command):
        """`command git` and `sudo git` discard exactly what bare git discards, and both walked
        past the gate until 2026-08-05 because the matcher read only the first word."""
        repo = _repo(tmp_path)
        root, _ = _transcript_root(tmp_path / "transcripts", [command], cwd=str(repo))
        res = _gate("--root", root)
        assert res.returncode == 1, "%s passed the gate: %s" % (command, res.stdout)
        assert "git checkout --" in res.stdout

    def test_the_red_carries_one_typed_line(self, tmp_path):
        """The gate contract's first convention: one parseable JSON object beside the human lines."""
        root, _ = _transcript_root(tmp_path, ["git checkout -- engine/assets/exhibition.js"])
        res = _gate("--root", root)
        objects = [json.loads(line) for line in res.stdout.splitlines()
                   if line.startswith("{") and line.rstrip().endswith("}")]
        assert len(objects) == 1, "a blocking red emits exactly one JSON object"
        record = objects[0]
        assert record["severity"] == "error"
        assert record["code"] == "worker-restore"
        assert "engine/assets/exhibition.js" in record["message"]
        assert record["fix"]

    def test_the_header_declares_the_gate_blocking(self):
        """The gate contract's second convention: a header comment names blocking or advisory."""
        with open(GATE, encoding="utf-8") as f:
            head = f.read(4000)
        assert "BLOCKING" in head


class TestEveryFindingSaysWhatTheShellDid:
    """A finding names its outcome, so the project receiving it knows what recovery it faces.

    tlvphotos read the finding of 2026-08-12 and answered it the same day
    (inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md): the harness classifier declined the
    `git checkout --`, it never ran, and nothing was lost — while the finding as written said
    uncommitted edits were dropped. The shell's own answer sat in the same transcript all along, in
    the tool_result whose `tool_use_id` repeats the call's id. All three outcomes are findings, since
    the rule forbids handing the command to a shell at all, and each one says which it was.
    """

    CASES = {
        "ran": ("ran", "RAN", "discarding every uncommitted change"),
        "declined": ("automode-blocked", "DECLINED", "nothing was discarded"),
        "unknown": (None, "UNKNOWN", "is unknown"),
    }

    @pytest.mark.parametrize("outcome", sorted(CASES))
    def test_each_outcome_reds_and_names_itself(self, tmp_path, outcome):
        answer, field, sentence = self.CASES[outcome]
        root, _ = _transcript_root(tmp_path, ["git checkout -- engine/assets/exhibition.js"],
                                   answers=[answer])
        res = _gate("--root", root)
        assert res.returncode == 1, "a %s command stopped reding: %s" % (outcome, res.stdout)
        assert "outcome : %s" % field in res.stdout, (
            "the finding never says the command %s:\n%s" % (outcome, res.stdout))
        assert sentence in res.stdout, (
            "the finding's own sentence never says what the %s outcome leaves to recover:\n%s"
            % (outcome, res.stdout))

    def test_the_declined_finding_names_the_denial_kind(self, tmp_path):
        """The harness's own word for the refusal, so a reader can tell a classifier block from a
        permission rule from a person saying no."""
        root, _ = _transcript_root(tmp_path, ["git checkout -- lab/data/step3-grid-derivation.json"],
                                   answers=["automode-blocked"])
        res = _gate("--root", root)
        assert "automode-blocked" in res.stdout
        assert "declined" in res.stdout

    def test_the_three_outcomes_read_differently(self, tmp_path):
        """The whole point, stated as one assertion: one command, three shells' answers, three
        different findings. A gate that collapses them back into one sentence reds here."""
        sentences = {}
        for outcome, (answer, _field, _s) in sorted(self.CASES.items()):
            root, _ = _transcript_root(tmp_path / outcome,
                                       ["git checkout -- engine/assets/exhibition.js"],
                                       answers=[answer])
            res = _gate("--root", root)
            first = [line for line in res.stdout.splitlines()
                     if line.startswith("check-worker-restore: ")][0]
            sentences[outcome] = first
        assert len(set(sentences.values())) == 3, (
            "the gate stopped telling the outcomes apart — it wrote %r for %d distinct shells' "
            "answers" % (sentences, len(sentences)))

    def test_an_executed_finding_prints_before_a_declined_one(self, tmp_path):
        """Ranked by the recovery each leaves: bytes that may be gone come first, an attempt that
        cost nothing comes last."""
        root, _ = _transcript_root(
            tmp_path,
            ["git checkout -- declined-first.js", "git checkout -- ran-second.js"],
            answers=["automode-blocked", "ran"])
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout
        assert res.stdout.index("ran-second.js") < res.stdout.index("declined-first.js"), (
            "the declined attempt printed ahead of the executed command:\n%s" % res.stdout)
        assert "1 ran, 1 declined" in res.stdout, "the verdict never tallies the outcomes"

    def test_the_typed_line_carries_the_outcome_and_the_tally(self, tmp_path):
        """A machine reading the one JSON object reads the most urgent finding of the run."""
        root, _ = _transcript_root(
            tmp_path,
            ["git checkout -- declined-first.js", "git checkout -- ran-second.js"],
            answers=["automode-blocked", "ran"])
        res = _gate("--root", root)
        objects = [json.loads(line) for line in res.stdout.splitlines()
                   if line.startswith("{") and line.rstrip().endswith("}")]
        assert len(objects) == 1
        assert objects[0]["outcome"] == "ran"
        assert objects[0]["outcomes"] == {"ran": 1, "declined": 1, "unknown": 0}
        assert "ran-second.js" in objects[0]["message"]

    def test_a_command_that_exited_non_zero_still_ran(self, tmp_path):
        """An error the SHELL returned is not a refusal: the command reached a shell, and whatever
        it discarded before it stopped is gone."""
        root, _ = _transcript_root(tmp_path, ["git checkout -- engine/assets/exhibition.js"],
                                   answers=["ran-error"])
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout
        assert "outcome : RAN" in res.stdout
        assert "DECLINED" not in res.stdout


class TestTheGateModelsCdInsideTheCommand:
    """The gate carries no model of `cd` inside one command string is the bug (2026-08-05): a
    worker `cd`ed into a freshly `git init`-ed throwaway fixture repo under scratchpad and ran
    `git checkout -q -- . 2>/dev/null || true` THERE, and the gate stamped it as a live-spec
    violation because it read every command as if it ran at the record's own cwd."""

    def test_a_cd_into_a_directory_gone_by_scan_time_is_not_a_finding(self, tmp_path):
        """The fixture directory the worker built and threw away no longer exists on disk when
        the gate runs, so a command it ran there is not this repo's problem."""
        gone = tmp_path / "throwaway" / "e2"  # never created — gone by construction
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["cd %s && git checkout -- ." % gone])
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout

    def test_a_cd_into_a_real_repo_is_a_finding_naming_that_directory(self, tmp_path):
        """The same shape, but the directory the worker `cd`ed into still holds a real `.git`
        at scan time — a live blast radius, so it reds and names where it really happened."""
        repo = tmp_path / "throwaway" / "e2"
        repo.mkdir(parents=True)
        (repo / ".git").mkdir()
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["cd %s && git checkout -- ." % repo])
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout
        assert str(repo) in res.stdout, "the finding names the directory it really ran in"

    def test_git_dash_c_names_its_own_directory(self, tmp_path):
        """`git -C <repo> ...` sets the directory for that one invocation, with no `cd` at all."""
        repo = tmp_path / "elsewhere"
        repo.mkdir()
        (repo / ".git").mkdir()
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["git -C %s checkout -- ." % repo])  # the record's cwd is the fixed default, not repo
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout
        assert str(repo) in res.stdout, "the finding names the -C directory, not the session cwd"

    def test_a_failed_cd_before_a_semicolon_places_the_command_at_the_cwd(self, tmp_path):
        """The escape an adversarial review found on 2026-08-05: `cd` into a directory that is not
        there fails, the shell stays in the record's own cwd, and the `;` runs git THERE — while the
        gate filed the command under a directory that never existed and passed it."""
        repo = _repo(tmp_path)
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["cd %s ; git checkout -- ." % (tmp_path / "nonexistent-at-scan")],
            cwd=str(repo))
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout
        assert str(repo) in res.stdout, "the finding names the directory the shell never left"

    def test_a_failed_cd_before_an_or_places_the_command_at_the_cwd(self, tmp_path):
        """`||` runs the next command precisely BECAUSE the cd failed, so the same reading holds."""
        repo = _repo(tmp_path)
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["cd %s || git checkout -- ." % (tmp_path / "nonexistent-at-scan")],
            cwd=str(repo))
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout
        assert str(repo) in res.stdout

    def test_a_cd_under_set_e_carries_the_rest_of_the_script_with_it(self, tmp_path):
        """The fixture scripts this repo's own workers write: `set -e`, a `mkdir -p X && cd X`, and
        the throwaway repo's own commands on the lines below. Under errexit a failed cd ends the
        script, so a line that ran at all ran at X — and X thrown away by scan time is not this
        repo's problem. Reading that newline as ambiguous would file the throwaway repo's command
        against the session's real tree, which is the false positive the `cd` model exists to end."""
        repo = _repo(tmp_path)
        gone = tmp_path / "scratchpad" / "e2"  # never created — thrown away by construction
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["set -e\nmkdir -p %s && cd %s\ngit init -q .\n"
             "git checkout -q -- . 2>/dev/null || true" % (gone, gone)],
            cwd=str(repo))
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout

    def test_set_plus_e_hands_the_conservative_reading_back(self, tmp_path):
        """`set +e` turns errexit off, and the failed cd stops carrying the lines after it."""
        repo = _repo(tmp_path)
        gone = tmp_path / "scratchpad" / "e3"
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["set -e\nset +e\ncd %s\ngit checkout -- ." % gone],
            cwd=str(repo))
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout
        assert str(repo) in res.stdout

    def test_a_failed_cd_before_an_and_is_not_a_finding(self, tmp_path):
        """`&&` runs the next command only when the cd succeeded. A target gone at scan time means
        git never ran there and never ran at the cwd either, so there is nothing to place."""
        repo = _repo(tmp_path)
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["cd %s && git checkout -- ." % (tmp_path / "nonexistent-at-scan")],
            cwd=str(repo))
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout

    def test_an_unresolvable_cd_target_reds_as_unknown(self, tmp_path):
        """`cd "$DIR"` where the command never assigned `DIR` cannot be placed statically, and
        UNKNOWN reads conservatively — the same posture as a record the gate cannot stamp."""
        root, _ = _transcript_root(
            tmp_path,
            ['cd "$DIR" && git checkout -- .'])
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout


class TestTheGateJudgesThisProjectsOwnSessions:
    """Whose sessions the gate reds on (narrowed 2026-08-18).

    The transcript root holds every session this machine ever ran, the owner's other projects among
    them, and until 2026-08-18 a `git checkout --` run in a neighbouring project refused THIS
    package's deliveries. Row 598 already ruled the other way in words — "the incident belongs to
    tlvphotos — its own session owns recovery and any repair — and live-spec holds the record alone"
    — so the gate now reds on the sessions whose recorded cwd belongs to this repository and carries
    a neighbour's finding as a notice that reds nothing.

    The narrowing is fail-safe: a session the gate cannot PLACE in another repository — a directory
    gone by scan time, a directory that is no repository at all — still reds, because row 598's
    catch and row 605's must both survive a change of scope.

    Narrowed again 2026-08-19: `cwd` is a session-WIDE field, and an owner's launch directory (a home
    directory, unplaceable in any repository) is not itself evidence the command that actually ran
    belongs to this project — the command may have `cd`ed into a real neighbouring checkout. When
    `cwd` alone answers nothing, the gate takes one further look at `effective_dir` — the directory
    `classify` already computed and already prints as `ran in` — and only reads the finding as a
    neighbour's when THAT places cleanly in a different, nameable repository. The refinement fires
    only where the `cwd` key was silent; it never overrides a `cwd` the key could place, and an
    `effective_dir` that is itself UNKNOWN or lands back in this project's own repository (a sibling
    lane worktree among them) leaves the fail-safe exactly where it stood.
    """

    COMMAND = "git checkout -- engine/assets/exhibition.js"

    @staticmethod
    def _foreign_repo(tmp_path, name="neighbour-project"):
        """A directory that is a real git repository of its OWN, the way tlvphotos is."""
        repo = tmp_path / name
        repo.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
        return repo

    @staticmethod
    def _gate_stands_in_a_repository():
        """Whether the gate's own copy has a repository to read its project key from.

        Gate b's meta-run copies this tree to a temp directory with no repository beside it. There
        the gate can place no session anywhere, so by design it keeps every finding and the two
        neighbour cases below have nothing to read. The fail-safe itself is proven by
        `test_a_session_in_no_repository_at_all_still_reds`, which needs no repository."""
        proc = subprocess.run(["git", "-C", os.path.join(ROOT, "guardrails"),
                               "rev-parse", "--git-common-dir"], capture_output=True, text=True)
        return proc.returncode == 0

    def _needs_a_repository(self):
        if not self._gate_stands_in_a_repository():
            pytest.skip("this tree carries no repository beside the gate (gate b's meta-run copies "
                        "it to a temp directory), so the gate holds no project key and keeps every "
                        "finding by design")

    @staticmethod
    def _typed_lines(res):
        return [line for line in res.stdout.splitlines()
                if line.startswith("{") and line.rstrip().endswith("}")]

    def test_a_neighbouring_projects_session_reds_nothing(self, tmp_path):
        """The whole narrowing, as one assertion: the same forbidden command, run by a session whose
        directory is another repository, no longer refuses this package's push."""
        self._needs_a_repository()
        foreign = self._foreign_repo(tmp_path)
        root, _ = _transcript_root(tmp_path / "transcripts", [self.COMMAND],
                                   project="-neighbour-project", session="s-foreign",
                                   cwd=str(foreign), answers=["ran"])
        res = _gate("--root", root)
        assert res.returncode == 0, (
            "another project's session still refuses this project's delivery:\n%s" % res.stdout)
        assert not self._typed_lines(res), (
            "a neighbour's finding still carries the blocking gate's typed line:\n%s" % res.stdout)

    def test_the_neighbours_finding_is_carried_as_a_notice_and_not_lost(self, tmp_path):
        """Narrowed, not blunted. The finding row 598 was written from — session, directory, command
        and outcome — is still on the page, so this project can still notify the one that owns it."""
        self._needs_a_repository()
        foreign = self._foreign_repo(tmp_path)
        root, _ = _transcript_root(tmp_path / "transcripts", [self.COMMAND],
                                   project="-neighbour-project", session="s-foreign",
                                   cwd=str(foreign), answers=["ran"])
        res = _gate("--root", root)
        assert "ANOTHER PROJECT'S SESSIONS" in res.stdout, (
            "the neighbour's finding was dropped instead of carried:\n%s" % res.stdout)
        for named in ("s-foreign", str(foreign), "engine/assets/exhibition.js", "RAN"):
            assert named in res.stdout, (
                "the notice never names %r, so a reader cannot write the neighbour:\n%s"
                % (named, res.stdout))

    def test_this_projects_own_session_reds_exactly_as_before(self, tmp_path):
        """The other direction. A session whose cwd is this repository's own tree reds, names its
        path and carries the typed line, which is the behaviour row 605's finding was read from."""
        root, _ = _transcript_root(tmp_path / "transcripts", [self.COMMAND],
                                   project="-this-project", session="s-ours",
                                   cwd=ROOT, answers=["ran"])
        res = _gate("--root", root)
        assert res.returncode == 1, (
            "this project's own session stopped reding — the narrowing blunted the gate:\n%s"
            % res.stdout)
        assert "engine/assets/exhibition.js" in res.stdout
        assert "outcome : RAN" in res.stdout
        assert len(self._typed_lines(res)) == 1
        assert "ANOTHER PROJECT'S SESSIONS" not in res.stdout

    def test_a_session_directory_gone_by_scan_time_still_reds(self, tmp_path):
        """Fail-safe. A worker's throwaway tree, or a lane worktree removed after the run, cannot be
        placed in any repository — and an unplaceable session reads as this project's."""
        gone = tmp_path / "removed-worktree"  # never created
        root, _ = _transcript_root(tmp_path / "transcripts", [self.COMMAND],
                                   project="-gone", session="s-gone", cwd=str(gone),
                                   answers=["ran"])
        res = _gate("--root", root)
        assert res.returncode == 1, (
            "a session the gate cannot place stopped reding, which loses findings:\n%s" % res.stdout)

    def test_a_session_in_no_repository_at_all_still_reds(self, tmp_path):
        """The same fail-safe from the other side: the directory is there and belongs to no
        repository, so nothing places it elsewhere and it reds."""
        plain = tmp_path / "not-a-repo"
        plain.mkdir()
        root, _ = _transcript_root(tmp_path / "transcripts", [self.COMMAND],
                                   project="-plain", session="s-plain", cwd=str(plain),
                                   answers=["ran"])
        res = _gate("--root", root)
        assert res.returncode == 1, res.stdout

    def test_an_unplaceable_cwd_with_a_neighbours_effective_dir_reds_nothing(self, tmp_path):
        """The shape that reached this gate on 2026-08-19: the session's recorded `cwd` is the
        owner's home directory, which no repository claims, but the command itself `cd`ed into a real
        neighbouring checkout before it ran. `cwd` alone answers nothing, so `effective_dir` gets the
        one further look the narrowing above describes, and places the command with its own project."""
        self._needs_a_repository()
        home = tmp_path / "home"  # unplaceable: exists, but no repository claims it
        home.mkdir()
        foreign = self._foreign_repo(tmp_path)
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["cd %s && %s" % (foreign, self.COMMAND)],
            project="-home", session="s-home-cd-foreign", cwd=str(home), answers=["ran"])
        res = _gate("--root", root)
        assert res.returncode == 0, (
            "an unplaceable cwd whose command actually ran in a neighbour's checkout still refused "
            "this project's delivery:\n%s" % res.stdout)
        assert "ANOTHER PROJECT'S SESSIONS" in res.stdout, (
            "the finding was dropped instead of carried as a neighbour's notice:\n%s" % res.stdout)
        assert str(foreign) in res.stdout

    def test_an_unplaceable_cwd_with_an_unknown_effective_dir_still_reds(self, tmp_path):
        """The same unplaceable `cwd`, but the command's own `cd` target cannot be read statically
        (an unassigned variable). `effective_dir` is UNKNOWN, so the one further look finds nothing to
        narrow with and the fail-safe default stands exactly as before: a worker that hid a `cd`
        behind an unreadable variable stays caught, never downgraded to a neighbour's."""
        home = tmp_path / "home"
        home.mkdir()
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ['cd "$DIR" && %s' % self.COMMAND],
            project="-home", session="s-home-cd-unknown", cwd=str(home), answers=["ran"])
        res = _gate("--root", root)
        assert res.returncode == 1, (
            "an unplaceable cwd with an UNKNOWN effective_dir stopped reding — unknown was read as "
            "foreign, which loses the catch:\n%s" % res.stdout)
        assert "ANOTHER PROJECT'S SESSIONS" not in res.stdout

    def test_an_unplaceable_cwd_with_effective_dir_in_a_sibling_worktree_still_reds(self, tmp_path):
        """The trap this narrowing must not fall into: a sibling worktree of THIS project answers
        this repository's own shared git directory, so a command that `cd`ed there from an unplaceable
        `cwd` is still this project's own session and still reds, exactly as a lane worktree always
        has."""
        self._needs_a_repository()
        lane = tmp_path / "sibling-lane"
        subprocess.run(["git", "-C", ROOT, "worktree", "add", "--detach", str(lane)],
                       check=True, capture_output=True, text=True)
        try:
            home = tmp_path / "home"
            home.mkdir()
            root, _ = _transcript_root(
                tmp_path / "transcripts",
                ["cd %s && %s" % (lane, self.COMMAND)],
                project="-home", session="s-home-cd-sibling", cwd=str(home), answers=["ran"])
            res = _gate("--root", root)
            assert res.returncode == 1, (
                "a sibling worktree of this project's own repository was read as a neighbour's, "
                "which is the trap this narrowing must not fall into:\n%s" % res.stdout)
            assert "ANOTHER PROJECT'S SESSIONS" not in res.stdout
        finally:
            subprocess.run(["git", "-C", ROOT, "worktree", "remove", "--force", str(lane)],
                           capture_output=True, text=True)

    def test_every_verdict_says_whose_sessions_it_judged(self, tmp_path):
        """A scope a reader cannot see is a scope that drifts, so both verdicts state it."""
        root, _ = _transcript_root(tmp_path / "clean", ["git status"])
        green = _gate("--root", root)
        assert green.returncode == 0, green.stdout
        assert "this project's own sessions" in green.stdout
        red_root, _ = _transcript_root(tmp_path / "red", [self.COMMAND], cwd=ROOT)
        red = _gate("--root", red_root)
        assert red.returncode == 1, red.stdout
        assert "this project's own sessions" in red.stdout


class TestGateStaysSilentOnOrdinaryWork:

    def test_a_reading_command_passes(self, tmp_path):
        root, _ = _transcript_root(tmp_path, ["git status", "git diff --stat engine/build.py"])
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout + res.stderr
        assert "OK (check-worker-restore)" in res.stdout

    def test_the_green_line_declares_its_reach(self, tmp_path):
        root, _ = _transcript_root(tmp_path, ["git status"])
        res = _gate("--root", root)
        assert "subagents/agent-*.jsonl" in res.stdout, "the green line names the files it opened"
        assert "Bash tool_use command field" in res.stdout, "and what inside them it read"

    def test_prose_naming_a_restore_is_left_alone(self, tmp_path):
        """Only a command handed to a shell counts. A grep pattern quoting the same text is silent,
        which is what keeps the gate's own tests and this pack's own prose out of its findings."""
        root, _ = _transcript_root(tmp_path, ["grep -rn 'git checkout -- ' skills/"])
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout

    def test_a_heredoc_body_quoting_the_command_is_left_alone(self, tmp_path):
        """A heredoc body is data handed to a command, not commands the shell reads. A brief written
        with `cat <<'EOF'` that carries the forbidden list is a session WRITING the rule down."""
        repo = _repo(tmp_path)
        root, _ = _transcript_root(
            tmp_path / "transcripts",
            ["cat <<'EOF' > brief.md\ngit checkout -- .\nEOF"],
            cwd=str(repo))
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout

    def test_a_quoted_script_literal_is_left_alone(self, tmp_path):
        """The same class, in the form that actually reds this gate: a reviewer's read-only probe
        passed a python script to `python3 -c "…"` and the gate cut the QUOTED script at its
        newlines, reading each of its lines as a command of its own (2026-08-05)."""
        repo = _repo(tmp_path)
        probe = ('python3 -c "\n'
                 "import sys\n"
                 "cases=[\n"
                 " ('semicolon cd','cd /tmp/aaa ; git checkout -- .'),\n"
                 " ('baseline no cd','git checkout -- .'),\n"
                 "]\n"
                 "for name,c in cases: print(name,c)\n"
                 '"')
        root, _ = _transcript_root(tmp_path / "transcripts", [probe], cwd=str(repo))
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout

    def test_unstaging_is_not_a_restore(self, tmp_path):
        """`git restore --staged` unstages and leaves the working tree untouched."""
        root, _ = _transcript_root(tmp_path, ["git restore --staged PRODUCT_SPEC.md"])
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout

    def test_reading_the_stash_is_not_taking_one(self, tmp_path):
        root, _ = _transcript_root(tmp_path, ["git stash list", "git stash show -p"])
        res = _gate("--root", root)
        assert res.returncode == 0, res.stdout


class TestAbsentAndEmptyInputs:

    def test_an_absent_transcript_root_stands_down_with_a_reason(self, tmp_path):
        missing = str(tmp_path / "no-such-projects-home")
        res = _gate("--root", missing)
        assert res.returncode == 0, res.stdout + res.stderr
        assert "STAND-DOWN" in res.stdout
        assert missing in res.stdout, "the stand-down names the root it looked for"
        assert "does not exist" in res.stdout
        assert "claims nothing" in res.stdout

    def test_a_root_holding_no_worker_run_reds_by_name(self, tmp_path):
        """An empty input set is a defect here, not a happy void (SPEC INV-218): a root that exists
        but holds no worker-run transcript means the layout the gate reads has moved, and a clean
        verdict over zero runs would protect nothing."""
        root = tmp_path / "projects"
        (root / "-Users-someone-tree").mkdir(parents=True)
        res = _gate("--root", str(root))
        assert res.returncode == 1, res.stdout
        assert "EMPTY" in res.stdout
        assert "worker-run transcripts" in res.stdout

    def test_a_window_holding_no_worker_run_is_permitted(self, tmp_path):
        """A session may spawn no worker, so an empty WINDOW reports OK and names the window."""
        root, _ = _transcript_root(tmp_path, ["git status"])
        res = _gate("--root", root, "--since-hours", "0.0001")
        assert res.returncode == 0, res.stdout
        assert "0.0001 hours" in res.stdout


class TestTheClauseStandsInEveryHome:

    @pytest.mark.parametrize("home", CLAUSE_HOMES)
    @pytest.mark.parametrize("sentence", CLAUSE_SENTENCES)
    def test_the_clause_is_present(self, home, sentence):
        assert " ".join(sentence.split()) in read_flat(home), (
            "%s no longer carries the worker-restore clause in the pack's own words (%r missing, "
            "ROADMAP row 479)" % (home, sentence))

    def test_the_five_homes_state_one_command_list(self):
        """One list across the homes and the gate. A brief that named fewer commands than the gate
        reds on is what turned a worker's obedient `git clean -fd` into a sibling lane's loss."""
        homes = CLAUSE_HOMES + ["guardrails/check-worker-restore.py", "guardrails/README.md"]
        listed = CLAUSE_SENTENCES[2]
        for home in homes:
            assert " ".join(listed.split()) in read_flat(home), (
                "%s states a command list of its own — the gate and every home carry one list"
                % home)

    def test_the_gate_reds_every_command_the_list_names(self, tmp_path):
        """The list in the prose against the list the gate holds: each form the sentence names is
        handed to the gate, and each one reds."""
        for command in list(DISCARDING.values()) + ALSO_DISCARDING:
            root, _ = _transcript_root(tmp_path / command.replace(" ", "_").replace("/", "_"),
                                       [command])
            res = _gate("--root", root)
            assert res.returncode == 1, (
                "the clause names %r and the gate passed it: %s" % (command, res.stdout))

    @pytest.mark.parametrize("home", CLAUSE_HOMES)
    def test_the_orchestrator_half_is_present(self, home):
        assert ORCHESTRATOR_HALF in read_flat(home), (
            "%s no longer carries the orchestrator's half of row 479" % home)

    def test_the_brief_stub_hands_the_clause_to_the_worker(self):
        """`scripts/open-lane.sh` is the one place the pack composes anything brief-shaped by
        machine, so the clause rides its printed stub verbatim."""
        stub = read_flat("scripts/open-lane.sh")
        assert "Copy this clause into the brief verbatim" in stub

    def test_the_gate_is_named_where_the_rule_is_stated(self):
        for home in CLAUSE_HOMES + ["guardrails/README.md"]:
            assert "check-worker-restore.py" in read_flat(home), (
                "%s states the rule and never names its mechanical arm, so a worker briefed from "
                "it cannot tell the rule is read by machine" % home)


class TestTheGateIsArmedWhereItSaysItIs:
    """The gate declares itself blocking at the verify step, and this is where that is proven.

    Two arms. The pipeline skill's verify step names the command a session runs before it accepts a
    worker's result. This suite runs the same gate against the machine's own transcript root, so a
    red reaches a person on the next suite run rather than sitting on disk.
    """

    def test_the_verify_step_names_the_command(self):
        skill = read_flat("skills/build-pipeline/SKILL.md")
        assert "python3 guardrails/check-worker-restore.py" in skill, (
            "the verify step never names the gate's command, so nothing runs it")
        assert "reads its verdict before it accepts the worker's result" in skill

    def test_the_gate_runs_against_this_machines_own_transcripts(self):
        """The real root, the session's own window. A host that keeps no transcripts where the gate
        looks stands down by name; a host that keeps them gets a verdict over real worker runs."""
        res = _gate("--since-hours", "24", counting_from=None)
        assert res.returncode == 0, (
            "a worker run since the counting start discarded working-tree changes:\n%s" % res.stdout)
        assert "STAND-DOWN" in res.stdout or "OK (check-worker-restore)" in res.stdout
        if "OK (check-worker-restore)" in res.stdout:
            assert "counting start" in res.stdout, (
                "the verdict never says how much history it read past")

    def test_the_counting_start_carries_history_and_reds_what_came_after(self, tmp_path):
        root, _ = _transcript_root(tmp_path, ["git checkout -- engine/assets/exhibition.js"])
        before = _gate("--root", root, "--counting-from", "2026-07-28")
        assert before.returncode == 0, "a run stamped 2026-07-27 red past a 2026-07-28 start"
        assert "1 finding stamped before the counting start" in before.stdout
        after = _gate("--root", root, "--counting-from", "2026-07-27")
        assert after.returncode == 1, "a run stamped on the counting start passed"

    def test_a_run_with_no_stamp_reds(self, tmp_path):
        """The gate cannot place an unstamped record in time, so it reads it as a new one."""
        runs = tmp_path / "projects" / "-Users-someone-tree" / "s-0002" / "subagents"
        runs.mkdir(parents=True)
        record = _run_record("git reset --hard HEAD")
        record.pop("timestamp")
        with open(runs / "agent-b00000000000000.jsonl", "w", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        res = _gate("--root", str(tmp_path / "projects"))
        assert res.returncode == 1, res.stdout

    def test_a_date_the_gate_cannot_read_reds_by_name(self, tmp_path):
        root, _ = _transcript_root(tmp_path, ["git status"])
        res = _gate("--root", root, "--counting-from", "last tuesday")
        assert res.returncode == 1
        assert "YYYY-MM-DD" in res.stdout
