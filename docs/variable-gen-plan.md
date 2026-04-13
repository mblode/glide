# Variable-gen execution plan

This is the phased execution plan for the `packages/variable-gen` buildout.

Related docs:
- [Research](./variable-gen-research.md)
- [PRD](./prd.md)
- [Technical spec](./variable-gen-technical-spec.md)
- [Package README](../packages/variable-gen/README.md)

## Current status

- [x] Audit the existing `cabinet` scripts and reports.
- [x] Audit the donor Circular roman and italic families.
- [x] Research official guidance for `fontTools`, `fontmake`, Glyphs, and
      FontLab.
- [x] Write the initial PRD, plan, technical spec, and package README.

## Team split

Treat the work as three parallel tracks:

- Team A: source ingestion and manifests
- Team B: compatibility analysis and repair
- Team C: variable build, substitutions, and validation

## Phase 1: package bootstrap

- [ ] Create the initial Python package layout under `packages/variable-gen`.
- [ ] Add an isolated dependency spec for `fonttools`, `glyphsLib`, `ufoLib2`,
      `scipy`, and build helpers.
- [ ] Add a CLI entrypoint with subcommands for `audit`, `repair`, `build`, and
      `validate`.
- [ ] Add a docs-linked sample manifest for Circular.

## Phase 2: donor discovery and manifests

- [ ] Implement donor scanning for OTF, TTF, UFO, and Glyphs sources.
- [ ] Build a manifest v2 format that supports arbitrary weight checkpoints, not
      just `400/500/700/900`.
- [ ] Capture axis user-space values and design-space values separately.
- [ ] Support separate roman and italic families with shared metadata.
- [ ] Record glyph-set differences and declared exclusions at ingest time.

## Phase 3: canonical source normalization

- [ ] Normalize all donors into a canonical working format.
- [ ] Decompose composites where interpolation safety requires it.
- [ ] Normalize curve model per build target:
      `ttf-interpolatable` for TrueType output, or a cubic-safe path for CFF2
      experiments.
- [ ] Preserve source metrics, names, and layout data in the manifest or side
      tables.
- [ ] Emit normalized intermediates to a stable work directory inside
      `packages/variable-gen`.

## Phase 4: compatibility analysis

- [ ] Run `fontTools.varLib.interpolatable` for the family and adjacent master
      pairs.
- [ ] Add structural fingerprinting for glyph presence, contour count, contour
      order, path direction, start points, segment type, and node count.
- [ ] Cluster failures by master pair so edge weights can be treated
      differently.
- [ ] Produce JSON and Markdown reports with severity levels.
- [ ] Mark glyphs that require alternates instead of direct interpolation.

## Phase 5: automated repair engine

- [ ] Port the reusable contour-matching logic from `cabinet/import_circular.py`
      and `cabinet/build/prepare_for_fontlab.py`.
- [ ] Add contour assignment with a Hungarian-style matcher.
- [ ] Normalize path direction and start points across masters.
- [ ] Normalize segment types and point counts.
- [ ] Support repair chains across more than four masters.
- [ ] Add confidence scoring so low-confidence repairs are reported, not hidden.

## Phase 6: substitution planning

- [ ] Define a manifest section for alternate glyph families and switch ranges.
- [ ] Support glyph-level substitution planning for shapes such as `Q`,
      `percent`, ligatures, and ss glyphs that cannot interpolate cleanly
      through the whole axis.
- [ ] Generate designspace rules or feature-variation inputs for build-time
      substitution.
- [ ] Report unresolved glyphs that still need designer-authored alternates.

## Phase 7: build and validate

- [ ] Assemble manifest-driven designspaces.
- [ ] Build variable fonts with deterministic metadata and STAT setup.
- [ ] Generate named static checkpoints, including Thin, Light, Regular, Book,
      Medium, Bold, Black, and ExtraBlack where available.
- [ ] Validate checkpoints against donor statics by point drift, area drift,
      metrics drift, and kerning drift.
- [ ] Fail the build when severity thresholds are exceeded.

## Phase 8: Circular pilot rollout

- [ ] Create the Circular manifest.
- [ ] Run audit on all eight roman donors.
- [ ] Run audit on all eight italic donors.
- [ ] Decide the glyph policy for the 11 `a.ss02` italic omissions.
- [ ] Run the repair engine on roman.
- [ ] Run the repair engine on italic.
- [ ] Add substitution handling for irreducible glyphs.
- [ ] Build `circular-variable`.
- [ ] Build `circular-variable-italic`.
- [ ] Publish a final validation report and remaining manual-review list.

## Exit criteria for phase 1 implementation

Phase 1 is done when:

- `packages/variable-gen` contains a runnable CLI scaffold.
- A Circular manifest can be loaded.
- `audit` produces a reproducible compatibility report from the donor folders.
- The package no longer depends on Glide-specific file names or root variable
  fonts.
