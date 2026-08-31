# Prover record — 2026-08-31 the blocked list settles itself

PUSH-REVIEW

Range: 4881623..f53242d. Base commit `4881623`, the head `origin/main` carries after the merged run
went out earlier today. Reviewed commits: `f97da1c` and `f53242d`.

Prover version that ran: product-prover 1.4.2, under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

Three entries in `PLAN.md`'s blocked list were written as questions for the owner. His standing word
of 28.08 00:53, repeated on 31.08 12:12, was to carry the run through and ask him nothing, so those
three were parked against an instruction that had already answered them. This range settles all
three, moves one rule up into the plan's own rules, turns the last entry that was work rather than a
question into a board task, and repoints one stale filename in this project's boot file.

## How this review was run

Read to refuse, by the session that made the change, over a range small enough to read whole. What a
document change can get wrong is a claim it has no ground for and a pointer that resolves to
nothing, so both were checked directly rather than argued.

Files read: `PLAN.md`, `CLAUDE.md`, `~/.claude/live-spec/profile.md`,
`skills/spec-author/SKILL.md`, `skills/spec-author/references/glossary.md`,
`skills/design-reviewer/SKILL.md`, `skills/director/SKILL.md`,
`skills/communicator/references/words.md`, `skills/live-spec-base/SKILL.md`,
`skills/live-spec-base/references/glossary.md`, `skills/product-prover-pack/SKILL.md`,
`templates/ROADMAP.template.md`, `adopt/ADOPT.md`, `adopt/START.md`.

Checks run: seven, each with its result.

1. The authority this range rests on, read at its source rather than recalled:
   `~/.claude/live-spec/profile.md` line 7 states the resolution order as his live word, then the
   host profile, then this file, then the package defaults. The settled entry cites that order and
   the two dates it rests on.
2. `bash scripts/state-probe.sh` and `bash scripts/render-board.sh` — the new task parses, the board
   draws 63 steps, and the two readers agree.
3. The first render after the plan edit flagged `plan-11` blocked because its acceptance command
   reads `board.html`, which that same render had yet to write. A second render cleared it. This is
   the board-idempotence narrowness recorded this morning, met live and behaving exactly as the
   record says it does.
4. `python3 guardrails/check-board.py`, `python3 guardrails/check-doc-rotation.py` and
   `python3 guardrails/check-authority-anchor.py` — all exit 0.
5. `python3 -m pytest -q` over the seven suites that read the plan, the board and the archives — 270
   passed, 2 skipped.
6. `git grep -n "in this pack" -- skills/ templates/ adopt/` and a sweep for the queue-teaching
   sentences: eleven files carry them, which is what put the new task's own count in its row rather
   than a number recalled from the finding it replaces.
7. `python3 -m pytest -q`, the whole suite — recorded in the delivery report for this push.

Findings: five.

**1. The settled bar rests on an authority a reader can go and check.** The entry does not assert
that the owner approved the twenty-one rewritten definitions; it says his standing instruction to
proceed without him outranks the clause in this file that requires him, and it names where that
order is written and on what dates the instruction was given. That distinction matters, since
recording a decision as the person's own when he never made it is the one attribution this pack
forbids. **Nothing to repair.**

**2. The consent clause and a standing grant still collide, and the entry says so rather than
hiding it.** This range settles what happens this time; it does not amend the clause. Writing the
amendment is a change to the plan's own rules on this session's judgment, and the entry puts the gap
in front of the owner as a note rather than a question holding work. **Stands.**

**3. The boot file change is one word.** `ROADMAP.md` became `ARCHITECTURE.md` in the sentence
naming three files a session should not open to orient itself. Checked against the tree: the old
name resolves to `attic/ROADMAP.md`, so the example was a ghost; the new one sits in the root, is
large, and is exactly the kind of file the sentence exists to steer a session away from. No other
line in that file moved. **Nothing to repair.**

**4. The queue-teaching finding is real work, and its acceptance says what finished looks like.**
Eleven files, a version bump and a migration note, and two questions that have to be answered before
any rewording starts — whether a host project should still get a queue of its own, and what a host
that already has one does when the pack stops describing it. Those are named in the row, so the
task does not arrive at a later session as a rewording job with a hidden decision inside it.
**Nothing to repair.**

**5. The architecture's line pin at the plan's task list went stale, and the suite caught it.** The
rule moved up into `PLAN.md`'s own rules pushed the `## Tasks` heading from line 157 to 164, past
the two-line tolerance a line pin allows, and `guardrails/check-pin-drift.sh` redded on it along
with four tests that read that gate. The pin carries the same label and now names the line the
heading sits on. Worth writing down because the gate did exactly what it exists for: a document
edit moved a line another document points at, and the pointer was told before anything shipped.
**Closed in `f53242d`.**

Blocking: none
