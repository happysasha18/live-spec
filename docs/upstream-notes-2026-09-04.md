# Upstream note — 2026-09-04

`~/.claude/skills/product-prover/SKILL.md` (the machine-installed copy) and this repo's own
`skills/product-prover/SKILL.md` were both patched locally tonight to match `spec/design-spec-review.md`
Requirement 60: a recommendation is written into the review record and ends there — it no longer
"queues for a taste call" or "queues for a judgment call". The phrasing "Where the queue order matters"
became "Where reading order matters" for the same reason, since nothing queues any more. The next
upstream update to product-prover will overwrite `~/.claude/skills/product-prover/SKILL.md`, so this
wording belongs in the upstream skill source, not only here.
