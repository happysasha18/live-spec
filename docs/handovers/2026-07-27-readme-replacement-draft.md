# live-spec

**Ten [Claude Code](https://claude.com/claude-code) skills over one shared rulebook, turning a wish spoken in passing into a specified, reviewed, tested, committed change — with scripts that block the push when the documents and the code disagree.**

---

On 17 July 2026 three landings under this pack were reported finished, with the suite green. Reviews the same day went at all three and pulled all three apart: six defects in the first, two of them defeating that landing's own claim, four in the second, and the third's own record claimed a clean sweep that was not clean. The tests had passed because a background race destroyed every verdict the judge wrote, and because a missing installed hook counted as a green skip. Everything was fixed before the release went out the next day.

Those reviews also ran in the same session that had done the work, which the pack then recorded as a defect of its own: the authoring seat is blind to its own new blind spot. From 18 July the rules require a release review from a seat that has seen none of the work. No script can see whether a context was truly clean, so that one is a discipline, and the gate under it checks only that the record exists, is dated to the release, and names a different seat.

That is the shape of the problem. The same model writes the code, the tests that judge it, and often the spec all three came from, so a green suite proves they agree with each other and nothing more. You tell your agent *"the report page needs a date filter"* and four minutes later it is written, tested, and green — and the spec never said what happens when the date is invalid, so it picked a behaviour and shipped it. Nobody chose that behaviour, nobody reviewed it, and the green suite never looked at it.

live-spec closes the loop from outside. You say the sentence in passing, with nothing to file and no form. It gets classified, written into a living spec, reviewed by a formal-verification pass, covered by tests derived from that spec, coded until green, and committed with its documents in one change. Scripts on the pre-push hook refuse a push when the documents and the code have drifted apart. There is no CLI. You talk to it.

---

## Install

```
/plugin marketplace add happysasha18/live-spec
/plugin install live-spec@live-spec
```

Or clone and run `./install.sh`, which copies the skills into `~/.claude/skills/`. Then attach it to a project. Use [`templates/`](templates/) for a new project. Use [`docs/adoption.md`](docs/adoption.md) for an existing codebase, where the pack writes the first spec from what actually ships. After that everything runs in plain words: *"attach live-spec to this project"*, any wish, *"status"*, *"publish"*.

What a host project needs for the push-time scripts: python3, the project in git with a resolvable `origin/main` or a base branch named in the config, a filled `guardrails.config.json`, and the four check lines added to your own pre-push hook by hand — the installer prints them and leaves your hooks alone. [`scaffold/guardrails/README.md`](scaffold/guardrails/README.md) walks it. Everything before the push works without any of that.

---

## What the spec looks like

A project under the pack keeps one document, `PRODUCT_SPEC.md`, stating what the product promises today. A stranger can read a section on the first pass. The format is a requirements genre, defined in [`docs/spec-format.md`](docs/spec-format.md):

- The document opens with a **glossary**. Every domain noun used anywhere in the spec has a one-sentence definition. An ordinary English word needs no entry.
- The body is a list of **requirements**. Each requirement has a short **context** (when the situation arises, who is involved, what the reader sees), one **user story** (as a person in a named role, I want one thing, so that one benefit follows), and **acceptance criteria**.
- The criteria are grouped into **named cases**. A case names a situation and lists two to six numbered steps. Each step carries one trigger and one response, written with the plain keywords *when*, *while*, *if*, *then*, and *shall*.
- A short code anchor trails at the end of a line and points to the rule's home in the spec. A reader can ignore the anchors. A maintainer follows them.

The test matrix follows the same format, defined in [`docs/test-matrix-format.md`](docs/test-matrix-format.md): each row is one criterion stating what a fact does and what it must never do, grouped by architecture node, and the coverage table at the document's end is generated from the rows and gated against hand edits. The roadmap and the architecture document follow it too, the architecture defined in [`docs/architecture-format.md`](docs/architecture-format.md): each part of the system stands as one node section naming its responsibility, the spec facts it owns, and where it lives in the code. One shared parser reads every node section, and every check reads a node through it.

Work enters the spec before code. A new behaviour arrives as a spec change, gets reviewed, and only then gets built. A removed feature leaves a dated tombstone, and its history moves to `JOURNAL.md`.

---

## What's different

**The gates are scripts, and here is exactly what they read.** Four of them come with the pack and sit in your own project:

- **Every surface your project registers really appears in what shipped, and is not empty.** This one reads rendered output and compares it against the registry.
- **Every registered surface cites a spec anchor that exists in the document.** A surface with nothing behind it, or citing an anchor nobody wrote, refuses the push.
- **A change to a user-facing file arrives with a change under the tests directory.** This one reads the list of changed file names, plus the contents of any file whose whole diff is a version bump, which it exempts. It proves a test was touched, and its own source says it judges nothing about whether that test is good.
- **The documents do not contradict each other:** no anchor indexed twice, no invariant missing its matrix row, no surface named twice, no decision marked open and resolved at once.

**What they cannot see.** A changed calculation. A new sort order. A different behaviour at an edge. A new field in an API. Two of the four compare documents to documents, one compares your registry to shipped output, and one reads a list of file names and little else, so a semantic defect walks past all four. That boundary is stated in [`scaffold/guardrails/README.md`](scaffold/guardrails/README.md) in the same words: guardrails catch structural defects; whether a number is right stays with the prover and with you.

This repository runs a longer chain of its own gates on the same hook, twenty-six of them, and one script checks that each carries a recorded case of it going red. Twenty-five carry their own; the twenty-sixth is declared as riding another gate's suite, and the checker accepts that as a class. It refuses one thing outright: a gate declared unable to fail. In its own words, a gate that by construction can never fail guards nothing, and that is a finding rather than a pass. A second hook runs before every commit, where a parked decision has to name the fact only you can supply, and a file staged while its working copy has moved on reds as a second writer. The [CI mirror](.github/workflows/gates.yml) is this repository's own, and the kit ships no workflow to an adopter.

**Some other frameworks enforce their specs by asking a model to check.** A model having a bad day reports that it checked.

**It can decline a gate it cannot build honestly, and records the reasoning.** A gate for parallel lanes was planned and then refused. The [record](docs/prover/2026-07-18-rows386-412-414-lane-open-act.md) gives three reasons: independence is a judgment, and a script sees only a diff; the evidence a correct run would leave is destroyed by design; and the one mechanical signal available fires on every lawful serial run. What shipped instead was a written reminder plus a mechanical cap that is built and proven by deed. The rule behind the decision runs a three-way test on every habit: is it forgotten, is it mechanically checkable, is it a taste call. Yes, yes, no earns a machine. Anything else stays a reminder, and a judgment call is never wired as an automated gate. There are more than three hundred such records in [`docs/prover/`](docs/prover/), including the ones where the reviewer missed something and said so.

**The rules are built for a model's failure modes.** Every claim shown for review is tagged with its source: read from the artifact, your own recorded word, or the agent's inference, with inferences flagged most visibly. The line between what a document says and what a model filled in is invisible to a reader, and that is where the errors live. A background worker from a dead session is treated as a concurrent writer until three signals agree it stopped. A decision you withdraw twice keeps its recommendation and is never raised again, because a tireless agent will go on asking on its own.

---

## Three thousand lines of rules, and that is the point

The rules are the part a software house would charge you for: thirty-four shared rules across the skill set, stated once. They cover how a spec gets written so it stays readable, when a question is worth your attention and when it is routine, and what a green suite does and does not prove. You do not read them. They run.

Most of them are held by a model following written text, which is the part you are right to distrust. So a rule that breaks twice earns a machine that same moment: an every-turn reminder at the decision point, or an after-the-fact check that turns the suite red. Workshop trouble runs its own three-rung ladder in the problem ledger — one line the first time, an owner the second, and a third recurrence with nobody owning it recorded as a defect of the method itself, with the owner's dated sentence that a thing is not worth fixing available at the second rung. It works: the agent kept stamping entries with times it had never read, hand-sweeping failed twice, and that rule now lives in a script that blocks the commit when a stamp is ahead of the clock.

The relationship is the one you have with a builder. You do not need to know how; you still decide what. A good contractor does not ask the client to choose the rebar, and does not pick the kitchen either.

The pack is opinionated. The opinions belong to one engineer, and they are not neutral industry practice. Adopting the pack adopts them.

---

## Staying in control

You keep control, in a strong sense. Access to the diff was never the problem. Knowing where to look is.

- **Nothing is decided silently.** Every default is printed in the delivery report, in the product's own words, marked as tweakable: *"on a phone this gallery stacks into one column."*
- **Routine choices are made and reported; the lane keeps moving.** Only what the documents genuinely leave open reaches you as a question.
- **Anything you can say in words is yours to set** — product behaviour, architecture, technology, the shape of a screen — at any level, as deeply as you want. What you say becomes a spec sentence and is held from then on. What you leave unsaid is decided for you and printed in the defaults list.
- **A decision recorded as yours has to cite the exchange where you said it.** A script refuses the record when nothing citable stands behind it.
- **Undo is one commit.** The change lands with its spec, matrix, and architecture together.
- **It cannot run away.** The gates go red and stop the push.

Many tools offer control by asking a long list of questions up front. That is more work for you.

---

## What it missed

Two projects run under this pack in production, and both caught the method out. The pack's own repository caught it first.

On 10 July 2026 an invited outsider was asked to prove this repository's own push gates physically block a broken state. They planted three breaks and pushed each to a throwaway remote. Two were physically blocked at the push. The third was a fake surface in a rendered artifact: the completeness gate stayed green and the broken state landed, because this repository had left one line of its own settings file blank — the line that tells the check how to recognise a surface in shipped output. The passing message still asserted that nothing unregistered was there, a claim the check had never verified. The [write-up](docs/prover/2026-07-10-external-push-probe.md) is dated, with its root cause.

A dead-end check ran on the right surface and still missed a one-way door, because it read states within a single surface while nothing walked the round trip between two surfaces. That was the method's own fault, and it became a new rule. A test guarded that near-silent audio stems are dropped from a view, and it stayed green for a month while the spec's actual requirement, that those stems stay visible and named, went unrendered. And a scroll that satisfies its motion contract exactly can still feel cheap, which no rubric will catch honestly.

> **A spec owns what a project can write down and test. Feel belongs to the owner's eye.**

The full accounts, including the reviews that missed something and said so, live in the prover records: [`docs/prover/`](docs/prover/).

---

## The skills

`live-spec-base` holds the shared rulebook · `build-pipeline` sequences a change end to end · `spec-author` writes the living spec · [`product-prover`](https://github.com/happysasha18/product-prover) reviews it · `design-reviewer` asks whether the design itself is right once the spec holds together · `test-author` derives the matrix and the tests · `communicator` shows work and asks answerable questions · `feedback-intake` routes what you hand back · `feedback-collector` drafts an upstream note into a folder for you to send, off unless a host turns it on · `text-audit` reads a text as a stranger and fixes where they stop · `publish` gates anything leaving the machine.

Map of everything: [`OVERVIEW.md`](OVERVIEW.md) · [pipeline](docs/pipeline.md) · [adoption](docs/adoption.md)

---

## Who it's for, and the limits

This pack is for people who can already build software, know what discipline costs, and now build with agents that are fast and untrustworthy. It is the wrong tool for a first project. It hands you a spec, an architecture document, a test matrix, and a pre-push hook. That is the right shape for the problem and too much for someone who has never shipped.

Two projects, one author, no outside adopters yet. Every story on this page comes out of that same set, checked by the method itself, which makes it a record of the method catching itself and no sample of what it does in other hands. The judgment loop is one model reviewing its own work. Only the mechanical gates are genuinely independent, which is why they are scripts. What a week of this costs in time and tokens has never been measured. The version moves fast and the rules will sharpen under you. The gates stabilize first, because those carry red-first proofs.

Prior art is credited in full, including what was borrowed and from whom: [survey](docs/prior-art-frameworks.md) · [originality audit](docs/research/2026-07-10-originality-audit.md) · [comparative reviews](docs/research/2026-07-06-bmad-kiro-livespec-comparison.md), briefed to criticize all three subjects. This pack sits alongside BMAD, Kiro, and the wider spec-driven-development family. What it adds is the mechanical push gate and the recorded prover discipline. [Superpowers](https://github.com/obra/superpowers) is ahead of anything here on execution discipline, and its stars are earned. If you know prior art we missed, open an issue.

**Known issues.** Internal vocabulary still leaks into human-facing text. A register lint blocks the known leaks in shown artifacts, and chat stays the weakest surface. The spec still carries counted style debt, dated in the queue. The settings card is young and has run on one project. All three are tracked and reviewed at every push.

---

[MIT](LICENSE) © Alexander Abramovich, 2026 · [`VERSION`](VERSION) · [what lives where](OVERVIEW.md)
