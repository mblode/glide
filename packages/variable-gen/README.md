# variable-gen

`variable-gen` is now the working home for the reusable static-to-variable font
repair pipeline used for Glide + Circular.

Docs:

- [Research](../../docs/variable-gen-research.md)
- [PRD](../../docs/prd.md)
- [Execution plan](../../docs/variable-gen-plan.md)
- [Technical spec](../../docs/variable-gen-technical-spec.md)

## Current scope

The package now contains a manifest-driven repair runner that can:

- re-import Circular donor statics into the live `.glyphs` sources
- apply per-glyph repair strategies from a manifest
- rebuild empty `.notdef` glyphs
- normalize path order, start points, and winding direction
- export UFO/designspace checkpoints
- build variable TTFs
- generate sampled static instances
- validate exact-master instances against donor statics
- produce ranked source-risk and instance-risk reports
- generate a review packet for manual cleanup

## Primary entry point

Run the full repair pipeline for both live sources:

```bash
.venv/bin/python packages/variable-gen/scripts/repair_circular_sources.py --font all
```

Run only one family:

```bash
.venv/bin/python packages/variable-gen/scripts/repair_circular_sources.py --font roman
.venv/bin/python packages/variable-gen/scripts/repair_circular_sources.py --font italic
```

Important outputs:

- Repair manifest:
  - `packages/variable-gen/manifests/circular-triage.json`
- Source reports:
  - `packages/variable-gen/reports/repair/roman-source-report.json`
  - `packages/variable-gen/reports/repair/italic-source-report.json`
- Export/interpolation reports:
  - `packages/variable-gen/reports/repair/roman-designspace-interpolatable.json`
  - `packages/variable-gen/reports/repair/italic-designspace-interpolatable.json`
- Instance risk reports:
  - `packages/variable-gen/reports/repair/roman-instance-risk-report.json`
  - `packages/variable-gen/reports/repair/italic-instance-risk-report.json`
- Review packet:
  - `packages/variable-gen/reports/repair/review-packet.md`
- Built variable fonts:
  - `packages/variable-gen/build/roman/glide-variable-vf.ttf`
  - `packages/variable-gen/build/italic/glide-variable-italic-vf.ttf`

## Comprehensive audit workflow

Run the all-glyph audit workflow for both families:

```bash
.venv/bin/python packages/variable-gen/scripts/audit_variable_font.py --family all
```

Run one family with denser in-between sampling:

```bash
.venv/bin/python packages/variable-gen/scripts/audit_variable_font.py --family italic --samples-per-span 9
```

Run a focused in-between audit that skips donor validation and only prioritizes
interior span failures:

```bash
.venv/bin/python packages/variable-gen/scripts/audit_variable_font.py --family all --interpolation-only
```

What it does:

- exports the live `.glyphs` source to UFOs + designspace
- runs `fontTools.varLib.interpolatable` across all designspace sources
- builds a variable TTF
- samples interior weights inside each adjacent master span
- audits every glyph in every sampled instance for intersections, zero-ink outlines, and short segments
- validates exact master instances against the Circular donor statics across all glyphs
- writes family JSON + Markdown reports plus an overview summary

Interpolation-only mode:

- skips exact-master donor comparison entirely
- keeps the full sampled-weight audit artifacts
- separates interior span risk from endpoint-only risk
- ranks glyphs by `interpolatable` issues plus interior sampled failures only
- writes suffixed reports so the focused run does not overwrite the default audit

Audit outputs:

- Per-family JSON:
  - `packages/variable-gen/reports/audit/roman/roman-variable-audit.json`
  - `packages/variable-gen/reports/audit/italic/italic-variable-audit.json`
  - `packages/variable-gen/reports/audit/roman/roman-variable-audit-interpolation-only.json`
  - `packages/variable-gen/reports/audit/italic/italic-variable-audit-interpolation-only.json`
- Per-family Markdown:
  - `packages/variable-gen/reports/audit/roman/roman-variable-audit.md`
  - `packages/variable-gen/reports/audit/italic/italic-variable-audit.md`
  - `packages/variable-gen/reports/audit/roman/roman-variable-audit-interpolation-only.md`
  - `packages/variable-gen/reports/audit/italic/italic-variable-audit-interpolation-only.md`
- All-family overview:
  - `packages/variable-gen/reports/audit/audit-overview.md`
  - `packages/variable-gen/reports/audit/audit-run-summary.json`
  - `packages/variable-gen/reports/audit/audit-overview-interpolation-only.md`
  - `packages/variable-gen/reports/audit/audit-run-summary-interpolation-only.json`

## Initial target family

Circular in:

- `cabinet/Circular/Circular`
- `cabinet/Circular/Circular Italic`

## Notes for implementation

- Prefer Python for the core engine. The current repo already relies on
  `fontTools`, `glyphsLib`, and UFO tooling.
- Keep the package headless by default.
- Treat Glyphs and FontLab as optional fallback review tools, not mandatory
  runtime dependencies.
