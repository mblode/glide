"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

// The 3-master design: real outlines exist only at these weights. Everything
// else on the axis is interpolated between them.
const MASTERS = [100, 400, 950] as const;
const MASTER_LABELS: Record<number, string> = {
  100: "Thin",
  400: "Regular",
  950: "Extra Black",
};

// The ramp shown in the glyph grid: master positions plus the two midpoints
// (250, 675) that sit furthest from any master — where 3-master interpolation
// drifts most.
const RAMP = [100, 250, 400, 675, 950] as const;
const isMaster = (w: number) => (MASTERS as readonly number[]).includes(w);

// Glyphs the interpolation audit flagged as risky across the long 3-master
// spans (start-point drift / area dips at in-between weights).
const FLAGGED = ["$", "¢", "S", "ț", "ā", "Į", "Ï", "Ř", "…"] as const;
// Clean control glyphs for contrast — these interpolate without issues.
const CLEAN = ["a", "e", "n", "o", "g", "R", "2", "8"] as const;

const PANGRAM = "The quick brown fox jumps over the lazy dog. $0123 ¢ S";

type Style = "roman" | "italic";

function GlyphRamp({
  glyphs,
  italic,
}: {
  glyphs: readonly string[];
  italic: boolean;
}) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-center">
        <thead>
          <tr>
            <th className="w-10" />
            {RAMP.map((w) => (
              <th key={w} className="px-1 pb-2 align-bottom">
                <span className="block font-semibold text-foreground text-sm tabular-nums">
                  {w}
                </span>
                <span
                  className={cn(
                    "text-[10px] uppercase tracking-wide",
                    isMaster(w)
                      ? "text-muted-foreground"
                      : "font-semibold text-amber-500"
                  )}
                >
                  {isMaster(w) ? "master" : "interp"}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {glyphs.map((g) => (
            <tr key={g} className="border-t border-border">
              <td className="py-2 pr-2 text-left text-muted-foreground text-xs">
                {g}
              </td>
              {RAMP.map((w) => (
                <td
                  key={w}
                  className={cn(
                    "px-1 py-2",
                    !isMaster(w) && "bg-amber-500/5"
                  )}
                >
                  <span
                    className="block text-3xl leading-none sm:text-4xl"
                    style={{
                      fontWeight: w,
                      fontStyle: italic ? "italic" : "normal",
                    }}
                  >
                    {g}
                  </span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function InterpolationInspector() {
  const [weight, setWeight] = useState(650);
  const [style, setStyle] = useState<Style>("roman");
  const italic = style === "italic";

  const atMaster = isMaster(weight);
  const masterName = MASTER_LABELS[weight];

  return (
    <div className="space-y-8">
      {/* Controls + live specimen */}
      <div className="space-y-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex gap-1">
            {(["roman", "italic"] as const).map((s) => (
              <Button
                key={s}
                size="sm"
                variant={style === s ? "default" : "outline"}
                onClick={() => setStyle(s)}
                className="capitalize"
              >
                {s}
              </Button>
            ))}
          </div>
          <span
            className={cn(
              "rounded-full px-3 py-1 text-xs font-semibold",
              atMaster
                ? "bg-muted text-muted-foreground"
                : "bg-amber-500/15 text-amber-600 dark:text-amber-400"
            )}
          >
            {atMaster
              ? `Master · ${masterName} (${weight})`
              : `Interpolated · ${weight}`}
          </span>
        </div>

        <div className="space-y-3">
          <div className="flex items-baseline justify-between">
            <Label htmlFor="inspect-weight">Weight</Label>
            <span
              className="text-2xl font-bold tabular-nums tracking-tight"
              style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
            >
              {weight}
            </span>
          </div>
          <Slider
            id="inspect-weight"
            min={100}
            max={950}
            step={1}
            value={[weight]}
            onValueChange={([v]) => setWeight(v)}
          />
          {/* axis stops: masters jump to weight; midpoints highlighted */}
          <div className="flex flex-wrap gap-2">
            {RAMP.map((w) => (
              <Button
                key={w}
                size="xs"
                variant={weight === w ? "default" : "outline"}
                onClick={() => setWeight(w)}
                className={cn(
                  !isMaster(w) &&
                    weight !== w &&
                    "border-amber-500/40 text-amber-600 dark:text-amber-400"
                )}
              >
                {isMaster(w) ? MASTER_LABELS[w] : `${w} (interp)`}
              </Button>
            ))}
          </div>
        </div>

        <p
          className="break-words text-4xl leading-tight tracking-[-0.03em] sm:text-6xl"
          style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
        >
          {PANGRAM}
        </p>
      </div>

      {/* Glyph ramps */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <h3 className="text-base font-bold tracking-tight">
            Audit-flagged glyphs
          </h3>
          <span className="text-muted-foreground text-sm">
            watch the <span className="font-semibold text-amber-500">interp</span>{" "}
            columns (250 / 650) for drift
          </span>
        </div>
        <GlyphRamp glyphs={FLAGGED} italic={italic} />
      </div>

      <div className="space-y-3">
        <h3 className="text-base font-bold tracking-tight">Clean control glyphs</h3>
        <GlyphRamp glyphs={CLEAN} italic={italic} />
      </div>

      <p className="text-muted-foreground text-sm leading-relaxed">
        Glide interpolates its whole 100–950 axis from three masters — Thin (100),
        Regular (400) and Extra Black (950). The amber columns (250, 675) are pure
        interpolations sitting farthest from any master, so shape drift shows up
        there first. Compare a flagged glyph like <strong>$</strong> or{" "}
        <strong>S</strong> against a clean one like <strong>o</strong> across the
        ramp.
      </p>
    </div>
  );
}
