## The change record — classify every touched code and hold the size ratchet

A spec-touching delivery carries a **delta record**: a JSON file under `docs/deltas/` (one per delivery,
e.g. `docs/deltas/2026-07-22-row445.json`) naming every code — every bracket anchor such as `INV-18` —
the delivery touched and, for each, exactly one of four kinds. A code names the criterion that carries
it, so classifying a code classifies its criterion. The kind names are fixed — they are what the
classifier gate `guardrails/check-delta-record.py` reads:

- **new** — a code the body of the spec did not carry before;
- **sharpen** — a code whose criterion text changed;
- **retire** — a code the body no longer carries;
- **scenario-only** — a code whose criterion text is unchanged, where only the material around it moved:
  its case grouping, its Context prose, or an example. In this one fixed label, "scenario" means those
  surroundings of the criterion; it does not carry the person-facing-requirement sense the body of the
  spec uses.

The classifier diffs the old criteria set against the new one under normalization — whitespace collapsed,
italic markers stripped, case folded outside code anchors — and reds where the record and the diff
disagree — an added code with no `new` declared, a
vanished code with no `retire`, a changed criterion with no `sharpen`. A `sharpen` also proves the old
sentence no longer survives anywhere in the new document. The delivery's measured criterion-byte growth
(excluding sharpen deltas and glossary additions) stays within the sum of the byte counts of its declared
new criteria.

Beside the per-delivery record, the whole spec holds a **bytes-per-criterion ratchet**: the byte count of
its criterion lines alone, divided by the count of criteria, recorded in `guardrails/spec-ratchet.json` and
held by `guardrails/check-size-ratchet.py`. A delivery may lower the bound or leave it; a delivery whose new
bytes-per-criterion rises above the recorded bound reds. Raising the bound is a change to the spec's own
size requirement, run through the pipeline, never a side effect of a landing.

