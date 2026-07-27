# Finding: the legibility lint pairs every colour with the PAGE background, never the ancestor's

**From:** the tlvphotos window, 2026-07-27. Found while clearing the pre-show gate on a decision page
before showing it to Alexander.

## What happened

`scripts/preshow-legibility-lint.py` blocked a decision page with seven `low-contrast` hits. All seven
were false. The page is a dark surface (`#12131a`) that carries several deliberately LIGHT cards inside
it — mock-ups of how a link unfurls in Telegram, WhatsApp and Google, each with its own light
background. The lint paired every foreground colour with the page background rather than with the
nearest ancestor that actually paints one, so a near-black caption sitting on white read as
"`#4d5156` on `#12131a`, ratio 2.3:1".

Measured in a real browser, walking up from each element to the first ancestor with a non-transparent
`background-color`, those same seven selectors read 4.65 to 12.43 — every one of them above the floor.

## The part that matters more

The same run MISSED two genuine failures the lint never named:

| selector | lint's verdict | measured against the real ancestor |
|---|---|---|
| `.tg-site` | not reported | **3.34:1** — below the floor |
| `.wa-host` | reported at 3.8:1 (wrong pair) | **4.43:1** — below the floor, by a different margin |

So the gate was wrong in both directions at once: it blocked seven passing rows and let one failing row
through unnamed. A gate that reports the wrong pairs teaches its user to skip it, which is the worse
outcome — the next real hit gets waved past with the false ones.

## The fix, as far as this window can see it

Resolve each element's effective background by walking ancestors until a non-transparent
`background-color` is found, falling back to the page background only when the walk reaches the root.
The check itself is a few lines; the measurement script this window used is below and can be lifted
whole.

```js
const bgOf = el => { let n = el;
  while (n) { const b = getComputedStyle(n).backgroundColor;
    if (b && !/rgba\(0, 0, 0, 0\)|transparent/.test(b)) return rgb(b); n = n.parentElement; }
  return PAGE_BG; };
```

Two caveats this window hit and could not settle from outside the pack: a static CSS reader cannot know
the DOM nesting, so either the lint drives a browser (as the measurement above does) or it reasons over
the selector prefixes it can see (`.gg .cap` under `.gg { background:#fff }` is resolvable that way;
`.wa-host` under `.wa-body` is not, since the rule sits on a sibling class). A browser-driven check is
the one that cannot be fooled.

## Not blocking anything here

The tlvphotos page shipped after the two real hits were fixed by measurement. This deposit carries the
finding only; no action is owed back to this window.
