#!/usr/bin/env python3
"""The stranger-door monitor (INV-147, ROADMAP row 261).

A stranger — a contributor with no push rights and no per-repo grant who can still open a
GitHub Issue — has no git path into the repo. This monitor is the bridge: it lists the open
stranger Issues, and for each that has not yet been surfaced at its current activity generation
it writes ONE new inbox/ file naming the source Issue and its source field, COMMITS that file
(touching inbox/ only, the source in the message — the same committed-file law the local and
remote arms obey [E-11, INV-112]), and records the surfaced generation on the Issue. From that
committed file on, the item is an ordinary inbox wish swept by the inbox law under its
git-atomic harvest [T-10, INV-11]. The monitor holds NO verdict: whether an item is a wish,
feedback, or neither stays the inbox sweep's call [T-20].

New stranger activity has an actor: the monitor reads an item's activity generation from activity
that is NOT its own writes — the newest comment that is not one of its marker comments — and on each
run re-surfaces an item whose activity generation is newer than the one it last recorded. Reading a
generation the monitor's own comments cannot advance is what keeps it from re-surfacing an item on
its own marker every run. A live round-trip exposed why the raw updatedAt cannot serve here: GitHub
advances an item's updatedAt to a moment STRICTLY LATER than the createdAt of the comment that caused
the bump, so the monitor's own claim and confirm comments push updatedAt a hair past their own
timestamps, and a next run comparing that raw updatedAt against the markers read it as fresh outside
activity and looped a duplicate every run. Reading the generation from non-marker comments closes
that loop: the monitor's own writes add no non-marker comment, so only another actor's comment
advances the generation. So a swept item a stranger comments on again is surfaced afresh rather than
sitting durably-recorded but operationally invisible [INV-138].

The surfacing decision is a PURE function of (open items, the generation each was last surfaced
at, existing inbox files), so a crash between depositing and recording still surfaces an item
exactly once. The process is single-instance by a lock (stale locks are stolen by age), and a
run that cannot reach the repo fails honestly [INV-67] — it names the reach it lacks, logs, and
retries on its next scheduled run, dropping no wish silently.

The bridge serves both Issues and Discussions: Issues over the `gh issue` commands, Discussions
over the GraphQL path (`gh api graphql`). Both are recorded by a hidden marker comment carrying
the surfaced generation, so neither needs a label.

Where two hosts' monitors watch one repo they converge on a single surfacing (INV-149): before a
host deposits, it posts a claim comment on the shared item carrying its host identity and deposits
only when its own claim wins the shared comment log (the earliest live claim, the lower host id
breaking a tie — a pure reading every host computes alike). A claim is the per-host lock lifted
onto the repo and stolen by age the same way, so a host that claims then dies cannot swallow the
wish — a surviving host wins past the stale claim and surfaces it. claim_winner / parse_claims are
pure and unit-tested; _claim wires the `gh` comment post and the read-back.

The core (items_to_surface / surface_key / single_instance / run) carries no I/O and is unit
-tested in tests/test_stranger_door.py. main() wires the `gh` CLI and the inbox/ directory.
"""
from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import time
from pathlib import Path

SURFACED_MARKER = "<!-- live-spec surfaced-gen:"  # a hidden marker comment records the generation
CLAIM_MARKER = "<!-- live-spec claim-gen:"  # a hidden marker comment claims a surfacing round (INV-149)
REPO_ROOT = Path(__file__).resolve().parent.parent
INBOX = REPO_ROOT / "inbox"
# A lock (and a claim) older than this is stolen (a hard-killed run left it behind). A staleness
# window — machinery tuning, kept and marked under the owner-ruled class
# (docs/audits/2026-08-07-number-rulings.md §3; the same value and role as the harness's
# OWNERLESS_STALE_AGE in templates/headless_harness.py). No incident or source behind the figure: an
# engineering default of one hour, far above any real run of this monitor, which is what makes an
# older lock safe to read as abandoned rather than live.
LOCK_STALE_SECONDS = 3600


# ---- the pure core -------------------------------------------------------------------------

def surface_key(item: dict) -> str:
    """The identity of one surfacing event: an item plus its activity generation."""
    return f"{item['kind']}-{item['number']}-gen{item.get('activity_gen', 0)}"


def items_to_surface(open_items: list[dict], existing_inbox_sources: set[str]) -> list[dict]:
    """The items that owe a fresh inbox file this run — the monitor's whole decision.

    An item is surfaced unless it was already surfaced at its current generation (no new
    activity since), or an inbox file for this exact generation already exists (the crash
    -safety check: a monitor that died after depositing but before recording still surfaces
    the item exactly once). `surfaced_gen` is the generation last recorded on the Issue, or
    None if it was never surfaced.
    """
    out = []
    for it in open_items:
        surfaced_gen = it.get("surfaced_gen")
        # `activity_gen` is read from the item's non-marker activity (its newest comment that is not
        # one of the monitor's own markers), never the raw updatedAt the monitor's own comments perturb
        # [INV-146, INV-138]. So the monitor's own claim and confirm — however far they push updatedAt —
        # never advance it, and the item settles at no new activity after its own surfacing. The marker
        # ceiling is the newest of ANY monitor marker the item carries — a surfaced-generation record OR
        # a cross-host claim (INV-149) — the belt-and-suspenders baseline that also holds a losing host's
        # trailing claim below the line in the two-host contended case. A genuine third-party comment is
        # a non-marker comment, so it advances `activity_gen` above both and re-surfaces the item once.
        # The confirm (surfaced_gen) still answers whether the item was ever surfaced. Absent an explicit
        # ceiling the confirm is the ceiling (a single monitor's own marker is always its last comment).
        marker_ceiling = it.get("marker_ceiling") or surfaced_gen
        if surfaced_gen is not None and marker_ceiling is not None \
                and it.get("activity_gen", "") <= marker_ceiling:
            continue
        if surface_key(it) in existing_inbox_sources:
            continue
        out.append(it)
    return out


# ---- the cross-host claim: two hosts on one repo converge on a single surfacing (INV-149) ----

def _iso_to_epoch(s: str):
    """Parse an ISO 8601 UTC timestamp (a GitHub createdAt) to epoch seconds, or None."""
    from datetime import datetime
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def claim_body(host_id: str, gen) -> str:
    """The claim comment a host posts on the source item before it deposits (INV-149).

    It carries the host's identity [INV-117] under CLAIM_MARKER — a marker DISTINCT from
    SURFACED_MARKER, so a claim never reads back as a recorded surfacing and never perturbs the
    re-surface generation the surfaced-gen record owns [INV-146].
    """
    return (f"A live-spec monitor on one host is surfacing this into the maintainers' inbox. "
            f"Where two hosts watch this repo, they converge on a single surfacing.\n\n"
            f"{CLAIM_MARKER} {gen} host:{host_id} -->")


def parse_claims(comments: list[dict]) -> list[dict]:
    """The claim records on one item — {host, created} per CLAIM_MARKER comment.

    `created` is the comment's own createdAt (the shared clock every host reads alike); `host` is
    the identity carried in the marker. A surfaced-gen record and an ordinary comment are not claims.
    """
    claims = []
    for c in comments:
        body = c.get("body", "")
        if CLAIM_MARKER in body:
            host = ""
            frag = body.split(CLAIM_MARKER, 1)[1]
            if "host:" in frag:
                host = frag.split("host:", 1)[1].split("-->", 1)[0].strip()
            claims.append({"host": host, "created": c.get("createdAt", "")})
    return claims


def claim_winner(claims: list[dict], now_epoch, stale_seconds: float = LOCK_STALE_SECONDS):
    """The host that owns this surfacing round — a pure reading every host computes alike (INV-149).

    The winner is the earliest LIVE claim by the comment's own creation time, the lower host
    identity breaking a tie [INV-117]. A claim older than stale_seconds is read as abandoned — a
    host that claimed then died before recording the surfacing — and is stolen by age the same way
    the per-host lock is [INV-147], so a surviving host wins past a dead winner and surfaces the
    wish itself [INV-1]. Returns the winning host id, or None when no live claim stands.
    """
    live = []
    for c in claims:
        ce = _iso_to_epoch(c.get("created", ""))
        if ce is None:
            continue
        if now_epoch is not None and now_epoch - ce > stale_seconds:
            continue  # abandoned claim — stolen by age
        live.append(c)
    if not live:
        return None
    winner = min(live, key=lambda c: (c.get("created", ""), c.get("host", "")))
    return winner.get("host", "")


@contextlib.contextmanager
def single_instance(lock_path, stale_seconds: float = LOCK_STALE_SECONDS):
    """Hold the monitor to one running instance; a second live acquisition stands down (False).

    A lock older than stale_seconds is stolen — a hard-killed run leaves its lock behind, and a
    permanent stand-down would blind the door against INV-147's required liveness.
    """
    acquired = False
    fd = None
    try:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            acquired = True
        except FileExistsError:
            try:
                age = time.time() - os.stat(str(lock_path)).st_mtime
            except FileNotFoundError:
                age = None
            if age is not None and age > stale_seconds:
                try:
                    os.remove(str(lock_path))
                    fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    acquired = True
                except (FileExistsError, FileNotFoundError):
                    acquired = False
            else:
                acquired = False
        yield acquired
    finally:
        if acquired:
            if fd is not None:
                os.close(fd)
            try:
                os.remove(str(lock_path))
            except FileNotFoundError:
                pass


def run(fetch_open_items, list_inbox_sources, deposit, log, claim=None) -> dict:
    """One monitor pass over injected I/O — honest on an unreachable repo, silent-drop never.

    `deposit` returns True when the item was durably surfaced (file committed AND generation
    recorded); an item whose deposit fails is logged and NOT counted surfaced, so the next run
    retries it rather than leaving a half-done deposit to masquerade as done [INV-67].

    `claim` is the cross-host coordinator (INV-149): for each item owing a surfacing it posts this
    host's claim on the shared item and returns True only when this host's claim wins the shared
    comment log, so where two hosts watch one repo exactly one deposits. A losing host stands down
    for the round, deposits nothing, and retries next run. `claim=None` runs the un-coordinated path
    (every item proceeds) — the shape the pre-INV-149 tests exercise. Production `main` always wires a
    real claim, so a lone host coordinates too and simply wins its own claim every time, at the cost
    of one claim comment per surfacing; a lone host cannot know it is alone, so it always claims.
    """
    try:
        open_items = fetch_open_items()
    except Exception as exc:  # any reach failure — network, auth, gh missing
        log(f"stranger-wish-monitor: cannot reach the repo ({exc}); dropping nothing, "
            f"retrying on the next scheduled run")
        return {"reachable": False, "surfaced": []}
    existing = list_inbox_sources()
    surfaced = []
    for item in items_to_surface(open_items, existing):
        if claim is not None and not claim(item):
            log(f"stranger-wish-monitor: did not hold the winning claim for {surface_key(item)} "
                f"this round; standing down, retrying next run (INV-149)")
            continue
        if deposit(item):
            surfaced.append(item)
        else:
            log(f"stranger-wish-monitor: deposit of {surface_key(item)} did not complete; "
                f"not counted surfaced, will retry next run")
    log(f"stranger-wish-monitor: {len(surfaced)} item(s) surfaced into inbox files")
    return {"reachable": True, "surfaced": surfaced}


# ---- the gh / filesystem shell (not unit-tested; the core above is) ------------------------

def _gh_json(args: list[str]):
    import json
    out = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    return json.loads(out.stdout or "[]")


def _gh_graphql(query: str, **variables):
    import json
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F", f"{k}={v}"]
    out = subprocess.run(args, capture_output=True, text=True, check=True)
    return json.loads(out.stdout or "{}")


def _surfaced_gen_from_comments(comments: list[dict]) -> str | None:
    """Whether (and when) the item was last surfaced — the createdAt of the newest surfaced-gen marker
    comment, or None if the monitor never surfaced it.

    This answers only "was it ever surfaced" and pins the round for the crash-safety key; the
    re-surface DECISION is made against `_activity_gen_from_comments`, which reads the item's activity
    from non-marker comments so the monitor's own markers can never advance it (INV-146, INV-138).
    """
    gen = None
    for c in comments:
        if SURFACED_MARKER in c.get("body", ""):
            created = c.get("createdAt", "")
            if gen is None or created > gen:
                gen = created
    return gen


def _marker_ceiling_from_comments(comments: list[dict]) -> str | None:
    """The newest createdAt among ALL monitor markers — a surfaced-gen record OR a claim (INV-149).

    A claim comment bumps the item's activity generation the same way a surfaced-gen record does, so
    the re-surface baseline must count both; measuring against the confirm alone would let a losing
    host's trailing claim loop a re-surface every run in the two-host contended case.
    """
    ceiling = None
    for c in comments:
        body = c.get("body", "")
        if SURFACED_MARKER in body or CLAIM_MARKER in body:
            created = c.get("createdAt", "")
            if ceiling is None or created > ceiling:
                ceiling = created
    return ceiling


def _is_monitor_marker(body: str) -> bool:
    """Whether a comment body is one of the monitor's OWN markers — a claim or a surfaced-gen record."""
    return SURFACED_MARKER in body or CLAIM_MARKER in body


def _activity_gen_from_comments(comments: list[dict]) -> str:
    """The item's activity generation — the newest createdAt among comments that are NOT the monitor's
    own markers (an empty string when the item carries no third-party comment).

    The item's raw updatedAt is NOT a safe activity signal. A live round-trip exposed why: GitHub
    advances an item's updatedAt to a moment STRICTLY LATER than the createdAt of the comment that
    caused the bump. So when the monitor posts its own claim and confirm marker comments, the item's
    updatedAt lands a hair past the newest marker's createdAt; feeding that raw updatedAt as the
    generation, the next run reads it as fresh outside activity, clears the marker ceiling, and
    deposits a duplicate — a self-triggered re-surface loop that fires every run on any open item.

    So the activity generation is read from activity that is NOT the monitor's own writes: the newest
    non-marker comment. The monitor's own claim and confirm — however far they push the raw updatedAt —
    add no non-marker comment, so they never advance this generation, and the item settles at no new
    activity after its own surfacing. A genuine third-party comment is a non-marker comment, so it
    advances the generation and re-surfaces the item once, exactly as INV-146 intends [INV-138].
    """
    gen = ""
    for c in comments:
        if _is_monitor_marker(c.get("body", "")):
            continue
        created = c.get("createdAt", "")
        if created > gen:
            gen = created
    return gen


def _owner_repo() -> tuple[str, str]:
    nwo = _gh_json(["repo", "view", "--json", "nameWithOwner"])["nameWithOwner"]
    owner, repo = nwo.split("/", 1)
    return owner, repo


def _fetch_issues():
    items = []
    # --limit is a fetch cap, not a policy bar: `gh issue list` defaults to 30, which would silently
    # hide open wishes, so it is raised to a figure far above this door's real traffic. No incident or
    # source behind the 200 — an engineering default. A repository that ever carries more than 200
    # open issues would drop the overflow silently, the same gap the discussion arm has below.
    issues = _gh_json(["issue", "list", "--state", "open", "--limit", "200",
                       "--json", "number,title,updatedAt,body"])
    for iss in issues:
        comments = _gh_json(["issue", "view", str(iss["number"]),
                             "--json", "comments"]).get("comments", [])
        items.append({
            "kind": "issue",
            "number": iss["number"],
            "title": iss.get("title", ""),
            "body": iss.get("body", ""),
            # the activity generation is read from non-marker activity, never the raw updatedAt the
            # monitor's own marker comments perturb past their own createdAt [INV-146, INV-138]
            "activity_gen": _activity_gen_from_comments(comments),
            "surfaced_gen": _surfaced_gen_from_comments(comments),
            "marker_ceiling": _marker_ceiling_from_comments(comments),
        })
    return items


def _fetch_discussions():
    # A repo with Discussions turned off offers no discussion channel; the monitor serves the
    # channels the repo has, so it degrades to none here rather than felling the whole run (a
    # GraphQL query against a repo without discussions would error and mask the Issue arm too).
    # A genuinely unreachable repo still raises from this call and fails the run honestly [INV-67].
    if not _gh_json(["repo", "view", "--json", "hasDiscussionsEnabled"]).get("hasDiscussionsEnabled"):
        return []
    owner, repo = _owner_repo()
    # first:100 is not a chosen number: 100 is GitHub's own documented maximum page size for a
    # GraphQL connection, so this asks for the largest page the API will return. Not a threshold —
    # a platform limit, the kind the owner's rule calls derived rather than invented.
    # Known gap, stated rather than papered over: neither connection is paginated past that first
    # page, so a repository with more than 100 open discussions, or a discussion with more than 100
    # comments, silently drops the remainder. Fixing that needs cursor paging, not a bigger number.
    q = ("query($owner:String!,$repo:String!){repository(owner:$owner,name:$repo){"
         "discussions(first:100,states:OPEN){nodes{number id title body updatedAt "
         "comments(first:100){nodes{body createdAt}}}}}}")
    data = _gh_graphql(q, owner=owner, repo=repo)
    nodes = (data.get("data", {}).get("repository", {}) or {}).get("discussions", {}).get("nodes", [])
    items = []
    for d in nodes:
        comments = d.get("comments", {}).get("nodes", [])
        items.append({
            "kind": "discussion",
            "number": d["number"],
            "id": d["id"],  # the node id, needed to post a comment
            "title": d.get("title", ""),
            "body": d.get("body", ""),
            # the activity generation is read from non-marker activity, never the raw updatedAt the
            # monitor's own marker comments perturb past their own createdAt [INV-146, INV-138]
            "activity_gen": _activity_gen_from_comments(comments),
            "surfaced_gen": _surfaced_gen_from_comments(comments),
            "marker_ceiling": _marker_ceiling_from_comments(comments),
        })
    return items


def _fetch_open_items():
    """List open Issues AND Discussions as monitor items, each carrying its activity generation."""
    return _fetch_issues() + _fetch_discussions()


def _list_inbox_sources() -> set[str]:
    keys = set()
    if not INBOX.exists():
        return keys
    for f in INBOX.glob("*.md"):
        for line in f.read_text(errors="ignore").splitlines():
            if line.startswith("surface-key:"):
                keys.add(line.split(":", 1)[1].strip())
    return keys


def _deposit(item: dict) -> bool:
    """Write, COMMIT, and record one surfaced item. Returns True only when all three held."""
    key = surface_key(item)
    slug = "".join(c if c.isalnum() else "-" for c in item.get("title", "wish"))[:40].strip("-")
    name = f"stranger-{item['kind']}-{item['number']}-{slug}.md"
    path = INBOX / name
    n = 2
    while path.exists():
        path = INBOX / f"stranger-{item['kind']}-{item['number']}-{slug}-{n}.md"
        n += 1
    path.write_text(
        f"surface-key: {key}\n"
        f"source: GitHub {item['kind']} #{item['number']}\n\n"
        f"# {item.get('title', '(no title)')}\n\n"
        f"{item.get('body', '')}\n\n"
        f"_Bridged from the stranger door by scripts/stranger-wish-monitor.py. "
        f"Route this by the inbox sweep; the wish-vs-not verdict is the sweep's [T-20]._\n"
    )
    # commit the file touching inbox/ only, the source in the message (E-11's committed-file law)
    rel = str(path.relative_to(REPO_ROOT))
    add = subprocess.run(["git", "-C", str(REPO_ROOT), "add", rel], capture_output=True, text=True)
    if add.returncode != 0:
        return False
    commit = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "commit", "-m",
         f"inbox: stranger {item['kind']} #{item['number']} ({item.get('title','')[:50]})", "--", rel],
        capture_output=True, text=True)
    if commit.returncode != 0:
        return False
    # record the surfaced generation on the item; a failed record is honest, not silent
    note = (f"Surfaced into the maintainers' inbox for review. Thank you — a live session will "
            f"route this wish.\n\n{SURFACED_MARKER} {item['activity_gen']} -->")
    if item["kind"] == "discussion":
        mut = ("mutation($discussionId:ID!,$body:String!){addDiscussionComment("
               "input:{discussionId:$discussionId,body:$body}){comment{id}}}")
        rec = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={mut}",
             "-F", f"discussionId={item['id']}", "-F", f"body={note}"],
            capture_output=True, text=True)
    else:
        rec = subprocess.run(
            ["gh", "issue", "comment", str(item["number"]), "--body", note],
            capture_output=True, text=True)
    return rec.returncode == 0


def _host_id() -> str:
    """This host's identity for the cross-host claim [INV-117, INV-149].

    The arbitration asks only that two hosts contending for one item carry different ids, so an
    explicit LIVE_SPEC_HOST_ID (when the host records one) else the machine hostname suffices —
    a contributor's own machine and a GitHub Actions runner never share a hostname, and two Action
    runs never overlap (the concurrency group serializes them). No identity stable beyond the round
    is needed.
    """
    import socket
    return os.environ.get("LIVE_SPEC_HOST_ID") or socket.gethostname()


def _fetch_item_comments(item: dict) -> list[dict]:
    """Re-read the source item's comments (Issue over `gh issue`, Discussion over GraphQL)."""
    if item["kind"] == "discussion":
        owner, repo = _owner_repo()
        # first:100 — GitHub's documented maximum GraphQL page size, as above; same unpaginated gap.
        q = ("query($owner:String!,$repo:String!,$number:Int!){repository(owner:$owner,name:$repo){"
             "discussion(number:$number){comments(first:100){nodes{body createdAt}}}}}")
        data = _gh_graphql(q, owner=owner, repo=repo, number=item["number"])
        disc = (data.get("data", {}).get("repository", {}) or {}).get("discussion", {}) or {}
        return disc.get("comments", {}).get("nodes", [])
    return _gh_json(["issue", "view", str(item["number"]), "--json", "comments"]).get("comments", [])


def _claim(item: dict, host_id: str) -> bool:
    """Post this host's claim on the shared item, re-read, and report whether it won (INV-149).

    The claim is a single-instance guard over the shared item — the per-host lock lifted onto the
    repo. This host posts its claim, then reads the item's claim comments back and wins only when
    its own claim is the earliest live one (the lower host id breaking a tie). A losing host returns
    False and stands down; a claim it cannot post fails honestly (False) and retries next run [INV-67].
    """
    body = claim_body(host_id, item.get("activity_gen", ""))
    if item["kind"] == "discussion":
        mut = ("mutation($discussionId:ID!,$body:String!){addDiscussionComment("
               "input:{discussionId:$discussionId,body:$body}){comment{id}}}")
        posted = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={mut}",
             "-F", f"discussionId={item['id']}", "-F", f"body={body}"],
            capture_output=True, text=True)
    else:
        posted = subprocess.run(
            ["gh", "issue", "comment", str(item["number"]), "--body", body],
            capture_output=True, text=True)
    if posted.returncode != 0:
        # could not post the claim (a missing issues/discussions write while the repo is still
        # reachable for the fetch) — stand down honestly and retry, naming the real cause [INV-67]
        print(f"stranger-wish-monitor: could not post the claim for {surface_key(item)} "
              f"({posted.stderr.strip()}); standing down, retrying next run")
        return False
    try:
        claims = parse_claims(_fetch_item_comments(item))
    except Exception as exc:
        # could not read the claims back — stand down and retry rather than risk a duplicate
        print(f"stranger-wish-monitor: could not read the claims for {surface_key(item)} "
              f"({exc}); standing down, retrying next run")
        return False
    return claim_winner(claims, time.time()) == host_id


def main() -> int:
    lock = REPO_ROOT / ".live-spec" / "stranger-monitor.lock"
    lock.parent.mkdir(exist_ok=True)
    with single_instance(lock) as acquired:
        if not acquired:
            print("stranger-wish-monitor: another instance holds the lock; standing down")
            return 0
        host_id = _host_id()
        result = run(_fetch_open_items, _list_inbox_sources, _deposit, print,
                     claim=lambda item: _claim(item, host_id))
        return 0 if result["reachable"] else 1


if __name__ == "__main__":
    sys.exit(main())
