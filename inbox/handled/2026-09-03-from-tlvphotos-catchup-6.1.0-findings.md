# Wish: two pack defects found during tlvphotos' 2.7.0 → 6.1.0 catch-up walk

**From:** a session working in `~/tlvphotos`, closing PLAN.md row S-51 (steps 8-9 of
`inbox/2026-08-27-live-spec-6.0.0-catchup.md`, now at `inbox/handled/`), 2026-09-03.
**Evidence:** `~/tlvphotos/.live-spec/adopt/2026-09-03-catchup-6.1.0.md` — the whole walk's Log and
Findings.

## 1. Gate `s` (`check-skill-review.sh`) has no carve-out for an unedited vendor-skill refresh

`sync-skills.sh` replaced 13 skill bodies wholesale, byte-for-byte from the pack. Every one of those
13 changes was already reviewed on the pack's own side (records under `~/live-spec/docs/skill-review/`).
The host gate still demanded a fresh `docs/skill-review/` record for each of the 13, as if a human had
hand-edited a skill body here. There is no path in the gate that recognizes "this SKILL.md is
byte-identical to a pack commit the pack already reviewed" and skips the demand, or that lets the host
satisfy it by citing the pack's own record instead of authoring a new one.

Worked around this time by writing 13 short host-side records under `docs/skill-review/2026-09-03-*.md`,
each quoting the pack's own verdict (source record path + date) rather than inventing a fresh review —
see the adopt file's step 3 Log for the full mapping (which pack record was quoted for which skill).
That workaround is legitimate but it is a per-host tax on every future sync; a host doing a wholesale
refresh with `sync-skills.sh` will hit this every time. A carve-out — accept a review satisfied when
the synced file hashes identical to a commit the pack's own `docs/skill-review/` already covers — would
remove the tax without weakening the gate for an actual hand-edit.

## 2. Step 9's rollback proof: the expected difference count is six, not five

The migration wish's step 0 takes the tracked-content fingerprint (`git ls-files -z | xargs shasum`)
**before** running the "before" suite (`python3 tests/run_all.py`). `tests/suite_timings.json` is a
tracked file the suite rewrites on every run, so it always differs from the pre-fingerprint at step 9's
post-rollback diff — a sixth difference beside the adopt file, the manifest itself, and the three
`product-prover` paths (which the wish's own step 9 acceptance names as four). This host's walk hit
exactly this: the real rollback rehearsal showed six differences, all expected, none a leak. A host
without a `tests/suite_timings.json`-shaped tracked artifact would never see this, so it may be specific
to hosts whose test runner rewrites a tracked file — but the wish's step 0 ordering (fingerprint before
suite) makes it a systematic gap for any host that has one. Either reorder step 0 (run the suite before
the fingerprint) or add the file to step 9's known-difference list explicitly.

Both findings are reported as-is; neither blocked this host's walk (S-51 accepted both as findings, not
defects the walk had to fix).

---

**Handled 2026-09-03, PLAN q-814.** Both findings landed: `guardrails/check-skill-review.sh` gained the
byte-identical-to-a-reviewed-pack-commit carve-out (finding 1), and `MIGRATION.md`'s before-and-after
self-test (INV-92) now names a test-runner-rewritten tracked file as an accounted-for difference class
by name (finding 2). See PLAN.md's own q-814 entry for the closing note and the tests proving both,
red-then-green.
