# Skill review — director, shadow mode ends, the skill acts

SKILL-REVIEW

Skill: director

Date: 2026-08-24

## Who reviewed it, and over what

An agent that did not write the file, given the file, the package's requirements and its
prohibitions, and told to break it rather than approve it — the same brief as the
2026-08-21 shadow-mode review, calibrated to match its rigor. This review covers two
commits, in two rounds, because the first round found a real blocker and nothing was
committed until it was fixed:

- `ad851b7d` — the substantive change: `skills/director/SKILL.md` goes from shadow mode
  (writes a decision sheet, does nothing else) to acting (checkpoint, brief, replan,
  independent verify, close), and `skills/director/references/verify-step-detail.md` is
  added, extracted from `build-pipeline`'s copy. `OVERVIEW.md`, `PRODUCT_SPEC.md`,
  `docs/director/capability-map.md` and `JOURNAL.md` change alongside it (glossary wording
  and status notes, not skill instructions).
- `9dec33f1` — the fix for this review's own round-one finding: `scripts/checkpoint.py`
  gains `update_checkpoint`, and `skills/director/SKILL.md`'s Execution section is revised
  to use it.

## Round one — a real blocker, reported rather than fixed

Read cold: `docs/skill-review/2026-08-21-director-shadow.md`, `docs/skill-review/README.md`,
the whole of `SKILL.md` at `ad851b7d` (not just the diff), both copies of
`verify-step-detail.md` side by side, `scripts/checkpoint.py`, and
`tests/test_checkpoint_mechanism.py`.

**The finding.** The seven-acts table's **Decision** and **Correction** rows both forbid
opening a second, duplicate tracking record for work already in flight — Decision's "must
not" column reads "open a second task duplicating work already under way," Correction's
reads "open a new task alongside the old one," and the prose at "A correction attaches to
work, not to a queue" says the same thing a third way: "find that work and change it...
Never answer a correction by creating a second row that contradicts the first." But
Execution's first bullet unconditionally ran `python3 scripts/checkpoint.py new <path>
...` for any work that had just earned a decision sheet, including a correction — and
`new_checkpoint` had exactly one behaviour: overwrite the whole file with a blank
template, no exists-check. This was verified live, not inferred: running `checkpoint.py
new` a second time against a path that already held real `DONE` content silently
overwrote it back to `(nothing yet)`, exit 0, no warning. So a correction to work already
in flight, followed literally, either destroyed the evidence of work already done (same
path) or created the forbidden duplicate (a different path) — both outcomes the file
elsewhere calls out as wrong, and Execution offered no branch for which case applied.
`Decision` also happened to be missing from Execution's own applicability list (`"an
instruction, a correction, or the settled half of a conditional"`), asymmetrically, even
though the decision-sheet section already implies by elimination — the no-sheet list is
question/idea/observation/halt, four of seven — that a Decision earns one too.

This was reported back in full rather than fixed by this reviewer, per the process; no
record was written or committed for that round.

## Round two — the fix, verified against the live CLI

`9dec33f1` was read in full (`git show 9dec33f1`, both files). `scripts/checkpoint.py`
gains `update_checkpoint(path, done=, in_progress=, next=, decision_sheet=)`, which reads
the existing checkpoint, replaces only the named section bodies, and writes back through a
new shared `_serialize_checkpoint` helper that `new_checkpoint` was also refactored onto —
confirmed byte-identical output for `new_checkpoint` isn't just asserted: the refactor is a
mechanical extraction (the same literal lines moved into a helper both writers call), and
all 16 pre-existing tests are still present unchanged in the diff. `update_checkpoint`
raises on a closed checkpoint, on an all-`None` call, and on a `decision_sheet` given to a
non-director-owned checkpoint. A `update` CLI subcommand was added with `--done`,
`--in-progress`, `--next`, `--decision-sheet`, matching the function's parameters.

`SKILL.md`'s Execution section now branches explicitly: "New work opens a checkpoint
before the first specialist is called; work already in flight updates the one it already
has — never a second `new` on the same work," followed by exactly which case is which
("An instruction naming a goal nothing already covers opens a fresh checkpoint... A
correction, or a decision that changes work already running, targets a checkpoint that
already exists — it never runs `new` again on that path, which would either silently
overwrite the existing DONE section... or, at a different path, open the duplicate this
file elsewhere forbids"), and the "new fact can change the graph" bullet now names the
concrete `update --next` command instead of the vaguer "rewrite the checkpoint's NEXT
section." `"a decision"` was added to the applicability list at line 212.

**Checks run, live, not just read:**

- `python3 -m pytest tests/test_checkpoint_mechanism.py -q` (backgrounded per the hard
  rule on this command) — `23 passed in 0.28s`, up from 16; the 7 new tests include the
  exact regression this review demonstrated (`test_update_never_clobbers_unrelated_
  completed_work`: seed real `DONE` content via `update`, update an unrelated section,
  confirm `DONE` survives byte-for-byte).
- Reconstructed the exact scenario by hand against the real CLI, not the test suite:
  opened a director checkpoint (`checkpoint.py new ... --decision-sheet "Goal: free-plan
  users can press export again..."`), seeded real `DONE`/`IN PROGRESS` content via
  `update` to simulate a worker's report landing, then ran the command Execution's revised
  prose actually specifies for a correction (`update <path> --decision-sheet "<revised>"
  --next "<...>"`). Result: `DONE` and `IN PROGRESS` byte-identical before and after, only
  `NEXT` and `DECISION SHEET` changed, one file throughout, `validate` clean at every step.
- Confirmed `new_checkpoint` still overwrites a second time against the same path (its
  documented "start over" behaviour, unchanged and now correctly never invoked by the
  skill for a correction or decision) — this is intentional, not a residual bug; the fix
  is that Execution's prose no longer reaches for it in the case that used to break.
- Re-confirmed `close` still refuses over open `NEXT`/`IN PROGRESS` and succeeds once
  cleared (unrelated regression check, unaffected by this diff, still true).
- Grepped `SKILL.md` for every place the instruction/correction/decision triad is
  enumerated together: exactly one place (`## Execution`'s opening line), and it now
  correctly includes all three. The exclusion-side enumeration ("For a question, an idea,
  an observation or a halt there is no sheet") is unchanged, unaffected by this fix, and
  still consistent with it by elimination.

**New ambiguity check (explicitly asked for): does the branch leave "which command do I
run" undecidable in any real case?** The revised bullet presupposes the Director already
knows whether a checkpoint exists for this work and, if so, its path. That's not a new gap
this fix introduces — a Correction is defined, unchanged since 2026-08-21, as changing
"something already in flight," and locating that work ("find that work and change it") was
already a precondition of handling a correction at all, before this fix existed. Given
Execution opens a checkpoint for every accepted instruction "before the first specialist is
called," any work in flight has one by construction, discoverable the same way the
Director already has to find the work itself. The one edge this doesn't spell out — a
correction or decision arriving against work whose checkpoint predates this acting version,
or was opened outside Execution's own discipline — is a bootstrapping question, not a flaw
in this diff, and not distinguishable from "the pack is mid-migration," which the commit
message for `ad851b7d` already says out loud (`build-pipeline` not yet removed). Not
blocking; not recorded as a defect, since it isn't one this change created.

## Cold spot-check of the rest of the file

The diff between `ad851b7d` and `9dec33f1` touches only three of Execution's bullets;
everything else in `SKILL.md` — the seven-acts table, the four highlighted rules, "one turn,
several acts," the decision sheet section and its worked example, the specialists table,
"what the human hears back," "work that belongs elsewhere" — is untouched between the two
commits and was already read cold and reviewed adversarially across both `ad851b7d` (this
review's first pass, full file) and the shadow-mode predecessor. No new read of those
sections was warranted by a three-bullet diff, and none surfaced a reason to redo it.

Verdict: ALLOW — the round-one blocker was real, verified live against the actual CLI
rather than inferred from reading; the round-two fix closes it (also verified live, same
method, plus the new automated regression test), introduces no new duplicate-writer path,
and correctly completes the instruction/correction/decision symmetry that was
asymmetric before. Nothing else broke in the process: `new_checkpoint`'s existing
behaviour and all 16 of its prior tests are unchanged, and the file's untouched sections
were not disturbed.
