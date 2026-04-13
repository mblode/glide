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
- problem_glyphs: `726`
- clean_glyphs: `17`
- interpolatable_problem_glyphs: `147`
- sampled_risky_glyphs: `401`
- glyphs_with_intersections: `62`
- glyphs_with_zero_ink: `0`
- glyphs_with_short_segments: `401`
- master_validation_point_problem_glyphs: `705`
- master_validation_area_problem_glyphs: `119`

## Interpolatable

- summary: `{"issue_types": {"kink": 120, "underweight": 191, "wrong_start_point": 3}, "problem_glyphs": 153}`

## Exact Masters

- `wght 100` pointMismatch=697 deviations=8 areaDiffs=71
- `wght 400` pointMismatch=694 deviations=11 areaDiffs=62
- `wght 950` pointMismatch=698 deviations=7 areaDiffs=74

## Sampled Weights

- `wght 100` riskyGlyphs=346 riskTypes={"short_segment": 346}
- `wght 150` riskyGlyphs=254 riskTypes={"intersections": 18, "short_segment": 253}
- `wght 200` riskyGlyphs=251 riskTypes={"intersections": 30, "short_segment": 248}
- `wght 250` riskyGlyphs=250 riskTypes={"intersections": 29, "short_segment": 249}
- `wght 300` riskyGlyphs=258 riskTypes={"intersections": 22, "short_segment": 257}
- `wght 350` riskyGlyphs=260 riskTypes={"intersections": 7, "short_segment": 260}
- `wght 400` riskyGlyphs=248 riskTypes={"intersections": 4, "short_segment": 248}
- `wght 492` riskyGlyphs=266 riskTypes={"intersections": 18, "short_segment": 265}
- `wght 583` riskyGlyphs=261 riskTypes={"intersections": 7, "short_segment": 259}
- `wght 675` riskyGlyphs=265 riskTypes={"intersections": 12, "short_segment": 264}
- `wght 767` riskyGlyphs=272 riskTypes={"intersections": 12, "short_segment": 271}
- `wght 858` riskyGlyphs=270 riskTypes={"intersections": 5, "short_segment": 270}
- `wght 950` riskyGlyphs=276 riskTypes={"intersections": 9, "short_segment": 276}

## Top Glyphs

- `gdotaccent` severity=1260 interpolatable=7 issueTypes=['kink', 'underweight'] riskyWeights=[200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=6 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=['100', '950']
- `gbreve` severity=1145 interpolatable=7 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=['100', '950']
- `gcircumflex` severity=1100 interpolatable=7 issueTypes=['kink', 'underweight'] riskyWeights=[200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=['100', '950']
- `utilde` severity=1055 interpolatable=7 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.0 masterDeviationWeights=[] masterAreaWeights=['100']
- `scedilla` severity=1015 interpolatable=5 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.02 masterDeviationWeights=[] masterAreaWeights=['400']
- `s.ordn` severity=975 interpolatable=5 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.09 masterDeviationWeights=[] masterAreaWeights=['400']
- `s.ordn.ss08` severity=935 interpolatable=5 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400']
- `commaturn` severity=895 interpolatable=5 issueTypes=['kink', 'underweight', 'wrong_start_point'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=1 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['100']
- `onehalf` severity=895 interpolatable=4 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.22 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `a.ordn` severity=875 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.09 masterDeviationWeights=[] masterAreaWeights=['100']
- `a.ordn.ss08` severity=875 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.09 masterDeviationWeights=[] masterAreaWeights=['100']
- `ae` severity=865 interpolatable=5 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `aeacute` severity=865 interpolatable=5 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `quotedbl` severity=830 interpolatable=5 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 858, 950] maxIntersections=0 minSegment=0.49 masterDeviationWeights=[] masterAreaWeights=[]
- `quotedbl.ss08` severity=830 interpolatable=5 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 858, 950] maxIntersections=0 minSegment=0.49 masterDeviationWeights=[] masterAreaWeights=[]
- `onehalf.ss08` severity=810 interpolatable=3 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.22 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `racute.ss03` severity=805 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.0 masterDeviationWeights=[] masterAreaWeights=[]
- `rcaron.ss03` severity=805 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.0 masterDeviationWeights=[] masterAreaWeights=[]
- `u.ordn` severity=765 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.23 masterDeviationWeights=[] masterAreaWeights=[]
- `u.ordn.ss08` severity=765 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.23 masterDeviationWeights=[] masterAreaWeights=[]
- `sacute` severity=755 interpolatable=4 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=['400']
- `scaron` severity=755 interpolatable=4 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=['400']
- `scircumflex` severity=755 interpolatable=4 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=['400']
- `two.tf` severity=740 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 858, 950] maxIntersections=2 minSegment=0.08 masterDeviationWeights=[] masterAreaWeights=[]
- `r.ss03` severity=715 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.0 masterDeviationWeights=[] masterAreaWeights=['100']
- `two.dnom` severity=710 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.22 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `two.numr` severity=710 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.34 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `two.numr.ss08` severity=710 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.29 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `uni2082` severity=710 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.29 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `ccedilla` severity=685 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.46 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `question` severity=675 interpolatable=2 issueTypes=['kink'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400']
- `questiondown` severity=675 interpolatable=2 issueTypes=['kink'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400']
- `questiondown.case` severity=675 interpolatable=2 issueTypes=['kink'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=3 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400']
- `atilde` severity=665 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.2 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `d.ordn` severity=655 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.09 masterDeviationWeights=[] masterAreaWeights=['100']
- `d.ordn.ss08` severity=655 interpolatable=1 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.09 masterDeviationWeights=[] masterAreaWeights=['100']
- `uni2113.ss08` severity=655 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.11 masterDeviationWeights=[] masterAreaWeights=['100']
- `sterling.ss08` severity=650 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 767, 858, 950] maxIntersections=0 minSegment=0.33 masterDeviationWeights=[] masterAreaWeights=['100', '400']
- `Ccedilla` severity=645 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.46 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `cedilla` severity=645 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=[]
- `ordfeminine` severity=635 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.41 masterDeviationWeights=[] masterAreaWeights=['100']
- `ordfeminine.ss08` severity=635 interpolatable=2 issueTypes=['underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=2 minSegment=0.4 masterDeviationWeights=[] masterAreaWeights=['100']
- `five.dnom` severity=625 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400']
- `five.numr` severity=625 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400']
- `five.numr.ss08` severity=625 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400']
- `uni2075` severity=625 interpolatable=3 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 300, 350, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.01 masterDeviationWeights=[] masterAreaWeights=['400']
- `uni2113` severity=575 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.14 masterDeviationWeights=[] masterAreaWeights=['100', '400', '950']
- `Scedilla` severity=565 interpolatable=2 issueTypes=['kink'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.46 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `aacute` severity=565 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.24 masterDeviationWeights=[] masterAreaWeights=['400', '950']
- `abreve` severity=565 interpolatable=2 issueTypes=['kink', 'underweight'] riskyWeights=[100, 150, 200, 250, 300, 350, 400, 492, 583, 675, 767, 858, 950] maxIntersections=0 minSegment=0.24 masterDeviationWeights=[] masterAreaWeights=['400', '950']

