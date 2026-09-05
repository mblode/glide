"use client";

import { useCallback, useEffect, useRef, useState } from "react";

/**
 * The hero wordmark, editable and self-sizing.
 *
 * People already tried to type here: the wordmark collected dead clicks, which
 * is what a click on inert text looks like, and One Page Love sells this page
 * on its "interactive editable text". Typing into a headline set at 24vw a
 * character used to push it straight past the gutter, so the type scales down
 * to whatever you have typed instead.
 */

const DEFAULT_TITLE = "Glide";

/** The size the hidden twin is measured at before the ratio is applied. */
const REFERENCE_SIZE = 100;

/*
  A floor, because "fits on one line" stops being a specimen somewhere around a
  sentence. Past this the heading wraps instead, which is what `break-words` on
  the heading is for.
*/
const MIN_SIZE = 40;

/*
  Sub-pixel rounding in the measurement can leave the fitted line a hair wider
  than the row, which is a horizontal scrollbar on the whole page.
*/
const SAFETY = 0.998;

const shared =
  "font-black leading-[0.85] tracking-[-0.04em] text-display";

export const HeroTitle = () => {
  const rowRef = useRef<HTMLDivElement>(null);
  const twinRef = useRef<HTMLSpanElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const [size, setSize] = useState<number>();

  const fit = useCallback(() => {
    const row = rowRef.current;
    const twin = twinRef.current;
    const heading = headingRef.current;
    if (!(row && twin && heading)) {
      return;
    }

    const typed = heading.textContent?.trim();
    twin.textContent = typed && typed.length > 0 ? typed : DEFAULT_TITLE;

    const available = row.clientWidth;
    // The clamp lives on the row, so its computed size is the ceiling: fitting
    // never makes the wordmark bigger than the page was designed to show it.
    const ceiling = Number.parseFloat(getComputedStyle(row).fontSize);
    if (available <= 0 || !Number.isFinite(ceiling)) {
      return;
    }

    const clamp = (value: number) =>
      Math.max(MIN_SIZE, Math.min(ceiling, value));

    twin.style.fontSize = `${REFERENCE_SIZE}px`;
    const referenceWidth = twin.getBoundingClientRect().width;
    if (referenceWidth <= 0) {
      return;
    }

    let next = clamp((available / referenceWidth) * REFERENCE_SIZE * SAFETY);

    /*
      A second pass, because the optical size axis reshapes the letters as they
      grow: the widths do not scale perfectly linearly off one measurement, and
      being 2% wide here is a page-wide sideways scroll.
    */
    twin.style.fontSize = `${next}px`;
    const fittedWidth = twin.getBoundingClientRect().width;
    if (fittedWidth > available) {
      next = clamp(next * (available / fittedWidth) * SAFETY);
    }

    setSize(next);
  }, []);

  useEffect(() => {
    const row = rowRef.current;
    if (!row) {
      return;
    }
    fit();
    const observer = new ResizeObserver(fit);
    observer.observe(row);
    return () => observer.disconnect();
  }, [fit]);

  return (
    /*
      The clamp is the ceiling the fitting measures against, and it is the size
      the page has always set the wordmark at: off the viewport the way Inter's
      title is (~14vw there), scaled up because "Glide" is five characters
      against their twenty-six and would otherwise sit marooned in the measure.
      The floor keeps it a headline rather than a hazard on a phone. The
      heading's negative margin is side-bearing compensation, so the G sits on
      the row's gutter.
    */
    <div className="w-full text-[clamp(5rem,24vw,26rem)]" ref={rowRef}>
      {/*
        It stays an `h1` with its heading role and its accessible name: no
        `role="textbox"` and no `aria-label`, so `contentEditable` reports the
        editable state on top of the heading rather than replacing it, and the
        server-rendered text is still "Glide" for anything that does not run
        scripts. Before hydration it renders at the row's clamp, which is the
        size the page has always shown.

        `dangerouslySetInnerHTML` for the same reason the specimen uses it:
        React refuses to manage children under `contentEditable`, and the
        string is a constant, so a re-render for the fitted size cannot
        overwrite what you typed.
      */}
      <h1
        className={`ml-[-0.015em] max-w-full break-words outline-none ${shared}`}
        contentEditable
        dangerouslySetInnerHTML={{ __html: DEFAULT_TITLE }}
        onInput={fit}
        ref={headingRef}
        spellCheck={false}
        style={size ? { fontSize: `${size}px` } : undefined}
        suppressContentEditableWarning
      />

      {/*
        Measured, never seen. `visibility: hidden` rather than `display: none`,
        which has no box to measure, and fixed off-screen so it cannot widen
        the row it is being measured against.
      */}
      <span
        aria-hidden="true"
        className={`pointer-events-none fixed top-0 left-[-200vw] invisible whitespace-pre ${shared}`}
        ref={twinRef}
      />
    </div>
  );
};
