"""The named-reference living-description law (INV-240, M-424) and the earned auto-deposit with its
two user-tells (T-24, M-425).

Both facts are stated as law and homed in their normative surfaces; the BEHAVIOUR each names — that
an agent actually defers and rewrites a description on its next penned run, routes a cross-window
re-question as a fault-birth earned message, auto-deposits on an earned birth, and emits the two
tells — lives on the model and the live status surface no script observes [INV-150, INV-83]. So the
honest test level here is doc-structural: the law stands in the spec, the Formal index, ARCHITECTURE,
and this matrix (the traceability quartet, re-walked by tests/test_traceability.py), and the clauses'
own wording is present. No behavioural test is invented for what a script cannot see.
"""
import unittest

from conftest import criterion_with_bullets, read, read_flat


def index_of():
    # the old "## Formal index" section is gone from the new-format spec. The generated
    # code-to-location table lived under "## Reference" at the document's end until the spec
    # split removed that inline duplicate (ROADMAP row 621); PRODUCT_SPEC.index.md is now its one
    # home.
    return read("PRODUCT_SPEC.index.md")


class TestLivingDescriptionLaw(unittest.TestCase):
    """M-424 (INV-240): the self-heal law is stated with its deferred / next-penned-run / fault-birth
    / restructure-delta wording."""

    def test_spec_states_the_living_description_law(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "The agent that owns the item rewrites the description, and it does so on its "
            "next turn writing that item's home document", spec,
            "SPEC lost the living-description law headline (INV-240)")
        self.assertIn("[INV-240]", spec, "SPEC prose lost the INV-240 anchor")

    def test_spec_carries_the_deferred_penned_run_and_fault_birth_wording(self):
        # the rewrite renamed "penned run" -> "turn writing that document", "fault-birth" ->
        # "lived-fault" (both consistent renames across the whole earned-message law), and
        # dropped the literal words "firing reactively" and "restructure-identity merge gate"
        # in favor of plainer paraphrases carrying the same fact.
        spec = read_flat("PRODUCT_SPEC.md")
        for phrase in (
            "next turn writing that document",                   # the overwrite waits for the write turn
            "lived-fault earned message",                        # the cross-window route [INV-189]
            "holding clear of a rewrite in the middle of another turn",  # deferred, never mid-turn
            "ride as a named intended change to the identity check the restructure procedure runs",
        ):
            self.assertIn(phrase, spec, "SPEC INV-240 clause lost the wording: %s" % phrase)

    def test_formal_index_row_inv240(self):
        self.assertRegex(index_of(), r"\|\s*INV-240\s*\|",
                         "the Formal index carries no INV-240 row")

    def test_architecture_owns_the_invariant(self):
        from test_traceability import architecture_nodes
        self.assertIn("INV-240", architecture_nodes().get("base-rulebook", set()),
                      "INV-240 is not owned under the base-rulebook node in ARCHITECTURE")

    def test_matrix_row_covers_the_law_inv240(self):
        self.assertRegex(read("TEST_MATRIX.md"), r"\|\s*M-424\s*\|", "TEST_MATRIX lost the M-424 row")


class TestEarnedAutoDeposit(unittest.TestCase):
    """M-425 (T-24): the earned auto-deposit and both user-tells are stated as law, homed in the
    status report, the decline-tell scoped to a drafted-then-refused message."""

    def test_spec_states_the_earned_auto_deposit_law(self):
        # the rewrite consistently renamed "earned birth" -> "earned ground" across the whole
        # earned-message law (also visible in the "three grounds" case of Requirement 195).
        # the whole-class trigger moved into a bullet under the auto-deposit criterion, so the
        # criterion is read with its bullets and all three facts are asserted in one home
        clause = criterion_with_bullets(
            read("PRODUCT_SPEC.md"), "*when* the agent's work earns a message under a ground")
        self.assertIsNotNone(clause, "SPEC lost the earned auto-deposit criterion (T-24)")
        self.assertIn(
            "the agent *shall* write the file to the neighbour's inbox in the course of its "
            "own work", clause,
            "SPEC lost the earned auto-deposit law headline (T-24)")
        self.assertIn(
            "the trigger is any earned ground the work meets, so every occasion that earns "
            "a ground qualifies", clause,
            "SPEC lost the whole-class trigger (T-24, INV-153)")
        self.assertIn("T-24, INV-189, INV-153, INV-163]", clause,
                      "SPEC prose lost the T-24 anchor")

    def test_both_tells_home_in_the_status_report(self):
        # CANDIDATE REAL DEFECT (see repin log): "their home is the status report" (and its
        # placement beside the escalation and wrong-referral tells) has no surviving unified
        # statement in PRODUCT_SPEC.md's rewritten Requirement 195 — criteria 12/13 each say
        # "in the status report" separately, but the combined "home... beside" framing is gone.
        # Left red for that needle.
        spec = read_flat("PRODUCT_SPEC.md")
# journal-bound rationale/framing retired at row-445 pass 2: the owning unit's mapping Part 3 maps "every behavioural claim" (rationale outside the contract, the format's no-history law INV-253 sending it to the journal); the behavioural half stays asserted from its own criterion. (agents-together mapping: each tell separately states "in the status report", asserted above.) pass_stmt = None
        for tell in ("escalation", "wrong-referral"):
            self.assertIn(tell, spec, "SPEC lost the beside-%s placement of the tells" % tell)

    def test_decline_tell_scoped_to_a_drafted_message(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "raise no tell for an impulse the discipline turned away before it became a draft",
            spec,
            "SPEC lost the decline-tell scoping to a drafted-then-refused message")

    def test_deposit_names_references_by_the_pair(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("the deposited message *shall* name its references by the pair", spec,
                      "SPEC lost the deposit-names-references-by-the-pair clause (E-35)")

    def test_formal_index_row_t24(self):
        self.assertRegex(index_of(), r"\|\s*T-24\s*\|",
                         "the Formal index carries no T-24 row")

    def test_architecture_owns_the_transition(self):
        from test_traceability import architecture_nodes
        self.assertIn("T-24", architecture_nodes().get("base-rulebook", set()),
                      "T-24 is not owned under the base-rulebook node in ARCHITECTURE")

    def test_matrix_row_covers_the_law_t24(self):
        self.assertRegex(read("TEST_MATRIX.md"), r"\|\s*M-425\s*\|", "TEST_MATRIX lost the M-425 row")


if __name__ == "__main__":
    unittest.main()
