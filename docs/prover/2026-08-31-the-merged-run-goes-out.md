# Prover record — 2026-08-31 the merged run goes out

PUSH-REVIEW

Range: 7159fed..HEAD. Base commit `7159fed`, the head `origin/main` carries. Every commit in the
range, in order: `f052ec5`, `4431b7a`, `70bc57e`, `4a90e70`, `69d55c6`, `1cd1617`, `46dd26a`,
`c62fef2`, `d7b1896`, `1caa5c4`, `664dee9`, `0f3ae08`, `84f522c`, `64fbe3f`, `f6ba125`, `70580bd`,
`5107567`, `fc828a9`, `2c624c3`, `b8547fc`, `3ea8bbd`, `6452c4c`, `03acd21`, `c7c4ab6`, `ef723ed`,
`ecb8b81`, `c9f8fd6`, `390dd1d`, and this pass's own repair commit.

Prover version that ran: product-prover 1.4.2, under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## Why this record stands beside the one of 28.08

`docs/prover/2026-08-28-four-repair-lanes-merged-and-re-reviewed.md` covers `7159fed..c7c4ab6`, the
range as it stood when that pass ended. Two commits landed after it, `ecb8b81` and `c9f8fd6`, and
the pass that wrote it was cut off mid-sentence while widening its own `Range:` header to name them,
leaving a header claiming twenty-six commits above a body still reading twenty-four. That
half-finished edit sat uncommitted for three days. It is reverted rather than finished: a record
cannot claim to have read commits written after it closed, and `Range:` is the one line the gate
reads for the range. The 28.08 record keeps the range it actually read, and this record covers the
whole of what is being pushed.

The push also falls on a different day from the work. The gate's push road wants a record dated the
day of the push, and the honest way to give it one is a review run today over the range as it stands
today.

## How this review was run

Read to refuse, on a tree nobody had touched in three days. Nothing below rests on the earlier
pass's prose: every landing that record claims was re-derived against the merged tree. Two
fresh-context readers with no part in building any of it then went over the range in parallel, one
on the guard, the lint and the two gates, one on the board's two readers, the archives and the
cross-document facts, each briefed to find reasons to refuse. Every finding either returned was
reproduced here before anything was changed, and every repair below is red-proven against the code
that shipped it.

That second read is what this pass is for. The first half confirmed the range; the second half found
sixteen more things, repaired ten of them, and left six standing with their reason. Three of the
repairs are for regressions this range itself introduced.

Files read: `hooks/worker-restore-guard.py`, `guardrails/check-worker-restore.py`,
`scripts/preshow-legibility-lint.py`, `scripts/state-probe.sh`, `scripts/render-board.sh`,
`scripts/plan_checks.py`, `scripts/sync-skills.sh`, `scripts/install-worker-restore-guard.sh`,
`guardrails/check-prover-record.sh`, `guardrails/check-doc-rotation.py`,
`guardrails/check-landing-next-steps.py`, `guardrails/pre-push`, `guardrails/check-tests.sh`,
`.github/workflows/gates.yml`, `tests/conftest.py`, `tests/test_guardrails.py`,
`tests/test_worker_restore_guard.py`, `tests/test_legibility_floor.py`,
`tests/test_landing_next_steps.py`, `tests/test_board_matches_the_canon.py`,
`tests/test_tasks_parser_finds_every_task.py`, `tests/test_listener_tripwire.py`,
`tests/test_doc_rotation.py`, `PLAN.md`, `NEXT_STEPS.md`, `matrix/guardrails.md`,
`skills/communicator/SKILL.md`, `skills/live-spec-base/SKILL.md`, `docs/prover/README.md`,
`docs/prover/2026-08-28-four-repair-lanes-merged-and-re-reviewed.md`,
`docs/skill-review/2026-08-28-communicator.md`, and the four archives under `docs/queue-archive/`
named `rotated-PLAN-2026-08-28-*`.

Checks run: seventeen, each with its result.

1. `python3 -m pytest -q`, the whole suite, alone on a clean tree, before any repair — 2,556 passed,
   5 skipped, 597.76s.
2. `hooks/worker-restore-guard.py` through its real hook entry on 69 command strings across three
   sweeps — the shapes the range added, then a second sweep of shapes its own docstring does not
   claim, then the routes the readers returned. The second and third sweeps found the fifteen routes
   of findings 1 to 6 below.
3. The same guard on the repaired code, 38 strings, then the full corpus: every route denied, every
   ordinary command allowed.
4. The same guard, live and unasked: it refused this pass's own `git checkout -- <record>` when the
   half-finished edit was being reverted, and named the file-writing route instead. The revert was
   done that way.
5. The fifteen routes against the shipped guard and against the repaired one, side by side — 15 of
   15 walked past before, 0 of 15 after; 3 of 3 honest commands denied before, 0 of 3 after.
6. `guardrails/check-worker-restore.py`'s `classify` on the same git-option shapes, before and
   after — the retrospective arm carried the identical hole and now reports the same violations the
   hook denies.
7. `scripts/preshow-legibility-lint.py` on nine pages built for the question, against the shipped
   code and the repaired code. Three of them are the fixtures added here; the shipped reader returns
   a false green on one and a false red on two.
8. `python3 -m pytest -q tests/test_worker_restore_guard.py tests/test_worker_restore.py` — 265
   passed. `tests/test_legibility_floor.py` — 22 passed. `tests/test_landing_next_steps.py` — 28
   passed. `tests/test_board_matches_the_canon.py` — 1 passed. `tests/test_doc_rotation.py` — 30
   passed.
9. `python3 guardrails/check-doc-rotation.py` on the merged tree — OK, exit 0.
10. `python3 guardrails/check-landing-next-steps.py` over `origin/main..HEAD` — OK, exit 0.
11. `python3 -m pytest -q tests/test_config_health.py`, after both installers ran — 34 passed.
12. `bash scripts/install-worker-restore-guard.sh` and `bash scripts/sync-skills.sh`, twice: once
    before the repairs and once after the guard changed. The board's own acceptance keys caught the
    drift in between — two done rows took the blocked mark until the guard was reinstalled, which is
    the mechanism this range added doing its job on this pass's own work.
13. Every gate the CI workflow runs outside the suite and outside the record gate, by hand against
    `LIVE_SPEC_DIFF_BASE=origin/main` — sixteen gates, all exit 0. The four host checks of gate h —
    all exit 0. `check-config-health.sh` and `check-freeze.sh` — both exit 0.
14. `bash scripts/state-probe.sh` and `bash scripts/render-board.sh` — both run clean, the board
    draws all 62 tasks, and the tree stays clean after.
15. A sweep over each of the four lane branches: every line the lane added, longer than a few words,
    looked for in the merged file at `HEAD`. Every line missing is accounted for by a documented
    conflict resolution or by one of this range's own later repairs.
16. `grep` for every pointer at the three renamed archives across the tree, and for the pre-rename
    names — twenty-three pointers, every one resolving to a file on disk, no pre-rename name left.
17. `python3 -m pytest -q`, the whole suite again after the repairs, alone on the tree — the count
    stands in the delivery report for this push.

Findings: twenty-one. Ten defects repaired here, five landings re-derived and confirmed, and six
narrownesses left standing with their reason.

### The guard

**1. Every git pre-command option but five walked past both arms of the worker-restore rule.**
`_git_args` stepped over a NAMED LIST — `-C`, `-c`, `--namespace`, `--work-tree`, `--git-dir` — so
`git --no-pager checkout -- foo` reached the verb reader as the word `--no-pager` and passed.
`-P`, `--paginate` and `--literal-pathspecs` are the same shape, and `--no-pager` is what a script
writes to keep git off a tty. `guardrails/check-worker-restore.py` carried the identical list, so the
retrospective arm reported nothing either: the act had no gate at all. A list of names cannot answer
a class git can grow at any release, and git's own grammar can — the pre-command options all begin
with `-`, and the first word that does not is the subcommand. Both arms read it that way now, and
only the options carrying a separate value word are named. **Closed.**

**2. A redirection standing where the command word goes hid the read half.** The shell lets a
redirection sit anywhere in a simple command, the front included, so `> foo git show HEAD:foo`
writes repository bytes over `foo`. The write half was found all along; the program name read as
`>`, so the read half went unseen and the pair was never assembled. The glued spelling `>foo cmd`
went the same way. Both are stripped before the program name is read. **Closed.**

**3. `exec > foo` and `{ … ; } > foo` split the pair across two pipelines of one command.** `exec >`
re-points the shell's own output for everything after it; the brace form hangs the redirection on
the group's closing brace, and the `;` that form requires is what ends the pipeline. The read then
sits in one pipeline and the write in the next, and each was judged alone. `( … ) > foo` needs no
`;` and was caught all along, which made the brace form an inconsistency rather than a concession
the file states. Both are read at the command level now, where the shell reads them. **Closed.**

**4. The keyword that OPENS a compound statement was missing where `do` and `then` already stood.**
`if git checkout -- foo; then :; fi` reached the verb reader as the word `if`. `while` and `until`
the same. `for f in *; do git checkout -- $f; done` was caught only because `do` happened to be on
the list. **Closed.**

**5. An append after the same command empties the path is a restore, and read as an append.** The
reason `>>` is innocent is that the file's own bytes survive it, and that reason is gone the moment
the same command takes them out first: `: > foo && git show HEAD:foo >> foo` destroys exactly what
`git checkout -- foo` destroys. `rm foo && …` and `truncate -s 0 foo; …` are the same act. The paths
a command empties are read once over the whole command, and an append onto one of them counts as
landing bytes on the tree. An append onto a path the command never emptied is still an append.
**Closed.**

**6. Two honest commands were refused.** `git restore -S foo` is index-only and touches no
working-tree byte; the arm read `--staged` and not git's short spelling, so `-S` was denied — and
`git restore -h` with it, which only prints help. Both spellings of both destinations are read now,
and a restore is refused when it writes the tree. One of the readers hit this live while doing
honest work. **Closed.**

### The legibility lint

**7. A painting rule the reader cannot match made an unreadable page print a clean pass.** An
attribute test, a `:not(…)` or a position test in a selector is a simple selector this reader does
not parse, and `_selector_weight` folded that into the same answer it gives a selector that plainly
does NOT match. `_element_paint` then stepped over the block, and the ancestor walk carried on past
the element's own surface to the page behind it and scored the text against a background no viewer
sees. A card painted `.card[data-theme="light"]` with near-white text on it printed "text meets the
contrast and size floor". Before the ancestor walk landed in this range the same page stood down for
the eye, so this is a regression the range introduced. A block whose selector is undecidable for an
element is neither a painter this reader may use nor one it may step over: the walk stops there and
the pair goes to the eye, with a stand-down line that says which of the two reasons it is.
**Closed.**

**8. The same defect, in the direction that blocks a showing.** Light text on a card painted
`.card[data-theme="dark"]` was scored against the page's white and redded — a block on a showing for
a pair nobody can complain of. Same repair, and a fixture holds each direction. **Closed.**

**9. The gradient ground ignored the specificity ranking two lines away from it.**
`_gradient_worst_ground` took the first matching painting block in document order while
`_element_paint` beside it ranked by specificity, so `div { background: linear-gradient(#fff,
#f0f0f0) }` written above `.card { background: linear-gradient(#000, #111) }` scored a card's white
caption against near-white and redded it. Two readers of one page disagreeing about which rule
paints it is the same class the 28.08 pass found between the board and the probe. The ranking is now
the one used beside it. **Closed.**

### The board and its readers

**10. One mark, two spellings, and no reader agreed.** `✅` and `✅️` are one mark on a board and two
different strings to a comparison, and `PLAN.md` already writes `👁️` with a variation selector while
writing `✅` without one. Every reader compares the mark literally, so a done mark typed with the
selector read as done to the eye while the board would not count it, the done count would be short,
and `guardrails/check-landing-next-steps.py` would ask the commit that set it for no resume refresh
at all. The mark is brought to one canonical spelling where it is PARSED, in both homes — the
board's shared parser and the gate's own — so every comparison downstream goes on reading as
written, and the eye keeps its selector because without one it renders as a monochrome glyph.
**Closed.**

**11. The one test written to catch the two readers disagreeing was blind to the rows this range
introduced.** `tests/test_tasks_parser_finds_every_task.py` was taught the third status tag on 28.08
— a done row whose acceptance command fails prints "marked done" rather than "verified" — and the
identical regex in `tests/test_board_matches_the_canon.py` was not touched. Every such line was
silently dropped from the comparison, so the test's reach over exactly the new state was zero; it
passed only because all nineteen keys happen to pass today. One vocabulary written in two homes,
one of them corrected. **Closed.**

**12. A failing-key row landed under a column heading that contradicted its own card.** The board's
Blocked column reads "waiting on the owner's word", which was true of everything that landed there
until this range gave a done row with a failing command the same mark. Nobody is waiting on the
owner for those. The sub-line names what the column actually holds and each card goes on saying
which of the two it is. **Closed.**

### Re-derived from the 28.08 record, against the tree

**13. Every landing that record claims is in the merged tree.** The lint ranks painting rules by
specificity; the guard reads grouping, launchers, `-c` clusters, `eval`, the single `&` and both
process substitutions; the board and the probe both give a done row whose key fails the blocked mark
and drop it from the done count; the suite's leak check ranges over the run's own temp root; the
meta-test's digest store carries a `(last red)` key whose red outranks a green on the same digest.

**14. The two repoints that record calls already paid really are paid.**
`tests/test_listener_tripwire.py:120` and `matrix/guardrails.md`'s M-412 row both name the archive's
current filename, and no pre-rename name survives anywhere in the tree.

**15. The trimmed legibility bullet keeps the instruction its own tool needs.** Checked against the
lint's behaviour rather than the commit's claim: a gradient the text clears over part of exits 0 and
prints its stand-down as an info line, so a session reading only the exit code would show a page
carrying a pair nobody looked at. The sentence that survives the trim is exactly the one that
prevents that.

### Standing, with their reason

**16. The board is not idempotent, and its own key is why.** `plan-11`'s acceptance command reads
`board.html`, and `scripts/render-board.sh` runs that key and THEN writes `board.html`, so the page
reports that row from the previous render. On the first render after a plan edit the row takes a
spurious blocked mark and the done count is short by one; a second render is correct. This range is
what makes it visible, since before it a failing key left the mark alone. Closing it means either a
render inside the probe on every session start or a renderer that writes twice — both costs the
board's owner never asked for — or changing that row's acceptance, which is a `PLAN.md` edit under
the very rule now waiting on his word. Reproduced on a copy of the tree, two renders of one
unchanged file disagreeing. **Stands.**

**17. Teaching the rotation gate's ambiguous-row arm the heading shape is not the repair.** That arm
looks for a `| n |` row in the live document, and since the one-list merge `PLAN.md` carries no table
row at all, so it fires on nothing. Run against the heading shape instead, it reds on more than forty
rows the tree holds on purpose: a manifest names rows by the number the retired queue gave them and a
live heading names a task by its id, and after the merge those are no longer one identity — some rows
were folded INTO a live task and archived under their own old number, and at least one was archived
and reopened the same day. Which copy is canonical for each is a question about the list. Proven by
running it: 40-odd violations on a tree every other gate calls clean. The finding is recorded here
rather than closed by a gate that would red the owner's own arrangement. **Stands.**

**18. The rotation gate's archive-row arm reads numeric ids only.** The folded-rows archive holds 94
`— id:` rows while its manifest line names 92; the two extras are `plan-1` and `plan-13`, which no
manifest line and no index table names. Nothing is lost today — `PLAN.md` names both under
`**Absorbed:**` with the archive's path — but those lines are hand-written and no check reads them.
Closing it means manifest lines this pass would have to write into `PLAN.md`, which is the same
question as finding 17. **Stands.**

**19. The probe prints twenty of the forty-three blockers and says nothing about the rest.** The
PLAN section prints "… 17 more below" for exactly this reason and the BLOCKERS section prints no
such line. Pre-existing: forty blockers at the base commit, and this range does not touch that
reader. **Stands.**

**20. Three of the guard's conservatisms are deliberate and are not loosened here.** `git checkout
foo.py` with a single unmarked word passes, because the word may be a branch and the guard will not
guess. An unexpanded `$VAR` in a redirect target is refused, because a variable is not evidence that
the bytes land somewhere harmless. And an absolute target with no `cwd` in the event counts as this
tree. All three are the file's own stated design, all three were verified to behave as it describes,
and a guard is not made friendlier by weakening it. One of them cost a reader a workaround while it
was working, which is the price the design names. **Stand.**

**21. The lint takes the FIRST of two rules at equal specificity, so an unconditional override reads
as the first.** That tie-break is what makes a `prefers-color-scheme` restatement resolve to the
colour every viewer gets, and the same rule silences a later unconditional override of the same
selector. Pre-existing, deliberate, and named in the reader's own docstring. **Stands.**

## One thing this pass did to itself

The suite's judged-tree fixture redded during a reader's run, naming this tree's own working copy as
changed. The changer was this pass, editing the guard while a reader it had dispatched was running
the suite in the same tree. The fixture is right to red on a changed tree and is not loosened. What
is worth writing down is that its message names a cause it cannot know — it says a script under test
wrote to the root — where the real cause was two writers in one tree, which is the collision this
project's own rules already forbid and which this pass walked into by dispatching readers into its
own working copy rather than into worktrees of their own.

Blocking: none
