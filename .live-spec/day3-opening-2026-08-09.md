# Day 3 opening — the install defect is narrower than the audit stated

Root: his order of 2026-08-08 22:17, and the plan's day 3, which fixes the install from the ready
list. The ready list is the day 1 delivery census, `.live-spec/day1-census-delivery.md`. Written
2026-08-09, 04:54, on commit `3b9bdd6`.

## What the census counted

A person who clones this repository and runs `./install.sh` receives the ten skill folders. A second
script, which the readme's own walkthrough never names, adds sixteen hook files. In that home, 33 of
the 66 installed files carry 219 references to files the install never placed.

The census sorted all 123 distinct missing targets into three classes. 96 are real files sitting in
this repository, which the two installers never copy. 19 are the generic names of documents that a
host project writes when the pack attaches to it, so no file could satisfy them in a bare home. 8
name things the pack deliberately leaves alone, such as the person's own root configuration.

## What the readme already says, and why it changes the repair

The readme states the two install paths plainly. The plugin install puts the whole tree under
`~/.claude/plugins/cache/`. The `install.sh` path carries skill files alone, and the readme then
tells the reader to clone this repository and run `adopt/install-scaffold.sh` from their project's
root for the push gate.

So the 96 references of the first class resolve for a person who followed the readme to its end. The
census measured the shorter path, which the readme itself calls incomplete.

The audit of 2026-08-08 stated 183 dangling references that no gate can see, and it named that the
one breakage a person outside this project meets. Measured against the documented complete path,
that number is materially softer. The measure stands as a number about the short path.

## What stays a real defect

**A path in a skill body never says which tree it lives in.** The rulebook carries a section
explaining that paths resolve in two trees, the pack's own and the host project's. The other nine
skills carry no such section, and they name paths such as `scripts/spec-style-lint.py` and
`guardrails/check-worker-restore.py` with nothing to locate them by. A person reading
`skills/text-audit/SKILL.md` alone meets thirty such paths.

**The readme's shortest path leaves a person without the machinery.** The two lines a reader meets
first are the plugin install. The clone and the scaffold install sit further down, past the setup
walk. A person who stops after `./install.sh` has skills that name tools they do not have.

**The claim about the plugin path is unverified here.** No live-spec plugin is installed on this
machine, and `~/.claude/plugins/cache/` holds one unrelated plugin. The readme's sentence about the
whole tree is therefore a claim this seat cannot check without installing the plugin into his own
setup.

## The repair, and the one fork that is his

The repair has two halves, and the first is this seat's.

Each of the nine working skills gains the same locating sentence the rulebook already carries, so
every path it names says which tree it resolves in. The 19 host-project names gain the same
treatment, since a reader meeting `PRODUCT_SPEC.md` in a skill body should read it as their own
project's file. This is a wording change across shipped skill bodies, and it carries a skill-creator
review under the standing gate.

The fork is his, because it decides what the product is. Verifying the plugin path means installing
the live-spec plugin into his own Claude Code setup, which changes what his sessions load. My
recommendation: verify it, since the readme's first two lines rest on that claim and a stranger meets
them first. A second route leaves the claim unverified and softens the readme's wording instead.

## What day 3 must move

Day 3 declares the install measure. Today it reads 218 references pointing at nothing on the short
path: day 1 counted 219, and row 2.2's removal took one of them with the check it retired. The
measure moves when a skill body's paths each say where they live, and the count is re-taken by the
same census method.
