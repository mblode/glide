# Incident Troubleshooting

## The roman variable build is brittle

Running `packages/variable-gen/scripts/repair_circular_sources.py --font roman` on head fails at the fontmake compile step unless you isolate three blocker glyphs first. The failure mode is always the same cu2qu error:

```
ERROR:fontTools.cu2qu.ufo:Glyphs named 'emacron' have incompatible segment types
ERROR:fontTools.cu2qu.ufo:Glyphs named 'gdotaccent' have incompatible segment types
ERROR:fontTools.cu2qu.ufo:Glyphs named 'uni021B' have different number of segments
```

- `emacron` + `gdotaccent`: brace layer at wght 675 has curve↔line type flips vs the main masters
- `uni021B`: Thin has 1 path where Regular / ExtraBlack have 2 paths

**Fix before any repair run**: `npm --workspace @glide/glyph-forge-engine run isolate-blockers`. This strips the bad brace layers, flattens all three masters to the Regular outline for those three glyphs, and sets their triage strategy to `reference_fallback`. The glyphs end up visually static across weights (unavoidable regression on their interior weights) but the whole font compiles.

## fontmake's `--no-check-compatibility` doesn't suppress cu2qu errors

The flag only skips fontmake's own post-build validation. cu2qu still refuses to convert cubic→quadratic if it produces different segment counts per master. When `repair_circular_sources.py` fails at the `build_variable_font` step, its `subprocess.run(..., capture_output=True)` swallows the real error. To see it, rerun fontmake directly:

```bash
.venv/bin/fontmake -m master_ufo/Glide.designspace -o variable --keep-overlaps \
  --output-path /tmp/x.ttf --no-check-compatibility 2>&1 | grep ERROR
```

## `--skip-import` preserves local .glyphs edits

The default repair pipeline re-imports Circular donor outlines, overwriting any manual flattening or hand-cleanup. Use `repair_circular_sources.py --font roman --skip-import` when you want your current `.glyphs` state to survive the strategy-application pass.

## Strategy downgrades cascade-break neighbouring glyphs

Replacing a comprehensive triage strategy with a lighter one (`structural_fallback → weighted_fallback`, `inherit_base_contours → donor_copy`) can introduce topology mismatches in glyphs that weren't in the replacement set. First real run of `bulk_stage.py` without `--no-downgrade` broke `gdotaccent` and `emacron` as collateral damage from overriding `uni021B`'s strategy.

Always run `bulk_stage.py` with `--no-downgrade`; the rigour ordering is in that script.

## Solver projections are hints, not contracts

Raster-space simulation under-predicts what happens in vector interpolation, especially for `.ss08` variants with complex topology cascades. Measured reality from one end-to-end run:

- Projected: 30 glyphs gaining > 0.1, 9 reaching green
- Delivered: 5 gaining > 0.05, 2 reaching green (`m.ordn`, `m.ordn.ss08`)
- 3 projected gainers regressed to 0.04 instead (need manual triage edit reversal)

When a bulk apply regresses specific glyphs, the fix is to delete only those entries from `circular-triage.json` and rerun with `--skip-import`. The `.bak` files `isolate_blockers.py` writes cover the full-revert path.

## Safe order of operations for any triage work

1. `npm run isolate-blockers` (if not already run on this source)
2. `bulk-stage --no-downgrade` your proposed edits
3. Review on `/triage` in the UI
4. `npm run apply` — writes to `circular-triage.json`, creates `.json.bak`
5. `repair_circular_sources.py --font roman --skip-import`
6. Rerun fontmake directly if the repair's subprocess error is opaque
7. `npm run forge:build` to re-score; compare to the snapshot you took in step 0
8. If specific glyphs regressed, edit `circular-triage.json` to drop just those entries and repeat from step 5

## Snapshot before any bulk run

```bash
cp packages/glyph-forge/manifests/glyph-scores.json /tmp/glyph-scores.before.json
cp packages/variable-gen/manifests/circular-triage.json /tmp/circular-triage.before.json
```

These are what you diff against after the repair to measure real gains vs projections. Trust the diff over the solver's projected column.
