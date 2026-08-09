Provenance: this record reviewed the pre-fix draft of the recovery plan on 2026-08-07 with clean
context. Its blocking and major findings were folded into the landed page at
`docs/plans/2026-08-07-recovery-plan.md`. Two of its blocking findings — the "или это невозможно"
title (B2) and the "непонятно с чего начинать" clause (B3) — are false alarms: the digest files
this review read had truncated both quotes, and the owner's original 14:23 message carries both
clauses verbatim.

# Adversarial review — recovery-plan-clean.md

Reviewer: fresh seat, clean context, 2026-08-07.
Target: `/private/tmp/claude-501/-Users-sashaabramovich/aeabf65b-a3f2-46a6-b0a4-c35810e3624d/scratchpad/recovery-plan-clean.md`
Evidence checked: digests 01–14; `/Users/sashaabramovich/live-spec` at commit ba479b6 —
`ROADMAP.md`, `NEXT_STEPS.md`, `PRODUCT_SPEC.md`, `JOURNAL.md`, `DECISIONS.md`,
`.live-spec/PROBLEMS.md`, `guardrails/README.md`, `docs/audits/2026-08-07-cost-map.md`,
`docs/audits/2026-08-07-number-rulings.md`, `docs/plans/2026-08-07-night-plan.md`, plus
`git show` on `PRODUCT_SPEC.md` history.

Method: every Russian phrase in quotation marks was grepped against the fourteen digests; every
count was re-measured against the tree.

---

## BLOCKING

### B1. A quote in Finding 4 is not his, and carries the wrong date

> "07-27: «каждый переспрос — найти откуда пришло в спеках и там починить.»"

No digest holds this sentence. The real line is 2026-07-28 20:48 (`digests/digest-09.md:75`):
"каждый переспрос мой это тебе знак что ты что то упустил в процессе коммуникации." The
"find where it came from in the specs and fix it there" half is a digest-writer's paraphrase
from a different session — `digest-07.md:71` records "a `[REPEAT]` meta-check on whether
're-ask triggers a root-fix in the spec' is already a codified rule", which is the digest
author's wording, not his.

This is the finding whose entire point is that his exact words must be preserved, and it is the
root cited by Step 5. Words he never typed are set inside quotation marks and dated to a day he
did not say them.

### B2. Part 4 answers a question he never asked

> `## Part 4 — Answer to "или это невозможно"`

The phrase appears in no digest and is absent from the 14:23 root request
(`digest-14.md:122`, the full turn is quoted there verbatim). The nearest real line is
2026-07-27 19:08 (`digest-12.md:39`): "может это нерешаемая задача на данный момент. если так
то ок." A whole section is titled with a quotation he did not produce, in a plan built on
letter-for-letter reporting.

### B3. Step 2's root manufactures the problem Step 2 solves

> Root: his 14:23, "бэклог очень сильно раздулся... непонятно с чего начинать"

His actual sentence (`digest-14.md:122`): "бэклог очень сильно раздулся потому что идей много,
но все работает все хуже и все дороже и менее эффективнее при каждой новой идее." The words
"непонятно с чего начинать" appear nowhere in the digests. The ellipsis splices an invented
clause onto a real one, and that invented clause is the exact need Step 2 claims to answer
("he reads the whole queue on one page and can say where to start"). The step's justification
is circular against a quote he did not say.

### B4. Step 4's routing table inverts the quote it names as its root

> Root: ... his 07-30 read on model routing, "Opus для чётких задач"
> ... Fable for adversarial reviews, deep audits, and the hardest design, only on his word;
> Opus for the seat's work and every judgment task; Sonnet for multi-step mechanical work

His words (`digest-10.md`, session 56596060): at 23:56 — "мне кажется он для четких задач
лучше, а для более креативных ты лучше подходишь" (Opus 5 = well-defined, Fable = creative);
at 00:18 — "вообще мне кажется что опус5 он хорош для четких задач, а вот на всех моих таких
сложных он куда то бежит, потом приходит с кучей цифр (несколько раз проверял) и затык. задача
не сделана."

He put Opus on well-defined work and said explicitly that Opus fails on his hard ones. The
table gives Opus "every judgment task" and gates Fable behind his express permission — the
reverse — while citing him as the reason. The string "Opus для чётких задач" is also not his;
he never writes the model name in Latin.

### B5. The plan publishes unverifiable counts, several of which the tree contradicts

This is the failure his 14:23 message names first ("это типа 222 прохода, 444 бага, 111 файла
и это ни о чем не говорит и мне их никак не верифицировать"), and the repository already
carries a gate against it (`guardrails/pre-push` gate ad / SPEC INV-305: "every count this
repository publishes about its own tree matches the tree, and the reproduction command beside
it returns the published number"). Not one number in this plan carries a reproduction command.
Four are wrong:

| Plan says | Tree says | Source |
|---|---|---|
| "204 open items, called rows, against 257 closed" | 209 rows in the live table; 9 `*landed*` → **200 open** | `awk` over `ROADMAP.md` row lines |
| "154 sit marked 'queued'" | **158** `*queued*` | same |
| "the far tier, holds 4 rows" | **3** `*far*` | same |
| "2,491 tests" | **2,502 tests in 539 seconds** | `NEXT_STEPS.md` LIVE STATE, stamped 2026-08-07 15:02 — 53 minutes before this plan's file was written |
| "grew 19% in the two weeks after ... the compaction campaign ... finished" | 614,464 B on 2026-07-24 → 704,463 B now = **+14.6%** | `git show <rev>:PRODUCT_SPEC.md \| wc -c` at seven dates; no base date in the history yields 19% |

`JOURNAL.md:2138` records that a whole landing (row 555) was built on 2026-08-06 precisely
because four hand-typed counts on the front pages had gone stale, and that entry names
"a number a session types into chat" as one of four surfaces the new gate cannot reach. This
plan is written on exactly that unheld surface and repeats the failure the landing was built
to stop.

### B6. Finding 3's flagship example is contradicted by the project's own journal

> 2026-08-06 is the clearest case. The entry connecting live-spec to a new
> project (adoption) finished by midday. The afternoon went to failing tests
> across the full test set, small scripts out of sync between copies, and count
> repairs — none of it on the day's agreed plan.

`JOURNAL.md:2207` ("2026-08-06, 16:00–16:53 — the three landings reach main, measured and
pushed") says: "The continuation session walked the handover's debt list in its stated order.
The three finished landings were committed by name: the measured published counts (row 555),
the check registry ... (row 556), and the spoken setup entry (row 557)." The same entry lists
the five suite reds and the three drifted installed copies as items on that stated debt list.

So: the count repairs *were* the day's plan (row 555), the sync drift and the reds *were* on
the stated list, and the adoption entry landed at 16:00–16:53, not "by midday". The day the
plan reconstructs as proof of drift is described by the repo as a debt list walked in order.
The real unplanned slide he complains about is at 00:17 on 08-07 (`digest-14.md:50`), a
different session on a different day. The clearest case is the weakest one.

### B7. Step 1's gate passes a fully drifted session

> Every work block must cite a plan item's ID, or state it's outside the plan and
> name the queue row recorded; a shape check fails any report that doesn't map
> this way.
> Acceptance: two sessions in a row where he can read the report against the plan
> file and match every block to an item by name.

The escape hatch swallows the gate. A session that spends the whole day on unplanned bug
chasing satisfies the check by labelling every block "outside the plan" and quoting a row
number — a shape check cannot tell a planned block from a declared-unplanned one. Both the
carrier and the acceptance test are then met by a session that advanced zero plan items,
which is the failure mode of 2026-08-06/07 verbatim. The gate is anchored on the report's
shape, not on where the time went.

### B8. Step 3's carrier cannot produce its output, and its condition is an invented number

> A retirement rule: every gate, hook, and standing check gets one line stating its
> removal condition — typically, that the failure it guards against hasn't happened
> in N finished pieces of work. A periodic review, riding the existing ten-item
> audit with no new cycle, lists retirement candidates for his decision.

Three separate breaks.

1. **N is a from-the-ceiling number.** `DECISIONS.md`, ~01:10 on 2026-08-07: numeric caps are
   rejected; `docs/audits/2026-08-07-number-rulings.md` §5 "Rooted out" is removing that whole
   family today. Step 3 reopens it hours later, in a plan that opens by praising the ruling.
2. **The evidence is unobtainable in principle.** A blocking gate prevents its own failure from
   being observed. "The failure hasn't happened in N pieces of work" is caused by the gate; it
   is not evidence the gate is unneeded. The condition would retire the gates that work best.
3. **The carrier is the wrong machine.** The "existing ten-item audit" is the every-ten-*landings*
   full document whole-read (`PRODUCT_SPEC.md:3021`; `skills/live-spec-base/SKILL.md:459`;
   `TEST_MATRIX.md` M-287). It reads documents for drift. It counts no hook or gate usage, and
   Step 3 instruments nothing. His actual 07-27 ask was for **usage counting**; the step drops
   the counting and keeps the archival.

---

## MAJOR

### M1. The plan breaks its own second governing rule at three of six steps

> Two rules govern the plan: ... total machinery does not grow — every new check
> names an old check or cost it removes.

- Step 1 pays: it retires the deferral-marker reminder.
- Step 2 adds a sorting page and "a cap on IN WORK items"; names nothing removed.
- Step 3 adds a retirement rule *and* a check that fails a check with no retirement line; names
  nothing removed.
- Step 4 says it outright: "Both stay; this table adds prices."

Five new artifacts, one retirement. The document's own constraint fails on its own contents.

### M2. Part 3 calls two things that do not exist "none new"

> Four things enforce this plan, all mechanical, none new: the Step 1 plan file ...
> and the board, once it exists

The Step 1 plan file is created by Step 1. The board is row 166, unbuilt. Two of the four
enforcers are new by the document's own text.

### M3. Step 2's "at most three" already exists under another name

> IN WORK, at most three

`ROADMAP.md` line 5: "execution runs at most three independent landings at once — the lane
cap". `docs/audits/2026-08-07-number-rulings.md` §1 records it as his word, 2026-07-06. The
plan's own Finding 2 acknowledges it ("only active work in one priority group, a lane, is
capped") and Step 2 then re-introduces it as new machinery. Either it repeats landed work or it
is a second, unrelated three with no ground.

### M4. Step 1 builds a new plan file over the one he asked to be fixed

> The current plan lives in one file, `docs/plans/current-order.md`: at most three
> items ... NEXT_STEPS points here

`NEXT_STEPS.md` already opens: "A digest with no redundancy (SPEC INV-48) — one live-state
block ... One status block stands here at a time." It is already the single plan file. And his
instruction of 2026-07-28 08:13 (`digest-09.md:24`) was the opposite of a three-item file:
"Некст степс раздутый не нужен. Туда только одну задачу и правильную историю и указания чтобы
ничего не сломалось." The plan adds a document instead of repairing the one he named, and
widens one task to three while citing him.

### M5. Three artifacts each claim to be the plan

Step 1: "nothing else claims to be the plan." Step 2 then builds "one sorting page" holding
IN WORK / NEXT / FAR. Step 6 builds the board as "a live, standing view of Steps 1, 2, and 5:
the plan, the sorted queue, the fixed wording." Nothing says which one a session reads when
they disagree, or which one is edited first. This is the drift surface the plan exists to
close.

### M6. Step 6 rests on an approval that has not happened

> It is being built in the approved form
> Acceptance: the board meets its approved design

`NEXT_STEPS.md`, forward queue item 2: "Row 166 resumes: the fresh adversarial review of the
board's specification, the stage-ladder re-map, the task-graph criteria." The night plan's
close: "Row 166's board work is the fresh adversarial review of the board's specification."
The specification is queued *for* review, not approved. The acceptance test therefore points at
a document that does not yet exist, and cannot be checked.

### M7. Step 6 misnames what shipped on 08-06

> the steps for connecting a new project (the attach walk) shipped 08-06

The attach walk is `adopt/ADOPT.md`; `TEST_MATRIX.md` M-226 records its tests red-proven
2026-07-10 and 2026-07-11 (row 251). What shipped on 08-06 is the *founding/setup* entry,
row 557 — `JOURNAL.md:2207`: "the spoken setup entry (row 557)"; `JOURNAL.md:2175`: "Saying
'attach live-spec to this project' now reaches a walk ... `adopt/START.md` is the founding
walk." Two different deliverables, one month apart, merged into one claim the owner would
read as "adoption is newer than it is".

### M8. Finding 2 gives row 166 two incompatible sizes

> row 166 alone carries seven dated paragraphs

against, in the same finding, "one row grew by nine additions in a single evening", and in
1.3 and Step 6, "the nine additions he made on 08-06". `JOURNAL.md:2249` confirms the nine
("2026-08-06, 22:01 — the work board's inception: nine widenings"). Seven paragraphs cannot
hold nine same-evening additions. One of the two numbers is wrong and the reader cannot tell
which.

### M9. Finding 5 converts his open question into its own answer

> Individual texts took 18 rewrite passes.

`digest-04.md:35`, 2026-07-23 21:08: "я подметил что сначала ты за 6 прогонов кусок доделывал
а потом когда вырос контекст то за 18 к концу. **это потому что контекст рос или там хуже было
написано?**" He offered two causes and asked which. The plan files the number under "no fixed
definition of done" and drops the cause he named first — context growth — which is the same
cause Part 4 later calls irreducible. The evidence is used for one hypothesis while the
document elsewhere argues for the other.

### M10. Step 4 prices in API dollars for a man on a $20 subscription

> $5 per million tokens in, $25 out (API price list, cached 2026-06) ... On a
> subscription plan, the same ratios set how fast the usage limit burns.

He moved to the $20 plan on 08-05 (`digest-12.md:82`, announced 08-04: "завтра будет даунгрейд
на 20$ в месяц"). What he actually tracks in session is the limit clock —
"бюджет перезапустился" (09:07), "97% сессии" (11:13), "через 3 часа освободится бюджет
сессии" (10:52), all in `digest-14.md`. None of it appears in the table. The provenance is also
weak by the plan's own measured-numbers standard: "cached 2026-06" is a two-month-old figure
with no command and no live check, in the one step whose entire subject is price.

### M11. Step 5's carrier for chat numbers is the thing Finding 4 declares useless

> A number spoken in chat must carry its meaning in the same sentence ... enforced
> by an existing chat-process line, reworded once, no new script added.

Finding 4: "the rules exist only as sentences in the shared rules file loaded every session,
and a session cannot hold that many once it runs long enough." `JOURNAL.md:2196` names
"a number a session types into chat" as one of four surfaces that "stay unheld" by any gate.
Step 5 therefore carries its own most-repeated failure on a reworded sentence — and Part 2's
opening promise ("no step depends on anyone remembering a written sentence") is broken here.

### M12. Step 5's acceptance test is passed by silence and inverts his own rule

> Acceptance: he reads one finished-work report start to end without a follow-up question.

He may not reply at all; the test then reads as passed. And his 2026-07-28 rule
(`digest-09.md:75`) makes a re-ask a *diagnostic* — "каждый переспрос мой это тебе знак что ты
что то упустил" — not a score to hold down. Turning it into an acceptance bar creates a quiet
pressure to write reports that discourage questions.

### M13. Step 2 invents a thirty-minute target while the tree is deleting that class

> The seat builds one sorting page, for a thirty-minute read.

`docs/audits/2026-08-07-number-rulings.md` §6: the "scan-in-30-seconds targets" inside the
rulebook files are being replaced with the qualitative form under the rulebook cut. The plan
reintroduces the same construct in Step 2 while Step 3 promises to keep removing it.

### M14. Part 4's limit rests on one session per tier and ignores the plan's own remedy

> The 08-07 overnight run drifted off track under Fable the same way earlier runs
> drifted under Opus: "ты сам уже не помнишь над чем работаешь" (09:20). That is a
> property of the tool itself; no check fixes it mid-task.

His 09:20 line (`digest-14.md:80`) ends: "в конце прошлой сессии был список" — he is naming a
list that existed and was not carried, which is precisely what Step 1's plan file supplies.
The same evidence supports "no plan artifact survived the session boundary" at least as well as
"the tool degrades". The document concedes as permanent the thing it claims to fix, off one
observation per model, and does not weigh the alternative. The paragraph also closes on
"700,000 tokens of context" — an invented figure in a section about invented figures.

### M15. Finding 1 presents a digest paraphrase as a direct quote

> He asked for this on 2026-07-27: "хук usage counting + periodic archival of
> declining hooks."

`digest-06.md:109` introduces that list as "Other items in the same dump (**routine, not quoted
verbatim per-item**)". The digest states it is not his wording; the plan sets it in quotation
marks and dates it.

---

## MINOR

### N1. Five quotations compressed inside quotation marks

- "ты просрал 2 недели работы просто так кидаясь цифрами" — actual: "ты просрал **простите** 2
  недели..." (`digest-10.md:66`).
- "once a plan and its KPIs are set we do not alter it and we report by it" — actual: "...and
  we **stick to the format** and we report by it" (`digest-10.md:43`).
- "зачем, на что влияет, в чём, каким способом" — actual: "зачем **измеряем**, на что это
  **повлияет**, в чем **измеряем**, каким способом **измеряем**" (`digest-10.md:38`).
- "больше не будет 'работай ночь как знаешь'" — actual: "больше не будет **такого** 'работай
  ночь **ты сам знаешь как лучше**'" (`digest-10.md:85`).
- "как это мы всю прошлую неделю всё верстали и теперь опять переиначиваем?" — actual:
  "как это мы **с фейблом** всю прошлую неделю..." (`digest-12.md:39`).

Each is close in substance. In a plan whose Step 1 promises reporting "word for word", quotation
marks that are not word for word set the wrong precedent.

### N2. Two gate counts, unreconciled

"31 automatic checks that block shipping" is correct (`guardrails/README.md:12`; `JOURNAL.md`
2026-08-06: "the push chain runs 31 checks"). But `docs/audits/2026-08-07-cost-map.md`, cited
in the same evidence list, says the publication gate is "27 checks". The plan takes one and
never mentions the other.

### N3. "103 safety-check files" over-counts

103 is every file in `guardrails/`, including JSON data files and the README. Runnable checks:
69 (`.sh` + `.py`).

### N4. The chat-clock example is misfiled and part-unsourced

"a 1,500-word log entry recording 22 catches" — the 22 is right (`.live-spec/PROBLEMS.md:15`
ends "twenty-second total"), and the four layers are right (rows 103, 104, 127, 134). But it is
one cell in the problem ledger, not a log entry, and the 1,500 words have no source.

### N5. Step 3 narrows his 00:17 complaint

"his 00:17 complaint about the test suite" — at 00:17 he said the work is slow and the context
too big, not anything about the suite (`digest-14.md:50`; the cost map's own header:
"the work feels slow, find out which part is justified").

### N6. Bare clock times with no date

"his 00:17 complaint", "his 20:31 proposal", "his 09:16 order", "his 09:16 order about invented
numbers". 00:17 and 09:16 are 08-07; 20:31 is 07-30 (`digest-12.md:35`). The owner cannot
locate three of the four.

### N7. Internal terms with no gloss

Glossed: rows, gates, guardrails, lane, hook, adoption. Not glossed: "the seat" (used eleven
times, including as a work tier), "base rule 22", "INV-108", "the ten-item audit", "the
far tier", "tail" in "the rulebook-cut tail" and "the numbers-table tail".

### N8. Sentences that need a second read

- Step 1: "The class-sweep rule still applies. It now runs as a scheduled, logged task. It does
  not take over the session immediately." — the two "It"s read as the bounded-interruption rule
  just introduced; they mean the class sweep.
- Step 3: "shipping-check time and fixed rules load per session get measured before and after
  each cut" — four nouns stacked, no verb until the ninth word.
- Step 2: "the item list checks formatting and has a document-length limit" — "the item list"
  is doing the checking, which reads as the queue checking itself.
- Finding 1: "the gate rule sets when a new check gets added" — "sets when" needs "governs".

### N9. Scope stretch on the 07-30 board quote

"доска меняется только если мы оба договорились" is real (`digest-10.md:110`, 09:20, "с этого
момента она меняется только если мы оба об этом договорились") but it is about one temporary
board, `~/context-slimdown.md`. Finding 4 reads it as a general law against going off track.

---

## What survived the attack

- 31 push gates, 103 files under `guardrails/`, `PRODUCT_SPEC.md` at 704 KB, ~45,000 tokens of
  fixed rules per session — all four match the tree and the cost map.
- The chat-clock example's mechanism: four layers across rows 103, 104, 127, 134, and 22
  recorded catches, both verifiable in `.live-spec/PROBLEMS.md`.
- Section 1.3's account of the 08-07 night: Requirement 310 exists and is the grounding law
  (`PRODUCT_SPEC.md:7808`); the 144-number census, the ~01:10 caps ruling, and the tests now
  reading live records all match `docs/audits/2026-08-07-number-rulings.md`.
- Rows 571–574 landed the same night, 575 queued, 570 at two of eleven files — all match the
  cost map.
- Row 166's nine widenings on 2026-08-06 (`JOURNAL.md:2249`).
- Finding 4's quotes at 07-19, 07-28 ("переформулируется"), 07-30 (the board lock), and 08-06
  ("ты делаешь план...") are real, correctly dated, and correctly attributed.
- Finding 5's three readability attempts, the 07-27 redo complaint, "ничего мы не добились" on
  08-04, and the $20 downgrade are all attested with the right dates.
- Finding 1's central mechanism — nothing in the tree retires a gate, hook, or rule — is not
  contradicted by anything I found.
- Step 4's answer that Opus 4.6/4.7/4.8 buy nothing over Opus 5 addresses the question he
  actually asked at 14:23.
- INV-108's citation ("attention alone holds nothing across sessions") is consistent with the
  base rulebook's recorded position on gates versus attention.
