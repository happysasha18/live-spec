# q-809 — session start-up weight, and every standing file

**Root:** his word 2026-09-02: "80кб много. можно удешевить? раза в 4?" and "зачем decision если
есть доска и journal? нам точно все файлы нужны?"

## Measured before

`scripts/state-probe.sh` line: required context (boot + profile + base + director) = 18501 tokens,
80122 bytes.

| file | before | after this pass |
|---|---|---|
| `~/.claude/CLAUDE.md` | 4386 | 4386 — untouched, he owns it ("CLAUDEmd не трогай, это другой пишут", 26.08) |
| `~/.claude/live-spec/profile.md` | 9680 | ~10600 — two of his new standing lines added, one dead script citation corrected |
| `skills/live-spec-base/SKILL.md` | 40443 | ~16500 |
| `skills/director/SKILL.md` | 25613 | 21900 |

Total ~53.4 KB, a third off. The quarter is not reached; the reason is director, below.

## Method

The pattern was already in the tree: live-spec-base keeps the glossary, the worked examples and the
settings ladder in `references/`, opened only when a question needs them. Extended to the rules —
the loaded body keeps one imperative sentence per rule plus its enforcement pointer and its SPEC
codes, and the citation, history, justification and worked example move to `references/rule-origins.md`.

## Steps

1. ✅ Per-rule inventory of the 22 shared rules — `.live-spec/checkpoints/q809-inventory-base.md`.
2. ✅ Same for director, profile, boot — `.live-spec/checkpoints/q809-inventory-director-profile.md`.
3. ✅ Standing-file census — `.live-spec/checkpoints/q809-standing-files-census.md`.
   Every standing document has a consumer that reads it by name. 34 dated one-off notes in
   `.live-spec/` (499 KB) are read by no script; 26 of them are cited by the prover review records
   under `docs/`, so removing them would leave a review pointing at nothing. The other 8 (36 KB)
   were removed in commit c6ffc709.
4. 🔄 Cut and repair.
   - live-spec-base body cut to one instruction per rule. Two rules were genuinely lost in that cut
     and restored by hand: rule 6's worker-liveness apparatus (worker id, briefed write-set, the
     liveness checks, the ~60 s heartbeat, INV-76, the leave-word extension INV-95) and rule 7's
     single PEN plus INV-49.
   - 44 tests went red. A lane is re-trimming `rule-origins.md` so it never restates an instruction
     (the pack's own rule 4 forbids two homes), restoring SPEC codes to the body, and reporting for
     each remaining red whether the body still carries the instruction.
   - `ARCHITECTURE.md` carries line-number pins into `live-spec-base/SKILL.md` that the shrink made
     stale. Sweep still owed, after the body settles.
5. 🔄 Director re-record — 35 scenarios, mandatory by `evals/director/README.md` whenever the skill
   changes. One fresh producer per scenario, holding only the skill text and one message, opaque
   labels so the scenario name cannot leak the answer. Verdicts land in the session scratchpad and
   are promoted with `promote.py` there.
6. ⬜ skill-creator over each skill touched.
7. ⬜ Re-measure with the same probe line; land the row.

## Why the quarter is not reached

Director's own body is now the largest of the four. Its weight is the act classification — the seven
acts and the disambiguation rules under them — which the eval already scores at 32 of 35. Cutting it
without a recorded run is cutting the pack's front door blind. The re-record in step 5 is what says
whether a shorter classification text holds; the answer decides whether the quarter is reachable.

## His words this session, carried into the work

- Blocked and reopened are two states. Done, commit 37c40c7e, then extended: a reopened row now
  takes its own mark 🔁, and that goes into the spec (a lane is writing it).
- Done tasks are not counted by default; the count that matters is the open work.
- The row's own name comes before its text in every report line.
- Up to 10 lanes in parallel, each with its own worktree and a clean merge; sonnet workers by
  default. Both recorded in the profile.
