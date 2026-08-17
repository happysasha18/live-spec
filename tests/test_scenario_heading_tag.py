"""Every person-facing scenario heading carries its feature tag — INV-132 (row 283, prover F4),
re-aimed at the requirements format (row 445, pass 2).

The convention moved with the format: a scenario is a `## Requirement N: ...` heading (H2) carrying a
trailing `[feature: F-x]` tag; an untagged requirement is machinery or reference, and the old
`[not a scenario]` marker retired with the prose shape (the pass-2 intro states the convention: "a
requirement whose heading carries a `[feature: F-...]` tag is a person-facing scenario"). The
forgotten-tag net is two-layered now:
  - every F-code lives ONLY on a `## Requirement` heading (the wave's F6 rule: no F-code rides a
    criterion or User Story bracket) — checked mechanically here, since a tag that slid into a body
    bracket is exactly a forgotten heading tag;
  - a promised feature with no tagged heading reds in the feature-coverage two-way trace
    (test_traceability::TestFeatureCoverage, reading ARCHITECTURE.md's coverage table) — the
    successor of the old H3 tag-or-marker sweep, named as this file's replacement pair.

KNOWN RED, kept deliberately: the spec's own INV-132 criteria (R224.3/R224.4) still say "third-level
heading ... or a not-a-scenario marker" — the pre-format convention — contradicting the intro and the
document's practice (tags on H2, no markers, every H3 a uniform `### Acceptance Criteria`). That
wording is a conversion leftover; test_spec_criteria_match_the_practiced_convention below stays red
until the spec author reconciles R224, and REPIN-LOG.md carries the defect's story.
"""

import os
import re
import unittest

from conftest import ROOT, read, read_flat, read_all_flat


def heading_tag_gaps(spec_text):
    """Two mechanical checks on the practiced convention (SPEC INV-132, the pass-2 shape):
      - a `## Requirement` heading whose bracket tail LOOKS like a feature tag but is malformed
        (e.g. `[feature: x]`, `[feature F-x]`) — a tag that will silently drop out of the trace;
      - an F-code appearing in a bracket anywhere OUTSIDE a `## Requirement` heading line — a
        scenario tag that slid into a criterion or User Story bracket, the forgotten-heading-tag
        shape the wave's F6 rule bans.
    Returns the offending lines."""
    gaps = []
    for line in spec_text.splitlines():
        if line.startswith("## Requirement"):
            if "[feature" in line and not re.search(
                    r"\[feature:\s*F-[a-z0-9-]+(?:\s*,\s*F-[a-z0-9-]+)*\s*\]\s*$", line.strip()):
                gaps.append("malformed tag: %s" % line.strip())
        else:
            for m in re.finditer(r"\bF-[a-z0-9][a-z0-9-]*\b", line):
                if re.search(r"\[[^\]]*\b%s\b[^\]]*\]" % re.escape(m.group(0)), line):
                    gaps.append("F-code outside a requirement heading: %s" % line.strip()[:100])
                    break
    return gaps


class TestScenarioHeadingTag(unittest.TestCase):
    def test_every_feature_tag_sits_well_formed_on_a_heading(self):
        gaps = heading_tag_gaps(read("PRODUCT_SPEC.md"))
        self.assertEqual(gaps, [],
                         "feature tags off their headings or malformed (SPEC INV-132): %s" % gaps)

    def test_the_checker_catches_the_seeded_defects(self):
        """The never side, permanent: a malformed heading tag and a body-bracket F-code are caught,
        and a properly tagged heading is spared."""
        spec = read("PRODUCT_SPEC.md")
        malformed = spec + "\n## Requirement 999: A broken tag  [feature: demo]\n"
        self.assertTrue(any("malformed" in g for g in heading_tag_gaps(malformed)),
                        "the checker missed a malformed heading tag — no teeth")
        slid = spec + "\n1. The system *shall* do a thing. [F-demo, INV-1]\n"
        self.assertTrue(any("outside a requirement heading" in g for g in heading_tag_gaps(slid)),
                        "the checker missed an F-code riding a body bracket — no teeth")
        tagged = spec + "\n## Requirement 999: A real scenario  [feature: F-demo]\n"
        self.assertEqual([g for g in heading_tag_gaps(tagged) if "999" in g], [],
                         "the checker flagged a properly feature-tagged heading")

    def test_spec_states_heading_convention(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("a requirement whose heading carries a `[feature: F-...]` tag is a "
                      "person-facing scenario", spec,
                      "the intro lost the practiced heading convention")
        self.assertIn("[INV-132]", spec)

    def test_spec_criteria_match_the_practiced_convention(self):
        """KNOWN RED (row-445 conversion leftover, see REPIN-LOG DEFECT 1): R224's INV-132 criteria
        still describe the retired H3 tag-or-marker convention. Goes green when the spec author
        moves them to the practiced one — the requirement heading carries the tag."""
        inv132_lines = [l for l in read("PRODUCT_SPEC.md").splitlines()
                        if "[INV-132" in l and l.lstrip()[:1].isdigit()]
        self.assertTrue(inv132_lines, "INV-132 carries no body criterion")
        self.assertTrue(any("requirement heading" in l for l in inv132_lines),
                        "INV-132's criteria still state the retired third-level-heading convention "
                        "rather than the practiced requirement-heading tag (R224.3/R224.4)")

    def test_formal_index_row(self):
        # locations only (SPEC INV-271): the row proves INV-132 is carried by a body criterion.
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| INV-132 |"):
                    self.assertRegex(line, r"R\d+\.\d+")
                    return
        self.fail("INV-132 index row missing")

    def test_spec_author_carries_heading_convention(self):
        sa = read_all_flat("skills/spec-author/SKILL.md")
        self.assertIn("[not a scenario]", sa)
        self.assertIn("untagged, unmarked requirement heading is unambiguously red", sa)


if __name__ == "__main__":
    unittest.main(verbosity=2)
