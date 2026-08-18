"""The stranger door (INV-146) and its monitor (INV-147) — ROADMAP row 261.

M-288 asserts the stranger-arm law lives in its prose homes and the templated door ships.
M-289 asserts the monitor's surfacing logic is a pure, idempotent, crash-safe function,
single-instance by a lock, and honest on an unreachable repo.
M-290 asserts the package repo's scheduled monitor action ships and is single-instance.
M-291 asserts the cross-host coordinator: two hosts on one repo converge on a single
surfacing by a claim on the shared item, arbitrated by a pure winner reading, the claim
stolen by age like the per-host lock, its marker distinct from the surfaced-gen record.
"""
import importlib.util
import os
import re
from pathlib import Path

from conftest import SPEC, read

REPO = Path(__file__).resolve().parent.parent


def _load_monitor():
    path = REPO / "scripts" / "stranger-wish-monitor.py"
    spec = importlib.util.spec_from_file_location("stranger_wish_monitor", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- M-288: the stranger arm lives in its prose homes + the templated door ships ----

def test_stranger_arm_in_prose_homes():
    spec = read(SPEC)     # the whole spec: the core and the parts its map names
    readme = (REPO / "inbox" / "README.md").read_text()
    # the spec inbox-law clause carries the stranger arm and the monitor bridge
    assert "stranger arm" in spec
    assert "monitor bridges" in spec or "monitor" in spec.lower()
    # inbox/README.md documents the stranger arm for a contributor without push/grant
    assert "stranger" in readme.lower()
    assert "monitor" in readme.lower()


def test_wish_issue_template_requests_source():
    tmpl = REPO / ".github" / "ISSUE_TEMPLATE" / "wish.yml"
    assert tmpl.exists(), "the templated stranger door must ship"
    text = tmpl.read_text().lower()
    # a source field is requested (the same source the inbox deposit names)
    assert "source" in text
    # the template is a GitHub Issue Form (has a body of form elements)
    assert "body:" in text or "- type:" in text


def test_stranger_arm_spec_anchor_and_index():
    spec = read(SPEC)     # the whole spec: the core and the parts its map names
    # each invariant carries a body clause (the bracketed anchor, alone or grouped with a sibling
    # code) AND a Formal-index row
    body_anchors = {"INV-146": "[INV-146]", "INV-147": "INV-147, INV-67]"}
    for code, anchor in body_anchors.items():
        assert anchor in spec, f"{code} needs a body clause anchor"
        assert f"| {code} |" in spec, f"{code} needs a Formal-index row"


# ---- M-289: the monitor's surfacing logic ----

def test_monitor_surfaces_each_item_once():
    m = _load_monitor()
    # two open, never-surfaced items (no recorded generation)
    items = [
        {"kind": "issue", "number": 1, "activity_gen": "t0"},
        {"kind": "issue", "number": 2, "activity_gen": "t0"},
    ]
    first = m.items_to_surface(items, existing_inbox_sources=set())
    assert len(first) == 2
    # after depositing, their keys are recorded — a second run surfaces nothing
    keys = {m.surface_key(it) for it in first}
    second = m.items_to_surface(items, existing_inbox_sources=keys)
    assert second == []


def test_monitor_idempotent_on_already_surfaced():
    m = _load_monitor()
    # an item already surfaced at its current generation is never re-surfaced
    surfaced = [{"kind": "issue", "number": 1, "surfaced_gen": "t0", "activity_gen": "t0"}]
    assert m.items_to_surface(surfaced, existing_inbox_sources=set()) == []
    # crash-safety: never recorded but its inbox file already exists → not surfaced twice
    unrecorded = [{"kind": "issue", "number": 1, "activity_gen": "t0"}]
    key = m.surface_key(unrecorded[0])
    assert m.items_to_surface(unrecorded, existing_inbox_sources={key}) == []
    # new stranger activity (a newer generation than the one recorded) re-surfaces once —
    # the monitor is the actor: it compares generations, no label-dropping by a third party
    reactivated = [{"kind": "issue", "number": 1, "surfaced_gen": "t0", "activity_gen": "t1"}]
    assert len(m.items_to_surface(reactivated, existing_inbox_sources={key})) == 1


def test_monitor_deposit_failure_is_not_counted_surfaced():
    m = _load_monitor()
    logged = []
    result = m.run(
        fetch_open_items=lambda: [{"kind": "issue", "number": 1, "activity_gen": "t0"}],
        list_inbox_sources=lambda: set(),
        deposit=lambda item: False,  # deposit did not complete (commit or record failed)
        log=lambda msg: logged.append(msg),
    )
    # a half-done deposit is logged honestly and NOT counted surfaced, so next run retries it
    assert result["reachable"] is True
    assert result["surfaced"] == []
    assert any("did not complete" in msg for msg in logged)


def test_monitor_single_instance_lock(tmp_path):
    m = _load_monitor()
    lock = tmp_path / "monitor.lock"
    with m.single_instance(lock) as got_first:
        assert got_first is True
        # a second acquisition while the first is held stands down
        with m.single_instance(lock) as got_second:
            assert got_second is False
    # released after the first exits → acquirable again
    with m.single_instance(lock) as got_third:
        assert got_third is True


def test_monitor_honest_failure_on_unreachable():
    m = _load_monitor()

    def unreachable_fetch():
        raise ConnectionError("github unreachable")

    logged = []
    result = m.run(
        fetch_open_items=unreachable_fetch,
        list_inbox_sources=lambda: set(),
        deposit=lambda item: logged.append(("deposit", item)),
        log=lambda msg: logged.append(("log", msg)),
    )
    # honest failure: it names the reach it lacks, logs, drops nothing, deposits nothing
    assert result["reachable"] is False
    assert result["surfaced"] == []
    assert any(kind == "log" for kind, _ in logged)
    assert not any(kind == "deposit" for kind, _ in logged)


def test_monitor_does_not_retrigger_on_own_marker():
    # The activity generation is read from non-marker activity, so the monitor's own marker comment
    # never advances it and an already-surfaced item reads as NO new activity — no re-surface loop.
    # A daily cron would otherwise manufacture one duplicate inbox file and one comment per open item
    # every run (the live round-trip failure M-295 guards at the fetch layer).
    m = _load_monitor()
    marker = m.SURFACED_MARKER
    tm = "2026-07-14T10:00:00Z"
    comments = [{"body": f"Surfaced for review.\n\n{marker} 2026-07-14T09:00:00Z -->", "createdAt": tm}]
    # surfaced_gen answers "was it surfaced" — the marker's own createdAt, not the pre-comment body value
    assert m._surfaced_gen_from_comments(comments) == tm
    # a surfaced item whose only activity is the monitor's own marker → not re-surfaced
    same = [{"kind": "issue", "number": 1, "activity_gen": tm, "surfaced_gen": tm}]
    assert m.items_to_surface(same, existing_inbox_sources=set()) == []
    # a genuine actor comment AFTER the marker advances the activity generation past it → re-surfaced once
    newer = [{"kind": "issue", "number": 1, "activity_gen": "2026-07-14T11:00:00Z", "surfaced_gen": tm}]
    assert len(m.items_to_surface(newer, existing_inbox_sources=set())) == 1


def test_fetch_discussions_degrades_when_disabled(monkeypatch):
    # A repo with Discussions turned off offers no discussion channel; _fetch_discussions returns []
    # rather than letting a GraphQL error fell the whole run (which would also drop the Issue arm).
    m = _load_monitor()

    def fake_gh_json(args):
        if "nameWithOwner" in args:
            return {"nameWithOwner": "owner/repo"}
        if "hasDiscussionsEnabled" in args:
            return {"hasDiscussionsEnabled": False}
        raise AssertionError("no further gh call expected once discussions are off: %r" % args)

    def fake_graphql(*a, **k):
        raise AssertionError("GraphQL must not run when discussions are disabled")

    monkeypatch.setattr(m, "_gh_json", fake_gh_json)
    monkeypatch.setattr(m, "_gh_graphql", fake_graphql)
    assert m._fetch_discussions() == []


# ---- M-290: the package repo's scheduled monitor action (INV-148) ----

WORKFLOW = REPO / ".github" / "workflows" / "stranger-monitor.yml"


def _workflow_text():
    assert WORKFLOW.exists(), "the scheduled monitor action must ship (INV-148)"
    return WORKFLOW.read_text()


def test_monitor_schedule_workflow_ships():
    text = _workflow_text()
    # it wakes on a daily cron AND on a manual dispatch (the verify hand-run)
    assert "schedule:" in text
    assert "cron:" in text
    assert "workflow_dispatch:" in text


def test_monitor_schedule_is_single_instance():
    text = _workflow_text()
    # a concurrency group serializes runs; an in-progress run is never cancelled,
    # so a second scheduled run waits rather than racing the first's push (the CI
    # form of the per-host lock, INV-147)
    assert "concurrency:" in text
    assert re.search(r"cancel-in-progress:\s*false", text), \
        "the concurrency group must not cancel a mid-flight run"


def test_monitor_schedule_grants_write_scopes():
    text = _workflow_text()
    # the token needs contents (push the inbox commit) + issues + discussions
    # (record the surfaced-generation marker comment, INV-146)
    for scope in ("contents", "issues", "discussions"):
        assert re.search(rf"{scope}:\s*write", text), f"missing {scope}: write grant"


def test_monitor_schedule_runs_and_pushes():
    text = _workflow_text()
    # it runs the monitor script and pushes whatever inbox commit it made
    assert "stranger-wish-monitor.py" in text
    assert "git push" in text


# ---- M-291: the cross-host coordinator (INV-149) ----

def test_parse_claims_reads_host_and_time():
    m = _load_monitor()
    comments = [
        {"body": f"claiming\n\n{m.CLAIM_MARKER} 2026-07-14T09:00:00Z host:mac -->",
         "createdAt": "2026-07-14T09:00:01Z"},
        {"body": "an ordinary human comment", "createdAt": "2026-07-14T09:05:00Z"},
        {"body": f"{m.SURFACED_MARKER} 2026-07-14T09:02:00Z -->", "createdAt": "2026-07-14T09:02:00Z"},
    ]
    claims = m.parse_claims(comments)
    # only the claim-marker comment is a claim — the human comment and the surfaced-gen record are not;
    # the claim carries its host id (from the marker) and its creation time (from the comment field)
    assert len(claims) == 1
    assert claims[0]["host"] == "mac"
    assert claims[0]["created"] == "2026-07-14T09:00:01Z"


def test_claim_winner_earliest_then_host_tiebreak():
    m = _load_monitor()
    now = m._iso_to_epoch("2026-07-14T10:00:00Z")
    # the earliest claim by creation time wins outright
    claims = [
        {"host": "mac", "created": "2026-07-14T09:00:05Z"},
        {"host": "action", "created": "2026-07-14T09:00:01Z"},
    ]
    assert m.claim_winner(claims, now) == "action"
    # a tie on creation time breaks to the lower host identity
    tied = [
        {"host": "mac", "created": "2026-07-14T09:00:00Z"},
        {"host": "action", "created": "2026-07-14T09:00:00Z"},
    ]
    assert m.claim_winner(tied, now) == "action"  # 'action' < 'mac'


def test_claim_winner_identical_across_hosts():
    m = _load_monitor()
    now = m._iso_to_epoch("2026-07-14T10:00:00Z")
    # both hosts read the SAME shared comment log and compute the SAME winner — so exactly one deposits
    shared_log = [
        {"host": "mac", "created": "2026-07-14T09:00:03Z"},
        {"host": "action", "created": "2026-07-14T09:00:01Z"},
    ]
    winner_by_mac = m.claim_winner(shared_log, now)
    winner_by_action = m.claim_winner(shared_log, now)
    assert winner_by_mac == winner_by_action == "action"


def test_stale_claim_stolen_by_age():
    m = _load_monitor()
    now = m._iso_to_epoch("2026-07-14T12:00:00Z")
    # 'action' claimed first, but its claim is older than the stale bound with no surfacing recorded
    # behind it (it died mid-round); the surviving host 'mac' wins past the abandoned claim
    claims = [
        {"host": "action", "created": "2026-07-14T09:00:00Z"},  # ~3h old > LOCK_STALE_SECONDS
        {"host": "mac", "created": "2026-07-14T11:59:00Z"},
    ]
    assert m.claim_winner(claims, now) == "mac"
    # with only the abandoned claim present there is no live winner — the survivor's next run re-claims
    assert m.claim_winner([claims[0]], now) is None


def test_claim_loser_stands_down_and_deposits_nothing():
    m = _load_monitor()
    deposited = []
    logged = []
    result = m.run(
        fetch_open_items=lambda: [{"kind": "issue", "number": 1, "activity_gen": "t0"}],
        list_inbox_sources=lambda: set(),
        deposit=lambda item: deposited.append(item) or True,
        log=lambda msg: logged.append(msg),
        claim=lambda item: False,  # this host lost the claim to another host this round
    )
    # a losing host deposits nothing and is not counted surfaced; it retries next run
    assert result["reachable"] is True
    assert result["surfaced"] == []
    assert deposited == []
    assert any("stood down" in msg or "claim" in msg for msg in logged)


def test_claim_winner_deposits():
    m = _load_monitor()
    deposited = []
    result = m.run(
        fetch_open_items=lambda: [{"kind": "issue", "number": 1, "activity_gen": "t0"}],
        list_inbox_sources=lambda: set(),
        deposit=lambda item: deposited.append(item) or True,
        log=lambda msg: None,
        claim=lambda item: True,  # this host won the claim
    )
    assert len(result["surfaced"]) == 1
    assert len(deposited) == 1


def test_claim_marker_never_reads_as_surfaced():
    m = _load_monitor()
    # a claim comment must NOT register as a surfaced-generation record, or a claim would falsely
    # advance the re-surface generation [INV-146]; the two markers are distinct strings
    assert m.CLAIM_MARKER != m.SURFACED_MARKER
    claim_only = [{"body": f"{m.CLAIM_MARKER} 2026-07-14T09:00:00Z host:mac -->",
                   "createdAt": "2026-07-14T09:00:01Z"}]
    assert m._surfaced_gen_from_comments(claim_only) is None
    # and a surfaced-gen record is not read as a claim
    surfaced_only = [{"body": f"{m.SURFACED_MARKER} 2026-07-14T09:00:00Z -->",
                      "createdAt": "2026-07-14T09:00:00Z"}]
    assert m.parse_claims(surfaced_only) == []


def test_marker_ceiling_counts_claims_and_confirms():
    m = _load_monitor()
    # the re-surface baseline is the NEWEST of any monitor marker — a claim OR a surfaced-gen record
    comments = [
        {"body": f"{m.SURFACED_MARKER} g -->", "createdAt": "2026-07-14T09:00:03Z"},  # confirm
        {"body": f"{m.CLAIM_MARKER} g host:mac -->", "createdAt": "2026-07-14T09:00:05Z"},  # later claim
        {"body": "a human comment", "createdAt": "2026-07-14T09:00:01Z"},
    ]
    # the ceiling is the later claim's time, not the confirm's — so a trailing claim raises the baseline
    assert m._marker_ceiling_from_comments(comments) == "2026-07-14T09:00:05Z"
    # no markers at all → None
    assert m._marker_ceiling_from_comments([{"body": "just a human", "createdAt": "t"}]) is None


def test_trailing_claim_does_not_reloop_surfacing():
    m = _load_monitor()
    # The two-host contended case: a winner surfaced (confirm at t3), then a LOSING host posted its
    # claim at t4 — later than the confirm, so the claim is now the item's newest comment and bumps
    # updatedAt to t4. Measured against the confirm alone this would read as fresh activity and
    # re-surface a duplicate every run. Measured against the newest marker (the claim itself), it
    # reads as no new activity, so the round stays closed (INV-149).
    looping = [{
        "kind": "issue", "number": 1,
        "activity_gen": "2026-07-14T09:00:04Z",       # updatedAt bumped by the loser's trailing claim
        "surfaced_gen": "2026-07-14T09:00:03Z",       # the winner's confirm
        "marker_ceiling": "2026-07-14T09:00:04Z",     # newest marker = the trailing claim
    }]
    assert m.items_to_surface(looping, existing_inbox_sources=set()) == []
    # but a GENUINE stranger comment or edit AFTER every marker rises above the ceiling → re-surfaced
    real_activity = [{
        "kind": "issue", "number": 1,
        "activity_gen": "2026-07-14T10:00:00Z",       # a stranger commented, no new marker
        "surfaced_gen": "2026-07-14T09:00:03Z",
        "marker_ceiling": "2026-07-14T09:00:04Z",
    }]
    assert len(m.items_to_surface(real_activity, existing_inbox_sources=set())) == 1


# ---- M-295: a run's own marker comments do not advance the activity signal (both channels) ----
# A live round-trip on the package repo's GitHub discussion #1 exposed a duplicate: GitHub advances
# an item's updatedAt to a moment STRICTLY LATER than the createdAt of the very comment that caused
# the bump. So after the monitor posts its own claim (18:36:55-gen) and confirm markers, the item's
# updatedAt reads ~19:20:53Z while the newest marker's createdAt is ~19:20:52Z. Feeding the raw
# updatedAt as the activity generation, the next run reads it as fresh outside activity, clears the
# marker ceiling, and deposits a SECOND inbox file — a self-triggered re-surface loop that fires
# every run on any open item. The activity generation must exclude the monitor's own marker comments.

def _own_marker_state(kind):
    # The state one item is in on the SECOND run: the monitor's own claim + confirm markers stand,
    # and GitHub has bumped the item's updatedAt a hair PAST the newest marker's createdAt. There is
    # no third-party activity — the only comments are the monitor's own two markers.
    claim = {"body": f"claiming\n\n{_load_monitor().CLAIM_MARKER} 2026-07-14T18:36:55Z host:h -->",
             "createdAt": "2026-07-14T19:20:51Z"}
    confirm = {"body": f"Surfaced.\n\n{_load_monitor().SURFACED_MARKER} 2026-07-14T18:36:55Z -->",
               "createdAt": "2026-07-14T19:20:52Z"}
    bumped = "2026-07-14T19:20:53Z"  # updatedAt bumped by the monitor's own confirm, strictly later
    return claim, confirm, bumped


def test_own_marker_updatedat_bump_does_not_reloop_discussion(monkeypatch):
    m = _load_monitor()
    claim, confirm, bumped = _own_marker_state("discussion")

    def fake_gh_json(args):
        if "hasDiscussionsEnabled" in args:
            return {"hasDiscussionsEnabled": True}
        if "nameWithOwner" in args:
            return {"nameWithOwner": "owner/repo"}
        raise AssertionError("no other gh json call expected for the discussion arm: %r" % args)

    def fake_graphql(query, **kw):
        return {"data": {"repository": {"discussions": {"nodes": [{
            "number": 1, "id": "D_1", "title": "a wish", "body": "please",
            "updatedAt": bumped,
            "comments": {"nodes": [claim, confirm]},
        }]}}}}

    monkeypatch.setattr(m, "_gh_json", fake_gh_json)
    monkeypatch.setattr(m, "_gh_graphql", fake_graphql)
    items = m._fetch_discussions()
    # exactly-once: the second run, seeing only the monitor's OWN markers, surfaces nothing
    assert m.items_to_surface(items, existing_inbox_sources=set()) == []


def test_own_marker_updatedat_bump_does_not_reloop_issue(monkeypatch):
    m = _load_monitor()
    claim, confirm, bumped = _own_marker_state("issue")

    def fake_gh_json(args):
        if args[:2] == ["issue", "list"]:
            return [{"number": 1, "title": "a wish", "body": "please", "updatedAt": bumped}]
        if args[:2] == ["issue", "view"]:
            return {"comments": [claim, confirm]}
        raise AssertionError("no other gh json call expected for the issue arm: %r" % args)

    monkeypatch.setattr(m, "_gh_json", fake_gh_json)
    items = m._fetch_issues()
    # the Issue channel shares the same latent defect and must be exactly-once too
    assert m.items_to_surface(items, existing_inbox_sources=set()) == []


def test_activity_gen_excludes_the_monitors_own_markers():
    m = _load_monitor()
    claim, confirm, _ = _own_marker_state("issue")
    # a genuine third-party comment newer than the markers IS activity
    human = {"body": "a stranger adds context", "createdAt": "2026-07-14T20:00:00Z"}
    # with only the monitor's own markers, the activity generation does not advance past them
    assert m._activity_gen_from_comments([claim, confirm]) <= "2026-07-14T19:20:52Z"
    # a genuine non-marker comment advances it
    assert m._activity_gen_from_comments([claim, confirm, human]) == "2026-07-14T20:00:00Z"
