# Push review — 2026-08-05 day of readability repairs

PUSH-REVIEW

Range: c869cbb..124d9cc

Commits:
- 124d9cc The status block reads the pushed state and names what stands open
- 642d229 The day's push carries an adversarial review of all its commits
- 44778ea Four evening arrivals become two rows and one correction, all kept in the attic
- 12acab2 The journal keeps the afternoon's review and the stash incident
- ad31edb The harvested messages rest in the attic and their rows cite them there
- 3f33ac5 The public edition catches up with its skill, and every refusal names its own case
- 2ea1cc4 The restore gate reads a failed cd, a quoted script and a wrapper prefix the way a shell does
- 2a8368a Anchor the user-language marker to a real comment opener, not a URL or path substring
- 7e39f75 The renamed word reaches the matrix rows and docstrings the sweep missed
- 467d667 The wording check no longer joins a phrase split across a paragraph break
- 8054fc3 The census skips a directory only at a path boundary
- 887ff4e The four defects the push review confirmed close, and the reading split is stated as the records hold it
- 29ebe2e The status block's counts match the records they cite
- b04e029 Review corrections land: the cited record, this skill's own sums, and the meaning-check reader
- 2343ac9 Two afternoon inbox arrivals harvest: one row, one landed fix, both kept in the attic
- 91ab6aa The language marker clears a string in every comment form a file can carry
- 1378b47 Skill-creator review of text-audit after the day's repairs
- d5bb900 The status block reads the day it just lived, and the journal keeps its why
- e6790b3 The recorded ceilings come down to what the files measure today
- 26719d9 Round 30 blocking stops close: three spec-only lints named, and step 3 orders refutation
- 48bc61e A review addendum covers the re-pinned rename sentences
- 9c2cc87 The last three sentences carrying the old word take the new one, tests re-pinned
- da6da0f The renamed word reaches its glossary, examples, matrix row and test
- b6eb51a Round 30-31 closes: the audit skill's numbers reconcile with their sources
- 50537d6 The restore gate places a command in the directory it really ran in
- f47408e The reporting skill's renamed word never reached its own reference files
- 58aec31 The block-drift arm reads every generated block a page lends
- 85b8265 The design map points at the lines its labels name again
- 0d5c3f3 Each language rule holds one owner, and three stated totals generate
- 7acf349 The pin gate earns a queue row after 29 stale pins passed it
- cbee7f0 The nine new queue rows read within the record
- a893716 A fresh prover pass re-reads the design map's pointer catch-up
- 5a41cf5 The design-review pointer describes the design pass it names
- dce526c The audit skill says which file holds which record, and blocking has one definition
- 1167ae9 Five inbox messages become nine queue rows and one row grows
- fd22f3c The reading queue leaves fixtures and templates unmeasured
- 83ebd2d The wording check reads a phrase broken across a line break
- 50fffff Two more design-map pointers catch up with a rewritten skill
- c3c9899 The mirror sync ends non-zero when it published nothing
- 52aa815 Three pages stop pointing a reader at the old templates
- fcc9107 A new project starting from the templates passes the gates
- a1f6792 The audit names the text its own readers never see
- 5e157de The shared rulebook comes down from 226 findings to 92
- b99b7eb The spec-writing skill names how to run each gate it cites
- a97f95b The reporting skill drops a coined word its own check bans
- cefd11d A push carries an adversarial review of the change it sends
- 6167a6e The design map comes under its own cap, and its pins all resolve
- a229b0d The pipeline skill names every template, command and code it uses
- e43e814 The install path a stranger follows now works end to end
- 258d544 The consistency skill comes down from 72 findings to zero
- 17434b7 Every step the review skill names can now be performed
- 1a7ecbe The reading step runs two readers, and the auditor merges them
- 1d10642 The public-edition mechanism carries its requirement and its rows
- b20eee3 The settled-questions page reads clean, and the count is pinned
- 091deed The audit skill says which of its checks read a spec alone
- b4e1425 The first public edition ships, and a half-made one publishes nothing
- 4071f8a A skill's public mirror ships the edition a stranger can read
- eb1d4a5 Every place that states the skill count says what it counts

The range holds 56 commits: the 21 read in the first pass, plus 35 read after. All touch a file outside
`docs/push-review/`, so the gate counts all 56 as reviewed.

The branch grew twice while this review ran. The first 19 commits were read first. Commits c3c9899
and 50fffff landed later and were read after. `docs/PROGRESS.md` and `guardrails/progress-baseline.json`
stand modified and uncommitted, carrying regenerated counts. One inbox message stands untracked, and
finding 21 covers it. Another session is editing this tree, so a commit landing after this record
needs its own reading.

The branch then grew a third time, by 35 more commits, from 50fffff to 44778ea. Four adversarial
reviewers read that stretch this afternoon and evening. Their confirmed findings are recorded below as
findings 22 to 31, each already closed by the commit named beside it. This addendum does not repeat the
checks run against the first 21 commits; it records what the four reviewers found in the 35 that
followed, and what still stands open.

Files read: guardrails/check-push-review.sh, guardrails/check-prover-record.sh, guardrails/pre-push, guardrails/gate-red-proofs.json, .github/workflows/gates.yml, docs/push-review/README.md, PRODUCT_SPEC.md (Requirements 304 and 305), TEST_MATRIX.md (rows M-491 to M-496), scripts/sync-mirrors.sh, scripts/check-shipped-language.py, scripts/rule-census.py, guardrails/check-skill-loadability.sh, guardrails/check-skill-review.sh, guardrails/check-pin-drift.sh, guardrails/check-doc-findings-bound.py, guardrails/local-overrides.json, ARCHITECTURE.md, README.md, editions/product-prover/ (SKILL.md, README.md, PROVENANCE.md, reference/stress-lenses.md, examples/sample-spec.md), skills/product-prover/SKILL.md, skills/design-reviewer/SKILL.md, skills/live-spec-base/SKILL.md, skills/spec-author/SKILL.md, skills/build-pipeline/SKILL.md, skills/communicator/SKILL.md, skills/text-audit/SKILL.md, templates/*.template.md, tests/test_mirror_editions.py, tests/test_push_review.py, tests/test_skill_count_agrees.py, tests/test_text_audit_fixtures.py, tests/test_convergence_locks.py, adopt/install-scaffold.sh, scaffold/guardrails.config.example.json

Checks run: (each command, then its result)

- `python3 -m pytest -q` — run 1: 2 failed, 2359 passed, 1 error, 447s. Run 2, with a temporary
  directory of its own: 3 failed, 2358 passed, 435s. See findings 1 and 13.
- `python3 guardrails/check-worker-restore.py --since-hours 24` — exit 1. See finding 13.
- `python3 -m pytest tests/test_mirror_editions.py tests/test_skill_count_agrees.py
  tests/test_push_review.py tests/test_text_audit_fixtures.py -q` — 45 passed, no skips
- `bash guardrails/check-prover-record.sh` — exit 1, twice, on two different arms. See finding 1.
- `python3 guardrails/check-doc-findings-bound.py` — exit 0 on the first reading, exit 1 after an
  inbox message appeared. See finding 21.
- `python3 guardrails/check-every-gate-can-fail.py` — exit 0; 29 gates, each with a red proof
- `bash guardrails/check-ci-mirror.sh` — exit 0; every local gate mirrored in CI
- `bash guardrails/check-skill-loadability.sh` — exit 0; 11 skills load
- `bash guardrails/check-shipped-language.sh` — exit 0; no offences in the shipped set
- `bash guardrails/check-config-health.sh` — exit 0; installed hooks match their sources
- `bash guardrails/check-freeze.sh` — exit 0; guarded documents match their baseline
- `bash guardrails/check-pin-drift.sh` — exit 0, four pins reported as drifting at the current head.
  See finding 8.
- `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md` — exit 0; 495 of 495 rows matched
- gates e, j, l, o, p, q, r, s, t, x, y, z, ab each run alone — each exit 0
- `bash adopt/install-scaffold.sh` in a fresh project cloned from this branch — exit 0, five files
  vendored, configuration seeded; the four vendored checks then run. See finding 10.
- `bash guardrails/check-push-review.sh` in seven scratch repositories built to probe the new gate —
  results under findings 2, 4, 5 and 7
- `bash scripts/sync-mirrors.sh --print-publish-source product-prover` — prints the edition directory
- `python3 scripts/preshow-register-lint.py skills/communicator/SKILL.md` — exit 0, and the banned
  word stands on the page. See finding 15.
- `cat skills/*/SKILL.md | wc -l` — 5178. `find skills -name '*.md' -exec cat {} + | wc -l` — 7121.
  See finding 20.

Findings: twenty-one, of which twelve block. Two push gates refuse this range today. The new push
gate accepts an empty record and lets an open blocking finding through, and the test matrix states the
opposite of both. The push publishes a public edition that lags the skill it copies. The tests added
today assert on script text rather than on behaviour, so a disarmed gate leaves them green. Five of
the day's rewrites changed what a rule requires while their commit messages claimed a readability
repair. The rest are recorded below with the file and line each stands on.

Blocking: - finding 1, gate a refuses this range — stands: the spec change that added the push-review requirement carries no prover record
- finding 2, an empty committed record satisfies the new gate — stands: the gate reads the working tree, and the test matrix claims the opposite
- finding 3, the public edition ships a copy the same day's repair never reached — stands: nothing reads the real edition, and this push is what publishes it
- finding 4, an open blocking finding passes the gate two ways — stands: the requirement says an open blocking finding holds the push
- finding 5, the review directory is a hole in the gate that guards it — stands: the requirement's wording is narrower than the script
- finding 6, the tests added today hold script text rather than behaviour — stands: a disarmed gate and a restored regression both leave them green
- finding 15, the reporting skill still carries the word its commit says it dropped — stands: the check that bans the word cannot see it across a line break
- finding 16, a fallback table became a duty on every pass — stands: the skill now requires what the spec states as a replacement
- finding 17, two hard rules in the review skill gained exceptions no spec states — stands: each lets a pass skip a step the rule existed to force
- finding 18, the pipeline skill points at the wrong section of the reporting skill — stands: a reader following it lands in the wrong place
- finding 19, the pipeline skill's list of skill-invoking steps omits one — stands: a reader budgeting the walk drops the architecture prove pass
- finding 20, the front page states a line count the tree contradicts — stands: the number is new in this push and wrong in both readings
- finding 21, gate aa refuses this tree — stands: a live document carries no entry in the record the gate reads

Verdict: do not push. Two gates in the chain refuse this range today, findings 1 and 21. Ten further
blocking findings stand open. Six of them are cheap: findings 15, 18, 19 and 20 are wording, finding
16 restores one sentence, and finding 21 is one command. Findings 2, 4 and 5 are one edit each to the
new gate. Findings 3, 6 and 17 need real work. The push becomes lawful once every blocking finding is
closed and this record is rewritten over the range that then stands.

## Blocking findings

### 1. Gate a refuses this range

`guardrails/check-prover-record.sh`, run at the repository root today:

```
FAIL (prover record): the newest committed prover record predates the last PRODUCT_SPEC.md change.
  PRODUCT_SPEC.md last changed in commit cefd11d58fa2f082384999a2b38515036d6df347; newest docs/prover/ commit is b4e14255370af9c55f88c0e1bb6c2f86ab0e8a8f.
```

Two commits in this range change `PRODUCT_SPEC.md`: 1d10642 adds Requirement 304, the public edition,
and cefd11d adds Requirement 305, the push review. One commit in this range adds a prover record,
b4e1425, and it is older than both. So the two new requirements this day's work rests on went through
no prover pass.

The same failure appears in the suite as
`tests/test_guardrails.py::TestGateA_ProverRecord::test_real_repo_passes`.

Consequence. `guardrails/pre-push` runs this as gate a and sets `fail=1`, so the push is refused
before gate ac is reached. Beyond the mechanics: the requirement that says a push carries an
adversarial review shipped without the review pass this project runs on a spec change.

Commit c3c9899 landed a prover record for the spec change while this review ran. Gate a still reds,
now on its other arm:

```
FAIL (prover record): the newest committed prover record predates the last ARCHITECTURE.md change.
  ARCHITECTURE.md last changed in commit 50fffff687f1927beed68538b1e9cb53ca8152db; newest docs/prover/ commit is c3c9899387e493f8c942daff9daf2a61b7217ae5.
```

Commit 50fffff changed two pointers in `ARCHITECTURE.md` after that record. So the gate is red again for the same reason in a new place. Any further edit to either document
reds it again.

Fix. Land the prover record last, after the final edit to the spec and the design map.

### 2. An empty committed record satisfies the new gate

`guardrails/check-push-review.sh` lines 141 and 164, both reading `body="$(cat "$rec")"`.

Arm A proves the path is tracked, through `git ls-files` at line 108. Arms C, D and E then read the
file from the working tree. So the committed bytes and the read bytes can differ.

Reproduced. A scratch repository. A zero-byte record is committed, which is exempt from review since
it touches only the review directory. The content is then written on disk and left uncommitted:

```
in git: 0 bytes; on disk: 118 bytes
OK (push review): docs/push-review/2026-08-05-x.md covers the pushed range a01fdfd..3fa0ed9
GATE EXIT=0
```

Consequence. The push ships an empty record. `docs/push-review/README.md` names "the record is
committed, rather than a scratch file in the working tree" as one of six things the gate holds. It
holds none of it. `TEST_MATRIX.md` line 650 claims "never a scratch record in the working tree
counting" and line 651 claims "never an empty file satisfying the gate". Both are false.

`tests/test_push_review.py` line 173, `test_untracked_record_does_not_count`, tests a path that is
untracked as a whole. The committed-empty case slips between its arms.

Fix. Read each record through `git show HEAD:<path>` rather than from disk.

### 3. The public edition ships a copy that the same day's repair never reached

`editions/product-prover/SKILL.md`, whole file. Compare `skills/product-prover/SKILL.md`.

Commit b4e1425 created `editions/product-prover/`. Commit 17434b7, later the same day, added eleven
missing inputs to `skills/product-prover/SKILL.md`. Its own message says each of the eleven named a
step a reader could not perform. The edition never received them.

Three of the eleven, counted across both copies:

| addition | `skills/product-prover/SKILL.md` | `editions/product-prover/` |
|---|---|---|
| the definition of a surface registry | 1 | 0 |
| the reading-load reading of the cognitive-load lens | 2 | 0 |
| the definition of a station | 1 | 0 |

Consequence. `.github/workflows/gates.yml` runs the `sync-mirrors` job after the gates pass on a push
to `main`. That job runs `scripts/sync-mirrors.sh`, which copies `editions/product-prover/` over the
public repository with `rsync --delete`. So this push is what publishes the lagging copy. The reader
it reaches is the one holding no other file, which is the reader the eleven repairs were for.

Nothing in the tree would notice. `tests/test_mirror_editions.py` line 36 states that its cases run in
a scratch pack. So the real tree's contents never decide the answer. No other test or gate names the
editions directory.

`guardrails/check-skill-loadability.sh` line 13 reads `$SKILLS_DIR/*/SKILL.md` alone. So the edition's
frontmatter, its name-to-folder agreement, its version and its scoping section go unchecked. The
mirror is published as a skill a stranger installs on its own. `publish_source_for` in
`scripts/sync-mirrors.sh` lines 78 to 92 accepts a `SKILL.md` of zero bytes.

Fix. Carry 17434b7's eleven additions into the edition. Then point the loadability gate at the
editions directory, and add a check that ties the edition's rule set to the skill's.

### 4. An open blocking finding passes the gate two ways

`guardrails/check-push-review.sh` line 194. Compare `PRODUCT_SPEC.md` R305.9 and `TEST_MATRIX.md`
line 651, which claims "never a blocking finding leaving the machine unexplained".

The line reads the block under `Blocking:` with an awk program that stops at the first blank line.
The arm below it looks for `closed:` or `stands:` as a bare substring anywhere in each item.

Reproduced, first way. A record whose `Blocking:` line carries one closed item, a blank line, then two
items with no marker:

```
Blocking: - first item — closed: fixed

- second item: the product corrupts data on every save
- third item: no marker at all
```

Exit 0. The two unexplained items are never read.

Reproduced, second way:

```
Blocking: - the data-loss bug is NOT closed: I ran out of time and am pushing anyway
```

Exit 0. The word "closed" appears, so the item counts as closed.

Consequence. A record that lists its blocking findings across paragraphs has every item after the
first paragraph waved through. A sentence that says a finding stands open reads as closed.

Fix. Read to the end of the list rather than to the first blank line. Anchor the marker at the start
of the item's text, after the list marker.

### 5. The review directory is a hole in the gate that guards it

`guardrails/check-push-review.sh` lines 82 to 95. Compare `PRODUCT_SPEC.md` R305.8, second bullet.

The requirement exempts "a commit carrying the record alone". The script exempts every commit whose
files all sit under `docs/push-review/`, whatever those files are.

Reproduced. A scratch repository, one commit adding `docs/push-review/lib/deploy.sh` and
`docs/push-review/notes.md`, with no record anywhere:

```
OK (push review): every commit in origin/main..HEAD carries the review record alone, so the
  range holds no change of its own to review.
exit=0
```

Consequence. Any file, including runnable code, ships past this gate by sitting in the one directory
the gate governs. The message printed says a record was carried, and the commit carried none.

Fix. Exempt a commit only where each of its files is a record file. A record file is a markdown file
directly under the review directory, named with a leading date.

### 6. The tests added today hold script text rather than behaviour

Four test files were added. Most of their claims are assertions that certain strings appear in a
script or a document.

`tests/test_push_review.py` lines 271 to 274:

```python
assert "check-push-review.sh" in prepush
assert "-- gate ac:" in prepush
```

Change `guardrails/pre-push` line 244 to `"$GUARDRAILS/check-push-review.sh" || true` and the gate
runs with its red discarded. The file reports 17 passed.

`tests/test_mirror_editions.py` lines 103 to 144 assert on the source of `scripts/sync-mirrors.sh`. No
test runs the copy step. Add one line after the asserted `rsync` line:
`cp "$skill_path/SKILL.md" "$mirror_dir/SKILL.md"`. That restores the exact regression this change was
written to fix. The file reports 10 passed. The same assertions red on a reformat that changes no
behaviour.

`tests/test_skill_count_agrees.py` line 75 compiles `_COUNT_PHRASE` around the literal word "working".
A sentence that states the count without that word is invisible to the guard. Add "live-spec is a pack
of nine skills." to `OVERVIEW.md` and the file stays at 9 passed. That is the defect class the file's
own docstring says it exists for.

Line 158 counts the entries under the heading and never compares their names to disk. Replace
`- **publish**` with a skill that exists nowhere and the count still agrees.

`tests/test_text_audit_fixtures.py` line 166 anchors the wrong-command fixture on a usage string that
lives inside `scripts/build-index.py`'s docstring. Teaching the builder to accept a positional output
file, leaving the docstring alone, makes the fixture's failing command succeed while every test stays
green.

Consequence. Each of these guards its subject against a rename and against little else. Four broken
trees report green. The gate disarmed. The mirror publishing the internal copy. A page stating a wrong
count. A fixture teaching a working command.

Fix. Run the thing. For the wiring test, run `guardrails/pre-push` against a planted red and assert the
chain fails. For the mirror tests, run the copy step against a scratch source and read the result. For
the count guard, match a number beside the word for skills. For the fixture, run the taught command
and assert it fails.

## Non-blocking findings

### 7. The new gate reviews one commit on a first push, and can review none

`guardrails/check-push-review.sh` lines 62 to 63. The base ladder's third rung is `HEAD~1`.

Reproduced. A repository with five commits and no `origin/main`, about to push to a fresh remote. The
record is committed last and covers the fifth commit alone. Since the record's commit touches only the
review directory, the reviewed set comes out empty:

```
OK (push review): every commit in HEAD~1..HEAD carries the review record alone, so the
  range holds no change of its own to review.
exit=0
```

Six commits go to the remote and the gate reviewed none of them. Without the record commit the same
run reviews exactly one commit of five.

`PRODUCT_SPEC.md` R305.2 says the delta is every commit between the remote's head and the local head.
R305.3's third rung says the previous commit. The two disagree when no remote head exists, and the
script follows the weaker one. This is the path a project adopting the pack takes on its first push.

In CI the same shape appears when `github.event.before` carries the all-zero identifier, on the first
push of a branch. The ladder then falls to `origin/main`, which after checkout equals the head, so the
range is empty and the gate returns exit 0.

Fix. Where no remote head resolves, read the range as every commit in the branch.

### 8. Today's rewrite broke a pin, and a commit message says the pins all resolve

`ARCHITECTURE.md` line 583 pins `skills/design-reviewer/SKILL.md:1` with the label "frontmatter + when
it fires". Commit 258d544 rewrote that skill and moved "When it fires" from the opening lines to line
87. The label's words no longer appear near the pinned line.

`bash guardrails/check-pin-drift.sh` reports four drifting pins at the current head and returns exit 0,
since the gate runs without `--strict`. Two of the four predate this range. The design-reviewer one is new: the copy
at `origin/main` carried both "When" and "fires" in its opening lines.

Commit 6167a6e's subject reads "The design map comes under its own cap, and its pins all resolve". The
pins do not all resolve at the head of this range. Commit 50fffff repaired two other pointers and left
this one standing.

Fix. Repoint the pin to line 87, or relabel it.

### 9. The shape the record's own guide documents is refused by the gate

`docs/push-review/README.md` line 45. Compare `guardrails/check-push-review.sh` lines 173 to 186.

The guide says `Blocking:` "reads `none`, or lists one item per blocking finding". Written that way,
with `Blocking:` on its own line and the items below it, the gate refuses the record:

```
FAIL (push review): docs/push-review/2026-08-05-x.md carries `Blocking:` with no value (SPEC INV-304).
  Fix: fill the record's fields — the shape is in docs/push-review/README.md.
```

Consequence. A reviewer following the guide is refused, and the message sends them back to the guide
they followed. The same trap sits on every field. This record carries its first blocking item on the
`Blocking:` line to work around it.

Fix. Accept a field whose value continues on the following lines, or state the one-line rule in the
guide and in the failure message.

### 10. The installer still seeds a configuration that switches a check off

`scaffold/guardrails.config.example.json` seeds `"waivers": {"completeness": "no rendered artifact yet
— declared 2026-07-10, owner <maintainer>"}`.

Run in a fresh project cloned from this branch:

```
--- check_completeness ---
WAIVED (completeness): no rendered artifact yet — declared 2026-07-10, owner <maintainer>
exit=0
```

Commit e43e814's message names this among four defects that "would have stopped a stranger cold". That
commit changed `MIGRATION.md`, `OVERVIEW.md` and `README.md` alone. The repair is a sentence at
`README.md` line 33 asking the reader to empty the waivers block.

The state improves on `origin/main`, which carried no such sentence. A reader who skips the sentence
installs a gate with one of its four checks off, and that check prints a green line.

Fix. Ship the example configuration with an empty waivers block, and move the example waiver into the
scaffold guide as an illustration.

### 11. A refused edition leaves a cloned repository behind

`scripts/sync-mirrors.sh`. The loop arms `trap 'rm -rf "$work_dir"' EXIT` after cloning a mirror. The
refusal path for a half-made edition runs `continue` at line 412, past the clone and before the
`trap - EXIT` at the loop's end. The next iteration re-arms the trap on a new directory.

Consequence. Each refused edition leaves one full clone in the temporary directory. The published
repositories are unaffected.

Fix. Remove the directory and clear the trap before the `continue`.

### 12. The mirror's own language scan reads one file

`scripts/sync-mirrors.sh` calls `check_mirror_language` on `README.md` alone. Everything else the
edition publishes rests on the repository gate, `scripts/check-shipped-language.py`, whose file set
comes from `git ls-files`.

Consequence. An untracked file inside `editions/<skill>/` is copied to the public repository and read
by no scan. The editions directory holds no untracked file today.

A neighbouring gap: the loop iterates `"$SKILLS_DIR"/*/`, so an edition is reached only through its
skill folder. Removing or renaming `skills/<name>/` leaves `editions/<name>/` unreachable and the
public repository frozen at its last state, with no line printed.

Fix. Scan every file the copy step is about to publish, and walk the union of the two directories.

### 13. The suite reads state outside the repository, so a neighbouring run reds it

The suite was run twice. The first run reported 2 failed, 2359 passed and 1 error. The second, with a
temporary directory of its own, reported 3 failed and 2358 passed. The two runs disagree on which
tests failed, and only one failure is common to both.

First run, dropped on the second: `tests/test_convergence_locks.py::test_live_spec_sits_at_the_clean_floor`
and a teardown error reading "the suite leaked temp artifacts (SPEC INV-100):
['livespec-test-suite-log.RuPXV0']". Both pass alone on this tree. Two other pytest runs were active
in copies of the repository, and the fixture at `tests/conftest.py` line 129 lists the shared system
temporary directory.

Second run, new: `tests/test_worker_restore.py::TestTheGateIsArmedWhereItSaysItIs::test_the_gate_runs_against_this_machines_own_transcripts`.
It reads the machine's agent transcripts from the last 24 hours and reds on a run that discarded
uncommitted work. The run it names is a worker of this review session, stamped 2026-08-05T09:44:33Z.
The command was `git checkout -q -- .` inside a scratch repository. This red comes from the review
itself.

Common to both runs, and the only failure the change under review causes:
`tests/test_guardrails.py::TestGateA_ProverRecord::test_real_repo_passes`, which is finding 1.
`TestGateB_Tests::test_real_content_passes` fails in the second run because it runs the suite again
inside itself and inherits the same reds.

Consequence. Gate b is red at push time, and it will stay red for 24 hours on the transcript arm
regardless of what the change does. A concurrent run in another copy of the repository also reds it.
Neither of those two reds belongs to the change under review.

Fix. Scope the leak fixture to a directory the run owns. Scope the transcript arm to runs whose
recorded working directory is the repository being pushed.

### 14. A gate reports an old record as fresh

`guardrails/check-skill-review.sh` picks the matched record by name and measures freshness on the
review directory's newest commit. Seven skills were rewritten today and each has a record dated today,
yet the gate reports July records as the fresh ones:

```
OK (skill review): skill 'spec-author' carries a fresh review record (docs/skill-review/2026-07-18-spec-author-product-prover.md).
```

Consequence. A skill rewritten today passes on a July record, so long as some other file in the
directory was committed today. The gate sits outside this range. Gate ac's arm C avoids the same shape
by requiring the matched record to name every commit.

### 15. The reporting skill still carries the word its commit says it dropped

`skills/communicator/SKILL.md` lines 77 and 78. Commit a97f95b's subject reads "The reporting skill
drops a coined word its own check bans". The word is the one
`scripts/preshow-register-lint.py` bans under the pattern named `en-pipeline-station`, which matches
the word for a pipeline step written as a railway stop.

Rule 9 lost it. Rule 13 still carries it, split by a line wrap:

```
    and the delivery report the human is never left reading silence: when a beat lands — a pipeline
    station passed, a load-bearing find, a change of direction — say it as it happens, one or two plain
```

The linter reads line by line, so the pattern never matches:

```
OK (preshow-register): no coined metaphor, calque, or transliterated pack term found.
lint exit=0
```

Consequence. A reader meets the coinage on the page. The check reports the file clean. Every check of
this shape has the same blind spot: a banned phrase survives by sitting across a line break.

Fix. Remove the phrase from rule 13. Then read the linter against joined paragraphs rather than lines.

### 16. A fallback table became a duty on every pass

`skills/product-prover/SKILL.md` line 908. Compare `PRODUCT_SPEC.md` line 1627, criterion R67.2.

The criterion states the surface-by-sweep table as "the replacement for the coverage tables on a kind
where those go not-applicable".

The copy at `origin/main` read: "Render the surface × sweep verdict table instead."

The new line reads: "Every FULL pass renders the surface × sweep verdict table, whatever the three
tables above did."

Consequence. A replacement became a universal duty. Every full review on an ordinary product now owes
a fourth table beside three that already cover it. The skill and the spec state different rules.

Fix. Restore the fallback wording, or change R67.2 in the same commit.

### 17. Two hard rules in the review skill gained exceptions no spec states

`skills/product-prover/SKILL.md` lines 387 and 440. Neither phrase appears in the copy at
`origin/main`.

Line 387, on the restructure-and-migration merge gate: "The gate then stands down by name, and the
pass reads the document as it stands."

The stand-down applies to a document handed over on its own. `PRODUCT_SPEC.md`'s INV-114 states no such
exemption. A rewrite delivered as a file now skips token identity, the punctuation check and the
two-sided pass.

Line 440, on the architecture lens: "Where none can be produced, record the ownership check as not
runnable with that reason, and run the remaining six."

The sentence above it says the paired spec "must be in view, because ownership is checkable only
against the fact list it owns". The lens now passes six of seven on the one case the sentence existed
to block.

Consequence. Both were introduced by 17434b7, whose subject reads "Every step the review skill names
can now be performed". Making a step performable by permitting its omission is a different change.

Fix. Take both exceptions to the spec first, or drop them.

### 18. The pipeline skill points at the wrong section of the reporting skill

`skills/build-pipeline/SKILL.md` line 205 names "communicator rule 6, the removal-accounting step of
that skill's writing-register checklist".

In `skills/communicator/SKILL.md` the writing register is a section beginning at line 420. The
pre-report walk is a separate section beginning at line 440, and the numbered steps live there.

Consequence. A reader following the pointer opens the register section and finds no numbered step 6.
The pointer was introduced by a229b0d, whose subject reads "The pipeline skill names every template,
command and code it uses".

Fix. Name the pre-report walk.

### 19. The pipeline skill's list of skill-invoking steps omits one

`skills/build-pipeline/SKILL.md` line 82. The copy at `origin/main` read "One pipeline, each step has
a tool."

The new line reads "One pipeline, and steps 1, 2, 5, and 6 each invoke a named skill."

The order stated on the same line runs: spec, prove, architecture, prove architecture, matrix, test,
code, verify, commit and show. Step 4 is "prove architecture", and the step's own text at line 344
reads "Prove the architecture — invoke `product-prover` with the architecture lens". Step 4 is missing
from the list.

Consequence. A reader who takes the list as the set of skill-invoking steps drops the architecture
prove pass. An open statement became a closed list that is wrong.

Fix. Add step 4, or restore the open wording.

### 20. The front page states a line count the tree contradicts

`README.md` line 68 and line 70. Neither exists on `origin/main`, so both ship with this push.

Line 68 heads a section "Nearly five thousand lines of rules". Line 70 reads "they and the skills
carrying them run to about 4,800 lines under `skills/`".

Measured:

```
cat skills/*/SKILL.md | wc -l                       5178
find skills -name '*.md' -exec cat {} + | wc -l     7121
```

Consequence. The narrowest reading of the sentence overshoots by 378 lines. The reading the sentence
actually states, everything under `skills/`, overshoots by 2,321. The heading says "nearly five
thousand" for a number above five thousand. This is the front page, and the number is the section's
whole point.

Fix. State the measured number and say which files it counts.

### 21. Gate aa refuses this tree

```
FAIL (doc-findings-bound): inbox/2026-08-05-from-tlvphotos-rotation-gate-reads-only-numbered-rows.md
is live and carries no entry in the record. Measure it into the record before it ships:
python3 scripts/rule-census.py --json guardrails/rule-census.json
```

The file is untracked and belongs to no commit in this range. The gate reads live documents from disk,
so it reds at push time regardless.

Consequence. `guardrails/pre-push` sets `fail=1` at gate aa. The push is refused for a reason the
change under review did not create.

Fix. Run the command the gate prints, then commit the record it writes.

## What was checked and held clean

- The push range. `git rev-list --count origin/main..main` returns 19. The brief said 20.
- An evil merge. A merge commit that resolves a conflict with new content is named by
  `git show --name-only`, so the gate demands it in the record. A clean merge is invisible to that
  command and carries no content of its own.
- Freshness. Committing the record and then committing more work reds the gate, as intended.
- A record covering another range. The gate names each missing commit.
- A staged record that is never committed. The gate reds on it.
- The gate's wiring as data. `guardrails/gate-red-proofs.json` carries gate ac's red proof, and that
  proof is a real behavioural test. `check-every-gate-can-fail.py` and `check-ci-mirror.sh` pass.
- The publish selection. `--print-publish-source product-prover` prints the edition directory, and the
  flag reaches no repository.
- The edition's self-containment as written. Every file path its `SKILL.md` and `README.md` name
  resolves inside the edition, apart from `docs/review/YYYY-MM-DD.md`, which the reader creates.
- The edition's structure against the skill's. The section list matches. Phase 3e's detail sits in
  `reference/stress-lenses.md`, which the edition carries, so the shorter page loses nothing there.
- Every link in `README.md`. All 31 relative links resolve.
- The install path. `bash adopt/install-scaffold.sh` runs to exit 0 in a fresh project and seeds the
  configuration. The four vendored checks then run and name their own dead paths.
- `guardrails/local-overrides.json` and `guardrails/check-config-health.sh` sit outside this range. The
  declared-difference mechanism is already on `origin/main`, and no machine reads its `review_by` date.
- The shipped-language gate reaches the editions directory, and the census measures its five files.
- The four new test files run to 45 passed with no skips.
- The scaffold checks for requirement shape and vocabulary refuse an empty input set by name and report
  their own reach.

## What could not be checked

- The mirror sync end to end. `scripts/sync-mirrors.sh` needs GitHub credentials and writes public
  repositories, so only its publish-selection flag was exercised. Finding 3 rests on reading the
  workflow and the script.
- Whether every rule kept its meaning through the day's rewrites. Seven skills, four documents and five
  templates were rewritten, some by workers running at the same time. A sentence-level comparison of
  old against new across all of them is beyond one pass. This record covers the rewrites through their
  cross-references, their stated counts and the pins. A second reader returned late in this review with
  findings 15 to 20, each re-verified here against the files. Its own report names about twenty
  further findings it took from sub-readers and did not verify itself. Those stay unread here. The
  clause-by-clause reading of the whole set is owed before the next push that touches those files.
- The counts in the commit subjects for the rulebook, 226 down to 92, and for the consistency skill, 72
  down to zero. The census in `guardrails/rule-census.json` stands modified and uncommitted, so a
  reading against the committed record measures a different tree.

## Repaired findings

Four adversarial reviewers read the 35 commits from 50fffff to 44778ea this afternoon and evening.
Each finding below is already closed, by the commit named beside it.

### 22. The morning harvest deleted four tracked messages with no archive copy

Commit 1167ae9, "Five inbox messages become nine queue rows and one row grows", deleted four inbox
files. They were `inbox/2026-07-30-authoring-coverage-findings.md`,
`inbox/2026-07-30-communicator-source-findings.md`, `inbox/2026-07-30-context-audit-from-fable.md`,
and `inbox/2026-07-30-live-spec-base-leftovers.md`. It removed 579 lines and placed no copy in
`attic/`. `ROADMAP.md` rows 537, 538, 539 and 540 went on citing those four paths after the files
were gone.

REPAIRED by ad31edb, "The harvested messages rest in the attic and their rows cite them there". The
four messages now sit under `attic/`. Each has its own manifest line in `attic/MANIFEST.md`, reading
"a harvested inbox message whose rows cite its items". Rows 537 through 540 are repointed at the
attic copies.

### 23. The design map carried 29 stale pointers under a green pointer check

`guardrails/check-pin-drift.sh` accepts a pin when any label word of four or more letters sits within
a 51-line window of the pinned line. So a pin pointing 70 lines from its sentence still reads clean.
The prover pass recorded in `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` found 29
stale pins across three skill files under that gate. One pin labelled rule 20 landed on the opening
line of rule 19.

REPAIRED by 85b8265, "The design map points at the lines its labels name again". It re-points 31 pins
across `ARCHITECTURE.md`, a wider set than the 29 the pass first counted. The pin block also carries
the `templates/TEST_MATRIX.template.md` pin, and one more inside `skills/build-pipeline/SKILL.md`
that the pass's own summary undercounted. A second reader,
`docs/prover/2026-08-05-pin-repoint-check.md`, checked all 31 changed pins and 11 further
spot-checked pins independently. Every one holds. The gate's weak reach, the 51-line window itself,
is not fixed here; it stands as queue row 541.

### 24. The restore gate placed a command by session directory, with no model of `cd`

`guardrails/check-worker-restore.py` reads a shell command string for a forbidden `git` invocation.
Until today it placed every finding at the session's recorded working directory, never at the
directory a `cd` inside the command actually moved to. A scratch-fixture command run inside a
throwaway directory misreported as a wipe of the live tree.

REPAIRED first by 50537d6, "The restore gate places a command in the directory it really ran in". It
tracks `cd`, a plain literal variable assignment, and `git -C <path>` as the command string is read
left to right. It reds only a forbidden command that lands in a directory whose enclosing git
repository still exists on disk.

That model still had three holes. Each was caught by an adversarial review of the push and closed the
same day by 2ea1cc4, "The restore gate reads a failed cd, a quoted script and a wrapper prefix the
way a shell does":

- A failed `cd` joined by `;` or `||` let a real wipe pass. `cd /nonexistent ; git checkout -- .` ran
  `git checkout` in the record's own directory. The gate filed it under the nonexistent path and
  never checked there. The gate now reads the separator: after `&&` the next command is placed at the
  `cd` target, since a failed `cd` would have stopped it. After `;` or `||` it is placed at the
  pre-`cd` directory instead, the conservative reading, unless the script carries `set -e`.
- A quoted script literal or a heredoc body read as executed commands. `python3 -c "…git checkout --
  .…"` was cut at the newlines inside the quoted string, and each line of the quoted script was read
  as its own command. Heredoc bodies are now dropped before the line is cut into segments, and the
  cutting itself steps over quoted spans.
- A wrapper prefix — `command`, `sudo`, `env` — escaped the matcher, since the gate looked for a
  segment whose first word was literally `git`. Each wrapper is now stripped before the check runs.

89 tests pass on `tests/test_worker_restore.py` after both commits. The whole-history finding count
recorded in `docs/language-defects.md` fell from 73 to 69 across the day. Four of those five were the
gate's own false positive on a reviewer's scratch-fixture probe, since verified and cleared, not a
change to the audited text.

### 25. The deliberate-string marker cleared a URL fragment or a doubled path separator

`scripts/check-shipped-language.py`'s `USER_REGION_MARK` pattern matched `user-language` after any of
its four comment openers (`#`, `<!--`, `/*`, `//`) anywhere in a line. That included inside a URL
(`https://user-language...`) or a doubled path separator (`docs//user-language.md`). Neither is a
real comment opener, so a line carrying either cleared the check on a string it should have caught.

REPAIRED by 2a8368a, "Anchor the user-language marker to a real comment opener, not a URL or path
substring". The pattern now requires its opener to sit at the start of a line, or after a whitespace
character. An opener embedded inside a URL or a path can no longer masquerade as a comment. Four
tests were added to `tests/test_guardrails.py`, covering the URL case, the doubled-separator case,
and the two real-comment cases that must keep passing.

### 26. The wording check joined a phrase across a paragraph break

An earlier fix in this same range, 83ebd2d, taught `scripts/preshow-register-lint.py` to flatten
whitespace runs to a single space, so a banned phrase split across a line wrap would still be caught.
That flattening was too wide. It also joined two words from two different paragraphs that happened to
sit next to each other across a blank line. "It drives the pipeline" followed by a new paragraph
opening "station crews then arrive" reported as the banned coinage, though the two halves share no
sentence.

REPAIRED by 467d667, "The wording check no longer joins a phrase split across a paragraph break". A
whitespace run holding two or more newlines, a blank line, now collapses to a paragraph mark no
pattern can cross. A single-newline soft wrap still collapses to a space and still joins. A test
carrying a stray `self=None` parameter, left over from an earlier draft of the file, was also fixed.
Two tests were added: one proving the paragraph-boundary case reports nothing, one proving the
soft-wrap case still reports.

### 27. The public edition lagged its skill, and every refusal printed the same reason

Commit b4e1425 created `editions/product-prover/` from the skill as it stood that morning. Commit
17434b7, later the same day, added eleven missing inputs to `skills/product-prover/SKILL.md`. The
edition never received them. `scripts/sync-mirrors.sh` would have published the stale copy on the
next push, silently: the sync's `edition_is_current` check stood aside on an edition with no commit
of its own, instead of refusing it. Every refusal it did print, whatever the real reason, read as
"holds no SKILL.md".

REPAIRED by 3f33ac5, "The public edition catches up with its skill, and every refusal names its own
case". `editions/product-prover/SKILL.md` now carries the eleven additions. Its
`reference/stress-lenses.md` and `PROVENANCE.md` are brought current with it. An edition with no
commit of its own now reads as older than any committed skill, and is refused rather than waved
through. Each refusal, whether no `SKILL.md` or a stale edition, prints its own reason and its own
remedy, read from one place rather than hardcoded three times over. Five tests were added to
`tests/test_mirror_editions.py`.

### 28. The audit skill claimed both readers agreed on all eight repaired passages

`skills/text-audit/SKILL.md` and `docs/language-defects.md` described the day's eight repaired
passages as ones "both readers stopped on and marked blocking". The two reading records,
`docs/language-reads/`'s rounds 30 and 31, agree on five of the eight. The other three were flagged
blocking by reading 31 alone. The skill also dropped its referral to the spec-critique pass
(product-prover), misdescribed `docs/language-defects.md` as the narrower "places only one reader
found", and stated a cost multiplier of 1.56 times as many stops, computed from a per-document
figure the neighbouring sentence itself discounts as unmeasured.

REPAIRED by 887ff4e, "The four defects the push review confirmed close, and the reading split is
stated as the records hold it". `docs/language-defects.md` now states the true split: five passages
both readings blocked, three that reading 31 alone blocked. One of the five also closes a stop
reading 30 alone marked blocking, since both sat in one paragraph. The skill now calls
`docs/language-defects.md` "the record of why each language rule says what it says", and restores
the product-prover referral for "an argument with a spec's claims". The multiplier is re-stated as
roughly 1.43 times as many stops, against the 227-stop baseline the sentence beside it actually
supports.

### 29. The status file miscounted its own rows, landings, and measured files

`NEXT_STEPS.md`'s live-state block claimed "today's landings, all after 13:12", but later landings
belonged to a different session than the one narrating. It claimed rows 532 to 541, but row 541 had
not yet been added when the earlier text was written, and row 542 had since landed. It claimed the
reading queue dropped 25 files, leaving 103 measured, where the true figures were 29 dropped and 98
remaining.

REPAIRED by 29ebe2e, "The status block's counts match the records they cite". The block now
distinguishes this session's landings from the morning process's own, states rows 532 to 542, and
reads 29 entries left the census with 98 files remaining measured.

### 30. The census directory exclusion matched by string prefix, not a path boundary

`scripts/rule-census.py`'s `SKIP_DIRS` check used `str.startswith()` against each excluded directory
name. A sibling directory whose name merely extended a skipped one — `templates-old` beside the
skipped `templates` — would drop from the count silently, unmeasured and unreported.

REPAIRED by 8054fc3, "The census skips a directory only at a path boundary". Each skip name now
carries a trailing path separator before the prefix check runs. Only a real subdirectory of a
skipped path is excluded, never a same-named neighbour.

### 31. A rename reached the skill body and stopped short of its glossary, examples, and tests

Commit 83ebd2d renamed "station" to "step" in `skills/communicator/SKILL.md` rule 13, to drop a
coined word the register lint bans. The old word survived in the skill's own glossary and worked
example, in rule 14's pointer, and in the live-status line. It also survived in `TEST_MATRIX.md` rows
M-112, M-124, M-127, M-133 and M-178, and in the docstrings of `tests/test_traceability.py` and
`tests/test_chat_law_hook.py`.

REPAIRED across three commits. da6da0f, "The renamed word reaches its glossary, examples, matrix row
and test", swept `references/words.md`, `references/field-examples.md`, the rule 14 pointer, the
live-status line, `TEST_MATRIX.md` row M-112, and `tests/test_report_format.py`. 9c2cc87, "The last
three sentences carrying the old word take the new one, tests re-pinned", caught three sentences the
first sweep's own record had left outside its write-set, and re-pinned `tests/test_traceability.py`
against them. 7e39f75, "The renamed word reaches the matrix rows and docstrings the sweep missed",
closed the remaining `TEST_MATRIX.md` rows (M-124, M-127, M-133, M-178) and the two test docstrings.

## Standing findings

Open items, each with its owner.

- Many specifics from the four July inbox messages (finding 22, now attic-restored) reached no queue
  row. They live only outside this repository, so no gate reaches them. Rows 537 to 540 carry the
  batches. Each one opens with a freshness re-check before acting, since some of what it describes
  may already be resolved by the day's own rewrites.
- The restore gate (finding 24) covers a spawned worker's transcript alone. A main-thread command
  that discards the tree escapes it. No row yet owns this gap.
- Two committed check records carry small self-miscounts, kept as history rather than corrected in
  place. ROADMAP row 541 names 29 stale pins, where the pass that repointed them acted on 31.
  `docs/prover/2026-08-05-pin-repoint-check.md`'s per-file split sums to 30, against its own stated
  31. Neither error changes a verdict; the proof tables in each document carry the true count.

## Dissent

For the person who decides. The census (finding 30's file, `scripts/rule-census.py`) leaves 12
template files and 13 test fixtures unmeasured, on the ground that nobody reads them here. A reviewer
contests this: the project's own README instructs a new project to start from `templates/`, so a
reader does exist, and an unmeasured template can drift unnoticed. The cut stands on the queue's
written decision. It is recorded here for the person's eye, not resolved by this record.

## Process incident

A worker ran `git stash` against this shared tree while extending a different document. It swept
three sibling files outside its own write-set. It restored its own files by re-applying its edits.
The three sibling files were verified intact afterward. The swept bytes remain in `stash@{0}`,
untouched, so nothing already committed or already re-applied is at risk. No work was lost.

The gate that reads worker transcripts for a tree-discarding command never fired on this incident. It
covers a spawned worker's own transcript, not a command run by the session that spawned it. That gap
is the same one named as a standing finding above. The journal entry for this incident is
`JOURNAL.md`'s afternoon review section, landed in commit 12acab2, "The journal keeps the afternoon's
review and the stash incident".
