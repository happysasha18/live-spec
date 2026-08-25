# Request-kind table

The closed set of request kinds referenced from `SKILL.md`'s "When to run it" section (SPEC INV-151):
every request kind has a named entry document and a mandatory back-check.

| Request kind | Enters at | Mandatory back-check |
|---|---|---|
| product behaviour | the spec step, flows down | none above it; the fit walk validates against the whole spec (FEATURE-FIT) |
| a technically-phrased request | the architecture step | the spec-motion tripwire fires **at intake** — a surface / state / unbacked-behaviour trip lifts it to the spec at the door (before the architecture work is built on an unlifted premise), outranking the request's own label (INV-16), and re-fires mid-work |
| a defect | the matrix step, red-on-bug test | a fixed fact also in spec prose updates the spec sentence the same change (INV-104); a recurring bug (~30 days, same area, caught by grepping `JOURNAL.md` for the area's name and its dates before taking the bug) re-doors to feature — a repeat means the area is missing an invariant |
| docs-only | its own light path | the removal accounting (INV-109) + the register lint |
| a tiny reversible edit | the skip shortcut (code + test) | the spec-backed-literal tripwire (INV-104); anything visual enters at the matrix minimum |
| a settings / parameter value | the settings ladder (profiles) | check it is genuinely a value — a new RULE is a feature for the spec |
| an inbox wish (cross-project arrival) | the inbox sweep, then classified at the door like any request | the door's own verdict on the wish at intake; the outsider never writes the tree (base rule 16) |
| a method / skill change | the same criterion, work-kind `skill` scaling each step's form | the pack's own product IS the method, so there is no separate meta-layer set — the design-reviewer's own landing this session is the worked proof (INV-22) |
| a sketch (see / try) | a labelled `prototype/` home | unclear see-vs-have ⇒ one plain question; promotion enters at the spec step (base rule 16) |
| research / a question from the docs | no layer (no write) | — |
| a feedback hand-back | feedback-intake, to the home its law owns | not the agent's own output; opens no queue row on its own (SPEC T-20) |
| setting an existing project up on the pack | the attach walk, `adopt/ADOPT.md` | each phase's own done-condition; the attach record names the pack version that ran |
| founding a new project on the pack | the founding walk, `adopt/START.md` | the scaffold suite green as the starting floor, before the first wish |
| bringing an already-adopted project onto the current pack | the catch-up walk, `MIGRATION.md` | that walk's before-and-after inventory and its named restore point |

The three setup rows are reached through the routing card,
[project-setup.md](project-setup.md). It resolves the pack's own tree, reads the project tree, and
picks among them (SPEC INV-307). All three entry documents sit in that resolved pack tree:
`adopt/ADOPT.md`, `adopt/START.md`, and `MIGRATION.md`. A host project may carry files of the same
name that mean something else.
