#!/usr/bin/env python3
"""check-landing-next-steps.py — the landing-refreshed-map gate (SPEC INV-242).

THE LAW. A "landing" commit owes a refresh of NEXT_STEPS.md in that SAME commit, since NEXT_STEPS.md
is the resume file (LIVE STATE + queue only) and a landing that does not update it leaves the next
session resuming from a stale map. Two triggers OR together, so both the pre-conversion history and the
post-conversion queue classify (SPEC INV-276, ROADMAP row 480):

  - the OLD trigger (pre-conversion body): the diff flips a ROADMAP.md row's Status cell to `landed`
    (case-insensitive) — the landed word lands as a live body status.
  - the NEW trigger (post-conversion live-body law): the diff REMOVES a body row from ROADMAP.md while
    a docs/queue-archive/*.md diff ADDS that same row number with an archived status whose own HEAD word
    is `landed` (case-insensitive, so the historical bold `**LANDED**` and the new `*landed*` both match)
    — the row leaves the body for the archive at its closing commit. The head word decides, not a bare
    substring: a status's own prose can quote "landed" inside a deferred trigger's Done-when citation
    without the row itself being landed (row 247, commit bc6f862b, 2026-08-27).

A commit that closes no row, or moves a row out as `declined` / `superseded` / `deferred` (anything
whose status HEAD is not `landed`), owes nothing here.

RANGE. Same base ladder as check-skill-review.sh / check-prover-record.sh: env LIVE_SPEC_DIFF_BASE
if set (and not the all-zeros sha) and it resolves to a commit; else origin/main if it resolves;
else HEAD~1. The range is BASE..HEAD, walked commit by commit via `git rev-list`.

DETECTION. For each commit, `git show <sha> -- ROADMAP.md` is read for its added (`+| ... |`) and
removed (`-| ... |`) table-row lines. A ROADMAP row is `| <num> | wish | class | STATUS | decision |`
— pipe-delimited, the Status cell the 4th cell between the pipes (index 3). A row number flips to
`landed` in this commit when an ADDED line for that number carries `landed` in its Status cell
while the REMOVED line for the same number did not (or there is no removed line at all — a row
born already `landed` counts too). The commit is a "landing" iff at least one row flips this way.

RED CONDITION. A landing commit whose changed-file list (`git show --name-only --format=`) does
not include NEXT_STEPS.md is a MISS. An unhealed miss reds: exit nonzero, one JSON line per
offending commit naming its short sha, the flipped row number(s), and the fix.

HEAL ROAD. A miss found after the fact cannot be fixed by amending history — that would fabricate
a record where the refresh always shipped with the landing. Instead a LATER commit in the same
BASE..HEAD range heals it forward, so the miss stays visible on record rather than being erased.
A commit heals a miss when it (a) touches NEXT_STEPS.md, (b) its message contains the phrase
`heals landing <shortsha>` where <shortsha> is at least 7 hex characters prefix-matching the missed
landing commit's full sha, and (c) its committer timestamp is not earlier than the landing commit's
— a heal that predates its landing heals nothing, since history only runs forward. One heal commit
may name several landings in one message. A healed miss prints a WARNING (severity "warn", naming
the landing, its rows, and the healing commit) and does not red; the miss stays on record even
though it no longer blocks.

This checker rides the suite rather than taking its own push-gate letter, because the push-gate
letters a–z are exhausted (INV-212's meta-guard requires every letter be classified). Riding the
suite is still enforcement at push: the suite is gate b, so a red here reds gate b and blocks the
push. Two suite tests cover it — a fixture-range test proving the detection logic, and a live-tree
test running it over this repo's real BASE..HEAD so the law is enforced against real commits, not
fixtures alone. It is deliberately NOT wired directly into guardrails/pre-push; see
tests/test_landing_next_steps.py::test_checker_not_wired_into_pre_push.
Self-contained: stdlib only, reads git in the current working tree.
"""
import json
import os
import re
import subprocess
import sys

ZERO_SHA = "0" * 40
ROW_RE = re.compile(r"\d+")
# Split a table row on unescaped pipes only, so a properly-escaped `\|` inside a wish cell does not
# shift the column count and hide the Status cell (adversarial audit 2026-07-20).
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")


def _run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def _resolves(ref, cwd):
    r = _run(["git", "rev-parse", "--verify", "--quiet", "%s^{commit}" % ref], cwd=cwd)
    return r.returncode == 0


def resolve_base(cwd):
    env_base = os.environ.get("LIVE_SPEC_DIFF_BASE", "")
    if env_base and env_base != ZERO_SHA and _resolves(env_base, cwd):
        return env_base
    if _resolves("origin/main", cwd):
        return "origin/main"
    if _resolves("HEAD~1", cwd):
        return "HEAD~1"
    return None


def parse_row_cells(line):
    """A pipe-delimited ROADMAP table-row line -> (row_number, status_cell), or None if the line
    is not a numbered row (the header, the separator, and prose lines all fail the digit test)."""
    if not line.startswith("|"):
        return None
    cells = CELL_SPLIT_RE.split(line)
    inner = cells[1:-1]
    if len(inner) < 4:
        return None
    num_str = inner[0].strip()
    if not ROW_RE.fullmatch(num_str):
        return None
    status = inner[3].strip()
    return int(num_str), status


def landed_rows_for_commit(sha, cwd):
    """The set of ROADMAP row numbers this commit flips to `landed`, sorted."""
    r = _run(["git", "show", sha, "--", "ROADMAP.md"], cwd=cwd)
    added = {}
    removed = {}
    for raw in r.stdout.splitlines():
        if raw.startswith("+++") or raw.startswith("---"):
            continue
        if raw.startswith("+"):
            parsed = parse_row_cells(raw[1:])
            if parsed:
                num, status = parsed
                added[num] = status
        elif raw.startswith("-"):
            parsed = parse_row_cells(raw[1:])
            if parsed:
                num, status = parsed
                removed[num] = status

    flipped = []
    for num, status in added.items():
        if "landed" not in status.lower():
            continue
        if _live_status(status):
            continue
        old_status = removed.get(num)
        if old_status is None or "landed" not in old_status.lower():
            flipped.append(num)
    return sorted(flipped)


def _live_status(status):
    """True when the status cell OPENS with one of the five live closed-vocabulary words — the
    post-conversion form (*queued* / *ready* / *in-work* / *deferred* / *far*). Such a row is live
    whatever prose follows (a deferred trigger may quote the word landed inside a Done-when citation),
    so it is never a landing flip."""
    head = status.strip().lstrip("*").lower()
    return head.startswith(("queued", "ready", "in-work", "deferred", "far"))


def _is_landed_status(status):
    """True when the status cell's own HEAD word (after stripping the leading `*`/`**`) is
    `landed` — bold `**landed**` historically, `*landed*` the new format, case-insensitive.
    Not a bare substring test: a row's long status prose can quote the word `landed` inside a
    deferred trigger's Done-when citation ("one real remote deposit landed") without the row
    itself being landed, and a naive "landed" in status.lower() reds on that quote (found live in
    row 247's superseded-move, commit bc6f862b, 2026-08-27). Mirrors _live_status's own head-word
    check for exactly this false-positive class."""
    head = status.strip().lstrip("*").strip().lower()
    return head.startswith("landed")


def landed_moves_for_commit(sha, cwd):
    """The set of ROADMAP row numbers this commit MOVES from the body to an archive with a `landed`
    archived status — the new trigger under the live-body law. A number reds here when the commit's
    ROADMAP.md diff removes its body row and a docs/queue-archive/*.md diff adds that same number
    whose status cell's own HEAD word (via _is_landed_status) is `landed`. A row moved out as
    declined/superseded/deferred (head word anything else) owes nothing, even where its preserved
    trigger prose happens to quote the word "landed" elsewhere in the cell."""
    r_body = _run(["git", "show", sha, "--", "ROADMAP.md"], cwd=cwd)
    removed = {}
    for raw in r_body.stdout.splitlines():
        if raw.startswith("+++") or raw.startswith("---"):
            continue
        if raw.startswith("-"):
            parsed = parse_row_cells(raw[1:])
            if parsed:
                removed[parsed[0]] = parsed[1]

    r_arch = _run(["git", "show", sha, "--", "docs/queue-archive"], cwd=cwd)
    arch_added = {}
    for raw in r_arch.stdout.splitlines():
        if raw.startswith("+++") or raw.startswith("---"):
            continue
        if raw.startswith("+"):
            parsed = parse_row_cells(raw[1:])
            if parsed:
                arch_added[parsed[0]] = parsed[1]

    commit_day = _commit_date(sha, cwd)
    flipped = []
    for num in removed:
        status = arch_added.get(num)
        if status is not None and _is_landed_status(status):
            if _is_relocation(status, commit_day):
                continue
            flipped.append(num)
    return sorted(flipped)


def _commit_date(sha, cwd):
    """The commit's own date (YYYY-MM-DD) from its committer clock."""
    r = _run(["git", "show", "-s", "--format=%cs", sha], cwd=cwd)
    return r.stdout.strip().splitlines()[-1].strip() if r.stdout.strip() else None


def _is_relocation(status, commit_day):
    """True when the archived status's landed date is two or more days older than the commit's own
    date: the row landed back then and this commit merely RELOCATES it to the archive (a conversion
    or an override fold), so the map was refreshed at the old landing and this move owes nothing
    (SPEC INV-242's carve: a fresh landing refreshes the map; a historical relocation does not).
    A status with no parseable date stays a fresh landing — the safe side."""
    if not commit_day:
        return False
    m = re.search(r"landed[^0-9]{0,40}(\d{4}-\d{2}-\d{2})", status, re.IGNORECASE)
    if not m:
        return False
    try:
        import datetime as _dt
        landed = _dt.date.fromisoformat(m.group(1))
        commit = _dt.date.fromisoformat(commit_day)
    except ValueError:
        return False
    # The day-lag that separates a historical relocation from a fresh landing. No incident or source
    # behind the 2 — an engineering default, not a policy decision (the 2026-08-07 census, row 7,
    # found no trace; the commit that introduced it, da6b26c, carries a subject line and no body).
    # What bounds the risk is the carve above, not this figure: an unparseable or absent date already
    # reads as a fresh landing, the safe side, so the number can only ever move a dated, already-past
    # landing out of the refresh duty — never let a fresh one escape it.
    return (commit - landed).days >= 2


def commit_files(sha, cwd):
    r = _run(["git", "show", "--name-only", "--format=", sha], cwd=cwd)
    return set(line.strip() for line in r.stdout.splitlines() if line.strip())


HEAL_RE = re.compile(r"heals landing ([0-9a-f]{7,40})", re.IGNORECASE)


def commit_message(sha, cwd):
    r = _run(["git", "show", "-s", "--format=%B", sha], cwd=cwd)
    return r.stdout


def commit_ts(sha, cwd):
    """The commit's committer-date unix timestamp — used to order a heal after its landing."""
    r = _run(["git", "show", "-s", "--format=%ct", sha], cwd=cwd)
    lines = r.stdout.strip().splitlines()
    return int(lines[-1]) if lines else 0


def heal_targets_for_commit(sha, cwd):
    """The set of lowercased shortshas this commit's message names via `heals landing <shortsha>`,
    when the commit also touches NEXT_STEPS.md — a commit that does not touch the resume file heals
    nothing regardless of what its message says."""
    if "NEXT_STEPS.md" not in commit_files(sha, cwd):
        return set()
    msg = commit_message(sha, cwd)
    return set(m.group(1).lower() for m in HEAL_RE.finditer(msg))


def main():
    r = _run(["git", "rev-parse", "--show-toplevel"])
    cwd = r.stdout.strip() if r.returncode == 0 else os.getcwd()

    base = resolve_base(cwd)
    if base is None:
        print("OK (landing-next-steps): no commit range resolves (single-commit tree, no "
              "origin/main) — nothing to check.")
        return 0

    r = _run(["git", "rev-list", "--reverse", "%s..HEAD" % base], cwd=cwd)
    if r.returncode != 0:
        print("OK (landing-next-steps): commit range %s..HEAD does not resolve — nothing to "
              "check." % base)
        return 0
    commits = [c for c in r.stdout.splitlines() if c.strip()]

    # First pass: which rows land ANYWHERE in the range beside a NEXT_STEPS.md refresh. A row landed
    # twice in one range — a first close reverted, then redone with the resume file beside it — is
    # discharged by the close that carried the refresh, since the law asks that a landing leave the
    # resume file current, and the redone close does exactly that (SPEC INV-242).
    per_commit = {}
    discharged = set()
    for sha in commits:
        flipped = sorted(set(landed_rows_for_commit(sha, cwd)) | set(landed_moves_for_commit(sha, cwd)))
        per_commit[sha] = flipped
        if flipped and "NEXT_STEPS.md" in commit_files(sha, cwd):
            discharged.update(flipped)

    # Heal candidates: every commit in the range that touches NEXT_STEPS.md and names at least one
    # missed landing by shortsha, paired with its committer timestamp for the after-its-landing check.
    heal_commits = []
    for sha in commits:
        targets = heal_targets_for_commit(sha, cwd)
        if targets:
            heal_commits.append((sha, targets, commit_ts(sha, cwd)))

    fail = False
    for sha in commits:
        flipped = [n for n in per_commit[sha] if n not in discharged]
        if not flipped:
            continue
        if "NEXT_STEPS.md" in commit_files(sha, cwd):
            continue
        short = sha[:8]
        nums = ", ".join(str(n) for n in flipped)

        landing_ts = commit_ts(sha, cwd)
        healer = None
        for hsha, targets, heal_ts in heal_commits:
            if heal_ts < landing_ts:
                continue
            if any(len(t) >= 7 and sha.lower().startswith(t) for t in targets):
                healer = hsha
                break

        if healer:
            record = {
                "severity": "warn",
                "code": "landing-next-steps",
                "message": ("landing commit %s flips ROADMAP row(s) %s to landed without a same-"
                            "commit NEXT_STEPS.md refresh, healed by %s (INV-242)"
                            % (short, nums, healer[:8])),
            }
            print(json.dumps(record))
            continue

        record = {
            "severity": "error",
            "code": "landing-next-steps",
            "message": ("landing commit %s flips ROADMAP row(s) %s to landed but does not touch "
                        "NEXT_STEPS.md (INV-242)" % (short, nums)),
            "fix": "refresh NEXT_STEPS.md in the landing commit",
        }
        print(json.dumps(record))
        fail = True

    if fail:
        return 1

    print("OK (landing-next-steps): every landing commit in %s..HEAD refreshes NEXT_STEPS.md "
          "(INV-242)." % base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
