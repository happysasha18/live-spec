"""The prover doc's reader-facing homes — outside adversarial review, 2026-07-16.

The frontmatter description carries only the autoload trigger; the prover/design-reviewer
boundary is homed in "Work that belongs elsewhere" (the modes paragraph points at it); the
paired-transition kind-split lives in its lens, and the KIND block stays general.
Red-proven against the pre-restructure file (HEAD before commit 2cca664)."""
# The description is discovery metadata, read by the tool that routes a request to the skill
# and by nothing in this pack. So what this pack has at stake in it is the negative half of
# rule 4: its own facts — the sibling pass's name, an anchor code — keep their one home in the
# canon's "Work that belongs elsewhere" section and in this pack's own adapter, and never gain
# a second one in a line written to be matched against. What the description says beyond that
# is the canon's own property, held by the canon's own validator and its own release.
from pathlib import Path

from conftest import external_clone_or_skip

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "product-prover" / "SKILL.md"
LENSES = ROOT / "skills" / "product-prover" / "reference" / "stress-lenses.md"
PACK = ROOT / "skills" / "product-prover-pack" / "SKILL.md"
GATE = ROOT / "guardrails" / "check-prover-record.sh"


def _skill():
    external_clone_or_skip()
    return SKILL.read_text(encoding="utf-8")


def _description():
    for line in _skill().splitlines():
        if line.startswith("description:"):
            return line
    raise AssertionError("prover SKILL.md lost its frontmatter description line")


def test_description_carries_only_the_trigger():
    """Only the trigger, stated as the two facts that must stay out of it.

    A third assertion stood here until 2026-08-28: that the description carried the literal
    phrase "hold together as written". It was written as a stand-in for "the line still says
    what the skill answers", and it broke the way a stand-in breaks. Release 1.4.2 shortened
    the description for exactly the discovery reliability the phrase was supposed to stand
    for, and the phrase left the canon altogether — so the check reddened on the improvement
    it was meant to protect, while a description carrying that phrase beside every pack fact
    in the tree would have passed it. It could not distinguish the property either way, which
    is the vacuous-when-green, red-on-rewording shape this pack forbids. The property it
    reached for is the canon's, held there by the canon's own validator; the two assertions
    below are this pack's own, and they still bite.
    """
    d = _description()
    assert "design-reviewer" not in d, "description carries the sibling pass again — trigger noise"
    assert "INV-141" not in d, "description carries an anchor code — trigger noise"


def test_boundary_homed_in_when_not_to_use():
    s = _skill()
    start = s.index("## Work that belongs elsewhere")
    end = s.index("## ", start + 5)
    section = s[start:end]
    # the externalized canon states the boundary generically; the sibling pass's name and
    # the INV-141 anchor are pack facts, bound to this section by the pack adapter's pin map.
    assert "belongs to a design-consistency review" in section, \
        "the prover/design-reviewer boundary left its one home"
    assert "This pass verifies the document." in section
    pack = PACK.read_text(encoding="utf-8")
    assert "| INV-141 | Work that belongs elsewhere" in pack, \
        "the pack adapter stopped pinning INV-141 to the boundary section"


def test_kind_block_stays_general_split_lives_in_lens():
    s = _skill()
    kind_block = s[s.index("`KIND` — whether the finding is a defect or a recommendation"):
                   s.index("`CATEGORY` —")]
    assert "one-sided pair" not in kind_block, \
        "the paired-transition family split leaked back into the KIND block"
    # the paired-transition lens lives in the canon's reference/stress-lenses.md now, and the
    # canon generalized "open motion question" into the taste-call open question surfaced to
    # the decision-owner (motion feel kept as a worked instance).
    external_clone_or_skip()
    lenses = LENSES.read_text(encoding="utf-8")
    lens = lenses[lenses.index("**Paired-transition symmetry**"):
                  lenses.index("**Persistence and versions**")]
    assert "declared one-sided pair" in lens and \
        "the open question is surfaced to the decision-owner" in lens, \
        "the family's kind-split left its lens home"


def _gate_repair_lines():
    """The gate's own repair lines — the strings it prints to an author, read from the
    echo statements rather than from any comment about them."""
    return [line.strip() for line in GATE.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("echo ") and "PROVER_DIR" in line]


def test_the_record_path_the_skill_prescribes_is_the_one_the_gate_demands():
    """Row 608: the skill sent an author to `docs/prover/YYYY-MM-DD.md` while the gate's
    own repair line named the slug form, so an author who obeyed the skill was refused.
    This pins the two together — either side drifting turns this red. Since the v5.0.0
    externalization the pack-specific record path lives on the tracked adapter (its persist
    sentence names the directory and the slug form in two backtick spans)."""
    pack = PACK.read_text(encoding="utf-8")
    assert "`docs/prover/`" in pack and "`YYYY-MM-DD-<slug>.md`" in pack, \
        "the pack's persist line stopped naming the slug form the gate demands"
    assert "YYYY-MM-DD.md" not in pack, \
        "the bare-date form the gate refuses is back in the pack's persist line"
    repairs = _gate_repair_lines()
    assert repairs, "check-prover-record.sh prints no repair line naming its record directory"
    assert any("$TODAY-<slug>.md" in line for line in repairs), \
        "the gate stopped telling an author to write the slug form the skill prescribes"


def test_the_lifecycle_lead_in_counts_the_bullets_that_follow_it():
    """Row 612: the lead-in states how many angles the lifecycle gathers, and this holds
    that stated count against the sub-lenses actually under it. In the canon's v5.0.0 shape
    the lifecycle is reference/stress-lenses.md's "### 4. Lifecycle" section: a lead-in
    naming five angles beside the transition-payload parent, then one bold-led paragraph
    per sub-lens — the parent plus the five, six heads."""
    external_clone_or_skip()
    lines = LENSES.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("### 4. Lifecycle"))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("### "))
    section = lines[start:end]
    lead_in = next((i for i, line in enumerate(section) if "Five separate angles" in line),
                   None)
    assert lead_in is not None, \
        "the lifecycle lead-in stopped stating the count of angles it gathers"
    heads = [line for line in section if line.startswith("**")]
    assert len(heads) == 6, \
        "the lifecycle section now has %d sub-lens heads under a lead-in promising a parent " \
        "plus five" % len(heads)
    assert heads[0].startswith("**Transition payload**"), \
        "the transition-payload parent stopped leading the lifecycle's sub-lenses"
