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
