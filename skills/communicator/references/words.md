# The words this skill uses

The vocabulary behind the rules in [`../SKILL.md`](../SKILL.md). The body points here at its top, and
a reader meeting an unfamiliar term on that page settles it from this file. Nothing here is a rule.
Every definition below was taken from a source in the tree: the glossary of `PRODUCT_SPEC.md`, the
words section of `skills/live-spec-base/SKILL.md`, a spec criterion, or a shipped script.

**Where the paths point.** Two trees are in play. Every path on the body's page and on this one sits
in the repository of the project the session is working on. A path opening with `references/` is the
exception: it names a file in this skill's own directory, beside this file. A path opening with
`skills/`, `scripts/`, `guardrails/`, `hooks/`, `templates/`, or `adopt/` names a file in the
live-spec pack's own repository. Its public home is `github.com/happysasha18/live-spec`. An install
copies each skill folder into one place, so a path naming another skill points to that skill's
folder, beside this skill's folder. The `templates/` and `adopt/` folders stay in the pack's
repository, since an install copies them nowhere.

**Where the codes resolve.** A bracket code such as `INV-93` or `E-17` points to that rule's home in
the project spec, `PRODUCT_SPEC.md`. The letter before the number names the kind: `E-` an entity,
`INV-` an invariant, `T-` a transition, `M-` a rhythm rule, `A-` an adoption step, `B-` a bootstrap
step, `ACT-` an actor, `C-` a composition-axis rule, `D-` a recorded decision, `S-` a header rule, and
`F-` a feature. `PRODUCT_SPEC.index.md` maps each code to the requirements that carry it. A row number
points into the project's one list, `PLAN.md`, which holds the plan and the queue in one document. A
row that has reached a terminal state moves to a dated file under `docs/queue-archive/`, so a number
missing from the list is looked up there.

**Two numbering systems share the `(rule N)` form.** On the body's page a bare *(rule N)* counts its
twenty-two rules. Inside the body's section "The writing register", and inside
[`writing-register.md`](writing-register.md), it counts that register's own eighteen rules. Read the
tag against the section it stands in.

**Base rules.** A "base rule N" points into `skills/live-spec-base/SKILL.md`; its own frontmatter
states how many numbered rules it carries. The ones the body cites are 1 ask never guess, 2 plain words carry the
meaning, 4 one canonical home per fact, 6 every long or delegated piece of work keeps a checkpoint,
10 nothing is silently deleted, 13 a claim needs its primary source, 16 a prototype stays a sketch,
and 27 the seat decides what it can decide.

## The terms

- **Wish** — one request a person voices in plain words, captured as a queue row.
- **Door** — the intake classification placing a wish at one entry point of the pipeline. Its five
  values are feature, bug, refactor, docs-only, and skip. It is decided before any code is written.
- **Work-kind** — the intake axis naming what a wish produces: product, infra, skill, or prose.
- **Footprint** — the reach the intake read named: presentation-only, single-module, or cross-cutting.
  The three-source read that names it reads the spec, the architecture, and the code at one moment
  (`INV-128`).
- **Map note** — the row field `map:`, recording how a wish maps onto the product. Its three values are
  changes feature X, a new feature, and restructure.
- **Lane** — one build train a session rolls through the pipeline. **Step** — one stage of that walk.
- **The pen** — the single write-lock a repository holds. One delivery reaches the shared truth at a
  time, and a lane waiting for the pen names the row it waits behind.
- **Seat** — the one acting orchestrating session. `references/glossary.md` records the senior, the
  orchestrator, and the lead as the source's other names for it; the base skill's own rules use the one
  name, seat. `PRODUCT_SPEC.md`'s glossary also names a **remote seat** — a session sharing no
  filesystem with the assigned one — a related but separate sense, naming where a session runs rather
  than which session orchestrates.
- **Worker** — a delegated agent session the seat briefs for a bounded piece of mechanical work.
- **Tier** — the model level a unit of work runs at: a one-shot worker, a mechanical worker, or the
  seat for judgment. Haiku and sonnet are the two worker levels, opus is the seat, and Fable is the
  hard-pass model the person names by hand.
- **Beat** — one narration line marking one unit of progress.
- **Movement** — a stretch of work ending at a breakpoint, where session memory can be wiped with no
  loss. That ending is stated in `skills/live-spec-base/SKILL.md` and in the spec glossary. [GAP: what
  opens a movement is unstated, so the pre-report walk's trigger rests on the seat's own reading.]
- **Stretch** — a run of work with one ending, which rule 18 delivers in a closing line. An
  away-stretch is a stretch the person has stepped away from, which rule 17 governs. [GAP: no document
  in the tree states what opens a stretch.]
- **Landing** — one piece of work reaching the repository's shared truth as one commit.
- **Delivery report** — the report a landing carries, and the canonical name for it.
- **Harvest** — writing an answer that came back into the queue row it belongs to.
- **Resume file** — the host's `NEXT_STEPS.md`, whose top item base rule 6 writes when work stops red.
- **Checkpoint** — a saved point of work that can be resumed from, written under `.live-spec/`.
- **Profile** — the host's own settings file, `.live-spec/profile.md`, built from
  `templates/profile.template.md`. Its show line settles how this project shows work.
- **Decision archive** — the directory `docs/decisions/`, where a decision page is filed once its
  answer comes back. The body also calls it the decision archives.
- **Facet** — one aspect of a feature's design, ending as a written spec sentence. A defaulted facet
  sentence carries the literal tag `[default]` at its line end.
- **`[target]` tag** — the marker a spec line carries, on a line of its own, for a feature or leg that
  is promised and not yet built.
- **Attic** — the host's append-only archive folder, `attic/`. A superseded file moves here with one
  manifest line and is kept for good.
- **Prover record** — one dated file under `docs/prover/`, recording one review pass and its verdict.
  **Matrix row** — one row of the project's `TEST_MATRIX.md`. **Adoption record** — the host's
  installed-set record under `.live-spec/`, written when a host takes the pack on (`adopt/ADOPT.md`,
  phase 6). [GAP: the tree names that file the installed-set record, so the two names are one thing.]
- **Far tier** — the queue's tier for a row kept with no revisit trigger and no plan to run.
  [`field-examples.md`](field-examples.md) holds its report shape.
- **Method version** — the pack-and-skill version set a piece of work was carried out under, read from
  the host's installed set.
