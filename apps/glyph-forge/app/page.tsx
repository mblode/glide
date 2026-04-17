import Link from "next/link";

import { Grid } from "@/components/grid";
import { attachGlyphScores } from "@/lib/data";
import {
  loadGlyphScores,
  loadManifest,
  loadSolverResults,
} from "@/lib/data.server";

export default async function HomePage() {
  const [glyphs, scores, solver] = await Promise.all([
    loadManifest(),
    loadGlyphScores(),
    loadSolverResults(),
  ]);
  const scored = attachGlyphScores(glyphs, scores, solver);

  const redCount = scores
    ? Object.values(scores).filter(
        (s) => s.worstComposite !== null && s.worstComposite < 0.3
      ).length
    : 0;
  const amberCount = scores
    ? Object.values(scores).filter(
        (s) =>
          s.worstComposite !== null &&
          s.worstComposite < 0.7 &&
          s.worstComposite >= 0.3
      ).length
    : 0;
  const solverImprovements = solver
    ? Object.values(solver).filter((v) => v.gain !== null && v.gain > 0.1).length
    : 0;

  return (
    <main>
      <header className="border-b border-border px-6 py-4">
        <div className="mx-auto flex max-w-[1600px] items-center justify-between gap-4">
          <div>
            <h1 className="font-semibold text-lg tracking-tight">Glyph Forge</h1>
            <p className="mt-0.5 text-xs text-muted-foreground">
              Audit loupe: broken glyphs in Glide variable font at Circular donor weights.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2 font-mono text-xs text-muted-foreground/70">
            <span>{glyphs.length} catalogued</span>
            {scores && (
              <span className="rounded bg-card px-2 py-0.5">
                {redCount} red · {amberCount} amber
              </span>
            )}
            {solverImprovements > 0 && (
              <span
                className="rounded bg-[--color-band-green]/15 px-2 py-0.5 text-[--color-band-green]"
                title="Glyphs where the solver projects a worst-case gain > 0.1"
              >
                solver can improve {solverImprovements}
              </span>
            )}
            <Link
              href="/triage"
              className="rounded border border-border px-2 py-0.5 hover:text-foreground"
            >
              triage queue →
            </Link>
          </div>
        </div>
      </header>
      <Grid glyphs={scored} />
    </main>
  );
}
