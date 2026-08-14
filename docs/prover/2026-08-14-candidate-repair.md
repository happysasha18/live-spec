# Prover record — the candidate-repair range: no prover mode ran, and this says why

**No product-prover mode was run in this pass, and none is claimed.** No prover version ran,
so this record's opening line names none. This is a review record of a pass that no push
carries, the form `docs/prover/README.md` provides for, and it carries no `PUSH-REVIEW`
marker on purpose — see *The push arm* below.

## The route law, and the decision it settles

The FULL-pass trigger is written for a MINOR bump: *"A minor (`x.Y.0`) bump of this pack
requires a `FULL` pass"* — `skills/product-prover-pack/SKILL.md:49`, pointing at
`skills/build-pipeline/references/minor-bump-gate.md`, whose own first line names MINOR and
nothing else. `skills/build-pipeline/SKILL.md:264-266` says FULL is *"required at MINOR gates
and structural rewrites"*.

This delta is neither. Of the documents a review reads — `SURFACES.md`, `PRODUCT_SPEC.md`
and its index, `ARCHITECTURE.md`, `docs/pipeline.md`, `docs/lenses.md`, `ROADMAP.md`
(`skills/product-prover-pack/SKILL.md:29-34`) — this range touches two:

- `PRODUCT_SPEC.md`: exactly one line. `git diff acf0e3c HEAD -- PRODUCT_SPEC.md` is the H1
  banner, `v4.3.0` → `v5.0.0`, date unchanged. No requirement text, no acceptance criterion,
  no clause moved. The 5.0.0 release itself predates this range's base.
- `ARCHITECTURE.md`: one `**pins**` block in the `product-prover` node — three pins re-homed
  off an external repository onto the tracked adapter, one drifted pin corrected, and three
  sentences of prose stating why. No node, responsibility, seam or flow changed.

**The open question, stated rather than answered.** The version move `4.3.0` → `5.0.0` is a
MAJOR bump by the pack's own tier law. No clause anywhere extends the FULL-pass trigger from
MINOR to MAJOR. The a-fortiori reading — a major costs more than a minor, so it can hardly
owe less — is plausible and is written nowhere. **The law is silent, and this record leaves
it silent rather than picking the answer that suits the pass.** It goes to the owner.

## Range

`acf0e3c..f09a876`, 19 commits, every one named. Two of them — the record itself and the
matrix-row repair the first complete suite demanded — landed after this record's first
writing, and are named here rather than left out of the range they belong to:

- `08acf23` The dev-machine sync and the config-health arm learn the external-skill fence the installer already carries
- `54f61fd` tests+adapter: re-home pack anchors on the product-prover-pack adapter
- `5724da7` tests: re-pin prover content needles to the externalized canon's real homes
- `a1a43f6` tests: skip, never crash, on a bare checkout with no prover clone
- `0d2082a` The document census stops walking the external clone and records the adapter the pack actually ships
- `6e9bfb3` The version stamper learns the external-skill fence: another repo's release number is not ours to write
- `6b1f0c4` Every tracked version home carries VERSION 5.0.0, and only the tracked ones
- `4bb6e65` The bare-checkout skip refuses to become CI's silent blind spot
- `c2a147d` The CI failure names its remedies instead of a queue row no branch here carries
- `76d926b` Eleven tracked-adapter anchors now hold on a bare checkout, ahead of the clone guard
- `057c87b` The tracked halves of the restructure-merge law stop hiding behind the clone guard
- `9e46503` Tracked documents are matched as written again; only the external canon reads flat
- `5e214b2` The pack's skill count stops counting another repository as one of its skills
- `f100c73` CI installs the external canon, pinned to a commit and verified — the fork is closed
- `1ebc6e8` Two checks of the CI authority model could pass over nothing; both now bite
- `db6c0d9` The published skills line count stops counting another repository's lines
- `35f3977` The architecture stops promising line numbers inside another repository
- `c1139b0` The candidate-repair range gets its record: no prover mode ran, and the law that says so is cited
- `f09a876` Row M-253 names the tests that now carry its law, not the three it used to have

## Files read

`PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `SURFACES.md`, `skills/product-prover-pack/SKILL.md`,
`docs/prover/README.md`, `guardrails/check-prover-record.sh`,
`skills/build-pipeline/references/minor-bump-gate.md`, `.github/workflows/gates.yml`,
`scripts/install-external-skills.sh`, `scripts/gen-tree-counts.py`,
`guardrails/tree-counts.json`, and the whole diff of the range above.

## Checks run

The bullets below were run before this record was first written. The four complete suites
after them were added once they finished, over the final tree, and say so in their own words.

- Gate g (pin drift): **OK, 209 pins checked** — with the canon installed AND on a bare
  checkout. Red at the base in both environments.
- Gate ad (published tree counts): **OK** — with the canon installed AND on a bare checkout.
  Red at the base.
- Gate aa (doc findings bound): **OK — 124 live documents, 22 held at zero, none above its
  record**, `ARCHITECTURE.md` held clean after this range's prose edit.
- Gate u (CI mirror parity): **OK**. Gate ae (named checks): **OK, 32 registry entries,
  11 skill bodies scanned**.
- Focused modules, bare checkout: `test_edge_completeness` + `test_finding_kind` +
  `test_restructure_merge_gate` → **17 passed, 8 skipped**.
  `test_prover_adapter_contract` + `test_architecture_format` → **30 passed**.
  `test_tree_counts` + `test_published_counts` → **47 passed**.
  `test_skill_count_agrees` → **13 passed**, with the canon installed and without it.
- Each of the four fresh-review repairs was proven red first; the before/after counts are in
  each commit's own message and in the wave digest.

**The four complete suites, added after they finished.** Run strictly one at a time on one
machine, each a whole `python3 -m pytest -q --durations=25`, over the final tree — the two
commits that landed after this record was first written are named in the range above.

| run | result | wall |
|---|---|---|
| final, tracked-only (no clone) | **7 failed, 2,491 passed, 54 skipped** | 16m 49s |
| final, clone-present (what CI now carries) | **7 failed, 2,544 passed, 1 skipped** | 16m 03s |
| baseline `acf0e3c`, tracked-only | **73 failed, 2,448 passed, 1 skipped** | 15m 42s |
| baseline `acf0e3c`, clone-present | **68 failed, 2,453 passed, 1 skipped** | 16m 08s |

Complete node-id sets were compared, not samples. **Introduced by this range: none, in
either environment** — `comm -23 final baseline` is empty both ways. The candidate closes 66
of the baseline's failures on a tracked-only checkout and 61 with the canon installed.

Two properties of the final set are worth stating because they are what the range was for.
It is the **same seven node ids in both environments**: the candidate no longer behaves
differently depending on whether a developer has run the installer. And the 54 skips of the
tracked-only run are exactly the canon-only assertions, which become 53 further passes when
the canon is present (2,491 + 53 = 2,544, one skip remaining in both) — the skips are named
and accounted for rather than silent.

The seven that remain, each present in both baseline sets:

1. `test_config_health.py::TestConfigHealth::test_this_repo_installed_hooks_match_source` —
   environmental; reads the real `~/.claude`, which has drifted from source on this machine.
2. `test_config_health.py::TestPermissionPathHealth::test_real_personal_settings_stands_down_or_passes`
   — environmental; reads real-HOME permissions.
3. `test_every_gate_can_fail.py::TestEveryGateCanFail::test_registered_proofs_exist` —
   pre-existing; gate f names a proof function `test_broken_skill_fails` that does not exist.
4. `test_every_gate_can_fail.py::TestEveryGateCanFail::test_real_chain_is_compliant` —
   cascade of 3.
5. `test_guardrails.py::TestGateB_Tests::test_real_content_passes` — cascade; gate b runs the
   whole suite inside itself and reds while anything above reds. Its inner run reports
   `6 failed, 2,533 passed` — this list minus itself.
6. `test_landing_next_steps.py::test_real_repo_range_refreshes_next_steps` — pre-existing;
   its message names `acf0e3c1`, the base commit itself, as the offending landing.
7. `test_worker_restore.py::…::test_the_gate_runs_against_this_machines_own_transcripts` —
   environmental; reads this machine's own transcript directory.

One red the range closes rather than merely leaves alone:
`TestGateA_ProverRecord::test_real_repo_passes` fails at both baselines and passes on both
final runs. This record is what closes it.

**Cost this range adds to a run:** the pinned installer step took 1.6s. The suite's own
shape dominates instead — `TestGateB_Tests::test_real_content_passes` 218.5s, then the
`TestGateG_PinDrift` family and `TestCIMirror` at 39–91s each. Reported, not tuned.

## Findings

An independent adversarial reviewer, briefed to refuse, read this range against git rather
than against any summary and returned **REFUSE** with three blocking findings. All three are
closed, each by a commit in the range above:

1. The pinned canon contradicted `ARCHITECTURE.md`'s own pins — closed by `35f3977`, which
   stops the pack promising line numbers in another repository at all.
2. The published skills line count became unsatisfiable once CI installed the canon — closed
   by `db6c0d9`, which fences the measurement and rebuilds the block.
3. The installer-step ordering assertion read the whole workflow file, so a step in the other
   job satisfied it — closed by `1ebc6e8`, which scopes the reader to the `gates` job.

A fourth, non-blocking, was also closed in `1ebc6e8`: a test claiming to compare the pin
against the adapter floor asserted only that a digit capture held digits, which cannot fail.

Two things the reviewer confirmed rather than found: no test was deleted, xfailed, skipped,
narrowed or relaxed anywhere in the range, and `guardrails/check-worker-restore.py` reports
no finding from this session in any tree.

## Blocking

none — the three blocking findings above each read `closed:` with the commit that closed it.

## The push arm, and why it refuses

`guardrails/check-prover-record.sh`'s push road resolves the base from `origin/main`, which
is `be4e4f0`, seven commits behind this range's own base. An honest push record would have to
name `be4e4f0..HEAD`, 21 commits — and this pass reviewed 17 of them. `PRODUCT_SPEC.md:3235`
holds that a record naming a range other than the pushed one covers nothing, so no
`PUSH-REVIEW` marker is written here and the push arm correctly refuses. Whoever pushes owes
a record over the real push range. That is not a defect in this record; it is this record
declining to claim a range it did not read.

The freshness arm is a different matter and was already owed before this candidate existed:
at `acf0e3c` the newest committed record (`13671c2`) already predated the last change to
`PRODUCT_SPEC.md`. This record is dated today and closes that arm on this branch.
