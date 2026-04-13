# Italic Repair Plan

## Scope

This plan covers the next repair stage for:

- `/Users/mblode/Code/mblode/glide/glide-variable-italic.glyphs`
- the current Circular donor import pipeline in `packages/variable-gen`
- the glyphs currently showing visual or export risk, including:
  - `X`
  - `a`
  - `b`
  - `g`
  - `r`
  - `s`
  - `t`
  - `u`
  - `slash`
  - `.notdef`
  - `percent`
  - `ampersand`
  - `two`

## Research Summary

- The current italic source is source-compatible after import:
  - path order issues: `0`
  - node count issues: `0`
  - start-point issues: `0`
  - post-write mismatches: `0`
- That is not enough. Several glyphs only become compatible after topology surgery during import.
- `.notdef` is currently a real blocker:
  - it is `metrics_only`
  - it has `0` paths in all italic masters
- `ncommaaccent` and `napostrophe` were already forced to reference fallback because export/remove-overlap was failing on interpolated donor outlines.
- Most of the glyphs called out by the user are not donor-clean. Their donor masters differ in segment count and/or contour structure, then the importer pads or rewrites them to make them technically compatible.

## Glyph Risk Buckets

### Tier 0: Blockers

- [x] `.notdef`
  - empty in all masters
  - must be rebuilt first
- [x] existing export-risk fallback glyphs
  - `ncommaaccent`
  - `napostrophe`

### Tier 1: High-risk topology surgery glyphs

These are structurally compatible only after non-trivial normalization:

- [ ] `X`
  - donor segment counts become `13` after repair from raw `11/12/11`
- [ ] `a`
  - donor contours are reordered and normalized to `5 + 12`
  - one master effectively flips contour complexity across contours
- [ ] `b`
  - donor normalized to `9 + 4`
- [ ] `g`
  - donor normalized to `4 + 15`
- [ ] `s`
  - donor normalized to `18`
- [ ] `t`
  - donor normalized to `19`
- [ ] `u`
  - donor normalized to `17`
- [ ] `percent`
  - donor normalized to `4/4/4/4/4`
- [ ] `ampersand`
  - donor normalized to `18/6/6`
- [ ] `two`
  - donor normalized to `17`

### Tier 2: Lower-risk suspects

- [ ] `r`
  - donor already matches structurally
  - likely visual/design review only
- [ ] `slash`
  - donor already aligns structurally, but normalization still adds an explicit closing segment

## Why The Current Pipeline Is Insufficient

- The importer is a source normalizer, not yet a full repair system.
- It checks:
  - contour order
  - start points
  - cubic compatibility
- It does not yet check:
  - contour winding direction as a first-class invariant
  - interpolated instance geometry
  - remove-overlap / boolean safety
  - donor-vs-instance drift
  - per-glyph repair strategies via manifest
  - component rebuild opportunities
- `cabinet/fix_export_compatibility.py` only targets:
  - `wrong_start_point`
  - `node_incompatibility`
- That means “technically compatible but visually wrong” glyphs are currently invisible to automation.

## Phase Plan

### Phase 1: Intake And Classification

- [x] Produce a dedicated italic triage manifest in `packages/variable-gen`
- [x] Record per-glyph strategy fields:
  - `clean`
  - `normalized`
  - `reference_fallback`
  - `component_rebuild`
  - `manual_review`
  - `export_blocker`
- [x] Seed the manifest with:
  - fallback glyphs from the current reports
  - the user-reported suspect set
  - `.notdef`

### Phase 2: Source-Level Canonicalization

- [x] Add contour winding audit to `populate_circular_glyphs.py`
- [x] Add contour winding normalization where safe
- [ ] Store per-contour topology signatures in the report
- [x] Record how many segments were inserted per contour per master
- [x] Flag glyphs whose normalized topology differs materially from donor topology

### Phase 3: Instance-Level Interpolation Audit

- [x] Export designspace/UFO checkpoints for the italic source
- [x] Sample intermediate locations between ThinItalic, Italic, and ExtraBlackItalic
- [ ] Score each sampled glyph for:
  - self-intersections
  - contour collapse
  - bad extrema
  - pathological handle movement
  - remove-overlap failure risk
- [x] Output a ranked “interpolation-risk” report

### Phase 4: Repair Strategy Engine

- [x] Add a per-glyph strategy manifest reader
- [ ] Support these automated strategies:
  - `normalize`
  - `reference_fallback`
  - `canonical_fallback`
  - `component_rebuild`
  - `skip`
- [ ] Integrate the stronger adjacent-master repair logic from:
  - `cabinet/build/prepare_for_fontlab.py`
- [x] Allow strategy overrides for the Tier 1 italic glyph set

### Phase 5: Export-Geometry Validation

- [ ] Add remove-overlap validation as a first-class pipeline step
- [ ] Add a report of glyphs that fail boolean cleanup after interpolation
- [ ] Persist the exact failing glyph list back into the manifest
- [ ] Distinguish:
  - source-compatible
  - export-compatible
  - visually approved

### Phase 6: Manual Review Handoff

- [x] Generate a compact review packet for remaining glyphs
- [ ] Include for each glyph:
  - donor master snapshots
  - normalized source snapshots
  - intermediate instance snapshots
  - recommended repair strategy
- [x] Limit manual review to the residual set after automation

### Phase 7: Regression Lock

- [x] Re-run source compatibility audit
- [x] Re-run instance interpolation audit
- [x] Re-run export/remove-overlap audit
- [x] Freeze approved glyph strategies in the manifest
- [x] Make reruns deterministic from `packages/variable-gen`

## Team Split

### Team A: Intake + Reports

- [ ] Build the glyph triage manifest
- [ ] Enrich importer reports with topology-surgery metrics

### Team B: Geometry + Repair

- [ ] Add winding audit
- [ ] Add strategy selection
- [ ] Integrate chain-repair logic from `prepare_for_fontlab.py`

### Team C: Export + Validation

- [ ] Add instance sampling
- [ ] Add boolean/remove-overlap validation
- [ ] Produce a ranked export-risk report

### Team D: Manual Review

- [ ] Review only the glyphs that survive automation
- [ ] Approve fallback vs redraw vs component rebuild on a per-glyph basis

## Immediate Next Pass

- [x] Rebuild `.notdef` in italic masters
- [x] Add the italic triage manifest
- [x] Instrument the importer to report topology surgery for every glyph
- [x] Run the first interpolation-risk scan on:
  - `X a b g r s t u slash .notdef percent ampersand two`
