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
    # The hook shrank on 2026-08-17 by the owner's decision: it had been retelling all seven laws in
    # full (~4.5 KB into every prompt) and now speaks one line that NAMES the seven and POINTS at the
    # two files holding their wording. The four tests below follow that decision. Each still proves
    # the same law reaches the window — by its name and its pointer now, rather than by its full text.
    # A test that pins wording the hook no longer says would only pin the size back on.

    POINTERS = ("~/.claude/live-spec/profile.md", "~/.claude/skills/live-spec-base/SKILL.md")

    def _line(self):
        result = subprocess.run([SCRIPT], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_output_points_at_the_law_texts(self):
        """The shrunk hook's whole contract: it stops carrying the texts, so it must carry the way to
        them. Both homes are named, and the line says the laws are to be acted on."""
        out = self._line()
        for needle in self.POINTERS:
            self.assertIn(needle, out, "the hook names no home for the law texts: %r" % needle)
        self.assertIn("Session laws (live-spec)", out, "the line does not announce what it is")
        self.assertIn("Act on them", out, "the line does not say the laws bind this turn")

    def test_output_names_all_seven_laws(self):
        """Names only, but all seven of them: a law dropped from the line is a law the window never
        hears about, and the numbering is how the profile's fuller text is found."""
        out = self._line()
        for n in range(1, 8):
            self.assertIn(" %d " % n, out, "law %d is not named in the reminder line" % n)

    def test_output_carries_both_laws(self):
        """Laws 2 and 3 — the language law (plain words talk, codes only trail) and the narration law
        (the work is narrated as it goes). Named, with the profile holding the wording."""
        out = self._line()
        for needle in (
            "plain words",                   # the language law's positive side
            "trail in parentheses",          # codes never lead
            "narrate the work",              # the narration law, by name
            "preshow-register-lint.py",      # the industry-words law's mechanical net, still named
            self.POINTERS[0],                # where the full wording stands
        ):
            self.assertIn(needle, out, "law line missing: %r" % needle)

    def test_output_carries_the_no_scissors_law(self):
        """Law 4. The banned shape is named and shown, and the profile holds its full statement."""
        out = self._line()
        for needle in (
            "contrast frame",                # the banned shape, named
            '"X, not Y"',                    # and shown, so the name is unmistakable
            self.POINTERS[0],                # the law's home stays the profile
        ):
            self.assertIn(needle, out, "no-scissors line missing: %r" % needle)

    def test_output_carries_the_routing_law(self):
        """Law 5. The seat's duty and the three tiers stay in the line, because a window that mis-routes
        spends the owner's money before any file can be read."""
        out = self._line()
        for needle in (
            "routing",
            "workers execute",
            "opus=judgment",
            "sonnet=mechanical multi-step",
            "haiku=single step",
            self.POINTERS[0],
        ):
            self.assertIn(needle, out, "routing line missing: %r" % needle)

    def test_output_carries_the_deferral_law(self):
        """Law 6. The re-test the law asks for is named by its trigger word, and the profile holds the
        rest (the AskUserQuestion case, the marker net, the spec home)."""
        out = self._line()
        for needle in (
            "deferral",                      # the subject
            "derivability",                  # the re-test the law asks for
            "before parking it",             # the moment it applies
            self.POINTERS[0],
        ):
            self.assertIn(needle, out, "deferral line missing: %r" % needle)

    def test_installer_covers_both_hooks(self):
        """ROADMAP row 506: the installer now GENERATES its clock-hook/chat-law-hook coverage from
        guardrails/judge-hooks.json rather than naming the event as a literal string in its own
        source, so this proves the BEHAVIOUR — run against an isolated fake $HOME, both end up wired
        as UserPromptSubmit entries — instead of grepping the script's text for a word the declarative
        rewrite no longer needs to spell out in the shell file itself. Full both-directions coverage
        of the declared WIRED set is proven in tests/test_install_session_hooks.py, which also asserts
        the six opt-in files land on disk unwired."""
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
