# Retired: `spec/public-contract.md` Requirement 194, criterion 15 and its case heading

Retired 2026-09-06, with the row that held it open (`q-385`). The criterion promised a gate nobody
was building and carried the `[target]` marker that put that promise on the owner's board. Its
revisit trigger — the first host declaring a contract in its own card — has not fired: every
adopted project's `.live-spec/agent.md` still reads "None today" under "Contracts this agent
publishes", so there is no real producer and no real consumer for the three arms to be proven
against, and a promise nobody can honestly finish is not a current commitment.

The default-deny law itself is untouched and stays live: criteria 4, 5 and 6 of the same
requirement carry it, `matrix/spec-author.md` M-362 proves it at `string` level, and
`tests/test_agent_channels.py::TestDefaultDeny` asserts it. What retired is only the promise of the
producer-side gate's machinery.

The row's own text, with the full reasoning, is at
`docs/queue-archive/rotated-PLAN-2026-09-06-q385-no-producer-declined.md`.

The excerpt, verbatim as it stood:

```
**Case: the default-deny gate is promised**

15. the gate that reds a default-deny violation on the producer's suite *shall* stay promised until a host's first real contract. [INV-185]
    [target]
```
