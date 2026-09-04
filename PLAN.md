# PLAN — the one plan for live-spec (2026-08-28)

## Goal

Turnkey software house. In the owner's own words, 26.08:

> He can come in and dump ideas in any order, and along the way the system already lines everything up beautifully — from a clear spec to the architecture and the test matrix. It knows how to optimize processes, build the right architecture, understand what needs checking on every pass. All of it lightweight (the previous version loaded 42k just from standing up). It knows how to communicate properly.

The user is a single author of a software product who thinks out loud and drives development through agents. He speaks freely, with no command syntax, and isn't required to run the internal machinery himself.

**The tasks below are not the goal.** They are the condition without which the goal can't be reached: working on the project across many sessions in a row without losing the thread. It was lost for a month. A task that doesn't move the project toward the goal doesn't get done.

## What counts as done

- The owner dumps thoughts, and a question doesn't turn into a task.
- An instruction isn't lost and gets one clear goal.
- Director picks a different route for different work; specialists get called only when needed.
- Required context is a card, the current work, and pointers; the full document loads only on
  proven need.
- Only checks for real safety and correctness block a push.
- One existing project has migrated, with a proven rollback.
- Another agent can continue the project from its files, with no spoken recap from the owner.

## One plan

**This file is the one plan. There is never a second one.** No "session plan," no "lane plan," no
task list anywhere else. A felt need for another plan is a sign that a task belongs here, not that
a new file should exist.

**It doesn't get rewritten.** A task's name and order change only on a new fact **and with
The owner's explicit consent.** Every edit goes into git with a reason: `git log PLAN.md` shows the
whole history. A silent rewording of a task is drift, even when the wording is better.

A session edits exactly one thing here: a task's status. Nothing else.

**A finished task leaves this board by a person's own hand, and by nothing else.** No script rotates
a done row off it; the one that used to understand only the shape of the retired queue and went to
the attic with it on 28.08. What a hand has to write is both halves of the act — the archive page
and the manifest line that names it — and the push gate proves both directions, so a hand that
writes one half is stopped there. Settled 31.08; the retired findings log carries how it was reached (`docs/queue-archive/2026-09-04-findings-log-retired.md`, this page's own findings section until it was cut on 04.09).

## Words used here

- **Task** — an entry in `## Tasks` below. There is no fixed count; the count is
  `grep -c '^### .*— id: ' PLAN.md`. (Corrected 28.08: the looser pattern this line used to give
  matched this very line as well, so the count it printed was always one too many.)
- **Item** — a line inside a task.
- **Canon** — the list of tasks with status marks that `scripts/state-probe.sh` prints. Never typed
  by hand. There is no other Canon.
- **The marks** — the one home is `~/.claude/playbook/CLAUDE.md`, section "How a reply to him
  looks": ✅ done · 🔄 in hand · 🔁 reopened · ⬜ queued · ⛔ blocked. Five, since his word of
  2026-09-04: a task is either queued and understood, or it does not exist. **Blocked means one
  thing** — something outside the work has stopped it, an expired key, a dead credential, a service
  that is down. Work that is merely waiting is not blocked. Something that needs his judgement is
  asked as a question in the reply, and it is never a task and never a mark of its own. The order
  the marks are printed in is written once, in the pack's own rulebook, rule 38 — this page does
  not restate it.
- **⬜ has a real bar: "queued" means accepted into work.** His word, 27.08, sharpened 04.09. A
  task earns ⬜ only when a reader can tell finished from unfinished without asking anyone: its
  definition of done is written, and it names every spec chapter it touches, by link. A command
  carries the done-when wherever a command can decide it, and that is the first thing to try. Where
  what the task leaves behind is a page, a measurement or a judgement, the definition says so in one
  line and names who reads it and what would convince them. A task carrying neither is an unformed
  idea; it is answered and dropped rather than written down. The cluster prefix a title may carry is
  written once, in the pack's own rulebook, rule 38.

- **🔄 means a worker has it now**, by the take-or-decline rule in the task shape above — never "a
  session happened to touch this file recently."
- **Verified / declared** — printed beside a mark, never a sixth mark. Verified: the task has a
  command in `scripts/plan_checks.py`, the probe ran it, and this is what it returned. Declared: no
  command exists, so the mark is whatever a session typed by hand. **A declared ✅ is not proof of
  done — it is a claim, read with the same suspicion as an open task, until it is verified.** Fixing
  this for every task is plan-10's own job.
- **A task that closes writes its own check in the same breath.** Whenever what a task leaves behind
  is a file, a script or a setting that can drift back, the session closing it adds that task's
  command the same moment it marks the task done; a close with no command is a claim, and this list
  has already had to go back and re-check thirty-seven of them. A task whose result is prose, a
  measurement or a decision writes no command and says in one line who read it and where.
- **Gates** — the checks that run before `git push`. Fail one, and the push is cancelled.
- **The prover** — the external skill that hunts for defects in a spec. It stays, and gets more
  work.
- **A host** — a foreign project the pack is installed in. There are five of them.

A word not on this list, and not one the owner said himself, gets explained where it's introduced,
or isn't used at all.

## Already decided — not reopened

- No mass removal of tests that guard wording: measured 26.08, 16% dead.
- The pre-push check stays untouched until Director is measured; building a second classifier by
  file path is forbidden — the model decides meaning, code decides mechanics.
- Migrating other projects comes last, after the release.
- The board is built as a rendering of the same Canon, not stood up as a separate feature.
- Dropped, and not coming back: Kimi/K3, Hermes, OpenRouter, LiteLLM.

**This file sits outside the jurisdiction of the format rules, the prover, and skill-review.** It
doesn't pass through the gates, and it needs no records.

Leads: Sonnet. Owner: this project's owner. Start: 26.08.2026.

**The start of every session:** `bash scripts/state-probe.sh`. Don't read the prose in this file
instead of that.

## Fallback when drifted

The owner only has to ask the session to check against the plan, in any window, on any model, with
an empty context. That means the session must: run `bash ~/live-spec/scripts/state-probe.sh` · read this file whole · look at `git log --oneline -15` and `git status` · look at what's actually on disk · and report in Canon, giving a separate line to everything that disagrees between the plan, the git history, and the disk. Fix nothing until he answers.

The main plan is **always one file: `~/live-spec/PLAN.md`.** Never start a second one.

---

## Laws of execution (breaking one is a stop, not a workaround)

1. **Moratorium.** Executing the plan does not create: ROADMAP lines, JOURNAL entries, prover
   records, skill-review records, new gates, new hooks, new configs, new storage locations. **And
   it does not edit existing gates, hooks or configs** — writing yourself into a gate's exception
   list is the same workaround, just from the other side. Found a problem — fix it where it sits, if it sits
   on the step in hand. Anything else becomes a task on this board, in the owner's own words, or
   it is dropped. There is no second list, and finding something is not a reason to stop.
2. **No invented numbers.** Any new threshold, limit or size needs an outside source or a
   reference to a real incident that already happened. No source, no number.
3. **Acceptance is a command, not a word.** Every step has a command and an observable output.
   The words "recorded," "logged," "record" are forbidden in the acceptance line.
4. **Red from a deletion is legitimate.** If deleting a dead test turns CI green, the fix is that
   deletion.
5. **Don't widen a step.** A step does exactly what's written. An adjacent finding becomes its own task on this board, or it is
   dropped.
6. **One term, one word.** A word the owner didn't say himself gets explained in plain words on
   the same line it's introduced. One thing is named the same way in every document and every
   reply. The pack's glossary: `skills/live-spec-base/references/glossary.md`.
7. **Every reply to the owner:** the time `[HH:MM]` as the first line, then a report in the
   "Canon" format — his own word from 18.08, which he himself carried between three projects:

   The format lives in one home — `~/.claude/playbook/CLAUDE.md`, section "How a reply to him
   looks." It isn't repeated here: two copies would drift apart, which is the very defect of "two
   homes for one fact."

   The full report form, for wherever his word is needed, has its own one home too —
   `~/.claude/playbook/personal/profile.md`, section "Owner reports" (his own word from 14.08
   12:08). Not repeated here, for the same reason.

   Sonnet keeps `TodoWrite` in sync with these steps, so the list stays visible in the interface.

8. **Take nothing on faith.** Not a handoff, not a past session, not a document, not its own
   memory. A claim of "done" is checked by a command before anything gets built on it. Proven on
   this project: a handoff claimed the whole plan was fully closed, and three of six packages
   turned out not even started; `evals/director.md` claimed no runs had happened, and runs had
   happened, showing 20 of 35. Where there's nothing to check with, say so to the owner instead of
   passing someone else's claim along as fact.
9. **Unpushed work doesn't spend the night as a single copy.** The machine has already lost a
   working tree once. If commits haven't reached `origin/main`, a copy goes into a side branch or
   a bundle off the machine, and that happens before the session ends.
10. **A green check on undone work is a defect in the check, not a sign of readiness.** Seeing
    this — repair the check on the spot, and name the repair in the session's report. Found three of these on 26.08: step 0 was green on an
    empty archive, step 1 looked at the wrong file, step 8 caught the word "directory" instead of
    `skills/director`.
11. **The owner's working contract must load — both files:**
    `~/.claude/playbook/personal/profile.md` (90 lines, the personal layer) and
    `.live-spec/profile.md` (the host layer, which wins over the personal one when they resolve).
    It already records the timestamp rule, the ban on the "X, not Y" contrast frame, the "what is
    X — my own mistake" reflex, the orchestrator seat, the mechanics run on sonnet. A session that
    hasn't loaded it is working wrong.

**End of session:** update a step's status (one line). Write nothing else.

---

## Tasks

One list: the plan's own steps and the former ROADMAP.md queue, merged 27.08 per step 11. The order the rows print in is written once, in the pack's rulebook, rule 38; this page does not restate it. Marks: see "Words used here" above — the one live copy in this page, itself pointing at `~/.claude/playbook/CLAUDE.md`. Former ROADMAP.md rows are archived verbatim at `docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`.

### ✅ Starting a work session with the assistant costs a quarter of what it costs today, and every standing file earns its place — id: q-809
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A task that turns out not to be done says so, instead of pretending it is blocked — id: q-807
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A person who did not build this can read the task list and understand it — id: q-808
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A finished task is shown and closed; a complaint about it becomes new work, not a stuck one — id: q-810
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The turnkey product contract is proven complete before any code starts — id: q-806
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A host refreshing its skills from the pack isn't taxed for a review the pack already did — id: q-814
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The worker-restore gate never blocks a push over an unrelated project's history — id: q-815
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A new project stops being handed the queue this one retired — id: q-801
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The playbook repo earns its keep or gets folded away — id: q-800
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A color-contrast check now looks at the right background — id: q-490
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The assistant never puts words in your mouth — id: q-497
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A cleared mistake stops blocking every future push — id: q-527
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Trimming a long document never loses what moved — id: q-531
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The installed copy and the working copy stay in sync — id: q-537
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A project's starting state is saved the moment it joins — id: q-55
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A safety check that only runs here now ships everywhere — id: q-567
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ You're warned before anything can trigger a security popup — id: q-581
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A worker's cleanup step never erases unsaved work — id: q-586
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A command that destroys unsaved work is refused before it runs — id: q-624
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The cost of every extra process step is measured and justified — id: q-568
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every new session's starting weight is measured and trimmed — id: q-570
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every made-up number in the system is found and removed — id: q-576
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ All project files live in one place again — id: plan-0
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A question you ask never turns into a task — id: plan-2
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Old clutter is cleared, past work kept readable — id: plan-3
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The same thing is always called the same name — id: plan-4
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The reviewer now catches real bugs in code — id: plan-5
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Checks that catch real mistakes are kept — id: plan-6
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every new session starts up lighter and faster — id: plan-7
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The release is labeled and ready to install — id: plan-8
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every "done" mark on the board gets checked — id: plan-10
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The plan, board and queue become one list — id: plan-11
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The spec finally describes what the product does — id: plan-12
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Checking for similar cases happens at every level — id: q-437
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ New projects know upfront which variations to design for — id: q-436
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every project gets its own status view — id: plan-14
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every rule finally lives in exactly one place — id: plan-16
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Each session reads only what it needs — id: plan-17
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The board shows everything the team is doing, live — id: q-166
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A queued row always carries a real reason to stay open; the Director owns why — id: q-813
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The Director's real route is proven end to end, on the actual mechanism, not the instructions — id: q-812
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The plain-language text checker becomes its own reusable tool — id: q-458
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Three small clarity fixes are restored to a rewritten rule — id: q-595
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The spec rule about exceptions now names them — id: q-609
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The rule about what gets skipped is now plain — id: q-610
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every new feature ships with real, complete tests, not just some — id: q-163
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every automatic check proves it can actually catch its problem — id: q-489
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A weak test now actually checks what it claims — id: q-592
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Sync failures now say exactly what went wrong — id: q-597
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A silent review step now leaves a written record — id: q-611
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The reviewer's instructions match what the checker expects — id: q-608
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Rule-location references are checked and now stay accurate — id: q-588
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Every safety check's rulebook comes from one generated source — id: q-625
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A stale reference in the test matrix is corrected — id: q-591
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The startup file carries only what it truly needs — id: q-205
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ One live list shows every tunable setting — id: q-427
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A retired rule number is now clearly marked — id: q-590
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The rule count now lives in exactly one place — id: q-593
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A count in the reviewer's instructions now matches what follows — id: q-612
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Three wording disagreements in the rulebook need your final call — id: q-536
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ One excuse shouldn't cover every future change — id: q-529
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A worker's mistake in another project was traced and reported — id: q-598
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A safety check no longer blames the wrong project — id: q-623
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The record of what changed never marks untouched work as changed — id: q-802
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A skill's rule states itself; the journal carries who said it and when — id: q-803
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A project joining the pack gets its style check wired where the other checks can see it — id: q-821
**Group:** Host adoption · **Priority:** normal
**Source:** the photo site's own session, 2026-09-04, in `inbox/2026-09-04-from-tlvphotos-style-gate-letter.md`,
during a full re-run of the joining installers.

**What it is.** The installer that wires a host's style check writes it under the letter `r`, which
the pack's own check chain already spends on the authority-anchor check — so a host ends up with two
checks under one letter. That host had already patched the collision by hand once, and this run
recreated it. The block is also written with a dash where the chain's own shape uses a colon, so the
two checks that read the chain by that shape cannot see it: a style check wired this way can never be
asked for its known-red proof and never checked for its mirror in continuous integration.

**Done when:** the installer writes the block under a letter nothing else uses, in the chain's own
shape; a host that already carries the old block has it replaced rather than doubled when the
installer runs again; and the two chain-reading checks list the style check among the gates they see.
Proven on a scratch host tree: run the installer twice and read the resulting chain.

**Closed 2026-09-04.** The installer writes under the letter `v` — checked against the chain itself
rather than against the wish, which named two letters as taken that were retired on 2026-08-21. A
block already wired under the old letter is swept into the new one on the next run, through the
repair path the installer already had for a block in the wrong place. Proven red first: the new test
was run against the installer as it stood and the old block survived untouched.

**Links:** `adopt/install-style-gates.sh` (the marker and the written block), `guardrails/pre-push`
(the letters in use), `tests/test_style_gate_kit.py`,
`inbox/handled/2026-09-04-from-tlvphotos-style-gate-letter.md`.

### ⬜ A correction never opens a second row, and the check that would prove it can tell a real change from noise — id: q-820
**Group:** Pack quality · **Priority:** critical
**Source:** the 2026-09-04 re-recording of the director's own scenarios, after the skill changed that
night, and the owner's own worry the same night that nothing validates the director.

**What the run found.** Re-recorded against the skill as it stands: 30 of 36 on the main set, 7 of 9
on the closing set. Four of the six main-set reds are one shape — a message that corrects work
already running is read as new work, and a row opens beside the one that should have been replanned.
That is the failure the owner has named more than any other: work appearing on his board that he
never asked for. The two closing reds defer to a row's own stale gate instead of the rule that
replaced it.

**What this row does NOT do.** It does not measure the eval's own spread. Three recordings read 31,
then 34, then 30, and the first instinct was to make the eval state how much a score moves on its
own — which means running it repeatedly to find out, and that is the machinery rule 39 refuses and
the owner has refused before: a run count proves nothing. What replaces it costs nothing: read the
shape, never the score. A scenario counts as failing when it fails twice on separate recordings, and
the number is not reported as a result at all.

**Done when:** the four correction scenarios pass on two separate fresh recordings, and the eval's
own README says a score is not a result — a scenario is red when it reds twice. Measured by
`python3 evals/director/check.py --all` and `python3 -m pytest -q tests/test_director_scenarios.py`.

**Links:** `evals/director/README.md`, `evals/director/scenarios.json`,
`evals/director/closing-scenarios.json`, `skills/director/SKILL.md` (the acts table and the
correction rule).

### ⬜ The status list a person reads looks the same in every project — id: q-818
**Group:** Board & visibility · **Priority:** normal
**Source:** owner 2026-09-04 01:48 — he asked for one unchanging shape for the list and sees a
slightly different one in each project.

**What it is.** The list of rows and marks a session prints at the top of every reply is rendered
by a script. This project renders it one way; a joined project renders it from its own vendored
copy of that script, and the copies have drifted. The photo site's copy is missing two of the
pieces the pack now ships, and its own plan uses three marks outside the shared five.

**Done when:** one renderer ships from the pack, every joined project prints from that copy, and a
check reds when a host's copy differs from the pack's own. The check reads the two files, not a
record about them. Proven red once against a deliberately drifted copy before it is trusted.

**Links:** `scripts/state-probe.sh`, `scaffold/status-view/`, `adopt/install-*.sh`,
`spec/live-status-reporting.md`.

### ⬜ Which row runs next is decided by a written rule, and a change of order is told to the person — id: q-819
**Group:** Board & visibility · **Priority:** normal
**Source:** owner 2026-09-04 01:48 — in the photo site the next row is picked in what looks to him
like a random order, and nothing says how it should be picked.

**What it is, as it stands after 2026-09-04.** The order the rows print in is now written, in the
rulebook's rule 38, and the probe's own ranking line reads as that rule's one machine reading. Two
halves are still open. What a priority MEANS in a project's own words is written nowhere — the field
exists on every row and only the word "critical" changes anything. And nothing derives the next move
from a stated rule about the work itself: the topmost free row is a position in a list, not a
judgement about what matters most.

**Done when:** a project can say in its own words what a priority means and what makes one row
matter more than another, that statement lives in one place, and the next-move line is derived from
it rather than from list position. The reply-side half is already done and stays done: rule 38 makes
a change in the order something the next reply says, with its reason.

**Links:** `scripts/state-probe.sh` (the ranking block), `spec/live-status-reporting.md`,
`skills/live-spec-base/SKILL.md`.

### ⬜ Every skill in the pack is measured by Anthropic's own skill tool, and the bloated ones come back down — id: q-817
**Group:** Pack quality · **Priority:** normal
**Source:** owner 2026-09-04 01:25 and 01:30 — the pass over every skill was agreed and he does not
see it happening; he wants it standing, for any skill new or changed, never a one-off.

**Where it stands, checked 04.09.** The standing rule already exists and is armed: the push gate
runs `guardrails/check-skill-review.sh`, which refuses a push when a skill changed in a real way
and no review record under `docs/skill-review/` is newer than that change. It is failing right now
for the rulebook and for the director skill, which is one of the two reasons this branch has not
gone out. So the rule stands; two things around it do not.

**What is actually missing.**
1. The gate proves a file exists and is dated after the change. It never proves Anthropic's
   `skill-creator` was the thing that produced it, so a session can satisfy it by writing a
   record by hand. That is the same defect shape as a check anchored on a comment.
2. No pass has ever run over the skills that did not change recently, so nothing has measured the
   ones that grew quietly. The rulebook is 24,682 bytes today.

**Done when:** every skill under `skills/` has been through the tool once, each report on record
under `docs/skill-review/` with the tool's own verdict quoted in it; the gate refuses a record that
carries no such quoted verdict; and the size of the rulebook and of `skills/director` is read with
`wc -c` before and after, both numbers written into this row.

**Links:** `guardrails/check-skill-review.sh`, `skills/director/references/landing-law.md` (the rule
itself), `spec/design-spec-review.md` (INV-208's home), every directory under `skills/`.

### ⬜ The product's performance after launch is tracked automatically — id: q-48
**Group:** Feedback & measurement · **Priority:** normal
**Source:** owner 2026-07-05.
**Closes:** q-49, q-96, q-100, q-469
**Absorbed:** 4 rows folded here 27.08, rotated off the board 28.08 — q-49, q-96, q-100, q-469. Full text: `docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md`.

**Acceptance:** A host's own status view prints that product's live numbers beside its tasks — how
the thing is doing since it shipped — fetched by the host's own tooling rather than by a person
going to look, and a test reds when the fetch is skipped or returns nothing. The same view carries
the result of a two-variant experiment when one is running.

**The trigger fired 24.07, and the row sat stale since — corrected 01.09.** The row's own text
called this "deferred on its own stated trigger: the first host with a live audience worth
measuring," as if that had not happened yet. It had, over a month before this correction:
the owner posted tlvphotos.com into three Russian Telegram groups on 24.07; sessions that day hit
21 against a 4–12 baseline, with 24 total campaign-labelled sessions over the following four days
(`~/tlvphotos/inbox/handled/2026-07-27-from-promoter-ga-campaign-numbers.md`). GA4 property
`544252011` is live and already read by `~/tlvphotos/scripts/ga_report.py`, and that same file
already reports organic-search visitors averaging 8.5 minutes on site against 23–70 seconds for
the campaign traffic. A live audience worth measuring exists and has been measured by hand for
weeks; the row's own text just never caught up to that fact until now.

**What the pack side owns, checked 01.09 against `INV-21`'s own requirement text**
(`spec/design-spec-review.md` Requirement 76, case "the reading machinery is promised" — "the
system *shall* keep the success-measure reading machinery promised under its own queue row").
One slice of it is genuinely built: the field-evidence route (`spec/customer-feedback.md`
Requirement 154, clause 4, `[INV-21]`) lands a person's reaction to a shipped feature as one dated
line in `FEEDBACK.md`, citing the feature's scenario — the human-triggered half of the promise,
shipped and traced. What is not built, and has no design authored yet, is the automatic half this
row's own acceptance names: fetch-by-the-host's-own-tooling, a status view that prints live
numbers unasked, and a test that reds when that fetch is skipped or empty. No spec chapter defines
that mechanism's shape yet (no measurement-plugin contract, no generic fetch interface) — it is a
feature that still needs its own spec-authored delta before code, the same as any other row here,
not something a single pass can freehand into existence without risking exactly the kind of
un-designed machinery this tree forbids building on spec.

**The remaining legs, split the way `q-163` splits its own method-versus-field halves:**
- **Pack-side (this row's own remaining work):** author the spec delta for the automatic-fetch
  contract — a generic interface a host's status-view tooling implements, and the red-when-empty
  test `INV-21` already promises — through `spec-author`, then build and trace it here.
- **Host-side, out of this window's tree:** wire tlvphotos's own status view to `ga_report.py`
  and Cloudflare so it prints live numbers beside its tasks without a person going to look — that
  wiring is `~/tlvphotos`'s own job, for a session inside that project's own window, once the
  pack-side contract above exists for it to implement against.

`INV-21`'s `[target]` tag stays live in `spec/design-spec-review.md`, so this row stays the open
owner `tests/test_traceability.py`'s `TARGET_ROW_OWNERS` checks against — closing it here would
orphan that promise. Still ⬜, not archived, not deferred on an unfired trigger: the trigger is
spent, and what is left is real, scoped work.

**Partially landed 02.09.** The pack-side contract this row's own remaining work named is now
authored, proven, and built. `spec-author`'s discipline ran first: `spec/success-measure-feed.md`
(Requirement 318) states the automatic-fetch shape — a JSON feed any host's own fetch tooling
writes, carrying a generation timestamp, its source in plain words, one or more named metrics, and,
where a two-variant experiment is running, its own block of exactly two variants — new invariant
`INV-324`. A self-run product-prover pass (`skills/product-prover-pack/SKILL.md`'s pack bindings)
checked the delta before any code: the pack-to-host split Requirement 267 already draws is cited
rather than restated, so no cross-cutting fact repeats; the neighbouring field-evidence route
(Requirement 154, clause 4) stays the human-triggered half, untouched, so the seam between the two
routes carries no blank answer; and every duty names its carrier (Requirement 316) — the two clauses
naming a host's own job (9 and 10) are written as a decided scope split rather than a `[target]`
promise, since nothing pack-side was ever going to perform them. `INV-21`'s own `[target]` tag stands
exactly where it stood: the reading machinery it promises is now real on the pack side alone, and the
host-side leg below is what keeps it open.

The machine: `scripts/check-success-measure-feed.py` reads a feed and reds a skipped fetch (no file),
an empty fetch (no metrics), a stale feed, and a malformed feed or two-variant experiment block —
proven both ways by `tests/test_success_measure_feed.py`'s twelve cases (red-proven live: each fault
case asserts its own red before the pass case is trusted). Traced at `architecture/guardrails.md`
(`INV-324`'s owns entry and the script's pin) and `matrix/guardrails.md`'s row `M-621`. Commands:
`python3 -m pytest -q tests/test_success_measure_feed.py` (12 passed) and
`python3 -m pytest -q tests/test_traceability.py tests/test_architecture_format.py
tests/test_index_generated.py tests/test_architecture_reference.py tests/test_matrix_reference.py
tests/test_scenario_heading_tag.py` (all green) prove the delta lands clean against the rest of the
spec, the architecture, and the matrix.

**What stays open, and whose it is.** Two legs of Requirement 318 name a host's own job and build
nothing here on purpose: writing the fetch tooling itself against a real source (a host's own
analytics account), and wiring a host's own status view to run the checker and print what it
confirms beside its tasks, unasked. That wiring is `~/tlvphotos`'s own job — GA4 property `544252011`
and `~/tlvphotos/scripts/ga_report.py` already exist there — for a session inside that project's own
window, once it reads this contract. This window does not do that part; it is out of reach for this
worktree the same way it was for q-163's field leg. The row stays open until that session runs.


### ✅ One command safely winds down all the work before you leave — id: q-235
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Sessions save tokens by reading only what they need — id: q-584
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A request meant for another project reaches it automatically — id: q-398
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ⬜ A broken promise between two projects is caught automatically — id: q-385
**Group:** Cross-project · **Priority:** normal
**Source:** split 2026-07-17.
**Deferred:** the first host declaring a contract in its card, the revisit trigger carried from the
original row. No host has declared one yet, so this stays queued rather than in hand.

**Reopened 2026-09-01.** Folded into q-398 on 27.08 ("Covered by: q-398 — A request meant for
another project reaches it automatically") and rotated off this board on 28.08. q-398 landed
2026-09-01 doing only its own stated acceptance — the routing-preamble hook (INV-190) — and never
touched this row's own promise, the same shape q-437 was found in on 31.08. The spec still carries
this as a deferred item in its own words: `spec/public-contract.md`, Requirement 194 criterion 15,
"the gate that reds a default-deny violation on the producer's suite *shall* stay promised until a
host's first real contract" [INV-185] [target]. A promise nobody is building stands here as its own
open row rather than inside a task that closed without it. Original wording, as row 385:
`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`.

**Definition of done:** three arms, red-proven against a real producer and consumer — a
producer-side gate reading the card's declared contracts and redding a published field with no
dated permission record [INV-185]; a consumer-side freshness check redding an artifact past the
consumer's declared staleness bound before any analysis [INV-187]; and a compatibility test redding
when the pinned version and the artifact's version diverge [INV-187]. The permission record's own
format lands with them, one home in the producer's tree.

### ✅ Independent work actually runs in parallel branches, proven live — id: q-386
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ A document's length never blocks a push over a made-up number — id: q-805
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ Automatic checks catch problems in parallel work before anyone has to look for them — id: q-804
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ✅ The front page is rewritten to be fully accurate — id: q-501
Closed. Full record: `docs/queue-archive/2026-09-04-closed-rows.md`.

### ⬜ The work board — worker lanes, timing, who's on what — builds once package 2 gives it a real trigger — id: q-816
**Group:** Board & visibility · **Priority:** normal
**Source:** restored 2026-09-03, correcting q-813 — `spec/work-board.md` Requirement 309 was
retired that same evening past what the owner had already settled the morning before:
`.live-spec/turnkey-contract-composed.md:305` records his 2026-09-02 12:46 word keeping
Requirement 309 and the rest of `matrix/work-board.md`, scheduled to build after package 2, never
retired. q-813's own closing text named the collision and left it open for his word; his word was
already on record, so no new decision was needed to restore this row.
**Deferred:** package 2 (the vertical path) closes, per `.live-spec/turnkey-contract-composed.md:305`
and q-806's own acceptance ("Package 2 ... does not start before this closes"). Until then this
stays queued rather than in hand — building it now, ahead of the schedule his own word already set,
is the same "don't serve machinery nobody needs" reasoning the contract itself argues from, just
pointed the other way: not never, but not yet.

**What it is.** `spec/work-board.md` Requirement 309 describes a kanban-style task queue for a
HOST project's own work — worker lanes, given-vs-actual time per task, per-agent attribution, one
stable published link — built on top of the same Canon `board.html` already renders for this
project's own plan. One piece of it stays retired on the owner's own same-12:46 word
(`.live-spec/turnkey-contract-composed.md:304`): the periodic ~5-second auto-refresh heartbeat
(former criteria 88, 90, 96, and the matching halves of matrix facts M-540/M-542) — that piece is
the one the contract calls "the one piece actually cut," and it stays cut here too.

**Acceptance:** `spec/work-board.md` Requirement 309's own criteria, minus the retired heartbeat
clauses above — a card per task, one lane per worker, given-vs-actual time, per-agent attribution,
one published link — proven live over one real stretch of work; **and**
`spec/live-status-reporting.md` Requirement 310 criterion 10 — once the board ships, a work block's
announcement home moves from the written plan page to the board's own per-task plan. Decided
2026-09-03: one row, not two, for one feature that happens to span two requirement files —
splitting it is fragmentation with no benefit. `docs/prover/2026-09-03-work-board-restoration-review.md`
finding F2 is closed by this widened wording, not by a second row.


## Environment — known traps

- A full local `pytest` run hangs at 0% CPU and never finishes. Run it narrowly with `-k` or a
  path; the full suite is CI-only. If it got started — find it and kill it by hand.
- `tests/test_guardrails.py` does a `git stash` and doesn't restore it on an interrupt. Commit
  before running it.
- `tiktoken` is installed into the system Python; the state script needs it to count tokens.
- Editing `guardrails/pre-push` requires `guardrails/install.sh` after it. Editing
  `skills/*/SKILL.md` requires `scripts/sync-skills.sh`, again on every repeat edit — otherwise
  gate m goes red.
- Pin registries (`.live-spec/r*-rule-*.md`, `architecture/*.md`) shift when lines are inserted
  or deleted in SKILL.md — check gate g.
- Prover and skill-review records get committed as separate commits.
- There are five real hosts: `tlvphotos`, `exhibition-engine`, `promoter`, `promoter-alexander`,
  `tc-cloud-validate`. The other 46 directories are working trees of the same repositories.
- Rescued files outside git: `~/live-spec-rescue-2026-08-26/` (133 files + 309 from
  `/private/tmp`).
- **Reserve for 26.08:** `live-spec-backup-2026-08-26.bundle`, 13 MB, full history, sitting in
  three places — `~/Documents/`, `~/OneDrive/`, `~/Google Drive/My Drive/`. To restore: `git
  clone <path to bundle> ~/live-spec-restored`. Made through `git bundle`, not through `git push
  --no-verify`: the mandate forbids `--no-verify` in its own separate line.

## What has been rotated off this list

Rows leave this list when they close or when the owner takes them off the board, and each one stays
findable in the archive it moved to. The pointers below are that record: read a row number here and
the file beside it holds the row's own text, word for word. The list they were rotated from was
called the roadmap until 27.08; it holds nothing now and rests in the attic, and this section is
where its pointers moved so one file carries the whole history of what left.

<!-- rotated-manifest -->
Rotated closed rows (base rule 10 — nothing lost; the archive keeps every moved row, grepable by number; the live queue below holds live material):
- rows 14, 27, 33, 42, 43, 62, 63, 67, 101, 121, 172, 189, 194, 196, 200, 201, 202 → docs/queue-archive/rotated-ROADMAP-2026-07-18.md
- rows 47, 59, 64, 99, 107, 109, 110, 115, 128, 130, 135, 136, 137, 138, 139, 145, 149, 150, 151, 152, 154, 155, 156, 157, 158, 159, 160, 161, 162, 188, 195, 209, 210, 211, 212, 213, 214, 216, 218, 219, 222, 223, 224, 225, 226, 227, 228, 232, 233, 237, 239, 240, 242, 244, 245, 246, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 303, 304, 305, 306, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 382, 383, 384, 387, 388, 390, 391, 392, 393, 394, 395, 397, 402, 403, 406, 407, 408, 409, 413, 414, 415, 416, 417, 418, 419, 420, 422, 423, 429, 430, 431, 433, 434, 438, 439, 441, 442, 443, 444, 445, 456, 461, 462, 463, 464, 468, 470, 476, 477, 478, 480, 482, 494, 495, 502, 506 → docs/queue-archive/rotated-ROADMAP-2026-07.md
- rows 522, 549, 555, 556, 557, 558, 565, 569, 571, 572, 573, 574, 577, 602, 618, 619, 626, 700 → docs/queue-archive/rotated-ROADMAP-2026-08.md
- rows 69, 197, 198, 199, 302, 307, 308, 309, 332, 389, 401, 425, 426, 428, 432, 435, 446, 447, 448, 449, 450, 451, 452, 465, 466, 467, 472, 473, 474, 475, 483, 498, 499, 500, 505, 508, 512, 513, 514, 515, 516, 518, 519, 520, 521, 523, 524, 526, 528, 530, 532, 533, 534, 535, 538, 539, 540, 541, 543, 544, 545, 546, 547, 548, 551, 553, 559, 560, 561, 562, 563, 564, 578, 579, 580, 585, 587, 594, 599, 600, 601, 603, 604, 606, 607, 613, 614, 615, 616, 620, 621, 622, 750 → docs/queue-archive/rotated-ROADMAP-2026-08-27-provenance-purge.md
- rows 44, 48, 49, 54, 93, 95, 96, 100, 108, 117, 118, 119, 129, 131, 133, 134, 140, 141, 143, 144, 148, 163, 165, 166, 168, 170, 171, 190, 191, 192, 193, 203, 204, 205, 206, 207, 208, 215, 217, 220, 221, 229, 230, 231, 234, 235, 236, 238, 241, 243, 247, 261, 381, 385, 386, 396, 398, 399, 400, 404, 405, 410, 411, 412, 421, 424, 427, 436, 437, 440, 453, 454, 455, 457, 458, 459, 460, 469, 471, 479, 481, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 496, 497, 501, 503, 504, 507, 509, 510, 511, 517, 525, 527, 529, 531, 536, 537, 542, 550, 552, 554, 566, 567, 568, 570, 575, 576, 581, 582, 583, 584, 586, 588, 589, 590, 591, 592, 593, 595, 596, 597, 598, 605, 608, 609, 610, 611, 612, 617, 623, 624, 625 → docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md
- rows 49, 93, 96, 100, 108, 117, 118, 119, 129, 131, 133, 134, 140, 141, 143, 144, 148, 168, 170, 171, 190, 191, 192, 203, 204, 206, 207, 208, 215, 217, 220, 221, 229, 230, 231, 234, 236, 238, 241, 247, 261, 381, 385, 396, 399, 400, 404, 410, 411, 412, 421, 424, 436, 437, 440, 454, 455, 457, 459, 460, 469, 471, 479, 481, 484, 485, 486, 487, 488, 491, 492, 493, 496, 503, 504, 507, 509, 510, 511, 517, 525, 542, 550, 552, 554, 566, 575, 582, 583, 589, 605, 617 → docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md
- rows 44, 95, 165, 193, 243 → docs/queue-archive/rotated-PLAN-2026-08-28-no-acceptance.md
- rows 596 → docs/queue-archive/rotated-PLAN-2026-08-28-no-reachable-outcome.md
- rows 405 → docs/queue-archive/rotated-PLAN-2026-08-28-q405-agent-messaging-stale-premise.md
- rows 453, 751 → docs/queue-archive/rotated-PLAN-2026-08-31-hostile-review-archive.md
- rows 811 → docs/queue-archive/rotated-PLAN-2026-09-03-q811-declined.md
<!-- /rotated-manifest -->
