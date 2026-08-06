"""Gate ae — the check registry records what each runnable file is (SPEC INV-306, M-505..M-511).

A skill body names a check by path, and a project that adopts the pack holds almost none of those
paths. Before that can be repaired the pack owes an honest record: per runnable file, what it is,
which tree it judges, whether it belongs in an adopting project, and what it needs to run. That
record is `scripts/check-registry.json` and `guardrails/check-named-checks.py` keeps it true.

The red-first proofs are `test_gate_reds_a_pack_only_check_named_in_a_skill_body`, which drives the
gate to a non-zero exit over a skill body naming a check that measures this pack's own machinery,
and `test_gate_reds_a_root_declared_argument_over_an_own_tree_default`, which drives it to a
non-zero exit over an entry whose recorded root disagrees with the default in its own source.

Each red below runs the gate over the real tree with one field replaced in a copy of the registry,
or over a fixture skill directory. No test writes inside the tree it reads.
"""
import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "guardrails", "check-named-checks.py")
REGISTRY = os.path.join(ROOT, "scripts", "check-registry.json")

CENSUS_LINE = "- the census, `python3 scripts/rule-census.py`.\n"


def load_registry():
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


def run(registry_path=None, skills_dir=None):
    cmd = ["python3", GATE, "--root", ROOT]
    if registry_path:
        cmd += ["--registry", registry_path]
    if skills_dir:
        cmd += ["--skills", skills_dir]
    return subprocess.run(cmd, capture_output=True, text=True)


def run_with(mutate):
    """Run the gate over the real tree with one edit applied to a copy of the registry."""
    data = load_registry()
    mutate(data)
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "check-registry.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return run(registry_path=path)


def skills_fixture(tmp, body):
    """Build a one-skill directory holding BODY as a skill body, and return the directory."""
    skill_dir = os.path.join(tmp, "text-audit")
    os.makedirs(skill_dir)
    path = os.path.join(skill_dir, "SKILL.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return tmp, path


class TestCheckRegistry(unittest.TestCase):

    def test_the_real_tree_passes(self):
        r = run()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_the_green_run_states_its_reach(self):
        r = run()
        self.assertIn("reach:", r.stdout)
        self.assertIn("check-named-checks", r.stdout)
        self.assertIn("entries read", r.stdout)
        self.assertIn("skill bodies scanned", r.stdout)
        self.assertIn("command-position paths found", r.stdout)

    def test_gate_reds_a_pack_only_check_named_in_a_skill_body(self):
        """RED-FIRST: a check that measures this pack's own machinery, named in a skill body.

        check-named-checks reds, names the skill file, names the line, and names the reach that
        makes the check pack-only.
        """
        with tempfile.TemporaryDirectory() as tmp:
            body = "# Text audit\n\nThe structure checks:\n\n" + CENSUS_LINE
            skills_dir, skill_path = skills_fixture(tmp, body)
            r = run(skills_dir=skills_dir)
            self.assertNotEqual(r.returncode, 0,
                                "a pack-only check in a skill body passed:\n%s" % r.stdout)
            self.assertIn("SKILL.md", r.stdout)
            self.assertIn(":5", r.stdout)
            self.assertIn("guardrails/language-rules.json", r.stdout)

    def test_gate_reds_a_root_declared_argument_over_an_own_tree_default(self):
        """RED-FIRST: an entry recording root argument whose source defaults the root to its own tree."""
        def flip(data):
            data["entries"]["scripts/sweep-rendered.py"]["root"] = "argument"
        r = run_with(flip)
        self.assertNotEqual(r.returncode, 0,
                            "a declared argument over an own-tree default passed:\n%s" % r.stdout)
        self.assertIn("scripts/sweep-rendered.py", r.stdout)
        self.assertIn("309", r.stdout)

    def test_gate_reds_an_entry_whose_key_names_no_file(self):
        def add_missing(data):
            data["entries"]["guardrails/check-nothing-at-all.py"] = {
                "kind": "check", "name": "nothing-at-all", "kit": "ships",
                "root": "argument", "reach": [], "needs": []}
        r = run_with(add_missing)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("guardrails/check-nothing-at-all.py", r.stdout)

    def test_gate_reds_a_kind_that_disagrees_with_the_tree(self):
        def relabel(data):
            entry = data["entries"]["guardrails/specformat.py"]
            entry["kind"] = "check"
            entry["name"] = "specformat"
            entry["kit"] = "ships"
            entry["root"] = "argument"
            entry["reach"] = []
        r = run_with(relabel)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("guardrails/specformat.py", r.stdout)
        self.assertIn("library", r.stdout)

    def test_gate_reds_a_duplicate_name(self):
        def duplicate(data):
            data["entries"]["guardrails/check-one-name.py"]["name"] = "vocabulary"
        r = run_with(duplicate)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("vocabulary", r.stdout)

    def test_gate_reds_a_document_the_source_states_and_the_reach_omits(self):
        def drop(data):
            entry = data["entries"]["guardrails/check-freeze.sh"]
            entry["reach"] = [m for m in entry["reach"] if m != "ARCHITECTURE.md"]
        r = run_with(drop)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("ARCHITECTURE.md", r.stdout)

    def test_gate_reds_a_reach_member_that_names_a_missing_path(self):
        def stale(data):
            data["entries"]["guardrails/check-doc-findings-bound.py"]["reach"] = [
                "guardrails/rule-census.json", "guardrails/no-such-record.json"]
        r = run_with(stale)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("guardrails/no-such-record.json", r.stdout)

    def test_gate_reds_an_imported_module_missing_from_needs(self):
        def drop(data):
            entry = data["entries"]["guardrails/check-vocabulary.py"]
            entry["needs"] = [m for m in entry["needs"] if m != "guardrails/specformat.py"]
        r = run_with(drop)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("guardrails/specformat.py", r.stdout)

    def test_gate_reds_a_needs_member_that_is_no_registry_entry(self):
        def add(data):
            data["entries"]["guardrails/check-vocabulary.py"]["needs"].append(
                "guardrails/check-board.py")
        r = run_with(add)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("guardrails/check-board.py", r.stdout)

    def test_gate_reds_a_command_position_path_with_no_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            body = "# A skill\n\nRun `python3 guardrails/check-board.py` at the end.\n"
            skills_dir, skill_path = skills_fixture(tmp, body)
            r = run(skills_dir=skills_dir)
            self.assertNotEqual(r.returncode, 0, r.stdout)
            self.assertIn("guardrails/check-board.py", r.stdout)
            self.assertIn(":3", r.stdout)

    def test_gate_reds_a_kit_that_disagrees_with_its_reach(self):
        def relabel(data):
            data["entries"]["guardrails/check-vocabulary.py"]["kit"] = "pack-only"
        r = run_with(relabel)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("guardrails/check-vocabulary.py", r.stdout)
        self.assertIn("ships", r.stdout)

    def test_gate_reds_a_name_on_a_library_entry(self):
        def name_it(data):
            data["entries"]["guardrails/specformat.py"]["name"] = "specformat"
        r = run_with(name_it)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("guardrails/specformat.py", r.stdout)

    def test_every_check_entry_carries_the_five_fields(self):
        entries = load_registry()["entries"]
        for key, entry in entries.items():
            if entry.get("kind") != "check":
                continue
            for field in ("name", "kit", "root", "reach", "needs"):
                self.assertIn(field, entry, "%s carries no %s" % (key, field))

    def test_the_registry_records_one_entry_per_kind_it_states(self):
        entries = load_registry()["entries"]
        kinds = sorted(set(e.get("kind") for e in entries.values()))
        self.assertEqual(kinds, ["check", "data", "library"])
        checks = [k for k, e in entries.items() if e["kind"] == "check"]
        self.assertEqual(len(checks), len(set(e["name"] for k, e in entries.items()
                                              if e["kind"] == "check")),
                         "two checks share one name")

    def test_the_registry_is_an_unchanged_copy_after_every_red_above(self):
        """Each red runs off a copy, so the committed registry is untouched by this file."""
        first = load_registry()
        run_with(lambda data: data["entries"].pop("guardrails/check-vocabulary.py"))
        self.assertEqual(first, load_registry())


if __name__ == "__main__":
    unittest.main()
