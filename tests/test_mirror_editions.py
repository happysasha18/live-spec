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

    def test_an_edition_with_no_skill_file_publishes_nothing(self):
        """The copy step deletes what it replaces, so a half-made edition would empty the public
        repository and leave it shipping nothing. Both the attribution stamp and the language scan
        return 0 on a missing file, so nothing downstream would catch it."""
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._scratch_pack(tmp, skills=["alpha"], editions=[])
            os.makedirs(os.path.join(pack, "editions", "alpha"))  # the directory, with no SKILL.md
            code, out, err = publish_source(pack, "alpha")
            self.assertNotEqual(code, 0, "a half-made edition must refuse rather than publish")
            self.assertEqual(out, "", "it names no source at all")
            self.assertIn("SKILL.md", err, "the refusal says what is missing")

    def test_a_refused_edition_never_falls_back_to_the_skill(self):
        """Falling back would publish the internal copy under the reader's nose, silently undoing
        the edition. The refusal stops this one mirror and says so."""
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._scratch_pack(tmp, skills=["alpha"], editions=[])
            os.makedirs(os.path.join(pack, "editions", "alpha"))
            self.assertNotIn("skills", publish_source(pack, "alpha")[1])

    def test_one_half_made_edition_leaves_its_neighbours_publishable(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._scratch_pack(tmp, skills=["alpha", "beta"], editions=["beta"])
            os.makedirs(os.path.join(pack, "editions", "alpha"))
            self.assertNotEqual(publish_source(pack, "alpha")[0], 0)
            self.assertEqual(publish_source(pack, "beta")[1],
                             os.path.join(pack, "editions", "beta"))

    def test_the_loop_skips_a_refused_edition_and_runs_on(self):
        """One broken edition leaves every other mirror to sync."""
        with open(SCRIPT, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn('if ! publish_src="$(publish_source_for "$skill_name")"; then', text,
                      "the loop must read the refusal")
        refusal = text.index('if ! publish_src=')
        self.assertIn("continue", text[refusal:refusal + 400],
                      "a refused edition moves to the next skill rather than ending the run")

    def test_the_flag_names_the_skill_it_needs(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._scratch_pack(tmp, skills=["alpha"], editions=[])
            result = subprocess.run(
                ["bash", os.path.join(pack, "scripts", "sync-mirrors.sh"),
                 "--print-publish-source"],
                capture_output=True, text=True, timeout=60)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("SKILL-NAME", result.stdout + result.stderr)


class TestAnEditionStaysAsNewAsItsSkill(unittest.TestCase):
    """Nothing ties an edition to the skill it mirrors, so a repair landing in skills/<name>/ leaves
    the edition behind and the sync publishes the older text without a word. That happened the day
    the mechanism shipped: eleven missing inputs were added to the prover skill and the edition never
    got them. The choice now compares the newest commit on each side.
    """

    def _git(self, cwd, *args, when=None):
        # The choice reads the COMMITTER date (%ct), so that is the one the test has to move.
        env = dict(os.environ,
                   GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        if when:
            env["GIT_AUTHOR_DATE"] = when
            env["GIT_COMMITTER_DATE"] = when
        return subprocess.run(["git", "-C", cwd] + list(args),
                              capture_output=True, text=True, env=env, timeout=60)

    def _pack(self, tmp, order):
        """A scratch pack whose two sides are committed in the given order, one second apart."""
        os.makedirs(os.path.join(tmp, "scripts"))
        shutil.copy(SCRIPT, os.path.join(tmp, "scripts", "sync-mirrors.sh"))
        for rel in ("skills/alpha", "editions/alpha"):
            os.makedirs(os.path.join(tmp, rel))
            with open(os.path.join(tmp, rel, "SKILL.md"), "w") as fh:
                fh.write("body\n")
        self._git(tmp, "init", "-q")
        for i, side in enumerate(order):
            when = "2026-01-01T00:%02d:00" % (10 + i * 30)
            self._git(tmp, "add", "--", side)
            self._git(tmp, "-c", "user.email=t@t", "-c", "user.name=t",
                      "commit", "-q", "-m", side, when=when)
        return tmp

    def test_an_edition_older_than_its_skill_publishes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._pack(tmp, ["editions/alpha", "skills/alpha"])
            code, out, err = publish_source(pack, "alpha")
            self.assertNotEqual(code, 0, "a stale edition must refuse rather than publish")
            self.assertEqual(out, "")
            self.assertIn("older than", err)

    def test_an_edition_as_new_as_its_skill_publishes(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._pack(tmp, ["skills/alpha", "editions/alpha"])
            code, out, _ = publish_source(pack, "alpha")
            self.assertEqual(code, 0)
            self.assertEqual(out, os.path.join(pack, "editions", "alpha"))

    def test_the_refusal_never_falls_back_to_the_internal_copy(self):
        """Falling back would publish the internal text under the reader's nose."""
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._pack(tmp, ["editions/alpha", "skills/alpha"])
            self.assertNotIn("skills", publish_source(pack, "alpha")[1])


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

    def test_a_refusal_ends_the_run_non_zero(self):
        """The summary line alone left the run exiting zero, so a half-made edition read as a clean
        sync. Every other mirror has already synced by the time this is decided, so the exit code
        reports what was left behind while keeping the work that succeeded."""
        with open(SCRIPT, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn('REFUSED+=("$skill_name")', text,
                      "a refused skill must be recorded, beyond the summary line")
        self.assertIn('if [ "${#REFUSED[@]}" -gt 0 ]; then', text,
                      "the run must read that record before it ends")
        tail = text[text.index('if [ "${#REFUSED[@]}" -gt 0 ]; then'):]
        self.assertIn("exit 1", tail, "a refusal must end the run non-zero")
        # The check stands after the loop, so one refusal never stops the mirrors behind it.
        self.assertLess(text.index("published nothing"), len(text))
        self.assertGreater(text.index('if [ "${#REFUSED[@]}" -gt 0 ]; then'),
                           text.index("== summary =="),
                           "the refusal check belongs after every mirror has had its turn")

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
