# Decisions on record — what the pack believes you decided

TOUCHPOINT-KIND: decision-readback
DECISION-RECORD

The two lines above declare this file's kind to the checking scripts, and they stay where they are.

## The words this page uses

The pack is the shipped live-spec method: its skills, its document and suite templates, and its
guardrail scripts. The skills sit under `skills/` in this repository, and the pack carries a version.

The seat is the one orchestrating agent session. It owns judgment, briefs workers, and reports to you.
A worker is a delegated agent session the seat briefs for one bounded piece of mechanical work.

The tree is this repository and the files in it. A live document is a markdown file the writing rules
bind today. A record of what happened stays outside that set. The journal, this page, the prover
records, the readings, and the attic state what was written at the time.

A host is one project the pack attaches to. Each host holds its own spec, queue, journal, and
`.live-spec/` folder.

A code at a line's end points to its home. `INV-`, `E-`, `T-` and `D-` codes are anchors in
`PRODUCT_SPEC.md`. A `D-` code marks an open decision. The spec writes it as a gap line under the
criterion it touches. The gap line's shape: `[GAP: … is an open decision, recorded open in
DECISIONS.md. D-6]`. Roadmap and queue numbers are rows in `ROADMAP.md`, and a row rotated out of the
live queue sits under `docs/queue-archive/`. `M-` codes are rows in `TEST_MATRIX.md`.

`[[teach]]` and `[[wait]]` mark what a line is allowed to do. A teaching line introduces a capability
you have not met; a waiting line asks for nothing. `guardrails/check-touchpoint-kind.py` reads both
markers and treats an untagged line as waiting traffic. `scripts/render-doc.py` passes them through to
the rendered page.

Some entries below rest on a message of yours written in Russian. The message stands as you sent it,
with an English rendering under it.

## What this page is

This is the read-back surface (`PRODUCT_SPEC.md` INV-207, roadmap row 415 in
`docs/queue-archive/rotated-ROADMAP-2026-07.md`). Each line under **On record** sets down a decision as
yours. Each one names the exchange it came from, so you can go back and check it. Read it on your own
clock, and strike anything you never said — move it under **Struck** with a one-line note. A struck
line is retracted and never deleted; nothing here vanishes. The pack renders this file for you through
`scripts/render-doc.py` when you ask. [[teach]]

The rule the gate holds: a decision recorded as yours must name its exchange — at minimum a date.
`guardrails/check-authority-anchor.py` is that gate. It scans this file at push and refuses an
on-record entry that carries no date. A line with no exchange is a challengeable judgment moved into
the one slot nothing questions. That is the defect this surface exists to catch. [[wait]]

## On record
<!-- record:on -->
- 2026-08-17 ~23:30 — the short chat-law reminder is the shipped norm for every host, not a
  personal overlay on your machine. Answering the coordinator's direct question — should the short
  form be the norm for everyone who installs the pack, or only on your own machine. Your words in
  chat: норма для всех конечно же. ты же обслуживатель всех проектов, елкипалки. In English: the
  norm for everyone, of course — you serve all the projects (closing with a colloquial aside, kept
  above as you wrote it). Consequence: the hook that opens every prompt names the seven session
  laws and points at the two files holding their wording, and it ships that way to each host; the
  pack no longer believes the earlier decision that the hook must retell the laws in full, so the
  records written under that belief follow this one instead. The word reached the night's work
  through the coordinator; the time is when it reached this seat, not when you typed it.
- 2026-08-13 08:51 — rule 31's "owner" is the agent that owns the zone (row 536, first ruling).
  Your words in chat: я никогда не видел правила 31! откуда мне знать что такое этот оунер. если
  это про агентов, тогда это агент. Consequence: everywhere rule 31 says "owner" about zone
  matters, it means the owning agent; a clause that genuinely needs you personally must name you
  explicitly, and the sweep of rule 31's text for that distinction rides whichever path the
  13.08 comparison decides.
- 2026-08-13 08:51 — the six stage-3 check questions are the seat's to rule on. Your words in
  chat: вопрос 3 мне там нечего решать это твоя внутренняя механика. Consequence: the seat rules
  on the fifteen silent-rot keeps and gates ae, n, p, o, ab itself, records each ruling as its
  own judgment under this delegation, and executes them at a landing; nothing in that set
  returns to you unless it changes what you personally meet.
- 2026-08-13 08:51 — the one-command-install check (D7) is postponed. Your words in chat:
  установка одной командой пока не настолько важна. Consequence: D7 leaves the waiting list and
  returns on your naming it; the README promise stays as is until then.
- 2026-08-07 11:19 — an inbox request is written down, and nothing stands in the way; a deposit
  never blocks a push. Your words in chat: это просто заявки; их надо записать и чтобы ничего
  не мешало; это баг; записать точно надо, а пуш тут при чем. The message check moves to the
  intake sweep as its one judging moment; the push chain reports what the sweep will meet and
  proceeds. You also released the push with the two deposits still in the inbox, and named the
  gate's old wiring a bug.
- 2026-08-07 09:16 — every number the process invented is found and rooted out (row 576). Your
  words in chat: вообще надо найти ВСЕ эти дебильные числа которые ты придумал и выкорчевать.
  The sweep, the eight-group ruling, and the first removal batch run under this word; the
  rulings page is yours to strike line by line.
- 2026-08-07 09:11 — the frozen task wording binds now, reaffirmed (rows 166 and 566). Your
  words in chat: we said we will communicate exactly in the same terms in the plan, when the
  plan was set; that was supposed to be in the spec — is it, and why is the session speaking
  differently? Answered with the citation: the law stands as the work-board requirement's
  criteria 49 and 58 (Requirement 309). The session had taken tasks into work without written
  statements; two statements were written, validated by a clean reader, and frozen the same
  morning, and every mention now speaks them letter for letter.
- 2026-08-07 09:11 — the README's published line-count boast is struck (the rulebook cut, row
  570). Your words in chat, on the six-thousand-line heading and the floor test holding it: I
  never asked for a number, again; you made it up. The heading and its floor go. The same-class
  three-hundred-records sentence goes with them, on your recorded class rule; strike this line
  if you want that sentence back. The measured-count block with its verification commands
  stays, since it states facts with their sources. The class, restated: a published measurement
  may state a fact, and no measurement becomes a standard or a selling claim without your word.
- 2026-08-07 ~01:10 — no numeric size caps on specifications; the standard is no redundancy (the
  cost audit, row 568). Your words in chat: the number is unjustified; a text should just have no
  redundancies — when you look at it, there should be nothing you can remove without losing the
  information; maximum size is beside the point; if reaching that takes many reviews and that is a
  problem, tell you about it. This strikes the audit page's proposed per-size sentence caps.
- 2026-08-07 ~01:10 — no self-invented numeric standards anywhere (the cost audit, row 568). Your
  words in chat, on the test-run time budget: it should be best and justified effort; why invent
  numbers and then hand you the values to think about. The invented 360-second budget is dropped;
  the record keeps measured numbers only. The class: every standard the process holds itself to is
  either yours, derived and justified, or absent.
- 2026-08-07 ~01:10 — the test plan's timing was never a question (the cost audit, row 568). Your
  words in chat: it is derived from the product and architecture specifications, as already said.
  So the written rule stands — the test plan starts once those documents exist and are settled;
  the audit page's question on it is withdrawn as already answered.
- 2026-08-06 ~21:49 — a task in work absorbs new words, and every task keeps an on-demand history
  (row 166, Live work board). Your words in chat: people have ideas in the flow, so a task already
  in work can be updated multiple times — the flexibility is the point of an AI-run delivery
  process, and how that is implemented and displayed must be thought through; a log per task,
  accessible on demand ("here you wanted this while it was in progress"), is agreed; you had not
  received research on kanban tools for inspiration; and it is time for the adversarial review of
  this feature's specification. You asked what the next steps are and whether we are still
  exploring — answered: still inception.
- 2026-08-06 ~21:35 — every new wish is placed in the task graph (row 166 and intake law). Your
  words in chat: when a new wish comes, it should be determined how it relates to what came
  before; the seat maintains all the tasks and their relations in its head, so it can always find
  the best implementation path, seeing possible parallelism and dependencies.
- 2026-08-06 ~21:34 — the stage ladder gains inception (row 166, Live work board). Your words in
  chat: "in work" means the item is clear and in the pipeline; before it sits the backlog of all
  kinds of ideas, then inception, where either everything becomes clear and the item moves to
  ready, or your input is needed — so one more stage stands between the backlog pile and ready,
  and that is where the board task itself stands now. "The board's rules, written and twice
  reviewed" is inception's product, never an execution subtask. Subtasks carrying info must be
  collapsible. A fresh wish arrives already connected to the feature and spec part it touches, as
  decided earlier. You also asked to reach a clean point so the session's context can be wiped.
- 2026-08-06 ~21:16 — a card's plan is a short list of deliverables (row 166, Live work board).
  Your words in chat: no need for both numbers and emoticons; a task never carries a hundred
  subtasks — like in every agile it splits into fewer deliverables, and the subtask list is never a
  log of everything (tonight's acceptance is a single bullet on the in-progress card); no legend —
  everything self-explanatory; the blue vertical lines in the subtasks questioned; "that sample is
  variant 3" is opaque; and whatever is in work is something the seat can take on its own without
  questions — you hope most tasks will be like that. The same turn asked: maybe find some kanban
  process skill and learn from it if needed — answered the same evening by the two studies, the
  method's and the tools'.
- 2026-08-06 ~21:00 — the board reads whole, soon (row 166, Live work board). Your words in chat:
  ideally, soon enough, you want to see everything on the board — all the backlog tasks — readable;
  there is one source of truth, every task referred from the product spec and the architecture; the
  done tasks need hiding as they will become a pile; the in-card step statuses should be emoticons
  too; a comment on every step about what was done is good and must be utterly understandable as
  well; the sentence "It replaces asking the agent how things are going" is broken English again;
  and the Live work board task now reads understandably. Two more remarks of the same turn: where
  the frozen standard lives was unclear to you (answered in chat at ~21:01 — a frozen copy under
  the project's documents folder, held and opened by the builder); and you may never open the
  board yourself — the seat holding this representation being sort of enough — a purpose remark
  the board's design carries: the page serves your eye when you want it, and binds the seat's own
  bookkeeping always.
- 2026-08-06 ~20:47 — the variant-5 board form holds, with four amendments (row 166, Live work
  board). Your words in chat: the board looks good now; the done part should be with emoticons to
  save the place — readability is the main thing; the same names will be referred in every
  communication, this window included; the "more" part auto-closing is frustrating; a reference
  like "17 findings" must say what the findings are and how they relate to the specific task; and
  option bullets have no place on a card already in progress — options are shown way before the
  ticket is accepted.
- 2026-08-06 ~20:36 — the variant-4 tiles failed your read, and the board gains lanes and per-task
  technical details (row 166). Your words in chat: there are also lanes for parallel agents, and
  also info per task like what is the branch and worktree; frankly, you do not get what is on the
  kanban shown — the tiles do not look like tasks, it is a text you need to crack your mind to
  understand. Verdict held as the card law: a card reads as a task at a glance — authored handle
  first, behavior line, chips — and technical details sit behind the card.
- 2026-08-06 ~20:35 — approvals are rare; transparency is the standing ask (row 166 and the method
  wide). Your words in chat: you do not like the idea of manual approval for everything; it should
  be rare — maybe more in the start, but in three to six months, as models grow up, readability and
  consistency improve anyway, and all you will need to see is transparency. Same message, the card's
  reading order: the short name is a super-sharp semantic handle — the "ah, this is what I think it
  is" recognition every time the ticket is referred — then the description describing the behavior,
  then all the other details. And a task is a part of the product spec, and that part is featured on
  the board.
- 2026-08-06 ~20:16 — the board is a kanban over the whole queue (row 166). Your words in chat,
  looking at the variant-3 sample: the page shows and maintains all the tasks — done, in progress,
  and the roadmap; each task carries a super-understandable short referrable name, a description
  that describes the behavior, a time estimation, a tag naming the feature it belongs to or that it
  crosses several modules, and an attached plan saying what can run in parallel if the budget
  permits; the whole reads as a kanban board showing progress and which worker is doing which task;
  recurring workers may get names and icons, personalities to be developed and shown for your eye.
- 2026-08-06 ~19:28 — the board's tasks carry time accounting (row 166). Your words in chat,
  opening the evening: work down the list — a one-time instruction for that session, which the
  seat read as resuming the queue's head; and for every task, add the time the seat estimated for
  it and the time it actually took. Both figures
  stand on the task's board row, at take-up as the estimate and at the close as the pair.
- 2026-08-06 ~19:17 — the work board is the next movement, ahead of the rest of the queue (row 166).
  Your words in chat: every task carries a name that is understandable, a description that is
  understandable, and a plan that is understandable; once approved, that wording freezes, and the
  seat speaks of the task in those words letter for letter — at take-up, along the way, and at the
  close. The same movement carries a validation step in front of the board: nothing enters work
  before it passes that check.
- 2026-07-27 ~11:35 — the repository carries no git tags. You never asked for them. The four that
  existed had stopped being made eight releases ago, which read as a machine misfiring. The version
  lives in `VERSION`, the release history in `JOURNAL.md`. The four deleted tags and the commits they
  pointed at are recorded in the journal, so any of them can be restored exactly.
- 2026-07-05 — `~/.claude/CLAUDE.md` became a thin loader: it now names the files a session reads
  before work starts. The working contract moved into the personal profile at
  `~/.claude/live-spec/profile.md`, and the method moved into the live-spec pack. You gave your OK
  that day.
- 2026-07-06 — the build-lane cap is three parallel lanes; a fourth opens only on your asked word
  [T-18]. A lane is one build train a session rolls through the pipeline.
- 2026-07-12 ~00:31 — live-spec runs on the Opus model as its default orchestrator. The seat briefs a
  worker and accepts the worker's result, and the worker does the drafting and the applying. Fable,
  the model used for the harder passes, runs only on your word.
- 2026-07-17 ~15:26 — nothing waits on a roster of agents. A dynamic system's permanent members
  declare themselves. A host declares itself by writing an agent card, the file `.live-spec/agent.md`
  naming its name, mission, zones, published contracts, and inbox address. Discovery is a live scan
  bounded to two directory patterns under each root, `<root>/*/.live-spec/agent.md` and
  `<root>/*/*/.live-spec/agent.md` [E-32, INV-184]. The pack maintains no ratified list.
- 2026-07-17 ~16:07 — every point of contact with the person has a kind, and the kind decides what
  may be said there. `guardrails/touchpoints.json` holds the kinds, ten of them today, this page among
  them under the name `decision-readback`. You named this the shape the rest of that work was built on.
- 2026-07-17 ~16:58 — a cleanup path announces what it ended: the identity, what it was, and the proof
  that the run owned it. That notice ships first, ahead of the stricter owned-identity check. The
  strict check takes a numeric process group the run owns [INV-204, INV-162]. It matches no program
  name. You run no python yourself, so a program-name match collides only where someone else runs one.
- 2026-07-20 ~14:34 — every code's plain description follows one form. Name the thing in a positive
  sentence. Where the rule governs a class, name the class and give a representative handful of its
  members. You read a sample of fifteen described codes at
  `docs/migration-sample/2026-07-20-backdescribe-sample.md` and accepted the form. You asked that a
  class-member list stay representative [E-35, INV-239].

- The pack's own repository counts as a host of the pack, so three projects run under it: the music
  producer's coach, the photo site, and live-spec itself. Asked 2026-07-27 ~18:09, because the public
  page said two while the architecture and the test matrix named three real hosts. Your word at ~18:11
  was that live-spec is the third, unambiguously. The page now says three.

- 2026-07-28 ~19:55 — a document is clean only once a reader has read it through the audit skill at
  `skills/text-audit/SKILL.md`. The reading covers every live document in the tree. Your words:

  ```text
  короче если аудита не было, то файл не "чистый", ultimately каждый файл читается именно через аудит. согласен? норм?
  ```

  In English: a file counts as clean only after an audit, and ultimately every file is read through
  the audit. Agreed? All right?

- 2026-07-28 ~20:48 — the queue is ordered by what enters a working context earliest. The entry
  documents and the pack skills stand at the front, and the queue then runs on through the rest of
  the tree. Your words:

  ```text
  давай без "потолка" это должно было отсечься! нет? про то что документы всегда same or better согласен, главное механизмы держать эту марку. порядок документов ты выводил раньше! мы сказали что начнем с тех которые первыми загрязняют твой же контекст. найди их сам. next steps? скиллы аудита (им все проверяем)? потом спеки? какие то вспомогательные файлы потом? понимаешь ход мысли? просто все подряд мы делали это плохо особенно когда походу загрязнается контекст. надо идти всегда из точки где контекст чист максимальной гигиеной.
  ```

  In English: drop the ceiling, which should already have been cut out. On documents always coming out
  the same or better, agreed, and the point is that mechanisms hold that mark. You derived the document
  order earlier: we said we would start with the ones that pollute your own context first. Find them
  yourself. Next steps? The audit skills, since everything is checked with them? Then the specs? Then
  some supporting files? Do you follow the reasoning? Taking everything in any order went badly,
  especially as the context gets dirtier along the way. Always start from a point where the context is
  clean, with the strictest hygiene.

- 2026-07-28 ~20:48 — a document comes out of an edit the same or better. What is compared is the
  document's readability before the edit against its readability after. Mechanisms hold that mark, and
  a session's own care is too thin to hold it. The exchange is the ~20:48 message quoted above, which
  carries both calls in one breath.

- 2026-07-28, at `15:09 UTC` — a reading is owed at a minor version bump, and after a large growth
  in a document's size. The size threshold stands unset: this exchange named no number, no unit, and
  no baseline, and no file in the tree sets one. The reader is an agent session, and the pack asks a
  person for no reading. You raised the major bump first:

  ```text
  Надо тогда поставить чтение агентом (не человеком как ты ошибаешься и говоришь) когда дибо размер сильно вырос либо когда major version?
  ```

  In English: so we should set up a reading by an agent. You keep calling it a person by mistake. The
  trigger is either a large growth in size or a major version?

  Hearing that a major bump is rare, you moved the trigger down at `15:12 UTC`:

  ```text
  Минорную ок.
  ```

  In English: the minor one is fine.

- 2026-07-28 ~21:40 — the night's three moves run in this order. Take the worker's report on the
  chat-law text, install the repaired file, and run the suite. Then make a recorded count refuse to
  rise. Then commit the prover record, then the rest by name, then push on a green suite. Your words:

  ```text
  дальше три хода по порядку:
  1. принять отчёт работника, поставить починенный файл в ~/.claude/hooks/, прогнать суиту
  2. починить гейт счётчика так, чтобы записанное число отказывалось расти
  3. закоммитить запись проверяющего, потом остальное по именам, потом пуш на зелёной суите
  ```

  In English: next, three moves in order. One, accept the worker's report, install the repaired file
  in `~/.claude/hooks/`, and run the suite. Two, fix the counter's check so the recorded number refuses
  to rise. Three, commit the reviewer's record, then the rest by name, then push on a green suite.

- 2026-07-28 ~21:40 — a worker's prompt is written by a separate clean worker. A clean worker is a
  fresh session that has no pack rules loaded. The seat writes none of the prompts. You settled this
  earlier the same day, at ~18:06, in an exchange this file does not carry. This turn restates it as
  standing. Your words:

  ```text
  правила работы: промпты работникам пишет отдельный чистый работник, не ты.
  ```

  In English: working rules. A separate clean worker writes the prompts for workers, and you write none
  of them.

- 2026-07-28 ~21:40 — every clarification you have to ask is a defect in how the pack talks to you.
  The class behind it goes into `guardrails/language-rules.json`, and it is swept across the whole
  tree. Your words:

  ```text
  каждое моё уточнение —
  это дефект связи, находи класс в guardrails/language-rules.json и выметай его по всему дереву.
  ```

  In English: every clarification of mine is a defect in communication. Find the class in
  `guardrails/language-rules.json` and sweep it across the whole tree.

- 2026-07-28 ~21:40 — the seat runs its own replies through `scripts/preshow-register-lint.py` before
  it sends them. Your words:

  ```text
  свои
  реплики прогоняй через scripts/preshow-register-lint.py до отправки.
  ```

  In English: run your own replies through `scripts/preshow-register-lint.py` before sending them.

- 2026-07-28 ~21:40 — a question the handover parks for you stays yours, and the session leaves it
  alone. A handover is the file a closing session writes for the next one, and handovers live under
  `docs/handovers/`. The handover you read at that moment named two questions as waiting. One of them
  you had answered at ~19:55 the same day, in the entry above. Your words:

  ```text
  два вопроса ждут меня, они в файле передачи. не начинай их решать сам.
  ```

  In English: two questions are waiting for me, and they are in the handover file. Do not start
  settling them yourself.

- 2026-07-28 ~21:44 — a session that has closed can answer none of the questions it parked for you.
  This observation opened the night's largest piece of work: the standing read of the previous
  session, recorded in the next entry. It stands as Requirement 303 in `PRODUCT_SPEC.md` and row 522
  in `ROADMAP.md`. Your words:

  ```text
  я только не понял кто займется вопросами из файла передачи :) потому что та сессия уже закончилась
  ```

  In English: I just did not follow who will take on the questions from the handover file, because that
  session has already ended.

- 2026-07-28 ~21:58 — a fresh agent reads the previous session, always, as a standing process. The
  reader is cheap by your word. You put it as a proposal and left before the built shape came back to
  you. It stands in the tree as Requirement 303 in `PRODUCT_SPEC.md` and row 522 in `ROADMAP.md`. Your
  words:

  ```text
  тогда имеет смысл дешевым воркером всегда читать прошлую сессию? как процесс? всегда?
  ```

  In English: does it make sense, then, to have a cheap worker always read the previous session? As a
  process? Always?

- 2026-07-28 ~22:10 — the night runs on clean agents that spawn further clean agents, with the
  context guarded and without you at the keyboard. The same turn stopped on one phrase of the reply
  you were reading, `и корень из них первый`, which you called unclear. That phrase renders as "and the
  root of them first". Your words:

  ```text
  "и корень из них первый." непонятно. все, я пошел спать. береги контекст спавни агентов чистых которые спавнят еще агентов. что думаешь что сможешь закрыть когда эти агенты закончат работу?
  ```

  In English: "and the root of them first." Unclear. That is all, I am off to sleep. Guard the context,
  spawn clean agents that spawn further agents. What do you think you can close once these agents
  finish their work?

- 2026-07-28 ~23:52 — the session report is the table and plan of parameters, filled from concrete
  checks. That table and plan is `docs/reports/2026-07-28-document-state-and-plan.md`. Every number in
  it is real, and each one traces back to a transcript. Your words:

  ```text
  пс помни что у тебя была таблица и план со всеми параметрами которые ты сказал что будешь постепенно заполнять на базе конкретных проверок! вот это я от тебя и ожидаю когда будет отчет сессии, и что все цифры настоящие! все в транскриптах
  ```

  In English: remember that you had a table and a plan with all the parameters. You said you would
  fill them in step by step from concrete checks. That is what I expect from you in the session
  report, and that every number in it is real. It is all in the transcripts.

- 2026-07-29, morning — a place where a reader stops counts against a document only when both readers
  of one round stopped there. A place one reader of the round found is recorded as residue in
  `docs/language-defects.md`, and it blocks nothing. This is the pack's own reasoning, so strike it
  freely. The session settled it in chat and wrote it down nowhere, which is the defect your 12:08
  instruction closes. The ground is the first three of six rounds of readings on
  `skills/text-audit/SKILL.md`. They returned fifteen and ten blocking stops, then five and eight,
  then nine and four. Those six records are
  `docs/language-reads/2026-07-29-read17-text-audit-skill.md` through `read22` of the same day. Each
  round gave two fresh readers the whole file and the reader prompt from `skills/text-audit`. A
  blocking stop is one place a reader could not go on. No reader's list repeated from one round to the
  next: each fresh reader named a set of its own. Inside a single round the two readers did stop at
  some of the same places. That agreement is what closes the reading loop, and it is the number
  `guardrails/progress-baseline.json` records per round. All six rounds stand there, readings 17
  through 29, agreeing on 8, 3, 2, 2, 2, and 3 places.

- 2026-07-29 12:08 — every decision about how the work runs is written down. A decision that lives only
  in chat does not exist. The entry above is the first one recorded under this instruction.

- 2026-07-29 12:08 — a number is never handed to you on its own. Whenever a number is stated to you, or
  written into a document, it carries four things. Why it is measured: the decision it informs, or the
  question it answers. What changes when it moves: what the project does differently if it rises or
  falls. Its unit: what is being counted, in what. Its method: the command or the procedure that
  produced it, so a reader reproduces it. A number stated without those four is a defect. You bound
  this to chat and to the skills, and you asked that a gate hold whatever a gate can hold. The case on
  record is this session's own sentence. A reader returned a count of stops. The sentence named none
  of the four: what a stop is, what the count decides, and how it was produced. The instruction
  reached this session through another session, so no words of yours stand here.

- **A text ships when both cold readers return nothing that blocks, twice in a row.** Alexander
  2026-08-05 at 22:52, on being handed the bar as an open question: quality never suffers, whatever
  else does. He rejected the framing that offered him a choice of bars. His sentence leaves the
  strictest reading standing: zero blocking places for both readers, held over two consecutive
  rounds, which is the bar already in force. The two looser shapes the session had offered are
  closed by it. The audit skill `skills/text-audit/SKILL.md` states this bar, and the loop runs to it.
- **The templates stay in the reading queue.** This is the pack's own reasoning, so strike it freely.
  A reviewer objected that the census had stopped measuring twelve template files on the ground that
  nobody reads them, while `README.md` sends a person starting a new project to exactly those files.
  The session judged the objection right and returned them, in commit 3b4308d on 2026-08-05. The test
  fixtures stay outside, since a test opens them by path and no person reads one, which is the audit
  skill's own rule for machine-read text. Alexander said nothing on this question. Asked about it at
  22:52 he answered that he had not understood it, and the next morning he was still asking what the
  templates are. An earlier form of this entry stood in his name; the adversarial review of
  2026-08-06 caught it.

- **One plan until it is done.** Alexander 2026-08-10 21:26: «даже если план в этой сессии не
  закончим в следующей над тем же планом всегда работаем. если сессия прервалась тот же план
  заново. все статусы тоже по тому же плану», and the reminder he asked for: «ты можешь сделать так
  чтобы гарантировать что если даже я ошибусь то ты хотя бы мне напомнишь про план (пока мы его
  весь не сделали)?». The standing order lives in `NEXT_STEPS.md`'s live-state block: the plan is
  `.live-spec/culling-plan-v3-2026-08-10.md` over the frozen base of 2026-08-08, every session
  resumes it, every status speaks its step codes, and a request of his that leaves the plan gets one
  reminder line before anything else happens.

- **The plan file gets a hand-slap guard — his one exception to campaign rule 2.** Alexander
  2026-08-10, evening: «ты поставил проверки бить себя по рукам при каждом коммите плана где
  ненужные изменения которые ты сам придумал?» — read as the order to install exactly that, and as
  the exception rule 2 reserves for his word. Scope: the plan file alone. Mechanism:
  `.live-spec/check-plan-delta.sh`, run as a local pre-commit step — a commit touching the plan must
  stage a `.live-spec/plan-v3-delta-<date>*.md` page carrying one rooted line per changed hunk. It
  stays outside the frozen gate roster until the campaign's closing ruling (plan v3, D9).

- **The plan-v3 sitting, first pass.** Alexander 2026-08-11 10:23, reading the D-section: D1 yes
  («вроде очевидно, не понимаю зачем тут меня спрашивать» — and the lesson lands: the obvious is
  never parked on him). D4 yes («д4 ок»). D8 yes («д8 ок»). The 3,095-runs, zero-catches figure
  behind D8 is a decision-time reading, not a logged measurement: `guardrails/net_meter.py` names
  the arm's would-be log as `.live-spec/net-meter.jsonl`, and no such file exists on the machine.
  The figure first stands in `JOURNAL.md`, 2026-08-11 11:08-12:00, at execution, and its absence of
  a recoverable source is confirmed at `docs/prover/2026-08-11-thirty-commit-range.md`, finding 12.
  D7 scheduled, later, and it blocks
  nothing («давай сделаем но если со мной то не сегодня»). D2 agreed in substance («согласен,
  чушь»), execution waits until the one-sentence fix reads clear to him, and he asked for the
  cause of the communication failures, answered in chat the same minute. D3 open on his three
  questions: what defines a failure class, class or same failure, why twice. His 2026-08-10 21:28
  «остальные два пункта тоже не понятны» named D7 and D8 of that evening's list; both carry his
  10:23 ruling above. D5 open («вообще не
  знаю что это и зачем»); the base two-hour order stands until his word. D6 struck in its old
  shape («какая-то выдуманная чушь»): the five-artifact escort itself is the defect. D9 open
  («не понял»). His direction for the whole campaign, verbatim: «мне кажется там много накопилось
  совсем ненужного. и его надо как ты сказал выпиливать а не чинить».

- **Plan parts wait for his review once submitted.** Alexander 2026-08-11 10:23: «тут ждало моего
  пересмотра, а вместо этого ты что то начал делать». Standing order: after a plan is submitted
  for his «принято», the session executes nothing from it except what he ordered directly, until
  the review happens. Work his written word already covers elsewhere is named to him before it
  starts.

- **The plan-v3 sitting, fourth pass.** Alexander 2026-08-11 21:22 in chat: the plan is accepted
  («мы же приняли план») — the «принято» the plan waited on. D2 read as «делай» from «давай все
  это правь» after the D3-absorption explanation; the seat states this reading as its own and he
  can strike it. Standing form of work: maximum delegation, Fable for orchestration and
  exceptional tasks only, maximum context hygiene («фиксируй форму работы…»). Push completed
  22:15, 34 commits e82da27..dfa9f57, first push under the one-record rule.

- 2026-09-02 ~14:24 — a fact rendered on a status surface (board, Canon, or any future one) that
  can be derived from what already exists is always computed live at read time, never stored as
  its own hand-set field. Answering the coordinator's own concrete case — whether "these two
  tickets can run in parallel" should be a field on a ticket. Your words in chat: "параллелности
  принял но надо записат что это must parameter calculated in real time или чето такое?" In
  English: accepted the parallelism point, but this needs writing down as a parameter that must be
  calculated in real time, or something like that. Consequence: no surface stores a fact another
  file already carries the raw material for; it reads that raw material and computes the fact each
  time, the way `state-probe.sh` already computes a done mark's real status from its acceptance
  command rather than trusting the stored ✅. The turnkey contract's parallel-visibility note
  (`.live-spec/turnkey-contract-composed.md` §8) already follows this; this entry makes it a
  standing rule for whatever comes after that too.

- 2026-09-02 ~14:24 — an invented number (a ceiling, a count, a cap seeded from nothing but a
  document's own past state) is removed the moment it's found, on sight, and no new one is ever
  added — a standing rule, not a one-time cleanup. Extending q-805's same-day cleanup
  (`51d2d402`, closed on his live word "все цифры с потолка уходят") from an event into a
  permanent law. Your words in chat: "про числа с потолка наверное надо тоже вписать чтобы
  искоренять если найдем и не добавлять?" In English: about invented-from-nowhere numbers,
  probably also need to write down: eradicate on sight if found, and don't add new ones.
  Consequence: `guardrails/check-size-ratchet.py`'s whole class (any check failing a document
  against a bound seeded from that document's own past measurement) stays retired for good, never
  reintroduced by a future session solving a future problem the same way; a session that finds a
  new instance removes it on sight rather than filing it for later, the same standing habit as a
  confirmed-bug class sweep (base rule 14).

- 2026-09-02 — starting a session should cost about a quarter of what it costs today, and every
  standing document either earns its place or goes. Your words in chat: "80кб много. можно
  удешевить? раза в 4?" In English: 80 KB is a lot. Can it be made cheaper — four times over? And,
  on the files themselves: "зачем decision если есть доска и journal? нам точно все файлы
  нужны?... я понимаю что куча твоей бухгалтерии внутренняя но и она если избыточна то надо
  чинить." In English: why do we need a decisions file if there's the board and the journal? Do we
  really need all these files?... I understand there's a pile of your internal bookkeeping, but
  even that needs fixing if it's excessive. Consequence: PLAN.md q-809 states the requirement
  impersonally and points here; its definition of done is the four starting documents cut to about
  a quarter of today's 80 KB with no rule lost, and every standing document in the tree named with
  a one-line answer to "what breaks if this is gone."

- 2026-09-02 14:50 — the blocked mark is reserved for work that genuinely cannot proceed; it is
  never a stand-in for a task whose own check quietly stopped passing. Your words in chat: "blocked
  is not 'reopened' не надо абьюзить статусы либо не по назначению, либо свои выдумывать." In
  English: blocked is not "reopened" — don't abuse statuses, neither off-label nor inventing your
  own. Consequence: PLAN.md q-807 states the requirement impersonally and points here; a task whose
  acceptance check has stopped passing returns to the queue (or to in-hand if someone picks it up)
  with a plain note, never the blocked mark.

- 2026-09-02 14:50 — the task list must read in language a person outside the work can follow.
  Your words in chat: "я понимаю таких треть. это плохо надо понять что надо пофиксить в промптах
  или чето такое." In English: I understand about a third of these. That's bad — need to figure
  out what needs fixing, in the prompts or something like that. Measured live in the same exchange:
  of the task lines shown, about one in three were understandable. Consequence: PLAN.md q-808
  states the requirement impersonally and points here; a reader outside the work must be able to
  say, for each task line, what it gives them and what state it is in.

- 2026-09-02 ~21:31 — a task closes when the seat carries it to a shown result, not when your eye
  approves it; a shown result you don't like becomes a new task, never a block on the one that
  shipped. Your words in chat: "доска вживую зачем мой глаз... если у тебя есть задача, то ты ее
  работаешь, если задача непонятна, тогда ты ее обсуждаешь. если ты ее взял в работу тогда ты
  доводишь до того чтобы показать и это 'сделано', если не понравится тогда будет новая задача."
  In English: why does the live board need my eye... if you have a task, you work it; if a task is
  unclear, you discuss it; once you've taken it into work you carry it through to showing it, and
  that is done — if it isn't liked, that becomes a new task. Consequence: PLAN.md gains q-810 —
  `director/SKILL.md` states that a shown, ordinary delivered result closes the checkpoint in the
  same step, and a row's own "needs his eye" gate is reserved for a taste call, a trade-off no
  artifact settles, or a change to the definition of correct, never for verifying a delivery a
  command or a plain read already confirms. `q-166`'s own acceptance line named his eye as the only
  check on an otherwise-ordinary result; closed under this rule the same night, on the reasoning
  that its remaining scope was never actually asked for again after 08-06 and the daily need it
  answers already ships. Carried forward unchanged: an action genuinely irreversible outside git
  still stops for your word before it runs, never only after it is shown (rule 12/17) — this
  decision is about when a built, reversible result counts as done, not about that gate.

- 2026-09-02 ~22:05 — the Director states its own disagreement with a request before executing
  it, as a step inside accepting work, not only as background personality. Your words in chat:
  "ты всегда можешь спорить если не согласен. не надо тупо делать потому что потом еще не
  поймешь что сделал и результат не порадует." and, catching that this session had just treated
  that remark as a passing reminder instead of running it through the same process a feature
  request gets: "ты сам по моей идее использования этого скилла лайвспек ты сам сейчас должен
  был бы понять что это фича... понять куда вписать, посмотреть влияет ли на архитектуру, добавить
  тест." In English: you can always argue if you disagree — don't just blindly execute, or you
  won't understand later what you did and the result won't satisfy. And: by my own idea of how
  this pack works, you should have recognized that remark itself as a feature, worked out where
  it belongs, checked whether it touches the architecture, and added a test. Consequence:
  `director/SKILL.md`'s Execution section states the rule at the acceptance step itself — writing
  a decision sheet is also the one moment to weigh whether the request is right, and a flaw the
  Director can see gets stated before the checkpoint opens, not folded silently into how the work
  gets built. This was already a personal standing rule (`~/.claude/CLAUDE.md`); what changed is
  that it now rides inside the Director's own procedure rather than only the personal layer. No
  architecture-level entities, states or transitions change — this is a procedural rule about how
  the Director's own step runs, the same shape as rule 12/27's existing taste-and-trade-off carve-
  outs, not a new node. A test lands with `q-810`'s own closing-rule eval (in flight the same
  night), which already needed a scenario distinguishing an ordinary delivery from a genuine fork
  the human owns — a scenario where the request itself is flawed extends that same set rather than
  standing up a second harness. No new PLAN.md row opened for this, on your own word the same
  exchange ("сейчас не надо по новой").

- 2026-09-02 ~22:15 — after tonight's backlog closes, the Director's real route (a free message in
  → the right classification → exactly one task with its own DOD → a worker executing it → a DOD-
  and-check-gated close → a fresh session resuming without duplicating or guessing) gets proven end
  to end on the actual mechanism, on a temporary host copy — no new hook, board server, event log,
  second plan, registry or status invented to do it; only `PLAN.md`, `checkpoint.py`,
  `state-probe.sh`, product-prover, test-author and `TEST_MATRIX.md` as they stand. Your words in
  chat, kept whole in `PLAN.md` q-812 rather than paraphrased here (a compressed version of this
  exact brief is the drift the row itself exists to catch). Consequence: `PLAN.md` gains q-812,
  queued behind tonight's open rows, with product-prover reviewing the route's own contract and
  test-author adding exactly the matrix rows and tests the proof needs — no more.

## Open — carried, awaiting your word
<!-- record:open -->
These are open questions the pack carries with a recommendation. They moved here from the old spec
body when the format sent decision history out of the spec. They are decisions the pack made for
itself, so they name no exchange and carry no date. Each waits for your word, and the pack runs on the
stated recommendation until then. The spec points to each by its code. The pointer is a gap line under
the requirement the question touches, in the shape given above.

Before this list reaches you again, every item is re-tested against the tree as it stands. An item an
artifact now answers is closed with that citation, and an item with a trigger of its own names that
trigger. Swept 2026-07-28: all three still stand open, and work is blocked by none of them.

The attic is a host's append-only archive folder, `attic/`. A file superseded during an adoption run
moves there with one manifest line and is kept for good (INV-7). The adoption attic's layout is open: a
flat folder with a manifest and a source-directory prefix on a name collision, against dated
subfolders. `adopt/ADOPT.md` states the folder and its manifest. The pack runs on the
flat-with-manifest form and revisits at the next real adoption run. [D-1]

A pair is the two repositories a founding creates when it takes the engine-and-instance split. The
engine is the generic reusable mechanism, shipped as its own host and tested on its own generic
fixtures. The instance is the concrete product a real person uses today, holding the content and
plugging into the engine. Each half is a full host with its own spec, queue, journal, and `.live-spec/`
folder (Requirement 187 in `PRODUCT_SPEC.md`).

The pair's queues are open: one reading view stitched across the pair's two queues, or strictly two.
The queues stay per-repo either way. The recommendation is two plain queues with no stitched view. It
holds until real friction earns one, which means flipping between two windows to follow one wish's two
halves. [D-6]

The pair instance's spec citation is open: whether the instance's spec may cite engine facts, or only
the content contract. The content contract is the engine's public list naming every place a concrete
instance plugs in, each entry carrying a handle and a test. The recommendation is that the instance
cites the engine's contract entries by their handle and nothing deeper. The reason: a contract entry is
the engine's versioned public promise, while an internal fact rots at the engine's next refactor. [D-7]

### Stage 3 C2 — six checks await your word

Source for all six: `.live-spec/stage3-verdicts-2026-08-12.md`, step C2's closing list ("List 2 — what
waits for Alexander's word"). Each line below is dated 2026-08-12, copied in the source page's own
wording, and stands until you rule on it — the seat has ruled on none of these.

**The class line, covering fifteen keeps.**

> Checks that guard silent rot stay in the chain for now: c, d, e, f, k, o, q, u, v, w, x, y, z, ad
> and ae are kept on the seat's extension of your word of 2026-08-09 11:22 about the
> architecture-pointer check, none of them has other coverage of its failure class, and the
> extension is the seat's own until you rule on it.

**Gate ae — `check-named-checks.py`.**

> Gate ae spends 20,157 bytes and 0.16 seconds proving that `scripts/check-registry.json`
> describes each runnable file correctly, has caught nothing since 2026-08-06, and has no other
> reader of the registry; the seat recommends retiring it and keeping the registry as a plain
> document, and runs it until your word.

**Gate n — `check-earned-message.py`.**

> Gate n spends 16,759 bytes running report-only at push, has caught no unearned message and has
> reded four lawful deposits between 2026-07-28 and 2026-08-07 (queue row 585); the seat
> recommends retiring it and leaving the intake sweep as the judging moment, and holds its repair
> until your word.

**Gate p — `check-touchpoint-kind.py`.**

> Gate p spends 7,980 bytes proving that each surface speaks only the message kind its touchpoint
> affords, with no catch on record and no other coverage; you are the person a wrong-kind message
> reaches, so the seat asks whether the machine still earns its place and keeps it running until
> your word.

**Gate o — `check-cleanup-notice.sh`.**

> Gate o requires a cleanup to print what it ended, and its own header says it shipped ahead of
> the stricter owned-identity check that is now gate j; with no catch on record for either, the
> seat asks whether the notice requirement is still wanted beside j and keeps o running until your
> word.

**Gate ab — `check-handover-provenance.py`, already retired.**

> The handover-provenance gate was retired on 2026-08-09 with no other machine covering its class
> (queue row 522: the discipline is now the seat's alone); under the removal rule the campaign
> adopted afterwards that missing coverage would have brought the question to you first, so the
> seat asks you to confirm the retirement stands.

## Struck — recorded as yours, then you struck it
<!-- record:struck -->
- ~~Parallel lanes rank above the communication layer, and they wait for a field run.~~ STRUCK
  2026-07-17: a session recorded this in your voice as your ranking. Read back at ~15:37, you
  recognised nothing, and no message of yours on any day said it. This is the incident that produced
  roadmap row 415, now in `docs/queue-archive/rotated-ROADMAP-2026-07.md`: a session's own judgment
  moved into the one slot nothing questions.

## Notes
<!-- record:note -->
Nothing here is ever dropped. A struck line stays with its note so the record of what was corrected
outlives the correction.

- **The plan-v3 sitting, second pass.** Alexander 2026-08-11, in chat between 11:12 and 14:49,
  answering the follow-up on the open D-items. D3: keep («Оставить»), given after the three
  questions — what defines a failure class, class or the same failure, why twice — were answered
  in chat; the plan's sitting block updated in place (delta page
  `.live-spec/plan-v3-delta-2026-08-11-2.md`). D2: he confirms the current rule is wrong and asks
  whether rule 23 becomes the only birth channel for checks and what limits that carries —
  explanation owed, execution still waits his «понял, делай». D5: he asks whether per-change
  verification alone suffices, questioning the evening measure — answer owed, his word pending.
  D9: he asks what the item is about — a plainer explanation owed.

- **The plan-v3 sitting, third pass.** Alexander 2026-08-11 ~14:55 in chat: D5 yes —
  verification runs after each real change, no scheduled runs, the two-hour session alarm
  removed. Standing order: the plan itself always carries execution statuses (done / in work /
  waiting), updated as point edits with delta pages. Rule-23 broadening (absorbing cut rule 30's
  legitimate function: any twice-recorded dated defect counts, document drift included) recorded
  as a campaign-close post-action in the plan; his word «figure it out и сделай чтобы не
  потерялось». D9 and R7 explanations owed in chat; D2 execution still waits his «делай».

- **D2 executed.** 2026-08-12, 02:30-03:17, root his «делай» 2026-08-11 21:22. Rule 30 — the
  generator rule, every machine-checkable property becomes a pre-push gate — cut whole from the
  rulebook at commit `3866a6c`; its number stays a hole; a check is now born from a second dated
  break of a standing rule (rule 23) or his word. Rulebook body 66,435 → 65,496 bytes. Suite
  2484 passed / 0 failed; the freeze baseline re-run came out byte-identical; installed skill
  copies synced the same night. Acceptance caught the executing worker stopping mid-run with a
  report naming invented facts — an invented rule text, code and byte counts (queue row 589);
  the worker then finished the cut and its final report matched the tree line for line. The
  slice was accepted on the diff, the suite and the gates. The cut owes a MIGRATION.md chapter
  at the next release: a host that adopted 2.0.0 still carries rule 30.

- **Gate b stays; step C3's one permitted removal is declined.** 2026-08-12, stage 3 step C2/C3
  (`.live-spec/stage3-verdicts-2026-08-12.md`). Gate b (`check-tests.sh`) is the only one of the
  25 checks whose evidence meets step C3's removal test in full: its neighbour,
  `.github/workflows/gates.yml`, re-runs the identical suite (SPEC M-5) and is the mechanism that
  caught the 2026-07-14 miss when the local runner's collection was wrong. The page's own verdict
  on b is repair, not removal — cutting it would move every regression's first catch from the
  pre-push moment to CI, after the push, for a gain of 451.45 seconds, while the repair recorded
  on the same page (run the 282-second nested meta-test in the CI mirror alone, drop it from
  pre-push) takes most of that time without opening the gap. The seat accepts that recommendation:
  gate b is not removed.

- **The worker-restore gate's counting start moves to 2026-08-13, carrying one finding as
  history.** 2026-08-12, the push pass's own suite red on
  `tests/test_worker_restore.py::TestTheGateIsArmedWhereItSaysItIs::test_the_gate_runs_against_this_machines_own_transcripts`.
  `guardrails/check-worker-restore.py`, run both at its default window and at
  `--counting-from 2026-08-01 --all`, found exactly one finding inside this window: session
  `af22b716-c9d7-48b2-b3fd-2be1820a1a14`, working in `/Users/sashaabramovich/tlvphotos`, ran
  `git checkout -- lab/data/step3-grid-derivation.json` at 2026-08-12T06:05:40Z. Reading
  `/Users/sashaabramovich/tlvphotos` (read-only): the file exists today, is tracked, and
  `git log --oneline -3` on it shows its last commit at 2026-08-11T23:41:50+03:00, before the
  discard — so the checkout did not destroy a never-committed file; it dropped uncommitted edits
  laid on top of a version already in the repository's history. What those edits contained, and
  whether they survive anywhere else, stays unknown from this side; the file today again shows
  local modifications, meaning further edits happened after the discard, and what those edits
  hold is for that project's own session to establish. The counting start
  (`COUNTING_FROM` in `guardrails/check-worker-restore.py`) moves from 2026-07-28 to 2026-08-13, the
  first date after this finding's timestamp the gate's date-only granularity can express, so the
  finding is carried as history rather than left to red every future run — a red that can never
  clear blocks every pass behind it, and the finding is recorded here, in the gate's own header,
  and at `ROADMAP.md` row 598 before the start moves past it. A message describing the incident and
  what to check went to `/Users/sashaabramovich/tlvphotos/inbox/2026-08-12-worker-discarded-uncommitted-work.md`;
  no other file in that tree was touched.

  **Correction, 2026-08-12.** The paragraph above is what this side could establish from its own
  transcripts, and one of its statements is wrong. tlvphotos answered the notice the same day
  (`inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md`, 2026-08-12): the harness classifier
  DECLINED that `git checkout --`, so the command never ran and dropped nothing. What sat
  uncommitted on the file was a single regenerated timestamp line, written minutes earlier by the
  project's own `lab/step3-grid-derive.py` during a verification step, and it survived the attempt
  and is now committed. Read "ran `git checkout -- lab/data/step3-grid-derivation.json`" above as
  "handed a shell `git checkout -- lab/data/step3-grid-derivation.json`", and read the sentence about
  dropped edits as describing what the command would have done. The finding itself stands: the rule
  forbids handing such a command to a shell, and this worker's brief carried the rule in words. The
  gate's blind spot was real too — it reported a command handed to a shell while the shell's own
  answer sat in the same transcript — and it is closed the same day: `check-worker-restore.py` now
  reads each call's `tool_result` and every finding says whether the command ran, was declined, or
  went unanswered, with the executed ones printed first. The counting start stays at
  `2026-08-12T06:06:00Z`. It was re-tested at the earlier `2026-07-28` with the outcome visible, and
  two findings red there — the declined tlvphotos attempt, and one that really ran, session
  `176e927f-4e67-4fa6-887e-86d1d6e5d1e4` at 2026-07-28T21:12:39Z with `git checkout --
  guardrails/rule-census.json` in this repository — so moving the start back would turn two finished
  incidents into a red no future run can clear.

- **The worker-restore gate's counting start moves to 2026-08-18T21:48:00Z, carrying
  twenty-eight findings as history, not twelve.** 2026-08-19, while reading
  `guardrails/check-worker-restore.py`'s history past its 2026-08-12T06:06:00Z start.
  `guardrails/check-worker-restore.py --all --counting-from 2026-08-12T06:06:00Z` found
  twenty-eight findings this project's own sessions ran since the old start, every one of them
  stamped before the latest of them (2026-08-18T21:47:11Z) — so any move that carries the
  twelve findings named below past the start necessarily carries the other sixteen too: there is
  no date between the earliest and the latest that separates one group from the other. The record
  below names all twenty-eight rather than the twelve first found, because a silent carry of the
  rest would repeat, at sixteen times the size, the exact gap row 605 already named once.

  **The twelve, 2026-08-18, four of this repository's own lane worktrees** — `live-spec-dt/wt`
  (one `git checkout HEAD -- guardrails/doc-bounds.json` at 19:11:13Z, RAN); `live-spec-split/wt`
  (eight — three `git checkout -- docs/PROGRESS.md`, three bare `git stash -q`, and one
  `git stash push -q -m "1v-fix"` against the whole tree, between 06:35:15Z and 07:31:30Z, plus one
  `git stash push -q tests/test_spec_parts.py` at 07:44:14Z); `live-spec-morning/wt` (two
  `git stash -q` at 05:53:22Z and 05:55:57Z); `live-spec-cull2/wt` (one `git checkout --
  docs/MEASUREMENTS.md` at 21:47:11Z, DECLINED by the harness — the rule reds on the handing to a
  shell alone, ROADMAP row 479). Every one is the same shape row 479 already forbids: a worker hid
  a file's or the tree's uncommitted state with a git command to compare a before-and-after, then
  restored it with the same class of command, rather than reading and holding the bytes itself.

  The heaviest of the twelve: the `live-spec-split/wt` finding at 07:44:14Z ran `git stash push -q
  tests/test_spec_parts.py` inside an agent whose own brief forbade it from changing files at all.
  One minute later, at 2026-08-18T10:45:09+03:00 (commit `56f179a9`, verified by reading
  `/private/tmp/live-spec-split/wt`'s own `git log` — 82 lines touching that same file), a second
  agent in that same worktree committed real, hand-written work to that identical file. A
  badly-timed pop would have overwritten or interleaved with that commit; this time the timing
  happened to clear, which is luck, not the rule holding.

  **The other sixteen, never before recorded anywhere, by day and worktree:**
  - 2026-08-13 — six: `/Users/sashaabramovich/live-spec` itself (one, 11:45:18Z);
    `live-spec-night/wt-packet-b` (one, 19:00:31Z); `live-spec-night-integration/wt-ck2` (one,
    20:10:03Z); `live-spec-night-integration/wt-integration` (three, 21:02:38Z-21:04:38Z).
  - 2026-08-15 — one, named separately below.
  - 2026-08-17 — five: `live-spec-slimdown/wt` (two, 15:33:26Z and 15:54:36Z);
    `live-spec-integrate-slimdown/wt` (one, 17:41:57Z); `live-spec-night18/wt-d` (one, 19:36:52Z);
    `live-spec-night18/wt-a2-comm` (one, 23:11:01Z).
  - 2026-08-18, in worktrees the first pass never named — four: `live-spec-progressfix/wt` (two,
    05:50:04Z and 05:52:22Z); `live-spec-readme2/wt` (two, 06:00:17Z and 06:01:30Z).

  **The 2026-08-15 finding stands apart from the other twenty-seven and is named on its own.**
  Session `b9af9566-98e6-41e5-b6be-dba10e984606` handed a shell `git clean -qfd` at
  2026-08-15T18:54:30Z with `ran in: UNKNOWN (a cd target the gate could not read statically)` —
  the one case `classify` cannot place at all, not even to a directory that turned out gone or
  foreign. This is the exact shape the fail-safe default exists for: an unplaceable effective
  directory reds, unconditionally, because a gate that stayed quiet over what it could not place
  would lose the catch it exists for (`is_own_session`'s own law, and `classify`'s). It reddened
  correctly. The counting-start move carries it into history along with the other twenty-seven all
  the same, and that is worth saying aloud rather than letting it vanish into a round number: the
  one finding this gate's own design was proudest of catching is carried past exactly like the
  ones it caught by dumb luck.

  **A second truth this same finding uncovered.** The habit did not surface today; it has stood
  since at least 2026-08-13, and this exact test —
  `tests/test_worker_restore.py::TestTheGateIsArmedWhereItSaysItIs::test_the_gate_runs_against_this_machines_own_transcripts`
  — has repeatedly reddened and been waved past rather than escalated: `docs/prover/2026-08-05-day-of-readability-repairs.md`
  finding 13 names it and calls it a red belonging to "a concurrent run", not the change under
  review; `docs/prover/2026-08-14-candidate-repair.md` lists it among seven reds called
  "environmental" and moves on; `docs/prover/2026-08-17-slimdown-pin-renumber.md` finds it red on a
  named worker's real commands and writes "stands: it is a true finding … and no edit in this range
  can clear it" — true on each occasion, and never once carried to an incident record or a
  counting-start review before this one. That practice — naming a real red, filing it under a word
  that excuses the range at hand, and moving on without ever tracing it to its source — is what let
  twenty-seven of these twenty-eight sit unrecorded for up to six days. It stops here: this record
  does not call the twenty-eight "environmental" or "pre-existing" and leave it there; it names
  every one, and the fix under way (below) targets the habit rather than the next range's
  convenience.

  Row 605 already named the smaller-scale version of this same failure: a `ran` discard carried
  past the counting start on a source comment alone, `guardrails/check-worker-restore.py:197`, is
  thinner than the gate's own law asks — the start moves forward only with a recorded reason. This
  time the reason is recorded in both homes the gate names, in full, before the start moves past
  any of the twenty-eight: here, and at `ROADMAP.md` row 624. The counting start (`COUNTING_FROM`
  in `guardrails/check-worker-restore.py`) moves from `2026-08-12T06:06:00Z` to
  `2026-08-18T21:48:00Z`, one minute past the latest of the twenty-eight (the declined
  `live-spec-cull2/wt` attempt at 21:47:11Z) and no further than that — narrower is impossible, since
  every one of the sixteen sits before that same latest timestamp.

  This record closes nothing. The habit that produced all twenty-eight — hiding a file with a git
  command to prove a before-and-after, instead of reading and holding its bytes — is unrepaired by
  this move alone: nothing today stops a worker from handing a shell one of the five forbidden
  forms in the first place, only this gate's after-the-fact transcript read. A hook that refuses
  the five forms at the moment a worker hands them to a shell is built as a separate package, but it
  is not yet standing on this machine — installing it is the owner's own act. ROADMAP row 624
  records the event and stays open on exactly that: the row closes when the hook is installed and
  armed here, not when it merely exists elsewhere.
