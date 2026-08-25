# build-pipeline

**Set a project up on live-spec, and hold two gate procedures with no other home yet. A [Claude Code](https://claude.com/claude-code) skill, part of the live-spec pack.**

build-pipeline used to be the pack's pipeline orchestrator. That job now belongs to **director**: it reads what a person said, decides what the accepted work touches, and calls the specialists — spec-author, product-prover, architect, test-author — as the work needs them, in place of this skill's old fixed nine-step sequence. This skill keeps two things that still need a home: the **setup walk**, which attaches live-spec to a project, and the **MINOR-bump gate** procedure.

---

## Setting a project up

Say *"attach live-spec to this project"*, *"found a new project on live-spec"*, or *"update live-spec here"*, and this skill resolves the pack tree, reads the project tree, and runs the matching walk — attaching an existing project, founding a new one, or catching an existing install up to the current pack version. Once the walk finishes, the first wish enters through `director` like any other request.

## The MINOR-bump gate

Before a MINOR (0.x.0) version bump, this skill still holds the 3-pass preventive audit (the whole spec re-proven, a matrix audit, a surface-composition check), the full design review, the cross-cut counter, and code compaction as a station beside doc compaction — until Package 5 gives this gate its own permanent home.

---

## What's inside

No code, no dependencies — a `SKILL.md` plus two reference files, a structured set of instructions Claude follows. Drop it in alongside `director` and the rest of the live-spec pack.

## Usage

Part of the live-spec pack — see the pack's own README for install instructions. Once installed, just say what you want set up:

> *"attach live-spec to this project"* · *"found a new project on live-spec"* · *"update live-spec here"*

---

## License

[MIT](LICENSE) © Alexander Abramovich.
