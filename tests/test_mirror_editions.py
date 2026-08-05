"""A skill's public mirror ships its public edition where one exists (2026-08-05).

A skill's copy under skills/ is written for a session that has already loaded this pack. It cites
internal codes as its authority and points at scripts and tests that travel with the pack. Read by a
stranger those codes resolve to nothing. On 2026-08-05 the public prover mirror was found shipping
that internal copy at 62 KB, published by the pack's own sync on every push.

A skill may ship a public edition under editions/<skill>/ with every internal code resolved into the
plain rule it stands for. Where that directory exists it is what the mirror publishes, and
skills/<skill>/ stays the copy this project loads. The pack stays the single source of truth for
both, so a hand edit made directly on a mirror is still overwritten by the next sync.

Extends the attribution and mirror mechanism (SPEC INV-96) and the push gate (SPEC M-6).
"""
import os
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT

SCRIPT = os.path.join(ROOT, "scripts", "sync-mirrors.sh")


def publish_source(pack_root, skill_name):
    """What the sync would publish for one skill, read out of the script itself."""
    result = subprocess.run(
        ["bash", os.path.join(pack_root, "scripts", "sync-mirrors.sh"),
         "--print-publish-source", skill_name],
        capture_output=True, text=True, timeout=60)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


class TestPublishSourceSelection(unittest.TestCase):
    """The choice runs in a scratch pack, so the real tree's contents never decide the answer."""

    def _scratch_pack(self, tmp, skills, editions):
        os.makedirs(os.path.join(tmp, "scripts"))
        shutil.copy(SCRIPT, os.path.join(tmp, "scripts", "sync-mirrors.sh"))
        for name in skills:
            os.makedirs(os.path.join(tmp, "skills", name))
            with open(os.path.join(tmp, "skills", name, "SKILL.md"), "w") as fh:
                fh.write("the copy this project loads\n")
        for name in editions:
            os.makedirs(os.path.join(tmp, "editions", name))
            with open(os.path.join(tmp, "editions", name, "SKILL.md"), "w") as fh:
                fh.write("the copy a stranger reads\n")
        return tmp

    def test_a_skill_with_no_edition_publishes_its_own_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._scratch_pack(tmp, skills=["alpha"], editions=[])
            code, out, err = publish_source(pack, "alpha")
            self.assertEqual(code, 0, err)
            self.assertEqual(out, os.path.join(pack, "skills", "alpha"))

    def test_a_skill_with_an_edition_publishes_the_edition(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._scratch_pack(tmp, skills=["alpha"], editions=["alpha"])
            code, out, err = publish_source(pack, "alpha")
            self.assertEqual(code, 0, err)
            self.assertEqual(out, os.path.join(pack, "editions", "alpha"),
                             "an edition exists, so it is what goes public")

    def test_one_skill_s_edition_leaves_its_neighbours_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._scratch_pack(tmp, skills=["alpha", "beta"], editions=["alpha"])
            self.assertEqual(publish_source(pack, "alpha")[1],
                             os.path.join(pack, "editions", "alpha"))
            self.assertEqual(publish_source(pack, "beta")[1],
                             os.path.join(pack, "skills", "beta"),
                             "a skill with no edition of its own is unaffected")

    def test_the_flag_names_the_skill_it_needs(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._scratch_pack(tmp, skills=["alpha"], editions=[])
            result = subprocess.run(
                ["bash", os.path.join(pack, "scripts", "sync-mirrors.sh"),
                 "--print-publish-source"],
                capture_output=True, text=True, timeout=60)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("SKILL-NAME", result.stdout + result.stderr)


class TestTheSyncUsesTheChoice(unittest.TestCase):
    """The selection is wired into the copy step, so it decides what actually reaches a mirror."""

    def test_the_copy_step_reads_the_selected_source(self):
        with open(SCRIPT, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn('publish_src="$(publish_source_for "$skill_name")"', text,
                      "the loop must ask for the publish source")
        self.assertIn('rsync -a --delete --exclude=\'.git\' "$publish_src/" "$mirror_dir/"', text,
                      "the copy step must read the selected source")
        self.assertNotIn('rsync -a --delete --exclude=\'.git\' "$skill_path" "$mirror_dir/"', text,
                         "the old copy step bypassed the choice and must be gone")

    def test_the_flag_touches_no_repository(self):
        """The print flag stands above every clone and every push, so a test never reaches GitHub."""
        with open(SCRIPT, encoding="utf-8") as fh:
            text = fh.read()
        flag = text.index("--print-publish-source")
        for reaching in ("gh repo clone", "git clone", "git push"):
            self.assertLess(flag, text.index(reaching),
                            "the print flag must exit before anything reaches a repository")


if __name__ == "__main__":
    unittest.main()
