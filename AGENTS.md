# Glide — agent instructions

Variable typeface shop. Two axes of work: (1) the font itself (`*.glyphs` sources → variable TTFs), (2) the web tooling around it (Next.js apps + Python renderers).

## Layout

```
glide/
├── apps/
│   ├── web/            # @glide/web — public marketing + specimen site
│   └── glyph-forge/    # @glide/glyph-forge — internal audit UI for broken glyphs
├── packages/
│   ├── variable-gen/   # @glide/variable-gen — Python static→variable repair engine
│   └── glyph-forge/    # @glide/glyph-forge-engine — Python SVG renderer + manifest for apps/glyph-forge
├── cabinet/            # Donor OTFs (Circular/, Circular Italic/, Circular Mono/) + build scripts
├── fonts/              # Built variable TTFs (glide-variable.ttf, glide-variable-italic.ttf) + /web/ WOFF2
├── docs/               # Plans, PRDs, technical specs
├── .venv/              # Python 3.14 — fontTools, glyphsLib, ufoLib2
├── glide-variable.glyphs         # Roman source (3 masters: Thin 100 / Regular 400 / ExtraBlack 950)
├── glide-variable-italic.glyphs  # Italic source (3 masters: same axis stops)
└── glide-mono.glyphs             # Mono source
```

Monorepo = npm workspaces + Turbo 2. `npm@10.9.2` pinned.

## Run it

```bash
turbo dev                                       # both apps, via portless
turbo dev --filter=@glide/web                   # https://glide.localhost
turbo dev --filter=@glide/glyph-forge           # https://forge.localhost
npm run build:fonts                             # copy built TTFs → fonts/web/ WOFF2
npm run forge:build                             # rebuild glyph SVG cache + manifest
```

Both apps go through **portless** (global) — no manual port management, HTTPS by default, `.localhost` names auto-resolve on macOS (for Safari, run `portless hosts sync` once). If the cert prompt was dismissed, re-run `portless trust`.

Python entry points always run through the venv, not the user's global Python:

```bash
.venv/bin/python packages/variable-gen/scripts/audit_variable_font.py --family all
.venv/bin/python packages/variable-gen/scripts/repair_circular_sources.py --font italic
.venv/bin/python packages/glyph-forge/python/build_cache.py
```

## Gotchas

- **Circular donor paths contain a space**: `cabinet/Circular/Circular Italic/`. Quote in shell; use `pathlib` or `os.path.join` in Python.
- **glyphsLib mis-maps the wght axis**: min=max=default=400 with a broken `avar`. Always run through `cabinet/export_designspace.py` — it re-infers the axis from master locations.
- **fontmake skia backend corrupts some dollars/cents** (qcurve nodes). Use `--output-format variable-cff2 --overlap-removal-backend pathops`.
- **cu2qu shuffles TrueType contour start points** across masters. `cabinet/fix_ttf_startpoints.py` realigns them post-build — don't skip it.
- **Source normalization is authoritative**: edits to `glide-variable*.glyphs` take precedence over UFO checkpoints in `master_ufo/`.
- **Next.js font loader `next/font/local` src must be a static literal** (learned the hard way — see commit `fec4c30`). No template strings, no computed paths.

## Do-not

- Do not edit `packages/variable-gen/` from a `glyph-forge` task. The repair engine and the audit UI are deliberately separate. `glyph-forge` *reads* `variable-gen`'s reports; never writes to them.
- Do not commit files from `/broken/` (debugging screenshots) or `.claude/strategy-experiments-*` (historical iterations) — both are local only.
- Do not regenerate built fonts (`fonts/*.ttf`) without re-running the full `cabinet/` pipeline; they are built artifacts with verified interpolation.
- Do not use `git add -A` at repo root. Large `.glyphs` files live at the root and are easy to accidentally blow away.

## Reports to read before proposing changes

- `packages/variable-gen/reports/audit/audit-overview.md` — current state of roman + italic
- `packages/variable-gen/reports/audit/{roman,italic}/*-variable-audit.md` — per-family risk
- `packages/variable-gen/reports/repair/review-packet.md` — glyphs still needing manual cleanup
- `packages/variable-gen/manifests/circular-triage.json` — authoritative repair strategy per glyph

## Available Context

Additional context is available in the files below. Consult the relevant file when working in a related area — see each description for scope.

- `.claude/knowledge/architecture-boundaries.md` — TTF subset vs full build, Circular weight mapping, Next.js 16 Turbopack server/client split, glyph-forge data flow, score band thresholds.
- `.claude/knowledge/incident-troubleshooting.md` — Roman variable-build blockers (`emacron` / `gdotaccent` / `uni021B`), fontmake/cu2qu error surfaces, `--skip-import` workflow, solver projection hit rate, safe bulk-triage playbook.
- `/Users/mblode/.claude/projects/-Users-mblode-Code-mblode-glide/memory/project_font_build.md` — Variable font build pipeline: how to rebuild TTFs from `.glyphs` source using fontmake, interpolation fixes, start-point alignment, known issues.
