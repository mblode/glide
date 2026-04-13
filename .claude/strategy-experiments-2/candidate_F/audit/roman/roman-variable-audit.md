# Roman Variable Audit

- source: `/Users/mblode/Code/mblode/glide/.claude/strategy-experiments-2/candidate_F/glide-variable.glyphs`
- designspace: `/Users/mblode/Code/mblode/glide/master_ufo/Glide.designspace`
- variable font: `/Users/mblode/Code/mblode/glide/.claude/strategy-experiments-2/candidate_F/audit-build/roman/glide-variable-audit-vf.ttf`
- samples per span: `4`
- sample weights: `[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950]`

## Spans

- `thin_to_regular` Thin(100) -> Regular(400) weights=[100, 160, 220, 280, 340, 400]
- `regular_to_extrablack` Regular(400) -> ExtraBlack(950) weights=[400, 510, 620, 730, 840, 950]

## Summary

- total_glyphs: `754`
- problem_glyphs: `737`
- clean_glyphs: `17`
- interpolatable_problem_glyphs: `61`
- sampled_risky_glyphs: `378`
- glyphs_with_intersections: `14`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `378`
- master_validation_point_problem_glyphs: `716`
- master_validation_area_problem_glyphs: `66`

## Interpolation Focus

- total_glyphs: `754`
- problem_glyphs: `258`
- clean_glyphs: `496`
- interpolatable_problem_glyphs: `61`
- sampled_risky_glyphs: `250`
- glyphs_with_span_risk: `250`
- glyphs_risky_in_all_spans: `204`
- glyphs_with_intersections: `13`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `249`
- span_problem_glyphs: `{"regular_to_extrablack": 221, "thin_to_regular": 233}`

## Interpolatable

- summary: `{"issue_types": {"kink": 17, "underweight": 59, "wrong_start_point": 5}, "problem_glyphs": 65}`

## Exact Masters

- `wght 100` pointMismatch=690 deviations=26 areaDiffs=58
- `wght 400` pointMismatch=689 deviations=27 areaDiffs=15
- `wght 950` pointMismatch=693 deviations=23 areaDiffs=57

## Sampled Weights

- `wght 100` riskyGlyphs=333 riskTypes={"intersections": 2, "short_segment": 333}
- `wght 160` riskyGlyphs=223 riskTypes={"intersections": 3, "short_segment": 223}
- `wght 220` riskyGlyphs=206 riskTypes={"intersections": 4, "short_segment": 203}
- `wght 280` riskyGlyphs=203 riskTypes={"intersections": 4, "short_segment": 200}
- `wght 340` riskyGlyphs=206 riskTypes={"intersections": 1, "short_segment": 206}
- `wght 400` riskyGlyphs=201 riskTypes={"intersections": 1, "short_segment": 201}
- `wght 510` riskyGlyphs=201 riskTypes={"intersections": 5, "short_segment": 199}
- `wght 620` riskyGlyphs=198 riskTypes={"intersections": 7, "short_segment": 197}
- `wght 730` riskyGlyphs=205 riskTypes={"intersections": 9, "short_segment": 204}
- `wght 840` riskyGlyphs=207 riskTypes={"intersections": 7, "short_segment": 207}
- `wght 950` riskyGlyphs=226 riskTypes={"intersections": 1, "short_segment": 226}

## Interpolation Priority Glyphs

- `uni021B.1` focusSeverity=400 interpolatable=0 issueTypes=[] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=359 minSegment=0.0
- `atilde` focusSeverity=320 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=0 minSegment=0.2
- `cedilla` focusSeverity=320 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=0 minSegment=0.6
- `itilde` focusSeverity=320 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=0 minSegment=0.2
- `ntilde` focusSeverity=320 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=0 minSegment=0.2
- `otilde` focusSeverity=320 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=0 minSegment=0.2
- `tilde` focusSeverity=320 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=0 minSegment=0.2
- `uni2082` focusSeverity=320 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=0 minSegment=0.41
- `six.tf.ss08` focusSeverity=315 interpolatable=3 issueTypes=['kink', 'underweight'] interiorWeights=[730] spanRiskWeights={"regular_to_extrablack": [730]} maxIntersections=0 minSegment=0.32
- `uni216F` focusSeverity=305 interpolatable=1 issueTypes=['underweight'] interiorWeights=[510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840]} maxIntersections=44 minSegment=1.08
- `six.tf` focusSeverity=295 interpolatable=1 issueTypes=['underweight'] interiorWeights=[160, 220, 280, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280]} maxIntersections=6 minSegment=0.2
- `ampersand` focusSeverity=290 interpolatable=2 issueTypes=['underweight'] interiorWeights=[280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [280, 340]} maxIntersections=0 minSegment=0.89
- `uni216F.ss08` focusSeverity=290 interpolatable=1 issueTypes=['underweight'] interiorWeights=[510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840]} maxIntersections=44 minSegment=1.27
- `aring.ss02` focusSeverity=280 interpolatable=0 issueTypes=[] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=8 minSegment=0.4
- `aringacute.ss02` focusSeverity=280 interpolatable=0 issueTypes=[] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=8 minSegment=0.4
- `zero.tf` focusSeverity=280 interpolatable=2 issueTypes=['underweight'] interiorWeights=[220, 280] spanRiskWeights={"thin_to_regular": [220, 280]} maxIntersections=2 minSegment=1.41
- `r.ordn` focusSeverity=260 interpolatable=1 issueTypes=['underweight'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=1 minSegment=0.0
- `sterling.tf` focusSeverity=260 interpolatable=1 issueTypes=['underweight'] interiorWeights=[160, 220, 280, 340, 510, 620, 730, 840] spanRiskWeights={"regular_to_extrablack": [510, 620, 730, 840], "thin_to_regular": [160, 220, 280, 340]} maxIntersections=1 minSegment=0.1
- `n.ordn` focusSeverity=245 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[160, 220, 840] spanRiskWeights={"regular_to_extrablack": [840], "thin_to_regular": [160, 220]} maxIntersections=0 minSegment=0.88
- `n.ordn.ss08` focusSeverity=245 interpolatable=2 issueTypes=['kink', 'underweight'] interiorWeights=[160, 220, 840] spanRiskWeights={"regular_to_extrablack": [840], "thin_to_regular": [160, 220]} maxIntersections=0 minSegment=0.88

## Top Glyphs

- `uni021B.1` severity=565 interpolatable=0 issueTypes=[] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=359 minSegment=0.0 masterDeviationWeights=[] masterAreaWeights=[]
- `atilde` severity=515 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `cedilla` severity=515 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.6 masterDeviationWeights=[] masterAreaWeights=[]
- `itilde` severity=515 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `ntilde` severity=515 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `otilde` severity=515 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `tilde` severity=515 interpolatable=2 issueTypes=['underweight', 'wrong_start_point'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `uni2082` severity=515 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=[]
- `six.tf.ss08` severity=500 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 730] maxIntersections=0 minSegment=0.32 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `six.tf` severity=490 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 160, 220, 280, 400, 510, 620, 730, 840, 950] maxIntersections=6 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=[]
- `aring.ss02` severity=485 interpolatable=0 issueTypes=[] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=8 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=['950']
- `uni216F` severity=485 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 510, 620, 730, 840, 950] maxIntersections=44 minSegment=1.08 masterDeviationWeights=[] masterAreaWeights=[]
- `aringacute.ss02` severity=475 interpolatable=0 issueTypes=[] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=8 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `ampersand` severity=470 interpolatable=2 issueTypes=['underweight'] riskyWeights=[280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.89 masterDeviationWeights=[] masterAreaWeights=[]
- `uni216F.ss08` severity=470 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 510, 620, 730, 840, 950] maxIntersections=44 minSegment=1.27 masterDeviationWeights=[] masterAreaWeights=[]
- `zero.tf` severity=465 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 220, 280] maxIntersections=2 minSegment=1.41 masterDeviationWeights=[] masterAreaWeights=['100', '950']
- `r.ordn` severity=455 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=1 minSegment=0.0 masterDeviationWeights=[] masterAreaWeights=[]
- `sterling.tf` severity=455 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=1 minSegment=0.1 masterDeviationWeights=[] masterAreaWeights=[]
- `emacron` severity=445 interpolatable=0 issueTypes=[] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=6 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=['100']
- `Euro` severity=425 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 160, 220, 280, 340, 400, 510, 620, 730, 840, 950] maxIntersections=0 minSegment=0.22 masterDeviationWeights=[] masterAreaWeights=['950']

