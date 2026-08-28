"""Neither reader is allowed to silently stop finding tasks.

Commit bc6f862b replaced PLAN.md's `## Steps` section with a `## Tasks` section carrying 160
entries, and both readers kept parsing the old shape — `scripts/state-probe.sh` printed an
empty PLAN block and `scripts/render-board.sh` wrote a board with 0 tasks, on a green exit
code from both. Nothing red-flagged that: the readers just quietly found nothing. This is the
regression this file exists to catch, the next time PLAN.md's shape moves again.

Three checks, each independent of `scripts/plan_checks.py`'s own `parse_tasks()` (a fresh
regex against PLAN.md's raw text, not a re-import of the thing being tested):

  - `scripts/render-board.sh` renders every id PLAN.md's `## Tasks` section declares — no
    more, no fewer. The board shows everything (it is a page, not a chat reply), so this is
    the direct "the reader found every task" proof.
  - every id `scripts/state-probe.sh` prints is a real declared task — it never invents one.
  - the probe's own numbers add up: the tasks it shows, plus its own "N more below" count,
    plus its own "done" count, equal PLAN.md's total declared task count. The probe only
    prints the top of the list (CLAUDE.md's Canon report is capped at seven to ten lines), so
    it cannot be checked by counting printed lines the way the board can — this checks that
    its bookkeeping never drops or double-counts a task, which is what "stopped finding the
    tasks" would look like from a reader that only shows a subset.

Runs against a THROWAWAY COPY of the repo in a temp directory, following the pattern in
tests/test_plan_is_not_executable.py: never touches the real PLAN.md, never mutates the
working tree.
"""
import hashlib
import importlib.util
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT

ROOT = pathlib.Path(ROOT)

NEEDED = ("PLAN.md", "scripts/state-probe.sh", "scripts/render-board.sh", "scripts/plan_checks.py")

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

# A fresh, independent read of PLAN.md's own task-header shape — deliberately not importing
# scripts/plan_checks.py's parse_tasks(), since the point is to notice if THAT parser (and so
# both readers built on it) stops matching PLAN.md's real shape.
_DECLARED_HEADER_RE = re.compile(r"^### \S+ .+? — id: (\S+)$")

# render-board.sh's card carries its id in the meta line:
#   <div class="meta">Group · priority priority · id</div>
# "priority" can itself be two words ("quick win"), so the id is whatever sits between the
# LAST " · " and the closing tag — the lazy .*? backtracks to find that split correctly.
_BOARD_META_ID_RE = re.compile(r'<div class="meta">.*? · (\S+)</div>')

# state-probe.sh's PLAN line: "  <icon> <title>  (<id>) <verified-or-declared>[ — <reason>][  <-- NEXT]"
_PROBE_LINE_RE = re.compile(
    r"^(?:✅|🔄|⛔|⬜|👁️)\s+.+?\s+\((\S+)\)\s+(?:verified|declared)(?:\s+—\s+.+?)?(?:\s*<-- NEXT)?\s*$"
)
# state-probe.sh's summary line: "  … N more below · M done · full list in PLAN.md / board.html"
_PROBE_SUMMARY_RE = re.compile(r"… (\d+) more below · (\d+) done")


def _declared_ids(plan_text):
    ids = []
    in_section = False
    for line in plan_text.splitlines():
        if line.strip() == "## Tasks":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        m = _DECLARED_HEADER_RE.match(line.rstrip())
        if m:
            ids.append(m.group(1))
    return ids


class TestNeitherReaderStopsFindingTheTasks(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = pathlib.Path(self._tmp.name)
        for rel in NEEDED:
            dst = self.tmp / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        self.plan_text = (self.tmp / "PLAN.md").read_text(encoding="utf-8")
        self.declared = _declared_ids(self.plan_text)

    def tearDown(self):
        self._tmp.cleanup()

    def test_the_fixture_actually_declares_tasks(self):
        # A guard on the guard: if this is ever 0, every other assertion below would pass
        # vacuously (an empty set matches an empty set), which is exactly the bug this file
        # exists to catch.
        self.assertGreater(len(self.declared), 0, "PLAN.md's ## Tasks section declares no tasks")
        self.assertEqual(
            len(self.declared), len(set(self.declared)),
            "PLAN.md declares the same task id more than once",
        )

    def test_board_renders_every_declared_id_and_no_others(self):
        out = self.tmp / "board.html"
        r = subprocess.run(
            ["bash", str(self.tmp / "scripts" / "render-board.sh"), str(out)],
            cwd=str(self.tmp), capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, "render-board.sh failed: " + r.stdout + r.stderr)
        rendered_ids = _BOARD_META_ID_RE.findall(out.read_text(encoding="utf-8"))
        self.assertTrue(rendered_ids, "the board rendered no task ids — its meta markup "
                                       "changed; update _BOARD_META_ID_RE")
        declared_set, rendered_set = set(self.declared), set(rendered_ids)
        self.assertEqual(
            declared_set, rendered_set,
            "the board and PLAN.md disagree on which tasks exist — missing from the board: "
            "%r; on the board but not declared: %r"
            % (sorted(declared_set - rendered_set), sorted(rendered_set - declared_set)),
        )
        self.assertEqual(
            len(self.declared), len(rendered_ids),
            "the board rendered a different NUMBER of task cards than PLAN.md declares tasks",
        )

    def _run_probe(self):
        r = subprocess.run(
            ["bash", str(self.tmp / "scripts" / "state-probe.sh")],
            cwd=str(self.tmp), capture_output=True, text=True,
        )
        return _ANSI_RE.sub("", r.stdout)

    def test_probe_never_prints_an_id_plan_md_does_not_declare(self):
        plain = self._run_probe()
        shown_ids = [
            m.group(1) for line in plain.splitlines()
            if (m := _PROBE_LINE_RE.match(line.strip()))
        ]
        self.assertTrue(shown_ids, "the probe printed no task ids — its PLAN-section print "
                                    "shape changed; update _PROBE_LINE_RE")
        unknown = set(shown_ids) - set(self.declared)
        self.assertFalse(unknown, "the probe printed id(s) PLAN.md never declared: %r" % sorted(unknown))

    def test_probe_summary_accounts_for_every_declared_task(self):
        plain = self._run_probe()
        shown_ids = {
            m.group(1) for line in plain.splitlines()
            if (m := _PROBE_LINE_RE.match(line.strip()))
        }
        m = _PROBE_SUMMARY_RE.search(plain)
        self.assertIsNotNone(
            m, "the probe printed no summary line — a person can no longer see how much is "
               "left below or how much is done",
        )
        more_below, done = int(m.group(1)), int(m.group(2))
        self.assertEqual(
            len(shown_ids) + more_below + done, len(self.declared),
            "shown (%d) + more-below (%d) + done (%d) = %d, but PLAN.md declares %d tasks — "
            "the probe silently lost or double-counted some"
            % (len(shown_ids), more_below, done, len(shown_ids) + more_below + done, len(self.declared)),
        )


def _shell_reader():
    """The one in-repo reader of shell text, borrowed from the worker-restore guard.

    "Which programs does this shell text actually run" is one question with one answer, and the
    guard at `hooks/worker-restore-guard.py` already answers it: it strips shell grouping, the
    `command`/`sudo`/`env` wrappers and the launchers, keeps quoted spans as the data they are,
    and finds the text a segment carries inside it. A second reader written here would drift from
    that one the day after it was written, and the drift would show up as this guard quietly
    passing something the other refuses.
    """
    path = ROOT / "hooks" / "worker-restore-guard.py"
    spec = importlib.util.spec_from_file_location("worker_restore_guard_reader", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestTheAcceptanceCommandsStayHonestMachinery(unittest.TestCase):
    """The acceptance-command table is machinery that runs at every session start, everywhere.

    `scripts/plan_checks.py`'s CHECKS map is read by both readers and executed by the probe,
    which is the first command a session runs on any machine that opens this project. Two
    properties keep that from turning into a cost nobody asked for, and neither is guarded by
    the tests above, which look only at what the readers print.

    Both were written 2026-08-28 with plan-10's own thirteen keys, and both name a thing that
    already happened here. A key outliving its row is the first: plan-1's key survived its task
    into the 28.08 board rotation and had to be removed by hand, still running every morning
    against a step that no longer existed. A key that writes is the second: PLAN.md's own trap
    list records `tests/test_guardrails.py` leaving a `git stash` unrestored on an interrupt,
    and a resume step that can do the same to a person's uncommitted work would be the worst
    possible place for it.

    The writing check first shipped the same day as a search for nineteen verbs over the command
    text with single-quoted spans cut out first. Both halves of that were wrong. Cutting the
    quoted spans hid every payload a check hands to a shell, so `bash -c 'rm -rf …'` read as the
    two words `bash -c`; and searching raw text for verbs cannot tell a program from a grep
    pattern, which is why the spans were being cut in the first place. Fourteen of fifteen
    destructive forms walked through, output redirection — the very class the restore guard closed
    that same day — not even on the list. What the command RUNS is a question about its shape, so
    it is now read as shell rather than searched as text (2026-08-28, the adversarial review of
    the day's range).
    """

    #: Programs that change the tree or the machine. A check exists to READ state.
    WRITING_PROGRAMS = frozenset((
        "rm", "rmdir", "unlink", "mv", "cp", "truncate", "shred", "tee", "install",
        "chmod", "chown", "chgrp", "touch", "ln", "mkdir", "mkfifo", "mknod", "dd",
        "patch", "kill", "pkill", "killall",
    ))

    #: git subcommands that move the tree, the index, the refs or the object store. A check has no
    #: business running any of them; reading history (`log`, `ls-files`, `rev-parse`) is free.
    WRITING_GIT = frozenset((
        "stash", "checkout", "switch", "restore", "reset", "clean", "commit", "add", "rm", "mv",
        "push", "pull", "fetch", "merge", "rebase", "cherry-pick", "revert", "apply", "am",
        "branch", "tag", "worktree", "gc", "prune", "init", "clone", "submodule", "notes",
        "config", "update-ref", "update-index", "checkout-index", "write-tree", "repack",
    ))

    #: Editors told to rewrite the file they are reading.
    IN_PLACE_PROGRAMS = frozenset(("sed", "perl", "ruby", "gsed"))

    #: One check hands a whole program in another language to an interpreter. This reader cannot
    #: judge what that program does, so it refuses every one of them — with the single exception
    #: recorded below, pinned by the exact bytes of the command it excuses.
    #:
    #: plan-11's check renders the board's own coverage in Python, opens PLAN.md and board.html to
    #: read them, and writes nothing. Refusing it would not make it judgeable: the only way to
    #: quiet this guard would be to move the payload into a script file, where this reader sees
    #: nothing at all instead of seeing it and standing down. So the payload is judged by hand,
    #: once, and pinned by hash — any edit to that command reds this test and asks for the
    #: judgement again (2026-08-28).
    JUDGED_BY_HAND = {
        "plan-11": "247911fbb4cced36d84b17491ca9c44ddd032d1707e33b3ac007b871c7608389",
    }

    def setUp(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_checks import CHECKS
        self.checks = CHECKS
        self.declared = set(_declared_ids((ROOT / "PLAN.md").read_text(encoding="utf-8")))
        self.shell = _shell_reader()

    # ---- reading one command as shell ----------------------------------------------------------
    def _writing_acts(self, command, depth=0):
        """Every way this command changes state, named in the words of the command itself."""
        found = []
        if depth > 3:
            return ["nesting this reader stops following"]
        for stages in self.shell._pipelines(command):
            for segment in stages:
                found.extend(self._segment_writing_acts(segment, depth))
        return found

    def _segment_writing_acts(self, segment, depth):
        found = []
        for target in self.shell._truncating_redirect_targets(segment):
            if not target.startswith("/dev/"):
                found.append("a redirect that writes `%s`" % target)
        if re.search(r"(?<![\w>])>>\s*(?!/dev/)\S", segment):
            found.append("an append redirect")
        tokens = self.shell._command_tokens(segment)
        if not tokens:
            return found
        program = tokens[0].rsplit("/", 1)[-1]
        args = tokens[1:]
        if program in self.WRITING_PROGRAMS:
            found.append("the program `%s`" % program)
        if program == "git":
            git_args = self.shell._git_args(segment) or []
            subcommand = next((a for a in git_args if not a.startswith("-")), "")
            if subcommand in self.WRITING_GIT:
                found.append("`git %s`" % subcommand)
        if program in self.IN_PLACE_PROGRAMS and any(
                a == "--in-place" or a.startswith("--in-place=") or
                (a.startswith("-") and not a.startswith("--") and "i" in a) for a in args):
            found.append("`%s` rewriting a file in place" % program)
        payload = self.shell._shell_payload(segment)
        if payload is not None:
            found.extend(self._writing_acts(payload, depth + 1))
        elif any(a in self.shell._inline_program_flags(program) for a in args):
            found.append("`%s` running a whole program this reader cannot judge" % program)
        for inner in self.shell._substitutions(segment):
            found.extend(self._writing_acts(inner, depth + 1))
        if program in ("find", "gfind"):
            for inner in self.shell._find_exec_commands(args):
                found.extend(self._writing_acts(inner, depth + 1))
        return found

    def test_the_fixture_actually_carries_checks(self):
        # The same guard-on-the-guard the class above keeps: an empty table would pass both
        # assertions below without reading anything.
        self.assertGreater(len(self.checks), 0, "scripts/plan_checks.py declares no checks")
        self.assertGreater(len(self.declared), 0, "PLAN.md's ## Tasks section declares no tasks")

    def test_every_key_names_a_task_the_plan_declares(self):
        orphans = sorted(set(self.checks) - self.declared)
        self.assertEqual(
            orphans, [],
            "scripts/plan_checks.py runs a command for %s, which PLAN.md's ## Tasks section no "
            "longer declares — the row was renamed, folded or archived and its command was left "
            "behind, running at every session start against nothing" % orphans,
        )

    def test_no_check_can_write_to_the_tree_or_the_machine(self):
        # Nothing is cut out of the command first. A grep's PATTERN stays where it is and stays
        # harmless, because it is read as an argument to grep rather than as a word that might be
        # a verb: "…run at every push" is a sentence in a skill file, and a shell reader can see
        # that it is one.
        for task_id, raw in sorted(self.checks.items()):
            if task_id in self.JUDGED_BY_HAND:
                continue
            acts = self._writing_acts(raw)
            self.assertEqual(
                acts, [],
                "the check for %s carries %s, and a check exists to read state, never to change "
                "it — this one runs on every machine that opens this project, before anyone has "
                "decided anything. The command: %r" % (task_id, "; ".join(acts), raw),
            )

    def test_a_hand_judged_payload_is_still_the_command_that_was_judged(self):
        """An exception recorded once must not quietly cover a command that has since changed."""
        for task_id, pinned in sorted(self.JUDGED_BY_HAND.items()):
            self.assertIn(
                task_id, self.checks,
                "%s carries a hand-judged exception and no longer exists — drop the pin" % task_id,
            )
            here = hashlib.sha256(self.checks[task_id].encode("utf-8")).hexdigest()
            self.assertEqual(
                here, pinned,
                "%s's check was judged by hand once, because it hands a whole program in another "
                "language to an interpreter and this reader cannot follow it. That command has "
                "changed since. Read it again, confirm it still only reads state, then update the "
                "pin to %s. The command: %r" % (task_id, here, self.checks[task_id]),
            )

    def test_the_writing_guard_catches_the_forms_that_used_to_walk_through(self):
        """The guard on the guard: every shape the text search of 2026-08-28 let past.

        Fourteen of these fifteen passed the first version of this check, which cut single-quoted
        spans out of the command and then searched what was left for nineteen verbs. They are kept
        here so a future rewrite of the reading cannot lose them again one at a time.
        """
        destructive = [
            "bash -c 'rm -rf /tmp/victim'",
            "sh -c \"git reset --hard\"",
            "echo x > PLAN.md",
            "echo x >> PLAN.md",
            "sed -i '' 's/a/b/' PLAN.md",
            "dd if=/dev/zero of=PLAN.md",
            "git worktree remove ../w",
            "git branch -D main",
            "git gc --prune=now",
            "touch NEW_FILE",
            "ln -sf /etc/passwd here",
            "mkdir -p /tmp/x",
            "rm -rf /tmp/victim",
            "python3 -c 'open(\"PLAN.md\",\"w\")'",
            "find . -name '*.pyc' -exec rm {} \\;",
            "( cd tests && git checkout -- conftest.py )",
            "timeout 5 git stash",
            "printf x | tee PLAN.md",
        ]
        for command in destructive:
            self.assertNotEqual(
                self._writing_acts(command), [],
                "the writing guard passes %r, and a check running that would change the tree "
                "at every session start" % command,
            )

    def test_the_writing_guard_leaves_an_ordinary_reading_check_alone(self):
        """A guard that reds a plain grep would be turned off within the week."""
        reading = [
            "test -f PLAN.md && test -x scripts/plan-step.sh",
            "grep -q 'doc- and code-compaction stations run at every push' tests/x.py",
            "grep -q 'the row was added and then reset' docs/notes.md",
            "bash guardrails/check-config-health.sh >/dev/null 2>&1",
            "python3 scripts/director-wire-report.py >/dev/null 2>&1",
            "test \"$(git log -1 --format=%ct -- evals)\" -ge 0",
            "ls ~/tlvphotos/.claude/skills 2>/dev/null | grep -q director",
            "test -z \"$(git ls-files prototype)\"",
            "cmp -s a b && grep -q worker-restore \"$HOME/.claude/settings.json\"",
        ]
        for command in reading:
            self.assertEqual(
                self._writing_acts(command), [],
                "the writing guard reds %r, which only reads state" % command,
            )


if __name__ == "__main__":
    unittest.main()
