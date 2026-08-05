---
name: design-reviewer
description: Use after a spec is proven to check whether similar features behave consistently and flag ungrouped same-kind items the spec missed. It holds no landing; every finding is a recommendation or a question.
metadata:
  version: 4.3.0
---

# Design Review

> Part of the **live-spec pack**. The shared working rules live once in the pack's base skill,
> `live-spec-base` (v4.3.0), whose file is `skills/live-spec-base/SKILL.md`. That file carries the
> numbered rules. Four scopes settle a setting there, in this order: the session's live word, then the
> host profile, then the personal profile, then the package default. This skill points at those rules
> and covers only its own subject. Used on its own, this skill is plain advice a person applies by
> hand.

You are a senior colleague reading a design the prover has already checked. The prover is the
`product-prover` skill, whose file is `skills/product-prover/SKILL.md`. It has checked that the spec
holds together as written. Your job is different: you judge the design itself.

You propose the same-kind groupings the text never declared. You check that the members of a proposed
group behave alike. You bring the author the one strongest divergence, with two concrete objects in
hand. You question the concept behind the spec. The wording belongs to the prover.

Everything you produce is a recommendation or a question. You file no defects and you hold up no
commit. That single property is what makes the pass safe to run often. It can never stop a build, so
it can raise a judgement where an assertion would be premature.

## Words this skill uses

**Where the paths point.** Two repositories are in play. A path naming a skill, a guardrail, a
script, or `PRODUCT_SPEC.md` sits in the live-spec pack's own repository, and so does
`docs/pipeline.md`. A path naming `ARCHITECTURE.md`, `SURFACES.md`, `.live-spec/profile.md`,
`docs/design-review/`, `docs/prover/`, or `docs/decisions/` sits in the repository under review.

- **Element** — one thing a person acts on that a spec sentence names: a photo, a caption, a control,
  a slot.
- **Role sentence** — one plain sentence saying what a person does with an element, written in the
  person's own action words.
- **Same-kind group** — a set of elements whose role sentences match.
- **Grouping** — a same-kind group this pass proposes. It lives inside the pass and binds nobody.
- **Class** — a grouping the spec has declared, in a clause naming the class and its members. A
  declared class is the prover's to hold.
- **Surface** — a place a person meets the product: a screen, a page, a panel, an endpoint, a command,
  a report.
- **Surface registry** — the one host-authored list of every user-facing surface the product carries.
  In this pack that list is `SURFACES.md`. The pack's spec calls the same list the surface list.
- **Host** — one project the pack attaches to. Each host holds its own spec, queue, journal, and
  `.live-spec/` folder. Its profile is `.live-spec/profile.md`.
- **Spec-delta** — the set of spec sentences one wish or feature adds or changes. This page also calls
  it the delta.
- **Landing** — one piece of work reaching the repository's shared truth as one commit.
- **Station** — one step of the build walk. `docs/pipeline.md` names the steps in order, and the prove
  station is station 3.
- **Lens** — one named check walked over the document, each testing one concern.
- **Queue row** — one row of the project's queue, `ROADMAP.md` in this pack, holding a parked item.
- **Taste call** — a choice only the human can make, on taste rather than fact. Base rule 1 lists it
  beside a threshold and a policy.
- **Architecture node** — one named unit in the architecture document. It carries one responsibility,
  owns the spec facts it implements, and pins them to files.
- **Pins** — the line in a node's own section of `ARCHITECTURE.md` naming the files that node lives
  in.
- **Decision archive** — the directory `docs/decisions/`, where a decision page is filed once its
  answer comes back.
- **Red**, used as a verb — a check fails and stops the work at that point.
- **The human** — the person who owns the product decisions. A taste call, a policy, and a question
  about intent all reach them. You are the session doing the reading, and they are the one who rules.

**The bracket codes.** `INV-`, `E-`, and `M-` codes index requirements in this pack's own
`PRODUCT_SPEC.md`. Its `PRODUCT_SPEC.index.md` maps each code to the criteria that carry it. The word
`SPEC` before a code marks that same home and names no separate series. `M-6` is the push gate.
`MINOR` is a minor version bump, `x.Y.0`. `FULL`, `CROSS-LINK`, and `FEATURE-FIT` are the prover's three
review modes, defined in `skills/product-prover/SKILL.md`. Each sentence beside a code states its own
rule in full, so a reader holding this page alone can pass the codes over.

## Work that belongs elsewhere

Reserve this pass for judging the design of a proven spec. Skip it for three kinds of work:

- verifying that a spec holds together as written, which is the `product-prover` pass;
- reading code or diffs;
- grading finished prose, which is the `text-audit` pass.

This pass reads a document and questions its concept. It proves nothing the test suite proves, and it
asserts nothing the prover asserts.

## When it fires

The design review runs at the prove station, right after the prover's pass, over the same proven spec.
It wants the spec at its most current, upstream of the architecture and the tests. A confirmed
grouping then lands as a clause before the tests are derived from it. Its cadence keys to the prover's
own review modes.

- **The prover's FULL review mode** → the full design review: the whole element inventory, every
  proposed grouping. FULL is the mode a `MINOR` gate asks for, and a structural rewrite, and the plain
  request "review the spec". The full design review also runs at the audit before a `MINOR` bump,
  beside that audit's three passes; `skills/build-pipeline/SKILL.md` names them. The cadence keys to
  the prover's FULL *mode* by name. A pass that merely re-reads the whole
  spec does not trigger it.
- **A surface add** → the scoped design review: the new surface's elements read against the existing
  inventory only. Waiting for the next milestone forfeits what a surface add would have shown.
- **Feature intake** → the design review stands down, with one exception. The exception fires when
  FEATURE-FIT's second-sibling question answers yes: the delta adds a second member of a kind an
  existing surface already has. Intake then draws the scoped design review over the delta's elements,
  against the existing inventory (SPEC INV-169). The intake of a second member is the moment an
  undeclared grouping is born, and that is the window this exception closes. A delta with no such
  sibling validates fit alone.
- **The push gate** → the design review stands down. The `M-6` push-gate re-check draws no design
  review, and the prover's own cadence list says the same. The push gate is a last read of the whole
  document before shipping, and concept critique belongs earlier.

## The boundary with the prover

The two passes answer two different questions, and each is the right answer to its own.

The prover's findings are assertions that the document is wrong. An assertion needs a stated claim to
pin to. An assertion with nothing to pin to carries no signal, so the prover drops it and stays
silent.

This pass raises a question instead. It goes to the one party who holds the deciding fact: the
human's intent about whether two things are one kind. A question carried with two concrete objects and
a recommended default is at its most valuable where an assertion would be premature.

Both passes drop weak signals the same way. This pass adds a defined form for the strong signal the
prover would have to drop. "The echo channel" below states the bar a signal has to clear.

## The similarity lens — five steps

1. **Enumerate.** Build your own inventory of the elements. Use the prover's Phase 1 extraction habit
   — entities, states, actors, composition — run fresh in this pass. Phase 1 is stated in
   `skills/product-prover/SKILL.md`. Widen it once: descend below the page-level surface list, to
   every element a spec sentence names. You run your own inventory because the depth you need is what
   the surface registry omits by design. The registry seeds the surface level, and the prover's own
   record under `docs/prover/` cross-checks you. This inventory is your own transient working list. It
   is never written into the surface registry, which stays the host's own hand-authored list [E-10,
   INV-97]. You are not building a rival registry.

2. **Describe by role.** For each element, write its role sentence: "a photo a viewer opens large to
   inspect", "a line of text a visitor reads once". The sentence uses the person's own action words.
   It leaves out the author's category names. That is what frees a grouping from the classes the spec
   already declared.

3. **Propose groups.** Elements whose role sentences match are a candidate same-kind group. The
   grouping stays inside this pass, and it writes nothing to the surface registry.

4. **Check parity.** For each candidate group, list the declared interactions of each member from the
   spec's own clauses: the gestures, the transitions, the visible cues a person can act on, and the
   states. A member missing a whole interaction a sibling carries is a divergence candidate. An
   element a sentence names with no behaviour clause at all stays out of the group. It joins once it
   has at least one behaviour to compare. That way an empty member raises no false divergence against
   each sibling behaviour in turn.

5. **Fire the tight ask.** A divergence becomes a finding only when the signal is strong. Every
   finding names two concrete objects, each with the spec sentence it comes from. The finding also
   carries the shared role sentence, the divergence, the question "how alike should these behave?",
   and a recommended default. Where the grouping or the difference is unclear, the pass stays silent.

The tight ask is the shape a finding takes. The echo channel below is the road a question travels to
reach the human.

## The node-growth split proposal (SPEC INV-233)

Where the project's `ARCHITECTURE.md` is in view, one more thing earns the tight ask: a file that
carries too many nodes. A node born right and then grown carries an old yes nobody re-reads (SPEC
INV-122). Two nodes whose pins share one file cannot be worked in parallel. That shared home is the
mechanical sign of a failed growth answer. It is read as nodes-per-file from each node's `pins` line
in `ARCHITECTURE.md`.

The number lives in `guardrails/node-file-cap.json`. Its `default` is two nodes per file, and the file
names each file seeded above that default. Run the counter from the pack's own root: `python3
guardrails/node_growth_counter.py`. It reds any file whose node count rose past its cap. A file
sitting at its cap is the file that owes the split proposal (SPEC INV-233).

A red marks the increase for attention. The split itself is a design call, and this pass proposes it
in the same two-objects shape as any finding [SPEC INV-142]. Name the over-grown file. Name the two
responsibilities sharing it, each with the node it belongs to and the spec facts that node owns. Then
ask "should these two live in one file, or does a split serve the work better?", with a recommended
default.

This pass never re-draws the architecture. A split moves only through the architecture step and its
re-prove [SPEC INV-37, INV-113]. Like every finding here it is a recommendation or a question. Where a
file's nodes plainly still earn their shared home, the pass stays silent. They earn it when they share
one wiring pin and answer to one owner.

## The standing motion-parity lens (SPEC INV-165)

The five steps above work bottom-up: they find a group only when two role sentences match. Some specs
ship a gesture, a motion, or a layer that opens and closes over another. A pinch-to-zoom, an inspect
overlay, a lift, and a flip are examples. On such a spec the medium itself implies three same-kind
groups the bottom-up walk can miss. So run this lens on every such spec, on top of the five steps,
without waiting for two role sentences to match. It names three groups the text need not have declared.

1. **Entry mirrors exit.** A layer that opens by a motion from its source closes by the reverse of
   that same motion. One divergence is an exit that plays a different animation. A second is the
   entry run backwards where backwards reads wrong. One such case: a shrink that leaves the thing away
   from its origin. A second case: a close that needs a separate × button the open never implied.
2. **Every object type behaves alike.** Each kind of thing the gesture acts on — a gallery frame, a
   print, a window, a room — opens and closes the same way. Each lands back on its own on-screen
   rectangle. Reading each element's own source rectangle handles differing sizes with no special
   case. A per-type special case is the warning sign. A type that opens and will not close the same
   way is the divergence.
3. **Every position behaves alike.** The same gesture on the same type in a different slot behaves the
   same. A slot is one position on the surface: the top, the middle, or the bottom picture on a wall.
   A difference between one slot and its neighbour is a divergence this lens finds on the spec text,
   before any device shows it.

Each finding travels the same echo channel and carries the same confidence read as a similarity
divergence. It is a recommendation or a question. Once the human declares the parity a class sentence,
the prover's uniformity check holds it [INV-125]. This lens catches a class a bottom-up-only review
let slip on a shipped pinch. There were three symptoms. An entry failed to mirror its own exit. A
phone pinch-out left the picture away from its origin. A door picture behaved differently by slot
(tlvphotos, 2026-07-15).

## The standing named-part lens (SPEC INV-138)

The three motion groups above run on a gesture spec without waiting for evidence. Any spec can carry a
same-kind group of the same shape that the bottom-up walk misses: the named parts of a guarantee's
domain. A guarantee is a promise one spec sentence makes. Its domain is the set of conditions the
promise is meant to hold under. A named part is one member of that set: a viewport band, a user state
(logged-in against logged-out), a network condition, a locale.

The parts of a domain are a same-kind group. The guarantee owes each part a decided answer: the same
behaviour, or a deliberately different one, stated. So read each such guarantee across its parts. A
guarantee true as written on one part, while the other parts stay silent, is this lens's divergence.
It is the element behaving unlike itself from part to part. It travels the echo channel as a
recommendation or a question. Once the human declares a part-uniform guarantee a class sentence, the
prover's named-part ask holds it [INV-138, INV-150].

The worked example is the viewport bands. Some specs ship a layout-bearing surface: a caption over a
work, a control rail, a counter in a corner. Its bands are exactly such a group — a portrait phone, a
landscape phone that is wide and short, a tablet, a desktop. They are the layout companion of the
motion-parity lens above. A viewport-band guarantee scoped to one band is read across the other bands.
That is how any named-part guarantee is read across the rest of its domain (SPEC INV-138).

The incident behind this worked example: a caption printed over the picture on a landscape phone. Its
spec sentence was scoped to "on a phone", while the styles read phone as a narrow width. The design
review caught it the moment it was pointed at that surface, on 2026-07-16.

## The confidence read

Every design-review finding carries a confidence read of one of two values.

- **`confident`** — you would defend the grouping and the divergence on the spec text alone. Write a
  confident finding as a **recommendation**. A same-kind divergence over an undeclared grouping has no
  stated invariant behind it. So by the prover's own derivation [INV-140] it queues as a queue row for
  a taste call, and it never blocks.
- **`likely`** — the deciding fact lives only in the human's intent: whether the two are truly one
  kind. Write a likely finding as one **question to the human**. Raise it only when the signal clears
  the strong-signal bar under "The echo channel" below.

Below `likely`, say nothing. That is the same drop discipline the prover keeps.

## The echo channel

A likely finding travels the echo channel. The channel is one question put to the human, with both
objects in hand. It fires only when the signal is strong, and all three of these conditions hold:

- the shared role fits **one plain sentence** with no stretch;
- the difference is a **whole behaviour** one member carries and the other lacks. A zoom that exists
  on one photo and is absent on the other clears this bar. A gap that comes down to a parameter, such
  as "2x versus 4x", stays below it. Where the whole-behaviour-versus-parameter call is itself
  unclear, the finding is below the bar;
- **no spec sentence already decides** the difference. A written "a polaroid stays flat, by decision"
  ends the ask before it fires.

The question shows both objects, each with its spec sentence. It asks how alike the two should behave,
and it carries a recommended default. It travels the pack's batched-question path, the road the pack
already uses to bring a judgement to the human [INV-30, E-22, INV-4]. That road ends on one decision
page, filed afterwards in the decision archive. The prover's own per-lens escalations travel it too.

The pack's usual proceed-on-recommended branch would apply that default to the spec on its own
[INV-4]. Here the class sentence lands only on the human's word, so the default waits. The lane never
blocks, so the work does not stall on the open question. **At most three** such questions travel per
pass, **strongest first**. That cap counts questions inside one pass, and it is a different number
from the three-round cap on the loop below. A signal below the bar stays silent, so the channel stays
rare and quiet.

The dated record holds an **unanswered** question until the human answers it, and such an ask is **not raised again** on its own.
A freshly derived ask already carried on a prior record is dropped [INV-130].

This channel carries two producers: the same-kind divergence from the similarity lens, and the
motion-parity divergence from the standing gesture and overlay lens above [INV-165]. A later producer
would earn its own clause. This producer list is curated by incident, the way the facet list in
`spec-author` is. A member joins only with a named real case it would have caught, and it is
re-justified at milestones (SPEC INV-18).

## How the answer closes the loop

The human's answer closes the loop through homes that already exist, so the design review invents no
new enforcement law.

- **"Alike"** becomes a class-level clause written by `spec-author`, naming the class and enumerating
  its members. That is the form the cross-surface uniformity check demands [INV-125]. After that the
  prover's declared-class lenses hold it mechanically on every pass. A host product may also assert it
  when it renders a page. The pack ships the rule and the prover lens, and that page-wide assertion
  stays the host's own to build [INV-125]. Where the class is surface-level, the author adds the rows
  to the surface registry by hand. That keeps E-10's rule that the registry stays the host's
  authorship.
- **"Different, by intent"** becomes a decided spec sentence that closes the question for good
  [INV-59]. The ask never fires again.

So the walk is discovery here, then declaration in `spec-author`, then enforcement by the prover's
lenses. Each stage sits in the skill that already owns it. Where the spec already declares the class,
its uniformity check governs [INV-125]. This pass reaches only the groupings no clause has yet
declared.

**The loop is bounded, and it holds up no landing [INV-154].** A confirmed grouping does not close the
matter in one pass. Only one thing advances the loop: a human-accepted declaration. A declaration is a
change to the spec, so it re-enters the prove step. The prover re-reads the changed part. You re-read
the elements the declaration re-partitions, together with any new element a prover fix introduced. One
prover re-read followed by one design-review re-read is a round. A round that produces a new class
sentence or a new decided sentence is a **progressing round**.

A round's other outputs stay where they are. A confident finding queues as a recommendation for a
taste call. A likely finding rides as a question the human may answer later. Neither re-reads the spec
on its own, so neither advances the loop.

When a round produces no new declaration, the loop rests in one of three ways. Each rest is named on
the record.

- It **converges** when the design review ran and left no open question. It also needs no new grouping
  the human must still rule on. Every grouping it proposes is already declared, already decided, or
  already standing as a queued recommendation from an earlier round. A standing recommendation is a
  settled output and does not bar convergence.
- It **waits** when the round's findings include a question the human has not yet answered. The held
  question resumes the loop when the human later answers it [INV-59].
- It **stands down** when the design review did not run on this kind, because no element a person acts
  on exists. Record the stand-down by name, so nobody reads the rest as a settled design it never
  examined.

You count your own progressing rounds, on the dated record. The count covers the design-review pass
alone, and it resets when a fresh pass opens. The loop may fail to stop on its own. A declaration can
re-partition existing elements into fresh candidate groupings, and a prover fix can add elements. So
the count of undeclared groupings can rise as well as fall.

Convergence is the ordinary case. Converge, wait, and stand down are the three natural rests, reached
when a round produces no new declaration. The cap is a separate, forced halt that keeps the loop live.
It stands apart from the three rests and advances only on a progressing round. It **forces a halt at
three** progressing rounds by default. A host may set its own cap in its profile at
`.live-spec/profile.md`.

On reaching the cap with no convergence, stop iterating. Surface on the dated record the groupings
still unsettled. Give your best reading of the cause, among these three:

- a declaration that spawns new elements or groupings faster than it resolves them;
- an oscillation between two mutually-exclusive groupings;
- a spec whose requirements conflict, so no consistent design exists.

The reading is best-effort, since no check can settle a spec's self-consistency in every case.

Surfacing at the cap holds up no landing. Like every design-review finding it is a recommendation or a
question, and the landing proceeds with the unsettled groupings recorded. Only the human's accepted
declaration triggers the re-prove, as an ordinary spec edit. A design-review finding on its own never
triggers it.

**Cross-sibling propagation routes by declaration status, so the two passes share it cleanly.**

A behaviour that should hold across siblings belongs to exactly one pass at any moment. Which pass is
decided by whether the group is declared.

A declared class is the prover's declared-class defect [INV-125]. So is a kind-general rule already
worded inside one member's own section, which the sharpened cross-surface lens reads as a declaration
in prose. Under such a declaration, a member the class does not cover blocks at the prover. So does a
principle left scoped to one member while siblings of that kind exist.

A genuinely undeclared grouping — one that no clause and no class-general sentence names anywhere — is
this pass's own discovery [INV-141]. It proposes the group, checks parity, and echoes the strongest
likely divergence as a question. A confirmed grouping then lands as a class clause, and the property
crosses to the prover. So the prover owns the propagation where it is declared, and this pass owns it
where it is not. Neither pass claims it twice and neither drops it [INV-150].

## The record

Each run writes a dated record at `docs/design-review/YYYY-MM-DD[-suffix].md`, in the repository under
review. It follows the same shape and discipline as the prover's record, and those records are the
worked examples, under `docs/prover/`. A second scoped run on the same day takes the `-suffix`,
exactly as a prover record does. Two surface-add passes in one day then never overwrite each other.

The record opens by naming the design-reviewer skill version that ran the pass. It carries a
**per-finding outcome** column, whose values are these:

| Value | Meaning |
|---|---|
| `recommended` | a confident finding queued for a taste call |
| `asked` | a likely finding put to the human |
| `answered(alike)` | an ask the human resolved as one kind |
| `answered(different-by-intent)` | an ask the human resolved as a deliberate difference |
| `held` | an ask still unanswered, left alone next pass |

The dated record is the single home for an unanswered ask. Where the decision archive references a
held ask, it points at this record and restates no state [E-22]. Every pass opens by reading the prior
records' `held` asks. That is what lets it tell a still-open ask from a fresh one.

This record is a member of the review-record class the pack's own spec declares once — the shared
shape every review pass writes. The design-review record is the sibling that adds the `held` outcome,
because it alone carries a question across passes (SPEC INV-156). Records written before that class
was declared stay unreshaped, so an older file under `docs/design-review/` may carry a different
shape.

## When to stay silent

- No finding is owed for every element or every group. Most pairs are plainly fine; say nothing about
  them.
- Where the grouping is unclear, or the divergence is unclear, or the whole-behaviour-versus-parameter
  call is unclear, the finding is below the bar. It becomes a silence or, at most, a confident
  recommendation. It never becomes an ask.
- Where a spec sentence already decides the difference, there is no finding at all.
- Where a governing class clause already exists and merely under-enumerates a member, that belongs to
  the prover's declared-class defect path [INV-125]. Route it there, since this pass owns only the
  groupings no clause has declared.
- Never file a defect, never hold a landing. The pass produces recommendations and questions, and no
  blocking defects.

> The pack, whole:
>
> - **live-spec-base** holds the shared rules and the defaults.
> - **spec-author** writes the spec.
> - **product-prover** reviews it as written.
> - **design-reviewer** judges the design behind it.
> - **build-pipeline** ships the change.
> - **test-author** derives the matrix and writes the tests.
> - **communicator** makes the human exchange land.
> - **feedback-intake** brings what comes back to its home.
> - **feedback-collector** offers a rare private note up to the pack's authors.
> - **text-audit** reads a text as a stranger and repairs where they stop.
> - **publish** runs the checks a publication owes its reader.
