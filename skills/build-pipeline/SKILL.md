---
name: build-pipeline
description: >-
  Use to set a project up on live-spec, where it reads the tree, picks the setup walk, and runs it. Spoken: attach live-spec to this project, adopt or install live-spec here, onboard this codebase onto live-spec, found a new project on live-spec, update live-spec here. Not the pipeline's entry point for an accepted change — `director` is — and retained only for the setup walk and the MINOR-bump gate procedure until Packages 5 and 6 give each its own home.
metadata:
  version: 6.1.0
---

# build-pipeline — setup walk and the MINOR-bump gate

> Part of the **live-spec pack**. The shared working rules, the settings ladder, and the pack's
> glossary live in `live-spec-base` (v6.1.0). This skill does not restate them. Loaded alone, every
> section below still runs.

**This skill is no longer the pipeline's entry point.** `skills/director/SKILL.md` reads what a
person said, decides what the accepted work touches, and calls the specialists it needs — its
dynamic graph of acts and dimensions replaces this skill's former fixed nine-step sequence, door
table, work-kind table, footprint scale, and request-kind table. This page keeps only the two
pieces of real, still-needed craft that have nowhere else to live yet.

## The craft ladder — which craft's standards judge each step (SPEC INV-33)

Each artifact is judged by its own craft's standards. The **spec** is judged as a strong product
manager judges it: the user's journey, the product's words. **Prove** and **prove architecture**
are judged as the prover's formal-methods reviewer judges them. The **architecture** is judged as
a software architect judges it: nodes, seams, one responsibility each. The **matrix** is judged as
a QA automation lead deriving coverage. The **test** is judged as the same QA engineer writing it.
The **code** is judged as a senior developer. **Verify** is judged by the visitor's own fresh eyes,
the builder's own view set aside. **Commit & show** is judged as a careful release manager whose
reader is the human.

The craft takes the work-kind's form (SPEC INV-22, INV-33). On a prose product the code step is
worked as a strong writer. On infra it is worked as a toolsmith. The ladder names the archetypes,
and the kind says what their standards look like in its medium.

## Setting a project up on the pack

A session that hears "attach live-spec to this project", "found a new project on live-spec", or
"update live-spec here" runs a setup walk first. Read
[references/project-setup.md](references/project-setup.md), the routing card beside this page. It
resolves the pack tree, reads the project tree, and names the walk this project takes. The setup
entry stands outside the derivation chain. When the walk finishes, the first wish enters through
`director` like any other request.

## Gates worth remembering

- **Before a MINOR (0.x.0) bump:** see
  [references/minor-bump-gate.md](references/minor-bump-gate.md) for the full gate procedure — the
  3-pass preventive audit, the full design review, the cross-cut counter, code compaction as a
  station beside doc compaction, and the skill-creator craft review — until Package 5 gives this
  gate its own permanent home.

## How it relates to the other skills

- `director` (`skills/director/SKILL.md`) — the pipeline's entry point. Reads the human's message,
  decides what accepted work touches, and calls `spec-author`, `product-prover` (+
  `design-reviewer`), `architect`, and `test-author` as the work needs them.
- `live-spec-base` — the shared rulebook, the settings ladder, and the glossary every term on this
  page resolves against.

## Work that belongs elsewhere

An accepted change of any kind — spec, architecture, matrix, test, code — routes through
`director`, not here. This skill runs only at two moments: setting a project up on the pack, and
the MINOR-bump gate procedure. Everything this page once carried beyond those two — the door, the
work-kind table, the footprint scale, the request-kind table, the fixed nine-step sequence — is
`director`'s job now.
