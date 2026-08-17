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
    "Glide is a variable UI sans-serif by Matthew Blode, with weight 100–950 and optical size 12–28 in roman and italic.",
  links: {
    author: "https://blode.co",
    github: "https://github.com/mblode/glide",
    license: "https://openfontlicense.org",
  },
  name: "Glide",
  url: `https://blode.co${basePath}`,
  version: "4.0.2",
};
