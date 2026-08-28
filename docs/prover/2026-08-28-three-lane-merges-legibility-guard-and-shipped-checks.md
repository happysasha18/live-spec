# Prover record — 2026-08-28 three lane merges: the legibility background, the restore guard, the shipped checks

PUSH-REVIEW

Range: c714833..fddd095 (11 commits), reviewed as one pass. Base commit `c714833`, the tip this
push starts from and the commit all three lanes branch off. Reviewed commits, in order:
`6ed7cff`, `5c2f6a7`, `c8bd5b1`, `3eed0aa`, `9cc56ee`, `e28bf3a`, `3c31213`, `6c0ee06`, `f44c026`,
`37674df`, `fddd095`.

Prover version that ran: product-prover 1.4.0 (`4503881`), under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

Three repairs, each built on its own branch by its own session, merged here and then reviewed as
one landing. `6ed7cff`, `5c2f6a7` and `c8bd5b1` are the lanes' own commits; `3eed0aa`, `9cc56ee`
and `e28bf3a` are the merges. `3c31213`, `6c0ee06`, `f44c026` and `fddd095` are this review's four
repairs, described under Findings, and `37674df` marks the three rows done on the board.

The legibility lint scored text against the page background wherever a selector carried no
ancestor chain, whatever the stylesheet actually said; it now scores only where the stylesheet
determines the background and reports the rest for the eye. The worker-restore guard matched five
command verbs, and sixteen assembled write-back routes passed it, including the one its own
refusal text recommended; it now judges the write target across the whole pipeline. The guardrails
installer shipped three hooks into other projects without the check scripts they call, and
`pre-commit` wrapped each content gate in a file test that skipped in silence when the script was
absent; the checks now travel, and a missing one stops the commit and names itself.

## How this review was run

Read to refuse. Every claim each lane makes about the code it changes was checked against that
code and, where the claim is about behaviour, against the behaviour — the guard was probed on
twelve command forms rather than read, the installer was run into two throwaway repositories
rather than trusted, and the scratch-copy failure was reproduced and measured both ways before
anything was changed. Four of the ten findings below are defects this review found and repaired;
one is a narrowness left standing with its reason; the rest are the lanes' own claims, checked.

Range: c714833..fddd095

Files read: `scripts/preshow-legibility-lint.py`, `scripts/preshow-register-lint.py`,
`hooks/worker-restore-guard.py`, `guardrails/check-worker-restore.py`, `guardrails/install.sh`,
`guardrails/pre-commit`, `guardrails/pre-push`, `guardrails/README.md`,
`guardrails/check-authority-anchor.py`, `guardrails/check-prover-record.sh`,
`guardrails/check-broad-kill.sh`, `guardrails/check-cleanup-notice.sh`,
`guardrails/check-muted-launch.sh`, `guardrails/check-earned-message.py`,
`tests/test_guardrails.py`, `tests/test_config_health.py`, `tests/test_authority_anchor.py`,
`tests/test_legibility_floor.py`, `tests/test_register_judge.py`,
`tests/test_worker_restore_guard.py`, `tests/test_worker_restore_run_scope.py`, `PLAN.md`,
`skills/live-spec-base/SKILL.md`,
`docs/prover/2026-08-28-ungrounded-numbers-and-board-cut-range.md`.

Checks run: `python3 -m pytest -q`, the whole suite the way CI runs it, at `fddd095` — 1 failed,
2469 passed, 2 skipped, in 18m17s; the one failure is finding 11 and belongs to no commit in this
range. `python3 -m pytest -q tests/test_config_health.py` before the installers — 2 failed, 32
passed, both on the installed restore guard having drifted from source; after
`bash scripts/install-worker-restore-guard.sh` and `bash guardrails/install.sh` — 34 passed; run a
third time after the guard's docstring edit and its reinstall — 34 passed.
`bash scripts/install-worker-restore-guard.sh` — installed, already wired, self-tests OK.
`bash guardrails/install.sh` from the pack root — three hooks installed, and again after the
same-tree repair with the same three. The guard probed through
`hooks/worker-restore-guard.py` on twelve command forms with the event's `cwd` set to this tree —
seven refused, five allowed, listed in finding 4. `guardrails/install.sh` run into two throwaway
repositories under the scratch directory: the checks and the two portable hooks install, the push
gate stays home, a commit passes, and a commit with one check deleted is refused by name.
`python3 scripts/preshow-legibility-lint.py` on a two-rule probe file, before and after finding 3's
repair. The authority-anchor gate run over a scratch copy of the tree built both ways — with
`.claude/worktrees` copied, exit 1 and 89 findings; without, exit 0. `python3 -m pytest -q
tests/test_worker_restore_run_scope.py` — 7 passed. `python3 -m pytest -q` over the five touched
modules at an intermediate commit — 1 failed, 238 passed, the failure finding 2's.
`bash guardrails/pre-push < /dev/null` at `fddd095` — gate a red for want of this record, every
other gate green; re-run at the record's own commit, verdict quoted in this record's closing line.
`git -C skills/product-prover log`, `reflog` and `show <rev>:SKILL.md` at two revisions, for
finding 11. `gh run list -L 3` — the last run on main, `33160556497`, green.

Findings: eleven, listed below.

1. **The three write-sets are disjoint but for one file, and the two accounts of it do not
   collide.** Checked rather than assumed, as the brief required. q-490 owns
   `scripts/preshow-legibility-lint.py`, `scripts/preshow-register-lint.py` and their tests and
   fixtures. q-586 owns `hooks/worker-restore-guard.py`, `guardrails/check-worker-restore.py` and
   its test. q-567 owns `guardrails/install.sh`, `guardrails/pre-commit`, `tests/test_guardrails.py`
   and `tests/test_config_health.py`. The one overlap is `guardrails/README.md`: q-567 writes at
   line 152, in the section on what the installer carries into another project, and q-586 at line
   258, in the section on what the PreToolUse guard judges. Git merged both without a conflict, and
   both texts stand in the merged file. They describe different machinery and neither weakens the
   other — q-586 states explicitly that the retrospective gate keeps its own named command list, so
   the installer's account of the shipped checks is untouched by the guard's wider reading. No merge
   was resolved by taking a side.

2. **The gate-machinery meta-test reddened, and the cause was not in the range.** The first full
   suite run after the merges gave `tests/test_guardrails.py::TestGateB_Tests::test_real_content_passes`
   red, with two inner failures in `tests/test_authority_anchor.py`. That meta-test copies the tree
   and runs the whole suite inside the copy, and the copy is deliberately git-less. The
   authority-anchor gate asks `git ls-files` for its file list and falls back to walking the
   filesystem when git is absent, so in the copy it walked into `.claude/worktrees` — three other
   sessions' checkouts of this same repository — and read the pack's own documents three more times
   over, the deliberately unanchored fixtures that gate ships to prove itself among them. Measured
   on the live tree, building the copy both ways and running only that gate: with the worktrees
   copied, exit 1 and 89 findings, every one of them in a file git would never have listed; with
   them excluded, exit 0. Not caused by the merges — none of the three lanes touches the gate, the
   fixtures, or the test; what the merges did was make the meta-test fire at all, since it runs only
   when the diff reaches gate machinery. Repaired in `f44c026`, in the copy rather than in the gate:
   the scratch copy now leaves `.claude/worktrees` behind, for any worktree any session opens.
   Nothing was excepted from the gate, whose reach over the copy's own content is unchanged.

3. **The legibility lane silently dropped the text it stopped guessing about.** Making an alpha
   component unreadable is right — `rgba(200,200,200,.5)` renders as whatever it is composited
   over, and scoring it as its opaque triple invents the number the whole ratio then rests on. But
   `parse_color` returns `None` for it, the same answer it gives a named colour, and `scan` passes
   over a declaration whose colour is `None` without a word. So text declared translucent left the
   report altogether: not scored, and not named either. On a probe file, `.solid { color:#ccc }`
   was reported at 1.6:1 and `.faint { color:rgba(200,200,200,.5) }` beside it produced no line at
   all. That is the defect the rest of the lane removes, one case over, and it is a regression
   against the base, where the pair was at least named with a wrong number. Repaired in `3c31213`:
   such a pair goes to the unresolved list with its own plain reason. The unresolved list reports
   for the eye and blocks nothing, so no gate tightens. Its heading, which spoke only of a
   background, now covers a foreground reason too.

4. **The restore guard closes the assembled act inside one command, and one route stays open.**
   Probed on twelve forms against the installed hook rather than read. Refused:
   `git show HEAD:PLAN.md > PLAN.md`, the same with `| tee`, `>|`, `| dd of=`, `git cat-file -p`
   in place of `show`, `git archive HEAD | tar -x`, and the absolute spelling of the target under
   the event's own `cwd`. Allowed, correctly: a bare `git show HEAD:PLAN.md`, `>> PLAN.md`,
   `> /dev/null`, `git log`, `git diff`. The refusal text no longer recommends a route the guard
   would refuse — it recommends printing the saved copy and writing the file with the file-writing
   tool, and the probe confirms the print half passes. What stays open is the act staged across two
   commands: `git show HEAD:foo > /tmp/foo` parks the bytes outside the tree and is allowed, and a
   later `cp /tmp/foo foo` carries no sign of the repository at all. It cannot be closed from a
   PreToolUse hook that sees one command per event, and refusing every copy onto a tree path would
   refuse ordinary work all day to close one route. The retrospective check does not close it
   either: it reads git verbs, and neither half is one. Stated in the hook's own reach paragraph in
   `6c0ee06`, beside the two limits it already declared, rather than left for the next reader to
   discover — which is the shape of the defect q-586 was.

5. **The installer's reason for keeping the push chain at home is not true as written.** Both the
   installer header and `guardrails/README.md` said every one of the push chain's gates reads a
   document of this repository's own. Three do not: `check-broad-kill.sh`,
   `check-cleanup-notice.sh` and `check-muted-launch.sh` read the diff and nothing else, and would
   hold in any repository — their only mentions of a repository document are in comments. The
   decision itself stands, on the reason that is true: most of the chain does read
   `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `TEST_MATRIX.md`, `docs/prover`, `skills/` and `scaffold/`,
   and the chain refuses a push when any gate reds, so a copy of it elsewhere blocks every push over
   files that project does not have. Corrected in `fddd095`, in all three places the claim was
   written — the header, the README, and the board row — with a sentence naming what a project does
   pick up when it takes the chain's shape by hand.

6. **The installer read a worktree of its own repository as a foreign project.** The same-tree test
   compared the destination's `guardrails` directory against the pack's by device and inode. A
   linked worktree of this very repository has its own `guardrails` directory at its own inode, so
   it read as a host: measured from `.claude/worktrees/agent-a8338406e08c9e601`, the test answers
   no while `git rev-parse --git-path hooks` resolves to `/Users/sashaabramovich/live-spec/.git/hooks`
   — the hooks directory every worktree shares. Running the installer from a worktree would
   therefore have refreshed `pre-commit` and `post-commit` in that shared directory and left
   `pre-push` behind, an unannounced drift the config-health gate would later red on, and printed
   a message telling the reader this repository lacks documents it has. Repaired in `fddd095` by
   comparing the shared git directory, the one path a repository and all its worktrees agree on.
   Confirmed against four cases: the pack root, the pack's `guardrails` folder, a linked worktree,
   and a repository elsewhere. Re-run from the pack root afterwards, all three hooks install as
   before; run into a fresh repository elsewhere, the three checks and the two portable hooks
   install and the push gate stays home.

7. **The shipped-checks lane holds end to end, tried rather than read.** Into a throwaway
   repository: the installer put `check-future-times.sh`, `check-deferral-marker.py` and
   `fence-refresh.sh` into that repository's own `guardrails/`, `pre-commit` and `post-commit` into
   its hooks, said plainly that it was leaving the push gate alone and why, and a commit went
   through under them. Deleting one check and committing again gave the refusal, naming the missing
   file and what to run — and it stops the commit, where before the gate would have skipped in
   silence and the commit would have looked checked.

8. **The register lint's stand-down notice reaches every caller it has.** `judge_document` now
   returns a pair instead of a list, which would break a caller that unpacks the old shape. The only
   caller in the tree besides the script's own `main` is `tests/test_register_judge.py`, updated in
   the same lane. The notice prints and does not block: the literal pattern list's verdict stands
   either way, which is what keeps a broken judge from turning into a refusal.

9. **One narrowness in the new background resolution, left standing.** `_page_background` returns
   the colour of the first page-element rule that paints anything, so a stylesheet that opens with
   `html { background: url(...) }` and sets a plain colour on `body` further down resolves to
   nothing, and every chainless pair in that file is reported unresolved. It errs to reporting
   rather than to a number, which is the direction the whole lane moves in, and no verdict can be
   wrong because of it. Left as it is rather than repaired: a second pass over the page rules would
   be machinery for a shape nothing in the tree has, and the reported pairs name themselves.

10. **The two config-health reds cleared on the installers, as expected, and nothing else moved.**
    Before the installers, `tests/test_config_health.py` gave two failures, both on the one message
    that the installed `worker-restore-guard.py` had drifted from source. After
    `scripts/install-worker-restore-guard.sh` and `guardrails/install.sh`, 34 passed. The guard
    installer writes into `~/.claude`, outside the project, which is its documented act and the
    owner's own self-install line. The `pre-commit` drift the brief also expected was already gone
    by then, carried by the q-567 merge itself. Re-run after the docstring edit in `6c0ee06`, so the
    installed copy and the source match at the tip of this range.

11. **The suite's one remaining red belongs to the external prover skill, not to this range.**
    `tests/test_prover_doc_homes.py::test_description_carries_only_the_trigger` asserts that the
    prover skill's frontmatter description still carries the phrase "hold together as written". It
    reads `skills/product-prover/SKILL.md`, the clone of another repository installed inside this
    tree and tracked by none of this repository's commits — `git ls-files` names it not at all. That
    clone moved today at 14:46 from `4503881`, version 1.4.0, to `efe05fa`, version 1.4.2, whose
    commit is "shorten product-prover discovery metadata" and which rewrote the description without
    that phrase. The owner confirmed the update in chat the same afternoon. The phrase is present at
    `4503881` and absent at `efe05fa`, checked at both revisions. CI installs the pinned
    `4503881`, so the server will not see this red. It is left as it stands: following the external
    skill's move means either moving the pin or rewriting what the test asserts, and either is a
    change of its own with its own review, not something to fold into this landing unremarked.

Blocking: one item, closed.
- closed: `tests/test_guardrails.py::TestGateB_Tests::test_real_content_passes` reddened on the
  merged tree (finding 2). Diagnosed to the scratch copy carrying three other sessions' worktrees
  into a git-less tree, measured both ways, and repaired in `f44c026` by leaving those worktrees
  out of the copy. It passes in the full run at `fddd095`. The authority-anchor gate was not
  loosened, skipped, or excepted; its reach over the copy's own content is what it was.

