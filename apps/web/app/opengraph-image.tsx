import { renderZoneOgImage } from "@/app/og-image-shared";

export {
  OG_CONTENT_TYPE as contentType,
  OG_SIZE as size,
} from "@/app/og-image-shared";

export const alt = "Glide";

/**
 * The house card (Rule 12), replacing the static `public/opengraph-image.png`.
 *
 * Converting the PNG to a generated route is also the Rule 11 fix. This zone
 * historically doubled its card to `/glide/glide/opengraph-image.png` when the
 * static file convention stacked with a zone `metadataBase`. A generated route
 * is not basePath-prefixed, so `metadataBase` supplies `/glide` exactly once
 * and the card lands at `/glide/opengraph-image`.
 *
 * The matching `twitter-image.png` is gone rather than converted: Next reuses
 * this route for `twitter:image`, and the old pair were the same file twice.
 */
export default function OpengraphImage() {
  return renderZoneOgImage({
    badge: "GLIDE",
    eyebrow: "blode.co/glide",
    // Shorter than the meta description, which runs long for the SERP. A card
    // is read in a feed, at a glance.
    subtitle: "A variable sans-serif for UI. Weights 100–950, roman and italic.",
    title: "Glide",
  });
}
