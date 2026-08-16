# Verification and release

**Trust: Authoritative.** These commands are the local and CI release gates.

## Verification tiers

| Tier | Command | Use | Gate |
| --- | --- | --- | --- |
| Fast | `npm run check` | Every edit | README install blocks match their source |
| Standard | `npm run verify` | Every pull request | Fast check, generated metadata, font mirrors, manifests, ZIP members, and production build |
| Release | `npm run verify:full` | Font publication | Standard verification plus a clean desktop-bundle rebuild matching the committed ZIP byte for byte |

The standard tier is intentionally the same command used by pull-request and
main-branch CI. A local pass and CI pass therefore mean the same thing.
`requirements-release.txt` pins the fontTools stack used by the deterministic
bundle check, so a dependency update is an explicit reviewed change.

## Promote a release

1. Build and approve the release in `static-to-variable-glide`.
2. Copy the complete manifest-approved artifact set into this repository.
3. Regenerate font metadata with
   `python3 scripts/update-font-metadata.py`.
4. Update install snippets, version metadata, immutable assets, and current
   aliases in the same change.
5. Run `npm run verify:full` from a clean checkout.
6. Merge the verified change before creating its `v*` tag.

The tag workflow reruns the release tier and publishes the already verified
desktop ZIP. A tag must point at the commit containing the matching immutable
version directory.

## Failure handling

- Documentation failure: edit `install-snippets.ts`, then mirror the exact
  checked block into `README.md`.
- Metadata failure: regenerate from the canonical Roman TTF; do not hand-edit
  generated TypeScript.
- Mirror or manifest failure: stop promotion and recopy the approved release as
  a unit.
- Bundle mismatch: rebuild from the reviewed variable fonts and investigate the
  first differing input; do not overwrite the checked ZIP merely to turn the
  gate green.
- Production build failure: fix the app before tagging. Font validation does
  not waive TypeScript or Next.js failures.

`apps/web/public/3.002/` remains the immediate rollback set. Rollback changes
current aliases only; immutable version directories remain untouched.
