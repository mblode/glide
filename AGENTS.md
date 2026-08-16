# Glide agent instructions

Glide is the public typeface, release-asset, and specimen-site repository. Read
[`docs/README.md`](docs/README.md) before changing release files or ownership
boundaries.

## Setup

Use Node 26, npm 12, and Python 3.12 or newer. The fast check uses only the
Python standard library; verification also needs fontTools.

```bash
npm ci
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-release.txt
```

## Commands

```bash
npm run dev          # https://glide.localhost via portless
npm run check        # fast install-documentation contract
npm run verify       # metadata, release mirrors, and production Next build
npm run verify:full  # verify plus a clean deterministic desktop-bundle rebuild
```

Run `npm run check` while editing, `npm run verify` before a pull request, and
`npm run verify:full` before publishing font assets.

## Repository ownership

- `static-to-variable` is the generic static-to-variable conversion engine.
- `static-to-variable-glide` privately reconstructs, tests, and packages Glide.
- `glide` publishes reviewed sources and artifacts and runs the public site.

Do not implement Glide-specific donor or outline logic in this repository, and
do not move product-specific behavior into the generic engine.

## Release contracts

- Treat `fonts/` as the canonical public binaries. Never edit a mirror by hand.
- Promote an entire manifest-approved release from `static-to-variable-glide`;
  do not copy individual TTF, WOFF2, ZIP, or versioned files independently.
- `apps/web/lib/install-snippets.ts` owns install examples. `README.md` is a
  checked mirror because Markdown cannot import the snippets.
- Regenerate `apps/web/lib/charset.ts` and `font-metrics.ts` with
  `python3 scripts/update-font-metadata.py`, then run `npm run verify`.
- Preserve `apps/web/public/3.002/` as the rollback release.
- Stage exact paths. Never use `git add -A`; root Glyphs sources and legacy
  experiment material make broad staging unsafe.

## Web gotchas

- `apps/web/app/layout.tsx` loads the shipping fonts from `apps/web/public/`.
- The app is mounted at `basePath=/glide`; raw image and download paths must use
  `asset()` from `apps/web/lib/config.ts`.
- `next/font/local` requires literal `src` paths. Do not compute font paths.
- Next.js writes the child rules in `apps/web/AGENTS.md`. Keep that generated
  block and read the relevant guide in `node_modules/next/dist/docs/`.
- Do not commit `.next/`, `.turbo/`, `fonts/static/`, editor backups, or new
  `.claude/` experiment output.
