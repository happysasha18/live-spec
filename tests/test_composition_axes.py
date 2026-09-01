"""A project.kind founding declares the COMPOSITION AXES it owes every surface — M-429 (SPEC INV-244).

Beside its concrete layers and proof kinds (INV-135) and its design principles (INV-136), a project
kind declares the composition axes it owes every surface beyond the kind-independent C-1 floor — the
further axes a surface answers because its kind renders under them. The founding records the kind's axis
set on a `project.axes` line in the host profile, and the founding check reds a kind recorded with no
axis-set declaration at all, the same rank a kind recorded with no layers or proofs carries [INV-135,
A-10]. A kind may declare **none beyond the floor** as an explicit stated decision — the empty case the
per-kind design-principles set already legitimises for a kind with no visitor-facing surface [INV-136].
The check reds on SILENCE and passes on an explicit "none": because an explicit "none beyond the C-1
floor" line IS present text, a line-anchored presence check naturally reds only true silence.

Two things this file proves, kept distinct:

  1. The completeness check — a presence-check on the `project.axes:` line, mirroring INV-135's
     `founding_complete` (which lives inside `tests/test_founding_layers_proofs.py`, NOT a production
     guardrail). It reds a kind-only profile and passes both an explicit axis set and an explicit
     "none". This logic is self-contained here; the fixtures below are its red-and-pass proof.

  2. The law's homes — the SPEC clause and Formal-index row, the ARCHITECTURE per-kind axis table (all
     seven project.kind rows), the live host profile's own `project.axes` line, spec-author's duty to
     read the declared axes before composing, the founding-question set's axes entry, and ADOPT's
     founding record. Against HEAD (pre-delta) none of these exist; the tests pointing at the still-
     unwired production surfaces (spec-author, founding-questions.json, ADOPT.md) red on the CURRENT
     tree, and the rest red against HEAD — recorded in the station's red run.

NOTE on the founding-questions.json mechanism: `scripts/founding-questions.json` feeds the INV-227
update check (`scripts/check-pack-update.sh`), which NAMES a never-answered question to a host on an
older `founding.set-version` — it is version arithmetic, not a presence-check on `project.axes`. So the
axes entry there serves the update check's "name the new question" duty; the RED-on-silence behavior is
the presence check above. The two are separate mechanisms.
"""

import os
import re
import sys
import unittest

from conftest import ROOT, read, read_flat, read_all_flat

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)

KIND = re.compile(r"(?m)^\s*[-*]?\s*`?project\.kind:")
AXES = re.compile(r"(?m)^\s*[-*]?\s*`?project\.axes:")

SEVEN_KINDS = ("static site", "fullstack", "backend", "book", "CLI", "skill pack", "custom")


def axes_declared(profile_text):
    """The founding check for composition axes: a profile that records a project.kind must also
    declare the composition axes its kind owes on a `project.axes` line. An explicit "none beyond
    the floor" IS a declaration (present text) and passes; true silence reds. Returns (ok, reason)."""
    if not KIND.search(profile_text):
        return True, "no project.kind recorded — nothing to complete"
    if not AXES.search(profile_text):
        return False, "project.kind recorded with no declared project.axes"
    return True, "kind and axes both declared"


# --- the three real hosts the ARCHITECTURE names for this check (ARCHITECTURE.md, the axes section) ---
# a visual kind owing input-capability; a kind declaring none beyond the floor; a kind-only profile.
FIXTURE_VISUAL = """# Host profile — tlvphotos
- `project.kind: photo portfolio (fullstack, static-first)`
- `project.layers: content · rendering engine · deployment`
- `project.proofs: a byte-diff of the baked output · the owner's eye-walk`
- `project.axes: input-capability — the input a visitor-facing surface is used through (touch · a fine pointer)`
"""

FIXTURE_NONE = """# Host profile — a skill pack
- `project.kind: skill pack`
- `project.layers: the rulebook and spec · the working skills · the guardrails, templates, and suite`
- `project.proofs: the pytest suite · deed proofs · the owner's read`
- `project.axes: none beyond the C-1 floor`
"""

FIXTURE_KIND_ONLY = """# Host profile — a half-founded project
- `project.kind: photo portfolio (fullstack)`
- `project.layers: content · rendering engine · deployment`
- `project.proofs: a byte-diff of the baked output · the owner's eye-walk`
"""


class TestFoundingAxesCheck(unittest.TestCase):
    def test_visual_kind_with_axes_passes(self):
        ok, reason = axes_declared(FIXTURE_VISUAL)
        self.assertTrue(ok, "a visual-kind profile declaring its axis set should be complete: " + reason)

    def test_kind_without_axes_line_goes_red(self):
        ok, reason = axes_declared(FIXTURE_KIND_ONLY)
        self.assertFalse(ok, "a kind recorded with no project.axes line must be flagged incomplete")
        self.assertIn("project.axes", reason)

    def test_explicit_none_beyond_floor_passes(self):
        """The crux: an explicit "none beyond the C-1 floor" IS present text, so the presence check
        passes it while true silence reds — reds-on-silence, passes-on-explicit-none."""
        ok, reason = axes_declared(FIXTURE_NONE)
        self.assertTrue(ok, "an explicit 'none beyond the floor' declaration must PASS: " + reason)

    def test_live_host_profile_declares_its_axes(self):
        """The pack's own flagship host must satisfy the founding check it ships.
        Read RAW — the check reads line-anchored `project.*:` records, not flattened prose."""
        ok, reason = axes_declared(read(".live-spec/profile.md"))
        self.assertTrue(ok, "live-spec's own host profile declares no composition axes: " + reason)


class TestCompositionAxesLaw(unittest.TestCase):
    def test_spec_states_the_law(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("A surface's composition axes are the set its project's kind owes", spec)
        self.assertIn("[INV-244]", spec)

    def test_formal_index_row(self):
        spec = read("PRODUCT_SPEC.md")
        row = next((l for l in spec.splitlines() if l.startswith("| INV-244 |")), "")
        self.assertTrue(row, "INV-244 Formal-index row missing")
        # index now carries locations only (SPEC INV-271) — move the "axes"/"kind" prose check
        # onto the body requirement heading that carries INV-244.
        flat = read_flat("PRODUCT_SPEC.md")
        self.assertIn("A surface's composition axes are the set its project's kind owes", flat)

    def test_architecture_has_composition_axes_table(self):
        arch = read_flat("ARCHITECTURE.md")
        self.assertIn("Composition axes by project.kind", arch)
        for needle in ("input-capability", "none beyond the floor"):
            self.assertIn(needle, arch, "ARCHITECTURE per-kind axis table lost: %s" % needle)

    def test_architecture_table_covers_all_seven_kinds(self):
        """The per-kind axis table declares every project.kind's axis set — all seven kinds."""
        arch = read("ARCHITECTURE.md")
        marker = "## Composition axes by project.kind"
        self.assertIn(marker, arch, "ARCHITECTURE has no composition-axes section")
        section = arch.split(marker, 1)[1].split("\n## ", 1)[0]
        for kind in SEVEN_KINDS:
            self.assertRegex(
                section, r"(?m)^\|\s*%s\b" % re.escape(kind),
                "the per-kind axis table has no row for project.kind '%s'" % kind,
            )

    def test_spec_author_reads_declared_axes(self):
        """Before composing a surface, spec-author reads its axes from the kind (SPEC INV-244), the
        way it already reads the declared layers (INV-135)."""
        sa = read_all_flat("skills/spec-author/SKILL.md")
        self.assertIn("INV-244", sa, "spec-author does not carry the composition-axes duty")
        self.assertIn("axes from the kind", sa,
                      "spec-author does not state it reads a surface's axes from the kind")

    def test_founding_questions_names_the_axes_question(self):
        """The versioned founding-question set (scripts/founding-questions.json) carries the axes
        question so the INV-227 update check names it to a host on an older set version."""
        import json
        man = json.load(open(os.path.join(ROOT, "scripts", "founding-questions.json"),
                             encoding="utf-8"))
        axes_qs = [q for q in man.get("questions", [])
                   if "project.axes" in (q.get("key") or "")]
        self.assertTrue(axes_qs, "founding-questions.json carries no project.axes question")
        self.assertIn("INV-244", " ".join(q.get("anchor", "") for q in axes_qs),
                      "the axes founding question does not anchor to INV-244")

    def test_adopt_founding_prompts_axes(self):
        """The host-profile founding record is set at adoption's orient (ADOPT.md): the founding
        declares the host's own composition axes."""
        adopt = read_flat("adopt/ADOPT.md")
        self.assertIn("project.axes", adopt)
        self.assertIn("INV-244", adopt)

    def test_architecture_owns_the_invariant(self):
        nodes = archformat.parse_nodes(read("ARCHITECTURE.md"))
        spec_author = next((n for n in nodes if n.name == "spec-author"), None)
        self.assertIsNotNone(spec_author, "ARCHITECTURE.md carries no spec-author node")
        self.assertIn("INV-244", spec_author.anchors_expanded,
                      "spec-author does not own INV-244")

    def test_matrix_row_covers_the_law(self):
        mat = read("TEST_MATRIX.md")
        row = next((l for l in mat.splitlines() if l.startswith("| M-429 |")), "")
        self.assertTrue(row, "TEST_MATRIX has no M-429 row")
        self.assertIn("INV-244", row)


def axis_verdict_sweep(axis_set, added_axis, verdicts):
    """The bounded pass SPEC INV-244 owes (q-437): adding or deriving one composition axis walks
    every OTHER axis already in the kind's declared set and demands one of three verdicts for
    each — already composed against, added now, or out of scope (with its stated reason). A
    sibling axis absent from `verdicts` is the pass left unfinished, not a clean sweep, and it
    reds. Returns (ok, reason)."""
    THREE_VERDICTS = ("already composed against", "added now", "out of scope")
    for sibling in axis_set:
        if sibling == added_axis:
            continue
        if sibling not in verdicts:
            return False, "sibling axis '%s' carries no verdict" % sibling
        verdict = verdicts[sibling]
        kind = verdict[0] if isinstance(verdict, tuple) else verdict
        if kind not in THREE_VERDICTS:
            return False, "sibling axis '%s' carries an unrecognized verdict '%s'" % (sibling, kind)
        if kind == "out of scope" and not (isinstance(verdict, tuple) and verdict[1]):
            return False, "sibling axis '%s' is out of scope with no stated reason" % sibling
    return True, "every sibling axis in the set carries a verdict"


class TestAxisVerdictSweep(unittest.TestCase):
    """SPEC INV-244's bounded pass, proven directly (q-437): walked on a two-axis registry, it
    must return a verdict for every axis beside the one just added. A sibling axis that comes
    back with no verdict is the honest reading that nobody has asked the question yet, and it
    reds rather than passing silently."""

    def test_sibling_axis_with_no_verdict_reds(self):
        registry = ("input-capability", "viewport-tier")
        ok, reason = axis_verdict_sweep(registry, "input-capability", verdicts={})
        self.assertFalse(ok, "a sibling axis carrying no verdict must be flagged, never pass silently")
        self.assertIn("viewport-tier", reason)


def cooccurrence_value_named(poles_answered, cooccurrence_answer):
    """The value-space in-between forcing step SPEC INV-244 owes (q-436): once an axis's two
    elementary poles (touch, a fine pointer) are each answered, the value where both poles hold at
    once — a tablet's touch alongside its hover — needs its own named answer, decided or
    `[default]`-tagged, distinct from either pole answered alone. An axis with both poles answered
    but no co-occurrence answer is the same blank-answer class the axis-verdict sweep (q-437)
    already reports. Returns (ok, reason)."""
    if not poles_answered:
        return True, "the elementary poles are not both answered yet — co-occurrence not owed yet"
    if not cooccurrence_answer:
        return False, "both elementary poles are answered but the co-occurrence value carries no answer"
    return True, "the co-occurrence value carries a named answer"


class TestCooccurrenceValueForcingStep(unittest.TestCase):
    """SPEC INV-244's value-space in-between forcing step (q-436): once touch and a fine pointer
    are both answered, the tablet-with-touch-and-hover case still needs its own named answer. A
    blank co-occurrence answer reds the same way a blank axis verdict does (q-437) — one shared
    blank-answer class, proven here on its own case."""

    def test_blank_cooccurrence_value_reds(self):
        ok, reason = cooccurrence_value_named(poles_answered=True, cooccurrence_answer=None)
        self.assertFalse(ok,
                          "an axis with both elementary poles answered but no co-occurrence value "
                          "must be flagged, never pass silently")
        self.assertIn("co-occurrence", reason)

    def test_poles_unanswered_does_not_yet_owe_cooccurrence(self):
        ok, reason = cooccurrence_value_named(poles_answered=False, cooccurrence_answer=None)
        self.assertTrue(ok, "the co-occurrence value is not owed before its two poles are answered: "
                             + reason)

    def test_named_cooccurrence_value_passes(self):
        ok, reason = cooccurrence_value_named(
            poles_answered=True,
            cooccurrence_answer="a tablet with touch and hover both present gets the touch layout `[default]`",
        )
        self.assertTrue(ok, "a named co-occurrence value must pass: " + reason)


if __name__ == "__main__":
    unittest.main(verbosity=2)
