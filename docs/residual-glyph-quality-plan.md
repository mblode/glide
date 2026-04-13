# Residual Glyph Quality Plan

This plan covers the current residual problem glyphs in:

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
- `dollar.tf`
- `cent.tf`
- `dollar.ss08`
- `cent.ss08`
- `dollar.tf.ss08`
- `cent.tf.ss08`

Roman reported set:

- `d`
- `r`
- `u`
- `dollar`
- `cent`
- `ncommaaccent`
- `napostrophe`
- `tcommaaccent`
- `uni021B`
- `dollar.tf`
- `cent.tf`
- `r.ss03`
- `racute.ss03`
- `rcommaaccent.ss03`
- `rcaron.ss03`
- `dollar.ss08`
- `cent.ss08`
- `dollar.tf.ss08`
- `cent.tf.ss08`

## Research status

- [x] Live-source audit completed for the full roman and italic residual sets.
- [x] Current repair reports reviewed:
  - [roman-source-report.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/roman-source-report.json)
  - [italic-source-report.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/italic-source-report.json)
  - [roman-designspace-interpolatable.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/roman-designspace-interpolatable.json)
  - [italic-designspace-interpolatable.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/italic-designspace-interpolatable.json)
  - [roman-instance-risk-report.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/roman-instance-risk-report.json)
  - [italic-instance-risk-report.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/italic-instance-risk-report.json)
  - [roman-master-validation.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/roman-master-validation.json)
  - [italic-master-validation.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/italic-master-validation.json)
- [x] Raw donor structure reviewed against [cabinet/Circular](/Users/mblode/Code/mblode/glide/cabinet/Circular).
- [x] Official external references checked:
  - Glyphs Handbook PDF: brace layers and alternate layers in variable fonts
  - fontTools `varLib.interpolatable` docs

## Bottom line

The problem has changed.

- [x] The residual glyphs are no longer exact-outline frozen across masters.
- [x] Source compatibility is currently clean in both families.
- [x] The remaining failure mode is now quality, not basic compatibility.

That quality failure splits four ways:

1. `weighted_fallback` is acceptable and should stay as the automation strategy.
2. `weighted_fallback` is structurally correct but needs tuning.
3. The glyph should stay variable, but needs brace or intermediate logic rather than scalar fallback.
4. The glyph needs a real redraw or explicit alternate-shape switching because the donor construction changes too much.

## Current source state

### Structural status

- [x] Roman strict source audit: `0` path order, `0` node count, `0` start, `0` post-write mismatches
- [x] Italic strict source audit: `0` path order, `0` node count, `0` start, `0` post-write mismatches
- [x] All glyphs in the reported residual sets vary across masters now

### Remaining live risk in the reported sets

Roman residual sampled-risk set:

- `d`
- `r`
- `u`
- `napostrophe`
- `uni021B`

Italic residual sampled-risk set:

- `a`
- `g`
- `r`
- `t`
- `u`
- `dollar`
- `ampersand`
- `two`
- `napostrophe`
- `uni021B`
- `dollar.tf`
- `dollar.ss08`
- `cent.ss08`
- `dollar.tf.ss08`

## External guidance

The relevant implementation guidance is consistent:

- [fontTools interpolatable docs](https://fonttools.readthedocs.io/en/latest/varLib/interpolatable.html): use this to detect wrong contour order and other interpolatability failures.
- [Glyphs Handbook PDF](https://handbook.glyphsapp.com/en/Glyphs%20Handbook.pdf): use brace layers when one glyph needs intermediate correction inside an otherwise working interpolation model.
- [Glyphs Handbook PDF](https://handbook.glyphsapp.com/en/Glyphs%20Handbook.pdf): use alternate layers and variable-font shape switching when a glyph changes construction, such as a dollar sign losing its stroke or a form-changing `a` or `g`.

## Repair buckets

### Bucket A: Keep structural fallback for true donor collapse or split

These donor sets are incompatible enough that the pipeline should keep a structural fallback strategy as the default automated path.

Roman:

- `dollar`
- `cent`
- `tcommaaccent`
- `dollar.tf`
- `cent.tf`
- `dollar.ss08`
- `cent.ss08`
- `dollar.tf.ss08`
- `cent.tf.ss08`

Italic:

- `dollar`
- `cent`
- `tcommaaccent`
- `dollar.tf`
- `cent.tf`
- `dollar.ss08`
- `cent.ss08`
- `dollar.tf.ss08`
- `cent.tf.ss08`

Why:

- donor contour-count collapse in the dollar and cent families
- split-versus-merged donor construction in `tcommaaccent`

### Bucket A2: Keep export-safety fallback

These glyphs are not raw donor impossibilities, but they already have a known export-safety history and should stay isolated from the normal interpolation path until there is a better targeted fix.

Roman:

- `ncommaaccent`

Italic:

- `ncommaaccent`

Why:

- raw donor normalization is possible
- current fallback choice is driven by export stability, not by an unavoidable donor collapse

### Bucket B: Tune weighted fallback

These glyphs are structurally quiet in the designspace report, but still show sampled small-segment or exact-master drift that suggests the current fallback transform is too naive.

Roman:

- `d`
- `r`
- `u`
- `ncommaaccent`
- `napostrophe`
- `uni021B`

Italic:

- `r`
- `s`
- `t`
- `percent`
- `two`
- `ncommaaccent`
- `napostrophe`
- `dollar.tf.ss08`
- `cent.tf.ss08`

Target fix:

- improve transform logic
- preserve donor sidebearings and bbox center more faithfully
- optionally apply contour-specific scaling instead of whole-glyph scaling

### Bucket C: Brace-layer or intermediate-master candidates

These glyphs still want a variable shape, but the current global weighted fallback is too crude. They are candidates for generated intermediate or brace layers in the `.glyphs` source.

Roman:

- `d`
- `u`
- `napostrophe`
- `uni021B`

Italic:

- `a`
- `r`
- `s`
- `t`
- `u`
- `percent`
- `two`
- `napostrophe`

Target fix:

- keep the three-master source
- synthesize brace layers at one or more internal weights
- keep the fallback topology, but correct the weight-specific geometry

### Bucket D: Alternate-shape or redraw required

These glyphs are poor candidates for a single scalar fallback and should not be treated as simple transform problems.

Roman:

- `r.ss03`
- `racute.ss03`
- `rcommaaccent.ss03`
- `rcaron.ss03`

Italic:

- `g`
- `ampersand`
- `cent`
- `uni021B`
- `dollar.ss08`
- `cent.ss08`

Why:

- the `ss03 r` cluster changes between merged and split construction by weight
- italic `g` and `ampersand` still show donor-form complexity beyond the current fallback model
- some italic alternates have acceptable compatibility but unacceptable exact-master drift

Target fix:

- explicit alternate-shape switching or bracket logic
- real redraw if donor fidelity matters more than full automation

## Detailed findings

### Roman

- [x] `d` now varies across masters and no longer throws designspace issues, but it still shows sampled min-segment risk at all five sampled weights.
- [x] `r` has raw donor compatibility but still shows sampled min-segment risk at all sampled weights, which suggests the current weighted fallback is over-correcting a glyph that should probably stay closer to the donor.
- [x] `u` has no remaining designspace issue types, but still shows sampled min-segment risk through `675`.
- [x] `ncommaaccent` is not a donor-side hard failure. Raw donors can be normalized, so its current fallback is an export-safety choice and should be tracked separately from the dollar and cent collapse classes.
- [x] `napostrophe` and `uni021B` are structurally stable under weighted fallback, but still show persistent sampled min-segment risk.
- [x] `r.ss03`, `racute.ss03`, `rcommaaccent.ss03`, and `rcaron.ss03` are currently quiet only because they are effectively structural fallback glyphs. They need their own bucket and should not be treated as successfully normalized.

### Italic

- [x] `a`, `g`, `u`, and `ampersand` are the strongest “quality not compatibility” failures.
- [x] `r`, `t`, `two`, `napostrophe`, and `uni021B` are structurally stable but still too fragile in sampled instances.
- [x] `ncommaaccent` is currently quiet and can likely stay in an export-safety fallback bucket unless a donor-faithful rebuild becomes necessary.
- [x] `percent` is interpolatable-clean now, but still wants review because donor contour order changes at the heavy end.
- [x] `dollar`, `dollar.tf`, `dollar.ss08`, `cent.ss08`, and `dollar.tf.ss08` are stable under weighted fallback but still carry quality drift that should be treated separately from compatibility.

## Phase 1: Freeze evidence and extend reporting

- [x] Confirm that the residual sets are no longer exact-outline frozen.
- [ ] Add a dedicated `repair_bucket` report for the new roman and italic residual sets.
- [ ] Add sampled min-segment thresholds to the source summary so risk is visible without opening the instance report.
- [ ] Add a specific `structural_fallback` classification distinct from `weighted_fallback`.
- [ ] Flag glyphs like the roman `ss03 r` cluster when the live source is quiet only because the donor construction was replaced.

## Phase 2: Split structural fallback from geometric tuning

- [ ] Create a separate manifest strategy:
  - `structural_fallback`
- [ ] Move these glyphs out of generic `weighted_fallback`:
  - roman `r.ss03`
  - roman `racute.ss03`
  - roman `rcommaaccent.ss03`
  - roman `rcaron.ss03`
- [ ] Consider moving these if they remain topology-preserving only:
  - roman `dollar`
  - roman `cent`
  - italic `dollar`
  - italic `cent`
- [ ] Keep `weighted_fallback` for glyphs where a scalar or contour-wise transform can still improve quality.

## Phase 3: Improve the fallback transform

- [ ] Change the transform model from whole-glyph scale only to contour-aware scaling and translation.
- [ ] Preserve the reference master exactly.
- [ ] Respect donor bbox, contour centroid, and contour count separately.
- [ ] Add a pass for accent/base contour alignment in multi-contour glyphs.
- [ ] Re-run the residual sets and compare:
  - sampled min-segment risk
  - exact-master area drift
  - point deviation at master weights

## Phase 4: Generate brace-layer candidates

- [ ] Add a brace-layer planner for glyphs in Bucket C.
- [ ] Emit proposed brace coordinates for each glyph based on current risk peaks.
- [ ] Start with:
  - roman `d`
  - roman `u`
  - roman `napostrophe`
  - italic `a`
  - italic `r`
  - italic `s`
  - italic `t`
  - italic `u`
  - italic `percent`
  - italic `two`
- [ ] Write generated brace layers into copied working sources before touching the main `.glyphs` files.
- [ ] Validate with:
  - `fonttools varLib.interpolatable`
  - sampled instances
  - exact-master donor checks

## Phase 5: Alternate-shape switching and redraw track

- [ ] Build a separate action track for Bucket D.
- [ ] Start with the roman `ss03 r` cluster:
  - decide whether to keep the split `Book` construction or introduce alternate switching
- [ ] Start with italic:
  - `g`
  - `ampersand`
  - `cent`
  - `uni021B`
  - `dollar.ss08`
  - `cent.ss08`
- [ ] For each, decide:
  - alternate-layer switching
  - bracket logic
  - true redraw
- [ ] Do not keep pushing scalar fallback on these glyphs.

## Phase 6: Validation gates

- [ ] Add a residual-glyph CI-style validator in `packages/variable-gen`.
- [ ] Fail when a tracked glyph regresses to exact-outline freeze.
- [ ] Fail when a tracked glyph exceeds sampled min-segment thresholds.
- [ ] Fail when a tracked glyph exceeds agreed exact-master area-drift thresholds.
- [ ] Emit a compact markdown review packet for only the tracked residual sets.

## Suggested execution order

1. Reclassify the roman `ss03 r` cluster as `structural_fallback`.
2. Implement contour-aware fallback tuning for Bucket B.
3. Generate brace-layer candidates for Bucket C.
4. Move Bucket D to explicit alternate-shape or redraw work.
5. Add validation gates so the same regressions do not come back.

## Success criteria

- [ ] No tracked residual glyph regresses to exact-outline freeze.
- [ ] No tracked residual glyph shows `interpolatable` issues.
- [ ] Sampled small-segment risk is eliminated or explicitly accepted per glyph.
- [ ] Structural fallback glyphs are explicitly labeled as such.
- [ ] Brace-layer and redraw candidates are isolated instead of mixed into generic fallback logic.
