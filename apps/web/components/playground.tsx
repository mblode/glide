"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { ENABLE_ITALIC } from "@/lib/flags";

const instances = [
  { weight: 400, label: "Regular" },
  { weight: 500, label: "Medium" },
  { weight: 700, label: "Bold" },
  { weight: 900, label: "Black" },
] as const;

export function Playground() {
  const [weight, setWeight] = useState(700);
  const [text, setText] = useState(
    "Glide variable font\nThe quick brown fox jumps over the lazy dog. 0123456789."
  );

  const lines = text.split("\n");
  const headline = lines[0]?.trim() || "Glide variable font";
  const body =
    lines.slice(1).join(" ").trim() ||
    "The quick brown fox jumps over the lazy dog. 0123456789.";

  return (
    <div className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-4">
          <div className="flex items-baseline justify-between">
            <Label htmlFor="weight-slider">Weight</Label>
            <span
              className="text-2xl font-bold tracking-tight tabular-nums"
              style={{ fontWeight: weight }}
            >
              {weight}
            </span>
          </div>
          <Slider
            id="weight-slider"
            min={400}
            max={900}
            step={1}
            value={[weight]}
            onValueChange={([v]) => setWeight(v)}
          />
          <div className="grid grid-cols-4 gap-2">
            {instances.map((inst) => (
              <Button
                key={inst.weight}
                size="sm"
                variant={weight === inst.weight ? "default" : "outline"}
                onClick={() => setWeight(inst.weight)}
              >
                {inst.label}
              </Button>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="custom-text">Custom text</Label>
          <Textarea
            id="custom-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            spellCheck={false}
            rows={4}
          />
        </div>
      </div>

      <div className="space-y-3">
        <p
          className="text-5xl leading-none tracking-[-0.06em] sm:text-7xl lg:text-8xl"
          style={{ fontWeight: weight }}
        >
          {headline}
        </p>
        <p
          className="max-w-2xl text-lg leading-snug tracking-tight text-muted-foreground sm:text-xl lg:text-2xl"
          style={{ fontWeight: weight }}
        >
          {body}
        </p>
        {ENABLE_ITALIC && (
          <>
            <p
              className="text-5xl italic leading-none tracking-[-0.06em] sm:text-7xl lg:text-8xl"
              style={{ fontWeight: weight }}
            >
              {headline}
            </p>
            <p
              className="max-w-2xl text-lg italic leading-snug tracking-tight text-muted-foreground sm:text-xl lg:text-2xl"
              style={{ fontWeight: weight }}
            >
              {body}
            </p>
          </>
        )}
      </div>
    </div>
  );
}
