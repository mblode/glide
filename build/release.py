#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.woff2 import compress as compress_woff2
from fontTools.varLib.instancer import instantiateVariableFont

from font_metadata import DESIGNER, MANUFACTURER, WEIGHT_NAMES, patch_metadata
LEGACY_NAME = "F" + "ingertip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and package the Glide release.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Rebuild and package Roman + Italic.")
    build.add_argument("--force", action="store_true", help="Delete generated output first.")

    subparsers.add_parser("verify", help="Verify packaged artifacts and metadata.")
    subparsers.add_parser("zip", help="Create a versioned release archive.")
    subparsers.add_parser("clean", help="Delete generated work and release directories.")
    return parser.parse_args()


def run(cmd: list[str], cwd: Path) -> None:
    completed = subprocess.run(cmd, cwd=cwd, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def read_version(version_file: Path) -> str:
    return version_file.read_text().strip()


def release_paths(repo_root: Path) -> dict[str, Path]:
    build_dir = repo_root / "build"
    work_dir = build_dir / "work"
    release_dir = build_dir / "release"
    return {
        "repo": repo_root,
        "build_scripts": build_dir,
        "docs_proof_source": repo_root / "docs" / "proof" / "index.html",
        "donors": repo_root / "src" / "donors" / "circular",
        "source_ttf": repo_root / "src" / "glide-variable.ttf",
        "version_file": repo_root / "version.txt",
        "work": work_dir,
        "work_sources": work_dir / "sources" / "glide-root-derived",
        "work_manifests": work_dir / "manifests",
        "work_fontlab": work_dir / "fontlab-ready",
        "work_normalized": work_dir / "normalized",
        "work_output": work_dir / "output",
        "work_reports": work_dir / "reports",
        "work_instances_roman": work_dir / "output" / "instances-roman",
        "work_instances_italic": work_dir / "output" / "instances-italic",
        "work_instances_italic_exact": work_dir / "output" / "instances-italic-exact",
        "release": release_dir,
        "release_variable_ttf": release_dir / "fonts" / "variable" / "ttf",
        "release_variable_woff": release_dir / "fonts" / "variable" / "woff",
        "release_variable_woff2": release_dir / "fonts" / "variable" / "woff2",
        "release_static_ttf": release_dir / "fonts" / "static" / "ttf",
        "release_static_woff": release_dir / "fonts" / "static" / "woff",
        "release_static_woff2": release_dir / "fonts" / "static" / "woff2",
        "release_static_otf": release_dir / "fonts" / "static" / "otf",
        "release_proof": release_dir / "proof",
        "release_reference": release_dir / "proof" / "reference",
        "release_reference_exact": release_dir / "proof" / "reference" / "exact",
        "release_metadata": release_dir / "metadata",
    }


def clean_generated(paths: dict[str, Path]) -> None:
    for key in ("work", "release"):
        path = paths[key]
        if path.exists():
            shutil.rmtree(path)


def ensure_dirs(paths: dict[str, Path]) -> None:
    for key, path in paths.items():
        if key.startswith("release_") or key.startswith("work_"):
            if path.suffix:
                continue
            path.mkdir(parents=True, exist_ok=True)


def build_workspace(paths: dict[str, Path]) -> None:
    python_exe = sys.executable
    scripts_dir = paths["build_scripts"]
    repo_root = paths["repo"]
    root_manifest = paths["work_manifests"] / "glide-root-derived.json"
    combined_manifest = paths["work_manifests"] / "glide-root-plus-seeded-italic.json"

    run(
        [
            python_exe,
            str(scripts_dir / "extract_root_glide_masters.py"),
            "--input",
            str(paths["source_ttf"]),
            "--output-dir",
            str(paths["work_sources"]),
            "--manifest",
            str(root_manifest),
            "--source-family-name",
            "Glide Source",
        ],
        repo_root,
    )
    run(
        [
            python_exe,
            str(scripts_dir / "seed_glide_italic_from_circular.py"),
            "--roman-dir",
            str(paths["work_sources"]),
            "--roman-manifest",
            str(root_manifest),
            "--donor-dir",
            str(paths["donors"]),
            "--output-dir",
            str(paths["work_sources"]),
            "--manifest-out",
            str(combined_manifest),
            "--report-out",
            str(paths["work_reports"] / "glide-italic-seed-report.json"),
            "--style-family-name",
            "Glide Source",
        ],
        repo_root,
    )
    run(
        [
            python_exe,
            str(scripts_dir / "prepare_for_fontlab.py"),
            "--sample-dir",
            str(paths["work_sources"]),
            "--manifest",
            str(combined_manifest),
            "--output-dir",
            str(paths["work_fontlab"]),
            "--reports-dir",
            str(paths["work_reports"] / "fontlab"),
            "--force",
        ],
        repo_root,
    )
    run(
        [
            python_exe,
            str(scripts_dir / "build_variable.py"),
            "--manifest",
            str(combined_manifest),
            "--sample-dir",
            str(paths["work_fontlab"]),
            "--output-dir",
            str(paths["work_output"]),
            "--normalized-dir",
            str(paths["work_normalized"]),
            "--reports-dir",
            str(paths["work_reports"]),
            "--italic-kerning-donor-dir",
            str(paths["donors"]),
            "--force",
        ],
        repo_root,
    )
    run(
        [
            python_exe,
            str(scripts_dir / "generate_instances.py"),
            "--input",
            str(paths["work_output"] / "glide-cli-roman-variable.ttf"),
            "--output-dir",
            str(paths["work_instances_roman"]),
            "--weights",
            "400,500,700,900",
            "--manifest",
            str(combined_manifest),
            "--family-key",
            "roman",
            "--validate",
            str(paths["work_fontlab"]),
            "--json-report",
            str(paths["work_reports"] / "roman-instance-validation.json"),
        ],
        repo_root,
    )
    run(
        [
            python_exe,
            str(scripts_dir / "generate_instances.py"),
            "--input",
            str(paths["work_output"] / "glide-cli-italic-variable.ttf"),
            "--output-dir",
            str(paths["work_instances_italic"]),
            "--weights",
            "400,500,700,900",
            "--manifest",
            str(combined_manifest),
            "--family-key",
            "italic",
            "--validate",
            str(paths["work_fontlab"]),
            "--json-report",
            str(paths["work_reports"] / "italic-instance-validation.json"),
        ],
        repo_root,
    )
    run(
        [
            python_exe,
            str(scripts_dir / "apply_circular_italic_kerning_to_instances.py"),
            "--instances-dir",
            str(paths["work_instances_italic"]),
            "--output-dir",
            str(paths["work_instances_italic_exact"]),
            "--donor-dir",
            str(paths["donors"]),
            "--report-out",
            str(paths["work_reports"] / "italic-instance-exact-kerning.json"),
        ],
        repo_root,
    )


def save_woff(source_ttf: Path, output_woff: Path) -> None:
    font = TTFont(source_ttf)
    font.flavor = "woff"
    font.save(output_woff)


def save_woff2(source_ttf: Path, output_woff2: Path) -> None:
    compress_woff2(str(source_ttf), str(output_woff2))


def generate_otf(source_ttf: Path, output_otf: Path) -> None:
    cmd = [
        "fontforge",
        "-lang=ff",
        "-c",
        "Open($1); Generate($2)",
        str(source_ttf),
        str(output_otf),
    ]
    run(cmd, source_ttf.parent)


def package_variable_font(
    source_ttf: Path,
    output_stem: str,
    output_dirs: dict[str, Path],
    *,
    italic: bool,
    version: str,
) -> list[str]:
    font = TTFont(source_ttf)
    patch_metadata(
        font,
        family_name="Glide",
        style_name="Italic" if italic else "Regular",
        weight=400,
        italic=italic,
        version_string=f"Version {version}",
    )
    final_ttf = output_dirs["ttf"] / f"{output_stem}.ttf"
    font.save(final_ttf)

    final_woff = output_dirs["woff"] / f"{output_stem}.woff"
    final_woff2 = output_dirs["woff2"] / f"{output_stem}.woff2"
    save_woff(final_ttf, final_woff)
    save_woff2(final_ttf, final_woff2)
    return [str(final_ttf), str(final_woff), str(final_woff2)]


def package_static_family(
    variable_font_path: Path,
    output_dirs: dict[str, Path],
    *,
    italic: bool,
    version: str,
) -> list[str]:
    packaged: list[str] = []
    for weight, weight_name in WEIGHT_NAMES.items():
        font = instantiateVariableFont(TTFont(variable_font_path), {"wght": weight})
        style_name = f"{weight_name} Italic" if italic else weight_name
        style_suffix = f"{weight_name}Italic" if italic else weight_name
        patch_metadata(
            font,
            family_name="Glide",
            style_name=style_name,
            weight=weight,
            italic=italic,
            version_string=f"Version {version}",
        )
        ttf_path = output_dirs["ttf"] / f"Glide-{style_suffix}.ttf"
        woff_path = output_dirs["woff"] / f"Glide-{style_suffix}.woff"
        woff2_path = output_dirs["woff2"] / f"Glide-{style_suffix}.woff2"
        otf_path = output_dirs["otf"] / f"Glide-{style_suffix}.otf"
        font.save(ttf_path)
        save_woff(ttf_path, woff_path)
        save_woff2(ttf_path, woff2_path)
        generate_otf(ttf_path, otf_path)
        packaged.extend([str(ttf_path), str(woff_path), str(woff2_path), str(otf_path)])
    return packaged


def write_css(paths: dict[str, Path]) -> Path:
    css_path = paths["release"] / "fonts" / "glide.css"
    css_path.write_text(
        """@font-face {
  font-family: "Glide";
  src:
    url("./variable/woff2/glide-variable.woff2") format("woff2"),
    url("./variable/woff/glide-variable.woff") format("woff"),
    url("./variable/ttf/glide-variable.ttf") format("truetype");
  font-style: normal;
  font-weight: 400 900;
  font-display: swap;
}

@font-face {
  font-family: "Glide";
  src:
    url("./variable/woff2/glide-variable-italic.woff2") format("woff2"),
    url("./variable/woff/glide-variable-italic.woff") format("woff"),
    url("./variable/ttf/glide-variable-italic.ttf") format("truetype");
  font-style: italic;
  font-weight: 400 900;
  font-display: swap;
}
"""
    )
    return css_path


def sync_proof(paths: dict[str, Path]) -> Path:
    source_html = paths["docs_proof_source"]
    target_html = paths["release_proof"] / "index.html"
    html = source_html.read_text()
    html = html.replace("../../build/release/fonts/", "../fonts/")
    html = html.replace("../../build/release/proof/reference/", "./reference/")
    target_html.write_text(html)

    for donor_name in (
        "lineto-circular-bookItalic.ttf",
        "lineto-circular-mediumItalic.ttf",
        "lineto-circular-boldItalic.ttf",
        "lineto-circular-blackItalic.ttf",
    ):
        shutil.copy2(paths["donors"] / donor_name, paths["release_reference"] / donor_name)

    for font_path in sorted(paths["work_instances_italic_exact"].glob("*.ttf")):
        shutil.copy2(font_path, paths["release_reference_exact"] / font_path.name)
    return target_html


def write_release_metadata(
    paths: dict[str, Path],
    packaged_files: list[str],
    proof_path: Path,
    version: str,
) -> Path:
    metadata_path = paths["release_metadata"] / "release.json"
    payload = {
        "family": "Glide",
        "version": version,
        "designer": DESIGNER,
        "manufacturer": MANUFACTURER,
        "formats": ["ttf", "otf", "woff2", "woff"],
        "build_command": "make build",
        "files": sorted(
            str(Path(file_path).relative_to(paths["repo"])) if Path(file_path).is_absolute() else file_path
            for file_path in packaged_files
        ),
        "proof": str(proof_path.relative_to(paths["repo"])),
    }
    metadata_path.write_text(json.dumps(payload, indent=2))
    return metadata_path


def verify_release(paths: dict[str, Path]) -> Path:
    required = [
        paths["release_variable_ttf"] / "glide-variable.ttf",
        paths["release_variable_ttf"] / "glide-variable-italic.ttf",
        paths["release_variable_woff2"] / "glide-variable.woff2",
        paths["release_variable_woff2"] / "glide-variable-italic.woff2",
        paths["release_variable_woff"] / "glide-variable.woff",
        paths["release_variable_woff"] / "glide-variable-italic.woff",
        paths["release"] / "fonts" / "glide.css",
        paths["release_proof"] / "index.html",
    ]
    missing = [str(path) for path in required if not path.exists()]

    font_checks: list[dict[str, object]] = []
    for font_path in sorted(paths["release"].glob("fonts/**/*.ttf")) + sorted(paths["release"].glob("fonts/**/*.otf")):
        font = TTFont(font_path)
        names = {
            name_id: sorted(
                {
                    record.toUnicode()
                    for record in font["name"].names
                    if record.nameID == name_id and record.platformID == 3
                }
            )
            for name_id in (1, 3, 4, 5, 6, 8, 9, 16, 17)
        }
        all_values = " ".join(value for values in names.values() for value in values)
        font_checks.append(
            {
                "path": str(font_path.relative_to(paths["repo"])),
                "has_legacy_name": LEGACY_NAME in all_values,
                "designer": names.get(9, []),
                "manufacturer": names.get(8, []),
            }
        )

    readme = (paths["repo"] / "README.md").read_text()
    payload = {
        "missing": missing,
        "counts": {
            "variable_ttf": len(list(paths["release_variable_ttf"].glob("*.ttf"))),
            "variable_woff": len(list(paths["release_variable_woff"].glob("*.woff"))),
            "variable_woff2": len(list(paths["release_variable_woff2"].glob("*.woff2"))),
            "static_ttf": len(list(paths["release_static_ttf"].glob("*.ttf"))),
            "static_woff": len(list(paths["release_static_woff"].glob("*.woff"))),
            "static_woff2": len(list(paths["release_static_woff2"].glob("*.woff2"))),
            "static_otf": len(list(paths["release_static_otf"].glob("*.otf"))),
        },
        "fonts": font_checks,
        "readme_mentions_legacy_name": LEGACY_NAME in readme,
        "readme_mentions_matthew_blode": "Matthew Blode" in readme,
    }
    verify_path = paths["release_metadata"] / "verify.json"
    verify_path.write_text(json.dumps(payload, indent=2))

    if missing:
        raise SystemExit(f"Missing required release files: {missing}")
    expected_counts = {
        "variable_ttf": 2,
        "variable_woff": 2,
        "variable_woff2": 2,
        "static_ttf": 8,
        "static_woff": 8,
        "static_woff2": 8,
        "static_otf": 8,
    }
    for key, expected in expected_counts.items():
        if payload["counts"][key] != expected:
            raise SystemExit(f"Unexpected release count for {key}: {payload['counts'][key]} != {expected}")
    if any(font["has_legacy_name"] for font in font_checks):
        raise SystemExit("Release fonts still contain legacy source metadata.")
    if payload["readme_mentions_legacy_name"]:
        raise SystemExit("README still mentions the legacy source name.")
    if not payload["readme_mentions_matthew_blode"]:
        raise SystemExit("README does not mention Matthew Blode.")
    return verify_path


def create_zip_archive(paths: dict[str, Path], version: str) -> Path:
    archive_path = paths["release"] / f"Glide-{version}.zip"
    if archive_path.exists():
        archive_path.unlink()
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted((paths["release"] / "fonts").rglob("*")):
            if source.is_file():
                archive.write(source, Path("Glide") / source.relative_to(paths["release"]))
        for source in sorted((paths["release"] / "proof").rglob("*")):
            if source.is_file():
                archive.write(source, Path("Glide") / source.relative_to(paths["release"]))
        for source in (
            paths["release_metadata"] / "release.json",
            paths["repo"] / "README.md",
            paths["repo"] / "version.txt",
        ):
            archive.write(source, Path("Glide") / source.name)
    return archive_path


def build_release(paths: dict[str, Path], force: bool) -> None:
    version = read_version(paths["version_file"])
    if force:
        clean_generated(paths)
    ensure_dirs(paths)
    build_workspace(paths)

    packaged_files: list[str] = []
    packaged_files.extend(
        package_variable_font(
            paths["work_output"] / "glide-cli-roman-variable.ttf",
            "glide-variable",
            {
                "ttf": paths["release_variable_ttf"],
                "woff": paths["release_variable_woff"],
                "woff2": paths["release_variable_woff2"],
            },
            italic=False,
            version=version,
        )
    )
    packaged_files.extend(
        package_variable_font(
            paths["work_output"] / "glide-cli-italic-variable.ttf",
            "glide-variable-italic",
            {
                "ttf": paths["release_variable_ttf"],
                "woff": paths["release_variable_woff"],
                "woff2": paths["release_variable_woff2"],
            },
            italic=True,
            version=version,
        )
    )
    packaged_files.extend(
        package_static_family(
            paths["work_output"] / "glide-cli-roman-variable.ttf",
            {
                "ttf": paths["release_static_ttf"],
                "woff": paths["release_static_woff"],
                "woff2": paths["release_static_woff2"],
                "otf": paths["release_static_otf"],
            },
            italic=False,
            version=version,
        )
    )
    packaged_files.extend(
        package_static_family(
            paths["work_output"] / "glide-cli-italic-variable.ttf",
            {
                "ttf": paths["release_static_ttf"],
                "woff": paths["release_static_woff"],
                "woff2": paths["release_static_woff2"],
                "otf": paths["release_static_otf"],
            },
            italic=True,
            version=version,
        )
    )
    packaged_files.append(str(write_css(paths).relative_to(paths["repo"])))
    proof_path = sync_proof(paths)
    packaged_files.append(str(proof_path.relative_to(paths["repo"])))
    write_release_metadata(paths, packaged_files, proof_path, version)
    verify_release(paths)


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    paths = release_paths(repo_root)

    if args.command == "clean":
        clean_generated(paths)
        return 0
    if args.command == "verify":
        verify_release(paths)
        return 0
    if args.command == "zip":
        verify_release(paths)
        archive = create_zip_archive(paths, read_version(paths["version_file"]))
        print(archive)
        return 0

    build_release(paths, force=args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
