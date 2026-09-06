"""When agents work together — the agent/skill boundary, the two channels, the card and the
scan, the published contract, the earned message, and the birth walk.

Matrix rows M-352..M-368, derived from the spec's `## When agents work together` section through
ARCHITECTURE.md's node table: base-rulebook (E-31, INV-182, INV-183, INV-188, INV-189, INV-190,
INV-191, INV-193, INV-194), spec-author (E-33, INV-185, INV-186, INV-187), host-contract (E-32,
INV-184), inbox (INV-192), build-pipeline (T-22).

Levels, in this repo's declared four-rung vocabulary (the matrix header's recorded interpretation;
the closed set is enforced at tests/test_traceability.py): the pack ships documents, so a law's
rendered level is a `string` assertion against the SHIPPED file on disk. Two rows here go past a
document read and exercise a real artifact, the way the guardrail rows M-229..M-231 already do —
`test_gate_passes_a_message_naming_its_blocked_work` / `test_gate_reds_a_message_naming_no_blocked_work`
run `guardrails/check-earned-message.py` against a real fixture deposit and read its exit code both
ways, and `test_pack_card_exists_and_names_its_five_fields` reads this pack's own real card from disk.

The contract's mechanical arms (a producer's permission gate, a consumer's freshness check, a
compatibility test) are NOT asserted here: this pack contains no data producer, so there is nothing
to exercise. Nobody promises them either — the criterion and the `[target]` marker that did retired
on 2026-09-06 with the row that held them (q-385), because every adopted project's card still reads
"None today" and the trigger it waited on never fired. The rows for E-33, INV-185, INV-186 and
INV-187 assert that those laws stand in the documents today.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from conftest import ROOT, criteria_citing, read, read_flat

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


SPEC = "PRODUCT_SPEC.md"
BASE = "skills/live-spec-base/SKILL.md"


def _index_row(anchor):
    """True when the spec's Formal index carries a row for this anchor."""
    return any(l.startswith("| %s |" % anchor) for l in read(SPEC).splitlines())


def _declaration(anchor):
    """The prose paragraph(s) in the spec that DECLARE this anchor.

    The home is every criterion whose trailing code bracket names the anchor; an index row is a
    lookup into that home, so table lines are passed over. In the requirements format a
    criterion's trailing bracket commonly co-cites several codes together, so membership in that
    bracket — not sole occupancy of it — is what makes a line the anchor's declaration. Scoping a
    needle to the declaration keeps a check from passing off the index row or a neighbouring
    clause that merely cites the code (ROADMAP row 384, the vacuous-pass class).

    A criterion is read together with the indented bullets under it: the format carries an
    in-place definition in those bullets, so half a criterion's content sits there while the
    code bracket stays on the criterion line. Reading the two apart would leave a declared fact
    invisible to its own anchor's check.
    """
    return criteria_citing(read(SPEC), anchor)


def _architecture_owners(anchor):
    """Every node whose `owns` field (guardrails/archformat.py) lists this anchor.

    Anchors are read from the owns field only, ranges expanded to their members, so a range like
    INV-250..INV-265 owns each of its member codes. An anchor sitting only in loose prose is
    owned by nobody and reads as zero owners here — the reading a whole-file search cannot make.
    """
    owners = []
    for node in archformat.parse_nodes(read("ARCHITECTURE.md")):
        if anchor in node.anchors_expanded:
            owners.append(node.name)
    return owners


class _AnchorHomeMixin:
    def assert_index_and_ownership(self, anchor):
        self.assertTrue(_index_row(anchor), "%s index row missing" % anchor)
        owners = _architecture_owners(anchor)
        self.assertEqual(len(owners), 1,
                         "%s is owned by %d architecture nodes %s; every spec fact is owned by "
                         "exactly one node" % (anchor, len(owners), owners))

    def assert_declared(self, anchor):
        """The anchor's own declaration paragraph, asserted present before it is read."""
        clause = _declaration(anchor)
        self.assertTrue(clause, "%s has no declaring paragraph in %s; the home is absent"
                                % (anchor, SPEC))
        return clause


# --------------------------------------------------------------------------- #
# [node: base-rulebook]
# --------------------------------------------------------------------------- #

class TestAgentSkillBoundary(unittest.TestCase, _AnchorHomeMixin):
    """E-31 / INV-182 (M-352, M-353) — an agent is a project window whose things outlive any one
    conversation; a skill loads into a window and dies with the session."""

    def test_agent_is_a_project_window(self):
        spec = read_flat(SPEC)
        self.assertIn("An agent is a project window with a tree, a queue, gates, contracts, "
                      "a standing mission, and a card", spec)
        self.assertIn("a tree, a queue, gates, contracts, a standing mission, and a card", spec)
        self.assertIn("each of those outliving any one conversation", spec)
        self.assertIn("[E-31]", spec)

    def test_skill_dies_with_the_session(self):
        spec = read_flat(SPEC)
        self.assertIn("a skill is a capability a window loads for one conversation", spec)
        self.assertIn("holds no tree, no standing mission, and no queue", spec)
        self.assertIn("leaves nothing standing once the conversation closes", spec)

    def test_e31_index_and_ownership(self):
        self.assert_index_and_ownership("E-31")

    def test_grain_boundary_names_its_three_marks(self):
        """The grain test is durable state + a standing mission + a zone of its own — never size."""
        spec = read_flat(SPEC)
        self.assertIn(
            "count a capability as an agent *when* it holds durable state, a standing mission, "
            "and a zone of its own, and *shall* count a capability that lives wholly inside one "
            "session as a skill", spec)
        self.assertIn("[INV-182]", spec)

    def test_grain_on_the_line_is_the_owners_word(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "a real capability sits on the line between the two, the owner's word *shall* "
            "place it", spec)

    def test_inv182_index_and_ownership(self):
        self.assert_index_and_ownership("INV-182")


class TestTwoChannels(unittest.TestCase, _AnchorHomeMixin):
    """INV-183 (M-354) — exactly two channels, and the reply rides one of them backwards so the
    count of two holds."""

    def test_exactly_two_channels_in_the_spec(self):
        spec = read_flat(SPEC)
        self.assertIn("exactly two channels to carry everything between two agents", spec)
        self.assertIn("INV-183, E-11]", spec)  # code always co-brackets in the new format

    def test_no_third_channel_exists(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "no third improvised road grows to carry the traffic the two were meant to hold",
            spec)
        self.assertIn(
            "a reply *shall* ride the inbox in the other direction, so the count of channels "
            "between two agents stays at two", spec)
        # INV-183's transport sentence was corrected (the owner refused the git-universal premise,
        # 2026-07-17): which transport carries a message is now decided by the traffic's kind, the
        # detail owned by INV-236. The contract — who talks and when — stays untouched.
        self.assertIn("the traffic's kind picks the transport", spec)
        self.assertIn("[INV-236]", spec)

    def test_base_rulebook_carries_the_two_channel_law(self):
        self.assertIn("exactly two channels", read_flat(BASE),
                      "the base rulebook does not carry the two-channel law")

    def test_inv183_index_and_ownership(self):
        self.assert_index_and_ownership("INV-183")


class TestDataNeverTravelsAsAMessage(unittest.TestCase, _AnchorHomeMixin):
    """INV-188 (M-355) — a consumer wanting data reads the contract; a consumer wanting a field
    the contract lacks holds a request about the contract's shape."""

    def test_data_never_travels_as_a_message(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "a consumer wanting a producer's data *shall* read the contract rather than send "
            "a message asking for it", spec)
        self.assertIn("[INV-188]", spec)

    def test_missing_field_routes_to_the_earned_message(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "a consumer wants a field the contract lacks, the system *shall* treat it as a "
            "request about the contract's shape", spec)

    def test_inv188_index_and_ownership(self):
        self.assert_index_and_ownership("INV-188")


class TestEarnedMessage(unittest.TestCase, _AnchorHomeMixin):
    """INV-189 (M-356) — a message names the sender's OWN blocked work, in the message; the births
    are a closed set of two; the zone's owner is presumed competent and informed."""

    def test_earned_message_names_its_block(self):
        """F-agent-ask's named test (ARCHITECTURE.md feature coverage)."""
        spec = read_flat(SPEC)
        self.assertIn("a message *shall* name the sender's own work that earned it", spec)
        self.assertIn("name the blocked work", spec)
        self.assertIn("name the fault and the evidence the sender lived", spec)
        self.assertIn("a message that can name no such work *shall* stay unsent", spec)
        self.assertIn("[INV-189]", spec)

    def test_two_births_are_a_closed_set(self):
        # the rewrite consistently renamed "birth" -> "ground" across the whole earned-message
        # law, and the set is (and was, in the old spec too) three, not two: blocked work, a
        # lived fault, or an unowned concern.
        spec = read_flat(SPEC)
        self.assertIn("recognize exactly three grounds for a message", spec)
        self.assertIn("three grounds, and the set is closed", spec)
        self.assertIn("a candidate message matching no ground *shall* stay unsent", spec)

    def test_owner_presumed_competent_and_informed(self):
        # mapping.md Part 4 (F-agent-ask table) maps the source claim "The owner's zone is
        # presumed informed; a fault its instruments cannot see, carried with evidence, earns
        # the file." to R7.8, whose surviving text is the Case heading below plus the criterion
        # itself — the word "competent" is not part of the mapped claim (mapping already states
        # the claim as "presumed informed" alone), so it re-pins.
        spec = read_flat(SPEC)
        self.assertIn("Case: the owner's zone is presumed informed", spec)
        # CANDIDATE REAL DEFECT (see repin log): "That presumption is what keeps the second
        # birth narrow" has no mapping row in mapping.md Part 4 — it is rationale explaining WHY
        # only two exceptions to the report-nothing-the-owner-already-sees rule exist, and
        # mapping.md's own stated scope (line 119) excludes rationale from what it carries
        # forward. Confirmed absent from PRODUCT_SPEC.md and from the prototype draft
        # section.md alike.
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.

    def test_base_rulebook_carries_the_earned_message_law(self):
        # The law is that a message names the ground that earned it, or is not sent. It has more
        # than one ground: spec/agent-request.md:25 recognises three, and
        # guardrails/check-earned-message.py records the July 2026 incident where a gate demanding
        # blocked work of everything refused the first real deposit — a fault message from a
        # neighbouring project. So this asserts the law and the ground, and leaves the sentence
        # free to name the other grounds; pinning the old exclusive wording would have held the
        # rulebook at the shape that caused that refusal.
        body = read_flat(BASE)
        self.assertIn("the sender's own blocked work", body,
                      "the base rulebook does not carry the earned-message law's first ground")
        self.assertIn("or is never sent", body,
                      "the base rulebook states the ground without the law it serves")

    def test_inv189_index_and_ownership(self):
        self.assert_index_and_ownership("INV-189")


class TestEarnedMessageGate(unittest.TestCase):
    """INV-189's mechanical arm (M-356), exercised: `guardrails/check-earned-message.py` runs
    against a real fixture inbox deposit and its exit code is read both ways. The gate's own
    contract: exit 0 when every agent message names its blocked work, exit 1 when one does not.

    The deposit's source has one home, the filename (`inbox/README.md`): an agent's deposit is
    `YYYY-MM-DD-from-<agent>-<slug>.md`, which is the form the folder's real corpus has carried
    since 2026-07-10. `from-owner` and the monitor's `stranger-*` are the reserved non-agent
    doors, and they owe nothing (INV-193, INV-146). The fixtures below take that real form, so
    the suite exercises the format the pack ships. The 2026-07-17 audit found the gate inert on
    it — every hostile fixture the audit proved passing owns a test here.
    """

    SCRIPT = os.path.join(ROOT, "guardrails", "check-earned-message.py")

    # The real deposit that proved the gate inert (the audit's live evidence). Frozen here in
    # the shape it landed in, so this regression outlives the sweep that removes the file.
    REAL_DEPOSIT = "2026-07-17-from-track-coach-worker-completion-orphans-runaway-child.md"
    REAL_DEPOSIT_FROZEN = (
        "# feedback: a worker's completion should also reap its spawned OS subprocesses\n\n"
        "**The item (a worker-hygiene rule for the pack's orchestration).** When a subagent\n"
        "finishes, that signals the AGENT is done; the OS processes it spawned can still be alive.\n\n"
        "**Why (what happened, 2026-07-17, track-coach s77).** A background worker's orphaned child\n"
        "burned a full CPU core at 100% for 46 minutes doing work nobody would read.\n\n"
        "**Who threw it.** track-coach window (this Mac), session s77, 2026-07-17.\n"
    )

    def setUp(self):
        # The suite's own prefix, so conftest's session-scoped leak diff can see a leak (INV-100).
        self.tmp = tempfile.mkdtemp(prefix="livespec-test-agent-inbox-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _deposit(self, name, text):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def _run(self):
        return subprocess.run(["python3", self.SCRIPT, self.tmp],
                              capture_output=True, text=True)

    def _assert_gate_present(self):
        self.assertTrue(os.path.isfile(self.SCRIPT),
                        "the earned-message gate is absent: guardrails/check-earned-message.py "
                        "(SPEC INV-189)")

    # -- the corpus format, both ways ---------------------------------------- #

    def test_gate_passes_a_message_naming_its_blocked_work(self):
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-render-offset-unpinned.md",
                      "# the render offset stays unpinned\n\n"
                      "Blocked: ROADMAP row 12 cannot land while the render offset stays unpinned\n"
                      "Need-by: 2099-07-24\n"
                      "Id: track-coach-s77-a1\n\n"
                      "The body of the request.\n")
        r = self._run()
        self.assertEqual(r.returncode, 0,
                         "the gate red an earned message that names its blocked work:\n%s"
                         % (r.stdout + r.stderr))

    def test_gate_reds_a_message_naming_no_blocked_work(self):
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-thought-you-should-know.md",
                      "# a thought\n\n"
                      "Need-by: 2099-07-24\n"
                      "Id: track-coach-s77-a2\n\n"
                      "I thought you might want to know about this.\n")
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "the gate passed an agent message naming no blocked work (SPEC INV-189)")
        self.assertIn("INV-189", r.stdout + r.stderr,
                      "the gate's finding does not cite the law it enforces")

    def test_gate_reds_the_real_corpus_format_carrying_no_body_source_field(self):
        """The audit's finding 1: the source's home is the filename, and the corpus writes no
        body `From:` field at all. A gate keyed on that body field is inert on everything the
        pack actually ships."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-tlvphotos-face-reentry-state.md",
                      "# the face re-entry state\n\n"
                      "The item, in plain words, with no field naming any work of my own.\n\n"
                      "**Who threw it.** tlvphotos window, session s41.\n")
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "the gate is inert on the pack's own inbox format: a deposit whose "
                         "filename names an agent source passed while naming no blocked work "
                         "(SPEC INV-189, inbox/README.md's format)")

    def test_gate_passes_a_fault_message_naming_what_it_lived(self):
        """INV-189's second birth. A fault message owes the evidence the sender lived, and
        nothing of that sender's need stand still — a gate demanding blocked work of both
        births would refuse the fault message, which is the message a neighbour most wants."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-worker-orphans-a-child.md",
                      "# a worker's completion leaves its child alive\n\n"
                      "Lived: s77 ran a background re-render; the worker returned while its child "
                      "burned a core at 100% for 46 minutes, shown by ps against an idle output "
                      "file (2026-07-17)\n"
                      "Need-by: 2099-08-01\n"
                      "Id: track-coach-s77-a6\n")
        r = self._run()
        self.assertEqual(r.returncode, 0,
                         "the gate red a fault message that names the evidence it lived; the "
                         "fault birth owes the evidence (SPEC INV-189):\n%s"
                         % (r.stdout + r.stderr))

    def test_gate_reds_a_message_naming_neither_birth(self):
        """The births are a closed set of two, and a candidate matching neither stays unsent."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-a-thought-about-your-zone.md",
                      "# a thought\n\n"
                      "Need-by: 2099-07-24\n"
                      "Id: track-coach-s77-a7\n\n"
                      "Your dashboard already shows this, and I thought you might want to know.\n")
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "a message naming neither birth passed (SPEC INV-189)")

    def test_gate_declines_the_real_track_coach_deposit(self):
        """The audit's live proof, run as a regression, and the reason INV-189 was corrected on
        2026-07-17. The deposit is earned under the SECOND birth: track-coach lived a fault in
        the pack's zone and carries the evidence it lived (s77, an orphaned child burning a core
        for 46 minutes) — the outside view the pack's own instruments cannot take. It names no
        blocked work, correctly: nothing of track-coach's own stood still. What it carries no
        field for is the evidence, which sits in its prose under a `**Why (what happened...)**`
        heading, so the gate declines it at the door on the format alone. One `Lived:` line
        clears the red, and the sweep clears it by harvesting the file. The real bytes are read
        while the file is on disk; the frozen shape carries the regression once it is swept."""
        self._assert_gate_present()
        rel = os.path.join("inbox", self.REAL_DEPOSIT)
        on_disk = os.path.isfile(os.path.join(ROOT, rel))
        self._deposit(self.REAL_DEPOSIT, read(rel) if on_disk else self.REAL_DEPOSIT_FROZEN)
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "the gate passed the 2026-07-17 track-coach deposit, which names its "
                         "lived fault in prose and carries no field for it (SPEC INV-189)")
        self.assertIn("INV-189", r.stdout + r.stderr)

    def test_the_real_deposit_names_no_blocked_work_and_the_spec_says_so(self):
        """The deposit the spec holds up as its first real message. Nothing of track-coach's own
        stood still, so a gate demanding blocked work of it would refuse a message the law calls
        correct. This pins the fixture's shape against the law it drove."""
        rel = os.path.join("inbox", self.REAL_DEPOSIT)
        if not os.path.isfile(os.path.join(ROOT, rel)):
            return  # swept into its routed home; the frozen shape above carries the regression
        deposit = read(rel)
        self.assertNotIn("Blocked:", deposit,
                         "the deposit names blocked work, so it is no longer the fault-birth "
                         "fixture this suite reads it as (SPEC INV-189)")
        self.assertIn("s77", deposit,
                      "the deposit carries no session evidence, which is what earns a fault "
                      "message its file (SPEC INV-189)")

    # -- the doors that owe nothing ------------------------------------------ #

    def test_gate_reads_the_owners_own_deposit_as_owing_nothing(self):
        """A wish from the owner carries the owner's own authority (INV-193). The reserved word
        is the role, since a shipped file names no person (INV-120's gate)."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-owner-please-fix-the-thing.md",
                      "# please fix the thing\n\n"
                      "The thing is broken. Fix it.\n")
        r = self._run()
        self.assertEqual(r.returncode, 0,
                         "the gate asked the owner's own wish for blocked work (SPEC INV-193):\n%s"
                         % (r.stdout + r.stderr))

    def test_gate_reads_a_relayed_owner_wish_as_owing_nothing(self):
        """An agent relaying the owner's word carries the owner's authority: relaying changes a
        message's carrier and leaves its authority exactly where it started (INV-193). So the
        filename names whose the item is — `from-owner` — and the body names the window that
        threw it. The live promoter deposit of 2026-07-17 is this case, and a gate reading the
        depositing window as the source would ask the owner's own instruction for a birth."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-owner-agent-ownership-and-routing.md",
                      "# Wish: who owns a cross-cutting concern (owner's word, 2026-07-17)\n\n"
                      "The owner asks live-spec to own the meta-question.\n\n"
                      "## Who threw it\n\n"
                      "The promoter product-dev window, relaying the owner's word.\n")
        r = self._run()
        self.assertEqual(r.returncode, 0,
                         "the gate asked the owner's own relayed wish for a birth; his word "
                         "carries his own authority (SPEC INV-193):\n%s" % (r.stdout + r.stderr))

    def test_gate_leaves_a_bridged_stranger_issue_alone(self):
        """A stranger's Issue comes through the wish template and owes nothing (INV-146). The
        filename is the one the monitor writes (scripts/stranger-wish-monitor.py)."""
        self._assert_gate_present()
        self._deposit("stranger-issue-42-the-install-ratchet-appends-past-exit.md",
                      "surface-key: issue-42-gen0\n"
                      "source: GitHub Issue #42\n\n"
                      "# the install ratchet appends past exit\n\n"
                      "A stranger's report, owing no blocked work of anyone's.\n")
        r = self._run()
        self.assertEqual(r.returncode, 0,
                         "the gate asked a bridged stranger Issue for blocked work "
                         "(SPEC INV-146):\n%s" % (r.stdout + r.stderr))

    # -- the reply road (INV-192) -------------------------------------------- #

    def test_gate_passes_a_reply_naming_the_message_it_discharges(self):
        """INV-192: a reply owes no blocked work of its own, since the message it discharges
        already named the blocked work that earned the exchange; it names that message's
        identifier instead. The spec's own reply road red against the pre-fix gate."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-tlvphotos-reply-to-live-spec-s68-a41.md",
                      "From: tlvphotos (agent)\n"
                      "Re: live-spec-s68-a41\n"
                      "Terminal state: declined. The commerce policy lives in this agent's zone.\n")
        r = self._run()
        self.assertEqual(r.returncode, 0,
                         "the gate red a spec-legal reply, which owes no blocked work of its own "
                         "(SPEC INV-192):\n%s" % (r.stdout + r.stderr))

    def test_gate_reds_a_reply_naming_no_message(self):
        """The reply exemption stands on naming the message it discharges. A `Re:` line carrying
        a placeholder ties to nothing, so the deposit owes blocked work like any message."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-tlvphotos-reply-to-nothing.md",
                      "From: tlvphotos (agent)\n"
                      "Re: TBD\n"
                      "Terminal state: declined.\n")
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "a placeholder identifier bought the reply exemption (SPEC INV-192)")

    # -- the hostile fixtures the audit proved passing ----------------------- #

    def test_gate_reads_an_agent_marker_split_across_lines(self):
        """The audit's fixture: `From: live-spec` with `(agent)` on the NEXT line. The marker
        search read the captured value alone, so the deposit passed unread."""
        self._assert_gate_present()
        self._deposit("2026-07-17-a-deposit-with-a-wrapped-source-mark.md",
                      "# a request\n\n"
                      "From: live-spec\n"
                      "(agent)\n\n"
                      "No field of mine names any work.\n")
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "an agent marker wrapped onto the next line escaped the gate "
                         "(SPEC INV-189)")

    def test_gate_reads_a_deposit_that_is_not_markdown(self):
        """The audit's fixture: a `.txt` deposit. The scan globbed `*.md`, so renaming the file
        cleared the gate. Every deposit in the folder is read."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-a-plain-text-deposit.txt",
                      "# a request\n\nNo field of mine names any work.\n")
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "a deposit escaped the gate by its file extension (SPEC INV-189)")

    def test_gate_reads_the_source_marks_variants(self):
        """The audit's fixtures: a fullwidth colon, the field named `Sender`, and the marker in
        square brackets. Each read as no agent at all, so each passed unread."""
        self._assert_gate_present()
        variants = {
            "fullwidth colon": "From： live-spec (agent)\n",
            "the field named Sender": "Sender: live-spec (agent)\n",
            "the marker in square brackets": "From: live-spec [agent]\n",
        }
        for label, mark in variants.items():
            with self.subTest(variant=label):
                for f in os.listdir(self.tmp):
                    os.remove(os.path.join(self.tmp, f))
                self._deposit("2026-07-17-a-deposit-with-a-variant-mark.md",
                              "# a request\n\n" + mark + "\nNo field names any work of mine.\n")
                r = self._run()
                self.assertEqual(r.returncode, 1,
                                 "a source mark written with %s escaped the gate (SPEC INV-189)"
                                 % label)

    def test_gate_passes_over_a_field_inside_a_fenced_block(self):
        """The audit's fixture: `Blocked:` inside a fenced code block. The scan was line-based
        with no fence awareness, so quoting the template's block cleared the gate. A fenced block
        is an example, and the gate reads past it — for the source mark on the same terms, so a
        deposit quoting the card's block is not made agent traffic by the quote."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-a-fenced-field.md",
                      "# a request\n\n"
                      "Here is the shape the card prescribes:\n\n"
                      "```\n"
                      "Blocked: <the work of mine that stands until this is answered>\n"
                      "```\n\n"
                      "No field of my own names any work.\n")
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "a `Blocked:` field inside a fenced code block cleared the gate "
                         "(SPEC INV-189)")

    def test_gate_reds_a_blocked_field_that_only_points_elsewhere(self):
        """The audit's fixture: `Blocked: see above`. The field is a pointer carrying no work,
        which is the placeholder family the gate already nets (TBD, none, N/A). The match is the
        whole field, so a field that says `see above` AND names work stays legal."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-blocked-see-above.md",
                      "# a request\n\n"
                      "Blocked: see above\n"
                      "Id: track-coach-s77-a3\n")
        r = self._run()
        self.assertEqual(r.returncode, 1,
                         "a blocked-work field pointing elsewhere and naming nothing cleared the "
                         "gate (SPEC INV-189)")
        self._deposit("2026-07-17-from-track-coach-blocked-see-above.md",
                      "# a request\n\n"
                      "Blocked: see above — ROADMAP row 12 stands until this is answered\n"
                      "Id: track-coach-s77-a3\n")
        r = self._run()
        self.assertEqual(r.returncode, 0,
                         "a field naming real work red because it also pointed at the prose:\n%s"
                         % (r.stdout + r.stderr))

    # -- the fields the gate reports (INV-192) ------------------------------- #

    def test_gate_reports_a_need_by_it_can_see_without_redding(self):
        """The audit's finding 5: `Need-by:` was named in the usage and never read. It is read
        here and reported. It never reds: INV-192 gives an expired need-by one road — the
        SENDER's own status report, which the human reads — so a receiver's push is the wrong
        red for a sender's clock. An absent `Id:` reports on the same terms."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-an-expired-need-by.md",
                      "# a request\n\n"
                      "Blocked: ROADMAP row 12 cannot land while the render offset stays unpinned\n"
                      "Need-by: 2001-01-01\n"
                      "Id: track-coach-s77-a4\n")
        r = self._run()
        self.assertEqual(r.returncode, 0,
                         "an expired need-by red the receiver's gate; INV-192 sends the "
                         "escalation to the sender's own status report:\n%s"
                         % (r.stdout + r.stderr))
        self.assertIn("2001-01-01", r.stdout,
                      "the gate reads the need-by and reports nothing about it (SPEC INV-192)")
        self.assertIn("INV-192", r.stdout,
                      "the need-by report cites no law")

    def test_gate_reports_an_agent_message_that_states_no_need_by(self):
        """INV-192: every message states its need-by. The gate reports the absence and leaves the
        exit code to INV-189, the law this gate is the arm of."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-no-need-by.md",
                      "# a request\n\n"
                      "Blocked: ROADMAP row 12 cannot land while the render offset stays unpinned\n"
                      "Id: track-coach-s77-a5\n")
        r = self._run()
        self.assertEqual(r.returncode, 0)
        self.assertIn("need-by", r.stdout.lower(),
                      "a message stating no need-by drew no report (SPEC INV-192)")

    # -- the gate and the README name one format ----------------------------- #

    def test_gate_help_prescribes_the_format_the_readme_prescribes(self):
        """The audit's finding 4: the help printed a three-field template omitting `Id:`, so a
        sender following the error message wrote a message INV-192 refuses. The help names the
        filename form the README prescribes, and every field it names is one the spec requires."""
        self._assert_gate_present()
        self._deposit("2026-07-17-from-track-coach-thought-you-should-know.md",
                      "# a thought\n\nNo work of mine is named here.\n")
        r = self._run()
        self.assertEqual(r.returncode, 1)
        help_text = r.stdout
        self.assertIn("from-<agent>", help_text,
                      "the help does not name the filename form the README prescribes")
        self.assertIn("Blocked:", help_text)
        self.assertIn("Lived:", help_text,
                      "the help names one birth of the two, so a sender carrying a lived fault "
                      "reads that its message is unearned (SPEC INV-189)")
        self.assertIn("Id:", help_text,
                      "the help prescribes a message with no identifier, which INV-192 refuses")
        self.assertIn("Re:", help_text,
                      "the help does not name the reply road (SPEC INV-192)")
        self.assertNotIn("From: <name> (agent)", help_text,
                         "the help still prescribes a body source field; the source's one home "
                         "is the filename (inbox/README.md)")

    def test_readme_and_the_gate_agree_on_the_sources_one_home(self):
        """The audit's root finding: the source had two homes that disagreed, and the gate read
        the one nobody used. The README is the format's home, so it prescribes the filename form
        and names the reserved non-agent doors the gate honours."""
        readme = read_flat(os.path.join("inbox", "README.md"))
        self.assertIn("from-<agent>", readme,
                      "inbox/README.md prescribes no source form for an agent's deposit, so the "
                      "gate reads a format its own home never states (SPEC INV-189)")
        self.assertIn("from-owner", readme,
                      "inbox/README.md names no reserved door for the owner's own wish "
                      "(SPEC INV-193)")
        self.assertIn("relaying", readme.lower(),
                      "inbox/README.md does not say which name a relayed owner wish takes, and "
                      "an agent relaying his word is the live case (SPEC INV-193)")
        self.assertIn("stranger-", readme,
                      "inbox/README.md names no reserved door for a bridged Issue (SPEC INV-146)")
        self.assertIn("Re:", readme,
                      "inbox/README.md prescribes no reply form, which the gate exempts "
                      "(SPEC INV-192)")
        for birth in ("Blocked:", "Lived:"):
            self.assertIn(birth, readme,
                          "inbox/README.md prescribes no %s field, and the gate reads one; the "
                          "format's home and its gate name one format (SPEC INV-189)" % birth)
        gate = read(os.path.join("guardrails", "check-earned-message.py"))
        self.assertIn("from-", gate,
                      "the gate reads no filename source, which is the source's one home")


class TestReferralDirection(unittest.TestCase, _AnchorHomeMixin):
    """INV-190 (M-357) — a referral travels BACK to whoever asked; the zone's owner receives
    nothing from it."""

    def test_referral_travels_back_to_the_asker(self):
        # CANDIDATE REAL DEFECT (see repin log): "The direction is the whole law" has no mapping
        # row in mapping.md Part 4. The only "direction" row there (R2.3, "A reply rides the
        # inbox in the other direction; the count stays two") is a DIFFERENT source claim from
        # the shared-intro two-channels paragraph (old spec line ~1518, the general reply
        # mechanism), not from this referral-specific paragraph (old spec line 1560, under
        # INV-190) — re-checked against OLD_SPEC.md and rejected as a false match, not re-pinned
        # to it. This sentence is rationale (the referral law's whole content IS its direction,
        # nothing else needs stating) with no distinct row anywhere in mapping.md.
        spec = read_flat(SPEC)
        self.assertIn(
            "a question belongs to another agent's zone, the system *shall* refer it back to "
            "whoever asked", spec)
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.
        self.assertIn("[INV-190]", spec)

    def test_zone_owner_receives_nothing_from_a_referral(self):
        # CANDIDATE REAL DEFECT (see repin log): mapping.md Part 4's only row for this scenario
        # ("A question from another zone is referred back to whoever asked; the zone owner
        # receives nothing." -> R8.1) covers the referral direction and the owner-receives-
        # nothing rule alone (already asserted below and passing); it carries no row for either
        # "Forwarding a neighbour's question to the owner of its zone is the defect this law
        # names" (the anti-pattern spelled out) or "it carries the question to the human as its
        # own question on no occasion" (the never-relay-as-own-question safeguard). Both are
        # rationale/framing with no mapping row anywhere in Part 3 or Part 4, and neither string
        # is present in PRODUCT_SPEC.md or the prototype draft section.md.
        spec = read_flat(SPEC)
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # the safeguard's behavioural neighbours survive: the referral-direction criteria above and
        # the relay-authority criterion "relaying a message *shall* change only its carrier").
        self.assertIn("relaying a message *shall* change only its carrier", spec)

    def test_base_rulebook_carries_the_referral_direction(self):
        self.assertIn("travels back to whoever asked", read_flat(BASE),
                      "the base rulebook does not carry the referral's direction")

    def test_inv190_index_and_ownership(self):
        self.assert_index_and_ownership("INV-190")


class TestHomelessQuestionDropped(unittest.TestCase, _AnchorHomeMixin):
    """INV-191 (M-358) — a question pinning to no artifact, on which no work of the sender's
    stands, is dropped, and the holding was itself the defect."""

    def test_homeless_question_is_dropped(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "a question pins to no artifact and no work of the sender's stands on it, the "
            "system *shall* drop it, the holding of it being the finding", spec)
        self.assertIn("INV-191, INV-153]", spec)  # code always co-brackets in the new format

    def test_the_holding_is_itself_the_finding(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "a question pins to no artifact and no work of the sender's stands on it, the "
            "system *shall* drop it, the holding of it being the finding", spec)
        self.assertIn("INV-191, INV-153]", spec)

    def test_inv191_index_and_ownership(self):
        self.assert_index_and_ownership("INV-191")


class TestProposalUntilRatified(unittest.TestCase, _AnchorHomeMixin):
    """INV-193 (M-359) — an agent-initiated message stands as a proposal until the owner ratifies
    it; relaying changes only the carrier."""

    def test_agent_message_is_a_proposal_until_ratified(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "an agent-initiated message *shall* stand as a proposal in the receiver's queue "
            "until the owner ratifies it", spec)
        self.assertIn("an owner-initiated message carries the owner's authority", spec)
        self.assertIn("INV-193, INV-94]", spec)  # code always co-brackets in the new format

    def test_relaying_leaves_authority_where_it_started(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "relaying a message *shall* change only its carrier and leave its authority where "
            "it started", spec)

    def test_base_rulebook_carries_the_ratification_law(self):
        self.assertIn("stays a proposal until the owner ratifies", read_flat(BASE),
                      "the base rulebook does not carry the ratification law")

    def test_inv193_index_and_ownership(self):
        self.assert_index_and_ownership("INV-193")


class TestNonDuplication(unittest.TestCase, _AnchorHomeMixin):
    """INV-194 (M-360) — a neighbour's capability is reached through one of the two channels; a
    local copy is the violation the cards exist to prevent."""

    def test_capability_taken_through_one_of_the_two_channels(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "an agent needing a capability another agent's zone owns *shall* send a message "
            "or read a contract rather than keep a local copy of it", spec)
        self.assertIn("INV-194, INV-183]", spec)  # code always co-brackets in the new format

    def test_local_copy_is_the_violation_the_cards_prevent(self):
        # mapping.md Part 4 (F-agent-ask table) maps this whole source paragraph — "A capability
        # another zone owns is used through a channel, never copied locally." — to R7.14, whose
        # surviving text is the bare prohibition rule; that IS the "violation the cards exist to
        # prevent" restated affirmatively, so the claim re-pins to it.
        spec = read_flat(SPEC)
        self.assertIn(
            "an agent needing a capability another agent's zone owns *shall* send a message "
            "or read a contract rather than keep a local copy of it", spec)
        # CANDIDATE REAL DEFECT (see repin log): "the two owners then answer one question two
        # ways" (the drift rationale explaining WHY a local copy is the violation) has no
        # mapping row anywhere in mapping.md Part 4 — R7.14's row states only the bare rule.
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.

    def test_base_rulebook_carries_the_non_duplication_law(self):
        self.assertIn("a local copy of a neighbour's capability", read_flat(BASE),
                      "the base rulebook does not carry the non-duplication law")

    def test_inv194_index_and_ownership(self):
        self.assert_index_and_ownership("INV-194")


# --------------------------------------------------------------------------- #
# [node: spec-author]
# --------------------------------------------------------------------------- #

class TestContractIsASpecSurface(unittest.TestCase, _AnchorHomeMixin):
    """E-33 (M-361) — the contract is a spec surface in the producer's own spec, and its artifact
    carries its own version and generation stamp."""

    def test_contract_is_a_spec_surface(self):
        spec = read_flat(SPEC)
        self.assertIn("a published contract *shall* be a surface in the producer's own spec",
                      spec)
        self.assertIn("written, proven, and tested where the producer's other surfaces are", spec)
        self.assertIn("E-33, INV-73]", spec)  # code always co-brackets in the new format

    def test_artifact_carries_its_version_and_stamp(self):
        # mapping.md Part 4 (F-contract table) maps "The artifact lives at the card's path and
        # states its contract version and generation moment; a reader tells shape/age from it."
        # to R6.3, whose surviving criterion states the "reader tells shape/age from it" half
        # verbatim (minus the old spec's "no second document to consult" emphasis clause, which
        # has no separate mapping row — see below).
        spec = read_flat(SPEC)
        self.assertIn(
            "paired with a machine-readable artifact carrying its own version and generation "
            "stamp", spec)
        self.assertIn(
            "so a reader tells its shape and its age from the artifact itself", spec)
        # CANDIDATE REAL DEFECT (see repin log): "with no second document to consult" has no
        # mapping row in mapping.md Part 4 — the row's own wording ("a reader tells shape/age
        # from it") never carried this emphasis clause forward; confirmed absent from
        # PRODUCT_SPEC.md and the prototype draft section.md alike.
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.

    def test_e33_index_and_ownership(self):
        self.assert_index_and_ownership("E-33")


class TestContractDefaultDeny(unittest.TestCase, _AnchorHomeMixin):
    """INV-185 (M-362) — a contract publishes nothing by default; a permission is an act with an
    author and a date; credentials never cross at all."""

    def test_contract_default_deny(self):
        """F-contract's named test (ARCHITECTURE.md feature coverage)."""
        spec = read_flat(SPEC)
        self.assertIn("nothing publishes by default", spec)
        self.assertIn(
            "a contract *shall* publish no field until the owner records an explicit "
            "permission for it in the producer's tree", spec)
        self.assertIn("records an explicit permission for it in the producer's tree with its "
                      "date and author", spec)
        self.assertIn("INV-185, INV-24]", spec)  # code always co-brackets in the new format

    def test_construction_grants_no_permission(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "a field with no recorded permission *shall* stay in the producer's tree, the way "
            "a neighbour's product is built granting no permission", spec)

    def test_credentials_never_cross_a_channel(self):
        spec = read_flat(SPEC)
        self.assertIn("credentials *shall* cross no channel under any permission", spec)
        self.assertIn("the published artifact being the one road a producer's product data "
                      "takes between two agents", spec)

    def test_base_rulebook_carries_the_default_deny_law(self):
        self.assertIn("publishes nothing by default", read_flat(BASE),
                      "the base rulebook does not carry the contract's default-deny law")

    def test_inv185_index_and_ownership(self):
        self.assert_index_and_ownership("INV-185")


class TestProducerFormAndClock(unittest.TestCase, _AnchorHomeMixin):
    """INV-186 (M-363) — every field names its four things; the producer declares ONE number, its
    cadence, and a deploy never triggers the contract."""

    def test_every_contract_field_names_its_four_things(self):
        spec = read_flat(SPEC)
        for naming in ("what the field means", "the window it is measured over",
                       "how it is aggregated", "the source it derives from"):
            self.assertIn(naming, spec, "a contract field's naming is unstated: %r" % naming)
        self.assertIn(
            "the reviewer *shall* read a field missing any of the four as an incomplete "
            "surface", spec)
        self.assertIn("[INV-186]", spec)

    def test_producer_declares_its_cadence_and_its_watcher(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "the producer *shall* declare one cadence — how often it regenerates the "
            "artifact", spec)
        self.assertIn(
            "the producer's own session-start check *shall* fail *when* its scheduled "
            "regeneration did not run", spec)

    def test_a_deploy_never_triggers_the_contract(self):
        # mapping.md Part 4 (F-contract table) maps "The producer declares one cadence and holds
        # to it; a deploy refreshes the artifact as a bonus and never triggers it." to R6.7,
        # whose surviving text is asserted below and passes.
        spec = read_flat(SPEC)
        self.assertIn("never triggering it", spec)
        # CANDIDATE REAL DEFECT (see repin log): "a contract triggered by it goes stale the day
        # the building stops" — the explanatory WHY behind the deploy-never-triggers rule — has
        # no mapping row anywhere in mapping.md Part 4; R6.7's row states only the bare rule.
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.

    def test_inv186_index_and_ownership(self):
        self.assert_index_and_ownership("INV-186")


class TestConsumerRead(unittest.TestCase, _AnchorHomeMixin):
    """INV-187 (M-364) — the consumer declares ONE number, its staleness bound; it pins a version
    and reads read-only; the two numbers are set independently."""

    def test_consumer_declares_its_staleness_bound(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "the consumer *shall* declare one staleness bound — how old the artifact may be "
            "for its analysis", spec)
        self.assertIn(
            "its freshness check *shall* fail past that bound before any analysis runs", spec)
        self.assertIn("[INV-187]", spec)

    def test_consumer_pins_a_version_and_reads_read_only(self):
        spec = read_flat(SPEC)
        self.assertIn("the consumer *shall* pin the contract version it was written against",
                      spec)
        self.assertIn("the consumer *shall* read the artifact read-only", spec)
        self.assertIn(
            "carry a compatibility test that fails *when* its pinned version and the "
            "artifact's version diverge", spec)
        self.assertIn("it *shall* name the stale data aloud and stop", spec)

    def test_cadence_and_bound_are_two_independent_numbers(self):
        spec = read_flat(SPEC)
        self.assertIn(
            "the cadence and the staleness bound *shall* be two numbers set independently, "
            "and neither side *shall* read the other's", spec)

    def test_inv187_index_and_ownership(self):
        self.assert_index_and_ownership("INV-187")


# --------------------------------------------------------------------------- #
# [node: host-contract]
# --------------------------------------------------------------------------- #

class TestCardAndScan(unittest.TestCase, _AnchorHomeMixin):
    """E-32 (M-365) — the card in each agent's own tree, the live scan that finds it, and the
    read that runs before the acting."""

    def test_card_and_scan_law(self):
        """F-roster's named test (ARCHITECTURE.md feature coverage)."""
        # CANDIDATE REAL DEFECT (see repin log): "Discovery is a scan for cards, and the scan
        # states where it looks and what it costs" has no mapping row in mapping.md Part 4 — its
        # own rows for the scan ("Discovery reads two globs per root and treats every card as an
        # agent." -> R5.4, matched below) cover the mechanics, not this title-style summary
        # sentence, which is gone from PRODUCT_SPEC.md's rewritten Requirement 193 (replaced by a
        # plainer Context paragraph).
        spec = read_flat(SPEC)
        self.assertIn(
            "the system *shall* treat a tree that carries a card as an agent, and writing the "
            "card *shall* be the one act that seats it", spec)
        self.assertIn(
            "the agent card *shall* live in the agent's own tree at `.live-spec/agent.md`",
            spec)
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.
        self.assertIn(
            "the system *shall* discover agents by reading two globs under each root", spec)
        self.assertIn("who owns what is always a lookup", spec)
        self.assertIn("[E-32]", spec)

    def test_card_names_its_five_fields(self):
        # the new format lists the card's fields comma-separated rather than semicolon-separated
        spec = read_flat(SPEC)
        for field in ("the agent's name", "its standing mission", "the zones it owns",
                      "each contract it publishes with the path its artifact lives at",
                      "its inbox address"):
            self.assertIn(field, spec, "the card's field is unstated: %r" % field)

    def test_the_read_runs_before_the_acting(self):
        # mapping.md Part 4 (F-roster table) maps "The owning card is read before acting; the
        # reviewer's review is the net for that discipline." to R5.9, matched below.
        # CANDIDATE REAL DEFECT (see repin log): "The read runs first, ahead of the acting" (the
        # rationale for why the order matters — every law below keys on the answer) has no
        # mapping row of its own in mapping.md Part 4.
        spec = read_flat(SPEC)
        self.assertIn(
            "the system *shall* read the owning card before acting on anything that might not "
            "be its own", spec)
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.

    def test_e32_index_and_ownership(self):
        self.assert_index_and_ownership("E-32")


class TestDeclarationLaw(unittest.TestCase, _AnchorHomeMixin):
    """INV-184 (M-366) — a tree's presence grants nothing and writing a card grants everything;
    no file outside any tree describes any agent; write-ownership grants the card with no
    permission act of its own; the pack's own card is read from disk."""

    def test_pack_card_exists_and_names_its_five_fields(self):
        """The card arm, exercised against this pack's own real `.live-spec/agent.md` on disk."""
        path = os.path.join(ROOT, ".live-spec", "agent.md")
        self.assertTrue(os.path.isfile(path),
                        "this pack's own card is absent: .live-spec/agent.md (SPEC E-32, INV-184)")
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        low = " ".join(raw.split()).lower()
        for field in ("name", "mission", "zone", "contract", "inbox"):
            self.assertIn(field, low, "the card names no %s (SPEC E-32)" % field)

        # The contracts field names each contract WITH the path its artifact lives at, so the
        # claim is read against the CONTRACTS section alone — a path elsewhere on the card (the
        # inbox address, a pointer to a rulebook) says nothing about a published contract.
        sections = re.split(r"^##\s+", raw, flags=re.M)
        contracts = [s for s in sections if s.lower().startswith("contracts")]
        self.assertEqual(len(contracts), 1,
                         "the card carries no single contracts section (SPEC E-32)")
        body = contracts[0]
        declares_none = re.search(r"\bnone\b", body, re.I) is not None
        paths = re.findall(r"`[^`]*/[^`]*`", body)
        self.assertTrue(
            declares_none or paths,
            "the card's contracts section names neither a published contract with the path its "
            "artifact lives at, nor its emptiness (SPEC E-32)")
        if not declares_none:
            # Each named contract carries its path; a bare list of names is an incomplete card.
            self.assertTrue(paths, "a card naming a published contract owes its artifact's path "
                                   "(SPEC E-32)")

    def test_no_file_outside_any_tree_describes_any_agent(self):
        # mapping.md Part 4 (F-roster table) maps "No file outside any tree describes an agent."
        # to R5.8, matched by the two assertions below that pass.
        # CANDIDATE REAL DEFECT (see repin log): "this design has no such file to protect" (the
        # write-ownership rationale) and "discovery reads those trees without writing anything
        # anywhere" (the read-only-during-discovery guarantee) have no mapping row of their own
        # in mapping.md Part 4 and are confirmed absent from PRODUCT_SPEC.md and the prototype
        # draft section.md.
        spec = read_flat(SPEC)
        self.assertIn(
            "the system *shall* let no file outside any tree describe any agent", spec)
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.
        self.assertIn(
            "each agent owning its own description the way it owns its own tree", spec)
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.
        self.assertIn("[INV-184]", spec)

    def test_write_ownership_grants_the_card(self):
        # mapping.md Part 4 (F-roster table) maps "Write-ownership grants the card, so it needs
        # no permission act." to R5.10 and "The card holds identity/addresses; product data in a
        # card is a contract field on the contract's permission road." to R5.11, both matched by
        # the passing assertions below.
        # CANDIDATE REAL DEFECT (see repin log): "the default-deny law meets no exception here"
        # and "whatever file it sits in" have no mapping row of their own in mapping.md Part 4 —
        # the underlying rules hold (R5.10, R5.11), but this specific explanatory framing of
        # each is gone from PRODUCT_SPEC.md and the prototype draft section.md alike.
        spec = read_flat(SPEC)
        self.assertIn(
            "the system *shall* grant the card by write-ownership, so writing it needs no "
            "permission act", spec)
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.
        self.assertIn(
            "product data placed in a card *shall* be a contract field taking the contract's "
            "permission road", spec)
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.

    def test_cardless_tree_is_flagged_beside_its_siblings(self):
        clause = self.assert_declared("INV-184")
        self.assertIn(
            "an inventoried live-spec host tree carries no `.live-spec/agent.md`, the system "
            "*shall* flag it as an incomplete record", clause)
        # the rank the flag carries now sits in a bullet under its own criterion, so the
        # declaration is read with its bullets rather than the whole file
        self.assertIn(
            "an incomplete record ranks the same as a project kind recorded with no declared "
            "layers", clause)

    def test_inv184_index_and_ownership(self):
        self.assert_index_and_ownership("INV-184")


# --------------------------------------------------------------------------- #
# [node: inbox]
# --------------------------------------------------------------------------- #

class TestMessageLifecycle(unittest.TestCase, _AnchorHomeMixin):
    """INV-192 (M-367) — the stable identifier, the reply riding the sender's own inbox, and the
    terminal state every message reaches."""

    def test_message_carries_a_stable_identifier(self):
        clause = self.assert_declared("INV-192")
        self.assertIn("the system *shall* mint a stable identifier per message from the "
                      "sender's session identity", clause)
        # the keying rides a bullet under the minting criterion, stated as a standing fact
        self.assertIn("an exchange is keyed to its first message's identifier, which "
                      "every reply names", clause)
        self.assertIn("INV-192, INV-117]", clause)  # code always co-brackets in the new format

    def test_reply_travels_the_senders_own_inbox(self):
        spec = read_flat(SPEC)
        self.assertIn("a reply *shall* travel back to the sender as one new file in the "
                      "sender's inbox", spec)
        self.assertIn("the count of channels between two agents stays at two", spec)

    def test_reply_owes_no_blocked_work_of_its_own(self):
        spec = read_flat(SPEC)
        self.assertIn("owing no blocked work of its own", spec)
        self.assertIn("the message it discharges already named the work", spec)

    def test_every_message_reaches_a_terminal_state(self):
        spec = read_flat(SPEC)
        self.assertIn("every message *shall* state its need-by and *shall* reach one terminal "
                      "state", spec)
        self.assertIn("delivered, declined, or escalated past its stated need-by", spec)
        self.assertIn("the system *shall* surface it in the sender's status report as blocked "
                      "work aged past its need-by", spec)

    def test_no_agent_wakes_a_dormant_window(self):
        spec = read_flat(SPEC)
        self.assertIn("*shall* wake a dormant window on no occasion", spec)

    def test_inv192_index_and_ownership(self):
        self.assert_index_and_ownership("INV-192")


# --------------------------------------------------------------------------- #
# [node: build-pipeline]
# --------------------------------------------------------------------------- #

class TestAgentBirth(unittest.TestCase, _AnchorHomeMixin):
    """T-22 (M-368) — the proposal, the owner's ratification, the contract that outlives the
    migration, and the grain the owner's word settles."""

    def test_agent_birth_walk(self):
        """F-agent-birth's named test (ARCHITECTURE.md feature coverage)."""
        spec = read_flat(SPEC)
        self.assertIn("a capability pins to no agent's zone, or a capability has outgrown its "
                      "host, the system *shall* let any agent propose a new agent", spec)
        self.assertIn("naming the capability, the zone the new agent would own, and the "
                      "contracts it would publish", spec)
        self.assertIn("[T-22]", spec)

    def test_ratification_authorizes_the_founding_and_the_agent_declares_it(self):
        spec = read_flat(SPEC)
        self.assertIn("the proposal *shall* carry the adversarial read an expensive decision "
                      "earns and *shall* stand as a proposal until the owner ratifies the "
                      "creation", spec)
        self.assertIn("**Case: the owner ratifies, the agent declares itself**", spec)
        # CANDIDATE REAL DEFECT (see repin log): "These are two acts on two objects" (the meta
        # framing that ratification and self-declaration are two distinct acts, not one) has no
        # mapping row anywhere in mapping.md Part 4 — the row set for this requirement (R9.2-
        # R9.5) states each act's mechanics but never this structural framing sentence.
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.
        # mapping.md Part 1 cites INV-10 into R9.3 ("The owner's word authorizes the creation (a
        # new tree/queue/gates/standing cost)."), whose surviving text is the affirmative form of
        # "no agent founds another on its own authority" — if only the owner's word authorizes
        # creation, no agent can found one on its own authority; re-pinned to that criterion.
        self.assertIn("the owner's word *shall* authorize the creation, since a new agent is a "
                      "new tree, a new queue, a new set of gates, and a standing cost the owner "
                      "carries", spec)
        self.assertIn("the founded agent *shall* declare itself by writing its own card, and "
                      "every scan *shall* find it from that moment", spec)

    def test_contract_outlives_the_migration(self):
        # mapping.md Part 4 (F-agent-birth table) maps "A migrated contract keeps the consumer's
        # pin until it chooses to move; the new owner publishes at the address its own card
        # names." to R9.8, matched below.
        spec = read_flat(SPEC)
        self.assertIn("**Case: the contract survives the migration**", spec)
        self.assertIn("the system *shall* let the consumer keep reading its pinned version "
                      "until it chooses to move", spec)
        # CANDIDATE REAL DEFECT (see repin log): "A migration that breaks a consumer's pin has
        # broken the contract rather than moved it" has no mapping row anywhere in mapping.md
        # Part 4 — it is the source's own rhetorical restatement of R9.8, not a distinct claim.
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.

    def test_grain_is_the_owners_call_recorded_with_its_date(self):
        # mapping.md Part 4 (F-agent-birth table) maps "A capability on the skill/agent line is
        # settled by the owner's word, recorded with its date." to R9.9, matched below.
        spec = read_flat(SPEC)
        self.assertIn("**Case: the kind is the owner's call**", spec)
        self.assertIn("the owner's word *shall* settle which it is, the call recorded with "
                      "its date", spec)
        # CANDIDATE REAL DEFECT (see repin log): "That weighing is taste, which is the
        # human-only fact this deferral names" has no mapping row anywhere in mapping.md Part 4
        # — R9.9's row states only the settled-by-owner's-word rule, not this "taste" rationale
        # (the "human-only fact" phrase exists elsewhere in the spec for a wholly different
        # requirement's deferral markers, not for this skill/agent grain call).
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.
        self.assertIn("recorded with its date in the proposing agent's journal", spec)

    def test_t22_index_and_ownership(self):
        self.assert_index_and_ownership("T-22")


# --------------------------------------------------------------------------- #
# [node: base-rulebook] — recognition, the exchange bound, the default owner
# --------------------------------------------------------------------------- #

class TestRecogniseAndRoute(unittest.TestCase, _AnchorHomeMixin):
    """INV-195 — an agent recognises a neighbour's zone on its own; the owner's word afterwards
    is an acknowledgement of a thing already done."""

    def test_agent_recognises_a_neighbours_zone_itself(self):
        # mapping.md Part 4 (F-agent-ask table) maps "The agent recognizes the neighbour's zone
        # on its own and takes the fitting channel." to R7.9 (= Requirement 195 criterion 9),
        # matched below via the structurally-fixed `assert_declared` (see the shared-helper note
        # at the top of this file).
        clause = self.assert_declared("INV-195")
        self.assertIn("the system *shall* scan for cards, find the owning agent, and take the "
                      "channel that fits, on its own recognition", clause)
        # CANDIDATE REAL DEFECT (see repin log): "carries no fact the agent lacked" has no
        # mapping row anywhere in mapping.md Part 4 — R7.9's row states only the bare
        # recognition mechanism, not this owner-afterwards-adds-nothing rationale.
        # retired at row-445 pass 2: journal-bound rationale (mapping.md Part-4 exclusion —
        # "its rationale, its dated provenance, and its history are excluded — those belong to the
        # journal"; DELTA.md wave: one restoration judged genuine content "(not rationale)", the
        # audited rest rationale). Behavioural half asserted above/below from its own criterion.
        # CANDIDATE REAL DEFECT (see repin log): "made the owner its router" has no mapping row
        # anywhere in mapping.md Part 4, for the same reason.
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.

    def test_the_base_rulebook_carries_the_recognition_duty(self):
        base = read_flat(BASE)
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.
        # retired at row-445 pass 2: journal-bound rationale/emphasis (mapping.md Part-4 exclusion;
        # DELTA.md wave verdict: one restoration judged genuine content "(not rationale)", the audited
        # rest rationale). The behavioural half stays asserted above from its own criterion.

    def test_inv195_index_and_ownership(self):
        self.assert_index_and_ownership("INV-195")


class TestExchangeBound(unittest.TestCase, _AnchorHomeMixin):
    """INV-196 — one question crosses between two agents twice; the third crossing goes to the
    owner. Every hop of a refer-and-re-send loop passes its own law, so the exchange needs its
    own bound."""

    def test_one_question_crosses_twice_then_goes_to_the_owner(self):
        clause = self.assert_declared("INV-196")
        self.assertIn("let one question cross between the same two agents at most twice", clause)
        self.assertIn("send the third crossing to the owner", clause)
        self.assertIn("reopen the count by rewording the question", clause)

    def test_the_bound_cites_the_kin_it_copies(self):
        """The human-decision withdrawal loop already carries this shape [INV-130]; the bound is
        that pattern applied to a channel rather than a fresh invention."""
        self.assertIn("INV-130", self.assert_declared("INV-196"))

    def test_inv196_index_and_ownership(self):
        self.assert_index_and_ownership("INV-196")


class TestWrongReferralNamed(unittest.TestCase, _AnchorHomeMixin):
    """INV-225 (M-406, ROADMAP 388) — a wrong referral is named as the finding, not absorbed by
    the two-crossing cap. A referral names the zone it says owns the question; it is wrong when
    that zone refers it back rather than answering, which crosses the same two agents twice
    [INV-196]. The escalation names the wrong referral rather than the neutral "could not settle"."""

    def test_wrong_referral_law_stands(self):
        clause = self.assert_declared("INV-225")
        self.assertIn("the system *shall* name the wrong referral in the sender's status "
                      "report", clause)
        self.assertIn("a wrong referral pointed at a zone which, by its own referring-back, "
                      "does not own the target", clause)
        self.assertIn("name the wrong referral in the sender's status report", clause)

    def test_wrong_referral_is_named_the_finding(self):
        clause = self.assert_declared("INV-225")
        # the mechanical distinction the checker reads, and the honest split it does NOT cross
        self.assertIn("a referral met by a counter-referral between the same two agents",
                      clause)
        self.assertIn("stays the receiving sweep's and the reviewer's judgment", clause)
        # PASS-2 RE-TRIAGE: restored by the prover MUST-FIX wave — mapping.md's "Restored owner
        # decision — zones may overlap" note records the zones-may-overlap decision and its
        # uniqueness-check consequence appended as new criteria (Requirement 196, criterion 20,
        # co-cited [INV-225]) rather than dropped. Re-pinned from the old spec's "no uniqueness
        # check is built" phrase to the restored criterion's own wording. Same underlying
        # restoration as TestDefaultOwner.test_zones_may_overlap below.
        self.assertIn("the system *shall* build no uniqueness check over zone claims, the wrong "
                      "referral alone earning a name", clause)
        self.assertIn("ride the suite", clause)
        self.assertIn("staying clear of the push chain", clause)

    def test_base_rulebook_carries_the_wrong_referral_law(self):
        self.assertIn("named as a wrong referral", read_flat(BASE),
                      "the base rulebook does not carry the wrong-referral law")

    def test_inv225_index_and_ownership(self):
        self.assert_index_and_ownership("INV-225")


class TestDefaultOwner(unittest.TestCase, _AnchorHomeMixin):
    """INV-197 — a concern no agent's zone owns goes to the pack, and the work never stalls on
    ownership (the owner's word through the promoter's inbox deposit, 2026-07-17)."""

    def test_an_unowned_concern_goes_to_the_pack(self):
        # mapping.md Part 4 (F-agent-ask table) maps "An unowned concern goes to the pack, which
        # answers who owns it (agent / new agent / skill)." to R8.5, matched below.
        clause = self.assert_declared("INV-197")
        self.assertIn("carried to the pack as its default owner", clause)
        self.assertIn("owning zone does not exist yet", clause)
        # CANDIDATE REAL DEFECT (see repin log): the cross-reference to INV-191 (the
        # homeless-question-dropped law) has no mapping row anywhere in mapping.md Part 1, Part
        # 3, or Part 4 that co-cites it with INV-197/R8.5/R8.6 — mapping's own Part 1 table
        # cites INV-191 only into R56.2, R195.13, R196.4, never beside R8.5/R8.6. The two laws
        # are no longer tied together in one criterion's bracket in PRODUCT_SPEC.md.
        # retired at row-445 pass 2: the INV-191 co-citation was a prose-adjacency artifact of the
        # old format — INV-191 owns its own criteria (R56.2, R195.13, R196.4), asserted green by
        # TestHomelessQuestionDropped; no mapping row co-cites it with INV-197 (worker analysis above).

    def test_work_never_stalls_on_ownership(self):
        clause = self.assert_declared("INV-197")
        self.assertIn("the agent *shall* do the work it can do now in whatever tree can hold "
                      "it", clause)
        self.assertIn("mark that work provisional", clause)
        self.assertIn("*while* ownership is being settled, the agent *shall* do the work it "
                      "can do now", clause)

    def test_zones_may_overlap(self):
        """His word, recorded against the queued uniqueness row it refuted the same day."""
        # PASS-2 RE-TRIAGE: restored by the prover MUST-FIX wave — mapping.md's "Restored owner
        # decision — zones may overlap" note (folded in after the re-pin sweep found this one
        # genuine content loss) appends the recorded owner decision as a new named case and
        # criterion under Requirement 196 (co-cited [INV-197, INV-225]), rather than leaving it
        # dropped. Re-pinned from the old spec's bare "Zones may overlap" phrase to the restored
        # Case heading plus the criterion's own wording, both now present.
        spec = read_flat(SPEC)
        self.assertIn("Case: zones may overlap", spec)
        self.assertIn(
            "the system *shall* let two agents' zones overlap, each card recording what its own "
            "agent claims and two cards claiming one area both standing, and *shall* force no "
            "agent to carve a disjoint zone", self.assert_declared("INV-197"))

    def test_inv197_index_and_ownership(self):
        self.assert_index_and_ownership("INV-197")


if __name__ == "__main__":
    unittest.main()
