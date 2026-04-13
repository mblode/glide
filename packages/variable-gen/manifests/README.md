# Manifests

This directory now contains the active repair manifest for the Circular donor
pipeline:

- `circular-triage.json`

The manifest controls per-family and per-glyph strategy decisions, including:

- `rebuild_notdef`
- `reference_fallback`
- `manual_review`

It is consumed by:

- `packages/variable-gen/scripts/repair_circular_sources.py`

The broader target manifest shape is still described in:

- [technical spec](../../../docs/variable-gen-technical-spec.md)
