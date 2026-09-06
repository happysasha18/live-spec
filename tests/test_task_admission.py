"""Accepted-work admission: source + outcome + DOD decide whether the board may change."""

import pytest
import importlib.util
import os
import json
import subprocess
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
        # Requirement 309 criterion 41: a statement carries a time estimate. With no comparable
        # closed row in a throwaway tree there is no history to read one off, so the route
        # carries the range and the derived basis says the history is missing.
        "estimate": "2\u20134 hours",
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
    """One admitted ticket, ready for work: a queued row whose statement has passed validation,
    and its open checkpoint. Returns both plus the id.

    The validation run is what lets these transitions reach `hold` at all — no task enters work
    on an unvalidated statement (Requirement 309 criterion 49). The reader half is a stub here;
    the mechanics it exercises are proven in `tests/test_statement_validation.py`.
    """
    plan, checkpoints = host(tmp_path)
    task_id = admission.admit(new_route(), plan, checkpoints)["task_id"]
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    reader = tmp_path / "reader.txt"
    reader.write_text(
        "What is to be done: a weekly digest reaches the test inbox\n"
        "Why: the people on the list get the week's news without asking\n"
        "How long: between two and four hours\n"
        "Echo-name placed: %s\n" % echo, encoding="utf-8")
    admission.validate(plan, task_id, reader=reader)
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
                      done="the fixture records one weekly message per subscriber",
                      source="the person, this turn",
                      reason="the list grew and one message for all of them is not the ask")
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


def verified(plan, checkpoints, task_id, cp):
    """Finished, and accepted by somebody other than the holder — what `close` now reads."""
    finished(plan, checkpoints, task_id, cp)
    admission.verify(plan, checkpoints, task_id, by="a second pair of eyes", commands=["true"])


def test_closing_closes_the_checkpoint_and_then_writes_the_mark(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    assert checkpoint.read_checkpoint(cp)["status"] == "closed"
    assert row_of(plan, task_id).startswith("### ✅ ")


def test_a_close_over_open_work_is_refused_and_the_mark_does_not_move(tmp_path):
    """The order is what this proves: the mark is the second write, so a checkpoint that
    cannot close leaves a ticket that is not marked done."""
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
    checkpoint.update_checkpoint(cp, next="the footer is still missing")
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "NEXT" in message
    assert checkpoint.read_checkpoint(cp)["status"] == "open"
    assert row_of(plan, task_id).startswith("### 🔄 ")


def test_a_second_close_over_a_closed_checkpoint_only_rewrites_the_mark(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    plan.write_text(plan.read_text(encoding="utf-8").replace("### ✅ ", "### 🔄 ", 1), encoding="utf-8")
    sheet = cp.read_bytes()
    admission.close(plan, checkpoints, task_id)
    assert cp.read_bytes() == sheet, "the re-run rewrote the checkpoint"
    assert row_of(plan, task_id).startswith("### ✅ ")


# --- T8, reopen --------------------------------------------------------------------------

def test_reopening_names_the_false_condition_and_never_writes_a_copy(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
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


def test_an_abandoned_row_can_be_taken_up_again(tmp_path):
    """T9 leaves the row queued in the list with its checkpoint closed. `hold` refused exactly
    that shape and named `reopen` as the door back, and `reopen` accepts only a done row — so no
    transition could move an abandoned row at all: a dead end reached by two legal moves (found
    2026-09-06 by the push review). The receipt kernel at `close` is where the bypass that
    refusal was guarding against is actually shut, and it runs unconditionally now."""
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the session", checkpoints_dir=checkpoints)
    admission.abandon(plan, checkpoints, task_id, "the channel it fed was retired")
    assert checkpoint.read_checkpoint(cp)["status"] == "closed"
    assert row_of(plan, task_id).startswith("### \u2b1c ")
    admission.hold(plan, task_id, "a second session", checkpoints_dir=checkpoints)
    assert checkpoint.read_checkpoint(cp)["status"] == "open", \
        "the abandoned row was taken up onto a checkpoint nobody reopened"
    assert row_of(plan, task_id).startswith("### \U0001f504 ")
    assert "Taken up again after the halt" in checkpoint.read_checkpoint(cp)["sections"]["NEXT"]


def test_a_done_row_is_still_refused_and_still_sent_to_reopen(tmp_path):
    """The arm above must not open the door T8 owns: a done row still comes back through
    `reopen`, which is the transition that records the false condition and its evidence."""
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    message = refused(admission.hold, plan, task_id, "a second session",
                      checkpoints_dir=checkpoints)
    assert "reopen" in message
    assert checkpoint.read_checkpoint(cp)["status"] == "closed"


def test_abandoning_without_a_reason_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the session")
    sheet = cp.read_bytes()
    message = refused(admission.abandon, plan, checkpoints, task_id, "   ")
    assert "reason" in message
    assert cp.read_bytes() == sheet


# --- the worker's brief ------------------------------------------------------------------

def with_keys(plan, *task_ids):
    """Give the host tree an acceptance table naming the rows — the pre-spawn gate's third leg."""
    scripts = plan.parent / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "plan_checks.py").write_text(
        "CHECKS = %r\n" % {t: "true" for t in task_ids}, encoding="utf-8")


def test_the_worker_brief_is_the_ticket_entry_plus_the_checkpoints_next_verbatim(tmp_path):
    """Diffed against the two sources themselves, read here independently of the emitter."""
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    with_keys(plan, task_id)
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
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
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
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
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

def test_reopening_a_ticket_with_no_checkpoint_opens_a_minimal_one(tmp_path):
    """Corrected 2026-09-06. This pinned a refusal until the adversarial read of that day: a row
    closed before checkpoints existed — q-822 on this project's own plan — then had no door into
    the kernel at all, because every other transition needs the checkpoint reopen was refusing to
    make. T8 still reopens the SAME id and never a copy; where there is no file to reopen it
    opens one, saying in its own header where the row came from."""
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    cp.unlink()
    admission.reopen(plan, checkpoints, task_id,
                     false_condition="the digest shipped", evidence="the inbox is empty")
    body = cp.read_text(encoding="utf-8")
    assert "opened at reopen" in body and "predates checkpoints" in body
    assert "Reopened: the done was false — the digest shipped; evidence: the inbox is empty" in body
    assert checkpoint.read_checkpoint(cp)["status"] == "open"
    assert row_of(plan, task_id).startswith("### 🔄 ")


# ---------------------------------------------------------------- the trusted closure kernel
# The definition of done is fixed at admission; changing it is its own explicit operation; the
# executor gives evidence and never the verdict; and the close reads a receipt rather than a
# claim. Every test below was red against the tree of 2026-09-06 before the kernel was built.


def repo(tmp_path):
    """A seeded ticket inside a real git tree — an acceptance receipt pins a real tree hash."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True, capture_output=True)
    return seeded(tmp_path)


def accepted(plan, checkpoints, task_id, cp, by="a second pair of eyes", commands=("true",),
             surfaces=()):
    admission.verify(plan, checkpoints, task_id, by=by, commands=list(commands),
                     surfaces=list(surfaces))


def test_admission_records_the_dods_own_text_and_hash(tmp_path):
    plan, checkpoints, task_id, _ = repo(tmp_path)
    row = row_of(plan, task_id)
    text, recorded = admission.read_dod(row)
    assert text == "the fixture records exactly one weekly message"
    assert recorded == admission.dod_digest(text)


def test_rewriting_the_done_without_a_source_and_a_reason_is_refused(tmp_path):
    plan, checkpoints, task_id, _ = repo(tmp_path)
    before = plan.read_bytes()
    message = refused(admission.correct, plan, checkpoints, task_id,
                      done="the fixture records at least one message")
    assert "--source" in message and "--reason" in message
    assert plan.read_bytes() == before


def test_correcting_the_done_keeps_the_previous_text_its_hash_the_source_and_the_reason(tmp_path):
    plan, checkpoints, task_id, _ = repo(tmp_path)
    old_text, old_hash = admission.read_dod(row_of(plan, task_id))
    admission.correct(plan, checkpoints, task_id,
                      done="the fixture records one weekly message per subscriber",
                      source="the person, 2026-09-06 10:12",
                      reason="the list grew and one message for all of them is not the ask")
    row = row_of(plan, task_id)
    assert old_text in row and old_hash in row
    assert "the person, 2026-09-06 10:12" in row
    assert "the list grew" in row
    text, recorded = admission.read_dod(row)
    assert text == "the fixture records one weekly message per subscriber"
    assert recorded == admission.dod_digest(text)


def test_a_close_over_a_silently_changed_done_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    accepted(plan, checkpoints, task_id, cp)
    plan.write_text(plan.read_text(encoding="utf-8").replace(
        "**Done when:** the fixture records exactly one weekly message",
        "**Done when:** the fixture runs"), encoding="utf-8")
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "definition of done" in message
    assert row_of(plan, task_id).startswith("### 🔄 ")


def test_the_producer_may_not_issue_its_own_acceptance_verdict(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    message = refused(admission.verify, plan, checkpoints, task_id,
                      by="the session", commands=["true"])
    assert "produced this work" in message
    assert "RECEIPT:" not in cp.read_text(encoding="utf-8")


def test_a_close_with_no_acceptance_receipt_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "receipt" in message
    assert checkpoint.read_checkpoint(cp)["status"] == "open"
    assert row_of(plan, task_id).startswith("### 🔄 ")


def test_a_receipt_whose_command_failed_is_a_failed_verdict(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    accepted(plan, checkpoints, task_id, cp, commands=["true", "false"])
    receipt = admission.read_receipt(cp)
    assert receipt["verdict"] == "failed" and receipt["checks"][1] == ["false", 1]
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "failed" in message
    assert row_of(plan, task_id).startswith("### 🔄 ")


def test_a_change_after_verification_voids_the_receipt(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    accepted(plan, checkpoints, task_id, cp)
    (tmp_path / "shipped.txt").write_text("one more edit\n", encoding="utf-8")
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "tree" in message
    assert row_of(plan, task_id).startswith("### 🔄 ")


def test_a_verified_and_unchanged_tree_closes(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    accepted(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    assert checkpoint.read_checkpoint(cp)["status"] == "closed"
    assert row_of(plan, task_id).startswith("### ✅ ")


def test_a_done_naming_a_rendered_surface_needs_the_surface_in_the_receipt(tmp_path):
    plan, checkpoints = host(tmp_path)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True, capture_output=True)
    task_id = admission.admit(
        new_route(done_when="the board page renders every row and is published at one link"),
        plan, checkpoints)["task_id"]
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    reader = tmp_path / "reader.txt"
    reader.write_text(
        "What is to be done: a weekly digest reaches the test inbox\n"
        "Why: the people on the list get the week's news without asking\n"
        "How long: between two and four hours\n"
        "Echo-name placed: %s\n" % echo, encoding="utf-8")
    admission.validate(plan, task_id, reader=reader)
    cp = checkpoints / (task_id + ".md")
    finished(plan, checkpoints, task_id, cp)
    message = refused(admission.verify, plan, checkpoints, task_id,
                      by="a second pair of eyes", commands=["true"])
    assert "--surface" in message
    assert "RECEIPT:" not in cp.read_text(encoding="utf-8")
    admission.verify(plan, checkpoints, task_id, by="a second pair of eyes",
                     commands=["true"], surfaces=["board.html"])
    assert admission.read_receipt(cp)["surfaces"] == ["board.html"]


def test_every_refusal_prints_a_plain_reason_exits_two_and_leaves_the_mark(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    run = subprocess.run(
        [sys.executable, str(SCRIPT), "close", task_id,
         "--plan", str(plan), "--checkpoints", str(checkpoints)],
        capture_output=True, text=True)
    assert run.returncode == 2, run.stdout + run.stderr
    assert "receipt" in run.stdout
    assert row_of(plan, task_id).startswith("### 🔄 ")


# --- the closure kernel holds past the checkpoint's own status ----------------------------

def test_an_abandoned_ticket_taken_back_up_still_cannot_close_without_a_receipt(tmp_path):
    """T9 closes the checkpoint, and the row taken up again over it must still meet the kernel.

    Red-proved 2026-09-06 against `scripts/task-admission.py` at 7993fa9b: `abandon` left the row
    marked ⬜ with a closed checkpoint, `hold` — which read only the mark — took it up again, and
    `close` then found a checkpoint that was not open, skipped every arm inside `if status ==
    "open"` and wrote ✅ with no receipt at all. The repair for that is at `close`, which now runs
    the whole kernel against the checkpoint's CONTENT unconditionally; this test holds that
    property end to end over the exact sequence that broke it.

    It first held the same property by refusing the second `hold` outright. That refusal named
    `reopen` as the door back and `reopen` accepts only a done row, so an abandoned row could be
    moved by no transition at all — a dead end the push review of 2026-09-06 reached in two legal
    moves. The take-up now reopens the sheet the halt left; the receipt is still the only way to ✅.
    """
    plan, checkpoints, task_id, cp = repo(tmp_path)
    admission.hold(plan, task_id, "the session", checkpoints_dir=checkpoints)
    admission.abandon(plan, checkpoints, task_id, "the channel it fed was retired")
    admission.hold(plan, task_id, "a second session", checkpoints_dir=checkpoints)
    assert checkpoint.read_checkpoint(cp)["status"] == "open"
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "no acceptance receipt" in message
    assert row_of(plan, task_id).startswith("### \U0001f504 "), \
        "a close with no receipt moved the mark"


def test_a_close_over_a_closed_checkpoint_that_carries_no_receipt_is_refused(tmp_path):
    """`close` is a transition against a receipt, whatever the checkpoint's status.

    Red-proved 2026-09-06 against `scripts/task-admission.py` at 7993fa9b: the whole receipt
    kernel — the receipt's presence, its verdict, the frozen done, the tree — sat inside `if the
    checkpoint is open`, so a row whose checkpoint had already been closed by any other
    transition took the ✅ mark with no evidence of any kind.
    """
    plan, checkpoints, task_id, cp = repo(tmp_path)
    admission.hold(plan, task_id, "the session", checkpoints_dir=checkpoints)
    checkpoint.update_checkpoint(cp, in_progress="(nothing)", next="(nothing)")
    checkpoint.close_checkpoint(cp)
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "receipt" in message
    assert row_of(plan, task_id).startswith("### 🔄 ")


def test_a_take_up_past_the_lane_cap_is_refused(tmp_path):
    """T2's own stated code requirement — "lane cap not exceeded" — and Requirement 309
    criterion 47, which bounds the steps running together by the same cap.

    Red-proved 2026-09-06 against `scripts/task-admission.py` at 7993fa9b, which read no cap at
    all: `hold --lanes 9` was accepted and wrote "lane decision runs 9" onto the trail, and a
    fourth row went in hand under a cap of three — more in-work rows than the board has lanes.
    """
    plan, checkpoints, task_id, cp = repo(tmp_path)
    profile = tmp_path / "profile.md"
    profile.write_text("lanes.cap: 2\n", encoding="utf-8")
    os.environ["LIVE_SPEC_PROFILE"] = str(profile)
    try:
        before = plan.read_bytes()
        message = refused(admission.hold, plan, task_id, "the session",
                          checkpoints_dir=checkpoints, lanes=9)
        assert "cap" in message and "2" in message
        assert plan.read_bytes() == before

        admission.hold(plan, task_id, "the session", checkpoints_dir=checkpoints, lanes=2)
        second = admission.admit(new_route(title="Send the monthly digest"), plan, checkpoints)
        third = admission.admit(new_route(title="Send the daily digest"), plan, checkpoints)
        for row in (second["task_id"], third["task_id"]):
            echo = admission.read_statement(row_of(plan, row))["echo"]
            reader = tmp_path / ("reader-%s.txt" % row)
            reader.write_text(
                "What is to be done: a digest reaches the test inbox\n"
                "Why: the people on the list get the news without asking\n"
                "How long: between two and four hours\n"
                "Echo-name placed: %s\n" % echo, encoding="utf-8")
            admission.validate(plan, row, reader=reader)
        admission.hold(plan, second["task_id"], "a second lane", checkpoints_dir=checkpoints)
        message = refused(admission.hold, plan, third["task_id"], "a third lane",
                          checkpoints_dir=checkpoints)
        assert "cap" in message
        assert row_of(plan, third["task_id"]).startswith("### ⬜ ")
    finally:
        os.environ.pop("LIVE_SPEC_PROFILE", None)


# ---------------------------------------------------------------- the kernel's own holes
# Four ways a row got past the kernel without meeting it, found by the adversarial read of
# 2026-09-06 against e65ae0ee. Every test below was red against that tree.


def pre_kernel(tmp_path):
    """A row shaped the way this project's own rows were before the kernel existed: its frozen
    scope written under `**Acceptance:**` rather than `**Done when:**`, and no `**DOD hash.**`
    line anywhere on it. q-816 stands in exactly this shape on the real plan."""
    plan, checkpoints, task_id, cp = repo(tmp_path)
    body = plan.read_text(encoding="utf-8").replace("**Done when:**", "**Acceptance:**")
    plan.write_text("\n\n".join(p for p in body.split("\n\n")
                                if not p.startswith("**DOD hash.**")), encoding="utf-8")
    return plan, checkpoints, task_id, cp


def test_a_close_over_a_row_whose_checkpoint_was_removed_is_refused(tmp_path):
    """Removing the checkpoint removed the whole kernel with it: the receipt, verdict, done-hash
    and tree checks all sat inside `if cp.exists():` while the ✅ mark was written regardless."""
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
    cp.unlink()
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "no checkpoint holds this row's receipt" in message
    assert row_of(plan, task_id).startswith("### 🔄 "), "the mark moved on a refused close"


def test_a_frozen_acceptance_stands_as_the_done_when_the_row_carries_no_done_when(tmp_path):
    """`read_dod` looked only for `**Done when:**`, so a pre-kernel row hashed the empty string:
    the hash comparison compared nothing and the surface guard had no text to fire on."""
    plan, checkpoints, task_id, cp = pre_kernel(tmp_path)
    text, recorded = admission.read_dod(row_of(plan, task_id))
    assert text == "the fixture records exactly one weekly message"
    assert admission.dod_digest(text) != admission.dod_digest("")
    assert recorded is None


def test_a_surface_naming_acceptance_is_held_to_the_surface_rule(tmp_path):
    plan, checkpoints = host(tmp_path)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True, capture_output=True)
    task_id = admission.admit(
        new_route(done_when="the board page renders every row and is published at one link"),
        plan, checkpoints)["task_id"]
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    reader = tmp_path / "reader.txt"
    reader.write_text(
        "What is to be done: a weekly digest reaches the test inbox\n"
        "Why: the people on the list get the week's news without asking\n"
        "How long: between two and four hours\n"
        "Echo-name placed: %s\n" % echo, encoding="utf-8")
    admission.validate(plan, task_id, reader=reader)
    body = plan.read_text(encoding="utf-8").replace("**Done when:**", "**Acceptance:**")
    plan.write_text("\n\n".join(p for p in body.split("\n\n")
                                if not p.startswith("**DOD hash.**")), encoding="utf-8")
    cp = checkpoints / (task_id + ".md")
    finished(plan, checkpoints, task_id, cp)
    message = refused(admission.verify, plan, checkpoints, task_id,
                      by="a second pair of eyes", commands=["true"])
    assert "--surface" in message
    assert "RECEIPT:" not in cp.read_text(encoding="utf-8")


def test_verify_records_the_hash_of_a_row_that_predates_the_kernel(tmp_path):
    """`if recorded and ...` skipped the comparison silently on a row that carries no hash. The
    first verification writes one, so from then on there is something real to compare."""
    plan, checkpoints, task_id, cp = pre_kernel(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    admission.verify(plan, checkpoints, task_id, by="a second pair of eyes", commands=["true"])
    row = row_of(plan, task_id)
    text, recorded = admission.read_dod(row)
    assert recorded == admission.dod_digest(text)
    assert "recorded at first verification" in row and "predates the kernel" in row


def test_a_close_over_a_row_with_no_recorded_hash_is_refused(tmp_path):
    plan, checkpoints, task_id, cp = pre_kernel(tmp_path)
    verified(plan, checkpoints, task_id, cp)
    body = plan.read_text(encoding="utf-8")
    plan.write_text("\n\n".join(p for p in body.split("\n\n")
                                if not p.startswith("**DOD hash.**")), encoding="utf-8")
    message = refused(admission.close, plan, checkpoints, task_id)
    assert "no recorded hash" in message
    assert row_of(plan, task_id).startswith("### 🔄 ")


# --- the pre-spawn gate (the tlvphotos defect, 2026-09-06) ------------------------------
# Red-proved against the brief as it stood: a row with no acceptance table was briefed, and a
# missing id raised a bare span error rather than the gate's own reason.

def test_no_brief_without_a_task_id(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    with pytest.raises(admission.AdmissionError, match="no worker or subagent starts before an admitted row"):
        admission.worker_brief(plan, checkpoints, "")


def test_no_brief_for_a_row_the_board_does_not_hold(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    with pytest.raises(admission.AdmissionError, match="a report or a row written after the work is not admission"):
        admission.worker_brief(plan, checkpoints, "q-999")


def test_no_brief_for_a_row_with_no_acceptance_command(tmp_path):
    plan, checkpoints, task_id, cp = seeded(tmp_path)
    admission.hold(plan, task_id, "the worker")
    with pytest.raises(admission.AdmissionError, match="carries no acceptance command"):
        admission.worker_brief(plan, checkpoints, task_id)
    with_keys(plan, task_id)
    assert task_id in admission.worker_brief(plan, checkpoints, task_id)


# --- T8 → verify → T7 is a road, not a dead end (found 2026-09-06 by the verifier) ---------

def test_a_reopened_row_verified_again_closes_without_a_hand_touching_next(tmp_path):
    plan, checkpoints, task_id, cp = repo(tmp_path)
    verified(plan, checkpoints, task_id, cp)
    admission.close(plan, checkpoints, task_id)
    admission.reopen(plan, checkpoints, task_id, "the done was read as met on a report", "the receipt was missing")
    assert "Reopened:" in checkpoint.read_checkpoint(cp)["sections"]["NEXT"]
    admission.verify(plan, checkpoints, task_id, by="a second pair of eyes", commands=["true"])
    admission.close(plan, checkpoints, task_id)
    data = checkpoint.read_checkpoint(cp)
    assert data["status"] == "closed"
    assert "settled by the receipt" in data["sections"]["DONE"]


def test_the_verifiers_own_check_may_spawn_the_probe(tmp_path):
    """The re-entry breaker binds acceptance keys inside a reader, never the verifier's checks."""
    plan, checkpoints, task_id, cp = repo(tmp_path)
    finished(plan, checkpoints, task_id, cp)
    admission.verify(plan, checkpoints, task_id, by="a second pair of eyes",
                     commands=["test -z \"$LIVE_SPEC_EVALUATING\""])
    receipt = [ln for ln in cp.read_text(encoding="utf-8").splitlines() if ln.startswith("RECEIPT:")][-1]
    assert '"verdict": "passed"' in receipt
