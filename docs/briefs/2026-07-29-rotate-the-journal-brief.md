# Brief — rotate the journal back under its byte bound

Written 2026-07-29 for one worker starting with an empty context. Every anchor below is named by path.

## Your job

`JOURNAL.md` stands at 641088 bytes. Its declared ceiling is 640000 bytes. The push gate refuses.

Move the oldest entries out of the live file into an archive. Leave a pointer line the reader can
follow. Prove that nothing was lost.

## The refusal, quoted

Run `python3 guardrails/check-doc-bound.py` from the repository root. It printed this at 2026-07-29:

> doc-bound (gate z): 1 growable doc(s) past bound (SPEC INV-234, ROADMAP 392):
>   JOURNAL.md is 641088 bytes, past its declared bound of 640000, with no rotation dated 2026-07-29.
>   Remedy: rotate the closed rows out (scripts/rotate-doc.py) so the live file shrinks back under the
>   bound, or raise max_bytes in doc-bounds.json with a recorded reason.

It exits 1. The gate is called from `guardrails/pre-push:226` and from `.github/workflows/gates.yml:98`.

## The bound and its recorded reason

The ceilings live in `guardrails/doc-bounds.json`. The journal's entry reads:

```
"JOURNAL.md": {
  "max_bytes": 640000,
  "reason": "seed 2026-07-18 above ~543 KB current with rotation headroom; old dated chapters rotate
             to a dated archive before this ceiling."
}
```

The reason names your remedy. Old dated chapters rotate to a dated archive.

The same file's opening comment names the convention behind every ceiling. Each was seeded above the
file's size of the day with roughly a hundred kilobytes of headroom.

## Raising the bound is refused

Take the first remedy the gate names and leave the second alone.

This repository holds a ratchet law over its declared numbers. A declared bound moves down on its own
and rises only against a recorded reason. The gate's own docstring states it at
`guardrails/check-doc-bound.py:26` to `:28`.

Tonight's work landed that same law over a different record. Two journal entries carry it:

> ## 2026-07-28 — the findings record is a ceiling in fact
>
> ## 2026-07-29 — the ratchet's second check was protection in name, and a worker's command reddened
> the suite

A session that raises its own ceiling to pass its own gate teaches the gate to mean nothing. So
`max_bytes` for `JOURNAL.md` stays at 640000, and the live file comes down to meet it.

## The precedent, and where it stops

The queue already rotates. Read these three anchors before you write anything:

- `scripts/rotate-doc.py` performs the move.
- `docs/queue-archive/` holds the rotated material.
- `ROADMAP.md` carries a manifest block at lines 28 to 32, between the markers
  `<!-- rotated-manifest -->` and `<!-- /rotated-manifest -->`.

That manifest block names what left and where it went. Its lines read like this one:

> - rows 14, 27, 33, 42, 43, 62, 63, 67, 101, 121, 172, 189, 194, 196, 200, 201, 202 →
> docs/queue-archive/rotated-ROADMAP-2026-07-18.md

### What the journal follows

Four parts of that shape carry over unchanged:

- the archive directory is `docs/queue-archive/`;
- the archive name carries the document it came from and the date of the move;
- the archive keeps everything that left, so nothing is lost;
- the live file keeps one pointer line naming the archive.

### What does not fit

Four parts of that shape do not carry over:

- the unit. The queue moves a table row of the shape `| n | ... |`. The journal moves a dated section.
- the closure judgment. A queue row rotates when its status cell carries a terminal word. A journal
  entry carries no status cell, and age is the only signal it has.
- the manifest line shape. The gate's parser reads `rows <numbers> → <path>`. The journal has no row
  numbers to name.
- the tool. Its docstring refuses the job outright, at `scripts/rotate-doc.py:45` to `:47`:

> Only ROADMAP.md's table shape is understood today (a row is a `| n | ... |` line). JOURNAL.md and the
> prose docs rotate by a different unit and are out of scope for this first mechanism; the tool refuses
> a doc whose shape it does not know rather than guess.

So you perform this rotation by hand. Do not call `scripts/rotate-doc.py` on `JOURNAL.md`, and do not
widen it to understand the journal. Widening the tool is a separate piece of work with its own spec.

## The journal's shape, as measured

Never read `JOURNAL.md` whole. It is 641 kilobytes, and one read floods your context and buys you
nothing. Read its structure with `grep -n`, and read a named line range when you need the text.

The structure, measured at 2026-07-29:

- line 1 is the document heading `# live-spec Journal`. It is the only `#` heading in the file.
- line 3 is the intro paragraph, one line long.
- 263 sections open with `## `. The file has 5852 lines.
- 247 of them open `## 2026-`, a date in the year-month-day form.
- 16 of them open `## Session ` and carry their date inside the title instead. Every one of those 16
  names a date between 2026-07-10 and 2026-07-12.

Confirm each of those counts yourself before you move anything:

```
grep -c '^## ' JOURNAL.md
grep -cE '^## 2026-' JOURNAL.md
grep -nE '^## ' JOURNAL.md | grep -vE '^[0-9]+:## 2026-'
```

### One correction to the file's reputation

The journal is described as newest first. It holds two runs instead of one, and you must know this
before you pick a cut point by position.

The first run descends from 2026-07-29 down to 2026-07-12. It ends at line 5355. The second run
climbs from 2026-07-13 to 2026-07-28, and it fills the rest of the file to the end.

So the file's last section is dated 2026-07-28, and the oldest material sits in the middle. A cut that
takes the tail bytes would archive recent entries. Cut by date instead.

## What leaves and what stays

### The rule

Every entry dated 2026-07-12 or earlier leaves. Everything dated 2026-07-13 or later stays.

The rule reaches the 16 `## Session ` entries cleanly, since each names a date of 2026-07-10, 07-11 or
07-12 in its own title.

### The one lucky fact

Those 170 entries stand in one unbroken block. Nothing dated 2026-07-13 or later sits inside it, and no
entry dated 2026-07-12 or earlier sits outside it. So the move is one contiguous slice.

The block is lines 1556 through 5355 inclusive, 3800 lines, 337872 bytes.

- line 1556 opens `## 2026-07-12 ~21:20 (build-worker) — LANE B of row 279`. It is the first line that
  leaves.
- line 5355 is blank. It is the last line that leaves.
- line 5356 opens `## 2026-07-13 ~13:40 — Row 298: per-kind design principles`. It is the first line
  that stays after the cut.
- line 1555 is blank, and line 1544 opens `## 2026-07-13 ~14:39 (opus, orchestrator seat)`.

Re-derive both boundaries from those heading texts before you cut. Someone may append a new entry at the
top of the file today, and every line number above moves the moment they do. The heading text is the
stable anchor, and the number is a convenience.

### The arithmetic

- the live file today: 641088 bytes.
- what leaves: 337872 bytes.
- the live file after: 303216 bytes.
- the ceiling: 640000 bytes. The live file lands 336784 bytes under it.

Two minimums stand behind that number, and the cut clears both by a wide margin on purpose:

- 1089 bytes must leave for the gate to pass at all.
- about 101088 bytes must leave to restore the file's own convention of roughly a hundred kilobytes of
  headroom under the ceiling.

The cut takes far more than either, because the journal gains an entry on most days. A rotation that
lands one kilobyte under the ceiling earns the same red again within the week.

### What each file holds afterwards

The live `JOURNAL.md` keeps its heading, its intro paragraph, the new pointer line, and 93 dated
sections. Its oldest kept entry is `## 2026-07-13 ~13:40`.

The archive holds all 170 entries that left, in the order they stood in the live file. It opens with its
own heading and a line naming the range it holds.

## Where the archive lives

Put it at `docs/queue-archive/JOURNAL-archive-2026-07-29.md`.

The directory comes straight from the precedent. The name deliberately stays outside the pattern
`rotated-*.md`, and the next section says why.

Settle all three questions below before you move a single byte. Run each command and record what it
printed.

### Check one: the census's live set

`scripts/rule-census.py` measures every markdown file the writing rules bind. Its list of record
directories at lines 71 to 78 already carves out `docs/queue-archive`. Its record files at line 79
already carve out `JOURNAL.md` itself.

So an archive in that directory never enters the measured set. This matters. An archive of 337
kilobytes of prose would arrive carrying thousands of findings. It would carry no entry in
`guardrails/rule-census.json`, and the findings gate would red on the next push.

Prove the carve-out holds after you write the file:

```
python3 -c "import importlib.util; s=importlib.util.spec_from_file_location('rc','scripts/rule-census.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); f=m.live_files(); print(len(f)); print([x for x in f if 'queue-archive' in x])"
```

It printed `108` and `[]` before the move. It must print an empty list after it.

Never run `python3 scripts/rule-census.py --json`. That flag writes the findings record, and others read
that record through the day.

### Check two: the bound gate itself

`guardrails/doc-bounds.json` declares four documents. The archive is none of them, so it carries no
ceiling of its own and the bound gate never reads it.

Confirm by reading the four keys under `docs` in that file. Add no entry for the archive.

### Check three: the rotation gate, which is the one that bites

`guardrails/check-doc-rotation.py` is gate t. It runs from `guardrails/pre-push:153` and from
`.github/workflows/gates.yml:64`.

Its orphan scan reads every file matching `docs/queue-archive/rotated-*.md` and reds any one that no
live manifest line points to. Two facts make that a trap for a journal archive:

- its manifest parser at line 65 reads only lines of the shape `rows <numbers> → <path>`. A journal
  archive holds no row numbers, so no line you write can register it.
- it scans `ROADMAP.md` alone by default, at line 172. A pointer line inside `JOURNAL.md` is invisible
  to it, and `ROADMAP.md` belongs to the session lead.

This was probed on a scratch tree at 2026-07-29. With the archive named
`docs/queue-archive/rotated-JOURNAL-2026-07-29.md` the gate printed:

```
FAIL (doc-rotation): a rotation lost content or left no manifest line (SPEC INV-209):
  - no manifest: docs/queue-archive/rotated-JOURNAL-2026-07-29.md exists but no live manifest line
  points to it (base rule 10 — a superseded portion moved with no manifest line)
```

The same tree with the file renamed to `JOURNAL-archive-2026-07-29.md` printed:

```
OK (doc-rotation): every rotated row is findable in its archive and every archive is named in a
manifest line — nothing lost (INV-209).
```

So the proposed name keeps the gate green and keeps the archive in the same directory as its precedent.
Reproduce both runs on your own scratch tree, and record what they print.

One neighbouring risk is already cleared. The same gate reds any numbered table row inside an archive
whose status cell carries no terminal word. `grep -cE '^\|\s*[0-9]+\s*\|' JOURNAL.md` returns 0, so the
journal carries no line of that shape and the check cannot fire on your archive.

Report a gap to the lead in your own report. The journal's rotation has no gate proving nothing was
lost, because gate t reads the queue's row shape alone. That gap deserves a queue row, and the lead
opens it.

## The pointer in the live file

Write one line into the live `JOURNAL.md`, directly under the intro paragraph, with a blank line on each
side. A reader who greps the live file for an old entry must meet it and follow it.

Something of this shape serves:

> Entries dated 2026-07-12 and earlier live in `docs/queue-archive/JOURNAL-archive-2026-07-29.md`,
> moved there on 2026-07-29 so the live file stays under its byte bound. Nothing was dropped.

Use the marker pair `<!-- rotated-manifest -->` only if check three tells you it is safe. On the naming
this brief proposes, the markers are unnecessary and the plain sentence is enough.

## The archive's own head

Open the archive with a heading and a range line, in the manner
`docs/queue-archive/rotated-ROADMAP-2026-07.md` opens. Two elements are required:

- a `# ` heading naming the document and the range, such as
  `# Archived JOURNAL entries — 2026-07-04 to 2026-07-12`.
- a line naming when the entries moved, why, where they came from, and that nothing was lost.

Then the 170 entries follow, byte for byte as they stood, in the order they stood.

## The proof

Rotation is a move, so the proof is that the bytes arrived and the count adds up.

### The count

The strongest proof is three numbers and one addition. Run this before the move and again after it:

```
grep -c '^## ' JOURNAL.md
grep -c '^## ' docs/queue-archive/JOURNAL-archive-2026-07-29.md
```

The expected numbers are 263 before, 93 in the live file after, and 170 in the archive. Then 93 plus 170
equals 263, and no entry was lost. Quote all four numbers in your report.

Take the archive's count with care. Its own `# ` heading holds one `#`, so it never joins the `## `
count. Its range line must open with no `## ` either.

### The bytes

```
wc -c JOURNAL.md docs/queue-archive/JOURNAL-archive-2026-07-29.md
```

The live file must read 303216 bytes. The archive reads 337871 bytes of moved material plus whatever
your heading and range line weigh.

Recover the exact identity too. The live file's bytes plus the moved bytes plus one newline equal
641088, the size the file held before you touched it. State that identity in your report.

### The two boundary reads

Grep the archive for its first and last entry, and grep the live file to prove they left it:

```
grep -c '^## 2026-07-12 ~21:20' docs/queue-archive/JOURNAL-archive-2026-07-29.md
grep -c '^## 2026-07-12 ~21:20' JOURNAL.md
grep -n '^## 2026-07-13 ~13:40' JOURNAL.md
```

The first returns 1, the second returns 0, and the third finds the live file's oldest kept entry.

### The gates

Run each of these from the repository root and record its output:

1. `python3 guardrails/check-doc-bound.py` — must exit 0 and print its OK line. Quote that line.
2. `python3 guardrails/check-doc-rotation.py` — must exit 0.
3. `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the counts out of the log's last line.

Write the suite log into your scratchpad directory. An exit status is no test result, so quote the log.

## What you must not do

Commit nothing and push nothing. The session lead does both.

Run no command that discards uncommitted work in any tree. That bars `git checkout -- <path>`, `git
restore` without `--staged`, `git stash`, `git reset --hard` and `git clean -f`. Other people hold
uncommitted work in this tree right now.

A file you mean to put back, you read first and put back by writing the bytes yourself. A check reads
every worker's commands for this rule, and one breach reds the suite for a day.

So take your own copy before you cut. Copy `JOURNAL.md` into your scratchpad directory first, and
restore from that copy by writing the bytes if the move goes wrong.

Never run `python3 scripts/rule-census.py --json`, which writes the findings record.

Do not re-seed `guardrails/rule-census.json`.

## The files other people hold

Another worker holds `DECISIONS.md` right now. Leave it closed.

`ROADMAP.md` and `NEXT_STEPS.md` belong to the session lead. Leave both closed.

Where this work owes a line to any of those three, write those words into your report. Their owner
places them. At least three lines are owed:

- the journal entry recording this rotation, its date rule, and its numbers;
- the queue row for the missing rotation gate over the journal's prose shape;
- whatever `NEXT_STEPS.md` owes about the live file's new size and its remaining headroom.

You own `JOURNAL.md` and your new archive file. Nobody else is editing either one.

## The writing standard your prose is held to

Every document this repository ships is measured. Four rules bind everything you write, including the
archive's heading, the pointer line, and your report:

- keep each sentence at or under 25 words;
- use plain product words;
- keep an internal code out of the front of a sentence, where it names nothing to a reader;
- write no sentence that names a thing by denying its neighbour.

Measure every document you wrote or edited:

```
python3 scripts/rule-census.py <file>
python3 scripts/preshow-register-lint.py <file>
```

Repair what they flag and re-run until both read zero for the lines you added. The entries you moved
carry their old prose unchanged, and you edit none of it. A record states what was written at the time,
and the rules bind it at the moment it was written.

## What done means

Report these nine things, each one a reader can check:

- the refusal the bound gate printed before your work, quoted;
- the OK line the same gate printed after it, quoted;
- the live file's byte count before and after, and the archive's byte count;
- the byte identity, showing the two files plus one newline recover 641088;
- the three section counts, 263 before, 93 live, 170 archived, and the addition;
- the archive's path, and what each of the three checks printed for it;
- the pointer line as it now stands in the live file, quoted;
- the boundary reads, showing the first archived entry left the live file and the oldest kept entry
  stands;
- the full-suite counts, quoted from the suite log.

Then report the lines `JOURNAL.md`, `ROADMAP.md` and `NEXT_STEPS.md` owe, in the words you would have
written into each.

Report anything you found and left alone.
