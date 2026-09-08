# Skill review — product-prover-pack

SKILL-REVIEW

Skill: product-prover-pack

Date: 2026-09-08
Reviewer: skill-creator (Anthropic)

Verdict: passes; the two new sections were reviewed as an addition to a binding page that reviews
nothing itself, and the page's own scope is unchanged.

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/product-prover-pack
Skill is valid!
(exit 0)
```

## What changed

Two sections, "Closure review" and "Global review", state the reach of a push review and what it may
block on: closure reads the accepted row alone and blocks on material failure, sending anything else
it notices to one deposit under `inbox/`; global is owed by the owner's request naming a critical
scope or by a row touching a critical cross-cutting surface, names that scope on the record, and
hunts reproducible material failure of that surface. Row q-827, the owner's word of 2026-09-08 21:25
and 21:26.

## Findings

- The page's description line and its `## Mode names` table were left alone. The four names there
  are the machine names the build pipeline passes to the prover; the two new modes are the reach a
  push review runs under, which is a different axis. Folding them into the same table would have
  read as a six-name list where a caller picks one, which is what the page does not mean. Folded as
  written: two sections, the table untouched.
- The sections carry the incident that produced them — four adversarial reads of one forty-line
  change in a single evening — because a reach rule with no incident behind it reads as a
  preference, and the next reader widens it back. Folded.
- Nothing about the modes lives only here: the record's own shape carries the `Mode:` line in
  `docs/prover/README.md`, and `guardrails/check-prover-record.sh` reads that field and refuses a
  global record naming no scope. A rule stated in a skill body alone would have been prose nobody
  runs. Folded, as the change under review.
- The page still reviews nothing itself and says so in its own first line, which the addition does
  not weaken: both sections state what a review's reach is, never how to run one. No finding.
