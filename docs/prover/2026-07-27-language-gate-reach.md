# Prover record — the language gate's reach and the calque list's shelf, 2026-07-27

Prover skill: product-prover, live-spec pack v4.3.0. Mode: CROSS-LINK with the architecture lens, delta
scoped. Reviewed by a seat that authored none of the work (SPEC INV-237).

## Scope

**What this record reviews.** One commit: `18f7a17`, "The language gate reads a file the delivery just
wrote, and the calque list is declared working-language data". Seven files — `PRODUCT_SPEC.md`,
`PRODUCT_SPEC.index.md`, `TEST_MATRIX.md`, `hooks/midturn-chat-scan.py`,
`scripts/check-shipped-language.py`, `scripts/shipped-language-allowlist.json`, `tests/test_guardrails.py`.

**What this record does not review.** The parent commit `4e7ef2d`, already covered by
`docs/prover/2026-07-27-push-gate-fold.md`. That record was read for context only.

**State read.** The working tree at `18f7a17` with one unrelated modification (`ROADMAP.md`) and no
untracked files. Every claim below rests on a run or on a file read, never on the commit message.

## Verdict

**HOLD — one must-fix stands between this and the push.** One must-fix, three should-fix.

The delta is right about the gap it names and right about how to close it. The gate did read the tracked
set alone, a file a delivery had just written was invisible until the following commit, and the union of
the cached and the untracked sets is the correct shape for a check that runs before the commit it holds.
The new test is real and it does pin the fact the matrix now claims for it. What holds the push is the
other half of the same change: the union reaches every untracked file in the tree, including files no
delivery wrote and git will never push, and the gate now depends on `.gitignore` to tell those apart while
no criterion says so and `.gitignore` does not carry the entries that would do it.

| # | Kind / severity | Claim / evidence | Status |
|---|---|---|---|
| M1 | defect / must-fix | The widened scan reaches past the shipped set the spec declares: any untracked, non-ignored text file reds, and a local note or a vendored directory blocks the push | OPEN |
| S1 | defect / should-fix | The cached half of the new union is pinned by no test; dropping `--cached` leaves the whole class green | OPEN |
| S2 | defect / should-fix | The same tracked-only enumerator survives in a sibling blocking gate, `guardrails/check-authority-anchor.py` | OPEN |
| S3 | recommendation / should-fix | The calque list's `note` fields are prose, and the whole-file entry spares them under a shelf declared for program data | OPEN |

---

## M1 — The widened scan reads files no delivery carries, and the escape it depends on is unstated

> "The system *shall* read every shipped text file the delivery carries, a file written and not yet
> committed included" — PRODUCT_SPEC.md, Requirement 150 / Case: what the shipped set holds, criterion 3

The code has no notion of a delivery. `git ls-files --cached --others --exclude-standard` returns the
index plus every file in the working tree that git neither tracks nor ignores, whoever wrote it and
whatever it is for. I ran the shipped engine over a scratch repository holding one committed clean file,
one untracked local note in Russian, one untracked `.venv/lib/meta.py` carrying a package author line, and
untracked notes under `docs/` and `inbox/`. The two excluded directories were spared correctly. The other
two reded:

> "  .venv/lib/meta.py:1  [owner-name]  # author: Alexander Petrov" — engine run over the scratch tree,
> exit 1, offences 2 (the second offence is the local note, reported as `notes-local.md:1 [cyrillic]`)

The person affected is anyone running the pack's own pre-push hook, where this engine is gate i and
blocking. They keep a virtual environment, an installed dependency tree, or a working note inside the repo
— none of it tracked, none of it ever pushed — and their next push stops with a file-and-line report about
a file that is not part of the push. `.gitignore` carries no entry for `.venv/`, `venv/`, or
`node_modules/`, so the most ordinary local artifact in a Python repository is exposed today. The gate's
own remedy line does not name the remedy that applies: it offers the diaries, a user-language fence, and
an allowlist entry, while the correct answer is an ignore rule.

Underneath the false red sits the definitional gap. Criterion 3 defines the shipped set as what the
delivery carries; the code defines it as the working tree minus what `.gitignore` hides. `.gitignore` has
become load-bearing for the shipped set's boundary and no criterion, no matrix cell, and no line of the
engine's own docstring says so, so nobody maintaining that file knows it is holding a gate's reach.

Do three things. Add `.venv/`, `venv/`, `node_modules/`, and `.DS_Store` to `.gitignore`, closing today's
exposure. Extend criterion 3 with the boundary it actually holds — the shipped set is the tracked files
plus the untracked files git does not ignore, so an ignore rule is how a local-only file leaves the set —
and mirror that sentence into M-260's fact cell and the `shipped_set` docstring. Add the ignore rule to
the gate's printed remedy line as a fourth option, named for the case where the reported file is local
only. The alternative shape, filtering the untracked arm down to files the delivery touched, needs a
notion of a delivery the gate does not have and should not grow.

`defect · boundary-issue (composition)`

---

## S1 — The union's other half is pinned by nothing

> "the gate must read it in that same delivery" — `tests/test_guardrails.py`,
> `test_gate_reads_a_file_that_is_written_and_not_yet_committed`

The new test seeds one committed clean file and one uncommitted file with an offence, and asserts the
uncommitted one reds. It proves the `--others` arm. Nothing proves the `--cached` arm survives, because
every other test in `TestGateShippedLanguage` hands the engine explicit file paths, which bypasses
`shipped_set` entirely, and the one whole-tree test asserts only that the real repository is green.

I copied the engine, dropped `--cached` from the argument list, and ran the copy over the repository:

> "OK (shipped-language): no Cyrillic, owner-name, or project-name offences in the shipped set." — engine
> copy with the cached arm removed, exit 0

It reports green by scanning nothing at all, since the tree currently holds no untracked files. So a change
that broke the tracked half of the enumeration would pass the fixture tests, pass the whole-tree test, and
pass the new test, and the matrix would still claim the gate reads every text file the delivery carries.

Extend the new test rather than adding another: after asserting the uncommitted file reds, write a second
offence into the committed file, re-run, and assert both file names appear in one report. That pins the
union as a union and costs four lines.

`defect · missing-outcome-check (postcondition)`

---

## S2 — The same blindness stands in a sibling gate

> "        out = subprocess.run([\"git\", \"-C\", root, \"ls-files\"]," —
> `guardrails/check-authority-anchor.py`, `_tracked`, line 346

This is the enumerator the delta just replaced, unchanged, in a gate that is also blocking in the same
pre-push hook (line 114, after gate i at line 77). Its consequence is the one the commit message
describes: an authority-anchor offence in a file a delivery has just written is read one commit late, one
commit after the push it was meant to hold. The delta fixed one instance of the class and left its twin
two directories over.

Give the two gates one enumerator. The shipped-language engine's `shipped_set` and the authority-anchor
`_tracked` differ only in their exclude lists and their extension filter, so the shared part is the git
call and the walk fallback. Failing that, apply the same three flags to `_tracked` and give it a test in
the shape S1 asks for. The first is the root fix and belongs to an architecture step; the second closes
the hole this week.

`defect · boundary-issue (composition)`

---

## S3 — The calque list's notes are prose, spared under a shelf declared for program data

> "user_language_globs : files whose Cyrillic is deliberate program data. Cyrillic in them is never an
> offence." — `scripts/check-shipped-language.py`, allowlist docstring

The shelf is the right one for this file. `hooks/chat-calques.json` is a pure data file read by
`hooks/midturn-chat-scan.py`; its patterns and its replacement strings are the detector's own vocabulary,
which is exactly the class `scripts/spec-style-lint.py`, `scripts/register-lint-floor.json` and
`hooks/chat-law-hook.sh` already stand on. The narrower shelf, per-snippet `cyrillic_waivers`, belongs to a
different kind: a code file carrying a handful of deliberate strings among its logic. Nothing
hides that should red: the entry spares the Cyrillic arm alone, so a personal name in the calque list
still reds, and I confirmed the name arm reads the file by inspection of `scan_file`, where
`name_file_ok` is drawn from `authorship_globs` alone.

The residue is small and worth naming. Each entry's `note` is English prose that ends in a quoted Russian
sentence — the line that earned the entry — and the file's own opening comment promises one more of them
per future entry. Prose is not program data, so that part of the file is spared by an entry whose declared
meaning does not cover it, and the amount of unread prose in the file grows by design.

Move the quoted line into its own field, `trigger`, beside `pattern` and `say`, so the file's Cyrillic is
program data in every field it appears in and the `note` stays English. One line of the opening comment
records the rule. This changes no behaviour and is a taste call.

`recommendation · boundary-issue (composition)`

---

## What is sound

**The gap the delta names is real and the fix is the right shape.** A gate that runs before a commit and
reads only what is committed cannot see the delivery it is holding. The union of the cached and the
untracked sets is the correct answer to that; M1 asks for the boundary to be stated and the ignore rules to
be filled in, and asks for nothing about the shape.

**The new test is genuine, and the red-first claim holds by construction.** It seeds a real git repository,
commits a clean file, writes an offending file that is in no commit, and asserts the report names it. With
the old enumeration that file is not in `ls-files` output, so the scan set holds only the clean file and the
engine prints green. The red-first proof needs no re-run to be believed, and I re-ran the class anyway: 18
passed.

**The renumber left no dangling reference.** Criterion 3 became criterion 4 and gained a new criterion 3.
I swept the tree for `R150.x` citations: the only ones outside the requirement body are the two generated
index tables, both regenerated correctly, and the frozen sketch under `prototype/`, which the fence keeps
out of the shipped set by design.

**The docstring change removed the offence without losing the fact.** The failing sentence is gone from
`hooks/midturn-chat-scan.py`; the docstring still states which two laws the line broke and why the Stop-side
scan stayed quiet, so a reader learns the case without the sample.

## The answers asked for

**Does the enumeration change do what the criterion claims, and can it red something lawful?** It does what
the criterion claims and more. Every file the delivery writes is now read in that delivery, proven by the
new test. The scan also reaches every other untracked, non-ignored text file, proven by run: a local note
and a file under an untracked `.venv/` both red, while `docs/` and `inbox/` are spared by the exclude list
and `outbox/`, `.claude/`, `.spec-freeze/` and `.2.0-work/` by `.gitignore`. The exposure that stands is a
vendored or generated directory with no ignore rule, and `.gitignore` carries none for the usual ones.
That is M1.

**Is the allowlist entry the right mechanism for the calque list?** Yes. The file is program data of the
detector-vocabulary kind, which is the declared meaning of `user_language_globs` and the shelf three
sibling files already stand on, and the entry spares the Cyrillic arm alone, so a personal name in that
file still reds. The one residue is the prose in the `note` fields, which is S3 and is a taste call.

**Does criterion 3 say what the code does, and does M-260 name a test that exists?** Criterion 3 says less
than the code does, which is M1. M-260 names `test_gate_reads_a_file_that_is_written_and_not_yet_committed`;
the test exists at `tests/test_guardrails.py`, asserts the stated fact, and passes. M-260's fact cell now
matches criterion 3's wording, so the two move together, and both need the same sentence added.

**Is anything stated in one place and denied in another?** No denial. One inventory is incomplete: the hook
docstring says the sentence stands in the hook's red fixture and in the record of the day, and it also
stands in `tests/test_midturn_chat_scan.py` and in the `note` of `hooks/chat-calques.json`. The docstring
claims no exclusivity, so this is not a contradiction, and it is the reason S3 is worth naming — the calque
list is now a permanent home for that class of sentence and the entry added here is what spares it.

**The five runs.**

| Command | Result |
|---|---|
| `python3 scripts/check-shipped-language.py` | green, exit 0, offences 0 |
| `python3 -m pytest tests/test_guardrails.py -q -k ShippedLanguage` | green, 18 passed, 62 deselected |
| `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md` | green, 1452 of 1452 criteria well-shaped across 295 requirements |
| `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` | green, committed index equals the fresh build, 369 codes agree |
| `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md` | green, committed reference equals the fresh build, 376 anchors agree |

## Fold of this record's findings, same movement (2026-07-27, by the authoring seat)

- **The must-fix is folded by narrowing the boundary rather than widening the scan.** The shipped set is
  the delivery's own index: a file staged for this delivery is read one commit before it lands, and a
  file belonging to no delivery — a local note, a vendored library — stays outside a blocking gate
  entirely. Criterion 3 states that boundary, and matrix row M-260 follows it.
- **The untested half is folded**: the test now runs both directions on a real repository — an unstaged
  local file carrying the same offending content passes, and the moment the file is staged the gate reds
  it by name.
- **The sibling gate's enumerator** reads the index as well, which is the boundary this record's fold
  makes the stated one, so the two gates agree by construction rather than by coincidence.
- **The calque list's shelf stands, with its reason written here**: the file's whole content is
  working-language vocabulary, each entry naming the word the pack forbids and the plain word it owes,
  so the Cyrillic arm can carry no meaning over it. The name arm still reads the file, which is the arm
  that would catch a person's name arriving in a note field.
