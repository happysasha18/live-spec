# [Project name] — Plan

The one list: what this project is for, what is asked of it, and where each ask stands. A wish is a
request for a change the product does not yet carry. A wish lands when the delivery that completes
it ships. Intake is continuous, a wish entering the list the moment it is spoken. Execution runs at
most the lane cap of independent landings at once, three by default, so up to three rows may read
*in-work*. A landing finishes before a colliding next one starts, and two landings collide when they
rewrite one clause or one behaviour's rule.

**One list, and never a second.** The plan and the queue are this one document. A felt need for
another list — a session plan, a lane plan, a task file of its own — says a row belongs here. Two
lists drift the moment one of them is edited alone, and then neither answers where the work stands.

The plan is a member of the format family. Its shared rules live once in `docs/spec-format.md` and
hold here unchanged:

- the closed-vocabulary glossary;
- the keyword form;
- the no-capitals rule;
- the trailing code anchor;
- the no-history law;
- the comprehension gate.

Its own rules are defined in full in `docs/roadmap-format.md`, which is their one home:

- the row shape;
- the status and class vocabularies;
- the live-body law;
- the row lint.

Read that page before editing this file. The sections below show the shape those rules take in a
row.

The keywords *when*, *if*, *then*, and *shall* are set in lowercase italics where a row's acceptance
cell uses them. A bracket code trailing a line, such as `[INV-277]`, points to the rule's home in
`PRODUCT_SPEC.md`. A reader may ignore it, and a maintainer follows it.

## The goal

[What this project is for, in the words its owner used. One paragraph. Every row below earns its
place by moving the project toward this; a row that moves nothing here is a row to decline.]

## Glossary

[Domain nouns this list's own rows use, each with a one-sentence definition. A word of ordinary
English needs no entry.]

## The body

The table below is the body: the live list, one row per open wish, the rows standing in ascending
id order. A rotated-manifest block sits above the body, one line per monthly archive file. Each
line names the rows that moved and the file that received them. A hand writes both halves — the
archive file and its manifest line — in one act, and the doc-rotation gate proves both directions.

<!-- rotated-manifest -->
Rotated closed rows (the archive keeps every moved row, grepable by number; the body below holds
only the live list):
- rows [ids] → docs/queue-archive/rotated-PLAN-[YYYY-MM].md
<!-- /rotated-manifest -->

| # | Wish (plain words) | Class | Status | Decision / acceptance |
|---|---|---|---|---|
| 1 | [Wish in plain producer/user language]. Asked by [name], [date]. door: [feature / bug / refactor / docs-only / skip] · kind: [product / infra / skill / prose] · footprint: [presentation-only / single-module / cross-cutting] · map: [architecture node] · entry: [entry condition, where one applies] | small | *queued* [date] | [Done-when criteria and non-goals, code anchors trailing at the line ends] |
| 2 | [Second example wish, its delivery split into two legs]. Asked by [name], [date]. door: feature · kind: product · footprint: single-module · map: [architecture node] · priority: quick win | surface | *in-work* [date] | [Leg one: done — ...; leg two: open — ...] |

Both rows above are invented placeholders, shown to teach the shape. A new plan starts with row 1
held open for the first real wish.

## The wish cell

The wish cell carries three things:

- **the ask**, in plain producer or user language;
- **its provenance** — whose word asked for the wish, and the date;
- **the intake notes**, which name the wish's door, kind, footprint, map placement, and entry
  condition.

The intake notes read as one run of labelled fields:

- door: feature · bug · refactor · docs-only · skip;
- kind: product · infra · skill · prose;
- footprint: presentation-only · single-module · cross-cutting;
- map: the architecture node the wish lands in;
- entry: the entry condition, where the wish declared one.

A priority mark rides the intake notes when the wish's priority stands other than normal. There are
two marks. **critical** says the shipped product is broken for its user, and the row lands before
everything else. **quick win** says the work is low effort and immediate value, free to bubble up
between landings with the jump named in the row. Ambiguous size or priority is asked at intake,
never guessed.

## The class cell

The class cell carries one word of the closed size vocabulary, one vocabulary shared with the spec:

- **bug** — something shipped is wrong;
- **small** — one landing, with no new surface;
- **surface** — a new stateful user-facing surface, entering the pipeline in full;
- **large** — a wish that decomposes into several landings.

## The status cell

The status cell carries one word of the closed status vocabulary, each set in lowercase italics and
carrying its date:

- *queued* — the wish is accepted and waiting its turn.
- *in-work* — the wish is claimed by a session.
- *deferred* — the wish is parked on a named revisit trigger, the trigger written in the status
  cell.
- *far* — the wish is parked with no near trigger.

A row whose wish carries more than one leg stays *in-work* while any leg remains open, the open leg
named in the acceptance cell. The row reaches a terminal exit only once every leg is closed, since
a row closes only whole. [INV-26]

## The live-body law

The body holds live rows only. A row reaching a terminal exit moves verbatim from the body to the
month's file in the archive. It moves in the same commit that closes it, its delivery report riding
with it. The terminal words are *landed*, *declined*, *superseded*, and *decided*; the last names a
row that exists to settle a question. The word *landed* names that transition a row makes, and a
body row never carries it as a status.

An archive file gathers one calendar month's moved rows, and the rotated-manifest block above the
body grows one line per archive file. A *deferred* or a *far* row stays live in the body. Its
revisit trigger is re-read at the next milestone review, and again whenever a session takes its
next wish from this list.

Declining a row that absorbed other wishes lists the absorbed rows. Decline each listed row by name,
or return it to the list as its own row — a superseded wish never dies by pointer. [T-8]

## The acceptance cell

The acceptance cell carries the done-when criteria and the non-goals, with code anchors trailing at
the line ends. The spec's Context blocks and User Stories stand down from the row. The spec owns
them and stays their one home, and the row points at the spec by anchor.
