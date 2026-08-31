"""INV-242 — the landing-refreshed-map gate.

NEXT_STEPS.md is the resume file (LIVE STATE + queue only); a commit that lands a ROADMAP row
(flips its Status cell to `landed`) but leaves NEXT_STEPS.md untouched hands the next session a
stale map. `guardrails/check-landing-next-steps.py` reds such a commit by name and prints the
flipped row number(s) and the fix. A commit that closes a row to `declined` / `deferred` /
`superseded`, or touches ROADMAP.md prose without a status flip, owes nothing.

Report-shape via the commit graph, not the working tree: it rides the suite only (its test IS its
push-gate coverage) and is NOT wired into guardrails/pre-push.
"""
import os
import subprocess

from conftest import ROOT, read

CHECK = os.path.join(ROOT, "guardrails", "check-landing-next-steps.py")

ROADMAP_HEADER = (
    "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n"
    "|---|---|---|---|---|\n"
)


def _roadmap_row(num, status, wish="Some wish"):
    return ROADMAP_HEADER + "| %d | %s | small | %s | Some decision |\n" % (num, wish, status)


def _git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def _init_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", ".")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    return repo


def _write(repo, name, content):
    (repo / name).write_text(content)


def _commit(repo, msg):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", msg)
    return _git(repo, "rev-parse", "HEAD").strip()


def _run_check(repo, base_sha):
    env = dict(os.environ)
    env["LIVE_SPEC_DIFF_BASE"] = base_sha
    return subprocess.run(["python3", CHECK], cwd=str(repo), capture_output=True, text=True, env=env)


def _commit_dated(repo, msg, date_iso):
    """A commit whose author/committer date is forced to `date_iso` — used to prove that a heal
    commit's real DAG position (a genuine descendant of its landing) is not enough on its own; the
    checker also reads the committer timestamp, so a backdated heal still fails the after-its-
    landing check."""
    _git(repo, "add", "-A")
    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = date_iso
    env["GIT_COMMITTER_DATE"] = date_iso
    r = subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", msg],
                        capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    return _git(repo, "rev-parse", "HEAD").strip()


def _roadmap_two_rows(status7, status9, wish7="Some wish", wish9="Another wish"):
    return (ROADMAP_HEADER
            + "| 7 | %s | small | %s | Some decision |\n" % (wish7, status7)
            + "| 9 | %s | small | %s | Some decision |\n" % (wish9, status9))


def test_reds_landing_commit_without_next_steps(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", _roadmap_row(7, "**landed 2026-07-20**"))
    _commit(repo, "land row 7, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode != 0, out
    assert "7" in out
    assert "INV-242" in out


def test_passes_landing_commit_that_touches_next_steps(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", _roadmap_row(7, "**landed 2026-07-20**"))
    _write(repo, "NEXT_STEPS.md", "state\nrow 7 landed\n")
    _commit(repo, "land row 7, with NEXT_STEPS refresh")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_passes_non_landing_commit(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    # prose-only edit: same status, no landed flip, no NEXT_STEPS touch
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open", wish="Some wish, revised prose"))
    _commit(repo, "prose edit, no status flip")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_passes_decline_deferred_superseded_close(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", _roadmap_row(7, "declined 2026-07-20"))
    _commit(repo, "decline row 7, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_reds_landing_with_escaped_pipe_in_wish(tmp_path):
    # A properly-escaped `\|` inside the wish cell must not shift the column count and hide the
    # Status cell — the checker splits on unescaped pipes only (adversarial audit 2026-07-20).
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open", wish=r"a wish with an escaped \| pipe"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md",
           _roadmap_row(7, "**landed 2026-07-20**", wish=r"a wish with an escaped \| pipe"))
    _commit(repo, "land row 7 with an escaped pipe in the wish, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode != 0, out
    assert "7" in out
    assert "INV-242" in out


def test_real_repo_range_refreshes_next_steps():
    # Live-tree enforcement: run the checker over THIS repo's real BASE..HEAD, so the law is
    # enforced against real commits in-suite (the far-tier / node-growth live-test pattern), not
    # fixtures alone. A real landing commit that skipped NEXT_STEPS reds the suite and, since the
    # suite is gate b, blocks the push.
    env = dict(os.environ)
    env.pop("LIVE_SPEC_DIFF_BASE", None)
    r = subprocess.run(["python3", CHECK], cwd=ROOT, capture_output=True, text=True, env=env)
    assert r.returncode == 0, (
        "a landing commit in this repo's range did not refresh NEXT_STEPS.md:\n" + r.stdout + r.stderr)


def test_checker_not_wired_into_pre_push():
    assert "check-landing-next-steps" not in read("guardrails/pre-push")


# --- the NEW trigger: the live-body law's closing-commit move (SPEC INV-276, ROADMAP row 480) ---

_ARCHIVE = "docs/queue-archive/rotated-ROADMAP-2026-07.md"
_ARCHIVE_HEADER = (
    "# Rotated ROADMAP rows — 2026-07\n\n"
    "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n"
    "|---|---|---|---|---|\n"
)


def _archive_row(num, status, wish="Some wish"):
    return _ARCHIVE_HEADER + "| %d | %s | small | %s | Some decision |\n" % (num, wish, status)


def _write_sub(repo, name, content):
    p = repo / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def test_new_trigger_landed_move_without_next_steps_reds(tmp_path):
    # A closing commit REMOVES row 7 from the body and ADDS it to the archive with a *landed* status,
    # and does not touch NEXT_STEPS.md — the new trigger reds.
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "*in-work 2026-07-23*"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", ROADMAP_HEADER)  # row 7 gone from the body
    _write_sub(repo, _ARCHIVE, _archive_row(7, "*landed %s; door: feature; delegation: kept*" % _today()))
    _commit(repo, "close row 7 into the month archive, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode != 0, out
    assert "7" in out
    assert "INV-242" in out


def test_new_trigger_landed_move_with_next_steps_passes(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "*in-work 2026-07-23*"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", ROADMAP_HEADER)
    _write_sub(repo, _ARCHIVE, _archive_row(7, "*landed %s*" % _today()))
    _write(repo, "NEXT_STEPS.md", "state\nrow 7 landed\n")
    _commit(repo, "close row 7 into the archive, with NEXT_STEPS refresh")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_live_deferred_status_quoting_landed_is_not_a_flip(tmp_path):
    # A *deferred* row whose trigger text QUOTES the word landed (a Done-when citation) is live,
    # never a landing flip — the closed live vocabulary at the cell's head decides (INV-242).
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "*queued* 2026-07-12"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", _roadmap_row(
        7, "*deferred* 2026-07-12 — revisit trigger: the clause \"one real deposit landed\" stays open"))
    _commit(repo, "re-status row 7 with a landed-quoting trigger, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def _today():
    import datetime
    return datetime.date.today().isoformat()


def test_new_trigger_relocation_of_old_landed_row_is_exempt(tmp_path):
    # A move whose archived status landed two or more days before the commit's own date is a
    # historical relocation — a conversion or an override fold — and owes no NEXT_STEPS refresh:
    # the map was refreshed at that old landing (SPEC INV-242's carve).
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "*queued* 2026-07-06"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", ROADMAP_HEADER)
    _write_sub(repo, _ARCHIVE, _archive_row(7, "**landed 2026-07-06 ~13:52, session 14** — whole"))
    _commit(repo, "relocate the historically landed row 7, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_new_trigger_declined_move_is_exempt(tmp_path):
    # A row leaving the body as *declined* (no landed token in the archived status) owes nothing.
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "*queued 2026-07-23*"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", ROADMAP_HEADER)
    _write_sub(repo, _ARCHIVE, _archive_row(7, "*declined 2026-07-23*"))
    _commit(repo, "decline row 7 into the archive, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_new_trigger_superseded_move_quoting_landed_is_not_a_flip(tmp_path):
    # The NEW-trigger sibling of test_live_deferred_status_quoting_landed_is_not_a_flip: a row
    # moved to the archive as *superseded* (head word), whose PRESERVED status prose still quotes
    # a deferred trigger's old Done-when citation ("one real remote deposit landed"), is not a
    # landing move — the archived status's own HEAD word decides, not a bare substring search.
    # Found live in row 247's rotation, commit bc6f862b, 2026-08-27: the real checker reded on
    # this exact shape before _is_landed_status replaced the bare "landed" in status.lower() test.
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "*deferred* 2026-07-12"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", ROADMAP_HEADER)  # row 7 gone from the body
    _write_sub(repo, _ARCHIVE, _archive_row(
        7, "*deferred* 2026-07-12 — revisit trigger: Done-when (c) \"one real remote deposit "
           "landed\" stays open — superseded 2026-08-27 (rotated into PLAN.md's Tasks list)"))
    _commit(repo, "rotate row 7 into PLAN.md's Tasks, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


# --- the heal road: a missed landing can be healed forward, never by amending history ---

def test_heals_missed_landing_with_later_heal_commit(tmp_path):
    # A landing commit misses its NEXT_STEPS.md refresh; a later commit that touches NEXT_STEPS.md
    # and names the miss by its shortsha heals it — the checker warns instead of redding.
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", _roadmap_row(7, "**landed 2026-07-20**"))
    land_sha = _commit(repo, "land row 7, no NEXT_STEPS touch")

    _write(repo, "NEXT_STEPS.md", "state\nrow 7 landed (healed)\n")
    _commit(repo, "heals landing %s — refresh the map after the fact" % land_sha[:8])

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode == 0, out
    assert '"severity": "warn"' in out
    assert "7" in out


def test_missed_landing_with_later_next_steps_commit_not_naming_sha_still_reds(tmp_path):
    # A later commit touches NEXT_STEPS.md but never names the missed landing's sha — it heals
    # nothing, so the miss stays an unhealed red.
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", _roadmap_row(7, "**landed 2026-07-20**"))
    _commit(repo, "land row 7, no NEXT_STEPS touch")

    _write(repo, "NEXT_STEPS.md", "state\nsome unrelated refresh\n")
    _commit(repo, "touch NEXT_STEPS.md, no heal phrase")

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode != 0, out
    assert "7" in out
    assert "INV-242" in out


def test_heal_phrase_commit_dated_before_its_landing_still_reds(tmp_path):
    # The heal commit is a genuine descendant of the landing (so it can legitimately name its real
    # sha) but its committer date is backdated to before the landing — a heal must come after its
    # landing in history, so this still reds.
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_row(7, "open"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", _roadmap_row(7, "**landed 2026-07-20**"))
    land_sha = _commit(repo, "land row 7, no NEXT_STEPS touch")

    _write(repo, "NEXT_STEPS.md", "state\nrow 7 landed (healed)\n")
    _commit_dated(repo, "heals landing %s — but backdated before the landing" % land_sha[:8],
                  "2020-01-01T00:00:00")

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode != 0, out
    assert "7" in out
    assert "INV-242" in out


def test_one_heal_commit_names_two_missed_landings(tmp_path):
    # A single heal commit's message can name several missed landings — both get healed.
    repo = _init_repo(tmp_path)
    _write(repo, "ROADMAP.md", _roadmap_two_rows("open", "open"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "ROADMAP.md", _roadmap_two_rows("**landed 2026-07-20**", "open"))
    land7 = _commit(repo, "land row 7, no NEXT_STEPS touch")

    _write(repo, "ROADMAP.md", _roadmap_two_rows("**landed 2026-07-20**", "**landed 2026-07-21**"))
    land9 = _commit(repo, "land row 9, no NEXT_STEPS touch")

    _write(repo, "NEXT_STEPS.md", "state\nrows 7 and 9 landed (healed)\n")
    _commit(repo, "heals landing %s, heals landing %s" % (land7[:8], land9[:8]))

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode == 0, out
    assert out.count('"severity": "warn"') == 2


# --- the live arm: PLAN.md is the one list (2026-08-28) ----------------------------------

PLAN_HEAD = "# PLAN\n\n## Tasks\n\n"


def _plan_task(mark, rid="plan-11", title="Some task"):
    return PLAN_HEAD + "### %s %s \u2014 id: %s\n\nBody.\n" % (mark, title, rid)


def test_reds_a_plan_task_marked_done_without_next_steps(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("\u2b1c"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", _plan_task("\u2705"))
    _commit(repo, "close plan-11, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode != 0, out
    assert "plan-11" in out
    assert "INV-242" in out


def test_passes_a_plan_task_marked_done_beside_a_next_steps_refresh(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("\u2b1c"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", _plan_task("\u2705"))
    _write(repo, "NEXT_STEPS.md", "state, refreshed\n")
    _commit(repo, "close plan-11 with the map refreshed")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_a_plan_task_taken_in_hand_owes_nothing(tmp_path):
    """Only the done mark is a close. A row moving to in-hand, blocked, or the owner's eyes is
    still open work, and the resume file owes it nothing."""
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("\u2b1c"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", _plan_task("\U0001f504"))
    _commit(repo, "take plan-11 in hand")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


# ---------------------------------------------------------------------------
# The LIVE ARCHIVE trigger (2026-08-28): a done task ROTATED off the board.
#
# The arm above sees a mark flip in place. Rotation is the other way a row closes — the block
# leaves PLAN.md for docs/queue-archive/ and nothing is added to the live list — and the PLAN arm
# shipped without it on the day rotation became live practice.
def _plan_archive(rid="plan-11", mark="✅", title="Some task"):
    return "# Rotated off PLAN.md\n\n### %s %s — id: %s\n\nBody.\n" % (mark, title, rid)


def test_a_done_task_rotated_into_the_archive_without_next_steps_reds(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("✅"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", PLAN_HEAD)
    _write_sub(repo, "docs/queue-archive/rotated-PLAN-2026-08-28-done.md", _plan_archive())
    _commit(repo, "rotate the done row off the board, no NEXT_STEPS touch")

    r = _run_check(repo, base)
    out = r.stdout + r.stderr
    assert r.returncode != 0, out
    assert "plan-11" in out
    assert "INV-242" in out


def test_a_done_task_rotated_into_the_archive_beside_a_refresh_passes(tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("✅"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", PLAN_HEAD)
    _write_sub(repo, "docs/queue-archive/rotated-PLAN-2026-08-28-done.md", _plan_archive())
    _write(repo, "NEXT_STEPS.md", "state, refreshed\n")
    _commit(repo, "rotate the done row off the board with the map refreshed")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_an_unfinished_task_rotated_into_the_archive_owes_nothing(tmp_path):
    """The mark a row carries OUT decides. A row archived while still open — folded, declined, put
    aside — closed nothing, the same carve the ROADMAP arm makes for declined / superseded."""
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("⬜"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", PLAN_HEAD)
    _write_sub(repo, "docs/queue-archive/rotated-PLAN-2026-08-28-open.md",
               _plan_archive(mark="⬜"))
    _commit(repo, "archive an open row")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_a_done_row_deleted_with_no_archive_beside_it_is_not_read_as_a_rotation(tmp_path):
    """The trigger asks for both halves. A done row simply removed with nothing added under
    docs/queue-archive/ is the rotation gate's business, not this one's."""
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("✅"))
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", PLAN_HEAD)
    _commit(repo, "delete the done row outright")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_a_retitled_done_row_still_on_the_board_is_no_rotation(tmp_path):
    """Rotated means gone from the board. Every edit to a heading line shows in a diff as one
    removal and one addition, so reading the removal alone called a retitle a rotation; an archive
    page quoting that row's id — which archive pages routinely do — then made the gate report a
    close for a row still sitting on the board (2026-08-28 adversarial read)."""
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("✅", title="Old title"))
    _write_sub(repo, "docs/queue-archive/rotated-PLAN-2026-08-28-other.md", "# archive\n")
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", _plan_task("✅", title="New title"))
    _write_sub(repo, "docs/queue-archive/rotated-PLAN-2026-08-28-other.md",
               "# archive\n\nCross-reference: the row at ### ⬜ Something — id: plan-11.\n")
    _commit(repo, "retitle a done row and quote its id in an archive page")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


def test_a_done_rows_mark_changed_in_place_is_no_rotation(tmp_path):
    """The same shape with the mark itself moving: a ✅ reopened to ⬜ is a row that stayed."""
    repo = _init_repo(tmp_path)
    _write(repo, "PLAN.md", _plan_task("✅"))
    _write_sub(repo, "docs/queue-archive/rotated-PLAN-2026-08-28-other.md", "# archive\n")
    _write(repo, "NEXT_STEPS.md", "state\n")
    base = _commit(repo, "base")

    _write(repo, "PLAN.md", _plan_task("⬜"))
    _write_sub(repo, "docs/queue-archive/rotated-PLAN-2026-08-28-other.md",
               "# archive\n\nSee ### ⬜ Some task — id: plan-11.\n")
    _commit(repo, "reopen the row and mention its id in an archive page")

    r = _run_check(repo, base)
    assert r.returncode == 0, r.stdout + r.stderr


# ---- The 2026-08-31 adversarial read: one mark, one spelling --------------------------------

def _load_gate_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "landing_gate", os.path.join(ROOT, "guardrails", "check-landing-next-steps.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_a_done_mark_carrying_a_variation_selector_is_still_a_done_mark():
    """`✅` and `✅️` are one mark on the board and two strings to a comparison. Reading the mark as
    typed let a heading marked done with the selector count as some other mark entirely: the row
    read done to the eye, and the commit that set it was asked for no resume refresh. PLAN.md
    already writes `👁️` with a selector, so this is the plan's own spelling, not an exotic one."""
    gate = _load_gate_module()
    plain = gate.parse_plan_heading("### ✅ A task — id: q-1")
    selected = gate.parse_plan_heading("### ✅️ A task — id: q-1")
    assert plain == ("q-1", gate.DONE_MARK)
    assert selected == plain, (
        "the two spellings of one mark have to reach the gate as one mark: %r vs %r"
        % (selected, plain)
    )


def test_the_boards_own_parser_agrees_with_the_gate_on_that_mark():
    """The plan has two readers and one vocabulary. A mark normalized in one home and read as typed
    in the other puts the board and the gate back into disagreement about the same row."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "plan_checks_for_marks", os.path.join(ROOT, "scripts", "plan_checks.py"))
    plan_checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plan_checks)
    assert plan_checks.normalize_mark("✅️") == "✅"
    assert plan_checks.normalize_mark("✅") == "✅"
    # The eye keeps its selector, since without one it renders as a monochrome glyph.
    assert plan_checks.normalize_mark("\U0001f441") == "\U0001f441️"
    assert plan_checks.normalize_mark("\U0001f441️") == "\U0001f441️"
