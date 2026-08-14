"use client";

import { useDeferredValue, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { CHARSET, type CharsetEntry } from "@/lib/charset";
import { cn } from "@/lib/utils";

type Style = "roman" | "italic";

function matchesQuery(entry: CharsetEntry, query: string): boolean {
  if (!query) {
    return true;
  }
  const q = query.toLowerCase();
  return (
    entry.name.toLowerCase().includes(q) ||
    entry.hex.toLowerCase().includes(q) ||
    entry.char.toLowerCase().includes(q) ||
    `u+${entry.hex}`.toLowerCase().includes(q)
  );
}

export function GlyphSet() {
  const [weight, setWeight] = useState(400);
  const [style, setStyle] = useState<Style>("roman");
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query.trim());
  const italic = style === "italic";

  const filtered = useMemo(
    () => CHARSET.filter((entry) => matchesQuery(entry, deferredQuery)),
    [deferredQuery]
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-5 sm:flex-row sm:flex-wrap sm:items-end sm:justify-between">
        <div className="flex gap-1">
          {(["roman", "italic"] as const).map((s) => (
            <Button
              key={s}
              size="sm"
              variant={style === s ? "default" : "outline"}
              onClick={() => setStyle(s)}
              className="capitalize"
            >
              {s}
            </Button>
          ))}
        </div>

        <div className="w-full max-w-sm space-y-2 sm:flex-1">
          <div className="flex items-baseline justify-between">
            <Label htmlFor="glyphs-weight">Weight</Label>
            <span
              className="text-lg font-bold tabular-nums tracking-tight"
              style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
            >
              {weight}
            </span>
          </div>
          <Slider
            id="glyphs-weight"
            min={100}
            max={950}
            step={1}
            value={[weight]}
            onValueChange={([v]) => setWeight(v)}
          />
        </div>

        <div className="w-full max-w-xs space-y-2">
          <Label htmlFor="glyphs-search">Search</Label>
          <Input
            id="glyphs-search"
            clearable
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onClear={() => setQuery("")}
            placeholder="Name, character, or U+…"
            autoComplete="off"
            spellCheck={false}
          />
        </div>
      </div>

      <p className="text-muted-foreground text-sm">
        Showing {filtered.length} of {CHARSET.length} encoded glyphs in the shipped
        webfont.
      </p>

      {filtered.length === 0 ? (
        <p className="rounded-xl border border-border bg-background/40 px-4 py-10 text-center text-muted-foreground text-sm">
          No glyphs match “{deferredQuery}”.
        </p>
      ) : (
        <div
          className="grid gap-px overflow-hidden rounded-xl border border-border bg-border [grid-template-columns:repeat(auto-fill,minmax(5.5rem,1fr))]"
          style={{
            fontWeight: weight,
            fontStyle: italic ? "italic" : "normal",
          }}
        >
          {filtered.map((entry) => (
            <div
              key={entry.cp}
              className={cn(
                "group relative flex aspect-square flex-col items-center justify-center gap-1 bg-card/80 p-2",
                "hover:bg-background/70"
              )}
              title={`${entry.name} · U+${entry.hex}`}
            >
              <span
                className="flex h-7 items-center justify-center text-[1.75rem] leading-none"
                aria-hidden={entry.cp === 0x20}
              >
                {entry.cp === 0x20 ? (
                  <span className="block h-px w-5 bg-muted-foreground/35" />
                ) : (
                  entry.char
                )}
              </span>
              <span className="max-w-full truncate font-mono text-[9px] text-muted-foreground opacity-70 transition-opacity group-hover:opacity-100">
                {entry.name}
              </span>
              <span className="sr-only">
                {entry.name}, U+{entry.hex}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
