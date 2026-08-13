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

`acf0e3c..35f3977`, 17 commits, every one named:

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

## Files read

`PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `SURFACES.md`, `skills/product-prover-pack/SKILL.md`,
`docs/prover/README.md`, `guardrails/check-prover-record.sh`,
`skills/build-pipeline/references/minor-bump-gate.md`, `.github/workflows/gates.yml`,
`scripts/install-external-skills.sh`, `scripts/gen-tree-counts.py`,
`guardrails/tree-counts.json`, and the whole diff of the range above.

## Checks run

Everything below was run against this exact tree before this record was written.

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

**Not claimed here:** four complete suites over this exact tree, in the tracked-only and
clone-present environments, against `acf0e3c` in both. They are owed by the charter and are
being run now; their complete node-id failure-set comparison lands in
`/private/tmp/live-spec-night/roadmap-wave-digest.md`. This record does not assert their
result, because at the moment it was written they had not finished.

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
