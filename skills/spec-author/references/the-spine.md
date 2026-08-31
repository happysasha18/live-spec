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

Mark anything that needs a human's domain call with **⟨DECIDE⟩** and a one-line question. Base rule 1
carries the law behind that marker, and this line names where a spec applies it.

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

