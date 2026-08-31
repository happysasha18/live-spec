## Words this skill uses

**Where the paths in this file point.** Two trees are in play. The named files under `scripts/`,
`guardrails/`, `templates/`, `tests/`, and `skills/` are the live-spec pack's own, at
`github.com/happysasha18/live-spec`. So are the design notes this page names by filename under
`docs/`. An install copies each skill folder into one place, so a path naming another skill points to
that skill's folder, beside this skill's folder. Every other path belongs to the project the pack is
attached to, including `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `JOURNAL.md`, and
`.live-spec/`.

Run every script named below from the live-spec repository root, as `python3 <path> <arguments>`. Each
one prints its own usage line when it is run with no arguments, so the arguments never have to be
guessed.

- **Wish** — one request a person voices in plain words, captured as a queue row.
- **Door** — the intake classification that sends a queued wish to one entry point of the pipeline. Its
  values are feature, bug, refactor, docs-only, and skip. It is decided before any code is written.
- **Queue row** — one row of the project's queue, `ROADMAP.md` in this pack. A closed row moves to
  `docs/queue-archive/`, so a row number cited below may sit there rather than in the live queue.
- **Lane** — one build train a session rolls through the pipeline.
- **Landing** — one piece of work reaching the repository's shared truth as one commit.
- **Host** — one project the pack attaches to. Each host keeps its own spec, queue, journal, and
  `.live-spec/` folder.
- **Host profile** — the host's own settings file, `.live-spec/profile.md`. This page reads its
  `project.kind`, `project.layers`, `project.design-principles`, and `project.axes` lines.
- **Kind** — what a host's product is, named from a fixed vocabulary: book, backend service, static
  site, fullstack app, CLI, or skill pack. The host profile records it.
- **Surface** — any part of the shipped product a user meets. A **stateful surface** holds state a
  user can change and find again later.
- **Spec-delta** — the set of spec sentences one wish or feature adds or changes.
- **Facet** — one aspect of a feature's design, ending as a written spec sentence.
- **Regression fence** — one sentence in a spec-delta naming a neighbouring promise that must stay
  true through the change, citing the clause it guards.
- **Composition axis** — one angle a stateful surface's behaviour can vary along.
- **Lens** — one named check the prover or the design review walks a document with.
- **Seat** — the session that orchestrates the work and reports to the person.
- **Red**, used as a verb — a check fails and stops the work at that point.

**The markers this page writes.** `[feature: F-x]` on a requirement heading marks a person-facing
scenario. `[target]` marks a surface or phase the spec names and does not yet specify for build.
`[default]` names a value the agent chose that the person may retune. `[GAP: ...]` under a criterion
records what the source left open. `⟨DECIDE⟩` marks a call base rule 1 sends to the person, and it
carries a one-line question.

**The bracket codes.** `INV-`, `E-`, `T-`, `S-`, `C-`, `M-`, `D-`, `A-`, `B-`, and `ACT-` codes index
requirements in this pack's own `PRODUCT_SPEC.md`. Its preamble names each letter's kind: `E-` an
entity, `INV-` an invariant, `T-` a transition, `M-` a rhythm rule, `A-` an adoption step, `B-` a
bootstrap step, `ACT-` an actor, `C-` a composition-axis rule, `D-` a recorded decision, and `S-` a
header rule. `PRODUCT_SPEC.index.md` maps each code to the criteria carrying it, written as `R12.4` —
requirement 12, criterion 4. Each sentence beside a code states its own rule in full, so a reader
holding this page alone can pass the codes over.

