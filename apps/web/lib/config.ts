/**
 * This app is served at blode.co/glide, proxied by the blode.co host app's
 * multi-zone rewrite. `basePath` is imported by next.config.ts so the prefix
 * lives in exactly one place.
 */
export const basePath = "/glide";

/**
 * `basePath` covers next/link and route handlers. It does NOT cover raw
 * `<a href>`, `<img src>`, `next/image` src, or manifest icon paths, so those
 * go through this helper.
 */
export const asset = (path: string) => `${basePath}${path}`;

export const siteConfig = {
  author: {
    name: "Matthew Blode",
    url: "https://blode.co",
  },
  description:
    "Glide is a variable sans-serif font family by Matthew Blode. Weights from 100 to 950 in roman and italic.",
  links: {
    author: "https://blode.co",
    github: "https://github.com/mblode/glide",
  },
  name: "Glide",
  url: `https://blode.co${basePath}`,
  version: "3.0.0",
};
