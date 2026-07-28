# Glide - agent instructions

Glide is now the public typeface and specimen site repo. The static-to-variable pipeline, CLI, reports, donor imports, and intervention studio live in `/Users/mblode/Code/mblode/static-to-variable`.

## Layout

```
glide/
├── apps/
│   └── web/                         # @glide/web - public marketing + specimen site
├── fonts/                           # Built TTF/WOFF2 files consumed by the site
├── glide-variable.glyphs            # Roman source
├── glide-variable-italic.glyphs     # Italic source
└── glide-mono.glyphs                # Mono source
```

## Run It

```bash
npm run dev      # https://glide.localhost via portless
npm run build    # production Next.js build for apps/web
npm run start    # Next.js production server
```

`npm@12.0.1` is pinned. The web app is a single npm workspace at `apps/web`.

## Boundaries

- Keep this repo focused on `apps/web`, shipped font files in `fonts/`, and root Glyphs sources.
- Do pipeline work in `/Users/mblode/Code/mblode/static-to-variable`, not here.
- Do not regenerate or replace `fonts/*.ttf` or `fonts/web/*.woff2` unless the new artifacts came from the static-to-variable pipeline and were intentionally copied back.
- Do not use `git add -A` at the repo root. Large `.glyphs` files live at the root and are easy to stage accidentally.
- Do not commit files from `broken/`, `.claude/strategy-experiments-*`, `.next/`, `.turbo/`, or editor backup files.

## Web Gotcha

Next.js font loader `next/font/local` requires static literal `src` paths. Do not use template strings or computed paths for local font files.
