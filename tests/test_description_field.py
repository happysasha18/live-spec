"""The Formal-index non-empty description-field gate (SPEC INV-239, M-421; E-35/INV-239, M-423).

The named-reference pair gives every registered code a plain one-sentence description, and that
description's one home is a dedicated field the Formal index gains [E-35, base rule 4]. This suite
covers the mechanical presence net over that field — `guardrails/attic/check-description-field.py` — and
the field's own existence in the shipped index.

Two facts sit under one owning test file, as the matrix rows say (M-421 the gate, M-423 the field):
the gate reds a registered code whose description field is empty and passes one that carries a
description, judging PRESENCE alone and never whether the description reads well or matches the item
(that semantic read is the human sampling net, INV-41); and it ships DORMANT — the existing code set
carries no rich descriptions yet (the back-describe migration is a future his-gated landing, INV-217,
folded finding N5), so an armed gate would red the whole tree, and the gate stays down until the
migration arms it through `guardrails/attic/description-field.json`.

Every armed/dormant case drives the real shipped script over a FIXTURE Formal-index snippet and a
FIXTURE config, so the real `guardrails/attic/description-field.json` is never flipped and the real tree
stays green under the dormant ship.
"""
import json
import os
import re
import subprocess
import tempfile
import unittest

from conftest import ROOT, read, read_flat

GATE = os.path.join(ROOT, "guardrails", "attic", "check-description-field.py")


def run_gate(spec_path=None, config_path=None):
    """Drive the shipped gate, pointing it at a fixture spec and/or a fixture config.

    Returns the CompletedProcess; the gate prints its finding to stdout and carries its verdict in
    the exit code (0 clean or dormant, non-zero on a red), the file-read-and-exit-code level the
    sibling index gates take [M-399, M-400].
    """
    env = dict(os.environ)
    if spec_path is not None:
        env["DESCRIPTION_FIELD_SPEC"] = spec_path
    if config_path is not None:
        env["DESCRIPTION_FIELD_CONFIG"] = config_path
    return subprocess.run(["python3", GATE], env=env, capture_output=True, text=True)


def write(tmp, name, text):
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


# A Formal-index snippet carrying the description field the migration adds — a dedicated Description
# column. INV-1 carries its description; INV-2's field is empty (the seeded red).
INDEX_WITH_EMPTY = """\
## Formal index

| Anchor | One line | Description | Section |
|---|---|---|---|
| INV-1 | no wish lost | Every wish a person throws reaches a recorded terminal state. | Throwing a wish |
| INV-2 | queue rows |  | Machines |
"""

# The same shape with every description present — the seeded green.
INDEX_ALL_DESCRIBED = """\
## Formal index

| Anchor | One line | Description | Section |
|---|---|---|---|
| INV-1 | no wish lost | Every wish a person throws reaches a recorded terminal state. | Throwing a wish |
| INV-2 | queue rows | Every wish is a row in the queue, so no request is tracked by memory. | Machines |
"""

# A row that OMITS its Description cell — three cells where the header names four. A header→cell zip
# would slide the multi-word Section text into the description slot and false-pass; the short-row
# guard must red it instead.
INDEX_OMITTED_CELL = """\
## Formal index

| Anchor | One line | Description | Section |
|---|---|---|---|
| INV-1 | no wish lost | Every wish a person throws reaches a recorded terminal state. | Throwing a wish |
| INV-2 | queue rows | When agents work together |
"""

# A row whose Description is a single character — present in the cell but no real description. The
# presence floor (at least two plain words, the floor the deposit lint shares) must red it.
INDEX_ONE_CHAR = """\
## Formal index

| Anchor | One line | Description | Section |
|---|---|---|---|
| INV-1 | no wish lost | Every wish a person throws reaches a recorded terminal state. | Throwing a wish |
| INV-2 | queue rows | x | Machines |
"""

ARMED = json.dumps({"armed": True, "reason": "test fixture — armed"})
DORMANT = json.dumps({"armed": False, "reason": "test fixture — dormant"})


class TestDescriptionFieldGate(unittest.TestCase):
    """M-421: the presence gate reds an empty description field and passes a carried one, and stays
    dormant until the back-describe migration arms it."""

    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE), "the gate script does not ship: %s" % GATE)
        self.assertTrue(os.access(GATE, os.X_OK) or GATE.endswith(".py"),
                        "the gate is not runnable")

    def test_gate_reds_a_code_with_an_empty_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write(tmp, "spec.md", INDEX_WITH_EMPTY)
            cfg = write(tmp, "cfg.json", ARMED)
            r = run_gate(spec, cfg)
            self.assertNotEqual(r.returncode, 0,
                                "the armed gate passed a code with an empty description field:\n%s" % r.stdout)
            self.assertIn("INV-2", r.stdout, "the red does not name the offending code")

    def test_gate_passes_a_code_that_carries_a_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write(tmp, "spec.md", INDEX_ALL_DESCRIBED)
            cfg = write(tmp, "cfg.json", ARMED)
            r = run_gate(spec, cfg)
            self.assertEqual(r.returncode, 0,
                             "the armed gate red a fully described index:\n%s" % r.stdout)

    def test_gate_reds_a_code_that_omits_its_description_cell(self):
        # A row shorter than the header omits a cell — a missing description, red exactly like an empty
        # one. Parsing by column index alone would slide the Section text into the description slot and
        # false-pass; the short-row guard reds it and names the code.
        with tempfile.TemporaryDirectory() as tmp:
            spec = write(tmp, "spec.md", INDEX_OMITTED_CELL)
            cfg = write(tmp, "cfg.json", ARMED)
            r = run_gate(spec, cfg)
            self.assertNotEqual(r.returncode, 0,
                                "the armed gate passed a row that omits its description cell:\n%s" % r.stdout)
            self.assertIn("INV-2", r.stdout, "the red does not name the code with the omitted cell")

    def test_gate_reds_a_one_character_description(self):
        # The presence floor is at least two plain words — the floor the deposit lint shares — so a
        # single-character cell is not a description. Presence only, never a correctness read.
        with tempfile.TemporaryDirectory() as tmp:
            spec = write(tmp, "spec.md", INDEX_ONE_CHAR)
            cfg = write(tmp, "cfg.json", ARMED)
            r = run_gate(spec, cfg)
            self.assertNotEqual(r.returncode, 0,
                                "the armed gate passed a one-character description:\n%s" % r.stdout)
            self.assertIn("INV-2", r.stdout, "the red does not name the thinly-described code")

    def test_gate_stays_dormant_until_the_migration_arms_it(self):
        # A tree whose description fields are empty (every code) — armed this reds the whole tree, so
        # the dormant ship must exit 0 on exactly this tree, proving the arming guard, not luck.
        with tempfile.TemporaryDirectory() as tmp:
            spec = write(tmp, "spec.md", INDEX_WITH_EMPTY)
            cfg = write(tmp, "cfg.json", DORMANT)
            r = run_gate(spec, cfg)
            self.assertEqual(r.returncode, 0,
                             "the dormant gate did not stand down on a tree with empty fields:\n%s" % r.stdout)
            self.assertIn("dormant", r.stdout.lower(), "the dormant gate does not say it stood down")

    def test_gate_judges_presence_not_semantic_match(self):
        # A description that is present but plainly wrong for the code (a mismatch) still PASSES: the
        # gate judges presence alone, the semantic read belonging to the human net [INV-41].
        mismatched = INDEX_ALL_DESCRIBED.replace(
            "Every wish is a row in the queue, so no request is tracked by memory.",
            "This sentence has nothing to do with the queue and is simply wrong for the code.")
        with tempfile.TemporaryDirectory() as tmp:
            spec = write(tmp, "spec.md", mismatched)
            cfg = write(tmp, "cfg.json", ARMED)
            r = run_gate(spec, cfg)
            self.assertEqual(r.returncode, 0,
                             "the gate reached past presence into a semantic match:\n%s" % r.stdout)

    def test_real_config_ships_retired(self):
        # RETIRED at the row-445 requirements-format conversion with its stated successor (the stage-1
        # design record, docs/prover/2026-07-22-row445-spec-format-delta.md): the criteria and the
        # glossary are the authored home of every code's plain statement, and the generated index
        # carries locations only (INV-271) — no description column remains for this gate to read. The
        # config ships disarmed and names that retirement; the fixture tests above keep the mechanism's
        # red-proof alive. Successor pair: check-description-field -> check-index-generated (gate x) +
        # tests/test_index_generated.py::TestArmedOnTheRealSpec.
        cfg = json.loads(read("guardrails/attic/description-field.json"))
        self.assertFalse(cfg["armed"],
                         "the description-field gate re-armed — it retired at the requirements-format "
                         "conversion; its successor is the generated-index gate (INV-271)")
        self.assertIn("RETIRED", cfg.get("reason", ""),
                      "the disarmed config must name its retirement and successor")

    def test_retired_gate_stands_down_by_name_on_the_real_tree(self):
        # No env override: the retired gate reads the real config (disarmed) and stands down by name,
        # exit 0 — it never reds the conversion-format tree whose index carries no description column.
        r = run_gate()
        self.assertEqual(r.returncode, 0,
                         "the retired gate did not stand down cleanly:\n%s\n%s" % (r.stdout, r.stderr))
        self.assertIn("dormant", r.stdout.lower())

    def test_gate_not_wired_into_pre_push(self):
        # It rides the suite (gate b) and takes NO push-gate letter, so it is never invoked from the
        # pre-push chain or the CI mirror directly (the far-tier placement).
        self.assertNotIn("check-description-field", read("guardrails/pre-push"),
                         "the gate is invoked in pre-push — it must ride the suite, not take a letter")
        self.assertNotIn("check-description-field", read(".github/workflows/gates.yml"),
                         "the gate has its own CI step — it must ride the suite pytest step")


class TestDescriptionFieldTraceability(unittest.TestCase):
    """M-421/M-423 doc-structural checks: the law stands in the spec, the Formal index, and the
    architecture (the traceability quartet), and the field's own existence in the shipped index."""

    def test_spec_states_the_law(self):
        # Pass 2 of the row-445 conversion landed the format-laws requirements (INV-250..271) and
        # rewrote the description-field claims: the pair law stands, the description field is
        # redefined as the authored home (criterion + glossary), and the gate's retirement with its
        # stated successor is now the spec's own criterion.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("plain one-sentence description pinned to the item at its owning surface", spec,
                      "SPEC lost the code-plus-description pair law (INV-239/E-35)")
        self.assertIn("the dedicated description-field gate *shall* retire with the criteria and "
                      "the glossary as its stated successor", spec,
                      "SPEC lost the gate's retire-with-successor criterion (INV-239/INV-271)")
        self.assertIn("the authored home of a code's plain statement", spec,
                      "SPEC lost the description field's authored-home definition")

    def test_formal_index_row(self):
        # The generated index (## Reference) carries locations only (INV-271); the row's presence
        # proves INV-239 is carried by a body criterion.
        spec = read("PRODUCT_SPEC.md")
        index = spec.split("## Reference", 1)[1]
        self.assertRegex(index, r"\|\s*INV-239\s*\|", "the generated index carries no INV-239 row")

    def test_architecture_owns_the_invariant(self):
        arch = read_flat("ARCHITECTURE.md")
        self.assertIn("check-description-field.py", arch,
                      "ARCHITECTURE does not own the description-field gate under its guardrails node")
        self.assertIn("INV-239", arch, "ARCHITECTURE lost the INV-239 anchor")

    def test_matrix_row_covers_the_law(self):
        matrix = read("TEST_MATRIX.md")
        self.assertRegex(matrix, r"\|\s*M-421\s*\|", "TEST_MATRIX lost the M-421 row")
        self.assertIn("check-description-field.py", matrix, "M-421 row does not name the gate script")

    def test_index_carries_locations_only_with_criteria_as_the_authored_home(self):
        # M-423 re-aimed at the successor shape (INV-271, the row-445 conversion): a bare code never
        # stands alone before a reader because every code's plain statement lives on its BODY criterion
        # (the authored home) while the generated index carries LOCATIONS ONLY. Two arms: the table's
        # second column is location tokens (Rn.k), never prose; and every table code resolves to a body
        # criterion (the symmetry test_formal_index re-proves suite-wide; asserted here for INV-239's
        # own row as this law's worked instance).
        spec = read("PRODUCT_SPEC.md")
        index = spec.split("## Reference", 1)[1]
        row = next((ln for ln in index.splitlines() if ln.startswith("| INV-239 |")), None)
        self.assertIsNotNone(row, "the generated index carries no INV-239 row")
        locations = row.strip().strip("|").split("|")[1].strip()
        self.assertRegex(locations, r"^R\d+\.\d+(, R\d+\.\d+)*$",
                         "the INV-239 index row carries prose — the generated index is locations only "
                         "(INV-271): %r" % locations)
        # the authored home: the criterion the first location points at states the law in plain words
        self.assertIn("plain one-sentence description", read_flat("PRODUCT_SPEC.md"),
                      "the body criterion no longer states INV-239's plain description law")

    def test_e35_formal_index_row(self):
        spec = read("PRODUCT_SPEC.md")
        index = spec.split("## Reference", 1)[1]
        self.assertRegex(index, r"\|\s*E-35\s*\|", "the generated index carries no E-35 row")

    def test_architecture_owns_e35_under_base_rulebook(self):
        arch = read_flat("ARCHITECTURE.md")
        self.assertIn("E-35", arch, "ARCHITECTURE lost the E-35 anchor")
        # E-35 is owned by the base-rulebook node (the named-reference machinery's family home).
        self.assertRegex(arch, r"base-rulebook[^|]*E-35",
                         "E-35 is not owned under the base-rulebook node in ARCHITECTURE")


if __name__ == "__main__":
    unittest.main()
