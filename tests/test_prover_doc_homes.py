"""The prover doc's reader-facing homes — outside adversarial review, 2026-07-16.

The frontmatter description carries only the autoload trigger; the prover/design-reviewer
boundary is homed in "Work that belongs elsewhere" (the modes paragraph points at it); the
paired-transition kind-split lives in its lens, and the KIND block stays general.
Red-proven against the pre-restructure file (HEAD before commit 2cca664)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "product-prover" / "SKILL.md"
GATE = ROOT / "guardrails" / "check-prover-record.sh"


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
    start = s.index("## Work that belongs elsewhere")
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


def _gate_repair_lines():
    """The gate's own repair lines — the strings it prints to an author, read from the
    echo statements rather than from any comment about them."""
    return [line.strip() for line in GATE.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("echo ") and "PROVER_DIR" in line]


def test_the_record_path_the_skill_prescribes_is_the_one_the_gate_demands():
    """Row 608: the skill sent an author to `docs/prover/YYYY-MM-DD.md` while the gate's
    own repair line named the slug form, so an author who obeyed the skill was refused.
    This pins the two together — either side drifting turns this red."""
    s = _skill()
    assert "docs/prover/YYYY-MM-DD-<slug>.md" in s, \
        "the prover's persist line stopped naming the slug form the gate demands"
    assert "docs/prover/YYYY-MM-DD.md" not in s, \
        "the bare-date form the gate refuses is back in the prover's persist line"
    repairs = _gate_repair_lines()
    assert repairs, "check-prover-record.sh prints no repair line naming its record directory"
    assert any("$TODAY-<slug>.md" in line for line in repairs), \
        "the gate stopped telling an author to write the slug form the skill prescribes"


def test_the_lifecycle_lead_in_counts_the_bullets_that_follow_it():
    """Row 612: the lead-in said the parent gathers five angles and six bullets followed.
    It now names the parent first and the five it gathers after it. This holds the stated
    count against the bullets actually under it."""
    lines = _skill().splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("- **Lifecycle**"))
    lead_in = next(i for i in range(start, len(lines))
                   if "the five angles it gathers follow it" in lines[i])
    bullets = 0
    for line in lines[lead_in + 1:]:
        if line.startswith("- **"):
            break
        if line.startswith("  - **"):
            bullets += 1
    assert bullets == 6, \
        "the lifecycle sweep now has %d bullets under a lead-in promising a parent plus five" % bullets
    assert lines[lead_in].strip().endswith(":"), \
        "the lifecycle lead-in stopped introducing the bullets it counts"
