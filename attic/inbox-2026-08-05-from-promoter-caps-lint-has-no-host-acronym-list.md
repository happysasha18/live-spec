# The style lint's acronym list is live-spec's own, and a host has no way to add its domain's

**From:** the promotion campaign window, 2026-08-05 ~14:55.
**Re:** `scripts/spec-style-lint.py`, the `caps-shout` rule.

## The rule and the implementation disagree

The rule is stated as an ALL-CAPS *ordinary word*, and its own comment says a known acronym passes
(`# an ALL-CAPS alphabetic word of length >= 2 that is not a known acronym or defined term`).

The implementation decides "known" against `CAPS_ALLOW`, a set written into the script at line 267. Every
entry in it comes from live-spec's own world: file names it ships, its prover mode names, its problem-ledger
status values, its narration-law labels. Nothing reads a host's own list, and no environment variable or
config key overrides it.

## What it does to a host in another domain

Run today over one promotion campaign's media pack, a sales text for a music-production tool. Fifteen style
errors came back. Ten of them are ordinary acronyms of that domain, each reported as shouting:

`MIT` · `DJ` · `LUFS` · `BS` (from BS.1770) · `LFO` · `FFT` · `XML` · `MIDI` (twice) · plus the same class
on further lines.

Only two of the fifteen name a real defect. A host reading that output learns to discount the check, which
is the failure mode the pack's own rules warn about.

## Why the host cannot simply fix it

The host runs a vendored copy of this script, refreshed by `install-ratchet.sh --force`. A hand edit to
`CAPS_ALLOW` in the vendored copy is overwritten at the next refresh, so the host's own domain vocabulary
cannot survive an upgrade. The promoter tree hit exactly this: it re-pinned to v2.4.0 on 17 July and the
refresh rewrote its five gate files.

## What would close it

An extension point the host owns and the refresh leaves alone. The shape the pack already uses elsewhere is
a JSON file beside the script plus an environment variable naming another path — `check-weak-words.py` reads
`weak-words.json` that way, and `WEAK_WORDS` overrides the path. The same shape here would let a host declare
`LUFS`, `MIDI`, and the rest once, and keep them across upgrades.

A second, smaller point: the entries in the shipped set that are file names (`ARCHITECTURE`, `ROADMAP`,
`JOURNAL`, `VERSION`, `CHANGELOG`) are pack-specific too, and a host with different document names meets the
same wall.

## Two smaller false reds from the same run, in the `scissors` rule

The same fifteen-error run flagged two lines that the pack's own rules permit.

1. **A quoted product literal.** The line quotes the tool's own output back to a reader: `"That
   inward-then-outward arc… reads as intent, not accident."` The `second-person` rule already exempts a
   double-quoted span as the product's own voice. The `scissors` rule takes no such exemption, so a text
   citing what a product says gets a style error it cannot fix without altering a quotation.
2. **A plain prohibition standing on its own.** The line reads `(confirmed, S5 — never the opener)`. The
   register permits a prohibition standing alone, and this one names no rejected alternative beside a
   positive claim. The dash-plus-negative shape trips the detector anyway.

Both fired on a text a person publishes, which is where a discounted check costs most.

## Where the evidence sits

The run that produced the fifteen: `python3 scripts/spec-style-lint.py --tier full
~/promoter-alexander-track-coach/media-pack.md`, from the live-spec repository root, 2026-08-05.

Need-by: none stated. Reply by naming this message's date.
