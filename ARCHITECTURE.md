# live-spec — Architecture

Derived from PRODUCT_SPEC.md. The package version has one home, the VERSION file, and is not pinned
here where it would read stale (row 265). A row number names the wish queue: an open row stands in
`ROADMAP.md`, and a closed one in the archive under `docs/queue-archive/`. Last reconciled with the spec: 2026-07-23.

This is how live-spec is built: the named nodes that the spec's facts live in. One node carries one name
and one responsibility — the one-surface-one-name rule, applied to structure. The dated record of every
architecture-lens prove lives at `docs/prover/architecture-prover-record.md`; this document states the
structure as it stands today. In the
field's vocabulary the nodes are the C4 model's building blocks and the arc42 building-block view (§5).
The seams below are their relationships. The runtime view is arc42's §6, and the placement view is its
deployment view (§7). The quality budgets are arc42 quality scenarios (§10).

The agent keeps this doc up to date by assignment. When a wish lands, its new facts go to the node that already
owns their kind, and the pin is refreshed. A fact with no home yet goes to the node that fits. A large or
surface-class wish updates the doc before the matrix is touched; a bug or small wish just cites the node it
lands in. An assignment changes no structure and triggers no re-prove. Only a new node or a new seam
does, and only then is the doc re-proved. The landing-by-landing history lives in JOURNAL.md; this doc
states the structure as it stands today. [E-14]

**What "pin" means here.** live-spec is a documentation-and-skills product: its shipped artifact is the
text. So a pin points to the `file:line` where a node's responsibility is stated or carried. A pin whose
line reads 1 names the file as a whole. Every pin
below comes from a grep or read actually run, never from memory. Two nodes carry a [target] mark in their
heading — specified, with some code still ahead. The same mark stands on an anchor, a pin, a
responsibility, or a table row, and it means the same thing there. A fully-target node keeps its pin
cell empty until its code lands (snapshot). A partly-live one pins what already ships, and leaves the
rest for the landing that follows (guardrails).

---

## The shape at a glance

live-spec is a skill pack: twelve working skills plus the one shared rulebook they all load, each of them
text a model reads. Templates, guardrails, and its own dogfood documents sit beside them in one repo.
Everything executes inside an agent session on the host machine.
The repo is the source of truth, and the installed copies under `~/.claude/skills/` are what a session
actually loads. Git hooks and CI re-run the same gates, and the human reads rendered pages in a
browser. No server, no runtime of its own.

## Parts map

| Part | Nodes | Topic |
|---|---|---|
| `architecture/rules-and-settings.md` | base-rulebook, host-contract, onboarding-card | shared rules stated once, the settings ladder, the recorded host/personal settings instances, and the rendered settings card |
| `architecture/authoring-and-review.md` | spec-author, product-prover, design-reviewer, text-audit | authoring the spec, formal spec/architecture review, the design-review pass, and the human-facing text audit loop |
| `architecture/pipeline-and-lanes.md` | build-pipeline, parallel-lanes | the wish lifecycle walked station by station, and concurrent work on one repo under the pen |
| `architecture/exchange.md` | communicator, work-board | the human-facing exchange, and the standing work-board page that shows the whole queue |
| `architecture/host-adoption.md` | attach, templates, package-docs | attaching the pack to a host, the document shapes a host copies at bootstrap, and live-spec's own dogfood host instance |
| `architecture/intake.md` | inbox, feedback-intake | the parallel-safe wish-intake door and the handed-in feedback intake, each routing items to their homes |
| `architecture/guardrails.md` | guardrails | mechanical pre-push checks, surface registry, and the CI mirror |
| `architecture/outward.md` | publish, design-sync, feedback-collector | the publish-quality gate, the optional design-sync machine, and the outbound feedback arm |
| `architecture/tests-and-baseline.md` | test-author, skill-evals, snapshot | the test method's one home, per-skill behaviour evals, and the saved baseline diff |
| `architecture/seams.md` | — | where two nodes meet: what crosses each seam and which side owns the format |
| `architecture/feature-coverage.md` | — | the feature layer mapped to the node(s) that implement each scenario and the test that exercises it |
| `architecture/runtime-and-placement.md` | — | how each promised flow walks through the nodes, and where everything runs |
| `architecture/by-project-kind.md` | — | the per-kind scaffold for footprint and proof, design principles, and composition axes |
| `architecture/quality-budgets.md` | — | what quality means for a skill pack, in numbers |
| `architecture/decisions.md` | — | the pack's decisions' homes, the coverage rule, and the boundary-health cross-cut counter |

## Nodes

Every spec fact is OWNED by exactly one node. A spec fact is a code anchored on a criterion in
PRODUCT_SPEC.md, located through the generated code-to-location table at `PRODUCT_SPEC.index.md`.
One split is deliberate. The wish walk `T-1..T-7` is one row of that table but two responsibilities:
the walk itself (T-1..T-6, build-pipeline) and the report step (T-7, communicator). Both sides are
named here and in the matrix.
