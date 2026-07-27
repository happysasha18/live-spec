# The seam between the build and the configuration (INV-291)

*Written 2026-07-27 at the ROADMAP row 496 build. The normative homes are PRODUCT_SPEC.md
Requirement 299, the per-kind design-principles table in ARCHITECTURE.md, and
`guardrails/check-config-surface.py`; this note records the design and the reasons behind it.*

## What the owner asked

On 2026-07-27 at about 15:00 Alexander asked first whether the design principles are split by front
and back, and then for parametrization: today, to switch an experiment off on his photo site he has
to run a full build, and by his design anything that can be changed without a big build should be
easy to change and deploy — a parameter, a text, an experiment switch, and the rest by our own
judgment.

The answer to his first question is that the principles are split by project kind, not by front and
back. A backend carries the same seam a frontend does: a rate limit, a feature flag, and an error
budget are values an owner turns without rebuilding a service. So the principle this note designs
enters the per-kind table for every deployed kind, and the front-and-back split stays out of it.

## The two sides, in plain words

**The build side** holds the behaviour and the structure — everything that reaches production only
by building the product again.

**The configuration side** holds the values the shipped product already reads: an experiment switch,
a piece of copy, a threshold or budget, a feature toggle. A change to one of them reaches production
by a deploy of configuration alone.

**The test a reader applies to place one thing.** Does the shipped product already know how to behave
once this value changes? If the running code already reads the value and already carries both
behaviours, the thing sits on the configuration side. If the change needs the code to do something it
does not do today — a new branch, a new element, a new call — it sits on the build side. One
corollary settles the case that looks like configuration and behaves like code: a value the product
reads at build time stays on the build side until that reading moves to run time. A string baked into
a page at build time is code by this test, however much it looks like a setting.

## Which kinds count as deployed

A kind is deployed when its product runs where its readers reach it and reads values it did not have
to be rebuilt to receive. By that reading the static-site, fullstack, photo-portfolio, and backend
kinds are deployed, and a book, a prose campaign, a CLI, and a skill pack are not.

The two edges are worth stating, because they are where the boundary earns its keep.

- **A CLI carries configuration files, and it is still not deployed.** Those files sit on the
  reader's machine. Its owner turns nothing in them without shipping a release the reader installs,
  so there is no place the owner alone deploys to.
- **A skill pack and a book publish, and publishing is not deploying.** Their product is the text
  itself; nothing of theirs runs somewhere reading a value. A change reaches the reader as a new
  copy of the text.

**How a check reads the boundary without holding a list of kinds.** The classification is a judgment,
and its home is the per-kind design-principles table in ARCHITECTURE.md, which a founding reads and
answers from. The founding asks every host, whatever its kind, and the host answers on one profile
line; a project that deploys nothing answers an explicit "none". So the check needs no list of kinds
in its code — it reads the host's own declaration, exactly as the composition-axes check does with
"none beyond the C-1 floor" [INV-244]. A list of kinds inside check code would be the literal-list
design the base rulebook already names as the wrong answer to a class.

## Where a host declares it

The host profile, on a `project.config-surface` line, beside `project.kind`, `project.layers`,
`project.proofs`, `project.design-principles`, and `project.axes`. No second home is opened. The
founding-question set `scripts/founding-questions.json` gains the question at set version 6, so the
update check names it to any host that founded on an older set [INV-227], and adoption's orient
records the answer like every other founding line.

The declaration names three things: what may be turned, where those values live, and how a change of
them reaches production.

## What the check reads, and what it reports

`guardrails/check-config-surface.py` opens two files — the host profile named on its command line
and its config `guardrails/config-surface.json` — and inside the profile it reads three records:
`project.kind`, `project.layers`, and `project.config-surface`. Its green line states that reach.

Three arms:

1. **silence** — a profile records a kind and carries no `project.config-surface` record. The red
   names the missing line and says what to write.
2. **empty** — the record exists with no words after its key.
3. **contradiction** — the declaration answers "none" while the host's own `project.layers` line
   names a deployment layer. The two declarations of one host disagree, and the red quotes both.

The third arm is where the check gets teeth past presence: a founding cannot clear the gate by
writing "none" over a project that plainly deploys. Both word lists — the "none" openers and the
deploy words — live in the config, so they grow without a code edit.

**What the check does not hold, said rather than skipped in silence:** whether a declared value truly
reaches production with no build. No script reads a host's deploy pipeline out of one profile line.
That half belongs to the founding conversation and to the proof by deed — the owner turns a switch in
production and no build runs.

**Standing.** The check rides the suite and stays off the push chain, the standing
`guardrails/check-wrong-referral.py` already carries [INV-225]. live-spec ships no deployed product
of its own, so the gate has host profiles to read and no push of this repo to block.
