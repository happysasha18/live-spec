# Worker-restore push review

PUSH-REVIEW

Range: `8d334a15..a25aea88`

Commits reviewed:

- `a25aea88` Repair worker restore acceptance

Files read: `guardrails/check-worker-restore.py`, `hooks/worker-restore-guard.py`,
`scripts/install-worker-restore-guard.sh`, their fixture and tests, the hook manifests, the
pipeline verify instructions, and each repaired `ARCHITECTURE.md` pin.

Checks run: 232 focused tests passed; `check-gates-manifest.py`, `check-skill-review.sh`,
`check-config-health.sh`, and `check-doc-findings-bound.py` passed. The doc-bound check measured
188 live documents and held 28 at zero.

Findings: The review tested ordinary wrapper forms and option-bearing wrappers, incompatible
exact-run flags, and malformed settings before installation. Those three bypasses or partial-write
risks were repaired before this reviewed commit. The final tree retains one incident record and no
intermediate review records. The acceptance path has no time window, retry, or suppression key. The
pin review found three stale source locations and corrected them to the named skill headings.

Blocking: none.
