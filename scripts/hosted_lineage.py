"""Verify signed native evidence and current inputs without exporting preserved originals."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = "integration/archive/"
CAPSULE = ARCHIVE + "hosted-native-attestation.json"
SIGNERS = ARCHIVE + "hosted-native-signers"
CHECKPOINT = ARCHIVE + "scientific-lineage-checkpoint_20261102.json"
CHECKPOINT_SHA = "63eaf457ae3ff03fc688f830f24ebb640f01dbbf8dc2e912887c10ec7f6e090a"
PROFILES = ARCHIVE + "hosted-verifier-profiles.json"
PROFILES_SHA = "pending-hosted-qualification"
SIGNERS_SHA = "pending-local-key-qualification"
NAMESPACE = "tobac-native-lineage"
IDENTITY = "tobac-native"


def digest(path: Path) -> str:
    """Hash actual file bytes, including the selected interpreter behind its venv link."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def checked(root: Path, name: str) -> Path:
    """Reject escapes and links before reading a declared repository input."""
    path = root / name
    if Path(name).is_absolute() or ".." in Path(name).parts or path.is_symlink():
        msg = "Unsafe hosted lineage input path"
        raise ValueError(msg)
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        msg = "Missing hosted lineage input"
        raise ValueError(msg)
    return path


def command(argv: list[str], *, data: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    """Use fixed argument arrays and suppress raw external diagnostics."""
    return subprocess.run(argv, input=data, capture_output=True, timeout=60, check=False)  # noqa: S603 -- Fixed OpenSSH tool arguments, no shell.


def runtime_profile(executable: Path | None = None) -> dict[str, Any]:
    """Identify the actual Python and signature-verifier binaries on this machine."""
    ssh = shutil.which("ssh-keygen")
    if ssh is None or sys.version_info[:3] != (3, 15, 1):
        msg = "Hosted verification requires Python 3.15.1 and OpenSSH ssh-keygen"
        raise ValueError(msg)
    return {
        "system": platform.system(),
        "machine": platform.machine(),
        "python_version": list(sys.version_info[:3]),
        "python_sha256": digest(executable or Path(sys.executable)),
        "base_python_sha256": digest(
            Path(sys.base_prefix) / ("python.exe" if os.name == "nt" else "bin/python3.15")
        ),
        "ssh_keygen_sha256": digest(Path(ssh)),
    }


def verify_signature(payload: Path, signature: Path, signers: Path) -> None:
    """Verify Ed25519 evidence with the maintained OpenSSH verifier."""
    ssh = shutil.which("ssh-keygen")
    if ssh is None:
        msg = "Missing OpenSSH signature verifier"
        raise ValueError(msg)
    result = command(
        [ssh, "-Y", "verify", "-f", str(signers), "-I", IDENTITY, "-n", NAMESPACE, "-s", str(signature)],
        data=payload.read_bytes(),
    )
    if result.returncode:
        msg = "Native evidence signature rejected"
        raise ValueError(msg)


def inventory_identity(root: Path) -> str:
    """Use the same scientific estate membership boundary as native verification."""
    names: set[str] = set()
    for pattern in ("configs/**/*", "data/**/*", "evidence/**/*", "src/**/*.py", "scripts/run_*.py"):
        names.update(
            p.relative_to(root).as_posix()
            for p in root.glob(pattern)
            if (p.is_file() or p.is_symlink()) and "__pycache__" not in p.parts and p.name != ".DS_Store"
        )
    return hashlib.sha256("\n".join(sorted(names)).encode()).hexdigest()


def qualified_profiles(root: Path) -> list[dict[str, Any]]:
    """Authenticate externally qualified runtime identities before trusting executable output."""
    path = checked(root, PROFILES)
    if digest(path) != PROFILES_SHA:
        msg = "Hosted verifier runtime profiles differ from acceptance"
        raise ValueError(msg)
    profiles: list[dict[str, Any]] = json.loads(path.read_bytes())["profiles"]
    return profiles


def authenticate(root: Path) -> dict[str, Any]:
    """Authenticate evidence, its verifier implementation and every accepted pin."""
    profiles = qualified_profiles(root)
    ssh = shutil.which("ssh-keygen")
    if ssh is None or digest(Path(ssh)) not in {p["ssh_keygen_sha256"] for p in profiles}:
        msg = "OpenSSH verifier differs from qualified binaries"
        raise ValueError(msg)
    if digest(checked(root, SIGNERS)) != SIGNERS_SHA:
        msg = "Native evidence signing authority differs from acceptance"
        raise ValueError(msg)
    payload = checked(root, CAPSULE)
    verify_signature(payload, checked(root, CAPSULE + ".sig"), checked(root, SIGNERS))
    capsule: dict[str, Any] = json.loads(payload.read_bytes())
    if capsule["schema"] != "tobac.signed-native-lineage/v1":
        msg = "Unknown native evidence schema"
        raise ValueError(msg)
    if capsule["verifier_sha256"] != digest(checked(root, "scripts/hosted_lineage.py")):
        msg = "Hosted verifier differs from the qualified implementation"
        raise ValueError(msg)
    for name, expected in capsule["pins"].items():
        if digest(checked(root, name)) != expected:
            msg = f"Stale native acceptance pin: {name}"
            raise ValueError(msg)
    if capsule["pins"].get(CHECKPOINT) != CHECKPOINT_SHA:
        msg = "Evidence does not attest the accepted native checkpoint"
        raise ValueError(msg)
    if inventory_identity(root) != capsule["inventory_sha256"]:
        msg = "Scientific inventory differs from native acceptance"
        raise ValueError(msg)
    return capsule


def verify_inputs(
    root: Path, capsule: dict[str, Any], names: list[str], manifest: Path | None = None
) -> dict[str, Any]:
    """Compare all selected inputs and object identities with native byte-verified acceptance."""
    accepted = json.loads(checked(root, CHECKPOINT).read_bytes())["runner_results"]
    if set(capsule["runners"]) != set(accepted):
        msg = "Native capsule has a missing or substituted runner"
        raise ValueError(msg)
    if manifest is not None:
        matches = [name for name, run in accepted.items() if run["manifest"] == "sha256:" + digest(manifest)]
        if len(matches) != 1 or (names and names != matches):
            msg = "Manifest does not belong to the requested accepted runner"
            raise ValueError(msg)
        names = matches
    selected = names or sorted(accepted)
    if len(set(selected)) != len(selected) or set(selected) - accepted.keys():
        msg = "Unknown or duplicate runner requested"
        raise ValueError(msg)
    verified = {}
    for name in selected:
        expected = accepted[name]
        proof = capsule["runners"][name]
        for field in (
            "attempt_id",
            "manifest",
            "receipt",
            "transformation",
            "validation",
            "output_inventory",
            "executed_input_objects",
            "originals",
            "artifacts",
        ):
            if proof[field] != expected[field]:
                msg = f"{name}: substituted accepted native {field}"
                raise ValueError(msg)
        for path, object_id in proof["executed_input_objects"].items():
            if "sha256:" + digest(checked(root, path)) != object_id:
                msg = f"{name}: stale scientific input: {path}"
                raise ValueError(msg)
        verified[name] = {
            "attempt_id": proof["attempt_id"],
            "manifest": proof["manifest"],
            "verified_inputs": len(proof["executed_input_objects"]),
            "verified_outputs": len(proof["artifacts"]),
        }
    return {
        "success": True,
        "qualified": True,
        "execution_mode": "qualified_attested_inputs",
        "scope": "signed local native byte verification and hosted current-input verification",
        "checkpoint_sha256": CHECKPOINT_SHA,
        "runners": verified,
        "native_lineage_qualified": False,
        "scientific_qualification": False,
    }


def verify(root: Path, names: list[str], manifest: Path | None = None) -> dict[str, Any]:
    """Require an authenticated capsule and an actually qualified repo-local runtime."""
    if not Path(sys.prefix).resolve().is_relative_to(root.resolve()):
        msg = "Hosted verifier requires a repo-local environment"
        raise ValueError(msg)
    capsule = authenticate(root)
    if runtime_profile() not in qualified_profiles(root):
        msg = "Hosted verifier runtime differs from qualified profiles"
        raise ValueError(msg)
    return verify_inputs(root, capsule, names, manifest)


def probe() -> dict[str, Any]:
    """Exercise real signing, verification and rejection before qualifying a runtime."""
    ssh = shutil.which("ssh-keygen")
    if ssh is None:
        msg = "Missing OpenSSH"
        raise ValueError(msg)
    with tempfile.TemporaryDirectory() as folder:
        base = Path(folder)
        key, payload, signers = base / "key", base / "payload", base / "signers"
        if command([ssh, "-t", "ed25519", "-N", "", "-f", str(key)]).returncode:
            msg = "Unable to create the synthetic qualification key"
            raise ValueError(msg)
        payload.write_bytes(b"synthetic signature qualification\n")
        signers.write_text(IDENTITY + " " + Path(str(key) + ".pub").read_text(encoding="utf-8"))
        if command([ssh, "-Y", "sign", "-f", str(key), "-n", NAMESPACE, str(payload)]).returncode:
            msg = "Synthetic signature creation failed"
            raise ValueError(msg)
        verify_signature(payload, Path(str(payload) + ".sig"), signers)
        payload.write_bytes(b"tampered qualification\n")
        try:
            verify_signature(payload, Path(str(payload) + ".sig"), signers)
        except ValueError:
            return {
                "profile": runtime_profile(),
                "valid_signature_passed": True,
                "tampered_signature_rejected": True,
            }
        msg = "Tampered signature was accepted"
        raise ValueError(msg)


def main() -> None:
    """Run the explicit hosted route or its isolated runtime qualification."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--probe", action="store_true")
    mode.add_argument("--configure", action="store_true")
    parser.add_argument("--runner", action="append", default=[])
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        receipt = probe() if args.probe else verify(ROOT, args.runner, args.manifest)
        if args.configure:
            with Path(os.environ["GITHUB_ENV"]).open("a", encoding="utf-8") as stream:
                stream.write(f"TOBAC_LINEAGE_ROUTE=attested\nTOBAC_LINEAGE_PYTHON={sys.executable}\n")
    except Exception as exc:  # noqa: BLE001 -- Qualification failures must remain structured and fail closed.
        receipt = {"success": False, "qualified": False, "error": str(exc)}
    print(json.dumps(receipt, sort_keys=True))  # noqa: T201 -- Machine-readable qualification receipt.
    raise SystemExit(2 if receipt.get("success") is False else 0)


if __name__ == "__main__":
    main()
