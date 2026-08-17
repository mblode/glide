"use client";

import { useEffect, useRef, useState, type KeyboardEvent } from "react";

import { GlyphCanvas } from "@/components/glyph-canvas";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { CHARSET, findGlyph, type CharsetEntry } from "@/lib/charset";
import { cn } from "@/lib/utils";

type Style = "roman" | "italic" | "mono";

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

export function GlyphSet() {
  /*
    Selection is local state. It used to live in the URL (`/glyphs?g=`) because
    the inspector had its own page; now that it sits in the homepage flow, a
    router push would scroll the page and add a history entry per glyph.
  */
  const [selectedName, setSelectedName] = useState<string | undefined>();
  const selected = findGlyph(selectedName);
  const [weight, setWeight] = useState(400);
  const [style, setStyle] = useState<Style>("roman");
  const italic = style === "italic";
  // Same as the specimen: Glide Mono is not a variable font, so it renders at
  // its single 400 cut and the weight slider is disabled.
  const mono = style === "mono";
  const effectiveWeight = mono ? 400 : weight;
  const gridRef = useRef<HTMLDivElement>(null);

  /*
    Keyboard navigation can walk the selection off screen, so it needs to be
    followed. The mount guard matters: without it this would yank the page down
    to the glyph grid the moment the homepage loads.
  */
  const hasMounted = useRef(false);
  useEffect(() => {
    if (!hasMounted.current) {
      hasMounted.current = true;
      return;
    }
    const node = document.getElementById(`glyph-${CSS.escape(selected.name)}`);
    node?.scrollIntoView({ block: "nearest", inline: "nearest" });
  }, [selected.name]);

  const inspect = (entry: CharsetEntry) => {
    setSelectedName(entry.name);
  };

  const onGridKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    const grid = gridRef.current;
    if (!grid || CHARSET.length === 0) {
      return;
    }

    const current = CHARSET.findIndex((entry) => entry.cp === selected.cp);
    const cols = columnCount(grid);
    let next = current < 0 ? 0 : current;

    switch (event.key) {
      case "ArrowRight":
        next = Math.min(CHARSET.length - 1, next + 1);
        break;
      case "ArrowLeft":
        next = Math.max(0, next - 1);
        break;
      case "ArrowDown":
        next = Math.min(CHARSET.length - 1, next + cols);
        break;
      case "ArrowUp":
        next = Math.max(0, next - cols);
        break;
      case "Home":
        next = 0;
        break;
      case "End":
        next = CHARSET.length - 1;
        break;
      default:
        return;
    }

    event.preventDefault();
    const entry = CHARSET[next];
    if (entry) {
      inspect(entry);
    }
  };

  const canvasLabel = `${selected.name}, U+${selected.hex}`;

  return (
    /*
      Sits in the homepage flow now, so none of the old dvh shell survives: no
      `flex-1`, no `min-h-0`, and no inner `overflow-y-auto`. The section grows
      to its content and the page is the only thing that scrolls.
    */
    <section aria-labelledby="characters-heading" id="characters">
      <h2 className="sr-only" id="characters-heading">
        Characters
      </h2>
      <div className="flex flex-col gap-4 border-border border-y px-[var(--row-padding)] py-3 sm:flex-row sm:flex-wrap sm:items-end sm:justify-between">
        <div role="radiogroup" aria-label="Style" className="flex gap-1">
          {(["roman", "italic", "mono"] as const).map((s) => (
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
              style={{
                fontFamily: mono
                  ? "var(--font-glide-mono), monospace"
                  : "var(--font-glide), sans-serif",
                fontWeight: effectiveWeight,
                fontStyle: italic ? "italic" : "normal",
              }}
            >
              {effectiveWeight}
            </div>
          </div>
          <Slider
            id="glyphs-weight"
            aria-label="Glyph weight"
            min={100}
            max={950}
            step={1}
            disabled={mono}
            value={[effectiveWeight]}
            onValueChange={([v]) => setWeight(v)}
          />
        </div>
      </div>

      <div className="grid lg:grid-cols-2">
        <section
          aria-label="Glyph inspector"
          className="flex h-[min(60vh,40rem)] flex-col border-border border-b lg:border-r lg:border-b-0"
        >
          <div className="relative flex items-center justify-center px-4 py-3">
            <div className="text-center">
              <div aria-live="polite" className="font-semibold tracking-tight">
                {selected.name}
              </div>
              <div className="font-mono text-sm tabular-nums text-muted-foreground">
                U+{selected.hex}
              </div>
            </div>
            <div
              aria-hidden="true"
              className="absolute right-4 text-3xl"
              style={{
                fontFamily: mono
                  ? "var(--font-glide-mono), monospace"
                  : "var(--font-glide), sans-serif",
                fontWeight: effectiveWeight,
                fontStyle: italic ? "italic" : "normal",
              }}
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
            mono={mono}
            weight={effectiveWeight}
          />
        </section>

        {/*
          Capped to the inspector's height so the two columns end level and 501
          cells do not run the page on for thousands of pixels. This is the one
          place a scrollbar earns its keep.
        */}
        <section
          aria-label="Glyph index"
          className="flex h-[min(60vh,40rem)] min-h-0 flex-col"
        >
          <div
            ref={gridRef}
            role="listbox"
            aria-label="Encoded glyphs"
            aria-activedescendant={`glyph-${selected.name}`}
            tabIndex={0}
            onKeyDown={onGridKeyDown}
            className="grid min-h-0 flex-1 grid-cols-[repeat(auto-fill,minmax(3rem,1fr))] gap-px overflow-y-auto quiet-scrollbar bg-border outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-inset"
            style={{
              fontFamily: mono
                ? "var(--font-glide-mono), monospace"
                : "var(--font-glide), sans-serif",
              fontWeight: effectiveWeight,
              fontStyle: italic ? "italic" : "normal",
            }}
          >
            {CHARSET.map((entry) => {
              const active = entry.cp === selected.cp;
              return (
                <button
                  key={entry.cp}
                  id={`glyph-${entry.name}`}
                  type="button"
                  tabIndex={-1}
                  onClick={() => inspect(entry)}
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
                </button>
              );
            })}
          </div>
        </section>
      </div>
    </section>
  );
}
