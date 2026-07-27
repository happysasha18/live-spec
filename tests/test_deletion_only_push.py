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

import glob
import os
import signal
import subprocess
import tempfile
import unittest

from conftest import ROOT

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


def run(args, cwd=None, extra_env=None, **kwargs):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        args, cwd=cwd or ROOT, capture_output=True, text=True, env=env, **kwargs
    )


def run_bounded(args, input_text, timeout):
    """Run a possibly-long-lived process, killing its WHOLE process group on timeout (never just
    the direct child) so a real gate chain that spawns check-tests.sh/pytest is never left running
    as an orphan after the test returns (base rule: cleanup scopes to what the run provably owns).
    Returns (returncode_or_None, combined_stdout). None means it was killed on timeout."""
    proc = subprocess.Popen(
        args, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, start_new_session=True,
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
    """check-tests.sh mktemps a livespec-test-suite-log.* file the instant it starts, before
    pytest itself runs; a test that intentionally kills the chain mid-flight to prove the
    ordinary path started can catch the chain right after that mktemp. Scoped cleanup: only
    files matching this exact prefix, only ones that did not exist before this test's own run."""

    PATTERN = os.path.join(tempfile.gettempdir(), "livespec-test-suite-log.*")

    def _before(self):
        return set(glob.glob(self.PATTERN))

    def _clean_new(self, before):
        for f in set(glob.glob(self.PATTERN)) - before:
            try:
                os.remove(f)
            except OSError:
                pass


class TestCheckerScriptShips(unittest.TestCase):
    def test_script_ships_and_is_executable(self):
        self.assertTrue(os.path.isfile(CHECKER), "guardrails/check-deletion-only-push.sh missing")
        self.assertTrue(os.access(CHECKER, os.X_OK), "check-deletion-only-push.sh not executable")


class TestCheckerLogic(unittest.TestCase):
    """The checker in isolation — real subprocess runs against synthetic ref-update input."""

    def check(self, lines):
        return run(["bash", CHECKER], extra_env={"PUSH_REF_LINES": lines})

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
        r = run(["bash", CHECKER], input=DELETION_STDIN)
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
        # any suite-log temp file that same descendant mktemps before being killed is swept too.
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
