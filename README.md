# Glide

A variable font supporting weights from 400 (regular) to 900 (black).

- **Variable font:** All weights in a single file for minimal file size and smooth weight transitions.
- **Weight range 400–900:** Regular, medium, semibold, bold, extrabold, and black.
- **Web-optimized:** Ships as `.woff2` for fast loading in browsers.
- **Tailwind-ready:** Maps directly to `font-sans` with standard weight utilities.

## Download

- [Glide-Variable.woff2](https://raw.githubusercontent.com/mblode/glide/main/Glide-Variable.woff2) — web font (recommended)
- [glide-variable.ttf](https://raw.githubusercontent.com/mblode/glide/main/glide-variable.ttf) — TrueType format

## Usage with Next.js + Tailwind CSS

### 1. Add the font to your project

Download `glide-variable.woff2` and place it in your project's `public/` directory.

### 2. Configure the font in your root layout

```tsx
import localFont from "next/font/local";

const glide = localFont({
  src: [{ path: "../public/glide-variable.woff2" }],
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

In your global CSS file, map `--font-glide` to Tailwind's `--font-sans`:

```css
@theme inline {
  --font-sans: var(--font-glide);
}
```

### 4. Use it

Glide is now your default sans-serif font. Apply any weight from 400 to 900:

```tsx
<p className="font-sans font-medium">Medium weight text</p>
<h1 className="font-sans font-bold">Bold heading</h1>
```

## Font Weights

| Weight | Name      | Tailwind Class   |
|--------|-----------|------------------|
| 400    | Regular   | `font-normal`    |
| 500    | Medium    | `font-medium`    |
| 600    | Semibold  | `font-semibold`  |
| 700    | Bold      | `font-bold`      |
| 800    | Extrabold | `font-extrabold` |
| 900    | Black     | `font-black`     |
