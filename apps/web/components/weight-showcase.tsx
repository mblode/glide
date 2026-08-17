"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";

/*
  The named styles the family is presented in. 200, 800, and 900 are reachable
  on the variable axis but are not listed: they sit too close to their
  neighbours to read as distinct cuts in a specimen.
*/
const weights = [
  { weight: 100, name: "Thin", sample: "Afstandstabel" },
  { weight: 300, name: "Light", sample: "Microphonics" },
  { weight: 400, name: "Regular", sample: "Nudicaudate" },
  { weight: 500, name: "Medium", sample: "Quicksilver" },
  { weight: 600, name: "Semibold", sample: "Blackletter" },
  { weight: 700, name: "Bold", sample: "Typefounder" },
  { weight: 950, name: "Extra Black", sample: "Letterpress" },
] as const;

/*
  Both cuts of every weight, so the count is what a foundry would quote. The
  list shows every style at once; the stack below shows one at a time, big.
*/
const styleCount = weights.length * 2;

export function WeightShowcase() {
  const [style, setStyle] = useState<"roman" | "italic">("roman");
  const italic = style === "italic";

  return (
    <section aria-labelledby="weights-heading" id="weights">
      <div className="flex flex-wrap items-start gap-x-10 gap-y-6 border-border border-t px-[var(--row-padding)] py-[var(--row-padding-vertical)]">
        <h2
          className="w-full font-semibold text-lg tracking-tight sm:w-40 sm:shrink-0"
          id="weights-heading"
        >
          {styleCount} styles
        </h2>

        {/*
          Each name set in the style it names, so the list is the specimen. The
          weight number rides as a superscript in `em` units, which keeps it
          proportional to whatever size the name lands at.
        */}
        <ul
          className="flex flex-1 flex-wrap items-baseline gap-x-6 gap-y-1 text-[clamp(2rem,4.5vw,4rem)] leading-[1.15] tracking-[-0.02em] [&_sup]:ml-[0.1em] [&_sup]:[vertical-align:2.8em] [&_sup]:text-[0.2em] [&_sup]:font-light [&_sup]:tracking-normal [&_sup]:opacity-50"
          role="list"
        >
          {weights.flatMap((entry) =>
            [false, true].map((isItalic) => (
              <li
                key={`${entry.weight}-${isItalic}`}
                style={{
                  fontWeight: entry.weight,
                  fontStyle: isItalic ? "italic" : "normal",
                }}
              >
                {entry.name}
                {isItalic ? " Italic" : ""}
                <sup className="tabular-nums">{entry.weight}</sup>
              </li>
            ))
          )}
        </ul>
      </div>

      <div className="border-border border-t px-[var(--row-padding)] py-[var(--row-padding-vertical)]">
        <div
          aria-label="Style"
          className="flex items-center gap-1 pb-8"
          role="radiogroup"
        >
          {(["roman", "italic"] as const).map((option) => (
            <Button
              aria-checked={style === option}
              className="max-sm:h-11"
              key={option}
              onClick={() => setStyle(option)}
              role="radio"
              size="sm"
              type="button"
              variant={style === option ? "default" : "outline"}
            >
              {option === "roman" ? "Roman" : "Italic"}
            </Button>
          ))}
        </div>

        {/*
          One weight per row at 13vw, which lands a word of this length close to
          the full measure without measuring anything. The rag on the right is
          the honest cost of that, and it is how a printed specimen reads too.
        */}
        {weights.map((entry) => (
          <div className="pb-10 last:pb-0" key={entry.weight}>
            <div className="grid grid-cols-3 gap-x-6 pb-2 text-muted-foreground text-sm">
              <span>{entry.name}</span>
              <span>{italic ? "Italic" : "Roman"}</span>
              <span className="text-right tabular-nums">{entry.weight}</span>
            </div>
            {/*
              Editable like the specimen above. The word goes in through
              `dangerouslySetInnerHTML` rather than as children so that
              toggling Roman/Italic re-renders the row without React
              reconciling the text back to its default and wiping the edit.

              It wraps rather than running on a single line. Inter keeps theirs
              to one line and lets it clip, but this one is editable: anything
              past the measure would be typed into a void you cannot scroll to,
              and a scrollbar per row is worse. The negative margin is
              side-bearing compensation, so the first stem sits on the same edge
              as the label above it.
            */}
            <div>
              <p
                aria-label={`${entry.name} sample text`}
                className="ml-[-0.055em] break-words text-[13vw] leading-[1.12] tracking-[-0.02em] outline-none"
                contentEditable
                dangerouslySetInnerHTML={{ __html: entry.sample }}
                role="textbox"
                spellCheck={false}
                style={{
                  fontWeight: entry.weight,
                  fontStyle: italic ? "italic" : "normal",
                }}
                suppressContentEditableWarning
              />
            </div>
          </div>
        ))}

        <p className="pt-10 text-pretty text-muted-foreground text-sm">
          Only three of these are drawn: Thin, Regular, and Extra Black. The rest
          are interpolated.
        </p>
      </div>
    </section>
  );
}
