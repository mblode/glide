# Contributing

This repo follows a simple split:

- source assets in `src/`
- proof source in `docs/proof/`
- generated build intermediates in `build/work/`
- packaged release artifacts in `build/release/`

## Prerequisites

- Python 3
- FontForge CLI

Setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
brew install fontforge
```

## Main Commands

Build everything:

```bash
make build
```

Verify packaged output:

```bash
make verify
```

Delete generated output:

```bash
make clean
```

Create a release zip:

```bash
make zip
```

Serve the proof pages:

```bash
make proof
```

## Build Flow

`make build` runs the release orchestrator in `build/release.py`, which does this:

1. Extract Roman checkpoints from `src/glide-variable.ttf`
2. Seed Glide Italic from the Circular donors in `src/donors/circular/`
3. Run the compatibility repair prep step
4. Build Roman and Italic variable fonts
5. Generate static named instances
6. Package web and desktop formats into `build/release/`
7. Generate the packaged proof and metadata

## Proofing

Two proof URLs are useful:

- `docs/proof/index.html`
  - source proof that reads from `build/release/`
- `build/release/proof/index.html`
  - packaged proof with release-relative paths

The proof page includes:

- Roman/Italic side-by-side review
- a weight slider
- named checkpoints
- a kerning lab comparing Circular donor italics, exact static matches, and the live Glide italic VF

## Manual FontLab / Glyphs Work

The build can prepare repaired static masters in `build/work/fontlab-ready/`, but the remaining design work is still manual where needed.

Typical manual steps:

1. Open the prepared masters in FontLab or Glyphs.
2. Review remaining compatibility issues, especially around the known `700` interpolation drift.
3. Refine seeded italic shapes that still feel too slanted instead of truly italic.
4. Export repaired statics back into the scripted pipeline if you want to carry those edits forward.

## Versioning

The release version lives in `version.txt`.

Release metadata and archive naming both read from that file.
