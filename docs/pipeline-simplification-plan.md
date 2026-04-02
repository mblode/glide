# Glide Build Pipeline Review

## Bottom Line

You probably do **not** need the whole current pipeline as the default `make build` path if `glide-variable.ttf` and `glide-variable-italic.ttf` are now good enough to be treated as the canonical release-grade sources.

You likely **do** still want some pipeline, but split into three lanes:

- `package`: take the two canonical variable fonts and emit release artifacts.
- `audit`: run interpolation validation, proof generation, and optional compare assets.
- `author`: rebuild the fonts from derived sources and donor data only when you are changing the design system itself.

## What The Repo Is Doing Today

- `make build` currently routes everything through [`build/release.py`](/Users/mblode/Code/mblode/glide/build/release.py#L486), which runs:
  - source extraction from [`src/glide-variable.ttf`](/Users/mblode/Code/mblode/glide/build/extract_root_glide_masters.py#L85)
  - italic seeding from Circular donors in [`src/donors/circular/`](/Users/mblode/Code/mblode/glide/build/seed_glide_italic_from_circular.py#L529)
  - FontLab prep and repair reporting via [`build/prepare_for_fontlab.py`](/Users/mblode/Code/mblode/glide/build/prepare_for_fontlab.py#L561)
  - Roman + Italic variable builds via [`build/build_variable.py`](/Users/mblode/Code/mblode/glide/build/build_variable.py#L571)
  - static instance generation and validation via [`build/generate_instances.py`](/Users/mblode/Code/mblode/glide/build/generate_instances.py#L143)
  - exact italic compare instances via [`build/apply_circular_italic_kerning_to_instances.py`](/Users/mblode/Code/mblode/glide/build/apply_circular_italic_kerning_to_instances.py#L55)
  - release packaging, proof sync, metadata, verification, and zip creation via [`build/release.py`](/Users/mblode/Code/mblode/glide/build/release.py#L255)

## Repo-Specific Findings

- The FontLab prep stage is not earning its place on the mandatory path right now.
  - The generated summary shows `Auto-repaired: 0` for both families and no reduction in compatibility issues: [`build/work/reports/fontlab/fontlab-prep-summary.md`](/Users/mblode/Code/mblode/glide/build/work/reports/fontlab/fontlab-prep-summary.md#L5)
- The static-instance validation stage is catching a real problem.
  - Roman `700` still shows `164` deviating glyphs: [`build/work/reports/roman-instance-validation.json`](/Users/mblode/Code/mblode/glide/build/work/reports/roman-instance-validation.json#L22)
  - Italic `700` still shows `161` deviating glyphs: [`build/work/reports/italic-instance-validation.json`](/Users/mblode/Code/mblode/glide/build/work/reports/italic-instance-validation.json#L22)
- The italic generation stage is still heavily synthetic.
  - Each italic weight is built from `124` direct-delta glyphs and `335` slant-fallback glyphs: [`build/work/reports/glide-italic-seed-report.json`](/Users/mblode/Code/mblode/glide/build/work/reports/glide-italic-seed-report.json#L67)
- The proof lane exists mostly for internal review, not shipping.
  - The proof page explicitly loads Circular donor italics and exact comparison instances: [`docs/proof/index.html`](/Users/mblode/Code/mblode/glide/docs/proof/index.html#L26)
- The release lane is broader than the user-facing promise.
  - The README says the repo builds two variable fonts, but `make build` also emits static TTF/OTF/WOFF/WOFF2, CSS, proof HTML, metadata, and zip-supporting assets: [`README.md`](/Users/mblode/Code/mblode/glide/README.md#L27)

## External Research That Changes The Decision

- CSS Fonts Level 4 expects a real italic face to be defined separately if you want designed italics instead of synthetic slanting, and allows variable fonts to advertise weight ranges in `@font-face`.
  - https://www.w3.org/TR/css-fonts-4/
- `fontTools.varLib.instancer.instantiateVariableFont(...)` can generate full static instances from a variable font, which means your static fonts do not need to be primary sources.
  - https://fonttools.readthedocs.io/en/latest/varLib/instancer.html
- Microsoft’s OpenType `STAT` guidance says variable fonts should expose axis records and axis values for compatibility naming, including italic distinctions across a family.
  - https://learn.microsoft.com/en-us/typography/opentype/spec/stat
- W3C’s WOFF 2.0 recommendation positions WOFF2 as the modern compressed webfont format.
  - https://www.w3.org/press-releases/2018/woff2-rec/
- Google Fonts’ variable-font guidance still calls out backward compatibility with static fonts and notes that DTP application support for variable fonts is not uniformly mature.
  - https://googlefonts.github.io/gf-guide/variable.html

## Recommendation

Treat the current pipeline as three different systems that were collapsed into one:

- **Authoring system**
  - Needed only if the canonical source remains:
    - one Roman VF in `src/`
    - Circular donor fonts
    - scripted italic derivation
- **QA system**
  - Useful because it is finding real drift at weight `700`
  - Not required to produce the two variable release files
- **Packaging system**
  - Still useful for:
    - WOFF2 output
    - optional WOFF fallback
    - metadata verification
    - zip creation
    - optional static-font bundles

If you are willing to promote the two variable fonts to the source of truth, then the default build should shrink to the packaging system.

## Target End State

- `make build`
  - package from canonical `glide-variable.ttf` and `glide-variable-italic.ttf`
- `make verify`
  - verify release files and metadata
- `make audit`
  - run instance generation, interpolation validation, and proof-only compare assets
- `make author`
  - rerun extraction, donor-based italic seeding, master prep, and variable rebuild from derived sources

## Phased Plan

### Phase 0: Decide The Source Of Truth

- [ ] Decide whether the canonical sources are the two final variable fonts or the current derived-master pipeline.
- [ ] If the two VFs are canonical, document where they live and how they are edited.
- [ ] If the donor-based pipeline remains canonical, keep the authoring lane and do not delete the donor logic yet.

### Phase 1: Split The Pipeline By Purpose

- [ ] Create a `package` command that starts from two variable fonts only.
- [ ] Create an `audit` command for proofing and validation outputs.
- [ ] Create an `author` command for source derivation and italic regeneration.
- [ ] Update [`Makefile`](/Users/mblode/Code/mblode/glide/Makefile#L11) so `make build` no longer implies every authoring and proofing step.

### Phase 2: Thin The Default Release Path

- [ ] Keep variable TTF packaging.
- [ ] Keep WOFF2 generation for web delivery.
- [ ] Decide whether WOFF is still needed for your target environments.
- [ ] Decide whether static TTF generation is needed for download bundles.
- [ ] Decide whether static OTF generation is needed at all or is just legacy packaging overhead.
- [ ] Keep metadata and verification because they are cheap and valuable.

### Phase 3: Demote Non-Essential Steps

- [ ] Remove [`build/prepare_for_fontlab.py`](/Users/mblode/Code/mblode/glide/build/prepare_for_fontlab.py#L1) from the default release path.
- [ ] Remove exact italic compare-instance generation from the default release path.
- [ ] Move proof asset copying behind `make audit` or `make proof`.
- [ ] Keep the validation reports, but stop generating them on every release build unless they gate release quality.

### Phase 4: Resolve The Real Quality Gate

- [ ] Investigate the `700` interpolation drift before deleting the audit lane.
- [ ] Decide whether the drift is acceptable for shipping or only acceptable for internal iteration.
- [ ] If the drift is unacceptable, keep the audit lane mandatory until fixed.
- [ ] If acceptable, convert the reports from blockers into informational artifacts.

### Phase 5: Remove Dead Authoring Logic If Safe

- [ ] Delete extraction-from-Roman-VF logic only after the Roman VF is no longer treated as the generator for the rest of the family.
- [ ] Delete donor-based italic seeding only after the italic VF is maintained directly.
- [ ] Delete donor kerning transfer utilities only after the final italic VF is the maintained artifact and no compare proof depends on donor kerning.

### Phase 6: Update CI To Match Reality

- [ ] Change CI so pull requests run `package + verify`.
- [ ] Run `audit` only where it provides signal you actually act on.
- [ ] Keep zip creation only on tags or release branches.
- [ ] Update [`README.md`](/Users/mblode/Code/mblode/glide/README.md#L21) and [`CONTRIBUTING.md`](/Users/mblode/Code/mblode/glide/CONTRIBUTING.md#L56) to reflect the split commands.

## Practical Default

If you want the simplest pragmatic move:

- Keep:
  - two canonical variable fonts
  - WOFF2 packaging
  - CSS
  - metadata verification
  - zip
- Move out of the default path:
  - FontLab prep
  - static instance validation
  - exact compare instances
  - donor proof assets
  - static OTF generation
- Keep only as optional:
  - static TTF/WOFF/WOFF2 bundles if you still care about older or non-variable consumers
