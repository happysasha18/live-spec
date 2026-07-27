"""The criterion-readability ratchet (SPEC INV-287, INV-288).

`guardrails/check-criterion-readability.py` reads the acceptance criteria of a requirements-format
document through four arms — a criterion over the word cap, a definition-shaped aside inside a
criterion, a closing clause with no finite verb, and an anchor that competes with the prose — and
compares each arm's count against the baseline recorded in `guardrails/criterion-readability.json`.
A rise reds; a count at the baseline passes; a fall passes and re-baselines under `--rebaseline`.

Each arm is proven in both directions against a pair of fixtures that differ only in the defect:
`readability_dirty.md` carries exactly one criterion per arm, `readability_clean.md` carries the
same four rules written to the bar. The fixture config seeds every baseline at zero, so a single
violating criterion is a rise and reds.
"""
import json
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

GATE = os.path.join(ROOT, "guardrails", "check-criterion-readability.py")
REAL_CONFIG = os.path.join(ROOT, "guardrails", "criterion-readability.json")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
DIRTY = os.path.join(FX, "readability_dirty.md")
CLEAN = os.path.join(FX, "readability_clean.md")
ARMS = ("long-criterion", "inline-gloss", "absolute-tail", "anchor-noise")

# Which criterion of readability_dirty.md each arm is meant to catch, and the words its report must
# put in front of the writer.
DIRTY_CRITERION = {
    "long-criterion": "R1.1",
    "inline-gloss": "R1.2",
    "absolute-tail": "R1.3",
    "anchor-noise": "R1.4",
}


def run(doc, config=None, *flags):
    env = dict(os.environ)
    if config is not None:
        env["CRITERION_READABILITY_CONFIG"] = config
    return subprocess.run(["python3", GATE, doc] + list(flags),
                          capture_output=True, text=True, env=env)


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


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_the_shipped_baselines_hold_on_the_live_spec(self):
        r = run(os.path.join(ROOT, "PRODUCT_SPEC.md"), REAL_CONFIG)
        self.assertEqual(r.returncode, 0,
                         "the readability ratchet red the live spec — a delivery raised one of the "
                         "four counts:\n%s" % r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        """Its siblings in the format family run through the suite (gate b), not a gate letter."""
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-criterion-readability", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-criterion-readability", f.read())


if __name__ == "__main__":
    unittest.main()
