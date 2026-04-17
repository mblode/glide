import { NextResponse, type NextRequest } from "next/server";

import {
  STRATEGY_NAMES,
  type PendingTriageEdit,
  type StrategyName,
} from "@glide/glyph-forge-engine";

import { loadManifest } from "@/lib/data.server";
import { indexByKey, keyOf, readPending, writePending } from "@/lib/pending.server";

type StageBody = {
  family: "roman" | "italic";
  glyph: string;
  strategy: StrategyName;
  source: "suggestion" | "manual";
  notes?: string;
};

function isValidBody(x: unknown): x is StageBody {
  if (!x || typeof x !== "object") return false;
  const b = x as Record<string, unknown>;
  return (
    (b.family === "roman" || b.family === "italic") &&
    typeof b.glyph === "string" &&
    b.glyph.length > 0 &&
    typeof b.strategy === "string" &&
    (STRATEGY_NAMES as readonly string[]).includes(b.strategy) &&
    (b.source === "suggestion" || b.source === "manual") &&
    (b.notes === undefined || typeof b.notes === "string")
  );
}

export async function POST(req: NextRequest) {
  const raw = await req.json().catch(() => null);
  if (!isValidBody(raw)) {
    return NextResponse.json({ error: "invalid body" }, { status: 400 });
  }

  const manifest = await loadManifest();
  const entry = manifest.find(
    (g) => g.family === raw.family && g.name === raw.glyph
  );
  if (!entry) {
    return NextResponse.json({ error: "glyph not in manifest" }, { status: 404 });
  }

  const pending = await readPending();
  const byKey = indexByKey(pending);
  const edit: PendingTriageEdit = {
    family: raw.family,
    glyph: raw.glyph,
    strategy: raw.strategy,
    source: raw.source,
    notes: raw.notes,
    stagedAt: new Date().toISOString(),
    previousStrategy: entry.existingStrategy ?? null,
  };
  byKey.set(keyOf(edit), edit);
  const next = Array.from(byKey.values()).sort((a, b) =>
    keyOf(a).localeCompare(keyOf(b))
  );
  await writePending(next);
  return NextResponse.json({ ok: true, edit, count: next.length });
}
