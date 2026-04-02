# Glide

Glide is a sans-serif type family by Matthew Blode.

This repository builds and packages two variable fonts:

- `glide-variable.ttf`
- `glide-variable-italic.ttf`

The release output lives in `build/release/`. Source assets live in `src/`. Generated intermediates live in `build/work/`.

## Install The Build Tooling

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
brew install fontforge
```

## Build

```bash
make build
```

This rebuilds:

- variable `TTF`, `WOFF2`, and `WOFF`
- static `TTF`, `OTF`, `WOFF2`, and `WOFF`
- `build/release/fonts/glide.css`
- `build/release/proof/index.html`
- `build/release/metadata/release.json`

## Verify

```bash
make verify
```

## Proof

```bash
make proof
```

Open:

- `http://127.0.0.1:8765/docs/proof/index.html` for the source proof
- `http://127.0.0.1:8765/build/release/proof/index.html` for the packaged proof

## Release Archive

```bash
make zip
```

This creates `build/release/Glide-$(cat version.txt).zip`.

## Repo Layout

- `src/glide-variable.ttf`: canonical Glide outline basis
- `src/donors/circular/`: Circular donors used for italic seeding and kerning reference
- `build/`: build scripts plus generated `work/` and `release/`
- `docs/proof/`: proof source
- `version.txt`: release version

## Notes

- The public family name is `Glide`.
- The packaged fonts carry Matthew Blode in designer and manufacturer metadata.
- Roman and Italic are shipped as separate variable fonts, which is the standard release model for a true-italic family.
- Contributor workflow is documented in `CONTRIBUTING.md`.
