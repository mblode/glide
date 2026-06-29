"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

const weights = [
  { weight: 100, name: "Thin" },
  { weight: 200, name: "ExtraLight" },
  { weight: 300, name: "Light" },
  { weight: 400, name: "Regular" },
  { weight: 500, name: "Medium" },
  { weight: 600, name: "Semibold" },
  { weight: 700, name: "Bold" },
  { weight: 800, name: "Extrabold" },
  { weight: 900, name: "Extra Black" },
] as const;

function WeightRow({
  weight,
  name,
  italic = false,
}: {
  weight: number;
  name: string;
  italic?: boolean;
}) {
  return (
    <div className="grid items-baseline gap-2 border-t border-border py-4 first:border-t-0 first:pt-0 sm:grid-cols-[140px_1fr] sm:gap-4">
      <div className="text-sm text-muted-foreground tabular-nums">
        <span className="block font-semibold text-foreground">{name}</span>
        {weight}
      </div>
      <p
        className="text-2xl leading-snug tracking-tight sm:text-3xl"
        style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
      >
        The quick brown fox jumps over the lazy dog.
      </p>
    </div>
  );
}

export function WeightShowcase({
  weights: weightsProp = weights,
}: {
  weights?: ReadonlyArray<{ readonly weight: number; readonly name: string }>;
}) {
  const [style, setStyle] = useState<"roman" | "italic">("roman");
  const italic = style === "italic";

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <h2 className="text-lg font-bold tracking-tight">Weights</h2>
        <div className="flex gap-1">
          <Button
            size="xs"
            variant={style === "roman" ? "default" : "outline"}
            onClick={() => setStyle("roman")}
          >
            Roman
          </Button>
          <Button
            size="xs"
            variant={style === "italic" ? "default" : "outline"}
            onClick={() => setStyle("italic")}
          >
            Italic
          </Button>
        </div>
      </div>
      <div>
        {weightsProp.map((w) => (
          <WeightRow
            key={w.weight}
            weight={w.weight}
            name={italic ? `${w.name} Italic` : w.name}
            italic={italic}
          />
        ))}
      </div>
    </div>
  );
}
