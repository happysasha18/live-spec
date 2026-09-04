"""The four host checks, runnable — matrix row material for SPEC INV-97 (row 241).

Exercises the generic guardrails under scaffold/guardrails/: each check green on the
clean fixture host, red (exit 1 + a parseable GUARDRAIL-FAIL line with the expected
code) on one planted defect per failure code, red-with-attach-me-line when the config
is missing, and visibly WAIVED (exit 0) when the config declares the waiver.

Planted-defect variants are built in tmp by copying the clean tree and patching one
file — never as full checked-in trees. Zero dependencies beyond the stdlib; run:
  python3 -m pytest tests/test_scaffold_guardrails.py -q
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT, read_flat
SCAFFOLD = os.path.join(ROOT, "scaffold", "guardrails")
CLEAN = os.path.join(ROOT, "tests", "fixtures", "scaffold_guardrails", "host-clean")

SCRIPTS = {
    "completeness": "check_completeness.py",
    "tests-present": "check_tests_present.py",
    "traces": "check_traces_to_spec.py",
    "conflicts": "check_conflicts.py",
}


def run_check(check, host, args=(), config_env=None):
    """Run one check script with cwd at the host root; GUARDRAILS_CONFIG cleared
    unless the test sets it explicitly."""
    env = dict(os.environ)
    env.pop("GUARDRAILS_CONFIG", None)
    if config_env is not None:
        env["GUARDRAILS_CONFIG"] = config_env
    script = os.path.join(SCAFFOLD, SCRIPTS[check])
    return subprocess.run(
        ["python3", script] + list(args),
        cwd=host, capture_output=True, text=True, env=env,
    )


def fail_payload(result):
    """The machine line: exactly one GUARDRAIL-FAIL prefix parsing as JSON is enough;
    returns the first one's payload."""
    for line in (result.stdout + result.stderr).splitlines():
        if line.startswith("GUARDRAIL-FAIL "):
            return json.loads(line[len("GUARDRAIL-FAIL "):])
    raise AssertionError(
        "no GUARDRAIL-FAIL line in output:\n%s%s" % (result.stdout, result.stderr))


class HostCase(unittest.TestCase):
    """Shared tmp-host builder: copy the clean fixture, patch per test."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="row241-host-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.host = os.path.join(self.tmp, "host")
        shutil.copytree(CLEAN, self.host)

    def path(self, rel):
        return os.path.join(self.host, rel)

    def read(self, rel):
        with open(self.path(rel), encoding="utf-8") as f:
            return f.read()

    def write(self, rel, text):
        with open(self.path(rel), "w", encoding="utf-8") as f:
            f.write(text)

    def patch_config(self, **overrides):
        cfg = json.loads(self.read("guardrails.config.json"))
        cfg.update(overrides)
        self.write("guardrails.config.json", json.dumps(cfg))

    def assert_green(self, check, args=()):
        r = run_check(check, self.host, args)
        self.assertEqual(r.returncode, 0, "expected green:\n%s%s" % (r.stdout, r.stderr))
        self.assertIn("OK (%s)" % check, r.stdout)
        return r

    def assert_red(self, check, code, args=()):
        r = run_check(check, self.host, args)
        self.assertEqual(r.returncode, 1, "expected red:\n%s%s" % (r.stdout, r.stderr))
        payload = fail_payload(r)
        self.assertEqual(payload["code"], code)
        self.assertEqual(payload["severity"], "error")
        self.assertTrue(payload["message"])
        self.assertTrue(payload["fix"])
        return r, payload


def git(host, *args):
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    })
    r = subprocess.run(["git"] + list(args), cwd=host, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise AssertionError("git %s failed: %s%s" % (args, r.stdout, r.stderr))
    return r


class GitHostCase(HostCase):
    """tests-present needs real git history: init + base commit on the tmp host."""

    def setUp(self):
        super().setUp()
        git(self.host, "init", "-q")
        git(self.host, "add", "-A")
        git(self.host, "commit", "-qm", "base")


class TestCleanHostIsGreen(HostCase):
    def test_completeness_green(self):
        self.assert_green("completeness")

    def test_traces_green(self):
        self.assert_green("traces")

    def test_conflicts_green(self):
        self.assert_green("conflicts")


class TestTestsPresent(GitHostCase):
    def test_no_changes_green(self):
        self.assert_green("tests-present", args=["--base", "HEAD"])

    def test_change_with_test_green(self):
        self.write("src/app.py", self.read("src/app.py") + "\n# touched\n")
        self.write("tests/smoke.py", self.read("tests/smoke.py") + "\n# touched\n")
        git(self.host, "commit", "-aqm", "change with test")
        self.assert_green("tests-present", args=["--base", "HEAD~1"])

    def test_change_without_test_red(self):
        self.write("src/app.py", self.read("src/app.py") + "\n# touched\n")
        git(self.host, "commit", "-aqm", "change without test")
        r, payload = self.assert_red("tests-present", "tests-present.missing-test",
                                     args=["--base", "HEAD~1"])
        self.assertIn("src/app.py", payload["message"])

    def test_non_user_facing_change_green(self):
        self.write("PRODUCT_SPEC.md", self.read("PRODUCT_SPEC.md") + "\nA docs-only line.\n")
        git(self.host, "commit", "-aqm", "docs only")
        self.assert_green("tests-present", args=["--base", "HEAD~1"])

    def test_version_stamp_only_change_green(self):
        # A diff that only substitutes version strings is the stamp script's mechanical output,
        # held by the stamped-copy guard test; it owes no test change of its own.
        self.write("src/app.py", self.read("src/app.py") + '\nPACK_VERSION = "1.0.0"\n')
        git(self.host, "commit", "-aqm", "carry a version string")
        self.write("src/app.py", self.read("src/app.py").replace('"1.0.0"', '"1.0.1"'))
        git(self.host, "commit", "-aqm", "stamp bump only")
        self.assert_green("tests-present", args=["--base", "HEAD~1"])

    def test_stamp_plus_real_edit_still_red(self):
        self.write("src/app.py", self.read("src/app.py") + '\nPACK_VERSION = "1.0.0"\n')
        git(self.host, "commit", "-aqm", "carry a version string")
        self.write("src/app.py",
                   self.read("src/app.py").replace('"1.0.0"', '"1.0.1"') + "\n# real behaviour edit\n")
        git(self.host, "commit", "-aqm", "stamp plus real edit")
        r, payload = self.assert_red("tests-present", "tests-present.missing-test",
                                     args=["--base", "HEAD~1"])
        self.assertIn("src/app.py", payload["message"])


class TestCompletenessDefects(HostCase):
    def test_registered_but_absent(self):
        self.write("SURFACES.md", self.read("SURFACES.md")
                   + '| ghost | id="ghost" | INV-1 |\n')
        r, payload = self.assert_red("completeness", "completeness.registered-but-absent")
        self.assertIn("ghost", payload["message"])

    def test_registered_but_empty(self):
        html = self.read("dist/index.html").replace(
            '<section id="stats">Revenue holds steady at 42.</section>',
            '<section id="stats"></section>')
        self.write("dist/index.html", html)
        self.assert_red("completeness", "completeness.registered-but-empty")

    def test_rendered_but_unregistered(self):
        html = self.read("dist/index.html").replace(
            "</body>", '<section id="mystery">Unregistered content.</section>\n</body>')
        self.write("dist/index.html", html)
        r, payload = self.assert_red("completeness", "completeness.rendered-but-unregistered")
        self.assertIn("mystery", payload["message"])

    def test_dead_path_is_red(self):
        self.patch_config(rendered_artifacts=["dist/nowhere.html"])
        self.assert_red("completeness", "completeness.dead-path")


class TestTracesDefects(HostCase):
    def test_unanchored_surface(self):
        self.write("SURFACES.md", self.read("SURFACES.md").replace(
            '| stats | id="stats" | INV-1 |', '| stats | id="stats" |  |'))
        self.assert_red("traces", "traces.unanchored-surface")

    def test_dead_anchor(self):
        self.write("SURFACES.md", self.read("SURFACES.md").replace(
            '| stats | id="stats" | INV-1 |', '| stats | id="stats" | INV-9 |'))
        r, payload = self.assert_red("traces", "traces.dead-anchor")
        self.assertIn("INV-9", payload["message"])


class TestConflictsDefects(HostCase):
    def test_duplicate_anchor(self):
        self.write("PRODUCT_SPEC.md", self.read("PRODUCT_SPEC.md")
                   + "| INV-1 | stats panel, again |\n")
        self.assert_red("conflicts", "conflicts.duplicate-anchor")

    def test_invariant_without_row(self):
        self.write("PRODUCT_SPEC.md", self.read("PRODUCT_SPEC.md")
                   + "| INV-3 | an invariant no matrix row cites |\n")
        r, payload = self.assert_red("conflicts", "conflicts.invariant-without-row")
        self.assertIn("INV-3", payload["message"])

    def test_a_suffixed_invariant_without_a_row_is_seen(self):
        """A spec grows a case under an invariant it already has by suffixing its id. The
        pattern read digits only until 2026-09-04, so a suffixed id never entered the index
        at all and this sub-check never asked for its matrix row — the check reported success
        over what it could not parse. Reported from the tlvphotos zone, where three such
        invariants stood with no matrix row for as long as they existed, under a green check."""
        self.write("PRODUCT_SPEC.md", self.read("PRODUCT_SPEC.md")
                   + "| INV-3a | a suffixed invariant no matrix row cites |\n")
        r, payload = self.assert_red("conflicts", "conflicts.invariant-without-row")
        self.assertIn("INV-3a", payload["message"])

    def test_a_suffixed_anchor_indexed_twice_is_counted(self):
        """The same blindness sat in sub-check (a): a duplicate whose number carried a letter
        was not counted as a duplicate either."""
        row = "| INV-3a | a suffixed anchor |\n"
        self.write("PRODUCT_SPEC.md", self.read("PRODUCT_SPEC.md") + row + row)
        self.write("TEST_MATRIX.md", self.read("TEST_MATRIX.md")
                   + "| M-99 | covers INV-3a | done |\n")
        r, payload = self.assert_red("conflicts", "conflicts.duplicate-anchor")
        self.assertIn("INV-3a", payload["message"])

    def test_resolved_but_live(self):
        marker = "⟨DECIDE⟩"  # built, not literal, so repo-wide greps stay quiet
        self.write("PRODUCT_SPEC.md", self.read("PRODUCT_SPEC.md")
                   + "\n- %s theme colour — RESOLVED 2026-07-01\n" % marker)
        self.assert_red("conflicts", "conflicts.resolved-but-live")

    def test_surface_named_twice(self):
        self.write("SURFACES.md", self.read("SURFACES.md")
                   + '| stats | id="stats" | INV-1 |\n')
        r, payload = self.assert_red("conflicts", "conflicts.surface-named-twice")
        self.assertIn("stats", payload["message"])


class TestConfigLadder(HostCase):
    def test_missing_config_is_red_with_attach_me_line(self):
        os.remove(self.path("guardrails.config.json"))
        for check in SCRIPTS:
            r, payload = self.assert_red(check, "%s.no-config" % check)
            self.assertIn("guardrails.config.example.json", payload["fix"])
            self.assertIn("scaffold/guardrails/README.md", payload["fix"])

    def test_env_var_config_wins(self):
        moved = self.path("elsewhere.config.json")
        os.rename(self.path("guardrails.config.json"), moved)
        r = run_check("completeness", self.host, config_env=moved)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("OK (completeness)", r.stdout)

    def test_waived_check_is_visible_and_green(self):
        self.patch_config(waivers={
            "completeness": "no rendered artifact yet — declared 2026-07-10, owner Alexander"})
        # a waiver beats even a defect the check would otherwise catch
        self.write("SURFACES.md", self.read("SURFACES.md")
                   + '| ghost | id="ghost" | INV-1 |\n')
        r = run_check("completeness", self.host)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("WAIVED (completeness)", r.stdout)
        self.assertIn("no rendered artifact yet", r.stdout)


class TestShippedShape(unittest.TestCase):
    def test_example_config_ships_and_parses(self):
        path = os.path.join(SCAFFOLD, "guardrails.config.example.json")
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
        for key in ("spec_path", "matrix_path", "tests_dir", "user_facing_globs",
                    "registry_path", "render_command", "rendered_artifacts",
                    "surface_discovery_pattern", "waivers"):
            self.assertIn(key, cfg)

    def test_readme_walks_the_attach(self):
        readme = read_flat(os.path.join(SCAFFOLD, "README.md"))
        self.assertIn("guardrails.config.example.json", readme)
        self.assertIn("pre-push", readme)
        for script in SCRIPTS.values():
            self.assertIn(script, readme)

    def test_walk_opens_with_the_config_step(self):
        # Row 251: a first-time host reads the pre-config red as breakage unless the walk
        # LEADS with the config and names the red as by-design; the no-config fix line
        # points at that step.
        readme = read_flat(os.path.join(SCAFFOLD, "README.md"))
        walk = readme.split("## The attach walk", 1)[1]
        first_step = walk.split("1. ")[0]
        self.assertIn("0. **Copy the example config first", first_step,
                      "the attach walk no longer opens with the config step")
        self.assertIn("red until you do, by design", first_step)
        with open(os.path.join(SCAFFOLD, "gate_lib.py"), encoding="utf-8") as f:
            gate_lib_src = f.read()
        fix_assignment = gate_lib_src.split("ATTACH_ME_FIX", 1)[1].split("def ", 1)[0]
        self.assertIn("step 0", fix_assignment,
                      "the no-config fix line no longer points at the walk's step 0")
        # the probe's lesson rides the discovery-pattern bullet: a null pattern is a named
        # choice, never a silent default
        self.assertIn("disarms the rendered-but-unregistered check", readme)


if __name__ == "__main__":
    unittest.main()
