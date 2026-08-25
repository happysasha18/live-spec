# Prover record — 2026-08-25 r5-pin-repoint-after-slice-2

PUSH-REVIEW

Range: 8b28a838..bba99eac (1 commit)
- bba99eac Re-point r5 rule-price pins after spec-author's +6 line shift

Files read: full diff of bba99eac (1 file, 15 insertions / 15 deletions); the whole of
`.live-spec/r5-rule-prices-2026-08-11.md`'s spec-author rows and their detail sections, before
and after; `skills/spec-author/SKILL.md`'s current line numbers for every quoted opening line
(confirmed by `grep -n` against the five affected rule texts); `guardrails/check-pin-drift.sh`'s
r5 leg to confirm what it checks (a line range's content proved by the pin's own naming words,
tolerance ±2 lines for single-line pins) and that the file's own byte/price/test-count columns
are untouched by this fix.

Checks run: `git push` on the prior commit (8b28a838) hit a local gate failure before touching
the remote — `guardrails/pre-push`'s gate g (pin drift) FAILED: "skills/spec-author/SKILL.md:
206-206 — no naming word of the label stands in lines 206-206". Cause: the immediately prior
commit (8875ca80, batch-2b slice 2) inserted a 6-line section into `spec-author/SKILL.md` above
five pinned ranges in `.live-spec/r5-rule-prices-2026-08-11.md`, drifting each range by +6 lines
— confirmed by `grep -n` showing "1. **Author / grow the relevant requirement**" moved from line
193 to 199, "3. **Run the completeness pass**" from 206 to 212, a consistent +6 across all five.

Fix: the same re-pointing method the file's own header already documents for an earlier,
larger version of this exact situation (the 2026-08-17 spec-author offload note: "Every
affected row's home path and line range was re-derived by matching its exact text in the new
tree. No rule's text, body-byte count, pinned-test count or price changed"). Each of the five
affected ranges (193-202→199-208, 210-214→216-220, 207-209→213-215, 203-205→209-211,
206-206→212-212) was updated in all three places it appears (the summary table row, the "Home:"
line, and the "Body bytes: ... counted over ... lines" line) — 15 edits total, verified by
`git diff` to touch only line-range digits, no other column, byte count, price, or rule text
anywhere in the file. Also checked whether any OTHER `.live-spec/` pin file cited a now-stale
spec-author line range — four other files reference `spec-author/SKILL.md` line numbers, but all
predate the 2026-08-17 offload and sit outside the affected range (587-596, 366, 264-268); none
of them is read by `check-pin-drift.sh`'s r5 leg or any other gate, so none needed a fix.

Re-ran `bash guardrails/check-pin-drift.sh` from the worktree root after the fix: exit 0, "OK
(pin drift, r5): 48 range pin(s) checked against r5-rule-prices-2026-08-11.md — each proved
against its own line range, by the label's naming words." No FAIL line. This is a narrow,
mechanical bookkeeping fix responding to a local gate catch (the gate itself is the adversarial
check here, the same shape as this session's earlier local-gate catches on the gate-a
self-naming exemption and the docs-discipline sync) — self-verified against the exact diff
rather than routed through a fresh independent-agent review round, consistent with how this
session has handled prior small mechanical gate-catch fixes.

Findings: one real drift caught by the local gate before it reached the remote, fixed cleanly,
re-verified green. No other defect found.

Blocking: none
