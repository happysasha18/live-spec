# Brief — the photo site's configuration surface (for the tlvphotos window)

*Written 2026-07-27 in the live-spec window at the ROADMAP row 496 build. This window never writes
another project's tree, so this brief is a handover: the pack side landed here, and the deed belongs
to the tlvphotos window. Nothing below is a task for this repo.*

## The rule that now stands in the pack

A project kind whose product is deployed carries one more design principle: the seam between what
ships inside a build and what its owner turns from outside one (SPEC INV-291, ARCHITECTURE's per-kind
design-principles table). An experiment switch, a piece of copy, a threshold or budget, and a feature
toggle reach production by a deploy of configuration alone; behaviour and structure stay in the code
the build ships.

The founding records the seam once, on a `project.config-surface` line in the host profile, beside
`project.kind`, `project.layers`, `project.proofs`, `project.design-principles`, and `project.axes`.
`guardrails/check-config-surface.py` reads that profile and reports a kind recorded with no
declaration, a declaration with no words, and a "none" written beside a `project.layers` line that
names a deployment layer. The photo site's layers already name deployment, so a "none" there reds.

**The placement test**, applied one thing at a time: does the shipped page already know how to behave
once this value changes? A value the running page already reads belongs to the configuration; a
change that needs the code to do something it does not do today belongs to the build. A string baked
into the page at build time belongs to the build until that reading moves to load time.

## What the photo-site window owes

1. **Answer the founding question** in `<tlvphotos>/.live-spec/profile.md`, on one
   `project.config-surface` line: what its owner turns without a build, where those values live, and
   how a change of them reaches production. The window also bumps its `founding.set-version` to 6,
   the set version that carries this question (`scripts/founding-questions.json` in the pack).

2. **Take the check.** Copy `guardrails/check-config-surface.py` and `guardrails/config-surface.json`
   from the pack into the host tree at its catch-up walk, and run it against the host profile. The
   check reads keys and word lists from its config, so a host that names its layers differently tunes
   the config rather than the code.

3. **Make the seam real for the experiment switch.** Today switching the experiment off costs a full
   build. The work is to move the switch's value out of the built page and into a file the deployed
   page reads, so turning it off is an edit to that file and a deploy of configuration alone. The
   page's behaviour under both settings stays in code, as it is today; only the value moves.

4. **The proof by deed.** The owner turns the experiment off in production and no build runs. That
   run is the row's first proof by deed, and it belongs to the tlvphotos window — the record of it
   goes in that project's journal, and one line comes back to the pack through the inbox so row 496
   can close its last leg.

## What stays open in the pack

The pack side is complete without the deed: the principle, the check, the founding question, and the
documents. Row 496's closing leg — one host changing a switch and a text in production with no build
— waits on the tlvphotos window and on the owner's own run.
