"""The chat laws' mechanical voice (row 141, SPEC INV-28 delivery).

The language law (plain words talk, codes only trail) and the narration law
(beats name wish+step, step ends digest, long silence owes a heartbeat)
live in skills a window may never load — so a prompt hook injects a one-line
reminder into every prompt on the working machine. The skills stay the laws'
homes; the hook only reminds. This test proves the script on disk, the line it
speaks, and that the one installer covers both session hooks (clock + laws).

Zero dependencies beyond the stdlib; run from the repo root:
  python3 -m pytest -q tests
"""

import os
import subprocess
import unittest

from conftest import ROOT
SCRIPT = os.path.join(ROOT, "hooks", "chat-law-hook.sh")
INSTALLER = os.path.join(ROOT, "scripts", "install-session-hooks.sh")


class TestChatLawHookScript(unittest.TestCase):
    def test_script_exists_and_executable(self):
        self.assertTrue(os.path.isfile(SCRIPT), "missing script: %s" % SCRIPT)
        self.assertTrue(os.access(SCRIPT, os.X_OK), "%s is not executable" % SCRIPT)

    def test_output_carries_both_laws(self):
        result = subprocess.run([SCRIPT], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        out = result.stdout
        for needle in (
            "plain product words",          # the language law's positive side
            "trail in parentheses",         # codes never lead
            "wish",                          # narration identity: which wish
            "pipeline step",                 # narration identity: which pipeline step
                                             # (was "station" until 2026-07-28, when the register
                                             # lint's coinage arm retired the phrase "pipeline
                                             # station"; the duty is the same — every beat names
                                             # the step of the pipeline the work stands at)
            "digest",                        # step-end digest
            "10 minutes",                    # the heartbeat threshold
        ):
            self.assertIn(needle, out, "law line missing: %r" % needle)

    def test_output_carries_the_no_scissors_law(self):
        result = subprocess.run([SCRIPT], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        out = result.stdout
        for needle in (
            "its own positive sentence",     # say what a thing IS
            "contrast frame",                # the banned shape, named
            "banned in every text",          # the scope
            "language.no-scissors",          # the law's home stays the profile
        ):
            self.assertIn(needle, out, "no-scissors line missing: %r" % needle)

    def test_output_carries_the_routing_law(self):
        result = subprocess.run([SCRIPT], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        out = result.stdout
        for needle in (
            "orchestrator seat",
            "cheapest sufficient tier",
            "locate their own anchors",
            "SPEC INV-69",
        ):
            self.assertIn(needle, out, "routing line missing: %r" % needle)

    def test_output_carries_the_deferral_law(self):
        result = subprocess.run([SCRIPT], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        out = result.stdout
        for needle in (
            "re-test it by derivability",     # the ask-moment re-test
            "AskUserQuestion",                # the question is a deferral too
            "itself the finding",             # an unnamed marker/question is the finding
            "check-deferral-marker.py",       # the mechanical net named
            "SPEC INV-152",                   # the law's spec home
        ):
            self.assertIn(needle, out, "deferral line missing: %r" % needle)

    def test_installer_covers_both_hooks(self):
        """ROADMAP row 506: the installer now GENERATES its clock-hook/chat-law-hook coverage from
        guardrails/judge-hooks.json rather than naming the event as a literal string in its own
        source, so this proves the BEHAVIOUR — run against an isolated fake $HOME, both end up wired
        as UserPromptSubmit entries — instead of grepping the script's text for a word the declarative
        rewrite no longer needs to spell out in the shell file itself. Full both-directions coverage
        of every declared hook (not just these two) is proven in tests/test_install_session_hooks.py."""
        import json
        import tempfile

        self.assertTrue(os.path.isfile(INSTALLER), "missing installer: %s" % INSTALLER)
        self.assertTrue(os.access(INSTALLER, os.X_OK), "%s is not executable" % INSTALLER)

        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ)
            env["HOME"] = home
            proc = subprocess.run(["sh", INSTALLER], capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

            settings_path = os.path.join(home, ".claude", "settings.json")
            with open(settings_path, encoding="utf-8") as f:
                settings = json.load(f)
            cmds = [
                hk.get("command", "")
                for group in settings.get("hooks", {}).get("UserPromptSubmit", [])
                for hk in group.get("hooks", [])
            ]
            for needle in ("clock-hook.sh", "chat-law-hook.sh"):
                self.assertTrue(
                    any(needle in c for c in cmds),
                    "installer did not wire %r as UserPromptSubmit: %r" % (needle, cmds),
                )


if __name__ == "__main__":
    unittest.main()
