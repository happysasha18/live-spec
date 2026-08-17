# live-spec

**Ten working [Claude Code](https://claude.com/claude-code) skills, plus the one shared rulebook they all load. They turn a wish spoken in passing into a specified, reviewed, tested, committed change. Scripts block the push when the documents and the code disagree.**

---

You tell your agent *"the report page needs a date filter"* and four minutes later it is written, tested, and green. The tests pass because they came from the same spec. The spec never said what happens when the date is invalid, so the agent picked some behaviour and shipped it. Nobody chose that behaviour and nobody reviewed it, and the green suite never looked at it.

That is the gap. The spec became the thing your agent builds from, and nothing checks the spec itself.

live-spec closes it. You say the sentence in passing, with nothing to file and no form. It gets classified, written into a living spec, reviewed by a formal-verification pass, covered by tests derived from that spec, coded until green, and committed with its documents in one change. A script on the pre-push hook compares the spec to the code that shipped and refuses the push when the two disagree. There is no CLI. You talk to it.

---

## Install

There are two ways in. Pick one road at step 1, then follow that road's lines wherever the steps below fork.

### Step 1 — get the pack onto your machine

**The plugin road.** Type two lines into Claude Code:

```
/plugin marketplace add happysasha18/live-spec
/plugin install live-spec@live-spec
```

That is the whole step. The plugin puts the entire pack tree under `~/.claude/plugins/cache/`. You do not clone this repository, now or later.

**The clone road.** Clone the repository and run its installer:

```
git clone https://github.com/happysasha18/live-spec.git
cd live-spec && ./install.sh
```

`install.sh` copies the skill folders into `~/.claude/skills/` and copies nothing else. Keep the clone. It is your copy of the pack tree, and step 3 runs a script that lives inside it.

### Step 2 — attach the pack to a project

Both roads do the same thing here. Open the project in Claude Code and say *"attach live-spec to this project"*, or *"found a new project on live-spec"* in an empty directory. The pack locates its own tree and reads yours, then runs the setup walk that fits. [`adopt/START.md`](adopt/START.md) founds a fresh project; [`adopt/ADOPT.md`](adopt/ADOPT.md) attaches an existing codebase and writes your first spec from what your code ships today. [`docs/adoption.md`](docs/adoption.md) tells the same story in plainer words.

### Step 3 — install the push gate

The push gate is a separate step, and it reads the documents step 2 just wrote. **The setup walk offers to install it for you.** That is the ordinary path. Read on only if you would rather do it by hand.

By hand, run one script from your project's root. It lives in the pack tree you already got in step 1, so the line you type depends on which road you took:

```
# plugin road — the tree sits in the plugin cache
bash ~/.claude/plugins/cache/*/live-spec/*/adopt/install-scaffold.sh

# clone road — the tree is the clone from step 1
bash /path/to/live-spec/adopt/install-scaffold.sh
```

It copies the four checks into your project's `guardrails/` and seeds `guardrails.config.json`.

That config then needs two things from you. Fill in your paths: the spec, the test matrix, the queue, the tests, and the surface registry — the table listing every surface the project ships, a surface being one named part a user meets: a screen, a page, a command, a public function. The queue is the dated list of what has been asked of the product and where each ask stands. This repository keeps its own in [`ROADMAP.md`](ROADMAP.md).

Second, empty the config's `waivers` block. It ships holding one example waiver, and that example switches the completeness check off. Leave the example in place and you run on three checks instead of four, with nothing to tell you.

One more step, outside the config: add the four check lines to `.git/hooks/pre-push`. They are listed in [`scaffold/guardrails/README.md`](scaffold/guardrails/README.md). Create that hook file if your project has none, and make it executable. The checks run on your next push.

The checks need Python 3.9 or newer, and a project that is already a git repository.

After that everything runs in plain words: any wish, *"status"* — where the work stands now and what is next — *"publish"*.

---

## What the spec looks like

A project under the pack keeps one document, `PRODUCT_SPEC.md`, stating what the product promises today. A stranger can read a section on the first pass. The format is a requirements genre, defined in [`docs/spec-format.md`](docs/spec-format.md):

- The document opens with a **glossary**. Every domain noun used anywhere in the spec has a one-sentence definition. An ordinary English word needs no entry.
- The body is a list of **requirements**. Each requirement has a short **context** (when the situation arises, who is involved, what the reader sees), one **user story** (as a person in a named role, I want one thing, so that one benefit follows), and **acceptance criteria**.
- The criteria are grouped into **named cases**. A case names a situation and lists two to six numbered steps. Each step carries one trigger and one response, written with the plain keywords *when*, *while*, *if*, *then*, and *shall*.
- Each line ends with a short code in brackets: `[INV-104]`, or `[E-6, T-12]` where several apply. The code is that rule's permanent id, and this spec line is its home. The test matrix and the architecture document cite the same code, so a maintainer can walk between all three. A reader can ignore the codes.

A **fact** is one thing the spec says the product does. The test matrix follows the same format, defined in [`docs/test-matrix-format.md`](docs/test-matrix-format.md). Each matrix row takes one fact and states both halves of it: what it does, and what it must never do. Rows are grouped by architecture node, and the coverage table at the document's end is generated from the rows and gated against hand edits.

The roadmap and the architecture document follow the format too. The architecture is defined in [`docs/architecture-format.md`](docs/architecture-format.md). Each part of the system stands as one node section, naming its responsibility, the facts it owns, and where it lives in the code. One shared parser reads every node section, and every check reads a node through it.

Work enters the spec before code. A new behaviour arrives as a spec change, gets reviewed, and only then gets built. A guardrail check goes red when a shipped behaviour has no spec sentence behind it. A removed feature leaves a dated tombstone, and its history moves to `JOURNAL.md`.

---

## What's different

**The gates are scripts.** Four checks decide whether a push in your project is allowed. The surface registry is the table listing the surfaces a project ships, `SURFACES.md` here. The first check reads that table both ways round: everything the registry lists is really shipped, and everything shipped is listed. The second: a change to a user-facing file carries a test. The third: every listed surface cites a spec code that exists. The fourth: no code is claimed twice and no surface is registered twice. The four are Python on the pre-push hook, mirrored in [CI](.github/workflows/gates.yml). A change that has drifted from its specification is refused. Some other frameworks enforce their specs by asking a model to check. A model having a bad day reports that it checked.

**It can decline a gate it cannot build honestly, and records the reasoning.** One planned gate was refused. It would have gone red on a session that landed two independent pieces of work one after the other. Those two could have run side by side. The [record of that refusal](docs/prover/2026-07-18-rows386-412-414-lane-open-act.md) gives three reasons. Whether two pieces of work were independent is a senior's read, and a script sees only a diff. The evidence a correct run leaves is destroyed on purpose: a finished lane's branch is torn down when it lands. And the one signal a script could key on would fire on every lawful one-at-a-time run too. So the requirement shipped as a written discipline, held by the session and backed by no script. The rule behind that: a requirement no script can enforce stays a note, and a judgment call is never wired as an automated gate. The records are in [`docs/prover/`](docs/prover/), including the ones where the reviewer missed something and said so.

**The rules are built for a model's failure modes.** Every claim shown for review is tagged with its source. The source is the artifact it was read from, your own recorded word, or the agent's inference. Inferences are flagged loudest ([the rule](skills/communicator/SKILL.md)). The line between what a document says and what a model filled in is invisible to a reader, and that is where the errors live. A background worker from a dead session counts as a live writer until three signals agree it stopped. Its files stop changing, its heartbeat goes stale, and it fails to answer a direct message ([`docs/worker-liveness.md`](docs/worker-liveness.md)). A decision you withdraw twice keeps its recommendation and is never raised again, because a tireless agent will go on asking ([the rule](skills/communicator/SKILL.md)).

---

## The rules are the product

The rules are the part a software house would charge you for: thirty-four shared rules across the skill set, stated once in [`live-spec-base`](skills/live-spec-base/SKILL.md). They cover how a spec gets written so it stays readable. They cover when a question is worth your attention and when it is routine. They cover what a green suite does and does not prove.

<!-- generated:count:skills-lines — scripts/gen-tree-counts.py owns the block below -->

Written out, they and the skills carrying them run to 5,549 lines under `skills/`. Of those, 4,228 lines are the skill bodies, and the rest are the reference pages a body loads on demand. Count them yourself with `cat skills/*/SKILL.md skills/*/references/*.md | wc -l` and `cat skills/*/SKILL.md | wc -l`. A push of this repository is refused where either command disagrees with the number printed here. The body figure is what a session pays before it starts work, so it is the figure to hold down. It is held under the figure that includes the references. When it rises, every session that loads a skill pays more to begin.

<!-- /generated:count:skills-lines -->

You do not read them. They run.

The relationship is the one you have with a builder. You do not need to know how; you still decide what. A good contractor does not ask the client to choose the rebar, and does not pick the kitchen either.

The pack is opinionated. The opinions belong to one engineer, and they are not neutral industry practice. Adopting the pack adopts them.

---

## Staying in control

You keep control, in a strong sense. Access to the diff was never the problem. Knowing where to look is.

- **Nothing is decided silently.** Every default the agent picked is printed in the delivery report at the end of a change. It appears in the product's own words, marked as tweakable: *"on a phone this gallery stacks into one column."* ([the rule](skills/communicator/SKILL.md))
- **Routine choices are made and reported; the lane keeps moving.** Only what the documents genuinely leave open reaches you as a question.
- **Undo is one commit.** The change lands with its spec, matrix, and architecture together.
- **It cannot run away.** The gates go red and stop the push.

Many tools offer control by asking a long list of questions up front. That is more work for you.

---

## What it missed

One check hunts dead ends: a state a user can enter and cannot leave. It ran on the right screen and found nothing, because that screen did have exits. The trap was a door shown only on a first visit, with no way back to it afterwards. The check tested each state for an exit and never asked whether a page you leave can be reached again. That was the method's own fault, and it became a new rule ([`docs/lenses.md`](docs/lenses.md), INV-50).

A test asserted that near-silent audio tracks are hidden from a view. The spec required the opposite: those tracks stay visible, with their names. The test was green for a month while the product did the wrong thing.

And a scroll that satisfies its motion contract exactly can still feel cheap, which no rubric will catch honestly.

> **A spec owns what a project can write down and test. Feel belongs to the owner's eye.**

The full accounts, including the reviews that missed something and said so, live in the prover records: [`docs/prover/`](docs/prover/).

---

## The skills

[`live-spec-base`](skills/live-spec-base/) holds the shared rulebook · [`build-pipeline`](skills/build-pipeline/) sequences a change end to end · [`spec-author`](skills/spec-author/) writes the living spec · [`product-prover`](https://github.com/happysasha18/product-prover) reviews it (external skill, own repository) · [`product-prover-pack`](skills/product-prover-pack/) is the adapter that binds that external skill to this pack · [`design-reviewer`](skills/design-reviewer/) asks whether the design itself is right once the spec holds together · [`test-author`](skills/test-author/) derives the matrix and the tests · [`communicator`](skills/communicator/) shows work and asks answerable questions · [`feedback-intake`](skills/feedback-intake/) routes what you hand back · [`feedback-collector`](skills/feedback-collector/) sends upstream notes with your consent · [`text-audit`](skills/text-audit/) reads a text as a stranger and fixes where they stop · [`publish`](skills/publish/) gates anything leaving the machine.

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

Three projects, one author, no outside adopters yet. The judgment loop is one model reviewing its own work. Only the mechanical gates are genuinely independent, which is why they are scripts. The version moves fast and the rules will sharpen under you. The gates stabilize first, because each one carries a red-first proof. A red-first proof is a test watched failing before the gate existed, which is what shows the gate can fail at all. Every gate's proof is named in [`guardrails/gate-red-proofs.json`](guardrails/gate-red-proofs.json), and a gate with no proof blocks the push.

Prior art is credited in full, including what was borrowed and from whom: [survey](docs/prior-art-frameworks.md) · [originality audit](docs/research/2026-07-10-originality-audit.md) · [comparative reviews](docs/research/2026-07-06-bmad-kiro-livespec-comparison.md), briefed to criticize all three subjects. This pack sits alongside BMAD, Kiro, and the wider spec-driven-development family. What it adds is the mechanical push gate and the recorded prover discipline. [Superpowers](https://github.com/obra/superpowers) is ahead of anything here on execution discipline, and its stars are earned. If you know prior art we missed, open an issue.

**Known issues.** Internal vocabulary still leaks into human-facing text. A register lint — [`scripts/preshow-register-lint.py`](scripts/preshow-register-lint.py) — blocks the leaks it already knows before an artifact is shown, and chat stays the weakest surface. The spec still carries style debt, counted and capped in [`scripts/spec-debt-cap.json`](scripts/spec-debt-cap.json), with the work to clear it dated in the queue, [`ROADMAP.md`](ROADMAP.md). The settings card is the page listing every setting the pack knows, its current value, and one plain line saying how to change it. That card is young and has run on one project. All three are tracked and reviewed at every push.

---

[MIT](LICENSE) © Alexander Abramovich, 2026 · [`VERSION`](VERSION) · [the ideas in five minutes](OVERVIEW.md)
