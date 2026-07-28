# text-audit

**An audit-and-fix loop for any human-facing text. It runs the mechanical lints, reads the text as a stranger, and repairs the places where the stranger stops. A [Claude Code](https://claude.com/claude-code) skill.**

Point it at a text a person will read: a README, a spec section, a decision page, marketing copy, an article. It runs the free mechanical lints first. Then it hands the text to a fresh reader who knows nothing of its history, and that reader marks every place a stranger stops. You repair those places from the source material, and a new reader reads again. The loop ends when two consecutive reads return nothing that blocks a reader.

---

## Why

The author of a text is the worst reader of it. The author already holds the context the text is missing, so the author reads a meaning a stranger cannot reach. Three examples show the shape:

- a term that was never defined;
- a phrase such as "depends on the upstream state", whose slot stands empty;
- a claim whose ground lives in the author's head.

The text reads fine to the person who wrote it, and it stops a stranger cold.

The repair is a reader who holds none of that context. This skill supplies the stranger. A fresh session reads the words on the page and reports where it stopped. Each stop is marked by whether it blocks a reader or only slows one. You repair the blocking stops from the material the text rests on, and a new stranger reads again. Two clean reads in a row show that the stream of stops has reached zero.

The loop came from the spec-format comprehension gate. A panel of fresh readers there found new blocking terms on every pass, and the terms already repaired stayed repaired. This skill packages that gate for any text.

---

## What it does

1. **The mechanical lints first.** Five lints run before any reader:

   - a term defined at first use;
   - a weak relational word with an unfilled slot;
   - requirement shape, where the text is a spec;
   - style and register;
   - one name per thing.

   A machine settles those cheap classes, so the reader spends attention on the ones no machine knows yet.
2. **A fresh cold reader.** The text goes to a session with zero context on its history, under a stated reader-prompt. That session returns the places a stranger stops, each one marked blocking or non-blocking. It fixes nothing, and it writes down the guess it made in place of a missing answer.
3. **Fixes from the source.** Each blocking finding is repaired from the material the text already rests on: the source spec, the code, the recorded decision. Where the source holds no answer, the finding is a real hole, and it is recorded as a question for the person. Inventing an answer is the one move the skill forbids.
4. **Read again, and close on two clean reads.** A new stranger reads the repaired text. The loop ends at two consecutive reads with zero blocking findings.

The skill states the register it holds a text to, and it ships the reader-prompt verbatim, ready to paste.

---

## When it fires

Any text whose clarity matters before it ships:

- a README before a push;
- a spec section after an edit;
- a decision page before it reaches the person;
- a piece of marketing copy or an article draft.

The trigger is a person asking whether a reader will understand the text. They ask it in words like these: *"audit this text"* · *"cold-read this"* · *"is this clear"* · *"will a stranger get this"*.

---

## What it can't do

- **Design review belongs to [product-prover](https://github.com/happysasha18/product-prover).** That skill argues with a spec's claims and finds design holes. A missing state and a false invariant are its findings. This skill reads prose for whether a stranger understands it. Run both on a spec; they read different failures on the same page.
- **Taste and voice stay with you.** This skill holds a text to a stated register and reports where a reader stops.
- **A finding with no source answer becomes a question for you.** The skill fills no gap from imagination.

---

## Install

Claude Code required. The skill is a single `SKILL.md` file, and installing it is a copy.

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

- **[communicator](https://github.com/happysasha18/live-spec/tree/main/skills/communicator)** — carries the work to the person and asks for decisions. The writing rules both skills hold a text to live in one file inside the pack, and this skill prints them out of that file.
- **[product-prover](https://github.com/happysasha18/product-prover)** — reads a spec for design holes; this skill reads prose for comprehension.
- **[live-spec](https://github.com/happysasha18/live-spec)** — the pack this skill belongs to. Its pipeline runs wish → spec → prove → tests → code → commit, and the spec is the single authority.

---

## License

[MIT](LICENSE) © Alexander Abramovich.

*Read-only mirror of one skill from the [live-spec pack](https://github.com/happysasha18/live-spec). Changes land in the pack and reach this mirror through `scripts/sync-mirrors.sh`, so open pull requests against the pack.*
