# Roman Variable Audit

- source: `/Users/mblode/Code/mblode/glide/glide-variable.glyphs`
- designspace: `/Users/mblode/Code/mblode/glide/master_ufo/Glide.designspace`
- variable font: `/Users/mblode/Code/mblode/glide/packages/variable-gen/build/audit/roman/glide-variable-audit-vf.ttf`
- samples per span: `5`
- sample weights: `[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950]`

## Spans

- `thin_to_regular` Thin(100) -> Regular(400) weights=[100, 150, 200, 250, 300, 350, 400]
- `regular_to_extrablack` Regular(400) -> ExtraBlack(950) weights=[400, 492, 583, 675, 767, 858, 950]

## Summary

- total_glyphs: `754`
- problem_glyphs: `270`
- clean_glyphs: `484`
- interpolatable_problem_glyphs: `66`
- sampled_risky_glyphs: `261`
- glyphs_with_intersections: `21`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `259`
- master_validation_point_problem_glyphs: `0`
- master_validation_area_problem_glyphs: `0`

## Interpolation Focus

- total_glyphs: `754`
- problem_glyphs: `270`
- clean_glyphs: `484`
- interpolatable_problem_glyphs: `66`
- sampled_risky_glyphs: `261`
- glyphs_with_span_risk: `261`
- glyphs_risky_in_all_spans: `209`
- glyphs_with_intersections: `21`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `259`
- span_problem_glyphs: `{"regular_to_extrablack": 226, "thin_to_regular": 244}`

## Interpolatable

- summary: `{"issue_types": {"kink": 19, "underweight": 63, "wrong_start_point": 5}, "problem_glyphs": 70}`

## Exact Masters

- skipped in `--interpolation-only` mode

## Sampled Weights

- `wght 100` riskyGlyphs=333 riskTypes={"intersections": 1, "short_segment": 333}
- `wght 150` riskyGlyphs=224 riskTypes={"intersections": 2, "short_segment": 224}
- `wght 200` riskyGlyphs=204 riskTypes={"intersections": 3, "short_segment": 202}
- `wght 250` riskyGlyphs=203 riskTypes={"intersections": 3, "short_segment": 200}
- `wght 300` riskyGlyphs=211 riskTypes={"intersections": 3, "short_segment": 208}
- `wght 350` riskyGlyphs=200 riskTypes={"short_segment": 200}
- `wght 400` riskyGlyphs=202 riskTypes={"short_segment": 202}
- `wght 492` riskyGlyphs=207 riskTypes={"intersections": 16, "short_segment": 204}
- `wght 583` riskyGlyphs=198 riskTypes={"intersections": 6, "short_segment": 195}
- `wght 675` riskyGlyphs=194 riskTypes={"intersections": 6, "short_segment": 192}
- `wght 767` riskyGlyphs=206 riskTypes={"intersections": 7, "short_segment": 205}
- `wght 858` riskyGlyphs=209 riskTypes={"intersections": 5, "short_segment": 208}
- `wght 950` riskyGlyphs=227 riskTypes={"short_segment": 227}

## Interpolation Priority Glyphs

- `aring.ss02` focusSeverity=350 interpolatable=0 issueTypes=[] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=8 minSegment=0.4
- `aringacute.ss02` focusSeverity=350 interpolatable=0 issueTypes=[] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=8 minSegment=0.21
- `atilde` focusSeverity=350 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.2
- `cedilla` focusSeverity=350 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.6
- `itilde` focusSeverity=350 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.2
- `ntilde` focusSeverity=350 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.2
- `otilde` focusSeverity=350 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.2
- `six.tf` focusSeverity=350 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300]} maxIntersections=6 minSegment=0.2
- `tilde` focusSeverity=350 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.2
- `uni2082` focusSeverity=350 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.41
- `uni216F` focusSeverity=345 interpolatable=1 issueTypes=['underweight'] interiorWeights=[492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858]} maxIntersections=50 minSegment=0.79
- `six.tf.ss08` focusSeverity=330 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[675, 767] spanRiskWeights={"regular_to_extrablack": [675, 767]} maxIntersections=0 minSegment=0.72
- `uni216F.ss08` focusSeverity=330 interpolatable=1 issueTypes=['underweight'] interiorWeights=[492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858]} maxIntersections=52 minSegment=0.57
- `ampersand` focusSeverity=320 interpolatable=2 issueTypes=['underweight'] interiorWeights=[250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [250, 300, 350]} maxIntersections=0 minSegment=0.89
- `zero.tf` focusSeverity=320 interpolatable=2 issueTypes=['underweight'] interiorWeights=[200, 250, 300] spanRiskWeights={"thin_to_regular": [200, 250, 300]} maxIntersections=2 minSegment=1.41
- `nine.tf` focusSeverity=305 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 492] spanRiskWeights={"regular_to_extrablack": [492], "thin_to_regular": [150, 200, 250, 300]} maxIntersections=12 minSegment=0.64
- `IJ` focusSeverity=290 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 250, 300, 350, 492] spanRiskWeights={"regular_to_extrablack": [492], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.41
- `sterling.tf` focusSeverity=290 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=1 minSegment=0.06
- `emacron` focusSeverity=270 interpolatable=0 issueTypes=[] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=9 minSegment=0.2
- `Atilde` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.4
- `Ccedilla` focusSeverity=250 interpolatable=1 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.6
- `Euro` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.78
- `Ntilde` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.4
- `Otilde` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.4
- `Utilde` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.4
- `ccedilla` focusSeverity=250 interpolatable=1 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.6
- `d.ordn` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.47
- `d.ordn.ss08` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.47
- `dcaron` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.4
- `onehalf.ss08` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.41
- `question` focusSeverity=250 interpolatable=1 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.27
- `r.ordn` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.0
- `r.ordn.ss08` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.01
- `tilde.uc` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.4
- `two.tf` focusSeverity=250 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.6
- `uni03BC` focusSeverity=250 interpolatable=1 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.5
- `n.ordn` focusSeverity=245 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 858] spanRiskWeights={"regular_to_extrablack": [858], "thin_to_regular": [150, 200]} maxIntersections=0 minSegment=0.64
- `n.ordn.ss08` focusSeverity=245 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[150, 200, 858] spanRiskWeights={"regular_to_extrablack": [858], "thin_to_regular": [150, 200]} maxIntersections=0 minSegment=0.64
- `iogonek` focusSeverity=235 interpolatable=1 issueTypes=['kink'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=1.03
- `three.dnom` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 300, 350]} maxIntersections=0 minSegment=0.41
- `three.numr` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 300, 350]} maxIntersections=0 minSegment=0.41
- `three.numr.ss08` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 300, 350]} maxIntersections=0 minSegment=0.41
- `three.ss08` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.83
- `three.tf.ss08` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.83
- `threequarters.ss08` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 300, 350]} maxIntersections=0 minSegment=0.4
- `two.ss08` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.6
- `two.tf.ss08` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=0 minSegment=0.6
- `uni2083` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 300, 350]} maxIntersections=0 minSegment=0.41
- `uni2782` focusSeverity=220 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 300, 350]} maxIntersections=0 minSegment=0.4
- `zero` focusSeverity=215 interpolatable=2 issueTypes=['underweight'] interiorWeights=[858] spanRiskWeights={"regular_to_extrablack": [858]} maxIntersections=0 minSegment=1.01

