from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parent.parent / "scripts" / "promote-versioned-release.py"
)
SPEC = importlib.util.spec_from_file_location("promote_versioned_release", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
REAL_BUILD_DESKTOP_BUNDLE = MODULE._build_desktop_bundle


@pytest.fixture(autouse=True)
def _stub_desktop_bundle_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    def build(public_new: Path, fonts_new: Path, _contract: dict) -> None:
        static = fonts_new / "static"
        static.mkdir(exist_ok=True)
        for weight in MODULE.WEIGHTS:
            (static / f"Glide-{weight}.ttf").write_bytes(
                f"desktop-{weight}".encode()
            )
            (static / f"Glide-{weight}Italic.ttf").write_bytes(
                f"desktop-{weight}-italic".encode()
            )
        (public_new / "glide.zip").write_bytes(b"desktop-bundle")

    monkeypatch.setattr(MODULE, "_build_desktop_bundle", build)


def _fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(MODULE, "ROOT", tmp_path)
    public = tmp_path / "apps/web/public"
    fonts = tmp_path / "fonts"
    source = public / "4.0.0"
    source.mkdir(parents=True)
    fonts.mkdir()
    (fonts / "web").mkdir()
    (public / "3.1.0").mkdir()
    (public / "3.002").mkdir()
    (public / "keep.png").write_bytes(b"keep")
    (fonts / "keep.txt").write_bytes(b"keep")
    for name in MODULE.ROOT_FILES:
        (source / name).write_bytes(("new-" + name).encode())
    for relative in sorted(MODULE.EXPECTED - set(MODULE.ROOT_FILES)):
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(relative.encode())
    artifacts = []
    for path in sorted(item for item in source.rglob("*") if item.is_file()):
        artifacts.append(
            {
                "path": path.relative_to(source).as_posix(),
                "size": path.stat().st_size,
                "sha256": MODULE._sha256(path),
            }
        )
    manifest = {
        "kind": "glide-4-production-candidate",
        "version": "4.0.0",
        "fontRevision": "4.000",
        "authority": MODULE.AUTHORITY,
        "qualityAssurance": {"ots": {"status": "pass"}, "fontbakery": {"FAIL": 0}},
        "artifacts": artifacts,
    }
    manifest["manifestSha256"] = MODULE.hashlib.sha256(
        (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    (source / MODULE.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    return source


def test_promote_replaces_aliases_and_preserves_unrelated_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _fixture(tmp_path, monkeypatch)
    MODULE.promote(source)
    assert (
        tmp_path / "apps/web/public/glide-variable.ttf"
    ).read_bytes() == b"new-glide-variable.ttf"
    assert (
        tmp_path / "fonts/web/glide-variable.woff2"
    ).read_bytes() == b"new-glide-variable.woff2"
    assert len(list((tmp_path / "fonts/static").glob("*.ttf"))) == 20
    assert (tmp_path / "apps/web/public/glide.zip").read_bytes() == b"desktop-bundle"
    assert (tmp_path / "fonts/static/Glide-Thin.ttf").read_bytes() == b"desktop-Thin"
    assert (tmp_path / "apps/web/public/3.1.0").is_dir()
    assert (tmp_path / "apps/web/public/3.002").is_dir()
    assert (tmp_path / "apps/web/public/keep.png").read_bytes() == b"keep"


def test_promote_rejects_non_versioned_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fixture(tmp_path, monkeypatch)
    other = tmp_path / "other"
    other.mkdir()
    with pytest.raises(ValueError, match="source must be immutable"):
        MODULE.promote(other)


def test_committed_journal_write_failure_rolls_back_both_alias_trees(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _fixture(tmp_path, monkeypatch)
    original = MODULE._write_journal

    def fail_committed(path: Path, phase: str) -> None:
        if phase == "committed":
            raise OSError("fault")
        original(path, phase)

    monkeypatch.setattr(MODULE, "_write_journal", fail_committed)
    with pytest.raises(OSError, match="fault"):
        MODULE.promote(source)
    assert not (tmp_path / "apps/web/public/glide-variable.ttf").exists()
    assert not (tmp_path / "fonts/glide-variable.ttf").exists()
    assert not (tmp_path / MODULE.JOURNAL).exists()


def test_committed_cleanup_keeps_journal_until_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _fixture(tmp_path, monkeypatch)
    real_rmtree = MODULE.shutil.rmtree

    def retain_backup(path: Path, *args: object, **kwargs: object) -> None:
        if Path(path).name.endswith("rollback"):
            return
        real_rmtree(path, *args, **kwargs)

    monkeypatch.setattr(MODULE.shutil, "rmtree", retain_backup)
    MODULE.promote(source)
    journal = tmp_path / MODULE.JOURNAL
    assert journal.read_text(encoding="utf-8").strip() == "committed"
    monkeypatch.setattr(MODULE.shutil, "rmtree", real_rmtree)
    MODULE._recover(
        tmp_path / "apps/web/public",
        tmp_path / "fonts",
        tmp_path / ".glide-public-rollback",
        tmp_path / ".glide-fonts-rollback",
        journal,
    )
    assert not journal.exists()


def test_hotfix_contract_promotes_401_and_protects_400(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(MODULE, "ROOT", tmp_path)
    public = tmp_path / "apps/web/public"
    fonts = tmp_path / "fonts"
    source = public / "4.0.1"
    source.mkdir(parents=True)
    (fonts / "web").mkdir(parents=True)
    for version in ("3.1.0", "3.002", "4.0.0"):
        directory = public / version
        directory.mkdir()
        (directory / "pinned.bin").write_bytes(version.encode())
    for name in MODULE._root_files("4.0.1"):
        (source / name).write_bytes(("hotfix-" + name).encode())
    for relative in sorted(
        MODULE._expected("4.0.1") - set(MODULE._root_files("4.0.1"))
    ):
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(relative.encode())
    authority = {
        "path": "reports/glide-4-authority-hotfix/frozen.json",
        "sha256": "a" * 64,
    }
    artifacts = [
        {
            "path": path.relative_to(source).as_posix(),
            "size": path.stat().st_size,
            "sha256": MODULE._sha256(path),
        }
        for path in sorted(source.rglob("*"))
        if path.is_file()
    ]
    manifest = {
        "kind": "glide-4-production-candidate",
        "version": "4.0.1",
        "fontRevision": "4.001",
        "authority": authority,
        "qualityAssurance": {"ots": {"status": "pass"}, "fontbakery": {"FAIL": 0}},
        "artifacts": artifacts,
    }
    manifest["manifestSha256"] = MODULE.hashlib.sha256(
        (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    (source / MODULE.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    contract = {
        "schemaVersion": 1,
        "kind": "glide-public-promotion",
        "semanticVersion": "4.0.1",
        "fontRevision": "4.001",
        "authority": authority,
        "protectedTrees": {
            f"apps/web/public/{version}": MODULE._tree_digest(
                f"apps/web/public/{version}"
            )
            for version in ("3.1.0", "3.002", "4.0.0")
        },
    }

    MODULE.promote(source, contract)

    assert (public / "glide-variable.ttf").read_bytes() == b"hotfix-glide-variable.ttf"
    assert (public / "4.0.0/pinned.bin").read_bytes() == b"4.0.0"
    (public / "4.0.0/pinned.bin").write_bytes(b"changed")
    with pytest.raises(ValueError, match="protected release tree changed"):
        MODULE.promote(source, contract)


def test_402_contract_requires_the_401_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(MODULE, "ROOT", tmp_path)
    contract = {
        "schemaVersion": 1,
        "kind": "glide-public-promotion",
        "semanticVersion": "4.0.2",
        "fontRevision": "4.002",
        "authority": {"path": "reports/authority.json", "sha256": "a" * 64},
        "desktopBundleBuilderSha256": "b" * 64,
        "protectedTrees": {
            "apps/web/public/3.1.0": "c" * 64,
            "apps/web/public/3.002": "d" * 64,
            "apps/web/public/4.0.0": "e" * 64,
        },
    }
    contract_root = MODULE.ROOT / "release-contracts"
    contract_root.mkdir()
    path = contract_root / "glide-4.0.2.json"
    path.write_text(json.dumps(contract), encoding="utf-8")
    with pytest.raises(ValueError, match="4.0.2 promotion must protect"):
        MODULE._load_contract(path)


def test_rejected_406_contract_is_revoked() -> None:
    contract = SCRIPT.parent.parent / "release-contracts" / "glide-4.0.6.json"
    with pytest.raises(ValueError, match="promotion contract is revoked: 4.0.6"):
        MODULE._load_contract(contract)


def test_410_contract_protects_every_prior_release() -> None:
    contract = SCRIPT.parent.parent / "release-contracts" / "glide-4.0.10.json"
    loaded = MODULE._load_contract(contract)

    assert loaded["authority"] == {
        "path": (
            "reports/glide-4-authority-4.0.10-curve-continuity/"
            "glide-4-six-master-authority-8378e3b6a205d3e8.json"
        ),
        "sha256": (
            "8378e3b6a205d3e8887149597c29121d4f011e320be5c276c2ac55ec4b26fbff"
        ),
    }
    assert set(loaded["protectedTrees"]) == {
        "apps/web/public/3.1.0",
        "apps/web/public/3.002",
        *(f"apps/web/public/4.0.{patch}" for patch in range(10)),
    }
    for relative, digest in loaded["protectedTrees"].items():
        assert MODULE._tree_digest(relative) == digest


def test_411_contract_protects_every_prior_release() -> None:
    contract = SCRIPT.parent.parent / "release-contracts" / "glide-4.0.11.json"
    loaded = MODULE._load_contract(contract)

    assert loaded["authority"] == {
        "path": (
            "reports/glide-4-authority-4.0.11-u2787/"
            "glide-4-six-master-authority-30a2e162234da823.json"
        ),
        "sha256": (
            "30a2e162234da8235d7d4d1f2d602e23910323adc0775b44d572d9ade7b8f189"
        ),
    }
    assert set(loaded["protectedTrees"]) == {
        "apps/web/public/3.1.0",
        "apps/web/public/3.002",
        *(f"apps/web/public/4.0.{patch}" for patch in range(11)),
    }
    for relative, digest in loaded["protectedTrees"].items():
        assert MODULE._tree_digest(relative) == digest


def test_412_contract_protects_every_prior_release() -> None:
    contract = SCRIPT.parent.parent / "release-contracts" / "glide-4.0.12.json"
    loaded = MODULE._load_contract(contract)

    assert loaded["authority"] == {
        "path": (
            "reports/glide-4-authority-4.0.12-u2787/"
            "glide-4-six-master-authority-26f48ba1d86669b2.json"
        ),
        "sha256": (
            "26f48ba1d86669b2128180a21ff3cca07012fcb52ac29bf63ad59dc2d50030c1"
        ),
    }
    assert set(loaded["protectedTrees"]) == {
        "apps/web/public/3.1.0",
        "apps/web/public/3.002",
        *(f"apps/web/public/4.0.{patch}" for patch in range(12)),
    }
    for relative, digest in loaded["protectedTrees"].items():
        assert MODULE._tree_digest(relative) == digest


def test_real_desktop_bundle_builder_is_hash_pinned_and_reproducible(
    tmp_path: Path,
) -> None:
    public_new = tmp_path / "public"
    fonts_new = tmp_path / "fonts"
    public_new.mkdir()
    MODULE.shutil.copytree(SCRIPT.parent.parent / "fonts", fonts_new)

    contract = MODULE._load_contract(
        SCRIPT.parent.parent / "release-contracts" / "glide-4.0.12.json"
    )
    REAL_BUILD_DESKTOP_BUNDLE(public_new, fonts_new, contract)

    assert (public_new / "glide.zip").is_file()
    assert len(list((fonts_new / "static").glob("*.ttf"))) == 20
    changed = dict(contract)
    changed["desktopBundleBuilderSha256"] = "0" * 64
    with pytest.raises(ValueError, match="builder is missing or changed"):
        REAL_BUILD_DESKTOP_BUNDLE(public_new, fonts_new, changed)
