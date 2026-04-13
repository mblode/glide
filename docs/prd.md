# Variable-gen PRD

This PRD defines the product goal for the reusable static-to-variable font
pipeline that will live in `packages/variable-gen`.

Related docs:
- [Research](./variable-gen-research.md)
- [Execution plan](./variable-gen-plan.md)
- [Technical spec](./variable-gen-technical-spec.md)
- [Package README](../packages/variable-gen/README.md)

## Product summary

Build an automated pipeline that turns a family of static fonts into one or
more production-ready variable fonts, with measurable compatibility checks,
repair steps, and fallback handling for glyphs that cannot interpolate cleanly.

The pilot donor family is Circular:

- Roman: [`cabinet/Circular/Circular`](../cabinet/Circular/Circular)
- Italic: [`cabinet/Circular/Circular Italic`](../cabinet/Circular/Circular%20Italic)

## Problem

The repo can already build a Glide-specific four-master variable font, but it
cannot yet take a raw static donor family and produce a reusable variable-font
source tree with confidence.

Current gaps:

- The existing pipeline is Glide-specific.
- The existing pipeline only covers `400/500/700/900`.
- The existing italic flow is seeded, not fully donor-driven.
- The raw Circular family has large compatibility issues across all eight
  weights.
- There is no formal system for handling glyph substitutions when some shapes
  cannot remain continuously interpolable.

## Users

Primary user:

- An internal type engineer who wants a repeatable pipeline, reports, and clear
  escalation paths instead of one-off editor work.

Secondary user:

- A designer who wants to review only the glyphs that the pipeline cannot fix
  with high confidence.

## Goals

### Product goals

- Ingest a static family from OTF, TTF, UFO, or Glyphs sources.
- Build a reusable manifest that describes axes, master order, style names,
  donor paths, and known exceptions.
- Detect and repair master incompatibility in an automated way.
- Build roman and italic variable fonts when both are available.
- Support the full Circular weight range from Thin to ExtraBlack.
- Preserve or rebuild kerning, naming, and layout tables in a deterministic
  way.
- Produce machine-readable reports and human-readable review queues.

### Circular pilot goals

- Build `circular-variable` with a `wght` range that includes the available
  donor weights from `250` to `950`.
- Build `circular-variable-italic` from the donor italic family, not from a
  slanted roman proxy.
- Reduce severe interpolatability failures in the source masters to zero before
  final build.
- Surface non-interpolable glyphs as explicit alternate-substitution work, not
  hidden build drift.

## Non-goals

- Fully automatic repair of every donor family without review.
- A general design editor.
- Multi-axis interpolation beyond the first weight-axis milestone.
- Web packaging, proofing, and marketing assets in the first milestone.
- Automatic authoring of new glyph designs when the donor family is missing a
  glyph.

## User stories

- As a type engineer, I can point the pipeline at a folder of donor statics and
  get a structured compatibility report before any build starts.
- As a type engineer, I can run a repair stage and see which glyphs were fixed,
  which were frozen, and which need alternates or manual review.
- As a designer, I can inspect a focused list of unresolved glyphs instead of
  manually scanning the whole family.
- As a release engineer, I can build variable fonts and selected static
  checkpoints from a single manifest.

## Success metrics

### Functional

- A single command can run audit, repair, build, and validate for a family
  manifest.
- The pipeline can emit both roman and italic variable fonts for Circular.
- The output range includes Thin through ExtraBlack donors.

### Quality

- `fontTools.varLib.interpolatable` reports zero severe structural issues for
  build inputs.
- Instance validation at donor checkpoints stays within documented tolerance
  bands.
- The pipeline reports every dropped glyph, frozen glyph, and unresolved glyph.

### Operational

- The pipeline runs headlessly by default.
- Optional editor-assisted review is isolated to an explicit fallback step.
- The build is deterministic from a manifest plus donor files.

## Constraints

- The implementation should live in `packages/variable-gen`.
- Planning and specs live in `docs/`.
- The repo already uses Python-based font tooling in `cabinet`; the new package
  should reuse that ecosystem rather than replace it with a weaker JS wrapper.
- The package should use the donor family in `cabinet/Circular/...`, not the
  older `src/donors/circular` layout assumed by current scripts.

## Milestones

1. Manifest-driven audit and report generation.
2. Automated compatibility repair for a full eight-weight roman family.
3. Automated compatibility repair for the matching italic family.
4. Alternate-substitution planning for irreducible glyphs.
5. End-to-end Circular variable build and validation.

## Open product questions

- Should Book remain a named checkpoint inside the final axis, or should it be
  a named instance only?
- Should the first release target TrueType variable output only, or also CFF2?
- How much unresolved drift is acceptable before a build is blocked?
- Should missing italic-only glyphs be dropped, copied from roman, or modeled as
  explicit exclusions in the pilot manifest?
