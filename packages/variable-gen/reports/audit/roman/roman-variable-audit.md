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
- problem_glyphs: `737`
- clean_glyphs: `17`
- interpolatable_problem_glyphs: `61`
- sampled_risky_glyphs: `378`
- glyphs_with_intersections: `23`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `378`
- master_validation_point_problem_glyphs: `716`
- master_validation_area_problem_glyphs: `86`

## Interpolation Focus

- total_glyphs: `754`
- problem_glyphs: `268`
- clean_glyphs: `486`
- interpolatable_problem_glyphs: `61`
- sampled_risky_glyphs: `260`
- glyphs_with_span_risk: `260`
- glyphs_risky_in_all_spans: `208`
- glyphs_with_intersections: `22`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `259`
- span_problem_glyphs: `{"regular_to_extrablack": 224, "thin_to_regular": 244}`

## Interpolatable

- summary: `{"issue_types": {"kink": 17, "underweight": 59, "wrong_start_point": 5}, "problem_glyphs": 65}`

## Exact Masters

- `wght 100` pointMismatch=691 deviations=25 areaDiffs=63
- `wght 400` pointMismatch=690 deviations=26 areaDiffs=34
- `wght 950` pointMismatch=694 deviations=22 areaDiffs=60

## Sampled Weights

- `wght 100` riskyGlyphs=333 riskTypes={"intersections": 2, "short_segment": 333}
- `wght 150` riskyGlyphs=225 riskTypes={"intersections": 3, "short_segment": 225}
- `wght 200` riskyGlyphs=206 riskTypes={"intersections": 4, "short_segment": 204}
- `wght 250` riskyGlyphs=203 riskTypes={"intersections": 4, "short_segment": 200}
- `wght 300` riskyGlyphs=210 riskTypes={"intersections": 3, "short_segment": 207}
- `wght 350` riskyGlyphs=199 riskTypes={"short_segment": 199}
- `wght 400` riskyGlyphs=201 riskTypes={"short_segment": 201}
- `wght 492` riskyGlyphs=205 riskTypes={"intersections": 15, "short_segment": 203}
- `wght 583` riskyGlyphs=198 riskTypes={"intersections": 5, "short_segment": 196}
- `wght 675` riskyGlyphs=193 riskTypes={"intersections": 5, "short_segment": 192}
- `wght 767` riskyGlyphs=206 riskTypes={"intersections": 7, "short_segment": 206}
- `wght 858` riskyGlyphs=208 riskTypes={"intersections": 5, "short_segment": 208}
- `wght 950` riskyGlyphs=226 riskTypes={"short_segment": 226}

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
- `sterling.tf` focusSeverity=290 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=1 minSegment=0.06
- `emacron` focusSeverity=270 interpolatable=0 issueTypes=[] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=9 minSegment=0.2
- `uni021B.1` focusSeverity=270 interpolatable=0 issueTypes=[] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=4 minSegment=0.91
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
- `three.tf` focusSeverity=205 interpolatable=1 issueTypes=['underweight'] interiorWeights=[150, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 350]} maxIntersections=0 minSegment=0.89
- `commaturn` focusSeverity=190 interpolatable=0 issueTypes=[] interiorWeights=[150, 200, 250, 300, 350, 492, 583, 675, 767, 858] spanRiskWeights={"regular_to_extrablack": [492, 583, 675, 767, 858], "thin_to_regular": [150, 200, 250, 300, 350]} maxIntersections=1 minSegment=0.03

## Top Glyphs

- `aring.ss02` severity=565 interpolatable=0 issueTypes=[] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=8 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=['100', '950']
- `aringacute.ss02` severity=565 interpolatable=0 issueTypes=[] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=8 minSegment=0.21 masterDeviationWeights=[] masterAreaWeights=['100', '950']
- `atilde` severity=545 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `cedilla` severity=545 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.6 masterDeviationWeights=[] masterAreaWeights=[]
- `itilde` severity=545 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `ntilde` severity=545 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `otilde` severity=545 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `six.tf` severity=545 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 400, 492, 583, 675, 767, 858, 950] maxIntersections=6 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `tilde` severity=545 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `uni2082` severity=545 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=[]
- `uni216F` severity=525 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 492, 583, 675, 767, 858, 950] maxIntersections=50 minSegment=0.79 masterDeviationWeights=[] masterAreaWeights=[]
- `six.tf.ss08` severity=515 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 675, 767] maxIntersections=0 minSegment=0.72 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `ampersand` severity=510 interpolatable=2 issueTypes=['underweight'] riskyWeights=[250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.89 masterDeviationWeights=[] masterAreaWeights=['950']
- `uni216F.ss08` severity=510 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 492, 583, 675, 767, 858, 950] maxIntersections=52 minSegment=0.57 masterDeviationWeights=[] masterAreaWeights=[]
- `zero.tf` severity=505 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 200, 250, 300] maxIntersections=2 minSegment=1.41 masterDeviationWeights=[] masterAreaWeights=['100', '950']
- `nine.tf` severity=485 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 400, 492] maxIntersections=12 minSegment=0.64 masterDeviationWeights=[] masterAreaWeights=[]
- `sterling.tf` severity=485 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=1 minSegment=0.06 masterDeviationWeights=[] masterAreaWeights=[]
- `emacron` severity=475 interpolatable=0 issueTypes=[] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=9 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=['100']
- `Euro` severity=455 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.78 masterDeviationWeights=[] masterAreaWeights=['950']
- `tilde.uc` severity=455 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=['100']
- `iogonek` severity=450 interpolatable=1 issueTypes=['kink'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 767, 858, 950] maxIntersections=0 minSegment=1.03 masterDeviationWeights=[] masterAreaWeights=['100', '400']
- `Atilde` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `Ccedilla` severity=445 interpolatable=1 issueTypes=['kink'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.6 masterDeviationWeights=[] masterAreaWeights=[]
- `Ntilde` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `Otilde` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `Utilde` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `ccedilla` severity=445 interpolatable=1 issueTypes=['kink'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.6 masterDeviationWeights=[] masterAreaWeights=[]
- `d.ordn` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.47 masterDeviationWeights=[] masterAreaWeights=[]
- `d.ordn.ss08` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.47 masterDeviationWeights=[] masterAreaWeights=[]
- `dcaron` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `onehalf.ss08` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=[]
- `question` severity=445 interpolatable=1 issueTypes=['kink'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.27 masterDeviationWeights=[] masterAreaWeights=[]
- `r.ordn` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.0 masterDeviationWeights=[] masterAreaWeights=[]
- `r.ordn.ss08` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=[]
- `two.tf` severity=445 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.6 masterDeviationWeights=[] masterAreaWeights=[]
- `n.ordn` severity=435 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 858, 950] maxIntersections=0 minSegment=0.64 masterDeviationWeights=[] masterAreaWeights=['400']
- `n.ordn.ss08` severity=435 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 858, 950] maxIntersections=0 minSegment=0.64 masterDeviationWeights=[] masterAreaWeights=['400']
- `two.ss08` severity=425 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 767, 858, 950] maxIntersections=0 minSegment=0.6 masterDeviationWeights=[] masterAreaWeights=['100']
- `two.tf.ss08` severity=425 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 767, 858, 950] maxIntersections=0 minSegment=0.6 masterDeviationWeights=[] masterAreaWeights=['100']
- `three.dnom` severity=415 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=[]
- `three.numr` severity=415 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=[]
- `three.numr.ss08` severity=415 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=[]
- `three.ss08` severity=415 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 767, 858, 950] maxIntersections=0 minSegment=0.83 masterDeviationWeights=[] masterAreaWeights=[]
- `three.tf.ss08` severity=415 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 767, 858, 950] maxIntersections=0 minSegment=0.83 masterDeviationWeights=[] masterAreaWeights=[]
- `threequarters.ss08` severity=415 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `uni2083` severity=415 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=[]
- `uni2782` severity=415 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `commaturn` severity=405 interpolatable=0 issueTypes=[] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=1 minSegment=0.03 masterDeviationWeights=[] masterAreaWeights=['100', '400']
- `eogonek` severity=405 interpolatable=0 issueTypes=[] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.63 masterDeviationWeights=[] masterAreaWeights=['100', '950']
- `undercommaaccent` severity=405 interpolatable=0 issueTypes=[] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=1 minSegment=0.02 masterDeviationWeights=[] masterAreaWeights=['100', '400']

