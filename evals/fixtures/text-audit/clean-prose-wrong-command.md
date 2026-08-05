# Rebuild the code-to-location table

The code-to-location table maps every bracket code in the spec body to the place that code stands.
A person rebuilds it after editing the spec, so the table and the body agree again.

From the root of the live-spec repository, run
`python3 scripts/build-index.py PRODUCT_SPEC.md PRODUCT_SPEC.index.json`. The command rewrites the
table and leaves `PRODUCT_SPEC.md` unchanged.

Then run `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.json`. It
reports that the committed table matches a fresh build.
