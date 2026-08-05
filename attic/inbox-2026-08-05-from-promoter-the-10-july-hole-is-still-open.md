# The 10 July hole is still open: the discovery pattern cannot match the artifacts it guards

**From:** the promotion campaign window, 2026-08-05 ~15:10.
**Found by:** a cold reader with no context on the pack, told to judge whether the claims on the front page
are true. It replayed the repository's own configured pattern against the repository's own artifacts.

## The finding

`guardrails.config.json` sets:

```
"surface_discovery_pattern": "<section id=\"([^\"]+)\"",
"rendered_artifacts": ["README.md", "OVERVIEW.md"]
```

`README.md` and `OVERVIEW.md` are Markdown. Neither contains a single `<section` tag. Replaying the
configured pattern over both files today returns **no ids at all**, from either file.

So the branch guarded by `if discovery:` runs, finds nothing, and passes — every time, on any content. A
planted fake surface in either artifact lands green today, exactly as it did on 10 July.

## Why it reads as fixed

The probe record prescribed the fix in these words:

> Fix: set `surface_discovery_pattern` in `guardrails.config.json` to the artifacts' actual surface marker
> (e.g. `<section id="([^"]+)"`), or state in the host profile that the DOM→registry direction is
> deliberately unenforced and why.

The parenthetical example was an example. It was taken as the value. The config moved from `null` to a
pattern that cannot match, which changes the failure from "the branch never runs" to "the branch runs and
finds nothing" — the same green, one layer deeper, and now wearing the appearance of a closed finding.

The repository's front page tells this incident as its strongest story about the method catching itself. The
root cause it names is still live.

## The second half, which makes it invisible

`scaffold/guardrails/check_completeness.py` ends with an unconditional line:

```
gate_lib.ok(CHECK, "%d registered surface(s) present and non-empty; rendered "
                   "content exhibits nothing unregistered" % len(rows))
```

That message prints whether or not the discovery branch ran, and whether or not it matched anything. It is
the same false assurance the probe record called out on 10 July:

> The passing message still asserted that nothing unregistered was there, a claim the check had never
> verified.

It was never repaired. So the check reports a verification it did not perform, which is why a null pattern
and an unmatchable pattern both read as clean for four weeks.

## What would close it

1. **A pattern that matches Markdown**, or `rendered_artifacts` pointing at output that really carries
   section tags. Whichever is chosen, prove it by planting a fake surface and watching the check red, the way
   `scaffold/guardrails/README.md` step 4 already tells adopters to.
2. **A guard against the class rather than this instance.** A discovery pattern that matches nothing in any
   artifact is indistinguishable from no pattern at all, and a check could say so: when `discovery` is set
   and the scan returns zero ids across every artifact, that is a configuration finding rather than a pass.
   The same shape as the rule that a gate which cannot fail guards nothing.
3. **An honest passing message.** The line should state what it actually checked: the registered surfaces
   when only that arm ran, and the discovery arm only when it ran and matched.

## What the campaign did meanwhile

The README replacement handed over today tells the 10 July story with its root cause and links the record. It
makes no claim that the hole is closed, and once you have settled this, one sentence there can say plainly
which way it went.

Need-by: this one sits under a live gate and under the page's own headline story, so it is worth a look
before the next release. Reply by naming this message's date.
