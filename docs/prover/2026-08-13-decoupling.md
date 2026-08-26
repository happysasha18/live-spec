<!-- ARCHIVED 2026-08-17, the owner's word. This record was written on an unmerged branch and
     carried into the tree when that branch was deleted, so the reasoning it holds outlives the ref.
     It reviews a range this tree never took, it discharges no gate, and it authorizes no push. -->

# Prover record — 2026-08-13 the decoupling: a node's body left the tree and every pointer at it stayed

Run by product-prover v1.3.0, the external canon installed by `scripts/install-external-skills.sh`
at `skills/product-prover/`. Lens set: `SKILL.md` sha256 `95f3628f4ad4`, `reference/stress-lenses.md`
sha256 `422e3b9a43a9`. Mode: FULL, over `PRODUCT_SPEC.md` and `ARCHITECTURE.md`, with the architecture
lens armed and the project's kind read as a skill pack. Pack bindings from
`skills/product-prover-pack/SKILL.md` v1.0.0.

PUSH-REVIEW

Range: be4e4f0..HEAD. `origin/main` resolves to be4e4f0, so be4e4f0 is the base. The commit this
record ships in carries the record alone and names no change of its own, which is the exemption
`guardrails/check-prover-record.sh:224-241` writes for the commit that first ships a record. The
change this pass reviewed is be4e4f0 itself — the v5.0.0 MAJOR that moved the prover's canon out of
this repository — read together with the two documents as they now stand.

- be4e4f0 v5.0.0 MAJOR — product-prover decouples: the canon moves to its own repository, the pack installs it as an external skill

The pass was adversarial by construction. Two readers with clean context, neither of them the seat
that landed the patches, were briefed to find reasons to refuse rather than reasons to allow, one
over each document. Both returned REFUSE independently. The seat then re-derived every load-bearing
claim against the tree itself before writing it here, and replaced both readers' replicated test
logic with an observed run. Three claims did not survive that re-derivation and are recorded under
"What the re-derivation corrected".

Files read: `PRODUCT_SPEC.md` whole (8,225 lines) by the spec reader, and at lines 268, 1618, 2674,
7491, 7514, 7610, 7951, 8235, 8576, 8594, 8626, 8818, 8841-8842 at the seat; `ARCHITECTURE.md` whole
(921 lines) by the architecture reader, and at lines 24-25, 35, 37-38, 81, 99, 114-140, 177, 181,
203, 366, 587, 621-622, 627-629, 666, 703-710, 728, 740-741 at the seat; `SURFACES.md`;
`PRODUCT_SPEC.index.md`; `skills/product-prover/SKILL.md` whole (837 lines) and its
`reference/stress-lenses.md` whole (437 lines); `skills/product-prover-pack/SKILL.md` whole;
`skills/build-pipeline/SKILL.md:653`; `docs/prover/README.md` whole;
`docs/prover/2026-08-13-push-range-3.md` whole; `guardrails/check-prover-record.sh` whole;
`scripts/install-external-skills.sh` whole; `scripts/sync-mirrors.sh` lines 1-20, 425-450, 520-530;
`install.sh`; `README.md` lines 22, 35, 72-76, 108-120; `TEST_MATRIX.md` lines 47-50, 79-82;
`MIGRATION.md`; `VERSION`; `.gitignore` lines 43-45; `guardrails/tree-counts.json`;
`guardrails/rule-census.json` lines 895-910; `ROADMAP.md` rows 608-612, 618, 619; and the twenty-six
test modules under `tests/` that read `skills/product-prover/`.

Checks run: each with its result, the seat's own runs.

- `git am -3` over the three prepared patches — three applied, zero conflicts, no hunk hand-edited.
- `git ls-files skills/product-prover/` — empty. `git check-ignore -v` reports `.gitignore:45`. The
  path is untracked and ignored; it exists on this machine only because the installer ran.
- `bash scripts/install-external-skills.sh` — `OK (external skills): product-prover 1.3.0 installed
  at skills/product-prover (floor 1.3.0)`, first run, no repeat needed.
- `bash guardrails/check-pin-drift.sh` — **FAILED**. 209 pins checked in `ARCHITECTURE.md`; four
  rotten, three of them the prover pins. The r5 arm passed at 53 range pins.
- `python3 guardrails/check-tree-counts.py` — **FAILED**, exit 1, 3 published-count faults. The tree
  returns 6,320 and 5,082 where `README.md` publishes 6,492 and 5,254.
- `cat skills/*/SKILL.md | wc -l` — 5,082 with the clone present. The same command over the tracked
  set alone — 4,245. One commit, two answers, 837 lines apart.
- `python3 -m pytest tests/test_traceability.py tests/test_delivery_separability.py
  tests/test_class_hunt.py tests/test_edge_completeness.py tests/test_restructure_merge_gate.py
  --tb=no -q` — **21 failed, 188 passed in 4.69 s**, on the machine with the clone installed. The
  full suite was not run here; it exceeds this seat's command ceiling and the orchestrator owns it.
- `python3 guardrails/check-doc-findings-bound.py` — **FAILED**, two faults, neither of them this
  record: `skills/live-spec-base/SKILL.md` rose from 68 to 69 findings, and
  `skills/product-prover/SKILL.md` "was repaired to zero and now carries 3 finding(s)". The second is
  F19 below. This record's own file draws no census entry and the gate does not ask for one.
- `check-doc-bound.py` — OK, 4 docs. `check-board.py` — OK. `check-doc-rotation.py` — OK.
  `check-freeze.sh` — GREEN, 3 files. `check-skill-loadability.sh` — OK, 12 skills.
  `check-named-checks.py` — OK, 32 registry entries. `check-matrix-reference.py TEST_MATRIX.md` — OK,
  544 of 544 rows.
- `bash guardrails/check-skill-review.sh` — OK; the push changes no skill body, so the gate stands
  down by name.
- `cat VERSION` — 5.0.0. Frontmatter sweep over `skills/*/SKILL.md` — ten skills stamped 4.3.0, the
  new bindings page 1.0.0, the installed canon 1.3.0.
- `grep -ci` over `PRODUCT_SPEC.md` for `product-prover-pack`, `install-external-skills` and
  `external skill` — 0, 0, 0.
- `grep -c '5\.0\.0' MIGRATION.md` — 0.
- `sed -n '288p;384p;749p' skills/product-prover/SKILL.md` — a blank line, `    in the pipeline;`,
  and `  resolved, and a command's output you actually ran…`. None carries what its pin claims.
- `shasum -a 256` over the two lens files — the digests recorded above.

Findings: nineteen. Sixteen block and three do not. Every one of them is a document defect against
`PRODUCT_SPEC.md` or `ARCHITECTURE.md` as they now stand, and none is closed in this range, because
this commit carries the record alone by the brief that ordered it. Each blocking item below therefore
reads `stands:` with the repair it is waiting for. Three of the sixteen are enforced by gates that are
red on the tree right now, so the push chain refuses on its own evidence and not on this record's
say-so.

**The class.** One class carries fourteen of the nineteen: *a node's body left the repository and
every pointer at it was left standing.* v5.0.0 deleted `skills/product-prover/{SKILL.md,README.md,
LICENSE}` and touched neither requirements document. The structural cause is that no seam was ever
drawn for the pack-to-external-canon boundary, so nothing enumerated what crossed it, and nothing
swept the crossers. That is the finding against the architecture the class lens asks for, and it is
F3 below.

**F1 — Three architecture pins into the prover resolve to nothing, and the pin gate is red on them.**

> `skills/product-prover/SKILL.md:288` (review modes) · `:749` (unwritten-seam hunt — the stress-lens
> family, INV-72) · `:384` (restructure-merge gate — INV-114 delta-judging) — ARCHITECTURE.md:135,
> 136, 138

Line 288 is blank; `## Review modes` stands at 312. Line 384 reads `    in the pipeline;`, the tail
of the feature-fit review's implied-neighbour-state seam; the restructure gate stands at 432. Line
749 is the Meta-rules primary-source sentence; the unwritten-seams sweep left `SKILL.md` altogether
and now lives in a different file, `reference/stress-lenses.md:249`. Beyond the line numbers, the
path itself is untracked and gitignored, so in a fresh clone all three pin into a directory that does
not exist until an installer runs. `ARCHITECTURE.md:24-25` states that every pin comes from a grep or
read actually run; no reader of this repository alone can honour that for these three.

Re-home all three onto `skills/product-prover-pack/SKILL.md`, the tracked page that now carries the
mode-name table at `:15`, the record contract at `:40` and the pin map at `:52`, and drop the pins
into the external body. Two alternatives are open and both cost more: vendor a frozen copy of the
canon under `docs/` and pin that, which buys a second copy to keep; or add a `repo@ref:file:line` pin
form and teach `check-pin-drift.sh` to resolve it, which is worth it only if more external skills are
coming.

`defect · missing-rule (invariant)`

**F2 — The published line counts are red now, and the measurement itself became non-deterministic.**

> "every count this repository publishes about its own tree carries a declared measurement, a home,
> and a push gate." — PRODUCT_SPEC.md:7491, Requirement 306 Context

`check-tree-counts.py` reports three faults: `README.md` publishes 6,492 and 5,254 where the tree
returns 6,320 and 5,082. Rebuilding the block repairs today's number and leaves the deeper defect
untouched. `guardrails/tree-counts.json` defines the count by globbing the working tree, and that
glob now crosses the external boundary: 5,082 body lines with the clone installed, 4,245 without.
`README.md:74` tells a public reader to run the command themselves and states that a push is refused
where the output disagrees. One commit now answers that command two ways, so a contributor who has
not run the installer reds the gate on an unrelated push, and one who has reds it the moment the
external repo ships a release of any different length.

Scope the measurement to tracked files — `git ls-files 'skills/*/SKILL.md'` — so the number is a
property of what this repository ships, then regenerate the block with `scripts/gen-tree-counts.py`.
If the intent is instead that the figure names what a session actually loads, then it owes a stated
precondition and gate ad owes a named stand-down when the external skills are absent; write which, in
that entry's ground block.

`defect · unenforceable-promise (discharge)`

**F3 — The architecture draws no seam for the boundary this change created.**

> "The places two nodes meet — named, because that is where composition bugs live. Each seam states
> what crosses it and which side owns the format." — ARCHITECTURE.md:621-622

Forty-one seam rows, and the newest boundary in the pack has none. What crosses it is a version-
floored clone of a skill body, a mode-name mapping, a record contract, and a pin map over sixteen
requirement codes. Which side owns the format is genuinely contested: the external repository owns
`SKILL.md`'s section names and line numbers, while this pack owns the requirement codes those
sections must carry. Nobody wrote that contest down, and F1, F2 and F13 are its symptoms.

Add the row: pack ↔ external prover canon, crossing the body at or above the floor and returning the
pack's mode names, record shape and pin map, with the external repository owning the body and
`product-prover-pack` owning the bindings. State in the row that the pack pins section names across
this seam and never line numbers.

`defect · boundary-issue (composition)`

**F4 — The placement view states the external node's home wrongly, not merely incompletely.**

> "the pack repo `~/live-spec` … the source of truth: skills, templates, guardrails, docs, tests" —
> ARCHITECTURE.md:741

Five places carry the pack and none of them is where the prover's body now lives. It arrives by `git
clone` from `github.com/happysasha18/product-prover` into a gitignored directory, at a floor read
from the bindings page and enforced by a `sort -V` compare at `scripts/install-external-skills.sh:57`.
That is a sixth place with its own load-bearing technology, and the placement table names none of it.
Architecture check 6 fails.

Add the sixth row naming the canon repository, what it holds, and `git clone` plus the version floor
as its technology; amend the `~/live-spec` row to read as the source of truth for every skill but the
prover.

`defect · boundary-issue (composition)`

**F5 — The suite asserts on strings the external canon does not carry, and 21 tests are red.**

> `pp = read_flat("skills/product-prover/SKILL.md"); self.assertIn("[INV-248]", pp)` —
> tests/test_delivery_separability.py:52

The standalone release deliberately stripped this pack's internal requirement codes, which is right
for a skill that must work on its own and fatal for tests that pin them. `grep -c 'INV-'` over the
installed `SKILL.md` and its `reference/stress-lenses.md` returns 0 and 0. Twenty-six test modules
read the removed path. An observed run over five of them returned 21 failed, 188 passed — and that is
the favourable case, with the clone present. Without it the same tests fail on a missing file
instead. There is no state of a fresh clone in which this suite is green.

Re-point every assertion that proves a pack law onto `skills/product-prover-pack/SKILL.md`, where the
requirement codes now live, and every assertion that proves the prover's own mechanics onto the
section name rather than the code, reading `reference/stress-lenses.md` where the lens moved. Guard
the external-skill group behind a skip that names the reason when the clone is absent, so a fresh
clone reports "external skill not installed" instead of a false red.

`defect · unenforceable-promise (discharge)`

**F6 — The spec's working-skills sentence names a skill the pack no longer carries and misses the one this commit created.**

> "the pack's working skills are spec-author, product-prover, design-reviewer, build-pipeline,
> test-author, communicator, publish, text-audit …, feedback-intake, and feedback-collector." —
> PRODUCT_SPEC.md:268

Requirement 199 (INV-66) demands the identical complete set in every place the pack lists its skills,
and reds the suite where a commit leaves a list naming fewer than the set.
`tests/test_traceability.py::TestPackListParity::test_real_repo_lists_complete` is red in the observed
run. The glossary tells a reader `product-prover` is a pack skill; `git ls-files skills/` proves it is
not, and `product-prover-pack` appears in no list at all.

Rewrite the sentence to the set the tree carries, add a glossary entry for **external skill** — a
skill the pack depends on, installed from its own repository, whose body the pack does not carry —
and sweep the same name into `OVERVIEW.md` and the five "The pack, whole:" footers.

`defect · internal-conflict (consistency)`

**F7 — "ten working skills" is false against the tree, and the new skill has no node.**

> "live-spec is a skill pack: ten working skills plus the one shared rulebook they all load" —
> ARCHITECTURE.md:35

`ls -1 skills/` returns twelve directories. `product-prover-pack` has no `### [node: …]` section
anywhere in the document and appears in `PRODUCT_SPEC.md` zero times, as do
`install-external-skills` and the phrase `external skill`. So three new parts — the bindings page,
the installer, and the external boundary — stand with no node and no requirement behind them.
Architecture checks 1 and 2 both fail.

Rewrite line 35 to name nine skills shipped here, one installed from its own repository, the shared
rulebook and the bindings page. Then fold the bindings into `[node: product-prover]` with an explicit
"body external, bindings here" line rather than giving it a node of its own — a bindings page with
one caller fails the prover's own second fitness question. Register
`scripts/install-external-skills.sh` in `scripts/check-registry.json`. Take the change to
`PRODUCT_SPEC.md:268` to its owner: it is a ratified sentence, and the three-source rule holds the
product suspect before the document.

`defect · internal-conflict (consistency)`

**F8 — A MAJOR release stamped its number into two files and left ten skills behind.**

> "The system *shall* keep the root VERSION file as the one home and *shall* write every skill's
> frontmatter version line … refreshed by the sync script at every bump and held by a guard test
> that reds a drifted copy." — PRODUCT_SPEC.md:8576, Requirement 273 criterion 1 (INV-178)

`VERSION` reads 5.0.0 and `.claude-plugin/plugin.json` reads 5.0.0. Every tracked skill's frontmatter
still reads 4.3.0, and `PRODUCT_SPEC.md:1` still opens at v4.3.0. A host reading any installed skill
is told it runs 4.3.0 while the pack it came from says 5.0.0, and the freshness check of Requirement
136 compares those strings exactly, so it reads every skill as unmoved across a major release.

Run the stamp script over all eleven skills and the spec header in the same change, and decide
explicitly whether `product-prover-pack` is stamped from `VERSION` like its siblings or keeps its own
line. If the latter, write that exception into Requirement 273 rather than leaving it as a silent
third numbering.

`defect · direct-contradiction (contradiction)`

**F9 — A MAJOR release that forces host action shipped no migration chapter.**

> "*when* a release cannot be taken without the host changing what it already carries, the system
> *shall* number it a major and ship its dated migration chapter." — PRODUCT_SPEC.md:8594,
> Requirement 274 criterion 4 (INV-217)

`grep -c '5\.0\.0' MIGRATION.md` returns 0. A host that vendored 4.3.0 has `skills/product-prover/`
sitting in its tree as pack-owned content and is told nothing: not that it must now run the external
installer, not that its own `.gitignore` and config-health expectations moved. Requirement 180 builds
the catch-up work list as the chain of chapters between the host's recorded version and the current
one, so catch-up walks a host from 4.3.0 to 5.0.0 and does nothing at all.

Land a dated `## 5.0.0` chapter naming the three host-side steps: run
`scripts/install-external-skills.sh`, add `skills/product-prover/` to the host `.gitignore`, and
re-run `scripts/sync-skills.sh`.

`defect · missing-prerequisite (precondition)`

**F10 — The adoption path the README prescribes installs a pack whose review step calls a skill that is not there.**

> "Or clone this repository and run `./install.sh`, which copies the skills into `~/.claude/skills/`."
> — README.md:22

`install.sh:8` copies from `skills/`, and `grep -c install-external-skills install.sh` returns 0. So
the documented adoption path gives an adopter ten skills and no prover, silently — the directory does
not exist in a fresh clone, and a loop over it iterates zero times rather than failing. The adopter
discovers it at the Prove step of their first wish, when `build-pipeline` reaches for a skill nothing
installed. Nothing in `adopt/` names the installer either.

Call `scripts/install-external-skills.sh` from `install.sh` and from the adoption walk, and have it
report the external skills it installed in the closing summary `install.sh` already prints. Where the
network is absent, the installer should stop with the one command that supplies the tree rather than
git's own clone error.

`defect · stuck-state (liveness)`

**F11 — Nothing states what happens when the canon is unreachable, the ref is gone, or the install never ran.**

> "*if* no read answers, *then* the system *shall* stop, *shall* hand the person one action that
> supplies the tree, and *shall* start no walk." — PRODUCT_SPEC.md:7610, Requirement 308 criterion 4

Requirement 308 writes exactly this contract for the pack's own tree. No equivalent exists for an
external skill. The installer runs `git clone` under `set -euo pipefail`, so a machine with no network
exits on git's message with no named next action. The absent case is worse because it is silent: the
review step has no body to load, and no gate notices. The edge-condition sweep reads the floor
`>= 1.3.0` as a range end with no other end — nothing says what happens when the canon ships a
breaking 2.0.0, and the pack would install it.

Give the external skill the same three-part answer Requirement 308 gives the pack tree: an ordered
resolution, the version said aloud before any review runs, and a named stop carrying the one command
that supplies it. State separately that a review with no prover installed refuses by name and never
proceeds from memory. Then either pin the floor to a compatible range or write the decided sentence
saying the pack rides the canon's tip and re-proves on every major.

`defect · missing-scenario (state-space)`

**F12 — The runtime view walks no flow for the install, and F-wish's failure column omits the failure this change created.**

> "How each promised flow runs through the nodes [INV-74] … One line per flow: the walk, then where
> it can fail." — ARCHITECTURE.md:703-706

F-wish walks `spec-author → product-prover → build-pipeline`, and its failure column names a misread
door, an unfolded defect, a red suite and a stale lane base. It does not name "the prover is not
installed". The installer can fail at four points — the network, an unreadable `requires:` line, a
body with no version stamp, a version below the floor — and belongs to no documented walk. Nothing
says who runs it or when. Architecture check 5 fails for the one flow the change created.

Add a runtime row for the external-skill install with its walk, its four failure points, and the
consequence that the review step refuses by name rather than proceeding without the prover.

`defect · missing-scenario (state-space)`

**F13 — Six tracked inventory rows and pins still cite the three deleted files.**

> `| Product-prover skill | skills/product-prover/SKILL.md | shipped text | test_artifact_inventory |`
> — TEST_MATRIX.md:49, with README at :80 and LICENSE at :81

Requirement 283 demands the inventory name every file the reader receives. The reader of a fresh
clone receives none of these three. The rows are green here only because the gitignored clone happens
to sit at the path — a hollow green of exactly the class the pack has a requirement to close.
Separately, Requirement 244's node-growth ratchet counts nodes per file from `ARCHITECTURE.md`'s pin
column, so it is now counting an untracked foreign file.

Retire the three matrix rows the way Requirement 124 retires a stale row citing an absent anchor —
retired, not vanished — and re-home the three architecture pins per F1.

`defect · boundary-issue (composition)`

**F14 — The spec writes a skill joining the pack and never writes one leaving it.**

> "a member add covers a new invariant joining a family, a new skill joining the pack, and a second
> sibling the intake question catches." — PRODUCT_SPEC.md:1618, Requirement 66 criterion 2 (INV-170)

Requirement 66 fires the quantifier re-verify on every member add. No requirement states what a
member removal owes. This commit is exactly that removal, and nearly every finding above is a
quantified sentence the removal falsified that nothing re-verified: the working-skills list, the
published counts, the artifact inventory, the pins, the eval set. Requirement 261 (INV-126) already
makes the general case a defect — a paired state change with one direction described and the other
silent — and the prover's own lifecycle sweep reads it the same way. This is that defect at the level
of the pack's own membership.

Add a criterion to Requirement 66: when a member leaves the pack, the system shall re-verify the same
quantified sentences and enumerations against the shrunk set, and shall name every list, count, pin
and inventory row that cited the departing member.

`defect · undefined-path (transitions)`

**F15 — The installable-artifact class gained a fifth member with no staleness net.**

> "The system *shall* have a new installable artifact state its own staleness net against this
> parity, the members named before the class standing as they are cited." — PRODUCT_SPEC.md:8626,
> Requirement 275 criterion 6 (INV-180)

The class enumerates four members and their nets: vendored kit scripts, installed hooks and gates,
stamped version copies, installed skills. The external-skill clone is a fifth kind and names none.
Nothing tells a maintainer the clone has gone stale against its canon: it reads `version: 1.3.0`,
matching the floor exactly, and no check re-reads it. When the canon ships 1.4.0 with a moved lens,
every review in this project runs the older lens set while the record truthfully says 1.3.0.

Add a criterion naming the external install's net, and implement it as a recorded ref or commit the
daily update check reads — the same shape criterion 2 gives the vendored kit. Simplest form: have the
installer write the resolved commit into `.live-spec/` and have the freshness check compare it.

`defect · missing-rule (invariant)`

**F16 — A fourth pin is rotten, unrelated to this change.**

> `skills/live-spec-base/SKILL.md:634` (ladder) — ARCHITECTURE.md:81

Line 634 is blank; `## The settings ladder` stands at 628. This predates be4e4f0 and the prover's
scoped-review rule would make it a tracked follow-up — but this pass was asked for a full review, and
gate g does not distinguish: it fails as one unit, so the push is refused until this pin moves too.

Repoint to `skills/live-spec-base/SKILL.md:628`.

`defect · missing-rule (invariant)`

**F19 — The prose census still holds a zero-findings record for the deleted body, and gate aa now applies it to the external canon.**

> `"skills/product-prover/SKILL.md": {"bytes": 73386, … "total": 0}` — guardrails/rule-census.json

Those 73,386 bytes are the internal body this commit deleted; the external canon measures about
51,000. The record was earned by text this repository no longer ships, and
`check-doc-findings-bound.py` — whose rule is that a document repaired to zero stays at zero — now
re-measures the installed clone against it and reports 3 findings. So the pack's prose gate is
judging the external repository's prose, on a standard the external repository never agreed to and
cannot see. Every prover release will now red this gate whenever its prose differs from the deleted
body's, and the maintainer of this pack cannot repair the text, because it belongs to another
repository. The same stale pair stands for `skills/product-prover/README.md`.

Drop both `skills/product-prover/` entries from the census, since the census's subject is the text
this repository ships. Then state in the census's ground block that an installed external skill is
out of its domain, so the next installer-created directory does not silently re-enter it. Gate aa's
other fault today, `skills/live-spec-base/SKILL.md` rising from 68 to 69 findings, predates this
change and is a separate repair.

`defect · boundary-issue (composition)`

**F17 — `editions/product-prover/` is still tracked and can now never publish.** *(non-blocking)*

`git ls-files editions/product-prover/` returns a full skill — `SKILL.md`, `LICENSE`, `README.md`,
`PROVENANCE.md`, examples and evals. The same commit that called the external repo the single source
of truth added a guard to `scripts/sync-mirrors.sh` that `continue`s past `product-prover` at line
442, and the edition publishes from inside that same loop at line 527. So the edition is tracked
content that no sync reads, no gate holds and no reader receives, while the same text also lives in
the external repository. `ARCHITECTURE.md:37-38` still tells a reader an edition is what that skill's
public mirror ships. It does not block because nothing consumes it today, which is precisely why it
will rot unwatched.

Move it to `attic/` with a manifest line per Requirement 179, and add a criterion stating that an
external skill ships no pack-side edition.

`recommendation · now · boundary-issue (composition)`

**F18 — The pin map has already drifted on two lens names before its first release, and nothing reads it.** *(non-blocking)*

> "When a lens moves or renames in a prover release, this table is the one place the pack updates." —
> skills/product-prover-pack/SKILL.md:55

All sixteen requirement codes in the map exist in `PRODUCT_SPEC.md`, and all ten named lenses exist
in the installed canon — so the map is sound in substance. Two names are already wrong: the pack
writes "Interactive-overlap across layers" where `reference/stress-lenses.md:310` heads it
"Interactive overlap across layers", and "False-serialization and over-broad independence edge"
where `:365` heads it "False serialization and over-broad independence". No gate, no test and no
criterion reads this table, so a rename in the canon invalidates it in silence.

Bring both names to the canon's headings verbatim, and add a check resolving each row's lens name
against a heading in the installed files, standing down by name when the clone is absent per F11.

`recommendation · now · hard-to-operate (ops-ux)`

## Acknowledged gaps

`ROADMAP.md` rows 618 and 619 already carry two of this territory's problems: the prover's body
running past its sizing guidance with no reference directory, and the internal copy drifting from its
public edition under a guard that reads timestamps alone. Row 618's premise moved under it — the
canon now ships at 837 lines with a `reference/` directory — and row 619's subject is F17's edition.
Both rows owe a re-read against the decoupling rather than a fresh finding here.

`acknowledged · boundary-issue (composition)`

## Coverage

The create-read-update-delete and authorization tables read N/A for this product and are replaced by
this line, as the prover's Phase 3e allows: the pack holds no user-mutated persistent entities and no
roles. The surface × sweep table stands as the coverage artifact.

| Surface | Cross-cutting laws | Edge conditions | Policy uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| `PRODUCT_SPEC.md` | hit (F8, F9, F15) | hit (F2, F11) | hit (F6, F15) | hit (F14) | hit (F2, F13) |
| `ARCHITECTURE.md` | hit (F1) | hit (F11, F12) | hit (F7) | hit (F12) | hit (F3, F4) |
| `scripts/install-external-skills.sh` | hit (F15) | hit (F11) | clean | hit (F10) | hit (F3) |
| `skills/product-prover-pack/SKILL.md` | clean | clean | hit (F18) | clean | hit (F3) |
| `install.sh` | clean | hit (F10) | clean | hit (F10) | hit (F10) |
| `guardrails/rule-census.json` | hit (F19) | clean | hit (F19) | clean | hit (F19) |

The surface inventory is review-derived, labelled that way here: `SURFACES.md` names no entry
reading `skills/product-prover/`, so the five rows above were extracted in Phase 1 from the change's
own footprint.

Class lens: swept — one class filed, *a node's body left the repository and every pointer at it was
left standing*, carrying F1, F2, F4, F5, F6, F7, F8, F9, F10, F12, F13, F17, F18 and F19. Three
sub-groups sit under it: filesystem readers of `skills/` that now read an untracked directory
(`tests/test_traceability.py:945` and `:1145`, `guardrails/check-config-health.sh:101`, `install.sh:8`,
`guardrails/tree-counts.json`, `guardrails/rule-census.json`); tracked artefacts pinning into the
deleted files (`TEST_MATRIX.md:49`, `:80`, `:81`, `ARCHITECTURE.md:135`, `:136`, `:138`,
and the census's two `skills/product-prover/` entries); and pack-list surfaces missing the newborn skill
(`PRODUCT_SPEC.md:268`, `OVERVIEW.md`, the five "The pack, whole:" footers). The structural cause is
F3, the undrawn seam.

## What the re-derivation corrected

Three claims from the two readers did not survive the seat's re-derivation and are recorded rather
than carried, and one of the seat's own runs was wrong before it was re-run.

- One reader read `[node: product-prover]`'s fourth pin, `.live-spec/profile.md:6`, as part of the
  rotten set. It resolves: line 6 carries `prover.cadence`, the file is tracked, and
  `check-pin-drift.sh` passes it. Only three of the node's four pins are rotten.
- One reader called the commit message's "pin map for 15 requirement codes" an error against a table
  of sixteen. The table carries sixteen distinct codes across ten rows; the commit message is off by
  one, which is a commit-message defect and not a document one, so it takes no finding.
- One reader reported the eval law red in both directions. `evals/product-prover.md` is indeed a
  tracked eval for a body this repository no longer ships, and `evals/product-prover-pack.md` is
  absent; the observed run confirms `test_skill_evals_present` red. That part stands, folded into F6's
  sweep rather than kept as its own finding.
- The seat's first gate sweep piped each gate through `head`, so the exit code it read was `head`'s
  and not the gate's. Gate aa was reported OK on that evidence and is in fact red, which is F19. The
  gates were re-run unpiped, and every verdict in the Checks-run list above is the gate's own. This is
  the pipe-through-a-pager trap the pack has already recorded once; it caught this pass too.

## What holds

Two things survived the whole pass. The bindings page is the right shape for the job: it collects the
mode names, the pack paths, the record contract and the pin map on one page, and every requirement
code on it resolves. And the installer holds its floor honestly — it reads the minimum from the
bindings page rather than carrying a second copy of the number, refuses a version below it by name,
and is idempotent.

## Readiness

Needs another iteration. The decoupling's design is sound and its execution left the two requirements
documents behind. Sixteen blocking findings stand, and three of them are already red on gates in the
push chain — g (pin drift), ad (tree counts) and aa (doc findings bound) — so the chain refuses on its
own evidence before it reaches this record.

Blocking: sixteen, and none is closed in this range. The commit carrying this record was ordered to
carry the record alone, so every repair below is owed by a following change.

- Finding 1, three architecture pins into the removed body — stands: `check-pin-drift.sh` fails on
  `ARCHITECTURE.md:135`, `:136` and `:138` today. Closes when all three are re-homed onto
  `skills/product-prover-pack/SKILL.md` and gate g passes.
- Finding 2, the published counts red and the measurement non-deterministic — stands:
  `check-tree-counts.py` exits 1 with 3 faults today. Closes when the measurement is scoped to tracked
  files and the block is regenerated.
- Finding 3, no seam row for the pack-to-canon boundary — stands: the boundary the change created has
  no row in a table whose stated job is to name every one. Closes when the row is written with its
  format owner.
- Finding 4, the placement view naming the wrong home — stands: architecture check 6 fails against the
  shipped tree. Closes when the sixth placement row lands.
- Finding 5, the suite asserting on absent strings — stands: 21 failed, 188 passed observed over five
  modules; twenty-six modules read the path. Closes when the assertions are re-pointed and the group
  is skip-guarded.
- Finding 6, the working-skills sentence — stands: `test_real_repo_lists_complete` is red. Closes when
  every pack list names the set the tree carries.
- Finding 7, "ten working skills" and the nodeless new parts — stands: twelve directories against a
  stated ten, and three parts with no node and no requirement. Closes when line 35 is rewritten, the
  bindings are folded into the prover node, and the installer is registered.
- Finding 8, the version stamps — stands: `VERSION` 5.0.0 against ten skills at 4.3.0. Closes when the
  stamp script runs across the release.
- Finding 9, the missing migration chapter — stands: `MIGRATION.md` names 5.0.0 nowhere. Closes when
  the dated chapter lands with its three host-side steps.
- Finding 10, the adoption path that installs no prover — stands: `install.sh` never calls the
  external installer. Closes when it does and the summary reports it.
- Finding 11, the unanswered unreachable, missing-ref and not-installed cases — stands: no requirement
  covers them. Closes when the external skill gets Requirement 308's three-part answer.
- Finding 12, the runtime view's missing walk — stands: architecture check 5 fails for the new flow.
  Closes when the install walk and its failure points are written.
- Finding 13, the six inventory rows and pins citing deleted files — stands: `TEST_MATRIX.md:49`,
  `:80`, `:81` claim files a fresh clone never receives. Closes when the rows are retired and the pins
  re-homed.
- Finding 14, member-add written and member-removal silent — stands: no requirement states what a
  removal owes. Closes when Requirement 66 gains its removal criterion.
- Finding 15, the fifth installable artifact with no staleness net — stands: nothing re-reads the
  clone against its canon. Closes when the net is named and implemented.
- Finding 16, the fourth rotten pin at `skills/live-spec-base/SKILL.md:634` — stands: gate g fails as
  one unit, so it holds the push with the other three. Closes when the pin moves to `:628`.
- Finding 19, the census judging the external canon on a deleted body's record — stands: gate aa is
  red today, reporting the installed clone at 3 findings against a zero it never earned. Closes when
  both `skills/product-prover/` entries leave the census and its domain says so.

The three non-blocking items — F17's stranded edition, F18's drifted pin-map names, and the
acknowledged roadmap rows — carry no push weight and wait on a judgment call.
