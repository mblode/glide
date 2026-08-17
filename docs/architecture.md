# Public repository architecture

**Trust: Authoritative.** This document describes the current Glide 3.1 public
repository contract.

## Three-repository boundary

| Repository | Owns | Does not own |
| --- | --- | --- |
| `static-to-variable` | Generic conversion and variable-font engine | Glide-specific donor repairs |
| `static-to-variable-glide` | Private Glide reconstruction, proofing, manifests, and release preparation | Public site behavior |
| `glide` | Reviewed Glyphs sources, public binaries, immutable releases, and specimen site | Donor reconstruction logic |

Changes cross repositories through built artifacts and a checksum manifest,
not imports or machine-specific sibling paths.

## Public asset flow

`fonts/` is the canonical public binary set. A release promotion copies the
approved set atomically to:

1. `fonts/web/` for self-hosting examples;
2. `apps/web/public/` for the current download aliases and specimen;
3. `apps/web/public/<version>/` for immutable downloads; and
4. `apps/web/public/glide.zip` for desktop installation.

`scripts/check-release-artifacts.py` verifies canonical files, public mirrors,
ZIP members, and versioned manifests. Do not fix a failed mirror check by
choosing whichever copy looks newest; return to the approved manifest.

## Generated surfaces

- `apps/web/lib/charset.ts` and `font-metrics.ts` come from
  `fonts/glide-variable.ttf` via `scripts/update-font-metadata.py`.
- `README.md` install blocks mirror `apps/web/lib/install-snippets.ts` and are
  checked by `scripts/check-install-docs.py`.
- `fonts/static/` is disposable output from `scripts/make-desktop-bundle.py`.
- The app loads fonts from `apps/web/public/`; `apps/web/app/fonts/` is not a
  release authority.

## Site boundary

The npm workspace contains one Next.js app at `apps/web`. It is deployed under
`/glide`, so raw asset URLs use `asset()` while Next links use the configured
base path. Font binaries are local assets; no third-party font host is needed.

Tracked `.claude/` experiments are legacy evidence. They are not architecture,
release input, or permission to add more generated experiments to git.
