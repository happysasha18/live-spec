# Prover record — 2026-08-28 every open task gets a definition of done, and the bar moves to admit five

PUSH-REVIEW

Range: 1b061a8b..HEAD (7 reviewed commits). Base commit `1b061a8b`, the tip this push starts from.
Reviewed commits, in order: `ead4a705`, `e94a2383`, `013ec60f`, `15407f96`, `aa4fa4aa`, `0462b696`,
`195c276c`.

Four of those are another session's, landing in the same tree while this one worked: `15407f96`,
`aa4fa4aa` and `0462b696` are its rotation-gate work, and `013ec60f` is this record's own first
commit. That session's three are reviewed in full in the record beside this one,
`docs/prover/2026-08-28-rotation-both-directions-and-the-comment-anchored-class.md`, which covers
the same range from the other side. They are read here only as far as this range had to touch
them — Finding 8 — and that record is where their own account stands.

Prover version that ran: product-prover 1.4.2, under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

Earlier today the board was cut to 63 rows and the definition of done for seventeen open rows was
restored from `docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`, where the 27.08
merge had dropped it. Every one of those seventeen came back as a sentence. `PLAN.md`'s own bar for
a queued task, in "Words used here", said a task earns its queued mark only when its definition of
done is a command. So the board failed its own rule, in the open, on more than half its open rows.

This range walks every open row and gives it a definition of done a reader can act on. Twenty-one
rows now name a command. Five say in one line that no command decides them, name who reads the
result, and name what would convince that reader. One row left the board. The bar itself was
amended, because it forbade the honest shape the five need.

One file changes, `PLAN.md`, plus one new file in `docs/queue-archive/`. A second session is writing
`guardrails/check-doc-rotation.py`, `scripts/rotate-doc.py`, `attic/MANIFEST.md`,
`docs/roadmap-format.md` and three test files in the same tree at the same time. Those are that
session's work, are not in this range, and were deliberately kept out of it — one commit here first
swept that session's staged rename in by accident and was split back apart before anything left the
machine (`git reset --soft` and a pathspec commit; the rename sits staged in the index exactly as it
did before).

## How this review was run

Read to refuse. The question asked of every rewritten row was the one the board keeps failing: could
a reader who has never seen this project tell finished from unfinished by what the row now says? A
row that answered "yes, by running this" had its command checked against the tree — the script named
has to exist, or the row has to be honest that it does not yet. A row that answered "only by reading
something" was checked for whether that was true, or whether a command had simply not been looked
for hard enough.

Range: 1b061a8b..e94a2383

Files read: `PLAN.md` (whole, both the rules sections and every task block),
`scripts/plan_checks.py`, `scripts/state-probe.sh`, `skills/live-spec-base/SKILL.md`,
`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md` (rows 166, 591, 596 and the
2026-08-12 review band), `docs/queue-archive/2026-08-28-archived-no-acceptance.md`,
`docs/queue-archive/2026-08-28-q405-agent-messaging-stale-premise.md`,
`guardrails/check-prover-record.sh`, `guardrails/judge-hooks.json`,
`tests/test_compaction_discipline.py`, `matrix/build-pipeline.md`, `live-spec/CLAUDE.md`.

Checks run:
- `bash scripts/state-probe.sh` — the board reads 26 open and 36 done, 62 rows, the marks unchanged
  and the two rows held for his eyes still held for his eyes.
- `bash scripts/render-board.sh` — 62 steps, 40 blockers, so the page and the list hold the same set.
- `python3 -m pytest -q` — 7 failed, 2468 passed, 3 skipped, 1 error, in 17m54s. Split by cause in
  Finding 6; five were this range's and are fixed, the rest are the second session's uncommitted
  rename.
- `python3 -m pytest -q` in a scratch worktree cut at `ead4a705` — 5 failed, 23 passed, 1 skipped
  over the eight names above, which is the proof of that split.
- `bash guardrails/check-pin-drift.sh` — after `e94a2383`: 173 pins checked, all proved; 39 range
  pins on the rule-price page proved too.
- `bash guardrails/pre-push < /dev/null` — see Blocking.
- `ls scripts/open-lane.sh guardrails/check-authority-anchor.py guardrails/check-worker-restore.py
  guardrails/check-skill-loadability.sh guardrails/check-matrix-reference.py` — every script a
  rewritten row names by path exists.
- `git log --oneline --diff-filter=D -- guardrails/check-hooks-can-fire.py
  guardrails/hook-red-proofs.json` — both were removed in `e61b29b7`, which is Finding 2.
- `grep -rn "q-596" PLAN.md scripts/ tests/ guardrails/ docs/*.md` — empty, so the archived row
  leaves no dangling pointer.
- `git diff PLAN.md | grep '^+' | grep -niE '\b(recorded|logged|record)\b'` — empty, so no new
  acceptance line breaks the plan's own law 3.
- `git diff PLAN.md | grep '^+' | grep -niE ', not |rather than a |instead of a '` — empty, so no new
  line carries the contrast frame he has banned.

## Findings

**1. The bar at "Words used here" contradicted two other places in the same file, and this range
changed a sentence he wrote.** The bar demanded a command of every queued task. Two other passages
already provided for the opposite: the closing rule four bullets below it ("A task whose result is
prose, a measurement or a decision writes no command and says in one line who read it and where"),
and plan-10's own second bullet ("Where an acceptance genuinely cannot be run by a command — it
needs the owner's eyes — the step says so in one line"). A file cannot hold all three. The bar is the
one that moved, because it is the newest and because the five rows it forbids are honestly of that
shape. This is a change to his own 27.08 wording, so it is named in §Blockers in plain words rather
than left to be discovered in a diff, and §Blockers states what the harder bar would cost if he
wants it back. **Not blocking** — his word of 28.08 00:53 is to carry the plan to the end without
asking, and the change is visible where he reads.

*Second-order note the bar's old wording also earned:* "a command, not a sentence" is itself the
"X, not Y" contrast frame his own profile bans. The new wording carries no frame.

**2. q-489's definition of done stood on machinery that was deliberately removed.** The row's
acceptance opened "Shipped 2026-07-27: `guardrails/hook-red-proofs.json` names a fixture per hook and
`guardrails/check-hooks-can-fire.py` runs each real hook against it". Neither file is in the tree.
`git log --diff-filter=D` puts their removal in `e61b29b7`, "Remove the checks whose only subject was
another check". The two legs the row still called owed — a caller census as a standing table, and a
retirement threshold — are the same shape, and a threshold with no outside source is forbidden by the
plan's own law 2 regardless. Rewriting the row to demand them back would have had this pass rebuild
what a considered decision had just torn out. The row keeps its title, which is worth keeping, and
its acceptance is now the part that still stands: a check ships with a fixture it reds against
without its fix. **Closed** in the row's own text, which says what was struck and why.

**3. plan-10's acceptance pointed at a section this file no longer has.** It required "every step
heading in `## Steps`" to carry a key. The section is `## Tasks`, and has been since the 27.08 merge.
Worse, the requirement had gone stale in substance too: earlier today's pass established that a key
is worth its weight only where a row's subject can drift back, and gave eleven rows keys rather than
all of them. An acceptance demanding a key for every task would have reddened against a decision
taken the same day. Rewritten to what the row actually wants — a done task carries either a command
or a named reading, and no command is a bare file-existence test. **Closed.**

**4. Two rows carried a "held for the owner" note his own 27.08 word had already retired.** q-527
waited on what counts as a cleared mistake; q-536 waited on three wording rulings in the rulebook.
Both are machinery, and his word of 27.08 puts machinery on this seat's desk and asks him only about
machinery he set up himself. Base rule 29 says a deferral marker is re-tested at every touch and
that a marker which cannot name a human-only fact defaults to the seat's. Neither could. Both notes
are replaced by a line saying the ruling is the seat's and why. q-536 keeps its title, "need your
final call", because a title changes only on his own word — which leaves a row whose name and body
now disagree. **Stands, named:** the disagreement is deliberate and one sentence long, and the body
says so; changing the title without asking would break a rule to fix a smaller one.

**5. One row named no outcome this project can reach, and only one.** q-596, the personal-settings
leak, says in its own acceptance that this repository cannot fix its cause and that it stands as a
dated note. There is no state in this tree that could move from undone to done, so no command and no
reading could tell the difference. Archived to
`docs/queue-archive/2026-08-28-archived-no-reachable-outcome.md` with the criterion written out. The
narrow criterion was applied on purpose: three other rows were tempting to archive and were kept —
q-800, whose answer is a decision somebody can still take; q-48, which waits on a world event and
names it; and q-489 above, whose title outlived its machinery. A row is hard to write, or it is
unreachable, and only the second earns the archive. **Closed.**

**6. The pass broke a pin, and the suite caught it — but only after the reds were separated by
cause.** The full suite came back 7 failed, 2468 passed, 3 skipped, 1 error. Five of the seven were
this range's own: adding lines above `PLAN.md`'s task list pushed the list from line 152 to line
157, and the architecture pins that line, so gate g landed on a blank line and four of its tests plus
the CI-mirror test went red with it. The other two failures and the error belong to the second
session's in-flight retirement of `scripts/rotate-doc.py`, whose pins point at a path that has moved
on disk and is not yet committed.

The split was proved rather than asserted, because a worker calling its own breakage somebody else's
debt is a failure this project has already had twice: a scratch worktree was cut at `ead4a705`, this
range and nothing else, and the seven were re-run there. Five reproduced. Two failed to reproduce and
the error did not appear, which puts them where their file paths already said they were.

The five were repaired by re-pointing the pin, `e94a2383`. The line the pin caches moved; the thing
it names did not. **Closed.** One honest note about that repair: the second session had already made
the same one-line edit in the working tree while carrying its own change through the same file's
neighbourhood. The line is this range's breakage to fix, so it is committed here rather than left to
ride out on somebody else's landing, and that session loses nothing by it.

**6b. Chain and suite as pushed.** Under Checks run above and Blocking below.

**7. What this pass did not do, said plainly.** It wrote definitions of done. It closed no row and
built none of the machinery the twenty-one commands name — several of those commands describe a
check that does not exist yet, which is correct for an open row and would be a lie on a closed one.
No key was added to `scripts/plan_checks.py`, because that file's own header reserves a key for the
moment a row closes. Anyone reading a row's command as a claim that it already runs has misread it,
and the rows say "done when" rather than "done".

**8. The sibling session's landing made one line of this file stale, and it is repaired here.**
While this pass ran, the other session retired `scripts/rotate-doc.py` to the attic and gave the
doc-rotation gate a second direction, so a closed row sitting in a referenced archive that no
manifest line names now reds. `PLAN.md`'s §Blockers carried a line saying the rotation tool only
understood the retired queue's table and that teaching it the board's shape was work nobody had
asked for, left open until someone did. That question is now answered: the tool is gone and the gate
proves both halves of a hand-made move. The line is rewritten as the record of the decision,
`195c276c`, which is why this range holds a seventh commit.

Read across the seam, their change is sound where it touches this one. `attic/MANIFEST.md` gains the
tombstone line base rule 10 asks for, and the three pointers that named the retired tool as live
machinery — `architecture/guardrails.md`, `matrix/guardrails.md` and the live-body law in
`docs/roadmap-format.md` — were repointed in the same landing. **One soft note, not blocking:**
`docs/roadmap-format.md` lines 71-72 still describe the tool as machinery that will be taught the
monthly append. Those two lines sit inside a section narrating a one-time conversion delivery that
already happened, so they read as a record of that delivery rather than as a live pointer. A reader
skimming for what exists today could still take them the other way. Named for that session, whose
file it is.

*The archive this range adds, `docs/queue-archive/2026-08-28-archived-no-reachable-outcome.md`, was
checked against their new direction: it carries no numbered table rows and no manifest line points
at it, so neither the orphan-archive arm nor the unclaimed-row arm reaches it. Gate t agreed.*

Blocking: none.
