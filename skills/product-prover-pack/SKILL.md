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
