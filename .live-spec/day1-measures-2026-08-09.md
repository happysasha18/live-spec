# Starting measures — day 1 of the culling

Root: his order of 2026-08-08, 22:17, and the plan's day 1, which owes the starting values of
the four measures. Measured 2026-08-09, between 00:33 and 00:45, on commit `fb1e9d7`.

The plan names the four measures and leaves their commands unwritten. The commands below are
this seat's, and day 14 must re-run these same commands for the comparison to hold.

| # | measure | starting value | command |
|---|---|---:|---|
| 1 | how far a stranger's install gets | pending the delivery census | day 1 census, `.live-spec/day1-census-delivery.md` |
| 2 | rulebook a session reads before work | 73 645 bytes ≈ 18 400 tokens | `cat skills/live-spec-base/SKILL.md ~/.claude/live-spec/profile.md \| wc -c`, divided by four |
| 3 | full test run | 447.22 s, 2502 tests, all green | `python3 -m pytest -q` |
| 4 | checks before a publish | 31 | `grep -oE -- '-- gate [a-z]{1,2}:' guardrails/pre-push \| sort -u \| wc -l` |

## What each number covers

**Measure 2** counts the two files a session reads before it starts: the shared rules
`skills/live-spec-base/SKILL.md` at 66 577 bytes, and the personal profile at 7 068 bytes. A
token here is four bytes. The audit of 2026-08-08 states 45 000 tokens for this measure. That
figure covers a session that also loads a working skill, and the skill bodies together run to
410 599 bytes, near 102 600 tokens. Both numbers are recorded so the comparison at day 14 can
name which one it moves.

**Measure 3** was red before day 1 began and is green now. The run before the repair took
450.47 s with two failures. The green run took 447.22 s. Of that time, gate b's own inner run
of the whole suite carries a large share, and the first batch of the rule cut takes that cost
out.

**Measure 4** counts distinct gate letters that `guardrails/pre-push` announces. The count
matches the 31 the plan states.

## The day's first repair

The two red tests are green as of commit `fb1e9d7`. Their cause held three parts. Two feedback
files under `inbox/` carried no entry in the document record. `NEXT_STEPS.md` had been cleared
to zero findings earlier and had grown back to 19, so the rule that a cleared document stays
cleared fired. The second red test, `test_guardrails::TestGateB_Tests::test_real_content_passes`,
runs the whole suite inside itself and reported the same failure.

The repair entered the two feedback files into the record with `python3 scripts/rule-census.py
--json guardrails/rule-census.json`, and rewrote the live-state block of `NEXT_STEPS.md` in short
sentences. The record was compared row by row before and after: only the two new rows appeared,
and no document's finding count rose.
