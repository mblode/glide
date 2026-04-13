# Roman E2369 Extended Interpolation Plan

Scope:

- Source: [glide-variable.glyphs](/Users/mblode/Code/mblode/glide/glide-variable.glyphs)
- Audit target: in-between failures across Thin -> Regular and Regular -> ExtraBlack
- Requested chars: `e2369` and `µ»½¾æèéêëđēĕėęġņŉœŕŗřŞşţťŧūŭůűųƏ`
- Resolved glyph names: `e`, `two`, `three`, `six`, `nine`, `mu`, `guillemotright`, `onehalf`, `threequarters`, `ae`, `egrave`, `eacute`, `ecircumflex`, `edieresis`, `dslash`, `emacron`, `ebreve`, `edotaccent`, `eogonek`, `gdotaccent`, `ncommaaccent`, `napostrophe`, `oe`, `racute`, `rcommaaccent`, `rcaron`, `Scedilla`, `scedilla`, `tcommaaccent`, `tcaron`, `tbar`, `umacron`, `ubreve`, `uring`, `uhungarumlaut`, `uogonek`, `uni018F`

## Research Basis

- [x] Confirmed Glyphs compatibility guidance: path order, component order, node count, and path direction need to stay compatible before interpolation repair work.
- [x] Confirmed Glyphs cleanup guidance: path direction, start-point order, and extremes are first-line fixes before deeper redraw/fallback work.
- [x] Confirmed fontTools `varLib.interpolatable` remains the primary diagnostic for contour-order, kink, and underweight issues in the designspace.
- [x] Confirmed from the current Glide reports that this request set has no active source-structure mismatches in the roman masters; the remaining work is in-between interpolation risk and strategy coverage.

Primary sources:

- Glyphs outline compatibility: https://handbook.glyphsapp.com/interpolation/outline-compatibility/
- Glyphs interpolation overview: https://handbook.glyphsapp.com/interpolation/
- Glyphs path editing, direction, and extremes: https://handbook.glyphsapp.com/editing-paths/
- fontTools interpolatable docs: https://fonttools.readthedocs.io/en/latest/varLib/interpolatable.html

## Current Evidence

- [x] Current active interpolatable subset: `two`, `three`, `six`, `nine`, `guillemotright`, `threequarters`, `scedilla`, `tcaron`, `uhungarumlaut`, `uni018F`
- [x] Highest-signal current blockers by focus score:
  - `six` (`underweight`, worst intersection count in this request set)
  - `nine` (`underweight`, worst intersection count in this request set)
  - `two`
  - `scedilla`
  - `tcaron`
  - `uhungarumlaut`
  - `uni018F`
  - `napostrophe`
  - `threequarters`
  - `three`
- [x] Current sampled-only subset: `e`, `onehalf`, `ae`, `egrave`, `eacute`, `ecircumflex`, `edieresis`, `dslash`, `emacron`, `ebreve`, `edotaccent`, `eogonek`, `gdotaccent`, `napostrophe`, `oe`, `racute`, `rcaron`, `Scedilla`, `tbar`, `umacron`, `ubreve`, `uring`, `uogonek`
- [x] Currently clean in the focused roman audit: `mu`, `ncommaaccent`, `rcommaaccent`, `tcommaaccent`
- [x] Missing targeted manifest coverage beyond the broad compat-cluster tracking: `e`, `three`, `six`, `nine`, `guillemotright`, `onehalf`, `threequarters`, `ae`, `gdotaccent`, `oe`, `scedilla`, `tbar`, `uni018F`
- [x] Existing explicit fallback coverage already present: `dslash`, `eogonek`, `napostrophe`, `Scedilla`, and `uogonek` are already on non-normalize fallback paths, so those should be tuned rather than reclassified from scratch.
- [x] Existing dependency groups already in the manifest:
  - `e` -> `egrave`, `eacute`, `ecircumflex`, `edieresis`, `emacron`, `ebreve`, `edotaccent`
  - `r` -> `racute`, `rcommaaccent`, `rcaron`
  - `u` -> `umacron`, `ubreve`, `uring`, `uhungarumlaut`
  - `t` -> `tcaron`
- [x] Integrated same-contour forms that should not use `inherit_base_contours`: `dslash`, `eogonek`, `Scedilla`, `scedilla`, `tbar`, `uogonek`

## Phase 1: Strategy Ownership

- [ ] Snapshot the requested glyph set from [roman-variable-audit-interpolation-only.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/audit/roman/roman-variable-audit-interpolation-only.json) into a dedicated per-cluster checklist report.
- [ ] Promote the normalize-only risk glyphs to explicit manifest ownership in [circular-triage.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/manifests/circular-triage.json): `e`, `three`, `six`, `nine`, `guillemotright`, `onehalf`, `threequarters`, `ae`, `gdotaccent`, `oe`, `scedilla`, `tbar`, `uni018F`.
- [ ] Decide which of those explicit entries should be `weighted_fallback`, `structural_fallback`, `manual_review`, or `donor_copy` candidates.
- [ ] Leave `mu`, `ncommaaccent`, `rcommaaccent`, and `tcommaaccent` on watch-only status unless the next audit shows regression.

Exit criteria:

- [ ] Every non-clean requested glyph has explicit strategy ownership rather than only broad compat-cluster tracking.

## Phase 2: Highest-Signal Interpolatable Blockers

- [ ] Repair the numeral cluster first: `six`, `nine`, `two`, `three`.
- [ ] Repair `threequarters` after the numeral donors are stable.
- [ ] Repair `scedilla`, `tcaron`, `uhungarumlaut`, and `uni018F`.
- [ ] Repair `guillemotright` only if it still fails after the next explicit-manifest pass; raw donor copy is a plausible option here because it is structurally safer than the other requested raw donor candidates.
- [ ] Re-run the focused roman audit after each mini-batch instead of waiting for the full cluster pass.

Exit criteria:

- [ ] `interpolatable issue_count == 0` for `six`, `nine`, `two`, `three`, `threequarters`, `scedilla`, `tcaron`, `uhungarumlaut`, `uni018F`, and `guillemotright`.

## Phase 3: Base-Driven Derived Families

- [ ] Stabilize base `e` before touching the `roman-e-accent-derived` group.
- [ ] Re-check `egrave`, `eacute`, `ecircumflex`, `edieresis`, `emacron`, `ebreve`, and `edotaccent` after the `e` base pass.
- [ ] Re-check the `u`-derived group after `uhungarumlaut` is clean: `umacron`, `ubreve`, `uring`.
- [ ] Re-check the `r`-derived group last because `r` is already on donor copy and `rcommaaccent` is currently clean.
- [ ] Decide whether `gdotaccent`, `ae`, and `oe` belong with this base-driven pass or need independent explicit repair entries.

Exit criteria:

- [ ] No requested derived glyph is still inheriting from an unrepaired base strategy.
- [ ] The `e*`, `r*`, and `u*` families no longer show new in-between regressions after their base passes.

## Phase 4: Integrated Same-Contour Forms

- [ ] Repair `dslash`, `eogonek`, `Scedilla`, `tbar`, and `uogonek` as whole-glyph cases.
- [ ] Keep `scedilla` separate from `Scedilla` if the lowercase cedilla still needs a different contour solution.
- [ ] Use `weighted_fallback`, `structural_fallback`, or targeted contour substitution for these glyphs; do not route them through `inherit_base_contours`.
- [ ] Add brace weights only where the sampled-risk concentrations justify them.

Exit criteria:

- [ ] Integrated forms no longer rely on derived-family inheritance assumptions.
- [ ] No repeated intersection or zero-ink failures remain for these glyphs across the sampled in-between weights.

## Phase 5: Residual Sampled-Only Cleanup

- [ ] Re-check `napostrophe`, `onehalf`, `ae`, `oe`, and `gdotaccent` after the earlier dependency passes.
- [ ] Re-check `e`, `Scedilla`, `dslash`, `eogonek`, `tbar`, and `uogonek` for short-segment-only residuals.
- [ ] Decide which residual short-segment warnings are acceptable donor drift and which still need geometry cleanup.

Exit criteria:

- [ ] Remaining warnings in this request set, if any, are explicitly reviewed residuals rather than unowned failures.

## Phase 6: Acceptance Run

- [ ] Run the repair pipeline on roman after the cluster fixes land.
- [ ] Export the variable TTF from the roman source.
- [ ] Run the all-glyph audit with focus on the requested subset and both interpolation spans.
- [ ] Record the before/after delta for this cluster in a dedicated summary.

Acceptance command set:

- [ ] `.venv/bin/python packages/variable-gen/scripts/repair_circular_sources.py --font roman --skip-import`
- [ ] `.venv/bin/python packages/variable-gen/scripts/audit_variable_font.py --family roman --interpolation-only`

Acceptance criteria:

- [ ] Requested glyph set has `interpolatable issue_count == 0`.
- [ ] Requested glyph set has no sampled intersections or zero-ink failures in Thin -> Regular or Regular -> ExtraBlack.
- [ ] Any residual short-segment-only warnings are documented and intentionally accepted.

## Team Split

- [x] Team Research: primary-source interpolation guidance gathered and verified.
- [x] Team Audit: requested glyphs mapped, ranked, and cross-checked against current roman reports.
- [ ] Team Numerals And Fractions: `two`, `three`, `six`, `nine`, `onehalf`, `threequarters`, `guillemotright`
- [ ] Team Derived Families: `e`, `e*`, `r*`, `u*`, `tcaron`
- [ ] Team Integrated Forms: `dslash`, `eogonek`, `Scedilla`, `scedilla`, `tbar`, `uogonek`, `uni018F`
- [ ] Team Residual Composites: `ae`, `oe`, `gdotaccent`, `napostrophe`
