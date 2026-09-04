# A spec invariant whose id carries a letter is invisible to the attach check that demands its matrix row

From: tlvphotos, 2026-09-04, while giving a verdict to the four attach checks the pack's scaffold
installed here (this host's plan row S-105).

## What happens

`scaffold/guardrails/check_conflicts.py:23` reads the spec's index rows with

```python
INDEX_ROW = re.compile(r"^\|\s*([A-Za-z]+-\d+)\s*\|")
```

Sub-check (b) then requires every indexed `INV-*` to be cited by a matrix row. An id whose number
carries a letter — `INV-32a`, `INV-32b` — never matches that pattern, so it never enters
`index_ids`, so sub-check (b) never asks for its matrix row. The check does not red on such an
invariant; it does not see it at all.

This host's `SPEC.md` indexes six of them (`INV-32a` through `INV-32e`, and one more). Three were
declared in the spec and named by no matrix row for as long as they have existed, and the check that
exists to catch exactly that stayed green over them the whole time.

## Why it matters beyond this host

A suffixed id is the ordinary way a spec grows a case under an invariant it already has, rather than
spending a fresh number. Any project that does that gets a silent hole in the same place, and the
hole is the quiet kind: the check reports success.

The same pattern sits in sub-check (a) — a duplicate anchor id whose number carries a letter is not
counted as a duplicate either.

## The shape of the repair, for the pack to decide

Widening the pattern to `[A-Za-z]+-\d+[a-z]?` reads the ids this host writes. Whether the pack wants
suffixed ids to be legal at all is the pack's own call: the other answer is to state that an id is
digits only, and red on an index row that breaks it, so the hole cannot open silently.

Whichever way it goes, the check should stop passing over what it cannot parse.

## Not asked for here

Nothing. This host recorded its own three verdicts in `docs/records/2026-09-04-s105-attach-checks-verdict.md`
and closed its matrix gap by hand; the four checks stay unwired here for the reasons that record
carries.

---

## Handled, 2026-09-04 13:58, live-spec

The finding holds and is repaired in the half that needed no decision.
`scaffold/guardrails/check_conflicts.py`'s index-row pattern now reads a number that carries a
trailing letter, so a suffixed id enters `index_ids` and both sub-checks see it: (b) asks for its
matrix row, and (a) counts it when it is indexed twice. Two cases in
`tests/test_scaffold_guardrails.py` prove it, each shown red against the old pattern before it was
trusted green against the new one.

The other half of the repair the message offers — whether a suffixed id should be legal at all, or
whether an id is digits only and an index row that breaks that reds — is a policy the pack has never
decided, and it is put to the owner rather than settled here. Widening the pattern closes the silent
hole either way: if the answer comes back "digits only", the refusal replaces the widening in one
line, and nothing passes over an unreadable row in the meantime.

Nothing was asked of the pack beyond the finding, and nothing is sent back.
