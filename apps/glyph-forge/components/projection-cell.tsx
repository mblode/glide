import type {
  CellScores,
  SolverCandidateName,
} from "@glide/glyph-forge-engine";

import { cn } from "@/lib/utils";
import { svgPath, type Family } from "@/lib/data";
import { ScoreBadge } from "./score-badge";

// Glide master weights — used when a candidate needs to interpolate anchors
const GLIDE_MASTER_WGHTS = [100, 400, 950] as const;

// Donor anchors used by donor_copy
const DONOR_ANCHORS = [250, 400, 950] as const;

function bracket<T extends readonly number[]>(target: number, anchors: T) {
  const sorted = [...anchors].sort((a, b) => a - b);
  if (target <= sorted[0]) return { lo: sorted[0], hi: sorted[0], t: 0 };
  if (target >= sorted[sorted.length - 1])
    return { lo: sorted[sorted.length - 1], hi: sorted[sorted.length - 1], t: 0 };
  for (let i = 0; i < sorted.length - 1; i++) {
    if (sorted[i] <= target && target <= sorted[i + 1]) {
      const lo = sorted[i];
      const hi = sorted[i + 1];
      const t = hi > lo ? (target - lo) / (hi - lo) : 0;
      return { lo, hi, t };
    }
  }
  return { lo: sorted[0], hi: sorted[sorted.length - 1], t: 0 };
}

/**
 * Render a CSS-composition approximation of what the glyph would look like under
 * the selected candidate strategy at `wght`. This matches the Python simulator's
 * intent at the visual level:
 *
 * - donor_copy:  two donor anchors, opacity-blended by bracket t
 * - reference_fallback:  glide(400) shown for every weight (static)
 * - weighted_fallback:  glide(W) under donor(W) with opacity = α
 */
export function ProjectionCell({
  family,
  glyph,
  wght,
  strategy,
  alpha = 0.5,
  score,
}: {
  family: Family;
  glyph: string;
  wght: number;
  strategy: SolverCandidateName;
  alpha?: number;
  score?: CellScores;
}) {
  const boxCls = "relative aspect-square w-full rounded bg-muted/60 p-3";

  let layers: { src: string; opacity: number; color: string }[] = [];

  if (strategy === "donor_copy") {
    const { lo, hi, t } = bracket(wght, DONOR_ANCHORS);
    if (lo === hi) {
      layers = [
        { src: svgPath(family, glyph, lo, "donor"), opacity: 1, color: "var(--color-glide)" },
      ];
    } else {
      layers = [
        { src: svgPath(family, glyph, lo, "donor"), opacity: 1 - t, color: "var(--color-glide)" },
        { src: svgPath(family, glyph, hi, "donor"), opacity: t, color: "var(--color-glide)" },
      ];
    }
  } else if (strategy === "reference_fallback") {
    layers = [
      { src: svgPath(family, glyph, 400, "glide"), opacity: 1, color: "var(--color-glide)" },
    ];
  } else if (strategy === "weighted_fallback") {
    layers = [
      { src: svgPath(family, glyph, wght, "glide"), opacity: 1 - alpha, color: "var(--color-glide)" },
      { src: svgPath(family, glyph, wght, "donor"), opacity: alpha, color: "var(--color-glide)" },
    ];
  }

  return (
    <div className="flex flex-col gap-1.5">
      <div className={boxCls}>
        {layers.map((l, i) => (
          <img
            key={`${l.src}-${i}`}
            src={l.src}
            alt=""
            loading="lazy"
            decoding="async"
            data-glyph-cell
            style={{ color: l.color, opacity: l.opacity }}
            className={cn(
              "absolute inset-0 m-auto h-[calc(100%-1.5rem)] w-[calc(100%-1.5rem)]",
              layers.length > 1 && "mix-blend-multiply"
            )}
          />
        ))}
        {score && (
          <div className="absolute right-1.5 top-1.5">
            <ScoreBadge composite={score.void ?? score.composite} compact />
          </div>
        )}
      </div>
      <span className="text-center font-mono text-[10px] text-muted-foreground/70">
        {wght}
      </span>
    </div>
  );
}
