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
