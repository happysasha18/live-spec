# text-audit

**An audit-and-fix loop for any human-facing text: run the mechanical lints, then read it as a stranger, and fix where the stranger stops. A [Claude Code](https://claude.com/claude-code) skill.**

Point it at a text a person will read — a README, a spec section, a decision page, marketing copy, an article. It runs the free mechanical checks first, then hands the text to a fresh reader who has no knowledge of its history and marks every place a stranger stops. You fix those places from the source material, and it reads again. The loop ends when two consecutive reads return nothing that blocks a reader.

---

## Why

The author of a text is the worst reader of it. The author already holds the context the text is missing, so the author reads meaning that a stranger cannot: a term that was never defined, a "depends on the upstream state" whose slot is empty, a claim whose ground lives only in the author's head. The text reads fine to the person who wrote it and stops a stranger cold.

The fix is a reader who holds none of that context. This skill supplies the stranger: a fresh session that reads the words on the page and reports where it stopped, classified by whether the stop blocks a reader or only slows one. You fix the blocking ones from the material the text rests on, and a new stranger reads again. Two clean reads in a row is the signal that the stream of stops has thinned to zero.

The loop came out of the spec-format comprehension gate, where a panel of fresh readers found new blocking terms on every pass while the fixed items stayed fixed. This skill packages that gate for any text.

---

## What it does

1. **Mechanical lints first** — vocabulary (every term defined at first use), weak relational words with unfilled slots, requirement shape where the text is a spec (context before criteria, one trigger and one response per criterion, a judge and a measure on every judgment), and style and register. A machine settles the cheap classes so the reader spends attention on the ones no machine knows yet.
2. **A fresh cold reader** — the text goes to a session with zero context on its history, under a stated reader-prompt. It returns the places a stranger stops, each marked blocking or non-blocking. It fixes nothing, and it writes down the guess it made in place of a missing answer.
3. **Fixes from the source** — each blocking finding is fixed from the material the text already rests on: the source spec, the code, the recorded decision. Where the source holds no answer, the finding is a real hole, recorded as a question for the person. Inventing an answer is the one move the skill forbids.
4. **Read again, close on two clean reads** — a new stranger reads the fixed text. The loop ends at two consecutive reads with zero blocking findings.

The skill states the register it holds a text to, and it ships the reader-prompt verbatim, ready to paste.

---

## When it fires

- **A README before a push**, a spec section after an edit, a decision page before it reaches the person, a piece of marketing copy, an article draft — any text whose clarity matters before it ships.
- The trigger is a person asking whether a reader will understand: *"audit this text"* · *"cold-read this"* · *"is this clear"* · *"will a stranger get this"* · *"check this for undefined terms"*.

---

## What it can't do

- **It is not the prover.** [product-prover](https://github.com/happysasha18/product-prover) argues with a spec's claims and finds design holes — a missing state, a false invariant. This skill reads prose for whether a stranger understands it. Run both on a spec; they read different failures on the same page.
- **It does not grade a voice.** It holds a text to a stated register and reports where a reader stops. Taste and voice stay with you.
- **It invents no answers.** A finding with no source answer becomes a question for you, never a gap the skill fills from imagination.

---

## Install

Claude Code required. No code, no dependencies, nothing to build — the skill is a single `SKILL.md`.

```bash
git clone https://github.com/happysasha18/live-spec.git
mkdir -p ~/.claude/skills/text-audit
cp live-spec/skills/text-audit/SKILL.md ~/.claude/skills/text-audit/
```

It also ships inside the [live-spec](https://github.com/happysasha18/live-spec) plugin, if you want the whole pipeline:

```
/plugin marketplace add happysasha18/live-spec
/plugin install live-spec@live-spec
```

Then just ask, in any project:

> *"audit this text"* · *"cold-read this README"* · *"will a stranger understand this section"*

---

## Related

- **[communicator](https://github.com/happysasha18/live-spec/tree/main/skills/communicator)** — the register this skill audits against has its full home in communicator's writing register.
- **[product-prover](https://github.com/happysasha18/product-prover)** — reads a spec for design holes; this skill reads prose for comprehension.
- **[live-spec](https://github.com/happysasha18/live-spec)** — the pack this skill belongs to: wish → spec → prove → tests → code → commit, with the spec as the single authority.

---

## License

[MIT](LICENSE) © Alexander Abramovich.

*Read-only mirror of one skill from the [live-spec pack](https://github.com/happysasha18/live-spec) — don't open PRs here; changes land in the pack and sync via `scripts/sync-mirrors.sh`.*
