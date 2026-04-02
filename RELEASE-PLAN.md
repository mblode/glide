# Inter-Inspired Glide Plan

## Phase 1. Separate Source From Generated Output

- [x] Move the canonical Glide basis into `src/`
- [x] Move Circular donors into `src/donors/circular/`
- [x] Move proof source into `docs/proof/`
- [x] Keep generated intermediates under `build/work/`
- [x] Keep packaged release output under `build/release/`

## Phase 2. Add One Public Command Surface

- [x] Add a root `Makefile`
- [x] Expose `build`, `verify`, `clean`, `zip`, and `proof`
- [x] Keep the Python orchestration in `build/release.py`

## Phase 3. Make Versioning Explicit

- [x] Add `version.txt`
- [x] Make packaged release metadata read from `version.txt`
- [x] Make the archive name read from `version.txt`

## Phase 4. Split User Docs And Contributor Docs

- [x] Keep `README.md` release and usage focused
- [x] Add `CONTRIBUTING.md` for build and proof workflow
- [x] Update docs to reflect `src/`, `build/work/`, and `build/release/`

## Phase 5. Make Proofing First-Class

- [x] Move the source proof out of `build/` and into `docs/proof/`
- [x] Keep the proof reading generated fonts instead of source fonts
- [x] Generate a packaged proof in `build/release/proof/`

## Phase 6. Make Release Packaging Reproducible

- [x] Build variable `TTF`, `WOFF2`, and `WOFF`
- [x] Build static `TTF`, `OTF`, `WOFF2`, and `WOFF`
- [x] Generate `build/release/fonts/glide.css`
- [x] Generate `build/release/metadata/release.json`
- [x] Generate a versioned release zip

## Phase 7. Add CI

- [x] Add a build-and-release workflow
- [x] Add a Pages deployment workflow for the packaged proof

## Phase 8. Clean Legacy Structure

- [x] Remove the root `sample/` layout
- [x] Remove root generated `release/` and `work/`
- [x] Keep the repo free of the legacy source name in tracked files
