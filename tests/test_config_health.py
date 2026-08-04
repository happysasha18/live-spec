"""INV-175 — the installed gate is the source gate, held by a config-health check.

A gate lives twice: source in guardrails/ travels with the repo, the installed copy in
.git/hooks/ actually runs. They drift the moment an install is skipped — the worked instance:
on 2026-07-16 the installed pre-push was missing gates k (freeze) and l (muted launch) that the
source carried. The check reds on a missing or drifted installed hook and names the one fix;
it runs inside the suite so even a stale pre-push surfaces the drift (self-healing); a checkout
with no installed hooks by design (CI) skips by name. The commit fence gains a second arm: a
file both staged and carrying unstaged modifications is a fence stop on the shared index.
"""
import json
import os
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(REPO, "guardrails", "check-config-health.sh")


def run_check(cwd, env_extra=None):
    env = dict(os.environ)
    env.pop("GITHUB_ACTIONS", None)
    env.pop("CI", None)  # the CI runner sets both; the temp-repo tests exercise the non-CI arm
    if env_extra:
        env.update(env_extra)
    return subprocess.run(["bash", CHECK], cwd=cwd, capture_output=True, text=True, env=env)


def make_repo(tmp, install=("pre-commit", "pre-push"), drift=None):
    subprocess.run(["git", "init", "-q", tmp], check=True)
    gdir = os.path.join(tmp, "guardrails")
    os.makedirs(gdir)
    for name in ("pre-commit", "pre-push"):
        with open(os.path.join(gdir, name), "w") as f:
            f.write("#!/bin/sh\nexit 0\n")
    hooks = os.path.join(tmp, ".git", "hooks")
    for name in install:
        body = "#!/bin/sh\nexit 0\n" if drift != name else "#!/bin/sh\n# stale\nexit 0\n"
        with open(os.path.join(hooks, name), "w") as f:
            f.write(body)
        os.chmod(os.path.join(hooks, name), 0o755)
    return tmp


class TestConfigHealth(unittest.TestCase):
    def test_this_repo_installed_hooks_match_source(self):
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("scratch copy installs no hooks by design")
        # env AS-IS: on a CI checkout the script itself skips by name (no local hooks by design);
        # on a working machine it verifies the real installed copies.
        r = subprocess.run(["bash", CHECK], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_installed_hook_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_repo(tmp, install=("pre-commit",))
            r = run_check(tmp)
            self.assertEqual(r.returncode, 1)
            self.assertIn("config-health", r.stdout)
            self.assertIn("guardrails/install.sh", r.stdout)

    def test_drifted_installed_hook_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_repo(tmp, drift="pre-push")
            r = run_check(tmp)
            self.assertEqual(r.returncode, 1)
            self.assertIn("pre-push", r.stdout)

    def test_matching_hooks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_repo(tmp)
            r = run_check(tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_ci_checkout_skips_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_repo(tmp, install=())
            r = run_check(tmp, env_extra={"GITHUB_ACTIONS": "true"})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("skip", r.stdout.lower())


class TestSessionHookDirDiff(unittest.TestCase):
    """INV-175 inverted (ROADMAP 417): the session-hook arm DIFFS the hook source directory (hooks/)
    against the installed set, so every installed hook is covered automatically — never a hardcoded
    basename list that goes blind to a hook added later. register-judge*.sh and any future hook are
    covered the moment they land in hooks/, with no edit to this gate."""

    def _repo_with_hooks(self, tmp, sources, installed):
        # sources: {name: body} written under tmp/hooks/. installed: {name: body} written under a
        # scratch HOME's .claude/hooks/. Returns the scratch HOME to hand the check as $HOME.
        subprocess.run(["git", "init", "-q", tmp], check=True)
        gdir = os.path.join(tmp, "guardrails")
        os.makedirs(gdir)
        for name in ("pre-commit", "pre-push"):
            with open(os.path.join(gdir, name), "w") as f:
                f.write("#!/bin/sh\nexit 0\n")
        # install the two git hooks so the git-hook arm passes and only the session arm is under test.
        ghooks = os.path.join(tmp, ".git", "hooks")
        for name in ("pre-commit", "pre-push"):
            p = os.path.join(ghooks, name)
            with open(p, "w") as f:
                f.write("#!/bin/sh\nexit 0\n")
            os.chmod(p, 0o755)
        hooks = os.path.join(tmp, "hooks")
        os.makedirs(hooks)
        for name, body in sources.items():
            with open(os.path.join(hooks, name), "w") as f:
                f.write(body)
        home = os.path.join(tmp, "scratch-home")
        chooks = os.path.join(home, ".claude", "hooks")
        os.makedirs(chooks)
        for name, body in installed.items():
            with open(os.path.join(chooks, name), "w") as f:
                f.write(body)
        return home

    def test_a_hook_beyond_the_old_three_names_reds_on_drift(self):
        # register-judge.py is neither scissors-scan.py, clock-hook.sh, nor chat-law-hook.sh — the old
        # loop was blind to it. Its drift must red now. (RED-FIRST against the pre-delta three-name loop.)
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo_with_hooks(
                tmp,
                sources={"register-judge.py": "print('v2')\n"},
                installed={"register-judge.py": "print('v1 stale')\n"})
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("register-judge.py", r.stdout)

    def test_a_sourced_hook_missing_from_install_reds_as_drift(self):
        """A hook that has source but no installed copy is DRIFT, not a green skip: the config is
        unhealthy because the judge can go dark while every gate stays green. (RED against the old skip.)"""
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo_with_hooks(
                tmp, sources={"register-judge-report.sh": "echo hi\n"}, installed={})
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("register-judge-report.sh", r.stdout)

    def test_an_installed_only_overlay_with_no_source_stays_silent(self):
        """A personal-layer overlay the pack never ships (installed, no source here) is correctly left
        alone — only a SOURCE hook missing from install is drift."""
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo_with_hooks(
                tmp, sources={}, installed={"personal-overlay.sh": "echo mine\n"})
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_matching_source_hook_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            body = "print('same')\n"
            home = self._repo_with_hooks(
                tmp,
                sources={"register-judge.py": body, "scissors-scan.py": body},
                installed={"register-judge.py": body, "scissors-scan.py": body})
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestDeclaredLocalOverride(unittest.TestCase):
    """A machine may deliberately run a changed copy of a hook — a check switched off for a stated
    span, say. The difference is declared as data in guardrails/local-overrides.json, and an entry
    pins the fingerprint of the installed file it covers. It therefore buys silence for exactly that
    copy: change the installed file again and the entry stops matching and the arm reds. Added
    2026-08-04, red-first against the form that had no override at all."""

    SRC = "print('source')\n"
    LOCAL = "print('local, switched off')\n"

    def _sha(self, body):
        import hashlib
        return hashlib.sha256(body.encode()).hexdigest()

    def _repo(self, tmp, entries, installed_body):
        helper = TestSessionHookDirDiff()
        home = helper._repo_with_hooks(
            tmp,
            sources={"midturn-chat-scan.py": self.SRC},
            installed={"midturn-chat-scan.py": installed_body})
        with open(os.path.join(tmp, "guardrails", "local-overrides.json"), "w") as f:
            json.dump({"hook_overrides": entries}, f)
        return home

    def test_a_declared_override_matching_the_installed_file_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo(tmp, [{
                "hook": "midturn-chat-scan.py",
                "installed_sha256": self._sha(self.LOCAL),
                "reason": "switched off while the documents it reads are rewritten",
            }], self.LOCAL)
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("declared local override", r.stdout)

    def test_the_override_stops_covering_a_file_that_changed_again(self):
        """The entry names one copy. A different local copy is undeclared drift and reds."""
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo(tmp, [{
                "hook": "midturn-chat-scan.py",
                "installed_sha256": self._sha(self.LOCAL),
                "reason": "switched off while the documents it reads are rewritten",
            }], "print('a third, undeclared edit')\n")
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("midturn-chat-scan.py", r.stdout)

    def test_an_override_without_a_reason_buys_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo(tmp, [{
                "hook": "midturn-chat-scan.py",
                "installed_sha256": self._sha(self.LOCAL),
            }], self.LOCAL)
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_an_override_naming_another_hook_covers_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo(tmp, [{
                "hook": "some-other-hook.sh",
                "installed_sha256": self._sha(self.LOCAL),
                "reason": "a different hook entirely",
            }], self.LOCAL)
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_drift_still_reds_when_no_declaration_file_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            helper = TestSessionHookDirDiff()
            home = helper._repo_with_hooks(
                tmp,
                sources={"midturn-chat-scan.py": self.SRC},
                installed={"midturn-chat-scan.py": self.LOCAL})
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)


class TestSkillCopyArm(unittest.TestCase):
    """INV-243 — a skill lives twice too: source in skills/ travels with the repo, the installed
    copy under ~/.claude/skills/<name> is what pack skills actually load from. Same shape as the
    session-hook directory-diff arm above, but for whole skill DIRECTORIES (diff -rq), since a
    skill is a tree (SKILL.md + references/ + scripts/...), not a single file."""

    def _repo_with_skills(self, tmp, pack_skills, installed_skills):
        # pack_skills / installed_skills: {skill_name: {relative_path: content}}
        subprocess.run(["git", "init", "-q", tmp], check=True)
        gdir = os.path.join(tmp, "guardrails")
        os.makedirs(gdir)
        for name in ("pre-commit", "pre-push"):
            with open(os.path.join(gdir, name), "w") as f:
                f.write("#!/bin/sh\nexit 0\n")
        # install the two git hooks so the git-hook arm passes and only the skill arm is under test.
        ghooks = os.path.join(tmp, ".git", "hooks")
        for name in ("pre-commit", "pre-push"):
            p = os.path.join(ghooks, name)
            with open(p, "w") as f:
                f.write("#!/bin/sh\nexit 0\n")
            os.chmod(p, 0o755)
        skills_dir = os.path.join(tmp, "skills")
        for sname, files in pack_skills.items():
            sdir = os.path.join(skills_dir, sname)
            for relpath, content in files.items():
                fpath = os.path.join(sdir, relpath)
                os.makedirs(os.path.dirname(fpath), exist_ok=True)
                with open(fpath, "w") as f:
                    f.write(content)
        home = os.path.join(tmp, "scratch-home")
        cskills = os.path.join(home, ".claude", "skills")
        os.makedirs(cskills, exist_ok=True)
        for sname, files in installed_skills.items():
            sdir = os.path.join(cskills, sname)
            for relpath, content in files.items():
                fpath = os.path.join(sdir, relpath)
                os.makedirs(os.path.dirname(fpath), exist_ok=True)
                with open(fpath, "w") as f:
                    f.write(content)
        return home

    def test_reds_missing_installed_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo_with_skills(
                tmp, pack_skills={"foo": {"SKILL.md": "content\n"}}, installed_skills={})
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("config-health", r.stdout)
            self.assertIn("sync-skills.sh", r.stdout)

    def test_reds_drifted_installed_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo_with_skills(
                tmp,
                pack_skills={"foo": {"SKILL.md": "v2\n"}},
                installed_skills={"foo": {"SKILL.md": "v1 stale\n"}})
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("foo", r.stdout)
            self.assertIn("drifted", r.stdout.lower())

    def test_passes_matching_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            body = "same\n"
            home = self._repo_with_skills(
                tmp,
                pack_skills={"foo": {"SKILL.md": body}},
                installed_skills={"foo": {"SKILL.md": body}})
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_ignores_personal_overlay_skill(self):
        # bar is installed with no pack source — a personal-layer skill the pack never ships. It
        # must be left alone; only foo (which has a pack source) is checked.
        with tempfile.TemporaryDirectory() as tmp:
            body = "same\n"
            home = self._repo_with_skills(
                tmp,
                pack_skills={"foo": {"SKILL.md": body}},
                installed_skills={
                    "foo": {"SKILL.md": body},
                    "bar": {"SKILL.md": "personal skill, no pack source\n"},
                })
            r = run_check(tmp, env_extra={"HOME": home})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_ci_skips_skill_arm(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = self._repo_with_skills(
                tmp, pack_skills={"foo": {"SKILL.md": "content\n"}}, installed_skills={})
            r = run_check(tmp, env_extra={"HOME": home, "GITHUB_ACTIONS": "true"})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestStagedVsWorktreeFenceArm(unittest.TestCase):
    def _repo_with_precommit(self, tmp):
        subprocess.run(["git", "init", "-q", tmp], check=True)
        subprocess.run(["git", "-C", tmp, "config", "user.email", "t@t"], check=True)
        subprocess.run(["git", "-C", tmp, "config", "user.name", "t"], check=True)
        gdir = os.path.join(tmp, "guardrails")
        os.makedirs(gdir)
        src = os.path.join(REPO, "guardrails", "pre-commit")
        with open(src) as f:
            body = f.read()
        dst = os.path.join(tmp, ".git", "hooks", "pre-commit")
        with open(dst, "w") as f:
            f.write(body)
        os.chmod(dst, 0o755)

    def test_staged_file_with_unstaged_edits_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._repo_with_precommit(tmp)
            p = os.path.join(tmp, "a.txt")
            open(p, "w").write("one\n")
            subprocess.run(["git", "-C", tmp, "add", "a.txt"], check=True)
            open(p, "a").write("two\n")  # unstaged edit on a staged file
            r = subprocess.run(["git", "-C", tmp, "commit", "-m", "x"],
                               capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("staged", (r.stdout + r.stderr).lower())

    def test_clean_staged_commit_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._repo_with_precommit(tmp)
            p = os.path.join(tmp, "a.txt")
            open(p, "w").write("one\n")
            subprocess.run(["git", "-C", tmp, "add", "a.txt"], check=True)
            r = subprocess.run(["git", "-C", tmp, "commit", "-m", "x"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestPermissionPathHealth(unittest.TestCase):
    """INV-216 — a permission rule whose target is a filesystem path that does not exist is a DEAD
    RULE, and config-health reds it. The worked instance (found on the owner's report, 2026-07-17
    ~15:29, that the harness "sometimes" refuses a push or a deploy): three deploy permissions named
    ~/tlvphoto after the tree was renamed to ~/tlvphotos on 2026-07-10, so for a week the rules sat
    looking correct while every deploy fell through to a prompt — a stale allow rule fails exactly
    like a missing one. The arm reads every permission rule that names a filesystem path in the
    personal ~/.claude/settings.json and the host's project settings, reds a rule whose path is
    absent, and reports the count it resolved so an unparsable shape is named, never silently
    skipped. It is personal-layer: it stands down by name where the settings cannot be read and never
    falsely passes, the same shape as the hook-drift arms above.

    Fixture isolation: CONFIG_HEALTH_PERMS_SETTINGS names the one settings file the arm scans, so a
    test drives the arm without touching the real personal settings."""

    def _write_settings(self, tmp, allow, name="settings.json"):
        p = os.path.join(tmp, name)
        with open(p, "w") as f:
            json.dump({"permissions": {"allow": allow}}, f)
        return p

    def _run(self, tmp, settings_path):
        # make_repo gives clean git hooks and no hooks/ dir, so only the permission-path arm is
        # under test here.
        make_repo(tmp)
        return run_check(tmp, env_extra={"CONFIG_HEALTH_PERMS_SETTINGS": settings_path})

    def test_dead_permission_path_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_tree = os.path.join(tmp, "no-such-tree")  # never created
            sp = self._write_settings(tmp, [
                "Bash(cd %s && bash scripts/deploy.sh)" % missing_tree,
            ])
            r = self._run(tmp, sp)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("config-health", r.stdout)
            self.assertIn("no-such-tree", r.stdout)

    def test_existing_permission_path_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            live = os.path.join(tmp, "tlvphotos")
            os.makedirs(os.path.join(live, "scripts"))
            with open(os.path.join(live, "scripts", "deploy.sh"), "w") as f:
                f.write("#!/bin/sh\n")
            sp = self._write_settings(tmp, [
                "Bash(cd %s && bash scripts/deploy.sh)" % live,
                "Bash(bash %s/scripts/deploy.sh)" % live,
                "Edit(%s/**)" % live,
            ])
            r = self._run(tmp, sp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_space_containing_path_that_exists_does_not_false_red(self):
        # A rule naming an existing path WITH A SPACE (the Google Chrome shape) must not split on the
        # space into a missing prefix and false-red — quoted and unquoted both.
        with tempfile.TemporaryDirectory() as tmp:
            spaced = os.path.join(tmp, "Google Chrome.app", "Contents")
            os.makedirs(spaced)
            sp = self._write_settings(tmp, [
                'Bash("%s" *)' % spaced,
                "Bash(%s *)" % spaced,
            ])
            r = self._run(tmp, sp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_absent_settings_stands_down_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            sp = os.path.join(tmp, "does-not-exist-settings.json")
            r = self._run(tmp, sp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("stands down", r.stdout.lower())

    def test_unparseable_settings_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            sp = os.path.join(tmp, "settings.json")
            with open(sp, "w") as f:
                f.write("{ this is not json ")
            r = self._run(tmp, sp)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_reports_the_count_of_rules_resolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            live = os.path.join(tmp, "here")
            os.makedirs(live)
            sp = self._write_settings(tmp, ["Edit(%s/**)" % live, "Bash(git push:*)"])
            r = self._run(tmp, sp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("resolved", r.stdout.lower())

    def test_unresolved_shape_is_named_not_reded(self):
        # A path behind an unresolvable variable is a shape the arm cannot resolve: it is NAMED in the
        # output (never a silent skip, row 384's law) and never false-reds.
        with tempfile.TemporaryDirectory() as tmp:
            sp = self._write_settings(tmp, ["Bash(cat $CONFIG_HEALTH_NO_SUCH_VAR/x/y.txt)"])
            r = self._run(tmp, sp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("unresolved", r.stdout.lower())

    def test_real_personal_settings_stands_down_or_passes(self):
        if os.environ.get("LIVE_SPEC_SCRATCH"):
            self.skipTest("scratch copy carries no .git for check-config-health.sh to root itself")
        # The arm run against the real personal + project settings (env AS-IS) either stands down by
        # name where they cannot be read, or passes on the repaired real ones — never a false red.
        r = subprocess.run(["bash", CHECK], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    # Traceability: the law lives in every derivation document, not only in the check.
    def test_spec_states_the_law(self):
        with open(os.path.join(REPO, "PRODUCT_SPEC.md")) as f:
            self.assertIn("INV-216", f.read())

    def test_architecture_owns_the_invariant(self):
        with open(os.path.join(REPO, "ARCHITECTURE.md")) as f:
            self.assertIn("INV-216", f.read())

    def test_matrix_row_covers_the_law(self):
        with open(os.path.join(REPO, "TEST_MATRIX.md")) as f:
            self.assertIn("M-397", f.read())


if __name__ == "__main__":
    unittest.main()
