# design-reviewer

**A senior design review of a product spec the prover has already checked. A [Claude Code](https://claude.com/claude-code) skill.**

Point it at a spec that already holds together as written. It reads the design the way a principal engineer would when the words are all correct but the shape might still be wrong: it builds its own inventory of what a person acts on, proposes the same-kind groupings the text never named, and asks whether the members of each group really behave alike.

This is the [prover's](https://github.com/happysasha18/product-prover) younger sibling. It runs after the prover, on the same spec. Where the prover asks whether the spec holds together as written, the design review asks whether the design itself is right — do same-kind things behave the same way, and what groupings did the text never declare?

---

## Why

The prover catches holes in what the text says: a missing state, a false claim, a transition with no exit. It works by arguing with sentences, so it needs a sentence to argue with.

Two elements that a person acts on the same way, which no clause ever grouped, are invisible to any amount of proving the text. There is no sentence that puts them side by side, so there is nothing to contradict. A photo opens full-screen; a cover image is described three sections away; nothing in the document ever says the two are the same kind of thing, so nothing notices that one gained a behaviour the other never did.

The design review closes that gap. It builds its own inventory of what a person acts on, proposes the same-kind groups no clause declared, and checks whether the members actually behave alike. The catch it exists for lives in the space between the sentences, where proving the sentences can never reach.

---

## What a finding looks like

A finding names two concrete objects, each with the spec sentence it comes from, the one role they share, and the single question it raises about how alike the two should behave. Illustrative:

> **A visitor can open a portrait full-screen, and may expect the same of a cover photo**
>
> *Spec §2.1:* "Tapping a portrait opens it full-screen, where the visitor can zoom and pan." *Spec §5.3:* "Each album carries a cover photo at the top of its page."
>
> **The shared role:** in both places a visitor is looking closely at a single image on the page.
>
> **The question:** should tapping the cover photo open it full-screen the way tapping a portrait does, or does the cover stay fixed by intent? The spec answers this for the portrait and leaves it open for the cover.
>
> **Recommended default:** treat the cover as the same kind as a portrait — one full-screen behaviour for every image a visitor looks at closely — unless you decide the cover is meant to stay flat.

Every finding is a recommendation or a question. It never blocks a landing. A finding you can defend on the spec text alone arrives as a recommendation, written into the review record and ending there — it becomes work only when you write it onto the plan in your own words; a finding whose answer lives only in your own intent arrives as a single question, carried with both objects in hand and a default already proposed, so answering it comes down to a single decision.

---

## When it fires

It runs after the prover, on the spec the prover has just checked, upstream of architecture and tests, so a confirmed grouping can land as a clause before any test is derived from it.

- **After a full prover pass** — the full design review: the whole inventory of what a person acts on, every proposed grouping.
- **When a new surface is added** — a scoped review: the new surface's elements read against the inventory that already exists, so a divergence introduced by the addition is caught the moment it arrives.

It stands down at feature intake and at the push gate. Intake is checking whether a feature fits; the push gate is a last read of the whole document before shipping. Neither is the moment for a concept critique, so the design review stays quiet at both.

---

## The loop

When you accept one of the groupings it proposes, the prover re-reads that change and the design review reads anything new the change introduced; the two settle together. The loop is bounded: after a few rounds that still do not settle, it stops, tells you which groupings are still open and its best reading of why, and it never holds up your release.

---

## Install

Claude Code required. No code, no dependencies, nothing to build — the skill is a single `SKILL.md`.

```bash
git clone https://github.com/happysasha18/design-reviewer.git
mkdir -p ~/.claude/skills/design-reviewer
cp design-reviewer/SKILL.md ~/.claude/skills/design-reviewer/
```

It also ships inside the [live-spec](https://github.com/happysasha18/live-spec) plugin, if you want the whole pipeline:

```
/plugin marketplace add happysasha18/live-spec
/plugin install live-spec@live-spec
```

Then just ask, in any project:

> *"review the design of this spec"* · *"do these behave the same?"* · *"what siblings did we miss?"* · *"design review this"*

---

## What it can't do

It never blocks a landing. Every finding is a recommendation or a question, and the decision stays with you: it hands you a divergence with both objects in hand and a default already proposed, and you say whether the two are one kind or different by intent.

It reads a spec that already holds together as written. Judging whether the words themselves are complete and consistent — a missing state, a false claim, an unhandled transition — is the prover's job, and the prover runs first. The design review reads the design behind a spec the prover has already checked, so it has nothing to say about a spec that does not yet hold together on the page.

---

## Related

- **[product-prover](https://github.com/happysasha18/product-prover)** — the older sibling. It checks that the spec holds together as written; the design review reads the design behind it once it does.
- **[live-spec](https://github.com/happysasha18/live-spec)** — the pack both passes belong to: wish → spec → prove → tests → code → commit, with the spec as the single authority.
- **[spec-author](https://github.com/happysasha18/live-spec/tree/main/skills/spec-author)** — the writing hand. When you confirm a grouping, spec-author turns it into a class clause the prover can then hold mechanically.

---

## License

[MIT](LICENSE) © Alexander Abramovich.

*Read-only mirror of one skill from the [live-spec pack](https://github.com/happysasha18/live-spec) — don't open PRs here; changes land in the pack and sync via `scripts/sync-mirrors.sh`.*
