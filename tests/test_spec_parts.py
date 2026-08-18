"""One spec, written across a core and its parts (the parts map, SPEC INV-250, INV-258, INV-259).

The spec is ONE document. It may be STORED as a core file plus part files: the core carries the
preamble, the glossary and a `## Parts map` table naming its parts in concatenation order, and each
part carries requirements only. `guardrails/specformat.py` is the single reader of that map — every
gate, the index builder and the suite's own `conftest.read()` go through it — so a consumer never
learns whether the spec is one file or thirty.

The map is EMPTY today: the core is the whole spec, and these proofs hold the identity that makes the
move safe — an empty map reads back the file's own bytes, and every consumer behaves as before. The
fixtures below carry a populated map, so the aggregating behaviour is proven now rather than at the
move: a core plus two parts parses, indexes and reads as the one-file document it was cut from, and a
part left out of the map is caught rather than silently dropped (INV-259).
"""
import os
import subprocess
import unittest

from conftest import ROOT, SPEC, read, spec_paths

import specformat as sf

FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
MINI = os.path.join(FX, "mini_good.md")
INDEX = os.path.join(FX, "mini_index_good.md")
CORE = os.path.join(FX, "mini_core.md")
PART_A = os.path.join(FX, "mini_part_a.md")
PART_B = os.path.join(FX, "mini_part_b.md")
CORE_DROPPED = os.path.join(FX, "mini_core_part_dropped.md")
CORE_ABSENT = os.path.join(FX, "mini_core_part_absent.md")

BUILDER = os.path.join(ROOT, "scripts", "build-index.py")
INDEX_GATE = os.path.join(ROOT, "guardrails", "check-index-generated.py")


def run(script, *args):
    return subprocess.run(["python3", script, *args], capture_output=True, text=True)


def codes_and_places(text):
    """Every code the body carries, with the R-and-criterion place it sits at — the document's
    identity as far as the index is concerned, independent of which file the bytes came from."""
    return sorted((c.req_num, c.number, tuple(c.codes)) for c in sf.parse(text).criteria)


class TestTheLiveSpecReadsAsOneDocument(unittest.TestCase):
    def test_the_core_leads_the_path_list(self):
        paths = spec_paths()
        self.assertEqual(paths[0], os.path.join(ROOT, SPEC),
                         "the core is the first file of the spec and the source of the part order")

    def test_every_part_the_map_names_is_in_what_the_suite_reads(self):
        text = read(SPEC)
        for p in spec_paths():
            with open(p, encoding="utf-8") as f:
                body = f.read().strip()
            self.assertIn(body, text,
                          "%s is named by the parts map but its bytes are missing from the text the "
                          "suite reads through conftest.read()" % os.path.basename(p))

    def test_an_empty_map_reads_back_the_core_byte_for_byte(self):
        # The identity the infrastructure commit rests on: with no parts declared, the aggregating
        # read IS the plain file read, so the ~140 tests reading the spec see exactly what they saw.
        if len(spec_paths()) > 1:
            self.skipTest("the parts map now names parts — the byte identity below is the "
                          "before-the-move state and no longer applies")
        with open(os.path.join(ROOT, SPEC), encoding="utf-8") as f:
            self.assertEqual(read(SPEC), f.read())


class TestTheMap(unittest.TestCase):
    def test_the_map_names_its_parts_in_order(self):
        with open(CORE, encoding="utf-8") as f:
            self.assertEqual(sf.parts_map(f.read()), ["mini_part_a.md", "mini_part_b.md"])

    def test_a_core_with_no_map_is_the_whole_document(self):
        with open(MINI, encoding="utf-8") as f:
            self.assertEqual(sf.parts_map(f.read()), [])
        self.assertEqual(sf.spec_paths([MINI]), [MINI])

    def test_a_core_expands_to_itself_and_its_parts(self):
        self.assertEqual(sf.spec_paths([CORE]), [CORE, PART_A, PART_B])

    def test_naming_core_and_parts_is_the_same_list(self):
        # A caller may pass the whole list (the gates' command lines do); expansion does not
        # duplicate a part that is already named, so the document is never read twice.
        self.assertEqual(sf.spec_paths([CORE, PART_A, PART_B]), sf.spec_paths([CORE]))

    def test_a_part_named_in_another_spelling_is_still_one_file(self):
        # A person types relative paths at a shell prompt while the map expands to absolute ones.
        # Sameness is the FILE, not the string: were it the string, the parts below would be read
        # twice and every count built over the document — index rows, criteria, bytes — would double.
        rel = [os.path.relpath(p, ROOT) for p in (CORE, PART_A, PART_B)]
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            self.assertEqual(len(sf.spec_paths(rel)), 3)
            self.assertEqual(len(sf.spec_paths([rel[0], PART_A, rel[2]])), 3)
            _paths, joined = sf.read_document(rel)
            self.assertEqual(joined.count("## Requirement 2:"), 1,
                             "a part named in two spellings was read twice")
        finally:
            os.chdir(cwd)


class TestConcatenation(unittest.TestCase):
    def test_a_core_and_its_parts_are_the_one_file_document(self):
        _paths, joined = sf.read_document([CORE])
        with open(MINI, encoding="utf-8") as f:
            one_file = f.read()
        self.assertEqual(codes_and_places(joined), codes_and_places(one_file))
        self.assertEqual([r.number for r in sf.parse(joined).requirements],
                         [r.number for r in sf.parse(one_file).requirements])
        self.assertEqual(sf.parse(joined).glossary_terms, sf.parse(one_file).glossary_terms)

    def test_one_path_and_no_parts_is_the_file_itself(self):
        _paths, text = sf.read_document([MINI])
        with open(MINI, encoding="utf-8") as f:
            self.assertEqual(text, f.read())

    def test_the_join_never_fuses_two_lines(self):
        # mini_part_a.md deliberately ends WITHOUT a trailing newline — a file a person can write
        # and an editor can save. Without the join's own newline its last criterion and the next
        # part's heading would land on one physical line, and both would stop parsing.
        with open(PART_A, encoding="utf-8") as f:
            self.assertFalse(f.read().endswith("\n"),
                             "the fixture that arms this proof gained a trailing newline; the join's "
                             "newline branch is unexercised again")
        _paths, joined = sf.read_document([CORE])
        self.assertIn("[INV-2]\n## Requirement 2:", joined)
        self.assertNotIn("[INV-2]## Requirement", joined)
        self.assertEqual([r.number for r in sf.parse(joined).requirements], [1, 2])


class TestTheBuilderOverParts(unittest.TestCase):
    def test_the_table_over_a_core_equals_the_one_file_table(self):
        r = run(BUILDER, CORE)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(INDEX, encoding="utf-8") as f:
            self.assertEqual(r.stdout, f.read())
        self.assertEqual(r.stdout, run(BUILDER, MINI).stdout)

    def test_naming_the_parts_explicitly_builds_the_same_table(self):
        self.assertEqual(run(BUILDER, CORE, PART_A, PART_B).stdout, run(BUILDER, CORE).stdout)


class TestAPartLeftOutIsCaught(unittest.TestCase):
    def test_the_whole_document_passes_the_index_gate(self):
        r = run(INDEX_GATE, CORE, INDEX)
        self.assertEqual(r.returncode, 0, "the gate red a core whose parts carry the whole "
                                          "committed table:\n%s" % r.stdout)

    def test_a_part_dropped_from_the_map_reds(self):
        # Risk 1 of the split: a part falls out of the map and is silently not indexed. The codes
        # its criteria carry then have no body home, and the committed table over-carries them —
        # the gate reds naming them (INV-259) instead of passing over a document with a hole in it.
        r = run(INDEX_GATE, CORE_DROPPED, INDEX)
        self.assertNotEqual(r.returncode, 0,
                            "a part missing from the map passed unnoticed:\n%s" % r.stdout)
        self.assertIn("INV-259", r.stdout)
        self.assertIn("INV-3", r.stdout, "the gate does not name the code the dropped part carried")

    def test_a_part_the_map_names_and_the_tree_lacks_reds(self):
        r = run(INDEX_GATE, CORE_ABSENT, INDEX)
        self.assertNotEqual(r.returncode, 0,
                            "a map naming a part that is not there passed:\n%s" % r.stdout)
        self.assertIn("cannot read", r.stdout)
        self.assertIn("mini_part_gone.md", r.stdout)

    def test_the_builder_reds_on_a_part_the_map_names_and_the_tree_lacks(self):
        r = run(BUILDER, CORE_ABSENT)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("cannot read", r.stdout)


class TestFreshnessSeesTheParts(unittest.TestCase):
    def test_the_freshness_check_reads_the_parts_directory(self):
        # gate a's freshness rule compares the newest prover record against the newest spec commit.
        # Reading PRODUCT_SPEC.md alone would go blind to a change that lands in a part.
        with open(os.path.join(ROOT, "guardrails", "check-prover-record.sh"), encoding="utf-8") as f:
            self.assertIn("-- PRODUCT_SPEC.md spec/", f.read())


if __name__ == "__main__":
    unittest.main()
