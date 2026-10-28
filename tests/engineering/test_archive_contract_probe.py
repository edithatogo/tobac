"""Frozen-source loading tests; tiny Git fixtures are not archive capability evidence."""

import importlib.util
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def module():
    """Load the diagnostic helper without requiring a producer checkout."""
    spec = importlib.util.spec_from_file_location("probe_archive", ROOT / "scripts/probe_archive_contract.py")
    assert spec is not None
    assert spec.loader is not None
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def test_mutable_revision_is_rejected_before_git_execution(tmp_path) -> None:
    with pytest.raises(ValueError, match="immutable commit hash"):
        module().frozen_bytes(tmp_path, "main", "src/archive_govt_nz/provenance.py")


def test_native_probe_preserves_existing_receipt(tmp_path, monkeypatch) -> None:
    output = tmp_path / "receipt.json"
    output.write_text("retained evidence")
    monkeypatch.setattr(
        "sys.argv",
        [
            "probe_archive_contract.py",
            "--repository",
            str(tmp_path),
            "--revision",
            "a" * 40,
            "--out",
            str(output),
        ],
    )
    with pytest.raises(SystemExit, match="2"):
        module().main()
    assert output.read_text() == "retained evidence"


def test_committed_bytes_are_used_when_producer_worktree_is_dirty(tmp_path) -> None:
    executable = shutil.which("git")
    assert executable is not None
    path = tmp_path / "fixture.py"
    path.write_bytes(b"committed synthetic bytes\n")
    for arguments in (
        ["init", "--quiet"],
        ["add", "fixture.py"],
        ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"],
    ):
        subprocess.run(  # noqa: S603 -- Resolved Git and fixed fixture argv; isolated temporary repository.
            [executable, *arguments], cwd=tmp_path, check=True, capture_output=True, timeout=30
        )
    revision = subprocess.check_output(  # noqa: S603 -- Resolved Git and fixed read-only argv.
        [executable, "rev-parse", "HEAD"], cwd=tmp_path, text=True, timeout=30
    ).strip()
    path.write_bytes(b"uncommitted synthetic changes\n")
    assert module().frozen_bytes(tmp_path, revision, "fixture.py") == b"committed synthetic bytes\n"
    assert path.read_bytes() == b"uncommitted synthetic changes\n"
