"use client";

import type { ComponentProps } from "react";

import { captureConversion } from "@/lib/conversion-events";

type TrackedLinkProps = {
  href: string;
  /** Wording-independent name for the action, such as "download-desktop". */
  label: string;
  /** Where on the page it sits: "nav", "hero", "install". */
  location: string;
} & Omit<ComponentProps<"a">, "href" | "onClick">;

/**
 * Anchor that fires `cta_clicked` or `download_clicked` before navigating.
 *
 * A plain `<a>`, never `next/link`: every href it carries is either a same-page
 * fragment or a file in `public/`, and `next/link` would prefetch an RSC
 * payload for a route that does not exist.
 */
export const TrackedLink = ({
  children,
  href,
  label,
  location,
  ...rest
}: TrackedLinkProps) => (
  <a
    href={href}
    onClick={() => captureConversion({ href, label, location })}
    {...rest}
  >
    {children}
  </a>
);
