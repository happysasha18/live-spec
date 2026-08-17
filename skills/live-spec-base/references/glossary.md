# The words this file uses

The one home for the terms the rulebook's rules deal in. It holds the short read for each term
and names `PRODUCT_SPEC.md` as the authority behind it. It sits in the base skill's own package,
beside `SKILL.md`. Open it when a term is being resolved, and not before. Every entry below reads
exactly as it read in the rulebook body.

Each term is defined once. Most sit in the glossary of `PRODUCT_SPEC.md`, whose entry is the authority
behind the short read given here.

- **the pack** — the shipped live-spec method: its skills, its document and suite templates, and its
  guardrail scripts. It carries a version.
- **a host** — one project the pack attaches to. Each host holds its own spec, queue, journal, and
  `.live-spec/` folder.
- **the seat** — the one acting orchestrator session that owns judgment, orchestrates the pipeline,
  briefs workers, judges lane independence, and reports to the person. The glossary keeps the one name
  seat throughout. It records the senior and the orchestrator as the source's other names for it, and
  this file adds a fourth, the lead. The four names mean the one session.
- **a worker** — a delegated agent session the seat briefs for a bounded piece of mechanical work,
  narrowed to the files its brief names.
- **a tier** — the model level a unit of work runs at: a no-decision one-shot worker, a multi-step
  mechanical worker, or the seat for judgment. Rule 5 names haiku and sonnet as the two worker levels.
- **a brief** — the written instruction set a worker runs from, carrying its files, its steps, its
  clock, and its stop conditions.
- **a wish** — one request a person voices in plain words, captured as a queue row and carried to a
  recorded terminal state.
- **a queue row** — one live wish written as exactly five cells of `ROADMAP.md`: its id, the wish,
  its class, its status, and its acceptance. Its home is `docs/roadmap-format.md`. This file calls it
  a row.
- **a lane** — one build train a session rolls through the pipeline. A lane branch is that lane's
  isolated copy, a git worktree holding a branch named for its queue row.
- **the pen** — the single write-lock a repository holds, under which one delivery reaches the
  repository's shared truth at a time.
- **a landing** — the act of one piece of work reaching the repository's shared truth as one commit
  under the pen.
- **a gate** — a check that must pass before work proceeds, and a red gate stops the work at that
  step. Where a sentence here says a check *reds* something, it means the check fails on it.
- **a checkpoint** — a saved point of work that can be resumed from, written under `.live-spec/`.
- **the attic** — the host's append-only archive folder `attic/`. A superseded file moves here with
  one manifest line and is kept for good.
- **a breakpoint** — a point where a movement ends and session memory can be wiped with no loss, its
  live state replaced, a dated journal entry added, and the work committed.
- **a door** — the intake classification placing a queued wish at one entry point of the pipeline,
  one of feature, bug, refactor, docs-only, or skip. An ask merely to see or try a thing takes a
  separate entry lane, the labelled-sketch door, held outside that five-way set.
- **an agent** — defined where the rule that binds it stands, at rule 31.
- **an agent card** — a host's self-describing file `.live-spec/agent.md`, stating its name, mission,
  zones, published contracts, and inbox address. `templates/agent.template.md` gives its shape.
