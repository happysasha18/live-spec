"""Accepted-work admission: source + outcome + DOD decide whether the board may change."""

import importlib.util
import json
import sys
from pathlib import Path

from conftest import ROOT


SCRIPT = Path(ROOT) / "scripts" / "task-admission.py"
sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location("task_admission", SCRIPT)
admission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admission)

import checkpoint  # noqa: E402 — the checkpoint half of the same state machine


def host(tmp_path):
    plan = tmp_path / "PLAN.md"
    plan.write_text("# Host plan\n\n## Tasks\n\n## Blockers\n\nNone.\n", encoding="utf-8")
    return plan, tmp_path / ".live-spec" / "checkpoints"


def new_route(**overrides):
    route = {
        "action": "new", "creates_work": True, "existing_task": None,
        "title": "Send the weekly digest", "project": "route-host", "scope": "Reports",
        "source": {"kind": "person", "detail": "the person, this turn"},
        "observable_outcome": "a weekly digest reaches the test inbox",
        "done_when": "the fixture records exactly one weekly message",
        "verification": "python3 tests/test_digest.py",
        "context_pointers": ["`scripts/digest.py`", "R-104"],
    }
    route.update(overrides)
    return route


def test_new_instruction_writes_one_row_and_one_checkpoint(tmp_path):
    plan, checkpoints = host(tmp_path)
    result = admission.admit(new_route(), plan, checkpoints)
    assert result["task_id"] == "q-1"
    assert plan.read_text(encoding="utf-8").count("— id: q-1") == 1
    body = (checkpoints / "q-1.md").read_text(encoding="utf-8")
    assert "Owner: pipeline" in body
    assert "Definition of done:" in body


def test_the_row_lands_inside_tasks_when_the_plan_has_no_blockers_section(tmp_path):
    """The row goes where the plan's readers look, not to the foot of the file.

    Red-proven against the pre-fix insertion on this project's own PLAN.md (2026-09-06), which
    carries no `## Blockers` section: q-823 was written past the end of `## Tasks`, so the parser
    every reader shares never saw it — no probe line, no board column, no next-action candidate.
    """
    plan = tmp_path / "PLAN.md"
    plan.write_text(
        "# Host plan\n\n## Tasks\n\n### \u2705 Done thing \u2014 id: q-4\n\n"
        "## Environment\n\nnotes.\n",
        encoding="utf-8",
    )
    admission.admit(new_route(), plan, tmp_path / ".live-spec" / "checkpoints")
    body = plan.read_text(encoding="utf-8")
    tasks = body[body.index("## Tasks"):body.index("## Environment")]
    assert "— id: q-5" in tasks
    assert body.rstrip().endswith("notes.")


def test_question_and_correction_write_nothing(tmp_path):
    plan, checkpoints = host(tmp_path)
    before = plan.read_bytes()
    none = admission.admit({"action": "none", "creates_work": False}, plan, checkpoints)
    existing = admission.admit(
        {"action": "existing", "creates_work": False, "existing_task": "q-7"},
        plan, checkpoints,
    )
    assert none["writes"] == [] and existing["writes"] == []
    assert plan.read_bytes() == before
    assert not checkpoints.exists()


def test_review_opinion_cannot_mint_work(tmp_path):
    plan, checkpoints = host(tmp_path)
    route = new_route(source={"kind": "review", "detail": "an internal review finding"})
    try:
        admission.admit(route, plan, checkpoints)
    except admission.AdmissionError as exc:
        assert "person or external_defect" in str(exc)
    else:
        raise AssertionError("review opinion admitted as work")


def test_external_defect_needs_a_promise_reproduction_and_observer(tmp_path):
    plan, checkpoints = host(tmp_path)
    route = new_route(source={"kind": "external_defect", "detail": "support report"})
    try:
        admission.admit(route, plan, checkpoints)
    except admission.AdmissionError as exc:
        assert "promised_behavior" in str(exc)
        assert "reproduction" in str(exc)
        assert "observed_by" in str(exc)
    else:
        raise AssertionError("unreproduced defect admitted as work")


def test_done_when_cannot_make_the_person_the_checker(tmp_path):
    plan, checkpoints = host(tmp_path)
    try:
        admission.admit(new_route(done_when="the user approves the result"), plan, checkpoints)
    except admission.AdmissionError as exc:
        assert "person" in str(exc)
    else:
        raise AssertionError("human-gated DOD admitted")


# ---------------------------------------------------------------- the ticket state machine
# T3-T9 of the product contract's section 4 table
# (`.live-spec/turnkey-contract-composed.md`), each proven twice: the legal move, and the
# illegal one the code refuses. Every one of these was red before the transition existed.


def seeded(tmp_path):
    """One admitted ticket: a queued row and its open checkpoint. Returns both plus the id."""
    plan, checkpoints = host(tmp_path)
    task_id = admission.admit(new_route(), plan, checkpoints)["task_id"]
    return plan, checkpoints, task_id, checkpoints / (task_id + ".md")


def row_of(plan, task_id):
    body = plan.read_text(encoding="utf-8")
    start = body.index("### ")
    while "— id: %s" % task_id not in body[start:body.index("\n", start)]:
        start = body.index("\n### ", start) + 1
    end = body.find("\n### ", start)
    if end == -1:
        end = body.find("\n## ", start)
    return body[start:end if end != -1 else len(body)]


def refused(fn, *args, **kwargs):
    """Run a transition expected to refuse; return the one-line message it printed."""
    try:
        fn(*args, **kwargs)
    except admission.AdmissionError as exc:
        return str(exc)
    raise AssertionError("the illegal move was not refused")


# --- a ticket carries its context pointers -----------------------------------------------

def test_an_admitted_ticket_carries_its_context_pointers(tmp_path):
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    row = row_of(plan, task_id)
    assert "**Context pointers.**" in row
    assert "`scripts/digest.py`" in row and "R-104" in row


def test_a_ticket_carrying_no_context_pointers_is_refused(tmp_path):
    plan, checkpoints = host(tmp_path)
    before = plan.read_bytes()
    message = refused(admission.admit, new_route(context_pointers=[]), plan, checkpoints)
    assert "context pointer" in message
    assert plan.read_bytes() == before and not checkpoints.exists()


# --- T3, the queued half -----------------------------------------------------------------

def test_a_correction_rewrites_a_queued_tickets_goal_and_done_in_place(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    sheet_before = cp.read_bytes()
    admission.correct(plan, checkpoints, task_id,
                      goal="Send the weekly digest to the whole list",
                      done="the fixture records one weekly message per subscriber")
    row = row_of(plan, task_id)
    assert "### ⬜ Send the weekly digest to the whole list — id: %s" % task_id in row
    assert "**Done when:** the fixture records one weekly message per subscriber" in row
    assert plan.read_text(encoding="utf-8").count("— id: %s" % task_id) == 1
    assert cp.read_bytes() == sheet_before, "the queued half touched the checkpoint"


def test_a_second_ticket_with_the_same_goal_is_refused(tmp_path):
    """T1's own duplicate rule: the goal line alone decides, and nothing else does."""
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    before = plan.read_bytes()
    message = refused(admission.admit, new_route(), plan, checkpoints)
    assert "already has this title" in message
    assert plan.read_bytes() == before
    assert sorted(pth.name for pth in checkpoints.iterdir()) == [task_id + ".md"]


def test_a_correction_on_a_ticket_in_hand_is_refused(tmp_path):
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    admission.hold(plan, task_id, "the session")
    before = plan.read_bytes()
    message = refused(admission.correct, plan, checkpoints, task_id, goal="something else")
    assert "in hand" in message
    assert plan.read_bytes() == before


# --- T4, blocked -------------------------------------------------------------------------

def test_a_blocker_names_one_of_the_three_kinds_and_the_concrete_thing(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.block(plan, checkpoints, task_id, "technical limit",
                    "`bash adopt/install-external-skills.sh` exits 1 against any host tree")
    row = row_of(plan, task_id)
    assert row.startswith("### ⛔ ")
    assert "**Blocked by:** technical limit: `bash adopt/install-external-skills.sh` exits 1" in row
    assert "install-external-skills.sh" in cp.read_text(encoding="utf-8")


def test_a_blocker_reason_that_only_restates_difficulty_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    before, sheet = plan.read_bytes(), cp.read_bytes()
    message = refused(admission.block, plan, checkpoints, task_id, "technical limit",
                      "this is complicated and takes too long")
    assert "difficult" in message or "hard" in message
    assert plan.read_bytes() == before and cp.read_bytes() == sheet


def test_a_blocker_kind_outside_the_three_is_refused(tmp_path):
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    before = plan.read_bytes()
    message = refused(admission.block, plan, checkpoints, task_id, "waiting on review",
                      "`pytest` exits 1")
    assert "technical limit" in message
    assert plan.read_bytes() == before


# --- T5, the block clears ----------------------------------------------------------------

def test_a_cleared_block_lands_in_hand_when_the_ticket_names_a_holder(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the session")
    admission.block(plan, checkpoints, task_id, "outside dependency", "`live-spec` 6.0.0 unreleased")
    admission.unblock(plan, checkpoints, task_id, "commit 8a076e76 releases 6.0.0")
    row = row_of(plan, task_id)
    assert row.startswith("### 🔄 ")
    assert "**Blocked by:**" not in row
    assert "**Holder:** the session" in row
    assert "Blocked:" not in cp.read_text(encoding="utf-8"), "the block line outlived the clearing"


def test_a_cleared_block_lands_queued_when_nobody_holds_the_ticket(tmp_path):
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    admission.block(plan, checkpoints, task_id, "owner action",
                    "the owner renews the Cloudflare deploy key")
    admission.unblock(plan, checkpoints, task_id, "his reply of 2026-09-06: the key is renewed")
    row = row_of(plan, task_id)
    assert row.startswith("### ⬜ ")
    assert "**Blocked by:**" not in row


def test_a_block_cleared_by_assumption_is_refused(tmp_path):
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    admission.block(plan, checkpoints, task_id, "outside dependency", "`live-spec` 6.0.0 unreleased")
    before = plan.read_bytes()
    message = refused(admission.unblock, plan, checkpoints, task_id, "assumed cleared by now")
    assert "commit" in message
    assert plan.read_bytes() == before


# --- T6, park ----------------------------------------------------------------------------

def test_parking_clears_the_holder_and_leaves_the_checkpoint_open_with_next(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the session")
    admission.park(plan, checkpoints, task_id, "the digest template still needs its footer")
    row = row_of(plan, task_id)
    assert row.startswith("### ⬜ ")
    assert "**Holder:**" not in row
    sheet = checkpoint.read_checkpoint(cp)
    assert sheet["status"] == "open"
    assert sheet["sections"]["NEXT"] == "the digest template still needs its footer"


def test_parking_a_ticket_nobody_holds_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    before, sheet = plan.read_bytes(), cp.read_bytes()
    message = refused(admission.park, plan, checkpoints, task_id, "what remains")
    assert "holder" in message
    assert plan.read_bytes() == before and cp.read_bytes() == sheet


# --- T7, done ----------------------------------------------------------------------------

def finished(plan, checkpoints, task_id, cp):
    admission.hold(plan, task_id, "the session")
    checkpoint.update_checkpoint(cp, done="the digest ships", in_progress="(nothing)", next="(nothing)")


def test_closing_closes_the_checkpoint_and_then_writes_the_mark(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    assert checkpoint.read_checkpoint(cp)["status"] == "closed"
    assert row_of(plan, task_id).startswith("### ✅ ")


def test_a_close_over_open_work_is_refused_and_the_mark_does_not_move(tmp_path):
    """The order is what this proves: the mark is the second write, so a checkpoint that
    cannot close leaves a ticket that is not marked done."""
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the session")
    checkpoint.update_checkpoint(cp, next="the footer is still missing")
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "NEXT" in message
    assert checkpoint.read_checkpoint(cp)["status"] == "open"
    assert row_of(plan, task_id).startswith("### 🔄 ")


def test_a_second_close_over_a_closed_checkpoint_only_rewrites_the_mark(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ✅ ", "### 🔄 ", 1), encoding="utf-8")
    sheet = cp.read_bytes()
    admission.close(plan, checkpoints, task_id)
    assert cp.read_bytes() == sheet, "the re-run rewrote the checkpoint"
    assert row_of(plan, task_id).startswith("### ✅ ")


# --- T8, reopen --------------------------------------------------------------------------

def test_reopening_names_the_false_condition_and_never_writes_a_copy(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    admission.reopen(plan, checkpoints, task_id,
                     false_condition="the fixture records exactly one weekly message",
                     evidence="tests/test_digest.py fails at HEAD 4f21c9a with two messages")
    body = plan.read_text(encoding="utf-8")
    assert body.count("— id: %s" % task_id) == 1, "reopening wrote a copy"
    assert row_of(plan, task_id).startswith("### 🔄 ")
    sheet = checkpoint.read_checkpoint(cp)
    assert sheet["status"] == "open"
    assert "4f21c9a" in sheet["sections"]["NEXT"]


def test_reopening_a_ticket_that_was_never_done_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    before, sheet = plan.read_bytes(), cp.read_bytes()
    message = refused(admission.reopen, plan, checkpoints, task_id,
                      false_condition="something", evidence="somewhere")
    assert "done" in message
    assert plan.read_bytes() == before and cp.read_bytes() == sheet


# --- T9, abandon -------------------------------------------------------------------------

def test_abandoning_clears_the_open_sections_with_the_reason_and_closes_in_the_same_step(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the session")
    checkpoint.update_checkpoint(cp, in_progress="drafting the footer", next="ship it")
    admission.abandon(plan, checkpoints, task_id, "the channel it fed was retired")
    sheet = checkpoint.read_checkpoint(cp)
    assert sheet["status"] == "closed"
    for name in ("IN PROGRESS", "NEXT"):
        assert sheet["sections"][name].splitlines()[-1].endswith("the channel it fed was retired)")
        assert "drafting the footer" not in sheet["sections"][name]
    assert "**Holder:**" not in row_of(plan, task_id)


def test_abandoning_without_a_reason_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the session")
    sheet = cp.read_bytes()
    message = refused(admission.abandon, plan, checkpoints, task_id, "   ")
    assert "reason" in message
    assert cp.read_bytes() == sheet


# --- the worker's brief ------------------------------------------------------------------

def test_the_worker_brief_is_the_ticket_entry_plus_the_checkpoints_next_verbatim(tmp_path):
    """Diffed against the two sources themselves, read here independently of the emitter."""
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the worker")
    checkpoint.update_checkpoint(cp, next="draft the footer, then run tests/test_digest.py")

    entry = row_of(plan, task_id).strip()
    sheet_next = cp.read_text(encoding="utf-8").split("## NEXT\n")[1].split("\n## ")[0].strip()

    brief = admission.worker_brief(plan, checkpoints, task_id)
    assert brief == entry + "\n\n## NEXT\n\n" + sheet_next + "\n"
    assert sheet_next in brief and entry in brief


# --- the human gate, without a name in it ------------------------------------------------
# Red-proved 2026-09-06 against the previous pattern, which hardcoded one person's name and
# read only "<subject> <verb>": four of the five refusals below were admitted.

HUMAN_GATED = (
    "the owner approved it",
    "confirmed by the owner",
    "accepted by the person",
    "the owner looks at it",
    "the person signs off on the page",
)

ARTIFACT_PROVEN = (
    "the test passes",
    "the page renders",
)


def test_a_done_that_ends_at_someones_eye_is_refused_in_either_word_order(tmp_path):
    for i, phrase in enumerate(HUMAN_GATED):
        room = tmp_path / ("gated-%d" % i)
        room.mkdir()
        plan, checkpoints = host(room)
        message = refused(admission.admit, new_route(done_when=phrase), plan, checkpoints)
        assert "person" in message, phrase


def test_no_persons_name_is_written_into_the_refusal(tmp_path):
    """The gate held on one machine and nowhere else while it named its author."""
    source = (Path(ROOT) / "scripts" / "task-admission.py").read_text(encoding="utf-8")
    assert "sasha" not in source.lower()


def test_an_artifact_proven_done_is_admitted(tmp_path):
    for i, phrase in enumerate(ARTIFACT_PROVEN):
        room = tmp_path / ("proven-%d" % i)
        room.mkdir()
        plan, checkpoints = host(room)
        result = admission.admit(new_route(done_when=phrase), plan, checkpoints)
        assert result["action"] == "new", phrase


# --- hold and block read the state they overwrite -----------------------------------------

def test_taking_a_closed_ticket_in_hand_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    before = plan.read_bytes()
    message = refused(admission.hold, plan, task_id, "a second session")
    assert "done" in message
    assert plan.read_bytes() == before


def test_taking_a_ticket_another_holder_already_runs_is_refused(tmp_path):
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    admission.hold(plan, task_id, "Builder (opus)")
    before = plan.read_bytes()
    message = refused(admission.hold, plan, task_id, "Checker (haiku)")
    assert "Builder (opus)" in message
    assert plan.read_bytes() == before, "the second lane renamed the holder of running work"


def test_the_same_holder_may_retake_its_own_ticket(tmp_path):
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    admission.hold(plan, task_id, "Builder (opus)")
    admission.hold(plan, task_id, "Builder (opus)")
    assert row_of(plan, task_id).count("**Holder:**") == 1


def test_blocking_a_closed_ticket_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    before = plan.read_bytes()
    message = refused(admission.block, plan, checkpoints, task_id, "owner action",
                      "the owner renews the deploy key")
    assert "done" in message
    assert plan.read_bytes() == before


def test_a_second_block_over_a_blocked_ticket_is_refused(tmp_path):
    plan, checkpoints, task_id, _ = seeded(tmp_path)
    admission.block(plan, checkpoints, task_id, "outside dependency",
                    "`live-spec` 6.0.0 unreleased")
    before = plan.read_bytes()
    message = refused(admission.block, plan, checkpoints, task_id, "technical limit",
                      "`pytest` exits 1")
    assert "already blocked" in message
    row = row_of(plan, task_id)
    assert row.count("**Blocked by:**") == 1
    assert "6.0.0 unreleased" in row, "the first blocker's cause was overwritten"
    assert plan.read_bytes() == before


# --- T8 needs the checkpoint it reopens ---------------------------------------------------

def test_reopening_a_ticket_with_no_checkpoint_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    cp.unlink()
    before = plan.read_bytes()
    message = refused(admission.reopen, plan, checkpoints, task_id,
                      false_condition="the digest shipped", evidence="the inbox is empty")
    assert "no checkpoint" in message
    assert plan.read_bytes() == before, "the row walked back to in-hand with nothing to resume"
