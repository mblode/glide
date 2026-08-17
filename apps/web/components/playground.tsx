"use client";

import { useState, type CSSProperties } from "react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { cn } from "@/lib/utils";

type Mode = "roman" | "italic" | "mono";

const modes: { id: Mode; label: string }[] = [
  { id: "roman", label: "Roman" },
  { id: "italic", label: "Italic" },
  { id: "mono", label: "Mono" },
];

export function Playground() {
  const [weight, setWeight] = useState(700);
  const [size, setSize] = useState(72);
  const [mode, setMode] = useState<Mode>("roman");
  const [tabularNums, setTabularNums] = useState(true);
  const [slashedZero, setSlashedZero] = useState(true);
  const [automaticOpticalSize, setAutomaticOpticalSize] = useState(true);
  const [text, setText] = useState(
    "Glide variable font\n11:45 0123456789 100,000 · 0 O o Ø",
  );

  const mono = mode === "mono";
  const italic = mode === "italic";
  const renderedWeight = mono ? 400 : weight;

  const specimenStyle: CSSProperties = {
    fontFamily: mono ? "var(--font-glide-mono), monospace" : undefined,
    fontWeight: renderedWeight,
    fontStyle: italic ? "italic" : "normal",
    fontOpticalSizing: !mono && automaticOpticalSize ? "auto" : "none",
    fontVariantNumeric: [
      tabularNums ? "tabular-nums" : "proportional-nums",
      slashedZero ? "slashed-zero" : "",
    ]
      .filter(Boolean)
      .join(" "),
    fontSize: `${size}px`,
  };

  return (
    <div>
      <div className="grid grid-cols-2 gap-x-4 gap-y-3 border-y border-border py-4 lg:grid-cols-[auto_minmax(12rem,1fr)_minmax(10rem,0.72fr)_auto] lg:items-end">
        <fieldset className="col-span-2 min-w-0 lg:col-span-1">
          <legend className="mb-1.5 text-xs font-medium text-muted-foreground">
            Style
          </legend>
          <div className="inline-flex rounded-lg border border-border bg-card p-1">
            {modes.map((item) => (
              <Button
                key={item.id}
                type="button"
                size="sm"
                variant={mode === item.id ? "default" : "ghost"}
                aria-pressed={mode === item.id}
                className="h-11 sm:h-9"
                onClick={() => setMode(item.id)}
              >
                {item.label}
              </Button>
            ))}
          </div>
        </fieldset>

        <div className="min-w-0">
          <div className="mb-1 flex items-baseline justify-between gap-3">
            <span className="text-sm font-medium leading-none">Weight</span>
            <output className="font-medium tabular-nums">
              {renderedWeight}
            </output>
          </div>
          <Slider
            min={100}
            max={950}
            step={1}
            value={[renderedWeight]}
            disabled={mono}
            aria-label="Weight"
            className="[--field-height:2.75rem] sm:[--field-height:2.25rem]"
            onValueChange={([nextWeight]) => setWeight(nextWeight)}
          />
        </div>

        <div className="min-w-0">
          <div className="mb-1 flex items-baseline justify-between gap-3">
            <span className="text-sm font-medium leading-none">Size</span>
            <output className="font-medium tabular-nums">
              {size}px
            </output>
          </div>
          <Slider
            min={12}
            max={160}
            step={1}
            value={[size]}
            aria-label="Size"
            className="[--field-height:2.75rem] sm:[--field-height:2.25rem]"
            onValueChange={([nextSize]) => setSize(nextSize)}
          />
        </div>

        <div
          className="col-span-2 flex flex-wrap gap-2 lg:col-span-1 lg:justify-end"
          role="group"
          aria-label="Font options"
        >
          <Button
            type="button"
            size="sm"
            variant="outline"
            disabled={mono}
            aria-pressed={automaticOpticalSize}
            className="h-11 sm:h-9"
            onClick={() => setAutomaticOpticalSize((enabled) => !enabled)}
          >
            Optical sizing {automaticOpticalSize ? "on" : "off"}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            aria-pressed={tabularNums}
            className="h-11 sm:h-9"
            onClick={() => setTabularNums((enabled) => !enabled)}
          >
            Tabular {tabularNums ? "on" : "off"}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            aria-pressed={slashedZero}
            className="h-11 sm:h-9"
            onClick={() => setSlashedZero((enabled) => !enabled)}
          >
            Slashed zero {slashedZero ? "on" : "off"}
          </Button>
        </div>
      </div>

      <div className="pt-8 sm:pt-10">
        <label className="sr-only" htmlFor="specimen-text">
          Specimen text
        </label>
        <textarea
          id="specimen-text"
          name="specimen-text"
          value={text}
          rows={4}
          wrap="soft"
          spellCheck={false}
          aria-describedby="specimen-hint"
          className={cn(
            "field-sizing-content min-h-80 w-full resize-none overflow-hidden border-0 bg-transparent p-0 text-foreground leading-[0.95] tracking-[-0.045em] outline-none focus-visible:rounded-lg focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-4 focus-visible:ring-offset-background",
            mono && "tracking-normal",
          )}
          style={specimenStyle}
          onChange={(event) => setText(event.target.value)}
        />
        <p id="specimen-hint" className="sr-only">
          Edit the specimen directly. Optical sizing follows the selected font
          size when it is on.
        </p>
      </div>
    </div>
  );
}
