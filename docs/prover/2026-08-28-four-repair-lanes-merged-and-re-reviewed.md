# Prover record — 2026-08-28 the four repair lanes, merged and read again

PUSH-REVIEW

Range: 7159fed..c7c4ab6 (24 commits), reviewed as one pass. Base commit `7159fed`, the tip all four
lanes branch off and the head origin/main carries. Reviewed commits, in order: `f052ec5`,
`4431b7a`, `70bc57e`, `4a90e70`, `69d55c6`, `1cd1617`, `46dd26a`, `c62fef2`, `d7b1896`, `1caa5c4`,
`664dee9`, `0f3ae08`, `84f522c`, `64fbe3f`, `f6ba125`, `70580bd`, `5107567`, `fc828a9`, `2c624c3`,
`b8547fc`, `3ea8bbd`, `6452c4c`, `03acd21`, `c7c4ab6`.

Prover version that ran: product-prover 1.4.2, under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

The closing pass on the day's own adversarial review. That review produced twelve confirmed
findings; four sessions repaired them on four branches cut from `7159fed`, each in an isolated
worktree, and all four had finished before this pass began. This range merges the four, resolves
where they collided, settles one disagreement between two of them, and then reads the whole of the
merged result again for reasons to refuse it.

The four lanes, by what they change. The legibility lint measures each rule against the nearest
painting ancestor in the page's own markup instead of asking one question per file; the
worker-restore guard reads the shape a shell writes rather than a segment's first token; the
acceptance-command guard reads its commands through that same shell reader. A done row whose
acceptance command fails takes the board's blocked mark and drops out of the done count; the
landing gate gains the rotation trigger it shipped without; three archives take the rotated name
the rotation gate can see. The amended bar's own record is corrected and the bar itself put to the
owner as a question; thirteen landing-record gaps are healed forward; two frozen numbers and two
mis-keyed checks are fixed. The suite's no-trace fixture ranges over the run's own temp root, and
the gate-machinery cache records its reds as well as its greens.

`2c624c3`, `b8547fc`, `3ea8bbd` and `6452c4c` are the merges, `03acd21` and `c7c4ab6` this pass's
own repairs.

## How this review was run

Read to refuse. Two fresh-context readers went over the merged range with no part in building it,
one on the two guards and the lint, one on the board readers and the suite fixtures, each briefed
to find reasons the change should be refused. Every finding either of them returned was re-derived
by hand before anything was changed: the guard was probed through its real hook entry point on the
exact command strings, the lint was run on pages built for the question, the landing gate was run
over a scratch repository carrying the shape in dispute. Three of the findings did not survive that
re-derivation and are recorded below as not reproducing, because a finding this pass could not
reproduce is part of what the pass covers. Nothing here rests on a lane's own prose about its own
work.

Range: 7159fed..c7c4ab6

Files read: `hooks/worker-restore-guard.py`, `scripts/preshow-legibility-lint.py`,
`scripts/state-probe.sh`, `scripts/render-board.sh`, `scripts/plan-step.sh`,
`scripts/plan_checks.py`, `scripts/sync-skills.sh`, `scripts/install-worker-restore-guard.sh`,
`guardrails/check-doc-rotation.py`, `guardrails/check-landing-next-steps.py`,
`guardrails/check-prover-record.sh`, `guardrails/check-prototype-fence.sh`, `guardrails/pre-push`,
`guardrails.config.json`, `scaffold/guardrails/guardrails.config.example.json`,
`guardrails/progress-baseline.json`, `tests/conftest.py`, `tests/test_guardrails.py`,
`tests/test_landing_next_steps.py`, `tests/test_legibility_floor.py`,
`tests/test_listener_tripwire.py`, `tests/test_plan_is_not_executable.py`,
`tests/test_plan_step_reader.py`, `tests/test_suite_hygiene.py`,
`tests/test_tasks_parser_finds_every_task.py`, `tests/test_worker_restore_guard.py`,
`tests/fixtures/legibility_ancestor.html`, `PLAN.md`, `NEXT_STEPS.md`, `spec/test-honesty.md`,
`docs/roadmap-format.md`, `docs/prover/README.md`,
`docs/queue-archive/rotated-PLAN-2026-08-28-no-acceptance.md`,
`docs/queue-archive/rotated-PLAN-2026-08-28-no-reachable-outcome.md`,
`docs/queue-archive/rotated-PLAN-2026-08-28-q405-agent-messaging-stale-premise.md`,
`docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md`,
`docs/prover/2026-08-28-every-open-task-gets-a-definition-of-done.md`,
`docs/prover/2026-08-28-ungrounded-numbers-and-board-cut-range.md`, `matrix/guardrails.md`,
`matrix/test-author.md`, `skills/communicator/SKILL.md`, `skills/live-spec-base/SKILL.md`.

Checks run: eleven, each with its result.

1. `guardrails/check-doc-rotation.py` on a reconstruction of one lane's own tree, manifest lines
   added — OK, exit 0.
2. the same gate on the same manifest lines over archives WITHOUT their index tables — FAIL, seven
   counts of content dropped, exit 1.
3. `guardrails/check-doc-rotation.py` on the merged tree — OK, exit 0.
4. `guardrails/check-landing-next-steps.py` over `7159fed..HEAD` — OK, exit 0.
5. the same gate over a scratch repository where a done heading is retitled beside an archive line
   quoting its id — a false error, then OK after the repair.
6. `hooks/worker-restore-guard.py` through its real hook entry on 16 command strings, before and
   after the repair — five shapes passed before, all five denied after, six ordinary commands
   allowed throughout.
7. `scripts/preshow-legibility-lint.py` on six pages built for the question, against the shipped
   code and the repaired code.
8. `python3 -m pytest -q tests/test_worker_restore_guard.py tests/test_worker_restore.py` — 238
   passed.
9. `python3 -m pytest -q tests/test_legibility_floor.py` — 19 passed.
10. `python3 -m pytest -q tests/test_config_health.py`, after both installers ran — 34 passed.
11. `python3 -m pytest -q`, the whole suite, alone on a clean field — recorded in the suite-run note
    below.

Findings: fourteen, listed below. Nine are defects this pass found and repaired; three are findings
a reader returned that did not reproduce; two are narrownesses left standing with their reason.

**1. The manifest-versus-index disagreement, settled by running the gate.** One lane reported its
three manifest lines green against a scratch copy of the plan. A second lane, reading the archives
as they stood at the shared base, found that the rotation gate also demands a numbered index row
inside each named archive and concluded the lines alone could not have been green. Both were run.
Manifest lines over archives with no index rows FAIL on seven counts of content dropped, one per
row: the reading of the gate is right, and it is the gate's own violation (a), not a subtlety. The
same manifest lines over the archives as that first lane actually wrote them return OK: the green
was real, because the same commit that renamed the files added those index tables, which the second
lane's isolated worktree could not see. Neither lane reported a green it did not have. The class
this matters for is the other one — a lane inferring another lane's state from a shared base rather
than from that lane's own tree — and it cost this pass nothing only because the gate is cheap to
run twice.

**2. Five destructive shapes still walked past the worker-restore guard.** Probed through the real
hook entry, not the module: `eval 'git checkout -- X'` (neither a wrapper nor a launcher, so the
program read as `eval`); `bash -lc` and `bash -cx` (a shell's short options cluster, against a
reader matching `-c` exactly); `echo hi & git checkout -- X` and its `|&` twin (a single `&`
separates commands the way `;` does, and only `&&` was read); and `cp <(git show HEAD:X) X` (process
substitution unread, and the copy family not a write target). All five are denied now, and each
rides in the routes-around corpus red-proven against the tree that shipped it. `ruby`'s
inline-program flags were a bare string rather than a tuple, which made the membership test a
substring test — a false denial of `ruby -`. **Closed.**

**3. The guard's own statement of what stays out of reach was wrong about two of its three items.**
It conceded the act staged across two commands while reading both halves inside one command, and it
did not name the writer that puts its destination inside a language the reader does not parse
(`awk '{print > "X"}'`, `sed -n 'w X'`, `ex -sc 'wq! X'`). Both corrected; the second is now a
stated concession rather than a hole a reader has to find. **Closed.**

**4. The acceptance-table guard's append arm was a raw search over the command text.** Every other
arm reads through the shell reader; this one did not, so `grep -q 'a >> b' notes.md` counted as a
write — precisely the grep-pattern false positive the shell reader was adopted to end. Both redirect
questions now run through one quote-aware walk inside that reader, and seven honest reading
commands hold the other direction. **Closed.**

**5. The landing gate called a retitle a rotation.** Its rotation arm read the removed side of the
`PLAN.md` diff alone, and every edit to a heading line shows as one removal and one addition. An
archive page quoting that row's id — which archive index tables and cross-references routinely do —
then made the gate report a close for a row still sitting on the board. Red-proven in a scratch
repository, repaired by comparing the two sides as the arm's own sibling already did, and held by
two tests that fail against the shipped code. **Closed.**

**6. The legibility lint printed a red no viewer can see.** It took the first matching painting
rule with no specificity at all, so `div { background: #fff }` written above
`.card { background: #111827 }` scored a card's caption against the page's white at 1.3:1 where the
real render is about 13:1. The lint blocks a showing on a red, so this one blocks on a pair that
does not exist. It ranks by specificity now and keeps document order as the tie-break, which is
what the `prefers-color-scheme` case the lane argued from actually needed — the two rules there
carry the same selector, so the unconditional one still wins. **Closed.**

**7. A red the lint used to print became a silence.** The lane repaired a real defect —
`_block_bg` reached past `linear-gradient(` and returned the near stop as though it were the
surface — by refusing to resolve a gradient at all. That is right where the text clears the floor
over part of the run and fails over the rest, which nothing but a render decides. It is wrong where
the text is under the floor at every stop: the file decides that pair on its own, and the reader
stood down on it instead. It reds now, scored against the friendliest stop the page offers, so the
number is one no render can argue with; a gradient the text is legible over part of still goes to
the eye. **Closed.**

**8. A fixture had been given a gradient so that finding 7's case would keep standing down.**
`tests/fixtures/legibility_ancestor.html` gained one line, `.outer-wrap { background:
linear-gradient(...) }`, in the lane that changed the reader. Without it the caption inside resolves
through the markup and reds at 2.2:1 — a correct red. The fixture exists to cover a surface painted
in a colour no text read can name; it carries an image now, which is genuinely unnameable and has no
stops, so the case it claims to cover is the case it covers. **Closed.**

**9. The probe called a row verified whose own command contradicts its done mark.** The lane's own
subject was that a failing key must not let a done mark stand, and it named three things to fix: the
mark, the done count, and the verified tag. The board's reader lost the tag and the probe kept it,
so the two readers of one plan disagreed on exactly the row the change was about, and the new test
locked the half-fix in by never asserting the tag was gone. The probe reads `marked done` now. That
in turn broke the suite's print-shape reader, which knew two tags and not three and silently dropped
those lines from its accounting — it reported four tasks lost that were on the screen. Both
repaired, and the shape reader now names all three tags with the reason. **Closed.**

**10. The spec still demanded the mechanism the suite fixture replaced.** `spec/test-honesty.md`
criterion 4 under INV-100 required the run to fail "through a session-scoped before-and-after diff
of the temp home". That is the very shape the temp-root repair removed, so the spec was not merely
stale — it stated as a duty the thing the repair took out. It now says each run gets a temp home of
its own, that an artifact of that run's own surviving in it fails the run, and that a run is never
judged by what another run left on the machine. `matrix/test-author.md` row M-236 named the old
mechanism too and is repointed. **Closed.**

**11. Two owed repoints turned out to be already paid, by a lane that could not be seen.** The
q-405 archive rename left `tests/test_listener_tripwire.py:120` and `matrix/guardrails.md`'s M-412
row pointing at the old filename, and both were carried on this pass's own list. Both were repaired
inside `4a90e70`, in the lane that made the rename, and no old archive name survives anywhere in the
tree. Recorded because the list was built from a lane's report of what it had left undone, and that
report was written without sight of the lane that had already done it. **Closed by an earlier
commit, not by this one.**

**12. Three findings a reader returned did not reproduce.** A painting rule carrying a pseudo-class
or an attribute test was reported to turn a stand-down into a silent pass; run on a page built for
it, the reader stands down and lists the pair as unresolved, which is the honest answer. The
gate-machinery cache was reported able to wedge the suite permanently on a stale red; the recorded
red forces the two-minute inner run and never fails it, and the store is machine-local, so it
propagates to nobody. The guard was reported to have gained false positives on `$VAR` paths and on
an absolute target with no `cwd`; both are the lane's own deliberate conservatism, both were
verified to behave as the lane describes, and neither is loosened here — a guard is not made
friendlier by weakening it. Recorded so a later reader does not spend the same hour.

**13. Two narrownesses stand, with their reason.** The landing gate's rotation trigger asks for the
removal and the archive line in ONE commit, so a hand that writes the archive page in one commit and
removes the rows in the next evades it; closing that means the gate holding state across commits,
which is a larger change than this pass should make on its own judgment, and the rotation gate
already holds the nothing-lost half of the same act. And the temp-root leak check now reads one
directory, so a test writing to the system temp by an absolute path is outside its reach —
`scripts/state-probe.sh` writes `/tmp/probe-next.txt` and the suite runs it. That second one is a
real gap in the fixture's stated promise and the honest place for it is a task on the board, not a
repair improvised at a push. **Both stand.**

**14. Two commit messages carried claims their code did not support, and one carried a miscount.**
The failing-key commit says "both readers of the plan say it the same way, from one home", which
finding 9 shows was false when written. The lint commit says the reader "keeps the first, the
unconditional one every viewer gets", which finding 6 shows is not what first-in-document-order
means. Both are history and stay as written; the code they describe is now what they describe. The
acceptance guard's docstring counted fifteen forms over a list of eighteen, and a record of what was
proven has to be able to count what it holds — corrected in place.

## The merge itself

Five conflicts, all in the two lanes that both touched the board's documents, each resolved by
reading both sides rather than taking one. The plan-checks comment where both lanes removed the same
arm and wrote a different true reason for it: the merged comment carries both facts. The
no-acceptance archive's criterion paragraph, where one lane argued from a bar widened six hours
earlier and the other re-tested all five rows against the bar in force: the re-tested paragraph
stands. The terminal status word in the three archive indexes, where one lane wrote `declined`
everywhere and the other `superseded` everywhere: the seven rows were refused off the board and none
was absorbed by a live row, so all three read `declined`, and the folded-rows archive of the same day
keeps `superseded`, which is what its ninety-two rows actually were. And the two single-row index
cells, which take the fuller reason from one lane and the dated anchor for the owner's word from the
other.

Two notes went stale on the merge and were corrected in it rather than left to be found: the resume
file's red-at-this-pause block, whose three manifest lines are now in `PLAN.md`, and the earlier
prover record's closing note that no manifest line points at the no-reachable-outcome archive.

## The suite run

One clean run, alone on the field, after both installers had put the merged guard and the merged
communicator skill in place. The count and the verdict line stand in the delivery report for this
push; the run before it — taken while this pass was still editing — is not a verdict and is not
quoted as one, and its one teardown error was the judged-tree fixture correctly catching those very
edits.

Blocking: none. Nine findings closed in `03acd21` and `c7c4ab6`, three did not reproduce, two stand
with their reason written above.
