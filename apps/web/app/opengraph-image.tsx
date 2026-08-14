import { OgLogo } from "@/app/og-logo";
import { renderZoneOgImage } from "@/app/og-image-shared";

export {
  OG_CONTENT_TYPE as contentType,
  OG_SIZE as size,
} from "@/app/og-image-shared";

export const alt = "Glide";

/**
 * This zone's card. Colours and mark come from Glide (`#fbb6cd` / `#8b1a0a`
 * and `app/icon0.svg`); type is Glide. A generated route is the form that
 * cannot double under `basePath`.
 */
export default function OpengraphImage() {
  return renderZoneOgImage({
    background: "#fdc5d7",
    color: "#e8391c",
    logo: <OgLogo />,
    title: "Glide",
  });
}
