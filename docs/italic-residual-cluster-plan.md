# Italic Residual Cluster Plan

This plan covers the remaining problematic glyphs in `/Users/mblode/Code/mblode/glide/glide-variable-italic.glyphs`:

- `X`
- `a`
- `g`
- `r`
- `s`
- `t`
- `u`
- `percent`
- `ampersand`
- `two`

## Bottom line

The cluster is not failing because the three italic masters are still structurally incompatible. The current source is already aligned for path count, node count, contour direction, and start points. The remaining failures are in the repaired topology itself: donor drift, `underweight`, `kink`, and a few sampled self-intersections.

## Evidence summary

- All 10 glyphs are still `manual_review` in `packages/variable-gen/reports/repair/italic-source-report.json`.
- Raw donor forensics show that none of the 10 glyphs are “false positives” caused only by the source file.
- `X` is the mildest case:
  - raw donor mismatch is small
  - no active designspace issue in `italic-designspace-interpolatable.json`
- `a` is the hardest donor case:
  - raw donor contours drift from `5+12` to `4+11` to `11+4`
  - `ExtraBlackItalic` effectively flips contour roles relative to `BookItalic`
- `a`, `g`, `s`, `u`, and `ampersand` carry both `kink` and `underweight` in `italic-designspace-interpolatable.json`.
- `r`, `t`, `percent`, and `two` are mostly `underweight`.
- `percent` is a real reorder case even though it is low magnitude:
  - the slash contour moves from last to first in `ExtraBlackItalic`
- Midpoint instance risk is concentrated in:
  - `g` with intersections around the light-side sample
  - `ampersand` with intersections around the heavy-side sample
  - `two` with intersections at both midpoint samples
- Exact-master drift already shows donor mismatch even at axis endpoints:
  - `u` has `11.77%` area drift at `wght 100`
  - `s` has `10.27%` area drift at `wght 400`
  - `g` has `4.08%` to `4.58%` area drift
  - `ampersand` has `1.32%` to `2.22%` area drift
  - `a` has `1.35%` to `1.58%` area drift

## Repair buckets

| Bucket | Glyphs | Why | Expected action |
| --- | --- | --- | --- |
| Freeze candidates | `X`, `r`, `percent` | Low-delta or single-warning glyphs | Test `reference_fallback` or `freeze_to_reference` first |
| Curve-balance repairs | `s`, `t`, `u` | Mostly `underweight` and localized `kink` on a single contour | Add localized contour correction and resample |
| High-risk redraw candidates | `a`, `g`, `ampersand`, `two` | Repeated donor drift, heavier topology surgery, midpoint failures | Prefer redraw/substitution over more blind normalization |

## Donor complexity order

Use this order when allocating repair time:

1. `a`
2. `ampersand`
3. `two`
4. `g`
5. `u`
6. `s`
7. `percent`
8. `t`
9. `X`
10. `r`

## Current execution result

- [x] Generated cluster evidence report:
  - `packages/variable-gen/reports/repair/italic-residual-cluster-evidence.json`
- [x] Generated exception plan report:
  - `packages/variable-gen/reports/repair/italic-residual-cluster-plan.json`
- [x] Planner output summary:
  - `keep_normalized`: `1`
  - `keep_under_review`: `2`
  - `localized_substitution`: `3`
  - `manual_redraw_required`: `4`
- [x] Applied automated fallback strategies to the full 10-glyph cluster.
- [x] Rebuilt the italic variable font and reran source, interpolatable, and instance-risk reports.
- [x] The 10-glyph cluster now has:
  - `0` interpolatable warnings
  - `0` sampled intersections
  - `0` source compatibility issues
- [ ] Exact-master donor fidelity is still compromised for several fallback glyphs, especially:
  - `r`
  - `s`
  - `t`
  - `u`
  - `two`

## Phase 1: Freeze the evidence

- [x] Snapshot the current evidence for the 10-glyph cluster into a dedicated report subset.
- [x] Record, per glyph:
  - donor raw structure
  - current normalized structure
  - interpolatable issue types
  - sampled intersection counts
  - exact-master area drift
- [x] Extend the manifest so these glyphs are no longer just `manual_review`.
- [x] Add a `repair_bucket` field for:
  - `freeze_candidate`
  - `curve_balance`
  - `redraw_candidate`

## Phase 2: Add a real exception planner

- [x] Add a post-report decision pass in `packages/variable-gen/scripts/repair_circular_sources.py`.
- [x] Make that pass read:
  - `italic-source-report.json`
  - `italic-designspace-interpolatable.json`
  - `italic-instance-risk-report.json`
  - `italic-master-validation.json`
- [x] Emit one explicit action per glyph instead of leaving the cluster at `manual_review`.
- [x] Support these actions in the plan:
  - `freeze_to_reference`
  - `localized_substitution`
  - `manual_redraw_required`

## Phase 3: Solve the easy wins first

- [x] Try `freeze_to_reference` for `X`.
- [x] Test `freeze_to_reference` for `r`.
- [x] Test `freeze_to_reference` for `percent`.
- [x] Rebuild and resample after each change.
- [ ] Keep the action only if all of these improve or stay flat:
  - no new designspace issues
  - no new sampled intersections
  - no worse exact-master area drift
  - current result: interpolation risk improved, donor fidelity did not

## Phase 4: Localized contour repair

- [x] Add targeted repair hooks for `s`, `t`, and `u`.
- [x] Restrict the repair to the flagged contour indices from `italic-designspace-interpolatable.json`.
- [ ] Add a threshold gate so the repair only runs when:
  - `underweight`
  - `kink`
  - tiny-segment collapse
  are present
- [x] Resample `wght 100`, `250`, `400`, `675`, and `950` after each repair.
- [ ] Promote any glyph that clears all checks from `curve_balance` to `approved`.
  - current result: approved for stability only, not for donor fidelity

## Phase 5: Redraw-heavy glyphs

- [x] Treat `a`, `g`, `ampersand`, and `two` as redraw candidates, not normalization candidates.
- [x] Extract side-by-side donor traces for the three masters.
- [x] Decide per glyph between:
  - keeping the current normalized outline
  - rebuilding one contour from the donor logic
  - freezing a contour or entire glyph
  - adding a manual replacement master shape
- [x] Start with `g` and `two` because they already show sampled intersections.
- [x] Move to `ampersand`, then `a`.
  - result: automated safety fallbacks were applied instead of true redraws

## Phase 6: Validation lock

- [x] Re-run the full repair pipeline after each bucket lands.
- [ ] Require the cluster to pass all of:
  - source compatibility
  - designspace interpolatable scan
  - sampled instance-risk scan
  - Glyphs export spot check
  - current result: first three pass, Glyphs visual/export spot check still pending
- [x] Write the final chosen action for each glyph back into `packages/variable-gen/manifests/circular-triage.json`.
- [ ] Mirror any successful automation pattern into the roman pipeline if the same glyph class appears there.
  - not executed in this pass

## Team split

### Team Alpha: donor forensics

- [ ] Extract raw donor topology for the 10 glyphs.
- [ ] Mark which contours are drifting versus being force-normalized.
- [ ] Hand off contour-level notes to Team Gamma.

### Team Beta: interpolation QA

- [x] Maintain the cluster-only interpolatable summary.
- [x] Track sampled intersections and tiny segments by weight.
- [ ] Gate merges on no-regression metrics.
  - metrics are available, but no hard gate was added yet

### Team Gamma: repair engine

- [x] Implement the exception planner.
- [x] Add `freeze_to_reference` and `localized_substitution`.
- [ ] Add cluster-only rerun support.
  - bucketed reports exist, but there is no dedicated cluster-only CLI mode yet

### Team Delta: manual shape review

- [ ] Review `a`, `g`, `ampersand`, and `two`.
- [ ] Approve redraw versus substitution per glyph.
- [ ] Confirm the winning outlines in Glyphs before freezing the manifest.
  - still needs a human visual review because the current solution favors stability over fidelity

## Immediate order

- [x] Reclassify the 10 glyphs into the three repair buckets.
- [x] Implement the exception planner in `repair_circular_sources.py`.
- [x] Test `freeze_to_reference` on `X`, `r`, and `percent`.
- [x] Add localized repair for `s`, `t`, and `u`.
- [x] Start redraw review with `g` and `two`.
