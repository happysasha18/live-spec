"""An inbox letter carries its own state (PLAN q-835).

Before this, a letter's state was guessed: its position (inbox/ open, inbox/handled/ done) plus a
prose section eight of the eleven archived letters never wrote. This proves the one reader,
`scripts/inbox_lifecycle.py`, and its two callers — admission (a route naming the letter it came
from records it on the row) and `scripts/state-probe.sh` (the INBOX block and a row's own printed
line).

Every fixture here is a throwaway tree in `tmp_path`; nothing touches this repository's own
`inbox/`, except the read-only proof that the eleven letters already on record still read (no
letter here is ever written to).
"""
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import ROOT

ROOT = Path(ROOT)

SCRIPT = ROOT / "scripts" / "task-admission.py"
sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location("task_admission", SCRIPT)
admission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admission)

import inbox_lifecycle  # noqa: E402 — the module under test, loaded off the real sys.path above


# ---------------------------------------------------------------- the reader itself


def letter(root: Path, name: str, body: str = "content\n", handled: bool = False) -> Path:
    folder = root / "handled" if handled else root
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_text(body, encoding="utf-8")
    return path


def plain_lines(stdout, starts_with):
    """The probe's own lines with their colour stripped, kept where one opens with `starts_with`.

    The probe colours every line, so a bare substring test over the raw output picks up whichever
    line happens to mention the same words — which is how two shapes of the link assertion came to
    read the plan row instead of the letter's own.
    """
    plain = [re.sub(r"\033\[[0-9;]*m", "", ln).strip() for ln in stdout.splitlines()]
    return [ln for ln in plain if ln.startswith(starts_with)]


def test_a_letter_with_no_status_line_reads_open_where_it_stands_in_the_inbox(tmp_path):
    letter(tmp_path, "a.md", "# A wish\n\nplain prose, no Status line.\n")
    info = inbox_lifecycle.read_state(tmp_path, "a.md")
    assert info["state"] == inbox_lifecycle.OPEN
    assert info["superseded_by"] is None


def test_a_letter_with_no_status_line_reads_handled_where_it_stands_in_the_archive(tmp_path):
    letter(tmp_path, "a.md", "# A wish, already archived\n", handled=True)
    info = inbox_lifecycle.read_state(tmp_path, "a.md")
    assert info["state"] == inbox_lifecycle.HANDLED


def test_a_letters_own_status_line_is_read_over_its_position(tmp_path):
    # Sitting under inbox/ (which reads OPEN with no line at all) but its own line says noted.
    letter(tmp_path, "a.md", "# A wish\n\nStatus: noted\n")
    assert inbox_lifecycle.read_state(tmp_path, "a.md")["state"] == inbox_lifecycle.NOTED


def test_a_superseded_letter_names_a_successor_that_is_on_disk(tmp_path):
    letter(tmp_path, "b.md", "successor\n")
    letter(tmp_path, "a.md", "# A wish\n\nStatus: superseded\nSuperseded-by: b.md\n")
    info = inbox_lifecycle.read_state(tmp_path, "a.md")
    assert info["state"] == inbox_lifecycle.SUPERSEDED
    assert info["superseded_by"] == "b.md"


def test_a_superseded_letter_with_no_successor_named_is_refused(tmp_path):
    letter(tmp_path, "a.md", "# A wish\n\nStatus: superseded\n")
    with pytest.raises(inbox_lifecycle.InboxLifecycleError, match="no Superseded-by"):
        inbox_lifecycle.read_state(tmp_path, "a.md")


def test_a_superseded_letter_naming_a_successor_off_disk_is_refused(tmp_path):
    letter(tmp_path, "a.md", "# A wish\n\nStatus: superseded\nSuperseded-by: ghost.md\n")
    with pytest.raises(inbox_lifecycle.InboxLifecycleError, match="ghost.md"):
        inbox_lifecycle.read_state(tmp_path, "a.md")


def test_an_unknown_state_word_is_refused_naming_the_four(tmp_path):
    letter(tmp_path, "a.md", "# A wish\n\nStatus: cancelled\n")
    message = ""
    try:
        inbox_lifecycle.read_state(tmp_path, "a.md")
    except inbox_lifecycle.InboxLifecycleError as exc:
        message = str(exc)
    for word in ("open", "handled", "noted", "superseded"):
        assert word in message, message


def test_a_letter_named_that_is_not_on_disk_is_refused(tmp_path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    with pytest.raises(inbox_lifecycle.InboxLifecycleError, match="not on disk"):
        inbox_lifecycle.read_state(tmp_path, "nothing-here.md")


def test_find_letter_looks_in_both_the_root_and_its_handled_folder(tmp_path):
    letter(tmp_path, "open.md", handled=False)
    letter(tmp_path, "closed.md", handled=True)
    assert inbox_lifecycle.find_letter(tmp_path, "open.md") == tmp_path / "open.md"
    assert inbox_lifecycle.find_letter(tmp_path, "closed.md") == tmp_path / "handled" / "closed.md"
    assert inbox_lifecycle.find_letter(tmp_path, "nowhere.md") is None


def test_every_letter_already_on_this_projects_own_record_still_reads(tmp_path):
    """The eleven letters this project already carries write no Status line — read-only here,
    against the real inbox/, so building this reader never asks anyone to touch them."""
    real_inbox = ROOT / "inbox"
    for path in sorted(real_inbox.glob("*.md")):
        info = inbox_lifecycle.read_state(real_inbox, path.name)
        assert info["state"] == inbox_lifecycle.OPEN
    for path in sorted((real_inbox / "handled").glob("*.md")):
        info = inbox_lifecycle.read_state(real_inbox, path.name)
        assert info["state"] == inbox_lifecycle.HANDLED


# ---------------------------------------------------------------- admission records the letter


def host(tmp_path, key="true"):
    plan = tmp_path / "PLAN.md"
    plan.write_text("# Host plan\n\n## Tasks\n\n## Blockers\n\nNone.\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / "scripts" / "plan_checks.py").write_text(
        "CHECKS = {'q-%%d' %% n: %r for n in range(1, 40)}\n" % key, encoding="utf-8")
    return plan, tmp_path / ".live-spec" / "checkpoints"


def new_route(**overrides):
    route = {
        "action": "new", "creates_work": True, "existing_task": None,
        "title": "Read the incoming letter", "project": "route-host", "scope": "Reports",
        "source": {"kind": "person", "detail": "the person, this turn"},
        "observable_outcome": "the letter's wish is met",
        "done_when": "the fixture records exactly one weekly message",
        "verification": "python3 tests/test_digest.py",
        "context_pointers": ["`scripts/digest.py`"],
        "estimate": "2–4 hours",
        "prior_record": {"read": [], "finding": "nothing on this host's record covers this"},
    }
    route.update(overrides)
    return route


def row_of(plan_path, task_id):
    body = plan_path.read_text(encoding="utf-8")
    start = body.index("### ")
    while "— id: %s" % task_id not in body[start:body.index("\n", start)]:
        start = body.index("\n### ", start) + 1
    end = body.find("\n### ", start)
    return body[start:end if end != -1 else len(body)]


def test_a_route_naming_no_letter_admits_exactly_as_before(tmp_path):
    plan, checkpoints = host(tmp_path)
    task_id = admission.admit(new_route(), plan, checkpoints)["task_id"]
    assert "**Source inbox.**" not in row_of(plan, task_id)


def test_a_route_naming_a_real_letter_records_it_on_the_row(tmp_path):
    plan, checkpoints = host(tmp_path)
    letter(tmp_path / "inbox", "2026-09-09-from-owner-wish.md", "the wish\n")
    route = new_route(source={"kind": "person", "detail": "the owner",
                              "inbox": "2026-09-09-from-owner-wish.md"})
    task_id = admission.admit(route, plan, checkpoints)["task_id"]
    row = row_of(plan, task_id)
    assert "**Source inbox.** 2026-09-09-from-owner-wish.md" in row


def test_a_route_naming_a_letter_off_disk_is_refused(tmp_path):
    plan, checkpoints = host(tmp_path)
    before = plan.read_bytes()
    route = new_route(source={"kind": "person", "detail": "the owner",
                              "inbox": "2026-09-09-from-owner-ghost.md"})
    try:
        admission.admit(route, plan, checkpoints)
    except admission.AdmissionError as exc:
        assert "2026-09-09-from-owner-ghost.md" in str(exc)
        assert "not on disk" in str(exc)
    else:
        raise AssertionError("a route naming a letter that does not exist was admitted")
    assert plan.read_bytes() == before


def test_the_rows_own_source_inbox_paragraph_is_parsed_off_the_row(tmp_path):
    """The paragraph render_task writes is what plan_checks_core reads back — one shape, read
    by both admission's writer and the status-view's reader."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import plan_checks_core

    plan, checkpoints = host(tmp_path)
    letter(tmp_path / "inbox", "2026-09-09-from-owner-wish.md")
    route = new_route(source={"kind": "person", "detail": "the owner",
                              "inbox": "2026-09-09-from-owner-wish.md"})
    task_id = admission.admit(route, plan, checkpoints)["task_id"]
    tasks = plan_checks_core.parse_tasks(plan.read_text(encoding="utf-8"))
    row = next(t for t in tasks if t["id"] == task_id)
    assert row["source_inbox"] == "2026-09-09-from-owner-wish.md"


# ---------------------------------------------------------------- scripts/state-probe.sh


NEEDED = (
    "scripts/state-probe.sh",
    "scripts/plan_checks.py",
    "scripts/plan_checks_core.py",
    "scripts/task-admission.py",
    "scripts/checkpoint.py",
    "scripts/inbox_lifecycle.py",
)


def build_probe_tree(tmp_path, plan_body="# Plan\n\n## Tasks\n\n## Blockers\n\n- none\n"):
    for rel in NEEDED:
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    (tmp_path / "PLAN.md").write_text(plan_body, encoding="utf-8")
    (tmp_path / "inbox").mkdir(exist_ok=True)


def run_probe(tmp_path):
    return subprocess.run(
        ["bash", str(tmp_path / "scripts" / "state-probe.sh")],
        cwd=str(tmp_path), capture_output=True, text=True,
        env={"HOME": str(tmp_path), "PATH": __import__("os").environ.get("PATH", "")},
    )


def test_the_inbox_block_still_shows_an_undated_open_letter(tmp_path):
    """No regression: the eleven letters already on record carry no Status line and must keep
    showing exactly as they did before this row."""
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "a-plain-wish.md", "no Status line at all\n")
    r = run_probe(tmp_path)
    assert "a-plain-wish.md" in r.stdout, r.stdout


def test_the_inbox_block_shows_a_letter_explicitly_marked_open(tmp_path):
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "a.md", "Status: open\n")
    r = run_probe(tmp_path)
    assert "a.md" in r.stdout, r.stdout


def test_the_inbox_block_hides_a_handled_letter_left_standing_in_place(tmp_path):
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "a.md", "Status: handled\n")
    r = run_probe(tmp_path)
    assert "a.md" not in r.stdout, r.stdout


def test_the_inbox_block_hides_a_noted_letter(tmp_path):
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "a.md", "Status: noted\n")
    r = run_probe(tmp_path)
    assert "a.md" not in r.stdout, r.stdout


def test_the_inbox_block_shows_no_superseded_letter_as_work(tmp_path):
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "b.md", "successor\n")
    letter(tmp_path / "inbox", "a.md", "Status: superseded\nSuperseded-by: b.md\n")
    r = run_probe(tmp_path)
    assert "a.md" not in r.stdout, r.stdout
    # b's own state (no Status line) is OPEN, so it still shows as work in its own right.
    assert "b.md" in r.stdout, r.stdout


def test_the_inbox_block_names_a_malformed_letters_own_fault_instead_of_crashing(tmp_path):
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "a.md", "Status: cancelled\n")
    r = run_probe(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "a.md" in r.stdout
    assert "open" in r.stdout and "handled" in r.stdout  # the four states named in the refusal


def test_the_inbox_block_shows_an_open_letters_link_to_the_row_it_became(tmp_path):
    plan = (
        "# Plan\n\n## Tasks\n\n"
        "### ⬜ A wish worked — id: q-1\n"
        "**Group:** Test · **Priority:** normal\n"
        "**Source:** the owner.\n\n"
        "**Source inbox.** a.md\n\n"
        "**Outcome:** it happens.\n\n"
        "**Done when:** it happens.\n\n"
        "**DOD hash.** deadbeef\n\n"
        "## Blockers\n\n- none\n"
    )
    build_probe_tree(tmp_path, plan_body=plan)
    letter(tmp_path / "inbox", "a.md", "Status: open\n")
    r = run_probe(tmp_path)
    # The assertion has to look at the LETTER's own line and at what that line SAYS. Two earlier
    # shapes of this test proved nothing: reading the whole output passed on the plan row, which
    # prints `q-1 ... inbox:a.md` whatever the inbox block does, and excluding `"q-1 "` kept that
    # same plan row, because an escape sequence sits between the id and the space. Both were shown
    # green with the link deleted, with a wrong title printed, and with a link invented for a
    # letter no row names (the verifications of 2026-09-09). The letter's own line is the one
    # opening with the inbox marker, and the whole line is compared.
    assert plain_lines(r.stdout, "! a.md") == ["! a.md  \u2192 q-1 A wish worked"], r.stdout


def test_the_link_lands_on_the_letter_the_row_names_and_not_on_its_neighbour(tmp_path):
    """Three open letters, two rows. Every other test in this file shows the probe a single letter
    and a single row, so `the row it was admitted into` and `some row` read alike there: a probe
    handing the first row it holds to whatever letter it is printing passes all of them, and so
    does one taking a link's words from whichever row comes first. The neighbour shares a first
    character on purpose, so a match comparing less than the whole name is caught too, and the
    third letter names no row so a fallback still has somewhere to fire.
    """
    plan = (
        "# Plan\n\n## Tasks\n\n"
        "### \u2b1c A wish worked \u2014 id: q-1\n"
        "**Group:** Test \u00b7 **Priority:** normal\n"
        "**Source:** the owner.\n\n"
        "**Source inbox.** a.md\n\n"
        "**Outcome:** it happens.\n\n"
        "**Done when:** it happens.\n\n"
        "**DOD hash.** deadbeef\n\n"
        "### \u2b1c A second wish \u2014 id: q-2\n"
        "**Group:** Test \u00b7 **Priority:** normal\n"
        "**Source:** the owner.\n\n"
        "**Source inbox.** another.md\n\n"
        "**Outcome:** it happens.\n\n"
        "**Done when:** it happens.\n\n"
        "**DOD hash.** deadbeef\n\n"
        "## Blockers\n\n- none\n"
    )
    build_probe_tree(tmp_path, plan_body=plan)
    letter(tmp_path / "inbox", "a.md", "Status: open\n")
    letter(tmp_path / "inbox", "another.md", "Status: open\n")
    letter(tmp_path / "inbox", "zz.md", "Status: open\n")
    r = run_probe(tmp_path)
    assert plain_lines(r.stdout, "! a.md") == ["! a.md  \u2192 q-1 A wish worked"], r.stdout
    assert plain_lines(r.stdout, "! another.md") == ["! another.md  \u2192 q-2 A second wish"], r.stdout
    assert plain_lines(r.stdout, "! zz.md") == ["! zz.md"], r.stdout


def test_an_open_letter_no_row_names_prints_no_link(tmp_path):
    """The mirror of the row-side negative: a letter nothing was admitted from carries no link.

    Without it, a probe inventing `-> q-999 INVENTED` beside any letter passes the whole file.
    """
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "a.md", "Status: open\n")
    r = run_probe(tmp_path)
    assert plain_lines(r.stdout, "! a.md") == ["! a.md"], r.stdout


def test_a_status_line_inside_a_code_fence_is_not_the_letters_own_field(tmp_path):
    """A letter quoting the field in an example must not silence itself. This is the fault the row
    exists to kill: a state read out of prose rather than out of the letter's own field."""
    body = (
        "A letter about the field itself.\n\n"
        "```\n"
        "Status: handled\n"
        "```\n\n"
        "It is open all the same.\n"
    )
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "a.md", body)
    r = run_probe(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "a.md" in r.stdout, "a letter whose only Status line is an example is still open"


def test_a_state_word_is_read_whatever_its_case(tmp_path):
    """A depositor typing the word in capitals meant the word. Recorded because it is a choice,
    and `inbox/README.md` says so where a depositor reads."""
    build_probe_tree(tmp_path)
    letter(tmp_path / "inbox", "a.md", "Status: NOTED\n")
    r = run_probe(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "a.md" not in r.stdout


def test_a_rows_own_printed_line_carries_its_letters_name(tmp_path):
    plan = (
        "# Plan\n\n## Tasks\n\n"
        "### ⬜ A wish worked — id: q-1\n"
        "**Group:** Test · **Priority:** normal\n"
        "**Source:** the owner.\n\n"
        "**Source inbox.** a.md\n\n"
        "**Outcome:** it happens.\n\n"
        "**Done when:** it happens.\n\n"
        "**DOD hash.** deadbeef\n\n"
        "## Blockers\n\n- none\n"
    )
    build_probe_tree(tmp_path, plan_body=plan)
    letter(tmp_path / "inbox", "a.md", "Status: open\n")
    r = run_probe(tmp_path)
    lines = [ln for ln in r.stdout.splitlines() if "q-1" in ln and "A wish worked" in ln]
    assert lines, r.stdout
    assert "inbox:a.md" in lines[0], lines[0]


def test_a_row_with_no_letter_prints_no_inbox_label(tmp_path):
    plan = (
        "# Plan\n\n## Tasks\n\n"
        "### ⬜ A wish worked — id: q-1\n"
        "**Group:** Test · **Priority:** normal\n"
        "**Source:** the owner.\n\n"
        "**Outcome:** it happens.\n\n"
        "**Done when:** it happens.\n\n"
        "**DOD hash.** deadbeef\n\n"
        "## Blockers\n\n- none\n"
    )
    build_probe_tree(tmp_path, plan_body=plan)
    r = run_probe(tmp_path)
    lines = [ln for ln in r.stdout.splitlines() if "q-1" in ln and "A wish worked" in ln]
    assert lines, r.stdout
    assert "inbox:" not in lines[0], lines[0]
