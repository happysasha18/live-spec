# Prover record — the acceptance moves into CI, and the five holes in that move

PUSH-REVIEW

Prover skill version: product-prover (installed under `skills/product-prover/`), read beside
`skills/product-prover-pack/SKILL.md` v6.1.0 and `skills/live-spec-base/SKILL.md`. The adversarial
read was run by a fresh seat that authored none of the change, briefed to find reasons to refuse
it and holding it defective until evidence said otherwise. Its verdict was **refuse**, with five
blocking findings. All five are closed in the commit below, which this record is committed after.

Range: 1d413c42..HEAD

- 9246e86e The acceptance is fixed at admission, and the run that decides happens in CI —
  guardrails/check-acceptance-rerun.py as CI gate v, the board's workflow moved behind a green
  gates run for the commit it judged, the acceptance frozen at admission with its digest anchored
  on the checkpoint, both anchors compared against the copy the remote holds, and the pre-spawn
  guard moved from a row id to a spawn token the brief cuts

This record ships in its own commit after it, which the gate exempts because a record cannot name
the commit that first carries it.

Files read: `guardrails/check-acceptance-rerun.py`, `guardrails/check-close-receipt.py`,
`guardrails/worker-admission-guard.py`, `scripts/task-admission.py`, `scripts/plan_checks.py`,
`scripts/plan_checks_core.py`, `scripts/plan-step.sh`, `scripts/render-board.sh`,
`scripts/checkpoint.py`, `.github/workflows/gates.yml`, `.github/workflows/pages.yml`,
`.claude/settings.json`, `.gitignore`, the diff under `tests/`, and both build-pipeline documents.

Checks run: the full suite on this range's final code, the local gate chain on the same tree, the
acceptance re-run against this project's own board, and the reviewer's own read-only probes of the
check table and of every key's reach. Each with its result below.

```
$ python3 -m pytest -q                      (on this range's final code)
2999 passed, 5 skipped, 1 xfailed in 1560.16s (0:26:00)
(exit 0)
```

```
$ bash guardrails/pre-push                  (local chain, this tree)
All gates green — push allowed.
(exit 0)
```

```
$ python3 guardrails/check-acceptance-rerun.py
   ran 71 done row(s)' own acceptance command at this commit.
   71 of them predate the acceptance anchor, so what ran is the command the tree records now.
   2 done row(s) hold a key that reads this machine rather than the tree, which a checkout
     cannot judge; admission refuses such a key today: q-458, q-624
   8 done row(s) record no acceptance command and were not run (admitted before one was
     required): q-205, q-568, q-584, q-610, q-612, q-800, q-808, q-809
   every done row's acceptance passes here.
(exit 0)
```

The reviewer's own probe of the board, quoted because finding 1 turns on it: 81 done rows, 73
keyed, 8 keyless, 2 reading the machine, and `plan-11`'s key reads `board.html`, which
`.gitignore` keeps out of git.

Findings: five blocking defects, five further ones, and one thing named and not repaired. Every
blocking defect is closed in this range.

1. **The change would have bricked the board it protects.** `plan-11`'s acceptance key exits 1
   unless `board.html` exists, and that file is gitignored, so a fresh CI checkout never has one.
   Gate v would have reddened on the first push, `gates` with it, and `pages` — now gated on a
   green gates run — would never have published again. **Closed** — the gates workflow draws the
   board once, with `LIVE_SPEC_BOARD_CHECKS=off`, before gate v runs, the same way the publisher
   draws it. No acceptance key was rewritten to fit the gate.

2. **One deleted line defeated the whole first claim.** The re-run tested its keyless arm before
   the `ACCEPT:` anchor and reported rather than reddening, so forging the receipt, closing the
   sheet by hand, flipping the mark and deleting the row's line from the check table passed both
   gates. **Closed** — the anchor is read first, and an anchor standing over a missing key reds by
   name; `test_deleting_the_key_of_an_admitted_row_reds_the_rerun`.

3. **Fail-open on the one file the gate stands on.** `acceptance_table` returned an empty map on
   any import error, which turned every done row keyless and the gate green. **Closed** — an
   unreadable table stops the gate; `test_a_check_table_that_does_not_load_reds_instead_of_passing`.

4. **`workflow_dispatch` published with no verdict to read**, so whoever could type a receipt could
   also run the page workflow by hand and publish it. **Closed** — the trigger is gone, and
   `tests/test_board_publish.py` now asserts its absence along with the three publish conditions.

5. **A fork's pull request could have published its own board.** `gates` also runs on
   `pull_request`, and `workflow_run.branches` filters on the triggering run's head_branch, so a
   fork branch named `main` would have fired `pages`, which checks out `workflow_run.head_sha` —
   with the fork's own check table deciding what green means. **Closed** — the publish also
   requires `workflow_run.event == 'push'` and `head_repository.full_name == github.repository`.

6. Further: the per-key timeout was vacuous (`future.result(timeout=…)` on a completed future) and
   the `as_completed` deadline escaped into a pool exit that waits for the very threads it was
   escaping. **Closed** — the timeout is on the child, in `run_key`.

7. Further: the token was called single-use in three places and is not; it stands for every spawn
   on its row until the row closes or a digest moves. **Closed** — the wording says what it does.

8. Further: `BRIEF-TOKEN:` lines shipped onto the public board with the rest of the checkpoint's
   trail. **Closed** — the renderer drops them; `test_the_board_never_prints_a_spawn_token`.

9. Further: `brief` now writes to the checkpoint, which it did not before. Recorded in its own
   docstring and in the skill body rather than repaired: the token has to be recorded somewhere,
   and the checkpoint is the file the guard already reads.

10. Further: a route missing a field raised `KeyError` past the CLI's own handler and printed a
    traceback. **Closed** — it is refused with one reason and exit 2, like every other refusal.

11. **Named, not repaired.** Every anchor here — the done's, the acceptance's, the spawn token —
    is a line in a checkpoint, in the same file as the receipt, so a hand on this machine can
    write one. That is why the receipt gate compares both anchors against the copy the remote
    already holds, and why the acceptance that decides is executed in CI: what a local hand cannot
    rewrite is what was pushed before it. Inside one machine these are costs rather than walls,
    and both documents now say so instead of claiming impossibility.

Spec and architecture re-check: `PRODUCT_SPEC.md` is unchanged in this range. `ARCHITECTURE.md`
itself is unchanged; one of its pins moved with the lines it names
(`architecture/pipeline-and-lanes.md`) and gate g proves all 193 against the code as it stands.
The closure kernel still has no requirement of its own in the spec; this range neither closes nor
widens that gap.

Blocking: five, all closed.
- F1 closed: the gates workflow draws the board once before gate v, so a key that reads the drawn
  page can be judged in a checkout. The defect: gate v would have reddened on arrival and the
  board would have stopped publishing.
- F2 closed: the `ACCEPT:` anchor is read before the keyless arm, and an anchor over a missing key
  reds by name. The defect: deleting one line from the check table turned a forged done into a row
  the gate merely reported. Held by `test_deleting_the_key_of_an_admitted_row_reds_the_rerun`.
- F3 closed: an acceptance table that will not load stops the gate. The defect: it returned an
  empty map, which made every done row keyless and the run green. Held by
  `test_a_check_table_that_does_not_load_reds_instead_of_passing`.
- F4 closed: `workflow_dispatch` is gone from the page workflow. The defect: a hand-run published
  with no gates verdict at all, which was the one door around the publish rule.
- F5 closed: the publish requires a push, from this repository, as well as a green gates run. The
  defect: a fork's pull request from a branch named `main` could have published its own board.
