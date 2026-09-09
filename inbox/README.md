# inbox — parallel-safe intake for wishes and feedback

The one door into this repo for a session NOT assigned to live-spec itself (a host's adopt run, any passing
conversation). Such a session may do exactly one thing here: **create one NEW file per item** — a wish or a
piece of feedback. It never edits
the spec, the queue, the journal, the skills — and never an existing inbox file (SPEC INV-10).

Why a folder of files: creating a fresh file cannot collide with anyone; editing a shared file can.

**Format:** `YYYY-MM-DD-<source>-<slug>.md` (name taken? append `-2`, `-3`, … — the pack's one collision law, base rule 18; two sessions racing one slug: add a short session token to the source mark) — a few plain lines:
- the item, in plain words (a wish, a reaction, an answer, a report)
- why (what broke / what was missing, with the primary source if there is one)
- who threw it (which host / which conversation)

**Whose the item is lives in the filename.** The `<source>` segment above is that fact's one home. An
agent's own message names its source `from-<agent>`, so a message from track-coach is
`2026-07-17-from-track-coach-<slug>.md` — the form every agent deposit here has carried since 2026-07-10.
The body's "who threw it" line above is a different fact and keeps its own home: the filename says whose
the item is, and the body says which window and which conversation put it on disk. The two differ every
time an agent relays something that is not its own.

Two source words are reserved for items that arrive with their own authority, and each owes nothing
further:

- **`from-owner`** — a wish carrying the owner's authority, whoever types the file. An agent relaying his
  word names the file `from-owner-<slug>` and names its own window in the body's "who threw it" line:
  relaying changes a message's carrier and leaves its authority exactly where it started, so a relayed
  wish is his and stands as an instruction (SPEC INV-193). An agent's OWN proposal never takes this word;
  that is the laundering the same law refuses. The reserved word is the role, because a shipped file names
  no person (SPEC INV-120).
- **`stranger-<kind>-<number>-<slug>.md`** — a bridged Issue, whose door is the wish template (SPEC
  INV-146). The monitor stamps no date on these, so this one form stands outside the dated shape above.

A deposit whose source carries no `from-` prefix stands outside agent traffic, and it is read as an
ordinary wish.

**An agent's message names its birth, inside the file (SPEC INV-189).** A message is born of the sender's
own work, and it says which of the two births it carries. A message that can name neither is never sent,
and one that arrives is declined at the door, so no human reads it. Curiosity, tidiness, and the thought
that a neighbour might want to know each describe a message the sender's own work does not need.

A message **blocked by this zone** names the work standing still: a real row, a real failing step, a real
thing the sender cannot finish while this zone stands as it does.

```
Blocked: <the work of mine that stands until this is answered>
Need-by: <a date, or none>
Id: <a stable identifier this message's reply can name>
```

A message **carrying a lived fault** names the fault and the evidence the sender lived: what it ran, what
happened, and how the fault showed itself. Nothing of the sender's need stand still for this birth — the
value is the outside view, which this zone's own instruments cannot take.

```
Lived: <the fault I hit in your zone, and the evidence I hold: what ran, what happened, how it showed>
Need-by: <a date, or none>
Id: <a stable identifier this message's reply can name>
```

The two births are named apart because they owe different things: the blocked message owes the work
standing still, and the fault message owes the evidence. A rule demanding blocked work of both would
refuse the fault message, which is the message a neighbour most wants.

**A letter's own state lives in a `Status:` line (PLAN q-835).** A letter's position in this folder used
to be the only fact a reader could check: open under `inbox/`, done under `inbox/handled/`. That fact
alone says nothing about a letter a session read and set aside, and nothing about a letter a later letter
replaced. A letter that carries no `Status:` line still reads by where it sits — open in the folder,
handled in `handled/` — so every letter already on this record reads unchanged. A letter that does carry
the line names one of four words, and a superseded letter also names the letter that replaced it:

```
Status: open | handled | noted | superseded
Superseded-by: <the filename of the letter that replaced this one>
```

`open` is a letter nobody has acted on. `handled` is a letter a session turned into a row, or otherwise
finished with. `noted` is a letter a session read and decided owns no row. `superseded` is a letter a
later letter replaced; it carries `Superseded-by:` naming that later letter, and a letter that names none,
or names a file that is not on disk, is refused rather than guessed at. `scripts/inbox_lifecycle.py` is
the one reader of this line — `scripts/state-probe.sh`'s INBOX section and a row's own admission both read
a letter's state through it, and neither keeps a second copy of the four words.

**A reply names the message it discharges (SPEC INV-192).** A reply travels the sender's own inbox and
owes no blocked work of its own: the message it answers already named the blocked work that earned the
exchange, so the reply names that message's identifier and states where the message ended.

```
Re: <the identifier of the message this answers>
Terminal state: <delivered, or declined naming the zone that owns the question>
```

**What the gate reads.** `guardrails/check-earned-message.py` (gate m of the pre-push hook) reads every
deposit in this folder, whatever its extension, with one exception: a name ending `.draft` is a deposit
still being written (SPEC INV-249), so the gate passes over it exactly as the receiving sweep does, and a
mid-write deposit reds no push. It treats one whose filename names an unreserved
`from-<agent>` source as agent traffic, and one carrying the agent card's `From: <name> (agent)` line the
same way whatever its filename. It reds when such a deposit names neither birth: no `Blocked:` line, no
`Lived:` line, and no `Re:` line naming a message it replies to. A field inside a fenced code block is an
example, and the gate reads past it. `Need-by` and `Id` are read and reported, and the exit code stays
with INV-189: an expired need-by escalates through the sender's own status report, which is the road
INV-192 gives it.

The gate reads a field that was forgotten. Three things stay past its reach, and each stays with this
sweep and the prover (SPEC INV-150): whether the named work stands still, whether the named evidence was
lived, and whether a deposit that declares no source at all is agent traffic — a sender who names the file
without the `from-` prefix and writes no marker is not read by the gate at all.

**A deposit is written whole before it is named (SPEC INV-249).** Writing a file's content takes many small
writes, so a sweep reading this folder while a neighbour is mid-write can harvest or delete a half-written file — a
live sweep once truncated a deposit mid-write. So a deposit is first written under a `.draft` name
(`YYYY-MM-DD-<source>-<slug>.md.draft`) and renamed to its final `from-...md` name only once its content is
complete; a rename within one filesystem is atomic, so the final name appears whole or never appears at all.
The receiving sweep acts only on a complete deposit and passes over any name still carrying the `.draft`
suffix, and it never deletes or edits a file that may be mid-write. A deposit already routed is left earned
in place rather than removed under a live writer, the same care the resume re-read gives a queued item it
finds already handled (SPEC INV-247).

Two edges the `.draft` name carries. **The name-taken check reads the `.draft` names too.** While a deposit
is in flight only its `.draft` name exists, so a second writer asking "is `<name>.md` taken?" would see
nothing and clobber the first writer's draft; so the collision check (base rule 18, the `-2`/`-3` rule
above) scans the `.draft` names as well, and two co-located windows writing at once each carry the short
session token in the source mark so their names cannot collide. **A stale `.draft` is reaped.** A `.draft`
a writer left behind after it stopped, still present with an unchanged modification time across a full
sweep, is stale, and the sweep removes it the way it removes a harvested file, so an abandoned draft never
lingers forever.

**From the same filesystem (a co-located window), the deposit is the file alone (SPEC INV-174).** You
share the assigned session's working tree and git index, so stop after writing the file: no staging, no
commit, no push — the assigned session's sweep commits the harvest itself, and your item is durable on
disk from the moment it is written. **From a separate clone,** commit your one new file (a commit touching
inbox/ only, message naming the source) — that commit is part of the exception. A live-spec session sweeps this folder as its first act, harvests each file into the home
its route owns (a wish into a ROADMAP row, feedback by the routing law — SPEC T-20), and removes the file
in the harvest commit (git history keeps it). An item that arrived from a stranger's Issue is answered on
that Issue too: the sweeping session posts the capture echo (heard · door · name · row) as a comment at
harvest, and the session that lands the row closes the Issue at its terminal exit — each write under the
session's own package-repo auth (SPEC INV-147).

**From a remote seat, over git.** A remote seat reaches a repo only through git, so it also pushes.
The deposit stays one new file here, committed touching inbox/ only with the source named, and then pushed
under a per-repo grant recorded in the host profile like the push grant. A seat with no grant fails honestly:
it names the grant it lacks and hands the owner the one action that supplies it (SPEC INV-112).

**From a stranger, through GitHub.** A stranger is a contributor with no push rights and no per-repo grant —
a read-only collaborator on a private repo, or anyone at all on a public one. The git deposit is closed to
them, so their door is a GitHub Issue or Discussion opened by the wish template
(`.github/ISSUE_TEMPLATE/wish.yml`, `.github/DISCUSSION_TEMPLATE/wish.yml`), which requests a source. A stranger
never writes the queue or the repo. The **monitor** bridges the gap: `scripts/stranger-wish-monitor.py` runs on
a schedule, converts each open un-surfaced Issue or Discussion into one new inbox file here (naming the source
and its origin) and commits it, then records the item's update generation on a marker comment — from that
committed file on it is an ordinary inbox wish under the sweep above. The monitor holds no verdict; whether an
item is a wish, feedback, or neither stays the inbox sweep's call (SPEC T-20). A missing source is asked for in a
comment before routing, and newer activity on a surfaced item re-surfaces it, so nothing pressed onto a closed
wish is lost (SPEC INV-146, INV-147).
