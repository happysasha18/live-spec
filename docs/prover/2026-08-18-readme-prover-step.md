# Prover record — 2026-08-18 readme-prover-step

PUSH-REVIEW

Range: 72f27fb5..a759db3f
- a759db3f The record carries the front door's missing line
- 221308c README: Step 1 (clone road) installs product-prover too
Files read: README.md, install.sh, scripts/install-external-skills.sh, skills/product-prover-pack/SKILL.md
Findings: the front door's first step left a stranger without the reviewer the pack pins a version of — the detail is below
Blocking: none

Step 1 brings the prover, so a stranger who follows the page ends up with a working pack.

Root: the rehearsal of tonight's walk followed README's first step literally and ended with
ten skills and no reviewer. `install.sh` deliberately skips any skill directory carrying its
own `.git`, and `product-prover` only ever exists as such a clone, made by
`scripts/install-external-skills.sh` — a script named only far below the fold. The prover
pack pins a version floor of that skill, so the walk would have reached the proving step and
stopped there, in front of the owner.

What happened: README's first step gains that script as its third command, with one plain
sentence saying what it brings. Two nearby claims that the install is "two lines" are
corrected, since they were true only before. Nothing in the machinery moved: the installer,
its version floor and its use in CI are untouched, and the `.git`-skip policy stands.

Checks run: proved by walking it, not by reading it. A clean sandbox HOME and a fresh clone
of this tree, then the three README lines run literally: after `./install.sh` alone
`product-prover` is absent, which reproduces the defect; after
`scripts/install-external-skills.sh` it stands at 1.3.0, which clears the pack's floor of
1.3.0. Re-running both commands is idempotent. Targeted tests: 233 passed, 2 skipped;
`check-tree-counts` and the register lint green.

Findings:
- A page can be false without a false sentence in it. Every line of that step was true; what
  was missing was a line. The rehearsal found it because it obeyed the page instead of
  knowing the product.
- Two stumbles remain from the same rehearsal and are not in this package: `install.sh` has
  no way to override HOME, and the plugin road likely shares this gap with no equivalent
  script to close it.

Blocking:
- none.
