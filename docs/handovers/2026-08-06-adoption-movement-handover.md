# Handover, 2026-08-06 — the adoption movement, stopped mid-landing on purpose

transcript: `/Users/sashaabramovich/.claude/projects/-Users-sashaabramovich/555af883-33bf-4b23-9996-f27461eea82a.jsonl`
written by: the working session itself, at Alexander's word to keep the state and restart clean.
The three previous sessions closed with no handover at all, which is why he has no record of the work
and why this file exists before the restart rather than after it.

The session ran from 2026-08-06 11:33 to about 16:30 on the local clock.

## Read this first, in one paragraph

Three changes were designed, formally reviewed, reworked, built, tested and document-landed today.
None is committed. The working tree holds 37 changed or new paths and `HEAD` is `9b3a666`. A fourth
change, the public prover edition's readability, is repaired in the tree and blocked on seventeen
edits to a file no worker held. The suite reads `5 failed, 2469 passed in 472.06s`, and every failure
has a named owner and a one-line fix, listed below. Nothing is lost and nothing is half-written; the
work stopped at a clean boundary.

## Where the work stands

`git status` shows 37 paths. Nothing is staged and nothing is committed. One landing lives on a
separate branch, `worktree-agent-ae20723e3138ec236`, commit `9a5df02`, in the worktree at
`.claude/worktrees/agent-ae20723e3138ec236` — its files are absent from the main tree and must be
merged before its matrix rows can move off *todo*.

## What was built today

**Published counts are counted by a machine.** A number this project publishes about its own tree is
now measured by a script and held by a gate on the push chain (gate ad, Requirement 306, INV-305,
queue row 555). The page that declared thirteen push checks while twenty-nine run is generated from
the push hook itself. A count of worker runs that no command could reproduce no longer states a
number and prints the command instead. Tests were watched red first, and six red proofs were
performed and reverted with the files restored byte-exact.

**Every check has a record of what it is.** `scripts/check-registry.json` records, for each runnable
file a skill body names, what kind of thing it is, which tree it judges, what it reads, and whether
it belongs in a project that adopts the pack (gate ae, Requirement 307, INV-306, queue row 556). It
found and fixed two places where the text-audit skill told a stranger's project to run checks that
only measure this pack's own documents. This landing is the one on the branch.

**The words on the front page load a walk.** Saying "attach live-spec to this project" now reaches a
real procedure, and a brand-new project has a founding walk for the first time (Requirement 308,
INV-307, queue row 557). It was proven by founding an actual throwaway project end to end, with three
reds proven: an unfilled configuration exits non-zero, a second run keeps the person's own sentences,
and a renamed template fails by name.

**The public prover edition is repaired for a stranger's eye.** Two cold readers read it — one under
the printed rule list, one holding no rules and no background. They returned twelve blocking stops
and one shared verdict: publish the full output of one real run, and cut the length. The README fell
from 2,919 words to 1,938. Alexander then ruled that the prover assumes no product kind at all, and
the readings were rewritten to hold for a service, a protocol, a library, a pipeline, a command-line
tool, or a screen.

## What is owed, in the order it should be taken

1. **Seventeen edits to `editions/product-prover/reference/stress-lenses.md`.** The repaired README
   now claims the method assumes no product kind, and that file still carries screen-bound readings,
   so the page states something its own package contradicts. The exact edits, quoted old and new, are
   in the repair worker's report. **The edition must not be published before these land.**
2. **Merge the branch** `worktree-agent-ae20723e3138ec236` and move matrix rows M-505 to M-511 off
   *todo*, then add the two architecture pins held back because they pointed at files not yet in the
   main tree.
3. **Re-run the two-run measurement of the prover edition.** A run was made today and must be thrown
   out: it measured the skill text while that text was being rewritten in parallel. The record is
   worthless and the mistake belongs to the session, not to the worker. Re-run it against the
   repaired text, then splice the real numbers into the marked placeholder at `README.md` line 51 of
   the edition.
4. **The five suite failures**, each with its fix: `tests/test_setup_entry.py` needs pinning into the
   `ALWAYS_SCOPED` block of `guardrails/check-push-reach.sh`; `scripts/sync-skills.sh` clears the two
   installed-copy drifts; `scripts/rule-census.py --json guardrails/rule-census.json` refuses to write
   while the two prover-edition files stand above their ceilings, so item 1 clears it; the
   suite-in-suite test inherits the rest.
5. **The freeze baseline**, `python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md
   TEST_MATRIX.md --compaction`, after the documents settle.
6. **`python3 scripts/gen-tree-counts.py` last of all**, because the skill tree grew during the work
   and the new gate catches exactly that drift.

## New queue rows opened today

555, 556, 557 carry the three landings and close at the push. 558 makes the session's opening read
leave an artifact and refuses a push from a session that wrote none. 559 puts a machine behind the
two-reader panel. 560 parks the naming of the surface registry on Alexander's word. 561 gives the
settings ladder a line naming where the pack's own tree lives. Row 166 was widened rather than
duplicated, to carry the record of completed work, per-row tags, per-step outcomes, and named
workers.

## What Alexander decided today

The prover assumes no product kind. Every reading states itself in terms any kind of product can meet.

Fable takes the orchestrator seat in the next continuation of this work.

The record of what was done belongs to the work board rather than standing as its own feature.

## What he asked for that is designed and unbuilt

A work board with tags, per-row plans whose steps each name their outcome, a live view of which
worker holds what, named workers with distinct voices, and a record a person can read to answer
"what was done" without asking the session. Row 166 holds it. He also asked for the reading bar to
become reachable; that design is at `scratchpad/design-D-reading-bar.md` in the session's scratch
directory and is summarised in row 559.

## Where this session failed, so the next one does not repeat it

The opening read of the previous session never happened. The session read the status documents and
started work, and Alexander had to ask for the sweep himself. It then found five of his asks from
earlier sessions that had been answered in chat and given no owner.

A measurement was run in parallel with a repair of the very text being measured. Both workers were
correct in isolation and the record they produced is void.

The first report of a finished landing was written in the project's internal vocabulary and he could
not read it. The plain-language rule has a written home and no machine holding chat, which is the
same class as the two failures above: a rule stated and unheld.

## To rebuild the picture from scratch

`python3 scripts/session-extract.py --session 555af883 --out <a path outside the tree>` pulls this
session's turns.

Everything the session produced outside the repository is copied to `~/live-spec-carry/2026-08-06/`,
which survives the session's own scratch directory. It holds the three designs, their three formal
reviews, the three reworked designs, the two cold readings of the prover edition, the reading-bar
design, the two skill-creator reviews, and every worker's full report. Two files there are
load-bearing:

- `a37080c376a46f44a.output` — the prover-edition repair report, holding the seventeen exact edits
  `reference/stress-lenses.md` needs. Item 1 above cannot be done without it.
- `design-D-reading-bar.md` — the reachable reading bar, which queue row 559 summarises and does not
  contain.

Anything from that directory which must live permanently goes into the repository on the next pass.
