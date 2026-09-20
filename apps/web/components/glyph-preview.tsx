"use client";

import { useLayoutEffect, useRef, useState } from "react";

import {
  GLIDE_ITALIC_X_HEIGHT_STOPS,
  GLIDE_METRICS,
  GLIDE_MONO_METRICS,
  GLIDE_TEXT_OPSZ,
  GLIDE_X_HEIGHT_STOPS,
} from "@/lib/font-metrics";

type GlyphPreviewProps = {
  char: string;
  cp: number;
  italic: boolean;
  label: string;
  mono: boolean;
  weight: number;
};

function xHeightAt(weight: number, mono: boolean, italic: boolean) {
  if (mono) return GLIDE_MONO_METRICS.xHeight;
  const stops = italic ? GLIDE_ITALIC_X_HEIGHT_STOPS : GLIDE_X_HEIGHT_STOPS;
  if (weight <= stops[0][0]) return stops[0][1];
  for (let i = 1; i < stops.length; i += 1) {
    const [x0, y0] = stops[i - 1];
    const [x1, y1] = stops[i];
    if (weight <= x1) return y0 + ((weight - x0) / (x1 - x0)) * (y1 - y0);
  }
  return stops[stops.length - 1][1];
}

export function GlyphPreview({ char, cp, italic, label, mono, weight }: GlyphPreviewProps) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const [box, setBox] = useState({ width: 0, height: 0 });

  useLayoutEffect(() => {
    const wrap = wrapRef.current;
    if (!wrap) return;
    const measure = () => {
      const width = wrap.clientWidth;
      const height = wrap.clientHeight;
      setBox((previous) => previous.width === width && previous.height === height
        ? previous : { width, height });
    };
    const observer = new ResizeObserver(measure);
    observer.observe(wrap);
    measure();
    return () => observer.disconnect();
  }, []);

  const size = Math.min(box.width, box.height) * 0.86;
  const cap = mono ? GLIDE_MONO_METRICS.capHeight : GLIDE_METRICS.capHeight;
  const baseline = box.height / 2 + (cap / GLIDE_METRICS.unitsPerEm) * size / 2;
  const guides = [
    { id: "cap", label: "Cap height", value: cap },
    { id: "x", label: "x-height", value: xHeightAt(weight, mono, italic) },
    { id: "base", label: "Baseline", value: 0 },
  ].map((guide) => ({ ...guide, y: baseline - guide.value / GLIDE_METRICS.unitsPerEm * size }));

  return (
    <div ref={wrapRef} className="relative min-h-0 min-w-0 flex-1">
      {/* SVG text honors explicit optical coordinates; Canvas font shorthand does not carry them. */}
      <svg
        aria-label={`${label}${mono ? "" : `, Text optical size ${GLIDE_TEXT_OPSZ}`}`}
        className="absolute inset-0 block size-full"
        role="img"
        viewBox={`0 0 ${box.width || 1} ${box.height || 1}`}
      >
        {guides.map((guide) => (
          <line key={guide.id} x1={0} x2={box.width} y1={guide.y + 0.5} y2={guide.y + 0.5}
            stroke="currentColor" strokeOpacity={0.22} vectorEffect="non-scaling-stroke" />
        ))}
        {cp === 0x20 ? (
          <rect x={box.width / 2 - size * 0.11} y={baseline - 1} width={size * 0.22}
            height={2} fill="currentColor" opacity={0.35} />
        ) : (
          <text x={box.width / 2} y={baseline} textAnchor="middle" fill="currentColor"
            style={{
              fontFamily: mono ? "var(--font-glide-mono), monospace" : "var(--font-glide), sans-serif",
              fontWeight: weight,
              fontStyle: italic ? "italic" : "normal",
              fontSize: size,
              fontOpticalSizing: "none",
              fontVariationSettings: mono ? "normal" : `"opsz" ${GLIDE_TEXT_OPSZ}`,
              fontSynthesis: "none",
            }}>{char}</text>
        )}
      </svg>
      <div aria-hidden="true" className="pointer-events-none absolute inset-0">
        {guides.map((guide) => (
          <div key={guide.id} className="absolute inset-x-0" style={{ top: guide.y, opacity: size ? 1 : 0 }}>
            <div className="absolute bottom-full left-3 pb-1 text-[0.625rem] text-foreground/50">{guide.label}</div>
          </div>
        ))}
      </div>
      {!mono && <span className="absolute right-3 bottom-2 text-[0.625rem] text-foreground/50">Text · {GLIDE_TEXT_OPSZ}</span>}
    </div>
  );
}
