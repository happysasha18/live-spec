# Notes beside q-832, from its closure review

True things the closure review of the 6.1.3 push noticed outside its reach. One paragraph each.
Nothing here opens a row or asks for a repair; the intake sweep decides whether any of it is owed
one.

The watcher's new line `no installer under adopt/ vendors <key> — no road is named for it` says
something false where the cause is an unreadable `adopt/` directory rather than an unclaimed key.
Driven on a mutated copy of the pack with `adopt/` at mode 000, with `adopt/` absent, and with one
installer unreadable, the run exits 0 and every key comes back under that sentence, while an
installer does in fact vendor them. The effect is safe — no host is ever sent to an installer that
carries nothing it needs — and it is theoretical for this pack, since the installers ship inside it.

The array reader in `scripts/check-pack-update.sh` matches `VENDOR[A-Z_]*=\((.*?)\n\)`, which needs
each array to close with `)` at column 0. An array reshaped onto one line either yields nothing —
the keys go unclaimed, which is honest in effect — or over-matches to the next line-start `)` and
harvests inert junk that can never equal a real manifest key. `test_every_adopt_installer_is_a_road_the_watcher_can_name`
re-implements that same regex inside the test, so it proves the routing wiring and reds if an
installer drops its array, and it cannot catch a mis-parse: both sides misread identically.

`scripts/task-admission.py` and `scripts/checkpoint.py` are vendored by both
`adopt/install-scaffold.sh` and `adopt/install-status-view.sh`, and the sorting attributes them to
the first installer alphabetically. Both roads restore them, proved by corrupting each in a scratch
host and running the road the watcher printed, so no host is misled; a host that adopted only the
status-view kit and is stale on those two alone is nonetheless told to run a kit it never adopted.

Two copy sites live outside the arrays the watcher reads:
`adopt/install-scaffold.sh:88` copies `guardrails.config.example.json` to the host's
`guardrails.config.json`, and `adopt/install-status-view.sh:84` copies
`scaffold/status-view/plan_checks.py` to the host's `scripts/plan_checks.py`. Neither file is ever
pinned into the ratchet manifest, so neither produces an unclaimed key today. It becomes a defect
the day somebody pins a seed.

`bash <pack>/adopt/install-style-gates.sh --force` with no doc argument is a silent no-op on a host
whose gated doc is not `PRODUCT_SPEC.md`: it prints an error naming the doc it could not find, exits
0, and vendors nothing. On a host that does carry `PRODUCT_SPEC.md`, the bare re-run resets
`gated_docs` to `["PRODUCT_SPEC.md"]` and `tier` to `universal`. This is the road the watcher prints
for a style-gate-stale host, unchanged by this release.
