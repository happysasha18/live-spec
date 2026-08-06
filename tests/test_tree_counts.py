"""A count this repository publishes about its own tree is built from the tree (SPEC R306, INV-305).

`guardrails/tree-counts.json` declares each count, `scripts/gen-tree-counts.py` measures the tree and
fills every generated block, and `guardrails/check-tree-counts.py` (gate ad) refuses a push where a
published count and the tree disagree, or where the reproduction command a reader is invited to run
returns something other than the published number.

Red-first: every case below was written and run before the registry, the generator and the gate
existed, so each one failed on a missing file first.

The fixture registry and the pages it names live under `guardrails/tree-count-fixtures/`, so a case
measures a tree it owns and never the repository.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

from conftest import ROOT

GATE = os.path.join(ROOT, "guardrails", "check-tree-counts.py")
GEN = os.path.join(ROOT, "scripts", "gen-tree-counts.py")
REGISTRY = os.path.join(ROOT, "guardrails", "tree-counts.json")
FIXTURES = os.path.join(ROOT, "guardrails", "tree-count-fixtures")
PREPUSH = os.path.join(ROOT, "guardrails", "pre-push")
GATES_YML = os.path.join(ROOT, ".github", "workflows", "gates.yml")
PROOFS = os.path.join(ROOT, "guardrails", "gate-red-proofs.json")

# The fixture registry names its pages relative to the fixture root, so a copy of that root is a
# whole world the gate can be pointed at.
CLEAN_PAGE = "page.txt"
DRIFTED_PAGE = "page-drifted.txt"
SENTENCELESS_PAGE = "page-sentenceless.txt"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def fixture_root(tmp):
    """A private copy of the fixture root, so a case may edit its registry and its pages."""
    root = os.path.join(tmp, "fixtures")
    shutil.copytree(FIXTURES, root)
    return root


def run_gate(root, registry="counts.json", extra=()):
    return subprocess.run(
        ["python3", GATE, "--root", root, "--registry", os.path.join(root, registry), *extra],
        capture_output=True, text=True)


def run_generator(root, registry="counts.json", out_dir=None):
    return subprocess.run(
        ["python3", GEN, "--root", root, "--registry", os.path.join(root, registry),
         "--out-dir", out_dir or root],
        capture_output=True, text=True)


def edit_registry(root, mutate, registry="counts.json"):
    path = os.path.join(root, registry)
    data = json.loads(read(path))
    mutate(data)
    write(path, json.dumps(data, indent=2) + "\n")
    return path


def swap_page(root, variant):
    shutil.copyfile(os.path.join(root, variant), os.path.join(root, CLEAN_PAGE))


def generator_module():
    spec = importlib.util.spec_from_file_location("gen_tree_counts", GEN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def typed_line(stdout):
    """The one typed JSON object a blocking red carries beside its human lines (guardrails/README.md
    convention 1). None where the output carries no such line."""
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except ValueError:
                continue
    return None


class TestTheCleanFixture(unittest.TestCase):
    def test_the_gate_and_the_generator_ship(self):
        self.assertTrue(os.path.isfile(GATE), "guardrails/check-tree-counts.py is not on disk")
        self.assertTrue(os.path.isfile(GEN), "scripts/gen-tree-counts.py is not on disk")
        self.assertTrue(os.path.isfile(REGISTRY), "guardrails/tree-counts.json is not on disk")

    def test_the_clean_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            r = run_gate(root)
            self.assertEqual(r.returncode, 0, "the gate red a clean fixture:\n%s" % r.stdout)

    def test_the_reach_line_names_counts_pages_commands_and_seconds(self):
        # R306.14: the green line names every count read, every page swept, every command run, and
        # the seconds the run took.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            r = run_gate(root)
            self.assertEqual(r.returncode, 0, r.stdout)
            for needle in ("fixture-lines", "fixture-floor", CLEAN_PAGE,
                           "cat tree/*.txt | wc -l", "seconds"):
                self.assertIn(needle, r.stdout, "the reach line misses %r:\n%s" % (needle, r.stdout))

    def test_the_green_line_states_what_the_gate_leaves_to_the_person(self):
        # R306.16: the gate judges whether a published count matches the tree and leaves the rest to
        # a person.
        with tempfile.TemporaryDirectory() as tmp:
            r = run_gate(fixture_root(tmp))
            self.assertIn("worth publishing", r.stdout)


class TestTheDriftArm(unittest.TestCase):
    def test_a_drifted_block_reds(self):
        # R306.4 (case 4): the committed block states four lines where a fresh build states five.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            swap_page(root, DRIFTED_PAGE)
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "a drifted block passed:\n%s" % r.stdout)
            self.assertIn("fixture-lines", r.stdout)
            self.assertIn(CLEAN_PAGE, r.stdout)

    def test_a_drifted_block_reds_the_published_number_against_its_own_command(self):
        # R306.6 (case 6): the second arm names the published number, the measured number, and the
        # command the page invites a reader to run.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            swap_page(root, DRIFTED_PAGE)
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, r.stdout)
            self.assertIn("cat tree/*.txt | wc -l", r.stdout)
            self.assertIn("5", r.stdout)

    def test_a_red_carries_one_typed_line(self):
        # guardrails/README.md convention 1.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            swap_page(root, DRIFTED_PAGE)
            r = run_gate(root)
            record = typed_line(r.stdout)
            self.assertIsNotNone(record, "a blocking red carried no typed line:\n%s" % r.stdout)
            for field in ("severity", "code", "message", "fix"):
                self.assertIn(field, record)

    def test_a_missing_marker_pair_reds_naming_the_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            page = os.path.join(root, CLEAN_PAGE)
            text = re.sub(r"<!-- /?generated:count:fixture-lines[^>]*-->", "", read(page))
            write(page, text)
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "a page with no marker pair passed:\n%s" % r.stdout)
            self.assertIn(CLEAN_PAGE, r.stdout)


class TestTheSentenceArm(unittest.TestCase):
    def test_a_page_missing_its_rendered_sentence_reds(self):
        # R306.5 (case 5): the page says six lines where the template renders five.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            swap_page(root, SENTENCELESS_PAGE)
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "a lost sentence passed:\n%s" % r.stdout)
            self.assertIn(CLEAN_PAGE, r.stdout)
            self.assertIn("Five lines stand in the fixture tree.", r.stdout)

    def test_the_generator_writes_no_text_at_a_sentence_home(self):
        # R306.5: the generator owns block text alone; a hand-written sentence stays as written.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            swap_page(root, SENTENCELESS_PAGE)
            r = run_generator(root)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("Six lines stand in the fixture tree.",
                          read(os.path.join(root, CLEAN_PAGE)))

    def test_a_sentence_wrapped_across_lines_still_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            page = os.path.join(root, CLEAN_PAGE)
            write(page, read(page).replace("Five lines stand in the fixture tree.",
                                           "Five lines stand\nin the fixture tree."))
            r = run_gate(root)
            self.assertEqual(r.returncode, 0, "a wrapped sentence red the gate:\n%s" % r.stdout)


class TestTheFloor(unittest.TestCase):
    def test_a_floor_the_tree_falls_below_reds(self):
        # R306.7 (case 7): the fixture tree holds five lines and the floor is raised to nine.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)

            def raise_floor(data):
                data["counts"]["fixture-floor"]["measurements"][0]["floor"] = 9

            edit_registry(root, raise_floor)
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "a tree below its floor passed:\n%s" % r.stdout)
            self.assertIn("9", r.stdout)
            self.assertIn("fixture-floor", r.stdout)

    def test_a_tree_above_its_floor_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run_gate(fixture_root(tmp))
            self.assertEqual(r.returncode, 0, r.stdout)


class TestWhatTheGateMayExecute(unittest.TestCase):
    def test_a_program_outside_the_allowlist_reds_and_runs_no_stage(self):
        # R306.10 (case 10): the first token of a stage reads python3, which the allowlist omits.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            r = run_gate(root, registry="counts-outside-allowlist.json")
            self.assertNotEqual(r.returncode, 0, "a program outside the allowlist ran:\n%s" % r.stdout)
            self.assertIn("python3", r.stdout)
            self.assertIn("ran no stage", r.stdout)

    def test_an_argument_that_leaves_the_repository_root_reds(self):
        # R306.11: a token climbing out of the root, and an absolute token.
        for token in ("../outside/*.txt", "/etc/hosts"):
            with tempfile.TemporaryDirectory() as tmp:
                root = fixture_root(tmp)

                def point_outside(data):
                    data["counts"]["fixture-lines"]["measurements"][0]["argv"][0][1] = token

                edit_registry(root, point_outside)
                r = run_gate(root)
                self.assertNotEqual(r.returncode, 0, "%r passed:\n%s" % (token, r.stdout))
                self.assertIn(token, r.stdout)

    def test_an_argument_holding_a_newline_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)

            def newline(data):
                data["counts"]["fixture-lines"]["measurements"][0]["argv"][0][1] = "tree/*.txt\nrm"

            edit_registry(root, newline)
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "a token holding a newline passed:\n%s" % r.stdout)

    def test_a_shell_metacharacter_is_an_ordinary_argument(self):
        """No shell stands between the registry and the program, so a token carrying a semicolon is
        one file name, and it matches nothing on disk."""
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            marker = os.path.join(tmp, "ran.txt")

            def inject(data):
                data["counts"]["fixture-lines"]["measurements"][0]["argv"][0][1] = (
                    "tree/one.txt; touch %s" % marker)

            edit_registry(root, inject)
            run_gate(root)
            self.assertFalse(os.path.exists(marker), "a token was handed to a shell")

    def test_the_published_command_is_rendered_from_the_argument_list(self):
        # R306.8: the reader's copy and the gate's execution are one field.
        module = generator_module()
        rendered = module.render_command([["cat", "tree/*.txt"], ["wc", "-l"]])
        self.assertEqual(rendered, "cat tree/*.txt | wc -l")


class TestTheGateMeasuresWhatThePushSends(unittest.TestCase):
    def _repo(self, tmp):
        root = fixture_root(tmp)
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        subprocess.run(["git", "init", "-q", root], check=True, env=env)
        subprocess.run(["git", "add", "counts.json", "counts-outside-allowlist.json", "page.txt",
                        "page-drifted.txt", "page-sentenceless.txt", "tree/one.txt", "tree/two.txt"],
                       cwd=root, check=True, env=env)
        subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=root, check=True, env=env)
        return root

    def test_an_uncommitted_measured_path_reds(self):
        # R306.12 (case 12): a measured file carries an edit the push does not send.
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            self.assertEqual(run_gate(root).returncode, 0, "the committed fixture repository red")
            with open(os.path.join(root, "tree", "one.txt"), "a", encoding="utf-8") as f:
                f.write("zeta\n")
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "an uncommitted measured path passed:\n%s" % r.stdout)
            self.assertIn("tree/one.txt", r.stdout)

    def test_an_uncommitted_page_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            page = os.path.join(root, CLEAN_PAGE)
            write(page, read(page) + "\nA line a person added and did not commit.\n")
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "an uncommitted page passed:\n%s" % r.stdout)
            self.assertIn(CLEAN_PAGE, r.stdout)


class TestVacuity(unittest.TestCase):
    def test_an_empty_registry_reds_by_name(self):
        # R306.13 (case 13): a registry parsing to zero counts reports clean over nothing.
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            edit_registry(root, lambda data: data.update({"counts": {}}))
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "an empty registry passed:\n%s" % r.stdout)
            self.assertIn("EMPTY", r.stdout.upper())

    def test_a_pattern_matching_no_file_reds_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)

            def nothing(data):
                data["counts"]["fixture-lines"]["measurements"][0]["argv"][0][1] = "tree/*.none"

            edit_registry(root, nothing)
            r = run_gate(root)
            self.assertNotEqual(r.returncode, 0, "a pattern matching nothing passed:\n%s" % r.stdout)
            self.assertIn("tree/*.none", r.stdout)


class TestTheGroundEveryCountCarries(unittest.TestCase):
    def _refuses(self, mutate):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            edit_registry(root, mutate)
            r = run_generator(root)
            self.assertNotEqual(r.returncode, 0, "the generator built it:\n%s" % r.stdout)
            return r.stdout

    def test_the_generator_refuses_an_empty_ground_field(self):
        # R306.2: each of the seven parts is owed.
        for field in ("counts", "unit", "decision", "on_move", "compared_to", "better", "target"):
            def blank(data, field=field):
                data["counts"]["fixture-lines"]["ground"][field] = ""

            out = self._refuses(blank)
            self.assertIn(field, out)

    def test_the_generator_refuses_a_missing_ground_field(self):
        def drop(data):
            del data["counts"]["fixture-lines"]["ground"]["decision"]

        self.assertIn("decision", self._refuses(drop))

    def test_an_empty_baseline_carrying_no_reason_is_refused(self):
        # R306.3: an empty baseline is accepted with a written reason and refused without one.
        def reasonless(data):
            data["counts"]["fixture-floor"]["ground"]["compared_to"] = {"value": "", "reason": ""}

        self.assertIn("compared_to", self._refuses(reasonless))

    def test_an_empty_baseline_carrying_a_reason_builds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            r = run_generator(root)
            self.assertEqual(r.returncode, 0, "the fixture's reasoned empty baseline refused:\n%s"
                             % r.stdout)

    def test_a_direction_outside_the_three_words_is_refused(self):
        def sideways(data):
            data["counts"]["fixture-lines"]["ground"]["better"] = "sideways"

        self.assertIn("better", self._refuses(sideways))

    def test_a_word_outside_the_cardinal_table_is_refused(self):
        # The word renderer holds one through twenty. A value above it reds by name, so the
        # renderer's edge is visible on the line that reds.
        def big(data):
            entry = data["counts"]["fixture-lines"]
            entry["measurements"][0]["argv"] = [["cat", "tree/*.txt"], ["wc", "-c"]]

        out = self._refuses(big)
        self.assertIn("cardinal", out.lower())


class TestTheGeneratorWritesAllOrNothing(unittest.TestCase):
    def test_a_refused_build_leaves_the_page_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            before = read(os.path.join(root, CLEAN_PAGE))
            edit_registry(root, lambda data: data["counts"]["fixture-lines"]["ground"]
                          .update({"unit": ""}))
            r = run_generator(root)
            self.assertNotEqual(r.returncode, 0, r.stdout)
            self.assertEqual(before, read(os.path.join(root, CLEAN_PAGE)),
                             "a refused build wrote to the page")

    def test_the_generator_fills_a_placeholder_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture_root(tmp)
            page = os.path.join(root, CLEAN_PAGE)
            swap_page(root, DRIFTED_PAGE)
            self.assertNotEqual(run_gate(root).returncode, 0)
            r = run_generator(root)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertEqual(run_gate(root).returncode, 0,
                             "the gate red a page the generator had just filled")
            self.assertIn("holds 5 lines", read(page))


class TestTheRealRegistry(unittest.TestCase):
    def test_the_registry_parses_and_declares_the_four_counts(self):
        data = json.loads(read(REGISTRY))
        self.assertEqual(sorted(data["counts"]),
                         ["gate-roster", "prover-records", "scaffold-checks", "skills-lines"])

    def test_every_count_carries_its_seven_ground_parts(self):
        data = json.loads(read(REGISTRY))
        for name, entry in data["counts"].items():
            for field in ("counts", "unit", "decision", "on_move", "compared_to", "better",
                          "target"):
                self.assertIn(field, entry["ground"], "%s carries no `%s`" % (name, field))

    def test_every_measurement_names_an_allowed_program(self):
        data = json.loads(read(REGISTRY))
        allowed = set(data["allowed_programs"])
        for name, entry in data["counts"].items():
            for measurement in entry["measurements"]:
                for stage in measurement["argv"]:
                    self.assertIn(stage[0], allowed, "%s runs %s" % (name, stage[0]))

    def test_every_home_names_a_page_that_stands(self):
        data = json.loads(read(REGISTRY))
        for name, entry in data["counts"].items():
            for home in entry["homes"]:
                self.assertTrue(os.path.isfile(os.path.join(ROOT, home["page"])),
                                "%s names the page %s, which is not there" % (name, home["page"]))

    def test_the_registry_says_an_argument_list_is_a_code_surface(self):
        self.assertIn("reviewed the way a change to a check script is reviewed", read(REGISTRY))


class TestTheWiring(unittest.TestCase):
    def test_the_gate_runs_as_gate_ad_on_the_push_hook(self):
        prepush = read(PREPUSH)
        self.assertIn("-- gate ad:", prepush)
        self.assertIn("check-tree-counts.py", prepush)

    def test_the_push_hook_passes_no_uncommitted_carve_out(self):
        """The precondition is what makes a green line rest on bytes the push sends, so the chain
        never hands the gate the flag that stands it down."""
        self.assertNotIn("--allow-uncommitted", read(PREPUSH))

    def test_the_ci_workflow_carries_the_matching_step(self):
        yml = read(GATES_YML)
        self.assertIn("gate ad", yml)
        self.assertIn("check-tree-counts.py", yml)

    def test_the_red_proof_is_registered(self):
        entry = json.loads(read(PROOFS))["proofs"]["ad"]
        self.assertEqual(entry["reds"], "check-tree-counts")
        self.assertTrue(entry["proof"].startswith("tests/test_tree_counts.py::"))
        self.assertIn(entry["proof"].split("::", 1)[1], read(os.path.abspath(__file__)))


if __name__ == "__main__":
    unittest.main()
