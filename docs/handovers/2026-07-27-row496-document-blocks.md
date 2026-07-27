# Handover — the three fenced documents' blocks for ROADMAP row 496 (INV-291)

*Written 2026-07-27 by the build worker on row 496. PRODUCT_SPEC.md, PRODUCT_SPEC.index.md,
ARCHITECTURE.md and TEST_MATRIX.md were held open by another writer while this row was built, so the
worker wrote none of them. The blocks below are the exact text to apply; everything else in the row
already stands in the tree.*

## The order to apply them

1. Paste block 1 into PRODUCT_SPEC.md immediately before `## Reference`.
2. Replace the two ARCHITECTURE.md table rows (blocks 2 and 3) and the base-rulebook owns cell
   (block 5), and insert the paragraph (block 4).
3. Append block 6 to TEST_MATRIX.md's `### [node: base-rulebook]` block.
4. Regenerate the two generated tables:
   - `python3 scripts/build-index.py PRODUCT_SPEC.md -o PRODUCT_SPEC.index.md` and splice that same
     table under PRODUCT_SPEC.md's `## Reference` heading;
   - `python3 scripts/build-matrix-reference.py TEST_MATRIX.md -o <scratch file>` and splice it under
     TEST_MATRIX.md's `## Reference` heading.
5. Run `python3 -m pytest -q tests/test_config_surface.py` — the six document-home tests that stand
   red until these blocks land go green, and the file reads 21 passed.

## What was already validated against a merged copy

The spec block was merged into a scratch copy of PRODUCT_SPEC.md and passed
`check-requirement-shape.py` (1502 of 1502 criteria well-shaped across 299 requirements),
`check-criterion-readability.py` (every arm at its baseline, no new reading defect),
`check-vocabulary.py`, `check-weak-words.py`, `scripts/spec-style-lint.py` (0 errors), and
`check-size-ratchet.py` (204.8 bytes per criterion, under the recorded 207.2). The architecture block
was merged the same way and parsed by `guardrails/archformat.py`; the matrix row parses as five cells
with its level pinned, its never side present, and `INV-291` as its trailing anchor.

## 1. PRODUCT_SPEC.md — new Requirement 299

Insert immediately before the `## Reference` heading (after Requirement 298's last criterion),
then regenerate the Reference table and the committed index.

```markdown
---

## Requirement 299: A deployed kind declares what its owner changes without a build

**Context:** A project whose product is deployed carries a seam. On one side sits the build, holding the behaviour and the structure, everything that reaches production only by building the product again. On the other side sits the configuration: the values the shipped product already reads, which reach production by a deploy of configuration alone. The per-kind design principles named the visitor walk, the reachable flows, the register and the trigger, and said nothing about this seam, so a host could ship an experiment switch that costs a full build to turn off. The founding now names the seam once, and a check reads the host's own declaration.

**User Story:** As the owner of a deployed product, I want the switches, the copy and the thresholds I turn to live outside the build, so that a change of mine reaches production by a deploy of configuration alone.

### Acceptance Criteria

**Case: the seam is declared at founding**

1. *when* a project's product is deployed, the system *shall* record a `project.config-surface` line in the host profile naming what its owner changes without a build. [INV-291, INV-36]
2. The declaration *shall* name where those values live and how a change of them reaches production. [INV-291]
3. The system *shall* keep behaviour and structure in the code a build ships. [INV-291]
4. *when* nothing of a project is deployed, the system *shall* accept an explicit "none" as the founding's stated answer. [INV-291, INV-244]

**Case: which side of the seam a thing sits on**

5. The system *shall* place a value the shipped product already reads on the configuration side. [INV-291]
6. The system *shall* place a change that needs the code to do something it does not do today on the build side. [INV-291]
7. A value the product reads at build time *shall* sit on the build side until that reading moves to run time. [INV-291]

**Case: the check over the founding**

8. *when* a profile records `project.kind` and carries no `project.config-surface` record, a founding check *shall* red and *shall* name the missing line. [INV-291, INV-135, A-10]
9. *if* the declaration carries no words after its key, *then* the check *shall* red. [INV-291]
10. *if* a declaration answers "none" while the project's own `project.layers` line names a deployment layer, *then* the check *shall* red and *shall* quote both lines. [INV-291, INV-135]
11. The check *shall* read its keys and its word lists from `guardrails/config-surface.json`. [INV-291]
12. Each run *shall* state its reach: the two files it opens, and the three profile records it reads. [INV-269]
13. The check *shall* leave to the founding conversation and to the proof by deed whether a declared value truly reaches production with no build. [INV-291]

**Case: the per-kind table carries the principle**

14. The architecture document *shall* carry this principle in the per-kind design-principles table for every deployed kind, with both sides of the seam named. [INV-291, INV-136]
15. A kind whose product runs in no place its readers reach *shall* carry no such principle. [INV-291, INV-136]
```

## 2. ARCHITECTURE.md — the frontend / visual row, replaced whole

```
| frontend / visual (fullstack app · static site · photo portfolio) | the visitor walk (first visit · return · cross-entry · from-any-point navigation · exits) · the feel pass scaled to a whole site (motion quality, affordance craft against the prototype bar) · motion and scroll feel as the human's gate · **interactive controls that belong to different layers occupy separate screen space** (the interactive-overlap rule) · cross-surface policy uniformity [INV-125] · paired-transition symmetry [INV-126] · **a legibility floor** — text meets a minimum contrast ratio against its background and a minimum size (SPEC INV-139) · **the seam between the build and the configuration** — an experiment switch, a piece of copy, a threshold or budget, and a feature toggle reach production by a deploy of configuration alone, while behaviour and structure stay in the code the build ships (SPEC INV-291) | the walk and the feel pass are the human's eye-walk [INV-30, INV-77]; the interactive-overlap rule, the policy-uniformity and paired-transition rules each get a browser or pixel-level row in the adopting project's suite; the legibility floor is read at the verify feel pass (a product surface's computed colours/sizes) and at the pre-show gate (`scripts/preshow-legibility-lint.py` on the styled file), its browser-computed row living in the adopting project's suite; the build-and-configuration seam is declared at founding on the host's `project.config-surface` line and read by `guardrails/check-config-surface.py`, its proof by deed the owner turning a switch in production while no build runs |
```

## 3. ARCHITECTURE.md — the code / backend service row, replaced whole

```
| code / backend service | the promised flows all reachable · error and empty states answered · latency and error-rate budgets held · **the seam between the build and the configuration** — an experiment switch, a piece of copy, a threshold or budget, and a feature toggle reach production by a deploy of configuration alone, while behaviour and structure stay in the code the build ships (SPEC INV-291) | integration tests and the budget rows [INV-41]; the build-and-configuration seam is declared at founding on the host's `project.config-surface` line and read by `guardrails/check-config-surface.py`, its proof by deed the owner turning a flag or a budget in production while no build runs |
```

## 4. ARCHITECTURE.md — a new paragraph, placed after the interactive-overlap paragraph and before `## Composition axes by project.kind`

```markdown
**The seam between the build and the configuration** (SPEC INV-291) is the principle every deployed
kind carries, and a founding names it on the host's own `project.config-surface` line beside the
layers, the proofs, the design principles, and the axes [INV-135, INV-136, INV-244]. A kind is
deployed when its product runs where its readers reach it and reads values it did not have to be
rebuilt to receive: the static-site, fullstack, photo-portfolio, and backend kinds stand on that
side, while a book, a prose campaign, a CLI, and a skill pack stand off it — a CLI carries a
configuration file, and that file sits on the reader's machine, so its owner turns nothing in it
without a release the reader takes. A reader places one thing on one side of the seam by a single
question: does the shipped product already know how to behave once this value changes? A value the
running code already reads belongs to the configuration; a change that needs the code to do
something it does not do today belongs to the build; and a value the product reads at build time
stays on the build side until that reading moves to run time. `guardrails/check-config-surface.py`
reads the host profile and reports three things — a kind recorded with no declaration, a declaration
with no words after its key, and a "none" written beside a `project.layers` line that names a
deployment layer — and it carries no list of kinds, since which kinds are deployed is the judgment
this table states and a founding answers. Whether a declared value truly reaches production with no
build sits past a profile line's reach, so the founding conversation and the proof by deed hold that
half: the owner turns a switch in production, and no build runs.
```

## 5. ARCHITECTURE.md — the base-rulebook node's owns cell, replaced whole

```
**owns** — E-12, E-13, INV-5, INV-9, INV-11 (the fence fires before every write and every commit in every writing skill with no lane rolling at all), INV-13, INV-14, INV-23, INV-56, INV-65, INV-76, INV-84, INV-98, INV-108, T-19, INV-40, ACT-1, ACT-2, ACT-3 (the brief's isolated-tree clause likewise stays with the delegation law that states it), M-2, M-7, E-17, INV-105, INV-107, INV-117 (the session identity is minted by every session at its start and feeds both the pen tie-break and the inbox source-mark's projection), INV-135, INV-136, INV-139, INV-291, INV-143, INV-145, INV-152, INV-163, INV-217, E-31 (the state-directory anchor is one anchor carrying two unrelated facts, the canonical `.live-spec` directory and the worktree-isolation default that fires on two lanes' overlapping write-sets, so it sits here with its leading fact and its stated category while the lanes node owns the mechanism that default fires), INV-182, INV-183, INV-188, INV-189, INV-190, INV-191, INV-193, INV-194, INV-195, INV-196, INV-197, INV-225 (the sibling of the far-tier report-shape check), E-35, INV-240, T-24
```

## 6. TEST_MATRIX.md — new row M-467, appended at the end of the `### [node: base-rulebook]` block

```
| M-467 | A deployed kind's founding declares what its owner changes without a build (INV-291, ROADMAP row 496): beside its concrete layers and proofs [INV-135], its design principles [INV-136] and its composition axes [INV-244], a kind whose product runs where its readers reach it records a `project.config-surface` line in the host profile naming what the owner turns from outside a build (an experiment switch, a piece of copy, a threshold or budget, a feature toggle), where those values live, and how a change of them reaches production, while behaviour and structure stay in the code the build ships; `guardrails/check-config-surface.py` reads three records of the host profile and reds three cases — a recorded kind with no declaration, a declaration with no words after its key, and a "none" written beside a `project.layers` line that names a deployment layer — passes an explicit "none" from a project that deploys nothing, states its reach on the green line [INV-269], reads its keys and word lists from `guardrails/config-surface.json`, and rides the suite off the push chain [INV-225]; the per-kind design-principles table in ARCHITECTURE.md names both sides of the seam for every deployed kind and states which kinds are deployed, the founding-question set carries the question at set version 6 [INV-227] and adoption's orient records the answer; homes the spec clause and its Reference row + the per-kind design-principles table + base-rulebook's owns + the founding-question set + adoption's orient + the pack's own host profile; never a deployed kind's founding silent on the seam, never an explicit "none" mistaken for silence, never a "none" standing beside a declared deployment layer, never a value called deployable without a build on a profile line's word alone where only a deed can say [INV-291] | string | `test_deployed_host_declaring_its_surface_passes` + `test_kind_with_no_config_surface_line_reds` + `test_explicit_none_passes_for_a_project_that_deploys_nothing` + `test_none_against_a_declared_deployment_layer_reds` + `test_empty_declaration_reds` + `test_profile_with_no_kind_passes` + `test_missing_profile_reds` + `test_missing_config_reds` + `test_green_run_states_its_reach` + `test_live_host_profile_passes_the_check_it_ships` + `test_spec_states_the_law` + `test_spec_reference_row` + `test_architecture_names_the_seam_for_every_deployed_kind` + `test_architecture_states_which_kinds_are_deployed` + `test_architecture_owns_the_invariant` + `test_matrix_row_covers_the_law` + `test_founding_questions_names_the_config_surface_question` + `test_adopt_founding_prompts_the_config_surface` + `test_live_profile_declares_its_own_config_surface` (red-first at the test station, 2026-07-27: 20 of 20 red against the pre-delta tree — the check, its config, the founding question and every document home absent; the check's eleven arms went green with the gate and its config, the founding surfaces with the profile, the question set and adoption's orient, and the six document-home tests stayed red until the spec, architecture and matrix blocks landed) | *built* |
```
