# Variable-gen research

This document records the current state of the repo, the donor Circular family,
and the external tooling that should shape `packages/variable-gen`.

Related docs:
- [PRD](./prd.md)
- [Execution plan](./variable-gen-plan.md)
- [Technical spec](./variable-gen-technical-spec.md)
- [Package README](../packages/variable-gen/README.md)

## Bottom line

The repo already contains a narrow, Glide-specific pipeline that proves a few
important ideas:

- Static checkpoints can be normalized, assembled into a designspace, and built
  into roman and italic variable fonts.
- Start point, contour order, and some segment-count problems can be detected
  and partially repaired with `fontTools`.
- Italics can be seeded from donor italics, but the current approach is a
  Glide-specific workaround, not a reusable static-to-variable pipeline.

The same repo also shows why a general pipeline is still needed:

- The current build flow is hardcoded for four weights: `400,500,700,900`.
- The current italic generation depends on seeded Glide romans plus Circular
  donor deltas, not a full donor family.
- The raw Circular family is not directly interpolatable across all eight
  weights.

## Existing repo audit

### Release orchestration

`cabinet/Makefile` is a thin wrapper around
[`cabinet/build/release.py`](../cabinet/build/release.py).

`release.py` orchestrates a fixed Glide build:

1. Extract four roman checkpoints from an existing root Glide variable font.
2. Seed four italic checkpoints from Circular donors.
3. Run a FontLab-prep repair pass.
4. Build roman and italic variable fonts.
5. Generate static instances at `400/500/700/900`.
6. Reapply exact donor italic kerning to compare instances.
7. Package release assets.

This is useful as a reference pipeline, but it is not reusable because the
paths, family naming, donor layout, and weight set are hardcoded.

### Scripts that already matter

These scripts contain the parts worth extracting into `packages/variable-gen`:

- [`cabinet/build/build_variable.py`](../cabinet/build/build_variable.py)
  - Normalizes source glyph sets.
  - Decomposes composites.
  - Runs `fontTools.varLib.interpolatable`.
  - Builds a designspace and variable font.
- [`cabinet/build/prepare_for_fontlab.py`](../cabinet/build/prepare_for_fontlab.py)
  - Contains the strongest repair logic in the repo.
  - Reorders contours, splits segments, coerces line/quad types, and tries to
    rebuild compatible master chains.
  - Still assumes four masters and was written as a FontLab-prep stage.
- [`cabinet/build/seed_glide_italic_from_circular.py`](../cabinet/build/seed_glide_italic_from_circular.py)
  - Seeds italics by mixing direct donor deltas with a slant fallback.
  - Only uses donor endpoints at `400` and `900`.
  - Is an important prototype for "alternate repair strategies per glyph".
- [`cabinet/build/italic_variable_kerning.py`](../cabinet/build/italic_variable_kerning.py)
  - Rebuilds canonical italic GPOS sources for variable interpolation.
- [`cabinet/build/generate_instances.py`](../cabinet/build/generate_instances.py)
  - Validates generated instances against source statics by point deviation,
    area deltas, and a crude stem check.
- [`cabinet/fix_source_files.py`](../cabinet/fix_source_files.py),
  [`cabinet/fix_glyphs_startpoints.py`](../cabinet/fix_glyphs_startpoints.py),
  [`cabinet/fix_ttf_startpoints.py`](../cabinet/fix_ttf_startpoints.py)
  - Show three different repair layers:
    source-level topology normalization, source-level start-point rotation, and
    post-`cu2qu` TTF start-point repair.
- [`cabinet/import_circular.py`](../cabinet/import_circular.py)
  - Contains the strongest earlier logic for contour matching and topology
    normalization when importing Circular outlines into Glide sources.

### Hardcoded assumptions that block reuse

The current scripts repeatedly hardcode:

- Family structure: `roman` and `italic`.
- Weight set: `400,500,700,900`.
- Weight names: `Regular`, `Medium`, `Bold`, `Black`.
- Donor file names and locations.
- Glide-specific source paths and output stems.
- A single `wght` axis with the default fixed at `400`.

Examples:

- [`cabinet/build/source_manifest.py`](../cabinet/build/source_manifest.py)
- [`cabinet/build/font_metadata.py`](../cabinet/build/font_metadata.py)
- [`cabinet/build/release.py`](../cabinet/build/release.py)
- [`cabinet/build/seed_glide_italic_from_circular.py`](../cabinet/build/seed_glide_italic_from_circular.py)

### Current build quality

The current generated Glide reports are good enough to prove the pipeline, but
not good enough to generalize:

- [`cabinet/build/work/reports/summary.json`](../cabinet/build/work/reports/summary.json)
  shows a four-master Glide build with 472 glyphs in both roman and italic.
- Roman still has 4 glyphs with compatibility issues.
- Italic still has 9 glyphs with compatibility issues.
- Validation reports show exact matches at `400`, `500`, and `900`, but sizable
  drift at `700`:
  - [`cabinet/build/work/reports/roman-instance-validation.json`](../cabinet/build/work/reports/roman-instance-validation.json)
  - [`cabinet/build/work/reports/italic-instance-validation.json`](../cabinet/build/work/reports/italic-instance-validation.json)

That means the current build is not yet a trustworthy template for full-family
automation.

## Circular donor audit

### Family inventory

The donor family in this repo is:

- Roman: [`cabinet/Circular/Circular`](../cabinet/Circular/Circular)
- Italic: [`cabinet/Circular/Circular Italic`](../cabinet/Circular/Circular%20Italic)

Available weight classes:

- `250`: Thin
- `300`: Light
- `400`: Regular
- `450`: Book
- `500`: Medium
- `700`: Bold
- `900`: Black
- `950`: ExtraBlack

Important findings from direct font inspection:

- All eight roman files contain 755 glyphs.
- All eight italic files contain 744 glyphs.
- Every italic is missing the same 11 `a.ss02` family glyphs that exist in
  roman.

Missing in all italics:

- `a.ss02`
- `aacute.ss02`
- `abreve.ss02`
- `acircumflex.ss02`
- `adieresis.ss02`
- `agrave.ss02`
- `amacron.ss02`
- `aogonek.ss02`
- `aring.ss02`
- `aringacute.ss02`
- `atilde.ss02`

### Raw compatibility results

Running `fontTools.varLib.interpolatable` on the donor OTFs shows that the raw
family is far from directly mergeable:

- Roman:
  - 604 glyphs with issues
  - dominant issue types: `node_incompatibility`, `node_count`,
    `wrong_start_point`, `underweight`, `contour_order`
- Italic:
  - 624 glyphs with issues
  - dominant issue types: `node_incompatibility`, `node_count`,
    `wrong_start_point`, `underweight`, `contour_order`, `kink`

Worst pairings are not evenly distributed. They cluster around:

- `Thin -> Light`
- `Regular -> Book`
- `Black -> ExtraBlack`

That matters because the eventual pipeline should treat compatibility as a graph
problem, not a single global pass.

The reduced subset closest to the current `.vfc` attempt is still far from
clean:

- Roman `Book -> Medium -> Bold -> Black`: 303 glyphs with issues
- Italic `Book -> Medium -> Bold -> Black`: 325 glyphs with issues

So the current `Book -> Black` ceiling is not only a missing-manifest problem.
Even that reduced donor slice still needs a compatibility-repair layer.

### Why the current `.vfc` only reaches Book-to-Black

The current repo builds around four weights and a pre-existing Glide variable
font, not around the full Circular donor family. The limiting factors are:

1. The current manifest and packaging logic only know about
   `400/500/700/900`.
2. The italic seeding script only samples donor endpoints at `400` and `900`.
3. The current release flow starts from extracted Glide masters, not from all
   eight Circular statics.
4. The raw Circular donors have large topology differences at the edges of the
   family, especially `Thin/Light` and `Black/ExtraBlack`.

So the missing Thin and ExtraBlack range is mostly a pipeline-design problem,
not only a file-availability problem.

## External tooling research

### fontTools

Useful official guidance:

- `designspaceLib` is the right source of truth for master locations, named
  instances, axis maps, and split variable-font outputs.
- `cu2qu.ufo.fonts_to_quadratic()` converts multiple fonts together and keeps
  them interpolation-compatible.
- `fontTools.varLib.interpolatable` is the right first-pass structural checker.
  Its optional dependency docs confirm that `scipy` or `munkres` improves the
  contour-assignment step.
- `featureVars` is the right low-level tool for conditional substitutions in
  variable fonts when some glyph shapes cannot stay continuously interpolable.

### fontmake

Useful official guidance:

- `fontmake` already formalizes the binary build stages we need after source
  repair.
- Its `ttf-interpolatable` output exists specifically for master binaries that
  are safe to merge into a variable font.
- Its docs confirm that the compile path includes overlap handling,
  cubic-to-quadratic conversion, GDEF/features generation, and variable-font
  table building.

### Glyphs

Useful official guidance:

- The handbook explicitly says successful interpolation requires compatible path
  order, starting points, and path direction across masters.
- `Correct Path Direction` resets direction, shape order, and start points
  across masters.
- Glyph switching and alternate layers are the right conceptual model when a
  glyph cannot stay continuously interpolable through the whole axis.

### FontLab

Useful official guidance:

- FontLab 8 is explicitly variable-first and advertises automatic master
  matching for point-compatible outlines.
- FontLab can create a multi-master font from separate single-master fonts with
  `Merge to Layers`.
- Matchmaker remains useful as an optional recovery tool after automated repair,
  but it should be a fallback, not the primary pipeline.

## Implications for `packages/variable-gen`

The package should not try to be a thin wrapper around `fontmake`.

It needs to own these stages:

1. Donor discovery and manifest generation.
2. Glyph set reconciliation.
3. Canonical outline conversion.
4. Compatibility analysis.
5. Automated repair.
6. Conditional substitution planning for irreducible glyphs.
7. Designspace assembly.
8. Variable build and instance validation.

The current repo already contains prototypes for steps 2 through 6. The work
now is to extract them into a general engine and remove Glide-specific
assumptions.

## Sources

- fontTools optional dependencies:
  https://fonttools.readthedocs.io/en/latest/optional.html
- fontTools `cu2qu` docs:
  https://fonttools.readthedocs.io/en/latest/cu2qu/index.html
- fontTools `designspaceLib` docs:
  https://fonttools.readthedocs.io/en/latest/designspaceLib/index.html
- fontTools `featureVars` docs:
  https://fonttools.readthedocs.io/en/stable/varLib/featureVars.html
- fontmake README:
  https://github.com/googlefonts/fontmake
- fontmake advanced usage:
  https://github.com/googlefonts/fontmake/blob/main/USAGE.md
- Glyphs handbook, editing paths:
  https://handbook.glyphsapp.com/editing-paths/
- Glyphs handbook, switching shapes:
  https://handbook.glyphsapp.com/switching-shapes/
- FontLab variations help:
  https://help.fontlab.com/fontlab-vi/Working-with-Font-Variations/
- FontLab 8 families and variation:
  https://help.fontlab.com/fontlab/8/whats-new/whats-new-07-families-variation/
