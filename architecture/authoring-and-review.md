### [node: spec-author]

**responsibility** — authoring method for a living, use-case-first, prover-ready PRODUCT_SPEC.md

**owns** —
- E-4 · C-1 · T-13 · INV-18 · INV-29 · INV-50 · T-14 · INV-19 · INV-20 · INV-21 · INV-101 · INV-118 · INV-126 · INV-127 · INV-138 · INV-226 · INV-244
- INV-248 (the lens carried by product-prover)
- INV-150 · INV-167 · INV-168 · E-33 · INV-185 · INV-186 · INV-187 · INV-215
- INV-321 (a criterion names what makes it happen: a command, a session following an instruction, a surface drawn on request, or nothing yet. It is a law of authoring, so it sits with the author's node; the `[target]` marker it leans on is this node's already)

**pins** —
- `skills/spec-author/references/the-spine.md:1` (spine)
- `skills/spec-author/references/the-spine.md:27` ([target] tag tripwire)
- `skills/spec-author/references/facet-sweep.md:26` (axes composition)
- `skills/spec-author/SKILL.md:96` (fences)
- `skills/spec-author/references/facet-sweep.md:1` (facet sweep — the canonical facet list)
- `skills/spec-author/references/how-it-reads.md:68` (the enumeration-threshold structure rule, INV-215)

**notes** —
- also carries the prototype-norm pointer's format sentence (`norm: <path>`, frozen copy in `docs/norms/`) — wiring, the invariant's owner is build-pipeline
- also carries the pole-declaration duty for a new host-specific capability (the pack-to-host split, owner base-rulebook)

### [node: product-prover]

**responsibility** — formal review of spec and architecture; executes the push-gate re-check

**owns** —
- M-6 · INV-61 · INV-72 · INV-114 · INV-125 · INV-140 · INV-170 · INV-171
- also carries lenses it does not own, each named beside its actual owner:
    - the entry-symmetry lens (owner spec-author)
    - the entry-state lens (owner spec-author)
    - the transition-payload lens (owner spec-author)
    - the declared-laws station (owner spec-author)
    - the paired-transition-symmetry lens (owner spec-author)
    - the scenario-level entry/exit lens (owner spec-author)
    - the edge-condition-completeness lens (owner spec-author)
    - the delivery-separability lens (owner spec-author)
    - the interactive-overlap lens (owner base-rulebook)
    - the cross-source-disagreement lens (owner build-pipeline)
    - the prototype-norm lens (owner build-pipeline)
- the discovery-side sibling of the declared-class uniformity lens is the design review (owner design-reviewer)

**pins** — the prover's mechanics live in a repository this pack does not own. The pack
cannot promise a line number there, so its pins stand on the tracked adapter instead. The
adapter is the one place the pack updates when a lens moves in a prover release.
- `skills/product-prover-pack/SKILL.md:15` (mode names — the review modes the pipeline asks for)
- `skills/product-prover-pack/SKILL.md:103` (unwritten seams — the stress-lens family, INV-72)
- `.live-spec/profile.md:6` (gate cadence instance)
- `skills/product-prover-pack/SKILL.md:73` (restructure-merge gate — INV-114 delta-judging)

### [node: design-reviewer]

**responsibility** — the design-review pass

**owns** —
- INV-141 (ROADMAP row 310)
- INV-142 · INV-154
- INV-156 (ROADMAP row 323. This node holds the class because it reached the one-class reading from the record-sibling seam it already owns, design review → record. The class is declared once here, and product-prover and build-pipeline cite it without restatement.)
- INV-165 · INV-169

**pins** — `skills/design-reviewer/SKILL.md:1` (frontmatter + when it fires), the similarity-lens, confidence-read, echo-channel, and record-discipline sections in the same file

### [node: text-audit]

**responsibility** — the audit-and-fix loop for human-facing texts. It runs the mechanical register lints first, then fresh zero-context cold reads. Each finding is fixed at its source until two consecutive reads come back clean.

**owns** — INV-266, INV-267, INV-268 (text-audit is the skill that runs this loop)

**pins** — an outside repository holds the loop, so the pins stand on the tracked adapter, for the
reason the product-prover node above states. The adapter is the one place the pack updates when a
text-audit release moves the loop's own shape.
- `skills/text-audit-pack/SKILL.md:1` (frontmatter — what the adapter carries, what it does not)
- `skills/text-audit-pack/SKILL.md:30` (the mechanical lints this pack declares — the register-lint arm)
- `skills/text-audit-pack/SKILL.md:74` (what a cheap reader means run inside this pack)

**notes** —
- the tenth working skill, named in the pack's skill roster and the pipeline-roles glossary. Its cold-read comprehension loop is the mechanical-lints-then-panel discipline the format-laws requirements state. The loop's own body lives at github.com/happysasha18/text-audit, its own repository with its own version line; this node's home in the pack is the binding page.
- this node carries the working-skill roster's text-audit member without owning that anchor. The roster entity's home stays base-rulebook.
