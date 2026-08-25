# Work-kind table

The per-kind meanings referenced from `SKILL.md`'s "The work-kind table" section (SPEC T-16, INV-22):
WHAT the wish builds scales HOW each step runs. The door picks WHICH steps run; this table picks the
FORM each running step takes.

| Step | product (a user faces it) | infra (tooling for the project) | skill (an agent works by it) | prose (a human reads it) |
|---|---|---|---|---|
| 1 spec | full delta: fences, axes, facet sweep over visible surfaces | the tool's contract: inputs → outputs, failure behaviour, where it runs; usually "no visible surface — facets N/A" | the behaviour it must produce: trigger, the correction it makes, when NOT to fire | the reader, the claims, the reading path; visual facets only if it renders |
| 2 prove | as written | as written | as written | as written — the prover reads documents natively |
| 3 architecture | nodes + `file:line` pins | one node owns the tool, pinned to its entry point | the skill IS a node; pin its SKILL.md | owned by a docs node; new node only if structure grows |
| 4 prove architecture | when structure changed | same | same | usually stands down — assignment, no structure change |
| 5 matrix | rendered-level rows (E-15) | function-level rows: run the tool, assert real output | string rows on the SHIPPED SKILL.md; behaviour eval when the eval machinery lands (row 94) | render-level: file shipped, sections present, links resolve |
| 6 test | assert the real render | run on a fixture, assert output | string assertions against the installed artifact | assert the shipped file's content |
| 7 code | as written | as written | as written | the writing IS the step |
| 8 verify by deed | open the real artifact, eyes on it — then the VISITOR WALK (first visit · return · cross-entry · from-any-point navigation · exits) and the FEEL pass (motion quality, affordance craft) against the approved prototype's bar; the feel pass also reads the kind's declared design principles (the host profile's `project.design-principles`, the pack's per-kind starter set in ARCHITECTURE.md) and runs each in the medium's own form — the frontend kind's interactive-overlap rule (interactive controls that belong to different layers occupy separate screen space) is walked wherever a covering overlay opens over floating chrome, its pixel/DOM row living in this project's own suite; findings become rows or red (SPEC INV-30, INV-136, INV-139) | one real run, eyes on the output | re-read the INSTALLED copy; fire the trigger once where cheap; walk the installed skill-creator's review of the touched skill — format, frontmatter, description-triggering (does the skill load when it should), evals where applicable — findings folded or rejected by name in the landing record (SPEC INV-99) | render it by the show rule and READ it |
| 9 commit & show | show the render | show the run's output | version bump + installed-copy sync, same session | open the rendered page for the human |
| design-sync / snapshot | product with visuals: declared scope syncs (human-gated) | stands down | stands down | stands down |
