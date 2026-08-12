# Stage 3, step C2: a verdict for every check with no dated catch

Date: 2026-08-12.

What this is: one verdict — keep, repair, or remove — for each of the 25 checks the day-1 census
marks "No real catch on record". Every verdict rests on the facts of that check's evidence line and
cites them. This page executes nothing: no check is removed, no check is changed, and nothing is
written to `DECISIONS.md` here. The orchestrator accepts these verdicts first.

Sources read: `.live-spec/stage3-check-evidence-2026-08-12.md` (step C1, the evidence lines);
`.live-spec/day1-census-checks.md` (the 31-gate table, its seconds column and its totals);
`.live-spec/culling-plan-v3-2026-08-10.md` (stage 3, steps C1–C3, and the R6 row for the repair
pattern); `.live-spec/handover-2026-08-09.md` lines 71–76 (Alexander's word of 2026-08-09 11:22).

**Counts: keep 18, repair 6, remove 1.**

- keep (18): c, d, e, f, j, k, l, o, p, q, u, v, w, x, y, z, ad, ae
- repair (6): b, g, i, n, r, aa
- remove (1): ab — already executed 2026-08-09; see its row and the closing list

## What the removal rule allows, read before the rows

C3 permits a removal only where the evidence line names another test or gate covering the same
failure class. The C1 page's own summary settles most of the question: nine checks have named
neighbours — b, d, x, l, o, j, v, y, z — and of those, all but one are named as partial or
scope-limited, "none named as full coverage of the same class". Where the evidence line itself says
the neighbour would miss the case, C3's door stays shut and the row says so.

One count in the source needs stating: the C1 summary reads "That is 8 checks with some named
coverage" while the letters it lists on the same line are nine. This page works from the letters,
and every one of the nine has its own row below.

One check meets C3 in full: gate b, whose neighbour re-runs the identical suite. That is the whole
list, and the closing section says why cutting it would be a poor trade anyway.

## What a check costs, measured

The 25 checks carry 187,863 bytes of live script (23 scripts; gate c has none, and gate ab's 6,592
bytes already sit in `attic/`). Wall time is a weak lever here: the census times gate b at 451.45
seconds and the other 24 at 31.07 seconds together, so cutting any check other than b buys under
ten seconds of a push. The real price of a check is its bytes plus its escort — a line in
`guardrails/pre-push`, a step in `.github/workflows/gates.yml` or a carve-out in
`guardrails/ci-mirror.json`, an entry in `guardrails/gate-red-proofs.json`, its own file under
`tests/`, a spec `INV-` code and a `TEST_MATRIX.md` row. Every removal frees that escort and costs
an edit in each of those places, which is the honest ledger for each candidate below.

## The repair pattern, taken from R6

R6 repaired the architecture-pointer check in commit `3915e95` ("the architecture-pointer gate
proves a pin against its own line, and eight rotten pointers come home"). Three moves, in order:
replace the proxy the check was measuring with the exact fact it claims to prove; sweep the tree
with the tightened check and land what it finds; extend the check's own red-proof so the tightened
form is shown to fire. Each repair below is written to that shape and names the smallest change
that closes the check's own documented defect.

---

## b — `check-tests.sh` — repair

The suite itself, 451.45 seconds of the census's 486.48. Its 2026-07-14 defect is closed already:
the local runner under-collected pytest-style tests, a version-pin regression rode through, CI
caught it, and the same day the runner switched to `pytest` (JOURNAL.md:1250, :1256). The live
defect is the one ROADMAP row 553 recorded on 2026-08-06 — a nested meta-test inside the suite
costs 282 of 456 seconds, more than half of every push's wall time for one test.

**Repair.** Defect: one nested meta-test holds 282 of the suite's 456 seconds at every push.
Smallest change: run that meta-test in the CI mirror alone — the evidence line names
`.github/workflows/gates.yml` as the second net that already re-runs the same suite — and drop it
from the pre-push run, leaving the reach of every other test untouched.

## c — `tests/test_traceability.py::test_architecture_owns_every_anchor_once` — keep

Guards a spec anchor owned by zero or by two architecture nodes. The evidence line finds no other
coverage: the two neighbouring tests in the same file assert index uniqueness and matrix coverage,
which are different facts. It runs no script and adds no seconds of its own, riding gate b.

This is the closest sibling of the architecture-pointer check Alexander kept on 2026-08-09 11:22 —
the same document, the same class of rot, found only by a machine that looks. **Recommendation of
mine, standing until he rules.**

## d — `check-matrix-reference.py` — keep

Guards `TEST_MATRIX.md`'s generated Reference section drifting from the body it is built from.
Gate x is the same shape of gate on `PRODUCT_SPEC.md`, both citing SPEC INV-269, and the evidence
line states plainly that x "would not notice a drift specific to `TEST_MATRIX.md`". C3's door
therefore stays shut. Price: 5,325 bytes, 0.08 seconds.

Silent-rot extension of the 11:22 word. **Recommendation of mine, standing until he rules.**

Noted for the orchestrator without a verdict attached: d and x are one mechanism written twice
(9,308 bytes across two gate letters). A merge into one gate parameterized by document would halve
the bytes with no lost reach, and would cost edits in `pre-push`, `ci-mirror.json`,
`gate-red-proofs.json`, CI, the matrix and two test files. At 0.16 seconds and 4 KB of yield, that
trade looks thin; it is recorded here so the option is on the table rather than lost.

## e — `check-prototype-fence.sh` — keep

Guards a production file structurally referencing a file inside a fenced `prototype/` folder — the
law that came out of the Room incident (`a5ad4c2`). The evidence line searched `tests/` for other
coverage of prototype-to-prod wiring and found none, so C3's door is shut. Its only recorded
finding is a wall-time one from 2026-07-27 (215 of 471 seconds); the census's own run on 2026-08-09
timed it at 9.15 seconds, and the later number is the one this page prices it by.

A prototype reference in shipped code holds until the prototype folder moves, which is rot no
reader sees. Silent-rot extension. **Recommendation of mine, standing until he rules.**

## f — `check-skill-loadability.sh` — keep

Guards a shipped skill file that fails to load: broken frontmatter, a name mismatched to its
folder, a missing description or version. The C1 page names f as one of the three thinnest rows —
no firing, no documented hole, no other coverage found — which also means C3's door is shut. It is
among the cheapest scripts in the set at 2,266 bytes and 0.25 seconds.

A skill that fails to load never triggers, and nothing announces the absence. Silent-rot extension.
**Recommendation of mine, standing until he rules.**

## g — `check-pin-drift.sh` — repair

Kept by Alexander's own word of 2026-08-09 11:22 ("the architecture-pointer check is essential",
`.live-spec/handover-2026-08-09.md`:71-73), carried out by the restore `d58c903`. Row 541's defect
was closed by R6 on 2026-08-11. Row 588, found 2026-08-11, is still open: 38 of 53 pins in
`.live-spec/r5-rule-prices-2026-08-11.md` had rotted, because this gate reads `ARCHITECTURE.md`
alone, and the row states that pins outside that file "carry no guard".

**Repair.** Defect: the gate's reach is one hardcoded document while pins live in several.
Smallest change: take the file set from a declared list rather than a fixed path, with
`ARCHITECTURE.md` as its first entry, then sweep and land what the widened reach finds — the same
order R6 followed. The script and the pin page are both in another worker's write set today, so
this repair may already be under way there.

## i — `check-shipped-language.sh` — repair

Guards stray Cyrillic and personal names in shipped-facing files. ROADMAP row 530 (2026-07-29)
records its own hole from the other side: it refused a decision-record entry that quoted the
person's own words verbatim in his own alphabet, because it read every line as the project's voice
with no quoted-region exception. The register lint named beside it in JOURNAL.md:1171 is the other
half of one net and watches machine-dialect prose, so C3's door is shut.

**Repair.** Defect: no quoted-region exception, so a faithful quotation of his words reds.
Smallest change: exempt block quotes and fenced quotations from the alphabet test while the
personal-name test keeps its full reach. Price: 579 bytes, the smallest script in the set.

## j — `check-broad-kill.sh` — keep

Guards a cleanup that ends a process by broad name instead of an owned PID, group or path.
JOURNAL.md:915 names the motivating incident: a broad `pkill chrome` closed the owner's real
browser mid-session and destroyed work state outside git. Gate o is named as the nearest neighbour
and is explicitly partial — o would pass a broad-name kill that prints a notice — so C3's door is
shut. Price: 8,076 bytes, 0.58 seconds, against a loss that lands on the owner's own machine.

## k — `check-freeze.sh` — keep

Guards a silent meaning change during compaction: a dropped anchor occurrence, a changed structural
marker, a drifted number-with-unit, a changed backticked path. The evidence line finds no other
coverage — gates z and aa watch the same documents for byte size and finding count, and neither
would notice a dropped citation — so C3's door is shut.

This is the check that watches the traffic this campaign itself generates: stage 2 rewrites rule
bodies, and this is the machine that proves a rewrite lost no meaning. Price: 3,092 bytes, 0.15
seconds. Silent-rot extension. **Recommendation of mine, standing until he rules.**

## l — `check-muted-launch.sh` — keep

The third net for SPEC INV-157, guarding a tracked script that shows a browser-launch signal with
no mute signal in the same file. Its own header names the other two nets — a string check of
`templates/headless_harness.py` and a consumer's by-deed process-group diff, both in
`tests/test_harness_template.py` — and states that neither would hear a divergent fork's unmuted
launch. That is the case this scanner exists for, so C3's door is shut on it. Price: 8,046 bytes,
2.40 seconds, the fifth-largest wall time in the set.

## n — `check-earned-message.py` — repair

Guards an inbox message that names neither allowed birth. ROADMAP row 585 (2026-08-07) records the
hole: the gate reads past every fenced block before reading any field, so a sender copying the
home's own printed template — which fences the birth block — failed the check on four real, lawful
deposits between 2026-07-28 and 2026-08-07. No other coverage exists; the judging moment is the
intake sweep, which is a reading step, so C3's door is shut.

**Repair.** Defect: the fence-stripping pass runs before the field read, so the template's own
fenced birth block is invisible to it. Smallest change: read the birth fields before stripping
fences, or strip only fences that carry no birth field.

Cost stated plainly: 16,759 bytes, report-only at push, zero catches, four documented false reds.
That ledger argues for retirement rather than repair, and C3 blocks it, so the check goes to
Alexander's desk in the closing list. The repair waits on his ruling — a retirement makes it moot.

## o — `check-cleanup-notice.sh` — keep

Guards a cleanup path that ends a process and emits no notice of what it ended and why the run
owned it. Gate j is the stricter successor on the same surface — this check's own header says it
"ships ahead of INV-162's stricter owned-identity check" — and the evidence line states the two
overlap only partially, since j would pass a correctly-scoped ending that prints nothing. C3's
door is shut. Price: 4,828 bytes, 0.64 seconds.

The notice requirement predates its stricter successor, and whether the pack still wants the notice
now that j enforces owned identity is a question of taste that belongs to Alexander; it goes to the
closing list. Silent-rot extension meanwhile — a cleanup that ends something quietly leaves nothing
for a reader to find. **Recommendation of mine, standing until he rules.**

## p — `check-touchpoint-kind.py` — keep

Guards a surface speaking a message kind — interruption, teaching line, wait line — its declared
touchpoint in `guardrails/touchpoints.json` does not afford. The evidence line finds no other
coverage: gate q reads one touchpoint for a different property. C3's door is shut. Price: 7,980
bytes, 0.05 seconds, with no firing and no documented hole found between its birth on 2026-07-17
and the census of 2026-08-09.

The reason it goes to the closing list rather than a silent-rot recommendation: a wrong-kind message
lands in front of Alexander, so he is the live detector for this class, which makes the machine's
value his call rather than mine.

## q — `check-board.py` — keep

Guards the waiting-list board losing an item: a closing report omitting a still-open item, a
demotion with no matching board line, a shown set over its twelve-item cap. The C1 page names q
among the three thinnest rows and finds no other coverage, so C3's door is shut. Price: 8,913
bytes, 0.05 seconds.

The class has no human detector by construction — an item silently dropped from the board is
exactly the item nobody remembers to look for. Silent-rot extension, and the strongest instance of
it in the set. **Recommendation of mine, standing until he rules.**

## r — `check-authority-anchor.py` — repair

Guards a sentence recording a decision as the person's own with no exchange a reader can go check.
The gate already shipped hollow once and was rebuilt (`8a0209f`). ROADMAP row 550, found
2026-08-06 by Alexander, records the live hole: the gate asks an entry for a date alone, so on
2026-08-05 a session wrote its own reasoning under his name with a real date on it and passed. The
row is still queued. No other coverage was found in `tests/` or `docs/prover/`, so C3's door is
shut.

**Repair.** Defect: a date satisfies the gate, and a date is the one part of a fabricated
attribution that is free to produce. Smallest change: require a quotation of the person's own words
plus a pointer to the exchange, which is the repair row 550 already specifies. At 24,425 bytes this
is the largest script in the set, so the repair earns its place by closing the hole without
growing the file.

## u — `check-ci-mirror.sh` — keep

Guards a gate letter that `pre-push` runs locally and `gates.yml` never runs in CI, with no
declared carve-out. Gate w reads the same enumeration for a different property — a known-red proof
— and the evidence line states it would not notice a gate missing from CI, so C3's door is shut.
Price: 3,333 bytes, 0.13 seconds.

A gate absent from CI leaves no trace anywhere; the local chain stays green and the second net
quietly shrinks. Silent-rot extension, and this campaign removes gates, which is exactly when the
mirror drifts. **Recommendation of mine, standing until he rules.**

## v — `check-judge-listed.py` — keep

Guards a chat judge whose hook file is installed correctly while its entry has fallen out of the
installed `settings.json`, so the judge never runs. Its own docstring names gate m and rules it
insufficient in the same breath: m "proves an installed hook FILE matches its source" but "does not
prove settings.json still LISTS the judge entries". C3's door is shut by the check's own account of
its neighbour. Price: 4,370 bytes, 0.05 seconds.

A judge present and never running is the purest form of the silent rot the 11:22 word was about.
Silent-rot extension. **Recommendation of mine, standing until he rules.**

## w — `check-every-gate-can-fail.py` — keep

The meta-gate: every gate in the push chain carries a known-red proof, so no gate can sit in the
chain unable to fire. Its docstring names the incident it was built to pay for — the
authority-anchor gate shipping hollow. The evidence line searched for another reader of
`guardrails/gate-red-proofs.json` and found none, so C3's door is shut. Price: 9,202 bytes, 0.06
seconds.

A hollow gate reports green forever and nothing else in the tree notices. Silent-rot extension, and
the check that keeps whatever survives this campaign honest. **Recommendation of mine, standing
until he rules.**

## x — `check-index-generated.py` — keep

Guards `PRODUCT_SPEC.md`'s committed index drifting from a fresh build off the body. Gate d is the
same shape on `TEST_MATRIX.md`, and the evidence line states d "would not notice a drift specific
to `PRODUCT_SPEC.md`", so C3's door is shut. Price: 3,983 bytes, 0.08 seconds. The merge option is
recorded in gate d's row above.

Silent-rot extension. **Recommendation of mine, standing until he rules.**

## y — `check-agent-card.py` — keep

Guards a live-spec host tree carrying no `.live-spec/agent.md` card, which leaves the tree
undeclared to any window trying to address it. `tests/test_agent_channels.py::test_pack_card_exists_and_names_its_five_fields`
asserts the same fact for the pack's own tree alone, and the evidence line states it "would not
notice a missing card in a different host tree" — the adopting host is the case the gate exists
for. C3's door is shut. Price: 2,756 bytes, 0.04 seconds, one of the cheapest scripts in the set.

Silent-rot extension. **Recommendation of mine, standing until he rules.**

## z — `check-doc-bound.py` — keep

Guards one of the four large working documents growing past its declared byte ceiling with no
rotation applied today. Its own docstring says it composes with gate t, and gate t is one of the
six checks that does hold a dated catch (2026-07-27). That relationship is composition: a rotation
is the remedy z accepts in place of a red, and t watches a different property on the same document
set, so C3's door is shut. Price: 6,177 bytes, 0.07 seconds.

This is one of the campaign's own instruments: the counters this cut is measured by sit inside the
documents z bounds. Silent-rot extension. **Recommendation of mine, standing until he rules.**

## aa — `check-doc-findings-bound.py` — repair

Two documented holes, both dated. ROADMAP row 526 (2026-07-29): the gate scored a refused reading
as zero and reported a pass, so a document whose check never ran read clean — a vacuous pass of
exactly the class gate w exists to prevent. ROADMAP
row 532 (2026-07-30, outside audit): the gate compared only the `total` field and never the `bytes`
field the same record already carried, missing a ratchet it could enforce with no new instrument.
Gate z watches the same documents for a different property, so C3's door is shut.

**Repair.** Two defects, two smallest changes: treat a refused reading as red instead of scoring it
zero, and compare the `bytes` field already present in the record alongside `total`. Both stay
inside the existing script and its existing input. Price to justify: 12,701 bytes and 9.82 seconds,
the second-largest wall time in the set — this repair is what would earn that back.

## ab — `check-handover-provenance.py` — remove, already executed

The check left the push chain on 2026-08-09 (`0ef204e`, "Day 2 row 2.2"), a few hours after the
census that named it. The script sits at `attic/check-handover-provenance.py` (6,592 bytes) and
`guardrails/pre-push` carries no gate ab line. There is nothing left for this campaign to cut, so
the verdict records the state and orders nothing.

One fact this row surfaces, and it matters beyond this row: ROADMAP row 522 states that with the
gate retired "this half stays a discipline the seat holds too" — no machine covers the class today.
Under the C3 rule now in force, that missing coverage would have sent this check to Alexander's
desk instead of to the attic. The one removal the campaign has executed so far would fail today's
own test. It goes to the closing list as a confirmation he can give or withhold.

## ad — `check-tree-counts.py` — keep

Guards a count this repository publishes about its own tree that does not match a fresh count, or
whose named reproduction command returns a different number. The evidence line finds no other
published-count reader, so C3's door is shut. Price: 17,287 bytes, 0.12 seconds.

The campaign publishes counts in every page it writes — byte totals, rule counts, gate counts — and
this is the machine that proves each one against the tree. A published number rots in silence and
convinces a reader anyway. Silent-rot extension. **Recommendation of mine, standing until he
rules.**

## ae — `check-named-checks.py` — keep

Guards a stale entry in `scripts/check-registry.json` for a runnable file a skill body names: a
wrong description of what it does, which tree it judges, whether it belongs in an adopting project,
what it needs to run. The C1 page names ae among the three thinnest rows and finds no other reader
of the registry, so C3's door is shut. Price: 20,157 bytes for 0.16 seconds — the second-largest
script in the set, guarding the freshness of descriptive text.

The check stays because nothing else reads the registry, and it goes to the closing list because
its bytes and the value it guards are the widest mismatch of the 25. Silent-rot extension
meanwhile. **Recommendation of mine, standing until he rules.**

---

## List 1 — removals C3 permits today

**Gate b — `check-tests.sh`.** The only row of the 25 whose evidence names coverage of the same
failure class without a stated gap: `.github/workflows/gates.yml` re-runs the same suite on its own
machine as the CI mirror (SPEC M-5), and that mirror is named as the mechanism that caught the
2026-07-14 miss when the local runner's collection was wrong.

What the tree would lose: the pre-push moment. Every regression the suite catches would land on the
server first and come back from CI afterwards, and the 2026-07-14 entry is the record of what that
gap costs even when it lasts hours. The gain is 451.45 seconds per push, the largest single number
in the census. My verdict on b is repair, and the repair above takes 282 of those seconds without
opening the gap.

**Nothing else.** For the other 24, C3's door is shut, and the eight remaining rows with named
neighbours are shut by their own evidence: d and x name each other and each is stated as blind to the other's
document; l's own header names two nets and says neither hears the case l exists for; o and j
overlap partially by o's own header; v's docstring names m and rules it insufficient in the same
sentence; y's neighbour is scoped to the pack's own tree; z's neighbour composes with it as a
remedy. The C1 page's summary reads the same way: "none named as full coverage of the same class."

## List 2 — what waits for Alexander's word

Each line below is written to go into `DECISIONS.md` as it stands. Nothing has been written there;
that is the orchestrator's step after these verdicts are accepted.

**The class line, covering fifteen keeps.**

> Checks that guard silent rot stay in the chain for now: c, d, e, f, k, o, q, u, v, w, x, y, z, ad
> and ae are kept on the seat's extension of your word of 2026-08-09 11:22 about the
> architecture-pointer check, none of them has other coverage of its failure class, and the
> extension is the seat's own until you rule on it.

**Gate ae — `check-named-checks.py`.**

> Gate ae spends 20,157 bytes and 0.16 seconds proving that `scripts/check-registry.json`
> describes each runnable file correctly, has caught nothing since 2026-08-06, and has no other
> reader of the registry; the seat recommends retiring it and keeping the registry as a plain
> document, and runs it until your word.

**Gate n — `check-earned-message.py`.**

> Gate n spends 16,759 bytes running report-only at push, has caught no unearned message and has
> reded four lawful deposits between 2026-07-28 and 2026-08-07 (queue row 585); the seat
> recommends retiring it and leaving the intake sweep as the judging moment, and holds its repair
> until your word.

**Gate p — `check-touchpoint-kind.py`.**

> Gate p spends 7,980 bytes proving that each surface speaks only the message kind its touchpoint
> affords, with no catch on record and no other coverage; you are the person a wrong-kind message
> reaches, so the seat asks whether the machine still earns its place and keeps it running until
> your word.

**Gate o — `check-cleanup-notice.sh`.**

> Gate o requires a cleanup to print what it ended, and its own header says it shipped ahead of
> the stricter owned-identity check that is now gate j; with no catch on record for either, the
> seat asks whether the notice requirement is still wanted beside j and keeps o running until your
> word.

**Gate ab — `check-handover-provenance.py`, already retired.**

> The handover-provenance gate was retired on 2026-08-09 with no other machine covering its class
> (queue row 522: the discipline is now the seat's alone); under the removal rule the campaign
> adopted afterwards that missing coverage would have brought the question to you first, so the
> seat asks you to confirm the retirement stands.

## Left open

Gate b's repair moves a test between the local chain and CI, which touches the same suite another
worker is holding today; the orchestrator sequences it. Gate g's repair may already be under way
in the worker that holds `guardrails/check-pin-drift.sh` and the pin page row 588 names. The
d-and-x merge is recorded in gate d's row as an option with its price attached, and carries no
verdict of mine.
