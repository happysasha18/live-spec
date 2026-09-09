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
    assert "a.md" in r.stdout
    assert "q-1" in r.stdout
    assert "A wish worked" in r.stdout


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
