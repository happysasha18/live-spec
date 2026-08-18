"""INV-219 (M-400, ROADMAP 387) — the card's gate and adoption's line.

INV-184 declared that a host tree carrying no `.live-spec/agent.md` card is flagged where its
siblings are flagged (beside the project kind [INV-36] and the declared layers [INV-135]), and
that the mechanical gate reading a tree for its card rode ROADMAP row 387 [target] — the law's
net until then being the prover's station. A declared law with no net ranks as a broken
invariant [INV-101], so the [target] stood.

This movement builds that gate — `guardrails/check-agent-card.py`, the sibling of the
kind-with-no-layers flag [A-10] — and names the card in adoption's own document `adopt/ADOPT.md`
so a pre-law tree writes its card at its catch-up [A-11], the duty binding forward [INV-159].
The pack itself is a host [INV-97], and carries its own card at `.live-spec/agent.md`, so the
gate reads this tree and passes. With the gate live, INV-184's [target] comes off.

Every check here asserts the SHIPPED files on disk.
"""
import os
import subprocess
import sys
import tempfile
import unittest

# The suite's one reading node: for the spec it returns the core and every part the map
# names, and for any other file the file itself. A local reader would have shadowed it.
from conftest import read

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARDRAILS = os.path.join(REPO, "guardrails")
CHECK = os.path.join(GUARDRAILS, "check-agent-card.py")


def run_check(tree=None):
    env = dict(os.environ)
    if tree is not None:
        env["AGENT_CARD_TREE"] = tree
    return subprocess.run([sys.executable, CHECK], cwd=REPO, capture_output=True, text=True, env=env)


class TestAgentCardGate(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(CHECK), "the gate is absent: guardrails/check-agent-card.py")

    def test_gate_reds_a_cardless_tree(self):
        # A host tree carrying no `.live-spec/agent.md` reds BY NAME (the red proof of gate y).
        with tempfile.TemporaryDirectory() as tmp:
            r = run_check(tree=tmp)
            self.assertNotEqual(r.returncode, 0,
                                "a card-less host tree must RED:\n%s\n%s" % (r.stdout, r.stderr))
            self.assertIn(".live-spec/agent.md", r.stdout + r.stderr,
                          "the red must NAME the missing card")

    def test_gate_passes_a_tree_with_a_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, ".live-spec"))
            with open(os.path.join(tmp, ".live-spec", "agent.md"), "w", encoding="utf-8") as f:
                f.write("# a host card\n\n## Name\n\nfixture-host\n")
            r = run_check(tree=tmp)
            self.assertEqual(r.returncode, 0,
                             "a tree carrying a card must pass:\n%s\n%s" % (r.stdout, r.stderr))

    def test_gate_passes_the_pack_own_tree(self):
        # The pack is a host [INV-97] and carries its own card, so the default read passes — the
        # honest self-application that keeps the gate from reddening this very push.
        r = run_check()
        self.assertEqual(r.returncode, 0,
                         "the pack's own tree must pass (its card is present):\n%s\n%s" % (r.stdout, r.stderr))

    def test_pack_carries_its_own_card(self):
        self.assertTrue(os.path.isfile(os.path.join(REPO, ".live-spec", "agent.md")),
                        "the pack, as its own first host, must carry .live-spec/agent.md or the gate reds this push")

    def test_gate_wired_into_pre_push(self):
        self.assertIn("check-agent-card.py", read("guardrails/pre-push"))

    def test_gate_mirrored_in_ci(self):
        self.assertIn("check-agent-card.py", read(".github/workflows/gates.yml"))


class TestAdoptionNamesTheCard(unittest.TestCase):
    def test_adoption_names_the_card(self):
        adopt = read("adopt/ADOPT.md")
        self.assertIn("agent.md", adopt,
                      "adoption's own document must name the card so a pre-law tree writes it at catch-up [A-11]")


class TestInv184TargetComesOff(unittest.TestCase):
    def test_inv184_index_row_carries_no_target(self):
        spec = read("PRODUCT_SPEC.md")
        for line in spec.splitlines():
            if line.startswith("| INV-184 |"):
                self.assertNotIn("[target]", line,
                                 "INV-184's Formal-index row still carries [target] though its gate now ships")
                return
        self.fail("INV-184 row not found in the Formal index")

    def test_inv184_prose_no_longer_rides_row_387_as_target(self):
        spec = read("PRODUCT_SPEC.md")
        self.assertNotIn("ride ROADMAP row 387 [target]", spec,
                         "INV-184's prose still defers its gate to row 387 [target] though the gate now ships")


class TestTraceability(unittest.TestCase):
    def test_spec_states_the_law(self):
        spec = " ".join(read("PRODUCT_SPEC.md").split())
        self.assertIn("[INV-219, INV-97]", spec)
        self.assertIn("check-agent-card.py", spec)

    def test_formal_index_row(self):
        self.assertIn("| INV-219 |", read("PRODUCT_SPEC.md"))

    def test_architecture_owns_the_invariant(self):
        arch = read("ARCHITECTURE.md")
        self.assertIn("INV-219", arch)
        self.assertIn("check-agent-card.py", arch)

    def test_matrix_row_covers_the_law(self):
        self.assertIn("INV-219", read("TEST_MATRIX.md"))


if __name__ == "__main__":
    unittest.main()
