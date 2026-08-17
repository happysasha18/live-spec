# spec-author

**Author and grow a living product spec as your project develops — structured, honest, and ready for review. A [Claude Code](https://claude.com/claude-code) skill.**

Point it at a feature you're about to build, and it writes (or grows) a requirements-genre `PRODUCT_SPEC.md` that states what the product *is* and how its parts compose: entities, states, transitions, actors, invariants, and — the part most specs miss — the **cross-section composition** between surfaces and the views/modes they live under.

It's the authoring half of a pair. **spec-author writes the spec; its sibling [product-prover](https://github.com/happysasha18/product-prover) reviews it.** Same formal-verification primitives on both sides, so the handoff is clean: author → prove → derive tests → code.

---

## The rule it won't break

> If a situation the system can reach isn't in the spec, the spec is incomplete — even if the code "works."

A spec exists so the next reader (the prover, a teammate, you in three months) can reason about every reachable situation. So spec-author won't silently fill a gap with a guess — it asks the leading question or marks it **⟨DECIDE⟩**. It never invents intent.

Same instinct as **[product-prover](https://github.com/happysasha18/product-prover)** and **[track-coach](https://github.com/happysasha18/track-coach)**: facts over plausible fiction, and the decision always stays with the author.

---

## The move most specs miss

When a surface carries **state** (a player, a form, an editor), the system usually also has **global axes** it renders under — a compact/detailed view, a quick/full mode, a tier, a screen size, what a reload restores (saved state meeting newer code), and concurrent use where it applies. The bugs that pass every unit test live in the **product** of surface-state × axis, because each was specified alone.

> Real example: a multi-stem audio player was specced as play / mute / solo / seek — clean. But nobody specced what the *compact view* does to it. Solo a part, switch to compact (which hides the controls), and you're left hearing one isolated part with nothing on screen to undo it. Each axis was fine; their product wasn't.

So for every stateful surface, spec-author enumerates it against **each** axis — is the state still visible? still reversible? does the transition preserve, reset, or block it? — and names the composition invariant. And it insists on **one surface, one name**, because a reviewer can only catch a cross-section hole when both sides are named identically and present in the same document.

When a surface persists state beyond the session (localStorage, files, preferences), spec-author enumerates the old-stored-value × current-code cross-section explicitly and demands a stated migrate / ignore / clear rule — the "reopened it and it looked broken" seam.

---

## What it does

- **Human-first, in product language** — the spec reads in plain product words a person *wants* to keep open, in whatever register fits, whether or not it reads like a textbook. Machine fragments with markup have no place in it. It opens with a closed-vocabulary glossary, then a body of requirements — each a Context block, a one-sentence User Story, and acceptance criteria grouped into named cases — with the prover's codes (`INV-18`, `⟨DECIDE⟩`) trailing as quiet handles at the line-ends. One document serves both the human and the prover — no forked "readable" copy that drifts. Edit history lives in the JOURNAL; the spec states today's truth.
- **The spine** — a completeness checklist every spec must satisfy: Purpose, Entities, States & transitions, Actors, Invariants (safety + liveness), Cross-section composition, and a closed-vocabulary Glossary.
- **Composition pass** — the step above: every stateful surface, multiplied across every view/mode/tier it lives under, with the composition invariant stated.
- **Completeness pass** — a short checklist run before a section is "done": every noun named once, every state has an exit, every transition has an actor, every claim is honest (or ⟨DECIDE⟩), and no second document claims to be the spec.
- **Honest gaps** — domain calls only a human can make are marked ⟨DECIDE⟩ with the question, never guessed.
- **Prover-ready handoff** — written in the same primitives [product-prover](https://github.com/happysasha18/product-prover) reviews, so you author → prove the *whole* spec → derive the test matrix → write code.

---

## What's inside

No code, no dependencies, nothing to build — spec-author is a `SKILL.md` and the `references/` pages beside it: a structured set of authoring instructions Claude follows, with the set pieces (the glossary, the reading form, the spine, the facet sweep and the rest) held one file each and loaded when the body sends the reader there. Drop it in and ask. Works anywhere Claude Code runs.

---

## Usage

Drop the folder into `~/.claude/skills/spec-author/` and just ask:

> *"start a spec for this"* · *"spec out this feature"* · *"add X to the spec"* · *"keep the spec in sync with what we just built"* · *"how should I structure this spec?"*

Then hand the result to **product-prover** for review before you write tests or code.

---

## License

[MIT](LICENSE) © Alexander Abramovich.
