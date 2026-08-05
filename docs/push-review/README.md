# Push review records

This directory holds one record per push review. A push review is the adversarial read of the change
a push is about to send. The reviewer is briefed to find reasons the change should be refused, and
holds the change defective until evidence says otherwise. A read that sets out to confirm the change
leaves the requirement unmet.

The rule lives in `PRODUCT_SPEC.md` under `[INV-304]`. The gate that reads these records is
`guardrails/check-push-review.sh`, wired into `guardrails/pre-push` as gate ac.

## What the review covers

The delta being pushed: every commit between the remote's head and the local head. Whatever is still
uncommitted is read with them. The range comes from the base ladder the prover-record gate uses —
`LIVE_SPEC_DIFF_BASE`, then `origin/main`, then `HEAD~1`.

The commit list for the record:

```
git log --oneline origin/main..HEAD
```

## The record's shape

One file per review, named `YYYY-MM-DD-<slug>.md`, committed before the push:

```
# Push review — 2026-08-05 <slug>

PUSH-REVIEW

Range: 258d544..9f21ab0
Commits:
- 9f21ab0 <subject>
- 258d544 <subject>
Files read: PRODUCT_SPEC.md, guardrails/pre-push, tests/test_push_review.py
Checks run: python3 -m pytest tests/test_push_review.py -q — 14 passed
Findings: <what the review found>
Blocking: none
```

Each field carries a value. A review that found nothing writes into `Findings:` what it examined. The
absence then rests on the coverage the fields above state, rather than on silence.

`Blocking:` reads `none`, or lists one item per blocking finding. Each item carries `closed:` with
what changed, or `stands:` with the reason it stands. A blocking finding holds the push until one of
those two is written.

## What the gate holds, and what it leaves to the reviewer

The gate holds six things:

- a record exists;
- the record is committed, rather than a scratch file in the working tree;
- the record is fresh against the pushed range;
- the record names the base commit;
- the record names every reviewed commit;
- each field carries a value, and a blocking finding is closed or explained.

The gate leaves three things to the reviewer:

- whether the review was adversarial;
- whether the files the record names were read;
- whether the findings are the ones the delta deserved.

No script decides those three. The record's named commits, files, checks and findings are the
pressure a machine can apply toward the review being real.
