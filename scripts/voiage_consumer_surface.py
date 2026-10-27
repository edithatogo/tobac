"""Inventory the consumer boundary without importing or executing upstream code."""

import ast
import hashlib
import json
from pathlib import Path

LOOKUP_ARGUMENTS = 2
REMOVED = frozenset({"dataset", "to_dataset", "from_dataset"})


def inventory(root: Path) -> dict[str, object]:
    """Hash maintained Python and reject references to the removed container surface."""
    sources = sorted(
        path
        for directory in ("src/tobac", "scripts", "tests/engineering")
        for path in (root / directory).rglob("*.py")
    )
    if not sources:
        msg = "No consumer Python sources found"
        raise ValueError(msg)
    hashes: dict[str, str] = {}
    imports: list[dict[str, object]] = []
    dynamic_imports: list[dict[str, object]] = []
    for path in sources:
        relative = path.relative_to(root).as_posix()
        content = path.read_bytes()
        hashes[relative] = hashlib.sha256(content).hexdigest()
        for node in ast.walk(ast.parse(content, filename=relative)):
            if isinstance(node, ast.Attribute) and node.attr in REMOVED:
                msg = f"Removed container symbol {node.attr} at {relative}:{node.lineno}"
                raise ValueError(msg)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in {"getattr", "hasattr"}
                and len(node.args) >= LOOKUP_ARGUMENTS
                and isinstance(node.args[1], ast.Constant)
                and node.args[1].value in REMOVED
            ):
                msg = f"Removed container lookup at {relative}:{node.lineno}"
                raise ValueError(msg)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "import_module"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
                and (node.args[0].value == "voiage" or node.args[0].value.startswith("voiage."))
            ):
                dynamic_imports.append({"path": relative, "line": node.lineno, "module": node.args[0].value})
            if isinstance(node, ast.ImportFrom) and (
                node.module == "voiage" or (node.module or "").startswith("voiage.")
            ):
                for alias in node.names:
                    if alias.name in REMOVED:
                        msg = f"Removed Voiage import {alias.name} at {relative}:{node.lineno}"
                        raise ValueError(msg)
                imports.append(
                    {
                        "path": relative,
                        "line": node.lineno,
                        "module": node.module,
                        "names": [alias.name for alias in node.names],
                    }
                )
    return {
        "schema": "tobac.voiage-consumer-surface.v1",
        "files": hashes,
        "voiage_imports": imports,
        "literal_dynamic_imports": dynamic_imports,
        "removed_symbol_references": 0,
        "scope": "Static consumer surface only; not installed wheel, dependency or scientific qualification",
    }


if __name__ == "__main__":
    print(json.dumps(inventory(Path(__file__).resolve().parents[1]), indent=2))  # noqa: T201 -- CLI inventory output.
