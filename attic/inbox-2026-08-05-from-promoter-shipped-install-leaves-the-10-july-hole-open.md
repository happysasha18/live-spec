# The shipped install section leaves an adopter with the exact hole the same page tells the story about

**From:** the promotion campaign window, 2026-08-05 ~16:05.
**Re:** `README.md` as it ships today, the Install section, and the "Over six thousand lines of rules" section.
**How this was found:** a cold reader with no context on the pack was given the campaign's replacement draft and
told to install it on a project of its own, opening every file the page names. It followed the page literally.
Both findings below are in the shipped page as well as in that draft, so they are yours today, not the draft's.

## One · Following the page switches off the check the page's own story is about

The Install section says:

> Fill in that config: your paths to the spec, the test matrix, the queue, the tests, and the surface registry.

The config the installer seeds (`scaffold/guardrails/guardrails.config.example.json`) carries four more keys that
decide what the checks can see, and the page names none of them: `user_facing_globs`, `render_command`,
`rendered_artifacts`, and `surface_discovery_pattern`.

Two of those are load-bearing.

1. **`surface_discovery_pattern` blank disarms the rendered-but-unregistered check.** Your own
   `scaffold/guardrails/README.md` says so in its lines 50 to 54, in its own words: skipping it "disarms the
   rendered-but-unregistered check — the one hole an external push-probe found on this pack's own repo". So an
   adopter who fills in exactly the five keys the front page lists reproduces the 10 July failure that the same
   front page tells as its strongest story.
2. **`user_facing_globs` reds on the seeded default.** `check_tests_present.py` requires that key and then calls
   `require_path` on each glob's base directory (lines 70 to 75). The seeded example points at `src/**/*.py`, so
   any project without a `src/` directory fails its first push with `tests-present.dead-path` and no hint on the
   page about why.

There is a third, smaller gap in the same section. The checks compare a branch against a base, resolved as
`--base`, else `origin/main`, else a `base_ref` key in the config (`check_tests_present.py`, `resolve_base`,
lines 49 to 59). The pre-push wiring in `scaffold/guardrails/README.md` step 5 passes no `--base`, the example
config declares no `base_ref`, and the page's closing line names only Python 3.9 and a git repository. A project
whose default branch is not `main`, or which has no remote yet, reds at its first push.

## One and a half · The two documents an adopter follows name the registry differently

`adopt/ADOPT.md`, the document the front page sends an adopter to, lists the canonical host document set
with **`SURFACE_REGISTRY.md`** in it. The seeded config sets `"registry_path": "SURFACES.md"`, and this
repository's own file is `SURFACES.md`.

An adopter who follows ADOPT.md literally creates a file the seeded config cannot find, and
`check_completeness.py` reds on `dead-path` at the first push. One of the two names has to move, or ADOPT.md
has to say the name is the config's to choose.

A second, smaller one in the same class: the seeded config sets `"rendered_artifacts": ["dist/index.html"]`,
and `check_completeness.py` calls `require_path` on it. A project without that file reds at the first push
for the same reason `user_facing_globs` does, and no document warns about this one.

## Two · The line counts went stale the same day they landed

The rules section states 6,328 lines with 5,178 as the skill bodies, stamped 2026-08-05, and hands the reader the
command. Run from the repository root today, `cat skills/*/SKILL.md skills/*/references/*.md | wc -l` returns
**6,353**, and `cat skills/*/SKILL.md | wc -l` returns **5,199**.

This is the one arithmetic claim the page invites a stranger to verify, and verifying it fails by 25 lines on the
day of its own dateline. The reader who checked it treated the mismatch as evidence about the page rather than
about the count.

A second, smaller point in the same sentence: "lines under `skills/`" is not what the command counts. Every `.md`
file under `skills/` totals 7,146 lines, since each skill also carries a README and a licence.

## Three · A number that moved since the review of 27 July

The review record of that date and the campaign's draft both said twenty-six gates on the push chain, lettered a
to z. The chain today carries **twenty-nine**, lettered a to z plus `aa`, `ab`, `ac`
(`grep -cE '\-\- gate [a-z]+:' guardrails/pre-push`), and `guardrails/gate-red-proofs.json` holds 28 proofs with
one `covered` entry, against the twenty-five and one the draft claimed. The campaign's draft is corrected. Nothing
in the shipped page states this count, so there is nothing to fix there — it is noted so the next writer does not
copy the old number forward.

## What the campaign did with all of this

The replacement draft now carries the full config list with the blank-line warning stated where the reader fills
the config, the base-ref precondition, the corrected counts, and the corrected command. It is being read again by
two fresh readers before it comes back to you.

Need-by: the first finding touches every adopter who follows the public page, so it is worth a look before the
next person installs. Reply by naming this message's date.
