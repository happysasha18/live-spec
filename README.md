# live-spec

Twelve working [Claude Code](https://claude.com/claude-code) skills, plus the one shared rulebook
they all load, that turn a wish spoken in passing into a specified, reviewed, tested, committed
change. Claude Code is Anthropic's own coding agent, an app you install once; this pack is a set
of instructions it loads. You talk to Claude Code, and live-spec is what answers. Each skill is a
packaged set of instructions for one part of the work.

## Who this is for

Whoever owns a real project running behind Claude Code and wants what ships to match what was
decided, without personally reading every diff to check. You say what changed in your own words;
live-spec turns that into the spec, the tests, and the code, and blocks the push the moment any
two of those three disagree with each other.

## What you get

You tell your agent *"the report page needs a date filter"* and four minutes later it is written,
tested, and green. The tests pass because they came from the same spec. The spec never said what
happens when the date is invalid, so the agent picked some behaviour and shipped it. Nobody chose
that behaviour and nobody reviewed it, and the green suite never looked at it.

That is the gap. The spec became the thing your agent builds from, and nothing checks the spec
itself.

live-spec closes it. You say the sentence in passing, with nothing to file and no form. It gets
classified, written into a living spec, reviewed by a formal-verification pass — an automated,
structured read of the spec itself that hunts for exactly this kind of gap, an unstated case nobody
decided — covered by tests derived from that spec, coded until green, and committed with its documents in one change.
A script on the pre-push hook compares the spec to the code that shipped and refuses the push when
the two disagree. There is no CLI. You talk to it.

Closing that one gap is only the first step toward the actual goal, still under construction: a
small, self-running engineering team sitting behind your one conversation. You hand it ideas and
instructions as they occur to you — a wish, a correction, a stray thought — and it aims to work
out on its own whether that is a question, a decision, feedback, or new work, assemble whichever
specialists the change actually needs, do everything that is derivable on its own, and ask you
only about taste, strategy, authority, and anything irreversible. What ships today is the first
working piece of that goal.

## What it missed

Real accounts: one of the formal-verification pass's own rules checks that every screen or step a
user can reach has a way out — no dead ends. It passed a design that let a first-time visitor into
a one-off screen with nothing on it ever pointing back out again, because having a way out and
being reachable again later are two different questions, and no rule asked the second one yet.
That gap became a new rule ([`docs/lenses.md`](docs/lenses.md)).

A test once asserted that near-silent audio tracks are hidden from the list a listener browses
them in. The spec required the opposite — those tracks stay visible, with their names. The test
was green for a month while the product did the wrong thing.

And a scroll that satisfies its motion spec exactly — every number in it met — can still feel
cheap to the person using it, which no rubric will catch honestly.

> **A spec owns what a project can write down and test. Feel belongs to the owner's eye.**

The full accounts, including the reviews that missed something and said so, live in the prover
records: [`docs/prover/`](docs/prover/).

## How it works

Work enters a living spec, `PRODUCT_SPEC.md`, before any code: a wish becomes a spec delta, a
formal-verification review folds in what it missed, an architecture document maps it to real code,
a test matrix derives from the proven spec, then the code gets written until the suite is green.
Four scripted checks sit on the pre-push hook and turn it red: a change with no test behind it, a
piece of content the spec promises that came out missing or blank, a behaviour with no spec
sentence backing it, and two different things sharing one name. The rules behind every step of
this pipeline — twenty-seven shared rules across the skill set — are stated once, in
[`live-spec-base`](skills/live-spec-base/SKILL.md). You do not read them yourself; the agent loads
them and follows them on every turn, automatically.

The full station-by-station walk, the spec's own format, and what each gate checks and why:
**[the pipeline, station by station →](docs/pipeline.md)** · [the ideas in five minutes
→](OVERVIEW.md)

## The skills

[`live-spec-base`](skills/live-spec-base/) holds the shared rulebook · [`director`](skills/director/)
reads the human's message first and decides what it is · [`build-pipeline`](skills/build-pipeline/)
sequences a change end to end · [`spec-author`](skills/spec-author/) writes the living spec ·
[`product-prover`](https://github.com/happysasha18/product-prover) reviews it (external skill, own
repository) · [`product-prover-pack`](skills/product-prover-pack/) is the adapter that binds that
external skill to this pack · [`design-reviewer`](skills/design-reviewer/) asks whether the design
itself is right once the spec holds together · [`architect`](skills/architect/) writes or updates
the architecture from the proven spec · [`test-author`](skills/test-author/) derives the matrix and
the tests · [`communicator`](skills/communicator/) shows work and asks answerable questions ·
[`feedback-intake`](skills/feedback-intake/) routes what you hand back ·
[`feedback-collector`](skills/feedback-collector/) sends upstream notes with your consent ·
[`text-audit`](https://github.com/happysasha18/text-audit) reads a text as a stranger and fixes
where they stop (external skill, own repository) · [`text-audit-pack`](skills/text-audit-pack/) is
the adapter that binds that external skill to this pack · [`publish`](skills/publish/) gates
anything leaving the machine.

## Staying in control

Every default the agent picked is printed in the delivery report at the end of a change, in the
product's own words, marked as tweakable. Only what the documents genuinely leave open reaches you
as a question — routine choices are made and reported, and the work keeps moving. Undo is one
commit: the change lands with its spec, matrix, and architecture together. And it cannot run away —
the gates go red and stop the push.

## Where the pack stands

One author, no outside adopters yet — small and early. Every gate earns its place before it ships:
someone watched the exact mistake it now catches happen for real, on purpose, then built the gate
and confirmed it catches that same mistake. A change that drifts from its own spec is refused
automatically, by the same script, whatever the day. Content judgment — *is this the right thing to
build* — has no independent check yet. The loop is one model reviewing its own work.

## Install

There are two ways in: the plugin road, which downloads nothing you have to keep, and the clone
road, for a programmer who wants the pack's own tree on disk. The lines below are the only ones you
ever type — everything after this, you say in plain words.

**Plugin road:**

```
/plugin marketplace add happysasha18/live-spec
/plugin install live-spec@live-spec
```

**Clone road:**

```bash
git clone https://github.com/happysasha18/live-spec.git
cd live-spec && ./install.sh
scripts/install-external-skills.sh
```

`install.sh` copies the skill folders into `~/.claude/skills/`. `scripts/install-external-skills.sh`
installs one more skill, `product-prover` — the one that reviews your spec — from its own
repository; it needs network access.

Either road, open your project in Claude Code and say *"attach live-spec to this project"*, or
*"found a new project on live-spec"* in an empty folder. The pack reads your project, asks what it
needs to know in plain words, writes your first spec, and wires the push gate — checks, config, git
hook, all of it — in the same walk. There is nothing to do by hand.

A programmer who wants to read or drive the documents directly, wire the gate into CI, or run a
piece of the setup by hand: the full technical walk-through is
[`docs/adoption.md`](docs/adoption.md), the push gate's own fields and hook lines are in
[`guardrails/README.md`](guardrails/README.md), and the spec, matrix, and architecture formats are
[`docs/spec-format.md`](docs/spec-format.md), [`docs/test-matrix-format.md`](docs/test-matrix-format.md),
and [`docs/architecture-format.md`](docs/architecture-format.md). A technical wish for the pack
itself is welcome — [open an Issue](https://github.com/happysasha18/live-spec/issues/new/choose).

**Known issues.** Words meant for the people building this pack still leak into text meant for a
stranger reading it — an insider term with no gloss, dropped as if the reader already knew it. A
register lint (a check for tone pitched at the wrong reader) —
[`scripts/preshow-register-lint.py`](scripts/preshow-register-lint.py) — blocks the leaks it
already knows before an artifact is shown, and chat stays the weakest surface. The spec still
carries style debt, held at zero for the defects the lint names by line
([`scripts/spec-debt-cap.json`](scripts/spec-debt-cap.json)), with the work to clear the rest dated in
the queue, [`PLAN.md`](PLAN.md). The settings card is the page
listing every setting the pack knows, its current value, and one plain line saying how to change
it. That card is new, and not yet tested by much real use. All three are tracked and reviewed at
every push. Release history: [`VERSION`](VERSION).

Prior art is credited in full, including what was borrowed and from whom:
[survey](docs/prior-art-frameworks.md) · [originality audit](docs/research/2026-07-10-originality-audit.md)
· [comparative reviews](docs/research/2026-07-06-bmad-kiro-livespec-comparison.md). This pack sits
alongside BMAD, Kiro, and the wider spec-driven-development family; what it adds is the mechanical
push gate and the recorded prover discipline. [Superpowers](https://github.com/obra/superpowers) is
ahead of anything here on execution discipline, and its stars are earned. If you know prior art we
missed, open an issue.

---

[MIT](LICENSE) © Alexander Abramovich, 2026 · [`VERSION`](VERSION) · [the ideas in five minutes](OVERVIEW.md)
