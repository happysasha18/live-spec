"""MINOR-gate 1.2.0 reconciliations (row 306) — enshrine the five folds the Fable
whole-spec audit forced, so none can silently drift back out. Landed 2026-07-13."""
import re
from pathlib import Path

from conftest import external_clone_or_skip

ROOT = Path(__file__).resolve().parent.parent


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


_ONES = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
         "eighteen", "nineteen")
_TENS = (None, None, "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")


def _spelled(n, noun="rules in the body"):
    """The English phrase a doc would use for this count: 31 reads "thirty-one rules in the body"."""
    if n < 20:
        word = _ONES[n]
    else:
        tens, ones = divmod(n, 10)
        word = _TENS[tens] if ones == 0 else "%s-%s" % (_TENS[tens], _ONES[ones])
    return "%s %s" % (word, noun)


def test_base_rule_26_homes_design_principles():
    # D3: base-rulebook carries a real text home for INV-136/139 ownership
    base = _read("skills/live-spec-base/SKILL.md")
    assert "26. **A project kind also declares design principles the verify pass runs" in base
    # The count is DERIVED from the file, never pinned as a magic string: a pinned literal makes
    # the suite's green depend on the number being wrong, and correcting it to the truth reds
    # (ROADMAP row 384, the vacuous-pass class; the same defect found in test_request_classifier
    # the same day, and this was its second instance).
    rules = len(re.findall(r"^\d+\. \*\*", base, re.M))
    assert rules > 0, "the base rulebook's numbered rule heads are unreadable"
    assert _spelled(rules) in base or "%d rules in the body" % rules in base, (
        "the base description states a rule count other than the %d rules on disk" % rules)
    assert "INV-136, INV-139" in base
    # the periodic-full-audit rule is base rule 28 (INV-145, Part C); rule 29 is the deferral test
    assert "28. **A periodic full audit" in base
    assert "29. **A deferral must justify itself" in base
    # README's mirrored rule count is fresh
    readme = _read("README.md")
    assert _spelled(rules, "shared rules") in readme or "%d shared rules" % rules in readme, (
        "README states a rule count other than the %d rules on disk" % rules)


def test_d1_reading_discipline_composes_with_brief_read():
    # D1: rule 25 / INV-137 compose with INV-53 rather than contradicting it. The requirements-
    # format rewrite dropped the explicit "composes with" prose sentence; the composition is now
    # expressed by co-citing both anchors on the one criterion that states the brief-owed read.
    base = _read("skills/live-spec-base/SKILL.md")
    assert "lead never reads a file merely to hand a worker its anchors" in base
    spec = _read("PRODUCT_SPEC.md")
    assert "[INV-53, INV-137]" in spec
    assert "the reader worker whose distillation returns the per-file lines" in spec


def test_d2_finding_kind_names_delta_scoped_exception():
    # D2: INV-140's "every defect blocks" carves out the delta-scoped gate (INV-114). The spec's
    # requirements-format rewrite restated this as a *when*/*shall* criterion; the externalized
    # prover canon states the same exception in its own generic words, and the pack adapter's
    # pin map carries the INV-114 anchor for the rewrite-gate home.
    spec = _read("PRODUCT_SPEC.md")
    assert "a delta-scoped gate meets a pre-existing defect outside the delta" in spec
    assert "queue it by that law rather than block the merge it did not create" in spec
    pack = _read("skills/product-prover-pack/SKILL.md")
    assert "| INV-114 | How to write findings; Reviewing a rewrite before it merges |" in pack
    # The tracked-file anchors above hold on a bare checkout; only the canon read below needs the clone.
    external_clone_or_skip()
    prover = " ".join(_read("skills/product-prover/SKILL.md").split())
    assert "Pre-existing findings become tracked follow-ups in the same change and never block" in prover


def test_d5_chat_law_hook_carries_reading_discipline():
    # D5: the session is told the reading discipline — base rule 25, SPEC INV-137.
    #
    # The hook used to prove this by retelling the rule in its own words; it carried the phrases
    # "base rule 25 for the reading discipline (SPEC INV-137)" and "dispatched to a reader worker"
    # (phrasing last moved 2026-07-28, read 16). On 2026-08-17 the owner had the hook shrunk: it no
    # longer retells any law, it names the seven and points at the two files holding their wording.
    #
    # So the guarantee moves surface rather than dissolving. What has to hold now is REACHABILITY:
    # the hook must name the home, and the home must actually carry the rule. Both halves are checked
    # here, because either one alone would let the duty slip away silently — a hook pointing at a file
    # that lost the rule, or a file keeping a rule nothing points at.
    hook = _read("hooks/chat-law-hook.sh")
    assert "live-spec-base/SKILL.md" in hook, (
        "the hook names no home for the law texts, so the reading discipline is unreachable from a "
        "session that only ever sees the hook's line"
    )
    home = _read("skills/live-spec-base/SKILL.md")
    assert "25. **The orchestrator reads to decide; discovery reads go to workers (SPEC INV-137).**" in home
    assert "dispatches it to a reader" in home


def test_version_homes_agree():
    # The pack version has one source of truth, the VERSION file, and every other home
    # must AGREE with it — so a bump that misses a home reds here. This is derived from
    # VERSION rather than pinned to a literal, so it stays current across releases on its
    # own; it replaced a per-release 1.x.y snapshot that had to be hand-edited every bump
    # (the maintenance trap that reds a green release, fixed at root 2026-07-15).
    version = _read("VERSION").strip()
    assert f'"version": "{version}"' in _read(".claude-plugin/plugin.json")
    assert f"v{version}, " in _read("PRODUCT_SPEC.md")
