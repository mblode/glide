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

function featureSettings(liga: boolean, tnum: boolean, zero: boolean) {
  return [
    `"liga" ${liga ? 1 : 0}`,
    `"tnum" ${tnum ? 1 : 0}`,
    `"zero" ${zero ? 1 : 0}`,
  ].join(", ");
}

export function Playground() {
  const [weight, setWeight] = useState(700);
  const [size, setSize] = useState(24);
  const [mode, setMode] = useState<Mode>("sans");
  const [liga, setLiga] = useState(true);
  const [tnum, setTnum] = useState(false);
  const [zero, setZero] = useState(false);
  const [text, setText] = useState(
    "Glide variable font\nThe quick brown fox jumps over the lazy dog. 0123456789.",
  );

  const mono = mode === "mono";
  const italic = mode === "italic";

  const lines = text.split("\n");
  const headline = lines[0]?.trim() || "Glide variable font";
  const body =
    lines.slice(1).join(" ").trim() ||
    "The quick brown fox jumps over the lazy dog. 0123456789.";

  const features = featureSettings(mono ? false : liga, mono ? false : tnum, zero);
  const previewStyle = mono
    ? {
        fontFamily: "var(--font-glide-mono), monospace",
        fontWeight: 400,
        fontFeatureSettings: features,
        fontVariantLigatures: "none" as const,
      }
    : {
        fontWeight: weight,
        fontStyle: italic ? "italic" : ("normal" as const),
        fontFeatureSettings: features,
        fontVariantLigatures: liga ? ("common-ligatures" as const) : ("none" as const),
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
            </>
          )}

          <div className="flex items-baseline justify-between">
            <Label htmlFor="size-slider">Size</Label>
            <span className="text-sm font-medium tabular-nums">{size}px</span>
          </div>
          <Slider
            id="size-slider"
            min={13}
            max={72}
            step={1}
            value={[size]}
            onValueChange={([v]) => setSize(v)}
          />

          <div className="flex flex-wrap gap-1">
            {!mono && (
              <>
                <Button
                  type="button"
                  size="xs"
                  variant={liga ? "default" : "outline"}
                  aria-pressed={liga}
                  onClick={() => setLiga((v) => !v)}
                >
                  Ligatures
                </Button>
                <Button
                  type="button"
                  size="xs"
                  variant={tnum ? "default" : "outline"}
                  aria-pressed={tnum}
                  onClick={() => setTnum((v) => !v)}
                >
                  Tabular numbers
                </Button>
              </>
            )}
            <Button
              type="button"
              size="xs"
              variant={zero ? "default" : "outline"}
              aria-pressed={zero}
              onClick={() => setZero((v) => !v)}
            >
              Slashed zero
            </Button>
          </div>
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
        className="space-y-3 [--preview-body:24px] [--preview-headline:54px]"
        style={
          {
            "--preview-body": `${size}px`,
            "--preview-headline": `${Math.round(size * 2.25)}px`,
          } as CSSProperties
        }
      >
        <p
          className={cn(
            "text-[length:var(--preview-headline)] tracking-[-0.06em]",
            mono && "break-words tracking-normal",
          )}
          style={previewStyle}
        >
          {headline}
        </p>
        <p
          className={cn(
            "max-w-2xl text-[length:var(--preview-body)] text-muted-foreground tracking-tight",
            mono && "break-words tracking-normal",
          )}
          style={previewStyle}
        >
          {body}
        </p>
      </div>
    </div>
  );
}
