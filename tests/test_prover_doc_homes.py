"""The prover doc's reader-facing homes — outside adversarial review, 2026-07-16.

The frontmatter description carries only the autoload trigger; the prover/design-reviewer
boundary is homed in "When NOT to use" (the modes paragraph points at it); the
paired-transition kind-split lives in its lens, and the KIND block stays general.
Red-proven against the pre-restructure file (HEAD before commit 2cca664)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "product-prover" / "SKILL.md"


def _skill():
    return SKILL.read_text(encoding="utf-8")


def _description():
    for line in _skill().splitlines():
        if line.startswith("description:"):
            return line
    raise AssertionError("prover SKILL.md lost its frontmatter description line")


def test_description_carries_only_the_trigger():
    d = _description()
    assert "design-reviewer" not in d, "description carries the sibling pass again — trigger noise"
    assert "INV-141" not in d, "description carries an anchor code — trigger noise"
    assert "hold together as written" in d, "description lost the question the skill answers"


def test_boundary_homed_in_when_not_to_use():
    s = _skill()
    start = s.index("## When NOT to use")
    end = s.index("## ", start + 5)
    section = s[start:end]
    assert "design-reviewer's own pass [INV-141]" in section, \
        "the prover/design-reviewer boundary left its one home"
    assert "This pass verifies the document." in section


def test_kind_block_stays_general_split_lives_in_lens():
    s = _skill()
    kind_block = s[s.index("`KIND` — the finding's verdict"):s.index("`CATEGORY` —")]
    assert "one-sided pair" not in kind_block, \
        "the paired-transition family split leaked back into the KIND block"
    lens_start = s.index("**Paired-transition symmetry**")
    lens_end = s.index("**Persistence and versions**")
    lens = s[lens_start:lens_end]
    assert "declared one-sided pair" in lens and "open motion question" in lens, \
        "the family's kind-split left its lens home"
