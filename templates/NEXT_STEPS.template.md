# [Project Name] — Next Steps

> Digest law: this whole file holds one live-state block and a digest with no redundancy — nothing
> removable without losing information (SPEC INV-48) — one terse line per open leg (its name, what
> stays open, where the detail lives); detail flows to the journal and the queue rows this file
> points at. Compaction moves prose to its home; it never drops an open leg.

**This is a resume file.** It holds ONLY the current live state + the forward queue. When a new movement lands, REPLACE the live state block. Never stack entries. Dated history and the WHY live in JOURNAL.md.

---

## LIVE STATE (YYYY-MM-DD)

[One paragraph: where the project is right now — what was last shipped, what is green, what is not yet done. Enough for a cold start without reading anything else.]

[If any in-work row carries several enumerated legs: name each leg met/open — an open leg is restated here at every update, never compressed away (SPEC INV-26).]

## Forward queue

1. [Next action, specific enough to start immediately]
2. [Item 2]
3. [Item 3]

Memory can be wiped after this message — NEXT_STEPS.md + JOURNAL.md have the full resume trail.
