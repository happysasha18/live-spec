# Prover record — 2026-09-04 status renderer, priority order, and the feed delta

Prover skill version: product-prover v1.6.2 (the installed copy under `skills/product-prover/`), run
against `skills/product-prover-pack/SKILL.md` v6.1.0 (pack bindings) and
`skills/live-spec-base/SKILL.md`.

PUSH-REVIEW

Range: 0a90c786..56d783b4
- 56d783b4 Every skill measured by the tool with its verdict quoted, and the reading defect that pass found (PLAN q-817, q-821)
- 5436d680 A project's live numbers print beside its rows, and the cadence comes from whoever owns the fetch (PLAN q-48)
- 3c90fcc2 One status renderer for every project, and a next move derived from a written rule (PLAN q-818, q-819)
- 8fceae92 Merge branch 'lane/q818'
- 1f3a7391 wip q-818: one status renderer, its extras hook, and the drift check
- 9dc63706 Skill-creator review on record for product-prover, the one skill the 2026-09-04 pass had not reached (PLAN q-817)
- bb684786 The rulebook's readability pass, and the reviews the changed skills owe (PLAN q-817)
- d582e5bd The skill-review gate reads the tool's own verdict, and a suffixed invariant id stops being invisible
- 336a9081 Merge branch 'lane/q817'
- e71e3ed8 wip q-817 gate
- a94cea98 A correction replans work already running and opens no row (PLAN q-820)

Files read: `PRODUCT_SPEC.md` (the section map row for `spec/live-status-reporting.md`),
`spec/live-status-reporting.md` (Requirements 319, 320), `spec/success-measure-feed.md`
(Requirement 318 whole), `spec/guardrails-freshness.md` (Requirements 242, 267),
`spec/design-spec-review.md` (Requirements 54, 55 — the declared-laws home),
`PRODUCT_SPEC.index.md`, `ARCHITECTURE.index.md`, `TEST_MATRIX.index.md`,
`architecture/guardrails.md`, `architecture/pipeline-and-lanes.md`, `matrix/guardrails.md`
(M-621, M-634, M-635, M-636), `skills/live-spec-base/SKILL.md` (rule 39),
`skills/product-prover-pack/SKILL.md`, `docs/prover/README.md`,
`scaffold/status-view/state-probe.sh`, `scripts/state-probe.sh`,
`scripts/plan_checks_core.py` (`read_priority_order`, `priority_rank`),
`scripts/check-success-measure-feed.py`, `guardrails/check-status-view-drift.py`,
`guardrails/check-skill-review.sh`, `guardrails/skill_review_verdict.py`,
`guardrails/pre-push` (gate ag), `adopt/install-status-view.sh`,
`templates/PLAN.template.md`, `PLAN.md` (the priority statement),
`tests/test_status_view_drift.py`, `tests/test_status_view_install.py`.

Checks run:
- `bash guardrails/check-prover-record.sh` — FAIL before this record (the newest committed record
  predates the last `PRODUCT_SPEC.md` change); re-run after this record lands.
- `python3 guardrails/check-status-view-drift.py` (in the pack) — exit 0, printing
  `check-status-view-drift: /Users/sashaabramovich/live-spec carries no scripts/ratchet-manifest.json — nothing vendored to check`.
  Zero files compared. This is the evidence behind F1.
- `cmp scripts/state-probe.sh scaffold/status-view/state-probe.sh` — identical today; nothing in the
  tree holds it so (F1).
- `python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/product-prover-pack` —
  `Skill is valid!`, exit 0. Ran to confirm the validator's output carries no machine-local path, so
  Requirement 242 criterion 7's quote comparison is portable across machines. It is.
- `grep` sweep of `scripts/`, `scaffold/status-view/` for any hardcoded staleness bound — none found
  (the rule 39 reading below).
- No test suite run: this pass was asked not to run it.

Findings: ten, listed below. Seven are defects and block; three are recommendations and block
nothing. The full list with each finding's severity is in the `Findings:` line at the end of this
record.

---

## Opening assessment

The delta does one honest thing three times: it takes a fact that had been asserted and makes
something read the fact itself. Requirement 319 replaces a recorded hash with the two files' own
bytes. Requirement 242 replaces a hand-written verdict with the validator's own printed output, run
again at the gate. Requirement 320 replaces a hardcoded priority word with a statement the project
writes and one reader parses. That is the pack's own "no self-certification" law applied to three
places at once, and each of the three is well-shaped as a rule.

Two things need attention. First, the two new mechanical nets have no reach: the drift check in
Requirement 319 compares zero files in the pack (no manifest there) and zero files on a host (the
vendored copy cannot see a pack), so the invariant it is the net for is enforced nowhere. Second,
the delta moved three duties to the pack pole — the renderer, the printing of the feed, the reading
of the priority statement — and shipped the duty without shipping what the duty needs: the feed's
checker is not in the installer's vendor list, and the priority statement has no written form and no
seeded template. Requirements 319 and 320 leave exactly one blank between them, and it is that one.

Confidence: needs another iteration. The rules are right; the discharge is not there yet.

---

## Phase 1 — the model

**Entities.**

- *renderer* — one file, `scaffold/status-view/state-probe.sh`, with a byte-identical pack copy at
  `scripts/state-probe.sh` and a vendored copy at each host's `scripts/state-probe.sh`.
- *extras file* — a project's own `scripts/state-probe-extras.sh`, sourced by the renderer, holding
  that project's own facts.
- *ratchet manifest* — a host's `scripts/ratchet-manifest.json`, mapping a pack-relative source path
  to the host's vendored copy.
- *drift check* — `guardrails/check-status-view-drift.py`, gate ag.
- *priority statement* — a bullet in a project's own plan naming its priority words and their order.
- *priority reader* — `read_priority_order` and `priority_rank` in `scripts/plan_checks_core.py`.
- *feed* — a host's `.live-spec/success-measure-feed.json`, written by the host's own fetch tooling.
- *feed checker* — `scripts/check-success-measure-feed.py`.
- *skill-review record* — a dated file under `docs/skill-review/`, now carrying a quoted validator
  block.
- *validator* — `scripts/quick_validate.py` from the installed skill-creator skill.

**States of a host's vendored renderer copy:** *matching* (bytes equal the pack's) → *drifted* (a
local edit, or the pack moved) → back to *matching* by a `--force` re-install. The drift check is
the only stated transition-observer, and it has a third state the spec names: *unjudged*, when no
manifest exists or no pack is reachable.

**States of a feed, as the checker reads it:** *absent* · *malformed* · *empty* · *stale against a
caller's bound* · *stale against its own cadence* · *fresh, cadence stated* · *fresh, no cadence
stated* · *malformed experiment block*. One further state is reachable and unnamed: *present, with a
`stale_after_hours` that is not a positive number, read by a caller who named its own bound* (F6).

**Actors.** The pack ships the renderer, the checker and the drift check. A host writes its extras
file, its priority statement, and its fetch tooling. A session writes the skill-review record; the
gate re-runs the validator.

**What I assumed.**

- I read "the pack's own shipped status renderer" in Requirement 318 clause 10 as the same one file
  Requirement 319 declares — the copy running in whatever project it is running in — not a
  pack-resident renderer reaching into a host. If clause 10 means something narrower, F5 changes
  shape but does not go away.
- I read Requirement 320 clause 6's "tasks nobody is working yet" as excluding the in-hand mark
  (🔄). The shipped renderer reads it the other way (F3). Tell me if the sentence was meant to
  include in-hand rows and the wording is the only thing wrong.
- I read Requirement 319 clause 10's "run this check in the pack's own push gate" as a demand that
  it be wired, which it is, and not as a demand that it compare anything there. F1 is filed against
  criterion 2's missing net rather than against clause 10.
- I found no authoritative surface named in these documents for "a host's own project-shaped
  defaults" beyond `templates/PLAN.template.md` and `adopt/install-status-view.sh`. If another
  seeding home exists, F4's second half may already be answered there.

---

## Phase 2 and 3 — findings

### F1 — The byte-identity Requirement 319 states has no net in the pack, and the gate wired to guard it compares zero files there

> "The system *shall* keep `scripts/state-probe.sh`, the pack's own copy, byte-identical to `scaffold/status-view/state-probe.sh`." — Requirement 319, criterion 2

> "The system *shall* run this check in the pack's own push gate" — Requirement 319, criterion 10

The pack carries no `scripts/ratchet-manifest.json`. Gate ag therefore takes criterion 9's stand-down
on every push from this repository and prints
`check-status-view-drift: … carries no scripts/ratchet-manifest.json — nothing vendored to check`,
exit 0, having opened no file. Nothing else in the tree compares the two copies: no test asserts it,
and `tests/test_status_view_install.py` only maps the installer's source-to-destination pairs. The
two files are identical today by hand. A maintainer who edits `scripts/state-probe.sh` — the path
`CLAUDE.md` names and every session runs — re-forks the two copies, the push gate stays green, and
the next `adopt/install-status-view.sh --force` ships the other file's bytes to every host, silently
reverting the edit. That is the same fork the requirement's own context says this work exists to
close.

Requirement 55 criterion 2 ranks a law with no named net a broken invariant, and criterion 2 here is
a stated invariant whose only candidate net does not read it.

Give criterion 2 a net that reads the two files. Two options: (a) a one-line check in the pack's
push gate and one test row comparing the two paths' bytes — smallest diff, and it is the same shape
gate ag already uses; (b) give the pack its own `scripts/ratchet-manifest.json` pinning
`scaffold/status-view/state-probe.sh` so gate ag's existing loop covers it — one file, no new code,
but it makes the pack pretend to be a host. I prefer (a).

`defect · missing-rule (invariant)`

### F2 — The same gate compares zero files on a host too, so INV-325's promise is enforced nowhere in the field

> "The system *shall* … vendor it to every host `adopt/install-status-view.sh` installs" — Requirement 319, criterion 10

> "*when* a host carries no ratchet manifest, or the pack is not reachable from this machine, the system *shall* stand down with one line naming why, and *shall* exit clean." — Requirement 319, criterion 9

`guardrails/check-status-view-drift.py` locates the pack as the directory it lives in, two levels up.
In a host, that resolves to the host's own root, which carries no `VERSION` file, so the check takes
criterion 9's stand-down and exits 0. The script's own docstring says so plainly. Reaching the pack
requires `--pack-root`, and `adopt/install-status-view.sh` wires no push-gate invocation carrying
it, states no environment variable, and Requirement 319 names no way for a host to say where its
pack lives. `tests/test_status_view_drift.py` exercises the check only with an explicit `--pack-root`
fixture, so the suite never sees the path a host actually takes.

The result: a maintainer of an adopting project edits their vendored `scripts/state-probe.sh` to fix
something local. Their push gate prints the stand-down line and passes. The drift the requirement's
user story promises to red "the moment a host's copy drifts" is never observed by anyone, in any
repository. Together with F1 this is one class — a new net whose reach is zero on both poles — and
base rule 39 reads directly on it: this is machinery that serves the process rather than the work
until one of its two poles actually compares something.

Add a criterion naming how a host points the check at a pack, and have the installer write it.
Concretely: an environment variable the check already could read (`LIVE_SPEC_PACK_ROOT`, beside the
existing `--pack-root`), recorded by the installer into the host's manifest at install time — the
installer knows `$PACK_ROOT` at that moment and writes nothing of it today. Alternative: state in
Requirement 319 that a host's copy is checked at the pack's own push instead, and drop the host-side
vendoring in criterion 10 rather than shipping a gate that cannot fire. Deletion is the cheaper
repair if no host has asked for the local check.

`defect · unenforceable-promise (discharge)`

### F3 — The spec and the shipped renderer disagree on which row wins the next move

> "The system *shall* derive the next move from the stated order — among the tasks nobody is working yet, the highest-ranking one — rather than from a task's position on the page." — Requirement 320, criterion 6

The renderer does something else. `scaffold/status-view/state-probe.sh` reads
`next_task = buckets["🔄"][0] if buckets["🔄"] else (buckets["⬜"][0] if buckets["⬜"] else None)` —
the first in-hand row wins whenever one exists, and only an empty in-hand bucket lets a queued row
win. An in-hand row is precisely a task somebody *is* working. Under criterion 6 as written, the
in-hand bucket should not be a candidate at all; under the code, a queued `critical` row never
outranks an in-hand `normal` row.

The person reading the list is the one affected: they ask "why is this row next" — the question the
requirement's user story names — and criterion 6 gives one answer while the printed line gives
another. Requirement 320 also leaves two of the six marks unanswered: a blocked row (⛔) and a
needs-eyes row (👁️) are both "nobody is working yet", and the code excludes blocked with a stated
reason ("a blocked task can't be advanced without clearing its outside cause first") that no
criterion carries.

INV-144 puts the spec as the definition of correct here, so this is a decision, not a silent rewrite.
Decide which behaviour is wanted and write it: (a) keep the code's behaviour and rewrite criterion 6
to say the in-hand row leads and the queue follows, each ranked inside its own group — my preference,
because it is what the printed list has meant for a while and it matches the Канон's own reading;
(b) keep criterion 6's words and change the code so the highest-ranking free row wins outright. Either
way, add a criterion naming where ⛔ and 👁️ rows stand in the candidate set.

`defect · direct-contradiction (contradiction)`

### F4 — Requirement 320 puts a statement in every host's plan without stating its written form or shipping a place to write it

> "The system *shall* have a project state, in one place in its own plan, the priority words it uses, the order those words rank in, and what each word means in that project's own terms." — Requirement 320, criterion 1

> "*when* a plan states no such list, the system *shall* invent no order — it *shall* keep the plan's own order and *shall* say in the printed list that the statement is missing." — Requirement 320, criterion 5

The one reader parses a very particular shape: a top-level bullet whose line starts `- **Priority**`,
followed by indented lines matching `^\s+\d+\.\s+\`([a-z][a-z0-9-]*)\`` — a numbered list of
backticked lowercase words. No criterion in Requirement 320 states any of that.
`templates/PLAN.template.md` carries no such bullet, and `adopt/install-status-view.sh` seeds none.
This pack's own `PLAN.md` has it, hand-written.

So every project that adopts the status view gets Requirement 319's one renderer, which then prints
criterion 5's "the statement is missing" line on every run, permanently, with nothing shipped telling
the maintainer what to write or where. They read a nag they cannot clear except by reading the
parser's regex. That is the one blank between Requirements 319 and 320: 319 ships a generic renderer
to every host, 320 makes that renderer demand a host-authored statement, and neither states the
statement's form nor seeds it.

This pack has already decided this question for a sibling case, in the same spec file and immediately
above Requirement 319: the wired-hook declaration must "state each hook's surface and command form …
so a host wiring one reads them" (Requirement 311, criterion 4). Apply the same answer here. Add a criterion to Requirement 320 stating the statement's
written form, and have `templates/PLAN.template.md` carry a seeded two-word statement the same way
`adopt/install-status-view.sh` already seeds an empty extras file.

`defect · missing-prerequisite (precondition)`

### F5 — Requirement 318 clause 10 moved the printing to the pack pole but the installer does not ship what the printing reads

> "The system *shall* have the pack's own shipped status renderer print a checked feed's numbers, its experiment where one is carried, and the fetch's own source, beside a project's rows and without a person going to look." — Requirement 318, criterion 10 (was: "leave a host's own status view printing … to each host")

The renderer's feed block is guarded by `[ -f "$FEED" ] && [ -f "$CHECKER" ]`, where `$CHECKER` is
`$REPO/scripts/check-success-measure-feed.py`. `adopt/install-status-view.sh`'s `VENDOR` array carries
four files plus the drift check, and `scripts/check-success-measure-feed.py` is not among them. No
other installer vendors it.

A maintainer of an adopting project writes their fetch tooling against the contract Requirement 318
promises, drops a well-formed feed at `.live-spec/success-measure-feed.json`, runs the probe, and
sees nothing. No section, no error, no line saying why — indistinguishable from criterion 12's
"a project carries no feed, print no such section". They have no way to tell a missing checker from
a missing feed, and the pack-pole promise clause 10 makes discharges for exactly one project: this
one, which happens to hold the checker at that path already.

Clause 10 moved the *print* across the pole and left the *reader the print needs* on the far side.
Two fixes, and both are wanted: add `scripts/check-success-measure-feed.py` to the installer's
`VENDOR` array and to the manifest it pins, and add a criterion to Requirement 318 saying a feed
present with no checker reachable prints one line naming that, rather than falling into clause 12's
silence.

`defect · unenforceable-promise (discharge)`

### F6 — A `stale_after_hours` that is not a positive number has no stated answer, and the shipped checker reads it on only one of its two paths

> "The system *shall* let a feed carry `stale_after_hours`, a positive number naming the refresh cadence…" — Requirement 318, criterion 2a

Criterion 2a describes the well-formed value. Criteria 6a and 6b answer two states — the feed states
a cadence, the feed states none. The third state is reachable and unanswered: the feed states
`stale_after_hours` as zero, a negative number, a string, or `true`. Criterion 7 enumerates the
malformed shapes the checker reds on and names only the experiment block.

The shipped checker does answer it — it reds `must be a positive number` — but only inside the
`from-feed` branch. A caller that names its own numeric bound never looks at the field at all, so a
feed carrying `"stale_after_hours": -5` passes the check clean, and a later run of the same feed
through `from-feed` reds on the same bytes. Two callers, one feed, two verdicts.

Add a criterion under "the checker reds on a skipped or empty fetch": a feed carrying
`stale_after_hours` that is not a positive number is malformed and reds, whatever bound the caller
passed. That both writes down the behaviour the code already has and makes it uniform across the two
caller paths.

`defect · missing-scenario (state-space)`

### F7 — Two clauses claim the same fixed place in the printed list without an order between them

> "…sourced near the renderer's end under that file's own heading" / "at one fixed place — after the plan block and before the alarm block" — Requirement 319, context and criterion 3

> "…beside a project's rows and without a person going to look" — Requirement 318, criterion 10

Both sections land in the same window: the shipped renderer sources the extras file, then prints the
`SINCE IT SHIPPED` feed block, then the alarm block. Criterion 3 calls its window "one fixed place",
which now holds two things, and nothing says which comes first. One shared renderer file makes the
order de facto fixed today, so nothing misbehaves — but a reader of Requirement 319 alone would place
the extras section immediately before the alarm, which is not where it is.

Say it once: extend criterion 3 to name the feed section as the thing standing between the extras
hook and the alarm block. One clause, and the window stops reading as exclusive.

`recommendation · boundary-issue (composition)`

### F8 — Requirement 242 rests criterion 6 on a term the spec uses once and never defines

> "The system *shall* require a directly-covering record to carry, besides the marker, the skill name, and the verdict, a block quoting the validator's own command and everything it printed…" — Requirement 242, criterion 6

"Directly-covering" appears exactly once in the whole spec. It is load-bearing: it decides which
records owe the quote. The gate has a second covering path — an earlier commit's record covering a
byte-identical vendor re-sync, which `guardrails/check-skill-review.sh` deliberately clears *before*
the quote check runs — and that path is what "directly" excludes. No criterion in Requirement 242
states that second path exists, so a reader cannot derive the distinction the term carries.

The re-sync carve-out itself predates this delta and is pre-existing debt, so under INV-114 it queues
rather than blocks. The undefined term is new here.

Either name the second path in a criterion of its own and let criterion 6 say it does not apply
there, or, cheaper, replace "directly-covering" with what it means: "a record found by the ordinary
search for this skill". I prefer the second — it costs one phrase and needs no new criterion.

`recommendation · over-general (abstraction)`

### F9 — Clause 11 prints a machine line where the rest of the list speaks the project's words

> "*when* the checker refuses a feed …, the system *shall* print the checker's own line in place of the numbers." — Requirement 318, criterion 11

The checker's line reads `check-success-measure-feed: FAIL stale — .live-spec/success-measure-feed.json
was generated 30.2h ago, past the 24h cadence the feed itself states`. It carries a script name and a
repository path onto the status list a person opens their day with — the surface this pack's declared
register law governs (Requirement 54 criterion 3, "the plain-language register on every human-facing
surface"). Requirement 319 criterion 4 draws a related line in the other direction: no fact naming the
pack's own files stands in the shared renderer.

This is a decided sentence, not a blank — clause 11 chose the checker's own line deliberately, and
tracing a refusal back to its checker is a real reason. So it does not rank as a missing clause under
Requirement 54. It is still the only line on the printed list written in machine words.

If you want the register held: have clause 11 print the checker's plain-language half — the reason
and the age — and drop the script prefix and the path. If you want the trace kept, say so in clause
11 as a named exemption, so the register law's sweep reads it as decided rather than as an oversight.

`recommendation · confusing-for-users (cognitive-load)`

### F10 — One renderer now serves every project on the machine, and it passes its next-move line through two fixed `/tmp` filenames

> "The system *shall* ship `scaffold/status-view/state-probe.sh` as the pack's own full renderer…" — Requirement 319, criterion 1

The renderer writes its computed next move to `/tmp/probe-next.txt` and `/tmp/probe-next-reason.txt`,
and reads them back near the end of the same script to print the `NEXT` block. Those paths are fixed
literals with no project, user or process in them, and the script `rm -f`s both at start.

Before this delta the file was one project's own script. Requirement 319 makes it the file every
adopting project runs. Two probes running at once — two sessions, two projects, the ordinary way this
owner works — race on the same two paths: one clears what the other just wrote, and the person reads
project A's next move printed under project B's rows, or reads a blank `NEXT` for a list that has one.
There is no error and no clue. On a shared machine the fixed name is also pre-creatable by another
user.

Requirement 319 says nothing about the renderer's own scratch state, which was harmless while the
renderer was one project's and is not now. Add a criterion: the renderer holds its own intermediate
state per run, not at a fixed shared path — `mktemp`, or a file under the project's own tree, or
restructure so the value never leaves the process. `mktemp` is the one-line version.

`defect · boundary-issue (composition)`

---

## Base rule 39 — the invented-number reading

Asked specifically: `stale_after_hours` was added so the pack chose no bound. That holds, and it
holds cleanly.

- Criterion 2a states the field and hands the number to the host, with the reason ("the tooling that
  writes a feed is the thing that knows how often it runs").
- Criterion 6b refuses to invent one when the feed states none — it reports the age and judges it
  against no bound. The shipped checker does exactly that.
- The renderer calls the checker as `"$CHECKER" "$FEED" from-feed`, passing the word rather than a
  literal, so no number hides at the call site.
- A grep of `scripts/` and `scaffold/status-view/` for a hardcoded staleness bound finds none. The
  number did not move somewhere else. Requirement 318's rule-39 reading is clean.

Rule 39's other half does bite this delta, in a different place. It refuses machinery built to serve
the process. Gate ag is new machinery earned by a real incident — the forked renderer, named in
Requirement 319's own context — but F1 and F2 together show its reach is zero on both poles: zero
files compared in the pack, zero on every host. Until one of those two is fixed it is a gate that
exists and catches nothing, which is the exact shape the rule refuses. The repair is the one the rule
names: make it reach, or delete it and say why.

The delta's other new things pass the rule. The extras file is a mechanism, not a threshold, and it
removes hardcoded facts rather than adding configuration. Requirement 320's priority statement
*deletes* a hardcoded word (`critical`) and puts the choice in the project's own words. Requirement
242's new criteria add no number at all.

---

## Phase 3.5 — acknowledged gaps

No explicit Open Items or TBDs in the delta. Requirement 319 criterion 9 and Requirement 242
criterion 8 are both written stand-downs — decided answers, not open items — and each names its
reason, which is the shape this pack asks for. F1 and F2 are filed against what the stand-downs leave
unenforced, not against the stand-downs themselves.

---

## Phase 4 — human and operational factors

Observability is the delta's weak point, and it is the same shape three times. F2's stand-down line
is honest but tells a host nothing they can act on. F5's missing checker produces no line at all.
F4's missing-statement line is actionable only for a reader who has the parser open. Each is a
person meeting the status view and getting less than they need to fix what it is telling them.

Domain language: F9 carries it. Nothing else in the delta leaks an internal word onto a person's
screen — Requirement 320 criterion 7's "in that project's own words" is exactly the right bar and
the renderer keeps it.

Security and privacy are out of scope for the delta except at one point, F10's fixed `/tmp`
filenames on a possibly-shared machine. That is named there rather than repeated here.

Scale: none of the new readers grows with anything unbounded. The drift check walks a manifest's
entries; the priority reader walks the plan once.

---

## Mandatory sweep verdicts

The document set under review is the delta's four requirements. The surfaces they place before a
person are the printed status list (its rows, its extras section, its `SINCE IT SHIPPED` section,
its `NEXT` line), the drift gate's push-gate output, and the skill-review gate's push-gate output.

| Surface | Declared laws | Edge-condition completeness | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| Status list — rows and NEXT | hit (F9 register, decided) | hit (F3 — ⛔ and 👁️ unanswered) | clean | clean | hit (F4) |
| Status list — extras section | clean | clean | clean | clean | hit (F7) |
| Status list — SINCE IT SHIPPED | hit (F9) | hit (F6) | clean | clean | hit (F5) |
| Drift gate output | clean | clean | clean | N/A — no lifecycle | hit (F1, F2) |
| Skill-review gate output | clean | clean | clean | N/A — no lifecycle | hit (F8) |

Class lens: swept — two classes filed. (1) *A new net with no reach*: swept both poles of gate ag and
found it vacuous on each (F1 pack pole, F2 host pole); swept the delta's other new net, Requirement
242's validator re-run, and found it does reach — it ran here and returned a real verdict, so the
class has exactly the two instances. (2) *A duty moved to the pack pole without what the duty needs*:
swept all three pole-crossings in the delta — the renderer (has what it needs), the feed printing
(F5, missing its checker), the priority reading (F4, missing its statement's form and seed).

The CRUD, invariants-per-state and authorization tables read N/A for this delta: it holds no
user-mutated persistent entities and no roles. The surface × sweep table above is this pass's
coverage artifact.

---

## Phase 5 — closing

**Top three to fix before development.** F1 and F2 together — give gate ag reach on at least one
pole, or delete it. F5 — vendor the feed checker and answer the feed-without-checker case. F3 —
decide which next-move rule is the real one and make the two agree.

**Properties to state explicitly.** Paste-ready:

- "The pack's own push gate reds when `scripts/state-probe.sh` and `scaffold/status-view/state-probe.sh`
  differ by a single byte."
- "A host's push gate names the pack it checks against, or says in one line that it is checking
  against nothing."
- "A project's priority statement is written as a `- **Priority**` bullet followed by a numbered list
  of backticked words, highest-ranking first."
- "A feed carrying `stale_after_hours` that is not a positive number is malformed, whatever bound the
  caller passed."
- "The renderer holds no intermediate state at a path shared with another project's run."

**Open questions for the author.** One only: was Requirement 320 criterion 6 meant to include the
in-hand rows, or was the renderer meant to stop preferring them? Both readings are defensible and
only the author knows which was intended (F3).

**Recommendations written into this record, blocking nothing.** F7 (the shared window between the
extras hook and the feed section), F8 ("directly-covering" left undefined), F9 (the checker's machine
line on a person's list).

**`[default]` count.** Not a FULL whole-spec pass, so no whole-document `[default]` census is owed.
The delta itself introduces no `[default]`-tagged sentence.

**Readiness.** Needs another iteration.

Findings: F1 the byte-identity in Requirement 319 criterion 2 has no net and gate ag compares zero
files in the pack (defect); F2 gate ag compares zero files on a host either, so INV-325 is enforced
nowhere (defect); F3 Requirement 320 criterion 6 and the shipped renderer disagree on which row wins
NEXT, and ⛔/👁️ are unanswered (defect); F4 Requirement 320 demands a priority statement whose written
form is stated nowhere and which no template seeds, so every host prints "the statement is missing"
permanently (defect); F5 Requirement 318 criterion 10 moved the printing to the pack pole but
`adopt/install-status-view.sh` does not vendor `scripts/check-success-measure-feed.py`, so the section
silently never prints on a host (defect); F6 a `stale_after_hours` that is not a positive number has
no stated answer and is read on only one of the checker's two paths (defect); F7 the extras hook and
the feed section claim the same "one fixed place" with no order between them (recommendation); F8
"directly-covering" is used once and never defined while a second covering path exists in the gate
(recommendation); F9 Requirement 318 criterion 11 prints a script name and a path onto the person's
status list (recommendation); F10 the one shipped renderer passes its NEXT line through fixed
`/tmp/probe-next*.txt` paths, which race across projects (defect). Base rule 39 on
`stale_after_hours`: clean — the pack chose no bound, criterion 6b refuses to invent one, the renderer
passes `from-feed` rather than a literal, and no hardcoded bound exists anywhere in `scripts/` or
`scaffold/status-view/`; rule 39's other half does bite gate ag, whose reach is zero on both poles.

Blocking: seven.
- F1 — gate ag compares zero files in the pack and criterion 2's byte-identity has no other net.
  stands: nothing in the tree reads the two files; the two copies are identical today only by hand.
- F2 — gate ag compares zero files on a host, so INV-325's promise discharges nowhere.
  stands: a host's vendored copy resolves the pack as its own root, which carries no VERSION, and no
  criterion or installer supplies a `--pack-root`.
- F3 — Requirement 320 criterion 6 and the shipped renderer name different next-move rules.
  stands: INV-144 makes this a decision the owner ratifies, and neither reading has been chosen.
- F4 — Requirement 320's statement has no written form and no seeded template.
  stands: `templates/PLAN.template.md` carries no priority bullet and `adopt/install-status-view.sh`
  seeds none, so every adopting host prints criterion 5's missing-statement line with no way to clear it.
- F5 — the feed section cannot print on any host the installer sets up.
  stands: `scripts/check-success-measure-feed.py` is absent from the installer's VENDOR array, and no
  criterion answers "feed present, checker missing".
- F6 — a `stale_after_hours` that is not a positive number has no stated answer, and only the
  `from-feed` path reads the field.
  stands: criterion 7 enumerates the malformed shapes and names only the experiment block, so the
  checker's real behaviour on a malformed cadence is written nowhere and is not uniform across the
  two caller paths. Cheapest of the seven to fold: one criterion.
- F10 — the shipped renderer's fixed `/tmp` scratch paths race across projects.
  stands: Requirement 319 states nothing about the renderer's own intermediate state, and the paths
  carry no project, user or process in them.

F7, F8 and F9 are recommendations and block nothing.
