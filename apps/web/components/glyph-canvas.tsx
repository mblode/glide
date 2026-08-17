"use client";

import { useLayoutEffect, useRef, type CSSProperties } from "react";

import { GLIDE_METRICS } from "@/lib/font-metrics";

type GlyphCanvasProps = {
  char: string;
  cp: number;
  italic: boolean;
  label: string;
  mono: boolean;
  weight: number;
};

type MetricGuide = {
  id: "cap" | "x" | "base";
  label: string;
  y: number;
};

function metricY(size: number, value: number, baselineY: number) {
  return baselineY - (value / GLIDE_METRICS.unitsPerEm) * size;
}

export function GlyphCanvas({
  char,
  cp,
  italic,
  label,
  mono,
  weight,
}: GlyphCanvasProps) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const guidesRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const wrap = wrapRef.current;
    const canvas = canvasRef.current;
    const guides = guidesRef.current;
    if (!wrap || !canvas || !guides) {
      return;
    }

    let frame = 0;

    const paint = () => {
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        return;
      }

      const dpr = window.devicePixelRatio || 1;
      const width = wrap.clientWidth;
      const height = wrap.clientHeight;
      if (width < 2 || height < 2) {
        return;
      }

      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, width, height);

      const size = Math.min(width, height) * 0.86;
      const capPx =
        (GLIDE_METRICS.capHeight / GLIDE_METRICS.unitsPerEm) * size;
      const baselineY = height / 2 + capPx / 2;
      const family = getComputedStyle(wrap).fontFamily;
      const color = getComputedStyle(wrap).color;

      const nextGuides: MetricGuide[] = [
        { id: "cap", label: "Cap height", y: metricY(size, GLIDE_METRICS.capHeight, baselineY) },
        { id: "x", label: "x-height", y: metricY(size, GLIDE_METRICS.xHeight, baselineY) },
        { id: "base", label: "Baseline", y: baselineY },
      ];
      for (const guide of nextGuides) {
        const row = guides.querySelector<HTMLElement>(`[data-guide="${guide.id}"]`);
        if (row) {
          row.style.top = `${guide.y}px`;
          row.style.opacity = "1";
        }
      }

      ctx.strokeStyle = color;
      ctx.globalAlpha = 0.22;
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (const guide of nextGuides) {
        ctx.moveTo(0, guide.y + 0.5);
        ctx.lineTo(width, guide.y + 0.5);
      }
      ctx.stroke();
      ctx.globalAlpha = 1;

      ctx.fillStyle = color;
      ctx.font = `${italic ? "italic" : "normal"} ${weight} ${size}px ${family}`;
      ctx.textAlign = "center";
      ctx.textBaseline = "alphabetic";

      if (cp === 0x20) {
        const bar = size * 0.22;
        ctx.globalAlpha = 0.35;
        ctx.fillRect(width / 2 - bar / 2, baselineY - 1, bar, 2);
        ctx.globalAlpha = 1;
        return;
      }

      ctx.fillText(char, width / 2, baselineY);
    };

    const schedule = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(paint);
    };

    const observer = new ResizeObserver(schedule);
    observer.observe(wrap);
    void document.fonts.ready.then(schedule);
    schedule();

    return () => {
      cancelAnimationFrame(frame);
      observer.disconnect();
    };
  }, [char, cp, italic, mono, weight]);

  return (
    <div
      ref={wrapRef}
      className="relative min-h-0 min-w-0 flex-1"
      style={
        {
          // Read back off this element by the canvas via getComputedStyle.
          fontFamily: mono
            ? "var(--font-glide-mono), monospace"
            : "var(--font-glide), sans-serif",
          fontWeight: weight,
          fontStyle: italic ? "italic" : "normal",
        } as CSSProperties
      }
    >
      <canvas
        ref={canvasRef}
        aria-label={label}
        className="absolute inset-0 block size-full"
        role="img"
      />
      <div
        ref={guidesRef}
        aria-hidden="true"
        className="pointer-events-none absolute inset-0"
      >
        {(
          [
            ["cap", "Cap height"],
            ["x", "x-height"],
            ["base", "Baseline"],
          ] as const
        ).map(([id, text]) => (
          <div
            key={id}
            data-guide={id}
            className="absolute inset-x-0 opacity-0"
          >
            <div className="absolute bottom-full left-3 pb-1 text-[0.625rem] text-foreground/50">
              {text}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
