#!/usr/bin/env python3
"""Build the desktop download bundle served at blode.co/glide/glide.zip.

Generates static instances from the shipping variable fonts, then packages them
with the variable fonts, the license, and a README into a Google-Fonts-shaped
zip. Reads fonts/*.ttf and never writes to them.

    python3 scripts/make-desktop-bundle.py

Outputs fonts/static/*.ttf (gitignored, derived) and apps/web/public/glide.zip.

Instance names come from the fvar named instances, which release_glide.py in the
static-to-variable repo already normalises. They are NOT taken from STAT, whose
axis values lack the platform name records fontTools' updateFontNames needs.
"""

import argparse
import os
import shutil
import zipfile
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FONT_DIR = os.path.join(REPO, "fonts")
DEFAULT_STATIC_DIR = os.path.join(DEFAULT_FONT_DIR, "static")
DEFAULT_ZIP_PATH = os.path.join(REPO, "apps", "web", "public", "glide.zip")
WINDOWS = (3, 1, 0x409)
MAC = (1, 0, 0)

# Fixed so the archive hashes the same on every run. Any constant works; this is
# the earliest timestamp the zip format can represent.
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

VARIABLE = ["glide-variable.ttf", "glide-variable-italic.ttf"]
MONO = "glide-mono.ttf"


def set_name(font, name_id, value):
    for platform in (WINDOWS, MAC):
        font["name"].setName(value, name_id, *platform)


def instances_of(path):
    vf = TTFont(path)
    try:
        defaults = {axis.axisTag: axis.defaultValue for axis in vf["fvar"].axes}
        return [
            (
                vf["name"].getDebugName(i.subfamilyNameID),
                vf["name"].getDebugName(i.postscriptNameID),
                int(i.coordinates["wght"]),
                defaults | dict(i.coordinates),
            )
            for i in vf["fvar"].instances
            if all(
                i.coordinates.get(tag, default) == default
                for tag, default in defaults.items()
                if tag != "wght"
            )
        ]
    finally:
        vf.close()


def build_statics(src, italic, static_dir):
    made = []
    for style, ps_name, wght, location in instances_of(src):
        # recalcTimestamp=False keeps head.modified as it is in the source font.
        # Left on, fontTools stamps it at compile time, which was the only thing
        # that differed between local and CI builds. Off, the bundle is
        # byte-reproducible and the release asset can be checked against the
        # copy the site serves.
        font = TTFont(src, recalcTimestamp=False)
        # Pin every axis. Glide 3.1 adds opsz while keeping the desktop statics
        # at the variable font's named/default optical location. Passing only
        # wght would leave a partially-variable font as soon as another axis is
        # introduced and would make the desktop bundle depend on fontTools'
        # partial-instancing behaviour.
        instancer.instantiateVariableFont(font, location, inplace=True)

        is_bold = wght == 700
        ribbi = is_bold or wght == 400

        if ribbi:
            family = "Glide"
            if is_bold:
                subfamily = "Bold Italic" if italic else "Bold"
            else:
                subfamily = "Italic" if italic else "Regular"
        else:
            # Weights outside RIBBI get their own family so apps that only
            # expose four slots per family can still reach them.
            family = f"Glide {style.replace(' Italic', '')}"
            subfamily = "Italic" if italic else "Regular"

        set_name(font, 1, family)
        set_name(font, 2, subfamily)
        set_name(font, 4, f"Glide {style}")
        set_name(font, 6, ps_name)
        set_name(font, 16, "Glide")
        set_name(font, 17, style)

        os2 = font["OS/2"]
        os2.usWeightClass = wght
        flags = os2.fsSelection & ~(1 | (1 << 5) | (1 << 6))
        if italic:
            flags |= 1
        if is_bold:
            flags |= 1 << 5
        if ribbi and not is_bold and not italic:
            flags |= 1 << 6
        os2.fsSelection = flags

        mac_style = font["head"].macStyle & ~0b11
        if is_bold:
            mac_style |= 1
        if italic:
            mac_style |= 1 << 1
        font["head"].macStyle = mac_style

        if "fvar" in font:
            raise AssertionError(f"{ps_name} is still variable")

        out = os.path.join(static_dir, f"{ps_name}.ttf")
        font.save(out)
        font.close()
        made.append(out)
    return made


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", default=DEFAULT_FONT_DIR)
    parser.add_argument("--static-dir", default=DEFAULT_STATIC_DIR)
    parser.add_argument("--zip-path", default=DEFAULT_ZIP_PATH)
    args = parser.parse_args()
    font_dir = os.path.abspath(args.font_dir)
    static_dir = os.path.abspath(args.static_dir)
    zip_path = os.path.abspath(args.zip_path)

    shutil.rmtree(static_dir, ignore_errors=True)
    os.makedirs(static_dir, exist_ok=True)

    statics = []
    for name in VARIABLE:
        src = os.path.join(font_dir, name)
        statics += build_statics(src, italic="italic" in name, static_dir=static_dir)

    readme = os.path.join(REPO, "scripts", "bundle-README.txt")
    ofl = os.path.join(REPO, "OFL.txt")

    entries = [(os.path.join(font_dir, n), f"Glide/{n}") for n in VARIABLE + [MONO]]
    entries += [(p, f"Glide/static/{os.path.basename(p)}") for p in sorted(statics)]
    entries += [(ofl, "Glide/OFL.txt"), (readme, "Glide/README.txt")]

    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for source, arcname in entries:
            # Zip entries carry the file's mtime, so pin it. Without this the
            # archive hash changes on every run even when every file inside is
            # identical.
            info = zipfile.ZipInfo(arcname, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(source, "rb") as fh:
                zf.writestr(info, fh.read())

    size = os.path.getsize(zip_path)
    print(f"{len(statics)} statics -> {static_dir}")
    print(f"{zip_path} ({size / 1_000_000:.1f} MB)")


if __name__ == "__main__":
    main()
