# Glide

Glide is a variable sans-serif typeface by Matthew Blode, supporting weights from 100 (thin) to 900 (black) in both roman and italic styles. The family also includes **Glide Mono**, a monospaced companion font for code and technical content.

## Font family

The default font family in [Blode UI](https://ui.blode.co) is "Glide". This versatile variable font is applied using Tailwind's `font-sans` utility class, and Glide Mono is used via `font-mono`.

```tsx
<p className="font-sans">This text uses the Glide font</p>
<p className="font-sans italic">This text uses Glide italic</p>
<code className="font-mono">const glide = "mono";</code>
```

## Install Glide

### 1. Download the fonts

Download [glide-variable.woff2](https://glide.blode.co/glide-variable.woff2), [glide-variable-italic.woff2](https://glide.blode.co/glide-variable-italic.woff2), and [glide-mono.woff2](https://glide.blode.co/glide-mono.woff2) and place them in your project's `public/` directory.

### 2. Configure the fonts in your root layout

In `app/layout.tsx`, import `localFont` and configure both Glide and Glide Mono:

```tsx
import localFont from "next/font/local";

const glide = localFont({
  src: [
    { path: "../public/glide-variable.woff2", style: "normal" },
    { path: "../public/glide-variable-italic.woff2", style: "italic" },
  ],
  variable: "--font-glide",
  weight: "100 900",
  display: "swap",
});

const glideMono = localFont({
  src: [{ path: "../public/glide-mono.woff2", style: "normal" }],
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

### 3. Map the CSS variables in Tailwind

In your global CSS file, map `--font-glide` to Tailwind's `--font-sans` and `--font-glide-mono` to `--font-mono`:

```css
@theme inline {
  --font-sans: var(--font-glide);
  --font-mono: var(--font-glide-mono);
}
```

### 4. Use it

Glide is now your default sans-serif font, and Glide Mono is your monospace font. Use `font-sans` with any weight from 100 to 900, and `font-mono` for code:

```tsx
<p className="font-sans font-medium">Medium text with Glide</p>
<code className="font-mono">const glide = "mono";</code>
```

## Glide Mono

Glide Mono is the monospaced companion to Glide, designed for code editors, terminals, and technical UI. It shares the same design language as Glide — clean geometry and high legibility — adapted for fixed-width contexts.

```tsx
<code className="font-mono">const glide = "mono";</code>
```

Glide Mono is a static font at weight 400.

## Variable font

Glide is shipped as two variable font files: regular and italic. Each contains all weights in a single file, allowing for precise typography with minimal file size impact.

## Font weights

| Weight | Name      | Class            |
| ------ | --------- | ---------------- |
| 100    | Thin      | `font-thin`      |
| 200    | ExtraLight| `font-extralight`|
| 300    | Light     | `font-light`     |
| 400    | Regular   | `font-normal`    |
| 500    | Medium    | `font-medium`    |
| 600    | Semibold  | `font-semibold`  |
| 700    | Bold      | `font-bold`      |
| 800    | Extrabold | `font-extrabold` |
| 900    | Black     | `font-black`     |

## Usage in Tailwind

```tsx
// Roman
<p className="font-sans font-thin">Thin text (100)</p>
<p className="font-sans font-light">Light text (300)</p>
<p className="font-sans font-normal">Regular text (400)</p>
<p className="font-sans font-medium">Medium text (500)</p>
<p className="font-sans font-semibold">Semibold text (600)</p>
<p className="font-sans font-bold">Bold text (700)</p>
<p className="font-sans font-extrabold">Extra Bold text (800)</p>
<p className="font-sans font-black">Black text (900)</p>

// Italic variants
<p className="font-sans italic">Regular italic (400)</p>
<p className="font-sans font-bold italic">Bold italic (700)</p>

// Mono
<code className="font-mono">const glide = "mono";</code>
```

## Technical details

### Glide

- **Family**: Glide
- **Designer**: Matthew Blode
- **Styles**: Roman + Italic (separate variable fonts)
- **Weight range**: 100–900 (variable `wght` axis)
- **Formats**: Variable TTF + WOFF2
- **Named instances**: Regular (400), Medium (500), Bold (700), Black (900)

### Glide Mono

- **Family**: Glide Mono
- **Designer**: Matthew Blode
- **Styles**: Regular
- **Weight**: 400 (static)
- **Formats**: TTF + WOFF2

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
