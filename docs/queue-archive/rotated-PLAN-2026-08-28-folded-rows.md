# Rotated off PLAN.md: the rows folded on 2026-08-27

Date: 2026-08-28. His word that morning, 11:48: "оставим то что нужно, остальное в архив — должны
считанные остаться. покажи их, остальные убери с доски." <!-- user-language --> (keep what is
needed, archive the rest — only a handful should remain; show me those and take the others off the
board.)

On 2026-08-27 a relevance pass (commit `293929f1`) read the merged task list and decided that most
of its rows were already covered by a larger row beside them. That pass wrote a `Covered by:` line
onto each one and left every row physically on the board, so the board still showed 131 open tasks
while only about thirty of them named work nobody else was already doing. This file holds the rows
that pass folded, exactly as they stood in `PLAN.md` on 2026-08-28, grouped under the row each was
folded into. Each surviving row on the board now carries one line naming the rows it absorbed and
pointing here.

Nothing here is a loss. Every one of these rows except two also stands in full, in its original
wording, in `docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`, under its own row
number — row 517 for `q-517`, and so on. This file is the second copy of that text, kept so the fold
decision can be read on its own terms. The two exceptions are `plan-1` and `plan-13`, which were
`PLAN.md`'s own steps and never queue rows, so this file is their only home outside git history.

Four rows the 27.08 pass folded were checked against their fold target on 2026-08-28 and stayed on
the board, so they are not in this file: `q-490`, `q-567`, `q-586` and `plan-10`. Each carries, on
the board, the fact its target does not cover.


---

## Folded into q-398 — A request meant for another project reaches it automatically

6 rows.

### ⬜ A bad message is caught the moment it's created — id: q-399
**Group:** Method reliability · **Priority:** normal
**Source:** incident 2026-07-17 — "a bogus deposit passed the receiving sweep's gate."
**Covered by:** q-398 — A request meant for another project reaches it automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Every handed-in item is logged automatically — id: q-503
**Group:** Feedback & measurement · **Priority:** normal
**Source:** found 2026-07-27 — the feedback ledger went unwritten for ten days despite ten real deposits.
**Covered by:** q-398 — A request meant for another project reaches it automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ A near-miss anywhere now warns every other project — id: q-511
**Group:** Worker & data safety · **Priority:** normal
**Source:** 2026-07-27 evening — a real near-loss of edits in a sibling project, caught only by luck.
**Covered by:** q-398 — A request meant for another project reaches it automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Handed-in files reach the project even from another machine — id: q-247
**Group:** Cross-project · **Priority:** normal
**Source:** owner 2026-07-10.
**Covered by:** q-398 — A request meant for another project reaches it automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Strangers can suggest changes through GitHub without special access — id: q-261
**Group:** Cross-project · **Priority:** normal
**Source:** split from q-247, 2026-07-12.
**Covered by:** q-398 — A request meant for another project reaches it automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ The first project sharing data gets its own safety checks — id: q-385
**Group:** Cross-project · **Priority:** normal
**Source:** split 2026-07-17.
**Covered by:** q-398 — A request meant for another project reaches it automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-386 — Independent work actually runs in parallel branches, proven live

7 rows.

### ⬜ Independent work is checked to prove it ran in parallel — id: q-412
**Group:** Parallel & multi-agent work · **Priority:** normal
**Source:** owner 2026-07-17 — "guess! nothing!" (three parallel items ran single-file).
**Covered by:** q-386 — Independent work actually runs in parallel branches, proven live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Finished work branches are cleaned up automatically — id: q-504
**Group:** Parallel & multi-agent work · **Priority:** normal
**Source:** found 2026-07-27 — the three-lane cap was full of dead, already-merged branches.
**Covered by:** q-386 — Independent work actually runs in parallel branches, proven live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Clear rules for running several workers at once — id: q-206
**Group:** Parallel & multi-agent work · **Priority:** normal
**Source:** homeless backlog item, homed 2026-07-10.
**Covered by:** q-386 — Independent work actually runs in parallel branches, proven live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Big builds are planned so pieces can be built in parallel — id: q-215
**Group:** Parallel & multi-agent work · **Priority:** normal
**Source:** owner 2026-07-10 ~10:08.
**Covered by:** q-386 — Independent work actually runs in parallel branches, proven live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Several independent workers are managed without stepping on each other — id: q-234
**Group:** Parallel & multi-agent work · **Priority:** normal
**Source:** owner 2026-07-10 ~13:06.
**Covered by:** q-386 — Independent work actually runs in parallel branches, proven live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Agents on one machine talk to each other directly — id: q-396
**Group:** Parallel & multi-agent work · **Priority:** normal
**Source:** owner 2026-07-17.
**Covered by:** q-386 — Independent work actually runs in parallel branches, proven live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ A trial run proves the multi-agent rules actually work — id: q-404
**Group:** Parallel & multi-agent work · **Priority:** normal
**Source:** plan section 7, 2026-07-17.
**Covered by:** q-386 — Independent work actually runs in parallel branches, proven live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-624 — A command that destroys unsaved work is refused before it runs

2 rows.

### ⬜ A worker never wipes out someone else's unsaved work — id: q-479
**Group:** Worker & data safety · **Priority:** normal
**Source:** found 2026-07-23, four separate real occurrences of workers destroying uncommitted work.
**Covered by:** q-624 — Repeated unsaved-work losses are finally traced, not waved past. Folded 27.08 by the relevance pass; kept whole so nothing is lost.
Note: traces to the same recurring defect family as q-511, q-598, q-605, q-624, q-589, q-586, q-596, q-623 — a worker or session destroying or misreporting work that isn't its own. q-624 found 28 real violations of this still-unenforced rule and may already be the true blocker on this task — worth the owner's word on whether this closes the moment q-624's hook is installed, or whether they are two separate deliverables.

### ⬜ An old file-discarding incident gets its own proper record — id: q-605
**Group:** Worker & data safety · **Priority:** quick win
**Source:** found 2026-08-12 push review.
**Covered by:** q-624 — Repeated unsaved-work losses are finally traced, not waved past. Folded 27.08 by the relevance pass; kept whole so nothing is lost.
Note: the row itself is undecided between "give this incident its own record" and "declare it already covered by row 598/624." The name above describes the felt gap, not a settled deliverable. It also sits inside the same date range q-624's sweep covered (2026-08-13 onward — 07-28 isn't explicitly re-listed there) — worth checking whether this is already folded into q-624's broader finding before both are kept as separate tasks.


---

## Folded into plan-17 — Each session reads only what it needs

4 rows.

### ⬜ Expensive AI help is used only when truly needed — id: q-507
**Group:** Budget & economy · **Priority:** normal
**Source:** owner 2026-07-27 ~20:31 — "about a fifth of the weekly budget in half a day" on mechanical work.
**Covered by:** plan-17 — Each session reads only what it needs. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ The method knows what to trim when money or time run short — id: q-140
**Group:** Budget & economy · **Priority:** normal
**Source:** owner 2026-07-06 ~20:23.
**Covered by:** plan-17 — Each session reads only what it needs. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Weekly spending is tracked and cheaper workers are used more — id: q-457
**Group:** Budget & economy · **Priority:** normal
**Source:** owner 2026-07-22, $6,486/week measured burn.
**Covered by:** plan-17 — Each session reads only what it needs. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Tests during work run fast; full proof runs at every release — id: q-575
**Group:** Budget & economy · **Priority:** normal
**Source:** cost audit, row 568, owner ~01:10 class ruling.
**Covered by:** plan-17 — Each session reads only what it needs. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into plan-12 — The spec finally describes what the product does

12 rows.

### ⬜ Shared displays are checked against what you see — id: q-517
**Group:** Spec & feature quality · **Priority:** normal
**Source:** deposit 2026-07-28 — a screen-reader announcement "was wrong in three ways for weeks" though every writer's own rule was obeyed.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Editing the spec updates every copy of it automatically — id: q-552
**Group:** Spec & feature quality · **Priority:** normal
**Source:** found 2026-08-06 — the same push was refused four times over one edit because two copies disagreed.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ New requests say which existing task they match — id: q-486
**Group:** Communication & reporting · **Priority:** normal
**Source:** owner 2026-07-27.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ New features are checked against how people actually use the product — id: q-108
**Group:** Spec & feature quality · **Priority:** normal
**Source:** owner 2026-07-06 ~00:25, tlvphoto evidence.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ A finished feature is walked through like a real visitor — id: q-117
**Group:** Spec & feature quality · **Priority:** normal
**Source:** inbox 2026-07-06 ~10:10; companion to q-108.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ A default choice gets a human decision within two releases — id: q-118
**Group:** Spec & feature quality · **Priority:** normal
**Source:** inbox 2026-07-06 ~10:10.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Every new feature states how fast it must be — id: q-143
**Group:** Spec & feature quality · **Priority:** normal
**Source:** owner 2026-07-06 ~21:03, on a page that loaded slow with no timing plan.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Every step of a journey states what it needs and leaves behind — id: q-192
**Group:** Spec & feature quality · **Priority:** normal
**Source:** owner 2026-07-09 late evening.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ New projects know upfront which variations to design for — id: q-436
**Group:** Spec & feature quality · **Priority:** normal
**Source:** tlvphotos inbox 2026-07-20.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Checking for similar cases happens at every level — id: q-437
**Group:** Spec & feature quality · **Priority:** normal
**Source:** tlvphotos inbox 2026-07-20; sibling of q-436.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ A reported bug is checked against the spec before it's fixed — id: q-459
**Group:** Spec & feature quality · **Priority:** normal
**Source:** owner 2026-07-22, rotation-bug case.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Every request is sorted as one-time or standing before it starts — id: q-440
**Group:** Method housekeeping · **Priority:** normal
**Source:** owner 2026-07-21, said sharply after a standing ask was treated as one-off.
**Covered by:** plan-12 — The spec finally describes what the product does. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-489 — Every automatic check proves it can actually catch its problem

7 rows.

### ⬜ A broken measurement refuses to fake a zero — id: q-525
**Group:** Method reliability · **Priority:** normal
**Source:** found 2026-07-28 — 109 tracked documents all carried a false zero count.
**Covered by:** q-489 — Every automatic check proves it can actually catch its problem. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Every quality check is tested to prove it actually works — id: q-217
**Group:** Method reliability · **Priority:** normal
**Source:** owner 2026-07-10 ~10:22 — "convergence of all processes is needed."
**Covered by:** q-489 — Every automatic check proves it can actually catch its problem. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ A full audit of a rough day finds what the method missed — id: q-220
**Group:** Method reliability · **Priority:** normal
**Source:** owner 2026-07-10 ~10:43.
**Covered by:** q-489 — Every automatic check proves it can actually catch its problem. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Documents are automatically re-checked so wording never drifts — id: q-230
**Group:** Method reliability · **Priority:** normal
**Source:** owner 2026-07-10 ~11:02.
**Covered by:** q-489 — Every automatic check proves it can actually catch its problem. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ The method watches its own numbers and improves them on a schedule — id: q-492
**Group:** Method reliability · **Priority:** normal
**Source:** owner 2026-07-27.
**Covered by:** q-489 — Every automatic check proves it can actually catch its problem. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Full documents get a periodic deep re-read on a set schedule — id: q-454
**Group:** Method reliability · **Priority:** normal
**Source:** owner 2026-07-22.
**Covered by:** q-489 — Every automatic check proves it can actually catch its problem. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Past working sessions are mined for lessons never written down — id: q-455
**Group:** Method reliability · **Priority:** normal
**Source:** owner 2026-07-22.
**Covered by:** q-489 — Every automatic check proves it can actually catch its problem. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-497 — The assistant never puts words in your mouth

2 rows.

### ⬜ A decision recorded as your word actually quotes you — id: q-550
**Group:** Method reliability · **Priority:** normal
**Source:** found 2026-08-06 — a session fabricated an entry under the owner's name that passed the existing check.
**Covered by:** q-497 — The assistant never puts words in your mouth. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ A worker's report matches the files it changed — id: q-589
**Group:** Worker & data safety · **Priority:** normal
**Source:** found 2026-08-12 — a worker's final report quoted facts that matched nothing in the actual tree.
**Covered by:** q-497 — The assistant never puts words in your mouth. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into plan-11 — The plan, board and queue become one list

4 rows.

### 🔄 Say the word, see exactly where things stand — id: plan-1
**Group:** Board & visibility · **Priority:** normal
**Source:** PLAN.md step 1, owner 26.08 ("pseudo-kanban").
**Covered by:** plan-11 — The plan, board and queue become one list. Folded 27.08 by the relevance pass; kept whole so nothing is lost.
Note: sibling of q-166 (Board & visibility) — q-166 is the full standing board with worker lanes and time-in-flight, parked separately by the owner as a bigger, separately-decided feature; this step is the near-term light view over the same Canon.

The probe reads step statuses from acceptance commands; the board renders as a page (pseudo-kanban, per his 26.08 word); ticket-field recon landed in `docs/research/2026-08-26-board-ticket-fields.md`; the clock-hook wiring was investigated (found: safe-mode disables it, not a pack defect). Acceptance: his own trigger word in a new empty-context session gets the state, no question asked; the board opens; he confirms in one line he sees the time and a clear list.

Full body (rules, acceptance commands, measurements) preserved in git history: `git log -p -- PLAN.md`, the step's own text before the 27.08 task-list merge.

### 🔄 The project's own goals are tracked with real, checkable numbers — id: q-617
**Group:** Method housekeeping · **Priority:** normal
**Source:** owner 2026-08-12/13 — goals lived only in memory, not in the plan's own status block.
**Covered by:** plan-11 — The plan, board and queue become one list. Folded 27.08 by the relevance pass; kept whole so nothing is lost.
Note: names the felt problem accurately, but the row is mid-repair and its final acceptance shape (a kept ledger vs. a live head-block table) wasn't fully settled in the source text.

### ⬜ Every open task reads clearly on the board — id: q-566
**Group:** Board & visibility · **Priority:** normal
**Source:** owner 2026-08-06 ~21:00, on record in DECISIONS.md.
**Covered by:** plan-11 — The plan, board and queue become one list. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Old queued tasks are reviewed and cleared out regularly — id: q-481
**Group:** Board & visibility · **Priority:** normal
**Source:** owner 2026-07-23 ~18:18 — "the roadmap is no five-year plan."
**Covered by:** plan-11 — The plan, board and queue become one list. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into plan-16 — Every rule finally lives in exactly one place

9 rows.

### ⬜ You hear only what changes for you — id: plan-13
**Group:** Communication & reporting · **Priority:** normal
**Source:** PLAN.md step 13, owner 27.08.
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

His word, 27.08: "ты не должен грузить пользователя фигней", and it needs one home rather than <!-- user-language -->
three. Today the rules about what reaches a person are spread between the communicator skill, the
personal profile and the session laws.

One rule, in the skill that owns showing work to a person: a person hears what changes for them.
The workshop's own bookkeeping — records, gate letters, row counts, internal findings — stays
inside the workshop.

**Acceptance:** the rule has one home and the other two places point at it · a check finds no
second copy of it.

### ⛔ Decisions explain what changes for you — id: q-119
**Group:** Communication & reporting · **Priority:** normal
**Source:** owner 2026-07-06 ~10:40 — "what you gave me in the HTML is not!!!"
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Work is narrated out loud as it happens — id: q-131
**Group:** Communication & reporting · **Priority:** normal
**Source:** owner 2026-07-06 ~13:57, second ask in one day.
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ The reply clock reads the real time automatically — id: q-134
**Group:** Communication & reporting · **Priority:** normal
**Source:** 2026-07-06 session 16 — leads still drifted from the wall clock.
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Every chat window follows the same rules automatically — id: q-141
**Group:** Communication & reporting · **Priority:** normal
**Source:** owner 2026-07-06 ~20:41 — "can you actually do something about communication??"
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ The visible task list speaks plain words, no codes — id: q-144
**Group:** Communication & reporting · **Priority:** normal
**Source:** owner 2026-07-06 ~21:22.
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ The session always reports what it did, unprompted — id: q-484
**Group:** Communication & reporting · **Priority:** normal
**Source:** owner 2026-07-27, three separate asks in one morning.
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Reports include a time estimate, and later say how close it was — id: q-471
**Group:** Communication & reporting · **Priority:** normal
**Source:** 2026-07-23, widened 2026-07-27 to a kept ledger of promised-vs-actual.
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Every mention of an item includes its plain description — id: q-424
**Group:** Communication & reporting · **Priority:** normal
**Source:** owner 2026-07-19.
**Covered by:** plan-16 — Every rule finally lives in exactly one place. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-166 — The board shows everything the team is doing, live

4 rows.

### ⬜ Ask "show me all the features" and get an answer — id: q-133
**Group:** Board & visibility · **Priority:** normal
**Source:** owner 2026-07-06 ~15:52.
**Covered by:** q-166 — The board shows everything the team is doing, live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.
Note: mostly landed (2026-07-06); one leg — it firing on his next real ask — stays open.

### ⬜ The status page shows the one thing being finished now — id: q-582
**Group:** Board & visibility · **Priority:** normal
**Source:** deposit 2026-08-07 09:54 — owner: "the pack has to learn to help the client focus."
**Covered by:** q-166 — The board shows everything the team is doing, live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Long builds show progress as they happen — id: q-583
**Group:** Board & visibility · **Priority:** normal
**Source:** deposit 2026-08-07 09:54 — a four-hour block with no feedback along the way.
**Covered by:** q-166 — The board shows everything the team is doing, live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ One view shows who's working on what, everywhere — id: q-411
**Group:** Board & visibility · **Priority:** normal
**Source:** owner 2026-07-17 ~15:54, named as far-tier (4.0) himself.
**Covered by:** q-166 — The board shows everything the team is doing, live. Folded 27.08 by the relevance pass; kept whole so nothing is lost.
Note: deferred by his own placement, not by a problem.


---

## Folded into q-458 — The plain-language text checker becomes its own reusable tool

11 rows.

### ⬜ Your text is changed only where you asked — id: q-485
**Group:** Readability & plain language · **Priority:** normal
**Source:** owner 2026-07-27.
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ A confusing sentence gets fixed at its source — id: q-487
**Group:** Readability & plain language · **Priority:** normal
**Source:** owner 2026-07-27 — called "the most valuable of the morning's asks."
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Text always names what a group of items actually is — id: q-510
**Group:** Readability & plain language · **Priority:** normal
**Source:** owner 2026-07-27 ~23:31 — reading his own "Опора 4" example. <!-- user-language -->
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ The spec reads like a person wrote it — id: q-148
**Group:** Readability & plain language · **Priority:** normal
**Source:** owner 2026-07-06 ~23:24, several approved/killed rounds since.
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Text is checked for awkward phrasing before you see it — id: q-170
**Group:** Readability & plain language · **Priority:** normal
**Source:** inbox 2026-07-07.
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Text you read is drafted with a clear head first — id: q-208
**Group:** Readability & plain language · **Priority:** normal
**Source:** owner 2026-07-10 ~00:53, third onboarding bounce.
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Text rewrites are checked to prove no meaning was lost — id: q-204
**Group:** Readability & plain language · **Priority:** normal
**Source:** homeless backlog item, homed 2026-07-10.
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Old documents are rewritten to read clearly, and stay that way — id: q-460
**Group:** Readability & plain language · **Priority:** normal
**Source:** owner 2026-07-22.
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Text never describes a tool as if it were a person — id: q-493
**Group:** Readability & plain language · **Priority:** normal
**Source:** deposit 2026-07-27 — owner stopped reading and named the class ("cups do not fluoresce").
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ A workflow diagram lives in exactly one place — id: q-381
**Group:** Readability & plain language · **Priority:** normal
**Source:** owner 2026-07-17.
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ A safety net catches messy chat text automatically — id: q-203
**Group:** Communication & reporting · **Priority:** normal
**Source:** homeless backlog item, homed 2026-07-10.
**Covered by:** q-458 — The plain-language text checker becomes its own reusable tool. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into plan-14 — Every project gets its own status view

5 rows.

### ⬜ Projects learn automatically when a new rule applies — id: q-509
**Group:** Communication & reporting · **Priority:** normal
**Source:** owner 2026-07-27 ~23:14.
**Covered by:** plan-14 — Every project gets its own status view. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ The method still works without git or GitHub — id: q-171
**Group:** Portability · **Priority:** normal
**Source:** owner 2026-07-08 ~09:07.
**Covered by:** plan-14 — Every project gets its own status view. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ The four safety checks are made portable to any project — id: q-241
**Group:** Portability · **Priority:** normal
**Source:** relayed 2026-07-10 ~14:22.
**Covered by:** plan-14 — Every project gets its own status view. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Your photo site can copy over the new setup on its own — id: q-221
**Group:** Cross-project · **Priority:** normal
**Source:** owner 2026-07-10 ~10:43.
**Covered by:** plan-14 — Every project gets its own status view. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ The right format shows up whether you're local or remote — id: q-168
**Group:** Cross-project · **Priority:** normal
**Source:** owner 2026-07-07 ~10:57.
**Covered by:** plan-14 — Every project gets its own status view. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-163 — A proven method builds thorough tests every time

3 rows.

### ⬜ Test practices are checked against how the industry does it — id: q-191
**Group:** Testing · **Priority:** normal
**Source:** owner 2026-07-09 late evening.
**Covered by:** q-163 — A proven method builds thorough tests every time. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Test suites follow rules that keep them running fast — id: q-491
**Group:** Testing · **Priority:** normal
**Source:** owner 2026-07-27, after a real 572-second suite was cut to 285.
**Covered by:** q-163 — A proven method builds thorough tests every time. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Slow tests are rebuilt to prove themselves quickly — id: q-554
**Group:** Testing · **Priority:** normal
**Source:** owner 2026-08-06 11:03.
**Covered by:** q-163 — A proven method builds thorough tests every time. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-427 — One live list shows every tunable setting

5 rows.

### ⬜ A list points at where handed-in files live — id: q-207
**Group:** Method housekeeping · **Priority:** normal
**Source:** homeless backlog item, homed 2026-07-10.
**Covered by:** q-427 — One live list shows every tunable setting. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Every project setting is catalogued in one place — id: q-229
**Group:** Method housekeeping · **Priority:** normal
**Source:** owner 2026-07-10 ~11:00, post-1.0.
**Covered by:** q-427 — One live list shows every tunable setting. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Every tool's version number stays in sync automatically — id: q-231
**Group:** Method housekeeping · **Priority:** normal
**Source:** owner 2026-07-10 ~11:29.
**Covered by:** q-427 — One live list shows every tunable setting. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ An approved idea from months ago finally gets built — id: q-238
**Group:** Method housekeeping · **Priority:** normal
**Source:** found 2026-07-10 — approved 2026-07-05, never built.
**Covered by:** q-427 — One live list shows every tunable setting. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Lessons learned automatically retire once no longer needed — id: q-410
**Group:** Method housekeeping · **Priority:** normal
**Source:** owner 2026-07-17 ~15:44.
**Covered by:** q-427 — One live list shows every tunable setting. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-54 — New projects learn who they're building for

8 rows.

### ⬜ Shared code is checked for leaked personal data — id: q-488
**Group:** Worker & data safety · **Priority:** normal
**Source:** owner 2026-07-27 — engines must "contain no personal data at all."
**Covered by:** q-54 — New projects learn who they're building for. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Every project knows and updates its own kind — id: q-129
**Group:** Onboarding & founding · **Priority:** normal
**Source:** owner 2026-07-06 ~13:27.
**Covered by:** q-54 — New projects learn who they're building for. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ New projects can split public code from private content — id: q-190
**Group:** Onboarding & founding · **Priority:** normal
**Source:** owner 2026-07-09 late evening.
**Covered by:** q-54 — New projects learn who they're building for. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ Design changes sync automatically to visual projects — id: q-93
**Group:** Onboarding & founding · **Priority:** normal
**Source:** 2026-07-05.
**Covered by:** q-54 — New projects learn who they're building for. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Switches and text can be changed live, without a full rebuild — id: q-496
**Group:** Product & infrastructure design · **Priority:** normal
**Source:** owner 2026-07-27 ~15:00 — his own photo site needed a full build just to flip a switch.
**Covered by:** q-54 — New projects learn who they're building for. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Every project states which outside services it depends on — id: q-236
**Group:** Product & infrastructure design · **Priority:** normal
**Source:** owner 2026-07-10 ~13:48.
**Covered by:** q-54 — New projects learn who they're building for. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ Design choices are checked against the real technical need — id: q-400
**Group:** Product & infrastructure design · **Priority:** normal
**Source:** owner 2026-07-17 afternoon.
**Covered by:** q-54 — New projects learn who they're building for. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ One window can manage several related projects at once — id: q-421
**Group:** Cross-project · **Priority:** normal
**Source:** owner 2026-07-18 ~21:00.
**Covered by:** q-54 — New projects learn who they're building for. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-48 — The product's performance after launch is tracked automatically

4 rows.

### ⛔ Two versions of a feature can be tried and measured — id: q-49
**Group:** Feedback & measurement · **Priority:** normal
**Source:** owner 2026-07-05.
**Covered by:** q-48 — The product's performance after launch is tracked automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ What people do with the product feeds back into planning — id: q-96
**Group:** Feedback & measurement · **Priority:** normal
**Source:** owner 2026-07-05.
**Covered by:** q-48 — The product's performance after launch is tracked automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⛔ A problem that keeps happening always gets an owner — id: q-100
**Group:** Feedback & measurement · **Priority:** normal
**Source:** owner 2026-07-05 ~23:00 — "solved!! Either solve the problem or agree that it isn't one."
**Covered by:** q-48 — The product's performance after launch is tracked automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.

### ⬜ A persistently bad number automatically becomes a task — id: q-469
**Group:** Feedback & measurement · **Priority:** normal
**Source:** relayed 2026-07-22 ~19:34.
**Covered by:** q-48 — The product's performance after launch is tracked automatically. Folded 27.08 by the relevance pass; kept whole so nothing is lost.


---

## Folded into q-581 on 2026-08-28 — You're warned before anything can trigger a security popup

One row. This fold was made on 2026-08-28, not by the 27.08 pass. q-542 names the leftover test
server that kept raising the owner's connection-approval dialog; q-581 names the class, being
warned before anything can raise such a dialog at all. Two rows for one class is the shape the pack's
own rule of thinking forbids, so the instance folds into the class.

### ⬜ A leftover test server stops popping up security warnings — id: q-542
**Group:** Worker & data safety · **Priority:** normal
**Source:** found 2026-08-05 — servers 8–22 days old repeatedly triggered the owner's connection-approval dialog.
