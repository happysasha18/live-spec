# live-spec — where the work stands

## LIVE STATE (2026-07-28) — one task: make the spec buildable from its own text

Follow `docs/plans/2026-07-28-top-level-readability.md`. Read that plan first. It holds the test the
work is measured by, the six groups of defects with all 43 rules, a real before-and-after example, the
order, the batch loop, the five checks per batch, and what to report after batch one.

The spec is read by the agent that builds from it. Measured 2026-07-27: a fresh agent given six
requirements implemented two from the text alone, left one with written-down questions, and did not
attempt three, which depend on lists and default values the text gives nowhere. Two of six is the number
this work moves.

Everything else in this project waits. Alexander's word, 2026-07-28 morning.

**The audit skill is finished, 2026-07-28 afternoon.** His direction that morning: every law lives in
the audit skill, and each law states a class of mistake with examples under it. The skill then applies
to a spec section. All four pieces stand:

- the skill prints all 41 human-prose rules out of the one rule file between markers;
- the rule against a coined word is wired into the model that reads chat by meaning;
- every law carries a recorded case, written text on the left and its repair on the right, taken from
  this project's own texts;
- the skill carries the section that runs it on a spec section: the working size of ten requirements,
  the lint that applies only there, the marks a rewrite leaves untouched, and the four checks that
  follow.

Both text skills were rewritten by the rules they hold a text to. The prover fell from 253 findings to
27, and it carries no sentence past the word cap. The audit skill fell from 53 to 36. What stands in
the prover is 25 findings from a checker reading a spec rule over a skill body (row 513), and 2 from a
heading that shouts in eleven skills (row 519). The records are
`docs/skill-review/2026-07-28-product-prover-prose.md` and
`docs/skill-review/2026-07-28-text-audit-cases-and-spec-section.md`.

Next: the ordered list of requirements, then batch one. The plan explains why no new script is built.

## How we got here

**2026-07-27, day.** The rules this project holds its own writing to were spread over 57 files, with 61
rules, nine of them stated twice with opposite verdicts. They now live in one file,
`guardrails/language-rules.json`, 55 rules today after seven duplicates were retired and two were opened 2026-07-28.
`scripts/gen-language-consumers.py` builds every page and every checker's rule text from that one file,
and `guardrails/check-language-rules.py` refuses any of them drifting from it.

**2026-07-27, night.** 93 acceptance criteria of `PRODUCT_SPEC.md` were rewritten by those rules.
Sentences past the word cap fell from 469 to 378, explanations inside a rule from 120 to 65, endings
with no verb from 147 to 123. Seven of the 93 rewrites lost meaning: the test suite caught three and an
independent read caught four. That ratio, one loss in thirteen, is why the plan runs five checks per
batch.

**2026-07-27, night, the part that produced nothing.** Nine readings by strangers were run on
`docs/language-defects.md`, an internal record shown to nobody. The count of places a reader got stuck
went 11, 8, 12, 6, 5, 5, 6, 5, 8 and never approached zero. Two causes: the text read was 340 lines, so
each repair opened a new snag somewhere else, and the measure counted sentence length while readers
were stopping on unexplained words. The plan fixes both by working 250 lines at a time and by measuring
what a fresh agent can build, which is the only honest count of an unexplained word.

**2026-07-28, morning.** All 106 live documents were measured: 5429 defects, of which 2286 are in the
top-level documents, 1712 in the skill bodies, and 1104 under `docs/`. The census is
`docs/audit/2026-07-28-rule-census.md` and its data is `guardrails/rule-census.json`. Readings on the
internal record page stopped.

## So that nothing breaks

**Several windows share this repository.** Stage files by name, never `git add -A`. Re-check `git log -1`
before writing. After accounting for a moved HEAD, re-arm the fence with `guardrails/fence-refresh.sh`.

**Never discard uncommitted work.** No session and no worker runs `git checkout -- <path>`,
`git checkout .`, `git restore` outside `--staged`, any `git stash` form, `git reset --hard/--merge/--keep`,
or `git clean -f/-x`. To put a file back, write back the bytes you read before changing it. This rule
broke four times and destroyed work twice.

**A green exit code is not a test result.** Write the suite's output to a file and read the printed count
of passes and failures: `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the last line.

**Re-baseline the frozen documents at each saved batch:**
`python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`

**Next free numbers**, so two lanes do not collide: requirement 302, INV-301, E-36, T-25, M-479, and
queue row 520.

## Standing word from Alexander

- Run a whole movement alone; save and publish on green without asking.
- Documents in plain English. Conversation in Russian, in ordinary words.
- Every gate runs. No exceptions.
- Before asking him anything, check whether an existing document already answers it. If it does, act and
  cite the document.
- Name every request as one-time or standing before acting on it, and say which it is.

## Parked until the one task is done

The queue rows stand in `ROADMAP.md`; nothing there is lost. The nearest are 510-518 and 484-493, opened
2026-07-27 and 2026-07-28. Carrying the document format to tlvphotos waits. The onboarding work waits.
The skill bodies, the reader docs, and the templates, which hold 3143 of the 5429 measured defects, wait
until the top-level documents are done.
