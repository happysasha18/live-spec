---
name: product-prover-pack
description: 'Pack-side bindings for the external product-prover skill inside the live-spec pack. It carries what the prover body no longer does: the pin map from this pack''s PRODUCT_SPEC requirement codes to prover lenses, the pack paths a review reads, the record home and shape the push gate checks, and the mode names the build pipeline uses. Load it whenever product-prover runs inside a live-spec project. It reviews nothing itself.'
metadata:
  version: 1.0.0
  requires: product-prover >= 1.3.0 (github.com/happysasha18/product-prover)
---

# Product Prover — pack bindings

The prover is an external skill with its own repository and version line. This page binds it to the
live-spec pack. A review run inside a live-spec project reads the prover's own SKILL.md first and
this page beside it. A review run anywhere else needs nothing from this page.

## Mode names

The build pipeline asks for a mode by machine name, and the prover answers to both name sets:

| Pipeline name | Prover name         |
| ------------- | ------------------- |
| `FULL`        | Full review         |
| `CROSS-LINK`  | New-surface review  |
| `FEATURE-FIT` | Feature-fit review  |

## Pack paths

Where the prover speaks of the reviewed project's documents, this pack keeps them at:

- surface registry — `SURFACES.md`
- the spec under review — `PRODUCT_SPEC.md`, its code index in `PRODUCT_SPEC.index.md`
- the architecture under review — `ARCHITECTURE.md`
- the build walk's stations — `docs/pipeline.md`
- lens histories — `docs/lenses.md`
- the queue — `ROADMAP.md`

`base rule n` names a numbered rule in `skills/live-spec-base/SKILL.md`. `P9` is the architecture
principle that every cross-cutting law owes a test row on each surface it governs, carried in
`skills/test-author/SKILL.md`.

## The record

A review inside this pack writes its record to `docs/prover/` as `YYYY-MM-DD-<slug>.md` and commits
it. `guardrails/check-prover-record.sh` is the gate that reads it; `docs/prover/README.md` holds the
shape. A record covering a push carries the `PUSH-REVIEW` marker and the fields `Range:`,
`Files read:`, `Checks run:`, `Findings:`, and `Blocking:`, each with a value. The record's opening
line names the prover version that ran, and the gate's freshness arms hold the record against the
last change to each guarded document.

A minor (`x.Y.0`) bump of this pack requires a `FULL` pass
(`skills/build-pipeline/references/minor-bump-gate.md`).

## Pin map

Each pack requirement below is carried by the named prover lens. The requirement's text lives in
`PRODUCT_SPEC.md`; the lens's mechanics live in the prover. When a lens moves or renames in a prover
release, this table is the one place the pack updates.

| Requirement | Prover home |
| ----------- | ----------- |
| INV-114 | How to write findings |
| INV-141 | Work that belongs elsewhere; Cross-surface policy uniformity |
| INV-30, INV-31, INV-72, INV-138 | Edge-condition completeness |
| INV-125 | Cross-surface policy uniformity |
| INV-126, INV-127, INV-165, INV-167 | Lifecycle |
| INV-72 | Unwritten seams; Interactive-overlap across layers; Edge-condition completeness |
| INV-136 | Interactive-overlap across layers |
| INV-128 | Three-source disagreement |
| INV-49 | False-serialization and over-broad independence edge |
| INV-244, INV-248 | Delivery separability along a declared axis |

## Version discipline

`scripts/install-external-skills.sh` installs the prover and refuses a version below the minimum in
this page's metadata. The installed copy under `skills/product-prover/` is not tracked by this
repository; the external repository is its only source of truth. Raising the minimum here is a pack
change and lands as one.

## The pack's lens bindings

This page is written against `live-spec-base` (v4.3.0). The bindings below are the pack-side review
duties a live-spec project adds to the external prover's own lenses. The prover's body states the
general method; each line here is the pack's concrete pin of one duty, read beside the body on every
review run inside a live-spec project.

- **Unwritten seams [INV-72].** For every surface the document places before a user, the review walks
  every other surface that can be present at the same time and asks what happens at the seam; a
  reachable situation with a blank answer is a finding. The reviewer reports the blank and invents no
  answer. The headline of this duty is the unwritten seam.
- **Entry symmetry (SPEC INV-50).** A conditionally-entered face with no deliberate re-entry path is a
  finding, and a written one-way counts as an answer.
- **Domain language on every user-facing surface.** The review holds every user-facing string to one
  bar: read them as the user would; a leaked internal word is a finding.
- **The architecture lens, six items.** Beside spec-fact ownership and named seams, the review checks
  that the quality budgets are stated with their instrumentation homes and watchers — each names its
  watcher — that the runtime view walks every promised flow, and that the placement view says where
  every node runs.
- **Unbacked surfaces and unlabelled sketches.** A surface no requirement backs, or a sketch shown
  without its label, is a finding; the stress families of questions in the prover's own reference run
  over each.
- **Gaps, never taste.** The review's output bar is: Report gaps. Taste is out of scope. What reads
  as a preference goes to the design reviewer or the human, never into a finding.
- **The norm lens.** An approved prototype cited as `norm: <path>` is the definition the build answers
  to; a plan contradicting its own artifact is a finding.
- **The record names its reviewer.** Every record closes naming the prover skill version it ran under,
  so a spec proven under an old lens set never keeps a silent green.
