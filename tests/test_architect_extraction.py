"""architect stands as a real, pointed-to, standalone skill (2026-08-24 extraction).

Commit 3cc8b47f extracted the architecture step of `skills/build-pipeline/SKILL.md` into a
standalone `skills/architect/SKILL.md`, repointed `skills/director/SKILL.md`'s specialist table
at it, and added a "`skills/…` cell vs `references/…` cell" convention paragraph explaining what
that table's two kinds of cell mean. `tests/test_skill_count_agrees.py` already holds the bare
*number* every "how many working skills" home states, but names nothing about which skills those
homes actually list, and does not read `skills/director/SKILL.md`'s specialist table at all — so
a name dropped from a roster, or a specialist table left pointing at the old
`skills/build-pipeline`-pending placeholder, would pass that test untouched. This test pins the
concrete facts this extraction established, so a later edit that quietly drops `architect` from a
roster, or repoints the specialist table back at a placeholder, reds here.

This test does NOT re-judge whether the extraction was the right call, or whether
`skills/architect/SKILL.md`'s body is good prose — that is `docs/skill-review/
2026-08-24-architect-extraction.md`'s job, already done. It holds the structural floor after the
fact.
"""
import os
import re
import unittest

from conftest import ROOT, read, read_flat

ARCHITECT_SKILL = os.path.join("skills", "architect", "SKILL.md")
DIRECTOR_SKILL = os.path.join("skills", "director", "SKILL.md")
LIVE_SPEC_BASE_SKILL = os.path.join("skills", "live-spec-base", "SKILL.md")


class TestArchitectSkillLoads(unittest.TestCase):
    def test_the_skill_file_exists(self):
        self.assertTrue(
            os.path.isfile(os.path.join(ROOT, ARCHITECT_SKILL)),
            "skills/architect/SKILL.md is missing",
        )

    def test_frontmatter_names_and_versions_the_skill(self):
        body = read(ARCHITECT_SKILL)
        self.assertTrue(body.startswith("---\n"), "architect's SKILL.md carries no frontmatter")
        front = body.split("---\n", 2)[1]
        self.assertRegex(front, r"(?m)^name:\s*architect\s*$")
        self.assertRegex(front, r"(?m)^\s*version:\s*5\.0\.0\s*$")

    def test_description_states_a_standalone_invocable_task(self):
        # The skill review's own claim: "'Here's a proven spec, produce or update the
        # architecture' is a complete task on its own — invoke this skill directly." Pinned
        # here so a later edit cannot quietly fold this back into a pipeline-only framing.
        flat = read_flat(ARCHITECT_SKILL)
        self.assertIn("invoke this skill directly", flat)


class TestDirectorPointsAtTheRealSkill(unittest.TestCase):
    def test_specialist_table_names_architect_skill_directly(self):
        flat = read_flat(DIRECTOR_SKILL)
        self.assertIn("| Architect |", flat.replace("|Architect|", "| Architect |"))
        self.assertIn("skills/architect", flat)
        # The pre-extraction placeholder must be gone, not merely joined by the new pointer.
        self.assertNotIn("pending this package's own architect-step decision", flat)

    def test_states_the_skills_vs_references_cell_convention(self):
        flat = read_flat(DIRECTOR_SKILL)
        self.assertIn("standalone skill the Director invokes on its own", flat)


class TestRostersNameArchitect(unittest.TestCase):
    def test_readme_skill_roster_names_architect(self):
        flat = read_flat("README.md")
        self.assertIn("[`architect`](skills/architect/)", flat)

    def test_live_spec_base_closing_roster_names_architect(self):
        flat = read_flat(LIVE_SPEC_BASE_SKILL)
        self.assertRegex(flat, r"\*\*architect\*\*\s+writes or updates the")

    def test_live_spec_base_description_lists_architect(self):
        body = read(LIVE_SPEC_BASE_SKILL)
        front = body.split("---\n", 2)[1]
        desc = re.search(r"(?m)^description:.*$", front)
        self.assertIsNotNone(desc, "live-spec-base's frontmatter lost its description line")
        self.assertIn("architect", desc.group(0))


if __name__ == "__main__":
    unittest.main()
