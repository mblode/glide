"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  useDeferredValue,
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent,
} from "react";

import { GlyphCanvas } from "@/components/glyph-canvas";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import {
  CHARSET,
  findGlyph,
  type CharsetEntry,
} from "@/lib/charset";
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

function columnCount(el: HTMLElement) {
  const first = el.firstElementChild as HTMLElement | null;
  if (!first) {
    return 1;
  }
  const cell = first.getBoundingClientRect().width;
  if (cell <= 0) {
    return 1;
  }
  return Math.max(1, Math.round(el.getBoundingClientRect().width / cell));
}

function glyphHref(entry: CharsetEntry) {
  return `/glyphs?g=${encodeURIComponent(entry.name)}`;
}

export function GlyphSet({ initialName }: { initialName?: string }) {
  const router = useRouter();
  const selected = findGlyph(initialName);
  const [weight, setWeight] = useState(400);
  const [style, setStyle] = useState<Style>("roman");
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query.trim());
  const italic = style === "italic";
  const gridRef = useRef<HTMLDivElement>(null);

  const filtered = useMemo(
    () => CHARSET.filter((entry) => matchesQuery(entry, deferredQuery)),
    [deferredQuery],
  );

  useEffect(() => {
    const node = document.getElementById(`glyph-${CSS.escape(selected.name)}`);
    node?.scrollIntoView({ block: "nearest", inline: "nearest" });
  }, [selected.name]);

  const inspect = (entry: CharsetEntry) => {
    router.push(glyphHref(entry), { scroll: false });
  };

  const onGridKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    const grid = gridRef.current;
    if (!grid || filtered.length === 0) {
      return;
    }

    const current = filtered.findIndex((entry) => entry.cp === selected.cp);
    const cols = columnCount(grid);
    let next = current < 0 ? 0 : current;

    switch (event.key) {
      case "ArrowRight":
        next = Math.min(filtered.length - 1, next + 1);
        break;
      case "ArrowLeft":
        next = Math.max(0, next - 1);
        break;
      case "ArrowDown":
        next = Math.min(filtered.length - 1, next + cols);
        break;
      case "ArrowUp":
        next = Math.max(0, next - cols);
        break;
      case "Home":
        next = 0;
        break;
      case "End":
        next = filtered.length - 1;
        break;
      default:
        return;
    }

    event.preventDefault();
    const entry = filtered[next];
    if (entry) {
      inspect(entry);
    }
  };

  const canvasLabel = `${selected.name}, U+${selected.hex}`;

  return (
    <div className="flex flex-1 flex-col lg:min-h-0">
      <div className="flex flex-col gap-4 border-b border-border px-4 py-3 sm:flex-row sm:flex-wrap sm:items-end sm:justify-between sm:px-6">
        <div role="radiogroup" aria-label="Style" className="flex gap-1">
          {(["roman", "italic"] as const).map((s) => (
            <Button
              key={s}
              type="button"
              size="sm"
              variant={style === s ? "default" : "outline"}
              role="radio"
              aria-checked={style === s}
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
            <div
              className="text-lg font-semibold tabular-nums tracking-tight"
              style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
            >
              {weight}
            </div>
          </div>
          <Slider
            id="glyphs-weight"
            aria-label="Glyph weight"
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
            placeholder="Name, character, or U+"
            autoComplete="off"
            spellCheck={false}
          />
        </div>
      </div>

      <div className="grid lg:min-h-0 lg:flex-1 lg:grid-cols-2">
        <section
          aria-label="Glyph inspector"
          className="flex h-[min(50vh,28rem)] min-h-0 flex-col border-b border-border lg:h-auto lg:border-r lg:border-b-0"
        >
          <div className="relative flex items-center justify-center px-4 py-3">
            <div className="text-center">
              <div
                aria-live="polite"
                className="font-semibold tracking-tight"
              >
                {selected.name}
              </div>
              <div className="font-mono text-sm tabular-nums text-muted-foreground">
                U+{selected.hex}
              </div>
            </div>
            <div
              aria-hidden="true"
              className="absolute right-4 text-3xl"
              style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
            >
              {selected.cp === 0x20 ? (
                <span className="block h-px w-5 bg-foreground/35" />
              ) : (
                selected.char
              )}
            </div>
          </div>

          <GlyphCanvas
            char={selected.char}
            cp={selected.cp}
            italic={italic}
            label={canvasLabel}
            weight={weight}
          />
        </section>

        <section
          aria-label="Glyph index"
          className="flex min-h-0 flex-col lg:overflow-y-auto"
        >
          <p className="px-4 py-3 text-muted-foreground text-sm sm:px-5">
            Showing {filtered.length} of {CHARSET.length} printable encoded glyphs.
          </p>

          {filtered.length === 0 ? (
            <p className="px-4 py-10 text-center text-muted-foreground text-sm sm:px-5">
              No glyphs match “{deferredQuery}”. Clear the search to see the
              full set.
            </p>
          ) : (
            <div
              ref={gridRef}
              role="listbox"
              aria-label="Encoded glyphs"
              aria-activedescendant={`glyph-${selected.name}`}
              tabIndex={0}
              onKeyDown={onGridKeyDown}
              className="grid grid-cols-[repeat(auto-fill,minmax(3rem,1fr))] gap-px bg-border outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-inset"
              style={{
                fontWeight: weight,
                fontStyle: italic ? "italic" : "normal",
              }}
            >
              {filtered.map((entry) => {
                const active = entry.cp === selected.cp;
                return (
                  <Link
                    key={entry.cp}
                    id={`glyph-${entry.name}`}
                    href={glyphHref(entry)}
                    scroll={false}
                    prefetch={false}
                    role="option"
                    aria-selected={active}
                    title={`${entry.name} · U+${entry.hex}`}
                    className={cn(
                      "relative flex aspect-square items-center justify-center bg-background",
                      "focus-visible:z-10 focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-inset",
                      active
                        ? "bg-foreground text-background"
                        : "hover:bg-foreground/8",
                    )}
                  >
                    <span className="absolute top-1/2 left-1/2 size-[max(100%,3rem)] -translate-x-1/2 -translate-y-1/2 pointer-fine:hidden" />
                    {entry.cp === 0x20 ? (
                      <span
                        aria-hidden="true"
                        className="block h-px w-5 bg-current opacity-40"
                      />
                    ) : (
                      <div aria-hidden="true" className="text-2xl">
                        {entry.char}
                      </div>
                    )}
                    <span className="sr-only">
                      {entry.name}, U+{entry.hex}
                    </span>
                  </Link>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
