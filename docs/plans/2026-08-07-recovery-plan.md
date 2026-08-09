# Diagnosis and recovery plan — live-spec, 2026-08-07

This page answers Alexander's request of 2026-08-07, 14:23: study the chat
transcripts, the pending-work queue, and how the project runs; return a
diagnosis and a firm plan — or say the task is impossible ("или скажешь что это
невозможно сделать", his words in that message). The plan must survive context
resets, keep its approved wording in every report, and pick AI models by real
prices.

Written by the audit seat (the session holding judgment) after reading the
repository whole and fourteen summary files that distill every session touching
this project from 2026-07-16 to 2026-08-07. A separate reviewer with clean
context then attacked this page; its findings are folded in, and its report is
filed beside the project's other review records.

## Part 1 — Diagnosis

### 1.1 The evidence base

Three weeks of session records (his own messages, pulled by the project's
reading tool), the pending-work queue and its archives, the daily work log, the
tracked-problems list, the list of automatic checks, the cost page of
2026-08-07, and the decisions record. Every claim carries its date. Every count
names the command that produced it, and the quotes sit in the fourteen summary
files where they can be re-read.

### 1.2 Five findings

**Finding 1 — every failure gets answered with a new check, and no check is
ever removed.** The project runs 31 automatic checks that block publishing
(counted by the command printed in the checks folder's own guide), keeps 103
check files, and 2,502 tests (the test run's own tail line, 2026-08-07 15:20).
The product specification is 704,463 bytes today against 590,695 at its format
change on 2026-07-23 — 19% growth in two weeks (both figures from the progress
page's published table). Every session loads about 45,000 tokens of shared
rules before any work (the cost page's measurement of 2026-08-07).

Each piece answered a real failure under an existing rule: the class-sweep rule
spreads every fix across the whole tree, and the gate rule wires every
machine-checkable quality as a blocking check. Together they explain the
slowness, the cost, and the pile-up he keeps naming. The chat clock is the
worked example: one drifting habit collected four layers of machinery and a
1,500-word ledger entry recording 22 catches. Nothing retires a check, a hook
(a small automatic script), or a rule when its failure class goes quiet. He
asked for the counterweight on 2026-07-27 — counting how often each hook is
used and periodically archiving the fading ones (his ten-item list of that
morning; the summary file preserves the list's meaning rather than each item's
exact words). The request went into the queue and the queue never reached it.

**Finding 2 — the queue admits far more than the project finishes, and each
item accumulates history inside itself.** Today the queue holds 209 open items
against 257 closed over the project's whole life; 159 sit marked "queued"
(counted by one grep over the queue file, 2026-08-07 16:05, five items higher
than at 14:30 because today's message sweep added five). One item — the work
board — took nine scope additions in a single evening (the work log,
2026-08-06) and carries seven dated paragraphs of that history inside its own
queue cell, against the queue's own rule that history lives in the archive.
The lowest tier for far-off ideas holds 4 items. Nothing limits admission to
the queue; only simultaneous work is capped.

**Finding 3 — the days that go off track are lawful step by step, and the
drift lives at the level of the day's priorities, which no artifact holds.**
His account of 2026-08-06 at 14:23 today: adoption was to be the emphasis, and
the day slid into bugs and then into bugs derived from bugs. The work log
shows each afternoon block following a recorded debt list in its stated order
— every step locally lawful. What no artifact held was the priority he had
voiced: the debt list itself, accumulated by bugs cutting ahead on earlier
days, legally consumed the day. The sharpest single case is that same evening:
"мы чисто пилили спеку доски, внезапно начинается какая то работа я вообще не
понимаю о чем речь и зачем. и этого шага не было ни в планах ни в программе ни
он не был обоснован" (2026-08-07, 00:17). A failing test jumps the queue by
rule; the class-sweep fans it out by rule; a red check blocks publishing until
every consequence lands. No rule weighs any of it against the day's declared
order, so the order loses every time.

**Finding 4 — he has dictated the discipline against drift at least seven
times, and prose alone did not hold it.** 07-19: "тебе надо все время
напоминать (как сейчас). это надо улучшить." 07-27: "Каждый раз когда
непонятная фигня пишется и я переспрашиваю то находить откуда она пршла в
спеках и там фиксить." 07-28: "С этого момента все что я не понял -
переформулируется." 07-29: "once a plan and it's KPIs and measurements are set
... we do not alter it and we stick to the format and we report by it," and
the measurement rule: "измерение это не просто слово, это объяснение зачем
измеряем, на что это повлияет, в чем измеряем, каким способом измеряем."
07-30: "больше не будет такого 'работай ночь ты сам знаешь как лучше'" and
"зафиксируй эту доску как четкий todo list. с этого момента она меняется
только если мы оба об этом договорились." 08-06: "ты делаешь план, мы его
одобряем и ты не перефразируешь это никогда."

Each became a written rule or a queue item, and the failures recurred anyway.
Two reasons. The rules live as sentences in files a session reads once, and a
session provably cannot hold them all once its context grows — "а то ты через
2 промпта в сессии начинаешь уже фигню полную писать и надо переспрашивать"
(07-28). And every new rule adds to the very load that makes holding rules
fail, so the cure feeds the disease. The project's own law says it plainly:
attention alone holds nothing across sessions. This plan applies that law to
itself — no step below rests on a session remembering a sentence.

**Finding 5 — most of the waste was repeated work, from efforts launched
without a fixed definition of done.** The readability effort ran three times:
the Fable week of 07-22, redone from 07-27 ("как это мы с фейблом всю прошлую
неделю все верстали и теперь опять переиначиваем?"), then the slim-down weeks
ending 08-04 with "ничего мы не добились." Single texts took up to 18 rewrite
passes — and whether that came from context growth or from bad source text was
his open question ("это потому что контекст рос или там хуже было написано?",
07-22), never answered with a measurement. Two verdicts stand on record: "ты
просрал простите 2 недели работы просто так кидаясь цифрами" (07-29) and the
plan cut to $20 a month (08-04). The project's own convergence law requires a
checkable definition of done before a process starts; it was never applied at
the scale of a multi-session effort, so these efforts had no finish test and
ran until frustration stopped them. Second-order waste was found and fixed on
2026-08-07 — the test suite silently running itself twice, meaningless
failures after midnight, a leaked folder per run (the night's work) — and the
cheap remaining piece, scoping test runs during work to the changed code, sits
queued (row 575).

### 1.3 What is already fixed, and stays

The night and morning of 2026-08-07 landed repairs this plan builds on rather
than repeats: the grounding law — every work block names the request behind it
— now rides every prompt (Requirement 310); the invented-number rulings — a
census found 144 numeric standards, his word at ~01:10 struck the made-up
caps, and the one standard for text is no redundancy; the measured-number
discipline — a published number names what it counts, the decision it informs,
the command, and its direction; and the four workshop repairs above. The work
board (row 166) is mid-build: its page form is frozen by his eye (the sixth
sample, 2026-08-06 20:57), its scope by his nine additions, and its
specification's fresh adversarial review is the next step of its own phase.
The board is the standing answer to "what is happening" and this plan feeds it
rather than competes with it.

## Part 2 — The plan

Six steps in order. Each names its root in his words, its mechanical carrier —
the thing that holds it when nobody remembers — its acceptance, and the model
tier that runs it.

Two rules govern the plan itself. First, no step rests on prose alone.
Second, the machinery ledger is published: this plan adds three mechanisms
(the order-file check of Step 1, the retirement line of Step 3, the
three-budget-lines rule of Step 4) and removes or shrinks four costs (the
parked-item reminder line once Step 1's check proves out; full test runs
during working sessions, row 575; the per-session rulebook load, row 570; and
every check the retirement reviews strike). Whether the ledger nets downward
is not asserted — it is measured by the two numbers Step 3 publishes.

### Step 1 — One order, one home, with teeth against drift

Root: his 07-29 plan-freeze rule; his 08-06 rule to report in the plan's exact
wording; his 07-28 rule that the resume file carries one task; his 14:23 ask.

The active order lives in one file, `docs/plans/current-order.md`. It holds
the one item in hand plus at most two more, honoring both his one-task rule
and the existing cap of three parallel work streams (his word of 07-06). Each
item carries a frozen name and a done-condition in his approved wording, and
sessions may not rephrase either. Precedence is stated once: this file is the
plan's home; the resume file NEXT_STEPS becomes a pointer to it plus the
resume mechanics it already carries; the board, when it ships, renders this
file and adds no third voice.

The teeth: work found mid-session that is outside the order is recorded in
one line (a queue item or a ledger line) and is worked immediately only when
it blocks the current item's own finish. Recording is one sentence; anything
past that sentence is work and must justify itself against the current item.

Mechanical carrier: a check on the delivery report and the handover. Every
work block cites an order-item name, or carries the one-line record mark plus
the sentence naming what it blocked. A report fails when any block maps to
neither, and it also fails when the session did outside-order work while no
order item advanced — the pattern of 08-06/07 fails the check by shape, and
tagging everything "outside the order" stops being an exit. This extends the
accounting the grounding law already owns, and the parked-item reminder line
in the chat hook retires once this check is proven.

Acceptance: two consecutive working sessions whose reports he can read
against the order file, matching every block by name, with the order items
visibly advancing. Tier: the seat writes the rule; a Sonnet worker wires the
check.

### Step 2 — Sort the queue to a size he can read

Root: his 14:23 words "бэклог очень сильно раздулся... и там непонятно с чего
начинать"; the queue's own rule that history lives in the archive; his 07-23
ask for much stricter shrink limits on the queue.

The seat builds one sorting page. Every open item lands in one of three
groups: IN WORK — the existing cap of three, today the board (166), the
rulebook cut tail (570), and the numbers-table tail (576); NEXT — about ten
items, each named in one plain line; FAR — everything else, each with a
one-line trigger naming what brings it back. Items keep their numbers. The
history piled inside queue cells moves to the archive where the queue's own
rule says it lives — a one-time mechanical sweep. Items he strikes on the page
close to the archive for good.

Mechanical carrier: the queue's existing format check and size bound; the
in-work cap is the existing three-lane cap rendered visibly, and the board's
approved column design carries it forward. Nothing new runs per-push.

Acceptance: he reads the whole queue on one page in one sitting and says
where to start without asking anything. Tier: Sonnet workers sweep the
histories; the seat writes the sorting; his eye strikes and picks.

### Step 3 — Shrink the machinery, with the evidence in hand

Root: his 14:23 "все работает все хуже и все дороже"; his 07-27 ask to count
hook usage and archive the fading ones; his 00:17 complaint about the test
suite; the cost page's own verdicts.

Three moves. First, the firing census: a small script walks the existing
logs and git history and writes, for every automatic check and hook, when it
last caught anything and how often it has fired — restoring the counting half
of his 07-27 ask. The existing whole-read audit that already runs every ten
finished changes gains one section: it reads the census and lists retirement
candidates. Retirement itself is always his word, because a silent check may
be silent for two opposite reasons — its failure class died, or the check
deters the failure — and only a reader can tell which. No numeric threshold is
invented; the census shows measured records and he judges. Second, row 575
lands: test runs during working sessions scope to the changed code, while the
full set still runs at every landing and publication — nothing ships with
less proof. Third, the rulebook cut (row 570) continues at its proven pace,
one file per session with a fresh verifier each time, to shrink the 45,000
tokens every session pays.

Mechanical carrier: the census script rides the existing audit cadence and
the existing registry of what each check is; a check without a census entry
shows up by shape. The gate rule's own text gains the exchange rule: a
landing that adds a blocking check names the check or the measured cost it
removes.

Acceptance: two numbers, published in the progress page's existing table and
re-measured at every landing — the wall time of a publication's checks, and
the fixed rulebook tokens a session loads. Both fall or hold; the direction
is the acceptance. Tier: Sonnet builds the census; the seat writes the rule
text; his word retires checks.

### Step 4 — Models priced, and big efforts budgeted before they start

Root: his 14:23 pricing question; his own routing reads of 07-30 ("мне
кажется он [опус] для четких задач лучше, а для более креативных ты [фейбл]
лучше подходишь", and: on his hardest open-ended tasks Opus "куда то бежит,
потом приходит с кучей цифр... задача не сделана"); his 07-27 line that the
cheap-by-default ratio deserves a check; his 07-29 measurement rule.

The price answer first. Opus 4.6, 4.7, 4.8 and Opus 5 all carry the same
list price — $5 per million tokens in, $25 out — so an older Opus buys
nothing, and Opus 5 is the straight replacement. Sonnet 5 is $3/$15 (an
introductory $2/$10 through 08-31), Haiku 4.5 is $1/$5, and Fable is $10/$50,
twice Opus. Source: the API price list as cached 2026-06 in the reference
this session consulted; worth one live re-check at next use. On his
subscription the meter is the plan's usage limit, and these ratios are the
best available read of how fast each tier burns it — Fable spends it at twice
the Opus rate, Sonnet at 60% of it, Haiku at a fifth of Sonnet.

The routing table follows his own reads and the recorded setup: precise,
well-specified work — orchestration, judgment on defined questions, briefs,
acceptance — runs on Opus; the creative and hardest passes — adversarial
reviews, deep audits, open-ended design — go to Fable, as his 07-30 words and
the recorded bootstrap already assign them; multi-step mechanical work,
readers, and sweeps go to Sonnet; single mechanical steps go to Haiku. The
routing reminder already rides every prompt and the delegation check already
fails a session that keeps mechanical work on the seat; the table adds the
prices and lives in the profile beside them.

The new half: budgets for big efforts. Any effort expected to span more than
one session opens with three lines in its order item — the checkable
definition of done, the budget estimate in sessions or tokens, and the
measure it will report. Step 1's check covers this: a multi-session item
missing the three lines fails the report check. This is his 07-29 measurement
rule applied at the scale where the three weeks were lost.

Acceptance: the next multi-session effort shows its three lines before work
starts, and the per-session usage report names the tiers used. Tier: the
seat.

### Step 5 — Reports in the order's words, and numbers that mean something,
in chat too

Root: his 08-06 19:02 "я офигеваю мне кажется это видимость работы о КОТОРОЙ
МЫ НЕ ДОГОВАРИВАЛИСЬ!!!"; his 08-06 12:04 "there should be no just numbers,
always tell what it is about clearly"; his 09:16 order to root out invented
numbers.

Most of this landed on 08-07: the grounding accounting and the number
rulings. Report lines keyed to order items come from Step 1's check. What
remains is chat itself, and here the plan states the honest limit rather than
inventing a gate: chat is the one surface no machine reads before he does.
Two things hold it. The existing per-prompt reminder line — reworded once so
a spoken number must carry its meaning in the same sentence — and his own
re-ask rule of 07-27: every question he has to ask back is recorded as a
defect against the wording that caused it, traced to its source, and fixed
there (already queued as its own item, row 487). His re-asks are the
diagnostic, and each one becomes fuel for a fix rather than a score against a
target.

Acceptance: his read of the next landing reports; each re-ask visibly
produces a recorded wording fix. Tier: the seat.

### Step 6 — The board ships, then adoption takes the head of the queue

Root: his standing board wish (row 166, scope frozen by his nine additions of
08-06); his direction of 08-06 toward adoption as the emphasis.

The board renders Steps 1, 2 and 5 — the order, the sorted queue, the frozen
wording — as one live page. Its own phase already names its next step: the
fresh adversarial review of its specification, then the column re-map and the
build. It becomes the order file's top item the moment Steps 1 and 2 land,
because they produce exactly the data it renders. When the board is up and
two sessions have held the order discipline, the queue head turns to
adoption: the spoken founding walk for a new project shipped 08-06, the
adoption walk for existing projects has stood since July, and the next item
is a real outside project run end to end.

Acceptance: the board's own specification, once its review passes — checking
before work enters, wording held letter for letter, estimate against actual
per task. Tier: by the pipeline; judgment at the seat.

## Part 3 — What holds this plan across resets

Four carriers. Two exist today: the resume file, cut back to its one-task
charter plus a pointer at the order file; and the work log's dated entry per
landing. Two are built by the plan itself: the order file with its report
check (Step 1), and the board as its rendering (Step 6). A session that wakes
with nothing reads one small file and knows the plan, its frozen wording,
and what done means for each item. No step of this plan asks a session to
remember anything.

## Part 4 — The direct answer to "или скажешь что это невозможно"

The order can be restored, with one limit stated honestly. The record shows
session attention degrading as context grows, on every tier: the overnight
run of 08-07 drifted under Fable exactly as earlier runs drifted under Opus —
"потом вообще потерялось и ты сам уже не помнишь над чем работаешь" (his
morning read, 08-07 09:20), and his own measurements of the same failure —
"совсем поехали формулировки с 700К контекстом" (07-28), "ты опять контекст
460К замусорил" (08-05). No check repairs that mid-turn. What the checks do
is catch it at every boundary — the report check, the order file a fresh
session reads — and keep the working unit small: short sessions, frequent
wipes he already enforces, one item in hand. His 09:20 morning line also
names the missing piece this plan supplies: "в конце прошлой сессии был
список" — the list existed and nothing forced the night to keep reporting
against it. Step 1 is precisely that force.

So the promise is: drift caught at every boundary and made visible in his
words, the queue readable, the machinery measured and shrinking, models
priced by what they cost. The counts of open work, the rulebook load, and
the cost of a publication all fall under Steps 2 and 3, and each fall is
published in the progress table where he can check it against the tree.
