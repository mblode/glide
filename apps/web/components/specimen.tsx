"use client";

import { type CSSProperties, useState } from "react";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";

type Family = "sans" | "italic" | "mono";

const families: { id: Family; label: string }[] = [
  { id: "sans", label: "Roman" },
  { id: "italic", label: "Italic" },
  { id: "mono", label: "Mono" },
];

const namedWeights = [
  { weight: 100, name: "Thin" },
  { weight: 200, name: "ExtraLight" },
  { weight: 300, name: "Light" },
  { weight: 400, name: "Regular" },
  { weight: 500, name: "Medium" },
  { weight: 600, name: "Semibold" },
  { weight: 700, name: "Bold" },
  { weight: 800, name: "Extrabold" },
  { weight: 900, name: "Black" },
  { weight: 950, name: "Extra Black" },
] as const;

const DEFAULT_WEIGHT = 400;
const DEFAULT_SIZE = 20;

/*
  Owned by contentEditable after first paint. React only rewrites
  dangerouslySetInnerHTML when the string itself changes, and this one is a
  constant, so re-rendering on every slider tick cannot wipe what you typed.
*/
const DEFAULT_DISPLAY = "Handgloves";

// Read-only: this copy is the argument for the typeface, not a sandbox.
const paragraphs = [
  "Glide is drawn for interfaces: the places where type has to survive small sizes, tight rows, and a reader who is not reading for pleasure. The brief was legibility under pressure, so the apertures are open, the letterforms are unambiguous, and the rhythm holds even when a label runs long.",
  "Three masters are drawn by hand: Thin, Regular, and Extra Black. Everything between them is interpolated, which is what lets a single variable file cover the whole 100–950 range without shipping ten static files to the browser.",
  "The optical size axis adapts the letterforms to the size they are set at. Below about sixteen pixels the shapes open up and the spacing loosens; above it the joins tighten and the counters close, so a headline keeps its colour instead of falling apart.",
  "The family covers roman, italic, and a monospaced companion for code, tabular data, and anywhere a column of characters has to line up. All of it is free under the SIL Open Font License.",
];

function nearestName(weight: number) {
  return namedWeights.reduce((best, entry) =>
    Math.abs(entry.weight - weight) < Math.abs(best.weight - weight)
      ? entry
      : best
  ).name;
}

export function Specimen() {
  const [family, setFamily] = useState<Family>("sans");
  const [weight, setWeight] = useState(DEFAULT_WEIGHT);
  const [size, setSize] = useState(DEFAULT_SIZE);

  const mono = family === "mono";
  const italic = family === "italic";
  // Glide Mono is not a variable font: it ships as a single 400 cut, so the
  // weight slider is disabled rather than offering a range that does not exist.
  const effectiveWeight = mono ? DEFAULT_WEIGHT : weight;

  return (
    /*
      The anchor stays `#playground`: lib/markdown.ts and the MCP
      `open_playground` tool both address this section by that id.
    */
    <section aria-labelledby="specimen-heading" id="playground">
      {/*
        The heading is visually dropped but kept for the section's accessible
        name; the controls are the only thing on this row now, aligned on their
        bottom edge so the buttons and slider tracks sit on one line.
      */}
      <h2 className="sr-only" id="specimen-heading">
        Specimen
      </h2>
      <div className="flex flex-wrap items-end gap-x-8 gap-y-5 border-border border-y px-[var(--row-padding)] py-5">
        <div aria-label="Style" className="flex gap-1" role="radiogroup">
          {families.map((entry) => (
            <Button
              aria-checked={family === entry.id}
              className="max-sm:h-11"
              key={entry.id}
              onClick={() => setFamily(entry.id)}
              role="radio"
              size="sm"
              type="button"
              variant={family === entry.id ? "default" : "outline"}
            >
              {entry.label}
            </Button>
          ))}
        </div>

        <div className="w-full space-y-2 sm:w-64">
          <div className="flex items-baseline justify-between gap-3 text-sm">
            <Label htmlFor="specimen-weight">Weight</Label>
            <span className="text-muted-foreground tabular-nums">
              {nearestName(effectiveWeight)} · {effectiveWeight}
            </span>
          </div>
          <Slider
            aria-label="Weight"
            disabled={mono}
            id="specimen-weight"
            max={950}
            min={100}
            onValueChange={([value]) => setWeight(value)}
            step={1}
            value={[effectiveWeight]}
          />
        </div>

        {/*
          The headline already caps with `vw` on a narrow measure, so a size
          dial on phones only burns a row. Keep it from `sm` up, where there
          is room to judge scale.
        */}
        <div className="hidden w-full space-y-2 sm:block sm:w-64">
          <div className="flex items-baseline justify-between gap-3 text-sm">
            <Label htmlFor="specimen-size">Size</Label>
            <span className="text-muted-foreground tabular-nums">{size}px</span>
          </div>
          <Slider
            aria-label="Size"
            id="specimen-size"
            max={40}
            min={12}
            onValueChange={([value]) => setSize(value)}
            step={1}
            value={[size]}
          />
        </div>

      </div>

      <div className="px-[var(--row-padding)] py-[var(--row-padding-vertical)]">
        <p className="pb-6 text-muted-foreground text-sm">
          Type your own headline.
        </p>

        {/*
          The size dial drives the headline and nothing else. The headline is
          the specimen — the thing you set, read, and judge — so it is sized in
          `em` off the dial, with a `vw` cap so it fills the measure instead of
          overflowing it. Both numbers keep the default word on one line at the
          default size; a headline that wraps reads as a bug, not as scale.

          The copy below is the argument for the typeface, not a sandbox, so it
          holds a fixed reading size. Resizing it with the dial made the page
          reflow around prose nobody was inspecting, and at the low end it drove
          an explanation of the typeface down to 12px.
        */}
        <div
          className="break-words"
          style={
            {
              fontFamily: mono
                ? "var(--font-glide-mono), monospace"
                : "var(--font-glide), sans-serif",
              fontWeight: effectiveWeight,
              fontStyle: italic ? "italic" : "normal",
              fontSize: `${size}px`,
              lineHeight: 1.55,
              // Display type wants negative tracking; mono does not — pulling
              // its glyphs together fights the fixed advance width the face
              // exists to keep.
              "--display-tracking": mono ? "normal" : "-0.02em",
              columnWidth: "34rem",
              columnGap: "2.5rem",
            } as CSSProperties
          }
        >
          <h3
            aria-label="Headline sample text"
            className="mb-[0.35em] text-[min(9em,15vw)] leading-[1.02] tracking-[var(--display-tracking)] outline-none [column-span:all]"
            contentEditable
            dangerouslySetInnerHTML={{ __html: DEFAULT_DISPLAY }}
            role="textbox"
            spellCheck={false}
            suppressContentEditableWarning
          />
          {paragraphs.map((paragraph) => (
            <p
              className="mb-[0.8em] text-pretty text-base leading-[1.55] last:mb-0"
              key={paragraph}
            >
              {paragraph}
            </p>
          ))}
        </div>
      </div>
    </section>
  );
}
