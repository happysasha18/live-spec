"""A task enters work only through a validated statement — matrix rows M-531 to M-535.

Requirement 309 criteria 41 to 62 put a statement on every task (echo-name, description, plan,
estimate), gate entry into work on that statement passing a mechanical floor and a clean-context
reader, freeze the wording at take-up, and read the plan's parallel mark against the lane decision
the take-up actually makes. Criteria 63 to 67 stand the actual beside the estimate at the close.

Every test here was red before `scripts/task-admission.py` grew the statement half: run against the
file as it stood at 4a1579d0, each one fails at the missing name it calls.
"""

import datetime
import importlib.util
import subprocess
import sys
from pathlib import Path

from conftest import ROOT

SCRIPT = Path(ROOT) / "scripts" / "task-admission.py"
sys.path.insert(0, str(SCRIPT.parent))
_spec = importlib.util.spec_from_file_location("task_admission", SCRIPT)
admission = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(admission)

import checkpoint  # noqa: E402


TODAY = datetime.date.today().isoformat()


def host(tmp_path):
    plan = tmp_path / "PLAN.md"
    plan.write_text("# Host plan\n\n## Tasks\n\n## Blockers\n\nNone.\n", encoding="utf-8")
    # A real git tree: an acceptance receipt pins the tree it was written against, and `close`
    # reads that receipt rather than any agent's claim. The host's own acceptance table goes
    # beside it, because a verifier runs the command the TREE recorded for the row.
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True, capture_output=True)
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / "scripts" / "plan_checks.py").write_text(
        "CHECKS = {'q-%d' % n: 'true' for n in range(1, 40)}\n", encoding="utf-8")
    return plan, tmp_path / ".live-spec" / "checkpoints"


def accepted_close(plan, checkpoints, task_id):
    """Take the row up, accept it by somebody other than its holder, and close it."""
    cp = checkpoints / (task_id + ".md")
    if not admission._holder(row_of(plan, task_id)):
        admission.hold(plan, task_id, "the session", checkpoints_dir=checkpoints)
    checkpoint.update_checkpoint(cp, in_progress="(nothing)", next="(nothing)")
    admission.verify(plan, checkpoints, task_id, by="a second pair of eyes", commands=["true"])
    admission.close(plan, checkpoints, task_id)


def new_route(**overrides):
    route = {
        "action": "new", "creates_work": True, "existing_task": None,
        "title": "Send the weekly digest", "project": "route-host", "scope": "Reports",
        "source": {"kind": "person", "detail": "the person, this turn"},
        "observable_outcome": "a weekly digest reaches the test inbox",
        "done_when": "the digest job runs on schedule; the fixture records exactly one message",
        "verification": "python3 tests/test_digest.py",
        "context_pointers": ["`scripts/digest.py`", "R-104"],
        "estimate": "2–4 hours",
    }
    route.update(overrides)
    return route


def row_of(plan, task_id):
    body = plan.read_text(encoding="utf-8")
    start = body.index("### ")
    while "— id: %s" % task_id not in body[start:body.index("\n", start)]:
        start = body.index("\n### ", start) + 1
    end = body.find("\n### ", start)
    if end == -1:
        end = body.find("\n## ", start)
    return body[start:end if end != -1 else len(body)]


def reader_record(tmp_path, echo, **overrides):
    """A stub standing in for the fresh reader's own answers. The mechanics are what is proven
    here; who writes the file is the pipeline skill's own sentence, and q-816's backfill is the
    one run made against a real fresh reader."""
    fields = {
        "What is to be done": "a weekly digest is sent and the test inbox records one message",
        "Why": "so the people on the list get the week's news without asking for it",
        "How long": "between two and four hours",
        "Echo-name placed": echo,
    }
    fields.update(overrides)
    path = tmp_path / "reader.txt"
    path.write_text(
        "\n".join("%s: %s" % (k, v) for k, v in fields.items() if v is not None) + "\n",
        encoding="utf-8")
    return path


def admitted(tmp_path, **overrides):
    plan, checkpoints = host(tmp_path)
    task_id = admission.admit(new_route(**overrides), plan, checkpoints)["task_id"]
    return plan, checkpoints, task_id, checkpoints / (task_id + ".md")


def refused(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except admission.AdmissionError as exc:
        return str(exc)
    raise AssertionError("the illegal move was not refused")


# --- M-531: the statement, its four fields, and its one home -----------------------------

def test_m531_a_statement_holds_its_four_fields_in_the_rows_own_entry(tmp_path):
    """Criteria 41, 42: echo-name, description, plan and estimate, kept in the queue row's own
    entry keyed by its id — no second store, and the five cells the row already had stay."""
    plan, checkpoints, task_id, cp = admitted(tmp_path)
    row = row_of(plan, task_id)
    assert "**Statement.**" in row
    statement = admission.read_statement(row)
    assert len(statement["echo"].split()) >= 2
    assert statement["description"]
    assert statement["steps"] and statement["basis"]
    assert statement["low"] and statement["high"] and statement["unit"]
    for cell in ("**Group:**", "**Source:**", "**Outcome:**", "**Done when:**",
                 "**Verification:**"):
        assert cell in row, "the queue row lost a cell it already had"
    # One store: the statement is in the plan and in no second file.
    assert "**Statement.**" not in cp.read_text(encoding="utf-8")
    assert sorted(p.name for p in checkpoints.iterdir()) == [task_id + ".md"]
    assert not list(tmp_path.glob("board.json"))


def test_a_route_that_can_yield_no_estimate_is_refused(tmp_path):
    """No invented default: with no comparable closed row in the tree and no estimate on the
    route, admission refuses rather than writing a number nobody stands behind."""
    plan, checkpoints = host(tmp_path)
    route = new_route()
    del route["estimate"]
    message = refused(admission.admit, route, plan, checkpoints)
    assert "estimate" in message
    assert "— id:" not in plan.read_text(encoding="utf-8")


def test_the_estimates_basis_names_the_closed_rows_it_rests_on(tmp_path):
    """Where the tree does carry comparable closed work, the basis names those rows and their
    own checkpoint stamps rather than saying there is no history."""
    plan, checkpoints = host(tmp_path)
    older = admission.admit(new_route(title="Send the monthly digest"), plan, checkpoints)
    echo = admission.read_statement(row_of(plan, older["task_id"]))["echo"]
    admission.validate(plan, older["task_id"], reader=reader_record(tmp_path, echo))
    accepted_close(plan, checkpoints, older["task_id"])
    task_id = admission.admit(new_route(), plan, checkpoints)["task_id"]
    statement = admission.read_statement(row_of(plan, task_id))
    assert older["task_id"] in statement["basis"]
    assert "no comparable history" not in statement["basis"]


def test_with_no_comparable_history_the_basis_says_so_in_those_words(tmp_path):
    plan, _, task_id, _ = admitted(tmp_path)
    assert "no comparable history in this tree" in \
        admission.read_statement(row_of(plan, task_id))["basis"]


# --- M-532: no task enters work before its statement passes validation -------------------

def test_m532_no_task_enters_work_before_its_statement_passes_validation(tmp_path):
    """Criteria 49, 50, 55: the floor, then the clean-context reader, then the row may be taken
    up — and not one step earlier."""
    plan, checkpoints, task_id, _ = admitted(tmp_path)
    message = refused(admission.hold, plan, task_id, "the session")
    assert "validation" in message
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    result = admission.validate(plan, task_id, reader=reader_record(tmp_path, echo))
    assert result["status"] == "ready"
    admission.hold(plan, task_id, "the session")
    assert "\U0001f504" in row_of(plan, task_id).splitlines()[0]


def test_m532_a_statement_that_fails_the_floor_is_rewritten_and_stays_out_of_work(tmp_path):
    """Criterion 53: a failed statement is rewritten and validated again, its task staying out
    of work until it passes."""
    plan, checkpoints, task_id, _ = admitted(tmp_path)
    admission._rewrite_row(plan, task_id, edits=[
        ("**Statement.**", "Echo-name: Send the weekly digest. Description: a digest goes out. "
                           "Plan: 1) build it. Estimate:  — basis: none.")])
    result = admission.validate(plan, task_id)
    assert result["status"] == "rewritten"
    assert "floor: failed" in row_of(plan, task_id)
    assert "validation" in refused(admission.hold, plan, task_id, "the session")


def test_a_reader_record_missing_an_answer_fails_the_statement(tmp_path):
    plan, _, task_id, _ = admitted(tmp_path)
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    record = reader_record(tmp_path, echo, **{"How long": None})
    result = admission.validate(plan, task_id, reader=record)
    assert result["status"] == "rewritten"
    assert "reader: failed" in row_of(plan, task_id)


def test_a_question_the_reader_cannot_answer_fails_the_statement(tmp_path):
    """Criterion 50's own clause, and the one this row's real reader run caught: the first
    statement written for q-816 said what and how long but never why, and the fresh reader
    answered "cannot tell from this". A record carrying that answer is a failed validation, not
    a complete one."""
    plan, _, task_id, _ = admitted(tmp_path)
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    record = reader_record(tmp_path, echo, Why="cannot tell from this")
    result = admission.validate(plan, task_id, reader=record)
    assert result["status"] == "rewritten"
    assert "reader: failed" in row_of(plan, task_id)


def test_a_reader_that_places_a_different_name_fails_the_statement(tmp_path):
    """Criterion 52: shown the echo-name alone, the reader names which change the task is."""
    plan, _, task_id, _ = admitted(tmp_path)
    result = admission.validate(
        plan, task_id, reader=reader_record(tmp_path, "some other piece of work"))
    assert result["status"] == "rewritten"
    row = row_of(plan, task_id)
    assert "echo-name placed: no" in row and "reader: failed" in row


def test_a_row_with_no_statement_at_all_fails_the_floor(tmp_path):
    plan, checkpoints = host(tmp_path)
    plan.write_text(plan.read_text(encoding="utf-8").replace(
        "## Tasks\n", "## Tasks\n\n### ⬜ A bare row — id: q-9\n\n**Outcome:** none.\n"),
        encoding="utf-8")
    assert admission.validate(plan, "q-9")["status"] == "rewritten"
    assert "validation" in refused(admission.hold, plan, "q-9", "the session")


# --- M-533: a passed validation is the ready state ---------------------------------------

def test_m533_a_passed_validation_writes_the_dated_ready_state(tmp_path):
    """Criteria 54, 55: the pass is the approval and it writes the row's ready state, dated."""
    plan, _, task_id, _ = admitted(tmp_path)
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    admission.validate(plan, task_id, reader=reader_record(tmp_path, echo))
    row = row_of(plan, task_id)
    assert "**Validation.**" in row
    record = admission.read_validation(row)
    assert record["status"] == "ready"
    assert record["date"] == TODAY
    assert record["floor"] == "passed" and record["reader"] == "passed"
    assert "⬜" in row.splitlines()[0], "validation is not a status mark of its own"


# --- M-534: the wording freezes at take-up -----------------------------------------------

def ready(tmp_path):
    plan, checkpoints, task_id, cp = admitted(tmp_path)
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    admission.validate(plan, task_id, reader=reader_record(tmp_path, echo))
    return plan, checkpoints, task_id, cp


def test_m534_the_wording_freezes_at_take_up_and_a_later_change_is_refused(tmp_path):
    """Criteria 58 to 62: take-up freezes the wording; a change after it is refused, and the
    refusal names the frozen statement."""
    plan, checkpoints, task_id, _ = ready(tmp_path)
    admission.hold(plan, task_id, "the session")
    row = row_of(plan, task_id)
    assert "**Frozen at take-up %s.**" % TODAY in row
    message = refused(admission.correct, plan, checkpoints, task_id, goal="something else")
    assert "frozen" in message.lower()
    assert admission.read_statement(row_of(plan, task_id))["echo"] in message


def test_m534_a_change_before_take_up_sends_the_statement_back_through_validation(tmp_path):
    """Criterion 61: a revision before take-up runs validation again — so the ready state goes."""
    plan, checkpoints, task_id, _ = ready(tmp_path)
    admission.correct(plan, checkpoints, task_id,
                      statement="Echo-name: Send the fortnightly digest. Description: a digest "
                                "reaches the test inbox every second week. Plan: 1) build the "
                                "job 2) record the message. Estimate: 2–4 hours — "
                                "basis: no comparable history in this tree; the range is read "
                                "off the plan's steps.")
    row = row_of(plan, task_id)
    assert "**Validation.**" not in row, "a rewritten statement kept its old validation"
    assert "fortnightly" in row
    assert "validation" in refused(admission.hold, plan, task_id, "the session")


def test_a_correction_that_leaves_the_statement_alone_keeps_the_ready_state(tmp_path):
    plan, checkpoints, task_id, _ = ready(tmp_path)
    admission.correct(plan, checkpoints, task_id, done="the fixture records one message",
                      source="the person, this turn", reason="one message is the real ask")
    assert admission.read_validation(row_of(plan, task_id))["status"] == "ready"


# --- M-535: the plan's expected parallel steps against the lane decision ------------------

def test_m535_the_plans_expected_parallel_steps_meet_the_lane_decision_at_take_up(tmp_path):
    """Criterion 46: the parallel mark is the plan's expectation, the take-up lane decision
    decides what actually runs, and a divergence is recorded plainly."""
    plan, checkpoints, task_id, cp = ready(tmp_path)
    admission.correct(plan, checkpoints, task_id,
                      statement="Echo-name: Send the weekly digest. Description: a weekly digest "
                                "reaches the test inbox. Plan: 1) build the job ∥ 2) write "
                                "the fixture 3) record the message. Estimate: 2–4 hours "
                                "— basis: no comparable history in this tree; the range is "
                                "read off the plan's steps.")
    echo = admission.read_statement(row_of(plan, task_id))["echo"]
    admission.validate(plan, task_id, reader=reader_record(tmp_path, echo))
    admission.hold(plan, task_id, "the session", checkpoints_dir=checkpoints, lanes=1)
    trail = checkpoint.read_checkpoint(cp)["sections"]["DONE"]
    lanes = [ln for ln in trail.splitlines() if ln.startswith("LANES:")]
    assert len(lanes) == 1, "the lane decision is not on the trail the close writes into"
    assert "plan expects 2 steps side by side" in lanes[0]
    assert "lane decision runs 1" in lanes[0]
    assert "divergence:" in lanes[0] and "none" not in lanes[0].split("divergence:")[1]
    # A close refuses over a non-empty IN PROGRESS, so the lane decision must not sit there.
    assert "LANES:" not in checkpoint.read_checkpoint(cp)["sections"]["IN PROGRESS"]


def test_m535_the_divergence_and_the_given_against_the_actual_land_in_the_trail(tmp_path):
    """Criteria 46, 63 to 65: the close carries the estimate beside the actual and the lane
    divergence into the delivery trail."""
    plan, checkpoints, task_id, cp = ready(tmp_path)
    admission.hold(plan, task_id, "the session", checkpoints_dir=checkpoints, lanes=2)
    accepted_close(plan, checkpoints, task_id)
    done = checkpoint.read_checkpoint(cp)["sections"]["DONE"]
    assert "estimate 2–4 hours → actual" in done
    assert "divergence: the plan expected 1 side by side and the lane decision runs 2" in done
    assert checkpoint.read_checkpoint(cp)["status"] == "closed", \
        "the lane decision written at take-up blocked the close"


def test_a_plan_whose_steps_run_out_of_order_fails_the_floor(tmp_path):
    """Criterion 43: the plan lists the steps in the order they run."""
    plan, checkpoints, task_id, _ = admitted(tmp_path)
    admission._rewrite_row(plan, task_id, edits=[
        ("**Statement.**", "Echo-name: Send the weekly digest. Description: a digest reaches the "
                           "test inbox. Plan: 2) record it 1) build it. Estimate: 2–4 hours "
                           "— basis: no comparable history in this tree; the range is read "
                           "off the plan's steps.")])
    result = admission.validate(plan, task_id)
    assert result["status"] == "rewritten"
    assert "order" in " ".join(result["floor"])


def test_taking_up_with_no_lane_decision_records_none(tmp_path):
    """The lane decision is what take-up was given; with none named the line says so rather
    than inventing a number."""
    plan, checkpoints, task_id, cp = ready(tmp_path)
    admission.hold(plan, task_id, "the session", checkpoints_dir=checkpoints)
    assert "lane decision runs 1" in cp.read_text(encoding="utf-8")


# --- M-649, M-650: what a plan's deliverables may be, and how many ------------------------

def _statement(plan_text):
    return ("Echo-name: Send the weekly digest. Description: a digest reaches the test inbox. "
            "Plan: %s. Estimate: 2–4 hours — basis: no comparable history in this tree; the "
            "range is read off the plan's steps." % plan_text)


def test_m649_an_activity_that_only_carries_value_alongside_others_is_not_a_deliverable(tmp_path):
    """Criterion 44: writing the tests is the criterion's own example — it carries value only
    beside the deliverable it tests, so it is not a slice that shows value on its own."""
    plan, checkpoints, task_id, _ = admitted(tmp_path)
    admission._rewrite_row(plan, task_id, edits=[
        ("**Statement.**", _statement("1) build the digest 2) write the tests for it"))])
    result = admission.validate(plan, task_id)
    assert result["status"] == "rewritten"
    assert ("an activity that carries value only alongside others — writing the tests, say — "
            "stays outside a plan's deliverables") in result["floor"]


def test_m649_a_plan_whose_every_deliverable_stands_on_its_own_passes_the_floor(tmp_path):
    plan, checkpoints, task_id, _ = admitted(tmp_path)
    admission._rewrite_row(plan, task_id, edits=[
        ("**Statement.**", _statement("1) build the digest 2) send it to the list"))])
    assert admission.floor_issues(row_of(plan, task_id)) == []


def test_m650_a_plans_deliverables_stay_a_handful(tmp_path):
    """Criterion 45 and its own sub-item: the most deliverables one plan holds stands at five.
    The number is the spec's, not this file's."""
    plan, checkpoints, task_id, _ = admitted(tmp_path)
    five = " ".join("%d) slice %d" % (n, n) for n in range(1, 6))
    admission._rewrite_row(plan, task_id, edits=[("**Statement.**", _statement(five))])
    assert admission.floor_issues(row_of(plan, task_id)) == []
    six = " ".join("%d) slice %d" % (n, n) for n in range(1, 7))
    admission._rewrite_row(plan, task_id, edits=[("**Statement.**", _statement(six))])
    result = admission.validate(plan, task_id)
    assert result["status"] == "rewritten"
    assert "a plan's deliverables stay a handful: at most five" in result["floor"]


def test_the_readers_answers_are_kept_in_the_checkpoint_as_evidence(tmp_path):
    """A Validation line says a reader passed; the four answers themselves are the evidence."""
    from test_task_admission import repo, admission, checkpoint
    plan, checkpoints, task_id, cp = repo(tmp_path)
    reader = tmp_path / "reader.txt"
    reader.write_text("What is to be done: send the weekly digest\nWhy: the readers asked for one\n"
                      "How long: 2-4 hours\nEcho-name placed: %s\n" % admission.read_statement(
                          admission.row_of(plan, task_id) if hasattr(admission, "row_of") else
                          __import__("test_task_admission").row_of(plan, task_id))["echo"],
                      encoding="utf-8")
    admission.validate(plan, task_id, reader=str(reader), checkpoints_dir=checkpoints)
    done = checkpoint.read_checkpoint(cp)["sections"]["DONE"]
    assert "READER " in done and "Why: the readers asked for one" in done


# --- criteria 63-65: the actual is a recorded datum, not a filesystem stamp ----------------

def test_the_close_reads_the_actual_off_the_recorded_open_time(tmp_path):
    """Every checkpoint write goes through `write_atomic`, which renames a fresh file over the
    old one — so the file's creation stamp is the stamp of the LAST write, and the span between
    it and the modification stamp is zero however long the work took. Read that way the close
    settled `actual 0.0 hours` against every estimate, and the three rows closed on 2026-09-06
    each shipped that number. The open time is recorded when the ticket is admitted and read
    back here."""
    plan, checkpoints, task_id, cp = ready(tmp_path)
    opened = [ln for ln in checkpoint.read_checkpoint(cp)["sections"]["DONE"].splitlines()
              if ln.startswith("OPENED: ")]
    assert opened, "admission recorded no open time on the checkpoint"
    # Two hours ago, written the way any transition writes it — through the atomic replace.
    was = (datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat(timespec="seconds")
    body = checkpoint.read_checkpoint(cp)["sections"]["DONE"].replace(
        opened[0], "OPENED: " + was)
    checkpoint.update_checkpoint(cp, done=body)
    st = cp.stat()
    assert abs(st.st_mtime - getattr(st, "st_birthtime", st.st_ctime)) < 1.0, \
        "the file's own stamps span a duration, so this test is not measuring what it claims"
    accepted_close(plan, checkpoints, task_id)
    trail = [ln for ln in checkpoint.read_checkpoint(cp)["sections"]["DONE"].splitlines()
             if ln.startswith("estimate ")]
    assert trail and "actual 2.0 hours" in trail[0], trail


def test_a_close_with_no_recorded_open_time_says_so_instead_of_printing_zero(tmp_path):
    """A row whose checkpoint predates the recording — q-822's, opened by `reopen` — has no
    duration to read, and the pack's own rule is to say so rather than print a number nobody
    wrote."""
    plan, checkpoints, task_id, cp = ready(tmp_path)
    body = "\n".join(ln for ln in checkpoint.read_checkpoint(cp)["sections"]["DONE"].splitlines()
                     if not ln.startswith("OPENED: "))
    checkpoint.update_checkpoint(cp, done=body or "(nothing yet)")
    accepted_close(plan, checkpoints, task_id)
    trail = [ln for ln in checkpoint.read_checkpoint(cp)["sections"]["DONE"].splitlines()
             if ln.startswith("estimate ")]
    assert trail and "actual not recorded" in trail[0], trail
