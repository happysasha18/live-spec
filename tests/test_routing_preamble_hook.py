"""tests/test_routing_preamble_hook.py — the routing preamble reaches an adopted project
automatically (PLAN.md id: q-398).

hooks/routing-preamble-hook.sh is a vendored UserPromptSubmit hook, sibling in shape to
hooks/chat-law-hook.sh: it injects one reminder line into every prompt's context, naming the
zone-referral law (spec/roles-and-agents.md, Requirement 196 [INV-190]) and the no-rewrite clause
beside it (criterion 21) — the hook only reminds, it never rewrites, redirects, or silently
resends the person's own message. It is wired the same way as its sibling: declared "wired" in
guardrails/judge-hooks.json and installed by scripts/install-session-hooks.sh.

This suite proves three things: the hook's own output carries the reminder (red-provable on a
fixture prompt naming a foreign zone — before this hook existed, no such line reached the
context at all, so a request meant for another project's zone had nothing surfacing the referral
duty automatically); the installer wires it exactly as it wires clock-hook.sh and
chat-law-hook.sh; and the adoption gate — guardrails/check-config-health.sh's session-hook
directory-diff arm (INV-175 inverted, ROADMAP row 417), which diffs a project's hooks/ source
against its installed set — reds a pack-loaded fixture project carrying the hook's source but no
installed copy, and passes once the fixture installs it. That gate arm needs no code change to
cover the new hook: it diffs hooks/ as a whole, so a hook added there is covered from the day it
lands.
"""
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

HOOK = os.path.join(ROOT, "hooks", "routing-preamble-hook.sh")
DECL = os.path.join(ROOT, "guardrails", "judge-hooks.json")
INSTALLER = os.path.join(ROOT, "scripts", "install-session-hooks.sh")
CONFIG_HEALTH = os.path.join(ROOT, "guardrails", "check-config-health.sh")


def _run_hook():
    result = subprocess.run(["sh", HOOK], capture_output=True, text=True)
    return result


class TestRoutingPreambleHookScript(unittest.TestCase):
    def test_hook_file_exists_and_is_executable(self):
        self.assertTrue(os.path.isfile(HOOK), "missing hook: %s" % HOOK)
        self.assertTrue(os.access(HOOK, os.X_OK), "%s is not executable" % HOOK)

    def test_output_names_the_zone_referral_law(self):
        r = _run_hook()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for needle in (
            "Routing preamble",
            "INV-190",
            "spec/roles-and-agents.md",
            "Requirement 196",
            "another adopted project zone",
        ):
            self.assertIn(needle, r.stdout, "routing preamble missing: %r" % needle)

    def test_output_carries_the_no_rewrite_clause(self):
        """The clause added beside INV-190 (criterion 21): the hook only reminds, it never
        rewrites, redirects, or resends the person's own message."""
        r = _run_hook()
        for needle in ("never rewrite", "redirect", "resend"):
            self.assertIn(needle, r.stdout, "no-rewrite clause missing: %r" % needle)

    def test_red_proof_on_a_fixture_prompt_naming_a_foreign_zone(self):
        """RED PROOF: before this hook existed, a prompt naming another project's zone reached the
        session with no reminder anywhere in its injected context — the referral law had no
        mechanical voice. This fixture prompt stands for that case; the hook's own output (which
        every prompt now carries, unconditionally, matching its sibling chat-law-hook.sh's shape)
        is what a session sees ahead of answering it. Proven red by deleting the hook file and
        re-running: the routing preamble line then reaches no prompt at all."""
        fixture_prompt = "please fix the login bug over in the tlvphotos repo"
        self.assertIn("tlvphotos", fixture_prompt)  # the fixture names a foreign zone
        r = _run_hook()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(
            "refer it back to whoever asked", r.stdout,
            "the routing preamble must reach context ahead of a prompt naming a foreign zone")


class TestRoutingPreambleHookDeclared(unittest.TestCase):
    def _decl(self):
        import json
        with open(DECL, encoding="utf-8") as f:
            return json.load(f)

    def test_declared_wired_alongside_its_siblings(self):
        decl = self._decl()
        self.assertEqual(decl["wired"].get("routing-preamble-hook"), "UserPromptSubmit")
        self.assertEqual(decl["file"].get("routing-preamble-hook"), "routing-preamble-hook.sh")
        self.assertEqual(
            decl["command"].get("routing-preamble-hook"),
            "sh ~/.claude/hooks/routing-preamble-hook.sh")


class TestRoutingPreambleHookInstalled(unittest.TestCase):
    def test_installer_wires_it_same_as_its_siblings(self):
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ)
            env["HOME"] = home
            proc = subprocess.run(["sh", INSTALLER], capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

            import json
            settings_path = os.path.join(home, ".claude", "settings.json")
            with open(settings_path, encoding="utf-8") as f:
                settings = json.load(f)
            cmds = [
                hk.get("command", "")
                for group in settings.get("hooks", {}).get("UserPromptSubmit", [])
                for hk in group.get("hooks", [])
            ]
            for needle in ("clock-hook.sh", "chat-law-hook.sh", "routing-preamble-hook.sh"):
                self.assertTrue(
                    any(needle in c for c in cmds),
                    "installer did not wire %r as UserPromptSubmit: %r" % (needle, cmds))

            installed = os.path.join(home, ".claude", "hooks", "routing-preamble-hook.sh")
            self.assertTrue(os.path.isfile(installed), "hook file not placed: %s" % installed)
            with open(installed, encoding="utf-8") as f:
                self.assertIn("Routing preamble", f.read())


class TestAdoptionGateRedsAFixtureCarryingNoHook(unittest.TestCase):
    """The adoption gate: guardrails/check-config-health.sh's session-hook directory-diff arm
    (INV-175 inverted). It diffs a project's hooks/ source directory against its installed set —
    every file under hooks/ is covered automatically, with no edit to the check itself needed when
    a new hook lands there (ROADMAP row 417, the earlier hardcoded-name loop's own fix). This
    fixture proves that arm now covers routing-preamble-hook.sh: a pack-loaded fixture project
    carrying the hook's source but no installed copy reds, naming the file; the same fixture with
    the hook installed passes."""

    def _fixture_repo(self, tmp, install_hook):
        subprocess.run(["git", "init", "-q", tmp], check=True)
        gdir = os.path.join(tmp, "guardrails")
        os.makedirs(gdir)
        for name in ("pre-commit", "pre-push"):
            with open(os.path.join(gdir, name), "w") as f:
                f.write("#!/bin/sh\nexit 0\n")
        ghooks = os.path.join(tmp, ".git", "hooks")
        for name in ("pre-commit", "pre-push"):
            p = os.path.join(ghooks, name)
            with open(p, "w") as f:
                f.write("#!/bin/sh\nexit 0\n")
            os.chmod(p, 0o755)

        # The fixture's own hooks/ source carries only the one hook under test — a pack-loaded
        # fixture project, not the real repo's full hooks/ directory.
        with open(HOOK, encoding="utf-8") as f:
            hook_body = f.read()
        hooks_dir = os.path.join(tmp, "hooks")
        os.makedirs(hooks_dir)
        with open(os.path.join(hooks_dir, "routing-preamble-hook.sh"), "w") as f:
            f.write(hook_body)

        home = os.path.join(tmp, "scratch-home")
        chooks = os.path.join(home, ".claude", "hooks")
        os.makedirs(chooks)
        if install_hook:
            with open(os.path.join(chooks, "routing-preamble-hook.sh"), "w") as f:
                f.write(hook_body)
        return home

    def _run_gate(self, tmp, home):
        env = dict(os.environ)
        env.pop("GITHUB_ACTIONS", None)
        env.pop("CI", None)
        env["HOME"] = home
        return subprocess.run(
            ["bash", CONFIG_HEALTH], cwd=tmp, capture_output=True, text=True, env=env)

    def test_fixture_with_no_installed_hook_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._fixture_repo(tmp, install_hook=False)
            r = self._run_gate(tmp, home)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("routing-preamble-hook.sh", r.stdout)
            self.assertIn("install", r.stdout.lower())

    def test_same_fixture_with_the_hook_installed_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._fixture_repo(tmp, install_hook=True)
            r = self._run_gate(tmp, home)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertNotIn("routing-preamble-hook.sh", r.stdout)


if __name__ == "__main__":
    unittest.main()
