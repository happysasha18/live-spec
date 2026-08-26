# Recon — what Alexander actually said should stand on a board ticket, 2026-07-29 to 2026-08-12

Written 2026-08-26 for PLAN.md step 1's line: "What should stand on each ticket — the owner already
said it concretely, 2-4 weeks ago." Recon over the repo's dated records and the surviving session
transcripts. No field below is invented; every one is traced to a dated quote.

## Summary

All the concrete field-level words come from one evening, **2026-08-06** (queue row 166, "Live work
board"), recorded twice over — in `DECISIONS.md` (paraphrased, dated, line-numbered) and in
`docs/handovers/2026-08-06-evening-work-board-handover.md` (closer to verbatim, with a few quotes in
his own broken-English chat text). No other session in the 2026-07-29–2026-08-12 window, and no
session outside it up to 2026-08-13, adds a new field; the original transcript file
(`657b4b30-f086-4f8b-933c-b6d4a23208da.jsonl`) has since rotated out of `~/.claude/projects/`, so
`DECISIONS.md` and the handover are now the only surviving records of his exact words. The fields he
named, in his own words: a short referrable name that reads as a recognition "handle"; a description
of the behavior; a time estimate, later paired at close with the actual time taken; a tag naming the
feature or the modules the task crosses; a plan/deliverable list marking what can run in parallel;
which worker (by name/icon) holds the task, and its lane; the branch and worktree; a compact
emoticon-style done mark; no numbering beside a deliverable's state mark; no option/open-choice
bullets on an in-progress card; and a details fold holding step-level history, never a bare finding
count. `spec/work-board.md` clauses 30–40 cover nearly all of this closely, in several places almost
verbatim — the one clean miss is clause 35's "one pipeline stage of the nine," which traces to no
quote found and is flagged by the project's own second prover round (K8) as ambiguous against his
"plan" wording.

## 1. Every field/element Alexander specified, dated and sourced

Primary source for all quotes below: `DECISIONS.md` lines 115–194 (paraphrased dated entries, each
opening "Your words in chat"), cross-checked against
`docs/handovers/2026-08-06-evening-work-board-handover.md` §"Every word Alexander gave, with its
time" (closer to verbatim, some literal quotes in his own English). Row 166 opened as the evening's
subject at ~19:17.

- **~19:17** — every task carries "a name that is understandable, a description that is
  understandable, and a plan that is understandable"; once approved that wording freezes and is
  spoken letter for letter at take-up, along the way, and at the close; a validation step stands in
  front of the board and nothing enters work before it passes. — `DECISIONS.md:189-194`

- **19:28** — "for every task, add the time the seat estimated for it and the time it actually took.
  Both figures stand on the task's board row, at take-up as the estimate and at the close as the
  pair." — `DECISIONS.md:184-188`

- **~20:16**, looking at variant 3 (`prototype/work-board-mockup-2026-08-06.html`) — "each task
  carries a super-understandable short referrable name, a description that describes the behavior, a
  time estimation, a tag naming the feature it belongs to or that it crosses several modules, and an
  attached plan saying what can run in parallel if the budget permits; the whole reads as a kanban
  board showing progress and which worker is doing which task; recurring workers may get names and
  icons, personalities to be developed and shown for your eye." — `DECISIONS.md:177-183`. The
  handover's literal transcript quote for the same turn: "the page shows and maintains all the tasks,
  done, in progress and on the roadmap; each carries a short referrable name, a description of the
  behavior, an estimate, a tag naming its feature or its reach across modules, and a plan saying what
  can run in parallel" (`docs/handovers/...md:93-97`).

- **20:35** — card reading order, literal quote from the handover: "the short description should be
  super-sharp as it will be the associated semantic 'handle' the AHA moment when [h]uan says 'ah,
  this is what I think it is' every time the ticket is referred", then a description, "then all the
  other details" (`docs/handovers/...md:101-104`). `DECISIONS.md:172-176` paraphrases the same:
  "the short name is a super-sharp semantic handle ... then the description describing the behavior,
  then all the other details. And a task is a part of the product spec, and that part is featured on
  the board." Same turn, on approvals: "you do not like the idea of manual approval for everything; it
  should be rare" (`DECISIONS.md:169-171`) — policy context, not a card field, but it is the reason
  the spec's validation clauses read as agent-approved rather than person-routed.

- **20:36**, rejecting variant 4 (`prototype/work-board-mockup-2026-08-06-v4.html`) — literal quote:
  "there are also lanes for parallel agents, and also info per taks like what is the branch/worktree
  etc. frankly, I don't get what's on the kanban you showed me. these tiles do not look like tasks,
  it's a text I need to crack my mind to understand what it is." (`docs/handovers/...md:105-109`).
  Recorded as the "card law" in `DECISIONS.md:163-168`: "a card reads as a task at a glance —
  authored handle first, behavior line, chips — and technical details sit behind the card."

- **20:47**, approving variant 5/6 with four amendments (`docs/norms/work-board.provenance.md`
  confirms this approval froze the norm) — literal quote: "the board looks good now. the 'done' part
  should be with emoticons to save the place. basically, readability is the main thing. also, the
  same names will be referred in every communication (this window included). the 'more' part is
  auto-closing this is frustrating as I don't have the time to look at it. ok after some tears there
  is a reference about 17 findings and I don't see how it is related to the specific task and what
  these findings are. also I don't think that some bullets should be there when the card is already
  'in progress'. showing option[s] to me is way before the ticket is accepted. right?"
  (`docs/handovers/...md:112-116`), paraphrased at `DECISIONS.md:156-162`.

- **21:00** — "you want to see everything on the board — all the backlog tasks — readable; there is
  one source of truth, every task referred from the product spec and the architecture; the done tasks
  need hiding as they will become a pile; the in-card step statuses should be emoticons too; a
  comment on every step about what was done is good and must be utterly understandable as well"
  (`DECISIONS.md:144-149`). Two remarks the handover flags as recorded nowhere else: he was unsure
  where the frozen norm lives, and he may never open the board himself — "having the representation
  exist may be enough" (`docs/handovers/...md:155-158`, `DECISIONS.md:150-155`).

- **21:16** — "no need for both numbers and emoticons"; "a task never carries a hundred subtasks —
  like in every agile it splits into fewer deliverables, and the subtask list is never a log of
  everything (tonight's acceptance is a single bullet on the in-progress card)"; "no legend —
  everything self-explanatory"; questioned the blue vertical lines in the subtasks and the "variant 3"
  sample label; "whatever is in work is something [the seat] can take on its own without questions ...
  most tasks will be like that"; asked for a kanban-process skill to learn from
  (`DECISIONS.md:135-143`, literal phrasing in `docs/handovers/...md:123-129`).

- **21:34** — the stage ladder: "'in work' means the item is clear and in the pipeline"; before it
  sits the backlog of all kinds of ideas, then inception — where either everything becomes clear and
  the item moves to ready, or his input is needed — so one more stage stands between the backlog pile
  and ready; the board's own rules (the spec, twice reviewed) are inception's product, never an
  execution subtask; subtasks carrying info must be collapsible; a fresh wish arrives already
  connected to the feature/spec part it touches (`DECISIONS.md:127-134`, literal:
  `docs/handovers/...md:130-136`).

- **~21:35** — every new wish is placed into the maintained web of tasks and their relations at
  arrival, so the best path, its parallelism and its dependencies can be read off it
  (`DECISIONS.md:123-126`).

- **21:49** — "people have ideas 'in the flow' so it might be that the task which is already in the
  work can be updated multiple times"; a log per task, reachable on demand, recording what he asked
  for while the work ran, is agreed; he had not received the kanban-tools research
  (`DECISIONS.md:115-122`, literal: `docs/handovers/...md:137-142`).

- **2026-08-26 (today, outside the 2-4-week window but the item that triggered this recon)** —
  `PLAN.md:166-167`: the existing sketch `prototype/work-board-sketch.html` is "так себе" ("so-so"),
  and a "pseudo-kanban" view with columns is wanted. No new field named, only the form.

No transcript search beyond `DECISIONS.md`/the handover turned up anything new. A keyword search
(`board|kanban|ticket|card|column|доск|тикет|карточ`) over every user-role turn dated 2026-07-29
through 2026-08-13 across `~/.claude/projects/-Users-sashaabramovich-live-spec/` returned 19 hits;
all but one cluster on 2026-08-13 and are session-setup instructions or register-judge prompts for
an unrelated "LiveSpec vNext" architecture pass, not card-field words. The worktree project
directories named in the task brief (`-private-tmp-live-spec-night`, `-roadmap-wave`,
`-green-candidate`, `-night-integration`, `-vnext-clean`) do not exist on this machine — only
`-Users-sashaabramovich-live-spec` and a handful of unrelated projects are present under
`~/.claude/projects/`.

## 2. Does `spec/work-board.md` (Requirement 309, clauses 30-40) cover what he said?

Close, clause by clause. "Sourced" means a quote above maps to it; "not sourced" means the clause's
content was not found stated by him in this window — that does not mean it is wrong, only that this
recon found no quote for it.

| Clause | Content | Coverage |
|---|---|---|
| 30 | Echo-name first (3-5 words), then description, then chips; rest behind a details layer. | **Sourced** for the ordering and the details-layer split (20:16, 20:35, 20:36 card law). The specific "three to five plain words" count is **not sourced** to any quote found — it reads as a retunable `[default]` the spec-author set, not his stated number. |
| 31 | Expand counts/references into plain words; a bare number is a defect. | **Sourced**, close to verbatim — his 20:47 line about "17 findings" needing to say what they are and how they relate to the task is the direct origin. |
| 32 | Placement tag chip, from feature/footprint notes. | **Sourced** — 20:16 "a tag naming the feature it belongs to or that it crosses several modules." |
| 33 | Card names and links the part of the product spec the task changes. | **Sourced** — 20:35 "a task is a part of the product spec, and that part is featured on the board"; reinforced 21:00 "one source of truth, every task referred from the product spec and the architecture." |
| 34 | In-work row shows its plan/deliverables. | **Sourced** — 20:16's "plan," 21:16's "split into fewer deliverables." |
| 35 | Mark beside the plan naming "the one pipeline stage of the nine." | **Not sourced.** No quote found names a nine-station pipeline vocabulary for the card. This is exactly the ambiguity the project's own second prover round flags as finding K8: "plan" is used for two different step lists in adjacent criteria — the task's own free-form steps (his sense) versus the pipeline's fixed nine stations — and the prover's own reading of "the person's word" guesses the task's own steps are meant, leaving the nine-station mark unresolved (`docs/prover/2026-08-06-work-board.md`, K8). Worth resolving before building, not inventing further. |
| 36 | Fine-grained trail kept off the card, in the delivery report/journal. | **Sourced** — 21:16 "the subtask list is never a log of everything," 21:49's per-task on-demand log agreement. |
| 37 | Deliverable line led by its state mark alone, no numbering. | **Sourced** — 21:16 "no need for both numbers and emoticons"; confirmed by `docs/norms/work-board.provenance.md`'s note that variant 8 froze "one marker per line, no internal numbering on cards." |
| 38 | In-work card shows settled deliverables/progress, never phrased as an option or open choice. | **Sourced, near-verbatim** — 20:47: "option bullets have no place on a card already in progress — options are shown way before the ticket is accepted." This is the strongest direct match in the whole set. |
| 39 | A genuine mid-work fork marks the card blocked and puts the question to the person. | **Not sourced** to a card-field quote in this window. It derives from the standing waiting-board machinery (Requirement 237 / INV-206) rather than from anything he said about board tickets on 2026-08-06. Consistent with his other words, but not traceable to one of them. |
| 40 | In-work row names its branch and worktree in the details. | **Sourced, near-verbatim** — 20:36: "also info per task like what is the branch/worktree etc." |

Outside clauses 30-40: the worker-craft case (clauses 77-85, names/icons/tiers for running steps)
traces directly to his 20:16 words ("recurring workers may get names and icons"). The five-column
case (clauses 20-29) is the one place spec and his words genuinely strain against each other, and the
project already knows it: `docs/prover/2026-08-06-work-board.md`'s round-2 findings K1-K4 document
that the five rendered columns ("awaiting validation," "ready," "in work," "waiting on the person,"
"done") cannot all be read off the queue's four recorded status words, and that his 21:34 stage-ladder
correction (backlog -> inception -> ready -> in work -> done, with "waiting on the person" a state
*inside* inception rather than its own column) was never folded back into the columns case before the
evening ended. `PLAN.md`'s own §Блокеры entry — "which sketch is approved" undecided — is the visible
symptom of the same unresolved thread continuing to today.

## 3. What each existing prototype/mockup file actually renders

Factual only — columns and per-card fields, no aesthetic reading.

- **`prototype/work-board-sketch.html`** (Russian; the 2026-07-07 sketch `docs/norms/work-board.provenance.md`
  calls "variant 2," and the one `PLAN.md` calls "так себе" today). Five sections, not a kanban: "Сейчас
  строится" (building now), "Ждёт вашего слова" (waiting on your word), "Готово сегодня" (done today),
  "Дальше в очереди" (next in queue), "Последние шаги" (last steps). Card markup is plain (`class="card"`,
  `"card now"`, `"card wait"`) with a `"stage"`/`"stage done"` marker; no chip/tag elements, no
  worker/branch/estimate fields at all.

- **`prototype/work-board-mockup-2026-08-06.html`** (English, built 19:41, "variant 3" — the one he
  reviewed at 20:16). Five sections: "In hand now," "Waiting on your word," "Awaiting validation — not
  yet in work," "Finished today," "Last steps." Cards (`card gate wide`, `card now`, `card wait`, `card
  wide`) carry `tag docs` / `tag feature` / `tag method` chips and a bare `time` field — no handle/chips
  split, no branch/worktree, no worker name/icon, no lanes.

- **`prototype/work-board-mockup-2026-08-06-v4.html`** (built 20:19, rejected at 20:36 — "these tiles do
  not look like tasks"). First file with a true five-column kanban header row: "In work," "Waiting on
  Alexander," "Ready," "Awaiting validation," "Done." Cards still carry only `tag area`/`tag docs`/`tag
  feature`/`tag method` and `time` inside a `chips` wrapper — no `handle`/`behav` split, no worker chip,
  no lane markup. This is the exact gap his rejection quote names.

- **`prototype/work-board-mockup-2026-08-06-v5.html`** (built 20:40, approved 20:47 with four
  amendments). Same five columns as v4. Cards now carry `class="handle"` and `class="behav"` (the
  name-then-description split his 20:35 and 20:36 words asked for), a `chips` block with `chip
  feature`/`chip docs`/`chip bug`/`chip est`/`chip worker`/`chip place`/`chip you`, and `lane`/`lane
  free`/`lanelbl` markup for parallel agents. This is the first file that satisfies the 20:16/20:35/20:36
  words structurally.

- **`docs/norms/work-board.html`** (the frozen norm; provenance says it is variant 6, refreshed in place
  to variant 7 at ~21:00 and variant 8 at ~21:16, per `docs/norms/work-board.provenance.md`). Same five
  columns as v4/v5. A sampled live card (`class="card live"`) carries: `p.handle` (short name), `p.behav`
  (one-line description), a `chips` row (`chip place`, `chip feature`, `chip est` showing "closed so
  far: est 237 min, took 89 min", two `chip worker` entries with emoji + craft name), and a `details.more`
  fold holding a `Deliverables` list where each line leads with a state-mark emoji (🔄 etc.) followed by
  plain text and a `span.who` naming the worker and tier — matching clauses 30, 34, 37, 40 and the
  worker-craft case directly. This file is the closest artifact to what he actually asked for across the
  evening, though `PLAN.md`'s §Блокеры still records no owner sign-off naming it (rather than the sketch
  or another variant) as final.

## Note on scope

This is recon only. No file besides this one was created or modified, and the board itself was not
built or touched.
