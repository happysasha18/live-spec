# live-spec

**Ten working [Claude Code](https://claude.com/claude-code) skills, plus the one shared rulebook they all load. They turn a wish spoken in passing into a specified, reviewed, tested, committed change. Scripts block the push when the documents and the code disagree.**

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

Those two lines go into Claude Code. Or clone this repository and run `./install.sh`, which copies the skills into `~/.claude/skills/`.

Then say *"attach live-spec to this project"* in the project you want it in, or *"found a new project on live-spec"* in an empty directory. The pack reads the tree and runs the setup walk it calls for: [`adopt/START.md`](adopt/START.md) for a fresh project, [`adopt/ADOPT.md`](adopt/ADOPT.md) for an existing codebase. On that second path the pack writes the first spec from what ships today. [`docs/adoption.md`](docs/adoption.md) describes the same run in plainer words.

The push gate is a third step, and it reads the documents attaching just wrote. The setup walk runs it for you. To run it by hand from your project's root, use the pack tree you already have. The plugin install puts the whole tree under `~/.claude/plugins/cache/`. The clone below is for the `install.sh` path, which carries skill files alone:

```
git clone https://github.com/happysasha18/live-spec.git
bash live-spec/adopt/install-scaffold.sh
```

That copies the four checks into your project's `guardrails/` and seeds `guardrails.config.json`. Fill in that config: your paths to the spec, the test matrix, the queue, the tests, and the surface registry. Empty its `waivers` block, which arrives holding one example waiver that switches the completeness check off.

Then add the four check lines to `.git/hooks/pre-push`, listed in [`scaffold/guardrails/README.md`](scaffold/guardrails/README.md). Create that hook file if your project has none, and make it executable. A push runs the checks once that hook calls them.

The checks need Python 3.9 or newer, and a project that is already a git repository.

After that everything runs in plain words: *"attach live-spec to this project"*, any wish, *"status"*, *"publish"*.

---

## What the spec looks like

A project under the pack keeps one document, `PRODUCT_SPEC.md`, stating what the product promises today. A stranger can read a section on the first pass. The format is a requirements genre, defined in [`docs/spec-format.md`](docs/spec-format.md):

- The document opens with a **glossary**. Every domain noun used anywhere in the spec has a one-sentence definition. An ordinary English word needs no entry.
- The body is a list of **requirements**. Each requirement has a short **context** (when the situation arises, who is involved, what the reader sees), one **user story** (as a person in a named role, I want one thing, so that one benefit follows), and **acceptance criteria**.
- The criteria are grouped into **named cases**. A case names a situation and lists two to six numbered steps. Each step carries one trigger and one response, written with the plain keywords *when*, *while*, *if*, *then*, and *shall*.
- A short code anchor trails at the end of a line and points to the rule's home in the spec. An anchor looks like `[INV-104]` or `[E-6, T-12]`. A reader can ignore the anchors. A maintainer follows them.

The test matrix follows the same format, defined in [`docs/test-matrix-format.md`](docs/test-matrix-format.md): each row is one criterion stating what a fact does and what it must never do, grouped by architecture node, and the coverage table at the document's end is generated from the rows and gated against hand edits. The roadmap and the architecture document follow it too, the architecture defined in [`docs/architecture-format.md`](docs/architecture-format.md): each part of the system stands as one node section naming its responsibility, the spec facts it owns, and where it lives in the code. One shared parser reads every node section, and every check reads a node through it.

Work enters the spec before code. A new behaviour arrives as a spec change, gets reviewed, and only then gets built. A guardrail check goes red when a shipped behaviour has no spec sentence behind it. A removed feature leaves a dated tombstone, and its history moves to `JOURNAL.md`.

---

## What's different

**The gates are scripts.** Four checks decide whether a push in your project is allowed. A surface is one named, user-visible part of what the project ships. The registry is the table listing them, `SURFACES.md` here. Every surface the registry lists shows up in what renders, and every rendered surface is listed. A change to a user-facing file carries a test. Every listed surface cites a spec anchor that exists. No anchor is duplicated and no surface is registered twice. The four are Python on the pre-push hook, mirrored in [CI](.github/workflows/gates.yml). A change that has drifted from its specification is refused. Some other frameworks enforce their specs by asking a model to check. A model having a bad day reports that it checked.

**It can decline a gate it cannot build honestly, and records the reasoning.** A planned gate would have failed a session that worked one step at a time. The [prover's record](docs/prover/) for that landing declined it, with three reasons: independence is a judgment, and a script sees only a diff; the evidence a correct run would leave is destroyed by design; and the one mechanical signal available would fire on every lawful sequential run. It shipped as a written discipline. The rule behind this decision is that a requirement no script can enforce stays a note, and a judgment call is never wired as an automated gate. The records are in [`docs/prover/`](docs/prover/), including the ones where the reviewer missed something and said so.

**The rules are built for a model's failure modes.** Every claim shown for review is tagged with its source: read from the artifact, your own recorded word, or the agent's inference, with inferences flagged most visibly. The line between what a document says and what a model filled in is invisible to a reader, and that is where the errors live. A background worker from a dead session is treated as a concurrent writer until three signals agree it stopped. A decision you withdraw twice keeps its recommendation and is never raised again, because a tireless agent will go on asking on its own.

---

## The rules are the product

The rules are the part a software house would charge you for: thirty-four shared rules across the skill set, stated once. They cover how a spec gets written so it stays readable. They cover when a question is worth your attention and when it is routine. They cover what a green suite does and does not prove.

<!-- generated:count:skills-lines — scripts/gen-tree-counts.py owns the block below -->

Written out, they and the skills carrying them run to 6,492 lines under `skills/`. Of those, 5,254 lines are the skill bodies, and the rest are the reference pages a body loads on demand. Count them yourself with `cat skills/*/SKILL.md skills/*/references/*.md | wc -l` and `cat skills/*/SKILL.md | wc -l`. A push of this repository is refused where either command disagrees with the number printed here. The body figure is what a session pays before it starts work, so it is the figure to hold down. It is held under the figure that includes the references. When it rises, every session that loads a skill pays more to begin.

<!-- /generated:count:skills-lines -->

You do not read them. They run.

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

[`live-spec-base`](skills/live-spec-base/) holds the shared rulebook · [`build-pipeline`](skills/build-pipeline/) sequences a change end to end · [`spec-author`](skills/spec-author/) writes the living spec · [`product-prover`](https://github.com/happysasha18/product-prover) reviews it (external skill, own repository) · [`design-reviewer`](skills/design-reviewer/) asks whether the design itself is right once the spec holds together · [`test-author`](skills/test-author/) derives the matrix and the tests · [`communicator`](skills/communicator/) shows work and asks answerable questions · [`feedback-intake`](skills/feedback-intake/) routes what you hand back · [`feedback-collector`](skills/feedback-collector/) sends upstream notes with your consent · [`text-audit`](skills/text-audit/) reads a text as a stranger and fixes where they stop · [`publish`](skills/publish/) gates anything leaving the machine.

## External skills

- **[product-prover](https://github.com/happysasha18/product-prover)** — spec verification and
  validation with formal-verification thinking. The pack's review step invokes it; it lives in its
  own repository with its own version line. `scripts/install-external-skills.sh` installs it
  (version floor in `skills/product-prover-pack/SKILL.md`); the pack-side bindings — mode names,
  record contract, pin map — live on that same page.


The ideas in five minutes: [`OVERVIEW.md`](OVERVIEW.md) · [pipeline](docs/pipeline.md) · [adoption](docs/adoption.md)

---

## Who it's for, and the limits

This pack is for people who can already build software, know what discipline costs, and now build with agents that are fast and untrustworthy. It is the wrong tool for a first project. It hands you a spec, an architecture document, a test matrix, and a pre-push hook. That is the right shape for the problem and too much for someone who has never shipped.

Three projects, one author, no outside adopters yet. The judgment loop is one model reviewing its own work. Only the mechanical gates are genuinely independent, which is why they are scripts. The version moves fast and the rules will sharpen under you. The gates stabilize first, because those carry red-first proofs.

Prior art is credited in full, including what was borrowed and from whom: [survey](docs/prior-art-frameworks.md) · [originality audit](docs/research/2026-07-10-originality-audit.md) · [comparative reviews](docs/research/2026-07-06-bmad-kiro-livespec-comparison.md), briefed to criticize all three subjects. This pack sits alongside BMAD, Kiro, and the wider spec-driven-development family. What it adds is the mechanical push gate and the recorded prover discipline. [Superpowers](https://github.com/obra/superpowers) is ahead of anything here on execution discipline, and its stars are earned. If you know prior art we missed, open an issue.

**Known issues.** Internal vocabulary still leaks into human-facing text. A register lint blocks the known leaks in shown artifacts, and chat stays the weakest surface. The spec still carries counted style debt, dated in the queue. The settings card is young and has run on one project. All three are tracked and reviewed at every push.

---

[MIT](LICENSE) © Alexander Abramovich, 2026 · [`VERSION`](VERSION) · [the ideas in five minutes](OVERVIEW.md)
