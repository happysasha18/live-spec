# From tlvphotos — the pack owes the client focus, and a long draft owes an early showing

**Root.** Alexander's words in the tlvphotos window, 2026-08-07 09:54: "это надо кстати сказать
лайвспеку, что надо научиться помогать «клиенту» сфокусироваться", and "я не понял почему ты так
долго полтора часа вчера катал черновик а потом выкатил что-то очень прототипичное зато дофига
токенов и времени потратил… попроси лайвспек сделать тебе аудит".

**Harvested 2026-08-07 into ROADMAP rows 582 and 583.** Finding 1 — the thread in hand and the
threads deliberately frozen — is row 582. Finding 2 and the audit asked for with it — the ceiling on
unshown work and the report that shows one thing — are row 583. The file carries the owner's own
words relayed by that window, so it was read as his wish rather than as an agent's message; the
earned-message gate reads the filename alone for that door, which is ROADMAP row 585.

Two findings, both observed in this project, both about the method rather than this codebase.

## Finding 1 — nothing in the pack keeps the number of open threads down

tlvphotos carries five prototype pages at once: the walk, the flight, the darkroom, the arrival
chooser, and the operations page. On 2026-08-06 a session spent its evening on the darkroom and on
a new page, while the two threads the client actually cares about — the operations page he calls
the best thing in the project, and the walk that should carry it — moved not at all. His reading:
"после лаба мы ушли куда-то и не вернулись… чего-то там твикали даркрум, а по факту ни того ни
другого не можем выкатить."

The pack has a queue and a resume anchor. Neither of them asks the question the client asked:
which one thing is being finished, and what is being left alone until it is. A queue that holds
eleven open rows reads to the client as a project that ships nothing.

**What is worth considering.** A rule that names the thread in hand and the threads deliberately
frozen, written where the client reads it, and a check that refuses a new page while two are open
and unshipped. The narration law already makes a session say what it is doing; it does not make a
session say what it is declining to do.

## Finding 2 — a long draft with no early showing is the expensive failure

The 2026-08-06 night block produced 1,556 new lines across four hours and shipped a page the client
read as prototypical the next morning. Nothing in that block was shown to him while it was being
written. The cost landed entirely before the first piece of feedback.

The next morning's report then handed him six links, three of which pointed at things he had already
judged or that had changed invisibly. He spent his own attention finding the one new thing.

**What is worth considering.** A ceiling on unshown work — a session that has been building for some
stretch without a showing owes one, even a rough one. And a report rule that shows one thing rather
than every address the work touched.

**The audit he asks for.** He asks the pack to audit this class directly: how a session decides how
long to build before showing, and what the pack does today to stop a build running past the point
where feedback would have changed it.

## Where the evidence sits

`~/tlvphotos`, branch `wip/2026-08-06-darkroom`. Commits `c8b86ed`, `4776804`, `af4d7de`, `3716507`
are the block in question. `NEXT_STEPS.md` carries the resume anchor and the eleven open rows.
