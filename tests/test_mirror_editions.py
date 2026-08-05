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


def publish_source(pack_root, skill_name, env=None):
    """What the sync would publish for one skill, read out of the script itself.

    `env` overrides single environment variables for the child. A value of None removes the
    variable, so a test can prove what happens with the freshness escape hatch unset.
    """
    child_env = dict(os.environ)
    for key, value in (env or {}).items():
        if value is None:
            child_env.pop(key, None)
        else:
            child_env[key] = value
    result = subprocess.run(
        ["bash", os.path.join(pack_root, "scripts", "sync-mirrors.sh"),
         "--print-publish-source", skill_name],
        capture_output=True, text=True, timeout=60, env=child_env)
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
        """One broken edition leaves every other mirror to sync. The loop captures the refusal's
        status rather than testing it with `if !`, which would invert it before it could be read."""
        with open(SCRIPT, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn('publish_src="$(publish_source_for "$skill_name")" || refusal_status=$?', text,
                      "the loop must read the refusal and keep its status")
        refusal = text.index('publish_src="$(publish_source_for "$skill_name")" || refusal_status=$?')
        self.assertIn("continue", text[refusal:refusal + 800],
                      "a refused edition moves to the next skill rather than ending the run")
        self.assertNotIn('if ! publish_src=', text,
                         "`if !` throws the status away, and each refusal reports its own reason")

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
        """Falling back would publish the internal text under the reader's nose.

        The test above already proves a stale refusal's stdout is empty, so asserting the fallback's
        absence against that same stdout would pass on nothing at all. This reads real output
        instead. The same pack committed the other way round prints a path on stdout, which proves
        the channel carries one; the stale run's whole output, stdout and stderr together, then
        names no internal directory as a source and says why it refused.
        """
        with tempfile.TemporaryDirectory() as tmp:
            fresh = self._pack(os.path.join(tmp, "fresh"), ["skills/alpha", "editions/alpha"])
            code, out, err = publish_source(fresh, "alpha")
            self.assertEqual(code, 0, err)
            self.assertEqual(out, os.path.join(fresh, "editions", "alpha"),
                             "stdout does carry a publish path when one is published")

            stale = self._pack(os.path.join(tmp, "stale"), ["editions/alpha", "skills/alpha"])
            code, out, err = publish_source(stale, "alpha")
            self.assertNotEqual(code, 0, "the stale edition must refuse")
            self.assertNotIn(os.path.join(stale, "skills", "alpha"), out + err,
                             "no surface offers the internal copy as the source instead")
            self.assertIn("older than", err, "and the refusal says why it refused")

    def test_a_stale_refusal_is_never_reported_as_a_missing_skill_file(self):
        """Every refusal used to be reported as an edition holding no SKILL.md, so the one remedy a
        reader was given could not fix a stale edition."""
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._pack(tmp, ["editions/alpha", "skills/alpha"])
            code, out, err = publish_source(pack, "alpha")
            self.assertNotEqual(code, 0)
            self.assertNotIn("holds no SKILL.md", out + err,
                             "a stale edition is reported as stale, not as a missing file")
            self.assertIn("Carry the skill's newer work into the edition", err,
                          "and it carries the remedy that actually fixes it")

    def test_the_freshness_escape_hatch_is_unset_in_a_normal_run(self):
        """SKIP_EDITION_FRESHNESS=1 turns the staleness refusal off. It exists for a deliberate
        one-off publish, and a gate run carrying it would report green on the very drift the
        refusal was added to catch."""
        self.assertNotEqual(os.environ.get("SKIP_EDITION_FRESHNESS"), "1",
                            "this suite must judge the refusal with the escape hatch off")

    def test_a_stale_edition_refuses_with_the_escape_hatch_unset(self):
        """The refusal is proved with the variable removed from the child's environment, so an
        exported value in the shell running the suite can never make this pass."""
        with tempfile.TemporaryDirectory() as tmp:
            pack = self._pack(tmp, ["editions/alpha", "skills/alpha"])
            code, out, err = publish_source(pack, "alpha",
                                            env={"SKIP_EDITION_FRESHNESS": None})
            self.assertNotEqual(code, 0, "with the hatch unset a stale edition publishes nothing")
            self.assertEqual(out, "")
            self.assertIn("older than", err)

    def test_the_escape_hatch_reaches_the_staleness_check_alone(self):
        """Set to 1 it publishes a stale edition, and that is its whole reach: a half-made edition
        is still refused, because emptying the public repository is not what the hatch is for."""
        with tempfile.TemporaryDirectory() as tmp:
            stale = self._pack(os.path.join(tmp, "stale"), ["editions/alpha", "skills/alpha"])
            code, out, err = publish_source(stale, "alpha", env={"SKIP_EDITION_FRESHNESS": "1"})
            self.assertEqual(code, 0, err)
            self.assertEqual(out, os.path.join(stale, "editions", "alpha"))

            half = self._pack(os.path.join(tmp, "half"), ["skills/alpha", "editions/alpha"])
            os.remove(os.path.join(half, "editions", "alpha", "SKILL.md"))
            code, out, err = publish_source(half, "alpha", env={"SKIP_EDITION_FRESHNESS": "1"})
            self.assertNotEqual(code, 0, "the hatch never reaches the missing-SKILL.md refusal")
            self.assertIn("SKILL.md", err)


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

    def test_each_refusal_reports_its_own_reason_and_remedy(self):
        """The summary line and the closing block both printed one hardcoded case — an edition
        holding no SKILL.md — for every refusal, staleness among them, while the stale edition's
        true remedy reached stderr alone. Both surfaces now read the reason and the remedy from the
        refusal's own status, and both live in one home so no surface can drift from the message
        printed where the refusal happened."""
        with open(SCRIPT, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn('SUMMARY_LINES+=("${skill_name}: skipped (${refusal_reason})")', text,
                      "the summary line names the refusal that actually happened")
        self.assertIn('REFUSAL_NOTES+=("${skill_name}: ${refusal_reason}. ${refusal_remedy}")', text,
                      "each refusal records its own reason and remedy for the closing block")
        tail = text[text.index('if [ "${#REFUSED[@]}" -gt 0 ]; then'):]
        self.assertIn('for note in "${REFUSAL_NOTES[@]}"', tail,
                      "the closing block prints the note each refusal wrote")
        self.assertNotIn("Each has an editions/<skill>/ directory holding no SKILL.md.", text,
                         "the hardcoded one-case reason must be gone from the closing block")
        for once in ('editions/${name}/ is older than skills/${name}/',
                     'editions/${name}/ holds no SKILL.md'):
            self.assertEqual(text.count(once), 1,
                             "each refusal's words are written once, in refusal_reason_for")

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
