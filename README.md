# Glide

Glide is a variable sans-serif typeface by Matthew Blode, supporting weights from 400 (regular) to 900 (black) in both roman and italic styles.

## Font family

The default font family in [Blode UI](https://ui.blode.co) is "Glide". This versatile variable font is applied using Tailwind's `font-sans` utility class.

```tsx
<p className="font-sans">This text uses the Glide font</p>
<p className="font-sans italic">This text uses Glide italic</p>
```

## Install Glide

### 1. Download the font

Download [glide-variable.woff2](https://ui.blode.co/glide-variable.woff2) and [glide-variable-italic.woff2](https://ui.blode.co/glide-variable-italic.woff2) and place them in your project's `public/` directory.

### 2. Configure the font in your root layout

In `app/layout.tsx`, import `localFont` and configure the Glide variable font:

```tsx
import localFont from "next/font/local";

const glide = localFont({
  src: [
    { path: "../public/glide-variable.woff2", style: "normal" },
    { path: "../public/glide-variable-italic.woff2", style: "italic" },
  ],
  variable: "--font-glide",
  weight: "400 900",
  display: "swap",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={glide.variable}>{children}</body>
    </html>
  );
}
```

### 3. Map the CSS variable in Tailwind

In your global CSS file, map `--font-glide` to Tailwind's `--font-sans` so `font-sans` uses Glide:

```css
@theme inline {
  --font-sans: var(--font-glide);
}
```

### 4. Use it

Glide is now your default sans-serif font. Use `font-sans` with any weight from 400 to 900:

```tsx
<p className="font-sans font-medium">Medium text with Glide</p>
```

## Variable font

Glide is shipped as two variable font files: regular and italic. Each contains all weights in a single file, allowing for precise typography with minimal file size impact.

## Font weights

| Weight | Name      | Class           |
| ------ | --------- | --------------- |
| 400    | Regular   | `font-normal`   |
| 500    | Medium    | `font-medium`   |
| 600    | Semibold  | `font-semibold` |
| 700    | Bold      | `font-bold`     |
| 800    | Extrabold | `font-extrabold`|
| 900    | Black     | `font-black`    |

## Usage in Tailwind

```tsx
// Roman
<p className="font-sans font-normal">Regular text (400)</p>
<p className="font-sans font-medium">Medium text (500)</p>
<p className="font-sans font-semibold">Semibold text (600)</p>
<p className="font-sans font-bold">Bold text (700)</p>
<p className="font-sans font-extrabold">Extra Bold text (800)</p>
<p className="font-sans font-black">Black text (900)</p>

// Italic variants
<p className="font-sans italic">Regular italic (400)</p>
<p className="font-sans font-bold italic">Bold italic (700)</p>
```

## Technical details

- **Family**: Glide
- **Designer**: Matthew Blode
- **Styles**: Roman + Italic (separate variable fonts)
- **Weight range**: 400–900 (variable `wght` axis)
- **Formats**: Variable TTF + WOFF2, static WOFF2 instances
- **Named instances**: Regular (400), Medium (500), Bold (700), Black (900)

## Repo layout

- `glide-variable.glyphs` / `glide-variable-italic.glyphs`: Glyphs source files
- `glide-mono.glyphs`: Mono source file
- `fonts/`: built font files (variable + static) and `glide.css`
- `apps/web/`: Next.js proof and documentation site

The static-to-variable generation pipeline, CLI, reports, and intervention studio now live in [`static-to-variable`](https://github.com/mblode/static-to-variable).

## Development

```bash
npm run dev
npm run build
```

`npm run dev` starts the web app with portless at `https://glide.localhost`.

## License

Copyright Matthew Blode. All rights reserved.
