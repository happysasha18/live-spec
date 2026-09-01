# Overnight session prompt — live-spec, close the backlog for real

Paste this whole thing as the first message of a fresh session in `~/live-spec`. Load the personal
profile and the live-spec pack normally (per `~/.claude/CLAUDE.md`'s own bootstrap) before starting.

## Scope — exactly these eight PLAN.md rows, nothing else

`q-803`, `q-54`, `q-163`, `q-48`, `q-385`, `q-804`, `q-436`, `q-501`.

Do not touch `q-166`, `plan-14` (both need a design decision from Alexander first, not a mechanical
build — leave them exactly as they stand) or `plan-9` (deliberately held by his own prior word, not
yours to resume). Read each of the eight rows in full in `PLAN.md` before starting its work — do not
work from this prompt's summary alone.

**q-501, narrowed tonight (his word, 2026-09-01 23:15):** drop the "how many projects the page may
claim" question entirely — do not name a count, do not ask, just remove that numeric claim from the
page if it makes one, or leave it absent if it already doesn't. The row's other two legs — the page
reading cleanly for a first-time reader, and the plain-language check passing clean — are real and
still yours to close normally. Its 👁️ mark can drop once these hold and nothing on the page states a
project count it can't back.

## The one standing rule for tonight — no unprotected concurrency

This project's own rule (`skills/live-spec-base/SKILL.md`, rule 7, "No unprotected concurrency — his
word, 2026-09-01"): two writers never touch the shared tree at once without a stated safety measure.
Tonight's measure is worktree isolation, no exception:

- Open every row's work with `bash scripts/open-lane.sh` (or by hand, following rule 7's own "lane-open
  act" steps exactly) — never edit a row's files directly on the shared `main` working tree.
- Stay within the profile's lane cap (`lanes.cap`, default 3) for how many rows run at once. Running
  fewer at a time, one after another, is completely fine and often simpler than maxing the cap — prefer
  correctness over parallelism tonight.
- A row's own lane is where ALL of its edits happen, including its `PLAN.md` mark flip. The merge back
  into `main` is the only moment `PLAN.md` gets touched on the shared tree, and it happens one row at a
  time even if several lanes finished their own work in parallel.
- If two rows would touch the same file (check before opening lanes — e.g. more than one row editing
  `PLAN.md`'s own machinery, or two rows both touching the same skill file), run those two sequentially,
  never in the same wave.

## What "done" means for a row tonight — no exceptions

- Its `PLAN.md` mark is `✅` only when backed by a real command in `scripts/plan_checks.py` running
  its actual acceptance, or — only if the acceptance genuinely cannot be a command — a
  "Checked by reading on <date>" line with what was actually checked. Follow the exact pattern
  `plan-10`'s landing already established (`tests/test_plan_done_marks_are_backed.py` is the test
  that enforces this — run it after every row closes).
- Before merging a row's lane into `main`, run the tests that actually cover its own change and
  confirm green. Do not trust a worker's own self-report — re-run the command yourself from the
  merged `main` tree after the merge, not just inside the lane before it.
- If a row's acceptance turns out to require something outside this session's reach (writing into
  another project's own tree, like `~/tlvphotos` — `q-163` and `q-48` both have exactly this shape,
  a pack-side leg you own and a host-side leg you don't) — land the pack-side leg for real, and leave
  the row honestly partial with the remaining leg named plainly in its own text, the same way `q-163`
  and `q-48` already read tonight. A partial, honestly-labeled row is a correct outcome. A row marked
  `✅` that isn't actually done is not.
- Do not invent new machinery beyond exactly what a row's own acceptance already asks for. Do not
  "improve" or refactor anything a row doesn't touch.

## The failure modes tonight exists to prevent — do not reproduce them

These three things happened during today's session and must not happen again:

1. **"Hostile review found real problems, redo everything."** Do the equivalent scrutiny WHILE
   building each row, not after. Before calling a row done, ask yourself the adversarial question
   directly — does this actually hold against the live tree, or does it just look done — and answer
   it with a real command, not a feeling. The end-of-night review (below) should find nothing, and if
   it does find something, that is this session's own failure to catch it earlier, not a normal step.
2. **"Two workers stepped on each other."** Worktree isolation (above) makes this structurally
   impossible tonight, if actually followed. Never skip `open-lane.sh` "to save time."
3. **"Next session needs to re-verify everything from scratch."** The morning report (below) has to be
   something Alexander can trust without re-checking it himself. That means: run the FULL test suite
   once, for real, with nothing else editing the tree at the same time, after every row has merged —
   not a targeted subset, not a run taken while something else was still writing. If it's not fully
   green, the night's work is not done, regardless of how many rows show `✅`.

## Order

Read all eight rows first, note any real file-overlap between them, then work through them — in
parallel lanes where genuinely disjoint, sequentially where not. `q-501` and `q-803` both plausibly
touch prose surfaces broadly (`q-803` sweeps `skills/*/SKILL.md` and `references/*.md` for stale
citations; check its exact scope against whatever `q-501`'s "first-time reader" pass touches, and
sequence them if they'd collide). Use your own judgment on the rest, but state each lane's write-set
before opening it.

## When every row is closed (or honestly partial)

1. Merge everything into `main`, one row at a time.
2. Run the complete suite once, on a quiet tree: `python3 -m pytest -q`. Confirm `0 failed, 0 errors`.
   If anything is red, fix it before writing the report — do not report a red suite as "basically done."
3. Update `NEXT_STEPS.md`'s `## LIVE STATE` block once, honestly, covering the whole night in one pass
   — not per-row.
4. Do not push. Pushing `live-spec`'s own repo stays a separate window's job (seat-split rule).
5. Write ONE closing message for Alexander when he next opens this session or asks — not a stream of
   progress updates while working. It should say, in plain Russian, per this project's own chat
   register (`~/.claude/live-spec/profile.md`): which rows closed clean, which stayed honestly partial
   and why, the full suite's final number, and nothing else — no self-congratulation, no inflation, no
   itemized blow-by-blow of the night's process.

Do not surface anything as needing his word tonight unless it is genuinely his — a taste call, a
policy question, or an act irreversible outside git. Everything else in these eight rows is yours to
decide and finish, the same standing rule that governed the rest of today's session.
