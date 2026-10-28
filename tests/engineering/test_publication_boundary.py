"""Publication guards reject staged copies, archives and replay checkouts before export."""

import gzip
import hashlib
import io
import json
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import publication_boundary as boundary


def run_git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])  # noqa: S603, S607 -- Fixed fixture Git argv.


@pytest.fixture
def repository(tmp_path):
    run_git(tmp_path, "init", "-q")
    run_git(tmp_path, "config", "user.name", "Fixture")
    run_git(tmp_path, "config", "user.email", "fixture@example.invalid")
    (tmp_path / "engineering").mkdir()
    (tmp_path / "public.json").write_text("{}\n")
    data = {
        "public_paths": ["engineering/publication-policy.json", "public.json"],
        "local_documents": {"docs/manuscript.md": hashlib.sha256(b"private draft").hexdigest()},
        "legacy_baseline": "unused",
    }
    (tmp_path / boundary.POLICY).write_text(json.dumps(data))
    run_git(tmp_path, "add", ".")
    run_git(tmp_path, "commit", "-qm", "fixture")
    return tmp_path


def test_index_reads_staged_bytes_not_clean_worktree(repository) -> None:
    (repository / "public.json").write_bytes(b"private draft")
    run_git(repository, "add", "public.json")
    (repository / "public.json").write_text("{}\n")
    with pytest.raises(ValueError, match="Known local document"):
        boundary.validate_tree(repository)


def test_forced_unknown_file_rejected(repository) -> None:
    (repository / "renamed.md").write_text("new manuscript")
    run_git(repository, "add", "-f", "renamed.md")
    with pytest.raises(ValueError, match="Unreviewed path"):
        boundary.validate_tree(repository)


def test_clean_tree_and_commit(repository) -> None:
    assert boundary.validate_tree(repository) == 2
    assert boundary.validate_tree(repository, "HEAD") == 2


def archive_bytes(data):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("renamed.json", data)
    return stream.getvalue()


def test_nested_renamed_document_rejected(repository) -> None:
    with pytest.raises(ValueError, match="Known local document"):
        boundary.inspect_bytes(
            archive_bytes(archive_bytes(b"private draft")), boundary.load_policy(repository)
        )


def test_export_excludes_checkout_context_and_prose(repository, tmp_path) -> None:
    source = tmp_path / "outputs"
    for name in ["source/public.json", "context/context.json", "paper.md", "real.csv"]:
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("public,number\nvalue,1\n")
    out = tmp_path / "exports"
    assert boundary.stage_exports(repository, source, out) == 1
    assert [p.name for p in out.iterdir()] == ["real.csv"]


def test_export_failure_leaves_no_destination(repository, tmp_path) -> None:
    source = tmp_path / "outputs"
    source.mkdir()
    (source / "copy.json").write_bytes(b"private draft")
    out = tmp_path / "exports"
    with pytest.raises(ValueError, match="Known local document"):
        boundary.stage_exports(repository, source, out)
    assert not out.exists()


def test_export_symlink_rejected(repository, tmp_path) -> None:
    source = tmp_path / "outputs"
    source.mkdir()
    (source / "link.json").symlink_to(repository / "public.json")
    with pytest.raises(ValueError, match="Symlink"):
        boundary.stage_exports(repository, source, tmp_path / "exports")


def test_archive_traversal_rejected(repository) -> None:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("../escape.json", "{}")
    with pytest.raises(ValueError, match="Unsafe publication path"):
        boundary.inspect_bytes(stream.getvalue(), boundary.load_policy(repository))


def test_intermediate_outgoing_copy_rejected_even_when_tip_is_clean(repository) -> None:
    baseline = run_git(repository, "rev-parse", "HEAD").decode().strip()
    policy_path = repository / boundary.POLICY
    policy = json.loads(policy_path.read_text())
    policy["legacy_baseline"] = baseline
    policy_path.write_text(json.dumps(policy))
    (repository / "public.json").write_bytes(b"private draft")
    run_git(repository, "add", ".")
    run_git(repository, "commit", "-qm", "unsafe intermediate")
    (repository / "public.json").write_text("{}\n")
    run_git(repository, "add", ".")
    run_git(repository, "commit", "-qm", "clean tip")
    with pytest.raises(ValueError, match="Known local document"):
        boundary.validate_outgoing(repository, ["HEAD"])


def test_staged_policy_divergence_rejected(repository) -> None:
    policy_path = repository / boundary.POLICY
    policy_path.write_text(policy_path.read_text() + "\n")
    with pytest.raises(ValueError, match="Staged publication policy"):
        boundary.validate_tree(repository)


def test_missing_export_scanner_removes_staging(repository, tmp_path) -> None:
    out = tmp_path / "exports"
    out.mkdir()
    (out / "safe.csv").write_text("x\n1\n")
    with pytest.raises(FileNotFoundError):
        boundary.scan_export(repository, out)
    assert not out.exists()


def test_edited_private_path_beneath_archive_prefix_rejected(repository) -> None:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("package-v1/docs/manuscript.md", "edited manuscript")
    with pytest.raises(ValueError, match="Disallowed archive member"):
        boundary.inspect_bytes(stream.getvalue(), boundary.load_policy(repository))


def test_gzip_expansion_budget_applies_before_tar_header_allocation(repository, monkeypatch) -> None:
    monkeypatch.setattr(boundary, "MAX_ARCHIVE_BYTES", 128)
    with pytest.raises(ValueError, match="Archive expansion budget"):
        boundary.inspect_bytes(gzip.compress(b"x" * 1024), boundary.load_policy(repository))


def test_safe_package_tar_gzip_is_inspected(repository) -> None:
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        member = tarfile.TarInfo("package/README.md")
        member.size = 2
        archive.addfile(member, io.BytesIO(b"ok"))
    boundary.inspect_bytes(stream.getvalue(), boundary.load_policy(repository))
