/** Public version, read from the shipped font's name table. */
export const GLIDE_VERSION = "4.0.8";

/** OS/2 + hhea values from the shipped glide-variable.ttf. */
export const GLIDE_METRICS = {
  unitsPerEm: 1000,
  capHeight: 709,
  ascender: 986,
  descender: -277,
} as const;

/**
 * x-height by weight. Glide's x-height rises across the weight axis
 * while cap height stays at a constant 709, so anything drawing an
 * x-height guide must interpolate rather than use the single OS/2
 * value, which describes the default master only.
 */
export const GLIDE_X_HEIGHT_STOPS = [
  [100, 524],
  [400, 532],
  [950, 552],
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
