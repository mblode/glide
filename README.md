<div align="center">

# [Glide](https://blode.co/glide)

**Glide 3 is a variable sans-serif with a continuous 100 to 950 weight axis in roman and italic, paired with Glide Mono**

Ship every weight from Thin to Extra Black out of one small font file, with a mono companion for code.

Version 3.002 keeps the family’s x-height at 532 units (x/cap 0.750, Inter’s
bar) with full width restore after the raise — bowls and arms track Glide 3.000
/ Circular more closely than the 3.001 half-X pin recipe.

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

For the web, put the WOFF2 files in `app/fonts/` next to your root layout:

```bash
curl -O https://blode.co/glide/glide-variable.woff2
curl -O https://blode.co/glide/glide-variable-italic.woff2
curl -O https://blode.co/glide/glide-mono-variable.woff2
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
  src: "./fonts/glide-mono-variable.woff2",
  variable: "--font-glide-mono",
  weight: "100 700",
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

- **Two variable files:** roman and italic ship separately, each interpolating the whole axis from three masters (Thin, Regular, Extra Black). One `wght` axis only — no optical-size axis.
- **Glide Mono:** a variable companion from 100 to 700. Ligatures stay off by default so `-->` and `==` keep their cell width. A static 400 cut is still in the desktop zip.
- **Size:** use the tracking classes in `fonts/web/glide.css` (`.glide-ui`, `.glide-display`) instead of an `opsz` axis.
- **Features:** ligatures on for Sans (`fi`/`fl` and `->`/`=>`). Tabular figures and slashed zero are opt-in (`.glide-tnum`, `.glide-zero`). Mono keeps `tnum` and `zero` on, ligatures off.
- **Formats:** variable TTF and WOFF2, with static instances in the desktop bundle.
- **Blode UI:** Glide is the default family there, applied through `font-sans` and `font-mono`.

## License

[SIL Open Font License 1.1](OFL.txt). Use Glide in personal and commercial work, embed it, modify it. You can't sell the font files on their own, and modified versions can't use the Glide name. Copyright 2026 Matthew Blode.

---

Crafted by [<img src="https://blode.co/avatar-circle.png" width="20" align="top" />](https://blode.co) [Matthew Blode](https://blode.co)
