# Prover records

This directory holds one record per review pass. Every push carries exactly one of them, and that
one record does the whole job: it is the fresh re-check of `PRODUCT_SPEC.md` and `ARCHITECTURE.md`
that the push gate has always demanded, and it is the adversarial read of the change the push is
about to send. The reviewer is briefed to find reasons the change should be refused, and holds the
change defective until evidence says otherwise. A read that sets out to confirm the change leaves
the requirement unmet.

The rule lives in `PRODUCT_SPEC.md` under `[M-6]`, `[INV-116]` and `[INV-304]`. The gate that reads
these records is `guardrails/check-prover-record.sh`, wired into `guardrails/pre-push` as gate a.

Records of review passes that no push carries — a milestone re-prove, a periodic audit — live here
too, under the same file naming. Only a record written for a push owes the range fields below.

## What the review covers

The spec and the architecture as they now stand, and the delta being pushed: every commit between
the remote's head and the local head. Whatever is still uncommitted is read with them. The range
comes from the base ladder the gate walks — `LIVE_SPEC_DIFF_BASE`, then `origin/main`, then `HEAD~1`.

The commit list for the record:

```
git log --oneline origin/main..HEAD
```

## The record's shape

One file per pass, named `YYYY-MM-DD[-slug].md`, committed before the push. The suffix is mandatory
once the date's plain file exists.

```
# Prover record — 2026-08-05 <slug>

PUSH-REVIEW

Range: 258d544..9f21ab0
- 9f21ab0 <subject>
- 258d544 <subject>
Files read: PRODUCT_SPEC.md, ARCHITECTURE.md, guardrails/pre-push
Checks run: python3 -m pytest -q — 2,484 passed
Findings: <what the review found>
Blocking: none
```

Those are all the fields, and the gate reads every one of them. Each carries a value. The commits
between the base and the head are listed under `Range:`, since the gate holds that the record names
every commit it covers. A review that found nothing writes into `Findings:` what it examined; the
absence then rests on the coverage the fields above state, rather than on silence.

`Blocking:` reads `none`, or lists one item per blocking finding. Each item carries `closed:` with
what changed, or `stands:` with the reason it stands. A blocking finding holds the push until one of
those two is written.

## What the gate holds, and what it leaves to the reviewer

The gate holds:

- a record dated today exists;
- the record is committed, rather than a scratch file in the working tree;
- the record is no older than the last change to `PRODUCT_SPEC.md` or `ARCHITECTURE.md`;
- the record is fresh against the pushed range;
- the record names the base commit and every reviewed commit;
- each field carries a value, and a blocking finding is closed or explained.

The gate leaves three things to the reviewer:

- whether the review was adversarial;
- whether the files the record names were read;
- whether the findings are the ones the delta deserved.

No script decides those three. The record's named commits, files, checks and findings are the
pressure a machine can apply toward the review being real.
