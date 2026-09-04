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

NEEDED = ("PLAN.md", "scripts/state-probe.sh", "scripts/render-board.sh",
          "scripts/plan_checks.py", "scripts/plan_checks_core.py")

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

# state-probe.sh's PLAN line: "  <id> <icon> <title>  <verified-or-declared>[ — <reason>][  <-- NEXT]"
# The id leads the line, padded to the widest id PLAN.md declares, ahead of its state mark and
# its title (his word, 02.09 — it used to trail at the end in parentheses).
_PROBE_LINE_RE = re.compile(
    # The tag after the title is one of three: `verified` where a command proved the mark,
    # `declared` where the row carries no command, and `marked done` where the row's own command
    # CONTRADICTS its done mark. The third joined the other two on 2026-08-28, when the probe
    # stopped calling such a row verified; reading only the first two dropped every one of those
    # lines from the count, and the accounting below then reported tasks lost that were sitting
    # on the screen.
    r"^(\S+)\s+(✅|🔄|🔁|⛔|⬜)\s+.+?\s+(?:verified|declared|marked done)"
    r"(?:\s+—\s+.+?)?(?:\s*<-- NEXT)?\s*$"
)
# state-probe.sh's summary line: "  … N open · M more below · full list in PLAN.md / board.html"
# No figure for finished work since 02.09, on his word: a running total only grows, and it needs a
# window nobody agreed on to mean anything. What the line owes a reader is what is still open, and
# how much of that sits below the printed rows. Rows closed since the last push get their own ✅
# lines above instead.
_PROBE_SUMMARY_RE = re.compile(r"… (\d+) open · (\d+) more below")


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
        shown = [
            m for line in plain.splitlines()
            if (m := _PROBE_LINE_RE.match(line.strip()))
        ]
        shown_open = len([m for m in shown if m.group(2) != "✅"])
        m = _PROBE_SUMMARY_RE.search(plain)
        self.assertIsNotNone(
            m, "the probe printed no summary line — a person can no longer see how much is "
               "open, or how much of it is left below the printed rows",
        )
        open_count, more_below = int(m.group(1)), int(m.group(2))
        self.assertEqual(
            shown_open + more_below, open_count,
            "printed open rows (%d) + more-below (%d) = %d, but the line says %d are open — the "
            "probe silently lost or double-counted some"
            % (shown_open, more_below, shown_open + more_below, open_count),
        )
        self.assertTrue(
            0 < open_count <= len(self.declared),
            "the open count (%d) is outside what PLAN.md declares (%d rows)"
            % (open_count, len(self.declared)),
        )
        # Every printed row is a row PLAN.md declares, and each appears once. The summary line
        # stopped carrying a done figure on 02.09, so the old exact accounting — shown +
        # more-below + done == declared — has no done term to close it any more. What the output
        # still proves is stated here in full, so the narrowing is visible rather than silent: the
        # printed ids are declared ids, none repeats, the open arithmetic closes, and the rows
        # printed as done cannot outnumber the rows that are not open.
        printed_ids = [m.group(1) for m in shown]
        self.assertEqual(len(printed_ids), len(set(printed_ids)),
                         "the probe printed a row twice: %s" % printed_ids)
        undeclared = [i for i in printed_ids if i not in self.declared]
        self.assertEqual(undeclared, [],
                         "the probe printed rows PLAN.md does not declare: %s" % undeclared)
        printed_done = len([m for m in shown if m.group(2) == "✅"])
        self.assertLessEqual(
            printed_done, len(self.declared) - open_count,
            "the probe printed %d done rows, more than the %d rows that are not open"
            % (printed_done, len(self.declared) - open_count),
        )


class TestADoneLineNamesARealClose(unittest.TestCase):
    """Every done line the probe prints stands for a row this branch actually closed.

    The fixture the other probe tests use is a throwaway copy with no `.git`, so the arm that
    reads the branch's upstream cannot run there and every assertion about done lines passes
    vacuously — printed_done is structurally zero (product-prover, 2026-09-02, finding 8). This
    one runs the probe in the real repository and re-derives the set independently: a printed
    done line is owed only where the row's hand mark is done now and was not done at the
    upstream. Where no upstream is reachable, no done line is owed at all.
    """

    def test_every_printed_done_row_flipped_since_the_upstream(self):
        import subprocess
        r = subprocess.run(["bash", str(ROOT / "scripts" / "state-probe.sh")],
                           cwd=str(ROOT), capture_output=True, text=True)
        plain = _ANSI_RE.sub("", r.stdout)
        printed_done = {
            m.group(1) for line in plain.splitlines()
            if (m := _PROBE_LINE_RE.match(line.strip())) and m.group(2) == "✅"
        }

        up = subprocess.run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
                            cwd=str(ROOT), capture_output=True, text=True)
        if up.returncode != 0 or not up.stdout.strip():
            self.assertEqual(printed_done, set(),
                             "no upstream is reachable, so no done line is owed: %s" % printed_done)
            return
        base = subprocess.run(["git", "show", "%s:PLAN.md" % up.stdout.strip()],
                              cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(base.returncode, 0, "could not read PLAN.md at the upstream")

        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_checks import parse_tasks
        done_at_push = {t["id"] for t in parse_tasks(base.stdout) if t["mark"] == "✅"}
        done_now = {t["id"] for t in parse_tasks((ROOT / "PLAN.md").read_text(encoding="utf-8"))
                    if t["mark"] == "✅"}
        owed = done_now - done_at_push

        stale = sorted(printed_done - owed)
        self.assertEqual(stale, [],
                         "the probe printed a done line for a row that did not close on this "
                         "branch: %s" % stale)


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
    #:
    #: plan-10's second pass (2026-09-01) added five more, each for the same reason: the row's own
    #: acceptance is proven by a specific pytest-style test function or method that takes no
    #: repository state as an argument beyond a scratch directory, and calling it directly is
    #: cheaper and more honest than re-deriving its assertions in shell. Each payload was read by
    #: hand before being pinned: every one imports a named test module from `tests/`, calls one or
    #: more of its own functions with nothing but a `tempfile.TemporaryDirectory()` (cleaned up in
    #: the same command, never left behind), and writes nothing under this repository's own tree.
    #: q-490 calls every `test_*` function in `tests/test_legibility_floor.py` (none take
    #: arguments). q-497 calls one `test_authority_anchor.py` function. q-527 calls one
    #: `test_worker_restore_made_good.py` function. q-581 calls `test_dialog_warning_guard.py`'s
    #: own functions over its own `KNOWN_EXAMPLES`/`ORDINARY` lists, read from the module itself,
    #: not retyped here. q-586 instantiates one `test_worker_restore.py` class and calls its
    #: methods over its own `DISCARDING`/`ALSO_DISCARDING` lists, same reason.
    JUDGED_BY_HAND = {
        "plan-11": "247911fbb4cced36d84b17491ca9c44ddd032d1707e33b3ac007b871c7608389",
        "q-490": "02244009b044657f265468334bb7c179090898dd78ef3d4767b5d6615bdfa506",
        "q-497": "a08acac50d8a277eee4202614b8140b76ffa4cb75c0b59e4365b91739c16624a",
        "q-527": "1c84c8e5a9271225666cfe832690345752a4b6cf25b30815193684286fd9794b",
        "q-581": "59fce43e95d4d4ae51534ed5c41d81d9d634555a27ac4ac416c6c79f5ce17ce3",
        "q-586": "25b2c366f1344f69057673bcc5a229410f688fc51951eea4f09313973bf8d3bf",
        #: q-805 (2026-09-02) chains file-absence tests, greps, `git show ... | diff`, and one
        #: `python3 -c` one-liner and one `spec-redundancy-precheck.py` call, each read by hand:
        #: the inline script only does `json.load(open(...))` and `sys.exit`, no write; the
        #: precheck script (checked directly: no `open(..., "w")`, no `.write()` beyond a usage
        #: line to stderr) only prints candidate pairs, piped into `grep -q`, itself read-only.
        #: Re-read and re-pinned 2026-09-04: the clause that compared the whole of
        #: spec/success-measure-feed.md against an old commit read as a freeze on a live spec
        #: chapter, and went red when q-48 added three real criteria to it. It now greps the two
        #: restored sentences the row actually promises. The `python3 -c` one-liner and the
        #: precheck call are unchanged and were read again: still `json.load(open(...))` and
        #: `sys.exit`, still a print piped into `grep -q`, no write on either road.
        "q-805": "f18d440939b934df429369e527ac9069fd2c5de118729e62df35e936fc8a7bfb",
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
        for target in self.shell._append_redirect_targets(segment):
            # Read as shell, like every other arm here. This was a raw regex over the segment
            # until 2026-08-28, so a `>>` inside a quoted span counted: `grep -q 'a >> b' notes.md`
            # was flagged as writing, which is the very grep-pattern false positive the shell
            # reader was adopted to end.
            if not target.startswith("/dev/"):
                found.append("an append redirect onto `%s`" % target)
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
        """The guard on the guard: every shape a reading of this table has let past so far.

        Most of these passed the first version of this check, which cut single-quoted spans out of
        the command and then searched what was left for nineteen verbs. The last group passed the
        shell reader that replaced it, until the adversarial read of 2026-08-28 evening found them
        in the reader itself. They are kept here so a future rewrite cannot lose them again one at
        a time. (The count that stood in this line named fifteen over a list of eighteen; a record
        of what was proven has to be able to count what it holds.)
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
            # Found in the shell reader itself, 2026-08-28 evening, and repaired there so both
            # readers gained them at once.
            "eval 'rm -rf /tmp/victim'",
            "bash -lc 'rm -rf /tmp/victim'",
            "bash -cx 'git reset --hard'",
            "echo starting & rm -rf /tmp/victim",
            "echo starting |& rm -rf /tmp/victim",
            "cp <(git show HEAD:PLAN.md) PLAN.md",
        ]
        for command in destructive:
            self.assertNotEqual(
                self._writing_acts(command), [],
                "the writing guard passes %r, and a check running that would change the tree "
                "at every session start" % command,
            )

    def test_the_writing_guard_leaves_a_reading_command_alone(self):
        """The other direction: a check that only reads must not be named as writing.

        A guard that reds honest work gets switched off, taking the real catches with it. The
        append arm was a raw regex over the command text until 2026-08-28 evening, so a check
        greping for the two characters `>>` was called a write.
        """
        harmless = [
            "grep -q 'a >> b' PLAN.md",
            "grep -q 'rm -rf' docs/language-rules.md",
            "test -f PLAN.md && grep -c '^### ' PLAN.md",
            "git log -1 --format=%ct -- PLAN.md",
            "bash -lc 'grep -q needle PLAN.md'",
            "python3 scripts/director-wire-report.py >/dev/null 2>&1",
            "ls ~/tlvphotos/.claude/skills 2>/dev/null | grep -q director",
        ]
        for command in harmless:
            self.assertEqual(
                self._writing_acts(command), [],
                "the writing guard calls %r a write, and a guard that reds honest work is a "
                "guard somebody turns off" % command,
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
