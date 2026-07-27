"""The agent-channel deposit-time description lint (SPEC INV-239, M-422).

The named-reference pair's new reach is the agent channel: when an agent deposits a `from-<agent>`
inbox file, every internal code it references travels beside its plain one-sentence description, so
the neighbour reads a self-explaining file [E-35, INV-183]. This lint is that reach's mechanical net
— `guardrails/check-deposit-description.py`. It reads the same `from-<agent>` deposits the
earned-message gate reads [INV-189, base rule 30] and reds a referenced internal code that arrives
with no description beside it, naming the code and the file. It judges PRESENCE alone and never the
semantic match, undecidable on a translated or reformulated sentence and owned by the human net
[INV-41, INV-83].

Every case drives the real shipped script over a FIXTURE inbox, so no real deposit is needed and the
real tree (whose inbox carries no agent deposits today) stays green.
"""
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

GATE = os.path.join(ROOT, "guardrails", "check-deposit-description.py")


def run_gate(inbox_dir):
    return subprocess.run(["python3", GATE, inbox_dir], capture_output=True, text=True)


def deposit(tmp, name, text):
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


# An agent deposit whose reference stands bare — the codes are listed with no description beside them.
BARE = """\
From: track-coach (agent)
Lived: a fault I hit in your zone, evidence in hand.
Refs: INV-189, INV-190
Id: tc-1
"""

# An agent deposit carrying the pair — the code travels beside its plain description.
DESCRIBED = """\
From: track-coach (agent)
Lived: the earned-message law [INV-189], which nets an unearned deposit, blocked my message, and I
       carry the evidence.
Id: tc-2
"""


class TestDepositDescriptionGate(unittest.TestCase):

    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE), "the gate script does not ship: %s" % GATE)

    def test_gate_reds_a_deposit_referencing_a_bare_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            deposit(tmp, "2026-07-20-from-track-coach-bare.md", BARE)
            r = run_gate(tmp)
            self.assertNotEqual(r.returncode, 0,
                                "the lint passed a deposit referencing a bare code:\n%s" % r.stdout)
            self.assertIn("INV-189", r.stdout, "the red does not name the bare code")
            self.assertIn("from-track-coach", r.stdout, "the red does not name the deposit file")

    def test_gate_passes_a_deposit_carrying_the_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            deposit(tmp, "2026-07-20-from-track-coach-described.md", DESCRIBED)
            r = run_gate(tmp)
            self.assertEqual(r.returncode, 0,
                             "the lint red a deposit that carries its description:\n%s" % r.stdout)

    def test_gate_is_presence_not_a_semantic_match(self):
        # A description present but plainly wrong for the code still PASSES: presence alone, the
        # semantic read belonging to the human net [INV-41].
        mismatch = ("From: track-coach (agent)\n"
                    "Lived: the price of tea in a distant harbour has nothing to do with [INV-189].\n"
                    "Id: tc-3\n")
        with tempfile.TemporaryDirectory() as tmp:
            deposit(tmp, "2026-07-20-from-track-coach-mismatch.md", mismatch)
            r = run_gate(tmp)
            self.assertEqual(r.returncode, 0,
                             "the lint reached past presence into a semantic match:\n%s" % r.stdout)

    def test_gate_reads_only_from_agent_inbox_files(self):
        # A bare code in a NON-agent deposit is not the lint's business: the owner's own wish and a
        # bridged stranger Issue owe nothing here, and a plain file declaring no agent source is not
        # read at all (the same door discipline the earned-message gate keeps).
        with tempfile.TemporaryDirectory() as tmp:
            deposit(tmp, "2026-07-20-from-owner-wish.md", "Refs: INV-189, INV-190\n")
            deposit(tmp, "2026-07-20-stranger-bug-1-report.md", "Refs: INV-189, INV-190\n")
            deposit(tmp, "2026-07-20-plain-note.md", "Refs: INV-189, INV-190\n")
            r = run_gate(tmp)
            self.assertEqual(r.returncode, 0,
                             "the lint read a bare code in a non-agent deposit:\n%s" % r.stdout)

    def test_passes_on_the_real_inbox(self):
        # The gate's ENFORCEMENT ride: the suite runs it against the REAL inbox, which carries no agent
        # deposits today, so it exits 0 now — and a real bare-code deposit would red the suite (gate b)
        # and block the push. The lint takes no push-gate letter.
        r = run_gate(os.path.join(ROOT, "inbox"))
        self.assertEqual(r.returncode, 0,
                         "the lint does not pass on the real inbox:\n%s\n%s" % (r.stdout, r.stderr))

    def test_gate_not_wired_into_pre_push(self):
        from conftest import read
        self.assertNotIn("check-deposit-description", read("guardrails/pre-push"),
                         "the lint is invoked in pre-push — it must ride the suite, not take a letter")
        self.assertNotIn("check-deposit-description", read(".github/workflows/gates.yml"),
                         "the lint has its own CI step — it must ride the suite pytest step")

    def test_spec_states_the_law(self):
        from conftest import criterion_with_bullets, read
        # R191.8: the literal script path "guardrails/check-earned-message.py" is gone from the
        # compact rewrite; the same "homed beside the earned-message gate" relationship is now
        # carried by the shared [INV-189] citation on the criterion that states the lint. The
        # mechanism itself moved into a bullet under that criterion, so the criterion is read
        # with its bullets and both halves are asserted against the one home.
        clause = criterion_with_bullets(
            read("PRODUCT_SPEC.md"), "the reviewer's review *shall* stand as the net")
        self.assertIsNotNone(clause, "SPEC lost the reviewer-is-the-net criterion (R191.8)")
        self.assertIn(
            "the law declares the mechanism as the deposit-time lint over each "
            "`from-<agent>` inbox file",
            clause,
            "SPEC lost the deposit-time lint as the mechanism the law declares",
        )
        self.assertIn(
            "[INV-239, INV-189, INV-150]",
            clause,
            "SPEC lost the homed-beside-the-earned-message-gate anchor (INV-189 co-citation)",
        )

    def test_formal_index_row(self):
        from conftest import read
        # the old "## Formal index" section is gone; the generated code-to-location table now
        # lives under "## Reference" at the very end (SPEC INV-271).
        index = read("PRODUCT_SPEC.md").split("## Reference", 1)[1]
        self.assertRegex(index, r"\|\s*INV-239\s*\|", "the Reference table carries no INV-239 row")

    def test_architecture_owns_the_invariant(self):
        from conftest import read_flat
        arch = read_flat("ARCHITECTURE.md")
        self.assertIn("check-deposit-description.py", arch,
                      "ARCHITECTURE does not own the deposit-description lint")

    def test_matrix_row_covers_the_law(self):
        from conftest import read
        matrix = read("TEST_MATRIX.md")
        self.assertRegex(matrix, r"\|\s*M-422\s*\|", "TEST_MATRIX lost the M-422 row")
        self.assertIn("check-deposit-description.py", matrix, "M-422 row does not name the lint script")


if __name__ == "__main__":
    unittest.main()
