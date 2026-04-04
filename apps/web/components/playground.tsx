"use client";

import { useState } from "react";

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
        <div className="rounded-xl border border-border bg-card p-5">
          <label
            htmlFor="weight-range"
            className="text-xs font-medium tracking-widest text-muted-foreground uppercase"
          >
            Weight
          </label>
          <p
            className="mt-2 text-3xl font-bold tracking-tight tabular-nums"
            style={{ fontWeight: weight }}
          >
            {weight}
          </p>
          <input
            id="weight-range"
            type="range"
            min={400}
            max={900}
            step={1}
            value={weight}
            onChange={(e) => setWeight(Number(e.target.value))}
            className="mt-4 w-full accent-mint touch-manipulation"
          />
          <div className="mt-3 grid grid-cols-4 gap-2">
            {instances.map((inst) => (
              <button
                key={inst.weight}
                type="button"
                onClick={() => setWeight(inst.weight)}
                className={`rounded-lg px-2 py-2 text-sm font-medium transition-colors ${
                  weight === inst.weight
                    ? "bg-foreground text-background"
                    : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
                }`}
              >
                {inst.label}
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-border bg-card p-5">
          <label
            htmlFor="custom-text"
            className="text-xs font-medium tracking-widest text-muted-foreground uppercase"
          >
            Custom text
          </label>
          <textarea
            id="custom-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            spellCheck={false}
            className="mt-3 min-h-[120px] w-full resize-y rounded-lg border border-input bg-background px-4 py-3 text-base leading-relaxed focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
      </div>

      <div className="space-y-3">
        <p
          className="text-5xl leading-[0.92] tracking-[-0.06em] sm:text-7xl lg:text-8xl"
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
        <p
          className="text-5xl italic leading-[0.92] tracking-[-0.06em] sm:text-7xl lg:text-8xl"
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
      </div>
    </div>
  );
}
