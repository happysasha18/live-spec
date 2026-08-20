# Worker-restore push review

PUSH-REVIEW

Range: `2cdeb52d..0ec4822a`

Commits reviewed:

- `0ec4822a` Fix worker restore CI contracts

Files read: `guardrails/check-worker-restore.py`, `hooks/worker-restore-guard.py`,
`scripts/install-worker-restore-guard.sh`, their fixture and tests, the hook manifests, the
pipeline verify instructions, and each repaired `ARCHITECTURE.md` pin.

Checks run: 232 focused tests passed; `check-gates-manifest.py`, `check-skill-review.sh`,
`check-config-health.sh`, and `check-doc-findings-bound.py` passed. The doc-bound check measured
188 live documents and held 28 at zero.

Findings: The review tested ordinary wrapper forms and option-bearing wrappers, incompatible
exact-run flags, and malformed settings before installation. Those three bypasses or partial-write
risks were repaired before this reviewed commit. CI then found three pre-existing exact-text and
opt-in-roster contracts that the first delivery had changed. The correction restores the contracts,
keeps the frontmatter valid, and leaves the guard a separately installed safety hook rather than
silently adding it to the generic host setup. The final tree retains one incident record and no
intermediate review records. The acceptance path has no time window, retry, or suppression key.

Blocking: none.
