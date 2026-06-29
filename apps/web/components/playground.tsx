"use client";

import { useState } from "react";
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
  const [mode, setMode] = useState<Mode>("sans");
  const [text, setText] = useState(
    "Glide variable font\nThe quick brown fox jumps over the lazy dog. 0123456789."
  );

  const mono = mode === "mono";
  const italic = mode === "italic";

  const lines = text.split("\n");
  const headline = lines[0]?.trim() || "Glide variable font";
  const body =
    lines.slice(1).join(" ").trim() ||
    "The quick brown fox jumps over the lazy dog. 0123456789.";

  const previewStyle = mono
    ? { fontFamily: "var(--font-glide-mono), monospace", fontWeight: 400 }
    : { fontWeight: weight, fontStyle: italic ? "italic" : ("normal" as const) };

  return (
    <div className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-4">
          {/* style: Sans / Italic / Mono */}
          <div className="flex gap-1">
            {modes.map((m) => (
              <Button
                key={m.id}
                size="sm"
                variant={mode === m.id ? "default" : "outline"}
                onClick={() => setMode(m.id)}
              >
                {m.label}
              </Button>
            ))}
          </div>

          {/* weight controls — only for the variable (non-mono) styles */}
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
        </div>

        <div className="space-y-2">
          <Label htmlFor="custom-text">Custom text</Label>
          <Textarea
            id="custom-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            spellCheck={false}
            rows={4}
            className={cn(mono && "font-mono")}
          />
        </div>
      </div>

      <div className="space-y-3">
        <p
          className={cn(
            "leading-none tracking-[-0.06em]",
            mono
              ? "break-words text-3xl tracking-normal sm:text-5xl"
              : "text-5xl sm:text-7xl lg:text-8xl"
          )}
          style={previewStyle}
        >
          {headline}
        </p>
        <p
          className={cn(
            "max-w-2xl leading-snug tracking-tight text-muted-foreground",
            mono ? "break-words text-base sm:text-lg" : "text-lg sm:text-xl lg:text-2xl"
          )}
          style={previewStyle}
        >
          {body}
        </p>
      </div>
    </div>
  );
}
