# Finding: a parked question stays in the waiting list after its answer arrives, and the human is the one who notices

**From:** the tlvphotos window, 2026-07-28 ~21:15. Reported by Alexander in his own words: a question
keeps reaching him that the session later answers by itself after a context reset, and that this has
happened more than once.

## What happened

He was handed a checklist of what waits for him. Two of its items were not his at all:

- **A question the agent then answered itself.** "How far should the overlap sweep reach" stood on the
  waiting board since 2026-07-13. A fresh session re-read the originating wish, found that it names the
  class whole (every interactive control, every covering overlay), derived that the reach needs no
  further word, and closed the item on its own — after showing it to him one more time. His reply: *is
  this a question you are asking yourself?*
- **A question the product had already answered.** "May a phone visitor take a work home" was parked on
  2026-07-08. The long-press ceremony that answers it shipped afterwards. The item stayed on the board
  and rode into every later report. His reply: *of course they may, that is what we built the long press
  for — why is this coming up again?*

## Why the existing net misses both

The deferral re-test fires when a marker is CREATED (`guardrails/check-deferral-marker.py`, base rule 29
and the invariant behind it). Both items passed that test on the day they were written: at that moment
no artifact held the answer. What no rule covers is the SECOND read. The waiting board is a durable file
that outlives the session that wrote it, and every item on it is a claim about the world — "no artifact
answers this" — that decays as the product grows and as later sessions derive things.

The failure is one-directional and invisible from inside: an item that has quietly become derivable
still reads exactly like an item that has not. Only the human can tell the difference, and paying him to
tell it is the defect.

## The shape of the fix, as this window would state it

The re-test belongs at READ time as well as at write time. Concretely, before a waiting board is shown
to a human — or before any of its items is quoted into a report, a checklist or a decision page — each
shown item is re-tested by derivability against the tree as it stands NOW:

- does an artifact answer it today (a spec sentence, a shipped behaviour, a landed test row, an earlier
  answer of his)? Then it is the agent's, and it clears with a citation instead of being shown.
- does the item name the human-only fact it waits on (a taste, a policy, an act irreversible outside
  git)? An item that cannot name that fact today is itself the finding, exactly as at creation time.

The cheap mechanical half: an item on the board carries the date of its last re-test, and a board whose
items were last re-tested before the tree's last landing is stale by construction. The expensive half —
whether an artifact now answers it — is a read, and it is the one the human should never do.

## Provenance

His words, this session, on the tlvphotos checklist. The tlvphotos window also swept its own board the
same session and cleared the two items above; that sweep is the local fix. This note asks for the
method-level one, because a board that shows a human a question already answered is a pack-wide shape.
