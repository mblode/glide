# Roman e2369 Extended Cluster Plan

Scope:

- Source: [glide-variable.glyphs](/Users/mblode/Code/mblode/glide/glide-variable.glyphs)
- Requested chars: `e2369µ»½¾æèéêëđēĕėęġņŉœŕŗřŞşţťŧūŭůűųƏ`
- Mapped glyphs: `e`, `two`, `three`, `six`, `nine`, `mu`, `guillemotright`, `onehalf`, `threequarters`, `ae`, `egrave`, `eacute`, `ecircumflex`, `edieresis`, `dslash`, `emacron`, `ebreve`, `edotaccent`, `eogonek`, `gdotaccent`, `ncommaaccent`, `napostrophe`, `oe`, `racute`, `rcommaaccent`, `rcaron`, `Scedilla`, `scedilla`, `tcommaaccent`, `tcaron`, `tbar`, `umacron`, `ubreve`, `uring`, `uhungarumlaut`, `uogonek`, `uni018F`

## Research Basis

- [x] Re-ran the live roman interpolation audit from [audit_variable_font.py](/Users/mblode/Code/mblode/glide/packages/variable-gen/scripts/audit_variable_font.py) on 2026-04-08:
  - `.venv/bin/python packages/variable-gen/scripts/audit_variable_font.py --family roman --interpolation-only`
- [x] Rechecked the active roman repair strategy and donor-compat metadata in [circular-triage.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/manifests/circular-triage.json) and [roman-source-report.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/roman-source-report.json)
- [x] Reviewed Glyphs primary docs:
  - Outline compatibility: <https://handbook.glyphsapp.com/interpolation/outline-compatibility/>
  - Interpolation overview: <https://handbook.glyphsapp.com/interpolation/>
- [x] Reviewed fontTools primary docs and implementation:
  - `varLib.interpolatable`: <https://fonttools.readthedocs.io/en/latest/varLib/interpolatable.html>
  - Source: <https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/interpolatable.py>

Key research takeaways:

- Glyphs requires the same path count, node order, anchors, components, and overall path/component order across masters.
- Glyphs explicitly treats `Correct Path Direction` as the first fix because it normalizes winding, start points, and shape order.
- fontTools `varLib.interpolatable` is the right source for the current report vocabulary:
  - `underweight` is a midpoint contour-size failure against the expected geometric-mean size.
  - `kink` is a visible smooth-point interpolation defect caused by handle-ratio or angle mismatch even when the contours are formally compatible.

## Current Evidence

Live roman audit summary from [roman-variable-audit-interpolation-only.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/audit/roman/roman-variable-audit-interpolation-only.json):

- `total_glyphs=754`
- `problem_glyphs=274`
- `interpolatable_problem_glyphs=76`
- `sampled_risky_glyphs=265`
- `glyphs_with_intersections=24`
- `thin_to_regular span problems=248`
- `regular_to_extrablack span problems=228`

Requested-cluster priority ranking by current severity:

- Tier 1: `six` `395`, `nine` `320`, `napostrophe` `315`, `two` `295`, `scedilla` `295`, `tcaron` `295`, `uhungarumlaut` `295`, `uni018F` `295`
- Tier 2: `threequarters` `265`, `three` `250`, `eogonek` `235`, `gdotaccent` `200`
- Tier 3 but still both-span risky: `e`, `ae`, `dslash`, `Scedilla`, `oe`, `onehalf`, `tbar`, `egrave`, `eacute`, `ecircumflex`, `edieresis`, `emacron`, `ebreve`, `edotaccent`, `racute`, `rcaron`, `umacron`, `ubreve`, `uring`
- Lower current signal: `uogonek` `120`, `guillemotright` `115`
- Currently not showing focused interpolation issues in the latest report: `mu`, `ncommaaccent`, `rcommaaccent`, `tcommaaccent`

Important strategy evidence from [roman-source-report.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/roman-source-report.json):

- Raw donor copy is only obviously safe in this requested set for `guillemotright`.
- The main base shapes in scope are not raw-donor-compatible across masters: `e`, `two`, `three`, `six`, `nine`, `ae`, `oe`, `Scedilla`, `scedilla`, `tcaron`, `uhungarumlaut`, `uogonek`, `uni018F`, `dslash`, `eogonek`
- Already promoted out of generic normalize:
  - `dslash`, `eogonek`, `Scedilla`, `uogonek`, `ncommaaccent`, `napostrophe` -> `weighted_fallback`
  - `tcommaaccent` -> `structural_fallback`
  - `tcaron`, `racute`, `rcommaaccent`, `rcaron`, `umacron`, `ubreve`, `uring`, `uhungarumlaut`, `egrave`, `eacute`, `ecircumflex`, `edieresis`, `emacron`, `ebreve`, `edotaccent` -> `inherit_base_contours`
- Still under-covered for their current risk level:
  - `e`, `three`, `six`, `nine`, `mu`, `onehalf`, `threequarters`, `ae`, `gdotaccent`, `oe`, `scedilla`, `tbar`, `uni018F`, `guillemotright`

## Repair Buckets

- Base-shape stabilization:
  - `e`, `two`, `three`, `six`, `nine`, `uni018F`
- Safe derived forms blocked on stable bases:
  - `egrave`, `eacute`, `ecircumflex`, `edieresis`, `emacron`, `ebreve`, `edotaccent`
  - `racute`, `rcommaaccent`, `rcaron`
  - `umacron`, `ubreve`, `uring`, `uhungarumlaut`
  - `tcaron`
- Integrated same-contour or attachment-heavy forms:
  - `dslash`, `eogonek`, `Scedilla`, `scedilla`, `tbar`, `uogonek`, `napostrophe`
- Multi-contour compounds and fractions:
  - `ae`, `oe`, `onehalf`, `threequarters`, `gdotaccent`
- Low-signal tracking only unless the next rerun changes them:
  - `mu`, `guillemotright`, `ncommaaccent`, `tcommaaccent`

## Phase 1: Baseline Lock

- [x] Map the requested character strings to live glyph names.
- [x] Re-run the roman interpolation-only audit from the live source.
- [x] Recheck Glyphs and fontTools primary guidance for interpolation compatibility and defect semantics.
- [x] Pull the current strategy coverage and donor-compat metadata from the roman repair report.
- [ ] Save a compact per-glyph baseline snapshot for this cluster so future passes can diff only the requested set.

Exit criteria:

- The current requested-set baseline is frozen in reports and this plan.

## Phase 2: Base Glyphs First

- [ ] Promote `three`, `six`, `nine`, and `uni018F` out of the broad `normalize` bucket into explicit repair strategies.
- [ ] Compare Thin, Regular, and ExtraBlack layers for `e`, `two`, `three`, `six`, and `nine` in Glyphs master compatibility view.
- [ ] For each of those bases, decide whether the next repair is:
  - manual contour redraw
  - weighted fallback
  - normalized donor-assisted rebuild
- [ ] Fix `six` first because it has the highest score and carries both `underweight` and intersection risk across both spans.
- [ ] Fix `nine` second because it is still intersection-heavy in Thin to Regular.
- [ ] Fix `two` and `three` next because they are feeding the fraction problems.
- [ ] Stabilize `e` before touching the `e*` derivative family again.
- [ ] Re-run the focused audit after the base pass and confirm that the repaired bases no longer carry `interpolatable` warnings.

Exit criteria:

- `e`, `two`, `three`, `six`, `nine`, and `uni018F` have explicit strategies and are no longer the primary `interpolatable` blockers in this cluster.

## Phase 3: Derived Families After Bases

- [ ] Rebuild `egrave`, `eacute`, `ecircumflex`, `edieresis`, `emacron`, `ebreve`, and `edotaccent` from the repaired `e` base and revalidate both spans.
- [ ] Keep `tcaron` blocked on `t` until `t` is manually reviewed, or promote it out of inheritance if the caron form still fails after `t` is stable.
- [ ] Recheck `racute`, `rcommaaccent`, and `rcaron` after the roman `r` donor-copy baseline; if they still fail, isolate the accent geometry rather than the base stem.
- [ ] Recheck `umacron`, `ubreve`, `uring`, and `uhungarumlaut` against the donor-copied `u`; if the failures persist, treat the accent placement/contour geometry as the defect, not the `u` base topology.
- [ ] Decide whether `ae` and `oe` can reuse any repaired `e` bowl logic or whether they need independent whole-glyph treatment.

Exit criteria:

- Safe derived forms are either clean or explicitly reclassified out of inheritance.

## Phase 4: Integrated Forms

- [ ] Keep `dslash`, `eogonek`, `Scedilla`, `uogonek`, and `napostrophe` on whole-glyph fallback paths; do not route them through `inherit_base_contours`.
- [ ] Promote `scedilla` out of generic `normalize` if it still shows the current two-span `kink` profile after the base `s` review.
- [ ] Review `tbar` as an integrated-bar form; do not assume the current normalize path is enough if both-span short-segment risk remains.
- [ ] Split the integrated-form repairs into:
  - contour-order and start-point normalization
  - donor-metric tuning
  - attachment geometry cleanup
- [ ] Re-run only this subgroup after each whole-glyph repair so fallback decisions do not mask regressions.

Exit criteria:

- Integrated forms are no longer relying on inheritance where the added structure is merged into the base contour.

## Phase 5: Compounds, Fractions, And Punctuation

- [ ] Rebuild `onehalf` and `threequarters` only after `two` and `three` are stabilized, so the fraction forms are not repaired from unstable donors.
- [ ] Decide whether `onehalf` and `threequarters` remain normalize-only or need explicit weighted/structural fallback once the numeral bases are fixed.
- [ ] Review `ae` and `oe` as multi-contour compounds with persistent both-span short-segment risk.
- [ ] Review `gdotaccent` as a heavy-span problem tied to the `g` base plus dot placement, not as a simple accent-derived form.
- [ ] Review `guillemotright`; it is the only obviously raw-donor-compatible glyph in this requested set, so it is the cleanest candidate for `donor_copy` or localized substitution if its Thin-span `underweight` warning persists.
- [ ] Keep `mu` in the tracked set but leave it out of the first repair wave unless the next audit rerun surfaces a focused problem again.

Exit criteria:

- Fractions and compounds are no longer blocked by unstable numeral or bowl bases.

## Phase 6: Validation Gates

- [ ] Run [repair_circular_sources.py](/Users/mblode/Code/mblode/glide/packages/variable-gen/scripts/repair_circular_sources.py) after each meaningful phase, not only at the end.
- [ ] Rebuild the roman audit VF and rerun:
  - `.venv/bin/python packages/variable-gen/scripts/audit_variable_font.py --family roman --interpolation-only`
- [ ] Check the requested cluster specifically in:
  - [roman-variable-audit-interpolation-only.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/audit/roman/roman-variable-audit-interpolation-only.json)
  - [roman-source-report.json](/Users/mblode/Code/mblode/glide/packages/variable-gen/reports/repair/roman-source-report.json)
- [ ] Keep `sourceStructureFailures=0` for the requested set.
- [ ] Drive `interpolatable` issues to zero for the base glyphs in this cluster.
- [ ] Eliminate intersection-bearing weights for `six`, `nine`, `napostrophe`, `eogonek`, and `gdotaccent`.
- [ ] Reduce both-span sampled-risk coverage before doing any broad manifest cleanup.

Exit criteria:

- The requested roman cluster is no longer dominated by both-span failures, and the remaining queue is reduced to isolated quality repairs instead of structural or strategy-class mistakes.

## Team Split

- [x] Team Research:
  - Glyphs compatibility rules
  - fontTools defect semantics
  - donor-compat strategy check
- [x] Team Audit:
  - live roman rerun
  - severity ranking
  - bucket mapping
- [ ] Team Base Shapes:
  - `e`
  - `two`
  - `three`
  - `six`
  - `nine`
  - `uni018F`
- [ ] Team Derived Families:
  - `e*`
  - `r*`
  - `u*`
  - `tcaron`
- [ ] Team Integrated Forms:
  - `dslash`
  - `eogonek`
  - `Scedilla`
  - `scedilla`
  - `tbar`
  - `uogonek`
  - `napostrophe`
- [ ] Team Compounds:
  - `ae`
  - `oe`
  - `onehalf`
  - `threequarters`
  - `gdotaccent`
  - `guillemotright`

## Immediate Next Queue

- [ ] `six`
- [ ] `nine`
- [ ] `e`
- [ ] `two`
- [ ] `three`
- [ ] `uni018F`
- [ ] `t` then `tcaron`
- [ ] `s` then `scedilla` and `Scedilla`
- [ ] `onehalf` and `threequarters`
- [ ] `ae` and `oe`
