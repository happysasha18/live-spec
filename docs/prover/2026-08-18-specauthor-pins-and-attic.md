# Prover record — 2026-08-18 the spec-author pin repoint, the attic pins, and the suite-size figure

PUSH-REVIEW

This record exists because `guardrails/check-prover-record.sh` reddened on freshness: the newest
committed record, `docs/prover/2026-08-17-slimdown-pin-renumber.md`, predates the last
`ARCHITECTURE.md` change, and `M-6`/`INV-116` want the prover pass to cover the architecture. The
architecture changed four times in this range — `011158b` repointed six pins into the spec-author
node, `6d1a2a6` repointed eight references into `guardrails/attic/` and refreshed the suite-size
figure, `cbdf3f8` carried an earlier lane's edit in on a merge, and `0ce20c8` refreshed the suite
size again to the number this pass measured.

**This record was extended twice.** The second extension, at the bottom, covers the three readability
lanes that rewrote `build-pipeline`, `communicator` and `live-spec-base` and moved 35 architecture
pins with them. It also carries the honest red: the pin gate's second leg is failing, on rot that
predates every line of tonight's work.

**This record was extended once.** It first landed at `3b73943` covering `db01da2..75c4377`, and the
gate was green on it. Two commits then landed in the same branch — `0ce20c8` and `6fa3062` — and
`0ce20c8` touches `ARCHITECTURE.md`, which reddened the freshness arm again and with it
`tests/test_guardrails.py::TestGateA_ProverRecord::test_real_repo_passes`. The extension below covers
both. I read those two commits myself; what I saw and what I merely accepted is marked as everywhere
else in this record.

Range: db01da2..a5d61a6 (base db01da2, the remote head; 59 commits in the range; the 39 through
`6fa3062` are listed below, and the 16 of the readability lanes that followed are listed in the
extension's own section 7, so each block sits beside the reading that covers it;
`ARCHITECTURE.md` itself is touched by `011158b`, `6d1a2a6`, `cbdf3f8`, the merge `b2ace4f` and
`0ce20c8`, and by `8a920ee`, `4d3d8fc`, `9c06806` and the merges `bb0f48a` and `a5d61a6`. The
coverage this pass actually gives each of the 59 is stated under Findings rather than implied by the
listing — see the coverage note there, which is the first thing a later auditor should read.)
- 6fa3062 The architecture ceiling pays for two path repoints, and nothing else
- 0ce20c8 The budget row states the suite size the merged tree collects
- 3b73943 The prover record covers the spec-author pin repoint, the attic pins and the suite size
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
docstring head, plus the `--window` help text in `check-far-tier.py`; `guardrails/doc-bounds.json`;
`guardrails/archformat.py` in
full, `guardrails/node-file-cap.json`, `guardrails/check-prover-record.sh` in full;
`tests/test_architecture_format.py` and `tests/test_architecture_pins.py` for their treatment of pin
paths; `docs/prover/README.md`; `docs/prover/2026-08-17-slimdown-pin-renumber.md` for the form. For
the extension: the full diffs of `0ce20c8` and `6fa3062`, `guardrails/doc-bounds.json`'s
`ARCHITECTURE.md` entry in full including its whole `reason` field, `guardrails/check-doc-bound.py`,
and `tests/test_doc_bound.py` for its `FOUR_DOCS` list. For the second extension: the whole
`25acaf5..HEAD` diff of `ARCHITECTURE.md`; `skills/live-spec-base/SKILL.md`,
`skills/build-pipeline/SKILL.md` and `skills/communicator/SKILL.md` at `25acaf5` and at HEAD, at
every pin line sampled and at the rule headings around them; `skills/build-pipeline/SKILL.md` at
`d11331f` and `db01da2` in full for the rule positions; `.live-spec/r5-rule-prices-2026-08-11.md`
(its header, its method section and all nine build-pipeline rows); `guardrails/check-pin-drift.sh` in
full, including `label_words`, the `FURNITURE` list and both legs' matching loops;
`.live-spec/culling-plan-v3-2026-08-10.md` at its R5 and queue lines; and the tip commit and diff of
`morning/2026-08-18-r5-remeasure`.

Checks run: `bash guardrails/check-pin-drift.sh` — exit 0, **207 pins proved** (63 line pins against
their own line at ±2 tolerance, 138 file-level `:1` pins, 6 unlabelled) plus 53 r5 range pins, with
all six `guardrails/attic/` paths and all three `skills/spec-author/references/` paths present in the
reach list; `python3 -m pytest -q tests/test_architecture_format.py tests/test_architecture_pins.py
tests/test_node_growth.py` — **26 passed, 1 skipped** in 0.96 s; `python3 -m pytest --collect-only -q`
— **2555 tests collected**, run twice, at `75c4377` (0.66 s) and again at `6fa3062` (0.48 s), the
same number both times; `git show --stat 37ff032` — nine reference files added, 534 lines out of the
body; a direct existence check that none of the six parked checks remains at `guardrails/<name>.py`;
`wc -c ARCHITECTURE.md` — **107774**, and `git show HEAD:ARCHITECTURE.md | wc -c` — 107774, the same;
`python3 guardrails/check-doc-bound.py` (gate z) — exit 0, "every growable doc sits within its
declared bound … 5 docs read", re-run at the final HEAD with `wc -c ARCHITECTURE.md` still **107774**
and `max_bytes` still 107774; `bash guardrails/check-pin-drift.sh` re-run at the final HEAD — **exit
1**: first leg green at 207 pins, second leg FAILED on one r5 entry, reported in full in section 9;
a replica of the r5 leg's matching rule written from the script's own source and validated against
the real gate at HEAD, then run at `d11331f`, `db01da2` and `25acaf5`; a byte measurement of the nine
build-pipeline rule bodies at `d11331f` and at HEAD against their recorded prices; an independent byte-arithmetic reconstruction of the ceiling rise,
computed from the pin lines themselves rather than read off the commit's reason field; and the
six-pin both-ends read described under Findings.

Findings: no blocking finding, one figure this record corrects against the architecture's own text,
and the coverage limits below. Every pin claim in this record was verified by reading BOTH ends —
the old line in the pre-move file and the new line in the file it now names — not by trusting the
commit message. What follows separates what I SAW from what I ACCEPTED.

Blocking: none.
- stands: the r5 leg of `check-pin-drift.sh` reds on one entry, `skills/build-pipeline/SKILL.md:385-403`.
  It is not blocking and it is not closed. It stands because the rot predates this range — proved at
  the base commit in section 9 — and because closing it means remeasuring prices that feed a frozen
  plan, which is the owner's decision. Named here rather than left for him to meet cold.

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

**My number was 2555 against the row's 2,532, and my number won.** The figure was stale at
`75c4377` by 23 tests. The cause was visible and was not a defect in `6d1a2a6`: eighteen test files
under `tests/` changed between `6d1a2a6` and `75c4377`, including `test_composition_axes.py`,
`test_delta_classifier.py`, `test_enumeration_reads_as_list.py`, `test_guardrails_unit.py` and
`test_scenario_entry_exit.py`, arriving on the `delta-extend`, `specauthor` and `watchman` merges
that land after it. A count written mid-integration and then integrated further is stale by
construction.

**Closed by `0ce20c8`, and re-measured rather than assumed.** That commit changes exactly one line of
`ARCHITECTURE.md` — a single insertion and a single deletion, the budget row — and the only figure
that moves in it is `at 2,532 tests` → `at 2,555 tests`. I confirmed by extracting every `at 2,5NN
tests` occurrence from its diff: the removed side carries `2,532` and `2,502`, the added side `2,555`
and `2,502`, so the historical `2,502` in the row's provenance tail is untouched and only the live
figure moved. That is the narrowest possible edit for the correction, and it is the correction this
pass asked for.

**Re-collected at the new HEAD, because a merge can move the number again.** At `6fa3062`:

```
$ python3 -m pytest --collect-only -q 2>&1 | tail -2
2555 tests collected in 0.48s
```

**2555, unchanged from my measurement at `75c4377`.** The row and the tree now agree. My own
collection remains the authority here, including over my own earlier number — it simply happens that
the two runs match.

I still did NOT verify that 2,532 was correct at `6d1a2a6` itself. Doing so needs a second worktree at
that commit, and cutting one is outside what this pass may do. So: 2,532 as a claim about `6d1a2a6`
is **accepted, not seen**; 2555 at `75c4377` and again at `6fa3062` is **seen, twice**. The row reds
no gate either way — `check-suite-budget.sh` reads only the `≤ 1780` seconds figure with
`grep -oE '≤ *[0-9]+'`, and the test count in that sentence is prose no check parses.

## 6. The ceiling raise in `6fa3062` — arithmetic reconciles to the byte, and the margin is zero

`guardrails/doc-bounds.json` raises `ARCHITECTURE.md`'s `max_bytes` from 107700 to 107774. I read the
diff rather than the summary of it, and I reconstructed the number instead of accepting the reason
field's account of it.

**The measured size, SEEN.** `wc -c ARCHITECTURE.md` is **107774**, and the committed blob measures
the same (`git show HEAD:ARCHITECTURE.md | wc -c` → 107774), so the working tree and the commit
agree. `max_bytes` is **107774**. The two are equal **to the byte**. No discrepancy — the claim "the
file's measured size exactly" is true, and I checked it rather than repeat it.

**The margin is zero, and that is the finding.** Equality is not a violation here: gate z passes
(`check-doc-bound.py` → exit 0, 5 docs read), and it tolerates equality for this file because
`tests/test_doc_bound.py`'s `FOUR_DOCS` is `["PRODUCT_SPEC.md", "ROADMAP.md", "TEST_MATRIX.md",
"JOURNAL.md"]` — `ARCHITECTURE.md` is not among them, so the strict-inequality assertion never
applies to it. I read that list to confirm it rather than trust the reason field's assertion of it.
But it does mean **there is not one byte of headroom**: the next edit to `ARCHITECTURE.md` that adds
even a single character reds gate z until this ceiling is raised again. That is the stated convention
of the entry ("the ceiling is the measured size and the ratchet points down only"), so it is a
designed property rather than an oversight — but a designed property that guarantees the next author
a red is worth naming out loud, and I name it. It is not blocking: nothing in this range needs to
grow the file.

**The cause, checked against the diff and not accepted from the commit message.** I was told the rise
is 48 bytes of attic paths plus 74 bytes of spec-author repointing. I recomputed both from the pin
text itself:

- **48 bytes** — eight places gained the six characters of `attic/`. I had already counted those eight
  in section 4 (`grep -c '^+.*guardrails/attic/'` → 8). 8 × 6 = **48**.
- **74 bytes** — the six spec-author pin lines measure 353 bytes before and 427 after, a delta of
  **+74**. Per pin: the-spine `+13`, [target] `+14`, axes `+16`, facet sweep `+15`, enumeration `+17`,
  and **fences `−1`**.
- 74 + 48 = **122**, and the ceiling rose 107774 − 107652 = **122**. It reconciles exactly, with no
  residue, so no byte of the rise is unaccounted for and none of it is content.

**One nuance the summary I was given does not carry, and I record it rather than smooth it.** "74
bytes for the six pins" is correct as a net, but the composition is five pins up and one pin *down*:
the fences pin `skills/spec-author/SKILL.md:340` → `skills/spec-author/SKILL.md:98` is one byte
SHORTER, because it never crossed into `references/` and its new line number has one fewer digit.
That refines the account rather than contradicting it — the net is what the ceiling pays, and the net
is right — but a reader told "six pins cost 74 bytes" would wrongly infer that each of the six grew.
The reason field in `doc-bounds.json` says "six pins into the spec-author skill were re-aimed at
paths inside references/", which is inexact on its face: only five of the six were, as this record's
own section 1 establishes. The byte figure it justifies is nonetheless exactly right.

**On the down-only rule.** I record the sanction as reported, not as verified: the raise is stated to
be authorised by the owner and the coordinator on the ground that "down-only" governs what a document
says, not how long the paths inside it are. I have **accepted** that authorisation, not witnessed it —
I saw no message from the owner myself. What I can and did verify is the factual premise it rests on:
every one of the 122 bytes is path text, the arithmetic leaves no remainder, and no word of
architecture prose was added anywhere in the two commits. So the premise is sound by my own reading;
the permission on top of it rests on the coordinator's word.

## Accepted losses and what this pass could not check

Named plainly, because a record that lists only its successes is a record that hides its shape.

- **Coverage.** This pass is the `M-6`/`INV-116` architecture re-check the gate reddened for. It is
  NOT a full adversarial read of all 59 commits in `db01da2..a5d61a6`. I read `ARCHITECTURE.md` and
  the files its pins name, plus `0ce20c8` and `6fa3062` in full, and for the readability lanes the
  pin diff and twelve sampled pins at both ends — but NOT the prose rewrites themselves. The three
  skills' bodies were rewritten across sixteen commits and I did not read those rewrites for meaning;
  I checked only that the pins still land on their labels' material. Whether the shortened sentences
  preserve every fact is the skill-review gate's question, and the finding counts quoted to me
  (build-pipeline 211→37, communicator 169→17, live-spec-base 70→20) are **accepted, not seen** — I
  did not run the readability measure. The install-road commits
  (`bc7b9fe`, `b145cea`, `665e2c1`, `104bc92`),
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
- **The authorisation for the ceiling raise is accepted, not witnessed.** The owner's and
  coordinator's word that "down-only" is a law about content and not about path length was relayed to
  me; I did not see it given. Its factual premise I did verify — see section 6.
- **This record's own commits are excluded from the freshness window, and I checked that rather than
  assume it.** The concern is circular: committing the record changes the tree, so a record could in
  principle invalidate itself. It cannot here, on two independent grounds I read for myself. First,
  `check-prover-record.sh`'s freshness arms compare the newest commit touching `docs/prover/` against
  the newest commit touching `PRODUCT_SPEC.md` and `ARCHITECTURE.md` — a record commit moves
  `RECORD_COMMIT` forward and can only ever make the comparison pass, never fail. Second, the size
  gate cannot be tripped either: `guardrails/doc-bounds.json` bounds exactly five documents —
  `PRODUCT_SPEC.md`, `ROADMAP.md`, `TEST_MATRIX.md`, `JOURNAL.md`, `ARCHITECTURE.md` — and nothing
  under `docs/prover/` is among them, which I confirmed by enumerating every bounded key in the file.
  So this record's own bytes are outside every window it must satisfy. The exclusion holds.
- **The prover gate was run on the WORK road only.** `bash guardrails/check-prover-record.sh` with no
  `--push` never reaches the range, field-shape or blocking-parser arms. This record carries the
  `PUSH-REVIEW` marker and all five fields, and names the base and every commit in the range, so the
  push road's arms should also find it sound — but I did not run them, and the 2026-08-17 record's
  gate-a finding is the standing warning that a shape certified on the work road can still be
  rejected by the real gate.

## 7. The readability lanes and their 35 pin repoints — twelve read at both ends, all twelve correct

Sixteen further commits landed after this record's last extension, in three readability lanes that
rewrote the three big skills for shorter sentences. Splitting long sentences moved lines, so
`ARCHITECTURE.md`'s pins into those files had to follow.

The 16:

- a5d61a6 Merge branch 'night/2026-08-18-plainer-base' into night/2026-08-18-integration
- 85772b5 The census records the rulebook at twenty findings
- 9c06806 The shared rulebook says the same things in shorter sentences
- bb0f48a Merge branch 'night/2026-08-18-plainer-bp' into night/2026-08-18-integration
- 4d3d8fc point the communicator pins at the lines the rewrite moved them to
- 8a920ee The architecture pins follow the lines the rewrite moved
- 2d870cd record the communicator's byte count after the condition fix
- 30c642b communicator: put the no-installed-set condition before its instruction
- caae507 refresh the recorded counts after the last communicator edit
- d828c81 communicator: keep the date on the client-asset case and clear two pronouns
- 961f09a build-pipeline: the tripwire list as a list, and the numbers to match
- 92d3b2f build-pipeline: plainer gates section, and the census record it now measures
- ae11951 record the communicator's new finding count and the skill line counts
- 76fe145 communicator: split the long sentences and drop the shouted words
- 2739420 build-pipeline: shorter sentences and plain words through steps 3 to 9
- 359cbfe build-pipeline: shorter sentences and plain words through the door steps

**The repoint's size, counted rather than accepted.** The diff `25acaf5..HEAD` over `ARCHITECTURE.md`
changes 35 pin lines into those three skills: **19 into `live-spec-base`, 10 into `build-pipeline`,
6 into `communicator`**. I was told "about 10 / 7 / 19"; base and build-pipeline match, and
communicator is 6 by my count, not 7. Every changed line in that diff is a pin line — I checked that
no prose, node, owns or notes line moved with them.

**Twelve pins read at both ends, spread across all three skills.** Same method as section 1: the old
line from `25acaf5`, the new line from the tree, each compared against the pin's own label.

| skill | old → new | label | what stands at the NEW line |
|---|---|---|---|
| live-spec-base | 71 → 72 | rules | `## The shared rules` |
| live-spec-base | 136 → 138 | rule 7 fence, INV-10/INV-11 | `7. **The concurrent-edit fence, before every write and every commit.**` |
| live-spec-base | 289 → 293 | rule 19, INV-23 workshop-noise | `19. **The problem ledger — workshop noise is owned, never re-suffered.**` |
| live-spec-base | 564 → 567 | rule 35, INV-302 session extract | `35. **A session's record is read at both ends by an agent that did not live it (SPEC INV-302).**` |
| live-spec-base | 163 → 165 | rule 7's worker-restore sub-rule, INV-298 | `- **A worker never restores a working tree with a git command (SPEC INV-298).**` |
| build-pipeline | 205 → 284 | the work-kind table | `## The work-kind table — what the wish builds scales how each step runs (SPEC T-16, INV-22)` |
| build-pipeline | 487 → 632 | gates | `## Gates worth remembering` |
| build-pipeline | 318 → 417 | re-carve paragraph, INV-113 | `Re-carving the whole node map is legal. It arrives as a restructure placement's own queue row` |
| build-pipeline | 91 → 96 | the craft ladder | `**The craft ladder — which craft's standards judge each step (SPEC INV-33).**` |
| communicator | 291 → 300 | rule 10 — the decision page | `- **Several open picks → ONE interactive decision page.** *(rule 10)*` |
| communicator | 343 → 351 | rule 11 — the evidence walk | `- **"Did we actually do X?" is answered by walking the evidence…** *(rule 11)*` |
| communicator | 278 → 287 | rule 7's chat-arm clock sentence | `- Time is a fact like the rest: a human-facing timestamp — the [HH:MM] a reply leads with…` |

**All twelve new targets carry their label's own material, and none is a plausible neighbour.** Two
are worth naming because their text was itself rewritten and I checked the rewrite rather than the
line number alone: the work-kind table's heading lost its shouted capitals (`WHAT … HOW` became
`what … how`) and the craft ladder's sentence was re-broken, but both still say what their label
names. `check-pin-drift.sh`'s first leg is green over the whole set: **207 pins proved**, 63 line
pins against their own line, and the reach list names all three rewritten skills.

## 8. The claim that some pins were green while pointing at nothing — CONFIRMED, and worse than stated

This was the claim I was asked to confirm or refute, and it is the most valuable thing in this part.
I refute the numbers and confirm the substance: the old pins were in worse shape than the summary
said, not better.

I took every pin in `ARCHITECTURE.md` at `25acaf5` that names one of the three skills — **35 pins** —
and printed the line each one actually landed on in the file as it then stood.

**Eleven sat on a blank line, not twelve.** The eleven are `live-spec-base` at 71, 136, 247, 289,
310, 321, 331, 345, 400, 408 and 417. Each is the empty line **exactly one above** its subject's
first line: 289 is blank and rule 19 opens at 290; 321 is blank and rule 21 opens at 322; 400 is
blank and rule 26 opens at 401. I verified those three headings by locating them in the old file
directly.

**Three sat exactly five lines inside their rule, not two.** Rule 31 opens at 449 and its pin read
454. Rule 32 opens at 515 and its pin read 520. Rule 35 opens at 559 and its pin read 564. All three
are `+5`, which is too regular to be chance and suggests one authoring pass that measured from the
wrong end.

**Two more were off by one onto their neighbour's line, which the summary did not mention at all.**
The pin labelled `rule 7's worker-restore sub-rule, INV-298` read 163, and line 163 is the tail of a
different sub-rule — `senior's own workers colliding (SPEC ACT-3, INV-11).` The worker-restore
sub-rule actually opens at 164. And the pin labelled `one row per landing commit` read 164 — the
worker-restore sub-rule's own line — while `**One row per landing commit.**` opens at 165. So the two
pins sat on each other's neighbours, each naming a rule one line below where it pointed.

**So at least 16 of the 35 were not on their subject's first line, and all 35 were green.** That
green is not hearsay: I ran `check-pin-drift.sh` myself in the first pass of this record, at
`75c4377`, and recorded "207 pins proved" with exit 0. These pins were in the tree then, in exactly
the state described above.

**Why they passed — the mechanism, read out of the gate.** `check-pin-drift.sh` proves a line pin
against a window of `±2` lines (`TOL`), and it proves it by looking for any *naming word* of the
label — a word of four or more characters that is not document furniture (`rule`, `step`, `gate`,
`line`, `table`, `check`, `node`, `file`, `home`, `section`, …), matched case-insensitively as a
substring, with a trailing `s` stripped. A blank line one above its heading therefore always passes:
the heading itself is inside the `±2` window. The `+5` cases are outside that window, and they passed
for the other reason — a naming word of the label happened to occur in the five-line window anyway.
The label for rule 31 carries `earned-message`, and its window carries "agent scans for cards and
reads the owning agent's"; a single common word is enough, because the gate breaks on the first hit.

**The honest reading:** the gate proves that a label's word appears near a line, which is a much
weaker claim than that the pin points at the right place. It is a rot detector, not an aim detector.
Tonight's rewrite did not damage these pins; it forced them to be re-aimed, and the re-aiming is what
put them on their subjects for the first time in a while. That is a real improvement, and it is the
opposite of what a reader would guess from "the rewrite moved 35 pins".

## 9. THE HONEST RED — the pin gate's second leg is failing, on rot older than tonight

**`bash guardrails/check-pin-drift.sh` exits 1.** Its first leg is green; its second leg is not:

```
OK (pin drift): 207 pin(s) checked — 63 line pin(s) proved against their own line …
FAIL (pin drift, r5): skills/build-pipeline/SKILL.md:385-403 — no naming word of the label stands in lines 385-403
FAILED (pin drift, r5): 53 range pin(s) checked against r5-rule-prices-2026-08-11.md, and the findings above stand.
```

The second leg checks the 53 range pins in `.live-spec/r5-rule-prices-2026-08-11.md`, the page that
prices the 53 rules living outside the shared rulebook. **One entry fails.** This section exists so
the owner meets the red here, with its cause, rather than meeting it cold.

I was given four claims about this red. I checked each. **Three hold in substance, two are wrong in
their numbers, and one is simply false.**

**(a) The rot predates tonight — TRUE, but not from the date I was told.** I was told the nine
`build-pipeline` entries had been missing their text by about 21 lines "already on 08-11, before any
night work". The first half is right and the second half is not. At `d11331f`, the commit that
created the page on 2026-08-11 at 03:01, I read the file it prices and found all nine ranges
**exact** — rule 1 at 243, rule 2 at 263, rule 3 at 286, rule 4 at 353, rule 5 at 364, rule 6 at 381,
rule 7 at 385, rule 8 at 404, rule 9 at 471, each matching its recorded range's first line to the
line. The page was accurate the day it was written. The rot arrived later, between 2026-08-11 and
tonight's base.

**And the offset is not "about 21".** At `db01da2` — the base commit, before a single line of
tonight's work — the nine had drifted by:

| rule | r5 range | actual start at db01da2 | offset |
|---|---|---|---|
| 1 | 243-262 | 222 | −21 |
| 2 | 263-285 | 242 | −21 |
| 3 | 286-352 | 265 | −21 |
| 4 | 353-363 | 324 | −29 |
| 5 | 364-380 | 335 | −29 |
| 6 | 381-384 | 352 | −29 |
| 7 | 385-403 | 356 | −29 |
| 8 | 404-470 | 375 | −29 |
| 9 | 471-500 | 422 | −49 |

Three at −21, five at −29, one at −49. "About 21 lines" describes only the first three; the median is
−29 and the worst is −49. The substance of the claim — **the nine entries were already rotten before
tonight, and nothing tonight caused it** — is confirmed by my own reading, and it is the part that
matters.

**(b) They passed by coincidence — TRUE, and the range widths are wider than stated.** I was told the
ranges are 19-67 lines wide. They are **4 to 67**: 20, 23, 67, 11, 17, 4, 19, 67 and 30 lines. Three
are narrower than the stated floor, and the 4-line one (rule 6) is the narrowest. The coincidence
mechanism is nonetheless real and is the same one section 8 describes: the r5 leg searches the
label's naming words anywhere in the pinned span, and the label here is the rule's own opening line,
whose words — "verify", "commit", "prove", "spec", "architecture" — recur constantly in a file about
exactly those things. A 67-line window into a build-pipeline body will almost always contain one.

**(c) Nine of nine passed at the base and eight of nine pass now — TRUE, verified by replicating the
gate.** I could not cut a worktree at the base to run the real script, so I re-implemented the r5
leg's matching rule in Python directly from the script's own source: `label_words`'s four-character
minimum, its hyphen and underscore splitting, its furniture list, its trailing-`s` strip, its
naming-before-furniture preference, and its case-insensitive substring match that stops at the first
hit. **The replica reproduces the real gate exactly at HEAD** — 53 checked, 1 failure, and the same
failing entry `skills/build-pipeline/SKILL.md:385-403` — which is what licenses its use on the
commits I cannot check out. Its verdicts:

| revision | entries checked | failures | build-pipeline entries passing |
|---|---|---|---|
| d11331f (page created, 08-11) | 53 | 0 | 9 of 9 |
| db01da2 (tonight's base) | 53 | 0 | 9 of 9 |
| 25acaf5 (before the rewrite) | 53 | 0 | 9 of 9 |
| HEAD (a5d61a6) | 53 | 1 | 8 of 9 |

So the claim holds exactly: **tonight's work did not break the record — it removed the coincidence
that was hiding rot already there.** The single red is the one entry whose luck ran out. That is a
gate telling the truth for the first time in a week, and it should be read as a gain.

**(d) A ready remeasure commit is waiting on `morning/2026-08-18-r5-remeasure` — FALSE. I checked and
it is not there.** The branch exists, but:

- it points at `8a920ee`, "The architecture pins follow the lines the rewrite moved";
- `git merge-base --is-ancestor` confirms it is **fully contained in HEAD** — 0 commits ahead, 11
  behind;
- its tip touches `ARCHITECTURE.md`, `guardrails/rule-census.json` and
  `skills/build-pipeline/SKILL.md`, and **does not touch the r5 page at all**;
- `git log --all -- .live-spec/r5-rule-prices-2026-08-11.md` returns five commits across every branch
  in the repository, the newest being `4d3d8fc`, already merged. **No commit anywhere remeasures the
  nine build-pipeline rows.**

I am not able to say where the intended commit went. What I can say is that nothing on that branch
would close this red, and a reader told to look there in the morning will find an ordinary merged
commit. **This is the one place where what I was told does not survive contact with the repository,
and I am recording it rather than smoothing it.**

**The reason for deferring the remeasure IS sound, and I verified its premise myself.** A remeasure
genuinely changes prices and order. Measuring the nine rules' bodies at HEAD against their recorded
prices:

| rule | recorded bytes | bytes at HEAD | change |
|---|---|---|---|
| 8 | 5,954 | 4,042 | −1,912 |
| 3 | 5,705 | 4,819 | −886 |
| 9 | 4,028 | 4,217 | +189 |
| 1 | 1,625 | 1,751 | +126 |
| 2 | 2,230 | 2,331 | +101 |
| 7 | 1,452 | 1,439 | −13 |
| 4 | 1,003 | 1,011 | +8 |
| 5 | 1,466 | 1,472 | +6 |
| 6 | 355 | 359 | +4 |

(The same measurement at `d11331f` returns every recorded figure to within a single byte — a
consistent −1 across all nine, the page's trailing-newline convention — which is what tells me the
prices were honest when written.)

**The order changes, not just the numbers.** `.live-spec/culling-plan-v3-2026-08-10.md` states at its
queue line that the queue runs from the most expensive rule first, and names this very page as the
source of the 53 rules' prices; the r5 page in turn calls that plan "the frozen plan". The old top of
the build-pipeline queue was rule 8 (5,954), then rule 3 (5,705), then rule 9 (4,028). Remeasured it
becomes rule 3 (4,819), then rule 9 (4,217), then rule 8 (4,042) — **rule 8 falls from first to
third**. So a remeasure is a change to the input of a frozen plan, and holding it for the owner's
word is the right call. That part of the reasoning I confirm.

**One inconsistency the reasoning does not cover, and it is a real one.** `4d3d8fc`, inside this very
range, **did** edit the r5 page: it repointed six `communicator` entries to new line ranges — 459-479
became 469-489, 449-457 became 459-467, and four more — while leaving every byte count and every
price untouched. So a repoint without a reprice is possible, was done tonight, and did not disturb
the frozen plan. The stated reason for not doing the same for build-pipeline is therefore incomplete
as given. It is nonetheless defensible on a ground the summary did not state: the communicator rows
moved because lines **above** them shifted, so their own text and bytes were unchanged, whereas the
build-pipeline rewrite changed the rules' own text, and the table above shows their bytes moved by up
to 1,912. Repointing those nine without repricing would leave the range right and the price wrong —
arguably worse than a clean red. **I record this as my own reading, not as something I was told.**

**Blocking? No — and I want to be exact about why.** This red is a true finding against a page whose
rot predates this range, it is fully described here, and closing it means editing the input to a
frozen plan, which is the owner's decision and not this pass's. It stands, named, with its cause,
its history and its cost measured. What I refuse to do is call it clean.

## What the gate said

After the second extension commit, over all 59 commits of the range:

```
$ bash guardrails/check-prover-record.sh
OK (prover record): committed record(s) for 2026-08-18 found:
  docs/prover/2026-08-18-specauthor-pins-and-attic.md
OK (freshness): record commit is not older than the last PRODUCT_SPEC.md commit.
OK (freshness): record commit is not older than the last ARCHITECTURE.md commit.

$ python3 -m pytest -q tests/test_guardrails.py -k TestGateA_ProverRecord
........                                                                 [100%]
8 passed, 70 deselected in 2.02s
```

`test_real_repo_passes` is among those eight, and it is the one the final full run caught red before
this extension.

**My own run left one file dirty, and I am naming it rather than quietly undoing it.** Running
`tests/test_guardrails.py` executes `scripts/progress-report.py` with the repository root as its
working directory, so it rewrote `docs/PROGRESS.md` in this tree: the generated date moves 2026-08-17
→ 2026-08-18, the open-findings count 4,950 → 4,970, and the quoted spec ceiling 840,000 → 703,126.
The behaviour predates this pass — the 2026-08-17 record names the same effect — and `c466d3e`
earlier in this range put the file back to the base's copy deliberately, so it is protected tonight.
I have left the change uncommitted and unrestored: committing it is outside the one file this pass
may write, and clearing it would mean a git-level restore, which is exactly the move base rule 7's
worker-restore sub-rule (INV-298) reds on. It is the integrator's to decide, and it is stated here so
the decision is made in the open rather than inherited from a tree someone quietly tidied.

The same gate reddened between the first landing of this record and its extension, on exactly the
freshness arm it is built to red on: `0ce20c8` touched `ARCHITECTURE.md` after `3b73943`. That is the
gate working, not the gate failing, and it is the reason this file was extended rather than left as
it stood.
