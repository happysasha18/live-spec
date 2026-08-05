# Skill review — the audit says that a repair writes text nobody has read

SKILL-REVIEW

Skills: text-audit.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes. The change adds one paragraph to step 5. It removes no instruction, and it makes an
existing instruction carry the reason it exists.

## What changed

Step 5 already said the loop closes on two consecutive rounds returning nothing that blocks. It gave
no reason, so a run that stopped after one round looked finished.

The step now says why the second round exists. Both readers of round one meet the text as it stood
before the fixes. Whatever the repair writes is unread. A definition written to close a finding
carries claims of its own, and nothing has checked them.

## The evidence behind it

On 2026-08-05 the shared rulebook was audited and repaired. A separate skill-creator review then found
four defects inside the repair's own new sections. One was a claim that every path in the file
resolves inside this repository, which is false for every host document the file names.

Neither cold reader could have caught those. Neither ever saw those sentences.

The same shape appeared on three other repairs the same day. Each closed round one and shipped without
round two, so in each case the repaired text went out unread.

## What the review looked at

**Does this change what anyone does?** It changes what a session may call finished. A run that stops
after round one now records the audit as open and says so in the reading record. The closing
condition itself is unchanged.

**Could it be read as permission to skip round one?** No. The paragraph rests on round one having
happened, since it describes what round one could not see.

**Does it contradict anything else in the file?** The loop's opening line and step 5 both state the
two-round condition, and they agree. The by-hand section already tells a run with no reader available
to say so in the record rather than counting the text as read, and this paragraph applies the same
discipline to a run that stops early.

## Findings

None blocking.

One observation. This paragraph asks a session to record an audit as open, and nothing mechanical
reads that record. A document whose findings fell without a second round is invisible to every check
in the tree. The findings record at `guardrails/rule-census.json` holds counts alone, so it cannot
tell a closed audit from a stopped one. Worth a queue row.

## Checks run

`python3 scripts/rule-census.py skills/text-audit/SKILL.md` — 0 findings, longest sentence 25 words,
holding the zero ceiling this file already carried.

`python3 scripts/preshow-register-lint.py skills/text-audit/SKILL.md` — exit 0.

`python3 -m pytest tests/test_config_health.py -q` — the repository copy and the installed copy hold
the same bytes.
