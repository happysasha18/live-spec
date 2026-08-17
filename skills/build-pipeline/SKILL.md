---
name: build-pipeline
description: Use to run a non-trivial feature, bug fix, behavior change, refactor, docs-only change, or feature removal through the full spec-to-ship pipeline. Use it as well to set a project up on live-spec, where it reads the tree, picks the setup walk, and runs it. Spoken: attach live-spec to this project, adopt or install live-spec here, onboard this codebase onto live-spec, found a new project on live-spec, update live-spec here. A tiny reversible edit and pure research stay outside the pipeline.
metadata:
  version: 5.0.0
---

# build-pipeline — ship a change by the method

> Part of the **live-spec pack**. The shared working rules live in one place: the pack's base skill,
> `live-spec-base` (v5.0.0), which also holds the settings ladder. Those rules are ask-never-guess ·
> plain words, anchors trail · one surface = one name · one home per fact · junior/senior split ·
> checkpoints · the concurrent-edit fence · freshness · journal discipline · attic-never-delete ·
> verify by deed · the human's gates · claims need primary sources · fix the class, sweep
> look-alikes · the door before code · prototype ≠ product. This skill references them and
> elaborates only its own domain. Used standalone, this note is plain advice.

## Words this skill uses

**Where the paths point.** Two repositories are in play. A path naming `skills/`, `guardrails/`,
`scripts/`, `templates/`, or `tests/` sits in the live-spec pack's own repository,
`github.com/happysasha18/live-spec`. An install copies each skill folder into one place, so a path
naming another skill points to that skill's folder, beside this skill's folder. A path opening with
`references/` names a file inside this skill's own directory, beside this file. Every other path
belongs to the project under change, including `PRODUCT_SPEC.md`, `ARCHITECTURE.md`,
`TEST_MATRIX.md`, `ROADMAP.md`, `JOURNAL.md`, `docs/prover/`, and `.live-spec/`.

- **the pack** — the shipped live-spec method: its skills, its document templates, and its gates.
  `skills/live-spec-base/SKILL.md` holds the shared rulebook and names the ten working skills.
- **host** — one project the pack attaches to. Each host holds its own spec, queue, journal, and
  `.live-spec/` folder.
- **the human** — the person who owns the product decisions. A taste call, a threshold, and a policy
  all reach them.
- **seat** — the orchestrating session that owns judgment, briefs workers, and reports to the human.
  This page also calls that actor the senior and the orchestrator.
- **worker** — a delegated session the seat briefs for bounded mechanical work, narrowed to the files
  its brief names. This page also calls it the junior.
- **wish** — one request as it was spoken, before the door places it.
- **door** — the intake classification that places a wish at one entry point: feature, bug, refactor,
  docs-only, or skip. It is decided before any code is written, and it stands apart from the wish's size.
- **work-kind** — the intake axis naming what a wish produces: product, infra, skill, or prose.
- **footprint** — the reach of one change: presentation-only, single-module, or cross-cutting.
- **tripwire** — one fixed rule in the door step that lifts a wish to a door whatever its casual label.
- **row** — one line of the project's queue, `ROADMAP.md` in this pack, holding one piece of work.
- **spec-delta**, also **the delta** — the set of spec sentences one wish adds or changes.
- **regression fence** — one sentence in a delta naming a neighbouring promise that must stay true,
  citing the existing clause it guards.
- **landing** — the act of one piece of work reaching the repository's shared truth as one commit.
- **lane**, also **train** — one build lane a session rolls through the pipeline.
- **the pen** — the single write-lock a repository holds. One lane at a time writes shared files under it.
- **departures board** — the status view read live off the queue's open rows. It names each rolling
  lane's step, and whom a waiting lane waits behind.
- **red**, used as a verb — a check fails and stops the work at that point. **Green** names a run with
  zero failures.
- **gate** — a check that must pass before the work proceeds.
- **architecture node** — one named unit in `ARCHITECTURE.md`. It carries one responsibility, owns the
  spec facts it implements, and pins them to the code.
- **seam** — the named boundary between two nodes, stating what crosses it and who owns the format.
- **checkpoint** — a saved point of work a session or a worker resumes from, written under `.live-spec/`.
- **norm** — an approved prototype frozen as the binding record of a surface's look and feel, kept
  under `docs/norms/`.
- **problem ledger** — the per-host file `.live-spec/PROBLEMS.md`, recording the workshop's recurring
  operational noise.
- **class hunt** — the search a confirmed bug drives before it closes. Name the defect abstractly,
  find every sibling of that kind, and fix them together.
- **compaction** — the station that removes redundancy from a document or from code.
- **shopfront** — the public README as the reader-facing front of a repository.
- **attic** — the host's append-only archive folder, `attic/`, where a superseded file moves.

**The bracket codes.** `INV-`, `T-`, `E-`, `ACT-`, and `M-` codes index requirements in this pack's
own `PRODUCT_SPEC.md`. `PRODUCT_SPEC.index.md` maps each code to the criteria that carry it. The word
`SPEC` before a code marks that same home and names no separate series. `M-1` is the milestone gate
and `M-6` is the push gate. A **base rule N** points at the numbered rule N in
`skills/live-spec-base/SKILL.md`; its own frontmatter states how many it carries. A **communicator rule N** points into
`skills/communicator/SKILL.md`. That file numbers twice: its behaviour rules carry an inline
`(rule N)` tag, and its writing-register checklist restarts at 1. This page names which of the two
it means each time.
Each sentence beside a code states its own
rule in full, so a reader holding this page alone can pass the codes over.

## The pipeline in one line

One pipeline, and steps 1, 2, 5, and 6 each invoke a named skill. The order is **spec → prove → architecture → prove architecture →
matrix → test → code → verify → commit & show**. A bug shortcuts to **bug → matrix → test → code** (citing the
existing architecture node it lands in). **Skip the pipeline only where all three of these hold.**
The change touches a single file. It adds no new state, no new element, and no new user-visible
behaviour. An existing test level already covers the touched fact. A skip still ships a test. The
order of test and fix follows test-author's small-fix path — red first by default, and a one-batch
fix owes the mechanical red proof. A skip still owes the door step's spec-backed-literal tripwire:
does this edit touch a spec-backed literal or clause? A yes routes the docs and the test into the
same session as the fix (SPEC INV-104). Anything touching visibility / layout / colour enters at the
matrix step minimum. Otherwise don't skip a step — the bugs that pass every test hide in the steps
you skipped. (The private playbook repo's PLAYBOOK.md holds the principle behind each step. This
skill is its executable projection; keep the two in sync.)

**The craft ladder — which craft's standards judge each step (SPEC INV-33).** Each artifact is judged
by its own craft's standards. The **spec** is judged as a strong product manager judges it: the
user's journey, the product's words. **Prove** and **prove architecture** are judged as the prover's
formal-methods reviewer judges them. The **architecture** is judged as a software architect judges
it: nodes, seams, one responsibility each. The **matrix** is judged as a QA automation lead deriving
coverage. The **test** is judged as the same QA engineer writing it. The **code** is judged as a
senior developer. **Verify** is judged by the visitor's own fresh eyes, the builder's own view set
aside. **Commit & show** is judged as a careful release hand whose reader is the human.

The delivery report's step accounting speaks in these standards. The craft each artifact was made under is
namable on ask.

The craft takes the work-kind's form (SPEC INV-22, INV-33). On a prose product the code step is
worked as a strong writer. On infra it is worked as a toolsmith. The ladder names the archetypes, and
the kind says what their standards look like in its medium.

## When to run it — and where each kind of change enters
- **Step zero, before ANY tool call: name the door aloud (SPEC T-12, INV-16; base rule 15).**
  The human then hears the intake line back as the capture echo. The echo names heard · door · name ·
  row · place on the map (communicator rule 12, its capture-echo behaviour rule). Its spec codes are
  INV-27 and INV-37.
  - The intake line states size, priority, door, and work-kind. A wish too big for its worth is
    negotiated in scope — cut surfaces or split into stages, never a time budget or estimate.
    Proposals proceed on the recommended option and are surfaced (SPEC T-15). The door is one of
    feature · bug · refactor · docs-only · skip. The work-kind is one of product · infra · skill ·
    prose — what the wish builds, one kind per wish. The kind scales the form of every step the wish
    walks (the work-kind table at [references/work-kind-table.md](references/work-kind-table.md);
    SPEC T-16, INV-22).

    The same line places the wish on the product's feature map — **changes feature X · a new feature ·
    restructure**. The placement is spoken in the echo and written in the row's `map:` note. The map is
    the spec's scenario sections plus the architecture's nodes, never a third document. A restructure
    verdict queues its own row: refactor door if only structure moves, feature door if behaviour moves
    too. The re-carve happens only through the architecture step and its re-prove (SPEC INV-37). A
    same-version docs-layout pass rides one sanctioned light vehicle. The pass builds on a clean pushed
    base, and locks the owner's decisions in a checkpoint first. It proves content survived by a
    word-token multiset check and a punctuation multiset check (SPEC INV-111).
  - **The same line reads the FOOTPRINT — a three-source impact read that decides the route (SPEC INV-128).**
    Beside the door and the work-kind, read the change against the spec, the architecture and the code
    at once. Name one footprint — **presentation-only** · **single-module** · **cross-cutting**. The
    footprint is spoken in the echo and written in the row's `footprint:` note. See
    [references/footprint-read.md](references/footprint-read.md) for the full read: how the footprint
    composes with the door, and what each footprint grants each step. That page also carries what a
    three-source disagreement owes, and the mid-work re-classification.
  - Tripwires decide by rule, ahead of judgment — a new user-visible surface · new persistent state · a new interaction on an existing surface
    · the spec marks the touched surface [target] · behaviour no spec clause backs ⇒ FEATURE, however
    casually asked. The tripwire verdict outranks a casual "bugfix" label, and queue-cutting belongs to the
    bug door alone — a re-doored wish takes no preemption.
  - Re-fire the door mid-work the moment the work is about to create a surface or state its door
    doesn't grant. Stop, reclassify, and continue by the right door. The re-door sometimes creates a
    surface or state that did not exist when the lanes opened. In that case the same re-check
    **re-runs the independence edges against every rolling lane (SPEC INV-131)**. The new surface can
    collide with a sibling that was independent a moment ago. A new edge pulls the re-doored lane back
    to serial, waiting behind the lane it now shares a surface with. The board carries a line for that
    move. That way the departures board never asserts a stale independence after the ground moved. The
    integration re-fence [INV-39] still catches the collision at landing; this closes the board's
    observability gap and adds no new net.
  - **A declared mockup-first entry condition is honoured from the row, cancelled only by name (SPEC
    INV-43).** See [references/mockup-first-entry.md](references/mockup-first-entry.md) for where the
    condition is written, what cancels it, and the worked case behind it.
  - **One wish = one user story (SPEC T-17):** a wish carrying several distinct things a person will
    do and see splits at intake. Each story takes its own row through the full pipeline. Stages slice
    one story's depth — that is T-15's knife — and separate stories never fuse into one row.
    Sub-behaviours (a hover face, a phone face, a backpointer) are the story's acceptance, folded into
    the one story. Unclear whether it is one story or two ⇒ ask at intake. And every row born of a
    split cites the one spoken wish it came from. A request to merely see or try, with no commitment,
    goes to a labelled prototype home instead (base rule 16). It stays a prototype, outside prod and
    unshown as product.
- **The door set is CLOSED, and a request enters at the highest document its change reaches (SPEC INV-151).**
  A request enters at the highest document in the derivation chain whose sentences must change to
  satisfy it. The chain is spec → architecture → matrix → code → docs. The settings ladder stands
  beside the chain for a pure value. Walk the chain from the top: after this is done, would any
  sentence in this document read differently? The first yes is the entry layer. The request then flows
  down through every step its door grants. The set of entry points is closed. Every request kind has a
  named home and a mandatory back-check. A request the set cannot place is one plain question, never
  an improvised route:

  See [references/request-kind-table.md](references/request-kind-table.md) for the full closed set of
  request kinds, their entry step, and mandatory back-check. The kinds are: product behaviour · a
  technically-phrased request · a defect · docs-only · a tiny reversible edit · a settings/parameter
  value · an inbox wish · a method/skill change · a sketch · research/a question · a feedback hand-back.

  **A request that matches no kind in this closed set becomes one plain question to the human (base
  rule 1), never a guessed route.**

  The closed set makes "no gap between the layers" a checkable property held by rule, where before it
  leaned on habit. The landing contract already lists every door-granted step applied or stood down by
  name (SPEC INV-22). So a request the set cannot place is surfaced to the human as a question. This
  is the request-side twin of three other findings. They are the property net's homeless-item finding
  (SPEC INV-150), the deferral test's (SPEC INV-152), and the earned message's (SPEC INV-189,
  INV-191). The four are one routing principle stated four times (SPEC INV-153). Every incoming thing
  routes to the home whose declared sentence governs it. A thing that pins to no home is itself the
  finding. The fourth control carries the principle across a window's edge. A message to another agent
  routes to the sender's own blocked work. A question no work stands on is dropped and never sent.
- **New feature / new stateful surface / behaviour change:** the full pipeline from step 1.
- **Bug:** enter at the matrix step with a red-on-bug test (`bug → matrix → test → code`). If the
  fixed fact also lives in SPEC prose, update the spec sentence in the same change.

  **The door step adds one tripwire at the bug door**. The tripwire asks: does this edit touch a
  spec-backed literal or clause — a version string, a pinned count, a named vocabulary, a promised
  wording? A yes binds two rules into one duty: the docs-travel-with-the-change rule, and the
  red-first small-fix path. Under that duty the docs and the test land in the same session as the
  fix. The tripwire reads the edit's content, so a one-word change to a spec-cited literal owes the
  same duty as a full feature (SPEC INV-104).

  **A confirmed bug drives a class hunt before it closes (SPEC INV-124). The hunt is four moves:**

  1. Name the defect abstractly — the kind of mistake, such as a scope too narrow, a missing guard,
     or an assumption that holds in one place and fails in the neighbour. Then actively search every
     surface where that kind could live, and fix all siblings in the same change. The search goes
     finding the siblings not yet seen. The matrix row and the red-on-bug test cover the class beyond
     the single instance (base rule 14).
  2. Check the architecture. A structural cause — a boundary drawn wrong or left silent, a node
     owning what it should not — updates ARCHITECTURE.md in the same change. A cluster in one
     district reads as an architecture smell.
  3. Check the spec. A spec silent on or under-describing the broken behaviour is the real defect,
     and it is fixed first so the prover can flag it. The code fix then lands under it (the
     spec-under-describes-composition lesson, generalized).
  4. Escalate to the human when the class boundary needs his read: which behaviours are one class,
     what the intended design was, whether a whole area wants a rethink. The method stops and asks
     for the boundary, and does not guess it.

  The four moves are the bug door's close condition. A point fix that leaves the siblings standing is
  a status, never a landing (SPEC INV-26).

  **A RECURRING bug re-doors to feature**. A second bug in the same area within ~30 days is not
  another patch: the area is missing an INVARIANT. So it escalates to the full pipeline from step 1 —
  spec the invariant, re-prove, then fix under it. The journal is how you notice: before taking any
  bug, grep JOURNAL.md for the area's name and check the dates.
- **Removal of a shipped feature is a change too.** The spec section becomes a dated tombstone marked
  removed. The matrix rows are retired, and none is left standing as built. The owning tests are
  deleted, and SKILL.md / README are swept — all the same session. (This is the step that actually got
  skipped once: an excision cleaned code + tests but left four doc surfaces dangling.)
- **Refactor (behaviour-neutral):** no spec/matrix delta. Enter at step 8 with the FULL suite, the
  visual sample set, and a matrix audit of the touched sections. A monolith refactor re-risks
  everything. Where the refactor moves node boundaries but leaves the document's shape standing,
  ARCHITECTURE.md's pins update in the same change. The pins-only path is scoped to a boundary shift
  that leaves the document's shape standing. A deliberate redesign restacks layers, moves a surface's
  ownership, or merges or splits nodes. Such a redesign re-shapes the architecture document to the new
  form, and re-proves it with the architecture lens in the same movement (SPEC INV-113). Updating the
  pins alone does not cover a redesign.
- **Docs-only change:** re-read the changed section rendered + one grep that no stale claim contradicts the
  code; no spec/matrix step.
- **A rewrite or restyle accounts for every removal of substance (SPEC INV-109).**
  The rule's one home is communicator rule 6, the removal-accounting step of that skill's
  writing-register checklist. That step owns the delivery report the accounting rides. The docs-only
  door above and the restyle loop both invoke it. Every removed section, argument, rationale, or
  worked example is listed there with its one line of judgment. A removal the rewriter cannot justify
  is raised as a question before the report closes. Line-level wording is left free.
- **A restructure or migration merged back to main is gated on the delta (SPEC INV-114).**
  A restructure or migration merge gate judges the delta. It has three parts. The first is
  load-bearing token identity old-versus-new, modulo the per-chunk named deltas, plus the
  punctuation-multiset check (SPEC INV-111). The second is the full suite green on the merged tree
  (SPEC INV-39). The third is a full prover pass on both sides, whose blocking set is delta-scoped.
  That set is an unmatched token, a red suite, a new-side finding absent on the old side, or an
  unnamed meaning change. Pre-existing findings equal on both sides route to queue rows in the same
  landing and never block. And a session that sharpens a human's spoken bar beyond his words says the
  sharpened form back and marks it as its own interpretation. The token-identity part scopes to a
  content-preserving restructure. A deliberate redesign changes content by intent, so it routes by the
  architecture-redesign law (SPEC INV-113). Its merge stands on the green suite and the delta-scoped
  prover pass, with no token-identity demand over text the redesign meant to change.
- **Skip entirely** only under the single boundary above (pure research, fact-gathering, a one-file
  no-new-behaviour edit already covered by a test level).

## Work that belongs elsewhere

The pipeline's skip covers the skip-boundary edit. That edit touches a single file, adds no new state,
element, or visible behaviour, and lands on a fact an existing test level already covers. It still
ships a test, just no pipeline. Two other kinds of work stand outside the pipeline rather than
skipping it. Pure research and fact-gathering change no artifact, so nothing enters here. An ask that
only wants to see or try something goes to the labelled prototype home (base rule 16). It comes back
through this pipeline only at promotion.

## Setting a project up on the pack

A session that hears "attach live-spec to this project", "found a new project on live-spec", or
"update live-spec here" runs a setup walk first. Read
[references/project-setup.md](references/project-setup.md), the routing card beside this page. It
resolves the pack tree, reads the project tree, and names the walk this project takes. The setup
entry stands outside the derivation chain, beside the sketch lane. When the walk finishes, the first wish enters at its
own door like any other request.

## The work-kind table — what the wish builds scales how each step runs (SPEC T-16, INV-22)

The door picks which steps run. The kind picks the form each running step takes. The work-kind table
at [references/work-kind-table.md](references/work-kind-table.md) is the per-kind meanings' one
normative home. That is the one place they are stated, and the spec binds the contract around it.

The contract stands before the table. At landing, every door-granted step has either **APPLIED in its
kind's form or STOOD DOWN by name** in the delivery report. A stand-down reads like "design-sync —
text product, stands down". A silently skipped step is a defect. **An unresolved kind scales nothing
down** — standing a step down requires a named kind (the ask rides the row, SPEC INV-12). And no kind
ever touches the safety net. That net is the door law and its tripwires, the delta's mandatory
sentences (fences · facets · non-goals · success measure), and ask-at-intake. A scope cut obeys the
same law (SPEC T-15).

See [references/work-kind-table.md](references/work-kind-table.md) for the full table of how each
step takes shape under product / infra / skill / prose. The steps are: 1 spec · 2 prove · 3
architecture · 4 prove architecture · 5 matrix · 6 test · 7 code · 8 verify by deed · 9 commit & show
· design-sync/snapshot. That table also carries the verify-by-deed VISITOR WALK and FEEL pass (SPEC
INV-30, INV-136, INV-139), and the skill-review duty (SPEC INV-99).

## The steps

1. **Spec — invoke `spec-author`.** Write or grow the project `PRODUCT_SPEC.md`: entities, states, transitions,
   actors, invariants, and the cross-section composition between surfaces. One surface = one name. Compose
   every stateful surface across **every** view/mode axis it lives under, including axes beyond its own. Real gaps are
   marked `⟨DECIDE⟩` and asked, never guessed. Use human-first language, with codes at line ends.

   A feature-doored wish also walks the **fit walk** and the **standard-facet sweep**. The fit walk is
   the kind-scaled product-fit interrogation: journey · flows · trigger lenses. Its lens lists live in
   spec-author, its prover mode is FEATURE-FIT, and its code is SPEC INV-29. The standard-facet
   sweep's canonical list lives in spec-author: phone/narrow layout · touch-vs-hover ·
   empty/error/loading · accessibility · performance. Every facet ends as a spec sentence, decided or
   `[default]`-tagged and told at landing as a plain-words tradeoff, never a confirmation request
   (SPEC INV-31). A mid-work re-door walks the sweep before work resumes (SPEC T-13, INV-18).

   And when the wish touches a surface that already lives, the delta opens with **regression fences**
   before that sweep. A regression fence names a neighbouring promise that must stay true, and cites
   the clause it guards. Each fence is named by anchor in the wish's row. A fence discharges through
   the cited clause's existing never-side row, never a new row (SPEC T-14, INV-19).

   The delta CLOSES with its two sentences. The first is non-goals, where "nothing left out" is valid
   and a narrowing one is surfaced. The second is one success measure, decided or `[default]`-tagged
   (SPEC INV-20, INV-21).

2. **Prove — invoke `product-prover`.** The prover only catches a cross-section hole when both sides
   are present and named the same at prove-time. A surface absent or unlinked then is invisible to it.
   The prover has two modes (see product-prover), **FULL** and **CROSS-LINK**. **FULL** walks all
   phases over the whole spec, and is required at MINOR gates and structural rewrites. **CROSS-LINK**
   walks the new surface's seams against the named existing surfaces, on every surface add.

   **Write the findings to the project's `docs/prover/YYYY-MM-DD.md`** — that record lives in the repo
   under review, separate from this skill's. **Give each finding a folded / rejected(+why) column**, so
   "fold every defect" is verifiable after a wipe. The next prover run opens by checking the previous
   file's unfolded rows. Fold every defect by the book, and record the recommendations. Resolve every
   `⟨DECIDE⟩` that the surfaces under change touch, asking the human when it's genuinely their call.
   List the remaining open ones in the reply so the count is visible. The step does not gate on
   resolving all of them.

   **Then, when the cadence calls for it, invoke `design-reviewer` over the same proven spec** (SPEC
   INV-141). It is a second pass right after the prover that judges the design, where the prover
   before it verified the spec holds. It proposes the same-kind groupings the text never declared, and
   checks behaviour parity within each. The cadence decides whether it runs at all. It runs full on a
   FULL prover pass, and scoped on a surface add. It stands down at FEATURE-FIT intake and the push
   gate, where it is not invoked.

   Every finding is a recommendation or a question and never a defect, so it never holds the lane. A
   confirmed grouping lands as a class clause through spec-author. That class clause
   **re-enters the prove step**. The prover re-reads it, and the design review re-reads what it
   re-partitions. The
   loop is bounded at three progressing rounds, and surfaced to the human at its cap without holding
   the lane [INV-154]. Only once the loop rests are the tests derived. Its strongest likely divergence
   rides the batched questions as one ask with two objects in hand (SPEC INV-142). Its record is
   `docs/design-review/YYYY-MM-DD[-suffix].md`.

3. **Architecture — write or update `ARCHITECTURE.md` from the proven spec** (template:
   `templates/ARCHITECTURE.template.md`). Template paths here and in step 5 resolve from the pack
   repo, github.com/happysasha18/live-spec. A standalone install fetches them there, never from the
   skill dir: the pack is the source, a copy would fork the truth. Named nodes, one responsibility and
   one name each. Every spec fact is owned by exactly one node. Named seams run between the nodes.

   The project's kind (`project.kind`, SPEC INV-36) PROPOSES the starting node structure. A fullstack
   app splits frontend / backend / template / store. A CLI takes one node per command, and a skill
   pack takes one node per skill. The template's "Node structure by project.kind" table carries the
   per-kind scaffold. The spec's facts then decide the final nodes, and a speculative node is still
   unbacked structure the prover flags.

   In a live codebase every node pins to its owning `file:line`. **This step is where the spec is
   reconciled with reality**. Each pin comes from a command you ran, never from the doc's own prose,
   your memory, or a worker's summary. Those are leads to verify (base rule 13). Specs drift from
   code, so fix the spec to the shipped truth, always in that one direction.

   A large or surface-class change updates the doc. A bug or small change just cites its existing node
   and skips to the matrix. (Running the pin-greps is junior work; judging what a mismatch means is
   the senior's.)

   **The architecture owes numbers as well as names (SPEC INV-41):** measurable quality budgets, plus
   each budget's instrumentation home. The instrumentation home is where the real numbers are measured
   and where a human can read them — an export, a debug view, a report. The author also names each
   budget's watcher. That watcher is the mechanical check that reds past the stated number, or the
   decided sentence naming why that budget is read by eye.

   WHAT is measurable comes from the project's KIND (SPEC INV-36). Ask "what does quality mean here,
   in numbers?" before writing any. See
   [references/architecture-step-detail.md](references/architecture-step-detail.md) for the per-kind
   numbers and for the quality that has no honest number.

   Each budget is asserted by a matrix-row acceptance, never a hope in prose. A surface with no budget
   line and no instrumentation home is a derivation defect, exactly like an unowned fact. The numbers
   are the host's taste. Propose with a recommendation, and set on the human's word at the surface's
   first budget landing.

   **The doc owes two more views beside the node map (SPEC INV-74, INV-75), scaled by kind:** the
   **runtime view** and the **placement view**. See
   [references/architecture-step-detail.md](references/architecture-step-detail.md) for what each view
   walks and states.

   **The doc is iterative, current only to what's shipped or in flight.** It maps the product as it
   stands plus the landing in flight. A node exists for what ships today, or for what the spec already
   promises under an owned queue row (marked [target], pin empty).

   A future feature earns its node when its landing arrives. A speculative node is unbacked structure,
   and the prover flags it. "Should I architect the next few milestones now?" is answered no strictly
   by the method, taste playing no part.

   **Every new or carved node passes a three-question fitness test at its birth (SPEC INV-122).** The
   three questions are these. The first is: can it be tested alone? The second is: does a real second
   place need it? The third is: can it and its neighbour be worked in parallel without queuing on
   shared files? Three yes answers make the node
   right. A single no is a flag to answer — name the plan that turns it to a yes, or fold the carve
   back. Two or more no make it premature. See
   [references/architecture-step-detail.md](references/architecture-step-detail.md) for the test's two
   homes and how a carve that fails it is folded back.

   Re-carving the whole node map is legal. It arrives as a restructure placement's own queue row (SPEC
   INV-37), walks this step, and is re-proven like any structure change. A placement may say the shape
   no longer fits; only a landing changes the shape.

   **Structure is deliberately redesigned when layers are restacked, a surface's ownership moves, or
   nodes are merged or split. In that case the architecture document is re-shaped to the new form and
   re-proven with the architecture lens in the same movement (SPEC INV-113). Updating the pins alone
   is scoped to a boundary shift that leaves the document's shape standing. After a real redesign the
   old shape itself lies, so fresh pins on a stale shape are a defect.**

4. **Prove the architecture — invoke `product-prover` with the architecture lens** whenever the doc
   changed in step 3. It runs six checks, each at the project's kind scale. Every spec fact has an
   owning node. No node stands without spec backing. Every seam names what crosses it and who owns the
   format. The quality budgets are stated with their instrumentation homes, each naming its watcher
   (INV-41). The runtime view walks every promised flow (INV-74). The placement view says where every
   node runs (INV-75).

   Findings land in the same `docs/prover/` record discipline as step 2. A full pass at an M-1 or M-6
   gate proves ARCHITECTURE.md beside the spec (INV-116). Such a pass also **appends its dated row to
   the architecture prover record** at `docs/prover/architecture-prover-record.md`. That is the dated
   home the record moved to when the architecture became a format member (SPEC INV-279). So that
   record tracks the architecture's freshness rule and stays current with it.

5. **Test spec — invoke `test-author` to derive `TEST_MATRIX.md` from the proven spec through the
   proven architecture (the method's one home, SPEC E-27).** The matrix is derived, and hand-filling
   its rows does not count. Rows are organized **architecture node × spec fact**, one block per node,
   and every fact gets ≥ 1 row. Then **every row states BOTH sides — what the fact DOES and what it
   must NEVER do**. The never side is the regression fence (SPEC INV-6), and a row without it is a
   derivation defect. And **every row pins a test level** (string / DOM-text / browser-computed /
   pixel).
   Any fact about visibility / layout / colour / interaction gets level ≥ browser-computed.

   It opens with an **artifact inventory** — every file the user receives. Every inventory entry owns
   at least one rendered-level row. Derivation closes with the template's **coverage validation
   checklist, actually walked**: every anchor ≥ 1 row · every node's negative-side rows exist · no
   stale refs. The template is `templates/TEST_MATRIX.template.md`. Its own current text says two
   mechanical checks now hold those facts, so read the template before walking anything by hand. A
   fact with no row or at a too-weak level is a derivation defect, fixed here.

   The matrix is the bridge: tests come from the matrix, upstream of the code. (The mechanical
   projection is junior work; choosing each row's level + assertion is the senior's.)

6. **Test — with `test-author`, write tests that assert the real shipped artifact.** Render the
   widget, produce the file, or call the function, and inspect the output as real behavior. A match
   against the source text counts for nothing here. Watch the new test fail first (red-on-bug), then
   implement. Never edit a test just to make a change pass.

7. **Code — implement until green.** Delegate well-scoped, mechanical implementation to a junior
   worker with a precise brief + a persistent checkpoint file, so a cut-off resumes from its
   checkpoint. Keep the hard parts (ambiguous specs, design, tricky debugging) on the senior model.
   Verify the junior's result by deed.

   **A norm-pointered surface builds with the artifact open (SPEC INV-43).** When the surface's spec
   clauses carry a `norm: <path>` pointer, OPEN the artifact before building. The frozen prototype is
   the norm for look and feel, and the clause text only its laws. Record a one-line plan-vs-prototype
   diff in the landing's accounting. A missing diff line is a defect at review. The verify step's feel
   bar (step 8) reads the same pointer.

   **Taste-heavy deliverables build smallest-first (SPEC INV-62).** Taste rules a deliverable of
   voice, copy, visual style, or spec prose. There, stop at the cheapest judgeable sample: one
   paragraph, one card, two sections. Take the human's word on it before the full build spends
   anything. Five full packs once failed on a problem a one-paragraph sample would have caught.

   **And a rejected artifact reopens its SOURCE (SPEC INV-63)**. The fix starts at the spec clause /
   card / brief that produced it: correct the source, then rebuild from it. Line-patching the rejected
   output against an unchanged source is the five-round trap, banned.

8. **Verify by deed.** Run it and see the result with your own eyes. Only call it done/working after that;
   otherwise label it an assumption.

   Run every check the diff can reach before any push — the reach map's law (SPEC INV-45). A
   prose-only diff runs the doc gates whole and says so. Any code, spec, matrix, skill, or test file
   in the diff means the whole suite. The reach map itself is the `reach_classes` block of
   `guardrails.config.json`, which pairs each file class with the checks it reaches. The pack's suite
   runs as `python3 -m pytest -q` from the repository root; a host with another runner names its own
   in its profile.

   **A session that spawned a worker runs `python3 guardrails/check-worker-restore.py` here, and reads
   its verdict before it accepts the worker's result (SPEC INV-298; the gate INV-299)**. See
   [references/verify-step-detail.md](references/verify-step-detail.md) for what the gate reads, the
   window it reads, and what a red owes.

   **Green means zero failures, and a skip-set exactly matching the expected pinned list**. An
   unexpected skip — Chrome absent, a real-data fixture missing — is a failure outright. **If red at a
   pause or session end, never commit.** Write the failing test name + hypothesis as the top
   `NEXT_STEPS.md` item. That red test is the checkpoint.

   **Green also means deterministic (SPEC INV-155).** A test that passes only sometimes is a defect,
   and intermittent green does not count as a pass. A flake whose root is in owned code — the test or
   the product — is fixed at that root. Name the nondeterminism: wall-clock time, ordering, shared or
   leaked state, an unseeded random, or a missing wait on a tool the test drives. Then remove it, so
   the test passes every run for the same reason. It is masked by nothing. Never a retry, never a
   rerun-until-green, never a raised timeout that hides the race, never "it passed this time" taken as
   a pass. Sometimes the nondeterminism is not removable in owned code, the external tool itself misbehaving at
   random. Only then is it workshop noise on the problem ledger [SPEC INV-23], a separate home.
   Green means deterministic.

   **The audit — a second pair of fresh eyes, REQUIRED where the stakes are high and only the
   author has judged the work (SPEC INV-46)**. Verify runs a fresh-context checker when the change is
   high-stakes and its only review is the author's own. High-stakes means one of two things. The delta
   is surface-sized, meaning a new surface or a multi-file behaviour change. Or the change edits the
   method itself — a rule whose meaning changed, a new or re-scoped invariant. A wording-only edit
   that changes no rule's meaning is not a method edit.

   The author's own review means no independent read has happened. An independent read is a
   differently-contexted head briefed from the primary sources on the "goal missed" hypothesis. A
   prover pass in the author's own context never counts as one. And delegation never makes the review
   independent, since the same head that briefed the worker reads the result. See
   [references/verify-step-detail.md](references/verify-step-detail.md) for the rest of the protocol:
   how the checker is briefed, the ladder it walks, and where its findings go.

   **The authoring seat never certifies its own work adversarially (SPEC INV-237)**. The freshness
   above is the whole rule, and the release pass may not waive it. A release's adversarial pass is the full re-prove at the release
   gate. It is authored by a fresh seat, never the seat that authored the change. A newly added lens or rule is run against the very document that introduces it before
   release (self-application), and the release record names the result. A release gate may require a
   dated clean-context review record naming a seat other than the release's. The mechanical floor
   checks that the record exists, is release-dated, and names a different seat; the rest is a
   discipline the seat holds.

9. **Commit & show.** Commit when green with no regression (unasked). Same or better is enough, and
   the work never waits for perfect.

   Where the host has a remote, PUSH accepted work there by rule (SPEC INV-82). The push stands on two
   things. First, every gate the diff reaches ran and passed, the verdict read from the suite log's
   own line. Second, the host's own push lines. The remote is discovered from the tree. Only a host with no remote
   gets one contextual question at the first push moment. The question is: create one — GitHub,
   GitLab, whatever the human names — or stay local, recorded in the host profile.

   Every push re-walks the README against the pushed truth, crisp and current, a stale claim fixed
   before the push. That is the shopfront law at every-push cadence. After the push the push step
   reads the remote gate's own verdict: the CI run the push triggered, one `gh run` read. A red
   verdict is the pushing session's own immediate bug. It is fixed and re-pushed the same session
   before anything else, so the human never meets the red first in a GitHub email. A slow gate is
   watched to its verdict on the detached-work cadence (SPEC INV-106, INV-35). The human's personally
   named gates still wait for his word.

   Bump the version, PATCH by default. The number reports what taking the release costs a host, and
   the tier is read off that cost. A patch fixes a machine to hold a law already stated, and the host
   does nothing. A minor grows what a host may adopt by re-running its catch-up walk with nothing
   rewritten. A major forces a host action and ships its dated MIGRATION.md chapter (base rule 32 /
   SPEC INV-217). The minor-versus-major call is a stated judgment the releasing session makes and
   names, held by no gate.

   Docs travel with the change — README + CHANGELOG + the skill's own `SKILL.md`, same session. Diary
   the why in `JOURNAL.md`.

   **The CHANGELOG speaks to the USER, the journal to the builder**. Each entry says what changed for
   the person using the product, with one concrete example from real output, in outcome terms only.
   Function names, internal ids, and row numbers live in the journal instead. And no doc pins a
   drifting version number in prose, since "current version: vX.Y" always goes stale. Point at the
   version's one home — the VERSION file, the frontmatter — or omit it.

   The delivery report tells the taste choices made without asking — the open `[default]`s. Each is
   given in plain words with an example and a tweakable mark. No confirmation is requested; silence is
   consent, never re-asked (SPEC INV-31). The same telling covers a tunable parameter you set to a
   sensible default: a resolution, a batch size, a timeout, a sampling rate. Each is named with what
   it trades, and tuned together later at most. A knob you can reasonably pick never stalls the work
   (SPEC INV-70).

   A delivery report, a ROADMAP row, and a decision page are exactly the surfaces where a decision
   gets recorded as the person's. So base rule 13's writing rule on human authority binds them (SPEC
   INV-207). A `[default]` the seat picked is the seat's own judgment, and is written in the pack's
   own voice. It is never dressed as the human's word. When a decision genuinely is the person's, the
   entry names the exchange it came from — a date a reader can check. An anchored copy goes to
   `DECISIONS.md`, the read-back set the human reads on his own clock and strikes what he never said.
   An autonomy grant authorizes the seat to decide. It never authorizes recording that decision as the
   human's.

   Show the human the real render in a new window; push or deposit only after they've reviewed it. A
   push re-renders all deposited artifacts. A push shipping a new version walks the publish skill's
   shopfront check. That check reads README claims + kind-owed visuals fresh, the outcome line riding
   the delivery report (SPEC INV-44). Where the host's design-sync is ON (base defaults; SPEC E-18), the landing's
   declared components also sync to the team's design project. That sync happens after the human's
   gate, and it never replaces the in-session show.

## Guardrails — the pipeline's mechanical enforcement (every project inherits them)
The nine steps are guidance, and an agent drifts from guidance. That drift is the failure that stops a
project converging. A whole panel ships empty, a behaviour nobody asked for gets buried, a change
lands with no test. So the pipeline is enforced by a machine. The project wires a `guardrails` check
to a **git pre-push hook**, beside the suite. A change that fails any of these reds, and cannot be
pushed. `guardrails/` is a directory of check scripts, and the pack ships one runner,
`guardrails/pre-push`, that a project installs as its own `.git/hooks/pre-push`.
`tests/test_traceability.py` (below) is the first of these — generalise it to the full set.

**Each project instantiates the checks for its own surfaces, and the pipeline requires that the check
exists and is green**. This is a first-class step, applied across the whole project as a standing part
of the method. A per-project patch does not satisfy it. See
[references/guardrails-catalog.md](references/guardrails-catalog.md) for the four mechanical guardrails
(Completeness incl. cross-surface policy uniformity SPEC INV-125 · Tests-present · Behaviour-traces-to-spec ·
Conflicts).

**Honest boundary:** guardrails catch structural defects — an empty surface, a missing test, untraced
behaviour, a partial artifact, an id/naming conflict. A subtle semantic bug (is the number right?)
stands outside their reach, and still needs `product-prover` + a human's eyes. Enforce structure
mechanically, and reason about meaning with the prover. Verify-by-deed (step 8) and commit/push (step
9) both run the guardrails first, so guidance and enforcement agree.

## The excuses table — read it the moment one of these crosses your mind

The shortcuts that break the method never announce themselves; they arrive as one of these thoughts.
Each is a tripwire: thinking it means stop and take the pipeline door you were about to skip. The six
thoughts stand here, so this page alone can fire the tripwire:

- "it's a one-liner / just a prototype";
- "I'll write the spec after it works";
- "the human is in a hurry";
- "the suite is green, ship it";
- "asking would bother them";
- "explaining it would take longer than just doing it myself".

See [references/excuses-table.md](references/excuses-table.md) for the full table of six excuse-thoughts
and why each is a trap (SPEC T-12, T-15, INV-4, INV-5, INV-15).

## Gates worth remembering
- **Before a MINOR (0.x.0) bump:** the 3-pass preventive audit — product-prover on the whole spec + a
  matrix audit + a surface-composition check. The gate also carries the full design review (SPEC
  INV-141) and the cross-cut counter (SPEC INV-128, INV-37). It carries code compaction too, as a
  station beside doc compaction (SPEC INV-123). See
  [references/minor-bump-gate.md](references/minor-bump-gate.md) for the full gate procedure.
- **Compaction runs every pass, above the milestone gate (SPEC INV-164):** the doc- and code-compaction
  stations run at every push, above the MINOR gate that once held them alone. Every push is held to
  the reached-clean floor by the mechanical gates. Those gates are the register lint at zero errors,
  the redundancy gate at zero open pairs, and the debt cap that only ratchets down
  (`scripts/spec-debt-cap.json`). The suite asserts them against the live document, so no bloat
  accumulates between milestones. This is the fix for the spec bloating when compaction ran
  milestone-only (2026-07-15).
- **Process bookkeeping scales to the delta (SPEC INV-61):** the pre-push re-check keeps its rigor and
  scales its form. A small delta is a skill/prose/infra kind with no new surface and no structure
  change. It ships a three-line SHORT-FORM record: previous records clean · the delta in one line ·
  the verdict. A
  surface-sized or structural delta keeps the full walk. Claims batch per declared lane, and the
  journal chapter and the resume rewrite come once per landing batch. Four things never scale: the
  law's own text, the red-first test, the delta's prove, and the gates.
- **Order is law:** `spec → prove → architecture → prove architecture → matrix → test → code`;
  `bug → matrix → test → code`. Never code first and back-fill a spec. And never jump from spec
  straight to tests. The two layers between them — architecture and test-spec derivation — are where
  whole classes of holes get caught (SPEC E-14/E-15/INV-15).
- **A row closes only whole (SPEC INV-26).** Where a row carries several legs, its Done-when
  enumerates each. The delivery report may close the row only with every leg met —
  half-done is a status, never a landing. An open leg keeps the row in-work. The resume file's
  LIVE-STATE restates it at every supersession, and never compresses it away (still open at compaction
  ⇒ restated in full).
- **Trains, one pen (SPEC T-18, INV-39):** one session may roll up to the profile-declared lane cap of
  independent build lanes without asking. The lanes are picked by a dependency graph, and each one is
  opened as an act performed. Every shared-doc edit, the integration, and the closing of a row take
  the pen one lane at a time. See [references/lanes-and-pen.md](references/lanes-and-pen.md) for the
  full lane law: the cap and the independence test, the pen-stage rules, and the lane graph with its
  deferred-trigger re-scan. That page also carries the open-lane act and the drafter-applier form
  [T-18, INV-39, INV-49, INV-214].
- **Junior delegation (decided from the request, before the first tool call, SPEC INV-69):** judgment
  work stays senior — spec, prove, architecture, matrix-level calls, findings triage, any taste call.
  Mechanical work is known edit strings, a known command, fan-out fact-gathering, or a report or list
  or dump to produce. It routes to a worker at the cheapest tier that can pass the brief. That routing
  is proposed and logged, and the senior is free to override aloud.
  See [references/delegation-protocol.md](references/delegation-protocol.md) for the full protocol:
  the routing rule, the brief's three birth laws, and the worker contract. That page also carries the
  cleanup-safety constraint, and the delegation-reporting duty with its per-block root and plan-line
  accounting.
- **A worker never restores a working tree with a git command (SPEC INV-298; the gate INV-299).** Every
  brief this skill composes carries this clause verbatim. Before a worker mutates a file it means to put
  back, it reads that file and holds its bytes. A worker puts a file back by WRITING ITS OWN SAVED BYTES.
  A worker runs no command that discards uncommitted work, in any tree: `git checkout -- <path>`,
  `git checkout .`, `git restore` outside `--staged`, `git stash` and its `push`, `save`, `create` and
  `store` forms, `git reset` with `--hard`, `--merge` or `--keep`, and `git clean` with `-f` or `-x`. Such
  a command's blast radius is a PATH, so its damage lands on files the worker never wrote and its brief
  never named. This rule binds a worker in every tree, including its own isolated worktree, since a
  worktree shares one repository with the lanes beside it and a worker cannot read off its brief what else
  that repository holds. A worker that holds no saved bytes for a file it mutated, or that believes a file
  needs a git-level restore, HALTS and reports the file and the mutation it made, and it writes no further
  file and runs no further command. The orchestrator owns recovery: it restores the named file from the
  last committed stage, hands the worker a fresh brief carrying that file's current bytes, and records the
  halt in the row's delivery report, and the halted work resumes under that new brief. The orchestrator's
  own half: a finished build stage is committed before the next worker touches its files.
  `guardrails/check-worker-restore.py` reads the worker runs' transcripts for the command and runs at the
  verify step.
- **Traceability is a test, enforced automatically.** A standing `tests/test_traceability.py` fails the
  suite on four things. One is a matrix row citing a missing test. Another is a duplicate invariant
  id. A third is a spec invariant with no matrix row. The fourth is a ⟨DECIDE⟩ marked resolved that
  still carries the live marker. So drift is caught every commit, continuously, and never waits for
  the next MINOR.

## How it relates to the other skills
- `spec-author` — writes/grows the spec (step 1). Public.
- `product-prover` — reviews the whole spec with formal-verification thinking (step 2). External skill, installed by `scripts/install-external-skills.sh`; pack bindings in `skills/product-prover-pack/SKILL.md`.
- `design-reviewer` — a second pass right after the prover (step 2): judges the design, proposes the
  same-kind groupings the text never declared, and echoes the strongest likely divergence to the human;
  recommendations and questions only, never a block. Public.
- `test-author` — derives the matrix and writes the tests (steps 5–6). Public.
- `build-pipeline` (this) — the orchestrator that sequences them through to a shipped, verified, committed
  change.

The pack holds six more skills, and `skills/live-spec-base/SKILL.md` names the ten working ones:

- `live-spec-base` — the shared rulebook and the settings ladder. Every `base rule N` on this page
  points there.
- `communicator` — carries the work to the human. Every `communicator rule N` on this page points there.
- `publish` — runs the checks a publication owes its reader, invoked at step 9's shopfront walk.
- `text-audit` — reads a text as a stranger and repairs where they stop.
- `feedback-intake` — files what comes back from a person or an inbox.
- `feedback-collector` — offers a rare private note up to the pack's authors.

> The method, made durable: spec-author and product-prover each own one step; build-pipeline is the spine that
> runs the whole arc from a spec to a shipped, tested, committed change.
