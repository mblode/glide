export const siteConfig = {
  name: "Glide",
  url: "https://glide.blode.co",
  version: "1.1",
  description:
    "Glide is a variable sans-serif font family by Matthew Blode. Weights from 100 to 950 in roman and italic.",
  author: {
    name: "Matthew Blode",
    url: "https://matthewblode.com",
  },
  links: {
    author: "https://matthewblode.com",
    github: "https://github.com/mblode/glide",
  },
  get downloadUrl() {
    return `${this.links.github}/releases/download/v${this.version}/Glide-${this.version}.zip`;
  },
};
