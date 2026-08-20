# SKILL-REVIEW — build-pipeline, exact worker-restore acceptance

Skill: build-pipeline
Date: 2026-08-20
Range: 8d334a15..346388e4 (skill's own last change: `346388e4`)

## Scope read

Read the complete current `skills/build-pipeline/SKILL.md` and its changed
`references/verify-step-detail.md`, then traced their commands into
`guardrails/check-worker-restore.py` and the PreToolUse hook installer. The change replaces an
ambient time-window acceptance check with a single explicit worker-run verdict and explains the
fresh-brief recovery path.

## Skill-creator and cold-read checks

`python3 /Users/sashaabramovich/.codex/skills/.system/skill-creator/scripts/quick_validate.py
skills/build-pipeline` passed after the description field was made valid YAML. An independent
cold-read reviewed the workflow without editing. It found three blocking defects: option-bearing
`env`/`command`/`sudo` wrappers bypassed the parsers, equals-spelled ambient options accompanied
`--run`, and malformed settings could produce a partial installation. Each finding was corrected
before this record: both parsers recognise the ordinary wrapper forms, exact-run rejects the option
spellings, and installer preflight parses settings before any write. Focused evidence: 62 tests
passed after those corrections; the Packet A profile passed 206 tests.

## Readability verdict

The acceptance procedure is now recoverable from the skill alone: retain the exact
`agent-*.jsonl` path; run `check-worker-restore.py --run <path>` before acceptance; reject a red
result; create a fresh brief after recovery; accept only its fresh exact run. The original record
remains a forensic finding. The reference gives the same steps in detail without adding a second
policy or a time threshold.

Verdict: ALLOW — the changed skill is valid, comprehensible on a cold read, and its blocking review
findings are covered by tests and folded into the delivered implementation.

Follow-up: the gate-aa repair rewrote one existing all-caps instruction (`ANY` to `any`) and one
acceptance sentence that the style reader classified as a scissors construction. The exact-run
workflow and its commands did not change. This record ships with that readability correction and
continues to cover the current skill revision.
