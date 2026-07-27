"""A deployed kind declares what its owner can change without a build — M-467 (SPEC INV-291).

Beside its concrete layers and proofs (INV-135), its design principles (INV-136) and its composition
axes (INV-244), a project kind whose product is deployed carries one more founding declaration: the
seam between what ships inside a build and what the owner turns from outside it. An experiment switch,
a piece of copy, a threshold or budget, and a feature toggle live on the configuration side and reach
production by a deploy of configuration alone; behaviour and structure stay in the code the build
ships. The founding records that seam on a `project.config-surface` line in the host profile, and the
check `guardrails/check-config-surface.py` reds a profile that records a kind and declares no such
surface.

Two things this file proves, kept distinct:

  1. The check itself — a runnable gate over a host profile, driven here by subprocess on fixture
     profiles. It reds on silence, passes on an explicit "none" from a project that deploys nothing,
     and reds a "none" that contradicts the host's own declared deployment layer. It rides the suite
     and stays off the push chain, the standing `guardrails/check-wrong-referral.py` already carries
     [INV-225], because the pack ships no deployed product of its own.

  2. The law's homes — the SPEC clause and its Reference row, the per-kind design-principles table in
     ARCHITECTURE.md with the seam named on both sides for every deployed kind, the base-rulebook
     node's owns cell, the matrix row, the versioned founding-question set, adoption's orient, and the
     pack's own host profile. The document homes land in the fenced core documents, so the tests
     pointing at them stay red until those blocks are applied.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

from conftest import ROOT, read, read_flat

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)

SCRIPT = os.path.join(ROOT, "guardrails", "check-config-surface.py")
CONFIG = os.path.join(ROOT, "guardrails", "config-surface.json")

DEPLOYED_ROWS = ("frontend / visual", "code / backend service")
BOTH_SIDES = (
    "reach production by a deploy of configuration alone",
    "behaviour and structure stay in the code",
)


def run(*args, **kw):
    env = dict(os.environ)
    env.update(kw.pop("env", {}))
    return subprocess.run(["python3", SCRIPT, *args], capture_output=True, text=True, env=env)


def write(tmp, name, body):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    return p


# --- the fixture hosts: a deployed kind, a kind that deploys nothing, a half-founded kind ---

FIXTURE_DEPLOYED = """# Host profile — a photo site

- `project.kind: photo portfolio (fullstack, static-first)`
- `project.layers: content · rendering engine · deployment`
- `project.proofs: a byte-diff of the baked output · the owner's eye-walk`
- `project.config-surface: the experiment switches, the visitor-facing copy, and the wallpaper
  budget live in `site-config.json`, read by the deployed page at load; the owner edits that file
  and runs the configuration deploy, which publishes it with no build. Behaviour, layout, and every
  new element stay in the code the build ships.`
"""

FIXTURE_NONE = """# Host profile — a skill pack

- `project.kind: skill pack`
- `project.layers: the rulebook and spec · the working skills · the guardrails, templates, and suite`
- `project.proofs: the pytest suite · deed proofs · the owner's read`
- `project.config-surface: none — nothing of this project is deployed; the product is the text a
  session reads, and every change reaches its reader through a release.`
"""

FIXTURE_SILENT = """# Host profile — a half-founded photo site

- `project.kind: photo portfolio (fullstack, static-first)`
- `project.layers: content · rendering engine · deployment`
- `project.proofs: a byte-diff of the baked output · the owner's eye-walk`
"""

FIXTURE_CONTRADICTION = """# Host profile — a deployed site claiming nothing to turn

- `project.kind: fullstack app`
- `project.layers: frontend · backend · deployment`
- `project.proofs: unit tests · the owner's walk`
- `project.config-surface: none`
"""

FIXTURE_EMPTY = """# Host profile — an empty declaration

- `project.kind: fullstack app`
- `project.layers: frontend · backend · store`
- `project.config-surface:`
"""

FIXTURE_NO_KIND = """# Host profile — no kind recorded yet

- `language.docs: English`
"""


class TestConfigSurfaceCheck(unittest.TestCase):
    def test_script_exists_and_executable(self):
        self.assertTrue(os.path.isfile(SCRIPT), "missing script: %s" % SCRIPT)
        self.assertTrue(os.access(SCRIPT, os.X_OK), "%s not executable" % SCRIPT)

    def test_config_ships_beside_the_check(self):
        self.assertTrue(os.path.isfile(CONFIG), "missing config: %s" % CONFIG)
        cfg = json.load(open(CONFIG, encoding="utf-8"))
        for key in ("declaration_key", "kind_key", "layers_key", "none_answers", "deploy_words"):
            self.assertIn(key, cfg, "the config declares no %s" % key)

    def test_deployed_host_declaring_its_surface_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "profile.md", FIXTURE_DEPLOYED)
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_kind_with_no_config_surface_line_reds(self):
        """The row's own done-when: a deployed kind that declares no configuration surface reds."""
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "profile.md", FIXTURE_SILENT)
            r = run(p)
            self.assertNotEqual(r.returncode, 0, "silence must red: " + r.stdout)
            self.assertIn("project.config-surface", r.stdout)

    def test_explicit_none_passes_for_a_project_that_deploys_nothing(self):
        """The crux, the shape the axes check already holds: an explicit "none" IS present text, so
        the presence arm passes it while true silence reds."""
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "profile.md", FIXTURE_NONE)
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_none_against_a_declared_deployment_layer_reds(self):
        """The teeth past presence: a "none" that contradicts the host's OWN declared layers reds,
        and the report quotes both lines."""
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "profile.md", FIXTURE_CONTRADICTION)
            r = run(p)
            self.assertNotEqual(r.returncode, 0, "a contradicted none must red: " + r.stdout)
            self.assertIn("project.layers", r.stdout)
            self.assertIn("project.config-surface", r.stdout)

    def test_empty_declaration_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "profile.md", FIXTURE_EMPTY)
            r = run(p)
            self.assertNotEqual(r.returncode, 0, "an empty declaration must red: " + r.stdout)

    def test_profile_with_no_kind_passes(self):
        """A profile recording no kind has no founding to complete — the axes check's own boundary."""
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "profile.md", FIXTURE_NO_KIND)
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_profile_reds(self):
        """A gate that cannot read its subject reds, never passes silently (INV-47's shape)."""
        with tempfile.TemporaryDirectory() as tmp:
            missing = os.path.join(tmp, "no-such-profile.md")
            r = run(missing)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("check-config-surface", r.stdout)
            self.assertIn("no-such-profile.md", r.stdout, "the red does not name the file it wanted")

    def test_missing_config_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "profile.md", FIXTURE_DEPLOYED)
            r = run(p, env={"CONFIG_SURFACE_JSON": os.path.join(tmp, "no-such-config.json")})
            self.assertNotEqual(r.returncode, 0, "a missing config must red: " + r.stdout)
            self.assertIn("check-config-surface", r.stdout)
            self.assertIn("no-such-config.json", r.stdout, "the red does not name the config it wanted")

    def test_green_run_states_its_reach(self):
        """Every gate in this family states its reach on the green line (SPEC INV-269)."""
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "profile.md", FIXTURE_DEPLOYED)
            r = run(p)
            self.assertIn("reach:", r.stdout)
            for needle in ("project.kind", "project.layers", "project.config-surface"):
                self.assertIn(needle, r.stdout, "the reach line names no %s record" % needle)

    def test_live_host_profile_passes_the_check_it_ships(self):
        r = run(os.path.join(ROOT, ".live-spec", "profile.md"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestConfigSurfaceLaw(unittest.TestCase):
    def test_spec_states_the_law(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("A deployed kind declares what its owner changes without a build", spec)
        self.assertIn("[INV-291]", spec)

    def test_spec_reference_row(self):
        spec = read("PRODUCT_SPEC.md")
        row = next((l for l in spec.splitlines() if l.startswith("| INV-291 |")), "")
        self.assertTrue(row, "INV-291 has no row in the generated Reference table")

    def test_architecture_names_the_seam_for_every_deployed_kind(self):
        """The per-kind design-principles table carries the principle for every deployed kind, with
        the seam named on both sides."""
        arch = read("ARCHITECTURE.md")
        marker = "## Design principles by project.kind"
        self.assertIn(marker, arch, "ARCHITECTURE has no design-principles section")
        section = arch.split(marker, 1)[1].split("\n## ", 1)[0]
        flat_rows = {}
        for line in section.splitlines():
            for kind in DEPLOYED_ROWS:
                if line.startswith("| " + kind):
                    flat_rows[kind] = " ".join(line.split())
        for kind in DEPLOYED_ROWS:
            self.assertIn(kind, flat_rows, "the design-principles table has no row for '%s'" % kind)
            for needle in BOTH_SIDES:
                self.assertIn(needle, flat_rows[kind],
                              "the '%s' row does not name the seam's side: %s" % (kind, needle))

    def test_architecture_states_which_kinds_are_deployed(self):
        arch = read_flat("ARCHITECTURE.md")
        self.assertIn("A kind is deployed when its product runs where its readers reach it", arch)
        self.assertIn("INV-291", arch)

    def test_architecture_owns_the_invariant(self):
        nodes = archformat.parse_nodes(read("ARCHITECTURE.md"))
        base = next((n for n in nodes if n.name == "base-rulebook"), None)
        self.assertIsNotNone(base, "ARCHITECTURE.md carries no base-rulebook node")
        self.assertIn("INV-291", base.anchors_expanded, "base-rulebook does not own INV-291")

    def test_matrix_row_covers_the_law(self):
        mat = read("TEST_MATRIX.md")
        row = next((l for l in mat.splitlines() if l.startswith("| M-467 |")), "")
        self.assertTrue(row, "TEST_MATRIX has no M-467 row")
        self.assertIn("INV-291", row)

    def test_founding_questions_names_the_config_surface_question(self):
        man = json.load(open(os.path.join(ROOT, "scripts", "founding-questions.json"),
                             encoding="utf-8"))
        qs = [q for q in man.get("questions", []) if "project.config-surface" in (q.get("key") or "")]
        self.assertTrue(qs, "founding-questions.json carries no project.config-surface question")
        self.assertIn("INV-291", " ".join(q.get("anchor", "") for q in qs),
                      "the configuration-surface founding question does not anchor to INV-291")

    def test_adopt_founding_prompts_the_config_surface(self):
        adopt = read_flat("adopt/ADOPT.md")
        self.assertIn("project.config-surface", adopt)
        self.assertIn("INV-291", adopt)

    def test_live_profile_declares_its_own_config_surface(self):
        """The pack's own host profile answers the founding question it ships."""
        profile = read(".live-spec/profile.md")
        self.assertRegex(profile, r"(?m)^\s*[-*]?\s*`?project\.config-surface:",
                         "live-spec's own host profile declares no configuration surface")


if __name__ == "__main__":
    unittest.main(verbosity=2)
