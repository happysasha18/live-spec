# Prover record — 2026-08-31, three lanes merged and the merge reviewed

PUSH-REVIEW

Range: 57ec6d85..HEAD. Base commit `57ec6d85`, the head `origin/main` carries. Every commit in the
range, in order: `1d64b25c`, `b59e6cd9`, `cf594500`, `55cd491d`, `98a003b5`, `b8fce842`, `a0e90df1`,
`3596533a`, `30ec1256`, `c32cb024`, `ad2dbb55`, `a82c15ae`, `df3f1019`, `02a04e80`, plus the repair
commit this record ships in, which names it below. Fourteen commits at the time of writing: seven
from the one-home lane, one from the playbook lane, two from the spec lane, three merge commits and
the follow-up landing that closed the two loose ends.

Prover version that ran: product-prover 1.6.0 as installed on this machine, under the pack bindings
in `skills/product-prover-pack/SKILL.md` 6.0.0. The project pins 1.4.2 for the server; the gap is
finding 12 below.

## How this review was run

The three lanes were merged onto main, then read to refuse. Two fresh-context readers with no part in
building any of the lanes went over the merged result in parallel — one on the prose, the pins, the
cross-document facts and the merge itself, one on the checks and gates the lanes shipped, working in
its own copy of the tree so no second writer touched the judged one. Each was briefed to find reasons
to refuse. Every finding below was reproduced before anything was changed, and every repair is
red-proven against the code that shipped it.

The interesting thing about this pass is where the defects were. Each lane was green in its own tree.
Almost nothing below is a defect of a lane's work; the defects are of the merge, and of checks that
passed in a tree where the thing they guard happened to be arranged conveniently.

Files read: `PLAN.md`, `NEXT_STEPS.md`, `JOURNAL.md`, `PRODUCT_SPEC.md`, `PRODUCT_SPEC.index.md`,
`ARCHITECTURE.md`, `ARCHITECTURE.index.md`, `TEST_MATRIX.index.md`, `spec/message-first-read.md`,
`spec/spec-extension.md`, `spec/wish-intake.md`, `spec/design-spec-review.md`,
`spec/doc-order-generated.md`, `architecture/pipeline-and-lanes.md`,
`architecture/rules-and-settings.md`, `architecture/authoring-and-review.md`,
`architecture/feature-coverage.md`, `matrix/director.md`, `guardrails/specformat.py`,
`guardrails/check-index-generated.py`, `guardrails/check-matrix-reference.py`,
`guardrails/check-architecture-reference.py`, `guardrails/check-pin-drift.sh`,
`guardrails/check-skill-review.sh`, `guardrails/check-prover-record.sh`, `guardrails/check-tests.sh`,
`guardrails/pre-push`, `.github/workflows/gates.yml`, `scripts/plan_checks.py`,
`scripts/state-probe.sh`, `scripts/sync-skills.sh`, `skills/director/SKILL.md`,
`skills/director/references/lanes-and-pen.md`, `skills/live-spec-base/SKILL.md`,
`skills/architect/SKILL.md`, `skills/spec-author/SKILL.md`, `skills/communicator/SKILL.md`,
`tests/test_one_home_per_rule.py`, `tests/test_first_read_carrier.py`, `tests/test_spec_parts.py`,
`tests/test_traceability.py`, `tests/test_agent_card.py`, `tests/test_lane_branch_road.py`,
`tests/test_catchup_walk.py`, `tests/test_guardrails.py`, `tests/test_plan_is_not_executable.py`,
`tests/test_director_wire_report.py`, `tests/conftest.py`,
`attic/feature-names-retired-2026-08-31.md`, `docs/reports/2026-08-31-playbook-repo.md`,
`docs/prover/2026-08-31-one-home-per-rule.md`, `docs/skill-review/2026-08-31-one-home-per-rule.md`,
`docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md`,
`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`, and the three lane branches at
their tips.

Checks run: fourteen, each with its result.

1. `python3 -m pytest -q`, the whole suite, alone on the merged tree with no worker active — 12
   failed, 2602 passed, 4 skipped, 1016.96s. The failures are findings 1 and 12 below.
2. `bash guardrails/check-pin-drift.sh` before the repair — exit 1, naming
   `scripts/state-probe.sh:195`. After — OK, 180 pins checked, 61 line pins against their own line,
   113 file-level, 6 unlabelled; and OK on the 39 range pins of the rule-prices reader.
3. `LIVE_SPEC_DIFF_BASE=57ec6d85 bash guardrails/check-skill-review.sh` before the record — exit 1,
   naming `director` changed in `02a04e80` with no covering review. Finding 2.
4. `bash guardrails/check-prover-record.sh` before this record — exit 1: the newest committed record
   predates the last spec change. Finding 3; this record is its answer.
5. `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — OK, 404
   locations, 32 parts named by the map, 313 requirement numbers each claimed once.
   `check-matrix-reference.py` — OK, 551. `check-architecture-reference.py` — OK, 411 anchors.
6. Every line each lane branch added, longer than a few words, looked for in the merged file at HEAD.
   Missing lines: the two superseded status-block headers, the two "row stays open" paragraphs the
   follow-up landing replaced, two pins the same landing re-pointed, and the four-arm form of one
   plan key that grew to nine. Every one accounted for. No content lost at the three merges.
7. INV-322 red-proven independently in a scratch copy against all three reference gates: a real
   requirement dropped into `spec/`, `matrix/` and `architecture/` as an unnamed part reds each gate
   by name, with no other fault firing; removing it returns all three to exit 0.
8. INV-323 red-proven the same way: `spec/draft-sandbox.md`'s requirement renumbered onto
   `spec/wish-intake.md`'s reds `check-index-generated.py`, naming the number and both lines.
9. `tests/test_one_home_per_rule.py`'s three arms proven to reach live text, one mutation each: a
   second copy of the report format appended to the communicator reds by file; the home's own
   sentence reworded reds as moved-or-lost; a pointer replaced by a paraphrase reds as leaving the
   reader nowhere. An unrelated paragraph appended to the README stays green.
10. The same file's table emptied to `{}` — before the repair, exit 0 and three skipped cases; after,
    exit 1 naming all three rules. Finding 4.
11. `scripts/state-probe.sh`'s comparison reversed in a scratch copy — before the repair, all five
    checks green; after, the new one reds naming both directions. Finding 6.
12. 34 of the 35 recorded reading runs deleted in a scratch copy — before, green; after, red naming
    the scenarios with no run. Finding 7.
13. `guardrails/specformat.py`'s unnamed-part reader emptied to `return []` in a scratch copy — the
    plan key for the spec task exited 0 before the repair and exits 1 after. Finding 8.
14. `bash scripts/install-worker-restore-guard.sh` (already present, self-tests OK) and
    `bash scripts/sync-skills.sh` (ten skills refreshed), then
    `python3 -m pytest -q tests/test_config_health.py` — 34 passed.

Findings: twelve. Nine repaired here, three standing with their reason.

### The merge's own class

**1. Sixteen `file:line` pins named the wrong line after the merge, and the gate saw one of them.**
Each lane pinned into files another lane was editing, and each was right in its own tree. After the
merge, `architecture/pipeline-and-lanes.md`'s pin at `scripts/state-probe.sh:195` landed on a line
reading `b "FACTS"`, which the pin-drift gate reds. Fifteen more were off by one, two, three, five or
forty-six and passed only because that gate forgives a two-line miss — the exact shape its own header
warns about. Eight into the rulebook from `architecture/rules-and-settings.md`, two more from
`architecture/pipeline-and-lanes.md`, one into the architect skill, one into the spec author, and one
pre-existing pointer at the settings ladder that was wrong before this range began. All sixteen were
re-read against the files and corrected. **Closed.**

**2. The follow-up landing edited a skill and shipped no review record.** `02a04e80` added the
decision sheet's ordering field to `skills/director/SKILL.md`; the newest review record covered the
one-home landing an hour earlier. `docs/skill-review/2026-08-31-decision-sheet-ordering-line.md`
covers it. **Closed.**

**3. The record on file claimed a range six commits long, and the range is fourteen.**
`docs/prover/2026-08-31-one-home-per-rule.md` was written inside one lane and reads `Range:
57ec6d85..HEAD (6 commits, plan-16)`, listing no commit hashes at all. That record keeps the range it
actually read; this one covers the whole of what is being pushed and names every commit. **Closed.**

### Checks that passed because the tree was arranged conveniently

**4. The one-home check could be switched off with no red anywhere.** Its three arms are parametrized
over a table of rules, so an empty table generates no cases at all: pytest reports three SKIPS, and
the plan key that runs the file exits 0. Dropping a single rule narrows the reach the same silent
way, and nothing else in the tree asserts anything about that table. This is the shape the gates under
`guardrails/` already refuse — each declares its expected-non-empty input and reds by name rather than
passing over nothing — and `scripts/plan_checks.py`'s own reader takes the same precaution. A floor is
named in the file now and only grows. **Closed.**

**5. The check that keeps a feature name off an unbuilt scenario read a leg's marker as the
scenario's.** It searched a requirement's whole body for the promised-marker, while the spec's own
glossary says the marker marks a feature OR A LEG, and fifteen of the nineteen markers in the spec
today are leg-level. The project's other reader of the same marker is already leg-scoped: it climbs to
the line above and reads that line's anchors. Two readers of one convention disagreeing is the class
this project keeps finding. The check passed today only because no leg-level marker happens to sit
under a tagged heading; the first author to mark a promised leg on a named feature would have been
pushed into deleting a true marker or a true name. It reads the marker the way the spec writes it now
— on its own line, belonging to the line above it — so a marker under the heading marks the scenario
and a marker under a criterion marks the leg. Prose that merely quotes the marker, which Requirement
316 does twice, is no longer read as a marker at all. Both directions carry a proof. **Closed.**

**6. The proof that the opening probe tells a stale score from a fresh one never ran the branch.**
All five checks were string searches over the probe's source. Reversing the comparison — a stale score
printing bare, a fresh one labelled a replay, which is precisely the failure the file's own opening
names — left both commit-time reads, both marker strings and the score line exactly where they were,
and every check green. The branch is lifted out of the script and run both ways now. It is found by
walking up from the line that prints the label to the `if` that guards it, so the test does not name
the operator and quietly become a source check again. **Closed.**

**7. "The recorded runs each answer a written scenario" checked that the folder was not empty.** One
run out of thirty-five passed it, while the grader says on the same line it already reads how many
scenarios it found no run for. The count is asserted now. **Closed.**

**8. The spec task's acceptance command read three function names out of two test files.** A function
name decides nothing about what the function asserts. The unnamed-part reader could be emptied to a
bare return — leaving the gate blind to a stray part — and the command still reported the task done.
The two proofs run for real now, by direct execution rather than through a suite, which is the pattern
the one-home key already used; four tenths of a second for both files. **Closed.**

### Claims that were not true

**9. The feature roster went from seventeen names to twelve, not ten.** Counted three ways: twelve
distinct tags across the spec and its parts, twelve rows in the coverage table, and the attic page's
own arithmetic, which says six leave and one arrives. The wrong number stood in the resume file, the
plan and the journal — the resume file being what the next session reads first. **Closed.**

**10. Requirement 314's context enumeration lagged its own criterion.** The follow-up landing repaired
the criterion's field list and left the context paragraph naming neither the ordering field nor the
dimensions. Two homes for one fact, inside one requirement. **Closed.**

**11. The playbook report still prescribed work that had already run.** Its opening said the personal
layer had never been pushed and its ordered action list opened with `git push`; all eight steps had
run from that repository's own window and everything was pushed. The analysis is kept as written,
since the reasoning behind the answer is what the page is for, and a dated section at the top says what
has happened since. **Closed.**

### Standing, with their reason

**12. Five checks are red because the external reviewing skill on this machine is three releases ahead
of what this project pins.** `skills/product-prover/` is its own repository and was released three
times today, to 1.6.0, which reworded the merge-gate and finding-routing clauses and moved a third of
its body into side files. `.github/workflows/gates.yml` pins commit `efe05fa`, v1.4.2, installs it
before the suite, and is green on the server. The local clone stands at `90d2d5c`. The five checks
that quote the older wording therefore fail here and nowhere else. Neither this range nor any work in
this project caused them, and neither can repair them: moving the pin means re-pinning five assertions
against reworded canon, which is its own piece of work, and putting the local clone back on the pinned
commit would write into a repository this pass was told not to touch and where another window may be
working. Named in the plan's blocked list. **Stands.**

**13. A promise this range added is owned by no row, and the check that would demand one cannot see
it.** Requirement 315, the idea shelf, carries its promised marker under the heading. The ownership
check climbs to the line above a marker and reads that line's anchor codes; a heading carries none, so
the promise never enters the map and no open row is required. It is the same argument that put q-437
back on the board in this range, applied to the promise the range itself made. Closing it means either
opening a row for the idea shelf or teaching the check to read a heading-level marker, which would then
demand that row anyway — and which of those is right is a question about the board. In the plan's
blocked list. **Stands.**

**14. The report format's own content has no checker in this repository.** The one-home landing
replaced five assertions that pinned the format's content with assertions that the agent card POINTS at
its home, which is correct — the home is the owner's own file, outside this tree. The consequence is
that `python3 tests/test_one_home_per_rule.py` proves no second copy exists and never proves the one
home holds anything. Deliberate and documented in the new docstring; a checker would have to read a
file this repository does not own. **Stands.**

### Also checked, and clean

Nothing in the range loosens, skips, or adds an exception to a check: no stand-down marker was added,
no tolerance widened, no gate letter dropped. The removed test assertions across the range are exactly
the seven of finding 14 plus two that moved to a better home with a new assertion guarding the
director's own clause. `check-landing-next-steps.py`, `check-doc-rotation.py`,
`check-config-health.sh` and `check-freeze.sh` are green over the range. The reopened q-437 row parses
under both readers of the board — `q-437 → ⬜`, group and priority present. The re-point of the
composition-axes promise from the closed spec task to q-437 is the existing ownership check doing its
job, not a loosening: leaving the map where it was would have reddened at the close.

Blocking: none
