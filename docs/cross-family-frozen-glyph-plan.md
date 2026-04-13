# Cross-Family Frozen Glyph Plan

This plan covers the newly reported broken glyphs in both sources:

- [glide-variable-italic.glyphs](/Users/mblode/Code/mblode/glide/glide-variable-italic.glyphs)
- [glide-variable.glyphs](/Users/mblode/Code/mblode/glide/glide-variable.glyphs)

## Scope

Italic reported set:

- `a`
- `g`
- `r`
- `s`
- `t`
- `u`
- `dollar`
- `percent`
- `ampersand`
- `two`
- `cent`
- `ncommaaccent`
- `napostrophe`
- `tcommaaccent`
- `uni021B`
- `slash`
- `dollar.tf`
- `cent.tf`
- `dollar.ss08`
- `cent.ss08`
- `dollar.tf.ss08`
- `cent.tf.ss08`

Roman reported set:

- `d`
- `e`
- `r`
- `u`
- `dollar`
- `cent`
- `napostrophe`
- `tcommaaccent`
- `uni021B`
- `dollar.tf`
- `cent.ss08`
- `dollar.tf.ss08`
- `cent.tf.ss08`

## Bottom line

The user-reported symptom is real. In the live sources, many of these glyphs now have identical outlines across all masters, with only widths changing.

That happens for two different reasons:

1. The manifest or repair runner explicitly freezes the glyph to the `Regular` or `Italic` outline.
2. The importer hits donor contour-count mismatches, falls back to a canonical reference outline, and the result still looks like a single-weight glyph across the axis.

## Confirmed live-source freeze set

### Italic: exact same outlines across all three masters

- [x] `a`
- [x] `r`
- [x] `s`
- [x] `t`
- [x] `u`
- [x] `dollar`
- [x] `percent`
- [x] `two`
- [x] `cent`
- [x] `ncommaaccent`
- [x] `napostrophe`
- [x] `tcommaaccent`
- [x] `uni021B`
- [x] `dollar.tf`
- [x] `cent.tf`
- [x] `dollar.ss08`
- [x] `cent.ss08`
- [x] `dollar.tf.ss08`
- [x] `cent.tf.ss08`

### Italic: still broken, but not exact-outline frozen

- [x] `g`
- [x] `ampersand`
- [x] `slash`

### Roman: exact same outlines across all three masters

- [x] `dollar`
- [x] `cent`
- [x] `napostrophe`
- [x] `tcommaaccent`
- [x] `uni021B`
- [x] `dollar.tf`
- [x] `cent.ss08`
- [x] `dollar.tf.ss08`
- [x] `cent.tf.ss08`

### Roman: still varying by master, but still reported broken

- [x] `d`
- [x] `e`
- [x] `r`
- [x] `u`

## Root cause buckets

| Bucket | Family | Glyphs | Why they freeze |
| --- | --- | --- | --- |
| Explicit strategy freeze | Italic | `a`, `r`, `percent`, `two` | Current manifest uses `freeze_to_reference` |
| Explicit blocker fallback | Italic | `ncommaaccent`, `napostrophe` | Current manifest uses `reference_fallback` |
| Localized substitution collapse | Italic | `s`, `t`, `u`, `g`, `ampersand` | Repair runner copies `Italic` contours into extremes |
| Import-time reference fallback | Italic | `dollar`, `cent`, `tcommaaccent`, `uni021B`, tabular and `.ss08` alternates | Donor contour-count mismatches trigger importer fallback |
| Explicit blocker fallback | Roman | `napostrophe` | Current manifest uses `reference_fallback` |
| Import-time reference fallback | Roman | `dollar`, `cent`, `tcommaaccent`, `uni021B`, `dollar.tf`, `cent.ss08`, `dollar.tf.ss08`, `cent.tf.ss08` | Donor contour-count mismatches trigger importer fallback |
| Not frozen, still risky | Roman | `d`, `e`, `r`, `u` | Raw donor drift or underweight issues remain, but outlines are not fully frozen |

## Donor findings

### Roman hardest donor cases

- [x] `uni021B`
  - `Thin` is `1 contour / 28 segments`
  - `Book` is `2 contours / 16+7`
  - `ExtraBlack` is `2 contours / 8+16`
- [x] `napostrophe`
  - contour order flips between `Thin/ExtraBlack` and `Book`
- [x] `tcommaaccent`
  - `Thin` is split into `2 contours`
  - `Book` and `ExtraBlack` are merged into `1 contour`
- [x] `dollar`, `dollar.tf`, `dollar.tf.ss08`
  - `Thin/Book` are `3 contours`
  - `ExtraBlack` collapses to `1 contour`
- [x] `cent`, `cent.ss08`, `cent.tf.ss08`
  - `Thin/Book` are `2 contours`
  - `ExtraBlack` collapses to `1 contour`

### Italic hardest donor cases

- [x] `a`
  - `5+12 / 4+11 / 11+4`
  - `ExtraBlackItalic` flips contour roles relative to `Italic`
- [x] `dollar`, `dollar.tf`, `dollar.ss08`, `dollar.tf.ss08`
  - `Thin/Italic` are `3 contours`
  - `ExtraBlackItalic` collapses to `1 contour`
- [x] `cent`, `cent.tf`, `cent.ss08`, `cent.tf.ss08`
  - `Thin/Italic` are `2 contours`
  - `ExtraBlackItalic` collapses to `1 contour`
- [x] `tcommaaccent`
  - `ThinItalic` is split into `2 contours`
  - `Italic` and `ExtraBlackItalic` are merged into `1 contour`
- [x] `uni021B`
  - `ThinItalic` is `1 contour`
  - `Italic` and `ExtraBlackItalic` are `2 contours`
- [x] `percent`
  - same contour count across masters
  - `ExtraBlackItalic` reorders the slash contour

## Research conclusions

- [x] The current repair pipeline is optimized for compatibility and export stability.
- [x] It does not enforce donor-fidelity gates.
- [x] The runner can now remove interpolatable warnings by freezing or substituting contours.
- [x] That can hide the real failure by turning a variable glyph into a static outline with variable widths.
- [x] Roman does not yet have the same cluster-level evidence and planner coverage as italic.

## Phase 1: Freeze detection and reporting

- [ ] Add a live-source `same_outline_across_masters` detector to the repair reports.
- [ ] Report this separately from:
  - `source-compatible`
  - `interpolatable-clean`
  - `donor-faithful`
- [ ] Generate cluster evidence reports for both the roman and italic reported sets, even when the glyphs are not in a repair bucket yet.
- [ ] Fail the report if a glyph becomes exact-outline frozen without an explicit allowlist reason.

## Phase 2: Undo unsafe freezes in italic

- [ ] Restore the italic source from a pre-fallback checkpoint before continuing real repair work.
- [ ] Candidate restore points:
  - `glide-variable-italic.glyphs.pre-action-plan.bak`
  - `glide-variable-italic.glyphs.pre-safe-fallback.bak`
- [ ] Remove `freeze_to_reference` from:
  - `a`
  - `r`
  - `percent`
  - `two`
- [ ] Remove `localized_substitution` from:
  - `g`
  - `s`
  - `t`
  - `u`
  - `ampersand`
- [ ] Rebuild italic reports from the donor-preserving baseline.

## Phase 3: Add a safer strategy taxonomy

- [ ] Split current fallback behavior into separate strategies:
  - `export_blocker_fallback`
  - `temporary_structure_fallback`
  - `localized_substitution`
  - `manual_redraw_required`
- [ ] Allow `temporary_structure_fallback` only for donor contour-count mismatch cases.
- [ ] Ban `freeze_to_reference` from non-blocker glyphs unless both:
  - donor fidelity stays within threshold
  - outline freeze is explicitly approved
- [ ] Add a fidelity threshold gate:
  - exact-master area drift must stay under a chosen percentage
  - no cluster glyph may be exact-outline frozen unless approved

## Phase 4: Roman cluster planner

- [ ] Add roman repair buckets for the newly reported set.
- [ ] Build roman cluster evidence and a roman exception plan report.
- [ ] Bucket the roman set:
  - blocker fallback: `napostrophe`
  - merge/split donor failures: `dollar`, `cent`, `tcommaaccent`, `uni021B`, alternates
  - donor drift but not frozen: `d`, `e`, `r`, `u`
- [ ] Do not apply fallbacks yet. First generate the same evidence packet that exists for italic.

## Phase 5: Family-specific repair tracks

### Italic

- [ ] Redraw or rebuild the true hard cases:
  - `a`
  - `g`
  - `ampersand`
  - `two`
- [ ] Build donor-preserving repair strategies for:
  - `s`
  - `t`
  - `u`
- [ ] Revisit importer fallback cases:
  - `dollar`
  - `cent`
  - `tcommaaccent`
  - `uni021B`
  - tabular and `.ss08` variants

### Roman

- [ ] Build contour-remap or substitution logic for:
  - `uni021B`
  - `napostrophe`
  - `tcommaaccent`
- [ ] Add dedicated handling for ExtraBlack contour collapse in:
  - `dollar`
  - `dollar.tf`
  - `dollar.tf.ss08`
  - `cent`
  - `cent.ss08`
  - `cent.tf.ss08`
- [ ] Keep `d`, `e`, `r`, and `u` in a donor-drift bucket, not a freeze bucket.

## Phase 6: Validation lock

- [ ] Require every reported glyph to pass:
  - source compatibility
  - interpolatable scan
  - sampled instance-risk scan
  - exact-master fidelity threshold
  - same-outline freeze gate
  - Glyphs visual spot check
- [ ] Add a regression summary for both families that lists:
  - still frozen by design
  - temporarily frozen by fallback
  - donor-faithful and approved

## Team split

### Team Alpha: live-source audit

- [ ] Maintain the freeze detector.
- [ ] Confirm which glyphs are identical across masters after each run.
- [ ] Flag any new accidental freezes immediately.

### Team Beta: donor forensics

- [ ] Own merge/split and contour-reorder analysis.
- [ ] Produce donor structure summaries for the roman and italic reported sets.
- [ ] Hand off donor repair recommendations to Team Gamma.

### Team Gamma: pipeline and strategy engine

- [ ] Add the new strategy taxonomy.
- [ ] Add family-specific cluster evidence reports.
- [ ] Add the fidelity and freeze gates.

### Team Delta: glyph repair

- [ ] Repair true redraw cases.
- [ ] Build safer contour substitutions for medium cases.
- [ ] Verify the repaired masters in Glyphs before freezing strategies.

## Immediate order

- [ ] Add freeze detection to the repair runner.
- [ ] Generate roman cluster evidence and planner reports.
- [ ] Restore italic from a pre-fallback backup before further repair work.
- [ ] Remove unsafe freeze/localized substitutions from the italic cluster.
- [ ] Re-run both families from the donor-preserving baseline.
- [ ] Start with the highest-value donor mismatch classes:
  - roman `uni021B`, `napostrophe`, `tcommaaccent`, `dollar/cent` families
  - italic `a`, `dollar/cent` families, `tcommaaccent`, `uni021B`
