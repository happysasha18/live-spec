# `SKILL-REVIEW` — text-audit, the three corrections the review owed

Skill: text-audit. Date: 2026-08-05, 14:20. Parent record: `2026-08-05-text-audit.md`, which landed
as commit `1378b47`.

That review passed the skill and owed three corrections, and all three close in the one commit that
adds this file. The sentence citing `2026-08-05-audit-runs-two-readers.md` now says that record
quotes a per-document figure from an earlier draft, with no measurement standing behind it. Under
"What the pass costs", the figures 355, 222 and 57 are marked as this skill's own sums. The roughly
thirty passages both readers found are named there as counted twice. The multiplier now measures
the pair against the prompted reader's 227 stops, the baseline this change replaced, at about 1.56
times as many. The old-vs-new meaning check hands its work to the meaning-check reader, which holds
both drafts, and that bullet links `skills/text-audit/references/rewrite-meaning-check.md`.

Checks: `python3 scripts/rule-census.py` reads 0 findings on the skill body and on this record.
`python3 scripts/preshow-register-lint.py skills/text-audit/SKILL.md` is clean.
`python3 guardrails/check-one-name.py skills/text-audit/SKILL.md` passes over the body. The
repository copy and the installed copy match under `diff -q`.
