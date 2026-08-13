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
front half of a pair: **spec-author writes the spec; [`product-prover`](https://github.com/happysasha18/live-spec/tree/main/skills/product-prover)
reviews it.** A spec written this way should be one the prover can check: same primitives, surfaces named once,
cross-links explicit.

spec-author's job is to keep a spec that is **complete for what exists, honest about what's undecided, and
structured so the prover can find the holes the author can't** — grown as the work grows, never front-loaded
as a giant document.

## Words this skill uses

**Where the paths in this file point.** Two trees are in play. The named files under `scripts/`,
`guardrails/`, `templates/`, `tests/`, and `skills/` are the live-spec pack's own, at
`github.com/happysasha18/live-spec`. So are the design notes this page names by filename under
`docs/`. An install copies each skill folder into one place, so a path naming another skill points to
that skill's folder, beside this skill's folder. Every other path belongs to the project the pack is
attached to, including `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `JOURNAL.md`, and
`.live-spec/`.

Run every script named below from the live-spec repository root, as `python3 <path> <arguments>`. Each
one prints its own usage line when it is run with no arguments, so the arguments never have to be
guessed.

- **Wish** — one request a person voices in plain words, captured as a queue row.
- **Door** — the intake classification that sends a queued wish to one entry point of the pipeline. Its
  values are feature, bug, refactor, docs-only, and skip. It is decided before any code is written.
- **Queue row** — one row of the project's queue, `ROADMAP.md` in this pack. A closed row moves to
  `docs/queue-archive/`, so a row number cited below may sit there rather than in the live queue.
- **Lane** — one build train a session rolls through the pipeline.
- **Landing** — one piece of work reaching the repository's shared truth as one commit.
- **Host** — one project the pack attaches to. Each host keeps its own spec, queue, journal, and
  `.live-spec/` folder.
- **Host profile** — the host's own settings file, `.live-spec/profile.md`. This page reads its
  `project.kind`, `project.layers`, `project.design-principles`, and `project.axes` lines.
- **Kind** — what a host's product is, named from a fixed vocabulary: book, backend service, static
  site, fullstack app, CLI, or skill pack. The host profile records it.
- **Surface** — any part of the shipped product a user meets. A **stateful surface** holds state a
  user can change and find again later.
- **Spec-delta** — the set of spec sentences one wish or feature adds or changes.
- **Facet** — one aspect of a feature's design, ending as a written spec sentence.
- **Regression fence** — one sentence in a spec-delta naming a neighbouring promise that must stay
  true through the change, citing the clause it guards.
- **Composition axis** — one angle a stateful surface's behaviour can vary along.
- **Lens** — one named check the prover or the design review walks a document with.
- **Seat** — the session that orchestrates the work and reports to the person.
- **Red**, used as a verb — a check fails and stops the work at that point.

**The markers this page writes.** `[feature: F-x]` on a requirement heading marks a person-facing
scenario. `[target]` marks a surface or phase the spec names and does not yet specify for build.
`[default]` names a value the agent chose that the person may retune. `[GAP: ...]` under a criterion
records what the source left open. `⟨DECIDE⟩` marks a call only the person can make, and it carries a
one-line question.

**The bracket codes.** `INV-`, `E-`, `T-`, `S-`, `C-`, `M-`, `D-`, `A-`, `B-`, and `ACT-` codes index
requirements in this pack's own `PRODUCT_SPEC.md`. Its preamble names each letter's kind: `E-` an
entity, `INV-` an invariant, `T-` a transition, `M-` a rhythm rule, `A-` an adoption step, `B-` a
bootstrap step, `ACT-` an actor, `C-` a composition-axis rule, `D-` a recorded decision, and `S-` a
header rule. `PRODUCT_SPEC.index.md` maps each code to the criteria carrying it, written as `R12.4` —
requirement 12, criterion 4. Each sentence beside a code states its own rule in full, so a reader
holding this page alone can pass the codes over.

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

A spec is read by a **human first** (a teammate, the author months later) and a prover second — and both from
**one** document. Write it in the **language of the product**: plain words a product person speaks — what the
thing is and does, in whole sentences. Machine fragments with markup have no place in it. It doesn't have to read like a textbook/lesson either;
**product language is the register**, whatever fits the project. Don't fork a "readable" copy and a
"checkable" copy; they drift apart and one goes stale. The format below serves both at once. It was tested on a real
project: a prover-facing spec that read like "machine fragments with markup" was rejected by its author and
stopped being read, and a spec no one reads stops doing its job.

- **The body is a list of requirements; each opens with its situation.** After the preamble and the
  glossary, the body is a list of requirements. A requirement is named by the situation it governs
  ("The spec keeps what is built apart from what is planned", "A wish is captured as a queue row that is
  never lost") and carries three parts in order: a **Context** block of two to four short sentences —
  when the situation arises, who is involved, what the reader sees; a one-sentence **User Story** — as a
  person in a named position, I want one thing, so that one benefit follows; and the **acceptance
  criteria**, the behaviour grouped into named cases. The reader meets the situation and the people in it
  before the first rule, and a term is introduced before a rule uses it. A person-facing requirement is
  also called a **scenario** — its heading carries a `[feature: F-x]` tag; a machinery or reference
  requirement is not a scenario.
- **Acceptance criteria group into named cases, one criterion carrying one trigger and one response.** A
  **case** is one bold line naming a situation ("**Case: a wish becomes a row at once**"), followed by two
  to six numbered criteria. Every criterion sits in exactly one case, and the numbering runs continuously
  through the requirement. The keywords *when*, *while*, *if*, *then*, and *shall* are set in lowercase
  italics: *shall* states a duty, *when* and *while* open a situation, *if* opens a condition and *then*
  its result. No word in the document is written in all capitals outside a code anchor or a filename. A
  guardrail holds this shape — `guardrails/check-requirement-shape.py` reds a requirement missing its
  Context, its User Story, or its `### Acceptance Criteria`, and a criterion whose case or anchor is wrong.
  The parser behind that guardrail reads fixed line forms, held in `guardrails/specformat.py`:
    - a requirement heading opens `## Requirement N: `;
    - the Context line opens `**Context:**`, and the story line opens `**User Story:**`;
    - the criteria sit under a `### Acceptance Criteria` heading, each one written `N. text`;
    - a case line reads `**Case: the situation**`, bold and alone on its line;
    - a glossary entry reads `- **term** — definition`.
- **Each scenario states how it is entered and how it exits (SPEC INV-127).** A scenario is a flow with
  edges, and its Context block carries them: it states how the situation arises — from which prior state,
  with what already true (the preconditions) — and what the situation leaves true when it resolves (the
  postcondition). An entry or exit that is trivially none — a top-level scenario entered from nowhere, a
  terminal one exiting to nowhere — is stated in one short clause, so a reader tells a decided edge from
  an overlooked one. The duty binds forward: a new scenario carries its edges from the first draft, and
  product-prover flags an existing scenario's unstated edge as a finding (its scenario-level
  precondition/postcondition lens, kin of the entry-symmetry lens INV-50).
- **The criteria carry the meaning; the machine handles stay quiet.** Every criterion is a plain sentence a
  person reads straight through. The short codes — `[INV-18]`, `[T-1]`, `[E-3]` — trail at the **end** of the
  line as quiet handles for the prover and the test matrix. A reader skims past them; the maintainer follows
  them. **Never open a criterion with its code.** A range such as `[T-1..T-7]` cites its whole run of codes
  in one anchor.
- **A generated code-to-location table closes the doc.** The spec closes with a `## Reference` section
  holding one table that maps every code its criteria carry → the requirement-and-criterion locations that
  carry it (for example `INV-1` → `R4.3, R4.4, R5.1`). The table is **generated output**, built from the
  body criteria by `scripts/build-index.py`; no one edits it by hand, and feature codes (`F-...`) live on
  their scenario headings and take no table row. The authored home of each code's plain statement is its
  criterion in the body and its noun in the glossary; the table carries locations only. The gate
  `guardrails/check-index-generated.py` reds a committed table that differs from a fresh build, a body code
  the table misses, or a table code no criterion carries — so the table can never drift into a second truth.
  Two commands work it. `python3 scripts/build-index.py PRODUCT_SPEC.md -o PRODUCT_SPEC.index.md` builds
  the table, and that output is spliced under `## Reference`. `python3
  guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` then reads the document
  beside its committed copy.
- **Name the situation in the case; put the exact threshold in the criterion.** The bold **case** line
  names the situation in plain words; the numbered criteria under it carry the exact number or condition.
  The reader gets the shape from the case; the builder drops into the criterion for the precise value.
- **Use lists inside a Context block or a criterion to break up a wall of prose.** The acceptance criteria
  are already a numbered list by construction; this rule governs the prose around them. When a Context block
  or a criterion spells out several forms, legs, or arms — a label's forms, a check's three legs, a law's
  four arms — lay them out as bullet or numbered items so the eye scans them, and keep prose for the
  reasoning that connects them.
- **The enumeration threshold makes that checkable (SPEC INV-215).** A prose paragraph carrying an
  enumeration of three or more distinct, parallel facts earns bullet or numbered structure — a filename
  rule with its collision law and its header fields and its body parts, run together in one paragraph, is
  a list the reader should scan, so lay the members out as items. Prose stays for the laws, their reasoning,
  and their boundaries; the enumeration of parallel members becomes the list. This stays a stated writing
  rule, read by eye and by the prover's cognitive-load lens, and it earns no mechanical lint. A regex
  flagging every three-comma sentence would trip on ordinary rhetorical triads — a neutral, precise, plain
  register, or a rule with its actor and its reason. Telling a genuine list-owed enumeration from a
  rhetorical triad is a meaning call the register judge and the prover make, past a regex's reach. The rule
  came from the owner, 2026-07-17, reading the promoter's inter-agent design doc: a paragraph packing a
  filename rule, a collision law, three header fields, and four body parts belongs in a bulleted list —
  the human language was already right, and the one remaining fix was reading efficiency.
- **A preamble and a glossary open the doc.** Open the spec with a short preamble: what the document covers
  in two or three sentences, what the bracket codes are (each letter's kind, taken from the list under
  "The bracket codes" above — and that a reader can ignore them while a maintainer follows
  them), how the keywords *shall*, *when*, *while*, *if*, and *then* read, and that **edit history lives in
  the JOURNAL, apart from the spec itself.** A **glossary** follows, before the first requirement: every
  domain noun the body uses carries a one-sentence entry there, defined once under one name (closed
  vocabulary — a coined word is translated to a defined standard term before it enters the document). The
  gate `guardrails/check-vocabulary.py` reds a term defined twice, a glossary entry no body line uses,
  and a coinage listed in `guardrails/spec-coinages.json`. Its own header states what it leaves out.
  No script can tell a domain noun from ordinary English, so a used-but-undefined noun is caught by
  the cold reader instead.
- **The spec states the current truth — a changelog lives elsewhere.** No "changed in v0.8.3 from…" edit-history notes in the prose;
  the *why-we-changed-it* belongs in `JOURNAL.md` (dated, with the reason). A superseded rule may stay with a
  one-line "superseded by §X" pointer when the old shape still needs explaining — but the prose reads as
  today's truth.
- **Layer overview up front.** If the spec stacks layers (a credibility floor, then features on top), open
  with a 3–5 line "how the layers stack" map so a reader always knows where they are.
- **Readable-first beats terse.** Clipped machine-fragment prose gets rejected by humans as hard as a wall of
  fluff does. Err toward a sentence that *reads well*; keep the structure, lose the jargon. Terseness is not
  the goal. The goal is a headline the eye lands on, then detail it can drill into.
- **Write in the pack's technical-writer register.** Spec prose reads like a native-English open-source
  technical writer: neutral, precise, easy to follow. The full register (define abstract terms in plain
  words at first use, one term per concept, concrete nouns, active voice, cut nominalizations and filler,
  metaphors only as one-off color) and the per-section verification checklist live once in the
  `communicator` skill's writing register — `skills/communicator/references/writing-register.md` (its home
  since row 266) — spec prose follows it like every other human-facing text.
- **A machine gate holds the register — attention alone drifts — and the prose is written by a clean agent.**
  Re-styling a spec by hand drifts (a voice reads fine on a sample, then the same tells return round after
  round). A **tell** here is a writing habit a reader recognizes as machine-written. The durable fix has
  five parts, and parts 2 to 5 are proven and sealed in `docs/prose-quality-gate-design.md`:
    1. A fresh agent with the pack not loaded writes the prose from bare facts. A context that has
       loaded the pack writes ornate prose, so it only does the mechanical half. This leg is spec law
       (SPEC INV-84), restated in `skills/live-spec-base/SKILL.md`.
    2. `scripts/spec-style-lint.py --gate` blocks the tells a regex can see: contrast-by-denial frames,
       define-by-exclusion openers, jargon, shouted capitals, second person, reassurance, and future
       narration. Defined terms are allowlisted and marked informative regions are exempt.
    3. `scripts/spec-redundancy-precheck.py` catches lexical near-duplication. `scripts/spec-judge.py`
       then runs a fresh language-model judge against the hash-pinned rubric `scripts/judge-rubric.md`,
       for the redundancy and register a regex cannot see.
    4. An unfixed tell is recorded in `scripts/spec-waivers.json` as a dated waiver, and the running
       total is capped by `scripts/spec-debt-cap.json`.
    5. `scripts/spec-done-gate.py` is the one definition of done.

  Restyle each section through this loop: fresh writer → gate to 0 errors → anchor multiset
  unchanged → suite green → re-point any broken traceability check-phrase by narrowing to a register-clean phrase
  (log it) → commit. The floor is the machine; the ceiling stays the exemplars + a human's read.

This is the shape `product-prover` is tuned to read, and the one a human will actually keep open.

## Shipped docs state each requirement impersonally

A shipped product doc — the spec, the test matrix, the README, a skill card — is read by everyone the project reaches: a contributor, an auditor, a future user, a reader months later. Write each requirement as three plain parts: the rule, the actor as a role (the user, the producer, the target user), and the reason it holds. The reason is load-bearing and stays; the personal attribution drops, and a dated decision keeps the date as a plain anchor and drops the name — "chosen 2026-07-06 for a cold-start reader" carries what the next reader can act on, and a person's name gives them nothing to act on.

For that reason, personal attribution and candid process voice have one home: the local-only diaries, the JOURNAL and NEXT_STEPS, which no publish ships. Who decided a thing, and a session's own frank notes about how it went, belong there — the shipped clause carries the rule and its reason, the diary carries the story. Write the shipped clause impersonally from the first draft; do not scrub names at publish time, and let the publish floor stand only as the backstop. (SPEC INV-118.)

## The spine — what every spec must contain (not its section order)

The spine is a completeness checklist: it constrains what the document contains, and the section order
stays free. The document is organized as a glossary
followed by a list of requirements (per "How it reads" and `templates/PRODUCT_SPEC.template.md`); each spine
item lives inside a requirement's criteria, or — for a domain noun — in the glossary, and every code is
findable through the generated code-to-location table. Never let a new feature land without its entry.

1. **Purpose** — why the product exists, in plain words: the opening preamble.
2. **Entities** — the nouns. Each defined in the **glossary**, with its attributes, its unit/valid range if
   it's a measure, and its **states** if it has a lifecycle. *One concept, one name* (see below).
3. **States & transitions** — every move an entity can make, told as criteria (which action, which actor,
   what triggers it). A state with no way out is a bug; say what exits it.
4. **Actors** — who initiates each significant action (user, role, automated service, external system).
   "Who does this?" must have an answer for every transition.
5. **Invariants** — the properties that must hold across *every* reachable state, stated as criteria that
   hold while the situation runs. Cover both sides:
   - **Safety** — what must never happen (mutually-exclusive modes, no over-claiming, no partial writes).
   - **Liveness** — what must eventually happen (every async path completes / times out / rolls back).
6. **Cross-section composition** — the part most specs miss. See the dedicated step below.
7. **Terms** — every domain term is defined in the glossary, once, under one name. A word of ordinary
   English needs no entry.

Mark anything that needs a human's domain call with **⟨DECIDE⟩** and a one-line question. Never invent
intent to fill a gap — flag it.

**Name the future with the [target] tag — it is a tripwire that drives the pipeline.** A surface or phase the
spec names but does not yet specify for build carries the literal tag `[target]` (the header's
current-vs-target paragraph lists them). That tag is the canonical, machine-checkable form of "not yet
specified / later surface": the pipeline's feature tripwires key off it — touching a [target] surface
starts at the spec step, full stop (SPEC S-0, INV-16). Plain-prose phrasings (`TBD`, "future work",
"planned") bind too, but always write the tag: a future the machine can't see is a future a session can
hand-build past the method.

**A clause born of an approved look points at its norm (SPEC INV-43).** When the human approves a
visual prototype as the look ("this is the door"), the clause that encodes it carries a `norm: <path>`
pointer at its line end, beside its anchors — the prose carries the laws, the artifact keeps the look;
a build from text alone ships a cheap look-alike with a green suite (tlvphotos, 2026-07-05). Approval
freezes the artifact into the project's records: copy it to `docs/norms/` with a dated provenance line
(what, approved when, from which sketch) and point at the frozen copy, keeping the one-way fence absolute
— the prototype's code sits in its own named home, and nothing in the shipped product reaches into it
(E-17); a pointer into a live prototype home would break it. A text-born clause carries no pointer, and the law
binds forward — a clause owes its pointer at the first landing that touches it.

**Reshaping an existing spec? Hold the anchor-set guard.** A restructure (a genre migration, a resection)
must carry exactly the prior anchor set: diff the sorted anchor list before and after — identical sets prove
the shape changed and no rule was lost; any delta must be a deliberate, named change. Do not renumber or
retire a code as a side effect of a restructure; where a rule genuinely changes home, keep its anchor and
state today's home.

## The move most specs miss: compose every stateful surface across every axis

This move catches the bugs that pass every unit test, and a feature-focused author skips it.

When a surface (a player, a form, an editor, a panel) carries **state**, the system almost always also has
**global axes** it renders under. This is the **canonical axis list — its home is here; other docs point at it:**

- **view** (compact / detailed) · **mode** (quick / full, read / edit) · **tier** · **viewport size** ·
  **persistence / reopen** (any state that survives a reload — localStorage, a saved file) ·
  **concurrency** where it applies ·
  **every other live surface** — every other surface that can be present at the same time, whether or not
  that other surface holds state: a sibling sharing the screen, or a surface the flow reaches just before
  or after this one (a static end screen counts). For each, state what this surface does while that one is
  present: hold, clear, or hand off.

The bugs that pass every unit test live in the **product** of surface-state × axis, because each was
specified alone. The three authors forget most: viewport size (a grid that reflows below some width),
persistence/reopen (state written last session auto-restoring into a changed UI), and every other live
surface (a caption still naming the previous photo once the closing screen arrives, because "what the
caption shows when the finale is in view" was never written).

So, for every stateful surface, before its section is called done:

- **Enumerate it against each global axis.** For each axis value (each view/mode/tier), state what happens
  to the surface's state and controls. Is the state still *visible*? Still *reversible*? Does the axis
  transition *preserve, reset, or block* the state?
- **Name the composition invariant.** e.g. *"a per-stem mute/solo is reachable only while its control
  surface is visible; entering the compact view resets to the full mix."* Without it, the
  stranding bug follows: a state set in one view, hidden by another, with no way to see or undo it.
- **One surface, one name.** If the player's lanes and the `#stemlanes` canvas are the same thing, call
  them the same thing everywhere. A reviewer (human or prover) can only connect a cross-section hole when
  both sides are named identically and present in the same document — two names for one surface hides the
  seam.
- **If the surface persists state, compose the versions too.** When it writes localStorage/disk, enumerate
  version-N-1 state × version-N code explicitly: what does the current UI do when it reads a stored value
  that's older, partial, or belongs to a since-removed feature? State a migrate / ignore / clear rule — this
  is the seam behind "reopened it and it looked broken".

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

A person asks for a feature in the words they have; the dimensions below exist whether or not anyone
names them ("add a room where photos hang" never says "and decide what happens on a phone"). When the
door says feature, drafting the spec-delta walks this checklist — the **canonical facet list; its home is
here**, one list for every project.

**Read the project's declared layers, do not assume code (SPEC INV-135).** Which surfaces a facet sweep
reaches, and what a footprint's layer means for this project, come from the host profile's declared
`project.layers` line (SPEC INV-36, INV-135) — a photo site's layers are content, rendering engine, and
deployment, a campaign's are message, channels, and assets, and the pack's own are the rulebook, the
working skills, and the guardrails. The facet dimensions below are kind-abstract; read the declared
layers so the sweep names this project's real surfaces; do not assume a codebase's.

**Read the kind's declared design principles too (SPEC INV-136).** Beside its layers and proofs a
project kind carries a set of design principles — checkable design rules the kind's products must hold,
homed in the per-kind design-principles table in ARCHITECTURE.md and declared for a visual kind on the
host profile's `project.design-principles` line. When the wish touches a surface a declared design
principle governs, write the principle's answer as a spec sentence the same way a facet ends as a
sentence — the frontend kind's interactive-overlap rule (interactive controls that belong to different
layers occupy separate screen space) is answered wherever a covering overlay opens over floating chrome,
so the delta states which controls retract while the overlay stands. The pipeline's verify station
runs the declared design principles, each in its medium's own form (ARCHITECTURE.md, `docs/pipeline.md`
station 9). The spec names the answer so that station has something to check.

**Read the surface's composition axes from the kind too (SPEC INV-244).** Beside its layers, proofs,
and design principles, a project kind owes every surface a further axis set beyond the kind-independent
C-1 floor — the composition axes a surface answers because its kind renders under them, homed in the
per-kind axis table in ARCHITECTURE.md and declared on the host profile's `project.axes` line, an
explicit "none beyond the C-1 floor" a legitimate answer for a kind with no visitor-facing surface.
The C-1 floor is the canonical axis list above: view, mode, tier, viewport size, persistence and
reopen, concurrency, and every other live surface.
Composing a surface reads these declared axes from the kind before folding the facet sweep below, the
same way it reads the declared layers, so the delta answers each axis this kind owes; it does not
assume another kind's set. And where an owed axis adds runtime code to cover it (SPEC INV-248), the
delta states how that axis is delivered — the surface shipping whole for a named architectural reason
(one bundle, one page never torn down, a no-server delivery, a payload too small for a split to pay),
or owing a delivery road a later row lands (a platform split, a lazy load) — so the artifact's
separability is a decided sentence beside the axis's behaviour, read by the prover's
delivery-separability lens.

- **the viewport bands** — width and height both run in bands (narrow, wide, short, tall, and the
  bands a future device adds), so every layout-bearing feature ends the sweep with a decided or
  `[default]` sentence per band its layout law names or excludes, and a law scoped to one band answers
  for the others. This is the author-side of the viewport-quantifier lens the prover holds. That lens is the
  worked instance of the range law's general sub-domain duty: a guarantee scoped to a named part of its domain
  answers for the remainder, and a user state or a locale draws the same sweep on its own parts (SPEC INV-138).
  This folds the old width-only phone facet together with orientation / short viewport: a landscape
  phone is wide and short, a band a width-thinking sweep misses, so a rotated phone meets a stated
  layout (incident: tlvphotos's caption zone printed over the picture on a
  landscape phone — the layout law said "on a phone", the styles mapped phone to width ≤ 640px, and a
  rotated phone fell out of both sentences, 2026-07-16);
- **touch where the design assumed a mouse** — anything hover-only needs a touch answer;
- **the empty, error, and loading states** of each new surface (spelled "empty, error, and loading");
- **accessibility** — reachable by keyboard, readable contrast;
- **the performance envelope** — at what input size it must stay usable; for a user-facing surface
  this facet ends as a measurable budget sentence ("the first image appears within 2 s on a cold
  visit"), never an unmeasurable "fast enough" — the architecture step pairs the budget with an
  instrumentation home and acceptance asserts it (SPEC INV-41);
- **visual hierarchy** — the gap between separate things larger than the gap within one thing (nesting
  depth drives spacing, never per-element guesswork); a heading never dimmer or smaller than the body it
  heads, sizes from one scale (incident: track-coach's inverted panel margins, 2026-07-05);
- **two windows at once** — the same stored state open in two windows; what one window's change does to
  the other (incident: track-coach's persisted aim auto-swapping cards, 2026-07-02);
- **a missing source** — an input file renamed, moved, or gone: the feature says what it shows and asks
  the person; it never guesses (incident family: the ask-don't-guess stem/source cases, track-coach 2026-06/07);
- **paired-transition symmetry** — when a surface has a pair of opposite state changes (open/close,
  enter/exit, expand/collapse, show/hide), the exit's motion mirrors the enter's unless a reason is written;
  the default is symmetry, and because motion feel is the human's own gate (SPEC INV-30) an undecidable pair
  is surfaced as a real question. A pair that enters with craft and exits instantly is never shipped silently; the answer
  ends as a spec sentence — mirror, a named shorter exit, or deliberately instant — decided or
  `[default]`-tagged like any facet (SPEC INV-126; incident: tlvphotos's polaroid room revealed under a soft
  veil in one breath and closed on a hard cut with no transition, found by hand on a real phone, 2026-07-12).
  That first part asks about the motion. Two further parts follow it, so the facet ends as three
  sentences rather than one.
    - The second part asks the reversibility of the means. Where the surface opens by a continuous,
      reversible gesture — a pinch, a drag, a lift — the same gesture reversed is written among its
      ways to close. A decided sentence may instead state why it is absent. Silence there is a
      finding, and the rightness of the reason stays the human's gate (SPEC INV-126). The incident:
      tlvphotos's pinch-to-zoom layer opened by a finger-tracked scale-up and closed only by a
      control. No reverse pinch, felt on a phone, 2026-07-14.
    - The third part asks magnitude beside existence. Where the pair rides a continuous, reversible
      quantity — a pinch span, a drag distance, a wheel accumulation — the author writes whether the
      two directions demand the same magnitude. That answer is symmetry or a named deliberate
      asymmetry, decided or `[default]`-tagged like any facet (SPEC INV-126). The incident:
      tlvphotos's inspect zoom opened on any spread past rest, and closed only at a squeeze to
      ~0.82× of rest. The reverse existed at a deeper cost to the hand. Every prover pass came clean
      because the lens asked only existence, felt on a real phone, 2026-07-16.
- **Edge completeness — both ends of a gate, and the three faces of a wait.** When the surface has a
  behaviour gated on a quantity that runs on a line (elapsed time since a last visit, a count, a distance, a
  size), write what it does at both ends of the range — below the low end and above the high end, beyond
  the one point the wish named; "on return", "after a while", "once there are several" each owe their two
  bounds. And when a slot is filled by asynchronously produced content, write the three faces of a wait —
  pending, arrived, failed — with a visible pending face while the content is in flight; this is the
  empty/error/loading facet above made specific for a reserved slot, its loading state named and shown. Each edge becomes a
  spec sentence, decided or `[default]`-tagged like any facet (SPEC INV-138).

**The list is curated, each facet earning its place by named incident.** A facet joins only with a named real incident it would have
caught. Five of the ten entries above name theirs, and the other five carry none. The list is
re-justified at milestones; a checklist
that grows by taste becomes a forty-row form nobody walks (the Google launch-checklist lesson).

**The declared-laws line rides every new section (SPEC INV-101).** Where the spec keeps a declared-laws home — the one place naming its cross-cutting laws (measurement, accessibility, error handling, a register: what the product declares) — a new surface's section states its line against each declared law, the clause or a dated exemption, before the prover ever reads the delta. Each declared law also carries its net — the review or gate that enforces it — written beside the law in that home, so the assignment lives where the laws are declared (SPEC INV-150). A law belongs to a mechanical gate where a deterministic guardrail or test decides the violation, to the prover where the violation pins to a stated sentence, and to the design review where the deciding fact lives only in the human's intent. The prover's cross-cutting station then audits the declared lines. It no longer has to discover them. A spec with no such home yet earns the home first, and a declared law with no named net is a finding there.

**Every facet ends as a spec sentence.** Either the human (or the walk's
batched questions) decided it, or the recommended option is taken so the lane keeps moving and the
sentence is written carrying the literal tag `[default]` at its line end — so a later prover tells a
taken default from a hole, and the matrix derives the facet's test row either way. Every defaulted facet
is then told on the delivery report's defaults list as a plain-words tradeoff in the product's terms
("on a phone this gallery stacks into one column — tweakable"), never one ping per facet and never a
confirmation request (SPEC INV-31) — communicator owns the report shape; a veto
becomes a new wish. A facet with no sentence is a spec defect the prover flags. The sweep scopes to the feature's visible
surfaces — a headless feature (new persistent state only) satisfies it with one explicit sentence, "no
visible surface — facets N/A", never a silent skip.

Boundaries, stated once: a wish re-doored to feature mid-work walks the sweep before work resumes — the
late-recognized surface is exactly the one whose facets nobody looked at. A fenced prototype is never
swept (a sketch has no facets to promise); the sweep fires when promotion makes it a feature. On an
adopted or promoted surface that already lives, a default is read from the shipped truth and reconciled
like any re-engineered claim, never invented greenfield. And the sweep versus the canonical axes above:
the sweep authors the facet sentences when the feature is first specified; the axes compose and test them
across views once the surface exists — one dimension, split by time, never specified twice.

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

## The primary unit — one per project type, traced end to end (SPEC E-29, INV-73)

A spec has a primary unit: the thing the reader counts, the product's spine repeated. The unit is a
parameter of the project's type — the way a domain swaps a template — declared once, then it sets the
heading style, the acceptance-criterion shape, and what the coverage check means.

| project type | primary unit | the coverage check validates |
|---|---|---|
| web / app | a user-facing **feature** (a visible flow) | every feature → architecture node(s) + a test |
| CLI / library / API | a **command** / function / endpoint | every surface → its contract, an owning module + a test |
| methodology package | a rule or **guarantee** the pack promises | every guarantee → an enforcing mechanism (a script, a gate, a template) |
| content / book / article | an **argument** / chapter / section | every promised argument → a home in the outline (a structure check; no technical architecture) |

**The mechanic is one, for every type.** Each unit carries a stable inline tag on its heading — the same
family as the anchors, e.g. `[feature: F-wish]` — and the downstream artifacts back-reference it: one
coverage table in ARCHITECTURE.md names the implementer node(s) and a test per unit. The two-way check reads
both directions — every unit has an implementer and a test, and every promised unit carries its tag. In this
pack that check is the feature-coverage trace in `tests/test_traceability.py`, reading ARCHITECTURE.md's
`## Feature coverage` table. This
is the anchor-ownership machinery extended a level up, never a second machine to keep in sync.

**No file explosion.** One PRODUCT_SPEC.md, one ARCHITECTURE.md, one TEST_MATRIX.md; the unit tags live
inline in the prose and the one coverage table binds them. Shard into per-feature files only for a
genuinely huge project, and only by explicit call.

**The source is plain Markdown; the render resolves the links.** The source stays plain Markdown — a
tag plus one table. When a doc is rendered, a relative `.md` cross-link opens its rendered `.html`
neighbour and its `#anchor` lands on the target heading (ROADMAP row 195, shipped 2026-07-10). Linking
a trailing bracket code to its row in the code-to-location table stays an optional later leg; until that lands, a reader
follows a bare tag by searching the source.

**On live-spec itself.** live-spec is a package, but its scenarios are the product's features, so it
dogfoods the web/app row: each person-facing scenario heading tags `[feature: F-x]` and the Feature
coverage table maps it to its skills and its test. The machines that work behind the scenes (guardrails,
host contract) implement guarantees; they are not user-facing features, and they stay outside the feature layer
by the type's own definition of its unit. The decided design note is `docs/spec-format-by-project-type.md`.

**The heading convention makes the reverse direction mechanical (SPEC INV-132).** For the two-way check to
catch a scenario whose tag was forgotten, an untagged heading has to be unambiguous — and it is not on its
own, since the checker cannot tell a new scenario missing its tag from a machinery or reference section
that never had one. So every requirement heading — `## Requirement N: …`, the level every person-facing
scenario uses — carries either its `[feature: F-x]` tag (a person-facing scenario) or the explicit
`[not a scenario]` marker (a machinery, rules, or reference section, legitimately untagged), and an
untagged, unmarked requirement heading is unambiguously red. The parts under it — the `### Acceptance
Criteria` sub-heading and the bold case lines — nest inside a requirement already tagged or marked, so they
owe nothing. When a section that is not a person-facing scenario is added, state its `[not a scenario]`
marker in the same edit — a new machinery heading that passes silently is the gap this closes.

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

Ask each question out loud; a "no" or "don't know" is a gap to fill or mark ⟨DECIDE⟩.

- **Entities:** Is every domain noun defined once in the glossary? Does each measure carry a unit + valid
  range? Does each entity with a lifecycle list its states?
- **Transitions:** For every state, what action leaves it, and who triggers it? Is there a state with no
  exit?
- **Invariants:** What must never happen here (safety)? What must eventually happen (liveness)? Is each
  one stated explicitly?
- **Composition:** Does this surface carry state? Under which of the canonical axes (view / mode / tier /
  viewport size / persistence-reopen / concurrency / every other live surface) is it shown? For each, is
  its state still visible and reversible? Is the transition's effect (preserve / reset / block) stated? If
  it persists state, is the older-stored-value × current-code case handled? For every other surface that
  can be present at the same time — a sibling on the screen, the surface one step before or after in the
  flow — is this surface's behaviour stated while that one is present?
- **Facets (feature door):** Did the facet sweep run — does every entry of the canonical facet list end
  in a spec sentence, decided or `[default]`-tagged and reported?
- **Naming:** Is anything in this section also referred to by another name elsewhere? Unify it.
- **Single source of truth:** Does any other document in this repo also claim to be the spec or the matrix
  ("source of truth")? If so, demote it to a pointer — two docs claiming authority is undefined when they disagree.
- **Honesty:** Is any claim here something the system can't actually deliver, or a guess dressed as a fact?
  Mark it ⟨DECIDE⟩ or cut it.
- **Readability (human-first, product language):** Does each case name its situation in plain words a
  non-author grasps in one read? Are the criteria phrased in product words a person would say, with the
  keywords in lowercase italics and no all-capital words outside a code anchor? Are the codes at line-*ends*,
  never opening a criterion? Is there any edit-history note in the prose that belongs in the JOURNAL? Does
  the spec open with a preamble and a glossary?
- **Shape (requirements genre):** Does every requirement carry a Context block, a one-sentence User Story,
  and criteria grouped into named cases, numbered continuously through the requirement? Does
  `guardrails/check-requirement-shape.py` pass? Is every spine item present inside the requirements or the
  glossary? Does the generated code-to-location table match a fresh `scripts/build-index.py` build, with
  `guardrails/check-index-generated.py` green? After a restructure: is the anchor set identical to before
  (or every delta named)?

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

## What spec-author produces

A `PRODUCT_SPEC.md` (or an updated section of one) in the requirements genre — a glossary and a body of
requirements, each with a Context block, a User Story, and named-case criteria, anchors trailing, closed
with a generated code-to-location table — complete against the spine, with surfaces named once and their
cross-axis composition stated — ready for `product-prover` to review and for a test matrix to be derived from. The reply also surfaces the ⟨DECIDE⟩ points that could not
be resolved and the leading questions behind them.

## Anti-patterns (refuse these)

- **Speccing a surface on one axis only** — the player described as play/mute/solo with no word on what the
  compact view does to it. Always compose.
- **Two names for one surface** — "the lanes" and "#stemlanes" as if separate. Unify.
- **Filling a gap silently** — inventing a threshold or a behavior the author never decided. Ask or
  ⟨DECIDE⟩.
- **Speccing after the code** — writing the spec to match what was built. The spec should lead, and the
  prover should find the holes before code exists.
- **Pinning a drifting version number in prose** — "current version: vX.Y" in a header or README always
  goes stale; the version has one home (the VERSION file, the frontmatter) — point there or omit it.
  This binds a **derived doc's header** too (ARCHITECTURE.md, TEST_MATRIX.md): a derived doc's header
  carries no frozen spec-version number — it names what it derives from, points at the version's one
  home (VERSION), and carries a dated "Last reconciled" provenance line, so
  a reader never meets a stale number that reads as the current version. A version string has no place
  in that header. The lint `tests/test_derived_doc_header_policy.py` holds the two headers to this (row 265).
- **A wall of undifferentiated prose** — behaviour run together in paragraphs with no case to land on. The
  fix is named cases with numbered criteria, so the reader scans the behaviour; machine-terse fragments are
  the opposite failure and get rejected just as hard (see "How it reads").
- **Codes opening the line / edit-history in the prose** — `INV-18:` as a criterion's first word, or "in v0.8
  we changed…" baked into a rule. Codes trail at line-ends; history goes in the JOURNAL.
- **Prose where a criterion belongs** — a behaviour told as a narrative paragraph, leaving the reader no
  numbered line to key on. Each rule is a criterion carrying one trigger, one response, and a trailing
  anchor, sitting in a named case.
- **A hand-edited code-to-location table** — editing the generated Reference table by hand, or letting it
  lag the body. The table is generated output (`scripts/build-index.py`); `guardrails/check-index-generated.py`
  reds a table that differs from a fresh build. Regenerate it; never hand-edit it.

## Pairing with product-prover

| | spec-author | product-prover |
|---|---|---|
| role | writes & grows the spec | reviews the spec |
| output | structured `PRODUCT_SPEC.md` sections | findings: gaps, contradictions, missing invariants |
| when | starting / adding a feature / a new surface | spec drafted or changed, before tests/code |

Author with this skill, review with the prover, then derive matrix + tests. Same primitives on both sides
so the handoff is clean.
