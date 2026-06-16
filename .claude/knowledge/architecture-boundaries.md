# Architecture & System Boundaries

## Which TTF to use for audit

- `fonts/*.ttf` — **subset** shipped to customers (~472 glyphs). Do not use for audit/scoring: it's missing `Amacron`, `Abreve`, `Aogonek`, most `Edotaccent`, etc.
- `packages/variable-gen/build/{roman,italic}/glide-variable{,-italic}-vf.ttf` — **full** 744-glyph build. Use this for any glyph-forge / scoring / rendering work.

`packages/glyph-forge/python/shared.py` points at the full build for this reason — don't "fix" it back to `fonts/`.

## Circular donor weight mapping

`usWeightClass` read from each OTF's `OS/2` table. Note the inversion at Regular ↔ Book:

| Circular style  | wght |
|-----------------|------|
| Thin            | 250  |
| Light           | 300  |
| **Regular**     | **400** |
| **Book**        | **450** |
| Medium          | 500  |
| Bold            | 700  |
| Black           | 900  |
| ExtraBlack      | 950  |

Regular is lighter than Book. Hardcoded in `packages/glyph-forge/src/types.ts` and `shared.py`; keep them in sync.

## Next.js 16 Turbopack gotcha

Turbopack cannot chunk `node:fs`/`node:path`/other built-in modules when a file is imported by a client component, even transitively. The error: `the chunking context (unknown) does not support external modules (request: node:fs/promises)`.

Fix: keep `node:*` imports in `*.server.ts` files and import `"server-only"` at the top. Client-safe helpers stay in `lib/data.ts`, server loaders stay in `lib/data.server.ts`. Never import `.server.ts` from a component marked `"use client"`.

## glyph-forge data flow

```
packages/variable-gen/reports/audit/*.json
  + packages/variable-gen/manifests/circular-triage.json
  + shared.py ITALIC_SEED / ROMAN_SEED
       │
       ▼  ingest_audit_reports.py
  packages/glyph-forge/manifests/broken-glyphs.json  (1,465 glyphs)
       │
       ▼  build_cache.py                             (~14s, 23k SVGs)
  packages/glyph-forge/public-cache/svg/
       │
       ▼  build_scores.py                            (~19s, 11k cell scores)
  packages/glyph-forge/manifests/{cell,glyph}-scores.json
       │
       ▼  recommend_strategy.py                      (heuristic)
  packages/glyph-forge/manifests/strategy-suggestions.json
       │
       ▼  apps/glyph-forge/scripts/sync-cache.ts     (predev/prebuild)
  apps/glyph-forge/public/{svg/, broken-glyphs.json, cell-scores.json, glyph-scores.json, strategy-suggestions.json}
```

Full rebuild: `npm run forge:build` from repo root. Idempotent — only re-renders missing SVGs.

## Score band thresholds

Set in `packages/glyph-forge/src/types.ts` (`scoreBand()`): `< 0.3` red, `0.3–0.7` amber, `≥ 0.7` green. Changing the bands requires re-syncing the UI; no Python change needed since scores are stored as raw floats.
