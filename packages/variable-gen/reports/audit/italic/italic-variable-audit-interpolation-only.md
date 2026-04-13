# Italic Variable Audit

- source: `/Users/mblode/Code/mblode/glide/glide-variable-italic.glyphs`
- designspace: `/Users/mblode/Code/mblode/glide/master_ufo/GlideItalic.designspace`
- variable font: `/Users/mblode/Code/mblode/glide/packages/variable-gen/build/audit/italic/glide-variable-italic-audit-vf.ttf`
- samples per span: `5`
- sample weights: `[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950]`

## Spans

- `thinitalic_to_italic` ThinItalic(100) -> Italic(400) weights=[100, 150, 200, 250, 300, 350, 400]
- `italic_to_extrablackitalic` Italic(400) -> ExtraBlackItalic(950) weights=[400, 492, 583, 675, 767, 858, 950]

## Summary

- total_glyphs: `743`
- problem_glyphs: `333`
- clean_glyphs: `410`
- interpolatable_problem_glyphs: `145`
- sampled_risky_glyphs: `303`
- glyphs_with_intersections: `57`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `303`
- master_validation_point_problem_glyphs: `0`
- master_validation_area_problem_glyphs: `0`

## Interpolation Focus

- total_glyphs: `743`
- problem_glyphs: `333`
- clean_glyphs: `410`
- interpolatable_problem_glyphs: `145`
- sampled_risky_glyphs: `303`
- glyphs_with_span_risk: `303`
- glyphs_risky_in_all_spans: `259`
- glyphs_with_intersections: `57`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `303`
- span_problem_glyphs: `{"italic_to_extrablackitalic": 284, "thinitalic_to_italic": 278}`

## Interpolatable

- summary: `{"issue_types": {"contour_order": 2, "kink": 99, "underweight": 171, "wrong_start_point": 6}, "problem_glyphs": 151}`

## Exact Masters

- skipped in `--interpolation-only` mode

## Sampled Weights

- `wght 100` riskyGlyphs=348 riskTypes={"short_segment": 348}
- `wght 150` riskyGlyphs=256 riskTypes={"intersections": 16, "short_segment": 255}
- `wght 200` riskyGlyphs=250 riskTypes={"intersections": 32, "short_segment": 249}
- `wght 250` riskyGlyphs=248 riskTypes={"intersections": 30, "short_segment": 247}
- `wght 300` riskyGlyphs=256 riskTypes={"intersections": 22, "short_segment": 255}
- `wght 350` riskyGlyphs=258 riskTypes={"intersections": 19, "short_segment": 258}
- `wght 400` riskyGlyphs=248 riskTypes={"intersections": 4, "short_segment": 248}
- `wght 492` riskyGlyphs=265 riskTypes={"intersections": 19, "short_segment": 264}
- `wght 583` riskyGlyphs=251 riskTypes={"intersections": 7, "short_segment": 249}
- `wght 675` riskyGlyphs=263 riskTypes={"intersections": 11, "short_segment": 262}
- `wght 767` riskyGlyphs=268 riskTypes={"intersections": 11, "short_segment": 265}
- `wght 858` riskyGlyphs=266 riskTypes={"intersections": 5, "short_segment": 266}
- `wght 950` riskyGlyphs=272 riskTypes={"intersections": 5, "short_segment": 272}

## Interpolation Priority Glyphs

- `a.ordn` focusSeverity=670 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.09
- `a.ordn.ss08` focusSeverity=670 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.09
- `uhungarumlaut` focusSeverity=655 interpolatable=4 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `quotedbl` focusSeverity=635 interpolatable=5 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.49
- `quotedbl.ss08` focusSeverity=635 interpolatable=5 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.49
- `utilde` focusSeverity=630 interpolatable=4 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.04
- `edieresis` focusSeverity=595 interpolatable=3 issueTypes=['contour_order', 'wrong_start_point'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=6 minSegment=0.2
- `edotaccent` focusSeverity=595 interpolatable=3 issueTypes=['contour_order', 'wrong_start_point'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=6 minSegment=0.2
- `u.ordn` focusSeverity=570 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.23
- `u.ordn.ss08` focusSeverity=570 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.23
- `ubreve` focusSeverity=570 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `u` focusSeverity=555 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `uacute` focusSeverity=555 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `ucircumflex` focusSeverity=555 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `udieresis` focusSeverity=555 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `ugrave` focusSeverity=555 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `umacron` focusSeverity=555 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `uring` focusSeverity=555 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.17
- `sacute` focusSeverity=550 interpolatable=4 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.41
- `scaron` focusSeverity=550 interpolatable=4 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.41
- `scircumflex` focusSeverity=550 interpolatable=4 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.41
- `two.tf` focusSeverity=545 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.08
- `two.dnom` focusSeverity=510 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=3 minSegment=0.22
- `two.numr` focusSeverity=510 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=3 minSegment=0.34
- `two.numr.ss08` focusSeverity=510 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=3 minSegment=0.29
- `uni2082` focusSeverity=510 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=3 minSegment=0.29
- `ccedilla` focusSeverity=470 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.46
- `question` focusSeverity=470 interpolatable=2 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=3 minSegment=0.01
- `questiondown` focusSeverity=470 interpolatable=2 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=3 minSegment=0.01
- `questiondown.case` focusSeverity=470 interpolatable=2 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=3 minSegment=0.01
- `atilde` focusSeverity=450 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.2
- `cedilla` focusSeverity=450 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.4
- `d.ordn` focusSeverity=450 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.09
- `d.ordn.ss08` focusSeverity=450 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.09
- `racute.ss03` focusSeverity=450 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.01
- `rcaron.ss03` focusSeverity=450 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=3 minSegment=0.01
- `uni2113.ss08` focusSeverity=450 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.11
- `five.dnom` focusSeverity=435 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 300, 350]} maxIntersections=0 minSegment=0.01
- `five.numr` focusSeverity=435 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 300, 350]} maxIntersections=0 minSegment=0.01
- `five.numr.ss08` focusSeverity=435 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 300, 350]} maxIntersections=0 minSegment=0.01
- `sterling.ss08` focusSeverity=435 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.33
- `uni2075` focusSeverity=435 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 300, 350]} maxIntersections=0 minSegment=0.01
- `Ccedilla` focusSeverity=430 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.46
- `ordfeminine` focusSeverity=430 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.41
- `ordfeminine.ss08` focusSeverity=430 interpolatable=2 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=2 minSegment=0.4
- `hungarumlaut` focusSeverity=400 interpolatable=4 issueTypes=['underweight'] interiorWeights=[] spanRiskWeights={} maxIntersections=0 minSegment=1.6
- `hungarumlaut.uc` focusSeverity=400 interpolatable=4 issueTypes=['underweight'] interiorWeights=[] spanRiskWeights={} maxIntersections=0 minSegment=None
- `Scedilla` focusSeverity=350 interpolatable=2 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.46
- `Uogonek` focusSeverity=350 interpolatable=2 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.8
- `aacute` focusSeverity=350 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"italic_to_extrablackitalic": [492, 583, 675, 767, 858], "thinitalic_to_italic": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.24

