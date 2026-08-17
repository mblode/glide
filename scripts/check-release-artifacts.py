#!/usr/bin/env python3
"""Verify that every public Glide font mirror and ZIP member agrees.

The canonical files live in ``fonts/``. The specimen app and CSS directory
mirror those files, and the desktop archive embeds the variable TTFs. A release
must never serve different binaries under the same filename.

Optionally pass the private pipeline's release manifest. In that mode every
canonical public font must have a matching filename and SHA-256 in the signed-
off build inventory.

    python3 scripts/check-release-artifacts.py
    python3 scripts/check-release-artifacts.py \
      --manifest release/glide-3.1.0-manifest.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile


REPO = Path(__file__).resolve().parent.parent
FONT_DIR = REPO / "fonts"
PUBLIC_DIR = REPO / "apps" / "web" / "public"
WEB_DIR = FONT_DIR / "web"
ZIP_PATH = PUBLIC_DIR / "glide.zip"

FONT_FILES = (
    "glide-variable.ttf",
    "glide-variable-italic.ttf",
    "glide-variable.woff2",
    "glide-variable-italic.woff2",
    "glide-mono.ttf",
    "glide-mono.woff2",
)
ZIP_CANONICAL = (
    "glide-variable.ttf",
    "glide-variable-italic.ttf",
    "glide-mono.ttf",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        raise AssertionError(f"missing {path.relative_to(REPO)}") from None


def check_mirrors() -> list[str]:
    errors = []
    for name in FONT_FILES:
        canonical = read(FONT_DIR / name)
        mirrors = [PUBLIC_DIR / name]
        if name.endswith(".woff2"):
            mirrors.append(WEB_DIR / name)
        for mirror in mirrors:
            actual = read(mirror)
            if actual != canonical:
                errors.append(
                    f"{mirror.relative_to(REPO)} differs from fonts/{name}: "
                    f"{sha256(actual)} != {sha256(canonical)}"
                )
    return errors


def check_zip() -> list[str]:
    errors = []
    with zipfile.ZipFile(ZIP_PATH) as archive:
        members = set(archive.namelist())
        for name in ZIP_CANONICAL:
            member = f"Glide/{name}"
            if member not in members:
                errors.append(f"{ZIP_PATH.relative_to(REPO)} is missing {member}")
                continue
            actual = archive.read(member)
            canonical = read(FONT_DIR / name)
            if actual != canonical:
                errors.append(
                    f"{member} differs from fonts/{name}: "
                    f"{sha256(actual)} != {sha256(canonical)}"
                )
    return errors


def manifest_artifacts(manifest: dict) -> list[dict]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise AssertionError("manifest.artifacts must be a list")
    return artifacts


def check_manifest(path: Path) -> list[str]:
    manifest = json.loads(read(path).decode("utf-8"))
    by_name: dict[str, set[str]] = {}
    for artifact in manifest_artifacts(manifest):
        artifact_path = artifact.get("path")
        digest = artifact.get("sha256")
        if not isinstance(artifact_path, str) or not isinstance(digest, str):
            raise AssertionError("every manifest artifact needs path and sha256")
        by_name.setdefault(Path(artifact_path).name, set()).add(digest)

    errors = []
    for name in FONT_FILES:
        digest = sha256(read(FONT_DIR / name))
        if digest not in by_name.get(name, set()):
            errors.append(f"fonts/{name} ({digest}) is absent from {path}")
    return errors


def check_versioned_manifests() -> tuple[list[str], int]:
    errors = []
    checked = 0
    for path in sorted(PUBLIC_DIR.glob("[0-9]*/*.json")):
        manifest = json.loads(read(path).decode("utf-8"))
        artifacts = manifest_artifacts(manifest)
        checked += 1
        for artifact in artifacts:
            relative = artifact.get("path")
            digest = artifact.get("sha256")
            size = artifact.get("size")
            if not isinstance(relative, str) or not isinstance(digest, str):
                errors.append(f"{path.relative_to(REPO)} has an invalid artifact")
                continue
            artifact_path = Path(relative)
            if artifact_path.parent.name == "static":
                continue
            versioned_path = path.parent / artifact_path.name
            data = read(versioned_path)
            if len(data) != size:
                errors.append(f"{versioned_path.relative_to(REPO)} size is wrong")
            if sha256(data) != digest:
                errors.append(f"{versioned_path.relative_to(REPO)} hash is wrong")
    return errors, checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        help="pipeline manifest whose artifacts must include every public font",
    )
    args = parser.parse_args()

    try:
        errors = check_mirrors() + check_zip()
        versioned_errors, versioned_count = check_versioned_manifests()
        errors += versioned_errors
        if args.manifest:
            errors += check_manifest(args.manifest.resolve())
    except (AssertionError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        errors = [str(error)]

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    print(f"ok   {len(FONT_FILES)} canonical fonts match every public mirror")
    print(f"ok   {len(ZIP_CANONICAL)} canonical fonts match glide.zip")
    print(f"ok   {versioned_count} versioned release manifests match their assets")
    if args.manifest:
        print(f"ok   public fonts match {args.manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
