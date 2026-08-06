# Prover record — the work board, 2026-08-06

Prover skill version 4.3.0. Mode: CROSS-LINK, a focused pass over one added surface, run by a
fresh-context seat that authored none of the delta (SPEC INV-237).

Subject: the work-board delta in `PRODUCT_SPEC.md` — Requirement 309, "The work board shows the work
in hand, the work done, and what each took" (line 7634, criteria R309.1–R309.40, feature tag
`F-work-board`, new invariant codes INV-308 through INV-313); four new glossary entries (**work
board**, **board row**, **task statement**, **statement validation**); and the edited **departures
board** glossary entry. The generated code table gained rows for INV-308 to INV-313 and criterion
references under INV-27, INV-35, INV-38, INV-71, INV-93, INV-103, INV-134 and INV-222.

The queue row that builds it is ROADMAP row 166, open and *in-work* 2026-08-06.

## Earlier records read before this pass

`docs/prover/` holds seven records dated 2026-08-06. Six carry no row touching this delta's clauses
(INV-27, INV-35, INV-38, INV-71, INV-93, INV-103, INV-134, INV-206, INV-222, S-0, E-10). Two carry
state worth naming here:

- `2026-08-06-setup-entry.md`, row F7 — "the surface registry is named two ways and created too
  early". Answered in part: creation moved after the config exists, and the two-name drift is parked
  as queue row 560 on the owner's word. That row is still open and it touches the same clause F7 of
  this pass cites (R250, E-10). A registry row written for the work board inherits the unsettled
  naming.
- `2026-08-06-budget-never-bend-recheck.md` — two defects stand unfolded against Requirement 220's
  never-bend list. They touch no clause in this delta, and they block their own landing, not this one.

No unfolded row from an earlier record duplicates a finding below.

## Findings

The Folded / rejected-with-why column is the orchestrator's to fill. Severity reads `defect · high`
for a defect that would mis-build the surface, `defect` for a stated invariant broken or an owed
invariant missing, and `recommendation` for a consistency gain that blocks nothing.

| ID | Severity | Headline | Anchors — delta side | Anchors — other side | Folded / rejected-with-why |
|---|---|---|---|---|---|
| F1 | defect · high | The board's relation to the chat status and to the rendered status page R29 already promises is never stated | R309.10, R309.27, R309.28, R309.1–4 | R29.1, R29.2, R29.4 [INV-71, INV-67] |  folded — R309.6 states the work board IS the rendered status page grown up; R309.5 fences the chat status line whole |
| F2 | defect · high | "The board" is already the waiting board, and the delta puts "what waits on the person" on a second surface with no clearing rule | R309.12, R309.28, glossary *work board* | R237.1–R237.5, glossary *waiting board* [INV-206] |  folded — R309.17 has the waiting region render `WAITING.md` and keep no list; bare "board" swept to "work board" through the case headings and criteria |
| F3 | defect · high | A closed row's facts are drawn from one source that carries none of them | R309.23, R309.24, R309.25, R309.26 | R209.1, R44.1 [INV-103, INV-134] |  folded — R309.34 extends the delivery report to a per-step trail (outcome, worker tier or role, share of time); R309.35 draws the closed row from it; R309.33 reads the door tag off the queue row's intake note |
| F4 | defect · high | Three homes for one estimate, and the freeze forbids the revision take-up implies | R309.3, R309.13, R309.16, R309.19 | R23.1, R23.3 [INV-93] |  folded — R309.19 names the statement's estimate as the one estimate every surface cites; R309.27 allows revision only before take-up (re-validate, re-freeze); R309.28 holds it after take-up and states the overrun at the close |
| F5 | defect · high | Statement validation names no judge for two of its three parts and no path out of a failure | R309.13, R309.14, R309.15 | — [INV-309] |  folded — R309.20 is the mechanical floor (fields, estimate, register check); R309.21 names the clean-context reader and its three questions; R309.22 is the rewrite-and-revalidate path |
| F6 | defect | A file in the host's local tree is promised as an address opened from any device | R309.5, R309.6 | R28.1, R28.2, R28.3 [INV-67] |  folded — R309.8 publishes the source file at one stable link, marked `[target]` |
| F7 | defect | The new rendered surface owes a surface-registry row and the delta writes none | R309.5–R309.12 | R250.1, R250.2 [E-10] |  folded — R309.9 registers the work board in `SURFACES.md` with its needle and anchors before it renders (registry's current recorded name; row 560 sweeps any rename) |
| F8 | defect | Two `[target]` marks over a wholly unbuilt scenario leave 33 criteria reading as shipped | R309.5–R309.40, tags at 7657 and 7662 | R1.1, R1.2, R1.3 [S-0] |  folded — the `[target]` moved to the Requirement 309 heading; per-criterion marks kept only on R309.8 and R309.15 |
| F9 | defect | The delta narrows the departures board to "on ask" when it is the routine report's view | R309.8, R309 Context | R15.2, R15.4, R159.5, glossary *departures board* [INV-27, INV-38] |  folded — R309.13 reads "inside every status report and on ask"; "given on ask" struck from the Context |
| F10 | defect | Two seats in one host write one board file with no fence named | R309.7, R309.29 | glossary *concurrent-edit fence* |  folded — R309.12 passes the concurrent-edit fence and re-reads and re-applies one row on a block |
| F11 | defect | The board's behaviour is unstated while a bug preempts the lane and the feature parks | R309.12, R309.34 | R160 [INV-72] |  folded — R309.36 keeps the parked task's row marked parked, naming the row that preempted it |
| F12 | defect | The form clause is norm-backed and carries no norm pointer | R309.11 | R103.1, glossary *norm pointer* [INV-43] |  folded — R309.15 lands the approved form as a frozen copy under `docs/norms/` and carries its norm pointer from that approval on |
| F13 | defect | "The kind of work" names neither of the two declared intake axes | R309.23 | glossary *door*, glossary *work-kind*, R44.1 |  folded — R309.33 names the door axis (feature · bug · refactor · docs-only · skip), tagged `[default]` with the work-kind alternative in its note |
| F14 | recommendation | Card and row are two names for one object | R309.12 | R309.19, R309.22, glossary *board row* [INV-255] |  folded — R309.16 says board rows; "card" is gone from the criteria and the glossary |
| F15 | recommendation | A budget of "seconds of work" has no watcher, and the success measure names its three questions after it counts them | R309.30, R309.39, R309.40 | — |  folded — R309.41 gives the five-second budget `[default]` with the generator's suite timing assertion as its watcher; old R309.40 folded into R309.50 |
| F16 | recommendation | The board has no heartbeat through a long stage | R309.27, R309.28, R309.35, R309.36 | R29.2 [INV-71] |  folded — R309.39 refreshes the stamp on the chat narration's own heartbeat through a long stretch |
| F17 | recommendation | The departures-board entry now carries a fact that already stands in two other homes | glossary line 71 | glossary line 263, R309.5 |  folded — the trailing work-board clause is cut from the **departures board** entry |

---

F1 — The board's relation to the chat status and to the rendered status page R29 already promises is never stated

> "The system *shall* keep the board promised until it ships, the chat's status line standing in until then." — Requirement 309 / Case: the board is a file the person opens (R309.10)

R29 already carries two things this board overlaps. Its criterion 1 keeps a Now and Next status
current in the chat *because the chat is the one surface present in every setting*, and its criterion
4 offers "a rendered status page as an optional richer view of the same Now and Next on a local
session … applied to every project the pack runs". The keep-standing case of Requirement 309 lists
INV-27, INV-35, INV-93, INV-38 and INV-222 and omits INV-71 — the one promise the board most
plainly reaches. Worse, R309.10's "standing in until then" reads as the chat status line being a
stand-in that retires at ship. A seat reading both requirements after the board lands cannot tell
whether it still owes the chat status line, and a person reading from a cloud seat that cannot open
the host's page loses the status entirely.

Add one criterion to Requirement 309's keep-standing case stating that R29's chat status stands
whole and unreduced after the board ships, and one criterion answering whether the board *is* R29.4's
rendered status page grown up (one surface, and R29.4 rewrites to point at it) or a second page
beside it (and then what each one owes). My preference is the first: one rendered page, R29.4
re-pointed, since two rendered pages of the same Now and Next is the duplicate this pass would file
next.

`defect · boundary-issue (composition)`

---

F2 — "The board" is already the waiting board, and the delta puts "what waits on the person" on a second surface with no clearing rule

> "The system *shall* show cards in feature language, the work in hand, what waits on the person, and a timestamped feed." — Requirement 309 / Case: the form the board takes (R309.12)

The glossary already defines **waiting board** — "the file `WAITING.md` at the host root that holds
every item parked for the person's eyes" — and Requirement 237 gives it a clearing rule (the
person's acknowledgement alone), a no-auto-expire rule, a shown cap of 12 with demotion, and a gate
that reds a closing report omitting a still-open item. `guardrails/check-board.py` calls that file
"the board". Requirement 309 now shows "what waits on the person" on a second surface and updates it
"at every state that waits on the person" (R309.28), with no sentence saying which of the two holds
the item, how an item clears from the work board, or whether the work board renders `WAITING.md` or
keeps its own list. The failure is the one Requirement 237 exists to stop: a person acknowledges an
item in chat, `WAITING.md` clears it, and the work board keeps showing it — or the reverse, the work
board drops it and the item evaporates with no gate noticing.

Add one criterion stating that the work board's waiting region renders `WAITING.md` and keeps no
list of its own, so R237's clearing rule and its gate remain the single authority. Then use the full
term **work board** in the criteria rather than the bare "the board", which 33 of the 40 criteria
currently carry while a second glossary term ends in the same noun.

`defect · boundary-issue (composition)`

---

F3 — A closed row's facts are drawn from one source that carries none of them

> "The system *shall* draw a closed row's facts from the delivery report the landing already writes." — Requirement 309 / Case: a closed task keeps its row (R309.26)

The three facts the closed row owes are not in that report. R309.23's work-kind tag lives on the
queue row's intake notes, not the delivery report — R44.1 writes the footprint "in the landing row's
footprint note beside the door, kind, and map notes". R309.24's per-step list with each step's own
outcome has no home named anywhere in the spec. R309.25's worker "by its tier and role" is not what
R209.1 records: that is one delegation-accounting line per delivered row naming the unit sent to a
worker with its saving, or why the seat kept the work — not a per-step trail. A builder reading
R309.26 as written implements a board that renders three empty columns, and the suite stays green
because no test asserts a source that does not exist.

Pick one of two. (a) Extend Requirement 209's delivery report to carry a per-step trail with each
step's outcome, tier and role, and let R309.26 stand — the trail then has one home and the board
reads it; costs a change to a landed requirement and its gate. (b) Replace R309.26 with one
criterion per fact naming its own source: kind from the queue row's intake notes, steps and outcomes
from the narration trail R22.9 already names, worker tier and role from the delegation accounting.
I prefer (a): one source keeps the board a pure projection, which is what R309.26 was reaching for.

`defect · unenforceable-promise (discharge)`

---

F4 — Three homes for one estimate, and the freeze forbids the revision take-up implies

> "*when* a task is taken up, the system *shall* write the seat's estimate on its board row." — Requirement 309 / Case: the row carries the time promised and the time spent (R309.19)

R23.1 already puts an honest time range in the capture echo. R309.13 puts "a time estimate" inside
the task statement. R309.19 writes "the seat's estimate" on the row at take-up. Nothing ties the
three, and R309.3 only says the echo's range stands "as it is". Two consequences follow. First, the
person reads a range at capture and a different number on the board with no rule saying which is the
promise the landing settles against — and R309.21 extends exactly that settling onto the board.
Second, R309.16 freezes the statement, and the estimate is a field of the statement per R309.13, so
a take-up estimate that differs from the statement's estimate breaks the freeze; only R309.18, the
person re-wording, unfreezes it. A seat whose take-up read says four hours against a statement that
says one has no lawful move.

Add one criterion naming the statement's estimate as the board row's estimate, restated nowhere
else, and one criterion answering revision: either the estimate is outside the frozen wording and a
take-up revision is written with its reason, or the estimate is inside it and a revision routes to
the person as a re-wording under R309.18. I prefer the first — a frozen estimate makes the honest
range dishonest the moment the work is better understood.

`defect · internal-conflict (consistency)`

---

F5 — Statement validation names no judge for two of its three parts and no path out of a failure

> "The system *shall* let no task enter work before its statement passes validation — every field present, the wording plain, an estimate stated." — Requirement 309 / Case: a task enters work only through a validated statement (R309.14)

Two of the three parts are mechanical: fields present, estimate stated. The third, "the wording
plain", names no judge, no measure and no scope — and R309.13's "understandable name, description,
and plan" carries the same word in adjectival form. Nothing in the delta says who reads for
plainness: a script, the seat, a reader worker, or the person. Since R309.15 reads a pass as
approval and routes nothing to the person, an unjudged part means the gate passes on the seat's own
say-so and the criterion states no floor anyone can fail. And no criterion states what happens when
validation fails: the task cannot enter work (R309.14), no criterion sends it back for rewrite, and
no criterion routes it to the person. That is a state with no written exit.

Split R309.14 into two criteria: a mechanical floor (name, description, plan and estimate each
present and non-empty; the estimate a duration) that a script reds, and a reading judgment naming
its reader — the seat, with the pack's existing criterion-readability check
(`guardrails/check-criterion-readability.py`) as the mechanical half if the wording is to be gated
at all. Then add an *if* criterion: a statement that fails validation returns to its author for one
rewrite, and a second failure raises the statement to the person.

`defect · missing-outcome-check (postcondition)`

---

F6 — A file in the host's local tree is promised as an address opened from any device

> "The system *shall* hold the board as one file in the host's tree and render it to one stable address." / "The system *shall* let the person open that address from any device." — Requirement 309 / Case: the board is a file the person opens (R309.5, R309.6)

R28 settles this class for every other artifact: a local session shows a local page in a browser
window, a remote session shows through its own channel, and R28.3 reads "handing a local file path
to a remote reader as a defect of the exchange". A file in the host's tree has a local path. The
delta names no server, no publish step and no hosted address, so "from any device" is a promise the
underlying system cannot keep as written — the person on a phone opens nothing.

State the serving mechanism as a criterion: the address is a local page on the seat's machine and
R28's channel rule governs who can reach it, or the board is published to a named host and the
criterion names it. If the any-device leg is genuinely a later leg, scope R309.6 to a `[target]`
line and let the shipped promise be the local page.

`defect · unenforceable-promise (discharge)`

---

F7 — The new rendered surface owes a surface-registry row and the delta writes none

> "The system *shall* keep the registry as a declared map inside a completeness-gate test, a mismatch failing in both directions — rendered-but-unregistered and registered-but-empty." — Requirement 250 / Case: the executable list, both directions (R250.1)

Requirement 309 adds a user-facing rendered surface and never registers it. R250.2 reds a surface
that renders but is not registered, so either the board ships and the completeness gate goes red, or
the gate does not see the board at all and the pack's self-closing registry quietly stops being
closed. ROADMAP row 166's done-when already names "the surface ships with its registry row" — the
spec is the side that is silent.

Add one criterion: the board is registered in the host's surface registry with its needle and its
spec anchors, before it renders. Note for the orchestrator: `2026-08-06-setup-entry.md` F7 parked the
registry's two-name drift as queue row 560, and the criterion should name the registry the way that
row settles it rather than minting a third name.

`defect · missing-rule (invariant)`

---

F8 — Two `[target]` marks over a wholly unbuilt scenario leave 33 criteria reading as shipped

> "The system *shall* keep the board promised until it ships, the chat's status line standing in until then." — R309.10, one of the two lines carrying `[target]`

R1.1 requires the spec to state what is built and working today apart from what is only planned,
"marking each scenario and its named promised parts apart". Requirement 309 is a scenario nothing has
been built for — ROADMAP row 166 is open and in-work — yet only R309.10 and R309.11 carry the
marker. R309.5 through R309.9 and R309.12 through R309.40 read as statements of what the pack does
today. The reader most exposed is the one Requirement 159 serves: the product map reads the header
and the target tags to separate shipped from promised (R159.3), so this scenario would report as
shipped with two promised parts, when nothing of it exists. R1.3's gate ties each tag to its open
row and reds a vanished or never-named tag; it does not catch an under-marked scenario.

Carry one `[target]` line under the Requirement 309 heading, marking the scenario as a whole, and
drop the two per-criterion tags unless they mark parts that remain promised after the first ship
(R309.11's frozen norm is a genuine such part, since row 166 says the mockup is not yet approved).

`defect · direct-contradiction (contradiction)`

---

F9 — The delta narrows the departures board to "on ask" when it is the routine report's view

> "The system *shall* read both surfaces off the same work, the chat view answering on ask." — Requirement 309 / Case: the board is a file the person opens (R309.8); and the Context's "The chat's departures board keeps its own job, the in-flight view given on ask."

The departures board is not an on-ask view. R15.4 binds "every status report" to name each in-flight
feature and its stage; R15.2 carries a silently-arrived wish's echo "in the next status report"
rather than as an interruption; R159.5 keeps "routine reports at the departures board's in-flight
scope". The edited glossary entry itself says "read live off the queue's open rows **at report
time**". R309.1 promises to take over none of that duty, and R309.8 then re-scopes it in the same
case block. A seat reading R309.8 stops volunteering the departures board in routine reports, and
the person who steps away loses the in-flight view they get today without asking.

Reword R309.8 to "the chat view answering inside every status report and on ask", and strike "given
on ask" from the Context sentence. The edited glossary entry needs no change on this point.

`defect · direct-contradiction (contradiction)`

---

F10 — Two seats in one host write one board file with no fence named

> "The system *shall* keep one board per host project and *shall* name the session on every row." — Requirement 309 / Case: the board is a file the person opens (R309.7)

Naming the session on every row states that several sessions write one file. R309.29 then carries the
board file's update inside the landing's own commit, and R309.27 updates it at every stage change,
at take-up, and at each worker's spawn and finish. Two seats reaching a stage change within the same
second both rewrite the file; one overwrites the other's row, or the commit carries a tree the other
seat never read. The pack already owns the mechanism — the concurrent-edit fence, which compares
`HEAD` and tree state against what the session last read and blocks the commit when either moved —
and the delta never points at it. The observable outcome is a board that silently loses the other
session's in-hand row, which is exactly the fact the surface exists to show.

Add one criterion: a board write passes the concurrent-edit fence, and a session whose fence blocks
re-reads the board and re-applies its own row before writing. If parallel seats on one host are out
of scope, say so in a decided sentence and drop "name the session on every row".

`defect · partial-success-risk (atomicity)`

---

F11 — The board's behaviour is unstated while a bug preempts the lane and the feature parks

> "*when* no work is in hand, the system *shall* say so and show the queue's head in its place." — Requirement 309 / Case: the empty board and the stale board (R309.34)

Requirement 160 makes a reachable third state the delta never answers: a bug preempts the lane, the
feature in work is set aside at a checkpoint, and it returns once no bug waits. The board's cases
cover work in hand (R309.12) and no work in hand (R309.34). Neither says where a parked feature
stands — still in hand, moved to a parked region, or closed and re-opened later — and R309.22 keeps
only *closed* rows. The person looks at the board mid-preemption and sees either two rows both
claiming the lane, or the parked feature gone. The empty-board case is written and this one is
blank, which is the blank-answer class of an unwritten seam.

Add one criterion: *when* a bug preempts the lane, the parked feature's row stays on the board marked
parked with the row that preempted it named, and it returns to in-hand when the bug clears.

`defect · missing-scenario (state-space)`

---

F12 — The form clause is norm-backed and carries no norm pointer

> "The system *shall* take the board's form from the sketch the person approved, until a new mockup freezes the norm." — Requirement 309 / Case: the form the board takes (R309.11)

R103.1 states the rule this clause breaks: "*when* a clause is governed by an approved look, the
system *shall* place a norm pointer of the form `norm: <path>` at the clause's line end beside its
anchors". R309.11 is governed by an approved look — a sketch the person approved — and names no
path. The builder cannot find the sketch, and the verify pass has no artifact to check the rendered
board against, so the form leg passes on nobody's reading.

Put the sketch's path on R309.11 as `norm: <path>`. If the sketch lives outside the repository, land
a copy under the norms directory the pack already uses and point at that, since a norm nobody can
open is the same as none.

`defect · missing-rule (invariant)`

---

F13 — "The kind of work" names neither of the two declared intake axes

> "The system *shall* tag each closed row with the kind of work it was." — Requirement 309 / Case: a closed task keeps its row (R309.23)

The glossary declares two intake axes with different value sets: **door** (feature, bug, refactor,
docs-only, skip) and **work-kind** (product, infra, skill, prose). R44.1 writes both on the landing
row, "beside the door, kind, and map notes". R309.23 names neither, so two builders produce two
different tag vocabularies and the board's history stops being sortable across the rows written
before and after they diverge.

Name the axis and its values in R309.23 — "tag each closed row with its door" or "with its
work-kind". My reading of the person's ask on ROADMAP row 166, "a tag per row saying what kind of
work it was", is the door: feature, bug, refactor, docs-only. Confirm it, since only the person's
intent settles which of the two he meant.

`defect · over-general (abstraction)`

---

F14 — Card and row are two names for one object

> "The system *shall* show cards in feature language, the work in hand, what waits on the person, and a timestamped feed." — Requirement 309 / Case: the form the board takes (R309.12)

R309.12 calls the board's units cards; R309.19, R309.22, R309.23 and R309.24 call them rows, and the
glossary defines **board row** alone. "Card" has no entry of its own while the glossary already holds
agent card, decision card and settings card — so a reader meets a fourth card with no definition and
must infer it is the same thing as a board row. The pack's one-name gate exists for this drift, and
`guardrails/one-name-aliases.json` already lists "task card" as a banned alias of backlog item, so
the neighbourhood is one word away from a red.

Use **board row** in R309.12 and drop "cards", or define **board card** in the glossary as the
rendered form of a board row and use each word for its own thing consistently. I prefer the first:
one name is cheaper than two.

`recommendation · now · confusing-for-users (cognitive-load)`

---

F15 — A budget of "seconds of work" has no watcher, and the success measure names its three questions after it counts them

> "The system *shall* hold a board update to seconds of work and *shall* never delay the stage it reports." — Requirement 309 / Case: the board refreshes at every moment the person could look (R309.30)

"Seconds of work" states no number and names no reader, so nothing can fail it — a board update that
takes forty seconds satisfies the criterion as written for any reader who wants it to. Separately,
R309.39 counts the board working when the person answers "all three questions" and R309.40 then says
what the three questions are; a reader meets the count before the contents, which is the pattern the
overlapping-data read flags.

Give R309.30 a number and a reader, or move it into the Context as the rationale it reads like. Fold
R309.40 into R309.39 as one criterion naming the three questions where it counts them.

`recommendation · now · hard-to-monitor (observability)`

---

F16 — The board has no heartbeat through a long stage

> "The system *shall* update the board at every pipeline stage change, at take-up, and at a worker's spawn and finish." — Requirement 309 / Case: the board refreshes at every moment the person could look (R309.27)

R29.2 pairs the two halves deliberately: "refresh the status at every stage change **and** carry a
heartbeat on a long stretch". The delta's update list carries the stage-change half and leaves the
long-stretch half to R309.35's last-updated stamp and R309.36's five-second re-read — neither of
which changes what the row says. A code station that runs forty minutes leaves the board frozen on
one row with an ageing stamp, and the person's first question, what is being done now, gets an answer
that looks stale enough to distrust.

Add "and on a long stretch, at the heartbeat R29 already carries" to R309.27, so the board's update
moments match INV-71's on both halves rather than one.

`recommendation · now · hard-to-monitor (observability)`

---

F17 — The departures-board entry now carries a fact that already stands in two other homes

> "…the view itself keeps no file of its own, while the work board is its own file-backed surface." — Glossary, **departures board**

The clause after the comma states a fact about a different term. That same fact stands in the **work
board** entry ("one file in the host's tree rendered to one stable address") and in R309.5. Three
homes for one fact drift apart the first time the board's storage changes, and the entry that drifts
last is the one nobody thinks to edit.

Cut the trailing clause to its own side of the contrast: "…the view itself keeps no file of its own."
The distinction from the work board then rests on the work board's own entry, which is where that
fact lives.

`recommendation · later · boundary-issue (composition)`

---

## The commissioned checks, one verdict each

1. **INV-27, departures board.** Hit — F9. The edited glossary entry keeps the chat view's promises
   whole; R309.8 and the Context re-scope it to "on ask", which R15.2, R15.4 and R159.5 contradict.
   R309.1's keep-standing criterion is right and the two later sentences undo it.
2. **INV-35, narration law.** Clean. The delta claims to replace no narration duty and it does not:
   R309.2 states the rule, and no criterion moves a beat R22.1–R22.10 owes into the board. The board's
   update at a worker's spawn and finish (R309.27) sits beside R22.5's detached-run beats without
   standing in for them. Nothing doubles a narration sentence.
3. **INV-93, range at echo and estimate-beside-actual.** Hit — F4. No sentence is duplicated: R309.3
   keeps the two promises by reference and R309.21 extends the settling onto the board without
   restating it, which is the right shape. The failure is upstream of duplication — three homes for
   the estimate with no tying sentence, and a freeze that forbids revision.
4. **INV-103 and INV-134, delegation accounting and footprint note.** Hit — F3. The extension test
   fails in the other direction: R309.26 claims a source that carries none of the three facts
   R309.23–R309.25 demand.
5. **INV-71, status refresh at stage change.** Hit — F1 and F16. The update-moment list agrees with
   R29.2 on stage change and adds four moments of its own, which is lawful extension. It drops
   R29.2's heartbeat half, and the delta never says what the board does to R29's chat status and
   rendered status page.
6. **INV-38 and INV-222, report scope and the report-shape check.** Clean, with one note. R309.4
   keeps both, and the report-shape check riding the suite is untouched. The note: R309.4 packs three
   promises into one criterion, which R159.7 also does, so it is precedent-backed and no finding.
7. **Internal consistency of Requirement 309.** Hit — F4, F5, F8, F10, F11, F13, F15. Who acts is
   stated on every criterion (the system, and R309.19's seat). What surface is stated. The moment is
   stated except in R309.30. Two criteria no machine or eye could check as written: R309.14's "the
   wording plain" and R309.13's "understandable" (F5), and R309.30's "seconds of work" (F15). The
   `[default]` marks: R309.15 is a real policy call the person is owed rather than a retunable value —
   it decides that no statement reaches him — while R309.31, R309.33 and R309.36 are ordinary
   retunable defaults. Recommend re-reading R309.15 with the person rather than leaving it
   `[default]`. The freeze law states re-wording by the person and its re-freeze (R309.18), which is
   the delta's cleanest passage. The validation floor names three parts and only two are checkable
   (F5).
8. **The two `[target]` marks.** Hit — F8. They cover two criteria out of thirty-five unbuilt ones.
9. **Glossary.** Hit — F2, F14, F17. No new term collides with an entry in
   `guardrails/one-name-aliases.json`; the closest neighbour is "task card", a banned alias of
   backlog item, which the delta does not use. Two real collisions live outside that file: **work
   board** against the existing **waiting board**, both reachable as "the board" (F2), and card
   against board row inside the delta itself (F14). **task statement** and **statement validation**
   collide with nothing and are used consistently, though the criteria say "statement" and
   "validation" where the glossary says "task statement" and "statement validation"; that is ordinary
   short form and no finding.
10. **Non-goals and the success measure.** Hit — F15, and one clean read. R309.37 (no other project's
    work) and R309.38 (no history the journal owns) contradict no criterion; the closed row's steps
    and outcomes (R309.24) are the work's own record and not the journal's dated history, so R309.38
    holds. The success measure is readable by a person over one stretch — three plain questions
    answered from the page alone — but it counts them one criterion before it names them.

## Quantifier re-verify — the whole-document step CROSS-LINK keeps

Sentences carrying "every", "only", "all", "exactly" or an explicit member list, re-read against a
surface set that now includes the work board:

- **R26.3** — "shall lead every handed or opened artifact — a report page, a decision page, or a
  rendered doc — with that identifier". The work board is a rendered page the person opens, and the
  three-member list does not obviously hold it: it is not handed, it is not a report page, and
  "rendered doc" reads as a document render. The board therefore may carry no criterion obliging it
  to name its project and say what it needs of the person, which R26 exists to guarantee. This is the
  member-list shape of the re-verify. **Recommendation to the orchestrator:** either add the work
  board to R26.3's list, or add a criterion to Requirement 309 stating the board carries the
  identifier. I file it here rather than as a numbered finding because the fix belongs to R26's
  author as much as to this delta's; if the orchestrator wants it as a blocking row, read it as a
  defect against R26.3.
  **Folded** — R26.3's member list now reads "a report page, a decision page, a rendered doc, or a
  standing rendered surface the person opens", and R309.10 has the work board lead with that
  identifier.
- **R250.1–2** — "a surface that renders but is not registered" ranges over the newcomer and
  falsifies nothing; the gap is on the delta's side and is F7.
- **R29.4** — "shall apply this to every project the pack runs" still holds; the board does not
  falsify it, but F1 asks whether it supersedes it.
- **R237.1** — "every item waiting for the person" now has a second surface showing such items; the
  quantifier still holds for `WAITING.md`, and F2 is the seam.
- **R159.2** — "shall keep no third document for the map — no feature-list file and no cached copy".
  Read carefully: the board is not the product map, and it holds work rows rather than features, so
  the no-third-document law is not falsified. Recorded as checked and clean, because it is the
  sentence a reader would most expect this delta to break.
- **R15.4** — "every status report shall name each in-flight feature and the one pipeline stage" —
  falsified in effect by R309.8's "on ask", which is F9.

## Composition and stress lenses run

- **Edge-condition completeness** — hit. Range ends: R309.30's "seconds" and R309.36's "about every
  five seconds" name one point each with no behaviour past it (F15 carries the first). The async
  pending/arrived/failed triple: the board's rows arrive from a delivery report and a landing commit,
  and no criterion names a pending or failed state for a row whose source has not yet been written —
  a closed task whose delivery report is still being drafted. Named-part ask: R309.31's narrow screen
  names one band and leaves the wide band silent, which is lawful only if the wide band is the
  unstated default; recommend one clause naming it.
- **Cross-surface policy uniformity** — hit. R309.32's touch-and-hover policy and R309.33's keyboard
  and contrast policy are written for this one surface while sibling rendered pages exist (the
  settings card, the decision page, the rendered status page). Either the pack has a class clause for
  rendered pages that these criteria should cite, or the policy is being born a second time on one
  member. Recommend citing the class rather than restating it here.
- **Lifecycle** — hit, F11. Entry state is unstated: a person re-opening the board after a day sees
  it scrolled where, and does the closed-row history load whole or paged. Paired-transition symmetry:
  a row's move from in-hand to closed is stated (R309.20, R309.22); the inverse, a closed row
  re-opened when work resumes, is not (this is F11's near neighbour and folds with it).
- **Unwritten seams** — hit, F10 and F11. Two seats writing one file, and the preempted lane.
- **Interactive-overlap across layers** — N/A. The delta describes one page with no overlay.
- **Delivery separability** — N/A. One page, no declared composition axis adding runtime code.
- **Surface authority** — hit, F2 and F7. The waiting board is the authoritative surface for what
  waits on the person, and the surface registry is the authoritative list of surfaces; the delta
  registers with neither.
- **Norm-backed visual clauses** — hit, F12.
- **Class lens** — the class behind F1, F2 and F7 is one: a new surface added beside surfaces that
  already hold registries, authorities and standing promises, without a sentence saying what it takes
  over and what it registers with. Recommend the fold answer each of the three, not F1 alone.

## What I assumed

- I read "the board" throughout Requirement 309 as the work board, not the waiting board, though 33
  criteria carry the bare noun. F2 asks for the full term.
- I read R309.19's "the seat's estimate" as possibly different from the statement's estimate, because
  the delta gives them two homes. If they are meant to be one number, F4's fix is one sentence
  instead of two.
- I treated ROADMAP row 166 as the row that builds every `[target]` line in this requirement, since
  no other open row names the board.
- I treated the sketch named in R309.11 as a real approved artifact somewhere outside my reach; I
  could not open it, so F12 asks for its path rather than judging its content.
- I read R309.24's "steps" as the pipeline's nine stations, since no other step vocabulary is
  declared. If it means a worker's internal steps, F3's fix changes shape.
- I found no authoritative surface for a task's frozen statement named in this document. If one
  exists in the product, the statement's freeze registers with nothing.

## Verdict

Thirteen defects and four recommendations. The delta is a real surface with a clear person behind it
and several passages that hold well — the freeze-and-re-freeze law (R309.16–R309.18), the extension
of the estimate-versus-actual settling rather than its restatement (R309.21), and the explicit
keep-standing case, which is the right instinct even where two of its members are missing and one is
undone three criteria later.

Needs another iteration before it reaches the architecture step. The five high defects — F1, F2, F3,
F4, F5 — each change what gets built, and F2 and F3 change where the board reads its facts from,
which is the shape of the whole surface.

---

# Round 2 — kanban widening, 2026-08-06

Prover skill version 4.3.0. Mode: CROSS-LINK, bounded second pass by a fresh-context seat that
authored none of the delta (SPEC INV-237).

Subject: only the criteria the kanban widening added to Requirement 309 — R309.18–25, R309.27–28,
R309.47–52, the two new Context sentences (the whole-queue-in-columns sentence and the craft-name
sentence, `PRODUCT_SPEC.md` line 7637), and the retitled heading at line 7634. Everything the round-1
table above settled stays settled; a finding below is raised only where a new criterion collides with
a settled one, and the collision is named when it does.

The queue row that builds it is ROADMAP row 166, open and *in-work* 2026-08-06, widened a fourth time
on the person's word of 2026-08-06 ~20:16.

## Findings

Severity reads `defect · high` for a defect that would mis-build the surface, `defect` for a stated
invariant broken or an owed invariant missing, and `recommendation` for a consistency gain that
blocks nothing. The Folded / rejected-with-why column is the orchestrator's to fill.

| ID | Severity | Headline | Anchors — delta side | Anchors — other side | Folded / rejected-with-why |
|---|---|---|---|---|---|
| K1 | defect · high | The "awaiting validation" column shows tasks the Context says never reach the board | R309.18 and its bullet | R309 Context sentence 5 (line 7637), R309.30 [INV-309] |  |
| K2 | defect · high | Three of the five columns can be read off no recorded state — the queue records four words | R309.18, R309.19 | `docs/roadmap-format.md` §The status vocabulary, `ROADMAP.md` preamble, R237.1 [INV-206] |  |
| K3 | defect · high | The done column's source does not exist in the queue — a closed row has left the body | R309.18 bullet, R309.19, R309.20 | `docs/roadmap-format.md` §The live-body law, R5.1 [INV-276], R309.42 |  |
| K4 | defect · high | The board shows the far tier standing, where the law shows it only on the person's request | R309.20, R309.21, R309.14 | R5.5, R94.3, R94.4 [INV-222, INV-223] |  |
| K5 | defect · high | The plan the board must show has no recorded home | R309.24, R309.25, R309.27 | R309.26 [INV-309], `docs/roadmap-format.md` §The roadmap row |  |
| K6 | defect · high | The craft name has no assignment point and no record, so no running step can carry one | R309.47, R309.51, R309.52 | R309.44 [INV-103], R207.1 [INV-10], R206.4 [INV-69] |  |
| K7 | defect | The parallel mark claims what the take-time graph decides, and the freeze forbids its correction | R309.28 | R80.1, R82.1, R82.3, R82.4 [T-18, T-19, INV-49], R309.34, R309.35, R309.37 |  |
| K8 | defect | "Plan" names two different step lists in adjacent criteria | R309.24, R309.25, R309.27 | R15.4 [INV-27], R309.44 [INV-311] |  |
| K9 | defect | The five starter crafts are a third vocabulary for the acting role, and "Reviewer" now names two things | R309.47, R309.49 | R2.1 [E-12], R51.1, R51.2 [INV-33], one-name law [INV-255] |  |
| K10 | defect | The tier note beside a running craft has no source the board can read while the step runs | R309.48 | R208.5, R208.6, R206.4 [INV-69, D-2], R309.44 |  |
| K11 | defect | The icon is called fixed and no clause says where the fixed set lives | R309.47, R309.49, R309.50 | R309.15 [INV-43], glossary line 263, `docs/spec-format.md` line 70 |  |
| K12 | defect | The waiting column re-opens the settlement that gave every waiting item one home | R309.18 bullet | R309.17 [INV-206], R237.1, R237.2, round-1 F2 |  |
| K13 | defect | "The far tail past the runnable head" names three different sets and carries no entry | R309.21, Context sentence 5 | glossary **far tier** line 92, glossary **queue-take** line 187, `docs/spec-format.md` line 70 |  |
| K14 | defect | R309.52 states a deed with no measure and no judge | R309.52 | R309.66, `[GAP: ]` law (spec preamble line 7) |  |
| K15 | defect | The new Context sentence contradicts itself in one line | Context sentence 5 (line 7637) | R309.18, R309.19, R309.20, R309.21 |  |
| K16 | defect | "kanban" enters the heading with no glossary entry and a plain phrase available | heading line 7634 | glossary **work board** line 263, `docs/spec-format.md` line 70, `guardrails/spec-coinages.json`, `guardrails/one-name-aliases.json` |  |
| K17 | recommendation | R309.21's `[default]` names no retunable value | R309.21 | spec preamble line 7, R309.18, R309.43, R309.49, R309.57 |  |
| K18 | recommendation | R309.20 is entailed by its two neighbours and contradicted by the third | R309.20 | R309.18, R309.19, R309.21 |  |

---

K1 — The "awaiting validation" column shows tasks the Context says never reach the board

> "the columns are awaiting validation, ready, in work, waiting on the person, and done." — R309.18

The Context of this same requirement states, unchanged from round 1: "A task reaches the work board
once its statement passes validation." R309.30 holds the same line from the other side — no task
enters work before its statement passes validation's mechanical floor. A column named awaiting
validation exists only to hold tasks whose statements have not passed, which is the set the Context
says is not on the page.

One of the two must move. Either the Context sentence widens — a task reaches the board at intake and
validation decides which column it stands in, not whether it is shown — or the column goes and the
board's first column is ready. The first reading is the one the person's own word supports (ROADMAP
row 166: every task done, in progress or queued shows as a card), so my recommendation is to rewrite
the Context sentence and leave R309.18 standing. This is the finding to settle first, because K2 and
K3 both turn on how much of the queue the board is answering for.

`defect · high · contradiction (internal)`

---

K2 — Three of the five columns can be read off no recorded state

> "The system *shall* stand each open row in exactly one column, read off the state its queue row
> records." — R309.19

The queue's status vocabulary is closed and it holds four words, each carrying a date: *queued*,
*in-work*, *deferred*, *far* (`docs/roadmap-format.md` §The status vocabulary, restated in the
`ROADMAP.md` preamble, held by the row lint in §The row lint). Against the five columns:

- **in work** reads off *in-work*. Clean.
- **awaiting validation** and **ready** both read off *queued*. The queue records nothing about a
  statement's validation, so the two columns are indistinguishable at the source. Nothing in
  R309.26–33 says the pass is written down anywhere at all.
- **waiting on the person** reads off nothing. *deferred* is "parked on a named revisit trigger" and
  the trigger is any outside event — a released dependency, a date — not necessarily the person, so
  *deferred* is a superset with no way to sieve the person's share out of it. The waiting board
  `WAITING.md` does hold what waits on the person, but it holds *items* — a parked question, an
  unread answer (R237.1) — not queue rows, and no clause links an item to a row.
- **done** has no source at all; see K3.

So the fix has to be stated, and the spec states neither of the two available shapes. Either **a new
recorded state goes on the row**, which opens the closed vocabulary and reaches
`docs/roadmap-format.md` §The status vocabulary, the `ROADMAP.md` preamble, and the row lint that
reds a status outside the closed set (§The row lint) — the honest cost, and the shape I recommend for
awaiting-validation-versus-ready, since one recorded word is then held by a gate. Or **a column is
derived from two sources**, and then the second source must be named: the statement's validation
record for ready, and a row-to-item link for waiting on the person. R309.19 as written promises the
first shape and the product can only deliver the second, and R309.19 is the clause that owns saying
which.

`defect · high · unstated-source`

---

K3 — The done column's source does not exist in the queue

> "The system *shall* keep every closed task's row on the work board rather than clear it." — R309.42

A closed row does not stay in `ROADMAP.md`. The live-body law moves it to the dated archive under
`docs/queue-archive/` in the same commit that closes it, carried verbatim
(`docs/roadmap-format.md` §The live-body law; R5.1 [INV-276]). R309.19 reads a column off "the state
its queue row records" and a done row has no queue row; R309.20 reaches only open rows; R309.42 keeps
the closed row on the board and names no source it is kept from.

Two further facts the done column silently collapses. The archive's terminal vocabulary is four
words — *landed*, *declined*, *superseded*, *decided* — and that sentence is their one home. A
declined row is not done, and a superseded row is not done either; one column takes all four and the
spec never says it does. And R309.43's door tag is read "from the queue row's own intake note", which
for a closed row means the archived row's intake note, not the live body's.

The fix belongs on R309.42: name the queue archive as the done column's source, say which terminal
exits stand in it, and re-point R309.43's "queue row" at the archived row. Round 1's F3 settled where
a closed row's *per-step* facts come from (the delivery report); it did not settle where the row
itself comes from, because until this widening the board carried no column that had to find it.

`defect · high · unstated-source`

---

K4 — The board shows the far tier standing, where the law shows it only on request

> "The system *shall* collapse the far tail past the runnable head into a stated count, and *shall*
> never drop it in silence." — R309.21

R5.5 is explicit: when the runnable report is produced, the system stands the far tier down by name
and shows it **only on the person's request**. R94.3 repeats it for the what's-left report and the
feature-map answer, and R94.4 reds the report-shape check when a report names a far-tier row among
the runnable what's-left. The work board is a standing page that holds whether or not anyone asks
(R309.14), so a far-tier count printed on it is shown without a request every moment of the day.

R309.21 carries [INV-222] as its anchor — the invariant this criterion is closest to breaking — and
an anchor is not a reconciliation. R309.20 makes it worse by demanding every open queue row, dropping
none, which reaches the far rows by name.

Two lawful shapes, and the spec should pick one out loud. Either the far tier's one line on the board
is the same stand-down line R5.5 already permits, and R309.21 says so by citing it — a count and the
tier's name, no rows, and the rows open on the person's act — or the board is declared not a runnable
report and R5.5's fence is stated as not reaching it, which I do not recommend, since a standing page
answering "what is left" is the runnable report in every sense but its name.

`defect · high · invariant-broken`

---

K5 — The plan the board must show has no recorded home

> "The system *shall* show an in-work row's plan on its board row." — R309.24

R309.26 gives every task a statement carrying its name, description, plan and estimate; R309.27 has
the plan list the steps ahead in run order; R309.34 freezes the wording. No clause says where any of
it is written down. The roadmap row is exactly five cells — id, wish, class, status, acceptance
(`docs/roadmap-format.md` §The roadmap row) — and the wish cell's intake notes carry the door, the
kind, the footprint, the map placement and an entry condition. There is no plan cell and no statement
file.

Round 1 recorded this as an assumption rather than a finding ("I found no authoritative surface for a
task's frozen statement named in this document"), which was right then: nothing yet read the
statement. This widening makes it load-bearing — R309.24 and R309.25 have the board read the plan on
every in-work row, and a fact with no home cannot be read. R309.26 is the clause that owns the fix:
name the statement's home, and say whether the roadmap row gains a cell or the statement is a file
the row points at.

`defect · high · unstated-source`

---

K6 — The craft name has no assignment point and no record

> "The system *shall* name the worker on each running step by a fixed craft name and icon." — R309.47

R309.51 says a step whose record names no craft shows its craft unnamed — so a step record is assumed
to exist and to have a craft field, and neither is anywhere declared. The only per-step record the
spec carries is the delivery report's per-step trail (R309.44), which holds "each step's outcome, the
worker tier or role that ran it, and the step's share of the task's time" — a *role*, not a craft
name, and the delivery report is written at the close, so it cannot feed a step that is running now.
The worker brief is the one artifact present at spawn, and the spec has it name the worker's files
(R207.1 [INV-10]) and its branch (R91.1 note), never a craft.

So the mapping the widening depends on — craft name to brief's role — has no author, no moment, and
no home. The fix is one criterion, and it should say all three: the seat assigns the craft name in
the worker's brief at spawn, the worker's checkpoint under `.live-spec/checkpoints/` (R206.4
[INV-69, ACT-3]) carries craft, icon and tier while the step runs, and the board reads it there. K10
needs the same sentence, so one clause closes both.

`defect · high · unstated-source`

---

K7 — The parallel mark claims what the take-time graph decides

> "The system *shall* have the plan mark which steps can run in parallel, within the lane cap and the
> economy ladder's rung." — R309.28

The independence graph is the authority the pack already has, and it sits somewhere else. It is built
at queue-take over the runnable head (R82.1 [INV-49]), it draws edges only on true dependency or
same-section collision (R82.1, R82.2), lanes open on a pairwise-independent set up to the cap
(R82.3, R80.1 [T-18]), and false serialization is held to the seat's read rather than a gate
(R82.4). The plan's mark is written earlier — the statement is validated before the task enters work
(R309.30) — so the mark is a prediction made before the graph that decides has been built.

The freeze then removes the correction path. R309.34 freezes the statement's wording and R309.35
holds it at take-up, along the way and at the close; R309.37 permits a revision only of the
*estimate*, and only before take-up. A frozen parallel mark the take-time graph contradicts has no
clause to reconcile it, and the criterion as written reads as a commitment rather than an
expectation.

Two repairs, and both are wanted. Say the mark is the plan's expectation and the queue-take graph
decides at take, R309.28 citing R82.1 — the answer to the question this check was set. And fix the
cap it names: the lane cap counts build lanes across *rows* in-work at once (R80.1), not steps inside
one task, so "within the lane cap" is a category slip unless the spec means the two to be one cap, in
which case it must say so. The economy ladder's rung (T-19) governs which tier a step rides, not how
many run together, so it caps nothing here either. Nothing in the pack currently caps intra-task step
parallelism, and this criterion should either name the cap or state that the seat holds it.

`defect · authority-mismatch`

---

K8 — "Plan" names two different step lists in adjacent criteria

R309.27's plan is the task's own steps in the order they run — free-form, one per task. R309.25 then
marks "the one pipeline step of the nine the row now sits at" *on that plan*, and the nine are the
fixed pack stations named once at R15.4 [INV-27]: spec, prove, architecture, prove
architecture, matrix, test, code, verify, commit-and-show.

If the plan is the nine, R309.27's ordering clause is vacuous, since the nine already run in fixed
order. If it is not the nine, the nine-step marker sits on a list that has no such steps. R309.44's
per-step trail inherits the ambiguity a third time — a trail step is a step of which list?

One sentence settles it. My reading of the person's word is that the plan is the task's own steps and
the pipeline station is a separate mark on the row, not on the plan; if so, R309.25 should read
"beside that plan" and say the station is read from the nine.

`defect · ambiguous-scope`

---

K9 — The five starter crafts are a third vocabulary for the acting role

> "The system *shall* take the starter crafts as the Reader, the Drafter, the Reviewer, the Builder,
> and the Checker." — R309.49 [default]

The product already names the acting role twice. R2.1 [E-12] names five roles — an analyst, an
architect, a design reviewer, a tester, a project manager. R51.1 [INV-33] names seven craft standards
— a strong product manager, a software architect, a quality-assurance automation engineer, a senior
developer, the prover's formal-reviewer role, a careful release engineer, the visitor's outside eyes.
R309.47 anchors [INV-33] as though the third list were the second, and it is not: no member maps
cleanly, and "Reviewer" now names both the design reviewer of R2.1 and something new, which is the
two-name drift the one-name law [INV-255] exists to catch.

The tag is `[default]`, so the value is retunable and the finding is not that the names are wrong.
The finding is that a third closed list arrives with no map to the two standing ones. Either the
starter crafts are taken from R51.1's list — the fix I recommend, since [INV-33] is already the
anchor — or R309.49 carries the map, one line, craft to role.

`defect · one-name`

---

K10 — The tier note has no source the board can read while the step runs

R309.48 stands a muted note of the worker's tier beside the craft name. Tier does have a home: the
routing rule logs one line — proposed tier, chosen tier, and why — on the checkpoint and the delivery
report (R208.5 [INV-69, D-2]). Neither serves a running step as the spec now stands. The delivery
report is written at the close. The checkpoint lives under `.live-spec/checkpoints/`, kept out of git
and off the temporary directory (R206.4), while the board's own file rides inside the landing
commit (R309.56) — so the board would read a running fact from a file the commit never carries, and
no criterion says it may.

There is also a moving-value question: R208.6 keeps the assignment-time override distinct from the
failed-acceptance escalation, both logged, so a step's tier can change mid-flight. R309.48 should say
the note follows the chosen tier as logged, not the tier proposed at spawn. The clause that closes K6
should name the checkpoint as the running step's record and this finding closes with it.

`defect · unstated-source`

---

K11 — The icon is called fixed and no clause says where the fixed set lives

R309.47 requires a fixed craft name **and icon**; R309.50 holds a worker's identity at its craft name,
its icon and its tier note. R309.49's `[default]` names five crafts and no icons. Nothing says whether
the icon set lives in the frozen norm under `docs/norms/` (R309.15 [INV-43]), in the generator, or in
a settings-ladder value. A thing called fixed with no home is not fixed, and two sessions will pick
two icons for the Reader.

The word **icon** is also a new domain noun with no glossary entry, which the vocabulary check reads
(`docs/spec-format.md` line 70: every domain noun in the text has its glossary entry); the **work
board** entry at glossary line 263 mentions neither icons nor columns.

`defect · unstated-source`

---

K12 — The waiting column re-opens the settlement that gave every waiting item one home

Round 1's F2 was folded by R309.17: the work board's waiting region renders `WAITING.md` and keeps no
list of its own, "so one clearing rule and one gate hold every waiting item". R309.18 now puts a
second waiting set on the same page — a column of queue rows waiting on the person — and it inherits
neither the clearing rule (an item clears on the person's acknowledgement alone, R237.1) nor the gate.

So the page carries two things called waiting that are different objects with different lifecycles,
which is the one-name problem [INV-255] and the surface-authority problem F2 already answered once.
The clean shape, if the column stays: state that the column is a *view* of rows whose waiting item
lives in `WAITING.md`, so the item is still the one object and the row is a pointer at it. That also
supplies the missing source K2 names for this column, so the two findings close together.

`defect · duplicate-home`

---

K13 — "The far tail past the runnable head" names three different sets

The phrase in R309.21 and in the new Context sentence could mean the *queued* rows standing below the
head, or the *far*-status rows (glossary **far tier**, line 92), or the *deferred* rows that are in
neither. The anchor [INV-222] points at the far tier alone, and the glossary carries **far tier** and
**queue-take** (line 187) but no entry for a far tail or a runnable head as a bounded set. Whoever
builds this collapses a set nobody has named. One glossary entry, or a rewrite naming the recorded
state, closes it — and it must agree with whatever K4 settles.

`defect · vocabulary`

---

K14 — R309.52 states a deed with no measure and no judge

> "The system *shall* keep which worker runs which task readable at one glance across the whole
> in-work column." — R309.52

No reader is named, no question is named, no threshold is named. The requirement's own working
measure (R309.66) asks three questions over one real working stretch — what is now being done, what
was done, and how long each took against its estimate — and none of them is who is running it. So the
one criterion that would falsify R309.52 does not ask its question.

Either fold a fourth question into R309.66 — who is running each thing in hand — which is the cheaper
fix and keeps one measure for the surface, or give R309.52 its own reader and question. By the pack's
own rule a criterion that states a behaviour and leaves its judge or its measure unstated carries a
`[GAP: ]` line rather than standing bare (spec preamble, line 7).

`defect · unmeasurable`

---

K15 — The new Context sentence contradicts itself in one line

> "The page carries the whole queue, not the work in hand alone: every open row stands in one column
> named for its state, and the far tail past the runnable head collapses to a count." — Context, line
> 7637

Three breaks in one sentence. The columns are not named for states — awaiting validation, ready,
waiting on the person and done are none of the four recorded words (K2). "Every open row" cannot
reach the done column, whose rows are closed (K3). And a row in the collapsed tail stands in no
column, against the same sentence's own "every open row stands in one column" and against R309.19 and
R309.20 (K4).

The Context is the passage a reader meets first, so it should be rewritten last, after K1 to K4 are
settled, and then say only what those settle.

`defect · contradiction (internal)`

---

K16 — "kanban" enters the heading with no glossary entry and a plain phrase available

The heading now reads "The work board shows the whole queue as a kanban". Two checks were asked and
both are answered. The word is **not** banned: `guardrails/spec-coinages.json` holds no entry for it
(its list retires coined and machine words — needle, utilize, functionality), and
`guardrails/one-name-aliases.json` holds no group naming it an alias. But the closed-vocabulary law
does reach it: every domain noun in the text has its glossary entry (`docs/spec-format.md` line 70,
inherited by every family member), and the glossary has no **kanban** entry, while the **work board**
entry (line 263) describes a standing page and never mentions columns at all.

So as it stands the heading carries an industry term the document never defines, where the plain
phrase the criteria already use — the whole queue in columns, one column per state — says the same
thing in the register the pack holds. Note that kanban *is* the person's own word (ROADMAP row 166's
fourth widening quotes him: "the board is a kanban over the whole queue"), and the queue row is the
right home for it, since the row records provenance. My recommendation: retitle to the plain phrase,
extend the **work board** glossary entry with the columns, and leave kanban standing in the queue
row's provenance where his word is quoted.

`defect · vocabulary`

---

K17 — R309.21's `[default]` names no retunable value

The marker "names a value the agent set that the human may retune" (spec preamble, line 7). Its three
neighbours obey: R309.18 lists the five columns, R309.43 names the alternative work-kind axis,
R309.49 lists the five crafts, R309.57 names five seconds and its watcher. R309.21 names nothing —
not a row count for the head, not a threshold, not an alternative. Either name the value the person
would turn (how many rows stand at the head before the tail collapses) or drop the tag.

Checked and clean on the other two new tags: R309.18's column list and R309.49's craft list are both
genuine retunable values with the value stated.

`recommendation`

---

K18 — R309.20 is entailed by its two neighbours and contradicted by the third

R309.18 gives one column per state and R309.19 stands every open row in exactly one of them, which
already means no open row is dropped. R309.21 then drops the far tail into a count, which is the one
exception. As written R309.20 is redundant against the pair and false against the third. Consider
folding "dropping none" into R309.19 and letting R309.21 stand as the single stated exception, once
K4 settles what that exception may show.

`recommendation`

## Cross-checks run and clean

Recorded because a reader would expect the widening to break them, and it does not.

- **R309.22 against R309.46** — the parked row's column and the parked row's mark. R309.22 places a
  parked row in the in-work column and explicitly leaves the mark to R309.46, which keeps the row
  marked parked and names the row that preempted it. One fact, one home, no duplication. This also
  agrees with the queue: a parked row's recorded status stays *in-work* under the open-leg law
  (`docs/roadmap-format.md` §The status vocabulary).
- **R309.23's placement tag** — the tag names the feature or the several modules the row reaches, and
  it is read from the queue row's own map and footprint notes, both of which the wish cell's intake
  notes really carry (`docs/roadmap-format.md` §The roadmap row). A source that exists — the only new
  read in this widening that has one.
- **Actor and deed** — every new criterion names the system as its actor and states a deed, except
  R309.52, whose deed is unmeasurable (K14).
- **Duplicated facts against round 1** — none found between the new criteria and R309.1–17, 26–46,
  53–66 beyond the two the findings above name (K12's waiting home against R309.17, K3's closed-row
  source against R309.42).
- **R309.19's in-work column against the lane cap** — up to three rows may read *in-work* at once
  (lane cap, package default three, `docs/roadmap-format.md` §What the roadmap is; R80.1), so an
  in-work column holding several rows is lawful and no criterion contradicts the cap.

## Verdict

Six high defects and twelve findings below them. The widening's shape is right and its sources are
not: five of the six high defects are one class — a column or a mark the board must read off a fact
the product does not record anywhere (K2 the three column states, K3 the closed row, K5 the plan, K6
the craft name, with K10 and K12 the same class one rung down). K1 and K4 are the two places the new
columns cross a standing law: the Context's validation gate, and the far tier's request-gate.

Needs another iteration before the architecture step. Settle K1 first, since how much of the queue
the board answers for decides K2, K3 and K4; then one criterion naming the running step's record
closes K6, K10 and K11 together.
