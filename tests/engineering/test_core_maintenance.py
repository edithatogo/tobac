"""Formatting/typing may change; the retained extraction and numerical AST may not."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def snapshot(tmp_path):
    for name in [
        "scripts/verify.py",
        "integration/baseline.json",
        "integration/core_maintenance_20261026.json",
        "evidence/core_extraction_20261024.py",
        "src/tobac/_core.py",
    ]:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return tmp_path


def verify(root):
    return subprocess.run(  # noqa: S603 -- Fixed local interpreter/verifier argv; no shell.
        [sys.executable, str(root / "scripts/verify.py")], capture_output=True, text=True, check=False
    )


def test_equivalent_formatting_and_annotation_pass(tmp_path) -> None:
    root = snapshot(tmp_path)
    path = root / "src/tobac/_core.py"
    path.write_text(path.read_text().replace("value: float", "value: int | float") + "\n")
    result = verify(root)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("change", ["formula", "original", "default", "constant", "cast", "field"])
def test_numerical_or_original_source_change_fails(tmp_path, change) -> None:
    root = snapshot(tmp_path)
    path = root / ("evidence/core_extraction_20261024.py" if change == "original" else "src/tobac/_core.py")
    text = path.read_text()
    if change == "formula":
        text = text.replace("1_000_000.0", "1_000_001.0")
    elif change == "default":
        text = text.replace("= 0.9", "= 0.8")
    elif change == "constant":
        text = text.replace("MATRIX_NDIM = 2", "MATRIX_NDIM = 3")
    elif change == "cast":
        text += "\ncast = lambda annotation, value: value * 2\n"
    elif change == "field":
        text = text.replace("prior_weights: FloatArray | None", "prior_weights: ClassVar[FloatArray | None]")
    else:
        text += "# changed historical bytes\n"
    path.write_text(text)
    result = verify(root)
    assert result.returncode != 0
    assert "Changed" in result.stderr
