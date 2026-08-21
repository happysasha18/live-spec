"""A deletion-only push stands the whole gate chain down (SPEC INV-290, ROADMAP row 502).

Alexander deleted four retired tags on 2026-07-27 ~18:05; the pre-push chain fired, read an empty
diff, fell through to the full suite, and his command died on its own two-minute limit. git feeds a
pre-push hook one line per ref update on stdin: `<local ref> <local sha> <remote ref> <remote
sha>` (githooks(5)). A deletion carries the all-zero object id as its LOCAL sha (verified against a
real `git push --delete` run, 2026-07-27) — the local ref field reads the literal "(delete)", which
the checker does not rely on.

Two layers are tested: `guardrails/check-deletion-only-push.sh` in isolation (the real script, real
subprocess runs, fast and deterministic), and `guardrails/pre-push` end to end — fed real stdin
through a real subprocess, bounded by a short timeout so a content push's test never waits for the
full suite it is proving untouched. The proof covers both directions: a deletion-only push stands
the chain down, a content push runs it exactly as before.
"""

import os
import re
import shutil
import signal
import subprocess
import tempfile
import unittest

from conftest import ROOT, SUITE_TEMP_PREFIXES, read

GUARDRAILS = os.path.join(ROOT, "guardrails")
CHECKER = os.path.join(GUARDRAILS, "check-deletion-only-push.sh")
PREPUSH = os.path.join(GUARDRAILS, "pre-push")

ZERO_SHA = "0" * 40
NONZERO_SHA = "1" * 40

DELETION_STDIN = (
    "(delete) %s refs/tags/v1 2611efa10c9b72d1bcae112da5bd787aeb178aba\n"
    "(delete) %s refs/tags/v2 2611efa10c9b72d1bcae112da5bd787aeb178aba\n"
) % (ZERO_SHA, ZERO_SHA)

CONTENT_STDIN = (
    "refs/heads/lane/502-probe %s refs/heads/lane/502-probe %s\n"
) % (NONZERO_SHA, ZERO_SHA)

MIXED_STDIN = DELETION_STDIN + CONTENT_STDIN


def run(args, *, cwd, extra_env=None, **kwargs):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, env=env, **kwargs
    )


# Row 574's deeper finding: guardrails/check-tests.sh, called bare (no SCOPED_TEST_FILES, no
# scratch argument — the branch a content push falls to below), runs the real suite as a nested
# pytest process with no marker distinguishing it from a top-level run. That nested run reaches
# this very class again and, with LIVE_SPEC_SCRATCH unset (this is the real tree, not the git-less
# scratch copy setUp already carves out), does not skip — it calls run_bounded a second time, and
# that inner call's own start_new_session=True hands its child a BRAND NEW process group, detached
# from the outer run's. The outer kill below reaches only its own group, so a nested pre-push that
# is still inside its own timeout window when the outer one fires keeps running, orphaned, past the
# point where this file's own cleanup already swept — a live instance of "a worker's completion can
# orphan a runaway child" (this pack's own prior finding). The env marker below is read by setUp:
# a nested invocation skips itself rather than racing a second, unguarded kill window.
NESTED_MARKER = "LIVE_SPEC_NESTED_PREPUSH_KILL_TEST"


def run_bounded(args, input_text, timeout):
    """Run a possibly-long-lived process, killing its WHOLE process group on timeout (never just
    the direct child) so a real gate chain that spawns check-tests.sh/pytest is never left running
    as an orphan after the test returns (base rule: cleanup scopes to what the run provably owns).
    The child's env carries NESTED_MARKER so that if the chain it spawns loops back into THIS test
    class (a bare check-tests.sh run reaches the real suite, which reaches this file again), the
    inner instance recognises it is already nested and skips rather than opening a second,
    unguarded process group the outer kill cannot reach.
    Returns (returncode_or_None, combined_stdout). None means it was killed on timeout."""
    env = dict(os.environ)
    env[NESTED_MARKER] = "1"
    proc = subprocess.Popen(
        args, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, start_new_session=True, env=env,
    )
    try:
        out, _ = proc.communicate(input=input_text, timeout=timeout)
        return proc.returncode, out
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _ = proc.communicate()
        return None, out


class _CleansSuiteLogLeaks(object):
    """A bounded kill (run_bounded below, SIGKILL, uncatchable) can land at any point inside the
    real chain this test deliberately spawns: check-tests.sh mktemps its own
    livespec-test-suite-log.* file the instant it starts, and — on the reach map's conservative
    branch — goes on to run the real, full suite as a nested pytest process, which is itself
    mid-way through creating and cleaning up other suite tests' own temp artifacts (row 574: an
    agent-inbox test's per-test temp dir was the one a sweep scoped to the log file alone left
    behind, since a kill this test throws on purpose can catch whichever artifact any suite test
    happens to hold open, not only the one file this class's cleanup used to know by name).
    Scoped cleanup by the suite's own prefix rule (conftest.py's SUITE_TEMP_PREFIXES — the same
    rule the session-end leak check reads) rather than one hardcoded pattern: every entry new
    since this test's own run started, file or directory alike."""

    def _before(self):
        return set(os.listdir(tempfile.gettempdir()))

    def _ours(self, names):
        return {n for n in names if n.startswith(SUITE_TEMP_PREFIXES)}

    def _clean_new(self, before):
        tmp = tempfile.gettempdir()
        after = set(os.listdir(tmp))
        for name in self._ours(after) - self._ours(before):
            path = os.path.join(tmp, name)
            if os.path.isdir(path) and not os.path.islink(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                try:
                    os.remove(path)
                except OSError:
                    pass


class TestCheckerScriptShips(unittest.TestCase):
    def test_script_ships_and_is_executable(self):
        self.assertTrue(os.path.isfile(CHECKER), "guardrails/check-deletion-only-push.sh missing")
        self.assertTrue(os.access(CHECKER, os.X_OK), "check-deletion-only-push.sh not executable")


class TestR226DoesNotContradictItself(unittest.TestCase):
    """M6: R226.6 once read "at every push, never scoped", stated as a universal over every push;
    R226.7 names a push where none of those five checks runs at all — the deletion-only stand-down
    this file proves. The two sat eight lines apart under adjacent case headings and could not both
    hold; the code holds 7 (the stand-down block sits above `fail=0` in `guardrails/pre-push`, so a
    deletion-only push never reaches the five checks criterion 6 names). Criterion 6 must carry its
    one exception by name rather than read as an unscoped universal a reader of INV-40 could
    believe."""

    def _requirement_226_body(self):
        spec = read("PRODUCT_SPEC.md")
        m = re.search(r"\n## Requirement 226:.*?(?=\n## )", spec, re.S)
        self.assertTrue(m, "PRODUCT_SPEC.md carries no Requirement 226")
        return m.group(0)

    # Each exception criterion 6 is allowed to name, and the mechanism that must exist for the
    # name to mean anything: the phrase a reader would find, then the file and the pattern that
    # proves the mechanism is real. A criterion-6 exception this map cannot resolve is the
    # finding — either the spec names a stand-down nothing implements, or a real stand-down
    # arrived and nobody taught this test about it.
    EXCEPTION_MECHANISMS = {
        "deletion-only": ("PRODUCT_SPEC.md", r"\n7\. \*when\* every ref-update line"),
        "inbox": ("guardrails/check-prover-record.sh", r"exactly one new inbox/ file"),
        "recordless": (".live-spec/agent.md", r"earns no record"),
        "case-or-space": ("guardrails/case_or_space_only.py", r"case-or-space carve-out"),
    }

    # The files that implement a stand-down criterion 6 must name: gate a's own script, and the
    # pre-push block that stands the whole chain — gate a included — down ahead of it.
    STAND_DOWN_SOURCES = ("guardrails/check-prover-record.sh", "guardrails/pre-push")
    STAND_DOWN_MARKER = re.compile(r"^\s*#\s*STAND-DOWN:\s*(\S+)\s*$", re.M)

    def _criterion_6(self):
        body = self._requirement_226_body()
        m6 = re.search(r"\n6\. (.*)", body)
        self.assertTrue(m6, "Requirement 226 carries no criterion 6")
        return m6.group(1)

    def _named_exceptions(self, text):
        """The exception list criterion 6 actually carries, parsed — not a substring guess.

        A vacuous substring assertion ("does the word deletion-only appear anywhere") passes a
        criterion that has silently grown a second, unnamed exception. This reads the clause
        after `except`, drops any lead-in before its colon and the trailing anchor, and splits
        the list into the items a reader would count.
        """
        m = re.search(r"\bexcept\b(.*)$", text)
        if not m:
            return []
        clause = m.group(1).split("[INV")[0]
        if ":" in clause:
            clause = clause.split(":", 1)[1]
        parts = re.split(r";|\band\b", clause)
        return [p.strip(" .,;") for p in parts if p.strip(" .,;")]

    def test_criterion_6_no_longer_reads_as_an_unscoped_universal(self):
        body = self._requirement_226_body()
        self.assertNotIn("at every push, never scoped", body,
                          "criterion 6 still reads as a universal R226.7 falsifies")

    def test_criterion_6_scopes_itself_to_a_push_that_carries_content(self):
        self.assertIn("carries content", self._criterion_6(),
                       "criterion 6 does not scope itself to a push that carries content")

    def test_every_exception_criterion_6_names_has_a_real_mechanism(self):
        """The teeth: each named exception resolves to a mechanism that exists on disk, and an
        exception this map cannot name reds rather than passing unread."""
        named = self._named_exceptions(self._criterion_6())
        self.assertTrue(named, "criterion 6 names no exception at all, yet R226.7 is one")
        for item in named:
            key = next((k for k in self.EXCEPTION_MECHANISMS if k in item), None)
            self.assertIsNotNone(
                key,
                "criterion 6 names an exception this test cannot resolve to a mechanism: %r. "
                "Either the spec names a stand-down nothing implements, or a real stand-down "
                "arrived and this map was not taught it." % item)
            path, pattern = self.EXCEPTION_MECHANISMS[key]
            self.assertRegex(read(path), pattern,
                             "criterion 6 names the %s exception, but %s carries no mechanism "
                             "for it" % (key, path))

    def _implemented_stand_downs(self):
        """Every stand-down the CODE implements, read off the `# STAND-DOWN: <name>` markers.

        The convention is stated in guardrails/check-prover-record.sh's header: an arm that can
        let a push past the prover-record demand carries one such line above it. Reading the
        markers is the point — the test that stood here read a hand-written proxy instead (does
        gate a's block in pre-push contain the word `case`), so it held nothing about the script
        the block calls. Gate a's stand-downs live inside check-prover-record.sh, and the whole
        chain's deletion-only stand-down lives in pre-push above it; both are read.
        """
        found = {}
        for rel in self.STAND_DOWN_SOURCES:
            for name in self.STAND_DOWN_MARKER.findall(read(rel)):
                found.setdefault(name, rel)
        return found

    def test_gate_a_carries_no_stand_down_criterion_6_does_not_name(self):
        """The other direction, and the reason `2718c69` was reverted: gate a once skipped the
        prover record on the prose-only and scoped reach verdicts — a third exception no
        criterion named. This reads the implemented stand-downs off the scripts themselves and
        holds the two lists equal in both directions: every mechanism the code implements is
        named by criterion 6, and every exception criterion 6 names has a mechanism behind it.
        An arm added without its marker reds against the marker convention; an arm added with a
        marker criterion 6 does not name reds here; a clause deleted from criterion 6 while its
        arm still stands in the code reds here too."""
        implemented = self._implemented_stand_downs()
        self.assertTrue(
            implemented,
            "no `# STAND-DOWN: <name>` marker anywhere in %s — either the stand-down arms lost "
            "their markers, or the convention this test reads was dropped from the scripts"
            % ", ".join(self.STAND_DOWN_SOURCES))

        criterion_6 = self._criterion_6()
        for name, rel in sorted(implemented.items()):
            self.assertIn(
                name, criterion_6,
                "%s implements a stand-down named %r that R226 criterion 6 does not name: a "
                "push can pass the prover-record gate for a reason the spec never states. "
                "Name it in criterion 6, or take the arm out." % (rel, name))

        for item in self._named_exceptions(criterion_6):
            self.assertTrue(
                any(name in item for name in implemented),
                "criterion 6 names an exception no marked stand-down implements: %r. The "
                "implemented ones are %s. Either the spec grants an exception nothing in the "
                "code performs, or a real arm lost its `# STAND-DOWN:` marker."
                % (item, sorted(implemented)))

        with open(PREPUSH, encoding="utf-8") as f:
            body = f.read()
        gate_a = body[body.index("-- gate a"):body.index("-- gate b")]
        self.assertRegex(gate_a, r'if ! "\$GUARDRAILS/check-prover-record\.sh" --push',
                         "gate a no longer runs the prover-record check at all")


class TestPrePushAnchorsOnTheRightInvariant(unittest.TestCase):
    """M5: `guardrails/pre-push` names this law's own invariant, INV-290, and no other. The
    stand-down block once carried INV-286 — the rendered-page clearing law, which landed the same
    evening on a different row — in both its comment and the line a person reads at the moment the
    whole gate chain stands down; a reader following that anchor would land on Requirement 296 and
    find a law about HTML pages where the reason for their push passing unguarded should be."""

    def _standdown_block(self):
        with open(PREPUSH, encoding="utf-8") as f:
            text = f.read()
        start = text.index("deletion-only stand-down")
        end = text.index("fail=0", start)
        return text[start:end]

    def test_standdown_block_names_inv_290_and_no_other_invariant(self):
        block = self._standdown_block()
        self.assertIn("INV-290", block, "the stand-down block does not anchor on its own law")
        self.assertNotIn("INV-286", block,
                          "the stand-down block still names INV-286, the rendered-page law")

    def test_the_printed_standdown_line_names_inv_290(self):
        block = self._standdown_block()
        printed = [l for l in block.splitlines() if "PUSH ALLOWED" in l]
        self.assertTrue(printed, "no printed stand-down line found")
        self.assertIn("INV-290", printed[0],
                      "the line the person reads at stand-down does not name INV-290")
        self.assertNotIn("INV-286", printed[0],
                          "the line the person reads at stand-down still names INV-286")


class TestCheckerLogic(unittest.TestCase):
    """The checker in isolation — real subprocess runs against synthetic ref-update input."""

    def check(self, lines):
        return run(["bash", CHECKER], cwd=ROOT, extra_env={"PUSH_REF_LINES": lines})

    def test_all_deletion_lines_exit_0(self):
        r = self.check(DELETION_STDIN)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("deletion-only", r.stdout)

    def test_all_content_lines_exit_1(self):
        r = self.check(CONTENT_STDIN)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_mixed_lines_exit_1(self):
        # a push that deletes a tag AND pushes real content is never treated as deletion-only.
        r = self.check(MIXED_STDIN)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_no_lines_exit_1_conservative(self):
        r = self.check("")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("conservative", r.stdout)

    def test_blank_lines_between_real_lines_are_skipped(self):
        r = self.check("\n" + DELETION_STDIN + "\n")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_reads_real_stdin_when_env_var_unset(self):
        # The env var has to be cleared for this case, and clearing it matters most when the suite
        # runs INSIDE the pre-push chain: the chain exports PUSH_REF_LINES with the real push's ref
        # lines, so a test that only passes stdin would read the live push instead of its own input.
        env = dict(os.environ)
        env.pop("PUSH_REF_LINES", None)
        r = subprocess.run(["bash", CHECKER], cwd=ROOT, capture_output=True, text=True,
                           env=env, input=DELETION_STDIN)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestPrePushStandsDownOnDeletion(_CleansSuiteLogLeaks, unittest.TestCase):
    """The integration proof: guardrails/pre-push itself, fed real stdin. Deletion-only stdin
    must finish fast with a named stand-down; content-shaped stdin must fall through to the
    ordinary chain (proven by a bounded partial read, never by waiting out the full suite)."""

    def setUp(self):
        # guardrails/pre-push's first line is `git rev-parse --show-toplevel`; the suite-in-suite
        # scratch copy (test_guardrails.py::TestGateB_Tests) runs the whole suite against a copy of
        # the tree with .git stripped by design, so these git-dependent, real-subprocess tests do
        # not apply there — the same carve-out test_config_health.py already takes for the same
        # reason.
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("scratch copy carries no .git for guardrails/pre-push to root itself")
        if os.environ.get(NESTED_MARKER):
            # A bare check-tests.sh run (the content-push branch below) can reach the real suite
            # a second time with a real .git, so LIVE_SPEC_SCRATCH alone does not catch this case —
            # NESTED_MARKER does. Skip: a nested run_bounded call would open a second process group
            # the outer kill cannot reach (row 574).
            self.skipTest("already inside a run_bounded chain — a nested instance would open an "
                          "unguarded process group (SPEC INV-100, ROADMAP row 574)")

    def test_deletion_only_push_finishes_in_seconds_with_a_named_standdown(self):
        code, out = run_bounded(["bash", PREPUSH], DELETION_STDIN, timeout=15)
        self.assertEqual(code, 0, out)
        self.assertIn("deletion-only", out.lower())
        # names the stand-down AND its reason, on one line
        self.assertIn("stand", out.lower())
        self.assertIn("reason", out.lower())
        # the ordinary chain never started
        self.assertNotIn("== live-spec push gate ==", out)

    def test_content_push_falls_through_to_the_ordinary_chain(self):
        # bounded smoke test: within a short window the ordinary chain must have started (its
        # banner + gate a's own line printed) and the deletion stand-down must never have fired.
        # Never waits for the full suite this proves untouched — a real content push's own gates
        # are exercised in full by the rest of the suite, not re-run here. The whole process
        # GROUP is killed on timeout (run_bounded), never just the top bash process, so a
        # check-tests.sh/pytest descendant this window catches is never left running afterward;
        # any suite temp artifact that descendant (or ITS OWN nested full-suite run) leaves
        # behind at the moment of the kill is swept too, by the suite's own prefix rule.
        before = self._before()
        code, out = run_bounded(["bash", PREPUSH], CONTENT_STDIN, timeout=3)
        self._clean_new(before)
        self.assertIsNone(code, "pre-push returned inside the timeout window on a real content "
                           "diff — unexpected, but the assertions below still hold: " + out)
        self.assertIn("== live-spec push gate ==", out)
        self.assertIn("gate a", out)
        self.assertNotIn("deletion-only", out.lower())

    def test_manual_invocation_with_no_stdin_is_unaffected(self):
        # a tty-less, empty-stdin invocation (e.g. piped from /dev/null) must never be read as
        # deletion-only — it falls through to the ordinary chain exactly as before this change.
        before = self._before()
        code, out = run_bounded(["bash", PREPUSH], "", timeout=3)
        self._clean_new(before)
        self.assertIsNone(code, "expected the ordinary chain to still be running past the "
                           "timeout window: " + out)
        self.assertIn("== live-spec push gate ==", out)
        self.assertNotIn("deletion-only", out.lower())


if __name__ == "__main__":
    unittest.main()
