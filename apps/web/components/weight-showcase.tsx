"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

const weights = [
  { weight: 100, name: "Thin", sample: "Quiet chrome labels" },
  { weight: 200, name: "ExtraLight", sample: "Placeholder field text" },
  { weight: 300, name: "Light", sample: "Helper caption line" },
  { weight: 400, name: "Regular", sample: "Default interface copy" },
  { weight: 500, name: "Medium", sample: "Selected menu item" },
  { weight: 600, name: "Semibold", sample: "Section heading" },
  { weight: 700, name: "Bold", sample: "Primary button label" },
  { weight: 800, name: "Extrabold", sample: "Empty-state title" },
  { weight: 900, name: "Black", sample: "Display wordmark" },
  { weight: 950, name: "Extra Black", sample: "Poster locking tight" },
] as const;

function WeightRow({
  weight,
  name,
  sample,
  italic = false,
}: {
  weight: number;
  name: string;
  sample: string;
  italic?: boolean;
}) {
  return (
    <div className="grid items-baseline gap-2 border-t border-border py-4 first:border-t-0 first:pt-0 sm:grid-cols-[140px_1fr] sm:gap-4">
      <div className="text-sm text-muted-foreground tabular-nums">
        <span className="block font-semibold text-foreground">{name}</span>
        {weight}
      </div>
      <p
        className="text-2xl tracking-tight sm:text-3xl"
        style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
      >
        {sample}
      </p>
    </div>
  );
}

export function WeightShowcase({
  weights: weightsProp = weights,
}: {
  weights?: ReadonlyArray<{
    readonly weight: number;
    readonly name: string;
    readonly sample: string;
  }>;
}) {
  const [style, setStyle] = useState<"roman" | "italic">("roman");
  const italic = style === "italic";

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <h2 className="text-lg font-bold tracking-tight">Weights</h2>
        <div role="radiogroup" aria-label="Style" className="flex gap-1">
          <Button
            type="button"
            size="xs"
            variant={style === "roman" ? "default" : "outline"}
            role="radio"
            aria-checked={style === "roman"}
            onClick={() => setStyle("roman")}
          >
            Roman
          </Button>
          <Button
            type="button"
            size="xs"
            variant={style === "italic" ? "default" : "outline"}
            role="radio"
            aria-checked={style === "italic"}
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
            sample={w.sample}
            italic={italic}
          />
        ))}
      </div>
    </div>
  );
}
