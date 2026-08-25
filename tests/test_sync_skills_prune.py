"""sync-skills.sh must mirror the repo exactly, including deletions.

Found 2026-08-25 during the build-pipeline cutover's first slice: `scripts/sync-skills.sh`
used `cp -r` to update the installed copy, which never removes a file that left the source
skill directory. Moving 4 reference files out of `skills/build-pipeline/references/` left
stale copies of those same 4 files sitting in the installed mirror, so `diff -rq` (the same
comparison `guardrails/check-config-health.sh`'s gate m runs) never reached equality and the
gate reds "installed skill drifted from source" even right after a sync.
"""
import os
import shutil
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNC = os.path.join(REPO, "scripts", "sync-skills.sh")


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def _scratch_sync(tmp):
    # sync-skills.sh resolves its source as "../skills" relative to its OWN path
    # (dirname "$0"), never the caller's cwd — so a scratch run needs its own copy of the
    # script sitting beside a scratch skills/ dir, not just a scratch cwd.
    dst = os.path.join(tmp, "scripts", "sync-skills.sh")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(SYNC, dst)
    return dst


class TestSyncSkillsPrunesRemovedFiles(unittest.TestCase):
    def test_a_file_removed_from_source_is_removed_from_the_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            sync = _scratch_sync(tmp)
            repo_skills = os.path.join(tmp, "skills")
            _write(os.path.join(repo_skills, "foo", "SKILL.md"),
                   "---\nname: foo\nmetadata:\n  version: 1.0.0\n---\nbody\n")
            dest = os.path.join(tmp, "installed")
            # The installed copy already carries a reference file that no longer exists in
            # the source skill dir — the exact shape left behind by a file move/deletion.
            _write(os.path.join(dest, "foo", "SKILL.md"),
                   "---\nname: foo\nmetadata:\n  version: 1.0.0\n---\nbody\n")
            _write(os.path.join(dest, "foo", "references", "gone.md"), "stale\n")

            r = subprocess.run(["bash", sync, dest], cwd=tmp,
                                capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

            self.assertFalse(
                os.path.exists(os.path.join(dest, "foo", "references", "gone.md")),
                "sync-skills.sh left a stale file behind that no longer exists in the source "
                "skill directory — it must mirror deletions, not just additions/edits")

            diff = subprocess.run(["diff", "-rq",
                                    os.path.join(repo_skills, "foo"),
                                    os.path.join(dest, "foo")],
                                   capture_output=True, text=True)
            self.assertEqual(diff.returncode, 0,
                              "installed copy still drifts from source after sync: %s"
                              % (diff.stdout + diff.stderr))

    def test_an_unrelated_installed_skill_is_left_alone(self):
        # sync-skills.sh must prune deletions WITHIN a skill it owns, never touch a skill
        # directory that isn't a source pack skill at all (e.g. an external clone install
        # or a skill this repo doesn't ship) — pruning must not become a wipe of $DEST.
        with tempfile.TemporaryDirectory() as tmp:
            sync = _scratch_sync(tmp)
            repo_skills = os.path.join(tmp, "skills")
            _write(os.path.join(repo_skills, "foo", "SKILL.md"),
                   "---\nname: foo\nmetadata:\n  version: 1.0.0\n---\nbody\n")
            dest = os.path.join(tmp, "installed")
            _write(os.path.join(dest, "foo", "SKILL.md"),
                   "---\nname: foo\nmetadata:\n  version: 1.0.0\n---\nbody\n")
            _write(os.path.join(dest, "unrelated-skill", "SKILL.md"), "not ours\n")

            r = subprocess.run(["bash", sync, dest], cwd=tmp,
                                capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(
                os.path.exists(os.path.join(dest, "unrelated-skill", "SKILL.md")),
                "sync-skills.sh must only mirror skills the source repo ships, "
                "never delete an installed skill absent from this repo's skills/")


if __name__ == "__main__":
    unittest.main()
