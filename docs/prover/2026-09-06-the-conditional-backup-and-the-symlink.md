# Prover record — 2026-09-06 the installer's conditional backup, and the link the byte test cannot see

PUSH-REVIEW

Prover skill version: product-prover (installed under `skills/product-prover/`), read beside
`skills/product-prover-pack/SKILL.md` (pack bindings). This pass was run from a seat that authored
none of the work below, briefed to find reasons to refuse it.

Range: 5928738a..43038fb0
- 5928738 The review record names its landing commit — the base this range is measured from
- 86e9cb5 The installer backs up an installed skill only where its bytes are not in git
- c51a279 The Cyrillic quote behind the backup rule moves to JOURNAL.md
- \<pending\> the uncommitted change under review — this record, the symlink exemption in
  `install.sh`, and the red-first test that holds it

The head sha is written `\<pending\>` on purpose: the commit that lands this record does not exist
while the record is being written, and it is the coordinator that fills the real hash in at commit
time. The gate reads the record for every reviewed commit's short sha, so that substitution has to
happen before the push, not after it.

Files read: `install.sh` (whole — 58 lines as this range left it, 60 after this pass's fix; not the
changed hunk alone, since the question asked was what the skipped backup could cost a later step),
`scripts/sync-skills.sh` (whole — the sibling
copier carrying the same byte-identity compare), `scripts/install-external-skills.sh` (the fence the
loop's `.git` arm defers to), `JOURNAL.md` (the entry this range adds, line 3803),
`tests/test_setup_entry.py` (case E whole, and the file's imports),
`tests/test_skill_count_agrees.py` (the `.git`-spelling note at lines 82–86 and 214),
`guardrails/check-shipped-language.sh` and `scripts/check-shipped-language.py` (the exclude list at
line 134 and the fix text at 288), `guardrails/check-prover-record.sh` (whole),
`docs/prover/README.md`, `docs/prover/2026-09-06-kernel-breaker-and-the-abandoned-row.md`,
`docs/prover/2026-07-06-feature-fit-retro.md` (the line naming the backup home),
`guardrails.config.json`, `architecture/host-adoption.md` (the `install.sh:1` pin), and both commit
messages in the range.

Checks run: six measurements and seven pytest files, each with its result below.
- `diff -rq` exercised directly over every destination shape the loop can meet, in a scratch tree —
  identical directory: exit 0; directory holding a file the source dropped: exit 1; directory
  holding an extra dotfile: exit 1; plain file where a folder belongs: exit 2; dangling symlink:
  exit 2; **symlink whose target matches the source: exit 0**. The last one is the measurement F1
  rests on.
- The real `install.sh` run end to end against six planted destinations under a throwaway `HOME` —
  no dest, identical directory, drifted directory, plain file, symlink-to-matching-target, dangling
  symlink. Before the fix the symlink shape left the attic empty; after it, five of the six back up
  and only the identical directory skips, which is the one case the change set out to skip.
- `rm -rf` over a symlink to a populated directory — the link goes, the target stands. This is what
  bounds F1's severity: what the skip loses is the arrangement, not the content.
- `python3 scripts/check-shipped-language.py --root <scratch>` over a file carrying the exact comment
  line `86e9cb5` shipped — `install.sh:2 [cyrillic]`, one offence. So the gate really does reach that
  shape in a `.sh`, and `c51a279`'s move is a fix rather than a restatement.
- `bash guardrails/check-shipped-language.sh` on the tree — OK, no Cyrillic, owner-name or
  project-name offences in the shipped set.
- `bash guardrails/check-pin-drift.sh` — 193 pins clean. `install.sh` is pinned file-level
  (`architecture/host-adoption.md:20`, `install.sh:1`), so the two lines this pass adds move nothing.
- `python3 -m pytest -q tests/test_setup_entry.py tests/test_installed_copy_staleness_class.py
  tests/test_config_health.py tests/test_skill_count_agrees.py tests/test_scaffold_install.py
  tests/test_status_view_install.py` — 100 passed.
- `python3 -m pytest -q tests/test_guardrails.py` — 94 passed, 2 skipped, in 617s. Run separately,
  because that file exercises `guardrails/install.sh`, a different installer that happens to share
  the name, and because an earlier run of it erred and the cause had to be proved rather than called
  unrelated. The error was `tests/conftest.py:414`, the session-scoped `judged_tree_gains_no_commits`
  fixture, whose message named the culprit outright: `?? docs/prover/2026-09-06-the-conditional-backup-and-the-symlink.md`
  — this very record, created while that run was in flight. The fixture snapshots the judged tree's
  `git status` before and after the whole session and reds when it moves, so it was reporting the
  reviewer's own writing, not a script under test. Proved by re-running the same file with the tree
  held still: green, no error. Nothing in the range or in this pass's fix touches it.
- `bash guardrails/check-prover-record.sh` (no `--push`) — its non-range arms print OK.
- The full suite was NOT run here; it runs after this record lands.

Findings: one defect closed, one finding that stands, one observation about the range's shape, and
two recommendations that open no row. The two questions the delta most deserved both came back clean
and are worth saying: nothing in this tree consumes the backup home, and the skipped copy costs the
rest of the loop nothing.

**What the skipped backup cannot cost.** Read the whole loop rather than the hunk: after the
three-armed branch, the only remaining steps are `rm -rf "$dest"` and `cp -r "$skill_dir" "$dest"`,
and neither reads `$backup` or `$backup_home`. Nothing else in the loop, and nothing after it, opens
the attic. A repository-wide grep for `skills-attic` and `SKILLS_DEST-attic` finds exactly one
producer — `install.sh:33` — and no consumer at all: not in `tests/`, not in `scripts/`, not in
`guardrails/`, not in `.github/`. The only other mention in the tree is
`docs/prover/2026-07-06-feature-fit-retro.md:67`, which names the home as a taste choice and says
"any out-of-scan folder works". The repo's own `attic/` — the one `guardrails.config.json`,
`check-board.py` and `MIGRATION.md` are about — is a different thing entirely, the host's
append-only archive, and shares nothing with this path but the word. So removing the 480 backups
leaves no reader in the tree without its file.

F1 (defect, closed) — the byte-identity test is blind to the one destination whose loss the guard was
widened for the same day, and the test named for that shape does not reach it.

> "a backup that only covered a directory left a file or a dangling symlink deleted with no copy
> anywhere" — `install.sh`, the comment standing directly above the changed condition

That comment records a fix made earlier the same day: the guard moved from `[ -d "$dest" ]` to
`[ -e "$dest" ] || [ -L "$dest" ]` so that a file or a symlink at the destination is backed up before
`rm -rf` takes it. `86e9cb5` then `&&`s a byte comparison onto that guard. `diff -rq` follows a
symlink and reads the *target's* bytes, while the removal below takes the *link*. Measured: a symlink
pointing at content identical to the source returns exit 0, the branch skips, and the attic comes
back empty — one half of the shape the previous fix was made for is unbacked again. The existing test
is named
`test_a_file_or_symlink_at_the_destination_is_backed_up_before_it_is_removed` and its docstring names
"a symlink — the shape a person who symlinked one skill at the pack has", but it plants only a plain
file, which returns exit 2 and still backs up. So the property the test claims went false while the
test stayed green.

The justification the change rests on does not cover this case, which is what makes it a defect
rather than a taste call: the rule is that a copy is redundant because the bytes are already in git.
A link is in no repository. Its target matching the source proves nothing about what the removal
destroys, because what the removal destroys is the link. Severity is bounded — `rm -rf` over a
symlink spares the target, so the content survives and only the arrangement is lost, and nothing in
the pack creates such a link (`ln -s` appears nowhere in `scripts/`, `guardrails/`, `skills/`,
`adopt/` or `install.sh`), so reaching it takes a hand. That is why it is recorded as a defect and
not as a blocking finding.

Closed: the condition now reads
`[ -L "$dest" ] || { [ -e "$dest" ] && ! diff -rq "$skill_dir" "$dest" >/dev/null 2>&1; }` — a
symlink, live or dangling, short-circuits ahead of the comparison and is always backed up; a real
file or directory keeps the skip the change was made for. The `elif` narrows to `[ -e "$dest" ]`,
since no link can reach it. The line is shorter than the one it replaces. The message on the backup
arm was rewritten too: "installed copy differs from the source" is not true on the symlink path, and
it now says what it does rather than why. Red-proved by
`test_a_symlink_at_the_destination_is_backed_up_even_where_its_target_matches_the_source`
(`tests/test_setup_entry.py`), which failed with "the symlink at the destination was removed with no
backup: []" against the tree as handed over, and which holds all four halves of the property — a
backup exists, it is itself a link, it points where the original pointed, and the target was not
reached through.
`defect · narrowed-guard (safety)`

F2 (finding, stands) — the 436-of-480 figure cannot be verified from this tree, and the act it
justifies destroyed its own evidence.

> "436 of 480 were byte-identical to an object git already held, the rest were superseded drafts of
> the same day." — `JOURNAL.md`, the entry this range adds

`~/.claude/skills-attic` exists and is empty, so the 480 backups the count was taken over are gone
and no re-derivation is possible. The figure was checked against the only corroboration available:
`86e9cb5`'s commit message states the same three numbers — 436, 480, and 44 remaining — in the same
words, so the journal entry is accurate against what the range itself says happened, and this pass
found nothing that contradicts it. It cannot go further than that, and says so rather than implying a
check it did not run.

Two things follow that the entry does not say. By its own account 44 backups were *not* byte-identical
to a git object, and those 44 were deleted with the rest; the entry characterises them ("superseded
drafts of the same day") but no number backs the characterisation, and it can no longer be tested.
And the deletion is not part of this diff, so it is outside what a record on this push can close.

Why it stands: a journal entry is one person's dated record of an act they performed, and rewriting
someone's account of their own measurement is not a review's job — the honest act is to say the
figure rests on the author's word from here on, which is what this paragraph does. Nothing in the
tree read those files (see "What the skipped backup cannot cost" above), so nothing is broken by
their absence; what is unavailable is the proof, not a dependency. No row opened.
`finding · unverifiable-measurement (provenance)`

F3 (observation, no action) — the range reds a push gate at its midpoint, and is safe only because
nothing pushes mid-range. `86e9cb5` shipped `install.sh` line 32 carrying Cyrillic and the words
"his word", both of which `guardrails/check-shipped-language.sh` refuses in a shipped file. Proved
rather than assumed: the detector run over a scratch tree holding that exact line reports
`install.sh:2 [cyrillic]`, one offence. `c51a279` closes it, and the gate is green on the tree as it
now stands, so the push itself is clean. It is recorded because the fix's shape is exactly what the
gate's own fix text prescribes — "move the history (who/when/why) to JOURNAL.md" — and `JOURNAL.md`
is on the detector's exclude list at `scripts/check-shipped-language.py:134`, so the quote's new home
is the one the gate names rather than a place it happens not to look.
`observation · gate-red-in-range (process)`

R1 (recommendation, stands) — `scripts/sync-skills.sh:35` carries the same byte-identity compare
behind `[ -d "$DEST/$name" ]`, which is true for a symlink to a directory, and then `rm -rf`s the
link. F1's class lives there too. It is left alone deliberately: that script has never taken a backup
of anything, so this range narrowed nothing there, and giving it a backup home it never had is new
machinery, which this pack's own standing rule holds until an incident calls for one. Named here so
the class is on record rather than rediscovered.
`recommendation · later · same-class-elsewhere (safety)`

R2 (recommendation, stands) — a skill deleted from the repository is never visited at all. The loop
walks `"$SKILLS_SRC"/*/`, so an installed copy whose source is gone is never compared, never backed
up and never removed; it simply lives on. This is unchanged by the range and untouched by it, and the
whole-tree compare in the config-health arm is where an orphan would surface. Not a finding against
this delta. No row opened.
`recommendation · later · unvisited-orphan (completeness)`

Class lens: swept. F1's class is "a cheap identity test standing in for the thing actually at risk".
The delta holds one other predicate of that shape — the external-skill fence at `install.sh:20`,
`[ -e "$skill_dir/.git" ]` — and that one tests the right object: `-e` covers both the directory
spelling and the file spelling a worktree writes, which `tests/test_skill_count_agrees.py:214` holds
by name. The two remaining arms of the branch were read against every state the first can leave: the
`elif` can now be reached only by a real file or directory, since every `-L` is taken above it, and
the `else` only by a path where neither `-L` nor `-e` holds, which is the fresh install. All six
destination shapes were then run through the real installer rather than reasoned about, and each
lands where this record says. F2's class is "a record whose evidence the same act removed" — swept
across the range's other claims: `c51a279`'s claim is about the gate, and the gate was run; both
commit messages' claims about what the code now does were each proved by running the code.

No index rebuild was owed: nothing under `spec/`, `matrix/` or `architecture/` moved in the range or
in this pass, and `check-pin-drift.sh` reports 193 pins clean with `install.sh` pinned file-level.

Blocking: none

No finding rises to holding the push. F1 was a real regression of a deliberate same-day fix and is
closed in this tree with a test that was red first. F2 is unverifiable rather than wrong, touches no
reader in the tree, and is recorded as standing on the author's word. F3 is already closed by the
range's own second commit.
