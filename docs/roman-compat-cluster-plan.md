# Roman Compatibility Cluster Plan

Scope:

- Source: [glide-variable.glyphs](/Users/mblode/Code/mblode/glide/glide-variable.glyphs)
- Cluster: `deruv$&2369¢«µ»½¾æèéêëùúûüďđēĕėęġĲĳŀņŉœŕŗřŞşţťŧūŭůűųƏ`

## Phase 1: Research And Audit

- [x] Map the character string to live Glide glyph names.
- [x] Audit the live roman source for path-count, node-count, start-point, and winding mismatches.
- [x] Review current repair reports to separate true source incompatibility from `underweight`/`kink` quality risk.
- [x] Check official guidance from Glyphs and fontTools for compatible interpolation requirements.

## Phase 2: Manifest And Cluster Coverage

- [x] Add manifest support for explicit glyph clusters driven by literal character strings.
- [x] Add manifest support for derived-family inheritance so `d`, `r`, and `u` families can share fallback strategy and brace planning.
- [x] Add the April 2026 roman compatibility cluster to the manifest so these glyphs stay visible in the repair reports.
- [x] Add inherited handling for safe accent-derived forms in the `d`, `e`, `r`, `u`, and `t` clusters.
- [x] Restrict inherited-contour handling to safe extra-contour derivatives so integrated forms like `dslash` and `uogonek` do not lose their built-in constructions.
- [x] Add safe accent-derived inheritance for the `e*` and `tcaron` forms.

## Phase 3: Structural Validation Gates

- [x] Record per-glyph source audit counts for:
  - path order
  - node count
  - start points
  - path direction
- [x] Teach the tracked-glyph validator to fail on source-structure regressions, not only area drift and interpolatable warnings.
- [x] Surface group and inheritance provenance in the tracked review output.

## Phase 4: Remaining Repair Work

- [ ] Re-run the roman repair pipeline so the new cluster metadata is baked into fresh source reports.
- [ ] Review the expanded tracked report and split the cluster into:
  - pure tracking only
  - weighted-fallback candidates
  - structural-fallback candidates
  - redraw candidates
- [ ] Decide whether roman `ampersand`, `two`, `three`, `six`, and `nine` should be promoted out of `normalize`.
- [ ] Decide whether `e` and the `e*` derivatives need fallback logic or should remain normalize-only with stricter reporting.

## Team Split

- [x] Team Alpha: live-source audit complete.
- [x] Team Beta: report forensics complete.
- [x] Team Gamma: manifest expansion and validator changes complete.
- [ ] Team Delta: glyph-level quality tuning still pending.
