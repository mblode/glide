/** Public version, read from the shipped font's name table. */
export const GLIDE_VERSION = "4.0.15";

/** OS/2 + hhea values from the shipped glide-variable.ttf. */
export const GLIDE_METRICS = {
  unitsPerEm: 1000,
  capHeight: 709,
  ascender: 986,
  descender: -277,
} as const;

/** The glyph inspector renders the Text optical size explicitly. */
export const GLIDE_TEXT_OPSZ = 14;

/** Measured Text x-height by weight; Roman and Italic are independent. */
export const GLIDE_X_HEIGHT_STOPS = [
  [100, 474],
  [400, 479],
  [950, 499],
] as const satisfies readonly (readonly [number, number])[];
export const GLIDE_ITALIC_X_HEIGHT_STOPS = [
  [100, 474],
  [400, 479],
  [950, 499],
] as const satisfies readonly (readonly [number, number])[];

/**
 * Glide Mono is single-weight, so its x-height does not vary and it
 * needs constants rather than stops. Anything drawing metric guides
 * must switch on the family: the proportional stops do not apply.
 */
export const GLIDE_MONO_METRICS = {
  capHeight: 709,
  xHeight: 532,
} as const;
