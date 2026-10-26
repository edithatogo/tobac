"""Verify extracted-core provenance and saved numerical-input/output hashes."""

import ast
import hashlib
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "integration/baseline.json").read_text())
maintenance = json.loads((root / "integration/core_maintenance_20261026.json").read_text())
original = root / maintenance["original_source"]
if hashlib.sha256(original.read_bytes()).hexdigest() != maintenance["original_sha256"]:
    msg = "Changed original extraction snapshot"
    raise SystemExit(msg)
text = original.read_text()
lines = text.splitlines(keepends=True)
nodes = {n.name: n for n in ast.parse(text).body if hasattr(n, "name")}


# Named bounds preserve the existing scientific/data contract.
CAST_ARGUMENT_COUNT = 2


class Annotations(ast.NodeTransformer):
    """Normalise static type annotations while retaining fields, defaults and bodies."""

    _function_depth = 0

    def visit_Name(self, node: ast.Name) -> ast.AST:
        """Expand only the explicitly approved immutable literal bindings."""
        if isinstance(node.ctx, ast.Load) and node.id in maintenance["constant_bindings"]:
            return ast.Constant(value=maintenance["constant_bindings"][node.id])
        return node

    def visit_Call(self, node: ast.Call) -> ast.AST:
        # typing.cast returns its value unchanged; it is not a numeric conversion.
        """Remove only static cast wrappers from the numerical comparison tree."""
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "cast"
            and len(node.args) == CAST_ARGUMENT_COUNT
        ):
            return self.visit(node.args[1])
        return super().generic_visit(node)

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """Remove parameter annotations from the numerical comparison tree."""
        node.annotation = None
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Normalize a function signature while retaining its executable body."""
        node.returns = None
        self._function_depth += 1
        super().generic_visit(node)
        self._function_depth -= 1
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AST:
        """Normalize static annotations while preserving dataclass fields and defaults."""
        if self._function_depth and node.value is not None:
            return ast.Assign(targets=[node.target], value=self.visit(node.value))
        # ClassVar/InitVar alter dataclass fields and must never be normalised away.
        if not any(
            isinstance(n, ast.Name) and n.id in {"ClassVar", "InitVar"} for n in ast.walk(node.annotation)
        ):
            node.annotation = ast.Name(id="_annotation", ctx=ast.Load())
        super().generic_visit(node)
        return node


active_tree = ast.parse((root / manifest["published_core"]).read_text())
for name, value in maintenance["constant_bindings"].items():
    assignments = [
        n
        for n in ast.walk(active_tree)
        if isinstance(n, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == name for target in n.targets)
    ]
    if len(assignments) != 1 or ast.literal_eval(assignments[0].value) != value:
        raise SystemExit("Changed core literal binding: " + name)
cast_imports = [
    n
    for n in active_tree.body
    if isinstance(n, ast.ImportFrom)
    and n.module == "typing"
    and any(a.name == "cast" and a.asname is None for a in n.names)
]
cast_rebindings = [
    n
    for n in ast.walk(active_tree)
    if (isinstance(n, ast.Name) and n.id == "cast" and isinstance(n.ctx, ast.Store))
    or (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == "cast")
    or (isinstance(n, ast.arg) and n.arg == "cast")
]
if len(cast_imports) != 1 or cast_rebindings:
    message = "Changed typing.cast binding"
    raise SystemExit(message)
active = {n.name: n for n in active_tree.body if hasattr(n, "name")}
for item in manifest["extracted_definitions"]:
    n = nodes[item["name"]]
    start = min([n.lineno] + [d.lineno for d in getattr(n, "decorator_list", [])]) - 1
    actual = hashlib.sha256("".join(lines[start : n.end_lineno]).encode()).hexdigest()
    if actual != item["sha256_of_extracted_source"]:
        raise SystemExit("Changed inherited definition: " + item["name"])
    if ast.dump(Annotations().visit(n)) != ast.dump(Annotations().visit(active[item["name"]])):
        raise SystemExit("Changed inherited numerical definition: " + item["name"])
if len(sys.argv) > 1:
    directory = root / sys.argv[1]
    run = json.loads((directory / "manifest.json").read_text())
    for path, digest in run["inputs"].items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != digest:
            raise SystemExit("Changed input: " + path)
    for path, digest in run["outputs"].items():
        if hashlib.sha256((directory / path).read_bytes()).hexdigest() != digest:
            raise SystemExit("Changed output: " + path)
print(  # noqa: T201  # CLI emits the requested structured result on stdout.
    json.dumps(
        {
            "verified_core_definitions": len(manifest["extracted_definitions"]),
            "run_verified": len(sys.argv) > 1,
        }
    )
)
