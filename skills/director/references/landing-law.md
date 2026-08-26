# Landing law — what a change owes on its way to shared truth

The pointer referenced from `SKILL.md`'s Execution section. These are the facts build-pipeline's
old fixed nine-step sequence carried as its own steps' law; they hold regardless of which
specialist or gate performs the step, so they moved here rather than into any one specialist's
own file.

**The bug door's spec-backed-literal tripwire (SPEC INV-104).** The tripwire asks: does this edit
touch a spec-backed literal or clause — a version string, a pinned count, a named vocabulary, a
promised wording? A yes binds two rules into one duty: the docs-travel-with-the-change rule, and
the red-first small-fix path. Under that duty the docs and the test land in the same session as
the fix. The tripwire reads the edit's content, so a one-word change to a spec-cited literal owes
the same duty as a full feature.

**A rewrite or restyle accounts for every removal of substance (SPEC INV-109).** The rule's one
home is communicator rule 6, the removal-accounting step of that skill's writing-register
checklist. That step owns the delivery report the accounting rides. Every removed section,
argument, rationale, or worked example is listed there with its one line of judgment. A removal
the rewriter cannot justify is raised as a question before the report closes.

**A restructure or migration merged back to main is gated on the delta (SPEC INV-114).** A
restructure or migration merge gate judges the delta. It has three parts. The first is
load-bearing token identity old-versus-new, modulo the per-chunk named deltas, plus the
punctuation-multiset check (SPEC INV-111). The second is the full suite green on the merged tree
(SPEC INV-39). The third is a full prover pass on both sides, whose blocking set is delta-scoped.
That set is an unmatched token, a red suite, a new-side finding absent on the old side, or an
unnamed meaning change. Pre-existing findings equal on both sides route to queue rows in the same
landing and never block. And a session that sharpens a human's spoken bar beyond his words says
the sharpened form back and marks it as its own interpretation. The token-identity part scopes to
a content-preserving restructure; a deliberate redesign routes by the architecture-redesign law
(SPEC INV-113) instead, its merge standing on the green suite and the delta-scoped prover pass
with no token-identity demand over text the redesign meant to change.

**A same-version docs-layout pass rides one sanctioned light vehicle (SPEC INV-111).** The pass
builds on a clean pushed base, and locks the owner's decisions in a checkpoint first. It proves
content survived by a word-token multiset check and a punctuation multiset check.

**Compaction runs every pass, above the milestone gate (SPEC INV-164).** The doc- and
code-compaction stations run at every push, above the MINOR gate that once held them alone. Every
push is held to the reached-clean floor by the mechanical gates — the register lint at zero
errors, the redundancy gate at zero open pairs, and the debt cap that only ratchets down
(`scripts/spec-debt-cap.json`). The suite asserts them against the live document, so no bloat
accumulates between milestones.

**The authoring seat never certifies its own work adversarially (SPEC INV-237).** The freshness
gate above is the whole rule, and the release pass may not waive it. A release's adversarial pass
is the full re-prove at the release gate, authored by a fresh seat, never the seat that authored
the change. A newly added lens or rule is run against the very document that introduces it before
release (self-application), and the release record names the result. A release gate may require a
dated clean-context review record naming a seat other than the release's. The mechanical floor
checks that the record exists, is release-dated, and names a different seat; the rest is a
discipline the seat holds.

**The release tier is a stated judgment, held by no gate (SPEC INV-217).** Bump the
version, PATCH by default. The number reports what taking the release costs a host, and the tier
is read off that cost. A patch fixes a machine to hold a law already stated, and the host does
nothing. A minor grows what a host may adopt by re-running its catch-up walk with nothing
rewritten. A major forces a host action and ships its dated MIGRATION.md chapter. The
minor-versus-major call is a stated judgment the releasing session makes and names.

**A substantive skill change earns a skill-creator review before it ships (SPEC INV-208, gate
s).** A push that meaningfully changes a skill under `skills/` needs a committed record under
`docs/skill-review/`. That record names the skill and carries a `SKILL-REVIEW` marker with a
`Verdict:` line, at least as new as the skill's own last change. `guardrails/check-skill-review.sh`
reds a push that lacks one.
