"""Tests for the durable prose-quality DONE-GATE (docs/prose-quality-gate-design.md).

These lock the MECHANISM (promotion, exemptions, waivers, redundancy pre-check, LLM-judge protocol,
the unified gate). The SPEC-CONTENT tests (every needle lints clean; no anchor hides in a blockquote;
PRODUCT_SPEC.md passes the whole gate) land after the whole-document rewrite, since the current SPEC still
carries the register warnings the rewrite removes.
"""
import datetime
import importlib.util
import json
import os
import re
import subprocess
import sys
import unittest

from conftest import ROOT, SPEC, read
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)
import gate_common  # noqa: E402


def _load_lint_module():
    """Load spec-style-lint.py as a module (its filename is hyphenated, so a plain import will not
    reach it) — the born-red proof needs its internals: the legacy SCISSORS regex, the new
    _rather_instead_scissors arm, and the shared scrub."""
    path = os.path.join(SCRIPTS, "spec-style-lint.py")
    spec = importlib.util.spec_from_file_location("spec_style_lint", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LINT_MOD = _load_lint_module()


def run(script, *args, stdin=None):
    return subprocess.run(["python3", os.path.join(SCRIPTS, script), *args],
                          input=stdin, capture_output=True, text=True)


class TestSpecStyleLintGate(unittest.TestCase):
    def test_default_keeps_soft_signals_advisory(self):
        r = run("spec-style-lint.py", "-", stdin="You open it and it CHANGES the queue.\n")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("second-person", r.stdout)
        self.assertIn("caps-shout", r.stdout)

    def test_gate_promotes_soft_signals_to_errors(self):
        r = run("spec-style-lint.py", "--gate", "-", stdin="You open it and it CHANGES the queue.\n")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("second-person", r.stdout)
        self.assertIn("caps-shout", r.stdout)

    def test_gate_exempts_user_story_and_blockquote(self):
        for text in ("**User story:** as the owner, you report a bug and you see it fixed.\n",
                     "> You can read this informative note however you like.\n"):
            r = run("spec-style-lint.py", "--gate", "-", stdin=text)
            self.assertEqual(r.returncode, 0, "exempt region must pass gate: %r\n%s" % (text, r.stdout))

    def test_gate_scissors_is_global_even_in_blockquote(self):
        r = run("spec-style-lint.py", "--gate", "-", stdin="> the card shows the outcome — not the mechanism.\n")
        self.assertEqual(r.returncode, 1, "scissors is global, no exemption\n%s" % r.stdout)
        self.assertIn("scissors", r.stdout)

    def test_gate_new_rules_fire(self):
        r = run("spec-style-lint.py", "--gate", "-",
                stdin="Simply open it.\nThe card will show the queue.\n")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("reassurance", r.stdout)
        self.assertIn("future-narration", r.stdout)


class TestScissorsCoverage(unittest.TestCase):
    """The contrast frame in every shape, and the additive forms that must stay legal."""

    def _flags_scissors(self, text):
        r = run("spec-style-lint.py", "-", stdin=text + "\n")
        return "scissors" in r.stdout

    def test_comma_appositive_is_caught(self):
        for t in ("It is a record, not a message.",
                  "Show status icons, not a table wall.",
                  "The map is a departures board, not a paragraph."):
            self.assertTrue(self._flags_scissors(t), "comma appositive missed: %r" % t)

    def test_russian_contrast_forms_are_caught(self):
        for t in ("Это чек-лист решает, а не ярлык.",
                  "Не ярлык, а чек-лист решает.",
                  "Не столько скорость, сколько ясность."):
            self.assertTrue(self._flags_scissors(t), "russian contrast missed: %r" % t)

    def test_additive_and_prohibition_forms_stay_legal(self):
        for t in ("This governs replies, not only documents.",
                  "A slip, not just a typo, still counts.",
                  "It informs, not merely enumerates.",
                  "Never delete a host file.",
                  "One term per concept, everywhere.",
                  "If it is not ready, the lane waits."):
            self.assertFalse(self._flags_scissors(t), "false positive on: %r" % t)

    def test_russian_conditional_a_is_not_a_contrast(self):
        # «а если / а бы / а когда / а также» continue a clause; they are not the «не X, а Y» contrast.
        for t in ("деньги не заканчиваются, а если бы заканчивались, что делать",
                  "не сработало, а также сломалось соседнее",
                  "правило написано, а когда проверим — увидим"):
            self.assertFalse(self._flags_scissors(t), "conditional «а» wrongly flagged: %r" % t)


class TestRatherInsteadDefinitional(unittest.TestCase):
    """The scissors frame in its two English prose conjunctions — "X rather than Y" / "X instead of
    Y" used DEFINITIONALLY (census 2026-07-22, finding 1). The dash/comma regex never saw these, so
    a file could carry dozens and pass clean. High-precision extension: a definitional contrast is
    caught; a lawful instructional substitution passes.

    Specimens are verbatim from the corpus (docs/, skills/) so the reds prove real volume, not a
    contrived shape."""

    # (line, source) — each a genuine contrast-by-denial the old rule missed
    REAL_DEFINITIONAL = (
        "since the compact row is now a map rather than a restatement.",              # restyle-repoint-log.md:76 — copula
        "but it is deterministic bash/YAML checking rather than a reviewer skill",     # prior-art-longtail.md:170 — copula
        'the "standards" are conventions rather than formal invariants',               # prior-art-frameworks.md:148 — copula
        "A codebase-context injection tool rather than an SDLC orchestrator.",         # prior-art-frameworks.md:152 — a/an rename
        'carries a dated "Last reconciled" provenance line instead of a version string, so',  # spec-author/SKILL.md:567 — instead-of rename
        "Force is carried by plain declarative statement rather than by RFC keywords.",  # spec-style.md:13 — parallel by
    )

    # lawful — a directive substitution, not a definition; must PASS (precision over recall)
    LAWFUL_INSTRUCTIONAL = (
        "Use TEST_MATRIX.md instead of a scratch list.",       # imperative "use"
        "Write to the engine rather than the site.",           # imperative "write" (the task's named form)
        "Route the reply to the owner instead of the queue.",  # imperative "route"
        "Save it to the cache rather than the home directory.",  # imperative "save"
        "Store the fact in VERSION instead of the spec body.",  # imperative "store"
    )

    # the residual class the docstring names — deliberately uncaught to hold precision; must PASS
    RESIDUAL_UNCAUGHT = (
        "the suite enforces the tag rather than trusting it",              # verb-vs-gerund, no copula/rename
        "so the open question travels with the text instead of being filled silently",  # verb-vs-gerund
        "Recommend rather than ask.",                                     # genuine contrast, but opens imperative
    )

    def _flags_scissors(self, text):
        r = run("spec-style-lint.py", "-", stdin=text + "\n")
        return "scissors" in r.stdout

    def test_definitional_rather_instead_is_caught(self):
        for t in self.REAL_DEFINITIONAL:
            self.assertTrue(self._flags_scissors(t), "definitional frame missed: %r" % t)

    def test_born_red_legacy_regex_missed_these(self):
        """Red-first, proven against the PRE-change logic: before this extension the scissors
        decision was exactly `SCISSORS.search(scrub(text))`. That legacy regex is still in the
        module — assert it matches NONE of the definitional specimens (they escaped, the census's
        finding 1), while the new `_rather_instead_scissors` arm catches every one. The delta the
        two assertions bracket IS the extension: a ratchet seeded on the old lint would have passed
        a file still carrying these frames."""
        scrub = LINT_MOD.gate_common.scrub
        for t in self.REAL_DEFINITIONAL:
            s = scrub(t)
            self.assertIsNone(LINT_MOD.SCISSORS.search(s),
                              "legacy scissors regex unexpectedly caught %r — no longer a born-red proof" % t)
            self.assertTrue(LINT_MOD._rather_instead_scissors(s),
                            "the new arm must catch what the legacy regex missed: %r" % t)

    def test_lawful_instructional_substitution_passes(self):
        for t in self.LAWFUL_INSTRUCTIONAL:
            self.assertFalse(self._flags_scissors(t), "false positive on lawful directive: %r" % t)

    def test_residual_class_passes_by_design(self):
        for t in self.RESIDUAL_UNCAUGHT:
            self.assertFalse(self._flags_scissors(t), "residual class must pass (precision): %r" % t)

    def test_quoted_specimen_passes(self):
        # a frame demonstrated inside backticks is talked ABOUT, not used — scrub strips it, so it
        # must not trip the rule (the same courtesy the dash/comma frame gets).
        self.assertFalse(
            self._flags_scissors("The banned frame `a map rather than a restatement` is shown here."),
            "a backtick-quoted specimen must pass")

    def test_old_dash_and_comma_frames_still_fire(self):
        # no-regression: the extension is an OR alongside the legacy regex, which must keep working.
        for t in ("It is a record, not a message.",
                  "the card shows the outcome — not the mechanism."):
            self.assertTrue(self._flags_scissors(t), "legacy scissors frame regressed: %r" % t)


class TestWaiverMechanism(unittest.TestCase):
    def _w(self, **kw):
        base = {"id": "w1", "rule": "second-person", "file": "PRODUCT_SPEC.md", "snippet": "you know",
                "reason": "r", "owner": "a", "date": "2026-07-08", "expiry": "2026-07-30"}
        base.update(kw)
        return base

    def test_active_waiver_matches_by_snippet(self):
        w = self._w()
        m = gate_common.match_waiver("second-person", "PRODUCT_SPEC.md", "past what you know to ask",
                                     [w], today=datetime.date(2026, 7, 10))
        self.assertIsNotNone(m)

    def test_expired_waiver_does_not_match(self):
        w = self._w(expiry="2026-07-09")
        m = gate_common.match_waiver("second-person", "PRODUCT_SPEC.md", "past what you know to ask",
                                     [w], today=datetime.date(2026, 7, 20))
        self.assertIsNone(m, "an expired waiver must not suppress — it reverts to a hard error")

    def test_wrong_rule_or_file_does_not_match(self):
        w = self._w()
        self.assertIsNone(gate_common.match_waiver("caps-shout", "PRODUCT_SPEC.md", "you know", [w]))
        self.assertIsNone(gate_common.match_waiver("second-person", "OTHER.md", "you know", [w]))

    def test_live_waiver_file_schema_and_bounded_expiry(self):
        path = os.path.join(SCRIPTS, "spec-waivers.json")
        waivers = gate_common.load_waivers(path)
        for w in waivers:
            for field in gate_common.WAIVER_FIELDS:
                self.assertTrue(w.get(field), "waiver %s missing %s" % (w.get("id"), field))
            d = datetime.date.fromisoformat(w["date"])
            e = datetime.date.fromisoformat(w["expiry"])
            self.assertLessEqual((e - d).days, gate_common.MAX_WAIVER_DAYS,
                                 "waiver %s expiry exceeds %d days" % (w["id"], gate_common.MAX_WAIVER_DAYS))


class TestDebtRatchet(unittest.TestCase):
    def test_waivers_within_cap(self):
        cap = json.load(open(os.path.join(SCRIPTS, "spec-debt-cap.json")))
        waivers = gate_common.load_waivers(os.path.join(SCRIPTS, "spec-waivers.json"))
        self.assertLessEqual(len(waivers), cap["max_waivers"],
                             "waiver count exceeds the committed ratchet cap")


class TestRedundancyPrecheck(unittest.TestCase):
    def test_seeded_duplicate_fires(self):
        text = ("The classifier assigns each wish exactly one door at intake.\n\n"
                "At intake the classifier assigns every wish exactly one door.\n")
        r = run("spec-redundancy-precheck.py", "-", stdin=text)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("REDUNDANCY", r.stdout)

    def test_distinct_sentences_pass(self):
        text = "The classifier doors a wish.\n\nThe prover reads committed law only.\n"
        r = run("spec-redundancy-precheck.py", "-", stdin=text)
        self.assertEqual(r.returncode, 0, r.stdout)


class TestJudgeProtocol(unittest.TestCase):
    def test_rubric_hash_is_pinned(self):
        sys.path.insert(0, SCRIPTS)
        import importlib.util
        spec = importlib.util.spec_from_file_location("specjudge", os.path.join(SCRIPTS, "spec-judge.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.PINNED_RUBRIC_SHA256, mod.rubric_sha256(),
                         "judge-rubric.md changed without re-pinning its sha256 in spec-judge.py")

    def test_malformed_output_is_invalid(self):
        with tmpfile("not json") as jf, tmpfile("doc\n") as doc:
            r = run("spec-judge.py", "--verify", doc, jf)
            self.assertEqual(r.returncode, 2, r.stdout)

    def test_selftest_miss_is_invalid(self):
        out = json.dumps({"findings": [
            {"criterion": "C2", "severity": "definite", "quote": "You can skip the rest of this section."}]})
        with tmpfile(out) as jf, tmpfile("doc\n") as doc:
            r = run("spec-judge.py", "--verify", doc, jf)
            self.assertEqual(r.returncode, 2, "missing a seed must be INVALID\n%s" % r.stdout)

    def test_hallucinated_quote_discarded_and_real_survives(self):
        out = json.dumps({"findings": [
            {"criterion": "C1", "severity": "definite", "quote": "At the door, the gate refuses a defect."},
            {"criterion": "C2", "severity": "definite", "quote": "You can skip the rest of this section."},
            {"criterion": "C3", "severity": "definite", "quote": "Simply ignore the footnotes for now."},
            {"criterion": "C2", "severity": "definite", "quote": "You may leave whenever you wish."},
            {"criterion": "C1b", "severity": "likely", "quote": "a span absent from the document"}]})
        with tmpfile(out) as jf, tmpfile("You may leave whenever you wish.\n") as doc:
            r = run("spec-judge.py", "--verify", doc, jf)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn('"surviving":1', r.stdout)
            self.assertIn('"discarded":1', r.stdout)


class TestDoneGate(unittest.TestCase):
    def test_missing_judge_is_red(self):
        with tmpfile("The gate blocks a defect at the door.\n") as doc:
            r = run("spec-done-gate.py", doc)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("DONE-GATE: RED", r.stdout)

    def test_all_conditions_green(self):
        out = json.dumps({"findings": [
            {"criterion": "C1", "severity": "definite", "quote": "At the door, the gate refuses a defect.",
             "duplicate_of": "The gate refuses a defect at the door."},
            {"criterion": "C2", "severity": "definite", "quote": "You can skip the rest of this section."},
            {"criterion": "C3", "severity": "definite", "quote": "Simply ignore the footnotes for now."}]})
        with tmpfile("The gate blocks a defect at the door.\n") as doc, tmpfile(out) as jf:
            r = run("spec-done-gate.py", "--judge", jf, doc)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("DONE-GATE: GREEN", r.stdout)


import contextlib
import tempfile


@contextlib.contextmanager
def tmpfile(content):
    fd, path = tempfile.mkstemp(suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        yield path
    finally:
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()


class TestSpecContentRegisterClean(unittest.TestCase):
    """Land after the SPEC body is converted (stage 5): the body carries no register defect the
    gate would block, and no re-pointed needle hides one. These two guard the whole document, not
    just the mechanism."""

    def _spec(self):
        return read(SPEC)

    def _load_linter(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "specstylelint", os.path.join(SCRIPTS, "spec-style-lint.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_needles_are_register_clean(self):
        """Every traceability-test string that is a LIVE SPEC needle (present verbatim in PRODUCT_SPEC.md)
        lints clean of the position-independent gate tells — so a needle can never be re-pointed to
        a phrase that itself carries scissors, jargon, a shout-cap, second person, reassurance, or
        future narration. Closes the re-point-to-a-defect loophole."""
        lint = self._load_linter()
        # scope to the BODY: the Formal index table is parked by his word and keeps its caps,
        # so a needle that lives only there is not a converted-body defect.
        full = self._spec()
        spec = full.split("## Formal index")[0]
        trace = open(os.path.join(ROOT, "tests", "test_traceability.py"), encoding="utf-8").read()
        literals = set(re.findall(r'"([^"\\]{6,})"', trace)) | set(re.findall(r"'([^'\\]{6,})'", trace))
        live = [s for s in literals if s in spec]
        self.assertGreater(len(live), 30, "expected many live SPEC needles to check")
        bad = []
        for s in live:
            errs, _ = lint.lint(s, gate=True)
            # negation-opener is a block-lead judgement; a mid-sentence needle fragment can trip it
            # spuriously, so this guard covers the position-independent tell classes.
            hard = [c for _, c, _ in errs if not c.startswith("negation-opener")]
            if hard:
                bad.append((s[:60], hard))
        self.assertEqual(bad, [], "needles carrying a register tell: %s" % bad)

    def test_no_anchor_hides_in_a_blockquote(self):
        """A bracketed anchor ([INV-…], [E-…], [T-…], [M-…], [A-…], [D-…], [B-…], [C-…], [S-…],
        [ACT-…]) marks NORMATIVE content; it must never sit inside a `>` blockquote, the informative
        lane the gate exempts — else a normative rule could hide there from the normative-only checks."""
        anchor = re.compile(r"\[(?:INV|E|T|M|A|D|B|C|S|ACT)-")
        offenders = [i for i, ln in enumerate(self._spec().splitlines(), 1)
                     if ln.lstrip().startswith(">") and anchor.search(ln)]
        self.assertEqual(offenders, [], "anchor inside a blockquote at SPEC lines %s" % offenders)


class TestProvenanceOutOfBody(unittest.TestCase):
    """Provenance stays out of the normative body: no birth-story ("(Born of …)", a Formal-index
    "; born of …" cell, or a "Born of …" / "was born of …" sentence) lives in PRODUCT_SPEC.md or any
    skill body — its home is the code-keyed docs index (docs/lenses.md), the JOURNAL, or a prover
    record (docs/spec-style.md R15). The lint's provenance-narrative arms enforce it; this is the
    standing completeness gate for the sweep — red while a story sits in a body, green when the last
    one has moved to its docs home."""

    SKILL_GLOB = "skills/*/SKILL.md"

    def _load_linter(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "specstylelint", os.path.join(SCRIPTS, "spec-style-lint.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def _bodies(self):
        import glob
        # ROADMAP row 315: TEST_MATRIX.md joined scope 2026-07-14 — the matrix carried 17 birth-story
        # cells ("; born of <case> (<date>); never …") swept to docs/lenses.md, keyed by the cell's
        # INV-code, with the M-code noted back at that entry.
        paths = [os.path.join(ROOT, "PRODUCT_SPEC.md"), os.path.join(ROOT, "TEST_MATRIX.md")]
        paths += sorted(glob.glob(os.path.join(ROOT, self.SKILL_GLOB)))
        return paths

    def test_no_provenance_narrative_in_any_body(self):
        lint = self._load_linter()
        offenders = []
        for path in self._bodies():
            rel = os.path.relpath(path, ROOT)
            # Read through the suite's one node: the spec arrives whole — the core and the parts its
            # map names — rather than as whichever single file the path points at.
            text = read(rel)
            errs, _ = lint.lint(text)
            offenders += [(rel, ln, snip) for ln, code, snip in errs
                          if code == "provenance-narrative"]
        self.assertEqual(
            offenders, [],
            "a birth-story sits in a normative body — move it to docs/lenses.md, the JOURNAL, or a "
            "prover record (docs/spec-style.md R15). %d found:\n%s"
            % (len(offenders), "\n".join("  %s:%d  %s" % o for o in offenders)))

    def test_matrix_carries_no_birth_story_clause(self):
        """ROADMAP row 315: TEST_MATRIX.md's 'born of' occurrences after the sweep. Every dated
        birth-story clause ("; born of <case> (<date>); never …", or a "(born of …)" parenthetical)
        moved to docs/lenses.md, keyed by the cell's INV-code with the M-code noted back. The one
        survivor is M-191's ordinary restrictive verb ("a silent pass born of broken skip plumbing")
        — no date, no story, mid-clause, the exact shape test_ordinary_verb_born_of_is_not_flagged
        blesses and R15 exempts by name ("a row born of a split cites its wish").

        This checks the raw file text by substring rather than routing every hit through
        lint()/gate_common.scrub(): one cell (M-212) carries a stray escaped backtick inside a code
        span ("`- \\``") that desyncs scrub's backtick pairing and can swallow a later parenthetical
        whole, hiding a birth-story from the shaped regex. The substring scan does not depend on that
        pairing, so it still catches the class the shaped check can miss."""
        text = open(os.path.join(ROOT, "TEST_MATRIX.md"), encoding="utf-8").read()
        hits = [ln for ln in text.splitlines() if re.search(r"\bborn of\b", ln, re.IGNORECASE)]
        offenders = [ln for ln in hits if "M-191" not in ln]
        self.assertEqual(
            offenders, [],
            "a birth-story clause still sits in TEST_MATRIX.md — move it to docs/lenses.md (R15): %s"
            % offenders)

    def test_ordinary_verb_born_of_is_not_flagged(self):
        """The lint keys on SHAPE, so the ordinary restrictive verb survives while the story is caught."""
        lint = self._load_linter()
        for legal in ("every row born of a split cites the one spoken wish it came from.",
                      "A clause born of an approved look points at its norm."):
            errs, _ = lint.lint(legal)
            codes = [c for _, c, _ in errs]
            self.assertNotIn("provenance-narrative", codes,
                             "ordinary-verb 'born of' wrongly flagged: %r" % legal)
        for pointer in ("A prototype-born clause cites norm: docs/norms/x.html at line end.",
                        "Each entry citing the engine's own public commit abc1234."):
            errs, _ = lint.lint(pointer)
            self.assertNotIn("provenance-narrative", [c for _, c, _ in errs],
                             "one-token pointer wrongly flagged: %r" % pointer)
        # an ordinary dated note that is NOT a birth-story stays clean: a bare-date opener, an
        # "(Audit …)" / "(The owner's word …)" opener, and a dateless "(recorded profile line …)".
        for clean in ("A calque degrades the product (2026-07-05 — machine-speak).",
                      "Money yes, deletion yes, a push no (2026-07-05: the criterion).",
                      "The attic had no answer (Audit 2026-07-05: the second collision).",
                      "Convergence covers every process (The owner's word, 2026-07-10: always).",
                      "A host may switch it on (recorded profile line, SPEC E-18, INV-14)."):
            errs, _ = lint.lint(clean)
            self.assertNotIn("provenance-narrative", [c for _, c, _ in errs],
                             "ordinary dated note wrongly flagged as a birth-story: %r" % clean)

    def test_dated_story_opener_parentheticals_are_caught(self):
        """The extended arm catches the dated/attributed birth-story parentheticals the born-of arm
        missed — keyed on a provenance opener plus an ISO date."""
        lint = self._load_linter()
        for story in ("The rule holds. (Set by the owner 2026-07-10, off a real miss.)",
                      "The rule holds. (Set on the owner's word, 2026-07-10: one command.)",
                      "The rule holds. (Born in the field: it bounced three times, 2026-07-10.)",
                      "The rule holds. (Sharpened 2026-07-12: a fresh audit caught a contradiction.)",
                      "The rule holds. (Raised by the web session's read, 2026-07-10 — a gap.)",
                      "The rule holds. (recorded live 2026-07-12: an entry analysis reads three sources.)",
                      "The rule holds. (recorded 2026-07-09: a deferred theme revived later.)",
                      "The rule holds. (the worked miss: whole surfaces emitted nothing, 2026-07-10)."):
            errs, _ = lint.lint(story)
            self.assertIn("provenance-narrative", [c for _, c, _ in errs],
                          "a dated story-opener parenthetical slipped past the lint: %r" % story)

    def test_each_story_shape_is_caught(self):
        lint = self._load_linter()
        for story in ("The gate blocks a defect. (Born of a real prover walk, 2026-07-13.)",
                      "| INV-x | the rule holds; born of the row 220 audit (2026-07-10) | Door |",
                      "The rule holds. Born of two windows filling their own context (2026-07-13).",
                      "This tripwire was born of the row 220 audit (2026-07-10)."):
            errs, _ = lint.lint(story)
            self.assertIn("provenance-narrative", [c for _, c, _ in errs],
                          "a birth-story shape slipped past the lint: %r" % story)
