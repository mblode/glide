<div align="center">

# [Glide](https://blode.co/glide)

**Glide 3 is a variable sans-serif with a continuous 100 to 950 weight axis in roman and italic, paired with Glide Mono**

Ship every weight from Thin to Extra Black out of one small font file, with a mono companion for code.

Version 3.001 raises the family’s x-height to 532 units (x/cap 0.750, Inter’s
bar) while retaining its 709-unit cap height, giving UI and body text more
presence without changing the 1000-unit em or the established weight range.

</div>

<p align="center">
  <img alt="The Glide specimen page, showing the weight slider and a live sample at 700" src=".github/assets/screenshot.jpg" width="800" />
</p>

## Demo

See the whole family set as running text and specimens.

<p>
<a href="https://blode.co/glide">
<img alt="View the specimen" src=".github/assets/demo.svg" width="200" />
</a>
</p>

## Install

For the web, put the three WOFF2 files in `app/fonts/` next to your root layout:

```bash
curl -O https://blode.co/glide/glide-variable.woff2
curl -O https://blode.co/glide/glide-variable-italic.woff2
curl -O https://blode.co/glide/glide-mono.woff2
```

For Font Book and design tools, download [glide.zip](https://blode.co/glide/glide.zip): the variable TTFs plus every static instance.

## Quickstart

Configure both fonts in `app/layout.tsx`:

```tsx
import localFont from "next/font/local";
import "./globals.css";

const glide = localFont({
  src: [
    { path: "./fonts/glide-variable.woff2", style: "normal" },
    { path: "./fonts/glide-variable-italic.woff2", style: "italic" },
  ],
  variable: "--font-glide",
  weight: "100 950",
  display: "swap",
});

const glideMono = localFont({
  src: "./fonts/glide-mono.woff2",
  variable: "--font-glide-mono",
  weight: "400",
  display: "swap",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${glide.variable} ${glideMono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

Map the variables onto Tailwind's own in your global CSS:

```css
@theme inline {
  --font-sans: var(--font-glide);
  --font-mono: var(--font-glide-mono);
}
```

`font-sans` is now Glide, `font-mono` is Glide Mono, and `italic` picks up the real italic rather than a slanted roman.

## Font weights

Every standard weight is a named instance, so the full ladder shows up in font menus like Font Book. Values in between work too, because the axis is continuous.

| Weight | Name | Class |
| ------ | ---- | ----- |
| 100 | Thin | `font-thin` |
| 200 | ExtraLight | `font-extralight` |
| 300 | Light | `font-light` |
| 400 | Regular | `font-normal` |
| 500 | Medium | `font-medium` |
| 600 | Semibold | `font-semibold` |
| 700 | Bold | `font-bold` |
| 800 | Extrabold | `font-extrabold` |
| 900 | Black | `font-black` |
| 950 | Extra Black | `font-[950]` |

## Notes

- **Two variable files:** roman and italic ship separately, each interpolating the whole axis from three masters (Thin, Regular, Extra Black).
- **Glide Mono:** a static font at weight 400, for code editors, terminals, and technical UI.
- **Formats:** variable TTF and WOFF2, with static instances in the desktop bundle.
- **Blode UI:** Glide is the default family there, applied through `font-sans` and `font-mono`.

## License

[SIL Open Font License 1.1](OFL.txt). Use Glide in personal and commercial work, embed it, modify it. You can't sell the font files on their own, and modified versions can't use the Glide name. Copyright 2026 Matthew Blode.

---

Crafted by [<img src="https://blode.co/avatar-circle.png" width="20" align="top" />](https://blode.co) [Matthew Blode](https://blode.co)
