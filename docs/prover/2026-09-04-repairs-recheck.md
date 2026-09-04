# Prover record — 2026-09-04 the six repairs, re-checked

Prover skill version: product-prover v1.6.2 (the installed copy under `skills/product-prover/`;
`SKILL.md` sha256 `5d98c4309c91`, `reference/stress-lenses.md` sha256 `422e3b9a43a9`), run against
`skills/product-prover-pack/SKILL.md` v6.1.0 (pack bindings) and `skills/live-spec-base/SKILL.md`.

PUSH-REVIEW

**Finding ids in this record.** The earlier pass's ten findings keep their own ids, `F1`–`F10`, and
are cited by them throughout. This pass's own findings are numbered `R1` onward, so the two sets
never collide inside one document. That is a deliberate departure from the prover's `F1, F2, …`
numbering, taken because this record quotes another record's findings on every page.

Range: 0a90c786..3d30e495
- 3d30e495 A test that only passed when its neighbours ran first now puts the path there itself
- dc7a9447 The resume file is refreshed for the day's five landings, and the load-weight row opens (PLAN q-822)
- e9fe5a0e Merge branch 'lane/q818-prover-fixes'
- a8c54239 Fix what the suite caught: a duplicate row id, a satisfied promise still tagged, and two checks the probe should not carry
- 523b67a1 wip: the prover's six blocking findings
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

This pass is the re-check the earlier record's repairs owe. That record,
`docs/prover/2026-09-04-status-renderer-priority-and-feed-delta.md`, covered 0a90c786..56d783b4 and
filed ten findings, seven of them blocking. The repairs landed in 523b67a1 and a8c54239 and changed
the spec again, which is why the earlier record no longer satisfies gate a. The range above is the
whole push; the reading below is the repair delta, `a8c54239..HEAD` plus the `[target]` drop that
landed in a8c54239 itself.

Files read: `docs/prover/2026-09-04-status-renderer-priority-and-feed-delta.md` (whole),
`spec/live-status-reporting.md` (Requirements 319, 320 including the new criteria 319.1a, 319.6a,
319.9a, 320.1a, 320.6a), `spec/success-measure-feed.md` (Requirement 318 whole, including 318.6c
and 318.11a), `spec/design-spec-review.md` (Requirements 76 and 102),
`architecture/guardrails.md` (the INV-324 and INV-325 entries, and the pin list),
`architecture/host-adoption.md`, `matrix/guardrails.md` (M-621, M-634, M-635, M-636),
`PRODUCT_SPEC.index.md` (the INV-21 row), `skills/live-spec-base/SKILL.md` (rules 38, 39, 40),
`skills/product-prover-pack/SKILL.md`, `skills/product-prover/SKILL.md`, `docs/prover/README.md`,
`guardrails/check-status-view-drift.py` (whole, after the repair), `guardrails/pre-push` (gate ag),
`adopt/install-status-view.sh` (whole), `scaffold/status-view/state-probe.sh` (the NEXT block, the
scratch-file block, the feed block, the extras hook), `scripts/state-probe.sh`,
`scripts/check-success-measure-feed.py`, `scripts/plan_checks_core.py`
(`read_priority_order`, `priority_rank`, `_PRIORITY_RE`, the mark table),
`templates/PLAN.template.md`, `PLAN.md` (the priority statement, the q-48 row),
`tests/test_status_view_drift.py`, `tests/test_status_view_install.py`,
`tests/test_priority_order.py`, `tests/test_success_measure_feed.py`,
`tests/test_traceability.py` (the TARGET_ROW_OWNERS map), `scripts/state-probe-extras.sh`.

Checks run:
- `git diff a8c54239..HEAD -- PRODUCT_SPEC.md spec/ guardrails/ scripts/ scaffold/ adopt/ templates/`
  and the same over `tests/` and `architecture/` — read whole, not summarized.
- `python3 guardrails/check-status-view-drift.py` (run in the pack) — exit 0, printing
  `check-status-view-drift: 1 vendored file(s) checked against /Users/sashaabramovich/live-spec — no drift`.
  One file compared, where the earlier pass measured zero. This is the evidence F1 is closed.
- The pack-pole check re-run against a **host-shaped fixture that carries its own `VERSION` file**,
  with a recorded `pack_root` and a genuinely drifted `scripts/state-probe.sh` — exit 0, printing
  `check-status-view-drift: 0 vendored file(s) checked against … — no drift`. The manifest branch is
  never reached. This is the evidence behind R1.
- The shipped renderer run against a two-row fixture (`🔁` at the highest priority word, `⬜` at the
  lowest) through the same temp-host harness `tests/test_priority_order.py` uses — `NEXT` printed the
  queued row, with the reason line `later — nothing of higher priority is free`. This is the evidence
  behind R2.
- The same renderer run against a fixture whose only open row is `🔁` — no `NEXT` block printed at
  all. This is the evidence behind R3.
- `git log --oneline -S "INV-21" -- spec/` and `git show a8c54239 -- spec/design-spec-review.md
  tests/test_traceability.py` — located the `[target]` drop and read both halves of it.
- `grep -rn "INV-21" spec/ PRODUCT_SPEC.index.md architecture/` — located the surviving clause text
  and the architecture line that contradicts it. Evidence behind R8.
- No test suite run: this pass was asked not to run it.

Findings: twelve, listed below. Eight are defects and block; four are recommendations and block
nothing. Of the earlier pass's seven blocking findings, four are closed outright, three are closed
in part. The full list with each finding's severity is in the `Findings:` line at the end.

---

## Opening assessment

The repairs are real work and most of them land. Four of the seven blocking findings are closed the
way the earlier record asked, with a criterion written and a test that reds without the fix. The
pack pole of gate ag now compares a file instead of nothing, which is the single most important
thing in the range: the gate stopped being a gate that catches nothing.

Two things need attention, and they are the two the repair narrowed. The pack-pole comparison is
narrowed correctly — the one pair it compares is the one pair criterion 2 claims byte-identity for,
and the other five entries in the vendor map are a pack file vendored to its own path, which would
compare a file with itself. The **discriminator** the narrowing rests on is the defect: "the repo
carries a `VERSION` file, so it is the pack" is false for a large class of ordinary host
repositories, and a host that carries one now has its whole manifest skipped and is told
`0 vendored file(s) checked … no drift`. F2's silence became a false green, which is worse than the
silence. The host-pole path is otherwise closed for new installs and still open for every host
installed before today, with no written migration.

The third thing is the next move. F3's `🔄` half is fixed and proven; the candidate set was narrowed
to `⬜` alone, and `🔁` fell out of it. A reopened row is a task nobody is working yet by criterion
6's own words and by rule 38's own group order, and the shipped renderer can now never pick one —
and prints "nothing of higher priority is free" while a higher-ranking free row sits one line above.

Confidence: needs another iteration. The direction is right and most of the discharge is there; four
of the twelve findings are one-sentence folds.

---

## Part A — the seven blocking findings, re-checked

### F1 — the pack pole compared zero files · **CLOSED**

Criterion 6a is written, `check-status-view-drift.py` grew its pole-1 branch, and two tests
(`test_the_packs_own_pair_reds_when_the_two_copies_differ`,
`test_the_packs_own_pair_passes_when_byte_identical`) red without the fix. Run live in this repo the
check now prints `1 vendored file(s) checked … no drift` where it printed a stand-down before. The
invariant at criterion 2 has a net that reads both files' bytes.

**On the narrowing.** The pack pole compares one pair, not the whole vendor map, and that is correct
rather than short. Of the six `VENDOR` entries only `scaffold/status-view/state-probe.sh|scripts/state-probe.sh`
has a source that differs from its destination inside the pack; the other five vendor a pack file to
its own relative path, so comparing them at the pack pole would compare a file with itself.
Criterion 2 states byte-identity for exactly that one pair. The net's reach equals the invariant's
reach, so the invariant is enforced, not narrowed. What the narrowing does leave is a maintenance
tie nobody wrote — see R11.

### F2 — the host pole compared zero files · **CLOSED IN PART, and the narrowing left a new hole**

What closed. Criterion 9a is written, `adopt/install-status-view.sh` records `manifest["pack_root"]`,
the check reads it when no `--pack-root` is given, `--pack-root` still wins, and four tests cover the
found / not-found / flag-wins / unreachable arms. For a host installed from today's installer, the
push gate finds its pack with no flag wired anywhere. That is the discharge F2 asked for.

What did not close, in two shapes.

*The old hosts.* A host installed before today carries a manifest with no `pack_root` key. The
lookup falls through to the two-levels-up default, which in a host resolves to the host's own root,
which carries no `VERSION`, so the check takes criterion 9's stand-down and exits 0 — bit for bit
the behaviour F2 filed. No criterion states the migration, and nothing in the delta tells such a
maintainer their gate is asleep. The road out exists (re-run the installer; the manifest write runs
without `--force`), so this is a hole with a written repair rather than an unenforceable promise.
It is narrower than F2 and it is the same shape.

*The discriminator.* This one is a new hole, and it is worse than what it replaced. It is R1 below.

### F3 — spec and renderer disagreed on the next move · **CLOSED IN PART**

What closed. The `🔄` half is fixed on both sides: `next_task = buckets["⬜"][0] if buckets["⬜"] else None`,
criterion 6 stands as written, and `test_a_row_in_hand_never_wins_next_over_a_higher_ranking_free_row`
reds without the change. Criterion 6a answers the blocked mark with its reason, and
`test_a_blocked_row_never_wins_next` proves it. That closes the two halves the earlier record named
as decidable.

What did not close. The earlier record asked for a criterion naming where `⛔` **and** `👁️` stand in
the candidate set. `👁️` turns out not to be this pack's vocabulary at all — the renderer's
`CATEGORY_ORDER` is `["✅", "🔄", "⛔", "🔁", "⬜"]` and `_TABLE_STATUS_MARKS` names no needs-eyes
word, so that half of F3 was reading the owner's personal `CLAUDE.md`, not this document set. The
mark that actually needed the answer is `🔁`, and it did not get one. R2 and R3 carry it.

### F4 — the priority statement had no written form and no seed · **CLOSED IN PART**

What closed. Criterion 1a states the form — a bullet beginning `- **Priority**`, its priority words
the backticked names of its indented numbered sub-items, in written order — and
`templates/PLAN.template.md` now carries a seeded two-word list under a `## Words used here`
heading. That list parses: `read_priority_order` returns `["critical", "normal"]` from it.

What did not close, in three shapes: the seeded list contradicts the template's own prose ten lines
above it (R5); an adopting host receives the renderer and the demand but not the template (R6); and
criterion 1a's "inside the plan's own 'Words used here' section" is stricter than the reader, which
matches the bullet anywhere in the file (R4).

### F5 — the feed printing had no reader on a host · **CLOSED**

`scripts/check-success-measure-feed.py` is in the installer's `VENDOR` array and in the manifest it
pins; `tests/test_status_view_install.py`'s `VENDORED` map asserts both. Criterion 11a is written,
and the renderer's guard split so a feed with no checker prints
`! a feed exists but scripts/check-success-measure-feed.py is missing — re-run adopt/install-status-view.sh to vendor it`
under the section's own heading instead of falling into clause 12's silence. Both halves the earlier
record asked for are there, and the two states — no feed, feed without reader — are now
distinguishable to the person reading the list.

### F6 — a malformed `stale_after_hours` had no stated answer and was read on one path · **CLOSED**

Criterion 6c is written in the checker's red list and says "whatever bound the caller passed". The
validation moved out of the `from-feed` arm and above both branches, so one feed now gets one verdict
from both callers, and `test_a_malformed_cadence_reds_under_a_caller_named_bound_too` reds without
the move. This was the cheapest of the seven to fold and it folded cleanly.

### F10 — the renderer's fixed `/tmp` scratch paths · **CLOSED**

Criterion 1a of Requirement 319 states the rule in the spec's own words — the renderer's
intermediate state lives "at a path unique to that run, never a fixed shared path" — and the
renderer uses `mktemp "${TMPDIR:-/tmp}/livespec-probe-next.XXXXXX"` for both files with a single
`trap … EXIT` cleaning them up. Two concurrent probes no longer share a name, and the pre-creatable
fixed name on a shared machine is gone. One residual seam the criterion does not cover is R7.

---

## Part B — the new criteria, read as a delta

### R1 — Any host that carries a `VERSION` file is read as the pack, so its whole manifest is skipped and it is told there is no drift

> "*when* the repo the check runs against carries its own `VERSION` file — it is the pack itself — the system *shall* compare `scaffold/status-view/state-probe.sh` against `scripts/state-probe.sh` directly, with no manifest needed" — Requirement 319, criterion 6a

Carrying a `VERSION` file at the repository root is an ordinary thing for a project to do; it is not
a property of this pack. The check tests exactly that and nothing else, and the pack-pole branch
returns before the manifest is ever opened. Run against a host fixture carrying `VERSION`, a
recorded `pack_root`, and a `scripts/state-probe.sh` edited to differ from the pack's, the check
prints `check-status-view-drift: 0 vendored file(s) checked against … — no drift` and exits 0.

Who is affected: the maintainer of an adopting project that versions itself. What they do: edit
their vendored `scripts/state-probe.sh`, then push. What goes wrong: gate ag skips their manifest
entirely and passes. What they see: a line that says no drift, when their copy has drifted. Before
this delta they got an honest stand-down naming why nothing was compared; now they get an assertion
that everything is fine. The same branch also returns a clean `0 … no drift` in the pack if
`scaffold/status-view/state-probe.sh` is ever deleted, since `_shipped_pairs` returns an empty list
and the count is not read.

Change the discriminator to something that names this pack rather than any versioned repository, and
make a zero-comparison never print as a pass. Three options: (a) test for the pack's own marker files
— `VERSION` **and** `scaffold/status-view/state-probe.sh` **and** `skills/live-spec-base/` — my
preference, one boolean, no new concept; (b) take the pole from an explicit flag (`--pack-pole`) that
`guardrails/pre-push` passes and nothing else does, which is unambiguous but puts the fact in two
places; (c) keep the file test but run the host branch too whenever a manifest exists, so a
versioned host is never silently skipped. Whichever is chosen, print a distinct line when zero pairs
were compared, so the vacuity F1 named can never read as a pass again.

`defect · missing-scenario (state-space)`

### R2 — A reopened row can never win the next move, and the printed reason says the opposite

> "The system *shall* derive the next move from the stated order — among the tasks nobody is working yet, the highest-ranking one" — Requirement 320, criterion 6

> "the next move is the topmost row nobody is working yet" — `skills/live-spec-base/SKILL.md`, rule 38

The renderer's candidate set is now `buckets["⬜"]` alone. A reopened row (`🔁`) keeps its own
`rank_icon` — the only remap in the classification block turns a `⛔` with no `blocked_by` into `⬜`
— so it sits in its own bucket and is never a candidate. A reopened row is a row that was done and
is done no longer because its own acceptance command stopped passing. Nobody is working it. Under
criterion 6's own words it is a candidate; under rule 38's group order it is a candidate ahead of
the whole queue.

Run against a fixture holding one `🔁` row at the plan's highest priority word and one `⬜` row at
its lowest, the renderer prints the queued row as `NEXT` with the reason line
`later — nothing of higher priority is free`. The person reading their board is told, in the plan's
own words, that nothing higher is free, while the higher-ranking free row is printed one line above
it. Criterion 7 exists to make the next move say why it is next; here it says something untrue.

Decide the candidate set once and write it. Two options: (a) add `🔁` to the candidate set ahead of
`⬜`, matching rule 38's group order and criterion 6's words, and say so in a criterion — my
preference, because rule 38 already decided this ordering and criterion 6 was written to follow it;
(b) keep the code and add a criterion excluding reopened rows with its reason, the way 6a excludes
blocked ones — but then rule 38's "topmost row nobody is working yet" is wrong as written and owes
the same edit. Either way the reason line must stop asserting that nothing higher is free when
something higher is free.

`defect · direct-contradiction (contradiction)`

### R3 — When no queued row exists, the next-move block vanishes with no line saying why

> "The system *shall* print, beside the next move, the priority word it won on, in that project's own words." — Requirement 320, criterion 7

Requirement 320 states what the next move is and how it is explained. It never states what the
printed list does when the candidate set is empty. Before this delta the case was unreachable in
practice, because an in-hand row always filled the slot. Now `next_task` is `None` whenever the `⬜`
bucket is empty, `NEXT_TITLE` reads empty, and the whole `NEXT` block is skipped.

Run against a fixture whose only open row is a reopened one, the renderer prints the row in the
`PLAN` block and then prints no `NEXT` block at all. The person opens their day on a board that
shows open work and offers no next move, with no line distinguishing "there is nothing free" from
"the block failed to render". The same holds for a board whose rows are all in hand, which is the
ordinary state while lanes run.

Add a criterion under "the next move says why it is next": when no row qualifies, the system prints
the block with one line naming that — everything open is in hand, blocked, or reopened — rather than
omitting the block. One clause, and the empty case stops being indistinguishable from a fault.

`defect · missing-scenario (state-space)`

### R4 — Criterion 1a scopes the statement to a named section, and the one reader does not

> "The system *shall* state that statement as a bullet beginning `- **Priority**` inside the plan's own \"Words used here\" section" — Requirement 320, criterion 1a

> "The system *shall* read that statement through `scripts/plan_checks_core.py` … and *shall* have no other reader decide a priority's rank." — Requirement 320, criterion 2

`read_priority_order` matches `^- \*\*Priority\*\*` against every line of the plan and stops at the
next top-level bullet or heading. It never looks for a `## Words used here` heading. A plan that
carries a `- **Priority**` bullet in some other section is out of criterion 1a and parses anyway; a
plan that carries two such bullets has the earlier one win silently, whichever section it sits in.
Nothing today writes two, so nothing misbehaves — but criterion 2 names this reader as the
statement's one machine reading, and it reads a looser shape than criterion 1a describes.

Pick one. Either drop the section clause from 1a and let the criterion state the bullet alone, which
is what is enforced — my preference, one phrase and no code — or scope the reader to the section and
say what happens to a second bullet.

`recommendation · internal-conflict (consistency)`

### R5 — The seeded template contradicts its own prose: it names `quick win` as a priority mark and then ranks it below `normal`

> "There are two marks. **critical** says the shipped product is broken for its user, and the row lands before everything else. **quick win** says the work is low effort and immediate value, free to bubble up between landings with the jump named in the row." — `templates/PLAN.template.md`, the intake-notes section

> "1. `critical` … 2. `normal` …" — `templates/PLAN.template.md`, the new "Words used here" bullet

The two passages sit ten lines apart in one file and name different vocabularies. The prose names
`critical` and `quick win`; the seeded list names `critical` and `normal` and never names
`quick win`. `priority_rank` places a word the statement does not name **last**. So a host that
follows the template's own instruction, writes `priority: quick win` in an intake note — the
template's own worked example on row 2 of its wish table does exactly that — gets that row ranked
below every `normal` row, which is the opposite of "free to bubble up between landings".

Who is affected: every project founded from this template. What they do: use the template's own
priority word. What goes wrong: the row sinks instead of rising, and the printed reason names a
priority word the list never explains. What they see: a next-move line that picks routine work over
the row the template told them would jump.

Add `quick win` to the seeded list in its stated rank — between `critical` and `normal` on the
template's own reading — or cut it from the prose above. Adding it is the smaller edit and keeps the
template's two halves saying one thing.

`defect · direct-contradiction (contradiction)`

### R6 — A project that adopts the status view still receives the demand for a priority statement and nothing that tells it the form

> "*when* a plan states no such list, the system *shall* invent no order — it *shall* keep the plan's own order and *shall* say in the printed list that the statement is missing." — Requirement 320, criterion 5

`adopt/install-status-view.sh` vendors six readers, seeds `scripts/plan_checks.py` and an empty
`scripts/state-probe-extras.sh`, and writes the manifest. It never touches the host's `PLAN.md` and
never copies `templates/PLAN.template.md`. An adopting project already has a plan of its own, so the
seeded template reaches projects founded from the template and no one else.

That leaves F4's own sentence still true for an adopting host: it gets Requirement 319's one
renderer, which prints criterion 5's missing-statement line on every run, permanently, with nothing
shipped to that host naming what to write. Criterion 1a repaired the half a reader with the pack
open needs; the half a host maintainer meets is unchanged.

Have the installer print the statement's form when the host's `PLAN.md` carries no `- **Priority**`
bullet — one `grep` and one `echo`, in the same step that already prints `seeded:` lines — or have
the renderer's own missing-statement line carry the bullet's shape instead of only naming its
absence. I prefer the renderer's line: it reaches every host on every run, including one that
adopted before today, and it costs one string.

`defect · missing-prerequisite (precondition)`

### R7 — The renderer passes load-bearing state through two exported variables across a host-authored hook

> "The system *shall* hold the renderer's own intermediate state … at a path unique to that run" — Requirement 319, criterion 1a

Criterion 1a fixed the path and left the channel unwritten. `NEXT_FILE` and `NEXT_REASON_FILE` are
exported at line 64, written by the python block, and read at line 419. Between those two points, at
line 295, the renderer sources `scripts/state-probe-extras.sh` — host-authored code running in the
same shell. A hook that sets its own `trap … EXIT` replaces the cleanup and leaks two files per run;
a hook that assigns either variable makes the `NEXT` block silently disappear. Nothing states what
the hook may touch. This pack's own extras file is clean today, so nothing misbehaves now.

Extend Requirement 319's extras clause with the hook's contract — the hook prints and reads, and
does not set traps or assign the renderer's own variables — or, cheaper and mechanical, read the two
scratch files into shell variables before the hook is sourced, so nothing the hook does can reach
them. I prefer reading them early: it needs no promise from a host.

`recommendation · boundary-issue (composition)`

### R8 — The `[target]` tag came off a clause that still promises the thing, and the architecture still says the tag is live

> "5. The system *shall* keep the success-measure reading machinery promised under its own queue row. [INV-21]" — Requirement 76, criterion 5, as it stands after the tag was removed

> "The `[target]` tag on Requirement 76's own reading-machinery clause stays live: writing the fetch tooling that fills a feed from a real analytics account is each host's own job and is unbuilt in this tree." — `architecture/guardrails.md`, the INV-324 entry

This is the caller's question, and the answer is that the promise is met in part and the drop erased
what is still owed. Three things stand against the drop.

*The clause's own sentence survived the tag.* Criterion 5 still reads "promised under its own queue
row", and q-48 — the row that held it — is closed (`PLAN.md`, `### ✅ … id: q-48`). The clause now
names a queue row that no longer exists. Requirement 102 criterion 3 is the honesty invariant in
both directions, and a clause promising something under a row nobody holds is the spec claiming what
is not built. Either the clause is rewritten to say what actually ships, or the tag belongs back on
it.

*Criterion 3 flipped and was not swept.* "keep it a written promise the human checks by eye **until
the reading machinery ships**" — the drop's own argument is that the machinery has now shipped. If
that is true, criterion 3's condition has flipped and criterion 3 was not edited. If it is false,
the tag should not have come off. The two cannot both stand.

*The architecture says the opposite, in a file written the same day.* The INV-324 entry states the
tag stays live and gives the reason. Nothing in the repair range touched it, so the pack now carries
a spec with no tag and an architecture asserting the tag is there. That is a three-source
disagreement inside two documents of one repository.

On the substance: what shipped is a feed **contract** — a checker that reds a skipped, empty, stale
or malformed feed, and a renderer that prints what the checker confirms. What Requirement 76 promises
is machinery that reads a **feature's success measure**, the sentence criterion 1 makes every
spec-delta write. No clause anywhere binds a feed metric to a spec-delta's success-measure sentence.
So the eye-check criterion 3 describes is still the only reading of a success measure this pack has;
the feed is the transport, not the reading. The fetch half being a host's own by the scope split at
Requirement 318 clauses 9 and 10 is a good reason to stop promising the fetch. It is not a reason to
stop promising the binding, which nobody has decided against.

Do one of three things, and say which. (a) Rewrite criterion 5 to name what the pack actually
undertakes — the feed contract at Requirement 318 — and rewrite criterion 3's "until the reading
machinery ships" to match; then the tag is rightly gone and the architecture line is edited with it.
My preference. (b) Put the tag back and re-own it to a live row, if the binding from a success
measure to a feed metric is still wanted. (c) Decide the binding is out of scope and write that
decision as a clause, which is the only version where deleting the promise outright is honest.
Whichever is chosen, `architecture/guardrails.md`'s INV-324 entry is edited in the same landing.

`defect · unenforceable-promise (discharge)`

### R9 — The architecture describes a one-pole drift gate and a five-file vendor list that no longer match what ships

> "The gate reads a host's `scripts/ratchet-manifest.json` and opens both the pack's file and the host's own vendored copy for every entry that resolves inside the pack … it stands down clean when a host carries no manifest or the pack is unreachable from this machine." — `architecture/guardrails.md`, the INV-325 entry

The gate now has two poles. The entry names neither the pack-pole comparison criterion 6a added nor
the recorded `pack_root` criterion 9a added, and its stand-down sentence is no longer the whole
story. `architecture/host-adoption.md` was touched in this range for a line-number refresh only.
`matrix/guardrails.md`'s M-634 narrative carries the same one-pole description.

Who is affected: the next session that reads the architecture to decide whether a change to this
gate is in scope. What goes wrong: it reads a description of the gate as it was this morning and
plans against it. This is the drift the three-source read exists to catch at entry rather than at
code.

Extend the INV-325 entry with both poles and the recorded pack root, in the same landing as the fix
for R1, since R1 changes the discriminator that entry would otherwise describe wrongly a second
time.

`defect · hard-to-operate (ops-ux)`

### R10 — Four matrix narratives do not name the six criteria added in this range

> M-634, M-635, M-621, M-636 — `matrix/guardrails.md`

The `does — / never —` narratives are the matrix's own statement of what each row proves. M-634 does
not name the pack pole or the recorded pack root; M-635 does not name the priority statement's
written form or the blocked-row exclusion; M-621 does not name the malformed-cadence red on both
caller paths; M-636 does not name the feed-without-checker line. The tests for all six exist and are
named by the right rows, so nothing is untested — the rows simply under-describe their own subject,
and the next reader deriving coverage from the matrix reads less than is there.

Extend the four narratives with the six behaviours. Mechanical, and it belongs in the same landing
as the criteria that created the gap.

`recommendation · hard-to-operate (ops-ux)`

### R11 — The pack pole's file pair is a second hand-written copy of a fact the vendor map already carries

> `_PACK_SELF_PAIR = ("scaffold/status-view/state-probe.sh", "scripts/state-probe.sh")` — `guardrails/check-status-view-drift.py`

The same pair is stated in `adopt/install-status-view.sh`'s `VENDOR` array, in
`tests/test_status_view_install.py`'s `VENDORED` map, in Requirement 319 criteria 1 and 2, and now
here. Four homes for one fact, with no sentence tying them. Today they agree. The day a second
scaffold-sourced file joins the vendor map, the pack pole silently keeps checking one pair, and the
new file's byte-identity has no net — the exact shape F1 filed, arriving by a different road.

Derive the pack pole's pairs from the shipped vendor list rather than restating it, by having the
installer's map live in one readable place both read, or add one line to the constant naming the
vendor array as its source and a test asserting the two agree. The test is the cheaper of the two
and needs no restructure.

`recommendation · boundary-issue (composition)`

### R12 — The recorded pack root is a machine-local absolute path written into a file the host commits

> "The system *shall* have `adopt/install-status-view.sh` record, under its own key in the host's manifest, the pack root it installed from" — Requirement 319, criterion 9a

`manifest["pack_root"] = pack_root` writes an absolute path from the installing machine into
`scripts/ratchet-manifest.json`, which the host commits — the check reads it at push time, so it has
to be tracked. A second person cloning that host, or the same person on a second machine, or CI,
reads a path that is not theirs. Two outcomes follow: the path does not exist, and the gate takes the
stand-down again for everyone but the installer, which is F2 returning for every collaborator; or the
path exists and holds a different checkout, and the gate compares against bytes nobody intended.

Record something portable instead, and let the absolute path stay machine-local. Options: (a) record
the pack root relative to the host root where one is a sibling of the other, and fall back to the
recorded absolute path — smallest change, covers the common layout; (b) keep the absolute path but
read an environment variable first (`LIVE_SPEC_PACK_ROOT`), which is the shape the earlier record's
F2 proposed and which every collaborator can set for themselves; (c) write the key into an untracked
local file beside the manifest. I prefer (b) with (a) behind it: the variable is per-machine by
nature, and the relative fall-back covers a checkout that sets nothing.

`defect · boundary-issue (composition)`

---

## Base rule 39 — the invented-number reading of the repair delta

Rule 39 refuses machinery that serves the process, and refuses a number pulled from the air.

The delta adds no number. Criteria 6a, 9a, 1a (both requirements), 6a of 320, 6c and 11a state
behaviour and thresholds none. `mktemp` replaced two literals with none. The seeded template list
names words, not values.

Rule 39's other half — the half the earlier record found biting gate ag — reads differently now. The
gate compared zero files on both poles then; it compares one file in the pack today, and a host's
manifest on any host that does not carry a `VERSION` file. The machinery has earned its place on the
pack pole. On the host pole its reach is real for a host installed from today's installer by the
person who installed it, and zero for three reachable cases: a host installed before today (F2's
residue), a host that carries a `VERSION` file (R1), and any collaborator on a host whose recorded
pack root is not a path on their machine (R12). Rule 39's repair reading applies to those three the
same way it applied to the whole gate before: make them reach, or say in a criterion that the host
pole is not checked and drop it. The pack pole alone would be a lawful, smaller answer.

One more rule-39 note on the new configuration. `pack_root` is a new configuration key, and rule 39
admits one on an incident that already happened — F2 is that incident, and it is on the record. The
key is earned. Its *value*, an absolute machine-local path in a tracked file, is what R12 is about,
and that is a correctness question rather than a rule-39 one.

---

## Phase 3.5 — acknowledged gaps

No explicit Open Items or TBDs in the repair delta. Criterion 9's stand-down and criterion 9a's
`--pack-root`-wins sentence are decided answers with their reasons written. F2's residue — a host
installed before today — is not acknowledged anywhere in the delta, so it is filed above rather than
here.

---

## Phase 4 — human and operational factors

Observability improved in two places and got worse in one. F5's repair replaced silence with a named
line, and F6's repair made one feed give one verdict. Against that, R1 replaced an honest stand-down
with an assertion that nothing drifted, which is the one direction observability must never move,
and R3 removed a block from the printed list without leaving a line where it stood.

Domain language: the new lines hold the register. The missing-checker warn names a script path and a
command, but it is a maintainer's line about the maintainer's own tooling, not a product string, and
it names the repair. R2's reason line is the domain-language failure in this delta and it is not a
vocabulary problem: the words are the project's own, and what they say is false.

Cognitive load: the candidate set for the next move is now decided in three places that do not
agree — rule 38's group order, criterion 6's words, and the renderer's one bucket. A person asking
"why is this row next" has three answers to choose from. R2 exists to collapse them to one.

Security and privacy: R12's absolute path in a tracked manifest leaks one machine's directory layout
into a repository that may be shared. Low severity, named once.

Scale: nothing in the delta grows with anything unbounded.

---

## Mandatory sweep verdicts

Surfaces: the printed status list (its rows and `NEXT` line, its `SINCE IT SHIPPED` section), the
drift gate's push-gate output, the installer's own output, and the seeded plan template a host reads.

| Surface | Declared laws | Edge-condition completeness | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| Status list — rows and NEXT | clean | hit (R2, R3 — the reopened mark and the empty candidate set) | clean | clean | hit (R6) |
| Status list — SINCE IT SHIPPED | clean | clean | clean | clean | clean (F5 closed it) |
| Drift gate output | hit (R1 — the net asserts a pass having compared nothing) | hit (R1, R12 — the poles' ends) | clean | N/A — no lifecycle | hit (F2 residue, R9) |
| Installer output | clean | clean | clean | N/A — no lifecycle | hit (R6, R12) |
| Seeded plan template | clean | clean | hit (R5 — two priority vocabularies in one file) | N/A — no lifecycle | hit (R4) |

Class lens: swept — three classes filed. (1) *A pole discriminator that mistakes a common property
for a unique one*: swept both new discriminators in the delta — the `VERSION`-file test (R1, hit) and
the `pack_root`-key lookup, which is keyed on a name this installer owns and so is safe (its value is
R12's subject, not its key). Two discriminators, one hit. (2) *A candidate set narrowed past the rule
it was narrowed to satisfy*: swept every mark in `CATEGORY_ORDER` against criterion 6 and rule 38 —
`✅` and `🔄` correctly out, `⛔` out with a written reason (6a), `🔁` out with no reason anywhere
(R2), and the empty-set case unwritten (R3). (3) *A repair that landed in the spec and the code and
not in the documents that describe them*: swept the four documents the delta's subjects are described
in — `architecture/guardrails.md` (hit twice, R8 and R9), `matrix/guardrails.md` (hit, R10),
`architecture/host-adoption.md` (clean, refreshed), `PRODUCT_SPEC.index.md` (clean).

The CRUD, invariants-per-state and authorization tables read N/A for this delta: it holds no
user-mutated persistent entities and no roles. The surface × sweep table above is this pass's
coverage artifact.

---

## Phase 5 — closing

**Top three to fix before this pushes.** R1 — the `VERSION`-file discriminator turns a whole class of
hosts' drift gate into a false green, which is worse than the silence it replaced. R2 — the next-move
line can print a false reason on this pack's own board today. R5 — the template shipped to repair F4
contradicts itself and ranks its own worked example last.

**Also fold in the same landing, one or two sentences each.** R3 (the empty candidate set), R6 (an
adopting host still meets the demand with no form), R8 (the `[target]` clause and criterion 3),
R9 (the architecture's two stale entries), R12 (the machine-local path).

**Properties to state explicitly.** Paste-ready:

- "The drift check names this pack by more than a `VERSION` file, and never reports a pass having
  compared zero pairs."
- "A reopened row is a candidate for the next move, ranked ahead of the queue and behind nothing but
  a blocked row's exclusion."
- "When no row qualifies as the next move, the printed list says so in one line rather than omitting
  the block."
- "A host installed before the pack recorded its root is told, in one line, that its drift gate is
  checking against nothing."
- "The plan template's priority prose and its priority list name one vocabulary."

**Open questions for the author.** Two, and only these two cannot be settled by inspection. First:
was the candidate set meant to be `⬜` alone, or `🔁` then `⬜` as rule 38's group order reads (R2)?
Second: is the binding from a feature's success-measure sentence to a feed metric still wanted, or
is the pack's undertaking now the feed contract alone (R8)? Both are decisions, not gaps.

**Recommendations written into this record, blocking nothing.** R4 (the section scope 1a states and
the reader does not), R7 (the extras hook shares the renderer's variables), R10 (four matrix
narratives), R11 (the pack pole's pair restated a fourth time).

**`[default]` count.** Not a FULL whole-spec pass, so no whole-document `[default]` census is owed.
The repair delta introduces no `[default]`-tagged sentence.

**Readiness.** Needs another iteration.

Findings: twelve. R1 any host carrying a `VERSION` file is read as the pack, its manifest skipped and
a `0 … no drift` pass printed over real drift (defect); R2 a reopened row can never win the next move
though criterion 6 and rule 38 both make it a candidate, and the printed reason claims nothing higher
is free (defect); R3 an empty candidate set drops the `NEXT` block with no line saying why (defect);
R4 criterion 1a scopes the priority bullet to a section the one reader does not look for
(recommendation); R5 `templates/PLAN.template.md` names `quick win` as a priority mark in its prose
and omits it from the seeded list, so its own worked example ranks last (defect); R6 a project
adopting the status view receives the renderer and the demand but never the template, so criterion
5's missing-statement line still has no shipped answer (defect); R7 the renderer's two scratch paths
travel as exported variables across a host-authored hook with no stated contract (recommendation);
R8 INV-21's `[target]` came off while criterion 5 still promises the machinery "under its own queue
row" whose row is closed, criterion 3's "until the reading machinery ships" was not swept, and
`architecture/guardrails.md` still states the tag is live (defect); R9 the architecture's INV-325
entry and M-634 describe a one-pole gate that no longer matches what ships (defect); R10 four matrix
narratives do not name the six new criteria (recommendation); R11 the pack pole's file pair is a
fourth hand-written copy of the vendor map's own fact with no tie (recommendation); R12 the recorded
pack root is a machine-local absolute path in a committed manifest (defect). Of the earlier record's
seven blocking findings, F1, F5, F6 and F10 are closed; F2, F3 and F4 are closed in part, with their
residues carried above as R1/R12, R2/R3 and R5/R6 respectively. Base rule 39 on the repair delta:
clean on numbers — the delta adds none; its other half still bites the host pole of gate ag, whose
reach is zero for a host installed before today, for a host carrying a `VERSION` file, and for any
collaborator whose machine does not hold the recorded path.

Blocking: eight.
- R1, the pack-pole discriminator mistakes any versioned repository for this pack — stands: reproduced against a host fixture carrying `VERSION`, a recorded `pack_root` and a drifted vendored copy; the check printed `0 vendored file(s) checked … no drift` and exited 0, never opening the manifest.
- R2, a reopened row can never win the next move and the reason line says nothing higher is free — stands: reproduced against a two-row fixture; Requirement 320 criterion 6, base rule 38 and the shipped code name three different candidate sets, and only the author can choose between the first two.
- R3, an empty candidate set prints no `NEXT` block and no line in its place — stands: reproduced against a fixture whose only open row is reopened; Requirement 320 states no answer for the empty case. Cheapest of the eight to fold, one criterion.
- R5, the seeded template's prose and its priority list name different vocabularies — stands: `quick win` appears in the template's intake prose and in its own worked wish row and is absent from the seeded list, so `priority_rank` places it last.
- R6, an adopting host still meets the missing-statement line with nothing shipped naming the form — stands: `adopt/install-status-view.sh` never touches `PLAN.md` and never copies the template, so criterion 1a reaches a reader with the pack open and no one else.
- R8, the `[target]` drop left a clause promising machinery under a closed queue row while the architecture still says the tag is live — stands: Requirement 76 criterion 5 is unedited, q-48 is `✅` in `PLAN.md`, criterion 3's "until the reading machinery ships" is unedited, and `architecture/guardrails.md`'s INV-324 entry asserts the opposite of the spec; the feed contract that shipped is the transport, and no clause binds a feed metric to a spec-delta's success measure.
- R9, the architecture's INV-325 entry and M-634 describe a gate with one pole — stands: neither was touched in the range, and both now under-describe what ships.
- R12, the recorded pack root is a machine-local absolute path in a committed manifest — stands: criterion 9a states the record and names no portability, so a collaborator reading another machine's path gets either F2's stand-down again or a comparison against an unintended checkout.

R4, R7, R10 and R11 are recommendations and block nothing.
