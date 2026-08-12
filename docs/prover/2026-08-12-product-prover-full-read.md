# product-prover — one full read by the orchestrator seat, 2026-08-12

Prover skill version read: 4.3.0 (`skills/product-prover/SKILL.md`, 67,412 bytes;
`skills/product-prover/README.md`, 11,360 bytes). Both read whole. Root: his standing ask,
restated 2026-08-12 08:18.

Every finding below was checked against a primary source — the pack's spec, its gates, its own
tree — never against the skill's prose alone (base rule 13).

---

## F1 — The record filename the skill prescribes is refused by the pack's own push gate

> "Persist the findings. They are written to the project's `docs/prover/YYYY-MM-DD.md`"
> — Meta rules, `skills/product-prover/SKILL.md:969`

`guardrails/check-prover-record.sh:131` tells the author the opposite:

> "Fix: run the product-prover pass and save its record as $PROVER_DIR/$TODAY-<slug>.md, then commit it."

An author who follows the skill writes `docs/prover/2026-08-12.md`. Two things go wrong. The push
gate names a different path in its own repair line, so the author is sent looking. And a second
pass on the same day overwrites the first pass's record, taking with it the folded-or-rejected
column the skill's next paragraph says makes the fold verifiable after a memory wipe.

The pack's own tree already votes: `docs/prover/` holds 381 records and 380 of them carry a slug.
Only `2026-07-04.md` follows the skill as written. Every real pass has silently overridden the
instruction.

Fix: the meta rule reads `docs/prover/YYYY-MM-DD-<slug>.md`, the slug naming the pass, matching the
gate's own repair line. Sweep the same sentence in `editions/product-prover/SKILL.md`.

`defect · direct-contradiction (contradiction)`

---

## F2 — The declaration member of the composition-lens family has no lens in the prover

> "The system *shall* read this as the declaration member of the composition-lens family."
> — `PRODUCT_SPEC.md:6330`, criterion 5 under INV-226

Phase 3e carries five members of that family: edge-condition completeness (INV-138),
cross-surface policy uniformity (INV-125), paired-transition symmetry (INV-126),
interactive-overlap (INV-136), delivery separability (INV-248). INV-226 is declared a sixth member
by the spec and appears nowhere in the skill: the strings "enumerate-or-ride", "member set" and
"open-ended" return no hit in `skills/product-prover/SKILL.md`. No test pins it there either —
`tests/test_instance_enumeration_keying.py` asserts nothing against the prover.

Consequence: a spec under review states a general duty over a closed, nameable member set and names
no members. INV-226 calls that the defect it keys. Every prover pass reads clean, because no lens
asks the question, and the unnamed members ride the general duty unreviewed. The reviewing author
learns of the gap only when a member behaves unlike its siblings in the shipped product.

Fix — a decision, so it earns a queue row rather than a same-session edit. Two answers:
a. a sixth mandatory sweep, "declaration": for every general law in the document, is its member set
   closed or open-ended, and does the clause enumerate or ride accordingly? Cost: the count "five
   mandatory sweeps" is pinned in `PRODUCT_SPEC.md:1632`, the README, the public edition and its
   examples, so this walks the pipeline.
b. one sentence in the skill saying INV-226 is the spec-author's authoring duty and carries no
   prover lens, by name. Cheaper, and it leaves the spec's "member of the composition-lens family"
   sentence claiming a lens the family's carrier does not hold.

Preference: (a). The spec's own word for the failure is "defect", and defect is the prover's verdict
to issue.

`defect · missing-rule (invariant)`

---

## F3 — "The whole-document property sweep" is an undefined term, and it decides what a surface add skips

> "This mode skips the whole-document property sweep, and it keeps one whole-document step: the
> quantifier re-verify (SPEC INV-170)." — Review modes / CROSS-LINK, `skills/product-prover/SKILL.md:299`

The phrase appears twice in the whole repository — that line and its twin in
`editions/product-prover/SKILL.md:322` — and is defined nowhere. The document's "Words this skill
uses" section defines lens, sweep, station, fold and five more, and leaves this one out.

A session running CROSS-LINK on a surface add cannot tell what it is skipping. Three readings are
open: Phase 3's property analysis 3a–3d; the five mandatory sweeps of 3e; or the
declared-cross-cutting-laws sweep alone. The readings differ where it costs most. That sweep's two
demands are "a clause per surface" and "a test per surface (P9)" — and a newly added surface is
exactly the thing that has neither. Read the term wide, and the mode skips the one check the add
most needs, while the surface × sweep table renders a row for a surface no sweep visited.

Fix: name what is skipped and what runs. Proposed sentence: "This mode skips Phase 3's
whole-document property analysis, 3a through 3d. Every mandatory sweep of 3e runs, scoped to the
new surface and its seams, and the quantifier re-verify runs whole-document (SPEC INV-170)."

`defect · undefined-path (transitions)`

---

## F4 — The class lens is a base rule shelved in the tier that owes nothing

The class lens sits under "Imaginative probes", whose opening reads:

> "imagine actively, past the reach of pattern-matching. These are habits of attention. No checklist
> ticks them off, and no verdict is owed" — `skills/product-prover/SKILL.md:739-740`

Base rule 14 is not a habit of attention:

> "A found defect is a sample of its class — go find the class, sweep the look-alikes. ... before
> calling the fix done, name the pattern behind the instance abstractly ... Then search the whole
> repo and every user-facing surface for that kind, and fix all siblings in the same change."
> — `skills/live-spec-base/SKILL.md:263`

Consequence: a FULL pass files a point finding, skips the class sweep, and owes no line saying so.
INV-171 split Phase 3e into two tiers precisely so a skipped check stays distinguishable from a
check that found nothing — and the class lens landed on the side where that distinction is gone.
The author reads a record with no class line and cannot tell whether the sweep ran clean or never
ran. `tests/test_class_hunt.py` asserts only that the words "Class lens" appear in the skill, so the
suite is green on a prover that never sweeps.

The public README compounds it: it lists the imaginative tier as "ties, concurrency, bounds,
dependency failures, and dangling references" (`README.md:92`) and never mentions the class lens, so
a standalone user never learns the pack's own strongest habit exists.

Fix: the class lens fires on a finding rather than on the document, so it is no per-surface sweep.
Give it its own line in the tier's opening — every finding filed carries a class answer, and the
record carries one class line per pass, reading swept / no class / not-applicable-with-reason. Add
it to the README's list of what the pass does.

`defect · hard-to-monitor (observability)`

---

## F5 — Six bullets stand under a stated five

> "The parent gathers five angles:" — Lifecycle sweep, `skills/product-prover/SKILL.md:635`

Six bullets follow. The count is defensible: the first bullet is transition payload, which is the
parent itself, and the five gathered angles are entry symmetry, entry state, paired-transition
symmetry, persistence and versions, and scenario entry and exit. Queue row 344's own record confirms
that reading.

It still stops a reader, and the skill's meta rule says a release's own lenses run against its own
body, naming the count-versus-contents lens by name. This is that lens on this document.

Fix, one line: "The parent below, and the five angles it gathers:". Sweep the public edition.

`recommendation · now · confusing-for-users (cognitive-load)`

---

## What I assumed

- That `editions/product-prover/SKILL.md` is a hand-maintained public standalone edition rather than
  a generated copy — `scripts/sync-mirrors.sh:70` describes it as a public edition a skill "may ship",
  and the two files differ by 1,312 diff lines including the front matter version, 1.0.0-standalone
  against the pack's 4.3.0. Every fix above therefore names its sweep into the edition separately.
  If the edition is meant to track the pack automatically, that assumption is wrong and the sweep
  instruction changes.

## Noted as sound

- The seven architecture-lens checks in Phase 0 count seven, and the paragraph that stands one down
  when no PRODUCT_SPEC is in reach says "run the remaining six". The counts agree.
- Every formal term in the category table has a glossary entry. Eighteen terms in the table, and the
  glossary carries all eighteen plus safety.
- The two INV-114 citations, at lines 184 and 397, look like one code carrying two unrelated claims.
  They are both correct: INV-114 indexes R184.1 through R184.5, and criterion 5 is the
  bar-interpretation rule while criteria 1 through 4 are the delta-scoped merge gate.
- ROADMAP row 204, cited at line 378 as the home of the wish for a token-identity script, is real and
  still queued.

## Where these landed

Each finding has a queue row, opened 2026-08-12: F1 is row 608, F2 is row 609, F3 is row 610, F4 is
row 611, and F5 is row 612. None of them was repaired in the same landing as this record, because
every one edits a skill body, which draws a fresh skill-creator review record and a full suite run
before it can be pushed. The next pass takes them in that order: 608 and 610 are one-line textual
fixes with their answers already written above, 612 is a lead-in reflow, and 609 and 611 carry a
decision each about what the prover owes a verdict for.
