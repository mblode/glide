import "server-only";

import { readFile } from "node:fs/promises";
import { join } from "node:path";

import type {
  BrokenGlyph,
  CellScores,
  GlyphScores,
  SolverVerdict,
  StrategySuggestion,
} from "@glide/glyph-forge-engine";

let manifestCache: BrokenGlyph[] | null = null;
let glyphScoresCache: Record<string, GlyphScores> | null | undefined =
  undefined;
let cellScoresCache: Record<string, CellScores> | null | undefined = undefined;
let suggestionsCache:
  | Record<string, StrategySuggestion>
  | null
  | undefined = undefined;
let solverResultsCache:
  | Record<string, SolverVerdict>
  | null
  | undefined = undefined;

function publicFile(name: string): string {
  return join(process.cwd(), "public", name);
}

export async function loadManifest(): Promise<BrokenGlyph[]> {
  if (manifestCache) return manifestCache;
  const raw = await readFile(publicFile("broken-glyphs.json"), "utf8");
  manifestCache = JSON.parse(raw) as BrokenGlyph[];
  return manifestCache;
}

async function tryLoad<T>(filename: string): Promise<T | null> {
  try {
    const raw = await readFile(publicFile(filename), "utf8");
    return JSON.parse(raw) as T;
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return null;
    throw err;
  }
}

export async function loadGlyphScores(): Promise<Record<
  string,
  GlyphScores
> | null> {
  if (glyphScoresCache !== undefined) return glyphScoresCache;
  glyphScoresCache = await tryLoad<Record<string, GlyphScores>>(
    "glyph-scores.json"
  );
  return glyphScoresCache;
}

export async function loadCellScores(): Promise<Record<
  string,
  CellScores
> | null> {
  if (cellScoresCache !== undefined) return cellScoresCache;
  cellScoresCache = await tryLoad<Record<string, CellScores>>(
    "cell-scores.json"
  );
  return cellScoresCache;
}

export async function loadSuggestions(): Promise<Record<
  string,
  StrategySuggestion
> | null> {
  if (suggestionsCache !== undefined) return suggestionsCache;
  suggestionsCache = await tryLoad<Record<string, StrategySuggestion>>(
    "strategy-suggestions.json"
  );
  return suggestionsCache;
}

export async function loadSolverResults(): Promise<Record<
  string,
  SolverVerdict
> | null> {
  if (solverResultsCache !== undefined) return solverResultsCache;
  solverResultsCache = await tryLoad<Record<string, SolverVerdict>>(
    "solver-results.json"
  );
  return solverResultsCache;
}
