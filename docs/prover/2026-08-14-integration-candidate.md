<!-- ARCHIVED 2026-08-17, the owner's word. This record was written on an unmerged branch and
     carried into the tree when that branch was deleted, so the reasoning it holds outlives the ref.
     It reviews a range this tree never took, it discharges no gate, and it authorizes no push. -->

# Prover record — 2026-08-14 integration candidate

NOT-A-PUSH-REVIEW. This is a review-pass record of the kind `docs/prover/README.md` allows for a
pass no push carries. **It does not discharge gate a's push arm, and no push is authorized by it.**
Two separate reasons, both stated here so nobody has to infer them:

1. The range below is `acf0e3c..bb7e759`. At push time the base ladder resolves to `origin/main`,
   which is `be4e4f0` — seven commits older. Those seven commits were not read by this pass, so a
   record claiming to cover the pushed range would be claiming coverage it does not have.
2. The mode question below is unresolved and is the owner's (see **Mode owed vs mode run**).

Range: acf0e3c..bb7e759
- acf0e3c (base — `main`, unmoved throughout this run)
- 22fc3e8 The dev-machine sync and the config-health arm learn the external-skill fence the installer already carries
- 2745a57 tests+adapter: re-home pack anchors on the product-prover-pack adapter
- 82e5595 tests: re-pin prover content needles to the externalized canon's real homes
- 9438f67 tests: skip, never crash, on a bare checkout with no prover clone
- 07f38b4 The document census stops walking the external clone and records the adapter the pack actually ships
- cff3b02 The version stamper learns the external-skill fence: another repo's release number is not ours to write
- 60e0b7e Every tracked version home carries VERSION 5.0.0, and only the tracked ones
- 9f68985 The bare-checkout skip refuses to become CI's silent blind spot
- b8d53f2 The CI failure names its remedies instead of a queue row no branch here carries
- bb7e759 Eleven tracked-adapter anchors now hold on a bare checkout, ahead of the clone guard

Files read: PRODUCT_SPEC.md (title line only — see below), ARCHITECTURE.md (unchanged by this
range, read for the freshness arm), MIGRATION.md, VERSION, .gitignore, .github/workflows/gates.yml,
ROADMAP.md, SURFACES.md, scripts/stamp-versions.py, scripts/sync-skills.sh, scripts/rule-census.py,
scripts/sweep-rendered.py, scripts/install-external-skills.sh, scripts/sync-mirrors.sh,
scripts/gen-language-consumers.py, scripts/measurements-table.py, install.sh,
guardrails/check-config-health.sh, guardrails/check-prover-record.sh, guardrails/rule-census.json,
guardrails/check-tree-counts.py, guardrails/check-every-gate-can-fail.py,
skills/product-prover-pack/SKILL.md, skills/product-prover/SKILL.md (the external clone, read only),
tests/conftest.py, tests/test_prover_adapter_contract.py, tests/test_version_is_one_fact.py,
tests/test_config_health.py, tests/test_traceability.py, tests/test_class_hunt.py,
tests/test_skill_count_agrees.py, tests/test_landing_next_steps.py, and the changed hunks of the
other 24 test modules in the range.

Checks run:
- `python3 -m pytest -q --durations=25` on the candidate — **16 failed, 2,513 passed, 1248.48s
  (20m 48s)**.
- The same 16 node ids on a detached worktree at `acf0e3c`, same machine, same installed external
  clone — **16 failed**. Every failure in the candidate reproduces at the base. **Introduced by
  this range: none.** Per-test evidence: `/private/tmp/live-spec-night/full-suite-classification.md`.
- Focused lanes, candidate: fences `3 passed`; the 31 changed modules `404 passed, 3 failed` (all
  three pre-existing); census + version homes `29 passed, 1 failed` → `10 passed` after `60e0b7e`.
- `tests/test_version_is_one_fact.py` red-first: `3 failed, 2 passed` → `5 passed`.
- `tests/test_prover_adapter_contract.py` red-first: `1 failed, 10 passed` → `11 passed`.
- Bare-checkout simulation (external clone moved aside), 31 changed modules — `369 passed,
  52 skipped, 2 failed` (the two environment-only config-health tests). No crash.
- Mutation proof of `bb7e759`, run twice independently: bare checkout + one anchor deleted from the
  tracked adapter → the guarded tests **fail** naming the missing anchor, where before the reorder
  they skipped. Coordinator's own reproduction: `1 failed, 11 passed, 2 skipped` on
  `tests/test_class_hunt.py`; restored, `14 passed`.
- Authority proof of `cff3b02`/`60e0b7e`: `sha1(skills/product-prover/SKILL.md)` is `770dafef…`
  before and after a real `scripts/stamp-versions.py` run; 12 tracked files stamped, the external
  clone byte-identical, and its own version still 1.3.0.
- `git diff 4e7a87d <candidate>` byte-identical to `git diff acf0e3c 2e36a06` — the assembly of the
  three packets introduced no drift beyond the packets themselves.
- `guardrails/check-every-gate-can-fail.py`, `guardrails/check-doc-rotation.py`,
  `guardrails/check-tree-counts.py`, `guardrails/check-prover-record.sh` run on both trees and
  compared.

Findings:

1. **The version stamper could write another repository's file, and would have.** Before `cff3b02`,
   `scripts/stamp-versions.py` walked `skills/*` with no external-clone boundary and rewrote every
   frontmatter `version:` it found. The installed external clone `skills/product-prover/` matches
   that pattern, so the next bump run would have overwritten product-prover's own `1.3.0` with this
   pack's number — a write into a project this repo neither owns nor releases. Proven red
   hermetically before the fence existed. Closed by `cff3b02` with `install.sh`'s own `.git`-probe
   idiom, and by `60e0b7e` demonstrating the fence under a real run.
2. **A convenience skip was about to become CI's permanent blind spot.** `.github/workflows/gates.yml`
   runs the suite with no step that installs the external skill, so the bare-checkout guard added in
   `9438f67` would have skipped, silently and forever, on every CI run. Closed by `9f68985`: under
   CI the guard fails and says what did not run. This does not newly red CI — gate ad already reds
   on a tracked-only checkout at the base commit, verified.
3. **The guard's own failure message pointed nowhere.** It cited ROADMAP row 624; the highest row
   this tree carries is 622, and 624 exists only on an unmerged branch. A test asserted the message
   contained "row 624" *because the failure must name where the remedy is held* — so the pin was
   green for a reason other than the one it claimed, and the dangling pointer had become
   load-bearing. Closed by `b8d53f2`, which names both remedies instead and adds a pin that refuses
   any cited row ROADMAP.md does not carry, checked against a synthetic citation so it cannot pass
   by vacancy.
4. **Eleven re-homed anchors were unprovable on a bare checkout.** `9438f67` placed the clone guard
   above assertions that read only the tracked adapter, so the very anchors `2745a57` had re-homed
   onto tracked ground stopped being proven wherever the clone was absent. Closed by `bb7e759`,
   mechanically verified as a pure reorder: across the 11 files, no line was removed and every added
   line is a comment.
5. **Checked and dismissed with evidence, not with a label:** `scripts/sweep-rendered.py` walks
   untracked `.html` under `skills/` and can move files to the attic. An aged `.html` planted inside
   the external clone was **not** swept — it classifies as a record, not a transient page. The gap is
   real but needs the external repository to adopt this pack's own transient mark. Routed as a
   follow-up, not repaired tonight.
6. **The census fence is exact, not approximate.** `SKIP_PREFIXES` is built as `dir + os.sep`, so
   `skills/product-prover/` does not swallow the tracked adapter `skills/product-prover-pack/`,
   which this same change adds to the record. `editions/product-prover/` stays measured.
7. **Sixteen reds, and the register said two.** An earlier statement of this candidate's known reds
   named only the two environment-only config-health tests. The suite returns sixteen. All sixteen
   reproduce at the base and none is introduced, but the count was understated and is corrected
   here and in the classification document. One further precision: the two config-health failures do
   not reproduce *identically* — `60e0b7e` stamped 5.0.0 into ten `SKILL.md` files, so the drifting
   installed-skill list grows from six to ten. Still host state, still no tree change can green it.

## Mode owed vs mode run

**Mode run: an adversarial read of the range** — three independent packet reviews, a
version-authority probe, and one final adversarial reviewer briefed to refuse, whose two blocking
findings are items 3 and 7 above and are both closed.

**Mode owed is unresolved and is the owner's call.** The argument for `FULL`: mode follows what a
change does, and this one changes behaviour (four tools gain fences; the stamper's write set
shrinks; a skip becomes a hard CI failure) and moves twelve requirement anchors to a different
document. The argument against: the prover's modes review a *document*, and this range changes one
line of `PRODUCT_SPEC.md` (its version stamp), no line of `ARCHITECTURE.md`, and no line of
`SURFACES.md`; what moved homes are test-side pins to documents that did not themselves move.
`CROSS-LINK` does not fit — no surface was added. `FEATURE-FIT` does not fit — no feature is written
down here for the first time.

**No FULL pass was run, and this record does not claim one.** If the owner rules FULL, it is owed
before the push, and this record's freshness does not substitute for it.

## Routed elsewhere — outside this pass's ownership

- **The CI remedy fork** (installer step in the gates job vs. proving over tracked files alone) —
  owner's, recorded on the unmerged emergency branch as its row 624.
- **The lane-cap overflow** surfaced by the C-K2 parser repair on its own branch — owner's.
- **The emergency branch's disposition** — owner's; memo at
  `/private/tmp/live-spec-night/emergency-branch-disposition.md`.
- **Suite wall time** — the gate-b pair and the pin-drift family are ~76% of a 20m 48s run.
  Reported with numbers, deliberately not optimized: a change there touches the adversarial harness.

Blocking:
- **stands:** no push is cleared by this record. The pushed range at push time begins at `be4e4f0`,
  seven commits before this pass's base, and the mode question above is open. Gate a's push arm is
  expected to refuse this record, and that refusal is correct.
- **closed:** the two blocking findings of the final adversarial review — the dangling row pointer
  (`b8d53f2`) and the understated red count (corrected in Findings 7 and in the classification
  document, with the full suite's numbers attached).
