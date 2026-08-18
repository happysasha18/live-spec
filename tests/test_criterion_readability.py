"""The criterion-readability ratchet (SPEC INV-287, INV-288).

`guardrails/check-criterion-readability.py` reads the acceptance criteria of a requirements-format
document through five arms — a criterion over the word cap, a definition-shaped aside inside a
criterion, a closing clause with no finite verb, an anchor that competes with the prose, and a
criterion whose pieces sum past a total cap — and compares each arm's count against the baseline
recorded in `guardrails/criterion-readability.json`. A rise reds; a count at the baseline passes; a
fall passes and re-baselines under `--rebaseline`.

Each arm is proven in both directions against a pair of fixtures that differ only in the defect:
`readability_dirty.md` carries exactly one criterion per arm, `readability_clean.md` carries the
same four rules written to the bar. The fixture config seeds every baseline at zero, so a single
violating criterion is a rise and reds.

A criterion is its numbered line together with the indented bullet lines of the sub-list under it,
so a second pair of fixtures — `readability_bullets_dirty.md` and `readability_bullets_clean.md` —
puts each defect inside a bullet under a short criterion line. Without that reach, moving a
criterion's overflow one line down would lower every count while the text a person reads stayed the
same length.

The fifth arm, criterion-load, sums a criterion's pieces instead of reading them one at a time: a
criterion can pass the word cap on every piece and still carry more than one rule once the pieces
are added together. `TestCriterionLoadArm` below proves it against small documents built in place,
since neither shipped fixture carries a criterion whose pieces each stay under the per-piece cap
while their sum runs past the total cap.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from conftest import ROOT, SPEC, read, spec_paths

GATE = os.path.join(ROOT, "guardrails", "check-criterion-readability.py")
REAL_CONFIG = os.path.join(ROOT, "guardrails", "criterion-readability.json")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
DIRTY = os.path.join(FX, "readability_dirty.md")
CLEAN = os.path.join(FX, "readability_clean.md")
BULLETS_DIRTY = os.path.join(FX, "readability_bullets_dirty.md")
BULLETS_CLEAN = os.path.join(FX, "readability_bullets_clean.md")
ARMS = ("long-criterion", "inline-gloss", "absolute-tail", "anchor-noise")

# Which criterion of readability_dirty.md each arm is meant to catch, and the words its report must
# put in front of the writer.
DIRTY_CRITERION = {
    "long-criterion": "R1.1",
    "inline-gloss": "R1.2",
    "absolute-tail": "R1.3",
    "anchor-noise": "R1.4",
}


def run_many(docs, config=None, *flags):
    """The gate over a document held in one or more files — a core and the parts its map names."""
    env = dict(os.environ)
    if config is not None:
        env["CRITERION_READABILITY_CONFIG"] = config
    return subprocess.run(["python3", GATE, *docs] + list(flags),
                          capture_output=True, text=True, env=env)


def run(doc, config=None, *flags):
    return run_many([doc], config, *flags)


def config_with(tmp, baselines, thresholds=None, name="cfg.json"):
    """A fixture config: the shipped thresholds, the given baselines, optional threshold edits."""
    cfg = json.load(open(REAL_CONFIG, encoding="utf-8"))
    for arm in ARMS:
        cfg["arms"][arm]["baseline"] = baselines[arm]
        if thresholds and arm in thresholds:
            cfg["arms"][arm]["threshold"].update(thresholds[arm])
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f)
    return path


def zeros():
    return dict((arm, 0) for arm in ARMS)


def highs():
    return dict((arm, 999) for arm in ARMS)


class TestGateShips(unittest.TestCase):
    def test_gate_and_config_ship(self):
        self.assertTrue(os.path.isfile(GATE), "the readability gate does not ship")
        self.assertTrue(os.path.isfile(REAL_CONFIG), "the readability config does not ship")

    def test_every_arm_declares_its_threshold_and_baseline_in_the_one_config(self):
        cfg = json.load(open(REAL_CONFIG, encoding="utf-8"))
        for arm in ARMS:
            self.assertIn(arm, cfg["arms"], "the config declares no arm %s" % arm)
            self.assertTrue(cfg["arms"][arm]["threshold"],
                            "arm %s carries no tunable threshold (INV-287)" % arm)
            self.assertIsInstance(cfg["arms"][arm]["baseline"], int,
                                  "arm %s carries no recorded baseline (INV-288)" % arm)
            self.assertTrue(cfg["arms"][arm]["fix"].strip(),
                            "arm %s tells the writer nothing to do instead" % arm)

    def test_a_missing_arm_in_the_config_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = json.load(open(REAL_CONFIG, encoding="utf-8"))
            del cfg["arms"]["absolute-tail"]
            path = os.path.join(tmp, "short.json")
            json.dump(cfg, open(path, "w"))
            r = run(CLEAN, path)
            self.assertNotEqual(r.returncode, 0, "a config missing an arm passed:\n%s" % r.stdout)
            self.assertIn("absolute-tail", r.stdout)


class TestEachArmRedsAndStaysSilent(unittest.TestCase):
    """Red-proof both directions, one arm at a time."""

    def _red_for(self, arm):
        with tempfile.TemporaryDirectory() as tmp:
            baselines = highs()
            baselines[arm] = 0
            r = run(DIRTY, config_with(tmp, baselines))
            self.assertNotEqual(r.returncode, 0,
                                "arm %s passed its own violating criterion:\n%s" % (arm, r.stdout))
            return r.stdout

    def test_long_criterion_reds_a_welded_sentence(self):
        out = self._red_for("long-criterion")
        self.assertIn("long-criterion", out)
        self.assertIn(DIRTY_CRITERION["long-criterion"], out)
        self.assertIn("words in one criterion", out)

    def test_inline_gloss_reds_a_definition_inside_the_criterion(self):
        out = self._red_for("inline-gloss")
        self.assertIn("inline-gloss", out)
        self.assertIn(DIRTY_CRITERION["inline-gloss"], out)
        self.assertIn("glossary", out)

    def test_absolute_tail_reds_a_closing_clause_with_no_finite_verb(self):
        out = self._red_for("absolute-tail")
        self.assertIn("absolute-tail", out)
        self.assertIn(DIRTY_CRITERION["absolute-tail"], out)
        self.assertIn("the rest becoming queue rows", out)

    def test_anchor_noise_reds_a_crowded_anchor(self):
        out = self._red_for("anchor-noise")
        self.assertIn("anchor-noise", out)
        self.assertIn(DIRTY_CRITERION["anchor-noise"], out)
        self.assertIn("codes in one anchor", out)

    def test_every_arm_stays_silent_on_the_clean_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(CLEAN, config_with(tmp, zeros()))
            self.assertEqual(r.returncode, 0,
                             "a clean document red an arm:\n%s" % r.stdout)
            self.assertIn("long-criterion=0/0", r.stdout)
            self.assertIn("inline-gloss=0/0", r.stdout)
            self.assertIn("absolute-tail=0/0", r.stdout)
            self.assertIn("anchor-noise=0/0", r.stdout)

    def test_each_arm_reds_only_its_own_defect(self):
        """Every arm at zero: each of the four arms reports exactly one criterion, its own."""
        with tempfile.TemporaryDirectory() as tmp:
            r = run(DIRTY, config_with(tmp, zeros()))
            self.assertNotEqual(r.returncode, 0)
            for arm in ARMS:
                self.assertIn("- %s: 1 criteria break it" % arm, r.stdout,
                              "arm %s did not report exactly its own criterion:\n%s"
                              % (arm, r.stdout))
                self.assertIn(DIRTY_CRITERION[arm], r.stdout)


class TestReportNamesWhereAndWhatToDo(unittest.TestCase):
    def test_a_red_names_file_code_line_text_and_the_fix(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(DIRTY, config_with(tmp, zeros()))
            self.assertIn("readability_dirty.md:", r.stdout, "the report names no file")
            self.assertIn("R1.3", r.stdout, "the report names no requirement code")
            self.assertIn("readability_dirty.md:24", r.stdout, "the report names no line")
            self.assertIn("write instead:", r.stdout, "the report tells the writer nothing to do")

    def test_a_red_carries_the_gate_contract_typed_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(DIRTY, config_with(tmp, zeros()))
            typed = [ln for ln in r.stdout.splitlines() if ln.startswith("{")]
            self.assertEqual(len(typed), 1, "a blocking red carries exactly one typed line")
            obj = json.loads(typed[0])
            self.assertEqual(obj["severity"], "error")
            self.assertEqual(obj["code"], "criterion-readability")
            self.assertTrue(obj["message"].strip())
            self.assertTrue(obj["fix"].strip())

    def test_every_run_states_its_reach(self):
        with tempfile.TemporaryDirectory() as tmp:
            red = run(DIRTY, config_with(tmp, zeros()))
            green = run(CLEAN, config_with(tmp, zeros(), name="cfg2.json"))
            for out in (red.stdout, green.stdout):
                self.assertIn("reach: files=[", out)
                self.assertIn("acceptance criteria of the body", out)
                self.assertIn("outside this gate's reach", out)


class TestThresholdsAreTunable(unittest.TestCase):
    def test_raising_the_word_cap_silences_the_long_criterion_arm(self):
        with tempfile.TemporaryDirectory() as tmp:
            baselines = highs()
            baselines["long-criterion"] = 0
            path = config_with(tmp, baselines, {"long-criterion": {"max_words": 60}})
            r = run(DIRTY, path)
            self.assertEqual(r.returncode, 0,
                             "the word cap is not read from the config:\n%s" % r.stdout)

    def test_lowering_the_anchor_cap_catches_the_clean_anchor(self):
        with tempfile.TemporaryDirectory() as tmp:
            baselines = highs()
            baselines["anchor-noise"] = 0
            path = config_with(tmp, baselines, {"anchor-noise": {"max_anchor_codes": 2}})
            r = run(CLEAN, path)
            self.assertNotEqual(r.returncode, 0,
                                "the anchor cap is not read from the config:\n%s" % r.stdout)
            self.assertIn("3 codes in one anchor", r.stdout)


class TestRatchetBehaviour(unittest.TestCase):
    def test_a_rise_reds_and_names_the_count_against_the_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(DIRTY, config_with(tmp, zeros()))
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("baseline 0", r.stdout)

    def test_a_count_at_the_baseline_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(DIRTY, config_with(tmp, dict((arm, 1) for arm in ARMS)))
            self.assertEqual(r.returncode, 0, "a count at its baseline red:\n%s" % r.stdout)

    def test_a_fall_passes_and_says_the_baseline_can_be_lowered(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(DIRTY, config_with(tmp, dict((arm, 5) for arm in ARMS)))
            self.assertEqual(r.returncode, 0, "a fall red:\n%s" % r.stdout)
            self.assertIn("fell", r.stdout)
            self.assertIn("--rebaseline", r.stdout)

    def test_rebaseline_writes_the_lower_counts_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = config_with(tmp, dict((arm, 5) for arm in ARMS))
            r = run(DIRTY, path, "--rebaseline")
            self.assertEqual(r.returncode, 0, r.stdout)
            cfg = json.load(open(path, encoding="utf-8"))
            for arm in ARMS:
                self.assertEqual(cfg["arms"][arm]["baseline"], 1,
                                 "arm %s was not re-baselined to its measured count" % arm)

    def test_rebaseline_refuses_to_raise_a_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = config_with(tmp, zeros())
            r = run(DIRTY, path, "--rebaseline")
            self.assertNotEqual(r.returncode, 0, "a rise was recorded as a new baseline:\n%s"
                                % r.stdout)
            cfg = json.load(open(path, encoding="utf-8"))
            for arm in ARMS:
                self.assertEqual(cfg["arms"][arm]["baseline"], 0,
                                 "arm %s baseline moved up" % arm)

    def test_an_unseeded_baseline_passes_with_its_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = config_with(tmp, dict((arm, None) for arm in ARMS))
            r = run(DIRTY, path)
            self.assertEqual(r.returncode, 0, "an unseeded config red:\n%s" % r.stdout)
            self.assertIn("not yet seeded", r.stdout)

    def test_an_empty_document_reds_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty = os.path.join(tmp, "empty.md")
            open(empty, "w", encoding="utf-8").write("# Nothing here\n")
            r = run(empty, config_with(tmp, zeros()))
            self.assertNotEqual(r.returncode, 0, "a document with no criteria passed:\n%s" % r.stdout)
            self.assertIn("criteria", r.stdout)


class TestABulletIsPartOfItsCriterion(unittest.TestCase):
    """The reach a criterion's bullets sit in. Each fixture criterion writes its own line short and
    puts one arm's defect in a bullet under it, so a gate that read the numbered line alone would
    call every one of them clean."""

    def _red_for(self, arm):
        with tempfile.TemporaryDirectory() as tmp:
            baselines = highs()
            baselines[arm] = 0
            r = run(BULLETS_DIRTY, config_with(tmp, baselines))
            self.assertNotEqual(r.returncode, 0,
                                "arm %s read a criterion's line and stopped there:\n%s"
                                % (arm, r.stdout))
            return r.stdout

    def test_a_criterion_with_short_bullets_passes_every_arm(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(BULLETS_CLEAN, config_with(tmp, zeros()))
            self.assertEqual(r.returncode, 0,
                             "a criterion whose line and bullets are all short red:\n%s" % r.stdout)
            for arm in ARMS:
                self.assertIn("%s=0/0" % arm, r.stdout)

    def test_a_long_bullet_reds_and_the_message_names_the_bullet(self):
        out = self._red_for("long-criterion")
        self.assertIn("long-criterion", out)
        self.assertIn("R1.1", out)
        self.assertIn("44 words in bullet 2 of this criterion (cap 35)", out)

    def test_a_definition_shaped_aside_in_a_bullet_reds_the_inline_gloss_arm(self):
        out = self._red_for("inline-gloss")
        self.assertIn("inline-gloss", out)
        self.assertIn("R1.2", out)
        self.assertIn("in bullet 1", out)
        self.assertIn("the glossary already defines `owner`", out)

    def test_a_bullet_closing_on_a_participle_reds_the_absolute_tail_arm(self):
        out = self._red_for("absolute-tail")
        self.assertIn("absolute-tail", out)
        self.assertIn("R1.3", out)
        self.assertIn("bullet 1 closes on `, the rest becoming queue rows`", out)

    def test_a_bullet_carrying_a_bracket_code_reds_the_anchor_noise_arm(self):
        out = self._red_for("anchor-noise")
        self.assertIn("anchor-noise", out)
        self.assertIn("R1.4", out)
        self.assertIn("bullet 1 carries the code anchor [INV-5]", out)

    def test_each_bullet_defect_reds_only_its_own_arm(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(BULLETS_DIRTY, config_with(tmp, zeros()))
            self.assertNotEqual(r.returncode, 0)
            for arm in ARMS:
                self.assertIn("- %s: 1 criteria break it" % arm, r.stdout,
                              "arm %s did not report exactly its own criterion:\n%s"
                              % (arm, r.stdout))

    def test_the_reach_line_counts_the_bullets_it_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(BULLETS_CLEAN, config_with(tmp, zeros()))
            self.assertIn("read the 5 acceptance criteria of the body", r.stdout)
            self.assertIn("6 indented bullet lines", r.stdout)

    def test_a_bullet_at_column_zero_after_a_blank_line_is_outside_the_criterion(self):
        """The sub-list ends at a blank line followed by unindented text. The clean fixture's last
        criterion is followed by such a bullet, long enough to red the word cap were it read."""
        with tempfile.TemporaryDirectory() as tmp:
            r = run(BULLETS_CLEAN, config_with(tmp, zeros()))
            self.assertEqual(r.returncode, 0,
                             "a bullet outside every criterion was read as part of one:\n%s"
                             % r.stdout)

    def test_a_criterion_with_no_bullets_measures_exactly_as_it_did_before(self):
        """The pair that carries no sub-list at all: the same four reds, the same clean run, and
        the same wording on the criterion line's own long-criterion message."""
        with tempfile.TemporaryDirectory() as tmp:
            dirty = run(DIRTY, config_with(tmp, zeros()))
            self.assertNotEqual(dirty.returncode, 0)
            for arm in ARMS:
                self.assertIn("- %s: 1 criteria break it" % arm, dirty.stdout)
            self.assertIn("49 words in one criterion (cap 35)", dirty.stdout)
            self.assertIn("closes on `, the rest becoming queue rows`", dirty.stdout)
            clean = run(CLEAN, config_with(tmp, zeros(), name="cfg2.json"))
            self.assertEqual(clean.returncode, 0, clean.stdout)
            self.assertIn("read the 4 acceptance criteria of the body", clean.stdout)
            self.assertIn("0 indented bullet lines", clean.stdout)


class TestParserOwnsTheBullets(unittest.TestCase):
    """The bullets come off the one shared parser, so every format gate can ask for them."""

    def test_the_shared_parser_hands_a_criterion_its_bullets_and_its_pieces(self):
        sys.path.insert(0, os.path.join(ROOT, "guardrails"))
        import specformat as sf
        with open(BULLETS_DIRTY, encoding="utf-8") as f:
            doc = sf.parse(f.read())
        first = doc.criteria[0]
        self.assertEqual(len(first.bullets), 2)
        self.assertEqual(first.bullets[0].text, "the panel names the place;")
        self.assertEqual([b.index for b in first.bullets], [1, 2])
        self.assertEqual(first.bullets[0].line_no, first.line_no + 1)
        labels = [label for (label, _t, _l) in first.pieces]
        self.assertEqual(labels, [sf.CRITERION_LINE, "bullet 1", "bullet 2"])
        self.assertEqual(first.pieces[0][1], first.body)
        self.assertEqual(doc.criteria[-1].bullets[0].text, "the row cites [INV-5] as its reason.")

    def test_a_criterion_with_no_sub_list_carries_no_bullets(self):
        sys.path.insert(0, os.path.join(ROOT, "guardrails"))
        import specformat as sf
        with open(CLEAN, encoding="utf-8") as f:
            doc = sf.parse(f.read())
        for crit in doc.criteria:
            self.assertEqual(crit.bullets, [])
            self.assertEqual(len(crit.pieces), 1)


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_the_shipped_baselines_hold_on_the_live_spec(self):
        """The recorded counts govern the verdict over the live document: the gate passes while
        every arm stands at or under its recorded count, and reds naming each arm that stands above
        it. This test read the verdict as green until 2026-07-27; it now reads it against the
        recorded counts, because the reach widened to a criterion's bullet sub-list and the numbers
        a document with sub-lists measures under that reach are higher. The recorded counts were
        taken while the gate read the numbered criterion line alone; a document carrying criterion
        sub-lists measures more under the wider reach, and writing those higher numbers into the
        config is a human decision made through the pipeline (INV-288), never a run's own act."""
        sys.path.insert(0, os.path.join(ROOT, "guardrails"))
        import importlib.util
        import specformat as sf
        spec = importlib.util.spec_from_file_location("criterion_readability_gate", GATE)
        gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        cfg = json.load(open(REAL_CONFIG, encoding="utf-8"))
        doc = sf.parse(read(SPEC))    # the whole spec: the core and the parts its map names
        counts = dict((arm, len(hits)) for arm, hits in gate.measure(doc, cfg).items())
        above = [arm for arm in ARMS if counts[arm] > cfg["arms"][arm]["baseline"]]
        r = run_many(spec_paths(), REAL_CONFIG)
        if above:
            self.assertNotEqual(r.returncode, 0,
                                "arms stand above their recorded count and the gate passed: %s\n%s"
                                % (", ".join(above), r.stdout))
            for arm in above:
                self.assertIn("- %s: %d criteria break it, baseline %d"
                              % (arm, counts[arm], cfg["arms"][arm]["baseline"]), r.stdout)
        else:
            self.assertEqual(r.returncode, 0,
                             "every arm stands at or under its recorded count and the gate red:\n%s"
                             % r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        """Its siblings in the format family run through the suite (gate b), not a gate letter."""
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-criterion-readability", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-criterion-readability", f.read())


class TestCriterionLoadArm(unittest.TestCase):
    """The fifth arm sums a criterion's pieces instead of reading them one at a time. A criterion can
    pass the long-criterion arm on every piece — its own line, and every bullet, each under the
    per-piece cap — and still carry more than one rule once the pieces are added together. These two
    small documents are built here rather than added to the shared fixtures: each puts two pieces
    under the per-piece cap into one criterion so their sum alone crosses the total cap, a shape the
    shared fixtures do not carry."""

    # One criterion: a short line, two bullets, each under the 35-word per-piece cap, summing to 70.
    LOAD_ONE = """# Mini spec — one criterion whose bullets alone push it past the total cap

This is a preamble.

## Glossary

- **widget** — one unit the product shows to a person.
- **panel** — the surface a widget sits on.

## Requirement 1: A widget shows on its panel

**Context:** The product shows widgets to a person.

**User Story:** As a person opening a panel, I want its widget to show, so that I see what the panel holds.

### Acceptance Criteria

**Case: the widget shows**

1. *when* a panel opens, the system *shall* show its widget. [INV-1]
   - the widget renders in the exact place the panel already named before the run started, and it keeps that place fixed even while the panel itself is redrawing its own frame around it;
   - every other panel already open on the screen stays completely untouched while this one widget quietly finishes its own render pass from start to end without interruption.
"""

    # Two criteria, each shaped like LOAD_ONE, so a run over this document finds two.
    LOAD_TWO = LOAD_ONE + """2. *when* the panel closes, the system *shall* drop its widget. [INV-2]
   - the widget leaves the place the panel named the moment the panel starts to close, and it never lingers a frame longer than the closing animation itself takes to finish running;
   - every other panel already open on the screen keeps its own widget in place while this one widget quietly finishes leaving the screen for good.
"""

    def _write(self, tmp, text, name="doc.md"):
        path = os.path.join(tmp, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def _cfg(self, tmp, baseline, max_total_words=60, name="cfg.json"):
        """The shipped config with every other arm out of reach and criterion-load set as given."""
        cfg = json.load(open(REAL_CONFIG, encoding="utf-8"))
        for arm in ARMS:
            cfg["arms"][arm]["baseline"] = 999
        cfg["arms"]["criterion-load"]["baseline"] = baseline
        cfg["arms"]["criterion-load"]["threshold"]["max_total_words"] = max_total_words
        path = os.path.join(tmp, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        return path

    def test_a_criterion_under_the_total_cap_passes(self):
        """readability_bullets_clean.md's first criterion sums its line and three bullets to 33
        words, under the 60-word cap, so criterion-load stays silent."""
        with tempfile.TemporaryDirectory() as tmp:
            r = run(BULLETS_CLEAN, self._cfg(tmp, 0))
            self.assertEqual(r.returncode, 0,
                             "a criterion whose line and bullets sum under the cap red:\n%s"
                             % r.stdout)
            self.assertIn("criterion-load=0/0", r.stdout)

    def test_bullets_alone_carry_a_criterion_past_the_cap(self):
        """The line stays at 10 words and each bullet stays under the 35-word per-piece cap, so
        long-criterion never fires; the sum of all three runs to 70, over the 60-word total cap, and
        the message names that total."""
        with tempfile.TemporaryDirectory() as tmp:
            doc = self._write(tmp, self.LOAD_ONE)
            r = run(doc, self._cfg(tmp, 0))
            self.assertNotEqual(r.returncode, 0,
                                "a criterion whose bullets alone push it past the cap passed:\n%s"
                                % r.stdout)
            self.assertIn("criterion-load", r.stdout)
            self.assertIn("R1.1", r.stdout)
            self.assertIn("70 words in this criterion's line and bullets together (cap 60)",
                          r.stdout)

    def test_a_body_past_the_cap_with_no_bullets_reds_both_arms(self):
        """readability_dirty.md's R1.1 carries no bullets and its body alone runs to 49 words: past
        the 35-word long-criterion cap, and — with the total cap lowered to 45 for this run alone —
        past the total cap too. The same one criterion breaks both arms."""
        with tempfile.TemporaryDirectory() as tmp:
            cfg = json.load(open(REAL_CONFIG, encoding="utf-8"))
            cfg["arms"]["long-criterion"]["baseline"] = 0
            cfg["arms"]["inline-gloss"]["baseline"] = 999
            cfg["arms"]["absolute-tail"]["baseline"] = 999
            cfg["arms"]["anchor-noise"]["baseline"] = 999
            cfg["arms"]["criterion-load"]["baseline"] = 0
            cfg["arms"]["criterion-load"]["threshold"]["max_total_words"] = 45
            path = os.path.join(tmp, "cfg.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cfg, f)
            r = run(DIRTY, path)
            self.assertNotEqual(r.returncode, 0, "the over-cap body passed:\n%s" % r.stdout)
            self.assertIn("- long-criterion: 1 criteria break it", r.stdout)
            self.assertIn("- criterion-load: 1 criteria break it", r.stdout)
            self.assertIn(DIRTY_CRITERION["long-criterion"], r.stdout)

    def test_the_recorded_baseline_matches_the_live_document(self):
        """The count the gate measures over the live PRODUCT_SPEC.md, under the shipped config's
        threshold, equals the baseline recorded for it — the same proof the four older arms already
        carry in TestArmedOnTheRealSpec, read here for the fifth."""
        sys.path.insert(0, os.path.join(ROOT, "guardrails"))
        import importlib.util
        import specformat as sf
        spec = importlib.util.spec_from_file_location("criterion_load_gate", GATE)
        gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        cfg = json.load(open(REAL_CONFIG, encoding="utf-8"))
        doc = sf.parse(read(SPEC))    # the whole spec: the core and the parts its map names
        count = len(gate.measure(doc, cfg)["criterion-load"])
        self.assertEqual(count, cfg["arms"]["criterion-load"]["baseline"],
                         "the recorded criterion-load baseline no longer matches the live document")

    def test_a_rise_above_a_recorded_baseline_reds_and_names_the_arm(self):
        """Two criteria break the arm on LOAD_TWO; a baseline of one recorded ahead of that run is a
        rise, and the report names criterion-load, the count, and the baseline it stands above."""
        with tempfile.TemporaryDirectory() as tmp:
            doc = self._write(tmp, self.LOAD_TWO)
            r = run(doc, self._cfg(tmp, 1))
            self.assertNotEqual(r.returncode, 0,
                                "two criteria over a recorded baseline of one did not red:\n%s"
                                % r.stdout)
            self.assertIn("criterion-load: 2 criteria break it, baseline 1", r.stdout)
            typed = [ln for ln in r.stdout.splitlines() if ln.startswith("{")]
            self.assertEqual(len(typed), 1, "a blocking red carries exactly one typed line")
            obj = json.loads(typed[0])
            self.assertEqual(obj["code"], "criterion-readability")
            self.assertIn("criterion-load", obj["message"])


if __name__ == "__main__":
    unittest.main()
