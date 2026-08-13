---
name: feedback-collector
description: Use, only if enabled, when the user shows a rare, strong reaction (delight or frustration) to offer drafting a private note to the pack's authors. Consent is asked every time, and the skill never sends the note — delivery is the human's own step.
metadata:
  version: 5.0.0
---

# feedback-collector — an occasional note home to the authors

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live
> ONCE in the pack's base skill, `live-spec-base` (v5.0.0), together with the settings ladder — this skill
> references them and elaborates only its own domain. Used standalone, this note is plain advice.

The pack moves feedback in three directions. communicator carries work OUT to the human. feedback-intake
carries what a person hands BACK. This skill carries an occasional note UP — to the people who wrote the
pack — so they learn what delighted or hurt real use. It is the outbound feedback arm, and it moves rarely
and only with the human's explicit word. Spec home: `PRODUCT_SPEC.md` E-30 / T-21 / INV-161.

**Where the paths in this file point.** Every path here belongs to the project the pack is attached
to. That covers `FEEDBACK.md`, `outbox/`, and `PRODUCT_SPEC.md`. The pack's own machinery sits in the
live-spec repository, at `github.com/happysasha18/live-spec`. After an install, `live-spec-base` sits
as a folder beside this skill's folder.

## Before anything: the flag

The arm is **off by default**. It reads nothing, offers nothing, and stays wholly silent unless the host
has turned it on with a recorded profile line:

```
- `feedback-upstream: on`   # this host sends occasional notes up to the pack's authors (dated)
```

A host that adopted the pack switches it on to send notes up. The authors' own origin machine leaves it
off — it has no upstream above it. Off means off: no reading for a strong moment, no offer, no note. Read
the flag first, every time (settings ladder, `live-spec-base` E-13).

## When it fires

With the flag on, the arm fires on **one genuinely strong, unmistakable reaction** — a real delight, a
real hurt, a comparably notable moment. It fires rarely by design: on a clear signal, and silent on a mild
or routine reaction. The reading of "strong" is a conservative floor here — take only the unmistakable, and
when in doubt, stay silent. (The finer reading
of the signal is its own later design pass; this v1 leans hard toward silence.)

## Work that belongs elsewhere

It stays silent — no offer, no note — on:

- any reaction below the unmistakable bar (mild, routine, ambiguous — the default, and the common case);
- the agent's own output or a question the agent asked;
- a host that has not turned the flag on;
- a moment the human hands in as ordinary feedback (feedback-intake owns that route).

When the human HANDS the reaction in — a comment on shown work — the two skills do separate parts of the
work. feedback-intake logs its field-evidence ledger line. This arm, if the moment reads as strong, offers
the upstream note (`PRODUCT_SPEC.md` E-30, T-20 route 4).

## The offer — positive consent, every time

On a qualifying moment, OFFER in one short line, in the conversation's own language, and ask for a positive
yes. Example (English; mirror the chat's language):

> That landed as a strong moment. Want me to draft a short note to the pack's authors about what happened
> here — what worked or what hurt? Nothing leaves without your explicit yes; it drafts privately to your
> `outbox/`, nothing public.

Consent here is a **positive word, asked every time**: the note is written only on an explicit yes. The
pack's usual silence-is-consent default (`INV-31`) does not apply here, because this is an outbound move
about a real person. A silence, a shrug, or an unclear answer leaves the note **unwritten**. Only an
explicit yes writes it.

## The upstream note — distilled, non-public, deposited

On the yes, write **one upstream note** and deposit it. The note is:

- **distilled** — the point of what happened, and only the point; never the transcript, never a script,
  never the user's private content past what the point needs;
- **self-contained** — it carries its own context, so a reader upstream who does not know this user
  understands it on its own;
- **a courteous private request** — shaped for the authors who will read it, and meant to stay private;
- **anonymized** — the host's real entities are masked before the note leaves the draft (SPEC INV-179).
  A person's name, the company or client, an internal product or repo name, a file path, a customer's
  data: each becomes a neutral role word ("the owner", "a client project", "an internal repo"). The
  masking is part of the draft the user reads at consent, so what they approve is exactly what would
  travel. The pack's own public names (skill names, invariant codes) stay. An enterprise host makes this
  a hard law: a note that leaks an internal name cannot be sent there, and a note masked after the yes is
  a different note from the one approved.

Example note (the shape to follow):

```
# Upstream note — 2026-07-15

What happened. A user shipping a batch of queue items hit real delight when the
pipeline's standing net caught a stray citation their hand-edit had missed — the
automated guard paid off visibly, in front of them.

What it tells the authors. The forward-binding net earns its keep on first
contact; the "net catches what the hand misses" moment is worth keeping as the
pack grows.

Context for a reader who wasn't here. live-spec is a spec-driven pipeline pack;
the user was mid-way through a release. No transcript or private content is
included — the distilled point only.

— drafted for the authors, private; delivery is the user's own step.
```

## outbox/ — where it lands, and where the pack stops

Deposit the note into the host's `outbox/` directory:

- **gitignored** — `outbox/` never rides a push; a private note must not travel with the repo;
- named by date (`outbox/upstream-note-YYYY-MM-DD.md`, a same-day suffix when a second lands);
- **cleared once the human has delivered it** — a step the human owns.

The pack's side ends here. It opens **no** network connection and **no** public request on its own —
sending outward is the human's gate (`live-spec-base` rule 17). Delivery upstream is a separate step the
human takes, however they choose (a private message, a private pull request, whatever they name).

## The local record

Record the offer and its answer as one dated line in the host's `FEEDBACK.md` — a sixth line-kind beside
feedback-intake's five routes (`INV-68`):

```
- 2026-07-15 · upstream-note offer · answered yes · outbox/upstream-note-2026-07-15.md
- 2026-07-15 · upstream-note offer · answered no · (no note written)
```

## What it is not

- **Not feedback-intake.** That skill RECEIVES what a person hands in and routes it home; this NOTICES a
  strong moment the agent observed and OFFERS to carry a note up. Opposite directions. It occupies exactly the
  "never on the agent's own output" seam feedback-intake leaves open (`T-20`).
- **Not a measurement machine.** It reads one moment and offers; it does not score, grade, or aggregate
  sentiment across a conversation or across notes. Reading machinery — plugins, aggregation — stays with
  the measurement family (`INV-21`, deferred).
- **Not an auto-sender.** No yes, no note; and even on a yes, no send — a deposit only.
