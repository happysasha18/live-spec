# Brief — a fresh agent reads the previous session

Written 2026-07-28 for one worker starting with an empty context. Every anchor is named below by path.

## This brief waits

Two workers are editing this tree right now, and both hold `PRODUCT_SPEC.md` and `TEST_MATRIX.md`. This work edits the same two files.

Start nothing until the session lead says the tree is yours. Ask the lead for that word first, and report the answer before your first edit.

## Why this exists

On 2026-07-28 a session wrote its own handover at 21:40 from memory. That handover named a question as waiting for the owner. The owner had answered the question at 19:55 in the same session.

The evidence sits at `docs/handovers/2026-07-28-readability-campaign-handover.md`, lines 80 and 81, under the heading `## What waits for the owner`.

A session that lived the work is a poor reader of its own record. The owner asked for a cheap agent to read the previous session instead.

His ask at 21:58 local time, in English. Does it make sense to always have a cheap agent read the previous session, as a process, always?

He wrote that ask in Russian. It sits in the session transcript for 2026-07-28, at that timestamp.

## What you build, in three parts

**Part one is a script.**

It extracts the owner's own turns from a session transcript and writes them into one compact file.

**Part two is the closing step of a session.**

The handover file is written by a fresh agent session that reads the extract. The session that lived the work no longer writes its own handover.

**Part three is the opening step of a session.**

A fresh agent reads the previous session's extract. It lists every decision the owner made, each with its timestamp.

That list is compared against `DECISIONS.md` and `NEXT_STEPS.md`. A decision missing from both is reported to the session lead before any work starts.

## The transcripts, and the traps in them

Session transcripts are JSON Lines files. One JSON object sits on each line.

The files for this repository live under `/Users/sashaabramovich/.claude/projects/-Users-sashaabramovich/*.jsonl`. There are 395 of them today.

Each line carries a `timestamp`, a `type` of `user` or `assistant`, a `message` object, and a `cwd`. A line also carries some of `isMeta`, `isSidechain`, `toolUseResult`, `sessionId`, `uuid`, `gitBranch`, and `version`.

Four traps sit in this data. Each one was checked against the real files on 2026-07-28.

**The wrong directory looks right.** The sibling directory `-Users-sashaabramovich-live-spec` holds 1043 files. They are one-shot machine calls, and they hold no human turns. The real conversations live in the top-level `-Users-sashaabramovich` directory.

**The working directory changes mid-file.** A session's opening human turns carry `cwd` of `/Users/sashaabramovich`. The value becomes `/Users/sashaabramovich/live-spec` only after the first tool call inside the repository. So a line-by-line filter on `cwd` drops the very turns that open a session.

Pick a whole file when any line in it names the repository path, and then read every human turn in that file.

**A `user` line is usually a machine.** One live transcript held 8 human turns against 34 machine lines of the same `type`. A machine line carries a `toolUseResult` key, or a `message` content list holding only tool results.

A human turn is a `user` line carrying no `toolUseResult` key, with `isSidechain` false and `isMeta` absent or false. Its content is a string, or a list holding a `text` block.

**The harness writes in the human's slot.** Some human-typed turns are wrappers the harness generated: `<local-command-caveat>`, `<command-name>`, `<command-message>`, `<command-args>`, and `<system-reminder>`. Drop a turn whose text is one of those wrappers, and strip such a block out of a turn that also carries real words.

## What the script writes

The output is one compact file. Each human turn takes its timestamp and its text.

The point of the file is size. A cheap model reads kilobytes of it, where the raw transcript runs to megabytes.

The script lives in `scripts/`. Use the standard library alone. Match the house style of the scripts already in that directory. They open with a docstring naming the rule they serve, a `Usage:` block, and the exit codes.

`scripts/needle-extract.py` and `scripts/rule-census.py` are two neighbours to read for that style.

## Where the extract goes

The extract goes to a scratch directory. It never enters this repository.

A transcript holds private conversation. The one exception is a decision entry in `DECISIONS.md`, which owes its evidence in the owner's own words.

Add the extract's own filename pattern to the repository's ignore rules if a plausible run could drop one here.

## The pipeline you work by

The method is `skills/build-pipeline/SKILL.md`. Its shared rules live in `skills/live-spec-base/SKILL.md`. Read both before your first edit.

Hold this order, and report each step as you finish it:

1. Acceptance criteria into `PRODUCT_SPEC.md`.
2. The generated index rebuilt, both copies of it.
3. New rows in `TEST_MATRIX.md`, and the matrix Reference rebuilt.
4. A test per new row, run and seen red against the current code.
5. The code, until every one of those tests is green.
6. The full suite, read from its log.

## Finding the requirement neighbours

Your criteria belong beside the requirements that already govern a session's lifecycle, and beside any existing rule about a handover. Find those requirements yourself.

Appending at the end of the specification is the wrong move. A rule about a session's close belongs where a reader of the session rules meets it.

Four requirements are worth reading as you search. Judge for yourself whether each is a neighbour:

- Requirement 25 at `PRODUCT_SPEC.md:784`, on the leave-word and the resume file;
- Requirement 93 at `PRODUCT_SPEC.md:2161`, on a deferred item re-derived before its work resumes;
- Requirement 126 at `PRODUCT_SPEC.md:2828`, on a landing closing its checkpoints;
- Requirement 127 at `PRODUCT_SPEC.md:2843`, on the resume file as a capped digest.

Search the specification for the word "handover" as well, and report what you found.

## The numbers you take

`NEXT_STEPS.md` names the free numbers at lines 87 to 89: requirement 303, INV-302, E-36, T-25, M-480, queue row 520.

Those numbers may have moved by the time you start, because another worker takes numbers today. Re-read that line, take the numbers you need, and raise the free number in the same edit.

## Rebuilding the generated tables

New criteria change the code-to-location table. Rebuild it with `python3 scripts/build-index.py PRODUCT_SPEC.md -o PRODUCT_SPEC.index.md`.

The same table is embedded in the specification under `## Reference`, and the two copies must match line for line. The equality is asserted by `tests/test_formal_index.py::test_committed_index_equals_embedded_table`.

Rebuild the matrix Reference with `python3 scripts/build-matrix-reference.py TEST_MATRIX.md -o <file>` and splice the table back. Its push gate is `guardrails/check-matrix-reference.py`.

## Where the two steps are enforced — your own design call

A rule that lives in prose alone is a rule a busy session skips. Decide where each of the two steps is held, and say why.

Three homes stand open, and each carries its own cost:

- a session hook under `hooks/`, installed by `scripts/install-session-hooks.sh` and declared in `guardrails/judge-hooks.json`;
- a push gate under `guardrails/`, wired into `guardrails/pre-push`;
- a rule in `skills/live-spec-base/SKILL.md`, held by a session's own discipline.

Read `guardrails/judge-hooks.json` before you choose the hook road. Requirement 292 at `PRODUCT_SPEC.md:6934` obliges every session hook to carry a known-red proof, held in `guardrails/hook-red-proofs.json`. Requirement 298 at `PRODUCT_SPEC.md:7121` obliges the installer to wire every declared hook.

A push gate owes an entry in `guardrails/gate-red-proofs.json` and a gate letter of its own.

State your call and its reason twice: in the code's own docstring, and in the acceptance criteria you write.

Answer one more question in the same place. A hook cannot make an agent spawn a reader, so name what your chosen home actually enforces, and name what stays with the session's discipline.

## What you must not touch

Wait for the lead's word before you touch anything. The two workers in flight hold `PRODUCT_SPEC.md`, `PRODUCT_SPEC.index.md`, `TEST_MATRIX.md`, `hooks/chat-law-hook.sh`, `scripts/rule-census.py`, `guardrails/check-doc-findings-bound.py`, and files under `tests/` and `docs/language-reads/`.

Make every change as a targeted edit to the lines you mean to change. A whole-file rewrite in a shared tree destroys another worker's concurrent edit.

Commit nothing and push nothing. The session lead does that.

Re-seed `guardrails/rule-census.json` never. A re-seed is no way to make a check green.

Leave `JOURNAL.md` and `ROADMAP.md` to the session lead. Report the line each of them owes.

Never write `guardrails/rule-census.json` from a test. A test that re-seeds the real record destroys it for everyone else working today.

## The writing standard your prose is held to

Every document this repository ships is measured. Keep each sentence at or under 25 words. Use plain product words. Keep an internal code out of the front of a sentence, where it names nothing to a reader. A sentence that names a thing by denying its neighbour is refused.

`PRODUCT_SPEC.md` is recorded at 1831 findings and measures 1831 findings, so it carries no headroom at all. One over-cap sentence added to it reds gate aa on the next push. `TEST_MATRIX.md` is recorded at 76.

Measure your own prose before you report, with `python3 scripts/rule-census.py <file>` over each document you changed. The count it prints must be the count that stood before your edit.

## The checks that close the work

Run each command from the repository root and record what it printed:

1. `python3 scripts/rule-census.py PRODUCT_SPEC.md TEST_MATRIX.md`
2. `python3 scripts/preshow-register-lint.py <file>` over each file you edited
3. `python3 guardrails/check-criterion-readability.py PRODUCT_SPEC.md`
4. `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md`
5. `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md`
6. `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md`
7. `python3 guardrails/check-doc-findings-bound.py`
8. `python3 guardrails/check-every-gate-can-fail.py`, when you added a gate
9. `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the counts out of that log

Write the suite log to your scratchpad directory. Read its last line for the counts. An exit status is no test result, so quote the log.

## What done means

Report these eight things, each one checkable by a reader:

- the list of files you changed, one line each, with what changed in it;
- the new acceptance criteria, quoted from the specification as they now stand, with the requirement each one joined;
- why you placed them there, naming the neighbour requirement you found;
- the new matrix row ids and the level each one pins;
- the name of each new test, its red output before the code, and its green output after;
- one real run of the script over one real transcript, giving its path and the human turns it found;
- the size of that raw transcript beside the size of the extract it produced;
- the full-suite counts quoted from the suite log;
- the census count for every document you edited, beside the count it held before.

Report where you put the enforcement of each of the two steps, and the reason you chose it. Report what your chosen home enforces, and what stays with the session's discipline. Report anything you found and left alone.
