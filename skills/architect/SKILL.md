---
name: architect
description: Use to write or update ARCHITECTURE.md from a proven spec — the node structure a project's kind proposes, file:line pins reconciled with shipped code, measurable quality budgets, the runtime and placement views, and the fitness test every new or carved node must pass. "Here's a proven spec, produce or update the architecture" is a complete task on its own — invoke this skill directly, not only as a step inside a larger pipeline.
metadata:
  version: 5.0.0
---

# architect — from a proven spec to the structure that carries it

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live ONCE in the pack's base skill, `live-spec-base` (v5.0.0), together with the
> settings ladder — this skill references them and elaborates only its own domain. Used standalone, this
> note is plain advice.

Every project's spec eventually needs a structure to live in: named units, each with one job, each
owning the spec facts it implements, wired together by named seams. `ARCHITECTURE.md` is that
structure. Deriving or updating it from a proven spec is a bounded, self-contained task — a human can
hand this skill a spec and ask for a structure, the same way they can hand `test-author` a proven spec
and architecture and ask for a matrix. This skill does that one job.

**Where the paths in this file point.** `templates/`, `guardrails/`, and `scripts/` name the live-spec
pack's own files, at `github.com/happysasha18/live-spec` — after an install these sit beside this
skill's own folder. Every other path belongs to the project under work: `PRODUCT_SPEC.md`,
`ARCHITECTURE.md`, `docs/prover/`, and the project's own source tree.

## What this skill owns

One artifact: **`ARCHITECTURE.md`** (template: `templates/ARCHITECTURE.template.md`), derived from a
proven `PRODUCT_SPEC.md`. Named nodes, one responsibility and one name each. Every spec fact owned by
exactly one node. Named seams between nodes, each stating what crosses it and who owns the format. A
**node** is one named unit in the document, carrying one responsibility, owning the spec facts it
implements, and pinning them to the code. A **seam** is the named boundary between two nodes.

A large or surface-class change updates the document before the matrix is touched. A bug or a small
change just cites its existing node and moves on — running the pin-greps that confirm the citation is
mechanical work, judging what a mismatch means is not.

## The node structure — the project's kind proposes it, the spec's facts decide it (SPEC INV-36)

`project.kind`, set once at founding or adoption, PROPOSES a starting node structure — a scaffold to
fit, not a verdict. A fullstack app splits into frontend / backend / template or renderer / store. A
backend service splits into entry-and-handler / domain core / data store / each external integration. A
CLI or library takes one node per public surface. A skill pack takes one node per skill, plus the shared
rulebook, the templates, and the guardrails as nodes of their own. A book or content project usually
takes one docs node until the structure genuinely grows. The full per-kind table, including where each
kind's composition bugs tend to hide, lives in the template's "Node structure by project.kind" section —
read it before proposing nodes for an unfamiliar kind.

Two shapes the plain table misses. A **derive-pipeline tier**: a data-heavy or machine-learning build
that chains through several intermediate data contracts (`raw → catalog.json → vector.json →
render-data.json`) gives each stage its own node and names the contract between them — collapsing several
derive steps into one node hides that many undocumented contracts. **Blended kinds**: a static-first
project can still carry one narrow edge-worker node holding secrets and every verdict kept off the
client — name it its own backend node and name its private-data seam, and call the kind
"fullstack, static-first."

The spec's facts then decide the final nodes. A node earns its place only by owning a spec fact; a node
with none is unbacked structure, and the prover flags it. Two projects of the same kind can end with
different node maps, because their specs differ.

## Pinning to shipped reality

In a live codebase, every node pins to its owning `file:line`. **This is where the spec is reconciled
with reality.** Each pin comes from a command actually run — a grep, a read — never from the document's
own prose, memory, or a worker's summary; those are leads to verify, not facts (base rule 13). Specs
drift from code over a project's life; when they disagree, the spec is fixed to the shipped truth,
always in that one direction, never the reverse. In a new project the pin list is a single dash until
code lands.

## Quality budgets (SPEC INV-41)

The document owes numbers as well as names. Before writing any budget, ask what quality MEANS here, in
numbers — and that answer comes from the project's kind (SPEC INV-36): a user-facing product measures
paint and interaction times ("first image within 2s on a cold visit"); a backend service measures
latency, throughput, and error rate; a CLI or pipeline measures run time on a typical input and
per-unit cost; a skill pack measures its evals' pass rate and suite wall-time; prose states honestly
what carries no number, by name, rather than inventing a vanity metric for it. See
[references/architecture-step-detail.md](references/architecture-step-detail.md) for this passage in
the words the step first used.

Each budget names its **instrumentation home** — where the real number is measured and where a human
can read it: an export, a debug view, a report — and its **watcher**: the mechanical check that reds
past the stated number, or, where none exists, the decided sentence saying why that budget is read by
eye instead. A surface with no budget line and no instrumentation home is a derivation defect, exactly
like an unowned spec fact. The numbers themselves are the host's taste: propose each with a
recommendation, and set it on the human's word at the surface's first landing.

A budget written here is not yet enforced by writing it here. It becomes real only once `test-author`
derives a `TEST_MATRIX.md` row from it that asserts the stated number — never a hope left standing in
this document's prose.

## Runtime and placement views (SPEC INV-74, INV-75)

Beside the node map, the document owes two more views, scaled by kind.

The **runtime view** walks every flow the spec promises through the nodes: which node serves each step,
what crosses each hop — citing the seam by name; the payload and its format stay the seam table's own
fact — and where the flow can fail. Every named failure point carries its fallback; a failure point with
no "if it fails" sentence is an unfinished walk. A flow the document cannot walk end to end is a
finding: a node is missing, or a seam is unnamed. The flow unit follows the kind — a web or app product
walks one visitor scenario per flow, a CLI walks one invocation per command, a skill pack walks a wish
through the skills, a book crosses no machines and satisfies the duty in one sentence.

The **placement view** states every node's place — build-time on the author's machine, a static file on
a content network, the client browser, an edge worker, an external service — plus the load-bearing
technology choice where one exists, first-class: a node-table column, or its own small table, so a
reader answers "where does this run" at a glance. It also states where secrets live and which tier holds
each verdict kept off the client — a secret's place is architecture, not an implementation footnote. A
single-place project satisfies the duty with one sentence. See
[references/architecture-step-detail.md](references/architecture-step-detail.md) for what each view
walks and states in the words the step first used.

## The node-fitness test, at every node's birth (SPEC INV-122)

Every new or carved node answers three questions at the moment it is proposed. Can it be tested alone?
Does a real second place need it? Can it and its neighbour be worked in parallel without queuing on
shared files? Three yes answers make the node right. A single no is a flag to answer, not a rejection —
name the plan that turns it to a yes, or fold the carve back into its caller. Two or more no answers make
the carve premature; fold it back.

The test has two homes. Its first is here, at the architecture step, where new abstractions are born and
a carve that fails it is folded back before it ships. Its second is `product-prover`'s speculative-node
flag: a node with one caller and no promised second is flagged for the second question's answer — never
auto-rejected, since the prover's job is to raise the question, not to decide it. See
[references/architecture-step-detail.md](references/architecture-step-detail.md) for the test's two
homes in the words the step first used.

## Keeping the document honest — iterative, re-carved, or redesigned (SPEC INV-37, INV-113)

The document is iterative, current only to what's shipped or in flight. It maps the product as it
stands, plus the landing in flight: a node exists for what ships today, or for what the spec already
promises under an open queue row, marked `[target]` with its pins left as a single dash. A future
feature earns its node only when its landing arrives — "should I architect the next few milestones now?"
is answered no, strictly, by the method; taste plays no part, since a speculative node is unbacked
structure the prover flags exactly as it flags an unbacked one born any other way.

**Re-carving the whole node map is legal.** It arrives as a restructure placement's own queue row (SPEC
INV-37), walks this same skill, and is re-proven like any other structure change — a placement may say
the shape no longer fits; only a landing actually changes it.

**Deliberate redesign is a distinct, larger move.** When layers are restacked, a surface's ownership
moves, or nodes are merged or split, the document is re-shaped to the new form and re-proven with the
architecture lens in that same movement (SPEC INV-113). Updating the pins alone is scoped to a boundary
shift that leaves the document's shape standing; after a real redesign the old shape itself lies, so
fresh pins written onto a stale shape are a defect, not a shortcut.

## Seams, feature coverage, and the decisions index

Three more sections round out the document, each with its own table in the template. **Seams** names the
place two nodes meet, what crosses it, and which side owns the format — a crossing with a real schema (a
data contract, a published interface, a file format) states where that schema lives, its one home.
**Feature coverage** maps every `[feature: F-x]`-tagged spec unit to the node(s) that implement it and
the test that exercises it, checked both ways: every tag gets a row, every row names a real node and a
real test. **Decisions — where they live** is one pointer table into the project's actual decision
homes — dated queue rows, journal chapters, the spec's own open decision marks — never a second home for
the decision itself.

The document closes on its **coverage rule**, walked at matrix derivation: every spec anchor appears in
some node's `owns` field. An orphan fact is a missing node or a missing assignment; a node owning nothing
traces to no spec backing, and is itself a finding.

## The generated Reference, and proving the finished document

A committed **Reference** table maps every spec anchor to the node(s) that own it, built off the node
sections' `owns` fields — generated output, never hand-kept. `scripts/build-architecture-reference.py`
builds it; `guardrails/check-architecture-reference.py` reds a committed copy that drifts from a fresh
build, an anchor a node owns that the table misses, or an anchor in the table that no node owns (SPEC
INV-315). Rebuild it after every change to the node sections rather than hand-editing the table.

Writing or updating the document is this skill's job; judging whether it holds together is
`product-prover`'s, run with the architecture lens whenever the document changed. That pass runs six
checks at the project's kind scale: every spec fact has an owning node, no node stands without spec
backing, every seam names what crosses it and who owns the format, every quality budget states its
instrumentation home and watcher (INV-41), the runtime view walks every promised flow (INV-74), and the
placement view says where every node runs (INV-75). Findings land in the project's `docs/prover/`
record. A full pass at a milestone or push gate proves `ARCHITECTURE.md` beside the spec (SPEC INV-116)
and appends its dated row to `docs/prover/architecture-prover-record.md`, the record's dated home once a
project's architecture becomes a format member (SPEC INV-279).

## Work that belongs elsewhere

Use this skill directly whenever a proven spec is in hand and the task is producing or updating the
structure that carries it. The Director calls it when a change touches boundaries, data, integrations,
scale, or operations (`skills/director/SKILL.md`'s specialist table). Use it only with a proven spec;
without one the derivation has nothing sound to derive from, and a request to design a structure with no
spec behind it routes to `spec-author` first.

Not for judging whether the finished document holds together — that is `product-prover`, run with the
architecture lens, above. Not for deriving the test matrix from a proven architecture — that is
`test-author`'s job, which reads this skill's output rather than producing it.

> The pack, whole: **live-spec-base** holds the shared rules and defaults · **director** decides
> whether a message even asks this skill to be called · **spec-author** writes the spec ·
> **product-prover** reviews it · **product-prover-pack** binds the external prover to the pack ·
> **design-reviewer** judges the design behind it · **architect** writes and updates the structure that
> carries a proven spec · **build-pipeline** ships the change · **test-author** derives the matrix
> and writes the tests · **communicator** makes the human exchange land · **feedback-intake** brings what
> comes back to its home · **feedback-collector** offers a rare private note up to the authors ·
> **text-audit** reads a text as a stranger and fixes where they stop · **text-audit-pack** binds the
> external audit skill to the pack · **publish** sees the work out the door, owing its kind's checklist.
