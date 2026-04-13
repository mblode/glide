# Variable-gen technical spec

This document specifies the architecture for the reusable
`packages/variable-gen` pipeline.

Related docs:
- [Research](./variable-gen-research.md)
- [PRD](./prd.md)
- [Execution plan](./variable-gen-plan.md)
- [Package README](../packages/variable-gen/README.md)

## Bottom line

`packages/variable-gen` should be a Python package with a manifest-driven CLI.
It should treat static-to-variable conversion as a staged compiler:

1. Ingest donors.
2. Normalize sources.
3. Analyze compatibility.
4. Repair what can be repaired safely.
5. Mark or route around what cannot be interpolated directly.
6. Build designspaces and variable fonts.
7. Validate outputs against donor checkpoints.

## Proposed package layout

The first implementation should grow toward this shape:

```text
packages/variable-gen/
  README.md
  pyproject.toml
  src/variable_gen/
    cli.py
    manifest.py
    discover.py
    normalize.py
    analyze.py
    repair.py
    substitutions.py
    build.py
    validate.py
    reporting.py
  manifests/
    circular.yaml
  tests/
```

## Runtime and dependencies

### Required

- Python 3.11+
- `fonttools[interpolatable,woff,ufo]`
- `glyphsLib`
- `ufoLib2`
- `scipy`

### Recommended

- `fontmake`
- `skia-pathops`
- `brotli`
- `zopfli`

### Optional fallback tools

- Glyphs app
- FontLab 8

These editors should be treated as optional review tools, not primary build
dependencies.

## Manifest v2

The current `cabinet/build/source_manifest.py` format is too narrow. The new
manifest should support:

```yaml
family_name: Circular
build_name: circular
axes:
  - tag: wght
    name: Weight
    default: 400
    values:
      - { user: 250, design: 250, name: Thin }
      - { user: 300, design: 300, name: Light }
      - { user: 400, design: 400, name: Regular }
      - { user: 450, design: 450, name: Book }
      - { user: 500, design: 500, name: Medium }
      - { user: 700, design: 700, name: Bold }
      - { user: 900, design: 900, name: Black }
      - { user: 950, design: 950, name: ExtraBlack }
families:
  roman:
    source_dir: cabinet/Circular/Circular
    style_link_default: Regular
  italic:
    source_dir: cabinet/Circular/Circular Italic
    style_link_default: Italic
glyph_policies:
  exclude_from_italic:
    - a.ss02
    - aacute.ss02
```

Key requirements:

- Arbitrary master counts.
- Separate user-space and design-space coordinates.
- Explicit exclusions and alternate policies.
- No hardcoded file names inside the code.

## Pipeline stages

### 1. Discovery

Inputs:

- OTF
- TTF
- UFO
- Glyphs

Outputs:

- Resolved source inventory
- Weight/style metadata
- Glyph-set summary
- Initial manifest or manifest validation report

### 2. Canonical normalization

Goals:

- Convert all sources into a common working representation.
- Decompose composites where needed.
- Reconcile glyph order.
- Normalize to the curve model required by the target build.

Recommended strategy:

- For TrueType variable output, normalize to UFO or TTF sources that were
  converted together with `cu2qu`, not one font at a time.
- Preserve a source-to-normalized mapping for traceability.

### 3. Compatibility analysis

The analyzer should combine official and custom checks.

Official check:

- `fontTools.varLib.interpolatable`

Custom checks:

- glyph presence
- contour count
- contour order
- contour winding
- start-point index
- segment type
- node count
- bounds and gross metrics drift

The analyzer should emit:

- family summary
- pair summary
- glyph summary
- repair recommendations
- substitution candidates

### 4. Repair engine

The repair engine should extract and generalize the best logic already present
in:

- `cabinet/import_circular.py`
- `cabinet/build/prepare_for_fontlab.py`
- `cabinet/fix_source_files.py`
- `cabinet/fix_glyphs_startpoints.py`
- `cabinet/fix_ttf_startpoints.py`

#### Repair order

Run repairs in this order:

1. glyph-set reconciliation
2. contour assignment
3. path direction normalization
4. start-point rotation
5. segment-type coercion
6. node-count repair by segment splitting
7. post-`cu2qu` TTF start-point repair when needed

#### Repair confidence

Every repair should emit one of:

- `safe`
- `review`
- `blocked`

`blocked` glyphs should move into substitution planning or manual review.

### 5. Substitution planning

Some glyphs should not be forced through continuous interpolation.

Examples:

- `Q` tail changes
- ligatures with changing topology
- percentage and currency glyphs with repeated severe incompatibilities
- style-set glyphs missing from one family

The pipeline should support:

- explicit alternate glyph families
- axis ranges for substitution
- designspace rules or `featureVars` inputs
- frozen glyphs when interpolation is not acceptable

### 6. Build

The build stage should:

- create designspaces from repaired sources
- build variable TTF outputs first
- optionally support later CFF2 experiments
- rebuild metadata and STAT tables from manifest data
- preserve or rebuild kerning deterministically

Preferred build flow:

1. normalized masters
2. repaired masters
3. interpolatable build inputs
4. `fontmake` or direct `varLib.build`
5. metadata patching
6. static checkpoint extraction

### 7. Validation

Validation should compare generated checkpoints to donor statics at named
weights.

Minimum checks:

- glyph presence parity
- point-count parity
- point-deviation thresholds
- area-drift thresholds
- advance-width drift
- kerning drift

The build should fail on:

- severe structural mismatches
- checkpoint drift above threshold
- unresolved blocked glyphs without declared policy

## Circular-specific requirements

The first pilot should encode these facts:

- Roman donors span 8 weights and 755 glyphs.
- Italic donors span 8 weights and 744 glyphs.
- All italics are missing the same 11 `a.ss02` family glyphs.
- Raw donor compatibility is poor, especially at:
  - Thin -> Light
  - Regular -> Book
  - Black -> ExtraBlack

That means the Circular build should not start from a two-endpoint model. It
should use all available checkpoints and let the repair engine decide which
glyphs can interpolate globally, which need local fixes, and which need
alternates.

## Circular-specific acceptance criteria

- `audit` reports all 8 roman donors and all 8 italic donors.
- `repair` reduces build inputs to zero severe interpolatable failures.
- `build` emits:
  - `circular-variable.ttf`
  - `circular-variable-italic.ttf`
- `validate` emits reports for:
  - Thin
  - Light
  - Regular
  - Book
  - Medium
  - Bold
  - Black
  - ExtraBlack

## What not to port from `cabinet` as-is

Do not carry these assumptions forward unchanged:

- fixed four-master weight maps
- Glide-specific source extraction
- donor endpoints only at `400` and `900`
- release packaging logic mixed into build logic
- implicit path conventions like `src/donors/circular`

## Risks

### Technical

- Some donors will remain structurally incompatible after automated repair.
- `cu2qu` can still introduce post-conversion start-point changes.
- Kerning interpolation may need family-specific logic when source GPOS varies
  heavily across weights.

### Product

- Users may expect perfect output from arbitrary static families.
- The Circular pilot may reveal that some edge weights should become named
  instances instead of full interpolation masters for specific glyph groups.

## Recommended first implementation cut

Build this in order:

1. manifest loader
2. donor scanner
3. audit report
4. repair engine
5. Circular manifest
6. Circular audit

Do not start with packaging or proofing. The first milestone is trustworthy
audit plus repair.
