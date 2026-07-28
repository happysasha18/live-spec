# live-spec

**Ten [Claude Code](https://claude.com/claude-code) skills that turn a wish spoken in passing into a specified, reviewed, tested, committed change — with scripts that block the push when the documents and the code disagree.**

---

You tell your agent *"the report page needs a date filter"* and four minutes later it is written, tested, and green. The tests pass because they came from the same spec. The spec never said what happens when the date is invalid, so the agent picked some behaviour and shipped it. Nobody chose that behaviour and nobody reviewed it, and the green suite never looked at it.

That is the gap. The spec became the thing your agent builds from, and nothing checks the spec itself.

live-spec closes it. You say the sentence in passing, with nothing to file and no form. It gets classified, written into a living spec, reviewed by a formal-verification pass, covered by tests derived from that spec, coded until green, and committed with its documents in one change. A script on the pre-push hook compares the spec to the code that shipped and refuses the push when the two disagree. There is no CLI. You talk to it.

---

## Install

```
/plugin marketplace add happysasha18/live-spec
/plugin install live-spec@live-spec
```

Or clone and run `./install.sh`, which copies the skills into `~/.claude/skills/`. Then attach it to a project. Use [`templates/`](templates/) for a new project. Use [`docs/adoption.md`](docs/adoption.md) for an existing codebase, where the pack writes the first spec from what actually ships. After that everything runs in plain words: *"attach live-spec to this project"*, any wish, *"status"*, *"publish"*.

---

## What the spec looks like

A project under the pack keeps one document, `PRODUCT_SPEC.md`, stating what the product promises today. A stranger can read a section on the first pass. The format is a requirements genre, defined in [`docs/spec-format.md`](docs/spec-format.md):

- The document opens with a **glossary**. Every domain noun used anywhere in the spec has a one-sentence definition. An ordinary English word needs no entry.
- The body is a list of **requirements**. Each requirement has a short **context** (when the situation arises, who is involved, what the reader sees), one **user story** (as a person in a named role, I want one thing, so that one benefit follows), and **acceptance criteria**.
- The criteria are grouped into **named cases**. A case names a situation and lists two to six numbered steps. Each step carries one trigger and one response, written with the plain keywords *when*, *while*, *if*, *then*, and *shall*.
- A short code anchor trails at the end of a line and points to the rule's home in the spec. A reader can ignore the anchors. A maintainer follows them.

The test matrix follows the same format, defined in [`docs/test-matrix-format.md`](docs/test-matrix-format.md): each row is one criterion stating what a fact does and what it must never do, grouped by architecture node, and the coverage table at the document's end is generated from the rows and gated against hand edits. The roadmap and the architecture document follow it too, the architecture defined in [`docs/architecture-format.md`](docs/architecture-format.md): each part of the system stands as one node section naming its responsibility, the spec facts it owns, and where it lives in the code. One shared parser reads every node section, and every check reads a node through it.

Work enters the spec before code. A new behaviour arrives as a spec change, gets reviewed, and only then gets built. A guardrail check goes red when a shipped behaviour has no spec sentence behind it. A removed feature leaves a dated tombstone, and its history moves to `JOURNAL.md`.

---

## What's different

**The gates are scripts.** Two checks decide whether a push is allowed: every fact in the spec has an owning test, and the documents match what shipped. Both are Python on the pre-push hook, mirrored in [CI](.github/workflows/gates.yml). A change that has drifted from its specification is refused. Some other frameworks enforce their specs by asking a model to check. A model having a bad day reports that it checked.

**It can decline a gate it cannot build honestly, and records the reasoning.** A planned gate would have failed a session that worked one step at a time. The [prover's record](docs/prover/) for that landing declined it, with three reasons: independence is a judgment, and a script sees only a diff; the evidence a correct run would leave is destroyed by design; and the one mechanical signal available would fire on every lawful sequential run. It shipped as a written discipline. The rule behind this decision is that a requirement no script can enforce stays a note, and a judgment call is never wired as an automated gate. There are more than three hundred such records in [`docs/prover/`](docs/prover/), including the ones where the reviewer missed something and said so.

**The rules are built for a model's failure modes.** Every claim shown for review is tagged with its source: read from the artifact, your own recorded word, or the agent's inference, with inferences flagged most visibly. The line between what a document says and what a model filled in is invisible to a reader, and that is where the errors live. A background worker from a dead session is treated as a concurrent writer until three signals agree it stopped. A decision you withdraw twice keeps its recommendation and is never raised again, because a tireless agent will go on asking on its own.

---

## Three thousand lines of rules, and that is the point

The rules are the part a software house would charge you for: thirty-five shared rules across the skill set, stated once. They cover how a spec gets written so it stays readable, when a question is worth your attention and when it is routine, and what a green suite does and does not prove. You do not read them. They run.

The relationship is the one you have with a builder. You do not need to know how; you still decide what. A good contractor does not ask the client to choose the rebar, and does not pick the kitchen either.

The pack is opinionated. The opinions belong to one engineer, and they are not neutral industry practice. Adopting the pack adopts them.

---

## Staying in control

You keep control, in a strong sense. Access to the diff was never the problem. Knowing where to look is.

- **Nothing is decided silently.** Every default is printed in the delivery report, in the product's own words, marked as tweakable: *"on a phone this gallery stacks into one column."*
- **Routine choices are made and reported; the lane keeps moving.** Only what the documents genuinely leave open reaches you as a question.
- **Undo is one commit.** The change lands with its spec, matrix, and architecture together.
- **It cannot run away.** The gates go red and stop the push.

Many tools offer control by asking a long list of questions up front. That is more work for you.

---

## What it missed

Three projects run under this pack in production, the pack's own repository among them, and they keep catching the method out. A dead-end check ran on the right surface and still missed a one-way door, because it read states within a single surface while nothing walked the round trip between two surfaces. That was the method's own fault, and it became a new rule. A test guarded that near-silent audio stems are dropped from a view, and it stayed green for a month while the spec's actual requirement, that those stems stay visible and named, went unrendered. And a scroll that satisfies its motion contract exactly can still feel cheap, which no rubric will catch honestly.

> **A spec owns what a project can write down and test. Feel belongs to the owner's eye.**

The full accounts, including the reviews that missed something and said so, live in the prover records: [`docs/prover/`](docs/prover/).

---

## The skills

`live-spec-base` holds the shared rulebook · `build-pipeline` sequences a change end to end · `spec-author` writes the living spec · [`product-prover`](https://github.com/happysasha18/product-prover) reviews it · `design-reviewer` asks whether the design itself is right once the spec holds together · `test-author` derives the matrix and the tests · `communicator` shows work and asks answerable questions · `feedback-intake` routes what you hand back · `feedback-collector` sends upstream notes with your consent · `text-audit` reads a text as a stranger and fixes where they stop · `publish` gates anything leaving the machine.

Map of everything: [`OVERVIEW.md`](OVERVIEW.md) · [pipeline](docs/pipeline.md) · [adoption](docs/adoption.md)

---

## Who it's for, and the limits

This pack is for people who can already build software, know what discipline costs, and now build with agents that are fast and untrustworthy. It is the wrong tool for a first project. It hands you a spec, an architecture document, a test matrix, and a pre-push hook. That is the right shape for the problem and too much for someone who has never shipped.

Three projects, one author, no outside adopters yet. The judgment loop is one model reviewing its own work. Only the mechanical gates are genuinely independent, which is why they are scripts. The version moves fast and the rules will sharpen under you. The gates stabilize first, because those carry red-first proofs.

Prior art is credited in full, including what was borrowed and from whom: [survey](docs/prior-art-frameworks.md) · [originality audit](docs/research/2026-07-10-originality-audit.md) · [comparative reviews](docs/research/2026-07-06-bmad-kiro-livespec-comparison.md), briefed to criticize all three subjects. This pack sits alongside BMAD, Kiro, and the wider spec-driven-development family. What it adds is the mechanical push gate and the recorded prover discipline. [Superpowers](https://github.com/obra/superpowers) is ahead of anything here on execution discipline, and its stars are earned. If you know prior art we missed, open an issue.

**Known issues.** Internal vocabulary still leaks into human-facing text. A register lint blocks the known leaks in shown artifacts, and chat stays the weakest surface. The spec still carries counted style debt, dated in the queue. The settings card is young and has run on one project. All three are tracked and reviewed at every push.

---

[MIT](LICENSE) © Alexander Abramovich, 2026 · [`VERSION`](VERSION) · [what lives where](OVERVIEW.md)
