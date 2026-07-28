# Brief — put the settled answer on the record

Written 2026-07-28 for one worker starting with an empty context. Every anchor is named below by path.

## Your job

The owner settled a question in conversation on the evening of 2026-07-28. No file wrote it down.

Three files still carry that question as open, and each still recommends the answer he passed over. A finding handed in from another project names the same defect and sits unanswered.

Your job has four parts. Write the answer into the decision record, and close the three open passages. Then answer the handed-in finding, and sweep the tree for the rest of the class.

## What he settled, and the words he used

Four decisions came out of 2026-07-28. Each one is stated below in plain English, with his own words under it as evidence.

Reproduce every quote character for character, including his spelling. Each quote rides inside a fenced block, so the census counter passes over it.

**Decision 1 — every live document is read.**

A document becomes clean once a reader has read it through the audit skill. The reading covers every live document in the tree.

His words at 19:55 local time:

```text
короче если аудита не было, то файл не "чистый", ultimately каждый файл читается именно через аудит. согласен? норм?
```

**Decision 2 — the queue is ordered by what enters a working context earliest.**

The front of the queue is the entry documents and the pack skills. The queue then runs on through the rest of the tree.

His words at 20:48 local time:

```text
давай без "потолка" это должно было отсечься! нет? про то что документы всегда same or better согласен, главное механизмы держать эту марку. порядок документов ты выводил раньше! мы сказали что начнем с тех которые первыми загрязняют твой же контекст. найди их сам. next steps? скиллы аудита (им все проверяем)? потом спеки? какие то вспомогательные файлы потом? понимаешь ход мысли? просто все подряд мы делали это плохо особенно когда походу загрязнается контекст. надо идти всегда из точки где контекст чист максимальной гигиеной.
```

**Decision 3 — a document leaves an edit the same or better.**

Mechanisms hold that mark, rather than a session's care. The same 20:48 quote carries this call, so the entry names that quote as its evidence.

**Decision 4 — a reading is owed at a minor version bump and after a large growth in size.**

The reader is an agent session. The pack asks a person for no reading.

His words at `15:09 UTC`:

```text
Надо тогда поставить чтение агентом (не человеком как ты ошибаешься и говоришь) когда дибо размер сильно вырос либо когда major version?
```

His words at `15:12 UTC`, after hearing that major versions are rare:

```text
Минорную ок.
```

## Part one — the decision record

The decision home is `DECISIONS.md` at the repository root.

Read its existing entries under the heading `## On record` before you write. Follow their shape exactly: the date, the time, the decision in plain words, and the exchange the decision came from.

Write one entry per decision above, four entries in all. Put each entry's fenced quote directly under the entry it belongs to.

Two gates read this file. Run both after your edit and repair whatever they report:

- `python3 guardrails/check-authority-anchor.py`, which refuses an entry naming no date;
- `python3 guardrails/check-touchpoint-kind.py DECISIONS.md`, which reads the file's declared kind.

Cyrillic is allowed in this file. `scripts/check-shipped-language.py` names `DECISIONS.md` in its excluded list at line 95, so his words stay in his own alphabet here.

Write the English sentences of each entry in English. His quote is the one Cyrillic thing you add.

## Part two — the three passages that still ask the question

Three files ask the reader-reach question as open, and each recommends the narrow answer. Replace each passage with the settled answer, and name 2026-07-28 as the date it was settled.

**`NEXT_STEPS.md`.**

The passage sits under the heading `## One decision waits for the owner` at line 56. Its two sentences run at lines 58 and 59, and open with the words "How wide the reader bar runs".

One more line in that file depends on the same question. Line 33 reads "Steps 1 to 3 stand today. Steps 4 and 5 wait for the owner's answer below." Repair that line too, because the answer arrived and no step waits on it now.

**`docs/plans/2026-07-28-two-goals-one-campaign.md`.** The closing section `## The question waiting for the owner` runs from line 121 to line 130. Replace the section with the settled answer.

That plan's section `## The order of documents`, at lines 77 to 88, already carries his ordering. Leave it exactly as it stands.

The plan today implies the queue stops after its six numbered groups. State in the plan that the queue runs to every live document, and put that sentence where a reader of the order section meets it.

**`docs/handovers/2026-07-28-readability-campaign-handover.md`.** The passage sits under `## What waits for the owner` at lines 80 and 81, and opens with the words "The reading question".

## The counts these three files disagree on

`NEXT_STEPS.md` and the plan both say 107 live documents. The handover says 109. `guardrails/rule-census.json` holds 109 entries today.

Report this as a finding and change no count in this pass. Write your new sentences so they name no count at all, and the disagreement then waits for its own repair.

## Part three — the handed-in finding

The file is `inbox/2026-07-28-from-tlvphotos-a-parked-question-stays-in-the-list-after-its-answer-arrives.md`. It reports that a parked question stays on a waiting board after its answer arrives, and that the person is the one who notices.

Read it whole. It names the class you are repairing here.

Answer it by this repository's own rule for a handed-in item, rather than by a reply you invent. The rule lives in `skills/feedback-intake/SKILL.md`. Read its routing table at lines 49 to 61, and its ledger section at lines 63 to 71. Read its receipt discipline at lines 73 to 85.

`inbox/README.md` states what the door does with a swept file, at lines 113 to 118. `FEEDBACK.md` at the repository root is the ledger, and its existing lines show the shape one ledger line takes.

Follow those two files. Where they leave the route open, say which route you chose and why.

Remove no inbox file and open no queue row on your own judgment. `ROADMAP.md` belongs to the session lead in this pass. Report the row it owes, with the words you would put in it, and let the lead write it.

## Part four — the sweep

The same class lives in other places. Any spot in this repository that parks a question for the owner is checked against what he has already said.

A question he already answered is closed with the answer and the date he answered it. A question he has not answered stays, and it names the human-only fact it waits on.

Start the sweep at these places and go wherever the search leads:

- `WAITING.md` at the repository root, the waiting board, held by `guardrails/check-board.py`;
- the section `## Open — carried, awaiting your word` in `DECISIONS.md`, at lines 45 to 64, holding three items marked `[D-1]`, `[D-6]`, and `[D-7]`;
- `docs/handovers/` and `docs/plans/`, for a section listing what waits for the owner.

Leave `ROADMAP.md` alone and report what you found in it.

## The mechanical net over parked items

`guardrails/check-deferral-marker.py` is the net. Read its docstring at lines 1 to 40 and its pattern list at lines 47 to 70.

The net fires when a parked item names no human-only fact. It reads `NEXT_STEPS.md` and `docs/decisions/*.md` by default, which is stated at line 37.

Answer two questions about it in your report:

- can this net catch a parked question the owner has already answered?
- what would it take to make it catch that case?

The handed-in finding argues the answer at its section "Why the existing net misses both". Read that section and say whether you agree with it.

Propose only. Build no new gate in this pass, and change no line of the net's code.

## What you must not touch

Two other workers are editing this tree right now. These files are theirs: `hooks/chat-law-hook.sh`, `tests/test_chat_law_hook.py`, `docs/language-reads/2026-07-28-read16-chat-law-hook.md`, `PRODUCT_SPEC.md`, `PRODUCT_SPEC.index.md`, `TEST_MATRIX.md`, `scripts/rule-census.py`, `guardrails/check-doc-findings-bound.py`, and everything under `tests/`.

Touch none of them. You still run `scripts/rule-census.py` as a command, and you never edit it.

Make every change as a targeted edit to the lines you mean to change. A whole-file rewrite in a shared tree destroys another worker's concurrent edit.

Commit nothing and push nothing. The session lead does that.

Re-seed `guardrails/rule-census.json` never. A re-seed is no way to make a check green.

## The writing standard your prose is held to

Every document this repository ships is measured. Keep each sentence at or under 25 words. Use plain product words. Keep an internal code out of the front of a sentence, where it names nothing to a reader. A sentence that names a thing by denying its neighbour is refused.

Two of your three target files carry no headroom at all. `NEXT_STEPS.md` is recorded at zero findings, and its longest sentence runs 24 words. The campaign plan is recorded at zero, and its longest sentence runs 25 words.

One over-cap sentence in either file reds gate aa on the next push. The gate is `guardrails/check-doc-findings-bound.py`.

`DECISIONS.md` and the handover file sit outside the recorded set, so no gate holds their counts. Hold your own prose in them to the same standard anyway, and report their counts before and after.

## The checks that close the work

Run each command from the repository root and record what it printed:

1. `python3 scripts/rule-census.py DECISIONS.md NEXT_STEPS.md docs/plans/2026-07-28-two-goals-one-campaign.md docs/handovers/2026-07-28-readability-campaign-handover.md FEEDBACK.md`
2. `python3 scripts/preshow-register-lint.py <file>` over each file you edited
3. `python3 guardrails/check-authority-anchor.py`
4. `python3 guardrails/check-touchpoint-kind.py DECISIONS.md`
5. `python3 guardrails/check-board.py`
6. `python3 guardrails/check-deferral-marker.py`
7. `python3 guardrails/check-doc-findings-bound.py`
8. `python3 scripts/check-shipped-language.py`
9. `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the counts out of that log

Write the suite log to your scratchpad directory. Read its last line for the counts. An exit status is no test result, so quote the log.

The counts standing before your edit are these: `DECISIONS.md` 13, `NEXT_STEPS.md` 0, the campaign plan 0, the handover 0.

## What done means

Report these seven things, each one checkable by a reader:

- the list of files you changed, one line each, with what changed in it;
- the four new entries in `DECISIONS.md`, quoted from the file as they now stand;
- the three replaced passages, each shown as the old text and the new text side by side;
- the route you gave the handed-in finding, with the line you wrote and the file it went into;
- every parked question the sweep found, and for each one whether you closed it and on what evidence;
- your two answers about `guardrails/check-deferral-marker.py`, and whether you agree with the handed-in finding;
- the census count for every file you edited, beside the count it held before.

Report the full-suite counts quoted from the suite log. Report the `ROADMAP.md` row the finding owes, in the words you would write it. Report anything you found and left alone.
