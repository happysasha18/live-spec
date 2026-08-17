# Prover record — 2026-08-18 the spec-author pin repoint, the attic pins, and the suite-size figure

PUSH-REVIEW

This record exists because `guardrails/check-prover-record.sh` reddened on freshness: the newest
committed record, `docs/prover/2026-08-17-slimdown-pin-renumber.md`, predates the last
`ARCHITECTURE.md` change, and `M-6`/`INV-116` want the prover pass to cover the architecture. The
architecture changed three times in this range — `011158b` repointed six pins into the spec-author
node, `6d1a2a6` repointed eight references into `guardrails/attic/` and corrected the suite-size
figure, and `cbdf3f8` carried an earlier lane's edit in on a merge.

Range: db01da2..75c4377 (base db01da2, the remote head; 37 commits in the range, listed below;
`ARCHITECTURE.md` itself is touched by `011158b`, `6d1a2a6`, `cbdf3f8` and the merge `b2ace4f`.
The coverage this pass actually gives each of the 37 is stated under Findings rather than implied
by the listing — see the coverage note there, which is the first thing a later auditor should read.)
- 75c4377 Merge branch 'night/2026-08-18-watchman' into night/2026-08-18-integration
- c6ec64a The two neighbour cases skip where the gate has no repository to read
- b2ace4f Merge branch 'night/2026-08-18-specauthor' into night/2026-08-18-integration
- 1b3ffe2 Merge branch 'night/2026-08-18-delta-extend' into night/2026-08-18-integration
- 1fd80f0 A criterion added under a code that already exists now has an honest answer
- 080f7ce Merge branch 'night/2026-08-18-attic' into night/2026-08-18-integration
- 6d1a2a6 The architecture aims at the parked checks, and states the suite size the tree collects
- fcf453b Merge branch 'night/2026-08-18-entrydocs' into night/2026-08-18-integration
- 104bc92 The install steps read in short sentences, and every fact they gained stays
- 0aa35fb Merge branch 'night/2026-08-18-attic' into night/2026-08-18-integration
- e442f8c Gate g runs locally only when the push can move a pin
- 228cbcd Three checks wired into nothing move to the attic
- 04d23d2 Three checks that could not fire move to the attic
- c466d3e The progress report goes back to the base's copy — it is protected tonight
- 030b36f Merge branch 'night/2026-08-18-machinery' into night/2026-08-18-integration
- 01a3c3f The owner's words on the record stand whole, and the question he answered stands with them
- 151130b The short chat-law reminder is on record as the norm for every host
- 134624b Merge remote-tracking branch 'origin/main' into night/2026-08-18-integration
- b2ff6e3 The local push chain runs the fast set, and the whole suite stays the server's job
- d85aa28 The README sentence comes back under the length cap, and the two reports catch up
- 4eeaf6f Merge branch 'night/2026-08-18-machinery' into night/2026-08-18-integration
- 66635ff The language rules and the reading-discipline test point at the short hook
- b145cea Every command in the install section can be typed, and a project with no remote passes
- b4d00f8 The worker-restore gate reds on this project's own sessions, and carries another project's finding as a notice
- 665e2c1 Install by the README and the four checks actually come up green
- da984a2 The night's records carry the wall-clock date they were written on
- 966db35 The census, the README counts and the two prose pages catch up with the offload
- fec8f98 A newcomer can install the pack by either road and knows what the words mean
- 80bc97a The language rules name the spec-author file each source now lives in
- 011158b The pins into spec-author point at where the words now stand
- d48b8a3 The repository carries the short chat-law hook, and its records say what it prints
- 08c361d The spec-author bookmarks read the whole skill surface, not the body alone
- 37ff032 spec-author: nine sections move to references, word for word
- 07a3c70 The size ceilings come down to what the files actually measure
- c928d35 The queue body drops its nine finished rows into the August archive
- cbdf3f8 Merge branch 'readability/2026-08-17' into night/2026-08-18-entrydocs
- bc7b9fe README: split the two install roads, and define the dialect at first use

Files read: `ARCHITECTURE.md` lines 95-120 (the spec-author node) and its whole `db01da2..HEAD` diff
hunk by hunk; `skills/spec-author/SKILL.md` at `37ff032^` at lines 161, 228, 254, 340, 356 and 381,
and the current body at line 98; the four moved-into reference files
`skills/spec-author/references/the-spine.md` (lines 1 and 27),
`references/facet-sweep.md` (lines 1 and 26), `references/how-it-reads.md` (line 68); the six parked
checks `guardrails/attic/check-far-tier.py`, `check-wrong-referral.py`, `check-listener-tripwire.py`,
`check-description-field.py`, `check-index-prose.py`, `check-release-note.py`, each at its own
docstring head, plus the `--window` help text in `check-far-tier.py`; `guardrails/archformat.py` in
full, `guardrails/node-file-cap.json`, `guardrails/check-prover-record.sh` in full;
`tests/test_architecture_format.py` and `tests/test_architecture_pins.py` for their treatment of pin
paths; `docs/prover/README.md`; `docs/prover/2026-08-17-slimdown-pin-renumber.md` for the form.

Checks run: `bash guardrails/check-pin-drift.sh` — exit 0, **207 pins proved** (63 line pins against
their own line at ±2 tolerance, 138 file-level `:1` pins, 6 unlabelled) plus 53 r5 range pins, with
all six `guardrails/attic/` paths and all three `skills/spec-author/references/` paths present in the
reach list; `python3 -m pytest -q tests/test_architecture_format.py tests/test_architecture_pins.py
tests/test_node_growth.py` — **26 passed, 1 skipped** in 0.96 s; `python3 -m pytest --collect-only -q`
— **2555 tests collected** in 0.66 s; `git show --stat 37ff032` — nine reference files added, 534
lines out of the body; a direct existence check that none of the six parked checks remains at
`guardrails/<name>.py`; and the six-pin both-ends read described under Findings.

Findings: no blocking finding, one figure this record corrects against the architecture's own text,
and the coverage limits below. Every pin claim in this record was verified by reading BOTH ends —
the old line in the pre-move file and the new line in the file it now names — not by trusting the
commit message. What follows separates what I SAW from what I ACCEPTED.

Blocking: none.

## 1. The six spec-author pins — all six SEEN at both ends, all six correct

For each pin I read the pre-move body at `37ff032^` at the old line number, and the current file at
the new line number, and compared the material against the pin's own parenthetical label. All six
land on the exact line the label names. None lands on a plausible neighbour.

| label | old | new | what stands at both ends |
|---|---|---|---|
| spine | `SKILL.md:228` | `references/the-spine.md:1` | the heading `## The spine — what every spec must contain (not its section order)`, identical |
| [target] tag tripwire | `SKILL.md:254` | `references/the-spine.md:27` | the paragraph opening `**Name the future with the [target] tag — it is a tripwire that drives the pipeline.**`, identical |
| axes composition | `SKILL.md:381` | `references/facet-sweep.md:26` | the paragraph opening `**Read the surface's composition axes from the kind too (SPEC INV-244).**`, identical |
| fences | `SKILL.md:340` | `SKILL.md:98` | the heading `## The regression fences — run first when the wish touches a surface that already lives (SPEC T-14, INV-19)`, identical — this section stayed in the body and was renumbered, exactly as claimed |
| facet sweep — the canonical facet list | `SKILL.md:356` | `references/facet-sweep.md:1` | the heading `## The facet sweep — run when a wish's door says feature (SPEC T-13, INV-18)`, identical, and the phrase **canonical facet list; its home is here** stands four lines below it, so the label's "canonical facet list" is carried by the target's own text |
| the enumeration-threshold structure rule, INV-215 | `SKILL.md:161` | `references/how-it-reads.md:68` | the bullet opening `- **The enumeration threshold makes that checkable (SPEC INV-215).**`, identical, with the same preceding line `reasoning that connects them.` in both |

Each new target is a first line of its own material, not an interior line that merely mentions the
subject. The `fences` pin is the one that did NOT cross into `references/`, and reading it confirmed
the claim rather than assuming it: `## The regression fences` is still in the body, at 98.

## 2. The node's facts did not change — SEEN

The whole `db01da2..HEAD` diff of `ARCHITECTURE.md` touches the spec-author node in exactly one hunk,
`@@ -100,12 +100,12 @@`, and every changed line inside it is a pin line. The `**responsibility**`
line, both `**owns**` lines (the 17-code line, the `INV-248` line and the
`INV-150 · INV-167 · INV-168 · E-33 · INV-185 · INV-186 · INV-187 · INV-215` line) and both
`**notes**` bullets are unchanged context in the diff. No code was added, removed or renamed; no
label text changed; the six labels are byte-identical before and after, and only the addresses moved.
The node owns what it owned.

## 3. Pins crossing into `references/` — legitimate, but by silence rather than by rule

This is the one place where I will not report more certainty than I found.

`guardrails/archformat.py` parses a pin with `PIN_RE = re.compile(r"`([^`]+:\d+)`(?:\s*\(([^)]*)\))?")`.
The path half is `[^`]+` — any text that is not a backtick. The format has **no notion of which file a
pin may name**. A `references/` path is neither privileged nor forbidden; it is simply unconstrained,
exactly as a `SKILL.md`, a `guardrails/*.py` or a `templates/*.md` path is. I read
`tests/test_architecture_format.py` and `tests/test_architecture_pins.py` for a path constraint and
found none: neither file mentions `references/` at all.

Ownership is unaffected because ownership is not a function of pins. A node owns the codes listed
under `**owns**`; `**pins**` are addresses, and `archformat.py` reads them only as a feed
(`_emit_pins`) for the drift check. Moving an address changes nothing a node owns.

Co-residence IS a function of pins, and it is worth stating exactly. `guardrails/node-file-cap.json`
defines a file's node count as "the number of distinct nodes whose ARCHITECTURE.md pins name it",
with a default ceiling of two and a ratchet that "points DOWN only". Under that definition the
crossing is benign and slightly helpful: `skills/spec-author/SKILL.md` is still named by the
spec-author node through the `:98` fences pin, so its count is unchanged at whatever it was; the
three `references/` files each enter at a count of 1, well under the default of 2; and no file's
count rises. `tests/test_node_growth.py` passes. Nothing here breaches the ratchet's direction.

**My plain answer to the question asked:** crossing is *tolerated*, not *sanctioned*. The pack's
rules permit it because they never contemplated the question, not because anyone decided it. I
searched for a rule that says a node's pins may name a reference file and found no such rule, and I
searched for a rule forbidding it and found no such rule either. The mechanism is silent. I record
that as a gap in the written format rather than dress it up as permission — a reader who later wants
to forbid or bless the crossing will find nothing in `archformat.py` or the node-format tests to
amend, and will have to write the rule from scratch.

## 4. The eight attic references — all eight SEEN to resolve, all six files carry their label word

`6d1a2a6` repointed eight `guardrails/…` references in `ARCHITECTURE.md` to `guardrails/attic/…`,
covering six parked checks. I counted the eight in the diff (`git diff db01da2..HEAD -- ARCHITECTURE.md
| grep -c '^+.*guardrails/attic/'` returns 8) and read each end.

- `guardrails/attic/check-far-tier.py --window` (communicator node) and `guardrails/attic/check-far-tier.py:1`
  — file present; its docstring opens "the far tier stands down by name" and carries "PARKED
  2026-08-18 in `guardrails/attic/`"; the `--window` flag is real, documented at line 25 as the
  INV-223 cadence-window arm. Label word **far tier** stands in the file's own text.
- `guardrails/attic/check-wrong-referral.py:1` — present; docstring "a wrong referral is named as the
  finding (SPEC INV-225)". Label word **wrong referral** stands.
- `guardrails/attic/check-listener-tripwire.py:1` — present; docstring "the tripwire for the day the
  harness ships a listener (SPEC INV-231, ROADMAP 405)". Label words **listener tripwire** stand.
- `guardrails/attic/check-description-field.py:1` (the `[target]` pin) and the same path in the
  `[E-35]` prose paragraph — present; docstring "the Formal-index non-empty description-field gate
  (SPEC INV-239, M-421)". Label words **non-empty description-field gate** stand.
- `guardrails/attic/check-index-prose.py:1` — present; docstring "a Formal-index code is carried in
  its home prose (SPEC INV-218). Retired from gate x at the row-445 conversion". Label word
  **index-prose** and the word **retired** the architecture's label uses both stand.
- `guardrails/attic/check-release-note.py:1` — present; docstring "a release note may offer the
  reader next-step choices, and the walk records the offer-or-none decision (SPEC INV-228, ROADMAP
  402)". Label words **release-note offer** stand.

None of the six remains at its old top-level `guardrails/` path — checked by direct existence test,
so the old pins would have broken had they not been repointed. `check-pin-drift.sh` proves the six
`:1` pins green and lists all six attic paths in its reach set.

**One of the eight is not a pin the gate can prove, and I say so rather than let the green stand for
it.** `guardrails/attic/check-far-tier.py --window` carries no `:<line>`, so `PIN_RE` does not match
it and gate g never counts it. It sits inside a `**pins**` list looking like a pin while being, to
every machine that reads the file, prose. Its file happens to be reached by the separate `:1` pin, so
nothing is currently broken — but the path in that line is proved by my eye alone, not by the gate.
The eighth reference, in the `[E-35]` prose paragraph near line 754, is likewise ordinary prose and
unproved by gate g; I verified it by reading it. So of the eight repointed references, **six are
gate-proved pins and two are proved only by this reading.**

## 5. The suite-size figure — the record corrects the architecture, not the other way round

`6d1a2a6` changed the wall-time row's parenthetical from "at 2,506 tests" to "at 2,532 tests". My own
collection at `75c4377`:

```
$ python3 -m pytest --collect-only -q 2>&1 | tail -3
2555 tests collected in 0.66s
```

**My number is 2555, and it wins over the record's 2,532.** The figure in `ARCHITECTURE.md` is stale
at HEAD by 23 tests. The cause is visible and is not a defect in `6d1a2a6`: eighteen test files under
`tests/` changed between `6d1a2a6` and HEAD, including `test_composition_axes.py`,
`test_delta_classifier.py`, `test_enumeration_reads_as_list.py`, `test_guardrails_unit.py` and
`test_scenario_entry_exit.py`, arriving on the `delta-extend`, `specauthor` and `watchman` merges
that land after it. A count written mid-integration and then integrated further is stale by
construction.

I did NOT verify that 2,532 was correct at `6d1a2a6` itself. Doing so needs a second worktree at that
commit, and cutting one is outside what this pass may do. So: 2,532 as a claim about `6d1a2a6` is
**accepted, not seen**; 2555 as the count at `75c4377` is **seen**. The row does not red any gate —
`check-suite-budget.sh` reads only the `≤ 1780` seconds figure with `grep -oE '≤ *[0-9]+'`, and the
test count in that sentence is prose no check reads. This is therefore a true statement gone stale,
named here, not a blocking finding.

## Accepted losses and what this pass could not check

Named plainly, because a record that lists only its successes is a record that hides its shape.

- **Coverage.** This pass is the `M-6`/`INV-116` architecture re-check the gate reddened for. It is
  NOT a full adversarial read of all 37 commits in `db01da2..75c4377`. I read `ARCHITECTURE.md` and
  the files its pins name. The install-road commits (`bc7b9fe`, `b145cea`, `665e2c1`, `104bc92`),
  the chat-law hook commits (`d48b8a3`, `151130b`, `66635ff`, `01a3c3f`), the census and report
  commits (`966db35`, `c466d3e`, `d85aa28`), the push-chain change `b2ff6e3`, the gate-g locality
  change `e442f8c`, `1fd80f0`, `c6ec64a` and `07a3c70` are named in the Range and were NOT read by
  me. Anyone treating this record as the adversarial read of the whole range would be treating it as
  something it does not claim to be.
- **The word-for-word claim of `37ff032` is accepted, not proved.** I proved six specific passages
  identical at both ends. I did NOT re-run a whole-corpus sentence-stream comparison across the nine
  moved sections the way the 2026-08-17 record did for its three skills. The move's own commit says
  "word for word" and the stat line (534 out of the body, 561 into nine files) is consistent with it,
  but consistency is not proof, and I am not reporting it as one.
- **`2,532` at `6d1a2a6`** — not checked, as stated above.
- **The `--window` reference and the `[E-35]` prose reference** — proved by my reading only; no gate
  covers either.
- **The prover gate was run on the WORK road only.** `bash guardrails/check-prover-record.sh` with no
  `--push` never reaches the range, field-shape or blocking-parser arms. This record carries the
  `PUSH-REVIEW` marker and all five fields, and names the base and every commit in the range, so the
  push road's arms should also find it sound — but I did not run them, and the 2026-08-17 record's
  gate-a finding is the standing warning that a shape certified on the work road can still be
  rejected by the real gate.

## What the gate said

```
$ bash guardrails/check-prover-record.sh
OK (prover record): committed record(s) for 2026-08-18 found:
  docs/prover/2026-08-18-specauthor-pins-and-attic.md
OK (freshness): record commit is not older than the last PRODUCT_SPEC.md commit.
OK (freshness): record commit is not older than the last ARCHITECTURE.md commit.
```
