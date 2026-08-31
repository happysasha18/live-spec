# Archived 2026-08-31: three rows the hostile review of the remaining board found dead

Asked for 2026-08-31, his own word: "из этих 20 в очереди точно все нужны?" (of these 20 in
the queue, are they really all needed?). A clean-context Opus review of every open row, recorded
in `.live-spec/checkpoints/night-run-2026-08-28.md` under "THE HOSTILE REVIEW OF THE REMAINING
BOARD", sorted four into "archive now, no work". Three land here, each verified again before
archiving rather than taken on the review's word alone. The fourth, `q-48`, is NOT archived
despite the review's verdict — checked against `tests/test_traceability.py`'s `TARGET_ROW_OWNERS`
before touching it, `q-48` is the live owner of spec anchor `INV-21`; archiving it (taking it out
of `PLAN.md`'s `## Tasks` section) would orphan that anchor the exact way tonight's whole
target-ownership correction exists to prevent. `q-48` stays on the board, marked deferred rather
than archived — see its own row for the note.

## Index

One line per archived row, findable by its own number (`docs/roadmap-format.md`'s terminal-word
vocabulary: declined). `plan-15` carried no row number in the retired queue's numbering and stands
under its own heading below only, the same exception `plan-1` and `plan-13` already carry in
`rotated-PLAN-2026-08-28-folded-rows.md`.

| # | Wish (plain words) | Class | Status | Decision / acceptance |
| --- | --- | --- | --- | --- |
| 453 | Your edits on a review page save straight to the files | small | declined 2026-08-31 | no incident, no owner word since the 2026-07-22 relay — archived, full text below |
| 751 | Every test in the suite is proven to guard something real | small | declined 2026-08-31 | plan-6 already answered the question 2026-08-26; re-measuring it again is the standing rule's own forbidden case — archived, full text below |

## plan-15 — The promoter project is updated to today's tools

**Group:** Cross-project · **Priority:** normal
**Source:** PLAN.md step 15.

Its wish sits in its own inbox. Smaller documents than tlvphotos and a wider version gap: its
record pins pack 2.4.0, a 3.3.0 note was read and parked in July, and the pack is at 6.0.0. Two
canonical documents are absent there entirely. It runs off the machine's global skill mirror with
no local copy, and it has been idle since 27.07, so nothing of the owner's is in flight to protect.

**Acceptance:** `ls ~/promoter/.claude/skills | grep -q director` passes and
`~/promoter/.live-spec/VERSION` reads the pack's current number, with that project's own `git status
--porcelain` showing changes confined to its skills and settings directories. The two canonical
documents absent there exist. The wish's own acceptance lines run green in that tree.

**Archived:** no owner word and no incident since 27.07 — idle, not blocked, not asked for again.

## q-453 — Your edits on a review page save straight to the files

**Group:** Communication & reporting · **Priority:** normal
**Source:** relayed 2026-07-22.

**Acceptance:** A test edits one line on a rendered review page, runs the save, and finds that
change byte for byte in the repository file the line came from; the same test reds when the save is
skipped. The script that carries the round trip ships inside the pack, `test -f` finding it there.

**Archived:** provenance is "relayed", not his own dated word, and nothing in the tree shows this
feature was ever missed or asked for again since 2026-07-22 — no incident, no owner word.

## q-751 — Every test in the suite is proven to guard something real

**Group:** Method reliability · **Priority:** normal
**Source:** owner 27.08 — "непонятно почему так много тестов, тоже надо пересмотреть."

**What it is.** The suite holds 2,426 tests. Nobody has checked how many of them could ever fail —
whether the thing each one guards has ever actually moved.

**Why now.** Plan-6 already ran this exact measurement on a smaller class, phrase-guard tests, and
it settled a real question with numbers rather than a guess: a 120-test sample showed 16% could
never have failed, and 84% guarded real content that changed — the finding was against mass
removal, because most of the sample earned its place. The same method, run over the whole suite,
answers the size question honestly instead of by feel.

**Done when.** No command decides this one. A sample of the suite is measured the way plan-6
measured its 120 tests, and the share that could never have failed is written on one page with the
sample size and the method beside it. The owner reads that number before a single test is cut. What
would convince him: the number, and being able to see how it was reached.

**Archived:** `plan-6` already ran this exact measurement 26.08 on 120 tests, found 16% dead, and
the owner's decision from that reading was against mass removal. This row proposes re-measuring the
same, now-settled question — exactly what his own standing rule forbids ("никогда ничего заранее
мерять не надо" — never re-measure for confidence; a settled reading is not re-opened by re-running
it).
