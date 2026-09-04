# The style-gate installer wires its block under a letter the pack has already spent

From: tlvphotos, 2026-09-04, during a full re-run of the three adopt installers (the host had drifted
to pack 3.6.0 on its gate layer while its skills read 6.1.0).

## What happened

`adopt/install-style-gates.sh` step d writes its block into the host's `guardrails/pre-push` as:

```
# live-spec:gate-r
echo ""
echo "-- gate r — style gate --"
```

Two problems, both mechanical.

**One. The letter r is already taken.** The pack's own `guardrails/pre-push:222` runs
`-- gate r: authority anchor (SPEC INV-207) --`, and every host that vendored the pack's gate chain
carries that same letter. So the installer hands the host a second gate under one letter. This host
had already hit it once by hand: the comment sitting above the insertion point reads "The ratchet
installer appends its own gate here under the letter r, which the pack itself gives to the
authority-anchor gate above" — the same collision, under the kit's earlier name, patched by hand and
then re-created by this run.

**Two. The marker shape does not match what the meta-gates enumerate.** Gate u (CI mirror) and gate w
(every gate can fail) enumerate the chain by the `-- gate X: ... --` marker — a letter, then a colon.
The installer writes `-- gate r — style gate --`, a letter then an em dash, which that shape does not
match. So a style gate wired by this installer is invisible to both meta-gates: it can never be
required to carry a known-red proof, and it can never be checked for a CI mirror.

The second problem is the more interesting one, because it defeats the installer's own stated purpose.
This host's inbox already carried a finding from 2026-07-14 saying the style lint "reaches the push
gate through the ratchet's cap rather than by its own name, so a reader of the gate list cannot see it
run". Re-running the installer to fix exactly that leaves it named in a shape the gate list's own
readers skip.

## What this host did

Kept the `# live-spec:gate-r` marker comment byte for byte, so a re-run of the installer finds the
block and reports `already-wired` rather than appending a second copy. Rewrote only the echoed line to
the host-gate form this file's own header defines: a pack gate carries the pack's letter and echoes
`-- gate X: ... --`; a host gate carries no letter and echoes `-- host gate: ... --`. The pack's own
push chain gives the style lint no letter, so host gate is the honest classification, and the check is
now visible by name in the printed chain.

## What the pack might do

Two candidates, and this host has no standing to pick between them:

1. Give the style lint its own free letter in the pack's own chain first, then have the installer
   write that letter with the colon form the meta-gates read. Free letters in the pack's chain today:
   the alphabet minus a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, x, y, z.
2. Have the installer write the block as a host gate (no letter, `-- host gate: ... --`), which is
   what a host-document check arguably is, and drop the letter from the block entirely.

Either way the installer should stop emitting a letter it did not reserve, and should emit whichever
marker shape the meta-gates actually enumerate.

## Evidence

- `~/live-spec/adopt/install-style-gates.sh`, step d, `BLOCK_LINES`.
- `~/live-spec/guardrails/pre-push:222` — the authority-anchor gate under r.
- `~/tlvphotos/guardrails/pre-push` — header rule for pack vs host gates; the hand-patched comment
  recording the same collision under the kit's earlier name; the repaired block at the tail.
- `~/tlvphotos/inbox/HANDLED.md`, row `2026-07-14-from-livespec-pack-v1.4.0-cleanup-and-divergence-rule`
  — the original "cannot see it run" finding.

---

**Handled 2026-09-04 (q-821).** Went with candidate 1. The installer now writes its block under gate
v, not r: verified directly against the tree rather than trusting this wish's own free-letter line —
`guardrails/pre-push` currently runs a-t, x, y, z, so v is free, and so are u and w, the two letters
this wish names as spent by the CI-mirror and every-gate-can-fail meta-gates. Those two gates, and
every other check whose only subject was another check, were retired 2026-08-21 (commit e61b29b7,
"Remove the checks whose only subject was another check") — over two weeks before this wish landed,
so the meta-gates it describes no longer run at all. v was picked anyway, over the now-also-free u or
w, to leave those two letters exactly as the retirement left them rather than resettle them by the
first fix that happened to need a letter.

The block now echoes `-- gate v: style gate --`, the colon shape the chain's own gates already use
(`guardrails/pre-push` gates a through z read this way). The installer's repair path — until now used
only to move a marker found past a dead exit, or to replace a live block still calling the retired
ratchet-lock test — was widened to also replace a live block that carries the old marker
`# live-spec:gate-r`: any found block not carrying the current `# live-spec:gate-v` marker line
counts as stale and gets swept into the new letter and shape, wherever it stands. A host that already
carries this host's own hand-patched form is repaired the same way, since its label still reads
"gate r" under the tolerant label-drift match.

Proven on a scratch host tree (`tests/test_style_gate_kit.py::TestGateStyleWiring`,
`test_e3_a_host_carrying_the_old_r_lettered_dash_block_is_replaced_by_v_colon_on_reinstall`): a
pre-push carrying the exact old block this bug produced, installer run twice, asserts the first run
reports `repaired: guardrails/pre-push gate v` and the second `already wired`, and that the file ends
up with exactly one `-- gate v: style gate --` block and no trace of `gate r` or the em-dash shape
anywhere. Run against the installer as it stood before this fix, the same test reds on the first
assertion — the old installer reports `already wired: guardrails/pre-push gate r — style gate` and
never touches the colliding, unreadable block, which is exactly the defect this wish named. The rest
of the wiring suite (`TestGateStyleWiring`, formerly `TestGateRWiring`) was carried over to the new
letter and shape rather than left asserting the retired ones. `python3 -m pytest -q tests/` full
suite green after the change.

Candidate 2 (host gate, no letter) was not taken: the check runs as a real pack gate wherever it is
adopted, and a host-gate label would misclassify it. This host's own hand-patched host-gate label
gets swept up and replaced by the letter-v form on its next installer run, same as any other host.
