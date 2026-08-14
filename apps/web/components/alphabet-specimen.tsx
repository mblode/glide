import Link from "next/link";

const ROWS = [
  "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
  "abcdefghijklmnopqrstuvwxyz",
  "0123456789",
  ".,;:!?&@#$%()[]{}",
] as const;

export function AlphabetSpecimen() {
  return (
    <div className="space-y-6">
      <h2 className="text-lg font-bold tracking-tight">Characters</h2>
      <div className="space-y-3 font-normal tracking-tight text-4xl sm:text-5xl lg:text-6xl">
        {ROWS.map((row) => (
          <p key={row} className="break-words">
            {row}
          </p>
        ))}
      </div>
      <p className="text-sm text-muted-foreground">
        <Link className="underline underline-offset-4 hover:text-foreground" href="/glyphs">
          Browse every glyph
        </Link>
      </p>
    </div>
  );
}
