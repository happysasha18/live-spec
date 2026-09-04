# Retired: the findings log that used to sit inside PLAN.md (2026-09-04)

This section held 59 findings written by the project's own reviews. 36 were already closed when it
was retired; the five most substantial of the remaining ones were checked against the live tree on
2026-09-04 and every one of them was already fixed or could not be reproduced.

It was retired because it was a second queue beside the task board: reviews filed work into it that
nobody had asked for, and the plan's own laws told a session to stop and wait whenever it wrote a
line here. The laws changed with it — a finding is now either fixed on the step in hand, or it
becomes a task on the board in the owner's own words, or it is dropped.

Kept verbatim below for the record. Nothing here is queued work.

---

## Blockers

One line per finding. Don't start a second list for them. Don't fix one without the owner's decision.

- **The format page for a row still calls itself the roadmap, and the roadmap is gone. Raised
  31.08, in q-801; closed 03.09.** Checked rather than assumed: `docs/roadmap-format.md`'s row
  shape and vocabularies are not stale. They match, cell for cell, what `templates/PLAN.template.md`
  hands a newly founded project (confirmed against `adopt/START.md`'s file-copy table) — a
  five-cell table, the *queued/ready/in-work/deferred/far* and *bug/small/surface/large*
  vocabularies, the live-body law, the row lint. This project's own current `PLAN.md` uses a
  different, heading-based format instead (`### <icon> title — id:`, `**Group:**/**Priority:**`),
  which is a separate, already-decided fact from plan-11, not a defect this page has. The only
  real problem was the page's own self-description: it opened by defining "the format the roadmap
  is written in" and Requirement 286 in `spec/doc-order-generated.md` (not `design-spec-review.md`)
  named `ROADMAP.md` as the format family's third member — both stale since plan-11 retired that
  file. Fixed as a naming fix, no substance changed: `docs/roadmap-format.md` now names itself the
  format "a project's plan/queue is written in" and speaks of "the queue" throughout rather than
  "the roadmap," and Requirement 286's Context sentence no longer names the retired file. Two dead
  citations found in the same page while reading it closely were fixed alongside, same class of
  defect: a stale "ROADMAP row 481" pointer (that row was absorbed into plan-11 in 28.08's cull
  without the sweep it promised ever being built) and a pointer to `prototype/2026-07-23-roadmap-format/`,
  deleted whole in `61a77841`. Landed in `d2d57d24` (docs/roadmap-format.md,
  spec/doc-order-generated.md), full suite green after: 2738 passed, 57 skipped, 0 failed.

- **This page still holds three copies of the report's own rules, and the lane that converged
  everything else could not touch them. Raised 31.08; closed 2026-09-03.** The report he reads every
  turn had its shape written in several places at once, and they disagreed; that is the thing plan-16
  closed. Every copy outside this page is now a pointer at the one home, and the new check reds if a
  second one appears on any surface that tells a session how to work. Three copies stood here: the
  marks and their meanings appeared twice, once in the words section and once above the task list, and
  the five things a message asking his word must carry sat four lines below a sentence saying the
  format is not repeated here. Fixed: the marks now live once, in "Words used here," citing
  `~/.claude/playbook/CLAUDE.md`; the task-list line now points at that one copy instead of restating
  it; the five things now point at their own real one home, `~/.claude/playbook/personal/profile.md`,
  section "Owner reports" — not `~/.claude/playbook/CLAUDE.md` as first assumed, which holds only the
  Canon format, never the five-line report shape.

- **The personal layer's only copy off this machine was 26 days old. Found 31.08, in q-800; closed
  the same day.** The boot file and the personal profile both live in the private playbook
  repository, and both were changed there on 27.08 without ever being pushed, so GitHub held the
  05.08 version while sessions read something newer. The window that owns `~/.claude/playbook` has
  since pushed; that repository now reports nothing ahead of its remote.

- **Two of his rules live only in the retiring playbook document. Found 31.08, in q-800; closed
  03.09.** Checked against the whole pack and found in no skill: that every plan names the parts it
  must not touch, which that document calls the cardinal sin (not "the cardinal mistake" as first
  written here — the playbook's own word for it, `PLAYBOOK.md` "Plan first", is corrected on
  landing), and that his "what's the point" or "what a mess" means stop editing and go look at the
  rendered output. Both now have one home in the pack: the first is
  `skills/live-spec-base/SKILL.md` rule 37; the second is folded into rule 22 (convergence), which
  already pointed at this same playbook chapter as the principle's fuller telling. Citations for
  both live in `skills/live-spec-base/references/rule-origins.md`. Neither rule is stated only in
  the playbook document any longer.

- **Four personal hook overlays, two arrangements. Found 31.08, in q-800.** The scanners read
  `~/.claude/hooks/`, where all four overlays sit. Two of them also exist as identical tracked copies
  in the playbook repository, kept in step by hand, and the other two have no versioned copy at all.
  The clean form is the one the profile already uses — the files live in the repository and
  `~/.claude/hooks/` holds symlinks. That edits armed hooks, which law 1 forbids while this plan
  runs, so it is written down and left alone.

- **The suite is red on five checks because the reviewing skill on this machine is three releases
  ahead of what this project pins. Found 31.08, at the merge.** The external reviewer lives in its
  own repository and was released three times today, up to 1.6.0, which reworded two of its rules and
  moved a third of its body into side files. This project's own build pins it at 1.4.2, installs that
  version before it runs the checks on the server, and is green there. The copy installed on this
  machine is 1.6.0, so five checks that quote the older wording fail here and nowhere else. Nothing in
  the work of today caused them and nothing in this project can repair them: the choice is to move the
  pin up and reword those five, which is its own piece of work, or to put the local copy back on the
  pinned version, which would change a repository this window was told not to touch while another may
  be working in it. Left as it stands, named here, with the server's green as the honest reading.

- **A role-profile brief layer for workers was proposed and never entered the pack. Found 03.09, in
  `inbox/2026-08-08-profile-briefed-worker-ab-result.md`; closed the same day.** A blind A/B from
  tlvphotos (08.08) gave the same mechanical task to a worker briefed with a short role profile plus
  the project's design charter and to a worker briefed in plain engineering words; a blind judge
  found the profiled arm won on vocabulary, documentation truth, and integration. The rule now lives
  in `skills/live-spec-base/SKILL.md` rule 7, as a sub-rule beside the worker-restore clause: a
  worker's brief for a project holding a design charter or design language of its own adds a short
  role-profile layer — identity, the charter as sole naming source, an escalation interdict for
  taste calls — on top of the functional brief, never instead of it. Citation and full incident
  record: `skills/live-spec-base/references/rule-origins.md` under rule 7. `director`'s own text
  ("A specialist gets a brief, not a copy") already points at the base rulebook for the shape of a
  brief and needed no change. The finding moved to
  `inbox/handled/2026-08-08-profile-briefed-worker-ab-result.md`.

- **The rule that a human verdict is a movement end, written into resume files the same minute, was
  proposed and never entered the pack. Found 03.09, in `inbox/2026-08-08-verdict-lands-same-minute.md`.**
  From tlvphotos (08.08): a rejection arrived mid-conversation, the session spent two hours on the
  design dialogue it triggered, and the resume files still said "awaits his walk" until an adversarial
  reviewer caught the gap. The proposed rule — a verdict on shown work ends the judged artifact's
  movement on the spot, amending the resume files in place rather than appending — names no skill or
  spec line in this pack; tlvphotos fixed its own charter and memory, but the pack-wide rule was
  never written.

  **Resolved 03.09.** The rule now lives in `skills/director/SKILL.md`'s closing-work section,
  directly under "A shown result closes the work" — the paragraph beginning "For the taste calls
  rule 12/27 reserve for him, his verdict... is itself the movement end for the judged artifact,"
  citing the 2026-08-08 tlvphotos incident by date, with the amend-in-place corollary stated in the
  same paragraph. `inbox/2026-08-08-verdict-lands-same-minute.md` moved to `inbox/handled/`.

- **`scripts/preshow-register-lint.py` still ships to no host tree; `guardrails/spec-coinages.json`
  now does. Found 03.09, in `inbox/2026-08-12-preshow-lint-script-missing.md`.** tlvphotos reported
  both files named by its session law (the preshow register check, the coinage list) missing from its
  own tree. `adopt/install-style-gates.sh` (added 02.09) now vendors `guardrails/spec-coinages.json`
  into a host at adopt time; no installer vendors `scripts/preshow-register-lint.py`, so the law that
  names it still blocks nothing on a host that has never run that installer.

  **Resolved 03.09, same day.** `scripts/preshow-register-lint.py` joined
  `adopt/install-style-gates.sh`'s `VENDOR_FILES` right beside `guardrails/spec-coinages.json`, same
  copy mechanism, same manifest pin, same `--force` idempotency — proven by
  `tests/test_style_gate_kit.py::TestStyleGatesInstall::test_install_vendors_the_gate_files_and_pins_each_source`,
  whose `VENDOR_FILES` tuple now names it too. A second gap surfaced checking both walks per this row's
  own ask: `install-style-gates.sh` was a founding-only step (`adopt/ADOPT.md`) that the catch-up walk
  (`MIGRATION.md` Phase 4) never re-ran, the identical shape plan-14 found and fixed for
  `install-status-view.sh` hours earlier — so an already-adopted host would still never receive either
  vendored file. Phase 4 now re-runs `install-style-gates.sh --force` beside `install-status-view.sh`,
  proven by `tests/test_catchup_walk.py::TestCatchupWalkVendorsTheStyleGateKit`. The inbox report moves
  to `inbox/handled/`.

- **A promise this range added is owned by nobody, and the check that would demand an owner cannot
  see it. Found 31.08, in the merge review; resolved 2026-09-03, in q-813 — the mechanism it named is
  gone, not merely fixed.** The idea shelf — where a possibility named in passing is kept in the
  person's own words — was written into the spec and marked as not built, correctly, since no file
  held one. The check that makes every such promise name an open task read the marker by the line
  above it, and that marker sat under a heading rather than under a numbered line, so the check never
  saw it and asked for no owner. His own correction on 2026-09-03 forbade the mechanism outright — no
  second list, ever, not even a shelf — so q-813 retired Requirement 315 (the idea shelf itself, `E-37`,
  `INV-320`) whole: `grep -c "Requirement 315" spec/message-first-read.md` now reads 0, and the
  retired text sits at `attic/spec-message-first-read-R315.md`. There is no longer a promise for the
  ownership check to miss.

- **The plan's own page carries two stale pointers into files that moved. Found 31.08, in the merge
  review; closed 2026-09-03.** Two lines here name a line number inside the rulebook and inside the
  reading skill, and both moved when those files were edited 31.08 (off by two and by eight that day;
  further edits since had widened both gaps by the time this closed). Fixed by checking each file's
  current content against its own citing sentence: the thrift-discipline rule (q-584) now sits at
  `skills/live-spec-base/SKILL.md:226`, not `:261`; the decision-sheet section (q-816's own citation)
  now spans `skills/director/SKILL.md:225-271`, not `:205-249`. Both corrected in place.

- **The reading skill changed and its score did not, so a ticked task stopped proving itself. Found
  31.08, at the merge; resolved 2026-09-03.** The task "a question you ask never turns into a task" is
  ticked, and its acceptance command asks that the recorded runs of the reading be newer than the
  skill they grade. Commit `98a003b5`, the one-home landing at 13:55 on 31.08, edited the reading
  skill; the runs stayed the ones recorded on 26.08, and further edits to the skill kept the gap open
  through today. `evals/director/traces` was fully re-recorded today (commit `56611b76`, "Director
  eval: full re-record of both sets against today's skill edits") after every `skills/director/SKILL.md`
  edit made today: `test "$(git log -1 --format=%ct -- evals/director/traces)" -ge "$(git log -1
  --format=%ct -- skills/director/SKILL.md)" && echo FRESH || echo STALE` prints `FRESH`. The score
  printed at every session start proves the skill as it stands again.

- **The other half of the same promise has no row. Found 31.08, while giving q-437 its one back;
  closed 2026-09-01.** The spec keeps two things promised under one sentence: the recursive
  similarity sweep, which is q-437's, and the step that forces an author to name the value in
  between the two obvious ones on each variation a product is rendered under — a tablet that
  carries touch and a pointer at once, between a phone and a desktop. That second half was q-436,
  folded into plan-12 on 27.08 and never worked either. plan-12 has closed. Only one row can own
  the promise in the map that keeps promises honest, and q-437 owns it, so nothing goes red; the
  value-space step is simply owned by nobody. q-436 got its own row back, and it built and closed
  the value-space half 2026-09-01: the duty is written into `skills/spec-author/references/facet-sweep.md`
  beside q-437's, `skills/product-prover-pack/SKILL.md` reads a co-occurrence value left unnamed as
  the same blank-answer class, and `spec/design-spec-review.md` Requirement 265 criterion 15 names
  the built step in place of the old "promised as a later increment" line.

- **The decision sheet's own ordering line waits for a session outside a worktree. Closed 31.08.**
  Your word of 27.08 gives the ordering to the first read: it brings work together, runs it side by
  side, and ranks it. The law now has a home — the spec states it and the architecture gives it a
  node, and the order itself is read off the states this page records, by command. What is still
  missing is the line on the decision sheet itself, the one that says which open piece runs next and
  why that one. Adding it edits a skill file, and the installed copies of the skills then differ from
  the source until `scripts/sync-skills.sh` runs. That command writes outside the project's tree,
  which a lane working in a worktree may not do, and running it while other windows are live would
  change a skill under a session already reading it. It was written, the suite went red on the drift
  by name, and it was taken back out. A session working in the main tree put it back the same day:
  the field is on the sheet, `scripts/sync-skills.sh` refreshed ten installed skills, the health
  check that reds on drift runs green, and the spec claims the field again.

- **The amended bar for "queued" stands, and the twenty-one definitions stay as written. Settled
  31.08.** The rule at the top of this page lets a session move a task's status and write in this
  section, and says a task's wording changes only on the owner's explicit say-so. On the evening of
  28.08 one session rewrote what finished looks like on twenty-one open tasks, widened the bar for
  what counts as queued, and cut about 1,500 words of accumulated history out of one task's body.
  Nothing among the checks watches that rule, so nothing stopped it, and two sessions that evening
  read the rule opposite ways.

  What settles it is the resolution order the owner's own profile states: his live word wins, then
  the host profile, then this file, then the package defaults. His word of 28.08 00:53 opened that
  run with "run the plan to the end, ask me nothing, wait for no word of mine", and he said it again
  on 31.08 12:12. A live instruction to proceed without him outranks a clause in this file that
  requires him. So the work stands on its own merits: the twenty-one definitions came back from the
  archive an earlier merge had dropped them into, the widened bar lets five honestly unmeasurable
  tasks stay on the board, and every one of the 1,500 words is findable under its own date. The
  handful of factual lines the repair pass corrected outside the two it allows stand with them — the
  task-count command that had been counting its own line, the photo site's finishing test that asked
  only that a version file exist and never read it, two closed rows that now say where their proof
  was read, the session-weight figure stated in the present tense while the real one had moved, and
  the rotated-off list that named none of the three archives written that day.

  One thing is worth the owner's eye whenever he next reads this page, and it is not a question that
  holds any work: the consent clause above and a standing "do not ask me" grant collide, and the
  clause says nothing about which wins. It should name what happens under such a grant, so the next
  session does not have to derive it the way this one did.

- **The boot file's stale example is repointed. Settled 31.08.** It told a session not to read the
  root prose to orient itself and named three files to leave alone; one of the three was the old
  wish queue, which moved to the attic on 28.08. The line stayed true and its example was a ghost.
  It now names the architecture document instead, which is large, sits in the same root, and is
  exactly the kind of file a session opens by mistake. Nothing else in that file changed. The
  standing word that nobody here writes it is about not putting working-mode instructions into it;
  repointing one filename that has moved is a correction of fact, so it does not reach that rule.

- **The two tasks that left the board while a worker still had them are closed. Settled 31.08, on
  the evidence written out below.** Neither goes back on the board: the first is finished on this
  side and waits only on the owner's own look, which the live-board task already carries; the second
  shipped on 13.08, and what it left undone aimed at a page belonging to a campaign that is over.
  What happened, in full: the morning cut folded four rows into the one-list task and moved them to
  `docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md`; two of the four were marked as being
  worked at that moment and neither carried a note saying so. Both were read back on 28.08 evening.
  The first, the light view of where things stand, is finished on this side: the opening report and
  the board page both draw off this file and a test fails if either stops finding a task. Its last
  leg is your own look, and that is the same look the full live board already waits on, so it is not
  lost. The second, the project's goals carried as numbers anyone can re-run, landed on 13.08 as
  `.live-spec/goals-under-watch-2026-08-13.md` — seven goals, each with the command that measures it
  and its value that morning. What never ran was the second half of it, a sweep of the older
  transcripts for goals stated and forgotten; and the page it would have updated belongs to the
  culling campaign, which is over. So the half that is left has no live home. Nothing is being put
  back on the board for it. If you want the project's goals under continuous watch as a standing
  thing, that is its own ask and it comes back as its own task.

- **The method still teaches every new project to keep the queue this one retired, and it is now a
  task rather than a finding.** Eleven files across the skills, the templates and the joining walk
  carry it, and rewording them is a release with a version number and a migration note, not a
  tidy-up. It went on the board on 31.08 as `q-801`, with what has to be answered before the
  rewording starts written into the row.

- **Nothing moves a finished task off the board except a person's own hands. Settled, and now
  written into this file's own rules.** The tool that used to do it understood only the table the
  retired queue was written in, and it went to the attic with that queue on 28.08 rather than being
  taught a shape nobody travels often. What it guaranteed by construction — the archive and its
  pointer written as one act — the push gate proves instead, in both directions, so a hand that
  writes one half is stopped there. The rule was only ever recorded here; on 31.08 it moved up to
  the rules at the top of this page, where a session reads it without opening §Blockers.

- **Every done mark was re-checked against the tree, 28.08 — five of them did not hold.** Two rows
  are back open: the list of every made-up number, where a sweep ran but the page nobody has read
  was never written, and the stale pointer in the test list, which went stale a second time when the
  rule it points at moved house. Two rows stay closed with a line saying their subject was removed
  after the work shipped, so there is nothing left to guard. One row keeps its closed mark and loses
  a stale line that said it was waiting on the owner — his own word of 27.08 had already taken that
  question off his desk, so the line contradicted him. Fifteen open rows got their definition of done
  back from the archive, where the 27.08 merge had dropped it; not one of the fifteen is a command,
  so they all still fail this file's own bar for queued, and rewriting them is a separate pass. They
  came across word for word, with one change in three places: the owner's own name, which the rest
  of this file does not use and the shipped-text check refuses, now reads the way every other line
  here reads.
  Eleven closed rows now compute their own mark; nine more say in one line who read them and where,
  because their result is prose or a measurement and no command can read it. **One thing to know:**
  the cost-per-step audit closed on a measurement taken elsewhere, and the page its own acceptance
  asked for — every fixed step with its price and who demanded it — was never written.

- **Every open task now says what finished looks like, and the bar for "queued" was amended to let
  five of them be honest, 28.08.** The seventeen tasks whose definition of done came back from the
  archive earlier today were sentences, and this file's own bar said a queued task owes a command.
  Twenty-one of the twenty-six open tasks now carry one. Five cannot and should not: the live board,
  the front page, the page of every number in the product, the measurement of how much of the test
  suite could ever fail, and the question of whether the playbook repository earns its own home.
  Each of those finishes in something a person reads and judges, and a command over them would only
  restate the words. So each says in one line that no command decides it, who reads it, and what
  would convince them. The bar itself was moved to allow that, and the reason first written down for
  moving it does not hold. Two passages were named as already providing for the opposite. Only one of
  them does: plan-10's second bullet, written on 27.08 at 15:07, three hours before the bar, which
  already made room for a step whose result needs his own eyes. The other, the closing rule under
  "Words used here", was written by this project at 15:31 on 28.08 — hours after the bar and hours
  before the amendment. It is this same day's work here, so it stands as no older authority and can
  carry no weight as a reason. The authorship was named wrongly too. His own refinement on 27.08 was
  that queued means accepted into work, clear what to do and well formalized; "done is a command" is
  this project's reading of that phrase, and those are not words he used. So what moved was this
  project's own formalization.
  **This is the one thing on this list that waits on him.** The bar now reads: a task is queued when
  its links point at something real and a reader can tell finished from unfinished without asking
  anyone, with a command wherever a command can decide. The stricter reading that stood before wants
  a command from every queued task, and putting it back takes the five rows above off the board as
  unformed ideas. Either bar is workable; one line from him settles which. Until then the softer one
  is what the file carries, and the five rows stand. One task also
  left the board entirely, the personal-settings leak: its own text says this project cannot reach
  the cause, so nothing here could ever move it from undone to done. It is in
  `docs/queue-archive/rotated-PLAN-2026-08-28-no-reachable-outcome.md`. Two tasks lost a line saying they
  waited on his word — what counts as a cleared mistake, and three wording disagreements in the
  rulebook — because his own word of 27.08 puts machinery on this seat's desk, and both are
  machinery; the wording row keeps its title, since titles are his. One task's definition of done
  stood on machinery deliberately removed in `e61b29b7` and was rewritten to the part that still
  stands. And the live board's definition of done, which had grown to some 1,500 words of
  accumulated history, is now the outcome it asks for, with every widening still findable under its
  own time in `DECISIONS.md` and verbatim as row 166 of the merged-queue archive.

- **The board was cut from 162 rows to 63 on 28.08, on his word.** His word that morning, 11:48:
  keep what is needed, archive the rest, only a handful should remain. Ninety-four rows the 27.08
  pass had folded were still standing on the board carrying a `Covered by:` line; they are now off
  it, in `docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md`, and every row that absorbed
  them carries one line naming which ones and pointing there. Five more left as stances rather than
  tasks, in `docs/queue-archive/rotated-PLAN-2026-08-28-no-acceptance.md` with the criterion written
  out. Three were found already shipped and marked done against the file that ships them: the text
  checker as its own skill, the settings list, and the installed-versus-working-tree check.
  Twenty-six tasks stand open, after the three repairs that landed later that day.

- **The nine compressed folds, resolved.** This line used to record that the 27.08 merge cut nine
  folded bodies past a fact each still needed. All nine were read against their fold target on
  28.08. Four stayed on the board and now carry, in their own row, the fact the target does not
  cover: q-490, a live hole in a legibility check that ships · q-567, the safety checks that do not
  install into a host · q-586, a sixth restore form the guard cannot see · plan-10, whose acceptance
  is its own. Three were covered after all and are archived: q-550 by q-497, q-170 by q-458, and
  q-552 by the spec split, which removed the second copy of the table that row was about and left
  the gate at `guardrails/pre-push:278` comparing the one that remains. q-405 was archived on his
  word of 28.08, in `docs/queue-archive/rotated-PLAN-2026-08-28-q405-agent-messaging-stale-premise.md`, and q-396
  goes with it under the same word, since agent-to-agent messaging already works in the harness. q-605's discarded bytes were `guardrails/rule-census.json`, generated output
  of `scripts/rule-census.py`; both were retired and neither is in the tree, so there is nothing
  left to have lost.

- **q-586, the one live defect this cut turned up, is fixed as of 28.08.** The guard that refuses a
  command destroying unsaved work used to name five forms, and a worker writing a file back out of
  `git show HEAD:<path>` walked past all five — the very command the guard's own refusal text told
  the reader to use for recovery. It had already cost two files once, on 2026-08-09. The guard now
  judges where the bytes land instead of matching words, so the redirected and piped assemblies are
  refused with the direct ones, and the refusal recommends printing the saved copy and writing the
  file with the file-writing tool.

- **27.08 afternoon, what this session established and what it left.** Six steps were added on his
  word (10–15) and four things landed: the queue went from 236 rows to 142, with 94 rows archived
  verbatim as declined because a provenance audit showed they traced to no instruction of his; the
  build-status sentences left three spec files; the migration wishes for tlvphotos and promoter sit
  in those hosts' own inboxes; and `spec/work-board.md`'s claim that nothing of the board is built
  is gone, since a gate, tests, a matrix and a rendered page exist beside it.
  **Take step 10 before step 9.** Four of the first ten steps carry no acceptance command, so their
  closed marks rest on a session's word. Running a migration before the marks are computed adds one
  more "done" nobody can check.
  **Open, his to answer, small:** three rows still marked held for the owner carry questions put to
  him and were kept out of the purge · six rows have no traceable origin, four of them labelled as
  his word with no quote or date, and he may recall what they were · where `lab/CROSSING-BRIEF.md`
  belongs in tlvphotos, which he answered in part today — it is spec material, and it went where it
  went because of the three-week emergency, so the conversion decides its home.
  **Found and not acted on:** promoter has no push gate wired at all, `core.hooksPath` unset and no
  hook file, while carrying vendored gate scripts · the seventeen declared feature names cover 29 of
  308 requirements and four of them describe nothing real, which step 12 takes up · director ranks
  nothing and nothing else owns the ordering law, which step 12 also takes up.

- **Gate i settled, and the session's own stopping-short corrected (27.08 morning, his word).**
  The night before, this seat held gate i open as "needs his decision" while sitting on his
  explicit standing permission from 00:49 ("push and deploy allowed, don't wait for me, don't ask
  for my word"). He came back with the obvious question — are we fixing it or did you just stop
  without finishing. He was right; the answer was derivable and the permission was already given,
  so holding it was the defect, not the caution. Recorded here because the same shape will recur:
  a standing permission covers the class of decisions it names, and re-asking inside that class is
  a way of not working. Settled by the mechanism the gate itself points at — two `name_waivers`
  entries in `scripts/shipped-language-allowlist.json`, each scoped to one file and to the exact
  hyphenated directory token, since renaming the real host directory would break every live
  reference to it. Proven narrow rather than asserted narrow: a plain personal name in those same
  two files still reds, and the token still reds in any file the waivers do not name — guarded by
  `tests/test_shipped_language_waiver_scope.py`, run against the real allowlist data.
- **The product speaks to its owner in codes, and the README promises it never will. His own
  words, 27.08 09:37, after two sessions of this.** He asked what the check is, what it protects
  and why it exists, and said plainly he is not going to go read the code to find out — then
  pointed at the README to ask who this pack is built for. The README's answer: a single author
  who says things in passing, types nothing after setup, opens none of these files, and is asked
  only about taste, strategy, authority and the irreversible. Measured against that, two separate
  defects, and the smaller one is mine: this seat reported to him in gate letters, requirement
  codes and file:line pins for two sessions running. The larger one is the product's: when the
  push gate refuses, it prints a gate letter and a requirement code as its reason. The person who
  owns this product hit his own product's refusal and could not tell what it wanted. A refusal
  message is the one piece of this pack a person is guaranteed to read, and it is written for an
  agent. Worth fixing at the source rather than translated case by case in chat.
- **The plan holds live shell commands, and that is the thing to remove.** Prior recommendation
  here was to carve a gate exception for plan-only commits whose diff touches no `<!-- check: -->`
  line. That is a patch at the symptom. The root fact is that a status board — the file where a
  session ticks a task and writes a blocker — can carry commands that run on every machine at
  every session start. Take the commands out of the plan and put them where the probe's own logic
  lives, and the plan becomes genuinely inert prose; then it needs no clever exception, because
  there is nothing left in it worth reviewing before a push. That removes machinery instead of
  adding a rule to it. Not done — it changes the tool he runs every morning, so it gets shown
  before it gets built.
- **The plan says it is outside the gates; the gates have never known that. Recorded 26.08,
  parked on "his word" three times since, and the parking was the error.** `PLAN.md:59` states
  this file sits outside the jurisdiction of the format rules, the prover and skill-review, and
  needs no records. Gate a knows nothing of it, so a commit that only moves a task's status or
  adds a §Blockers line demands a full adversarial push record — which is what made closing a
  range chase its own tail twice this morning. Provenance, checked rather than assumed: that
  exemption sentence was written by an agent session (`8f69a7c8`, 26.08 17:53), never by him, so
  it is not his word and cannot authorize anything on its own. The rule that kept sending this
  question to him is `PLAN.md` law 1's clause forbidding edits to existing gate config — also
  agent-written, added `b3f1008f` 26.08 18:32, for a sound reason its own commit message states:
  law 1 had banned creating gates while leaving an agent free to silence one by writing itself
  into its allowlist. That is a real anti-self-dealing rule, and this session did exactly the
  thing it guards against this morning (the gate-i waiver). The defect is narrower: the rule has
  no path for "the gate is factually wrong," so every false positive becomes a wake-the-owner
  event.
  **What blocks a simple fix is a finding worth more than the gate question.** `PLAN.md` is not
  inert bookkeeping: its `<!-- check: ... -->` comments are executed as shell by
  `scripts/state-probe.sh:52-58` (`subprocess.run(..., shell=True)`) at the start of every
  session, since the probe is the first command a session runs. So a `PLAN.md`-only commit can
  change what runs on every machine that opens this project, and blanket-exempting the file from
  review would hand an agent a recordless path to arbitrary execution — the same class of hole
  law 1's clause was written to close. Recommendation, for whenever he wants it: exempt a
  `PLAN.md`-only commit from gate a **only when its diff touches no `<!-- check:` line**, which is
  mechanically decidable and keeps the execution surface under full review. Not built yet.
- **Open, smaller, and nobody's word needed yet — a shipped pack script carries one person's
  project roster.** `scripts/state-probe.sh:159` loops over five hard-coded host directories that
  are this owner's own projects. It ships to every host that installs the pack. The gate-i waiver
  above stops it reading as a leaked name; it does not answer whether a pack script should carry
  that list at all, rather than discovering hosts or reading them from local settings. A design
  question for whenever, recorded so the waiver's own note points at something real.
- **Adversarial review (Opus), his own request tonight — real regressions caught, fixed, verified.**
  Found: tonight's 4 test-guard removals were all wrong (see the corrected entry below) and one of
  them had turned `tests/test_traceability.py` red — reverted. Found and fixed: two real bugs in
  `scripts/director-wire-report.py` (a false "covered" reading on a multi-line document list, and
  a field-label mismatch against the skill's own worked example), plus a missing
  "never wired into pre-push or CI" test. Found and corrected: several wrong numbers and stale
  line-pins in tonight's own PLAN.md writing (file counts, a decision-sheet line range, a
  requirement citation, a corrections count) — see the corrected entries below. Found, not tonight's
  doing: `tests/test_no_history.py`'s clean-corpus fixture pointed at a file step 3 deleted the
  night before — fixed, repointed to `spec/roles-and-agents.md`, 5 passed. Found, left alone:
  `tests/test_deletion_only_push.py::test_content_push_falls_through_to_the_ordinary_chain` is a
  pre-existing flake under load (a 3-second timing window) — not touched, out of scope for tonight,
  his to decide whether the timeout is worth widening. Everything above is fixed and re-verified by
  command, not by the review's word alone.

- **Machinery inventory, his second question tonight, answered — corrected after adversarial
  review caught the first count.** 52 Python/shell files in `guardrails/` and 38 in `scripts/`
  (90 total; the first pass said 55/37, miscounted) checked for what they do and where they're
  actually called from — the real hook chain, CI, another script, or a test, not guessed from the
  filename. 87 of the 90 are load-bearing, reached from `guardrails/pre-push`'s own lettered gate
  sequence, from `.github/workflows/gates.yml`, or from a test that exercises them. 3 came back
  with no live caller: `scripts/render-board.sh` (reached only from PLAN.md's own prose — the
  board render step 1 asks for, a thing a person runs by hand), `scripts/
  install-separator-fence.sh` (its own header calls it a one-time installer, already run), and
  `scripts/apply-criterion-rewrites.py` (genuinely no caller anywhere, no note explaining why —
  the one real candidate for a closer look, left alone tonight). Why so many scripts and gates:
  mostly real work, not duplication — the push gate enforces around twenty separately-named
  invariants (case-purity, pin drift, prototype fencing, shipped-language, skill-review
  freshness, and more), each with its own small checker.
- **Director→pre-push wire: investigated, a read-only report built, the live skip waits for a
  spec change.** Director's decision is already persisted, in an existing home — every accepted
  piece of work gets a "decision sheet," including a "documents that must change" line, written
  into `.live-spec/checkpoints/*.md` under `## DECISION SHEET` (`skills/director/SKILL.md:225-271`)
  — and `scripts/checkpoint.py` already has a mechanical, closed-set test for "this line says
  nothing needs to change" (`_is_empty_body()`, line 59); closed checkpoints keep the section on
  disk. Gate (a) (`check-prover-record.sh`) demands one review record for the whole pushed range,
  with three named `STAND-DOWN` exceptions cross-checked against Requirement 226
  (`spec/guardrails-freshness.md:95`, criterion 6 at line 118) and enumerated by
  `tests/test_deletion_only_push.py` — that same test file's own comments record this exception
  list being over-widened and reverted at least twice already (`check-prover-record.sh:167-186`,
  the `recordless` class; and commit `2718c69`, a third exception criterion 6 never named).
  Letting Director's decision skip the record would need a fourth `STAND-DOWN` class and a new
  Requirement 226 criterion — a change to the spec text itself, his word on the wording, not built
  tonight. Built instead: `scripts/director-wire-report.py`, a standalone, read-only report, not
  called from `guardrails/pre-push`, `install.sh`, or CI and never affecting any exit code, that
  finds which commits in the pushed range are covered by a closed, in-range checkpoint whose
  decision sheet says nothing needs to change. The skip stays off. First version had two adversarial-
  review-caught bugs — a false "covered" reading on an ordinary multi-line document list, and a
  field label that didn't match the skill's own worked example — both fixed with regression tests
  proving each case; also added the same "never wired into pre-push or CI" test
  `test_no_history.py` already carries for its own gate, so that claim is a command now, not
  prose. Committed. One structural limit surfaces every run against this repo:
  `.live-spec/checkpoints/` is gitignored (`.gitignore:1`), so a checkpoint file is never itself
  part of any commit range — the report always shows 0 covered here, correctly, because git never
  sees a checkpoint file change. A future wire needs the decision to live somewhere git tracks.
  Also answered tonight, plainly: how Director's 33/35 score is computed (`evals/director/` —
  `scenarios.json` holds 35 fixed scenarios, `traces/*.json` hold one recorded live run per
  scenario, `check.py` runs a fast, model-free field-by-field comparison between them) and where
  it's fragile — the acceptance command only catches gross failure (a duplicate file, stale
  traces, a "0 of X" print), so a worse score would still pass the same green check; trace
  generation is a manual, unsynchronized step outside `check.py`, honest only while each run stays
  blind; and the expectations in `scenarios.json` themselves moved during the same cycle that
  measured against them (9 `corrections` entries, not 8 — corrected after adversarial review).
  Nothing here broke tonight; worth knowing before trusting the number again next time the skill
  changes.
- **His word tonight, 00:49: three open forks answered.** (1) Ceremony cancellation (the
  prover/skill-review record on every text edit) — parked exactly as it stood before tonight;
  his own reason: even a one-word edit ("removing 'не'" <!-- user-language -->) can flip meaning,
  so the "just a text edit" boundary isn't obvious and he won't guess it at this hour. (2) The
  Director→pre-push wire — authorized, build it, everything up to the tlvphotos migration
  (step 9). (3) Standing for
  tonight's session only, not a rewrite of law 1: do everything this session can, adversarial
  review at the end by Opus or Fable, close what can be closed, push and deploy on green, don't
  wait for him and don't ask for his word — he's asleep. Also on his mind, not yet acted on: he
  doesn't understand how Director actually gets checked/scored ("так много всего" <!-- user-language -->) · where the
  machinery is more than the job needs, and why there are this many Python scripts and gates ·
  an idea for later — measure how long a tagged task/subtask actually took, to estimate similar
  future work · onboarding as its own feature, explicitly tomorrow, not tonight · he's troubled
  that a fresh session's real load looks bigger than 42k now, maybe specific to this project's own
  "продолжай лайвспек" <!-- user-language --> boot jumping to ~120k — worth measuring for real,
  separately from step 7's
  13,163-token figure, which may not count everything a live session actually pulls in.
- **Step 7 closed — no target number, his own word.** 16,571 → 13,163 tokens (−20.6%), 13 of 34
  rules covered by neither an eval fixture nor a runnable script sit in
  `attic/live-spec-base-unbacked-rules-2026-08-26.md` (the glossary and the working skills are no
  longer 34 but 21 rules). His word tonight: no number to chase, best-effort stands, and the same
  standing killed two more unsourced guard thresholds pack-wide (see the number-sweep blocker).
  Checked personally: gate g (pin drift) is clean, the example on rule 14 (class hunt) — no
  guardrail/hook actually caught it. There were 17 reds from a deletion (law 4, "legitimate") —
  fixed the same night in a separate pass, not a rollback.
- **Step 4 done, informational read only.** Converged: senior/orchestrator/lead → "seat" (21
  files, tests green) · "briefed hands" → "briefed workers" · "a careful release hand" → "...
  release manager" · the bare metaphor "hand" in rule 2 rewritten with no metaphor ·
  "worktree"/"branch" in the whole-concept sense (not the git mechanics) → "lane branch" in the
  two places it confused. Left untouched: the worker-restore phrase baked in byte-for-byte under
  a gate (INV-299, 5 homes in sync — a separate task) and the live git mechanics (worktree and
  branch are two different objects, they need both words). Two flags for his eyes, whenever: the
  seat/a-seat overload the glossary already carries · `verify-step-detail.md` calling itself "the
  Director," possibly on purpose.
- **Stale law-10 note, kept for the record.** Earlier tonight, when 8 of 15 were still red, this
  line flagged that step 2's acceptance command only checks "no duplicate file," "traces newer
  than the skill," and "check.py doesn't print 0 of X" — not whether every scenario is green or
  accepted. That gap in the check itself is still real (it would go green on a much weaker score
  than 33/35 too), but the practical worry it named is gone now that the score genuinely is
  honest. Fixing the acceptance command's own looseness is still a
  separate PLAN.md edit, not this session tonight without his word (moratorium, law 1).
- **Push to origin/main: DONE, 27.08 09:27.** `a42c6fd2..8d6dba98`, 91 commits, the whole backlog
  that had been sitting local since 26.08. Full gate chain read in full rather than summarized:
  every gate green, then the real `git push`, then `git ls-remote origin main` confirming the
  remote is at `8d6dba98` and the probe reporting `matches origin/main` with 0 unpushed. The
  gates that had been red across the two sessions and are now closed: **i** (from 382 findings
  down to 3, then to 0 by the scoped waiver above), **e**, **s**, **h**, **m**, and **a**.
  **Correction, same morning, checked against the code rather than remembered:** this entry first
  claimed gate a needed teaching that "a range of pure records owes no record," and named that as
  a design task awaiting the owner. That claim was false, and citing his word for it was the
  second stopping-short of the morning. The rule already exists, implemented twice:
  `check-prover-record.sh:166-208` stands the gate down by name when every commit in the range
  touches only the record directories (the `recordless` class), and `check-prover-record.sh:313-329`
  drops record-only commits from the reviewed set when a record does exist. Nothing to build.
  What actually re-fired the gate each time was a `PLAN.md` commit, which the gate correctly
  treats as content — see the plan-versus-gate contradiction recorded separately below.
- **Step 3 done, informational read only.** Garbage deleted on his own word (yes, delete):
  `prototype/` whole at 4.2M, the 9 stale `docs/briefs` files (3 still-read ones kept), all of
  `docs/wishes`, `docs/director/`, `docs/gate-audit/`, and the closed-row checkpoint files (the
  3 tied to still-open rows kept). `docs/matrix-notes/` deliberately left — lower-confidence,
  never separately confirmed. Transcripts — 1,247 files, 310M, copied into `attic/transcripts/`
  (checksummed against the source), the originals in `~/.claude/projects/` NOT touched (the move
  was replaced with a copy — one of them is already cited by line number as a primary source, and
  Claude Code's autosaves read those same paths too). `.live-spec/PROBLEMS.md` gained seven new
  lines, Fable's read of a Sonnet worker's breakdown (one anchor quote re-checked by command) —
  his to glance at whenever, not a blocker.
- **One project's gate stops work in another.** `check-worker-restore.py` scans
  `~/.claude/projects` — transcripts from every project, the last 24 hours. A push in
  `~/tlvphotos` was blocked three times on 25–26.08 because of a `git stash` in live-spec's
  working tree in `/private/tmp`. Deposited:
  `inbox/2026-08-25-from-tlvphotos-worker-restore-gate-ambient-scope.md`. A live obstacle to
  the owner's work.
- **Step 2 pushed to 33/35, honestly.** His word tonight: close everything honestly green, ask
  Fable on the hard one, no new machinery. Checked by command
  `python3 evals/director/check.py --all`. Five skill-text clarifications and three fixture
  corrections (each backed by multiple independent blind-isolation runs, matching this corpus's
  own evidence bar) closed 7 of the former 9 reds, including the `halt-with-a-reason-worth-keeping`
  regression. Two stay red on purpose, not from lack of trying: `idea-with-a-cheap-branch` (a
  narrower residual than before) and `mixed-conditional-pause` — Fable found it genuinely
  contradicts two already-passing sibling fixtures (`halt-until-tomorrow`, `halt-without-the-word`),
  which want the identical pattern collapsed the opposite way; no single rule satisfies both
  without breaking a pass. Full reasoning: `docs/prover/2026-08-26-director-eight-red-scenarios.md`.
  Zero regressions across the full 35 plus the wider director-adjacent suite (324 tests).
  *Corrected 31.08: this note's number was not honest, though the session writing it believed it
  was. Only the nine reds of the day were re-drawn, so the 33 counted twenty-six scenarios against a
  skill version that had already moved. The full re-draw and the standing score are on plan-2's own
  row.*
- **Step 6, second sub-item done: the 22 "file exists" functions, looked at by eye, informational.**
  Under a strict reading (the entire function is presence/absence only — no content read, no
  subprocess return-code, no stdout check) only 10 exist, not 22: they guard that a shipped data
  file or a gate's own dependency (`guardrails/one-name-aliases.json`, `guardrails/weak-words.json`,
  the harness template, the skill-review and push-review record homes, and similar) actually
  ships, plus 2 that guard a sweep script reaps exactly the stale profile dirs it should and none
  it shouldn't. Every one of the 10 looks like a real regression guard against a shipped artifact
  going missing, not machinery guarding itself — none removed, none need removing. A looser reading
  that also counts "the file exists AND the wrapping script exits 0" (no text or content check)
  would roughly double the count toward the original 22 estimate; that widening is a scope call,
  not made tonight.
- **Step 6, first sub-item — already closed before tonight; tonight's attempt at it was wrong and
  is reverted.** The night before (26.08, commit `c3be01a3`, discovered only after an adversarial
  review) had already removed 16 of the 18 proven-dead guards and deliberately kept 2 — the
  footprint-read and adversarial-by-nature guards — because tracing their history past a file move
  showed real content edits `git log -S` alone can't see, exactly the caveat step 6 already names.
  Tonight worked from a day-old scratchpad without checking whether this had already happened,
  re-derived a "18 candidates" list that was 16 items stale, and removed 4 things: those same 2
  the prior session had already excluded for cause, 1 whole test function
  (`test_reconciliation_phrase_in_spec_author`) whose deletion turned `tests/test_traceability.py`
  red (`matrix/publish.md:11` still cited it as the test backing a BUILT row), and 1 measured
  against `PRODUCT_SPEC.md`, which no longer holds that phrase after the spec split — it moved to
  `spec/roles-and-agents.md`, where the phrase has 2 real commits, not 1. All 4 restored by
  `git revert 2c20f2f1` (commit `ca44edd4`); `python3 -m pytest` on the four files plus
  `test_traceability.py`: 223 passed. Nothing remains to remove under this sub-item — it was
  already done. Remaining under step 6: the 22 "file exists"-shape functions (looked at, 10 real,
  none removed — see above) · the ceremony cancellation (a gate edit, needs his word, moratorium
  law 1) · the Director→pre-push wire's live skip (also a gate edit, plus a spec-level change —
  see above).
- **Step 5 closed.** The prover's code mode is on `github.com/happysasha18/product-prover`,
  branch `code-mode-1.4.0`, commit `b71894a` — his word from 26.08 22:59 ("go ahead and push,
  don't wait for me"), received, the push done and personally re-checked (`git ls-remote`
  matches). Before the push it went through a real skill-creator run (found and fixed a real
  ambiguity in code mode's closing summary) and a readability read. Adversarial review by
  Fable/Opus was skipped on his own permission (his call whether it was worth doing) — the
  finding has already been re-checked twice. An adjacent finding stayed adjacent: `scripts/install-pack-hooks.sh:23-27` has no `*)` branch in its argument parsing (`--dryrun` instead of `--dry-run` silently installs the hooks for real) — not fixed this session (law 5), his word is needed on the finding itself, not on the push.
- **Settled 27.08 — the board question answered by him directly, so the sketch question is moot.**
  He looked at the rendered board and said what was wrong with it: the details behind the toggle
  showed raw markup, one card dumped its whole body onto its face while another did it right,
  subtasks wanted their own status, and the task names must match the plain list word for word,
  always. All four are fixed and the last is held by a test rather than by care. Two standing
  rules came with it and now live in the skill that governs showing work: a rendered page is
  offered and never opened unasked, with the plain list as the default surface; and one item
  carries one name across every surface. The older open question below — whether to build the
  full five-column feature with agent lanes and worker chips — stays exactly as it was, neither
  reopened nor closed by this, since the light view is what the plan asked for and what he has now
  reviewed.
- **The clock reaches sessions again — resolved, no action left.** The cause recorded below was a
  terminal launched with safe mode on, which disables every hook for the sessions it holds. This
  session gets its wall-clock stamp on every turn, so the condition is gone. Nothing was built to
  fix it and nothing should be.
- **`docs/director/capability-map.md` — gone, the entry is stale.** That whole directory was
  deleted by step 3's cleanup on his own word. There is nothing left to have drifted.
- **Which board sketch is approved — a candidate found, the owner's word not checked.**
  `docs/norms/work-board.html` (variant 8) is recorded as a frozen norm
  (`docs/norms/work-board.provenance.md`): approved 06.08 ~20:47, grown out on his own words
  until 21:16. This is the shape of the FULL "Live board" feature (spec `spec/work-board.md`,
  requirement 309: five columns, agent lanes, worker chips, time issued/left) — the very one
  after which, at 21:17 that same evening, he said he genuinely didn't understand what it was
  about or why, while the 26.08 plan asks only for a light view with columns over the Canon. Today's `scripts/render-board.sh` doesn't build that norm — it renders PLAN.md in 4 columns, using only the fields present in its own data (title, description, status, details), with no workers/lanes/time, which aren't there. Three files `work-board-mockup-2026-08-06*.html` sit outside git (in `.gitignore`), `prototype/work-board-sketch.html` is the older one (variant 2), called "so-so" tonight. Recon: `docs/research/2026-08-26-board-ticket-fields.md`. Needs the owner's word: build requirement 309 later as a separate decision, or leave it a frozen norm with no build.
- **The unclosed branch `p2-change-classifier`, declined 03.09.** Builds a second file-path-based
  classifier for the push gate's own review-scope decision — exactly what this file's own "Already
  decided" section forbids ("building a second classifier by file path is forbidden — the model
  decides meaning, code decides mechanics"). Archived whole rather than merged:
  `attic/prototypes/2026-08-13-p2-change-classifier.patch`, manifest line in `attic/MANIFEST.md`.
  One separable idea inside it (a noclobber lock serializing two concurrent `pre-push` chains) is
  not itself forbidden and stays on the shelf, unbuilt, until that race is actually hit. Six other
  stale, fully-merged worktree directories (five `agent-*`, none carrying a commit not already in
  `main`) swept the same pass — pure litter, no content lost.
- **`build-pipeline` is still listed as the pipeline's owner** in `TEST_MATRIX.md`,
  `ARCHITECTURE.md` and its index, `MIGRATION.md`, `skills/spec-author/SKILL.md`, and six closing
  rosters. No gate catches this. A separate design task, not a one-line fix.
- **Global hooks were cut 26.08 at 09:28** from ~10 to 4; the meter `hook-meter.py` was also
  removed. Backup: `~/.claude/settings.json.bak-2026-08-17`. Decide what to bring back.
  **The cut was blanket, not a verdict on any one hook** — this line already said so before today,
  and the meter's own reading from 11.08, taken before the cut, answers the "what to bring back"
  question with real numbers rather than a guess: `scissors-scan.py` fired 131 times in 3,288 runs
  and `affirmation-scan.py` 37 times in 2,612 — both caught real things at a real rate, and both are
  the same shape of check plan-16 is already about to build for the "fact stated, not announced"
  rule. `hedge-scan.py` fired 4 times in 3,023 runs — under this project's own retirement law (a net
  silent past its window is a candidate, `.live-spec/r3-rule-fires-2026-08-11.md`), that one is a
  candidate to stay retired, not to return. Bringing back two of three, on the numbers, is a
  decision to put to him rather than one this session makes alone.
- **Why time doesn't reach the session — found, not cleaned up.** `~/.claude/hooks/clock-hook.sh`
  prints the time correctly by hand; but this session's parent process (`PID 12188: claude
  --safe-mode`) sets `CLAUDE_CODE_SAFE_MODE=1` — per `--help`, safe-mode disables every hook,
  skill, CLAUDE.md, and MCP server for the sessions it holds. This is a terminal-launch choice,
  not a pack defect and not a reason to add a hook; the fix is that the owner doesn't start
  live-spec work from under a `--safe-mode` window (or explicitly decides to keep it that way and
  live without a clock in replies).
- **plan-17 closed: a session's real starting weight, measured; the ponytail question, answered
  without installing it.** The old "required context" line counted two skill files and missed the
  boot file and profile that also load every session — real floor measured 17,575 tokens on 27.08,
  and 17,676 on 28.08 as the pack grew; the opening report prints today's figure (was reported as
  14,294). On top of that floor, the boot instruction told every session to read `PLAN.md` whole:
  30,815 tokens, before any task-specific reading starts. `scripts/plan-step.sh <id>` now opens one
  task's own section (a few hundred tokens) instead, and `live-spec/CLAUDE.md` points there instead
  of at "read it whole." Ponytail: declined, not deferred. His own source note already carries the
  numbers — an independent benchmark found it worth about a tenth off cost against a claimed fifth,
  and it works by injecting its ruleset into every session. That is new fixed weight added to the
  same floor this item just cut by two-thirds; a benefit smaller than claimed does not clear a cost
  added to the thing being shrunk.
  **Found while closing it: the fold overclaimed.** plan-17's own "Closes:" line names eight ids;
  four are real duplicates of "a session reads only what it needs," including q-568 itself, the
  00:17–01:10 cost audit this row's own text traces to (q-570, q-584, q-205, q-568), and are closed
  with it. The other four — q-575 (test tempo), q-507 (expensive AI help used sparingly),
  q-457 (weekly spend tracked, cheaper workers used more), q-140 (what to trim when money or time
  run short) — are distinct budget questions the 27.08 relevance pass folded into this row without
  this row's work touching any of them. Left open, unclosed by this session; the "Closes:" line
  itself needs a correction this session has no standing to make (PLAN.md's own rule: a task's
  text changes only with the owner's consent).
- **q-489 is the same overclaim, one row over.** (It had no definition of done when this was
  written; it gained one at 18:08 the same day, so that half of the complaint is settled and the
  sentence saying so is gone.) Its "Closes:" line names nine ids (q-217,
  q-492, q-230, q-454, q-455, q-220, q-525, q-490, q-576); read all nine — they are nine real,
  distinct pieces of work (check-quality proofs, a self-improvement schedule, drift re-checks,
  periodic deep re-reads, mining past sessions for lessons, a rough-day audit, a measurement
  that refuses to fake a zero, a contrast-check fix that's largely done, and invented numbers),
  not nine phrasings of one task. Not closing q-489 itself, and not inventing a single
  acceptance line to paper over nine different ones. `q-576` (invented numbers) is being worked
  now on its own merit, marked 🔄 by someone before this session and independently real — a
  sonnet worker is sweeping scripts/config for ungrounded numeric thresholds now; the sample
  checked by hand first (spec-debt-cap.json, register-lint-floor.json) was well-governed, so
  this may turn up few or no findings, and the count will be reported honestly either way.
- **The sweep landed: 45 ungrounded numeric thresholds, real, not a fishing trip.** Scope:
  every scripts/guardrails/hooks/templates file plus every JSON config, PLAN.md and prose
  excluded. 15 constants already properly sourced (the house style, done right, when it's
  done); 45 bare thresholds with no incident or derivation behind them (mostly judge/lint
  tuning windows and timeout/retry budgets); 9 genuinely unsure, flagged rather than guessed.
  Not fixed yet — 45 real judgment calls is its own body of work, continuing.
- **q-527, q-529, q-536 were never his to decide — his own word tonight, and it checks out.**
  All three carried `👁️` ("needs his eyes"); all three trace to `Source: found <date>`, not an
  owner quote — see [[only-his-dated-words-are-law]]. His ruling, verbatim: machinery is this
  seat's to decide, ask only if he personally set the machinery up himself; recorded properly
  in `~/.claude/playbook/inbox/2026-08-27-from-live-spec-machinery-deferral.md` (a cross-project
  file, not an edit — this window doesn't write to the playbook repo directly) rather than a
  new pack rule, since `profile.md`'s existing `deferral` bullet already covers it and only
  needed the machinery case named. Re-marked ⬜ (q-527, q-536) — real, unresolved, just not his
  — and ✅ (q-529): its own root cause traced to `scripts/rule-census.py` /
  `guardrails/check-doc-findings-bound.py`, both retired since the 2026-07-29 report that found
  it; the systems that replaced them (`guardrails/check-size-ratchet.py`, `spec-debt-cap.json`)
  require a human-edited reason alongside every threshold change by construction, so the
  "a reason survives the raise it excused" bug the report described cannot recur in the current
  design. q-536's own "three wording disagreements" could not be pinned down to three specific
  items — the 2026-07-30 readability-pilot findings it points at run to 40+ items across two
  archived docs, almost all already resolved in a rewrite since, and three weeks of subsequent
  readability work make most of what remains open a stale read of files rewritten since. Not
  closed — a real recount would need to re-read the current source against each remaining
  candidate, not this session's guess.
- **q-576 swept, not closed: real fixes landed, all of it decided.** Worker finished, verified by
  hand rather than taken on its word — see `.live-spec/checkpoints/q576-invented-numbers-sweep.md`
  for the full account. Of the 45: 6 removed as dead/invented/stale (including a config that
  outlived the code that read it), 12 really grounded (a judge timeout that was genuinely broken —
  25s under its own measured 33s call cost — is fixed and installed live), 27 no source found —
  that's the finding, not a pending question, kept as engineering defaults and labeled as such;
  4 out of this repo's write-scope. Six files (`guardrails/check-worker-restore.py`,
  `check-runaway-child.py`, `reap_owned_group.py`, `language-rules.json`, `progress-baseline.json`,
  `scripts/spec-redundancy-precheck.py`) cited a `decision-dossier-2026-08-15.md` that was checked,
  in full, against the filesystem and git history and never existed — fixed on this session's own
  call: the false citations replaced with an honest pointer to the one real record from that day
  (`work/2026-08-15-unowned-numbers.md`), the actual values left untouched. No open question here
  — remaining work is the 27 real numbers, and each already carries its own honest label.

- **The check that nothing calls is a class, not two instances. Found 02.09, working q-804.** That
  row exists because two shipped checks passed their own fixture tests while a full-tree grep found
  nothing invoking either one; q-804 gives all three of its arms real callers. A sweep for the same
  shape across the rest of `guardrails/` finds five more scripts referenced only from prose or from
  their own data file, with no executable caller anywhere: `check-delta-record.py`,
  `check-deposit-description.py`, `check-landing-next-steps.py`, `check-tier-refusal.py`, and
  `check-config-surface.py`. One of them is admitted in writing already —
  `guardrails/language-rules.json` says of `check-no-history.py`, "check-no-history.py is armed
  nowhere." Each may be right on its own reading; what is not right is that nothing in the tree
  tells a reader which checks are armed and which merely exist, so the same discovery costs a
  hostile review its time again each pass.

  **Corrected 03.09, re-checked before trusting the class as reported.** "No executable caller
  anywhere" overstates all five, and the `check-no-history.py` quote does too. Each of
  `check-delta-record.py`, `check-deposit-description.py`, `check-landing-next-steps.py`,
  `check-tier-refusal.py`, `check-config-surface.py` and `check-no-history.py` has its own
  dedicated test file, and at least one test per file runs the check against the real shipped data
  rather than only a synthetic fixture (`test_the_shipped_record_and_patterns_pass` for
  `check-tier-refusal.py`; `test_real_repo_range_refreshes_next_steps` for
  `check-landing-next-steps.py`, which reddened for real tonight on this session's own two landing
  commits; `test_armed_passes_on_the_real_spec` for `check-no-history.py`, whose own comment names
  the exact mechanism — "armed at the row-445 conversion delivery (INV-270): the gate runs on the
  live PRODUCT_SPEC.md via the suite (gate b)"). So `guardrails/language-rules.json`'s own "armed
  nowhere" note is itself stale, contradicted by a test already committed beside it. The real,
  narrower gap across all six: none has a direct standalone line inside `guardrails/pre-push` —
  each runs only through pytest, gate b, on every push, which is genuinely armed, just indirectly.
  Reported, not fixed: naming the armed set precisely (direct gate line vs. suite-only, and fixing
  the one stale "armed nowhere" note), or adding a direct line for the ones that deserve one, is its
  own piece of work and the priority is the owner's call.

- **A criterion added beside the work-board restoration promised a switch its owning row's own
  acceptance could not reach. Found 03.09, in `docs/prover/2026-09-03-work-board-restoration-review.md`
  finding F2, from commit `061d1294`; closed the same day, his word.** That commit added criterion
  10 to `spec/live-status-reporting.md` Requirement 310: once the work board ships, the announcement
  home for a work block moves from the written plan page to the board's own per-task plan. Two ways
  out were named, both his: widen `q-816`'s acceptance, or give the criterion its own row. His word:
  a second row for one feature that happens to span two requirement files is fragmentation with no
  benefit. `q-816`'s acceptance now names R310 criterion 10 beside R309's own criteria.

---

