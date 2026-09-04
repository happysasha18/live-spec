# Skill-creator review records

This directory is the home for skill-creator review records. When a push substantively changes a
skill under `skills/`, the push gate `guardrails/check-skill-review.sh` (gate s, SPEC INV-208) reds
unless a committed record here covers that change. Alexander asked for the blocking gate on
2026-07-17 ~18:26: the session kept forgetting to run Anthropic's skill-creator review after a skill
edit, so the habit became a machine.

A pure version-frontmatter stamp — the `version:` line and the `live-spec-base (vX.Y.Z)` reference
that `scripts/stamp-versions.py` rewrites at every version bump — is not a substantive change and
owes no review; the gate exempts it by construction.

## A record's minimal shape

Save one file per landing that changed a skill, dated, named for the skill(s) it covers:
`docs/skill-review/YYYY-MM-DD-<skill>.md`. It carries, at minimum:

- a standalone `SKILL-REVIEW` marker line (the self-declaration shape the gate reads);
- a `Skill: <name>` line for each skill reviewed (the directory name under `skills/`);
- a `Verdict:` line carrying the skill-creator review's outcome;
- a block quoting the validator's own output: a line naming the exact command run, then a fenced
  code block holding everything that command printed, closed by a line reading `(exit N)`.

The quoted block, in full:

````
## The tool's own verdict

```
$ python3 <path to quick_validate.py> skills/<name>
<everything that command printed>
(exit <N>)
```
````

Naming a record and a verdict never proves Anthropic's `skill-creator` produced it — a session can
write the marker, the name, and a verdict by hand. Quoting the tool's own printed output is what
closes that hole, the same way `docs/skill-review/2026-09-04-build-pipeline.md` and
`docs/skill-review/2026-09-04-product-prover-pack.md` already do. Where the validator is on the
machine, the gate runs it itself and reds if its real verdict disagrees with what the record
quotes, or if the validator reports the skill invalid, whatever the record quotes — a currently-
broken skill never passes on an old, honest quote. Where the validator is absent, that arm stands
down by name and the record's other checks — the marker, `Skill:`, `Verdict:`, and this quoted
block — still run.

Everything else — the findings, what was folded, what was rejected and why — is free prose beneath.
The template `templates/skill-review.template.md` is the starting form. The gate checks that a
committed record naming the changed skill, carrying the marker, a verdict, and this quoted block,
exists and is at least as new as the skill's last change; a stale earlier review does not cover a
later change.
