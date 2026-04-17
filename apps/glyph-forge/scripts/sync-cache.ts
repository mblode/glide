#!/usr/bin/env tsx
/**
 * Mirror packages/glyph-forge/public-cache/svg/ and manifests/broken-glyphs.json
 * into apps/glyph-forge/public/ before dev or build.
 *
 * Runs as predev/prebuild. Idempotent.
 */
import { cp, mkdir, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const appRoot = resolve(__dirname, "..");
const repoRoot = resolve(appRoot, "..", "..");

const enginePackageRoot = resolve(repoRoot, "packages", "glyph-forge");
const engineCache = resolve(enginePackageRoot, "public-cache", "svg");
const engineManifest = resolve(
  enginePackageRoot,
  "manifests",
  "broken-glyphs.json"
);
const engineGlyphScores = resolve(
  enginePackageRoot,
  "manifests",
  "glyph-scores.json"
);
const engineCellScores = resolve(
  enginePackageRoot,
  "manifests",
  "cell-scores.json"
);
const engineSuggestions = resolve(
  enginePackageRoot,
  "manifests",
  "strategy-suggestions.json"
);
const engineSolverResults = resolve(
  enginePackageRoot,
  "manifests",
  "solver-results.json"
);

const targetSvgDir = resolve(appRoot, "public", "svg");
const targetManifest = resolve(appRoot, "public", "broken-glyphs.json");
const targetGlyphScores = resolve(appRoot, "public", "glyph-scores.json");
const targetCellScores = resolve(appRoot, "public", "cell-scores.json");
const targetSuggestions = resolve(
  appRoot,
  "public",
  "strategy-suggestions.json"
);
const targetSolverResults = resolve(appRoot, "public", "solver-results.json");

async function exists(path: string): Promise<boolean> {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

async function main() {
  if (!(await exists(engineManifest))) {
    console.error(
      `glyph-forge: manifest not found at ${engineManifest}.\n` +
        `Run \`npm run forge:build\` from the repo root first.`
    );
    process.exit(1);
  }

  await mkdir(resolve(appRoot, "public"), { recursive: true });

  if (await exists(engineCache)) {
    await cp(engineCache, targetSvgDir, { recursive: true, force: true });
    console.log(`glyph-forge: synced SVG cache → ${targetSvgDir}`);
  } else {
    console.warn(
      `glyph-forge: no SVG cache at ${engineCache} yet. Grid will render missing-thumbnail placeholders until you run \`npm run forge:build\`.`
    );
  }

  await cp(engineManifest, targetManifest, { force: true });
  console.log(`glyph-forge: synced manifest → ${targetManifest}`);

  for (const [src, dst, label] of [
    [engineGlyphScores, targetGlyphScores, "glyph-scores"],
    [engineCellScores, targetCellScores, "cell-scores"],
    [engineSuggestions, targetSuggestions, "strategy-suggestions"],
    [engineSolverResults, targetSolverResults, "solver-results"],
  ] as const) {
    if (await exists(src)) {
      await cp(src, dst, { force: true });
      console.log(`glyph-forge: synced ${label} → ${dst}`);
    } else {
      console.log(
        `glyph-forge: no ${label} at ${src} (optional — run \`npm run forge:build\` to generate)`
      );
    }
  }
}

main().catch((err) => {
  console.error("glyph-forge: sync failed");
  console.error(err);
  process.exit(1);
});
