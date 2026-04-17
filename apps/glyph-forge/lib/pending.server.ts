import "server-only";

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";

import type { PendingTriageEdit } from "@glide/glyph-forge-engine";

const PENDING_PATH = resolve(
  process.cwd(),
  "..",
  "..",
  "packages",
  "glyph-forge",
  "manifests",
  "pending-triage-edits.json"
);

export async function readPending(): Promise<PendingTriageEdit[]> {
  try {
    const raw = await readFile(PENDING_PATH, "utf8");
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as PendingTriageEdit[]) : [];
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return [];
    throw err;
  }
}

export async function writePending(
  edits: PendingTriageEdit[]
): Promise<void> {
  await mkdir(dirname(PENDING_PATH), { recursive: true });
  await writeFile(PENDING_PATH, JSON.stringify(edits, null, 2), "utf8");
}

export function keyOf(edit: Pick<PendingTriageEdit, "family" | "glyph">): string {
  return `${edit.family}/${edit.glyph}`;
}

export function indexByKey(
  edits: PendingTriageEdit[]
): Map<string, PendingTriageEdit> {
  return new Map(edits.map((e) => [keyOf(e), e]));
}
