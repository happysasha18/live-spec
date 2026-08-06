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
- 2026-08-06 ~19:28 — the board's tasks carry time accounting (row 166). Your words in chat: for
  every task, add the time the seat estimated for it and the time it actually took. Both figures
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
