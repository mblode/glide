# @glide/glyph-forge-engine

SVG renderer + broken-glyph manifest that backs the `@glide/glyph-forge` Next.js audit UI.

Read-only relationship with `@glide/variable-gen`: ingests its audit JSON reports, never writes to them.

## Run

```bash
npm run ingest   # variable-gen audit JSONs + seed lists → manifests/broken-glyphs.json
npm run cache    # bulk render every (glyph × weight × source) to public-cache/svg/
npm run build    # both, in order
```

Single-glyph render for debugging:

```bash
../../.venv/bin/python python/render_glyph.py \
  --family italic --glyph agrave.ss02 --weight 500 --source glide
```

## Outputs

- `manifests/broken-glyphs.json` — union of audit-flagged + user-seed glyphs with verdict + strategy cross-ref
- `public-cache/svg/{family}/{glyph}/{weight}-{source}.svg` — per-cell outlines (8 donor weights × 2 sources)

`apps/glyph-forge`'s `scripts/sync-cache.ts` copies both into its `public/` at dev/build time.

## Weight mapping

Uses Circular donor's native 8 weights (read from each OTF's `OS/2.usWeightClass` at ingest time):

| Circular name | wght value |
|---|---|
| Thin        | 250 |
| Light       | 300 |
| Regular     | 400 |
| Book        | 450 |
| Medium      | 500 |
| Bold        | 700 |
| Black       | 900 |
| ExtraBlack  | 950 |

Glide is instanced at those same values for 1:1 apples-to-apples comparison.
