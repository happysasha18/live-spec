---
name: spec-author
description: Use to start a new product spec, add a feature to an existing spec, or keep a spec in sync with behavior changes. Setting a project up on live-spec comes earlier, at build-pipeline's setup entry. Documenting already-built code after the fact and a prototype sketch that carries no spec stay outside it.
metadata:
  version: 5.0.0
---

# Spec Author

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live once in the pack's base skill, `live-spec-base` (v5.0.0), together with the
> settings ladder — this skill references them and elaborates only its own domain. That base skill's
> file is `skills/live-spec-base/SKILL.md`, and it states each of those rules in full. Loaded without
> it, this page still runs every section below. What it loses is those shared rules and the settings
> ladder, which live in that base skill alone.

spec-author authors and grows a **living spec** — a requirements-genre `PRODUCT_SPEC.md` that says what the product is, what every
part is allowed to claim, and how the parts compose — *incrementally, as the project develops*. spec-author is the
front half of a pair: **spec-author writes the spec; [`product-prover`](https://github.com/happysasha18/product-prover)
reviews it.** A spec written this way should be one the prover can check: same primitives, surfaces named once,
cross-links explicit.

spec-author's job is to keep a spec that is **complete for what exists, honest about what's undecided, and
structured so the prover can find the holes the author can't** — grown as the work grows, never front-loaded
as a giant document.

## Words this skill uses

Where this page's paths point, how to run the scripts it names, the terms it uses
(wish, door, lane, host, surface, spec-delta, facet, fence, axis, lens, seat, red),
the markers it writes, and the bracket codes.
See [references/glossary.md](references/glossary.md).

## Work that belongs elsewhere

Reserve it for a spec the code will chase. Skip it for retro-documenting already-built code so it looks
specced (the spec leads, code chases), for a prototype (a sketch gets a label and a fence, never a spec),
for pure research notes, and for the skip-boundary edit (single file, no new behaviour — it goes straight
to code + its test); and reach for product-prover instead when what's wanted is a review — its half of the pair.

## The one rule

> A spec exists so the next reader — the prover, a teammate, or the author months later — can reason about
> every reachable situation. If a situation the system can reach isn't in the spec, the spec is incomplete,
> even if the code "works."

## How it reads — human-first, in plain product language

Who reads a spec and in what register, and the shape of the body: requirements carrying Context,
User Story, and acceptance criteria grouped into named cases.
See [references/how-it-reads.md](references/how-it-reads.md) for the whole form
and the guardrails that hold it.

## Shipped docs state each requirement impersonally

A shipped product doc — the spec, the test matrix, the README, a skill card — is read by everyone the project reaches: a contributor, an auditor, a future user, a reader months later. Write each requirement as three plain parts: the rule, the actor as a role (the user, the producer, the target user), and the reason it holds. The reason is load-bearing and stays; the personal attribution drops, and a dated decision keeps the date as a plain anchor and drops the name — "chosen 2026-07-06 for a cold-start reader" carries what the next reader can act on, and a person's name gives them nothing to act on.

For that reason, personal attribution and candid process voice have one home: the local-only diaries, the JOURNAL and NEXT_STEPS, which no publish ships. Who decided a thing, and a session's own frank notes about how it went, belong there — the shipped clause carries the rule and its reason, the diary carries the story. Write the shipped clause impersonally from the first draft; do not scrub names at publish time, and let the publish floor stand only as the backstop. (SPEC INV-118.)

## The spine — what every spec must contain (not its section order)

The completeness checklist of what a spec must contain — purpose, entities, states and transitions,
actors, invariants, cross-section composition, terms — and where each item lives.
See [references/the-spine.md](references/the-spine.md) for the items and their rules.

## The move most specs miss: compose every stateful surface across every axis

Why the bugs that pass every unit test live in surface-state × axis, the canonical axis list,
and the sweep to run over every stateful surface.
See [references/composition-sweep.md](references/composition-sweep.md) for the list itself and the sweep.

## Declare the pole when a capability could live in the pack or in each host (SPEC INV-163)

When authoring a capability the pack could hold once or each host could hold its own, declare which pole it
takes, so the pack↔host home is written as a decided sentence. One question decides it: can the
pack ship a single identical body that every host runs? When it can, the body centralizes to one pack home,
adopted by a package update. When the body is host-specific — it names a host's own surfaces, holds a host's
own data, or reads a host's own artifacts — the pack ships the shape (a template and its guidance) and each
host owns the instance it fills. Write the chosen pole into the clause and cite the split [INV-163]; the duty
binds forward [INV-159], so a new host-specific capability names its pole from the first draft while the
bodies that predate the clause stand as they are cited.

## The feature delta, assembled — one home for its mandatory parts

Author in this order; every part below is mandatory for a feature and no scope cut may trim it
(scope dials richness; it never trims the safety net — SPEC T-15):

1. **Regression fences** — when the wish touches a live surface (next section; SPEC T-14, INV-19);
2. **The new behaviour itself** — entities, states, transitions, composed across the canonical axes;
3. **The standard-facet sweep** — every facet a spec sentence, decided or `[default]`-tagged (SPEC T-13, INV-18);
4. **The fit walk** — how the feature sits in the person's path, kind-scaled (SPEC INV-29);
5. **The two closing sentences** — non-goals + one success measure (SPEC INV-20, INV-21).

A delta missing any numbered part is incomplete at authoring time — the author catches it before the prover ever sees it.

## The regression fences — run first when the wish touches a surface that already lives (SPEC T-14, INV-19)

Before authoring anything new, preserve the neighbours. The spec-delta opens with one sentence per
existing promise that must stay true through the change ("the catalog still opens on click"), each
citing the spec clause it guards. A fence is not new law and earns no new matrix row — the cited
clause's row already carries its never-side, and the landing's full-suite run is what proves the fence
held. Split what the delta touches: promises that stay are fenced; behaviour being changed is
re-authored as new law — a fact is fenced or re-authored, never both. A fence that finds no clause
behind it has discovered an unwritten promise: reconcile it from the shipped truth (like an adopted
claim), write it as its own spec fact with its own row, and state it explicitly. If
the cited neighbour claim is adoption-born and still unverified, its reconciliation runs before it can
be fenced — a hope cannot be fenced. Name the fences by cited anchor in the wish's queue row, which is
a row of `ROADMAP.md` in this pack ("fences: …"), so "untouched and still true" stays searchable. A
prototype fences nothing — it promises
nothing.

## The facet sweep — run when a wish's door says feature (SPEC T-13, INV-18)

Every entry of the canonical facet list ends as a spec sentence, decided or `[default]`-tagged.
See [references/facet-sweep.md](references/facet-sweep.md) for the list itself, each facet's
incident, the declared-layers/principles/axes reads, and the closing rules.

## The fit walk — run with the facet sweep when the door says feature (SPEC INV-29)

The facets above ask what every visible feature owes its device; the fit walk asks how the feature
sits in the person's path — the questions nobody thinks to ask until a guest is stuck at the tenth
picture with no way on (tlvphotos, 2026-07-06). **The lens lists' home is here**, kind-scaled, curated
with incidents exactly like the facet list:

- **product / UX kind — the visitor's journey:** how does the person arrive here (every entry door,
  including the ones past the main one) · what do they do here · where do they go NEXT from every state this surface
  can be in (no dead ends — the door↔room loop incident, tlvphotos 2026-07-06) · what does a return
  visit change (seen-state, no-repeat — and the remembered state it implies) · a conditionally-entered
  face (first visit, empty state, onboarding, a one-time banner) names its deliberate re-entry path or
  states the one-way as a decision (SPEC INV-50) · what does the feel owe
  against the approved prototype's bar · what next feature does this one invite;
- **infra / backend kind — the flows:** inputs → outputs · the data's lifecycle (created, updated,
  stale, gone) · every failure path and what the caller sees;
- **skill kind — the behaviour:** the trigger · the correction it makes · when it must not fire.

The walk interrogates the feature, never the person (SPEC INV-29): derive answers from the existing
spec and shipped truth; close the trivially-closable holes and write how each was closed;
`[default]`-tag the rest; batch only the genuine taste calls with the facet sweep's report. Every
answer lands as a spec sentence — the same silence-is-not-an-option law as the facets.

## The delta's two closing sentences — non-goals and the success measure (SPEC INV-20, INV-21)

Every feature's spec-delta closes with two short sentences, always written; neither may be
left out. **Non-goals**: what is deliberately left out ("version comparison waits for a later pass");
"nothing deliberately left out this time" is itself valid — only a missing sentence is a hole, and a
non-goal that narrows what the wish asked for rides the batched report, never a silent narrowing.
**A success measure**: how we'd notice the feature worked for its person, a number where one exists;
decided or `[default]`-tagged — the tag marks provenance only, no test row derives from it until the
reading machinery lands. The quantification questions (analytics tag? how measured? A/B worth it?) ride
the facet sweep's batched report. Both bind forward; an adopted feature owes its pair at the first
landing that touches it. A prototype writes neither — it promises nothing.

## Removing a shipped feature is a change too

The tombstone and the retired matrix rows are already the shared rule (base rule 10). What that rule
does not name: the owning tests are deleted, and the skill's own SKILL.md / README are swept — all
in the same session as the removal.

## The primary unit — one per project type, traced end to end (SPEC E-29, INV-73)

What a primary unit is, which unit each project type carries, the one tag-and-trace mechanic
shared by every type, and the no-file-explosion rule.
See [references/primary-unit.md](references/primary-unit.md) for the table and the tracing rules.

## The content contract — when a generic engine is extracted from an instance (SPEC INV-79)

A generic engine carved out of a working project inherits the donor's assumptions silently: an id
format, a hardcoded wordmark, a path, a language default. At extraction the spec opens a **content
contract** section: every donor-specific constant the extraction finds becomes a named entry — what
the engine requires from any instance's content, in the engine's own vocabulary — and each entry
owes a test that the engine works without the donor's value (test-author's half of the same law).
An assumption with no entry is a leak the next instance discovers in production.

## Crossing the instance→engine boundary — provenance and naming (SPEC INV-119)

A feature usually proves itself first on a live instance and then generalizes into the engine. When that history goes into the engine's spec, write it as the engine's own record: the reader is anyone who runs the engine, so every provenance handle points at something that reader can reach, and the spec reads as generic from the first line.

Four conventions carry the boundary:

- **The history reads as a reconciliation.** Head the history section "Reconciliation log — how each behaviour landed in code", and let each entry trace a behaviour to where it landed in the engine's own code. This is a spec-versus-code reconciliation the engine's reader can follow. It is not a fork's delta against an instance's reference implementation.
- **Provenance cites the engine's own public commit.** Each entry names where the behaviour landed in the engine — "landed in engine commit `<hash>`" — a commit any reader can check out in the engine's own history. A private instance's commit is invisible to that reader, so an instance hash stays out of the engine's provenance.
- **One intro sentence states the normal intake path, once.** Open the log with a single sentence naming the usual route — "Most rows record a feature proven first on a live instance and then generalized into the engine" — so no per-entry line re-explains where features come from.
- **A mechanism carries a neutral internal name; a visible instance label is marked as instance copy.** Name a mechanism by what it does in the engine's own vocabulary — "the unfold step", "the show-more control". Where a running instance shows locale-specific words for it, the spec notes that string as instance-supplied copy the instance plugs in [INV-79], and the neutral term stays the mechanism's one name [E-4].

## Standard vocabulary — what our house terms map to

The pack's method is its own, but its concepts are the field's, and naming the lineage lets a reader who
knows requirements engineering recognize what a live-spec document is doing. The crosswalk to the field's
vocabulary (`ISO`/arc42/C4) lives in `docs/spec-format-by-project-type.md`.

Two boundaries the crosswalk does not erase: our spec stays a single requirements-genre document — a
glossary and a body of requirements — and a term joins our vocabulary only when it is measurable or
verifiable here, never for the borrowed authority alone.

## How spec-author works

1. **Author / grow the relevant requirement** in `PRODUCT_SPEC.md`: find (or open) the requirement the
   change belongs to — the intake placement verdict made real: the scenario is the wish's place on
   the feature map (SPEC INV-37) — and grow its Context, its User Story, and its named-case criteria, plain
   language, anchors at line-ends. Add any new domain noun to the glossary in the same edit. The
   code-to-location table is regenerated at freeze by `scripts/build-index.py`; leave it to the builder
   rather than editing it by hand. Reuse the existing vocabulary; don't introduce a second word for an existing concept.
   Starting fresh? Copy `templates/PRODUCT_SPEC.template.md`. (Template paths resolve from the pack repo —
   github.com/happysasha18/live-spec. A standalone install of this skill reads them from a checkout of
   that repository, taken with `git clone https://github.com/happysasha18/live-spec`. They are
   deliberately not copied into the skill dir: the pack is the source, a copy would fork the truth.)
2. **Ask, don't silently fill.** When the spec needs a decision only the author can make (a threshold, a
   policy, desired behavior on an edge), ask the leading question or mark ⟨DECIDE⟩, treating intent as
something to confirm; never infer it.
3. **Run the completeness pass** (below) on the section just written.
4. **Hand off to `product-prover` on the whole spec — the delta included.** The prover catches a
   cross-section hole only when *both* sides of the seam are in the document; a surface added in
   isolation, or left unlinked, is invisible to it. So re-prove the whole spec whenever a surface is added.
5. **Then walk the two layers to the tests** — the architecture doc (nodes owning the spec's facts,
   proven with the architecture lens), then the matrix derived node × fact (`spec → prove → architecture
   → prove architecture → matrix → test → code`; build-pipeline owns the steps). The spec leads; code
   chases it.

## The completeness pass — run before declaring a section done

The questions to ask out loud before a section is called done — entities, transitions, invariants,
composition, facets, and the rest.
See [references/completeness-pass.md](references/completeness-pass.md) for the questions.

## The comprehension gate — a changed section passes two layers before it ships

A stranger reads a shipped section on first pass, so a changed section clears a comprehension gate: the
mechanical lints first, then a panel of fresh cold readers. This gate is spec law and every changed
section runs it, closing on two consecutive reads that return zero blocking findings. The text-audit
skill carries the loop's method and the reader-prompt — the mechanical lints, the cold reader, and the
two-consecutive-clean stopping rule — so run it there rather than restating the loop here. Per changed
section the gate is cheap: a small delta puts one glossary entry and a handful of criteria in front of a
reader, and the whole document stays out of the reading.

**A source hole is a `[GAP: ...]` line, never a filled-in guess.** The source is whatever the criterion is
authored from — the person's wish, an older document, or the shipped truth. Where that source states a
behaviour and leaves its judge, its measure, or its scope unstated, the criterion names the actor most
likely to own the call — the system, or the person the requirement already involves — and carries a `[GAP: ...]` line under
it stating what the source left open, so the named actor reads as provisional. Inventing behaviour is
forbidden; a gap line is the correct output for a real hole (this is ask-never-guess in the criterion
form). Every judgment names its judge and its
inputs, and every relational word fills its slots — proportional to what, larger than what, sufficient for
what — right where the word stands.

## The change record — classify every touched code and hold the size ratchet

The delta record under `docs/deltas/`, the four fixed kinds it classifies every touched code into,
the classifier gate that reads it, and the size ratchet.
See [references/change-record.md](references/change-record.md) for the kinds and the ratchet.

## What spec-author produces

A `PRODUCT_SPEC.md` (or an updated section of one) in the requirements genre — a glossary and a body of
requirements, each with a Context block, a User Story, and named-case criteria, anchors trailing, closed
with a generated code-to-location table — complete against the spine, with surfaces named once and their
cross-axis composition stated — ready for `product-prover` to review and for a test matrix to be derived from. The reply also surfaces the ⟨DECIDE⟩ points that could not
be resolved and the leading questions behind them.

## Anti-patterns (refuse these)

The shapes to refuse: one-axis surfaces, two names for one surface, silent gap-filling,
speccing after the code, pinned drifting version numbers, and the rest.
See [references/anti-patterns.md](references/anti-patterns.md) for the full list.

## Pairing with product-prover

| | spec-author | product-prover |
|---|---|---|
| role | writes & grows the spec | reviews the spec |
| output | structured `PRODUCT_SPEC.md` sections | findings: gaps, contradictions, missing invariants |
| when | starting / adding a feature / a new surface | spec drafted or changed, before tests/code |

Author with this skill, review with the prover, then derive matrix + tests. Same primitives on both sides
so the handoff is clean.
