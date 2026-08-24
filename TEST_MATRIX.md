# live-spec — Test Matrix

Derived from PRODUCT_SPEC.md through the proven ARCHITECTURE.md. The package version has one home, the
VERSION file, never pinned here where it would read stale. Last reconciled with the spec: 2026-07-23.
This is the test-matrix member of the format family, written in the requirements genre the family
defines; the shared laws live once in `docs/spec-format.md` and the matrix's own additions in
`docs/test-matrix-format.md`, both inherited here by reference.

**What this document covers.** For each fact the spec states, which test holds it, pinned at which
level, and whether that test exists yet. Three parts follow: the artifact inventory (every file the
reader receives, each asserted at the rendered level), the matrix rows grouped into node blocks, and
the generated `## Reference` mapping each spec anchor to the rows that cover it.

**The bracket codes.** A code anchor — `[INV-x]`, `[T-x]`, `[E-x]`, `[M-x]` — trails at the end of a
row's fact sentence and points to the rule's home in PRODUCT_SPEC.md; the anchor is the row's parent
fact, and the generated Reference reads each row's coverage from it. A reader can ignore the anchors; a
maintainer follows them. A bare pointer like (row 386) or (ROADMAP 388) cites a queue row in
ROADMAP.md — the movement that carried the work. Short codes M-1..M-7 are the spec's milestone
anchors; a matrix row id always writes three digits (M-001..).

**How the keywords read.** The keywords *when*, *while*, *if*, *then*, and *shall* are set in lowercase
italics, and no word stands in all capitals outside a code anchor.

**Test levels, adapted to a text product.** live-spec ships documents and skills, no browser surface,
so the ladder's rungs read differently here than on a rendered product. The document uses three levels
of the ladder today: `string` (the bulk — a `string` assertion against the shipped file on disk, never
a source fragment or a memory of it), `DOM-text` (the rendered-card assertions), and `browser-computed`
(facts a real engine must compute). Each row pins its own level in its Test level cell, and the level
column is the one source of which row sits where. The rung names are the family's, kept for parity
across projects, and each project fills them with its own real engine: here the `browser-computed`
rung holds the facts a real git must compute on a live repository, and `DOM-text` holds the rendered
onboarding cards.

**Status vocabulary.** *built* (the test exists and runs green) · *todo* (the owner named in the row) ·
*retired* (the row is kept, never deleted).

---

## Artifact inventory

Every file a host (or this flagship repo's reader) receives, each asserted at the project's rendered
level — for this text product, the shipped file on disk. Each entry is checked shipped-and-non-empty
by `test_artifact_inventory` — the test parses this table, so adding an entry auto-extends the check.

| Artifact | Path | Type | Owning test |
|---|---|---|---|
| Base rulebook skill | `skills/live-spec-base/SKILL.md` | shipped text | `test_artifact_inventory` |
| Spec-author skill | `skills/spec-author/SKILL.md` | shipped text | `test_artifact_inventory` |
| Product-prover skill | `skills/product-prover/SKILL.md` | shipped text | `test_artifact_inventory` |
| Build-pipeline skill | `skills/build-pipeline/SKILL.md` | shipped text | `test_artifact_inventory` |
| Communicator skill | `skills/communicator/SKILL.md` | shipped text | `test_artifact_inventory` |
| Spec template | `templates/PRODUCT_SPEC.template.md` | shipped text | `test_artifact_inventory` |
| Architecture template | `templates/ARCHITECTURE.template.md` | shipped text | `test_artifact_inventory` |
| Matrix template | `templates/TEST_MATRIX.template.md` | shipped text | `test_artifact_inventory` |
| Roadmap template | `templates/ROADMAP.template.md` | shipped text | `test_artifact_inventory` |
| Agent card template | `templates/agent.template.md` | shipped text | `test_artifact_inventory` |
| Journal template | `templates/JOURNAL.template.md` | shipped text | `test_artifact_inventory` |
| Next-steps template | `templates/NEXT_STEPS.template.md` | shipped text | `test_artifact_inventory` |
| Profile template | `templates/profile.template.md` | shipped text | `test_artifact_inventory` |
| Problem-ledger template | `templates/PROBLEMS.template.md` | shipped text | `test_artifact_inventory` + `test_problems_template_shape` |
| Kill-list template | `templates/KILL_LIST.template.md` | shipped text | `test_artifact_inventory` + `test_kill_list_mechanical` |
| Bootstrap suite scaffold | `templates/test_scaffold.template.py` | shipped script | `test_artifact_inventory` + `test_scaffold_bootstrap_runs` (real simulated bootstrap, both ways) |
| Dev-machine skill sync | `scripts/sync-skills.sh` | shipped script | `test_artifact_inventory` + `test_sync_skills_script` (real run, twice) |
| Adoption procedure | `adopt/ADOPT.md` | shipped text | `test_artifact_inventory` |
| Founding procedure | `adopt/START.md` | shipped text | `test_artifact_inventory` + `test_a_founding_resolves_the_pack_and_reaches_the_first_green` (a real founding on a throwaway tree) |
| Setup routing card | `skills/build-pipeline/references/project-setup.md` | shipped text | `test_artifact_inventory` |
| Installer | `install.sh` | shipped script | `test_artifact_inventory` |
| Migration note (rename) | `MIGRATION.md` | shipped text | `test_artifact_inventory` |
| Front door | `README.md` | shipped text | `test_artifact_inventory` |
| The one-page map | `OVERVIEW.md` | shipped text | `test_artifact_inventory` |
| Plugin manifest | `.claude-plugin/plugin.json` | shipped config | `test_artifact_inventory` |
| Plugin marketplace ref | `.claude-plugin/marketplace.json` | shipped config | `test_artifact_inventory` |
| Plugin icon | `.claude-plugin/icon.png` | shipped image | `test_artifact_inventory` |
| Doc renderer | `scripts/render-doc.py` | shipped script | `test_artifact_inventory`, `test_render_doc_smoke` |
| Base skill README | `skills/live-spec-base/README.md` | shipped text | `test_artifact_inventory` |
| Base skill license | `skills/live-spec-base/LICENSE` | legal | `test_artifact_inventory` |
| Spec-author README | `skills/spec-author/README.md` | shipped text | `test_artifact_inventory` |
| Spec-author license | `skills/spec-author/LICENSE` | legal | `test_artifact_inventory` |
| Product-prover README | `skills/product-prover/README.md` | shipped text | `test_artifact_inventory` |
| Product-prover license | `skills/product-prover/LICENSE` | legal | `test_artifact_inventory` |
| Test-author README | `skills/test-author/README.md` | shipped text | `test_artifact_inventory` |
| Test-author license | `skills/test-author/LICENSE` | legal | `test_artifact_inventory` |
| Feedback-intake README | `skills/feedback-intake/README.md` | shipped text | `test_artifact_inventory` |
| Feedback-intake license | `skills/feedback-intake/LICENSE` | legal | `test_artifact_inventory` |
| Feedback-collector README | `skills/feedback-collector/README.md` | shipped text | `test_artifact_inventory` |
| Feedback-collector license | `skills/feedback-collector/LICENSE` | legal | `test_artifact_inventory` |
| Build-pipeline README | `skills/build-pipeline/README.md` | shipped text | `test_artifact_inventory` |
| Build-pipeline license | `skills/build-pipeline/LICENSE` | legal | `test_artifact_inventory` |
| Communicator README | `skills/communicator/README.md` | shipped text | `test_artifact_inventory` |
| Communicator license | `skills/communicator/LICENSE` | legal | `test_artifact_inventory` |
| Inbox door + law | `inbox/README.md` | shipped text | `test_artifact_inventory` |
| Guardrails scaffold text | `scaffold/guardrails/README.md` | shipped text | `test_artifact_inventory` |
| CI mirror workflow | `.github/workflows/gates.yml` | shipped config | `test_artifact_inventory` + `TestCIMirror` |
| The pack's own spec | `PRODUCT_SPEC.md` | flagship doc | `test_artifact_inventory` |
| The pack's own architecture | `ARCHITECTURE.md` | flagship doc | `test_artifact_inventory` |
| The pack's own matrix | `TEST_MATRIX.md` | flagship doc | `test_artifact_inventory` |
| The queue | `ROADMAP.md` | flagship doc | `test_artifact_inventory` |
| The journal | `JOURNAL.md` | flagship doc | `test_artifact_inventory` |
| The resume file | `NEXT_STEPS.md` | flagship doc | `test_artifact_inventory` |
| Package version | `VERSION` | version home | `test_artifact_inventory` |
| Host profile (dogfood) | `.live-spec/profile.md` | settings instance | `test_artifact_inventory` |
| License | `LICENSE` | legal | `test_artifact_inventory` |
| Prover records | `docs/prover/` | records dir (non-empty) | `test_artifact_inventory` |
| Guardrails (pack gates + fence) | `guardrails/` | scripts dir (non-empty) | `test_artifact_inventory` |
| Decision archives | `docs/decisions/` | records dir (non-empty) | `test_artifact_inventory` |
| Research reports | `docs/research/` | records dir (non-empty) | `test_artifact_inventory` |
| Queue archives | `docs/queue-archive/` | records dir (non-empty) | `test_artifact_inventory` |
| Audit records | `docs/audit/` | records dir (non-empty) | `test_artifact_inventory` |
| Prior-art survey | `docs/prior-art.md` | shipped text | `test_artifact_inventory` |
| Adoption guide | `docs/adoption.md` | shipped text | `test_artifact_inventory` |
| Pair adoption guide | `docs/pair-adoption.md` | shipped text | `test_artifact_inventory` |
| Architecture method | `docs/architecture-method.md` | shipped text | `test_artifact_inventory` |
| Onboarding and settings | `docs/onboarding-and-settings.md` | shipped text | `test_artifact_inventory` |
| Pipeline walk | `docs/pipeline.md` | shipped text | `test_artifact_inventory` |
| Push law | `docs/push-law.md` | shipped text | `test_artifact_inventory` |
| Test method | `docs/test-method.md` | shipped text | `test_artifact_inventory` |
| Worker liveness | `docs/worker-liveness.md` | shipped text | `test_artifact_inventory` |
| Publish skill | `skills/publish/SKILL.md` | shipped text | `test_artifact_inventory` |
| Publish README | `skills/publish/README.md` | shipped text | `test_artifact_inventory` |
| Publish license | `skills/publish/LICENSE` | legal | `test_artifact_inventory` |
| Test-author skill | `skills/test-author/SKILL.md` | shipped text | `test_artifact_inventory` |
| Feedback-intake skill | `skills/feedback-intake/SKILL.md` | shipped text | `test_artifact_inventory` |
| Feedback-collector skill | `skills/feedback-collector/SKILL.md` | shipped text | `test_artifact_inventory` |
| Design-reviewer skill | `skills/design-reviewer/SKILL.md` | shipped text | `test_artifact_inventory` |
| Skill evals — method + honest boundary | `evals/README.md` | shipped text | `test_artifact_inventory`, `test_eval_readme_states_honest_boundary` |
| Skill evals — one per working skill | `evals/` | shipped text dir | `test_skill_evals_present` (self-closing over skills/) |
| Eval run records | `docs/evals/` | records dir (non-empty) | `test_artifact_inventory` |
| Work board page — the frozen norm | `docs/norms/work-board.html` | rendered page | `test_artifact_inventory` + `test_norm_fingerprints` |

---

## Parts map

| Part | Rows | Topic |
|---|---|---|
| `matrix/base-rulebook.md` | 66 | shared working rules stated once + package defaults + the settings ladder |
| `matrix/spec-author.md` | 32 | authoring method for a living, use-case-first, prover-ready PRODUCT_SPEC.md |
| `matrix/product-prover.md` | 12 | formal review of spec and architecture; executes the push-gate re-check |
| `matrix/build-pipeline.md` | 79 | the wish lifecycle, walked station by station. The walk runs intake → classify → spec → prove → architecture → prove architecture. It then runs matrix → test → code → verify → commit & show → landed. |
| `matrix/parallel-lanes.md` | 18 | concurrent work on one repo. The pen serializes every shared-truth write. The cap and the graph pick the lane set. The lane's branch sits in its own worktree. The lane-open act opens each lane, and the integration lands it. |
| `matrix/publish.md` | 7 | the publish-quality gate: per-kind publication checklist (its one home) + the target-plugin seam; runs before the human's gate, never instead (row 98) |
| `matrix/skill-evals.md` | 2 | behaviour tests for the pack's own skills: per working skill one scenario, red proven bare, re-run at milestones (row 94) |
| `matrix/communicator.md` | 44 | the human-facing exchange. It carries reports, batched questions, decision pages, and done-claim answers. It also carries the capture echo and departures board, the feature map on demand, the pre-report walk, and working narration. |
| `matrix/templates.md` | 8 | the document shapes a host copies at bootstrap; the matrix's generated reference section |
| `matrix/attach.md` | 41 | attaching the pack to a host. That covers the adoption phases, the VCS gate, the attic, and the who-am-I-working-with step. It also covers the skill install, the version record, and the pack update check. The catch-up walk that brings an already-adopted host onto the current pack sits here too. |
| `matrix/inbox.md` | 14 | the parallel-safe intake door for wishes born outside a live-spec session. Its remote arm serves granted seats. Its stranger arm bridges Issues and Discussions into inbox files through a monitor. Two hosts on one repo converge on a single surfacing by a claim on the shared item. |
| `matrix/host-contract.md` | 4 | the recorded settings instances. Those are this host's profile, the human's personal profile, and the thin loader that boots the personal layer. The agent records sit here too: the self-declaring card in each agent's own tree, found by the pack's live scan. |
| `matrix/package-docs.md` | 16 | live-spec's own host instance (dogfood): spec, queue, journal, resume file, version, records, dev-machine skill sync, its own problem ledger |
| `matrix/guardrails.md` | 123 | mechanical pre-push checks + surface registry + CI mirror |
| `matrix/text-audit.md` | 1 | the audit-and-fix loop for human-facing texts. It runs the mechanical register lints first, then fresh zero-context cold reads. Each finding is fixed at its source until two consecutive reads come back clean. |
| `matrix/snapshot.md` | 3 | saved baseline of the last accepted run; declared-scope diff (ROADMAP row 55) |
| `matrix/design-sync.md` | 2 | an optional machine, [target: machine; wiring live]. A landing's declared components sync to the team's design project, human-gated (ROADMAP row 93). The machine's first real run remains. |
| `matrix/test-author.md` | 21 | the test method's one home. It derives TEST_MATRIX.md from the proven spec through the proven architecture, and it writes the tests. Its parts are the level ladder, real-artifact assertions, red-first proof, the pinned skip-set, and traceability as a standing test (row 163). |
| `matrix/feedback-intake.md` | 3 | the intake half of the exchange. It receives anything handed back through three channels and routes each item to the home its law owns. It keeps the feedback ledger's shape and echoes every arrival (row 47). |
| `matrix/feedback-collector.md` | 4 | the outbound feedback arm, the pack's third arrow. On a rare genuinely-strong reaction it offers, with the human's positive consent, to draft a distilled non-public upstream note to the pack's authors. It deposits that note in the gitignored `outbox/` and sends nothing, so delivery stays the human's own step. It is off by default, under the `feedback-upstream` flag. It stands apart from feedback-intake, the inverse arrow, and from the measurement family (ROADMAP row 321). |
| `matrix/onboarding-card.md` | 8 | the settings card. A build-time renderer parses the base's package-defaults table and the profile files into the card page, per the frozen norm. The card is shown at the end of founding or adoption, and on the standing "what can I customize?" question (F-onboarding). |
| `matrix/design-reviewer.md` | 7 | the design-review pass |
| `matrix/work-board.md` | 26 | the standing page that shows the whole queue as columns of cards, the work in hand among them. It carries four parts. The page itself. The one source file in the host's tree, holding each task's statement, its validation record, and the craft set. The generator that renders that file with the queue into the page. And the statement-validation check a task passes before it enters work (F-work-board, ROADMAP row 166). |
