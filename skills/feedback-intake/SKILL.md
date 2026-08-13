---
name: feedback-intake
description: Use whenever feedback arrives — a comment, answer, file, or reaction from a person, a file appearing in inbox/ (whoever put it there, person or agent), an inbox sweep, or an append to the feedback ledger FEEDBACK.md — and route it to where it belongs.
metadata:
  version: 4.3.0
---

# feedback-intake — nothing handed in is ever lost

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live ONCE in the pack's base skill, `live-spec-base` (v4.3.0), together with the
> settings ladder — this skill references them and elaborates only its own domain. Used standalone, this
> note is plain advice.

A person looks at what shipped and something occurs to them — a reaction, an answer, a screenshot with
a red circle, a log file. **Feedback** is anything a person hands back to the project: any size, any
moment, any channel (SPEC E-28). The person is usually the project's human; when the project's product
has users of its own, their reports follow the same route once a session receives them. This skill owns
what happens next: every received item lands, the same session, in the home its route owns — and the
person hears where it went.

**Where the paths in this file point.** Every path here belongs to the project the pack is attached
to. That covers `FEEDBACK.md`, `inbox/`, and `.live-spec/PROBLEMS.md`. The pack's own machinery sits in
the live-spec repository, at `github.com/happysasha18/live-spec`. After an install, `live-spec-base`
sits as a folder beside this skill's folder.

## When it fires

The moment any session receives a handed-in item, and at every inbox sweep, for the files that carry
feedback. A file that carries a wish goes through the door. It fires in ANY session. An unassigned
session cannot write the host's files, so its intake move is the inbox door: one new file, committed,
swept later by the host's own session.

## Work that belongs elsewhere

Never on the agent's own output or on a question the agent asked. Never on something the human merely
mentions without handing it in. When it is unclear whether a remark was handed in, one plain question
settles it. And it never opens a queue row on its own judgment: the door owns that verdict (SPEC
T-12); this skill only recognizes that an item is wish-shaped and walks it there.

## The three channels (SPEC T-20)

- **Spoken or typed** — a remark in the conversation, or a note in a file the person points at.
- **A comment on something shown** — decision pages and review pages already capture answers as saved
  JSON (SPEC INV-4, INV-64); each saved answer is a feedback item whose home the capture law already
  names (the archive and its harvested row).
- **A dropped file** — a screenshot, a log, a document: handed over in the conversation, or arriving
  from any outside session through the host's inbox door (one NEW file per item, the wish files' own
  naming and collision law, SPEC E-11). A file arriving with no words gets one plain question about
  what it means; a guess is never written into the ledger.

## The routing table — every item takes exactly one route, every route has a home

| What arrived | Route | Home |
|---|---|---|
| an item asking for new behaviour | it is a WISH — walk it through the door: arrival, echo, row (SPEC T-12) | its queue row |
| a fix-sized comment on shown work | FIXED the same session; a story-sized comment queues as a wish | the fixing commit + its journal line |
| an answer to an open question | CLOSES it, harvested the same session (SPEC INV-59) | the decision archive + the harvested row |
| a reaction to a shipped feature | FIELD EVIDENCE — the line cites the feature's scenario; the feature's success measure (SPEC INV-21) gains real signals | a dated feedback-ledger line |
| workshop noise (a flaky tool, a missing dependency) | the problem ledger's law (SPEC INV-23) | `.live-spec/PROBLEMS.md` |

What separates the two ledgers is the subject: the product's behaviour goes to FEEDBACK.md, the
workshop's goes to PROBLEMS.md, one home each. Field evidence grows into a wish only by the human's
word or a tripwire verdict.

## The feedback ledger (FEEDBACK.md)

The routes above that had no home before this skill — field evidence, plain reactions, wordless files
still waiting for their question — get one: **FEEDBACK.md**, an append-only file beside the queue at the host
root. One dated line per item: when it arrived · who handed it in and through which channel · what it
concerns on the feature map · the item in plain words · where it went. The ledger begins
with a two-line header naming this law; a ledger holding only its header is healthy. It archives
like the queue and is never trimmed (SPEC INV-1). Only the assigned session writes it; outsiders use
the inbox door (SPEC INV-10), and an append follows the concurrent-edit fence like any shared-doc edit (SPEC T-18).

## The receipt discipline (SPEC INV-68)

- Every arrival is echoed back in one sentence — **one echo per item**. A wish-shaped item's echo IS
  the wish echo (SPEC INV-27); every other item hears what was received and where it went.
- A re-mention of an already-recorded item **appends its date** to the existing line and changes
  nothing else — the problem ledger's own discipline, applied here.
- The ledger line is written the same session the item arrives; at an inbox sweep, ONE commit both
  lands the route (the row, the ledger line) and removes the swept file (SPEC T-10). The sweep reads only
  a complete deposit. It passes over a `.draft`-suffixed file a neighbour may still be writing, so it never
  harvests or removes a mid-write deposit. A `.draft` file left stale across a full sweep — its mtime
  unchanged and its writer gone — is removed the same way a harvested file is, so an abandoned draft never
  lingers (SPEC INV-249).
- Dates come from the clock, read at the moment of writing, never invented (SPEC INV-24).

## What this skill deliberately leaves alone

No end-user feedback widget on a host's own product. When a site's visitors write in, that belongs to
the measurement family — the pack's deferred measurement machinery — under its own queue row, or it arrives
relayed to a session. No automatic reading, scoring, or aggregation of the ledger; that reading work
stays a named target of the measurement family. No new inbox-door mechanics — the inbox is reused
exactly as it stands.

> The pack, whole: **live-spec-base** holds the shared rules and defaults · **spec-author** writes the spec ·
> **product-prover** reviews it · **product-prover-pack** binds the external prover to the pack · **design-reviewer** judges the design behind it · **build-pipeline** ships the change · **test-author** derives the matrix
> and writes the tests · **communicator** makes the human exchange land · **feedback-intake** brings what
> comes back to its home · **feedback-collector** offers a rare private note up to the authors · **text-audit** reads a text as a stranger and fixes where they stop · **publish** sees the work out the door, owing its kind's checklist.
