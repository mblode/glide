import posthog from "posthog-js";

/**
 * The conversion events blode.co already sends from its own CTAs
 * (`blode-co/apps/web/lib/conversion-events.ts`). A zone reuses these names
 * and property keys rather than inventing its own, so one funnel spans the
 * hub and every product page.
 *
 * Until this shipped, /glide sent no conversion events at all: every reading
 * of the hero came from `$autocapture` element text, which breaks the moment a
 * label is reworded. `label` and `location` survive a rewording.
 */
export const CTA_CLICKED_EVENT = "cta_clicked";
export const DOWNLOAD_CLICKED_EVENT = "download_clicked";

/**
 * blode.co counts `.zip` and `.dmg` as downloads because those are the only
 * binaries it serves. Here the font files themselves are the product, so a
 * `.woff2` or `.ttf` click is the same conversion as taking the desktop
 * bundle, and it belongs on the same event.
 */
const DOWNLOAD_HREF = /\.(?:zip|ttf|woff2)(?:[?#]|$)/iu;

export const isDownloadHref = (href: string): boolean =>
  DOWNLOAD_HREF.test(href);

export const conversionEventForHref = (
  href: string
): typeof CTA_CLICKED_EVENT | typeof DOWNLOAD_CLICKED_EVENT =>
  isDownloadHref(href) ? DOWNLOAD_CLICKED_EVENT : CTA_CLICKED_EVENT;

export interface ConversionClick {
  href: string;
  /** Wording-independent name for the action, such as "download-desktop". */
  label: string;
  /** Where on the page it was clicked: "nav", "hero", "install". */
  location: string;
}

/**
 * `$pathname` and `$current_url` so a funnel can join the click to the
 * `$pageview` that preceded it. Never throws: a click has to navigate even
 * when analytics is blocked.
 */
export const captureConversion = ({
  href,
  label,
  location,
}: ConversionClick): void => {
  try {
    posthog.capture(conversionEventForHref(href), {
      href,
      label,
      location,
      ...(typeof window === "undefined"
        ? {}
        : {
            $current_url: `${window.location.origin}${window.location.pathname}`,
            $pathname: window.location.pathname,
          }),
    });
  } catch {
    // Analytics must not be able to fail a click.
  }
};
