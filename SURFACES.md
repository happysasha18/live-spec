# Surface registry — what a reader of this repo meets

The pack is a documentation-and-skills product: its user-facing surfaces are the shopfront
pages a GitHub reader lands on. One row per surface: name · a needle that must be present and
non-empty in the rendered content · the spec anchors the surface answers to. The completeness
and traces checks (scaffold/guardrails/) read this table; the DOM is the source of truth and
this registry must keep up.

| Surface | Needle | Spec anchors |
|---|---|---|
| readme-opening | There is no CLI. You talk to it | INV-44, INV-82 |
| readme-pipeline | coded until green, and committed with its documents in one change | INV-44 |
| readme-known-issues | Known issues | INV-44 |
| overview-map | the ideas in five minutes | INV-48 |
| work-board | https://happysasha18.github.io/live-spec/board.html | INV-308, INV-309, INV-310, INV-311, INV-312, INV-313, INV-71, INV-67 |

The work board's needle is its own canonical link, `https://happysasha18.github.io/live-spec/board.html`,
so the one identifying line the page leads with names the address the page is read at.
`.github/workflows/pages.yml` is how it gets there: on every push to main it runs this repository's
own `scripts/render-board.sh` against this repository's own checkout and publishes the single
`board.html` that renderer wrote. The page has no second store and no hand upload — one source
file, one link.
