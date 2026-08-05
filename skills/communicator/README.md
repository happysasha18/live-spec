# communicator

A small skill for one thing: **showing work to a human and asking for decisions they can actually make.**

It works on the exchange with a human. Code is a separate concern. The same failure keeps happening in agent work — describing in words
what should be shown with the eyes, and asking a person to decide in units they don't think in (pixels, dB,
model weights, internal ids). `communicator` is the antidote, written as twenty-two rules gathered into
six areas.

It is the presentation member of the live-spec pack, which ships eleven skills. The four its rules
touch most often:

| skill | job |
|---|---|
| live-spec-base | hold the shared rules and the settings ladder |
| spec-author | write the spec |
| product-prover | review the spec |
| **communicator** | **make the human-facing exchange land** |

## When it fires

Every time you (a) need the human to **decide** something — especially anything visual or textual, (b) report a
**result or progress**, or (c) **name a problem**. Rule of thumb: if your next sentence is a question the person
can't answer without seeing something, stop and show it.

## Seven of the twenty-two rules (short)

1. **Show, don't describe** — and when unsure, ask by showing (a mockup), never in raw units or a bare term.
2. Name a problem → make it **actionable in the same breath, with your recommended pick**.
3. **Show proactively, for approval** — the moment there's a real was → became, don't wait to be asked.
4. Don't fragment attention — **batch, show once, in one window** (was → became → why → before/after).
5. Put the artifact **where they'll actually see it** (browser or inline) — real data, never a path.
6. **Plain language, in the product's own words** — use-cases over mechanism, one name per thing, the spec's vocabulary.
7. **Honest about the result** — small is not a win; and don't escalate what you can decide yourself.

The other fifteen cover narration while work runs, the away-stretch, decision pages, the feature map,
and how the person's word is held once given. Full text is in [`SKILL.md`](./SKILL.md).

## Install

Drop the whole folder into your skills directory (for example `~/.claude/skills/communicator/`). It is
`SKILL.md` plus four files under `references/`, which the body loads on demand. They are `words.md`,
`field-examples.md`, `page-lifecycle.md`, and `writing-register.md`. The body sends a reader to
`words.md` first. There is no code to build.

## License

MIT.
