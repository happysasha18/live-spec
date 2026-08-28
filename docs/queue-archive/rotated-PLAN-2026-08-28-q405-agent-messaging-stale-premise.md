# q-405 archived: its blocking premise is stale (from live-spec, 2026-08-28 00:44)

His word, verbatim reason: "сообщение между агентами уже работает в харнессе когда надо запилим"
— agent-to-agent messaging already works in the harness; wire it up when actually needed, not
tracked as a pending row until then.

## Index

One line for the archived row, findable by its own number — the pointer a reader who greps the
live list for that number follows to get here.

| # | Wish (plain words) | Class | Status | Decision / acceptance |
| --- | --- | --- | --- | --- |
| 405 | Instant messaging between agents turns on once the tool supports it | archive | declined 2026-08-28 | his word of 2026-08-28 00:44 — messaging between agents already works in the harness, so it gets wired up when it is actually needed instead of standing as a blocked row; the row's full text stands below |

## What it was

```
### ⛔ Instant messaging between agents turns on once the tool supports it — id: q-405
**Group:** Parallel & multi-agent work · **Priority:** normal
**Source:** 2026-07-17/18.
**Covered by:** q-386 — Independent work actually runs in parallel branches, proven live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.
**Blocked by:** waiting for agent-to-agent messaging support in the tool itself — not his decision, a real absence.
Stays deferred, not far, by its own mechanical trigger: `guardrails/check-listener-tripwire.py`
re-scans every queue-take for a session record naming a live listener (INV-129), and re-opens this
row the day one exists.
```

## Why the premise is stale

JOURNAL.md row 490 (2026-08-XX) recorded the real state at the time: "the harness's socket
plumbing... is built and switched off... addressed push waits on the harness itself shipping a
listener." `guardrails/attic/check-listener-tripwire.py` is a real, already-built, red-proven
one-shot check for exactly this — retired to `attic/`, not deleted, ready to reactivate.

Tonight this session had `SendMessage`/`ListAgents` as live tools — direct agent-to-agent
messaging inside a session is something the harness now supports, at least in the form this
window has access to. Whether that specific capability is the same one q-405/INV-129 was
watching for is not re-verified here (his instruction was to archive, not to re-run the
tripwire) — if it matters again, `guardrails/attic/check-listener-tripwire.py` still exists and
still works; that's the thing to run, not a fresh row re-derived from memory.

## What's not touched

`q-386` (its parent, "Independent work actually runs in parallel branches, proven live") and its
own group ("Parallel & multi-agent work") stand as they were — this archives one row, not the
group's other eight members.
