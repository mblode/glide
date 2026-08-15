"use client";

import { useState, type CSSProperties } from "react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

type Mode = "sans" | "italic" | "mono";

const modes: { id: Mode; label: string }[] = [
  { id: "sans", label: "Sans" },
  { id: "italic", label: "Italic" },
  { id: "mono", label: "Mono" },
];

export function Playground() {
  const [weight, setWeight] = useState(700);
  const [size, setSize] = useState(48);
  const [mode, setMode] = useState<Mode>("sans");
  const [tabularNums, setTabularNums] = useState(true);
  const [slashedZero, setSlashedZero] = useState(true);
  const [automaticOpticalSize, setAutomaticOpticalSize] = useState(true);
  const [opticalSize, setOpticalSize] = useState(16);
  const [text, setText] = useState(
    "Glide variable font\n11:45 0123456789 100,000 · 0 O o Ø",
  );

  const mono = mode === "mono";
  const italic = mode === "italic";

  const lines = text.split("\n");
  const headline = lines[0]?.trim() || "Glide variable font";
  const body =
    lines.slice(1).join(" ").trim() ||
    "The quick brown fox jumps over the lazy dog. 0123456789.";

  const previewStyle: CSSProperties = mono
    ? { fontFamily: "var(--font-glide-mono), monospace", fontWeight: 400 }
    : {
        fontWeight: weight,
        fontStyle: italic ? "italic" : ("normal" as const),
        fontOpticalSizing: automaticOpticalSize ? "auto" : "none",
        fontVariationSettings: automaticOpticalSize
          ? "normal"
          : `'wght' ${weight}, 'opsz' ${opticalSize}`,
        fontVariantNumeric: [
          tabularNums ? "tabular-nums" : "proportional-nums",
          slashedZero ? "slashed-zero" : "",
        ]
          .filter(Boolean)
          .join(" "),
      };

  return (
    <div className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-4">
          <div role="radiogroup" aria-label="Style" className="flex gap-1">
            {modes.map((m) => (
              <Button
                key={m.id}
                type="button"
                size="sm"
                variant={mode === m.id ? "default" : "outline"}
                role="radio"
                aria-checked={mode === m.id}
                onClick={() => setMode(m.id)}
              >
                {m.label}
              </Button>
            ))}
          </div>

          {!mono && (
            <>
              <div className="flex items-baseline justify-between">
                <Label htmlFor="weight-slider">Weight</Label>
                <span
                  className="text-2xl font-bold tracking-tight tabular-nums"
                  style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
                >
                  {weight}
                </span>
              </div>
              <Slider
                id="weight-slider"
                min={100}
                max={950}
                step={1}
                value={[weight]}
                onValueChange={([v]) => setWeight(v)}
              />

              <div
                className="flex flex-wrap gap-2"
                role="group"
                aria-label="OpenType features"
              >
                <Button
                  type="button"
                  size="sm"
                  variant={tabularNums ? "default" : "outline"}
                  aria-pressed={tabularNums}
                  onClick={() => setTabularNums((enabled) => !enabled)}
                >
                  Tabular nums
                </Button>
                <Button
                  type="button"
                  size="sm"
                  variant={slashedZero ? "default" : "outline"}
                  aria-pressed={slashedZero}
                  onClick={() => setSlashedZero((enabled) => !enabled)}
                >
                  Slashed zero
                </Button>
              </div>
            </>
          )}

          <div className="flex items-baseline justify-between">
            <Label htmlFor="size-slider">Size</Label>
            <span className="text-sm font-medium tabular-nums">{size}px</span>
          </div>
          <Slider
            id="size-slider"
            min={12}
            max={72}
            step={1}
            value={[size]}
            onValueChange={([v]) => setSize(v)}
          />

          {!mono && (
            <>
              <div className="flex items-baseline justify-between gap-4">
                <Label htmlFor="optical-size-slider">
                  Optical size · {automaticOpticalSize ? "auto" : opticalSize}
                </Label>
                <Button
                  type="button"
                  size="sm"
                  variant={automaticOpticalSize ? "default" : "outline"}
                  aria-pressed={automaticOpticalSize}
                  onClick={() => setAutomaticOpticalSize((enabled) => !enabled)}
                >
                  Auto
                </Button>
              </div>
              <Slider
                id="optical-size-slider"
                min={12}
                max={28}
                step={1}
                value={[opticalSize]}
                disabled={automaticOpticalSize}
                onValueChange={([v]) => setOpticalSize(v)}
              />
            </>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="custom-text">Custom text</Label>
          <Textarea
            id="custom-text"
            name="custom-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            spellCheck={false}
            rows={4}
            className={cn(mono && "font-mono")}
          />
        </div>
      </div>

      <div
        className="space-y-3 [--preview-body:48px] [--preview-headline:108px]"
        style={
          {
            "--preview-body": `${size}px`,
            "--preview-headline": `${Math.round(size * 2.25)}px`,
          } as CSSProperties
        }
      >
        <p
          className={cn(
            "break-words text-[length:var(--preview-headline)] tracking-[-0.06em]",
            mono && "tracking-normal",
          )}
          style={previewStyle}
        >
          {headline}
        </p>
        <p
          className={cn(
            "max-w-2xl break-words text-[length:var(--preview-body)] text-muted-foreground tracking-tight",
            mono && "tracking-normal",
          )}
          style={previewStyle}
        >
          {body}
        </p>
      </div>
    </div>
  );
}
