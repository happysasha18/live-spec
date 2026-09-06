# Archived off PLAN.md: a deferred row whose trigger nobody can make fire

Date: 2026-09-06. `q-385` waited on one named event — the first host declaring a contract in its own
card. The event is checkable, which is why the row was allowed to stand deferred where `q-811`'s
"a real ask for it" was not. Checked again tonight, the event has not happened and nothing in this
project's reach can make it happen.

## The evidence, read tonight

Twenty-six adopted projects carry a `.live-spec/agent.md`. Every one of them says the same thing
under **Contracts this agent publishes**:

| Project card | "Contracts this agent publishes" |
| --- | --- |
| `~/live-spec/.live-spec/agent.md` | "None. This agent publishes no data feed today, so no consumer pins a version against it." |
| `~/promoter/.live-spec/agent.md`, `~/promoter-alexander/.live-spec/agent.md` | "None today." |
| `~/tlvphotos/.live-spec/agent.md` and the twenty-two other `tlvphotos-*` / `tlv-hand-u4` trees | "None today. The built public site is an output, not a data feed a consumer pins a version against." |

Read with: `for f in ~/*/.live-spec/agent.md; do awk '/Contracts this agent publishes/{flag=1} flag{print}' "$f"; done`.

## Why it is declined rather than left deferred

The row's own definition of done says "red-proven against a real producer and consumer." There is
no producer and no consumer. The three arms could only be proven against a fixture, and a fixture
producer is exactly the synthetic proof this project's own rules refuse — a gate anchored on
something built for the gate says nothing about the world. So the row cannot be finished honestly,
and its trigger has no owner: nothing on this board or in any host's plan is working toward a first
published contract, and the pack does not decide for a host what data it publishes. A promise with
no builder and no date is not a commitment; it is a queue entry that reads, to anyone glancing at
the board, exactly like work somebody had taken on.

## What was retired with it, and what was kept

Retired, all in the same commit:

- `spec/public-contract.md` Requirement 194 criterion 15 and its case heading — the promise of the
  producer-side default-deny gate, and the `[target]` marker under it. Excerpt verbatim:
  `attic/spec-public-contract-R194-C15.md`, with its line in `attic/MANIFEST.md`.
- `"INV-185": "q-385"` from `TARGET_ROW_OWNERS` in `tests/test_traceability.py`, per SPEC S-0 —
  a satisfied or retired promise leaves both the tag and its map entry, in one commit.
- The `(ROADMAP row 385, [target])` clauses inside `matrix/spec-author.md` M-362 and M-364, which
  named this row as the owner of the unbuilt mechanical arms.
- The same claim in `tests/test_agent_channels.py`'s module docstring.

Kept, untouched and still proven:

- The default-deny **law** itself — Requirement 194 criteria 4, 5 and 6 — with `M-362` at `string`
  level and `tests/test_agent_channels.py::TestDefaultDeny`.
- The consumer's read law — criteria 9 to 12 — with `M-364` and `TestConsumerRead`.
- The read grant (`INV-232`, `scripts/read-grant.py`) built by row 389 and untouched by this.

## When it comes back

Requirement 194's own Context carries the one line: when a host first publishes a real contract,
the gate is admitted then, through `python3 scripts/task-admission.py`, with its definition of done
written against that real producer and that real consumer. That is where whoever authors the first
contract lands — criterion 1 of the same requirement sends them there — so the note sits on the
page they will already be reading. Never by resurrecting this row.

## Index

One line for the archived row, findable by its own number.

| # | Wish (plain words) | Class | Status | Decision / acceptance |
| --- | --- | --- | --- | --- |
| 385 | A broken promise between two projects is caught automatically | surface | declined 2026-09-06 | its trigger — a host publishing a first contract — has not fired and no work anywhere is aimed at making it fire; all twenty-six agent cards read "None today", so the three arms have no real producer or consumer to be red-proven against and the row could not be finished honestly. The spec criterion and `[target]` marker it held open retired with it |

---

### ⬜ A broken promise between two projects is caught automatically — id: q-385
**Group:** Cross-project · **Priority:** normal
**Source:** split 2026-07-17.
**Deferred:** the first host declaring a contract in its card, the revisit trigger carried from the
original row. No host has declared one yet, so this stays queued rather than in hand.

**Reopened 2026-09-01.** Folded into q-398 on 27.08 ("Covered by: q-398 — A request meant for
another project reaches it automatically") and rotated off this board on 28.08. q-398 landed
2026-09-01 doing only its own stated acceptance — the routing-preamble hook (INV-190) — and never
touched this row's own promise, the same shape q-437 was found in on 31.08. The spec still carries
this as a deferred item in its own words: `spec/public-contract.md`, Requirement 194 criterion 15,
"the gate that reds a default-deny violation on the producer's suite *shall* stay promised until a
host's first real contract" [INV-185] [target]. A promise nobody is building stands here as its own
open row rather than inside a task that closed without it. Original wording, as row 385:
`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`.

**Definition of done:** three arms, red-proven against a real producer and consumer — a
producer-side gate reading the card's declared contracts and redding a published field with no
dated permission record [INV-185]; a consumer-side freshness check redding an artifact past the
consumer's declared staleness bound before any analysis [INV-187]; and a compatibility test redding
when the pinned version and the artifact's version diverge [INV-187]. The permission record's own
format lands with them, one home in the producer's tree.
